#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 18:15:30 KST
핵심 내용: has_content 필드가 있거나 리프 노드인 노드만 추출하는 재활용 가능한 스크립트
상세 내용:
- load_nodes (라인 25-40): JSON 노드 파일 로드
- is_leaf_node (라인 45-55): 리프 노드 여부 확인
- filter_content_nodes (라인 60-90): 조건에 맞는 노드 필터링
- save_filtered_nodes (라인 95-115): 필터링된 노드 저장
- main (라인 120-150): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: content_node_filter
참조: has_content 필드나 리프 노드 조건에 따른 노드 필터링
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

def load_nodes(nodes_file: str) -> List[Dict[str, Any]]:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # headers 키가 있는 경우 추출
        if isinstance(nodes, dict) and 'headers' in nodes:
            nodes = nodes['headers']
            
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 오류: {e}")
        return []

def is_leaf_node(node: Dict[str, Any]) -> bool:
    """노드가 리프 노드인지 확인합니다."""
    children_ids = node.get('children_ids', [])
    return not children_ids or len(children_ids) == 0

def filter_content_nodes(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    has_content 필드가 있거나 리프 노드인 노드만 필터링합니다.
    
    Args:
        nodes: 노드 리스트
        
    Returns:
        필터링된 노드 리스트
    """
    filtered_nodes = []
    
    print("🔍 노드 필터링 중...")
    print("   조건 1: has_content 필드가 존재하고 True인 경우")
    print("   조건 2: 리프 노드 (children_ids가 비어있는 경우)")
    print()
    
    for node in nodes:
        node_id = node.get('id', 'Unknown')
        title = node.get('title', 'No Title')
        has_content = node.get('has_content', False)
        is_leaf = is_leaf_node(node)
        
        # 조건 확인
        should_include = False
        reason = ""
        
        if has_content:
            should_include = True
            reason = "has_content = True"
        elif is_leaf:
            should_include = True
            reason = "리프 노드"
        
        if should_include:
            filtered_nodes.append(node)
            print(f"✅ 포함: #{node_id} '{title}' ({reason})")
        else:
            print(f"⏭️  제외: #{node_id} '{title}' (has_content = False, 비-리프 노드)")
    
    print(f"\n📊 필터링 결과:")
    print(f"   - 원본 노드 수: {len(nodes)}개")
    print(f"   - 필터링 후: {len(filtered_nodes)}개")
    print(f"   - 제외된 노드: {len(nodes) - len(filtered_nodes)}개")
    
    return filtered_nodes

def save_filtered_nodes(filtered_nodes: List[Dict[str, Any]], output_file: str) -> bool:
    """필터링된 노드를 새로운 JSON 파일로 저장합니다."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_nodes, f, ensure_ascii=False, indent=2)
        
        print(f"💾 필터링된 노드 저장 완료: {output_file}")
        print(f"   - 저장된 노드 수: {len(filtered_nodes)}개")
        
        return True
        
    except Exception as e:
        print(f"❌ 파일 저장 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("사용법: python content_node_filter.py <노드파일> [출력파일]")
        print("예시: python content_node_filter.py script_node_structure_with_content.json filtered_nodes.json")
        print()
        print("필터링 조건:")
        print("  1. has_content 필드가 True인 노드")
        print("  2. 리프 노드 (children_ids가 비어있는 노드)")
        return
    
    nodes_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"{Path(nodes_file).stem}_filtered.json"
    
    print("📋 내용 노드 필터링 도구")
    print("=" * 60)
    print(f"📄 입력 파일: {nodes_file}")
    print(f"📁 출력 파일: {output_file}")
    
    # 파일 존재 확인
    if not Path(nodes_file).exists():
        print(f"❌ 파일을 찾을 수 없습니다: {nodes_file}")
        return
    
    # 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("❌ 노드 데이터를 로드할 수 없습니다.")
        return
    
    print("\n" + "=" * 60)
    
    # 노드 필터링
    filtered_nodes = filter_content_nodes(nodes)
    
    if filtered_nodes:
        # 필터링된 노드 저장
        if save_filtered_nodes(filtered_nodes, output_file):
            print(f"\n✨ 작업 완료! 필터링된 노드가 '{output_file}'에 저장되었습니다.")
        else:
            print(f"\n❌ 작업 실패: 파일 저장 중 오류가 발생했습니다.")
    else:
        print(f"\n⚠️  조건에 맞는 노드가 없습니다.")

if __name__ == "__main__":
    main()