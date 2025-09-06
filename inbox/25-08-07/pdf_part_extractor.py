# 목차
# - 생성 시간: 2025-08-07 11:23:15 KST
# - 핵심 내용: core_toc_with_page_ranges.json의 페이지 정보를 활용하여 PDF에서 Part별로 실제 텍스트 내용을 추출하는 도구
# - 상세 내용:
#     - load_toc_data(1-15): JSON 파일에서 TOC 데이터와 페이지 범위를 로드하는 함수
#     - extract_pdf_text(17-30): PDF에서 지정된 페이지 범위의 텍스트를 추출하는 함수
#     - extract_parts_from_pdf(32-65): Part별로 PDF 내용을 추출하고 구조화하는 함수
#     - save_part_content(67-85): 각 Part의 내용을 마크다운 파일로 저장하는 함수
#     - main(87-105): 전체 프로세스를 실행하는 메인 함수
# - 상태: 활성
# - 주소: pdf_part_extractor
# - 참조: core_toc_with_page_ranges.json, 2022_Data-Oriented Programming_Manning.pdf

import json
import os
from typing import Dict, List, Any, Tuple
import pdfplumber
from datetime import datetime

def load_toc_data(file_path: str) -> List[Dict]:
    """TOC JSON 파일을 로드하고 Part 정보를 추출합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Part 정보만 추출 (level 0이면서 "Part"가 포함된 항목)
        parts = [item for item in data if item['level'] == 0 and 'Part' in item['title']]
        print(f"발견된 Part 수: {len(parts)}")
        for part in parts:
            print(f"- {part['title']}: 페이지 {part['start_page']}-{part['end_page']} ({part['page_count']}페이지)")
        return parts
    except Exception as e:
        print(f"TOC 파일 로드 실패: {e}")
        return []

def extract_pdf_text(pdf_path: str, start_page: int, end_page: int) -> str:
    """PDF에서 지정된 페이지 범위의 텍스트를 추출합니다."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []
            
            # 페이지 번호는 0부터 시작하므로 1을 빼줍니다
            for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
                if page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"## 페이지 {page_num + 1}\n\n{page_text}\n")
            
            return "\n".join(text_content)
    except Exception as e:
        print(f"PDF 텍스트 추출 실패 (페이지 {start_page}-{end_page}): {e}")
        return ""

def extract_parts_from_pdf(pdf_path: str, parts_info: List[Dict], output_dir: str):
    """Part별로 PDF 내용을 추출하고 저장합니다."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    extraction_summary = []
    
    for i, part in enumerate(parts_info, 1):
        part_title = part['title']
        start_page = part['start_page']
        end_page = part['end_page']
        page_count = part['page_count']
        
        print(f"\n[{i}/{len(parts_info)}] {part_title} 추출 중...")
        print(f"페이지 범위: {start_page}-{end_page} ({page_count}페이지)")
        
        # PDF에서 텍스트 추출
        content = extract_pdf_text(pdf_path, start_page, end_page)
        
        if content:
            # 파일명에서 특수문자 제거
            safe_title = part_title.replace('—', '_').replace(' ', '_').replace('/', '_')
            filename = f"Part_{i:02d}_{safe_title}.md"
            file_path = os.path.join(output_dir, filename)
            
            # 마크다운 헤더와 메타데이터 추가
            markdown_content = f"""# {part_title}

## 메타데이터
- **Part 번호**: {i}
- **페이지 범위**: {start_page}-{end_page}
- **총 페이지 수**: {page_count}
- **추출 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')}

## 내용

{content}
"""
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            extraction_summary.append({
                "part_number": i,
                "title": part_title,
                "filename": filename,
                "page_range": f"{start_page}-{end_page}",
                "page_count": page_count,
                "content_length": len(content),
                "status": "성공"
            })
            
            print(f"✅ 저장 완료: {filename} ({len(content):,} 문자)")
        else:
            print(f"❌ 추출 실패: {part_title}")
            extraction_summary.append({
                "part_number": i,
                "title": part_title,
                "status": "실패"
            })
    
    return extraction_summary

def save_extraction_summary(summary: List[Dict], output_dir: str):
    """추출 결과 요약을 저장합니다."""
    summary_file = os.path.join(output_dir, "extraction_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"📋 추출 요약 저장: extraction_summary.json")

def main():
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges.json"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts"
    
    print("🚀 PDF Part별 내용 추출 시작...")
    print(f"📖 PDF: {os.path.basename(pdf_file)}")
    print(f"📋 TOC: {os.path.basename(toc_file)}")
    print(f"📁 출력: {output_dir}")
    
    # TOC 데이터에서 Part 정보 로드
    parts_info = load_toc_data(toc_file)
    if not parts_info:
        print("❌ Part 정보를 찾을 수 없습니다.")
        return
    
    # PDF에서 Part별 내용 추출
    summary = extract_parts_from_pdf(pdf_file, parts_info, output_dir)
    
    # 추출 결과 요약 저장
    save_extraction_summary(summary, output_dir)
    
    # 최종 결과 출력
    successful = len([s for s in summary if s.get('status') == '성공'])
    print(f"\n🎉 추출 완료! {successful}/{len(parts_info)}개 Part 성공")
    print(f"📁 결과 파일들이 '{output_dir}' 디렉터리에 저장되었습니다.")

if __name__ == "__main__":
    main()