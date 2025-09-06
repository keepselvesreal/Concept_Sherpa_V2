#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:00 KST
핵심 내용: part2_scalability.json에서 리프 노드만 추출하여 id, title, level만 포함하는 간소화된 JSON 생성
상세 내용:
    - load_json() (line 15-20): JSON 파일 로드
    - filter_leaf_nodes() (line 22-31): children_ids가 빈 배열인 리프 노드 필터링
    - simplify_nodes() (line 33-40): id, title, level만 포함하도록 데이터 간소화
    - save_json() (line 42-48): 결과를 새 JSON 파일로 저장
    - main() (line 50-62): 전체 프로세스 실행
상태: active
주소: part2_scalability_leaf_nodes_simple
참조: part2_scalability.json
"""

import json

def load_json(file_path):
    """JSON 파일 로드"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_leaf_nodes(nodes):
    """리프 노드만 필터링 (children_ids가 빈 배열인 노드들)"""
    leaf_nodes = []
    for node in nodes:
        if node.get('children_ids', []) == []:
            leaf_nodes.append(node)
    return leaf_nodes

def simplify_nodes(nodes):
    """노드에서 id, title, level만 추출"""
    simplified = []
    for node in nodes:
        simplified_node = {
            'id': node['id'],
            'title': node['title'],
            'level': node['level']
        }
        simplified.append(simplified_node)
    return simplified

def save_json(data, file_path):
    """JSON 파일로 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 입력/출력 파일 경로
    input_file = 'part2_scalability.json'
    output_file = 'part2_scalability_leaf_simple.json'
    
    # JSON 로드
    nodes = load_json(input_file)
    
    # 리프 노드 필터링
    leaf_nodes = filter_leaf_nodes(nodes)
    
    # 간소화
    simple_leaf_nodes = simplify_nodes(leaf_nodes)
    
    # 저장
    save_json(simple_leaf_nodes, output_file)
    
    print(f"리프 노드 {len(simple_leaf_nodes)}개를 {output_file}에 저장했습니다.")

if __name__ == '__main__':
    main()