#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 16:27:43 KST
핵심 내용: 노드 구조에 부모-자식 관계를 추가하는 재사용 가능한 스크립트
상세 내용:
- load_nodes (라인 20-30): JSON 파일에서 노드 데이터 로드
- build_hierarchy (라인 35-70): 레벨 기반으로 부모-자식 관계 구축 
- add_parent_child_relationships (라인 75-95): parent_id와 children_ids 필드 추가
- save_nodes (라인 100-110): 업데이트된 노드 구조를 JSON 파일로 저장
- main (라인 115-125): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: node_hierarchy_builder
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json 구조 참조
"""

import json
import sys
from typing import List, Dict, Any, Optional

def load_nodes(file_path: str) -> List[Dict[str, Any]]:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # headers 키가 있는 경우 추출
        if isinstance(nodes, dict) and 'headers' in nodes:
            nodes = nodes['headers']
            
        return nodes
    except Exception as e:
        print(f"파일 로드 오류: {e}")
        return []

def build_hierarchy(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """레벨 기반으로 부모-자식 관계를 구축합니다."""
    
    # 노드를 정렬 (id 순서대로)
    nodes_sorted = sorted(nodes, key=lambda x: x.get('id', 0))
    
    # 각 노드에 parent_id와 children_ids 초기화
    for node in nodes_sorted:
        node['parent_id'] = None
        node['children_ids'] = []
    
    # 부모-자식 관계 구축
    for i, current_node in enumerate(nodes_sorted):
        current_level = current_node.get('level', 0)
        
        # 현재 노드의 부모 찾기 (더 낮은 레벨의 가장 가까운 이전 노드)
        for j in range(i-1, -1, -1):
            potential_parent = nodes_sorted[j]
            parent_level = potential_parent.get('level', 0)
            
            if parent_level < current_level:
                # 부모 발견
                current_node['parent_id'] = potential_parent['id']
                potential_parent['children_ids'].append(current_node['id'])
                break
    
    return nodes_sorted

def add_parent_child_relationships(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """기존 노드 구조에 parent_id와 children_ids 관계를 추가합니다."""
    
    print(f"총 {len(nodes)}개 노드 처리 시작...")
    
    # 계층 구조 빌드
    nodes_with_hierarchy = build_hierarchy(nodes)
    
    # 통계 출력
    root_nodes = [n for n in nodes_with_hierarchy if n['parent_id'] is None]
    leaf_nodes = [n for n in nodes_with_hierarchy if len(n['children_ids']) == 0]
    
    print(f"루트 노드: {len(root_nodes)}개")
    print(f"리프 노드: {len(leaf_nodes)}개")
    print(f"계층 구조 구축 완료")
    
    return nodes_with_hierarchy

def save_nodes(nodes: List[Dict[str, Any]], output_path: str) -> None:
    """업데이트된 노드 구조를 JSON 파일로 저장합니다."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        print(f"결과가 {output_path}에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 오류: {e}")

def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("사용법: python node_hierarchy_builder.py <input_file> [output_file]")
        print("예시: python node_hierarchy_builder.py script_node_structure.json")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file
    
    print(f"입력 파일: {input_file}")
    print(f"출력 파일: {output_file}")
    
    # 노드 로드
    nodes = load_nodes(input_file)
    if not nodes:
        print("노드를 로드할 수 없습니다.")
        return
    
    # 계층 관계 추가
    nodes_with_hierarchy = add_parent_child_relationships(nodes)
    
    # 결과 저장
    save_nodes(nodes_with_hierarchy, output_file)

if __name__ == "__main__":
    main()