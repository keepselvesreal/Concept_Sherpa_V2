#!/usr/bin/env python3
"""
# dynamic_boundary_extractor.py

## 생성 시간: 2025-08-10 16:15:10 KST

## 핵심 내용: Claude SDK를 사용한 동적 리프노드 섹션 경계 추출 (일반화 가능)

## 상세 내용:
- DynamicBoundaryExtractor (라인 29-189): Claude SDK 기반 동적 경계 추출 메인 클래스
- load_files (라인 38-68): 원문과 리프노드 파일 로드
- extract_leaf_node_boundaries (라인 70-139): 특정 리프노드의 섹션 경계를 Claude SDK로 추출
- find_context_nodes (라인 141-165): 이전/다음 노드 컨텍스트 파악
- validate_extracted_boundaries (라인 167-189): 추출된 경계 검증
- main (라인 192-232): 메인 실행 함수 (3번째 리프노드로 테스트)

## 상태: 활성

## 주소: dynamic_boundary_extractor

## 참조: claude_boundary_finder_v2
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Claude SDK 관련 임포트
try:
    from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("⚠️ Claude SDK가 설치되지 않았습니다.")


class DynamicBoundaryExtractor:
    """일반화된 동적 리프노드 경계 추출기"""
    
    def __init__(self, debug: bool = True):
        """
        초기화
        
        Args:
            debug: 디버그 모드 활성화
        """
        self.debug = debug
        self.options = ClaudeCodeOptions(
            system_prompt=(
                "당신은 문서 구조 분석 전문가입니다. "
                "주어진 문서에서 특정 섹션의 정확한 시작과 끝을 식별하는 것이 목표입니다. "
                "섹션 경계는 해당 섹션의 내용만 포함하고 다른 섹션과 중복되지 않아야 합니다. "
                "고유하고 정확한 경계 문자열을 제공해주세요. "
                "도구 사용 없이 텍스트 분석만으로 응답해주세요."
            ),
            max_turns=1,
            allowed_tools=None  # 도구 사용 완전 비활성화
        )
    
    def load_files(self, source_path: str, nodes_path: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        원문과 리프노드 파일을 로드합니다.
        
        Args:
            source_path: 원문 파일 경로
            nodes_path: 리프노드 파일 경로
            
        Returns:
            tuple: (원문 텍스트, 리프노드 리스트)
        """
        # 원문 로드
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                source_text = f.read()
            print(f"✓ 원문 로드 완료: {len(source_text):,}자")
        except Exception as e:
            print(f"❌ 원문 로드 실패: {e}")
            return "", []
        
        # 리프노드 로드
        try:
            with open(nodes_path, 'r', encoding='utf-8') as f:
                leaf_nodes = json.load(f)
            print(f"✓ 리프노드 로드 완료: {len(leaf_nodes)}개")
        except Exception as e:
            print(f"❌ 리프노드 로드 실패: {e}")
            return source_text, []
        
        return source_text, leaf_nodes
    
    async def extract_leaf_node_boundaries(self, source_text: str, target_node: Dict[str, Any], prev_node: Optional[Dict[str, Any]], next_node: Optional[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        """
        Claude SDK를 사용해 특정 리프노드의 섹션 경계를 동적으로 추출합니다.
        
        Args:
            source_text: 전체 원문 텍스트
            target_node: 추출할 타겟 리프노드
            prev_node: 이전 리프노드 (컨텍스트용)
            next_node: 다음 리프노드 (컨텍스트용)
            
        Returns:
            tuple: (시작 경계 문자열, 종료 경계 문자열)
        """
        target_title = target_node.get('title', '')
        target_id = target_node.get('id', 'Unknown')
        
        # 컨텍스트 정보 구성
        context_info = []
        if prev_node:
            context_info.append(f"이전 섹션: '{prev_node.get('title', '')}'")
        if next_node:
            context_info.append(f"다음 섹션: '{next_node.get('title', '')}'")
        context_str = " | ".join(context_info) if context_info else "단독 섹션"
        
        # 문서가 너무 길면 타겟 주변으로 샘플링
        if len(source_text) > 20000:
            target_pos = source_text.find(target_title)
            if target_pos != -1:
                start_sample = max(0, target_pos - 3000)
                end_sample = min(len(source_text), target_pos + 12000)
                source_sample = source_text[start_sample:end_sample]
                print(f"   📏 문서 샘플링: {len(source_sample):,}자 (전체 {len(source_text):,}자)")
            else:
                source_sample = source_text[:20000]
                print(f"   📏 문서 앞부분 샘플링: {len(source_sample):,}자")
        else:
            source_sample = source_text
        
        prompt = f"""
다음 문서에서 "{target_title}" 섹션의 정확한 경계를 찾아주세요.

섹션 컨텍스트: {context_str}

요구사항:
1. 시작 경계: "{target_title}" 섹션이 시작되는 지점의 고유한 문자열 (30-50자)
2. 종료 경계: 해당 섹션이 끝나는 지점의 고유한 문자열 (30-50자)
3. 경계는 해당 섹션에서만 나타나는 고유한 패턴이어야 함
4. 다른 섹션과 겹치지 않도록 정확한 경계 설정

정확히 다음 형식으로만 응답해주세요:
START_BOUNDARY: [시작 경계 문자열]
END_BOUNDARY: [종료 경계 문자열]

문서:
{source_sample}
"""
        
        try:
            print(f"🧠 Claude SDK로 '{target_title}' (ID: {target_id}) 경계 추출 중...")
            
            async with ClaudeSDKClient(options=self.options) as client:
                # 쿼리 실행
                await client.query(prompt)
                
                # 응답 수신
                response_text = ""
                async for message in client.receive_response():
                    # TextBlock에서 텍스트 추출
                    message_str = str(message)
                    if 'TextBlock' in message_str:
                        # TextBlock에서 텍스트 부분 추출
                        import re
                        text_matches = re.findall(r"TextBlock\(text='([^']*)'", message_str)
                        for text in text_matches:
                            response_text += text + " "
                    elif hasattr(message, 'text'):
                        response_text += message.text
                    elif isinstance(message, str):
                        response_text += message
                
                if not response_text:
                    print(f"⚠️ Claude SDK 응답이 비어있음")
                    return None, None
                
                # 응답에서 경계 추출 (유연한 파싱)
                if self.debug:
                    print(f"   📄 Claude 응답: {response_text[:500]}...")
                
                # 정규표현식으로 경계 추출
                import re
                start_match = re.search(r'START_BOUNDARY:\s*(.+)', response_text, re.IGNORECASE)
                end_match = re.search(r'END_BOUNDARY:\s*(.+)', response_text, re.IGNORECASE)
                reasoning_match = re.search(r'REASONING:\s*(.+)', response_text, re.IGNORECASE)
                
                start_boundary = None
                end_boundary = None
                reasoning = None
                
                if start_match:
                    start_boundary = start_match.group(1).strip().strip('`').strip('"').strip("'")
                if end_match:
                    end_boundary = end_match.group(1).strip().strip('`').strip('"').strip("'")
                if reasoning_match:
                    reasoning = reasoning_match.group(1).strip()
                
                if start_boundary and end_boundary:
                    print(f"✓ 경계 추출 성공!")
                    if reasoning and self.debug:
                        print(f"   💭 추출 근거: {reasoning}")
                    print(f"   📍 시작: '{start_boundary[:40]}...'")
                    print(f"   📍 종료: '...{end_boundary[-40:]}'")
                    return start_boundary, end_boundary
                else:
                    print(f"⚠️ 경계 추출 실패")
                    if self.debug:
                        print(f"   응답: {response_text[:300]}...")
                    return None, None
            
        except Exception as e:
            print(f"❌ Claude SDK 오류: {e}")
            return None, None
    
    def find_context_nodes(self, leaf_nodes: List[Dict[str, Any]], target_index: int) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        타겟 노드의 이전/다음 노드를 찾습니다.
        
        Args:
            leaf_nodes: 전체 리프노드 리스트
            target_index: 타겟 노드의 인덱스
            
        Returns:
            tuple: (이전 노드, 다음 노드)
        """
        prev_node = leaf_nodes[target_index - 1] if target_index > 0 else None
        next_node = leaf_nodes[target_index + 1] if target_index < len(leaf_nodes) - 1 else None
        
        if prev_node:
            print(f"   ← 이전: {prev_node.get('title', 'Unknown')}")
        if next_node:
            print(f"   → 다음: {next_node.get('title', 'Unknown')}")
            
        return prev_node, next_node
    
    def validate_extracted_boundaries(self, source_text: str, start_boundary: str, end_boundary: str) -> bool:
        """
        추출된 경계가 원문에 존재하고 유효한지 검증합니다.
        
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
            print(f"❌ 시작 경계를 원문에서 찾을 수 없습니다")
            return False
        
        if end_pos == -1:
            print(f"❌ 종료 경계를 원문에서 찾을 수 없습니다")
            return False
        
        if start_pos >= end_pos:
            print(f"❌ 시작 위치({start_pos})가 종료 위치({end_pos})보다 늦습니다")
            return False
        
        section_length = end_pos - start_pos + len(end_boundary)
        print(f"✅ 경계 검증 완료! 섹션 길이: {section_length:,}자")
        
        return True


async def main():
    """메인 실행 함수 - 3번째 리프노드로 테스트"""
    print("🚀 동적 리프노드 경계 추출기 시작 (3번째 노드 테스트)")
    print("=" * 60)
    
    if not CLAUDE_SDK_AVAILABLE:
        print("❌ Claude SDK를 먼저 설치하세요")
        return 1
    
    # 파일 경로
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    
    try:
        # 추출기 생성
        extractor = DynamicBoundaryExtractor()
        
        # 파일 로드
        source_text, leaf_nodes = extractor.load_files(source_path, nodes_path)
        if not source_text or not leaf_nodes:
            return 1
        
        # 3번째 리프노드 선택 (인덱스 2)
        target_index = 2
        if target_index >= len(leaf_nodes):
            print(f"❌ 3번째 리프노드가 존재하지 않습니다 (총 {len(leaf_nodes)}개)")
            return 1
        
        target_node = leaf_nodes[target_index]
        print(f"\n🎯 테스트 대상: {target_index + 1}번째 노드")
        print(f"   제목: {target_node.get('title', 'Unknown')}")
        print(f"   ID: {target_node.get('id', 'Unknown')}")
        
        # 컨텍스트 노드 찾기
        prev_node, next_node = extractor.find_context_nodes(leaf_nodes, target_index)
        
        # 경계 추출
        print(f"\n🔍 동적 경계 추출 시작...")
        start_boundary, end_boundary = await extractor.extract_leaf_node_boundaries(
            source_text, target_node, prev_node, next_node
        )
        
        if not start_boundary or not end_boundary:
            print("❌ 경계 추출 실패")
            return 1
        
        # 검증
        print(f"\n🔎 경계 검증 중...")
        if not extractor.validate_extracted_boundaries(source_text, start_boundary, end_boundary):
            return 1
        
        # 최종 결과
        print(f"\n🎉 동적 경계 추출 성공!")
        print(f"📝 시작 경계: '{start_boundary}'")
        print(f"📝 종료 경계: '{end_boundary}'")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)