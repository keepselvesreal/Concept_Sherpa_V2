# 생성 시간: Fri Aug  8 10:45:28 KST 2025
# 핵심 내용: TOC JSON 파일에 부모-자식 관계 필드를 추가하는 도구
# 상세 내용:
#   - add_hierarchy_relationships 함수 (6-42줄): 목차 항목들에 부모-자식 관계 정보를 추가하는 주 함수
#   - find_parent_index 함수 (45-56줄): 현재 항목의 부모 인덱스를 찾는 헬퍼 함수 
#   - find_children_indices 함수 (58-71줄): 현재 항목의 자식 인덱스들을 찾는 헬퍼 함수
#   - main 함수 (74-95줄): 파일 처리 및 새 파일 저장 실행부
# 상태: 활성
# 주소: toc_relationship_enhancer
# 참조: core_toc_with_page_ranges_v2.json

import json
from typing import List, Dict, Any, Optional

def add_hierarchy_relationships(toc_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """TOC 데이터에 부모-자식 관계 정보를 추가"""
    enhanced_toc = []
    
    for i, item in enumerate(toc_data):
        enhanced_item = item.copy()
        current_level = item['level']
        
        # 부모 찾기
        parent_index = find_parent_index(toc_data, i, current_level)
        if parent_index is not None:
            enhanced_item['parent_index'] = parent_index
            enhanced_item['parent_title'] = toc_data[parent_index]['title']
        else:
            enhanced_item['parent_index'] = None
            enhanced_item['parent_title'] = None
            
        # 자식 찾기
        children_indices = find_children_indices(toc_data, i, current_level)
        enhanced_item['children_indices'] = children_indices
        enhanced_item['children_count'] = len(children_indices)
        
        # 자식 제목 목록
        if children_indices:
            enhanced_item['children_titles'] = [
                toc_data[idx]['title'] for idx in children_indices
            ]
        else:
            enhanced_item['children_titles'] = []
            
        # 계층 경로 (root부터 현재까지)
        path_indices = []
        current_idx = i
        while True:
            parent_idx = find_parent_index(toc_data, current_idx, toc_data[current_idx]['level'])
            if parent_idx is None:
                break
            path_indices.insert(0, parent_idx)
            current_idx = parent_idx
            
        enhanced_item['hierarchy_path'] = path_indices + [i]
        enhanced_item['depth'] = len(path_indices)
        
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
    output_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/core_toc_with_relationships.json'
    
    try:
        # 원본 파일 로드
        with open(input_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
            
        print(f"원본 TOC 항목 수: {len(toc_data)}")
        
        # 관계 정보 추가
        enhanced_toc = add_hierarchy_relationships(toc_data)
        
        # 새 파일에 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_toc, f, ensure_ascii=False, indent=2)
            
        print(f"관계 정보가 추가된 TOC 저장 완료: {output_file}")
        
        # 샘플 확인
        print("\n샘플 항목 (인덱스 2):")
        sample = enhanced_toc[2]
        print(f"제목: {sample['title']}")
        print(f"레벨: {sample['level']}")
        print(f"부모: {sample['parent_title']}")
        print(f"자식 수: {sample['children_count']}")
        print(f"계층 깊이: {sample['depth']}")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()