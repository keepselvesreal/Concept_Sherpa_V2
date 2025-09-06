#!/usr/bin/env python3
"""
Chapter 검색 디버깅
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer
import re

def debug_chapter_search():
    """Chapter 검색 디버깅"""
    normalizer = TOCNormalizer()
    
    # PDF 내용 추출
    normalizer.extract_pdf_content('/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf')
    
    print("=== Chapter 1 검색 디버깅 ===\n")
    
    # Chapter 1 패턴들 테스트
    section_number = '1'
    title = 'Complexity of object-oriented programming'
    
    # 실제 find_section_in_pdf에서 사용하는 패턴들 
    patterns = []
    
    # Chapter 섹션 특별 처리
    title_escaped = re.escape(title.replace(' ', '').replace('-', ''))  # 공백과 하이픈 제거
    title_partial = re.escape(title.split()[0] if title else '')  # 첫 단어만
    patterns.extend([
        rf'\d+\s+CHAPTER\s+{re.escape(section_number)}\s+{re.escape(title)}',
        rf'CHAPTER\s+{re.escape(section_number)}\s+{re.escape(title)}', 
        rf'\d+\s+CHAPTER\s+{re.escape(section_number)}\s+.*{title_partial}',  # 첫 단어 매칭
        rf'\d+\s+CHAPTER\s+{re.escape(section_number)}\s+.*{title_escaped}',  # 연결된 텍스트 매칭
    ])
    
    # 제목과 함께 매칭 (일반적인 경우)
    title_clean = re.escape(title.strip())
    patterns.extend([
        rf'{re.escape(section_number)}\s+{title_clean}',
        rf'Chapter\s+{re.escape(section_number)}\s*[:\-\s]*{title_clean}',
        rf'{re.escape(section_number)}\.?\s+{title_clean}',
    ])
    
    # 번호만으로 매칭 (백업)
    patterns.extend([
        rf'^{re.escape(section_number)}\s+[A-Z]',
        rf'Chapter\s+{re.escape(section_number)}[^\d]',
        rf'Part\s+{re.escape(section_number)}[^\d]',
        rf'PART\s+{re.escape(section_number)}[^\d]',
    ])
    
    print(f"검색 패턴들:")
    for i, pattern in enumerate(patterns):
        print(f"  {i+1}: {pattern}")
    
    print(f"\n페이지별 매칭 결과:")
    
    # 각 페이지에서 검색 - 페이지 25 이후부터
    for page_num, page_text in enumerate(normalizer.pdf_pages):
        if not page_text or page_num < 25:
            continue
            
        lines = page_text.split('\n')
        for line_idx, line in enumerate(lines):
            line = line.strip()
            
            for pattern_idx, pattern in enumerate(patterns):
                if re.search(pattern, line, re.IGNORECASE):
                    print(f"  페이지 {page_num + 1}, 라인 {line_idx + 1}: 패턴 {pattern_idx + 1} 매칭")
                    print(f"    라인: {line}")
                    print(f"    패턴: {pattern}")
                    return (page_num, line_idx)
    
    print("  매칭 없음")
    return None

if __name__ == "__main__":
    debug_chapter_search()