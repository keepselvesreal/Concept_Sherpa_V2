#!/usr/bin/env python3
"""
누락된 섹션들을 PDF에서 찾는 스크립트
"""

import pdfplumber
import re

def find_missing_sections():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    missing_sections = [
        "6.2.1 The tree of function calls",
        "6.2.2 Unit tests for functions down the tree", 
        "6.2.3 Unit tests for nodes in the tree"
    ]
    
    search_patterns = [
        "6.2.1",
        "tree of function calls",
        "6.2.2", 
        "functions down the tree",
        "6.2.3",
        "nodes in the tree",
        "Unit tests",
        "Chapter 6",
        "6.2"
    ]
    
    print("누락된 섹션들을 PDF에서 검색 중...")
    
    with pdfplumber.open(pdf_path) as pdf:
        found_locations = {}
        
        # 더 넓은 범위에서 검색 (100-250 페이지)
        for page_num in range(100, min(250, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
            
            # 각 패턴 검색
            for pattern in search_patterns:
                if pattern.lower() in text.lower():
                    if pattern not in found_locations:
                        found_locations[pattern] = []
                    found_locations[pattern].append(page_num + 1)
                    
                    # 6.2 관련 섹션이면 상세 출력
                    if "6.2" in pattern:
                        print(f"\n*** '{pattern}' 발견 - 페이지 {page_num + 1} ***")
                        
                        # 해당 섹션 주변 텍스트 출력
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if pattern.lower() in line.lower():
                                start = max(0, i-3)
                                end = min(len(lines), i+7)
                                print("컨텍스트:")
                                for j in range(start, end):
                                    marker = ">>> " if j == i else "    "
                                    print(f"{marker}{lines[j]}")
                                print()
                                break
        
        print(f"\n=== 검색 결과 요약 ===")
        for pattern, pages in found_locations.items():
            if pages:
                unique_pages = sorted(set(pages))
                print(f"'{pattern}': 페이지 {unique_pages}")

if __name__ == "__main__":
    find_missing_sections()