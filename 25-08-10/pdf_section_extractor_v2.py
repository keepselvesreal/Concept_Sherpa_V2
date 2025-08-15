#!/usr/bin/env python3
"""
* 생성 시간: Sun Aug 10 22:18:34 KST 2025
* 핵심 내용: 개선된 PDF 섹션 추출 도구 (v2)
* 상세 내용:
*   - PyPDF2를 사용한 PDF 텍스트 추출 (line 12-25): 페이지별 텍스트 변환
*   - 패턴 기반 섹션 탐지 (line 27-55): 정규식으로 섹션 경계 식별
*   - 컨텍스트 기반 추출 (line 57-85): 섹션 제목 이후부터 다음 섹션까지 추출
*   - 텍스트 정제 및 저장 (line 87-110): 불필요한 내용 제거 후 마크다운 저장
* 상태: active  
* 주소: pdf_section_extractor_v2
* 참조: pdf_section_extractor
"""

import PyPDF2
import re
from pathlib import Path

def extract_pdf_text(pdf_path):
    """PDF 파일에서 모든 텍스트를 추출"""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text + "\n"
    return text

def extract_section_by_pattern(full_text, section_number, section_name):
    """패턴 기반으로 섹션 추출"""
    # 섹션 시작 패턴 - 더 유연하게
    start_patterns = [
        f"{section_number}\\s+{re.escape(section_name)}",
        f"{section_number}\\s*{re.escape(section_name)}",
        f"^{section_number}\\s+{re.escape(section_name)}",
    ]
    
    # 다음 섹션들의 패턴
    next_section_patterns = [
        r"7\.3\s+Schema flexibility",
        r"7\.4\s+Schema composition", 
        r"7\.5\s+Details about",
        r"Summary\s*$",
        r"^Summary\s",
        r"Chapter\s+8",
        r"8\s+Advanced"
    ]
    
    start_pos = None
    end_pos = None
    
    # 시작점 찾기
    for pattern in start_patterns:
        match = re.search(pattern, full_text, re.MULTILINE | re.IGNORECASE)
        if match:
            start_pos = match.start()
            print(f"시작점 발견: {pattern} at position {start_pos}")
            break
    
    if start_pos is None:
        print(f"'{section_number} {section_name}' 섹션을 찾을 수 없습니다.")
        return None
    
    # 종료점 찾기 - 시작점 이후에서 검색
    search_text = full_text[start_pos + 100:]  # 시작점 이후 100자 뒤부터 검색
    
    for pattern in next_section_patterns:
        match = re.search(pattern, search_text, re.MULTILINE | re.IGNORECASE)
        if match:
            end_pos = start_pos + 100 + match.start()
            print(f"종료점 발견: {pattern} at position {end_pos}")
            break
    
    if end_pos is None:
        print("종료점을 찾지 못해 텍스트 끝까지 추출합니다.")
        end_pos = len(full_text)
    
    # 섹션 텍스트 추출
    section_text = full_text[start_pos:end_pos]
    return section_text

def clean_text(text):
    """텍스트 정제"""
    # 페이지 번호와 헤더 제거
    text = re.sub(r'^\d+\s+(CHAPTER\s+\d+.*?)\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    
    # 여러 개의 연속된 줄바꿈을 2개로 통일
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 앞뒤 공백 제거
    return text.strip()

def extract_json_schema_section():
    """7.2 JSON Schema in a nutshell 섹션 추출"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    print("PDF 텍스트 추출 중...")
    full_text = extract_pdf_text(pdf_path)
    print(f"전체 텍스트 길이: {len(full_text)} 문자")
    
    # 섹션 추출
    section_text = extract_section_by_pattern(full_text, "7.2", "JSON Schema in a nutshell")
    
    if section_text:
        # 텍스트 정제
        clean_section = clean_text(section_text)
        
        # 파일로 저장
        output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/7_2_JSON_Schema_section.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 7.2 JSON Schema in a nutshell\n\n")
            f.write(clean_section)
        
        print(f"\n추출 완료: {output_file}")
        print(f"섹션 길이: {len(clean_section)} 문자")
        print("\n첫 500자 미리보기:")
        print("-" * 50)
        print(clean_section[:500])
        print("-" * 50)
        
        return output_file
    else:
        print("섹션 추출에 실패했습니다.")
        return None

if __name__ == "__main__":
    extract_json_schema_section()