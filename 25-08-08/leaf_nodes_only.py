# 생성 시간: 2025-08-08 12:05:04 KST
# 핵심 내용: enhanced_toc_with_relationships.json에서 리프 노드만 추출하여 id, title, level 필드만 포함된 JSON 파일 생성
# 상세 내용:
#   - main() 함수 (라인 8-35): 메인 실행 로직, 파일 읽기 및 리프 노드 추출 및 저장
#   - extract_leaf_nodes() 함수 (라인 37-46): 리프 노드 필터링 및 필요 필드만 추출
# 상태: 활성
# 주소: leaf_nodes_only
# 참조: 없음

import json

def main():
    # 입력 파일 경로
    input_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json'
    output_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/leaf_nodes_only.json'
    
    try:
        # JSON 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"전체 노드 개수: {len(data)}")
        
        # 리프 노드 추출
        leaf_nodes = extract_leaf_nodes(data)
        
        print(f"리프 노드 개수: {len(leaf_nodes)}")
        
        # 결과를 JSON 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(leaf_nodes, f, ensure_ascii=False, indent=2)
        
        print(f"리프 노드가 {output_file}에 저장되었습니다.")
        
        # 처음 5개 리프 노드 출력
        print("\n처음 5개 리프 노드:")
        for i, node in enumerate(leaf_nodes[:5]):
            print(f"{i+1}. ID: {node['id']}, Level: {node['level']}, Title: {node['title']}")
            
    except Exception as e:
        print(f"오류 발생: {e}")

def extract_leaf_nodes(data):
    """리프 노드만 추출하여 id, title, level 필드만 반환"""
    leaf_nodes = []
    
    for node in data:
        # children_ids가 비어있는 노드가 리프 노드
        if 'children_ids' in node and len(node['children_ids']) == 0:
            leaf_nodes.append({
                'id': node['id'],
                'title': node['title'],
                'level': node['level']
            })
    
    return leaf_nodes

if __name__ == "__main__":
    main()