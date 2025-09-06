#!/usr/bin/env python3
"""
PDF에서 특정 섹션을 찾는 테스트 스크립트
"""

import pdfplumber
import re

def search_sections_in_pdf():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    # 찾을 섹션들
    search_terms = [
        "Summary",
        "Introduction", 
        "1.1.1 The design phase",
        "UML 101",
        "1.2.1 Many relations between classes",
        "6.2.0",
        "6.2.1",
        "Part1",
        "Flexibility"
    ]
    
    print("PDF에서 섹션 검색 중...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            found_sections = {}
            
            # 각 페이지에서 검색
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if not text:
                    continue
                
                # 각 검색어에 대해 확인
                for term in search_terms:
                    if term not in found_sections:
                        # 대소문자 구분 없이 검색
                        if term.lower() in text.lower():
                            found_sections[term] = {
                                'page': page_num,
                                'context': text[:1000]  # 첫 1000자
                            }
                            print(f"✓ '{term}' 발견 - 페이지 {page_num}")
                
                # 50페이지까지만 검색 (시간 절약)
                if page_num >= 50:
                    break
            
            print(f"\n=== 검색 결과 ===")
            print(f"찾은 섹션: {len(found_sections)}/{len(search_terms)}")
            
            for term, info in found_sections.items():
                print(f"\n[{term}] - 페이지 {info['page']}")
                # 해당 섹션 주변 텍스트 미리보기
                lines = info['context'].split('\n')
                for i, line in enumerate(lines):
                    if term.lower() in line.lower():
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        print("Context:")
                        for j in range(start, end):
                            marker = ">>> " if j == i else "    "
                            print(f"{marker}{lines[j]}")
                        break
            
            return found_sections
                
    except Exception as e:
        print(f"오류 발생: {e}")
        return {}

if __name__ == "__main__":
    search_sections_in_pdf()