#!/usr/bin/env python3
"""
# claude_leaf_boundary_updater.py

## 생성 시간: 2025-08-10 16:45:10 KST

## 핵심 내용: Claude SDK로 리프노드의 15자 시작/종료 문자열 추출 후 업데이트

## 상세 내용:
- ClaudeLeafBoundaryUpdater (라인 29-179): Claude SDK 기반 리프노드 경계 업데이트 메인 클래스
- load_files (라인 38-68): 원문과 리프노드 파일 로드
- extract_15char_boundaries (라인 70-137): 특정 리프노드의 15자 시작/종료 추출
- update_leaf_node_boundaries (라인 139-162): 리프노드 파일의 start_text, end_text 업데이트
- save_updated_nodes (라인 164-179): 업데이트된 리프노드 저장
- main (라인 182-222): 메인 실행 함수

## 상태: 활성

## 주소: claude_leaf_boundary_updater

## 참조: boundary_extractor_final
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple

# Claude SDK 관련 임포트
try:
    from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("⚠️ Claude SDK가 설치되지 않았습니다.")


class ClaudeLeafBoundaryUpdater:
    """Claude SDK를 사용한 15자 경계 추출 및 리프노드 업데이트"""
    
    def __init__(self, debug: bool = True):
        """
        초기화
        
        Args:
            debug: 디버그 모드 활성화
        """
        self.debug = debug
        self.options = ClaudeCodeOptions(
            system_prompt=(
                "당신은 문서 분석 전문가입니다. "
                "주어진 문서에서 특정 섹션의 시작 부분과 끝 부분에서 "
                "정확히 15자씩 추출하는 것이 목표입니다. "
                "추출한 문자열은 해당 섹션을 고유하게 식별할 수 있어야 합니다."
            ),
            max_turns=1,
            allowed_tools=None
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
    
    async def extract_15char_boundaries(self, source_text: str, target_node: Dict[str, Any], next_node: Optional[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        """
        Claude SDK를 사용해 특정 리프노드의 15자 시작/종료 문자열을 추출합니다.
        
        Args:
            source_text: 전체 원문 텍스트
            target_node: 타겟 리프노드
            next_node: 다음 리프노드 (경계 판단용)
            
        Returns:
            tuple: (15자 시작 문자열, 15자 종료 문자열)
        """
        target_title = target_node.get('title', '')
        target_id = target_node.get('id', 'Unknown')
        next_title = next_node.get('title', '') if next_node else None
        
        # 문서 샘플링 (타겟 주변으로)
        if len(source_text) > 20000:
            target_pos = source_text.find(target_title)
            if target_pos != -1:
                start_sample = max(0, target_pos - 3000)
                end_sample = min(len(source_text), target_pos + 12000)
                source_sample = source_text[start_sample:end_sample]
            else:
                source_sample = source_text[:20000]
        else:
            source_sample = source_text
        
        prompt = f"""
문서에서 "{target_title}" 섹션의 시작과 끝에서 정확히 15자씩 추출해주세요.

요구사항:
1. 시작 15자: 해당 섹션이 시작되는 지점의 첫 15자
2. 종료 15자: 해당 섹션이 끝나는 지점의 마지막 15자
3. 공백과 줄바꿈도 문자로 계산
4. 정확히 15자만 추출

다음 형식으로만 응답:
START_15: [정확히 15자]
END_15: [정확히 15자]

문서:
{source_sample}
"""
        
        try:
            print(f"🧠 Claude SDK로 '{target_title}' (ID: {target_id}) 15자 경계 추출 중...")
            
            async with ClaudeSDKClient(options=self.options) as client:
                await client.query(prompt)
                
                response_text = ""
                async for message in client.receive_response():
                    message_str = str(message)
                    if 'TextBlock' in message_str:
                        import re
                        text_matches = re.findall(r"TextBlock\(text='([^']*)'", message_str)
                        for text in text_matches:
                            response_text += text + " "
                    elif hasattr(message, 'text'):
                        response_text += message.text
                    elif isinstance(message, str):
                        response_text += message
                
                if not response_text.strip():
                    print(f"⚠️ Claude SDK 응답이 비어있음")
                    return None, None
                
                if self.debug:
                    print(f"   📄 Claude 응답: {response_text[:200]}...")
                
                # 15자 경계 추출
                import re
                start_match = re.search(r'START_15:\s*(.{15})', response_text)
                end_match = re.search(r'END_15:\s*(.{15})', response_text)
                
                start_15 = start_match.group(1) if start_match else None
                end_15 = end_match.group(1) if end_match else None
                
                if start_15 and end_15:
                    print(f"✓ 15자 경계 추출 성공!")
                    print(f"   📍 시작 15자: '{start_15}'")
                    print(f"   📍 종료 15자: '{end_15}'")
                    return start_15, end_15
                else:
                    print(f"⚠️ 15자 경계 추출 실패")
                    return None, None
                    
        except Exception as e:
            print(f"❌ Claude SDK 오류: {e}")
            return None, None
    
    def update_leaf_node_boundaries(self, leaf_nodes: List[Dict[str, Any]], target_index: int, start_text: str, end_text: str) -> List[Dict[str, Any]]:
        """
        리프노드의 start_text, end_text를 업데이트합니다.
        
        Args:
            leaf_nodes: 리프노드 리스트
            target_index: 업데이트할 노드 인덱스
            start_text: 15자 시작 문자열
            end_text: 15자 종료 문자열
            
        Returns:
            업데이트된 리프노드 리스트
        """
        updated_nodes = leaf_nodes.copy()
        
        if 0 <= target_index < len(updated_nodes):
            updated_nodes[target_index]['start_text'] = start_text
            updated_nodes[target_index]['end_text'] = end_text
            
            node_title = updated_nodes[target_index].get('title', 'Unknown')
            print(f"✓ 노드 업데이트 완료: '{node_title}'")
            print(f"   start_text: '{start_text}'")
            print(f"   end_text: '{end_text}'")
        else:
            print(f"❌ 잘못된 노드 인덱스: {target_index}")
        
        return updated_nodes
    
    def save_updated_nodes(self, updated_nodes: List[Dict[str, Any]], output_path: str) -> bool:
        """
        업데이트된 리프노드를 파일로 저장합니다.
        
        Args:
            updated_nodes: 업데이트된 리프노드 리스트
            output_path: 출력 파일 경로
            
        Returns:
            저장 성공 여부
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
            print(f"✅ 업데이트된 리프노드 저장 완료: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 파일 저장 실패: {e}")
            return False


async def main():
    """메인 실행 함수"""
    print("🚀 Claude SDK 15자 경계 추출 및 리프노드 업데이트")
    print("=" * 55)
    
    if not CLAUDE_SDK_AVAILABLE:
        print("❌ Claude SDK를 먼저 설치하세요")
        return 1
    
    # 파일 경로 설정
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/Part2_Scalability_Chapter_07_with_boundaries.json"
    
    # 테스트할 리프노드 인덱스 (3번째 = 인덱스 2)
    target_index = 2
    
    try:
        # 업데이터 생성
        updater = ClaudeLeafBoundaryUpdater()
        
        # 파일 로드
        source_text, leaf_nodes = updater.load_files(source_path, nodes_path)
        if not source_text or not leaf_nodes:
            return 1
        
        # 타겟 노드 확인
        if target_index >= len(leaf_nodes):
            print(f"❌ 인덱스 {target_index}의 노드가 존재하지 않습니다")
            return 1
        
        target_node = leaf_nodes[target_index]
        next_node = leaf_nodes[target_index + 1] if target_index + 1 < len(leaf_nodes) else None
        
        print(f"\n🎯 대상 노드: '{target_node.get('title', 'Unknown')}'")
        
        # 15자 경계 추출
        start_15, end_15 = await updater.extract_15char_boundaries(source_text, target_node, next_node)
        
        if not start_15 or not end_15:
            print("❌ 15자 경계 추출 실패")
            return 1
        
        # 리프노드 업데이트
        print(f"\n📝 리프노드 업데이트 중...")
        updated_nodes = updater.update_leaf_node_boundaries(leaf_nodes, target_index, start_15, end_15)
        
        # 파일 저장
        print(f"\n💾 결과 저장 중...")
        if updater.save_updated_nodes(updated_nodes, output_path):
            print(f"\n🎉 작업 완료!")
            print(f"📁 출력 파일: {output_path}")
        else:
            return 1
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)