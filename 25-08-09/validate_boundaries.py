#!/usr/bin/env python3
"""
추출된 경계 마커 검증 스크립트

생성된 JSON 파일의 경계 마커들이 실제로 원본 텍스트에서 
정확히 섹션을 추출할 수 있는지 검증합니다.
"""

import json
import re
from typing import Dict, List, Tuple


def normalize_for_comparison(text: str) -> str:
    """비교를 위한 텍스트 정규화"""
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def fuzzy_find(haystack: str, needle: str, threshold: float = 0.8) -> int:
    """유사도 기반 텍스트 검색"""
    needle_norm = normalize_for_comparison(needle)
    
    # 정확한 매칭 시도
    pos = haystack.find(needle_norm)
    if pos >= 0:
        return pos
    
    # 부분 매칭 시도 (처음 50자만)
    needle_short = needle_norm[:50]
    pos = haystack.find(needle_short)
    if pos >= 0:
        return pos
    
    return -1


def extract_section_by_boundaries(chapter_text: str, start_marker: str, end_marker: str) -> Tuple[str, int, int]:
    """경계 마커를 사용해서 섹션을 추출합니다."""
    
    chapter_norm = normalize_for_comparison(chapter_text)
    
    # 시작 위치 찾기
    start_pos = fuzzy_find(chapter_norm, start_marker)
    if start_pos == -1:
        return "", -1, -1
    
    # 종료 위치 찾기 (시작 위치 이후부터)
    end_pos = fuzzy_find(chapter_norm[start_pos:], end_marker)
    if end_pos == -1:
        return "", start_pos, -1
    
    end_pos = start_pos + end_pos + len(normalize_for_comparison(end_marker))
    
    # 추출
    extracted = chapter_norm[start_pos:end_pos]
    
    return extracted, start_pos, end_pos


def validate_extraction(chapter_text: str, nodes: List[Dict]) -> Dict:
    """경계 마커를 사용한 섹션 추출을 검증합니다."""
    
    results = {
        'total_nodes': len(nodes),
        'successful_extractions': 0,
        'failed_extractions': 0,
        'details': []
    }
    
    print("🔍 경계 마커 기반 섹션 추출 검증 중...")
    print("=" * 60)
    
    for node in nodes:
        title = node.get('title', '')
        start_marker = node.get('start_text', '')
        end_marker = node.get('end_text', '')
        expected_length = node.get('section_length', 0)
        
        if not start_marker or not end_marker:
            print(f"❌ {title}: 마커 없음")
            results['failed_extractions'] += 1
            continue
        
        # 섹션 추출 시도
        extracted_section, start_pos, end_pos = extract_section_by_boundaries(
            chapter_text, start_marker, end_marker
        )
        
        if extracted_section:
            extracted_length = len(extracted_section)
            success = True
            results['successful_extractions'] += 1
            
            print(f"✅ {title}")
            print(f"   예상 길이: {expected_length:,}자")
            print(f"   추출 길이: {extracted_length:,}자")
            print(f"   위치: {start_pos:,} - {end_pos:,}")
            
            # 길이 차이가 크면 경고
            if abs(extracted_length - expected_length) > expected_length * 0.1:
                print(f"   ⚠️  길이 차이가 큽니다 ({abs(extracted_length - expected_length):,}자)")
                
        else:
            success = False
            results['failed_extractions'] += 1
            print(f"❌ {title}: 추출 실패")
            print(f"   시작 마커 찾기: {'성공' if start_pos >= 0 else '실패'}")
            print(f"   종료 마커 찾기: {'성공' if end_pos >= 0 else '실패'}")
        
        results['details'].append({
            'title': title,
            'success': success,
            'extracted_length': len(extracted_section) if extracted_section else 0,
            'expected_length': expected_length,
            'start_pos': start_pos,
            'end_pos': end_pos
        })
        
        print()
    
    return results


def main():
    """메인 함수"""
    print("🚀 경계 마커 검증 스크립트 시작")
    print("=" * 40)
    
    # 파일 경로
    boundaries_json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_with_boundaries.json"
    chapter_text_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    
    # 파일 로드
    print("📂 파일 로드 중...")
    with open(boundaries_json_path, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    with open(chapter_text_path, 'r', encoding='utf-8') as f:
        chapter_text = f.read()
    
    print(f"✅ 노드 수: {len(nodes)}")
    print(f"✅ 원본 텍스트: {len(chapter_text):,}자")
    print()
    
    # 검증 실행
    results = validate_extraction(chapter_text, nodes)
    
    # 결과 요약
    print("📊 검증 결과 요약:")
    print("=" * 40)
    print(f"전체 노드: {results['total_nodes']}")
    print(f"추출 성공: {results['successful_extractions']}")
    print(f"추출 실패: {results['failed_extractions']}")
    print(f"성공률: {results['successful_extractions']/results['total_nodes']*100:.1f}%")
    
    # 실패한 노드들 상세 정보
    failed_nodes = [d for d in results['details'] if not d['success']]
    if failed_nodes:
        print(f"\n❌ 추출 실패 노드들:")
        for node in failed_nodes:
            print(f"  - {node['title']}")
    
    if results['successful_extractions'] == results['total_nodes']:
        print("\n🎉 모든 노드에서 섹션 추출이 성공했습니다!")
        return 0
    else:
        print(f"\n⚠️  {results['failed_extractions']}개 노드에서 추출에 실패했습니다.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)