# 목차
# - 생성 시간: 2025-08-07 11:35:25 KST
# - 핵심 내용: PDF의 목차 페이지에서 깔끔한 목차 정보를 추출하고 정리하는 도구
# - 상세 내용:
#     - extract_toc_pages(1-25): PDF에서 목차 페이지만 추출하는 함수
#     - clean_toc_content(27-55): 목차 텍스트를 정리하고 구조화하는 함수
#     - format_toc_output(57-75): 목차를 읽기 쉽게 포맷팅하는 함수
#     - main(77-85): 실행 함수
# - 상태: 활성  
# - 주소: extract_clean_toc
# - 참조: 2022_Data-Oriented Programming_Manning.pdf

import pdfplumber
import re

def extract_toc_pages(pdf_path: str):
    """PDF에서 목차 페이지들만 추출"""
    toc_content = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # 목차는 보통 앞쪽 15페이지 내에 있음
        for page_num in range(5, 20):  # 6페이지부터 20페이지까지
            if page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text and ('contents' in text.lower() or 'part ' in text.lower()):
                    # 목차 관련 페이지만 수집
                    clean_text = text.replace('\n\n', '\n').strip()
                    toc_content.append(f"페이지 {page_num + 1}:\n{clean_text}\n")
    
    return toc_content

def clean_toc_content(toc_pages):
    """목차 내용을 정리하고 구조화"""
    all_text = "\n".join(toc_pages)
    
    # 주요 섹션들 추출
    lines = all_text.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('페이지'):
            continue
            
        # 목차 헤더
        if line.lower() in ['contents', 'brief contents']:
            clean_lines.append(f"\n📋 {line.upper()}")
            continue
            
        # Part 구분
        if re.match(r'PART \d+', line):
            clean_lines.append(f"\n🔖 {line}")
            continue
            
        # 챕터 제목 (번호 + ■ + 제목 + 페이지)
        chapter_match = re.match(r'(\d+)\s*■\s*(.+?)\s+(\d+)$', line)
        if chapter_match:
            num, title, page = chapter_match.groups()
            clean_lines.append(f"   {num:>2}. {title} ...................... {page}")
            continue
            
        # 하위 섹션들 (점으로 구분된 내용)
        if '■' in line and any(char.isdigit() for char in line):
            # 여러 항목이 한 줄에 있는 경우 분리
            parts = re.split(r'\s*■\s*', line)
            for part in parts:
                if part.strip() and any(char.isdigit() for char in part):
                    clean_lines.append(f"      • {part.strip()}")
            continue
            
        # 부록들
        if line.lower().startswith('appendix'):
            clean_lines.append(f"   📎 {line}")
            continue
    
    return clean_lines

def format_toc_output(clean_lines):
    """최종 출력 형태로 포맷팅"""
    print("=" * 70)
    print("📚 DATA-ORIENTED PROGRAMMING - 목차")
    print("=" * 70)
    
    for line in clean_lines:
        if line.strip():
            print(line)
    
    print("\n" + "=" * 70)

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    print("🔍 PDF 목차 페이지 추출 중...")
    toc_pages = extract_toc_pages(pdf_path)
    
    print("🧹 목차 내용 정리 중...")
    clean_lines = clean_toc_content(toc_pages)
    
    print("📖 깔끔한 목차 출력:")
    format_toc_output(clean_lines)

if __name__ == "__main__":
    main()