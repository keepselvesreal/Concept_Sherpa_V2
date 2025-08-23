#!/usr/bin/env python3
"""
PDF 내용 추출 테스트 스크립트
"""

import pdfplumber
from pathlib import Path

def test_pdf_extraction():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    print("PDF 파일 테스트 중...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"총 페이지 수: {len(pdf.pages)}")
            
            # 처음 몇 페이지에서 내용 찾기
            for i, page in enumerate(pdf.pages[:10], 1):
                text = page.extract_text()
                if text:
                    print(f"\n=== Page {i} ===")
                    print(text[:300] + "..." if len(text) > 300 else text)
                    
                    # 특정 패턴 찾기
                    if "Summary" in text:
                        print(f"*** 'Summary' 찾음 (페이지 {i}) ***")
                    if "Introduction" in text:
                        print(f"*** 'Introduction' 찾음 (페이지 {i}) ***")
                    if "1.1" in text:
                        print(f"*** '1.1' 찾음 (페이지 {i}) ***")
                        
                    if i == 3:  # 첫 3페이지만 확인
                        break
                        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    test_pdf_extraction()