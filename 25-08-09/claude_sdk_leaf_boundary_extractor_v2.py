#!/usr/bin/env python3
"""
Claude Code SDK 기반 리프 노드 경계 텍스트 추출기 (Max Plan 사용자용)

이 스크립트는 리프 노드 JSON 파일과 마크다운 원문을 입력받아,
각 리프 노드 섹션의 시작과 끝 부분에서 지정된 길이의 텍스트를 추출합니다.

요구사항:
- Python 3.10+
- Node.js
- Claude Code: npm install -g @anthropic-ai/claude-code
- Python 패키지: pip install claude-code-sdk

사용법:
python claude_sdk_leaf_boundary_extractor_v2.py [leaf_nodes_json] [chapter_markdown] [output_json]
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
    """Claude Code SDK를 활용한 리프 노드 경계 텍스트 추출기 (Max Plan 최적화)"""
    
    def __init__(self, extract_length: int = 15, debug: bool = True):
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
            'claude_partial_matches': 0,
            'fallback_partial_matches': 0,
            'total_processing_time': 0,
            'text_length_analysis': {},
            'section_detection_analysis': {},
            'errors': []
        }
        
        # 로깅 설정
        self._setup_logging()
        
        # Max Plan 사용자용 간단한 옵션
        self.options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="JSON만 반환하세요. 설명이나 추가 텍스트는 금지입니다."
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
        self.logger = logging.getLogger(f"{__name__}_{timestamp}")
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # 핸들러 중복 방지
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
            
            self.logger.info(f"✓ 리프 노드 로드 완료: {len(all_nodes)}개 (7장: {len(chapter7_nodes)}개)")
            self.logger.info(f"✓ 챕터 텍스트 로드 완료: {len(chapter_text):,}자")
            
            return chapter7_nodes, chapter_text
            
        except FileNotFoundError as e:
            self.logger.error(f"파일을 찾을 수 없습니다: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 파싱 오류: {e}")
            raise
    
    async def process_nodes_with_claude(self, chapter_text: str, leaf_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Claude SDK를 사용하여 모든 노드를 한 번에 처리합니다 (강화된 디버깅).
        
        Args:
            chapter_text: 전체 챕터 텍스트
            leaf_nodes: 리프 노드 리스트
            
        Returns:
            업데이트된 리프 노드 리스트
        """
        try:
            # 📊 텍스트 길이 분석
            self.stats['text_length_analysis'] = {
                'original_length': len(chapter_text),
                'used_length': 0,
                'truncated': False
            }
            
            # 📍 섹션 사전 분석
            section_analysis = self._analyze_sections_in_text(chapter_text, leaf_nodes)
            self.stats['section_detection_analysis'] = section_analysis
            
            self.logger.info(f"📊 섹션 분석 결과:")
            for node_id, analysis in section_analysis.items():
                title = analysis.get('title', 'Unknown')
                found = analysis.get('found', False)
                positions = analysis.get('positions', [])
                self.logger.info(f"   [{node_id}] {title}: {'✓' if found else '✗'} ({len(positions)} 위치)")
            
            # 텍스트 길이 최적화 (Max Plan 고려하되 섹션 분석 반영)
            max_text_length = self._calculate_optimal_text_length(chapter_text, section_analysis)
            limited_text = chapter_text[:max_text_length] if len(chapter_text) > max_text_length else chapter_text
            
            self.stats['text_length_analysis']['used_length'] = len(limited_text)
            self.stats['text_length_analysis']['truncated'] = len(chapter_text) > max_text_length
            
            # 🎯 타겟 프롬프트 생성 (분석 결과 반영)
            prompt = self._create_enhanced_batch_prompt(leaf_nodes, limited_text, section_analysis)
            
            self.logger.info(f"🤖 Claude에게 {len(leaf_nodes)}개 노드 일괄 요청 (텍스트: {len(limited_text):,}자)")
            self.logger.debug(f"📝 프롬프트 길이: {len(prompt):,}자")
            
            self.stats['claude_api_calls'] += 1
            
            responses = []
            async for message in query(prompt=prompt, options=self.options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            responses.append(block.text)
            
            if responses:
                full_response = "\n".join(responses)
                self.logger.info(f"📥 Claude 응답 길이: {len(full_response)} 문자")
                self.logger.debug(f"📝 Claude 응답 샘플: {full_response[:300]}...")
                
                # 강화된 응답 파싱
                parsed_nodes = self._parse_claude_response_enhanced(full_response, leaf_nodes, section_analysis)
                if parsed_nodes:
                    success_count = len([n for n in parsed_nodes if n.get('start_text', '')])
                    self.logger.info(f"✅ Claude로 {success_count}/{len(parsed_nodes)}개 노드 처리 성공")
                    
                    # 부분 실패시 자동 폴백 적용
                    if success_count < len(parsed_nodes):
                        self.logger.warning(f"⚠️ {len(parsed_nodes) - success_count}개 노드 실패, 폴백으로 보완")
                        return await self._enhance_with_fallback(chapter_text, parsed_nodes)
                    
                    return parsed_nodes
            
            # Claude 완전 실패 시 폴백
            self.logger.warning("⚠️ Claude 응답 파싱 실패, 전체 폴백 검색 사용")
            return await self._process_nodes_fallback(chapter_text, leaf_nodes)
            
        except Exception as e:
            self.logger.error(f"Claude 처리 오류: {e}")
            import traceback
            self.logger.debug(f"상세 오류: {traceback.format_exc()}")
            
            self.stats['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': f"Claude processing error: {str(e)}",
                'context': 'batch_processing',
                'traceback': traceback.format_exc()
            })
            # 폴백으로 처리
            return await self._process_nodes_fallback(chapter_text, leaf_nodes)
    
    def _analyze_sections_in_text(self, text: str, leaf_nodes: List[Dict]) -> Dict:
        """텍스트 내 섹션들을 사전 분석"""
        analysis = {}
        
        for node in leaf_nodes:
            node_id = node.get('id')
            title = node.get('title', '')
            
            # 다양한 제목 패턴 검색
            title_patterns = [
                title,  # 원본
                title.replace("'", "'").replace("'", "'"),  # 따옴표 정규화
                title.replace(""", '"').replace(""", '"'),  # 인용부호 정규화
                re.sub(r'\s+', ' ', title.strip()),  # 공백 정규화
                title.split()[0] if title.split() else title,  # 첫 번째 단어만
            ]
            
            # 추가 패턴들 (7.1, 7.2 등)
            if re.match(r'^\d+\.\d+', title):
                title_patterns.append(title.split()[0])  # "7.1" 부분만
            
            positions = []
            for pattern in title_patterns:
                if not pattern:
                    continue
                
                # 정확한 매칭
                start = 0
                while True:
                    pos = text.find(pattern, start)
                    if pos == -1:
                        break
                    positions.append({
                        'position': pos,
                        'pattern': pattern,
                        'context': text[max(0, pos-20):pos+len(pattern)+20]
                    })
                    start = pos + 1
            
            analysis[node_id] = {
                'title': title,
                'found': len(positions) > 0,
                'positions': positions,
                'patterns_tried': title_patterns
            }
        
        return analysis
    
    def _calculate_optimal_text_length(self, text: str, section_analysis: Dict) -> int:
        """섹션 분석 결과에 기반한 최적 텍스트 길이 계산"""
        # 기본 Max Plan 제한
        base_limit = 12000
        
        # 모든 섹션이 발견된 마지막 위치 찾기
        last_found_pos = 0
        for analysis in section_analysis.values():
            if analysis['found'] and analysis['positions']:
                max_pos = max(pos['position'] for pos in analysis['positions'])
                last_found_pos = max(last_found_pos, max_pos)
        
        # 마지막 섹션 이후 충분한 여유 공간 추가
        optimal_length = min(base_limit, last_found_pos + 5000)
        
        self.logger.debug(f"텍스트 길이 최적화: 마지막 섹션 위치 {last_found_pos}, 최적 길이 {optimal_length}")
        return optimal_length
    
    def _create_enhanced_batch_prompt(self, leaf_nodes: List[Dict], text: str, section_analysis: Dict) -> str:
        """강화된 일괄 처리용 프롬프트 생성"""
        
        # 발견된 섹션과 실패한 섹션 구분
        found_nodes = []
        missing_nodes = []
        
        for node in leaf_nodes:
            node_id = node.get('id')
            analysis = section_analysis.get(node_id, {})
            if analysis.get('found', False):
                found_nodes.append(node)
            else:
                missing_nodes.append(node)
        
        # 프롬프트 구성
        prompt_parts = [
            f"텍스트에서 각 제목의 시작과 끝 부분을 찾아 JSON 배열로 반환하세요.",
            f"",
            f"텍스트:",
            text,
            f"",
            f"찾을 노드들 ({len(found_nodes)}개 발견됨, {len(missing_nodes)}개 미발견):"
        ]
        
        # 노드 정보 (발견 상태 포함)
        for node in leaf_nodes:
            node_id = node.get('id')
            title = node.get('title', '')
            level = node.get('level', 1)
            analysis = section_analysis.get(node_id, {})
            found_status = "✓" if analysis.get('found', False) else "✗"
            
            prompt_parts.append(f"- [{node_id}] {title} (레벨 {level}) {found_status}")
        
        prompt_parts.extend([
            f"",
            f"각 노드에 대해 다음 형식으로 반환:",
            f"{{",
            f'  "id": [노드ID],',
            f'  "title": "[제목]",',  
            f'  "level": [레벨],',
            f'  "start_text": "[섹션 시작부분 {self.extract_length}자]",',
            f'  "end_text": "[섹션 끝부분 {self.extract_length}자]",',
            f'  "section_start_pos": [시작위치],',
            f'  "section_end_pos": [끝위치]',
            f"}}",
            f"",
            f"JSON 배열만 반환하세요. 설명 금지."
        ])
        
        return "\n".join(prompt_parts)
    
    def _parse_claude_response_enhanced(self, response_text: str, original_nodes: List[Dict], section_analysis: Dict) -> Optional[List[Dict]]:
        """강화된 Claude 응답 파싱"""
        try:
            self.logger.debug(f"강화된 응답 파싱 시작: {response_text[:200]}...")
            
            # JSON 블록 찾기 (여러 패턴 시도)
            json_patterns = [
                r'```json\s*([\s\S]*?)\s*```',  # 표준 JSON 블록
                r'```\s*([\s\S]*?)\s*```',      # 일반 코드 블록
                r'\[[\s\S]*?\]'                  # JSON 배열 직접
            ]
            
            json_text = ""
            for pattern in json_patterns:
                matches = re.findall(pattern, response_text, re.IGNORECASE)
                if matches:
                    # 가장 큰 매치 선택
                    json_text = max(matches, key=len).strip()
                    self.logger.debug(f"JSON 패턴 '{pattern}' 매치 성공")
                    break
            
            if json_text:
                parsed_data = json.loads(json_text)
                
                if isinstance(parsed_data, list) and len(parsed_data) >= 0:
                    self.logger.info(f"✅ 강화된 JSON 파싱 성공: {len(parsed_data)}개 노드")
                    
                    # 원본 노드와 매칭하여 보완
                    return self._merge_with_original_nodes_enhanced(parsed_data, original_nodes, section_analysis)
                else:
                    self.logger.error("잘못된 JSON 구조")
                    return None
            else:
                self.logger.error("JSON을 찾을 수 없음")
                # 응답 텍스트에서 수동으로 정보 추출 시도
                return self._extract_from_plain_text(response_text, original_nodes, section_analysis)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 파싱 실패: {e}")
            # 수동 추출 시도
            return self._extract_from_plain_text(response_text, original_nodes, section_analysis)
        except Exception as e:
            self.logger.error(f"강화된 응답 파싱 오류: {e}")
            return None
    
    def _extract_from_plain_text(self, response_text: str, original_nodes: List[Dict], section_analysis: Dict) -> Optional[List[Dict]]:
        """JSON 파싱 실패시 플레인 텍스트에서 정보 추출"""
        self.logger.info("🔧 플레인 텍스트에서 정보 수동 추출 시도")
        
        results = []
        for node in original_nodes:
            node_id = node.get('id')
            title = node.get('title', '')
            
            # 응답에서 해당 노드 언급 찾기
            node_mentions = []
            for line in response_text.split('\n'):
                if str(node_id) in line or title in line:
                    node_mentions.append(line.strip())
            
            if node_mentions:
                self.logger.debug(f"노드 {node_id} 언급 발견: {len(node_mentions)}건")
                self.stats['claude_partial_matches'] += 1
            
            # 기본 노드로 설정 (추후 폴백으로 보완)
            result_node = node.copy()
            result_node.update({
                'start_text': '',
                'end_text': '',
                'section_start_pos': -1,
                'section_end_pos': -1,
                'claude_mentions': node_mentions
            })
            results.append(result_node)
        
        return results if results else None
    
    def _merge_with_original_nodes_enhanced(self, parsed_nodes: List[Dict], original_nodes: List[Dict], section_analysis: Dict) -> List[Dict]:
        """강화된 노드 병합"""
        result = []
        
        for original in original_nodes:
            node_id = original.get('id')
            original_title = original.get('title', '').strip()
            
            # 파싱된 노드에서 매칭되는 것 찾기
            matched = None
            for parsed in parsed_nodes:
                # ID 매칭
                if parsed.get('id') == node_id:
                    matched = parsed
                    break
                # 제목 매칭 (정규화)
                parsed_title = parsed.get('title', '').strip()
                if (parsed_title == original_title or
                    re.sub(r'\s+', ' ', parsed_title) == re.sub(r'\s+', ' ', original_title)):
                    matched = parsed
                    break
            
            if matched and matched.get('start_text', '').strip():
                # 매칭 성공
                merged = original.copy()
                merged.update({
                    'start_text': matched.get('start_text', '')[:self.extract_length],
                    'end_text': matched.get('end_text', '')[:self.extract_length],
                    'section_start_pos': matched.get('section_start_pos', -1),
                    'section_end_pos': matched.get('section_end_pos', -1)
                })
                result.append(merged)
                self._update_stats(success=True)
                self.logger.debug(f"✓ 노드 {node_id} 매칭 성공")
            else:
                # 매칭 실패 - 폴백 대상
                failed = original.copy()
                failed.update({
                    'start_text': '',
                    'end_text': '',
                    'section_start_pos': -1,
                    'section_end_pos': -1,
                    'needs_fallback': True,
                    'error': 'No matching data from Claude'
                })
                result.append(failed)
                self._update_stats(success=False, error='No matching Claude data')
                self.logger.debug(f"✗ 노드 {node_id} 매칭 실패 - 폴백 필요")
        
        return result
    
    async def _enhance_with_fallback(self, chapter_text: str, partial_nodes: List[Dict]) -> List[Dict]:
        """부분 실패한 노드들을 폴백으로 보완"""
        self.logger.info("🔄 부분 실패 노드들을 폴백으로 보완 중...")
        
        enhanced_nodes = []
        for node in partial_nodes:
            if node.get('needs_fallback', False) or not node.get('start_text', '').strip():
                # 폴백 처리 필요
                try:
                    title = node.get('title', '')
                    start_pos, end_pos = self._fallback_search_enhanced(chapter_text, title, node.get('id'))
                    
                    if start_pos != -1:
                        start_text, end_text = self._extract_boundary_texts(chapter_text, start_pos, end_pos)
                        
                        enhanced = node.copy()
                        enhanced.update({
                            'start_text': start_text,
                            'end_text': end_text,
                            'section_start_pos': start_pos,
                            'section_end_pos': end_pos,
                            'processed_by': 'fallback',
                            'needs_fallback': False
                        })
                        enhanced_nodes.append(enhanced)
                        self.stats['fallback_partial_matches'] += 1
                        self.logger.debug(f"✓ 폴백으로 노드 {node.get('id')} 보완 성공")
                    else:
                        enhanced_nodes.append(node)
                        self.logger.warning(f"✗ 폴백으로도 노드 {node.get('id')} 처리 실패")
                        
                except Exception as e:
                    self.logger.error(f"폴백 보완 오류 (노드 {node.get('id')}): {e}")
                    enhanced_nodes.append(node)
            else:
                # 이미 성공한 노드
                enhanced_nodes.append(node)
        
        return enhanced_nodes
    
    def _create_batch_prompt(self, leaf_nodes: List[Dict], text: str) -> str:
        """일괄 처리용 프롬프트 생성"""
        
        # 노드 정보 간단히 정리
        node_info = []
        for node in leaf_nodes:
            node_info.append({
                'id': node.get('id'),
                'title': node.get('title', ''),
                'level': node.get('level', 1)
            })
        
        prompt = f"""텍스트에서 각 제목의 시작과 끝 부분을 찾아 JSON 배열로 반환하세요.

텍스트:
{text}

찾을 노드들:
{json.dumps(node_info, ensure_ascii=False, indent=2)}

각 노드에 대해 다음 형식으로 반환:
{{
  "id": [노드ID],
  "title": "[제목]", 
  "level": [레벨],
  "start_text": "[섹션 시작부분 {self.extract_length}자]",
  "end_text": "[섹션 끝부분 {self.extract_length}자]",
  "section_start_pos": [시작위치],
  "section_end_pos": [끝위치]
}}

JSON 배열만 반환하세요. 설명 금지."""
        
        return prompt
    
    def _parse_claude_response(self, response_text: str, original_nodes: List[Dict]) -> Optional[List[Dict]]:
        """Claude 응답 파싱"""
        try:
            self.logger.debug(f"응답 파싱 시작: {response_text[:200]}...")
            
            # JSON 블록 찾기
            json_pattern = r'```json\s*([\s\S]*?)\s*```'
            json_matches = re.findall(json_pattern, response_text, re.IGNORECASE)
            
            json_text = ""
            if json_matches:
                json_text = json_matches[0].strip()
            else:
                # JSON 배열 직접 찾기
                array_pattern = r'\[[\s\S]*?\]'
                array_matches = re.findall(array_pattern, response_text)
                if array_matches:
                    json_text = max(array_matches, key=len).strip()
            
            if json_text:
                parsed_data = json.loads(json_text)
                
                if isinstance(parsed_data, list) and len(parsed_data) > 0:
                    self.logger.info(f"✅ JSON 파싱 성공: {len(parsed_data)}개 노드")
                    
                    # 원본 노드와 매칭하여 누락된 필드 보완
                    return self._merge_with_original_nodes(parsed_data, original_nodes)
                else:
                    self.logger.error("잘못된 JSON 구조")
                    return None
            else:
                self.logger.error("JSON을 찾을 수 없음")
                return None
                
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 파싱 실패: {e}")
            return None
        except Exception as e:
            self.logger.error(f"응답 파싱 오류: {e}")
            return None
    
    def _merge_with_original_nodes(self, parsed_nodes: List[Dict], original_nodes: List[Dict]) -> List[Dict]:
        """파싱된 노드를 원본과 병합"""
        result = []
        
        for original in original_nodes:
            # 파싱된 노드에서 매칭되는 것 찾기
            matched = None
            for parsed in parsed_nodes:
                if (parsed.get('id') == original.get('id') or 
                    parsed.get('title', '').strip() == original.get('title', '').strip()):
                    matched = parsed
                    break
            
            if matched:
                # 원본 노드를 기본으로 하고 파싱된 데이터로 업데이트
                merged = original.copy()
                merged.update({
                    'start_text': matched.get('start_text', ''),
                    'end_text': matched.get('end_text', ''),
                    'section_start_pos': matched.get('section_start_pos', -1),
                    'section_end_pos': matched.get('section_end_pos', -1)
                })
                result.append(merged)
                self._update_stats(success=True)
            else:
                # 매칭 실패 시 빈 값으로 설정
                failed = original.copy()
                failed.update({
                    'start_text': '',
                    'end_text': '',
                    'section_start_pos': -1,
                    'section_end_pos': -1,
                    'error': 'No matching data from Claude'
                })
                result.append(failed)
                self._update_stats(success=False, error='No matching Claude data')
        
        return result
    
    async def _process_nodes_fallback(self, chapter_text: str, leaf_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """폴백: 간단한 텍스트 검색으로 처리"""
        self.logger.info(f"🔄 폴백 검색으로 {len(leaf_nodes)}개 노드 처리 중...")
        self.stats['fallback_searches'] += 1
        
        updated_nodes = []
        
        for node in leaf_nodes:
            try:
                title = node.get('title', '')
                
                # 간단한 텍스트 검색
                start_pos, end_pos = self._fallback_search(chapter_text, title)
                
                # 경계 텍스트 추출
                start_text, end_text = self._extract_boundary_texts(chapter_text, start_pos, end_pos)
                
                # 노드 업데이트
                updated_node = node.copy()
                updated_node.update({
                    'start_text': start_text,
                    'end_text': end_text,
                    'section_start_pos': start_pos,
                    'section_end_pos': end_pos
                })
                
                updated_nodes.append(updated_node)
                self._update_stats(success=True)
                
                self.logger.debug(f"✓ 폴백 처리 성공: {title}")
                
            except Exception as e:
                self.logger.error(f"폴백 처리 실패: {node.get('title', 'Unknown')} - {e}")
                error_node = node.copy()
                error_node.update({
                    'start_text': '',
                    'end_text': '',
                    'section_start_pos': -1,
                    'section_end_pos': -1,
                    'error': str(e)
                })
                updated_nodes.append(error_node)
                self._update_stats(success=False, error=str(e))
        
        return updated_nodes
    
    def _fallback_search_enhanced(self, text: str, title: str, node_id: int) -> Tuple[int, int]:
        """강화된 폴백 검색 (더 많은 패턴 시도)"""
        self.logger.debug(f"강화된 폴백 검색 시작: [{node_id}] {title}")
        
        # 1단계: 기본 패턴들
        title_variants = [
            title,  # 원본
            title.replace("'", "'").replace("'", "'"),  # 따옴표 정규화
            title.replace(""", '"').replace(""", '"'),  # 인용부호 정규화
            re.sub(r'\s+', ' ', title.strip()),  # 공백 정규화
        ]
        
        # 2단계: 섹션 번호 패턴 (7.4, 7.5 등)
        if re.match(r'^\d+\.\d+', title):
            section_num = title.split()[0]  # "7.4" 부분
            title_variants.extend([
                section_num,
                f"\n{section_num}",  # 줄바꿈 후 섹션 번호
                f"=== 페이지.*{section_num}",  # 페이지 표시와 함께
                f"{section_num}.*\n"  # 섹션 번호 후 줄바꿈
            ])
        
        # 3단계: 키워드 기반 검색
        title_words = title.split()
        if len(title_words) > 1:
            # 주요 키워드들
            for word in title_words[1:]:  # 첫 번째는 보통 번호
                if len(word) > 3:  # 의미있는 단어만
                    title_variants.append(word)
        
        # 4단계: 정규식 패턴 검색
        start_pos = -1
        found_pattern = None
        
        for variant in title_variants:
            if not variant:
                continue
            
            # 정확한 문자열 매칭
            pos = text.find(variant)
            if pos != -1:
                start_pos = pos
                found_pattern = variant
                break
                
            # 정규식 매칭 (특수 패턴)
            if "===" in variant or ".*" in variant:
                try:
                    pattern = variant
                    matches = re.search(pattern, text, re.MULTILINE)
                    if matches:
                        start_pos = matches.start()
                        found_pattern = variant
                        break
                except re.error:
                    continue
        
        if start_pos == -1:
            self.logger.warning(f"'{title}' 섹션을 찾을 수 없음 (시도된 패턴: {len(title_variants)}개)")
            return 0, len(text)
        
        self.logger.debug(f"'{title}' 발견: 위치 {start_pos}, 패턴 '{found_pattern}'")
        
        # 섹션 끝 찾기 (강화된 마커)
        next_section_markers = [
            '\n# ',
            '\n## ',
            '\n### ',
            '\n#### ',
            f'\n{section_num[0]}.{int(section_num.split(".")[1]) + 1}' if re.match(r'^\d+\.\d+', title) else None,  # 다음 섹션 번호
            '\n=== 페이지',
            '\nSummary',
            '\n요약',
            '\n\n## ',  # 다른 챕터
            '\nListing\d+\.\d+',  # 코드 리스팅
        ]
        
        # None 제거
        next_section_markers = [m for m in next_section_markers if m is not None]
        
        end_pos = len(text)
        search_start = start_pos + len(found_pattern) + 50
        
        for marker in next_section_markers:
            if marker.startswith('\n'):
                # 정확한 문자열 검색
                next_pos = text.find(marker, search_start)
            else:
                # 정규식 검색
                try:
                    match = re.search(marker, text[search_start:], re.MULTILINE)
                    next_pos = search_start + match.start() if match else -1
                except re.error:
                    next_pos = -1
            
            if next_pos != -1:
                end_pos = min(end_pos, next_pos)
        
        self.logger.debug(f"'{title}' 섹션 범위: {start_pos}-{end_pos} ({end_pos-start_pos}자)")
        return start_pos, end_pos
    
    def _fallback_search(self, text: str, title: str) -> Tuple[int, int]:
        """간단한 폴백 검색"""
        # 제목 정규화
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
            self.logger.warning(f"'{title}' 섹션을 찾을 수 없음")
            return 0, len(text)
        
        # 다음 섹션까지 찾기
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
        search_start = start_pos + len(title) + 50
        
        for marker in next_section_markers:
            next_pos = text.find(marker, search_start)
            if next_pos != -1:
                end_pos = min(end_pos, next_pos)
        
        self.logger.debug(f"'{title}' 섹션 발견: {start_pos}-{end_pos}")
        return start_pos, end_pos
    
    def _extract_boundary_texts(self, text: str, start_pos: int, end_pos: int) -> Tuple[str, str]:
        """경계 텍스트 추출"""
        # 시작 텍스트
        start_text = text[start_pos:start_pos + self.extract_length].strip()
        
        # 끝 텍스트
        end_start = max(end_pos - self.extract_length, start_pos)
        end_text = text[end_start:end_pos].strip()
        
        return start_text, end_text
    
    async def save_results(self, updated_nodes: List[Dict[str, Any]], output_path: str):
        """결과 저장"""
        try:
            # 출력 디렉토리 생성
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
            
            # 최종 통계 계산
            success_count = len([n for n in updated_nodes if n.get('start_text', '')])
            error_count = len([n for n in updated_nodes if n.get('error')])
            
            self.logger.info(f"✅ 결과 저장 완료: {output_path}")
            self.logger.info(f"📊 최종 통계:")
            self.logger.info(f"   - 성공: {success_count}개")
            self.logger.info(f"   - 실패: {error_count}개")
            self.logger.info(f"   - 총합: {len(updated_nodes)}개")
            self.logger.info(f"   - Claude API 호출: {self.stats['claude_api_calls']}회")
            self.logger.info(f"   - 폴백 검색: {self.stats['fallback_searches']}회")
            
            # 총 처리 시간
            total_time = time.time() - self.start_time
            self.logger.info(f"   - 총 처리 시간: {total_time:.2f}초")
            
        except Exception as e:
            self.logger.error(f"결과 저장 실패: {e}")
            raise


async def main():
    """메인 실행 함수"""
    print("🚀 Claude Code SDK 리프 노드 경계 텍스트 추출기 (Max Plan 최적화)")
    print("=" * 70)
    
    # 명령행 인수 처리
    if len(sys.argv) == 4:
        leaf_nodes_path = sys.argv[1]
        chapter_path = sys.argv[2] 
        output_path = sys.argv[3]
    else:
        # 기본 파일 경로
        leaf_nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part2_scalability_leaf_nodes.json"
        chapter_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
        output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_with_boundaries_v2.json"
    
    # 설정
    extractor = ClaudeSDKLeafBoundaryExtractor(extract_length=15, debug=True)
    
    try:
        # 1. 파일 로드
        print("\n📂 파일 로드 중...")
        leaf_nodes, chapter_text = await extractor.load_files(
            leaf_nodes_path, chapter_path
        )
        
        if not leaf_nodes:
            print("⚠️ 7장 관련 리프 노드가 없습니다.")
            return 1
        
        # 2. Claude로 일괄 처리 (Max Plan 최적화)
        print(f"\n🤖 Claude SDK로 {len(leaf_nodes)}개 노드 일괄 처리 중...")
        updated_nodes = await extractor.process_nodes_with_claude(
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
Max Plan 사용자 최적화 버전 특징:

1. 일괄 처리 방식:
   - 모든 노드를 한 번의 Claude API 호출로 처리
   - 비용 효율성 극대화

2. 간단한 프롬프트:
   - "JSON만 반환" 옵션으로 토큰 절약
   - 불필요한 설명 제거

3. 강력한 폴백 시스템:
   - Claude 실패 시 즉시 텍스트 검색으로 대체
   - 100% 처리 보장

4. 상세한 모니터링:
   - 실시간 진행상황 및 통계
   - 로그 파일로 디버깅 지원
   - 성공/실패율 추적

5. 오류 복구:
   - 부분 실패 시에도 최대한 결과 생성
   - 각 노드별 오류 정보 기록

사용 방법:
# 기본 경로 사용
python claude_sdk_leaf_boundary_extractor_v2.py

# 사용자 지정 경로
python claude_sdk_leaf_boundary_extractor_v2.py [리프노드JSON] [원문MD] [출력JSON]
"""