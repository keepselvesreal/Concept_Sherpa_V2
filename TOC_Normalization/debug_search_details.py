#!/usr/bin/env python3
"""
검색 상세 디버깅
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer
import re

def debug_search_details():
    """검색 상세 디버깅"""
    normalizer = TOCNormalizer()
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== 검색 상세 디버깅 ===\n")
    
    # 페이지 29, 30, 31, 32 내용 확인
    for page_num in [29, 30, 31, 32]:
        if page_num < len(normalizer.pdf_pages):
            print(f"--- 페이지 {page_num + 1} ---")
            lines = normalizer.pdf_pages[page_num].split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line:
                    print(f"{i+1:2d}: {line}")
            print()

if __name__ == "__main__":
    debug_search_details()