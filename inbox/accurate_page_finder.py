#!/usr/bin/env python3
import pdfplumber
import re
from pathlib import Path

def find_actual_chapter_pages():
    """실제 챕터 시작 페이지를 수동으로 찾기"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    # 이미 알고 있는 정보
    known_mappings = {
        "Chapter 1": 31  # 이미 확인한 내용
    }
    
    chapter_patterns = {
        "Chapter 2": [
            r"2\s+Separation\s+between\s+code\s+and\s+data",
            r"Separation\s+between\s+code\s+and\s+data",
            r"A\s+whole\s+new\s+world"  # Chapter 2 부제목
        ],
        "Chapter 3": [
            r"3\s+Basic\s+data\s+manipulation",
            r"Basic\s+data\s+manipulation"
        ],
        "Chapter 4": [
            r"4\s+State\s+management",
            r"State\s+management"
        ],
        "Chapter 5": [
            r"5\s+Basic\s+concurrency\s+control",
            r"Basic\s+concurrency\s+control"
        ],
        "Chapter 6": [
            r"6\s+Unit\s+tests",
            r"Unit\s+tests"
        ],
        # Part 2 시작 추정
        "Chapter 7": [
            r"7\s+Basic\s+data\s+validation",
            r"Basic\s+data\s+validation"
        ],
        "Chapter 8": [
            r"8\s+Advanced\s+concurrency\s+control",
            r"Advanced\s+concurrency\s+control"
        ],
        "Chapter 9": [
            r"9\s+Persistent\s+data\s+structures",
            r"Persistent\s+data\s+structures"
        ],
        "Chapter 10": [
            r"10\s+Database\s+operations",
            r"Database\s+operations"
        ],
        "Chapter 11": [
            r"11\s+Web\s+services",
            r"Web\s+services"
        ],
        # Part 3 시작 추정
        "Chapter 12": [
            r"12\s+Advanced\s+data\s+validation",
            r"Advanced\s+data\s+validation"
        ],
        "Chapter 13": [
            r"13\s+Polymorphism",
            r"Polymorphism"
        ],
        "Chapter 14": [
            r"14\s+Advanced\s+data\s+manipulation",
            r"Advanced\s+data\s+manipulation"
        ],
        "Chapter 15": [
            r"15\s+Debugging",
            r"Debugging"
        ]
    }
    
    print("정확한 챕터 페이지 찾기...")
    
    with pdfplumber.open(pdf_path) as pdf:
        results = known_mappings.copy()
        
        # 각 챕터를 순서대로 찾기 (이전 챕터 이후부터 검색)
        start_page = 31  # Chapter 1 이후부터
        
        for chapter, patterns in chapter_patterns.items():
            print(f"\n{chapter} 검색 중 (페이지 {start_page}부터)...")
            
            found = False
            for page_num in range(start_page, min(start_page + 50, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text() or ""
                
                # 패턴 매칭
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        # 실제 챕터 시작인지 확인
                        if is_actual_chapter_start(text, chapter):
                            results[chapter] = page_num + 1
                            print(f"  {chapter}: 페이지 {page_num + 1} 발견")
                            print(f"  내용 미리보기: {text[:150]}...")
                            start_page = page_num + 1  # 다음 검색 시작점 업데이트
                            found = True
                            break
                
                if found:
                    break
            
            if not found:
                print(f"  {chapter}: 찾지 못함")
                start_page += 20  # 대략적으로 다음 검색 범위 이동
    
    return results

def is_actual_chapter_start(text: str, chapter_name: str) -> bool:
    """실제 챕터 시작인지 확인"""
    # 목차 페이지 제외
    if re.search(r"contents|table\s+of\s+contents", text, re.IGNORECASE):
        return False
    
    # 너무 짧은 텍스트 제외 (헤더만 있는 경우)
    if len(text.strip()) < 200:
        return False
    
    # 챕터 시작 지표들
    chapter_indicators = [
        r"This\s+chapter\s+covers",
        r"In\s+this\s+chapter",
        r"This\s+chapter\s+is\s+about",
        r"chapter\s+covers",
        # 또는 충분한 양의 내용
    ]
    
    for indicator in chapter_indicators:
        if re.search(indicator, text, re.IGNORECASE):
            return True
    
    # 충분한 양의 텍스트가 있으면 실제 내용으로 간주
    return len(text.strip()) > 800

def verify_specific_pages():
    """특정 페이지들을 직접 확인"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    # 추정되는 챕터 시작 페이지들 (1장 이후 대략 20-25페이지씩)
    estimated_pages = {
        "Chapter 2": [54, 55, 56, 57, 58],  # 1장이 31-54였으므로
        "Chapter 3": [75, 76, 77, 78, 79],
        "Chapter 4": [95, 96, 97, 98, 99],
        "Chapter 5": [115, 116, 117, 118, 119],
        "Chapter 6": [135, 136, 137, 138, 139],
    }
    
    print("추정 페이지 직접 확인...")
    
    with pdfplumber.open(pdf_path) as pdf:
        for chapter, page_candidates in estimated_pages.items():
            print(f"\n=== {chapter} 후보 페이지들 ===")
            
            for page_num in page_candidates:
                if page_num <= len(pdf.pages):
                    page = pdf.pages[page_num - 1]  # 0-based index
                    text = page.extract_text() or ""
                    
                    print(f"\n페이지 {page_num}:")
                    print(f"첫 200자: {text[:200]}...")
                    
                    # 챕터 시작 패턴 확인
                    if chapter == "Chapter 2":
                        if re.search(r"Separation\s+between\s+code\s+and\s+data", text, re.IGNORECASE):
                            print(f"*** {chapter} 발견! 페이지 {page_num} ***")
                    elif chapter == "Chapter 3":
                        if re.search(r"Basic\s+data\s+manipulation", text, re.IGNORECASE):
                            print(f"*** {chapter} 발견! 페이지 {page_num} ***")
                    # 다른 챕터들도 동일하게...

def main():
    print("=== PDF 챕터 페이지 매핑 (정확한 방법) ===")
    
    # 방법 1: 패턴 기반 검색
    results = find_actual_chapter_pages()
    
    print(f"\n=== 발견된 챕터들 ===")
    for chapter, page in sorted(results.items(), key=lambda x: x[1]):
        print(f"{chapter}: 페이지 {page}")
    
    # 방법 2: 특정 페이지 직접 확인
    print(f"\n=== 추정 페이지 직접 확인 ===")
    verify_specific_pages()

if __name__ == "__main__":
    main()