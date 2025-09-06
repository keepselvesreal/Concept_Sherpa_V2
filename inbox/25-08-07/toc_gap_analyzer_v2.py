#!/usr/bin/env python3
"""
생성 시간: 2025-08-07 10:34 KST
핵심 내용: TOC에서 상위 구성 단위와 하위 구성 단위 사이의 모든 누락된 내용을 완전히 추출하여 JSON으로 저장
상세 내용:
    - load_toc_data(라인 15-25): JSON 파일에서 TOC 데이터 로드
    - find_complete_gaps(라인 27-85): 모든 상위→하위 구성 단위 간격을 완전히 식별
    - validate_gaps(라인 87-105): 추출된 간격의 유효성 검증
    - save_gaps_to_json(라인 107-125): 결과를 JSON 파일로 저장
    - main(라인 127-150): 메인 실행 함수
상태: 활성
주소: toc_gap_analyzer_v2
참고: toc_gap_analyzer.py 원본을 기반으로 수정하여 완전한 간격 추출 기능 추가
"""

import json
from pathlib import Path
from typing import List, Dict, Any

def load_toc_data(file_path: str) -> List[Dict[str, Any]]:
    """TOC JSON 데이터를 로드합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return []

def find_complete_gaps(toc_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """상위 구성 단위와 하위 구성 단위 사이의 모든 간격을 완전히 식별합니다."""
    gaps = []
    
    print("=== 상위→하위 구성 단위 간격 검색 중 ===")
    
    for i, parent_item in enumerate(toc_data):
        parent_level = parent_item.get('level', 0)
        parent_start = parent_item.get('start_page', 0)
        parent_end = parent_item.get('end_page', 0)
        parent_title = parent_item.get('title', '')
        
        # 현재 항목 이후에서 하위 구성 단위들을 찾습니다
        target_level = parent_level + 1
        
        # 첫 번째 직계 하위 구성 단위를 찾습니다
        first_child = None
        first_child_index = None
        
        for j in range(i + 1, len(toc_data)):
            next_item = toc_data[j]
            next_level = next_item.get('level', 0)
            
            # 현재 항목과 같거나 더 상위 level을 만나면 중단 (다른 섹션 시작)
            if next_level <= parent_level:
                break
                
            # 직계 하위 구성 단위를 찾으면 기록
            if next_level == target_level:
                first_child = next_item
                first_child_index = j
                break
        
        # 첫 번째 하위 구성 단위가 있으면 간격 분석
        if first_child:
            child_start = first_child.get('start_page', 0)
            child_title = first_child.get('title', '')
            
            # 간격 정보 생성
            gap_info = {
                'gap_id': len(gaps) + 1,
                'parent': {
                    'title': parent_title,
                    'level': parent_level,
                    'start_page': parent_start,
                    'end_page': parent_end,
                    'index': i
                },
                'first_child': {
                    'title': child_title,
                    'level': target_level,
                    'start_page': child_start,
                    'index': first_child_index
                },
                'gap_analysis': {
                    'gap_start_page': parent_start,
                    'gap_end_page': child_start,
                    'page_gap': child_start - parent_start,
                    'same_page': child_start == parent_start,
                    'has_page_gap': child_start > parent_start,
                    'priority': 'high' if child_start - parent_start > 1 else 'medium' if child_start > parent_start else 'low'
                },
                'content_check_needed': child_start >= parent_start  # 같은 페이지라도 확인 필요
            }
            
            gaps.append(gap_info)
            
            print(f"Gap {gap_info['gap_id']}: {parent_title} (L{parent_level}, p{parent_start}) → {child_title} (L{target_level}, p{child_start}) [간격: {child_start - parent_start}]")
    
    return gaps

def validate_gaps(gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """추출된 간격들의 통계와 검증 정보를 생성합니다."""
    total_gaps = len(gaps)
    same_page_gaps = len([g for g in gaps if g['gap_analysis']['same_page']])
    page_gaps = len([g for g in gaps if g['gap_analysis']['has_page_gap']])
    high_priority = len([g for g in gaps if g['gap_analysis']['priority'] == 'high'])
    medium_priority = len([g for g in gaps if g['gap_analysis']['priority'] == 'medium'])
    low_priority = len([g for g in gaps if g['gap_analysis']['priority'] == 'low'])
    
    return {
        'total_gaps': total_gaps,
        'same_page_gaps': same_page_gaps,
        'page_gaps': page_gaps,
        'priority_distribution': {
            'high': high_priority,
            'medium': medium_priority, 
            'low': low_priority
        },
        'needs_content_check': len([g for g in gaps if g['content_check_needed']])
    }

def save_gaps_to_json(gaps: List[Dict[str, Any]], validation: Dict[str, Any], output_file: str):
    """간격 정보를 JSON 파일로 저장합니다."""
    output_data = {
        'extraction_info': {
            'extraction_time': '2025-08-07 10:34 KST',
            'source_file': 'core_toc_with_page_ranges.json',
            'purpose': '상위 구성 단위와 하위 구성 단위 사이의 누락된 내용 영역 완전 추출'
        },
        'validation_summary': validation,
        'gaps': gaps
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n결과가 {output_file}에 저장되었습니다.")

def main():
    """메인 실행 함수"""
    input_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges.json"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/toc_content_gaps.json"
    
    # 1. TOC 데이터 로드
    toc_data = load_toc_data(input_file)
    if not toc_data:
        print("TOC 데이터를 로드할 수 없습니다.")
        return
    
    print(f"총 {len(toc_data)}개의 TOC 항목을 로드했습니다.\n")
    
    # 2. 완전한 간격 추출
    gaps = find_complete_gaps(toc_data)
    
    # 3. 검증 정보 생성
    validation = validate_gaps(gaps)
    
    # 4. 결과 출력
    print(f"\n=== 추출 결과 요약 ===")
    print(f"총 간격 수: {validation['total_gaps']}")
    print(f"같은 페이지 간격: {validation['same_page_gaps']}")
    print(f"페이지 차이 있는 간격: {validation['page_gaps']}")
    print(f"우선순위 분포: High({validation['priority_distribution']['high']}), Medium({validation['priority_distribution']['medium']}), Low({validation['priority_distribution']['low']})")
    print(f"내용 확인 필요: {validation['needs_content_check']}개")
    
    # 5. JSON 파일로 저장
    save_gaps_to_json(gaps, validation, output_file)

if __name__ == "__main__":
    main()