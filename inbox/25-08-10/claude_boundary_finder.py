#!/usr/bin/env python3
"""
# claude_boundary_finder.py

## 생성 시간: 2025-08-10 15:55:10 KST

## 핵심 내용: Claude SDK를 사용해 특정 리프노드 섹션의 정확한 시작/종료 문자열 추출

## 상세 내용:
- ClaudeBoundaryFinder (라인 27-196): Claude SDK 기반 경계 문자열 추출 메인 클래스
- load_source_text (라인 36-55): 7장 원문 마크다운 파일 로드
- load_leaf_nodes (라인 57-77): 7장 리프노드 JSON 파일 로드
- find_target_node (라인 79-98): 타겟 노드 찾기
- extract_boundaries_with_claude (라인 100-164): Claude SDK를 사용한 경계 추출
- validate_boundaries (라인 166-196): 추출된 경계 검증
- main (라인 199-249): 메인 실행 함수

## 상태: 활성

## 주소: claude_boundary_finder

## 참조: 
"""

import json
import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Claude SDK 관련 임포트는 실행 시에 처리
try:
    from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
    from claude_code_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("⚠️ Claude SDK가 설치되지 않았습니다. pip install claude-code-sdk 실행하세요.")


class ClaudeBoundaryFinder:
    """Claude SDK를 사용한 리프노드 섹션 경계 추출기"""
    
    def __init__(self, debug: bool = False):
        """
        초기화
        
        Args:
            debug: 디버그 모드 활성화
        """
        self.debug = debug
        self.options = ClaudeCodeOptions(
            system_prompt=(
                "당신은 문서 구조 분석 전문가입니다. "
                "마크다운 문서에서 특정 섹션의 정확한 시작과 끝 위치를 찾는 것이 목표입니다. "
                "섹션 경계는 다음 섹션 제목이 나타나기 직전까지입니다."
            ),
            max_turns=1
        )
    
    def load_source_text(self, source_path: str) -> str:
        """
        7장 원문 마크다운 파일을 로드합니다.
        
        Args:
            source_path: 원문 파일 경로
            
        Returns:
            원문 텍스트
        """
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✓ 원문 로드 완료: {len(content):,}자")
            return content
        except FileNotFoundError:
            print(f"❌ 원문 파일을 찾을 수 없습니다: {source_path}")
            return ""
        except Exception as e:
            print(f"❌ 원문 로드 중 오류: {e}")
            return ""
    
    def load_leaf_nodes(self, nodes_path: str) -> List[Dict[str, Any]]:
        """
        7장 리프노드 JSON 파일을 로드합니다.
        
        Args:
            nodes_path: 리프노드 파일 경로
            
        Returns:
            리프노드 리스트
        """
        try:
            with open(nodes_path, 'r', encoding='utf-8') as f:
                nodes = json.load(f)
            print(f"✓ 리프노드 로드 완료: {len(nodes)}개")
            return nodes
        except FileNotFoundError:
            print(f"❌ 리프노드 파일을 찾을 수 없습니다: {nodes_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 오류: {e}")
            return []
    
    def find_target_node(self, nodes: List[Dict[str, Any]], target_title: str) -> Optional[Dict[str, Any]]:
        """
        타겟 제목의 노드를 찾습니다.
        
        Args:
            nodes: 리프노드 리스트
            target_title: 찾을 제목
            
        Returns:
            찾은 노드 또는 None
        """
        for node in nodes:
            if node.get('title', '') == target_title:
                print(f"✓ 타겟 노드 발견: {target_title} (ID: {node.get('id')})")
                return node
        
        print(f"❌ 타겟 노드를 찾을 수 없습니다: {target_title}")
        print("   사용 가능한 제목들:")
        for node in nodes:
            print(f"     - {node.get('title', 'Unknown')}")
        return None
    
    async def extract_boundaries_with_claude(self, source_text: str, target_title: str, next_title: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Claude SDK를 사용해 섹션의 정확한 시작/종료 경계를 추출합니다.
        
        Args:
            source_text: 전체 원문 텍스트
            target_title: 타겟 섹션 제목
            next_title: 다음 섹션 제목 (종료점 판단용)
            
        Returns:
            tuple: (시작 경계 문자열, 종료 경계 문자열)
        """
        # 텍스트가 너무 길면 샘플링
        if len(source_text) > 15000:
            # target_title 주변으로 텍스트 추출
            target_pos = source_text.find(target_title)
            if target_pos != -1:
                start_sample = max(0, target_pos - 2000)
                end_sample = min(len(source_text), target_pos + 8000)
                source_sample = source_text[start_sample:end_sample]
            else:
                source_sample = source_text[:15000]
        else:
            source_sample = source_text
        
        next_section_info = f"다음 섹션은 '{next_title}'입니다." if next_title else "문서의 마지막 섹션입니다."
        
        prompt = f"""
다음 마크다운 문서에서 "{target_title}" 섹션의 정확한 시작과 끝 경계를 찾아주세요.
{next_section_info}

요구사항:
1. 시작 경계: "{target_title}" 제목을 포함한 섹션 시작 부분의 고유한 문자열 (20-40자)
2. 종료 경계: 해당 섹션의 마지막 부분 고유한 문자열 (20-40자)
3. 종료 경계는 다음 섹션 제목 바로 전까지의 내용에서 선택

응답 형식:
START_BOUNDARY: [시작 경계 문자열]
END_BOUNDARY: [종료 경계 문자열]

문서 내용:
{source_sample}
"""
        
        try:
            print(f"🔍 Claude SDK로 '{target_title}' 섹션 경계 분석 중...")
            
            async for message in query(prompt=prompt, options=self.options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response = block.text
                            
                            # 시작 경계 추출
                            start_boundary = None
                            end_boundary = None
                            
                            lines = response.split('\n')
                            for line in lines:
                                if 'START_BOUNDARY:' in line:
                                    start_boundary = line.split('START_BOUNDARY:')[1].strip()
                                elif 'END_BOUNDARY:' in line:
                                    end_boundary = line.split('END_BOUNDARY:')[1].strip()
                            
                            if start_boundary and end_boundary:
                                print(f"✓ 경계 추출 완료!")
                                print(f"   시작: '{start_boundary[:50]}...'")
                                print(f"   종료: '{end_boundary[:50]}...'")
                                return start_boundary, end_boundary
                            else:
                                print(f"⚠️ 경계 추출 실패, 응답: {response[:200]}...")
            
            return None, None
            
        except Exception as e:
            print(f"❌ Claude SDK 오류: {e}")
            return None, None
    
    def validate_boundaries(self, source_text: str, start_boundary: str, end_boundary: str) -> bool:
        """
        추출된 경계가 원문에 존재하는지 검증합니다.
        
        Args:
            source_text: 원문 텍스트
            start_boundary: 시작 경계 문자열
            end_boundary: 종료 경계 문자열
            
        Returns:
            검증 성공 여부
        """
        start_pos = source_text.find(start_boundary)
        end_pos = source_text.find(end_boundary)
        
        if start_pos == -1:
            print(f"❌ 시작 경계를 원문에서 찾을 수 없습니다: '{start_boundary[:30]}...'")
            return False
        
        if end_pos == -1:
            print(f"❌ 종료 경계를 원문에서 찾을 수 없습니다: '{end_boundary[:30]}...'")
            return False
        
        if start_pos >= end_pos:
            print(f"❌ 시작 위치({start_pos})가 종료 위치({end_pos})보다 늦습니다")
            return False
        
        extracted_length = end_pos - start_pos + len(end_boundary)
        print(f"✓ 경계 검증 완료!")
        print(f"   시작 위치: {start_pos}")
        print(f"   종료 위치: {end_pos}")
        print(f"   추출될 텍스트 길이: {extracted_length:,}자")
        
        return True


async def main():
    """메인 실행 함수"""
    print("🚀 Claude SDK 기반 리프노드 경계 추출기 시작")
    print("=" * 55)
    
    if not CLAUDE_SDK_AVAILABLE:
        print("❌ Claude SDK를 먼저 설치하세요: pip install claude-code-sdk")
        return 1
    
    # 파일 경로 설정
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    target_title = "7.2 JSON Schema in a nutshell"
    
    print(f"📂 원문 파일: {source_path}")
    print(f"📂 리프노드 파일: {nodes_path}")
    print(f"🎯 타겟 섹션: {target_title}")
    
    try:
        # 경계 추출기 생성
        finder = ClaudeBoundaryFinder(debug=True)
        
        # 1. 파일 로드
        print(f"\n📖 파일 로드 중...")
        source_text = finder.load_source_text(source_path)
        leaf_nodes = finder.load_leaf_nodes(nodes_path)
        
        if not source_text or not leaf_nodes:
            print("❌ 파일 로드 실패")
            return 1
        
        # 2. 타겟 노드 찾기
        print(f"\n🔍 타겟 노드 검색 중...")
        target_node = finder.find_target_node(leaf_nodes, target_title)
        
        if not target_node:
            print("❌ 타겟 노드를 찾을 수 없습니다")
            return 1
        
        # 3. 다음 섹션 제목 찾기 (종료점 판단용)
        target_index = next(i for i, node in enumerate(leaf_nodes) if node.get('title') == target_title)
        next_title = leaf_nodes[target_index + 1].get('title') if target_index + 1 < len(leaf_nodes) else None
        
        # 4. Claude SDK로 경계 추출
        print(f"\n🧠 Claude SDK 경계 추출 중...")
        start_boundary, end_boundary = await finder.extract_boundaries_with_claude(
            source_text, target_title, next_title
        )
        
        if not start_boundary or not end_boundary:
            print("❌ 경계 추출 실패")
            return 1
        
        # 5. 경계 검증
        print(f"\n✅ 경계 검증 중...")
        if not finder.validate_boundaries(source_text, start_boundary, end_boundary):
            print("❌ 경계 검증 실패")
            return 1
        
        # 6. 결과 출력
        print(f"\n🎉 경계 추출 완료!")
        print(f"시작 경계: '{start_boundary}'")
        print(f"종료 경계: '{end_boundary}'")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n❌ 사용자에 의해 중단됨")
        return 1
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)