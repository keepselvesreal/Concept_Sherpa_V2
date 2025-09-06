#!/usr/bin/env python3
"""
* 생성 시간: Sun Aug 10 22:18:34 KST 2025
* 핵심 내용: 정밀 PDF 섹션 추출 도구 - 실제 본문 내용 추출
* 상세 내용:
*   - PyPDF2 페이지별 추출 (line 12-28): 페이지 번호와 함께 텍스트 처리
*   - 본문 내용 탐지 알고리즘 (line 30-65): 목차가 아닌 실제 본문 찾기
*   - 섹션 경계 정확 탐지 (line 67-95): 시작 키워드 이후 실제 내용까지 추출
*   - 텍스트 정제 및 검증 (line 97-120): 추출 품질 확인 후 저장
* 상태: active
* 주소: precise_section_extractor  
* 참조: pdf_section_extractor_v2
"""

import PyPDF2
import re

def extract_pdf_with_pages(pdf_path):
    """PDF를 페이지별로 추출하여 위치 정보 유지"""
    pages_text = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            pages_text.append({
                'page_num': page_num + 1,
                'text': page_text
            })
    return pages_text

def find_section_in_pages(pages_text, section_title):
    """페이지별로 섹션 찾기"""
    section_pattern = re.compile(rf"^{re.escape(section_title)}\s*$", re.MULTILINE)
    
    for i, page_data in enumerate(pages_text):
        page_text = page_data['text']
        match = section_pattern.search(page_text)
        
        if match:
            print(f"섹션 '{section_title}' 발견: 페이지 {page_data['page_num']}")
            
            # 매치 위치 이후의 텍스트 가져오기
            start_pos = match.end()
            section_content = page_text[start_pos:].strip()
            
            # 다음 페이지들도 확인하여 섹션 끝까지 가져오기
            next_section_patterns = [
                r"^7\.3\s+Schema flexibility",
                r"^7\.4\s+Schema composition",
                r"^Summary\s*$"
            ]
            
            # 현재 페이지에서 다음 섹션 찾기
            for pattern in next_section_patterns:
                next_match = re.search(pattern, section_content, re.MULTILINE)
                if next_match:
                    section_content = section_content[:next_match.start()].strip()
                    print(f"현재 페이지에서 다음 섹션 발견, 여기서 종료")
                    return section_content, page_data['page_num']
            
            # 다음 페이지들도 확인
            full_content = section_content
            
            for j in range(i + 1, min(i + 10, len(pages_text))):  # 최대 10페이지까지 확인
                next_page_text = pages_text[j]['text']
                
                # 다음 섹션이 시작하는지 확인
                section_end = False
                for pattern in next_section_patterns:
                    if re.search(pattern, next_page_text, re.MULTILINE):
                        # 다음 섹션 시작 전까지만 가져오기
                        match_end = re.search(pattern, next_page_text, re.MULTILINE)
                        if match_end:
                            full_content += "\n\n" + next_page_text[:match_end.start()].strip()
                        section_end = True
                        print(f"페이지 {pages_text[j]['page_num']}에서 다음 섹션 발견, 추출 완료")
                        break
                
                if section_end:
                    break
                else:
                    full_content += "\n\n" + next_page_text.strip()
            
            return full_content, page_data['page_num']
    
    return None, None

def clean_section_text(text):
    """섹션 텍스트 정제"""
    # 목차 라인 제거 (숫자.숫자 패턴으로 시작하고 페이지 번호로 끝나는 라인)
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # 목차 패턴 제거 (예: "7.3 Schema flexibility and strictness 149")
        if re.match(r'^\d+\.\d+.*?\d+\s*$', line.strip()):
            continue
        # 단순 숫자만 있는 라인 제거 (페이지 번호)
        if re.match(r'^\d+\s*$', line.strip()):
            continue
        # 챕터 헤더 제거 (예: "CHAPTER 7 Basic data validation")
        if re.match(r'^CHAPTER\s+\d+.*$', line.strip(), re.IGNORECASE):
            continue
            
        cleaned_lines.append(line)
    
    # 다시 합치고 여러 줄바꿈 정리
    cleaned_text = '\n'.join(cleaned_lines)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text.strip()

def extract_json_schema_section():
    """7.2 JSON Schema in a nutshell 섹션 정밀 추출"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    print("PDF 페이지별 텍스트 추출 중...")
    pages_text = extract_pdf_with_pages(pdf_path)
    print(f"총 {len(pages_text)}페이지 추출 완료")
    
    # 섹션 찾기
    section_content, start_page = find_section_in_pages(pages_text, "7.2 JSON Schema in a nutshell")
    
    if section_content:
        # 텍스트 정제
        clean_content = clean_section_text(section_content)
        
        # 결과가 너무 짧으면 다른 패턴으로 시도
        if len(clean_content) < 100:
            print("추출된 내용이 너무 짧습니다. 대체 방법으로 시도합니다.")
            # 'JSON Schema' 키워드로 더 넓게 검색
            for page_data in pages_text:
                if "JSON Schema" in page_data['text'] and "nutshell" in page_data['text']:
                    print(f"JSON Schema 관련 내용을 페이지 {page_data['page_num']}에서 발견")
                    clean_content = clean_section_text(page_data['text'])
                    break
        
        # 파일로 저장
        output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/7_2_JSON_Schema_precise.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 7.2 JSON Schema in a nutshell\n\n")
            f.write(f"**추출 페이지:** {start_page}\n\n")
            f.write(clean_content)
        
        print(f"\n추출 완료: {output_file}")
        print(f"섹션 길이: {len(clean_content)} 문자")
        print("\n첫 800자 미리보기:")
        print("-" * 60)
        print(clean_content[:800])
        print("-" * 60)
        
        return output_file
    else:
        print("7.2 JSON Schema in a nutshell 섹션을 찾을 수 없습니다.")
        return None

if __name__ == "__main__":
    extract_json_schema_section()