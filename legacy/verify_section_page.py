#!/usr/bin/env python3
"""
특정 섹션의 실제 PDF 페이지 위치 검증
"""

import pdfplumber
import re
from typing import Optional, List

def find_section_page(pdf_path: str, section_title: str, search_range: tuple = None) -> Optional[int]:
    """PDF에서 특정 섹션의 정확한 페이지 찾기"""
    
    # 검색 패턴 생성
    patterns = generate_search_patterns(section_title)
    
    print(f"'{section_title}' 섹션 검색 중...")
    print(f"검색 패턴: {patterns}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            start_page = search_range[0] - 1 if search_range else 0
            end_page = min(search_range[1] if search_range else len(pdf.pages), len(pdf.pages))
            
            print(f"검색 범위: 페이지 {start_page + 1} ~ {end_page}")
            
            for page_num in range(start_page, end_page):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    # 각 패턴에 대해 검색
                    for pattern in patterns:
                        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                        for match in matches:
                            # 매치된 텍스트 주변 컨텍스트 확인
                            start_pos = max(0, match.start() - 50)
                            end_pos = min(len(text), match.end() + 50)
                            context = text[start_pos:end_pos].replace('\n', ' ')
                            
                            print(f"  페이지 {page_num + 1}에서 발견:")
                            print(f"  매치: '{match.group()}'")
                            print(f"  컨텍스트: ...{context}...")
                            
                            # 실제 섹션 헤딩인지 확인 (주변에 다른 텍스트가 많이 없어야 함)
                            lines = text.split('\n')
                            for i, line in enumerate(lines):
                                if pattern.lower().replace('\\s+', ' ') in line.lower():
                                    # 섹션 헤딩 라인 찾기
                                    stripped_line = line.strip()
                                    if len(stripped_line) < 100:  # 섹션 제목은 보통 짧음
                                        return page_num + 1
                            
                            return page_num + 1
            
            print("  섹션을 찾을 수 없습니다.")
            return None
            
    except Exception as e:
        print(f"PDF 검색 중 오류: {e}")
        return None

def generate_search_patterns(section_title: str) -> List[str]:
    """섹션 제목에 대한 검색 패턴 생성"""
    patterns = []
    
    # 기본 제목 (특수문자 이스케이프)
    clean_title = re.escape(section_title)
    patterns.append(clean_title)
    
    # 공백을 유연하게 처리
    flexible_spaces = re.sub(r'\\?\s+', r'\\s+', clean_title)
    patterns.append(flexible_spaces)
    
    # 번호가 있는 경우 처리
    if re.match(r'^\d+', section_title):
        # 6.2.1 The tree of function calls -> "6.2.1" 과 "The tree of function calls" 분리
        match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)', section_title)
        if match:
            number_part = match.group(1)
            title_part = match.group(2)
            
            # 다양한 번호 형식 패턴
            escaped_number = re.escape(number_part)
            escaped_title = re.escape(title_part)
            flexible_number = number_part.replace('.', r'\s*\.\s*')
            
            patterns.extend([
                f"{escaped_number}\\s+{escaped_title}",
                f"{escaped_number}\\.?\\s+{escaped_title}",
                f"{flexible_number}\\s+{escaped_title}",
                escaped_title  # 번호 없이 제목만
            ])
    
    return list(set(patterns))  # 중복 제거

if __name__ == "__main__":
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    # 테스트할 섹션들
    test_sections = [
        ("6.2.1 The tree of function calls", (138, 168)),
        ("1.1.1 The design phase", (31, 53)),
        ("3.2 Representing records as maps", (71, 98)),
        ("9.4.1 Writing queries with persistent data structures", (203, 224))
    ]
    
    for section_title, page_range in test_sections:
        actual_page = find_section_page(pdf_path, section_title, page_range)
        print(f"\n결과: '{section_title}' -> 페이지 {actual_page}")
        print("-" * 80)