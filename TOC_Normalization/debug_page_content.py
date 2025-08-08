#!/usr/bin/env python3
"""
특정 페이지 내용 상세 디버깅
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer

def debug_page_content():
    """페이지 7 내용 상세 확인"""
    normalizer = TOCNormalizer()
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== 페이지 7-10 상세 내용 ===\n")
    
    for page_num in range(7, min(15, len(normalizer.pdf_pages))):
        print(f"\n--- 페이지 {page_num + 1} ---")
        page_text = normalizer.pdf_pages[page_num]
        if page_text:
            lines = page_text.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line:
                    print(f"{i+1:2d}: {line}")
        else:
            print("(빈 페이지)")

if __name__ == "__main__":
    debug_page_content()