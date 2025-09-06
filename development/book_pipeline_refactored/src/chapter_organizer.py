# 생성 시간: 2025년 09월 02일 17시 10분  
# 핵심 내용: AI가 식별한 장 정보를 바탕으로 extraction-system의 기존 구조와 동일한 형태로 장별 폴더와 파일을 생성하는 ChapterOrganizer 클래스
# 상세 내용:
#   - ChapterOrganizer.__init__ (라인 25-35): 기본 경로와 로거 초기화
#   - generate_book_folder_name (라인 37-50): PDF 파일명에서 책 폴더명 생성
#   - create_book_directory (라인 52-65): extraction-system 하위에 책 디렉토리 생성
#   - generate_chapter_folder_name (라인 67-80): 장 정보에서 폴더명 생성 (기존 구조 따름)
#   - create_chapter_directory (라인 82-95): 책 폴더 하위에 장별 디렉토리 생성
#   - filter_toc_items_for_chapter (라인 97-110): 장별 목차 항목 필터링
#   - save_chapter_toc_json (라인 112-130): 장별 목차 JSON 파일 저장 (기존 형식)
#   - create_chapter_content_md (라인 132-165): 장별 내용 마크다운 파일 생성 (기존 형식)
#   - organize_book_chapters (라인 167-220): 전체 책의 장들을 정리하는 메인 메서드
# 상태: active  
# 참조: 새로 생성된 파일

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from refactoring_logger import RefactoringLogger, RefactoringLogContext


class ChapterOrganizer:
    """
    AI가 식별한 장 정보를 바탕으로 extraction-system 폴더 구조에서
    기존과 동일한 형태의 장별 폴더와 파일을 생성하는 클래스
    """
    
    def __init__(self, base_extraction_path: Path, logger: Optional[RefactoringLogger] = None):
        """
        ChapterOrganizer 초기화
        
        Args:
            base_extraction_path: extraction-system 기본 경로
            logger: 로깅용 RefactoringLogger 인스턴스
        """
        self.base_extraction_path = Path(base_extraction_path)
        self.logger = logger
        
        # extraction-system 디렉토리 생성
        self.base_extraction_path.mkdir(parents=True, exist_ok=True)

    def generate_book_folder_name(self, pdf_filename: str) -> str:
        """
        PDF 파일명에서 책 폴더명 생성 (기존: Data_Oriented_Programming)
        
        Args:
            pdf_filename: PDF 파일명 (예: "2022_Data-Oriented Programming_Manning.pdf")
            
        Returns:
            str: 폴더명 (예: "Data_Oriented_Programming")
        """
        # 확장자 제거
        name_without_ext = pdf_filename.replace('.pdf', '')
        
        # 연도, 출판사 등 제거 (간단한 규칙)
        name_parts = name_without_ext.split('_')
        
        # 첫 번째가 연도인 경우 제거
        if name_parts and name_parts[0].isdigit():
            name_parts = name_parts[1:]
        
        # 마지막이 출판사명인 경우 제거 (Manning, O'Reilly 등)
        if name_parts and name_parts[-1].lower() in ['manning', 'oreilly', "o'reilly"]:
            name_parts = name_parts[:-1]
        
        # 특수문자를 언더스코어로 변환
        folder_name = '_'.join(name_parts)
        folder_name = re.sub(r'[^a-zA-Z0-9_]', '_', folder_name)
        folder_name = re.sub(r'_+', '_', folder_name)  # 연속된 언더스코어 제거
        
        return folder_name.strip('_')

    def create_book_directory(self, pdf_filename: str) -> Path:
        """
        extraction-system 하위에 책 디렉토리 생성
        
        Args:
            pdf_filename: PDF 파일명
            
        Returns:
            Path: 생성된 책 디렉토리 경로
        """
        folder_name = self.generate_book_folder_name(pdf_filename)
        book_dir = self.base_extraction_path / folder_name
        book_dir.mkdir(parents=True, exist_ok=True)
        
        if self.logger:
            context = RefactoringLogContext("ChapterOrganizer", "create_book_directory")
            self.logger.operation_info(context, f"Created book directory: {book_dir}")
        
        return book_dir

    def generate_chapter_folder_name(self, chapter_info: Dict[str, Any]) -> str:
        """
        장 정보에서 폴더명 생성 (기존 구조: "1_Complexity_of_object_oriented_programming")
        
        Args:
            chapter_info: 장 정보 딕셔너리
            
        Returns:
            str: 폴더명
        """
        title = chapter_info.get('title', '').strip()
        if not title:
            raise ValueError("Invalid chapter information: missing title")
        
        # 공백과 특수문자를 언더스코어로 변환하고 정리
        folder_name = re.sub(r'[^a-zA-Z0-9]+', '_', title)
        folder_name = re.sub(r'_+', '_', folder_name)  # 연속된 언더스코어 제거
        folder_name = folder_name.strip('_')
        
        return folder_name

    def create_chapter_directory(self, book_dir: Path, chapter_info: Dict[str, Any]) -> Path:
        """
        책 폴더 하위에 장별 디렉토리 생성
        
        Args:
            book_dir: 책 디렉토리 경로
            chapter_info: 장 정보
            
        Returns:
            Path: 생성된 장 디렉토리 경로
        """
        folder_name = self.generate_chapter_folder_name(chapter_info)
        chapter_dir = book_dir / folder_name
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        return chapter_dir

    def filter_toc_items_for_chapter(self, chapter_info: Dict[str, Any], toc_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        장별 목차 항목 필터링
        
        Args:
            chapter_info: 장 정보
            toc_items: 전체 목차 항목들
            
        Returns:
            List[Dict]: 해당 장에 속하는 목차 항목들
        """
        start_page = chapter_info.get('start_page', 0)
        end_page = chapter_info.get('end_page', 9999)
        
        chapter_toc_items = [
            item for item in toc_items 
            if start_page <= item.get('page', 0) <= end_page
        ]
        
        return chapter_toc_items

    def save_chapter_toc_json(self, chapter_dir: Path, chapter_info: Dict[str, Any], 
                             toc_items: List[Dict[str, Any]]) -> Path:
        """
        장별 목차 JSON 파일 저장 (기존 형식: {장제목}_toc.json)
        
        Args:
            chapter_dir: 장 디렉토리 경로
            chapter_info: 장 정보
            toc_items: 장에 속하는 목차 항목들
            
        Returns:
            Path: 저장된 JSON 파일 경로
        """
        folder_name = self.generate_chapter_folder_name(chapter_info)
        json_file = chapter_dir / f"{folder_name}_toc.json"
        
        # 기존 형식과 동일하게 저장
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(toc_items, f, ensure_ascii=False, indent=2)
        
        if self.logger:
            context = RefactoringLogContext("ChapterOrganizer", "save_chapter_toc_json")
            self.logger.operation_info(context, f"Saved {len(toc_items)} TOC items to: {json_file}")
        
        return json_file

    def create_chapter_content_md(self, chapter_dir: Path, chapter_info: Dict[str, Any]) -> Path:
        """
        장별 내용 마크다운 파일 생성 (기존 형식: {장제목}_content.md)
        
        Args:
            chapter_dir: 장 디렉토리 경로
            chapter_info: 장 정보
            
        Returns:
            Path: 생성된 마크다운 파일 경로
        """
        folder_name = self.generate_chapter_folder_name(chapter_info)
        md_file = chapter_dir / f"{folder_name}_content.md"
        
        title = chapter_info.get('title', '')
        start_page = chapter_info.get('start_page', 0)
        end_page = chapter_info.get('end_page', 0)
        
        # 기본 구조만 생성 (실제 내용은 향후 PDF 텍스트 추출로 채울 예정)
        content = f"""# {title}

## Page {start_page}

[이 섹션은 PDF 텍스트 추출 기능이 구현되면 실제 내용으로 채워질 예정입니다]

페이지 범위: {start_page}-{end_page}
추출 일시: {datetime.now().strftime("%Y-%m-%d %H:%M:%S KST")}

---

> 향후 PDF 텍스트 추출 시스템이 완성되면 이 파일은 실제 장 내용으로 업데이트됩니다.
> 현재는 장 구조와 메타데이터만 포함되어 있습니다.
"""
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return md_file

    def organize_book_chapters(self, pdf_filename: str, chapters_info: List[Dict[str, Any]], 
                              toc_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        전체 책의 장들을 extraction-system 구조에 정리 (기존 형식 준수)
        
        Args:
            pdf_filename: PDF 파일명
            chapters_info: AI가 식별한 장 정보들
            toc_items: 전체 목차 항목들
            
        Returns:
            Dict: 정리 결과 정보
        """
        context = RefactoringLogContext("ChapterOrganizer", "organize_book_chapters")
        
        try:
            # 1. 책 디렉토리 생성
            book_dir = self.create_book_directory(pdf_filename)
            book_title = self.generate_book_folder_name(pdf_filename).replace('_', ' ')
            
            if self.logger:
                self.logger.operation_start(context, {
                    "pdf_filename": pdf_filename,
                    "chapters_count": len(chapters_info),
                    "book_directory": str(book_dir)
                })
            
            created_chapters = []
            
            # 2. 각 장별 처리
            for chapter_info in chapters_info:
                try:
                    # 장 디렉토리 생성
                    chapter_dir = self.create_chapter_directory(book_dir, chapter_info)
                    
                    # 해당 장의 목차 항목들 필터링
                    chapter_toc_items = self.filter_toc_items_for_chapter(chapter_info, toc_items)
                    
                    # JSON 파일 저장 (기존 형식)
                    json_file = self.save_chapter_toc_json(chapter_dir, chapter_info, chapter_toc_items)
                    
                    # 마크다운 파일 생성 (기존 형식)
                    md_file = self.create_chapter_content_md(chapter_dir, chapter_info)
                    
                    created_chapters.append({
                        "title": chapter_info.get('title', ''),
                        "directory": str(chapter_dir),
                        "toc_items_count": len(chapter_toc_items),
                        "json_file": str(json_file),
                        "markdown_file": str(md_file)
                    })
                    
                except Exception as e:
                    if self.logger:
                        self.logger.operation_error(context, f"Error processing chapter {chapter_info.get('title', '')}: {e}")
                    continue
            
            result = {
                "success": True,
                "book_title": book_title,
                "book_directory": str(book_dir),
                "created_chapters": created_chapters,
                "total_chapters": len(created_chapters)
            }
            
            if self.logger:
                self.logger.operation_success(context, {
                    "success": True,
                    "total_chapters_created": len(created_chapters)
                })
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.operation_error(context, str(e))
            return {"success": False, "error": str(e)}