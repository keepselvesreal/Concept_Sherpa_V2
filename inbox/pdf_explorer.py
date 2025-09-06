#!/usr/bin/env python3
import pdfplumber
import re

def explore_pdf_structure(pdf_path: str, max_pages: int = 50):
    """PDF 구조 탐색 및 1장 위치 찾기"""
    print(f"PDF 구조 탐색 중... (최대 {max_pages}페이지)")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"총 페이지 수: {total_pages}")
        
        for page_num in range(min(max_pages, total_pages)):
            page = pdf.pages[page_num]
            text = page.extract_text() or ""
            
            # 각 페이지의 첫 몇 줄만 출력
            lines = text.split('\n')[:10]
            first_lines = '\n'.join(lines)
            
            print(f"\n=== 페이지 {page_num + 1} ===")
            print(first_lines[:300] + "..." if len(first_lines) > 300 else first_lines)
            
            # 1장 관련 패턴 체크
            chapter_patterns = [
                r"1\s+Complexity\s+of\s+object-oriented",
                r"^\s*1\s*\n.*complexity",
                r"OOP\s+design.*Classic",
                r"1\.1\s+OOP\s+design",
                r"Sources\s+of\s+complexity"
            ]
            
            for pattern in chapter_patterns:
                if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                    print(f"🎯 패턴 발견: {pattern}")
            
            # 페이지가 실제 내용인지 목차인지 판단
            if "contents" in text.lower() and "forewords" in text.lower():
                print("📋 목차 페이지로 판단")
            elif len(text.strip()) > 1000 and not ("contents" in text.lower() and "page" in text.lower()):
                print("📄 실제 내용 페이지로 판단")

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    explore_pdf_structure(pdf_path)

if __name__ == "__main__":
    main()