# 생성 시간: Fri Aug  8 10:48:55 KST 2025
# 핵심 내용: 25-08-07 버전과 동일한 형식의 enhanced_toc_with_relationships.json 생성 도구
# 상세 내용:
#   - create_enhanced_toc 함수 (6-35줄): 간단한 id/parent_id/children_ids 구조로 변환하는 주 함수
#   - find_parent_index 함수 (38-49줄): 부모 인덱스를 찾는 헬퍼 함수
#   - find_children_indices 함수 (51-64줄): 자식 인덱스들을 찾는 헬퍼 함수
#   - main 함수 (67-89줄): 파일 처리 및 저장 실행부
# 상태: 활성
# 주소: enhanced_toc_creator
# 참조: core_toc_with_page_ranges_v2.json, enhanced_toc_with_relationships.json (25-08-07)

import json
from typing import List, Dict, Any, Optional

def create_enhanced_toc(toc_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """25-08-07 형식과 동일한 enhanced_toc 생성"""
    enhanced_toc = []
    
    for i, item in enumerate(toc_data):
        enhanced_item = {
            "title": item["title"],
            "level": item["level"],
            "start_page": item["start_page"],
            "end_page": item["end_page"],
            "page_count": item["page_count"],
            "id": i,
            "parent_id": find_parent_index(toc_data, i, item["level"]),
            "children_ids": find_children_indices(toc_data, i, item["level"])
        }
        
        # is_added_node 필드가 있으면 추가
        if "is_added_node" in item:
            enhanced_item["is_added_node"] = item["is_added_node"]
        
        enhanced_toc.append(enhanced_item)
    
    return enhanced_toc

def find_parent_index(toc_data: List[Dict[str, Any]], current_index: int, current_level: int) -> Optional[int]:
    """현재 항목의 부모 인덱스를 찾기"""
    if current_level == 0:
        return None
        
    # 역순으로 탐색하여 바로 상위 레벨 찾기
    for i in range(current_index - 1, -1, -1):
        if toc_data[i]['level'] == current_level - 1:
            return i
    return None

def find_children_indices(toc_data: List[Dict[str, Any]], current_index: int, current_level: int) -> List[int]:
    """현재 항목의 직접 자식 인덱스들을 찾기"""
    children = []
    target_level = current_level + 1
    
    # 다음 항목부터 탐색
    for i in range(current_index + 1, len(toc_data)):
        item_level = toc_data[i]['level']
        
        # 같은 레벨이나 더 상위 레벨이 나오면 탐색 종료
        if item_level <= current_level:
            break
            
        # 직접 자식 (바로 하위 레벨)만 추가
        if item_level == target_level:
            children.append(i)
            
    return children

def main():
    """메인 실행 함수"""
    input_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/core_toc_with_page_ranges_v2.json'
    output_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json'
    
    try:
        # 원본 파일 로드
        with open(input_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
            
        print(f"원본 TOC 항목 수: {len(toc_data)}")
        
        # enhanced_toc 생성
        enhanced_toc = create_enhanced_toc(toc_data)
        
        # 새 파일에 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_toc, f, ensure_ascii=False, indent=2)
            
        print(f"Enhanced TOC 저장 완료: {output_file}")
        
        # 샘플 확인
        print("\n샘플 항목들:")
        for i in [0, 1, 2]:
            sample = enhanced_toc[i]
            print(f"ID {sample['id']}: {sample['title']} (부모: {sample['parent_id']}, 자식: {len(sample['children_ids'])}개)")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()