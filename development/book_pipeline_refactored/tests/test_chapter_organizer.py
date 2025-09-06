# 생성 시간: 2025년 09월 02일 17시 05분
# 핵심 내용: 실제 PDF에서 추출된 장 정보를 바탕으로 책 제목 기반 폴더 구조에서 장별 폴더와 파일을 생성하는 ChapterOrganizer 클래스의 TDD 테스트
# 상세 내용:
#   - load_real_data (라인 20-35): 실제 추출된 결과 파일을 로드하는 helper 메서드
#   - test_create_book_directory (라인 45-55): 책 제목 기반 디렉토리 생성 테스트
#   - test_create_chapter_directory_under_book (라인 57-75): 책 폴더 하위에 장별 디렉토리 생성 테스트
#   - test_save_chapter_toc_json_with_book_structure (라인 77-105): 책 구조 내에서 JSON 저장 테스트
#   - test_organize_all_chapters_under_book (라인 107-140): 전체 15개 장을 책 폴더 하위에 정리하는 테스트
#   - test_book_folder_path_generation (라인 142-158): extraction-system 경로 생성 테스트
# 상태: active
# 참조: 새로 생성된 파일

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from chapter_organizer import ChapterOrganizer
from refactoring_logger import RefactoringLogger


class TestChapterOrganizerWithBookStructure:
    
    @pytest.fixture
    def load_real_data(self):
        """실제 추출된 데이터를 로드"""
        results_dir = Path('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/logs/results')
        
        # AI 장 식별 결과 로드
        with open(results_dir / 'ai_chapter_identification_result.json', 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        
        # TOC 추출 결과 로드 
        with open(results_dir / 'toc_extraction_result.json', 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        
        return {
            'chapters_info': chapter_data['chapters_info'],
            'identified_chapters': chapter_data['identified_chapters'],
            'toc_items': toc_data['toc_structure'],
            'pdf_filename': '2022_Data-Oriented Programming_Manning.pdf'
        }
    
    @pytest.fixture
    def extraction_system_base(self):
        """extraction-system 기본 경로"""
        return Path('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system')
    
    @pytest.fixture 
    def logger(self, extraction_system_base):
        """테스트용 로거 fixture"""
        return RefactoringLogger(extraction_system_base / "logs")
    
    @pytest.fixture
    def chapter_organizer(self, extraction_system_base, logger):
        """ChapterOrganizer 인스턴스"""
        return ChapterOrganizer(extraction_system_base, logger)

    def test_create_book_directory(self, chapter_organizer, load_real_data, extraction_system_base):
        """책 제목 기반 디렉토리 생성 테스트"""
        # Given
        pdf_filename = load_real_data['pdf_filename']
        
        # When
        book_dir = chapter_organizer.create_book_directory(pdf_filename)
        
        # Then
        expected_dir = extraction_system_base / "Data_Oriented_Programming"
        assert book_dir == expected_dir
        assert book_dir.exists()
        assert book_dir.is_dir()
        
        print(f"✅ Created book directory: {book_dir}")

    def test_create_chapter_directory_under_book(self, chapter_organizer, load_real_data, extraction_system_base):
        """책 폴더 하위에 장별 디렉토리 생성 테스트"""
        # Given
        pdf_filename = load_real_data['pdf_filename'] 
        book_dir = chapter_organizer.create_book_directory(pdf_filename)
        first_chapter = load_real_data['chapters_info'][0]
        
        # When
        chapter_dir = chapter_organizer.create_chapter_directory(book_dir, first_chapter)
        
        # Then
        expected_path = extraction_system_base / "Data_Oriented_Programming" / "chapter_01_complexity_oop"
        assert chapter_dir == expected_path
        assert chapter_dir.exists()
        assert chapter_dir.is_dir()
        
        # 상위 디렉토리가 책 디렉토리인지 확인
        assert chapter_dir.parent == book_dir
        
        print(f"✅ Created chapter directory: {chapter_dir}")

    def test_save_chapter_toc_json_with_book_structure(self, chapter_organizer, load_real_data, extraction_system_base):
        """책 구조 내에서 목차 JSON 저장 테스트"""
        # Given
        pdf_filename = load_real_data['pdf_filename']
        book_dir = chapter_organizer.create_book_directory(pdf_filename)
        first_chapter = load_real_data['chapters_info'][0]
        chapter_dir = chapter_organizer.create_chapter_directory(book_dir, first_chapter)
        
        # Chapter 1에 속하는 목차 항목들 필터링
        chapter_toc_items = [
            item for item in load_real_data['toc_items'] 
            if first_chapter['start_page'] <= item['page'] <= first_chapter['end_page']
        ]
        
        # When
        json_file = chapter_organizer.save_chapter_toc_json(
            chapter_dir, 
            first_chapter, 
            chapter_toc_items
        )
        
        # Then
        expected_file = extraction_system_base / "Data_Oriented_Programming" / "chapter_01_complexity_oop" / "toc_items.json"
        assert json_file == expected_file
        assert json_file.exists()
        
        # JSON 내용 검증
        with open(json_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data["chapter_info"]["title"] == first_chapter["title"]
        assert saved_data["book_info"]["title"] == "Data-Oriented Programming"
        assert saved_data["book_info"]["filename"] == pdf_filename
        assert len(saved_data["toc_items"]) > 0
        
        print(f"✅ Saved TOC JSON in book structure: {json_file}")

    def test_organize_all_chapters_under_book(self, chapter_organizer, load_real_data, extraction_system_base):
        """전체 15개 장을 책 폴더 하위에 정리하는 테스트"""
        # Given
        pdf_filename = load_real_data['pdf_filename']
        chapters_info = load_real_data['chapters_info']
        toc_items = load_real_data['toc_items']
        
        # When
        result = chapter_organizer.organize_book_chapters(pdf_filename, chapters_info, toc_items)
        
        # Then
        assert result["success"] == True
        assert result["book_title"] == "Data-Oriented Programming"
        assert len(result["created_chapters"]) == 15
        
        # 책 디렉토리 존재 확인
        book_dir = extraction_system_base / "Data_Oriented_Programming"
        assert book_dir.exists()
        
        # 각 장별 디렉토리와 파일 존재 확인
        chapter1_dir = book_dir / "chapter_01_complexity_oop"
        chapter15_dir = book_dir / "chapter_15_debugging"
        
        assert chapter1_dir.exists()
        assert chapter15_dir.exists()
        assert (chapter1_dir / "toc_items.json").exists()
        assert (chapter1_dir / "chapter_content.md").exists()
        assert (chapter15_dir / "toc_items.json").exists() 
        assert (chapter15_dir / "chapter_content.md").exists()
        
        # 전체 구조 확인
        expected_structure = f"""
        {extraction_system_base}/
        └── Data_Oriented_Programming/
            ├── chapter_01_complexity_oop/
            │   ├── toc_items.json
            │   └── chapter_content.md
            ├── chapter_02_separation_code_data/
            └── ... (총 15개 장)
        """
        
        print(f"✅ Organized all {len(chapters_info)} chapters under book directory")
        print(f"📁 Book structure: {book_dir}")

    def test_book_folder_path_generation(self, chapter_organizer):
        """extraction-system 경로에서 책 폴더명 생성 테스트"""
        # Given
        test_cases = [
            ("2022_Data-Oriented Programming_Manning.pdf", "Data_Oriented_Programming"),
            ("Clean Code_Robert Martin.pdf", "Clean_Code_Robert_Martin"),
            ("Design Patterns - GoF.pdf", "Design_Patterns_GoF")
        ]
        
        for pdf_filename, expected_folder_name in test_cases:
            # When
            folder_name = chapter_organizer.generate_book_folder_name(pdf_filename)
            
            # Then
            assert folder_name == expected_folder_name
            print(f"✅ '{pdf_filename}' → '{folder_name}'")

    def test_chapter_markdown_with_book_info(self, chapter_organizer, load_real_data, extraction_system_base):
        """책 정보가 포함된 마크다운 생성 테스트"""
        # Given
        pdf_filename = load_real_data['pdf_filename']
        book_dir = chapter_organizer.create_book_directory(pdf_filename)
        first_chapter = load_real_data['chapters_info'][0]
        chapter_dir = chapter_organizer.create_chapter_directory(book_dir, first_chapter)
        
        chapter_toc_items = [
            item for item in load_real_data['toc_items'] 
            if first_chapter['start_page'] <= item['page'] <= first_chapter['end_page']
        ]
        
        # When
        md_file = chapter_organizer.create_chapter_markdown(
            chapter_dir,
            first_chapter, 
            chapter_toc_items,
            book_info={"title": "Data-Oriented Programming", "filename": pdf_filename}
        )
        
        # Then
        content = md_file.read_text(encoding='utf-8')
        assert "# 1 Complexity of object- oriented programming" in content
        assert "**책 제목**: Data-Oriented Programming" in content  
        assert "**소스 파일**: 2022_Data-Oriented Programming_Manning.pdf" in content
        assert "**페이지**: 31-53" in content
        
        print(f"✅ Created chapter markdown with book info: {md_file}")

    def test_directory_cleanup_on_rerun(self, chapter_organizer, load_real_data, extraction_system_base):
        """재실행 시 디렉토리 정리 테스트"""
        # Given - 첫 번째 실행
        pdf_filename = load_real_data['pdf_filename']
        result1 = chapter_organizer.organize_book_chapters(
            pdf_filename, 
            load_real_data['chapters_info'][:2],  # 처음 2개 장만
            load_real_data['toc_items']
        )
        
        book_dir = extraction_system_base / "Data_Oriented_Programming"
        assert len(list(book_dir.iterdir())) == 2  # 2개 장 폴더
        
        # When - 두 번째 실행 (전체 15개 장)
        result2 = chapter_organizer.organize_book_chapters(
            pdf_filename,
            load_real_data['chapters_info'],  # 전체 15개 장
            load_real_data['toc_items']
        )
        
        # Then
        assert result2["success"] == True
        assert len(list(book_dir.iterdir())) == 15  # 15개 장 폴더
        
        print(f"✅ Directory cleanup and reorganization successful")