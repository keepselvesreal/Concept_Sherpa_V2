#!/usr/bin/env python3
"""
생성 시간: 2025-08-07 10:16 KST
핵심 내용: TOC 구조에서 서로 다른 level의 구성 단위 사이에 누락된 내용 영역을 식별하고 분석하는 도구
상세 내용:
    - load_toc_data(라인 15-25): JSON 파일에서 TOC 데이터 로드
    - find_level_gaps(라인 27-60): 모든 level 간의 누락된 내용 영역 식별
    - analyze_page_gaps(라인 62-85): 페이지 범위 분석 및 실제 내용 존재 여부 판단
    - generate_introduction_items(라인 87-110): Introduction 항목 생성
    - main(라인 112-130): 메인 실행 함수
상태: 활성
주소: toc_gap_analyzer
참고: core_toc_with_page_ranges.json 파일을 기반으로 작성
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

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

def find_level_gaps(toc_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """모든 level에서 상위-하위 구성 단위 사이의 누락된 내용 영역을 식별합니다."""
    gaps = []
    
    for i, item in enumerate(toc_data):
        current_level = item.get('level', 0)
        current_start = item.get('start_page', 0)
        current_title = item.get('title', '')
        
        # 다음 항목들 중에서 현재 level보다 1 높은 첫 번째 항목을 찾습니다
        target_level = current_level + 1
        next_child = None
        
        for j in range(i + 1, len(toc_data)):
            next_item = toc_data[j]
            next_level = next_item.get('level', 0)
            
            # 더 깊은 level을 만나면 계속 진행
            if next_level > target_level:
                continue
            # 같은 level 이하를 만나면 중단
            elif next_level <= current_level:
                break
            # target_level과 같으면 찾은 것
            elif next_level == target_level:
                next_child = next_item
                break
        
        # 하위 구성 단위가 있고, 페이지 간격이 있으면 gap으로 간주
        if next_child:
            child_start = next_child.get('start_page', 0)
            
            # 페이지 간격이 있거나 같은 페이지인 경우 모두 확인 대상
            if child_start >= current_start:
                gap_info = {
                    'parent_title': current_title,
                    'parent_level': current_level,
                    'parent_start_page': current_start,
                    'child_title': next_child.get('title', ''),
                    'child_level': target_level,
                    'child_start_page': child_start,
                    'gap_start_page': current_start,
                    'gap_end_page': child_start,
                    'page_gap': child_start - current_start,
                    'needs_check': True  # 실제 내용 확인 필요
                }
                gaps.append(gap_info)
    
    return gaps

def analyze_page_gaps(gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """페이지 간격을 분석하고 실제 내용 존재 가능성을 판단합니다."""
    analyzed_gaps = []
    
    for gap in gaps:
        gap_start = gap['gap_start_page']
        gap_end = gap['gap_end_page']
        page_gap = gap['page_gap']
        
        # 분석 결과 추가
        gap['analysis'] = {
            'same_page': page_gap == 0,
            'one_page_gap': page_gap == 1,
            'multi_page_gap': page_gap > 1,
            'likely_has_content': page_gap >= 1,  # 1페이지 이상 차이면 내용 있을 가능성 높음
            'priority': 'high' if page_gap > 1 else 'medium' if page_gap == 1 else 'low'
        }
        
        analyzed_gaps.append(gap)
    
    return analyzed_gaps

def generate_introduction_items(gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Introduction 항목들을 생성합니다."""
    introduction_items = []
    
    for gap in gaps:
        if gap['analysis']['likely_has_content']:
            # Introduction 항목 생성
            intro_item = {
                'title': f"{gap['parent_title']} Introduction (사용자 추가)",
                'level': gap['child_level'],  # 하위 구성 단위와 같은 level
                'start_page': gap['gap_start_page'],
                'end_page': gap['gap_end_page'] if gap['page_gap'] > 0 else gap['gap_start_page'],
                'page_count': max(1, gap['page_gap']),
                'insert_after_index': None,  # 나중에 원본 데이터에서 위치 찾기
                'source_gap': gap
            }
            introduction_items.append(intro_item)
    
    return introduction_items

def main():
    """메인 실행 함수"""
    input_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges.json"
    
    # 1. TOC 데이터 로드
    toc_data = load_toc_data(input_file)
    if not toc_data:
        print("TOC 데이터를 로드할 수 없습니다.")
        return
    
    print(f"총 {len(toc_data)}개의 TOC 항목을 로드했습니다.\n")
    
    # 2. 레벨 간 간격 식별
    gaps = find_level_gaps(toc_data)
    print(f"식별된 level 간 간격: {len(gaps)}개\n")
    
    # 3. 페이지 간격 분석
    analyzed_gaps = analyze_page_gaps(gaps)
    
    # 4. 결과 출력
    print("=== 식별된 누락된 내용 영역 ===")
    for i, gap in enumerate(analyzed_gaps, 1):
        print(f"\n{i}. {gap['parent_title']} (level {gap['parent_level']}) → {gap['child_title']} (level {gap['child_level']})")
        print(f"   페이지 범위: {gap['gap_start_page']} → {gap['gap_end_page']} (간격: {gap['page_gap']})")
        print(f"   분석: {gap['analysis']}")
    
    # 5. Introduction 항목 생성
    introduction_items = generate_introduction_items(analyzed_gaps)
    print(f"\n=== 생성될 Introduction 항목: {len(introduction_items)}개 ===")
    for i, item in enumerate(introduction_items, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   Level: {item['level']}, 페이지: {item['start_page']}-{item['end_page']}")

if __name__ == "__main__":
    main()