# 생성 시간: 2025-08-08 16:02:03 KST
# 핵심 내용: enhanced_toc_with_relationships.json에서 파트별 리프 노드 JSON 파일들을 생성
# 상세 내용:
#   - main() 함수 (라인 9-38): 메인 실행 로직, 파일 읽기 및 파트별 JSON 생성 조율
#   - create_part_leaf_nodes() 함수 (라인 40-81): 파트별 리프 노드 추출 및 필드 구성
#   - find_part_leaf_nodes() 함수 (라인 83-105): 특정 파트의 모든 리프 노드 재귀 검색
#   - get_part_name() 함수 (라인 107-115): 파트 제목을 파일명으로 변환
# 상태: 활성
# 주소: create_part_leaf_nodes
# 참조: enhanced_toc_with_relationships (전체 목차 구조)

import json
import os

def main():
    # 파일 경로 설정
    input_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/leaf_nodes_by_parts'
    
    try:
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        print(f"출력 디렉토리 생성/확인: {output_dir}")
        
        # enhanced_toc_with_relationships.json 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            all_nodes = json.load(f)
        
        print(f"전체 노드 개수: {len(all_nodes)}개")
        
        # 파트별 리프 노드 JSON 생성
        create_part_leaf_nodes(all_nodes, output_dir)
        
        print(f"\n✅ 파트별 리프 노드 JSON 파일 생성 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

def create_part_leaf_nodes(all_nodes, output_dir):
    """파트별 리프 노드 추출 및 JSON 파일 생성"""
    
    # 파트 노드들 찾기 (level 0이고 "Part"가 제목에 포함)
    part_nodes = [node for node in all_nodes if node['level'] == 0 and 'Part' in node['title']]
    
    print(f"파트 개수: {len(part_nodes)}개")
    
    for part_node in part_nodes:
        part_id = part_node['id']
        part_title = part_node['title']
        
        print(f"\n🔍 처리 중: {part_title}")
        
        # 해당 파트의 모든 리프 노드 찾기
        leaf_nodes = find_part_leaf_nodes(part_id, all_nodes)
        
        # 리프 노드를 필요한 필드만으로 구성
        part_leaf_data = []
        for leaf_node in leaf_nodes:
            leaf_data = {
                'id': leaf_node['id'],
                'title': leaf_node['title'],
                'level': leaf_node['level'],
                'start_text': '',  # 나중에 Claude SDK로 채워질 예정
                'end_text': ''     # 나중에 Claude SDK로 채워질 예정
            }
            part_leaf_data.append(leaf_data)
        
        # 파트별 JSON 파일 저장
        part_name = get_part_name(part_title)
        output_file = os.path.join(output_dir, f'{part_name}_leaf_nodes.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(part_leaf_data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {len(part_leaf_data)}개 리프 노드 → {output_file}")

def find_part_leaf_nodes(part_id, all_nodes):
    """특정 파트의 모든 리프 노드를 재귀적으로 찾기"""
    leaf_nodes = []
    
    def find_children_recursive(parent_id):
        children = [node for node in all_nodes if node.get('parent_id') == parent_id]
        
        for child in children:
            # 리프 노드인지 확인 (children_ids가 비어있음)
            if len(child.get('children_ids', [])) == 0:
                leaf_nodes.append(child)
            else:
                # 자식이 있으면 재귀적으로 계속 탐색
                find_children_recursive(child['id'])
    
    # 파트 노드의 자식부터 시작
    find_children_recursive(part_id)
    
    # ID 순으로 정렬
    leaf_nodes.sort(key=lambda x: x['id'])
    
    return leaf_nodes

def get_part_name(part_title):
    """파트 제목을 파일명으로 변환"""
    if 'Part 1' in part_title:
        return 'part1'
    elif 'Part 2' in part_title:
        return 'part2' 
    elif 'Part 3' in part_title:
        return 'part3'
    else:
        return 'unknown_part'

if __name__ == "__main__":
    main()