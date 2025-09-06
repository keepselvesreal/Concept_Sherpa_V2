#!/usr/bin/env python3
import PyPDF2
import pdfplumber
import sys
import re

def extract_toc_with_pypdf2(pdf_path):
    """PyPDF2를 사용하여 PDF 목차 추출"""
    print("=== PyPDF2로 목차 추출 ===")
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # 북마크(아웃라인) 추출
            if reader.outline:
                print("북마크 발견:")
                
                def print_outline(outline, level=0):
                    for item in outline:
                        if isinstance(item, list):
                            print_outline(item, level + 1)
                        else:
                            indent = "  " * level
                            if hasattr(item, 'title'):
                                print(f"{indent}- {item.title}")
                            else:
                                print(f"{indent}- {str(item)}")
                
                print_outline(reader.outline)
            else:
                print("북마크를 찾을 수 없습니다.")
                
    except Exception as e:
        print(f"PyPDF2 오류: {e}")

def extract_toc_with_pdfplumber(pdf_path):
    """pdfplumber를 사용하여 목차 패턴 추출"""
    print("\n=== pdfplumber로 목차 패턴 추출 ===")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 처음 몇 페이지에서 목차 찾기
            for page_num in range(min(10, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text and any(keyword in text.lower() for keyword in ['contents', 'table of contents', '목차']):
                    print(f"\n페이지 {page_num + 1}에서 목차 발견:")
                    
                    # 목차 패턴 찾기 (숫자.숫자 형태 또는 Chapter 형태)
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        # 챕터나 섹션 패턴 매칭
                        if re.match(r'^\d+\.?\d*\s+[A-Za-z]', line) or \
                           re.match(r'^Chapter\s+\d+', line, re.IGNORECASE) or \
                           re.match(r'^Part\s+\d+', line, re.IGNORECASE):
                            print(f"  {line}")
                    break
            else:
                print("목차 섹션을 찾을 수 없습니다.")
                
    except Exception as e:
        print(f"pdfplumber 오류: {e}")

def main():
    pdf_path = '/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf'
    
    print(f"PDF 파일 분석: {pdf_path}")
    
    # 두 가지 방법으로 목차 추출 시도
    extract_toc_with_pypdf2(pdf_path)
    extract_toc_with_pdfplumber(pdf_path)

if __name__ == "__main__":
    main()