#!/usr/bin/env python3
"""
구체적인 검색 테스트
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer
import re

def test_specific_patterns():
    """구체적인 패턴 테스트"""
    normalizer = TOCNormalizer()
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== 구체적인 패턴 테스트 ===\n")
    
    # Chapter 1 패턴 테스트
    chapter_patterns = [
        r'\d+\s+CHAPTER\s+1\s+Complexity of object-oriented programming',
        r'CHAPTER\s+1\s+Complexity of object-oriented programming',
        r'\d+\s+CHAPTER\s+1\s+.*Complexity',
    ]
    
    print("Chapter 1 패턴 테스트:")
    for pattern in chapter_patterns:
        print(f"  패턴: {pattern}")
        found = False
        for page_num, page_text in enumerate(normalizer.pdf_pages):
            if page_num < 25:  # TOC 페이지들 제외
                continue
            if not page_text:
                continue
                
            lines = page_text.split('\n')
            for line_idx, line in enumerate(lines):
                line = line.strip()
                if re.search(pattern, line, re.IGNORECASE):
                    print(f"    → 발견: 페이지 {page_num + 1}, 라인 {line_idx + 1}: {line}")
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"    → 못 찾음")
    
    # Part 1 패턴 테스트  
    part_patterns = [
        r'PART\s+1\s+Flexibility',
        r'\d+\s+PART\s+1\s+Flexibility',
    ]
    
    print("\nPart 1 패턴 테스트:")
    for pattern in part_patterns:
        print(f"  패턴: {pattern}")
        found = False
        for page_num, page_text in enumerate(normalizer.pdf_pages):
            if page_num < 25:  # TOC 페이지들 제외
                continue
            if not page_text:
                continue
                
            lines = page_text.split('\n')
            for line_idx, line in enumerate(lines):
                line = line.strip()
                if re.search(pattern, line, re.IGNORECASE):
                    print(f"    → 발견: 페이지 {page_num + 1}, 라인 {line_idx + 1}: {line}")
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"    → 못 찾음")

if __name__ == "__main__":
    test_specific_patterns()