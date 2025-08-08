#!/usr/bin/env python3
"""
완전성 검증 스크립트 - TDD 방식
expected_introductions.json의 예상 결과와 실제 toc_normalizer.py 결과를 비교하여
누락된 Introduction 항목들을 식별합니다.
"""

import json
import re
from pathlib import Path
from typing import List, Set, Dict


def load_expected_introductions(json_file: str) -> List[Dict]:
    """예상 Introduction 항목들 로드"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['expected_introductions']


def extract_actual_introductions(normalized_toc_file: str) -> List[Dict]:
    """실제 생성된 TOC에서 Introduction 항목들 추출"""
    with open(normalized_toc_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    actual_introductions = []
    
    for line_idx, line in enumerate(lines):
        line = line.strip()
        
        # Introduction (사용자 추가) 패턴 찾기
        if "Introduction (사용자 추가)" in line:
            # 번호 추출
            match = re.search(r'(\d+(?:\.\d+)*\.0|[A-Z]\.\d+(?:\.\d+)*\.0)', line)
            if match:
                intro_number = match.group(1)
                actual_introductions.append({
                    'intro_number': intro_number,
                    'line_index': line_idx + 1,
                    'raw_line': line
                })
    
    return actual_introductions


def normalize_intro_numbers(expected_intros: List[Dict]) -> Set[str]:
    """예상 Introduction 번호들을 정규화하여 Set으로 변환"""
    normalized = set()
    
    for intro in expected_intros:
        intro_num = intro['intro_number']
        normalized.add(intro_num)
    
    return normalized


def compare_results(expected_file: str, actual_file: str) -> Dict:
    """예상 결과와 실제 결과 비교"""
    print("=== TDD 완전성 검증 ===")
    
    # 예상 결과 로드
    expected_intros = load_expected_introductions(expected_file)
    expected_numbers = normalize_intro_numbers(expected_intros)
    
    print(f"예상 Introduction 항목 수: {len(expected_numbers)}")
    
    # 실제 결과 로드
    if not Path(actual_file).exists():
        print(f"실제 TOC 파일이 없습니다: {actual_file}")
        return {
            'status': 'FAIL',
            'expected_count': len(expected_numbers),
            'actual_count': 0,
            'missing_count': len(expected_numbers),
            'missing_items': list(expected_numbers)
        }
    
    actual_intros = extract_actual_introductions(actual_file)
    actual_numbers = {intro['intro_number'] for intro in actual_intros}
    
    print(f"실제 Introduction 항목 수: {len(actual_numbers)}")
    
    # 비교 분석
    missing_numbers = expected_numbers - actual_numbers
    extra_numbers = actual_numbers - expected_numbers
    
    print(f"누락된 항목 수: {len(missing_numbers)}")
    print(f"추가 항목 수: {len(extra_numbers)}")
    
    # 상세 분석
    result = {
        'status': 'PASS' if len(missing_numbers) == 0 else 'FAIL',
        'expected_count': len(expected_numbers),
        'actual_count': len(actual_numbers),
        'missing_count': len(missing_numbers),
        'extra_count': len(extra_numbers),
        'missing_items': sorted(list(missing_numbers)),
        'extra_items': sorted(list(extra_numbers))
    }
    
    # 결과 출력
    if result['status'] == 'PASS':
        print("✅ 모든 예상 Introduction 항목이 생성되었습니다!")
    else:
        print("❌ 누락된 Introduction 항목들이 있습니다:")
        
        if missing_numbers:
            print(f"\n누락된 항목들 ({len(missing_numbers)}개):")
            missing_with_context = []
            for intro in expected_intros:
                if intro['intro_number'] in missing_numbers:
                    missing_with_context.append(intro)
            
            # 번호 순으로 정렬
            missing_with_context.sort(key=lambda x: (
                len(x['intro_number'].split('.')),
                x['intro_number']
            ))
            
            for i, intro in enumerate(missing_with_context, 1):
                print(f"  {i:2d}. {intro['intro_number']} - "
                      f"between {intro['parent_number']} '{intro['parent_title']}' "
                      f"and {intro['child_number']} '{intro['child_title']}'")
        
        if extra_numbers:
            print(f"\n추가 항목들 ({len(extra_numbers)}개):")
            for i, extra in enumerate(sorted(extra_numbers), 1):
                print(f"  {i:2d}. {extra}")
    
    return result


def generate_missing_items_report(expected_file: str, actual_file: str, output_file: str) -> None:
    """누락된 항목들에 대한 상세 보고서 생성"""
    result = compare_results(expected_file, actual_file)
    
    if result['status'] == 'PASS':
        report = {
            'status': 'PASS',
            'message': 'All expected Introduction items are present',
            'summary': result
        }
    else:
        # 누락된 항목들의 상세 정보
        expected_intros = load_expected_introductions(expected_file)
        missing_details = []
        
        for intro in expected_intros:
            if intro['intro_number'] in result['missing_items']:
                missing_details.append({
                    'intro_number': intro['intro_number'],
                    'parent_number': intro['parent_number'],
                    'parent_title': intro['parent_title'],
                    'child_number': intro['child_number'],
                    'child_title': intro['child_title'],
                    'content_lines': intro['content_lines']
                })
        
        # 번호 순으로 정렬
        missing_details.sort(key=lambda x: (
            len(x['intro_number'].split('.')),
            x['intro_number']
        ))
        
        report = {
            'status': 'FAIL',
            'message': f'{len(result["missing_items"])} Introduction items are missing',
            'summary': result,
            'missing_details': missing_details,
            'next_steps': [
                '1. toc_normalizer.py의 파싱 패턴 개선',
                '2. Appendix 섹션 (A.1, B.2, C.3 등) 처리 추가',
                '3. Part 레벨 내용 검증 추가',
                '4. PDF 섹션 찾기 알고리즘 개선'
            ]
        }
    
    # 보고서 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n완전성 보고서 저장: {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='TOC 정교화 완전성 검증')
    parser.add_argument('--expected', required=True, help='예상 결과 JSON 파일')
    parser.add_argument('--actual', required=True, help='실제 정교화된 TOC 파일')
    parser.add_argument('--report', required=True, help='완전성 보고서 출력 파일')
    
    args = parser.parse_args()
    
    try:
        generate_missing_items_report(args.expected, args.actual, args.report)
        return 0
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())