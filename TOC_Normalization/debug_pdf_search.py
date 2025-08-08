#!/usr/bin/env python3
"""
PDF 검색 디버깅 스크립트
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer

def debug_pdf_search():
    """PDF에서 Part와 Chapter 검색 디버깅"""
    normalizer = TOCNormalizer()
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== PDF 검색 디버깅 ===\n")
    
    # Part 1 검색
    part1_pos = normalizer.find_section_in_pdf('1', 'Flexibility')
    print(f"Part 1 위치: {part1_pos}")
    
    # Chapter 1 검색
    chapter1_pos = normalizer.find_section_in_pdf('1', 'Complexity of object-oriented programming')
    print(f"Chapter 1 위치: {chapter1_pos}")
    
    # 첫 몇 페이지의 내용 확인
    print("\n=== 첫 10페이지 내용 샘플 ===")
    for i in range(min(10, len(normalizer.pdf_pages))):
        page_text = normalizer.pdf_pages[i]
        if page_text and len(page_text.strip()) > 50:
            lines = page_text.split('\n')[:5]  # 첫 5줄만
            print(f"페이지 {i+1}: {' | '.join(line.strip() for line in lines if line.strip())}")
    
    # "Part" 키워드 검색
    print("\n=== 'Part' 키워드 검색 ===")
    for i, page_text in enumerate(normalizer.pdf_pages[:20]):  # 첫 20페이지만
        if 'part' in page_text.lower():
            lines = page_text.split('\n')
            for j, line in enumerate(lines):
                if 'part' in line.lower():
                    print(f"페이지 {i+1}, 라인 {j+1}: {line.strip()}")
                    break

if __name__ == "__main__":
    debug_pdf_search()