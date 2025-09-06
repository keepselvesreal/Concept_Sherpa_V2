#!/usr/bin/env python3
"""
경계 마커를 사용해서 실제 섹션을 추출하는 테스트 스크립트
"""

import json
import re


def normalize_for_comparison(text: str) -> str:
    """비교를 위한 텍스트 정규화"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_section_by_boundaries(chapter_text: str, start_marker: str, end_marker: str) -> str:
    """경계 마커를 사용해서 섹션을 추출합니다."""
    
    chapter_norm = normalize_for_comparison(chapter_text)
    start_marker_norm = normalize_for_comparison(start_marker)
    end_marker_norm = normalize_for_comparison(end_marker)
    
    # 시작 위치 찾기
    start_pos = chapter_norm.find(start_marker_norm)
    if start_pos == -1:
        # 부분 매칭 시도
        start_short = start_marker_norm[:50]
        start_pos = chapter_norm.find(start_short)
        if start_pos == -1:
            return ""
    
    # 종료 위치 찾기
    end_pos = chapter_norm.find(end_marker_norm, start_pos)
    if end_pos == -1:
        # 부분 매칭 시도
        end_short = end_marker_norm[:50]
        end_pos = chapter_norm.find(end_short, start_pos)
        if end_pos == -1:
            return ""
    
    end_pos += len(end_marker_norm)
    
    # 추출된 섹션을 원본 형태로 복원
    # 정규화된 텍스트에서의 위치를 원본에서 찾기
    extracted_norm = chapter_norm[start_pos:end_pos]
    
    # 원본에서 해당 부분 찾기 (근사치)
    original_start = chapter_text.find(start_marker[:30])
    if original_start >= 0:
        original_end = chapter_text.find(end_marker[-30:], original_start)
        if original_end >= 0:
            return chapter_text[original_start:original_end + len(end_marker[-30:])]
    
    return extracted_norm


def main():
    """메인 함수"""
    print("🧪 섹션 추출 테스트")
    print("=" * 40)
    
    # 파일 로드
    with open("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_with_boundaries.json", 'r') as f:
        nodes = json.load(f)
    
    with open("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md", 'r') as f:
        chapter_text = f.read()
    
    # 특정 노드들 테스트
    test_nodes = ["7.1 Data validation in DOP", "7.2 JSON Schema in a nutshell", "Summary"]
    
    for test_title in test_nodes:
        print(f"\n📖 테스트: {test_title}")
        print("-" * 50)
        
        # 해당 노드 찾기
        node = next((n for n in nodes if n['title'] == test_title), None)
        if not node:
            print(f"❌ 노드를 찾을 수 없습니다: {test_title}")
            continue
        
        start_marker = node.get('start_text', '')
        end_marker = node.get('end_text', '')
        
        if not start_marker or not end_marker:
            print(f"❌ 마커가 없습니다")
            continue
        
        # 섹션 추출
        extracted = extract_section_by_boundaries(chapter_text, start_marker, end_marker)
        
        if extracted:
            print(f"✅ 추출 성공: {len(extracted):,}자")
            print(f"\n📝 추출된 섹션 미리보기 (처음 200자):")
            print("-" * 30)
            print(extracted[:200] + "..." if len(extracted) > 200 else extracted)
            print("-" * 30)
            
            print(f"\n📝 추출된 섹션 끝부분 (마지막 200자):")
            print("-" * 30)
            print("..." + extracted[-200:] if len(extracted) > 200 else extracted)
            print("-" * 30)
            
        else:
            print(f"❌ 추출 실패")
            print(f"시작 마커: {start_marker[:50]}...")
            print(f"종료 마커: {end_marker[:50]}...")


if __name__ == "__main__":
    main()