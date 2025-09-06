#!/usr/bin/env python3
"""
* 생성 시간: Sun Aug 10 22:18:34 KST 2025
* 핵심 내용: PDF에서 특정 섹션 추출 도구
* 상세 내용:
*   - PyPDF2를 사용한 PDF 텍스트 추출 (line 12-25): PDF 파일 읽기 및 텍스트 변환
*   - 섹션 경계 탐지 함수 (line 27-45): 시작/종료 텍스트 패턴으로 섹션 식별  
*   - 텍스트 정제 함수 (line 47-58): 불필요한 공백, 페이지 번호 제거
*   - 메인 추출 함수 (line 60-85): 섹션별 텍스트 추출 및 저장
* 상태: active
* 주소: pdf_section_extractor
* 참조: /home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf
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
            text += f"\n=== 페이지 {page_num + 1} ===\n"
            text += page_text
    return text

def find_section_boundaries(full_text, start_pattern, end_pattern):
    """텍스트에서 섹션의 시작과 끝을 찾음"""
    # 패턴을 정규식으로 변환 (줄바꿈과 공백을 유연하게 처리)
    start_regex = re.escape(start_pattern).replace(r'\ ', r'\s+').replace(r'\n', r'\s*\n\s*')
    end_regex = re.escape(end_pattern).replace(r'\ ', r'\s+').replace(r'\n', r'\s*\n\s*')
    
    start_match = re.search(start_regex, full_text, re.MULTILINE | re.DOTALL)
    end_match = re.search(end_regex, full_text, re.MULTILINE | re.DOTALL)
    
    if start_match and end_match:
        return start_match.start(), end_match.end()
    elif start_match:
        return start_match.start(), None
    else:
        return None, None

def clean_extracted_text(text):
    """추출된 텍스트 정제"""
    # 페이지 구분선 제거
    text = re.sub(r'=== 페이지 \d+ ===\n?', '', text)
    # 여러 개의 연속된 공백을 하나로 통합
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    # 앞뒤 공백 제거
    return text.strip()

def extract_section(pdf_path, section_title, start_text, end_text):
    """PDF에서 특정 섹션 추출"""
    print(f"PDF에서 '{section_title}' 섹션 추출 중...")
    
    # PDF 전체 텍스트 추출
    full_text = extract_pdf_text(pdf_path)
    
    # 섹션 경계 찾기
    start_pos, end_pos = find_section_boundaries(full_text, start_text, end_text)
    
    if start_pos is None:
        print(f"시작 텍스트를 찾을 수 없습니다: {start_text[:50]}...")
        return None
    
    if end_pos is None:
        print("종료 텍스트를 찾을 수 없어서 다음 섹션까지 추출합니다.")
        # 다음 섹션의 시작을 찾아서 종료점으로 사용
        next_section_patterns = [
            r'7\.3\s+Schema flexibility',
            r'7\.4\s+Schema composition',
            r'Summary'
        ]
        for pattern in next_section_patterns:
            match = re.search(pattern, full_text[start_pos:], re.MULTILINE)
            if match:
                end_pos = start_pos + match.start()
                break
        
        if end_pos is None:
            end_pos = len(full_text)  # 파일 끝까지
    
    # 섹션 텍스트 추출
    section_text = full_text[start_pos:end_pos]
    section_text = clean_extracted_text(section_text)
    
    return section_text

if __name__ == "__main__":
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    # 7.2 JSON Schema in a nutshell 섹션 추출
    section_title = "7.2 JSON Schema in a nutshell"
    start_text = "7.2 JSON Schema in a nutshell"
    end_text = "7.3 Schema flexibility and strictness"
    
    extracted_text = extract_section(pdf_path, section_title, start_text, end_text)
    
    if extracted_text:
        # 추출된 텍스트를 파일로 저장
        output_file = f"/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/{section_title.replace(' ', '_').replace('.', '_')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {section_title}\n\n")
            f.write(extracted_text)
        
        print(f"추출 완료: {output_file}")
        print(f"텍스트 길이: {len(extracted_text)} 문자")
        print("첫 200자 미리보기:")
        print(extracted_text[:200] + "...")
    else:
        print("섹션 추출에 실패했습니다.")