# 생성 시간: Sun Aug 31 20:46:37 KST 2025
# 핵심 내용: content_nodes.json 파일에서 다음 항목의 level이 현재 항목보다 큰 경우 end_page를 다음 항목의 start_page로 수정
# 상세 내용:
#   - main(file_path) (라인 8): 메인 함수로 JSON 파일 경로를 받아 처리
#   - update_end_pages(nodes) (라인 28): 노드 리스트에서 end_page 업데이트 로직 수행
#   - save_updated_nodes(nodes, file_path) (라인 46): 수정된 노드 리스트를 JSON 파일로 저장
# 상태: active
# 주소: update_end_pages
# 참조: 없음

import json
import sys

def main(file_path):
    """
    content_nodes.json 파일의 end_page를 업데이트하는 메인 함수
    
    Args:
        file_path (str): content_nodes.json 파일 경로
    """
    try:
        # JSON 파일 로드
        with open(file_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        print(f"원본 파일 로드 완료: {len(nodes)}개 노드")
        
        # end_page 업데이트
        updated_nodes = update_end_pages(nodes)
        
        # 수정된 파일 저장
        save_updated_nodes(updated_nodes, file_path)
        
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)

def update_end_pages(nodes):
    """
    노드 리스트에서 end_page를 업데이트
    
    Args:
        nodes (list): 노드 리스트
        
    Returns:
        list: 업데이트된 노드 리스트
    """
    updated_count = 0
    
    for i in range(len(nodes)):
        current_node = nodes[i]
        
        # 다음 항목이 존재하는지 확인
        if i + 1 < len(nodes):
            next_node = nodes[i + 1]
            
            # 다음 항목의 level이 현재 항목보다 큰 경우
            if next_node['level'] > current_node['level']:
                old_end_page = current_node['end_page']
                new_end_page = next_node['start_page']
                
                # end_page 업데이트
                current_node['end_page'] = new_end_page
                # page_count 재계산
                current_node['page_count'] = new_end_page - current_node['start_page'] + 1
                
                print(f"업데이트: {current_node['title']} - end_page: {old_end_page} → {new_end_page}")
                updated_count += 1
    
    print(f"\n총 {updated_count}개 항목 업데이트 완료")
    return nodes

def save_updated_nodes(nodes, file_path):
    """
    수정된 노드 리스트를 JSON 파일로 저장
    
    Args:
        nodes (list): 수정된 노드 리스트
        file_path (str): 저장할 파일 경로
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)
    
    print(f"수정된 파일 저장 완료: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python update_end_pages.py <content_nodes.json_경로>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)