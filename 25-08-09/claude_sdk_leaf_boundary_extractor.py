#!/usr/bin/env python3
"""
Claude Code SDK 기반 리프 노드 경계 텍스트 추출기

이 스크립트는 리프 노드 JSON 파일과 마크다운 원문을 입력받아,
각 리프 노드 섹션의 시작과 끝 부분에서 지정된 길이의 텍스트를 추출합니다.

요구사항:
- Python 3.10+
- Node.js
- Claude Code: npm install -g @anthropic-ai/claude-code
- Python 패키지: pip install claude-code-sdk

사용법:
python claude_sdk_leaf_boundary_extractor.py [leaf_nodes_json] [chapter_markdown] [output_json]
"""

import json
import asyncio
import sys
import re
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
from claude_code_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError


class ClaudeSDKLeafBoundaryExtractor:
    """Claude Code SDK를 활용한 리프 노드 경계 텍스트 추출기"""
    
    def __init__(self, extract_length: int = 200, debug: bool = False):
        """
        초기화
        
        Args:
            extract_length: 시작/끝에서 추출할 텍스트 길이 (기본값: 200자)
            debug: 디버그 모드 활성화
        """
        self.extract_length = extract_length
        self.debug = debug
        self.start_time = time.time()
        self.stats = {
            'processed_nodes': 0,
            'successful_nodes': 0,
            'failed_nodes': 0,
            'claude_api_calls': 0,
            'fallback_searches': 0,
            'total_processing_time': 0,
            'errors': []
        }
        
        # 로깅 설정
        self._setup_logging()
        
        self.options = ClaudeCodeOptions(
            system_prompt=(
                "당신은 텍스트 분석 전문가입니다. "
                "주어진 마크다운 텍스트에서 특정 섹션의 시작과 끝 위치를 정확히 찾아주세요. "
                "섹션 제목은 #, ##, ### 등의 헤더나 제목 텍스트로 시작할 수 있습니다."
            ),
            max_turns=2
        )
        
        self.logger.info(f"🚀 추출기 초기화 완료 - 추출 길이: {extract_length}자, 디버그: {debug}")
    
    def _setup_logging(self):
        """로깅 설정"""
        # 로그 파일명에 타임스탬프 포함
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/logs/extractor_{timestamp}.log"
        
        # 로그 디렉토리 생성
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # 로거 설정
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # 핸들러 설정 (파일과 콘솔)
        if not self.logger.handlers:
            # 파일 핸들러
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # 콘솔 핸들러
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 포매터 설정
            detailed_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
            )
            simple_formatter = logging.Formatter('%(levelname)s - %(message)s')
            
            file_handler.setFormatter(detailed_formatter)
            console_handler.setFormatter(simple_formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        print(f"📋 로그 파일: {log_file}")
    
    def _log_progress(self, current: int, total: int, node_title: str):
        """진행 상황 로깅"""
        percentage = (current / total) * 100
        elapsed = time.time() - self.start_time
        eta = (elapsed / current) * (total - current) if current > 0 else 0
        
        self.logger.info(
            f"진행률: {percentage:.1f}% ({current}/{total}) | "
            f"경과: {elapsed:.1f}s | 예상 완료: {eta:.1f}s | "
            f"현재: {node_title}"
        )
    
    def _update_stats(self, success: bool, error: str = None):
        """통계 업데이트"""
        self.stats['processed_nodes'] += 1
        if success:
            self.stats['successful_nodes'] += 1
        else:
            self.stats['failed_nodes'] += 1
            if error:
                self.stats['errors'].append({
                    'timestamp': datetime.now().isoformat(),
                    'error': error,
                    'node_count': self.stats['processed_nodes']
                })
    
    def _log_stats(self):
        """현재 통계 로깅"""
        self.logger.info(
            f"📊 현재 통계 - 성공: {self.stats['successful_nodes']}, "
            f"실패: {self.stats['failed_nodes']}, "
            f"Claude API 호출: {self.stats['claude_api_calls']}, "
            f"폴백 검색: {self.stats['fallback_searches']}"
        )
    
    async def load_files(self, leaf_nodes_path: str, chapter_path: str) -> Tuple[List[Dict], str]:
        """
        리프 노드 JSON 파일과 챕터 마크다운 파일을 로드합니다.
        
        Args:
            leaf_nodes_path: 리프 노드 JSON 파일 경로
            chapter_path: 챕터 마크다운 파일 경로
            
        Returns:
            tuple: (리프 노드 리스트, 챕터 텍스트)
        """
        try:
            # 리프 노드 JSON 로드
            with open(leaf_nodes_path, 'r', encoding='utf-8') as f:
                all_nodes = json.load(f)
            
            # 7장 관련 노드만 필터링 (id 66-72)
            chapter7_nodes = [
                node for node in all_nodes 
                if isinstance(node.get('id'), int) and 66 <= node['id'] <= 72
            ]
            
            # 챕터 텍스트 로드
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_text = f.read()
            
            print(f"✓ 리프 노드 로드 완료: {len(all_nodes)}개 (7장: {len(chapter7_nodes)}개)")
            print(f"✓ 챕터 텍스트 로드 완료: {len(chapter_text):,}자")
            
            return chapter7_nodes, chapter_text
            
        except FileNotFoundError as e:
            print(f"❌ 파일을 찾을 수 없습니다: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 오류: {e}")
            raise
    
    async def find_section_boundaries_with_claude(self, chapter_text: str, section_title: str) -> Tuple[int, int]:
        """
        Claude SDK를 사용하여 섹션 경계를 찾습니다.
        
        Args:
            chapter_text: 전체 챕터 텍스트
            section_title: 섹션 제목
            
        Returns:
            tuple: (시작 위치, 끝 위치)
        """
        # 텍스트가 너무 길면 일부만 사용
        text_sample = chapter_text[:8000] if len(chapter_text) > 8000 else chapter_text
        
        prompt = f"""
다음 마크다운 텍스트에서 "{section_title}" 섹션의 시작과 끝 위치를 찾아주세요.

응답 형식은 정확히 다음과 같이 해주세요:
START_POSITION: [숫자]
END_POSITION: [숫자]

텍스트:
{text_sample}
"""
        
        try:
            async for message in query(prompt=prompt, options=self.options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response = block.text
                            start_pos = self._extract_position(response, "START_POSITION")
                            end_pos = self._extract_position(response, "END_POSITION")
                            
                            if start_pos is not None and end_pos is not None:
                                return start_pos, end_pos
        
        except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
            print(f"⚠️ Claude SDK 오류, 폴백 검색 사용: {e}")
        
        # 폴백: 간단한 텍스트 검색
        return self._fallback_search(chapter_text, section_title)
    
    def _extract_position(self, response: str, position_type: str) -> Optional[int]:
        """응답에서 위치 정보를 추출합니다."""
        lines = response.split('\n')
        for line in lines:
            if position_type in line:
                try:
                    # ":"으로 분리해서 숫자 부분 추출
                    parts = line.split(':')
                    if len(parts) >= 2:
                        number_str = parts[1].strip().replace('[', '').replace(']', '')
                        return int(number_str)
                except (ValueError, IndexError):
                    continue
        return None
    
    def _fallback_search(self, text: str, title: str) -> Tuple[int, int]:
        """간단한 폴백 검색 방법"""
        # 제목을 정규화 (공백, 특수문자 처리)
        title_variants = [
            title,
            title.replace("'", "'"),
            title.replace("'", "'"),
            title.replace(""", '"'),
            title.replace(""", '"'),
            re.sub(r'\s+', ' ', title.strip())
        ]
        
        start_pos = -1
        for variant in title_variants:
            start_pos = text.find(variant)
            if start_pos != -1:
                break
        
        if start_pos == -1:
            # 부분 매칭 시도
            title_words = title.split()
            if title_words:
                start_pos = text.find(title_words[0])
        
        if start_pos == -1:
            print(f"⚠️ '{title}' 섹션을 찾을 수 없음, 전체 텍스트 사용")
            return 0, len(text)
        
        # 다음 섹션 시작점을 찾거나 텍스트 끝까지
        next_section_markers = [
            '\n# ',
            '\n## ',
            '\n### ',
            '\n#### ',
            '\n=== 페이지',
            '\nSummary',
            '\n요약'
        ]
        
        end_pos = len(text)
        search_start = start_pos + len(title) + 50  # 현재 섹션 제목 이후부터 검색
        
        for marker in next_section_markers:
            next_pos = text.find(marker, search_start)
            if next_pos != -1:
                end_pos = min(end_pos, next_pos)
        
        print(f"✓ '{title}' 섹션 발견: {start_pos}-{end_pos} ({end_pos-start_pos}자)")
        return start_pos, end_pos
    
    def extract_boundary_texts(self, text: str, start_pos: int, end_pos: int) -> Tuple[str, str]:
        """
        섹션의 시작과 끝에서 지정된 길이의 텍스트를 추출합니다.
        
        Args:
            text: 전체 텍스트
            start_pos: 섹션 시작 위치
            end_pos: 섹션 끝 위치
            
        Returns:
            tuple: (시작 텍스트, 끝 텍스트)
        """
        # 시작 텍스트 추출
        start_text = text[start_pos:start_pos + self.extract_length]
        
        # 끝 텍스트 추출
        end_start = max(end_pos - self.extract_length, start_pos)
        end_text = text[end_start:end_pos]
        
        return start_text.strip(), end_text.strip()
    
    async def process_leaf_node(self, chapter_text: str, leaf_node: Dict[str, Any]) -> Dict[str, Any]:
        """
        단일 리프 노드를 처리합니다.
        
        Args:
            chapter_text: 전체 챕터 텍스트
            leaf_node: 처리할 리프 노드
            
        Returns:
            업데이트된 리프 노드
        """
        try:
            node_title = leaf_node.get('title', 'Unknown')
            node_id = leaf_node.get('id', 'N/A')
            print(f"  처리 중: [{node_id}] {node_title}")
            
            # 섹션 경계 찾기 (Claude SDK 또는 폴백 사용)
            start_pos, end_pos = await self.find_section_boundaries_with_claude(
                chapter_text, node_title
            )
            
            # 시작/끝 텍스트 추출
            start_text, end_text = self.extract_boundary_texts(
                chapter_text, start_pos, end_pos
            )
            
            # 리프 노드 업데이트
            updated_node = leaf_node.copy()
            updated_node['start_text'] = start_text
            updated_node['end_text'] = end_text
            updated_node['section_start_pos'] = start_pos
            updated_node['section_end_pos'] = end_pos
            
            print(f"    ✓ 시작 텍스트: {len(start_text)}자")
            print(f"    ✓ 끝 텍스트: {len(end_text)}자")
            print(f"    ✓ 위치: {start_pos}-{end_pos}")
            
            return updated_node
            
        except Exception as e:
            print(f"    ❌ 오류 발생: {e}")
            # 오류 시 빈 텍스트로 설정
            updated_node = leaf_node.copy()
            updated_node['start_text'] = ""
            updated_node['end_text'] = ""
            updated_node['section_start_pos'] = -1
            updated_node['section_end_pos'] = -1
            updated_node['error'] = str(e)
            return updated_node
    
    async def process_all_nodes(self, chapter_text: str, leaf_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        모든 리프 노드를 처리합니다 (순차 처리로 Claude API 부하 관리).
        
        Args:
            chapter_text: 전체 챕터 텍스트
            leaf_nodes: 리프 노드 리스트
            
        Returns:
            업데이트된 리프 노드 리스트
        """
        print(f"\n🔄 {len(leaf_nodes)}개 리프 노드 처리 시작...")
        
        updated_nodes = []
        
        for i, node in enumerate(leaf_nodes, 1):
            print(f"\n[{i}/{len(leaf_nodes)}]", end=" ")
            
            try:
                updated_node = await self.process_leaf_node(chapter_text, node)
                updated_nodes.append(updated_node)
                
                # Claude API 부하 관리를 위한 짧은 대기
                if i < len(leaf_nodes):
                    await asyncio.sleep(1)
                    
            except Exception as e:
                print(f"❌ 노드 처리 실패: {e}")
                # 오류 시 원본 노드 사용
                error_node = node.copy()
                error_node['start_text'] = ""
                error_node['end_text'] = ""
                error_node['error'] = str(e)
                updated_nodes.append(error_node)
        
        print(f"\n✅ 모든 리프 노드 처리 완료!")
        return updated_nodes
    
    async def save_results(self, updated_nodes: List[Dict[str, Any]], output_path: str):
        """
        처리 결과를 JSON 파일로 저장합니다.
        
        Args:
            updated_nodes: 업데이트된 리프 노드 리스트
            output_path: 출력 파일 경로
        """
        try:
            # 출력 디렉토리 생성
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 결과 저장 완료: {output_path}")
            
            # 통계 정보 출력
            success_count = len([n for n in updated_nodes if n.get('start_text', '')])
            error_count = len([n for n in updated_nodes if n.get('error')])
            
            print(f"📊 처리 결과:")
            print(f"   - 성공: {success_count}개")
            print(f"   - 실패: {error_count}개")
            print(f"   - 총합: {len(updated_nodes)}개")
            
        except Exception as e:
            print(f"❌ 결과 저장 실패: {e}")
            raise


async def main():
    """메인 실행 함수"""
    print("🚀 Claude Code SDK 리프 노드 경계 텍스트 추출기 시작")
    print("=" * 60)
    
    # 명령행 인수 처리
    if len(sys.argv) == 4:
        leaf_nodes_path = sys.argv[1]
        chapter_path = sys.argv[2] 
        output_path = sys.argv[3]
    else:
        # 기본 파일 경로
        leaf_nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part2_scalability_leaf_nodes.json"
        chapter_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
        output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_with_boundaries.json"
    
    # 설정
    extractor = ClaudeSDKLeafBoundaryExtractor(extract_length=200)
    
    try:
        # 1. 파일 로드
        print("\n📂 파일 로드 중...")
        leaf_nodes, chapter_text = await extractor.load_files(
            leaf_nodes_path, chapter_path
        )
        
        if not leaf_nodes:
            print("⚠️ 7장 관련 리프 노드가 없습니다.")
            return 1
        
        # 2. 리프 노드 처리
        updated_nodes = await extractor.process_all_nodes(
            chapter_text, leaf_nodes
        )
        
        # 3. 결과 저장
        print("\n💾 결과 저장 중...")
        await extractor.save_results(updated_nodes, output_path)
        
        print("\n🎉 모든 작업 완료!")
        print(f"   - 입력: {leaf_nodes_path}")
        print(f"   - 원문: {chapter_path}")
        print(f"   - 출력: {output_path}")
        
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단됨")
        return 1
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    # 비동기 메인 함수 실행
    exit_code = asyncio.run(main())
    exit(exit_code)


"""
사용 방법:

1. 필요한 패키지 설치:
   pip install claude-code-sdk

2. Claude Code CLI 설치:
   npm install -g @anthropic-ai/claude-code

3. 스크립트 실행:
   # 기본 경로 사용
   python claude_sdk_leaf_boundary_extractor.py
   
   # 사용자 지정 경로
   python claude_sdk_leaf_boundary_extractor.py [리프노드JSON] [원문MD] [출력JSON]

주요 기능:
- 7장 관련 노드만 자동 필터링 (id 66-72)
- Claude SDK를 활용한 지능적 섹션 경계 탐지
- 폴백 메커니즘으로 안정적인 텍스트 검색
- 각 노드의 시작/끝 텍스트 추출 (기본 200자)
- 상세한 진행 상황 및 통계 정보 제공
- 에러 처리 및 복구 메커니즘

출력 JSON 형식:
각 리프 노드에 다음 필드가 추가됩니다:
- start_text: 섹션 시작 부분 텍스트 (200자)
- end_text: 섹션 끝 부분 텍스트 (200자)  
- section_start_pos: 섹션 시작 위치
- section_end_pos: 섹션 끝 위치
- error: 오류 발생 시 오류 메시지
"""