#!/usr/bin/env python3
"""
내용 검증 디버깅
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer, TOCItem
import re

def debug_content_verification():
    """내용 검증 상세 디버깅"""
    normalizer = TOCNormalizer()
    
    # TOC 파싱
    normalizer.parse_toc_markdown('/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_TOC.md')
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== 내용 검증 상세 디버깅 ===\n")
    
    # Part 1과 Chapter 1 찾기
    part1 = None
    chapter1 = None
    
    for item in normalizer.toc_items:
        if item.number == '1' and 'flexibility' in item.title.lower():
            part1 = item
        elif item.number == '1' and 'complexity' in item.title.lower():
            chapter1 = item
    
    if part1 and chapter1:
        # PDF에서 위치 찾기
        part1_pos = normalizer.find_section_in_pdf(part1.number, part1.title)
        chapter1_pos = normalizer.find_section_in_pdf(chapter1.number, chapter1.title)
        
        if part1_pos and chapter1_pos:
            parent_page, parent_line = part1_pos
            child_page, child_line = chapter1_pos
            
            print(f"Part 1 위치: 페이지 {parent_page + 1}, 라인 {parent_line + 1}")
            print(f"Chapter 1 위치: 페이지 {child_page + 1}, 라인 {child_line + 1}")
            
            # 중간 내용 추출
            content_lines = []
            
            if parent_page == child_page:
                # 같은 페이지 내에서 확인
                page_lines = normalizer.pdf_pages[parent_page].split('\n')
                content_lines = page_lines[parent_line + 1:child_line]
            else:
                # 여러 페이지에 걸쳐 확인
                # 부모 섹션 이후 부분
                parent_page_lines = normalizer.pdf_pages[parent_page].split('\n')
                content_lines.extend(parent_page_lines[parent_line + 1:])
                
                # 중간 페이지들 전체
                for page_idx in range(parent_page + 1, child_page):
                    if page_idx < len(normalizer.pdf_pages):
                        content_lines.extend(normalizer.pdf_pages[page_idx].split('\n'))
                
                # 자식 섹션 이전 부분
                if child_page < len(normalizer.pdf_pages):
                    child_page_lines = normalizer.pdf_pages[child_page].split('\n')
                    content_lines.extend(child_page_lines[:child_line])
            
            print(f"\n중간 내용 ({len(content_lines)}줄):")
            meaningful_lines = 0
            for i, line in enumerate(content_lines):
                line = line.strip()
                print(f"{i+1:2d}: {line}")
                
                # 실질적인 내용이 있는지 확인
                if line and not re.match(r'^\d+$', line) and len(line) > 15:
                    # 다른 섹션 헤딩이 아닌지 확인
                    if not re.match(r'^(\d+(\.\d+)*|[A-Z]\.\d+(\.\d+)*)\s+', line):
                        meaningful_lines += 1
                        print(f"      → 의미있는 라인")
            
            print(f"\n의미있는 라인 수: {meaningful_lines}")
            print(f"2줄 이상 기준: {meaningful_lines >= 2}")

if __name__ == "__main__":
    debug_content_verification()