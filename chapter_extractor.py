"""
생성 시간: 2025-08-30 11:58:40 KST
핵심 내용: PDF에서 목차 정보 기반으로 특정 장의 내용만 추출하는 스크립트
상세 내용:
    - import 구문 (1-8): 필요한 라이브러리 import
    - ChapterExtractor 클래스 (10-120): 메인 추출 로직을 담은 클래스
        - __init__ (11-15): 초기화 및 PDF 문서 로드
        - load_toc_json (17-25): JSON 목차 파일 읽기
        - get_chapter_by_level (27-35): 레벨 1 장들만 필터링
        - extract_text_from_pages (37-52): 페이지 범위에서 텍스트 추출
        - clean_filename (54-59): 파일명 정리 (특수문자 제거)
        - save_as_markdown (61-78): 마크다운 형식으로 저장
        - extract_chapter (80-106): 단일 장 추출 메인 로직
        - extract_all_chapters (108-120): 모든 장 추출
    - main 함수 (122-145): 스크립트 실행 진입점
상태: active
주소: chapter_extractor
참조: 
"""

import json
import fitz  # PyMuPDF
import os
import re
import argparse
from pathlib import Path
import sys

class ChapterExtractor:
    def __init__(self, pdf_path):
        """PDF 문서 초기화"""
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        print(f"PDF 로드 완료: {len(self.doc)} 페이지")
    
    def load_toc_json(self, json_path):
        """JSON 목차 파일 읽기"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON 파일 읽기 실패: {e}")
            return None
    
    def get_chapter_by_level(self, toc_data, level=1):
        """특정 레벨의 장들만 추출 (기본값: 레벨 1)"""
        chapters = []
        for item in toc_data:
            if item.get('level') == level:
                chapters.append(item)
        return chapters
    
    def extract_text_from_pages(self, start_page, end_page):
        """지정된 페이지 범위에서 텍스트 추출"""
        text_content = []
        
        # PDF 페이지는 0부터 시작하므로 1을 빼줌
        start_idx = start_page - 1
        end_idx = end_page - 1
        
        if start_idx < 0 or end_idx >= len(self.doc):
            print(f"페이지 범위 오류: {start_page}-{end_page} (총 {len(self.doc)} 페이지)")
            return ""
        
        for page_num in range(start_idx, end_idx + 1):
            page = self.doc[page_num]
            text = page.get_text()
            text_content.append(f"--- 페이지 {page_num + 1} ---\n{text}")
        
        return "\n\n".join(text_content)
    
    def clean_filename(self, title):
        """파일명에 사용할 수 없는 문자 제거"""
        # 특수문자 제거 및 공백을 언더스코어로 변경
        cleaned = re.sub(r'[<>:"/\\|?*]', '', title)
        cleaned = re.sub(r'\s+', '_', cleaned.strip())
        return cleaned
    
    def save_as_markdown(self, content, title, output_dir="output"):
        """마크다운 형식으로 저장"""
        # 출력 디렉터리 생성
        Path(output_dir).mkdir(exist_ok=True)
        
        # 파일명 생성
        clean_title = self.clean_filename(title)
        filename = f"raw_{clean_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        # 마크다운 형식으로 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(content)
        
        print(f"저장 완료: {filepath}")
        return filepath
    
    def extract_chapter(self, chapter_info, output_dir="output"):
        """단일 장 추출"""
        title = chapter_info.get('title', 'Unknown')
        start_page = chapter_info.get('start_page')
        end_page = chapter_info.get('end_page')
        
        if not start_page or not end_page:
            print(f"페이지 정보 누락: {title}")
            return None
        
        print(f"추출 중: {title} (페이지 {start_page}-{end_page})")
        
        # 텍스트 추출
        content = self.extract_text_from_pages(start_page, end_page)
        
        if not content.strip():
            print(f"내용이 비어있음: {title}")
            return None
        
        # 마크다운으로 저장
        filepath = self.save_as_markdown(content, title, output_dir)
        return filepath
    
    def extract_all_chapters(self, toc_data, output_dir="output", level=1):
        """모든 레벨 1 장 추출"""
        chapters = self.get_chapter_by_level(toc_data, level)
        
        print(f"레벨 {level} 장 {len(chapters)}개 발견")
        
        extracted_files = []
        for chapter in chapters:
            filepath = self.extract_chapter(chapter, output_dir)
            if filepath:
                extracted_files.append(filepath)
        
        print(f"총 {len(extracted_files)}개 파일 추출 완료")
        return extracted_files

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="PDF에서 장별로 내용 추출")
    parser.add_argument("pdf_path", help="PDF 파일 경로")
    parser.add_argument("json_path", help="JSON 목차 파일 경로") 
    parser.add_argument("-o", "--output", default="output", help="출력 디렉터리 (기본값: output)")
    parser.add_argument("-l", "--level", type=int, default=1, help="추출할 장 레벨 (기본값: 1)")
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not os.path.exists(args.pdf_path):
        print(f"PDF 파일을 찾을 수 없습니다: {args.pdf_path}")
        sys.exit(1)
    
    if not os.path.exists(args.json_path):
        print(f"JSON 파일을 찾을 수 없습니다: {args.json_path}")
        sys.exit(1)
    
    # 추출 실행
    try:
        extractor = ChapterExtractor(args.pdf_path)
        toc_data = extractor.load_toc_json(args.json_path)
        
        if toc_data:
            extractor.extract_all_chapters(toc_data, args.output, args.level)
        else:
            print("목차 데이터 로드 실패")
            sys.exit(1)
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()