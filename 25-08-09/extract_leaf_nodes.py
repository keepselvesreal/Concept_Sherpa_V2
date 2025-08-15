#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:49:54 KST
핵심 내용: 각 파트별 JSON에서 리프 노드만 추출하여 text_boundaries 형식으로 저장
상세 내용:
  - load_json_data (라인 21-26): JSON 파일 로드 함수
  - is_leaf_node (라인 28-31): 리프 노드 판별 함수
  - extract_leaf_nodes (라인 33-46): 리프 노드 추출 및 형식 변환
  - process_part_files (라인 48-73): 파트별 파일 처리
상태: 활성
주소: extract_leaf_nodes
참조: part별 JSON 파일들
"""

import json
import os

def load_json_data(file_path):
    """JSON 파일을 로드하여 반환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_leaf_node(node):
    """리프 노드인지 확인 (children_ids가 비어있으면 리프 노드)"""
    return len(node.get('children_ids', [])) == 0

def extract_leaf_nodes(data):
    """리프 노드만 추출하여 text_boundaries 형식으로 변환"""
    leaf_nodes = []
    
    for node in data:
        if is_leaf_node(node):
            leaf_node = {
                "id": node["id"],
                "title": node["title"], 
                "level": node["level"],
                "start_text": "",
                "end_text": ""
            }
            leaf_nodes.append(leaf_node)
    
    return leaf_nodes

def process_part_files():
    """모든 파트 파일을 처리하여 리프 노드 추출"""
    input_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09'
    
    # 처리할 파일 목록
    part_files = [
        {'input': 'part1_flexibility.json', 'output': 'part1_flexibility_leaf_nodes.json'},
        {'input': 'part2_scalability.json', 'output': 'part2_scalability_leaf_nodes.json'},
        {'input': 'part3_maintainability.json', 'output': 'part3_maintainability_leaf_nodes.json'},
        {'input': 'appendix_a_principles.json', 'output': 'appendix_a_principles_leaf_nodes.json'},
        {'input': 'appendix_b_generic_access.json', 'output': 'appendix_b_generic_access_leaf_nodes.json'},
        {'input': 'appendix_c_paradigms.json', 'output': 'appendix_c_paradigms_leaf_nodes.json'},
        {'input': 'appendix_d_lodash.json', 'output': 'appendix_d_lodash_leaf_nodes.json'}
    ]
    
    # 각 파트별로 처리
    for file_info in part_files:
        input_path = os.path.join(input_dir, file_info['input'])
        output_path = os.path.join(input_dir, file_info['output'])
        
        # 데이터 로드
        data = load_json_data(input_path)
        
        # 리프 노드 추출
        leaf_nodes = extract_leaf_nodes(data)
        
        # 결과 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(leaf_nodes, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {file_info['input']} → {file_info['output']} ({len(leaf_nodes)} leaf nodes)")

if __name__ == "__main__":
    process_part_files()