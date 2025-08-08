#!/usr/bin/env python3
"""
생성 시간: 2025-08-07 10:34 KST
핵심 내용: 수정된 Introduction 번호 체계로 상위-하위 구성 단위 간격에서 Introduction 항목을 생성하고 기존 TOC에 삽입
상세 내용:
    - load_gaps_data(라인 15-25): 간격 데이터 JSON 파일 로드
    - generate_introduction_title(라인 27-70): 올바른 Introduction 번호 체계 생성 (하위 구성 단위보다 앞 순서)
    - create_introduction_items(라인 72-100): Introduction 항목들 생성
    - insert_introductions_to_toc(라인 102-130): 기존 TOC에 Introduction 항목들 삽입
    - save_updated_toc(라인 132-145): 수정된 TOC를 _v3 파일로 저장
    - main(라인 147-170): 메인 실행 함수
상태: 활성
주소: toc_introduction_generator_v2
참고: toc_introduction_generator.py를 기반으로 올바른 번호 체계로 수정
"""

import json
import re
from typing import List, Dict, Any

def load_gaps_data(file_path: str) -> Dict[str, Any]:
    """간격 데이터 JSON 파일을 로드합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return {}

def generate_introduction_title(parent_title: str, child_title: str) -> str:
    """하위 구성 단위보다 앞에 오는 올바른 Introduction 번호 체계를 생성합니다."""
    
    # Child title에서 번호 체계 추출
    child_number = ""
    
    # 패턴 매칭 우선순위에 따라 처리
    patterns = [
        r'^([ABC]\.\d+\.\d+\.\d+)',     # A.1.2.3 등
        r'^([ABC]\.\d+\.\d+)',         # A.1.2 등  
        r'^([ABC]\.\d+)',              # A.1, B.2, C.3 등
        r'^([ABC])',                   # A, B, C
        r'^(\d+\.\d+\.\d+\.\d+)',      # 1.1.1.1 등
        r'^(\d+\.\d+\.\d+)',           # 1.1.1, 2.3.4 등
        r'^(\d+\.\d+)',                # 1.1, 2.3 등  
        r'^(\d+)',                     # 1, 2, 3 등
    ]
    
    for pattern in patterns:
        match = re.match(pattern, child_title.strip())
        if match:
            child_number = match.group(1)
            break
    
    # Introduction 번호 생성 로직 (하위 구성 단위보다 앞에 오도록)
    if child_number:
        if re.match(r'^[ABC]$', child_number):  # A, B, C -> A.0, B.0, C.0
            intro_number = f"{child_number}.0"
        elif re.match(r'^[ABC]\.\d+$', child_number):  # A.1 -> A.0, B.2 -> B.0
            base = child_number.split('.')[0]
            intro_number = f"{base}.0"
        elif re.match(r'^\d+$', child_number):  # 1, 2, 3 -> 0 (Part level)
            intro_number = "0"
        elif re.match(r'^\d+\.\d+$', child_number):  # 1.1 -> 1.0, 2.3 -> 2.0
            base = child_number.split('.')[0]
            intro_number = f"{base}.0"
        elif re.match(r'^\d+\.\d+\.\d+$', child_number):  # 1.1.1 -> 1.1.0, 2.3.4 -> 2.3.0
            parts = child_number.split('.')
            intro_number = f"{parts[0]}.{parts[1]}.0"
        elif re.match(r'^\d+\.\d+\.\d+\.\d+$', child_number):  # 1.1.1.1 -> 1.1.1.0
            parts = child_number.split('.')
            intro_number = f"{parts[0]}.{parts[1]}.{parts[2]}.0"
        else:
            intro_number = "0"
    else:
        intro_number = "0"
    
    return f"{intro_number} Introduction (사용자 추가)"

def create_introduction_items(gaps_data: Dict[str, Any], original_toc: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """간격 데이터를 기반으로 Introduction 항목들을 생성합니다."""
    introduction_items = []
    
    gaps = gaps_data.get('gaps', [])
    
    for gap in gaps:
        # High 또는 Medium priority만 처리 (내용이 있을 가능성이 높은 것들)
        if gap['gap_analysis']['priority'] in ['high', 'medium']:
            parent_title = gap['parent']['title']
            child_title = gap['first_child']['title']
            child_level = gap['first_child']['level']
            gap_start = gap['gap_analysis']['gap_start_page']
            gap_end = gap['gap_analysis']['gap_end_page']
            parent_index = gap['parent']['index']
            
            # Introduction 제목 생성
            intro_title = generate_introduction_title(parent_title, child_title)
            
            # Introduction 항목 생성
            intro_item = {
                'title': intro_title,
                'level': child_level,
                'start_page': gap_start,
                'end_page': gap_end if gap_end > gap_start else gap_start,
                'page_count': max(1, gap_end - gap_start),
                'insert_after_index': parent_index,  # 부모 항목 다음에 삽입
                'source_gap_id': gap['gap_id']
            }
            
            introduction_items.append(intro_item)
            print(f"생성된 Introduction: {intro_title} (Level {child_level}, 페이지 {gap_start}-{intro_item['end_page']})")
    
    return introduction_items

def insert_introductions_to_toc(original_toc: List[Dict[str, Any]], introduction_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """기존 TOC에 Introduction 항목들을 적절한 위치에 삽입합니다."""
    
    # Introduction 항목들을 삽입 위치 순으로 정렬 (뒤에서부터 삽입해야 인덱스가 밀리지 않음)
    introduction_items.sort(key=lambda x: x['insert_after_index'], reverse=True)
    
    updated_toc = original_toc.copy()
    inserted_count = 0
    
    for intro_item in introduction_items:
        insert_position = intro_item['insert_after_index'] + 1
        
        # Introduction 항목을 TOC 형식에 맞게 변환
        toc_item = {
            'title': intro_item['title'],
            'level': intro_item['level'],
            'start_page': intro_item['start_page'],
            'end_page': intro_item['end_page'],
            'page_count': intro_item['page_count']
        }
        
        # 지정된 위치에 삽입
        updated_toc.insert(insert_position, toc_item)
        inserted_count += 1
        
        print(f"삽입됨: {intro_item['title']} at position {insert_position}")
    
    print(f"\n총 {inserted_count}개의 Introduction 항목이 삽입되었습니다.")
    return updated_toc

def save_updated_toc(updated_toc: List[Dict[str, Any]], output_file: str):
    """수정된 TOC를 _v3 파일로 저장합니다."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_toc, f, ensure_ascii=False, indent=2)
    
    print(f"수정된 TOC가 {output_file}에 저장되었습니다.")

def main():
    """메인 실행 함수"""
    gaps_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/toc_content_gaps.json"
    original_toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges.json"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges_v3.json"
    
    # 1. 데이터 로드
    gaps_data = load_gaps_data(gaps_file)
    with open(original_toc_file, 'r', encoding='utf-8') as f:
        original_toc = json.load(f)
    
    if not gaps_data or not original_toc:
        print("필요한 데이터를 로드할 수 없습니다.")
        return
    
    print(f"원본 TOC: {len(original_toc)}개 항목")
    print(f"식별된 간격: {gaps_data['validation_summary']['total_gaps']}개\n")
    
    # 2. Introduction 항목들 생성 (올바른 번호 체계로)
    introduction_items = create_introduction_items(gaps_data, original_toc)
    
    # 3. TOC에 Introduction 항목들 삽입
    updated_toc = insert_introductions_to_toc(original_toc, introduction_items)
    
    # 4. 수정된 TOC 저장
    save_updated_toc(updated_toc, output_file)
    
    print(f"\n최종 TOC: {len(updated_toc)}개 항목 (원본 {len(original_toc)}개 + 추가 {len(introduction_items)}개)")

if __name__ == "__main__":
    main()