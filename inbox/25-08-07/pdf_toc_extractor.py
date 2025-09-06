# 목차
# - 생성 시간: 2025-08-07 11:28:30 KST
# - 핵심 내용: PDF 파일에서 목차를 추출하여 구조화된 형태로 저장하는 도구
# - 상세 내용:
#     - extract_bookmarks(1-20): PDF의 북마크/아웃라인에서 목차를 추출하는 함수
#     - extract_toc_from_pages(22-50): PDF 페이지에서 목차 텍스트를 직접 추출하는 함수
#     - format_toc_structure(52-70): 추출된 목차를 계층구조로 포맷팅하는 함수
#     - save_toc_data(72-85): 목차 데이터를 JSON과 마크다운으로 저장하는 함수
#     - main(87-105): 전체 프로세스를 실행하는 메인 함수
# - 상태: 활성
# - 주소: pdf_toc_extractor
# - 참조: 2022_Data-Oriented Programming_Manning.pdf

import json
import os
import re
from typing import Dict, List, Any, Optional
import pdfplumber
import PyPDF2
from datetime import datetime

def extract_bookmarks(pdf_path: str) -> List[Dict]:
    """PDF의 북마크/아웃라인에서 목차를 추출합니다."""
    bookmarks = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            def process_outline(outline, level=0):
                if isinstance(outline, list):
                    for item in outline:
                        process_outline(item, level)
                else:
                    title = outline.title
                    # 페이지 번호 추출 시도
                    page = None
                    if hasattr(outline, 'page') and outline.page:
                        page = pdf_reader.get_destination_page_number(outline) + 1
                    
                    bookmarks.append({
                        'title': title,
                        'level': level,
                        'page': page
                    })
                    
                    # 하위 항목 처리
                    if hasattr(outline, '/First'):
                        process_outline(outline['/First'], level + 1)
            
            if pdf_reader.outline:
                process_outline(pdf_reader.outline)
                
    except Exception as e:
        print(f"북마크 추출 실패: {e}")
    
    return bookmarks

def extract_toc_from_pages(pdf_path: str, start_page: int = 1, end_page: int = 20) -> List[str]:
    """PDF 페이지에서 목차 텍스트를 직접 추출합니다."""
    toc_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"PDF 총 페이지 수: {len(pdf.pages)}")
            
            # 목차가 있을 것으로 예상되는 페이지들을 확인
            for page_num in range(min(start_page - 1, len(pdf.pages)), min(end_page, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    # "contents", "table of contents" 등의 키워드가 있는지 확인
                    if any(keyword in text.lower() for keyword in ['contents', 'table of contents', 'toc']):
                        print(f"페이지 {page_num + 1}에서 목차 발견")
                        toc_text.append(f"=== 페이지 {page_num + 1} ===\n{text}")
                    
                    # 챕터나 부분 제목이 있는 것처럼 보이는 페이지도 포함
                    elif any(keyword in text.lower() for keyword in ['chapter', 'part', 'appendix']):
                        toc_text.append(f"=== 페이지 {page_num + 1} ===\n{text}")
                        
    except Exception as e:
        print(f"페이지에서 목차 추출 실패: {e}")
    
    return toc_text

def parse_toc_structure(text_lines: List[str]) -> List[Dict]:
    """목차 텍스트를 구조화된 형태로 파싱합니다."""
    toc_items = []
    
    for line in text_lines:
        line = line.strip()
        if not line:
            continue
            
        # 페이지 번호 패턴 찾기
        page_match = re.search(r'\.{2,}\s*(\d+)$|(\d+)$', line)
        page_num = None
        if page_match:
            page_num = int(page_match.group(1) or page_match.group(2))
            # 페이지 번호와 점들 제거
            title = re.sub(r'\.{2,}\s*\d+$|\s+\d+$', '', line).strip()
        else:
            title = line
        
        # 레벨 추정 (들여쓰기나 번호 체계로)
        level = 0
        if title.startswith('    '):
            level = 2
        elif title.startswith('  '):
            level = 1
        elif re.match(r'^\d+\.\d+', title):
            level = 2
        elif re.match(r'^\d+\.', title):
            level = 1
        elif title.lower().startswith(('part', 'appendix')):
            level = 0
        
        toc_items.append({
            'title': title,
            'level': level,
            'page': page_num
        })
    
    return toc_items

def save_toc_data(bookmarks: List[Dict], page_toc: List[str], output_dir: str):
    """목차 데이터를 저장합니다."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')
    
    # 북마크 기반 목차 저장
    if bookmarks:
        bookmark_file = os.path.join(output_dir, "toc_from_bookmarks.json")
        with open(bookmark_file, 'w', encoding='utf-8') as f:
            json.dump({
                "extraction_time": timestamp,
                "method": "PDF bookmarks",
                "total_items": len(bookmarks),
                "toc": bookmarks
            }, f, ensure_ascii=False, indent=2)
        print(f"북마크 목차 저장: {bookmark_file}")
    
    # 페이지 기반 목차 저장
    if page_toc:
        page_toc_file = os.path.join(output_dir, "toc_from_pages.txt")
        with open(page_toc_file, 'w', encoding='utf-8') as f:
            f.write(f"# PDF 페이지에서 추출한 목차\n")
            f.write(f"추출 시간: {timestamp}\n\n")
            f.write("\n\n".join(page_toc))
        print(f"페이지 목차 저장: {page_toc_file}")
        
        # 구조화된 목차로 변환 시도
        all_lines = []
        for text_block in page_toc:
            all_lines.extend(text_block.split('\n'))
        
        structured_toc = parse_toc_structure(all_lines)
        if structured_toc:
            structured_file = os.path.join(output_dir, "toc_structured.json")
            with open(structured_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "extraction_time": timestamp,
                    "method": "Page text parsing",
                    "total_items": len(structured_toc),
                    "toc": structured_toc
                }, f, ensure_ascii=False, indent=2)
            print(f"구조화된 목차 저장: {structured_file}")

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_toc"
    
    print("🚀 PDF 목차 추출 시작...")
    print(f"📖 PDF: {os.path.basename(pdf_path)}")
    print(f"📁 출력: {output_dir}")
    
    # 방법 1: 북마크에서 목차 추출
    print("\n📑 북마크에서 목차 추출 중...")
    bookmarks = extract_bookmarks(pdf_path)
    if bookmarks:
        print(f"✅ 북마크에서 {len(bookmarks)}개 항목 발견")
    else:
        print("❌ 북마크에서 목차를 찾을 수 없음")
    
    # 방법 2: 페이지 텍스트에서 목차 추출
    print("\n📄 페이지 텍스트에서 목차 추출 중...")
    page_toc = extract_toc_from_pages(pdf_path)
    if page_toc:
        print(f"✅ {len(page_toc)}개 페이지에서 목차 관련 텍스트 발견")
    else:
        print("❌ 페이지에서 목차를 찾을 수 없음")
    
    # 결과 저장
    save_toc_data(bookmarks, page_toc, output_dir)
    
    print(f"\n🎉 목차 추출 완료!")
    print(f"📁 결과가 '{output_dir}' 디렉터리에 저장되었습니다.")

if __name__ == "__main__":
    main()