#!/usr/bin/env python3
"""
Part-Chapter 내용 확인 디버깅 스크립트
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer, TOCItem

def debug_content_check():
    """Part-Chapter 간 내용 존재 확인 디버깅"""
    normalizer = TOCNormalizer()
    
    # TOC 파싱
    normalizer.parse_toc_markdown('/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_TOC.md')
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== Part-Chapter 내용 확인 디버깅 ===\n")
    
    # Part 1과 Chapter 1 사이 내용 확인
    part1 = None
    chapter1 = None
    
    for item in normalizer.toc_items:
        if item.number == '1' and 'flexibility' in item.title.lower():
            part1 = item
        elif item.number == '1' and 'complexity' in item.title.lower():
            chapter1 = item
    
    if part1 and chapter1:
        print(f"Part 1: {part1}")
        print(f"Chapter 1: {chapter1}")
        print(f"Part 1 is parent of Chapter 1: {part1.is_direct_parent_of(chapter1)}")
        
        # 내용 확인
        has_content = normalizer.check_content_between_levels(part1, chapter1)
        print(f"내용 존재 여부: {has_content}")
    else:
        print("Part 1 또는 Chapter 1을 찾을 수 없음")
        print(f"Part 1: {part1}")
        print(f"Chapter 1: {chapter1}")

if __name__ == "__main__":
    debug_content_check()