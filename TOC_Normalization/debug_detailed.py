#!/usr/bin/env python3
"""
상세한 디버깅 스크립트
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer, TOCItem

def debug_detailed():
    """상세한 디버깅"""
    normalizer = TOCNormalizer()
    
    # TOC 파싱
    normalizer.parse_toc_markdown('/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_TOC.md')
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== 상세한 디버깅 ===\n")
    
    # Part 1과 Chapter 1 찾기
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
        
        # PDF에서 위치 찾기
        part1_pos = normalizer.find_section_in_pdf(part1.number, part1.title)
        chapter1_pos = normalizer.find_section_in_pdf(chapter1.number, chapter1.title)
        
        print(f"Part 1 PDF 위치: {part1_pos}")
        print(f"Chapter 1 PDF 위치: {chapter1_pos}")
        
        if part1_pos and chapter1_pos:
            part_page, part_line = part1_pos
            chapter_page, chapter_line = chapter1_pos
            
            print(f"Part 1: 페이지 {part_page + 1}, 라인 {part_line + 1}")
            print(f"Chapter 1: 페이지 {chapter_page + 1}, 라인 {chapter_line + 1}")
            
            # 페이지 차이가 있는지 확인
            if chapter_page > part_page:
                print(f"페이지 차이: {chapter_page - part_page}페이지")
                print("→ Part-Chapter 사이에 내용이 있을 것으로 예상됨")
                
                # 중간 내용 확인
                has_content = normalizer.check_content_between_levels(part1, chapter1)
                print(f"실제 내용 존재 여부: {has_content}")
            else:
                print("→ 같은 페이지에 있음 - 내용 없을 가능성 높음")

if __name__ == "__main__":
    debug_detailed()