# 생성 시간: Thu Sep  4 08:47:30 KST 2025
# 핵심 내용: ChapterExtractionService의 Social Unit 테스트 (내부 의존성 포함, 실제 유틸리티 사용)
# 상세 내용:
#   - TestChapterExtractionServiceSocial (라인 18-180): ChapterExtractionService의 사회적 단위 테스트 클래스
#   - test_normalize_title_with_service (라인 23-45): normalize_title 메서드 테스트
#   - test_extract_pdf_content_with_real_pdf (라인 47-75): PDF 내용 추출 메서드 테스트
#   - test_find_chapter_items_with_real_toc (라인 77-110): 장별 목차 항목 찾기 메서드 테스트
#   - test_save_chapter_content_to_folder_real_data (라인 112-150): 폴더 생성 및 저장 메서드 테스트
# 상태: active
# 주소: tests/unit/social/test_chapter_extraction_service_social
# 참조: 기존 extract_chapters_v5 로직과 동일한 결과 검증

import pytest
import sys
import json
from pathlib import Path

# ChapterExtractionService import를 위한 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.chapter_extraction_service import ChapterExtractionService
from services.toc_service import TocService
from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory

@pytest.mark.social_unit
class TestChapterExtractionServiceSocial:
    """
    ChapterExtractionService의 Social Unit 테스트
    - 실제 ConfigManager, LoggerFactory 사용
    - 내부 의존성 포함한 협력 테스트
    - 기존 extract_chapters_v5 로직과 동일한 동작 검증
    """
    
    def test_normalize_title_with_service(self, temp_directory):
        """
        요구사항: ChapterExtractionService.normalize_title()이 다양한 제목 입력에 대해 정규화된 문자열 반환
        입력: 다양한 형태의 제목 문자열 (str)
        출력: 정규화된 제목 문자열 (str) - 특수문자 제거, 공백을 언더스코어로 변환
        """
        # Given: ChapterExtractionService 인스턴스 생성
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        service = ChapterExtractionService(config_manager, logger)
        
        # When & Then: 다양한 제목 정규화 테스트
        test_cases = [
            ("1 Complexity of object- oriented programming", "1_Complexity_of_object_oriented_programming"),
            ("2 Separation between code and data", "2_Separation_between_code_and_data"),
            ("A.1 Principle #1: Separate code from data", "A.1_Principle_1_Separate_code_from_data"),
            ("Special-chars: !@#$%^&*()", "Special_chars"),
            ("Multiple   spaces    test", "Multiple_spaces_test"),
            ("", ""),
            ("   leading_trailing   ", "leading_trailing")
        ]
        
        for original, expected in test_cases:
            result = service.normalize_title(original)
            assert result == expected, f"입력: '{original}' → 기대: '{expected}', 결과: '{result}'"

    def test_extract_pdf_content_with_real_pdf(self, real_pdf_path, temp_directory):
        """
        요구사항: ChapterExtractionService.extract_pdf_content()가 PDF에서 지정된 페이지 범위의 텍스트 추출
        입력: PDF 파일 경로 (str), 시작 페이지 (int), 끝 페이지 (int)
        출력: 추출된 텍스트 내용 (str) - 페이지별로 마크다운 형식
        """
        # Given: ChapterExtractionService 인스턴스
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        service = ChapterExtractionService(config_manager, logger)
        
        # When: PDF에서 첫 3페이지 내용 추출
        extracted_content = service.extract_pdf_content(real_pdf_path, 1, 3)
        
        # Then: 추출된 내용 검증
        assert isinstance(extracted_content, str), "추출된 내용은 문자열이어야 함"
        assert len(extracted_content) > 0, "내용이 추출되어야 함"
        assert "## Page" in extracted_content, "페이지 마커가 포함되어야 함"
        
        # 페이지별 구조 확인
        pages = extracted_content.split("## Page")
        assert len(pages) >= 2, "최소 2개 페이지가 추출되어야 함"
        
        print(f"\n📄 ChapterExtractionService PDF 내용 추출 테스트 결과:")
        print(f"  - 추출된 텍스트 길이: {len(extracted_content)} 문자")
        print(f"  - 페이지 섹션 수: {len(pages) - 1}")
        print(f"  - 첫 100자: {extracted_content[:100]}...")

    def test_find_chapter_items_with_real_toc(self, real_pdf_path, temp_directory):
        """
        요구사항: ChapterExtractionService.find_chapter_items()가 실제 목차에서 특정 장의 하위 항목들을 찾아 반환
        입력: 목차 구조 (List[Dict]), 장 시작 ID (int), 다음 장 시작 ID (int)
        출력: 해당 장의 모든 하위 목차 항목들 (List[Dict])
        """
        # Given: ChapterExtractionService와 실제 목차 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        service = ChapterExtractionService(config_manager, logger)
        
        # 실제 목차 데이터 추출
        toc_service = TocService(config_manager, logger)
        toc_data = toc_service.extract_complete_toc(real_pdf_path)
        toc_structure = toc_data['toc_structure']
        
        # 첫 번째와 두 번째 최상위 항목 찾기
        root_items = [item for item in toc_structure if item['level'] == 0]
        assert len(root_items) >= 2, "최소 2개의 최상위 항목이 있어야 함"
        
        first_chapter_id = root_items[0]['id']
        second_chapter_id = root_items[1]['id']
        
        # When: 첫 번째 장의 하위 항목들 찾기
        chapter_items = service.find_chapter_items(toc_structure, first_chapter_id, second_chapter_id)
        
        # Then: 하위 항목들 검증
        assert isinstance(chapter_items, list), "결과는 리스트여야 함"
        assert len(chapter_items) > 0, "최소 1개의 하위 항목이 있어야 함"
        
        # 모든 항목이 적절한 구조를 가지는지 확인
        for item in chapter_items:
            assert isinstance(item, dict), "각 항목은 딕셔너리여야 함"
            assert 'id' in item, "각 항목에 id가 있어야 함"
            assert 'title' in item, "각 항목에 title이 있어야 함"
        
        print(f"\n🔍 ChapterExtractionService find_chapter_items 테스트 결과:")
        print(f"  - 첫 번째 장 ID: {first_chapter_id}")
        print(f"  - 두 번째 장 ID: {second_chapter_id}")
        print(f"  - 찾은 하위 항목 수: {len(chapter_items)}")
        print(f"  - 첫 번째 하위 항목: {chapter_items[0]['title'] if chapter_items else 'None'}")

    def test_save_chapter_content_to_folder_real_data(self, real_pdf_path, temp_directory):
        """
        요구사항: ChapterExtractionService.save_chapter_content_to_folder()가 장별 폴더를 생성하고 목차와 내용을 저장
        입력: 장 제목 (str), 장 항목들 (List[Dict]), 장 내용 (str), 출력 디렉터리 (Path)
        출력: 장별 폴더에 저장된 TOC 및 내용 파일들
        """
        # Given: ChapterExtractionService와 실제 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        service = ChapterExtractionService(config_manager, logger)
        
        # 실제 목차 데이터에서 첫 번째 장 준비
        toc_service = TocService(config_manager, logger)
        toc_data = toc_service.extract_complete_toc(real_pdf_path)
        toc_structure = toc_data['toc_structure']
        
        root_items = [item for item in toc_structure if item['level'] == 0]
        first_chapter = root_items[0]
        chapter_title = first_chapter['title']
        
        # 테스트 항목들과 내용 준비
        test_items = [first_chapter]
        test_content = "# 테스트 장 내용\n\n이것은 ChapterExtractionService 테스트 내용입니다."
        
        output_dir = Path(temp_directory) / "test_service_chapters"
        output_dir.mkdir(exist_ok=True)
        
        # When: 장별 폴더 생성 및 저장
        toc_filepath, content_filepath = service.save_chapter_content_to_folder(
            chapter_title, test_items, test_content, output_dir
        )
        
        # Then: 생성된 파일들 검증
        assert toc_filepath.exists(), "목차 파일이 생성되어야 함"
        assert content_filepath.exists(), "내용 파일이 생성되어야 함"
        
        # 목차 파일 내용 검증
        with open(toc_filepath, 'r', encoding='utf-8') as f:
            saved_toc = json.load(f)
        assert isinstance(saved_toc, list), "저장된 목차는 리스트여야 함"
        assert len(saved_toc) == len(test_items), "저장된 항목 수가 일치해야 함"
        
        # 내용 파일 검증
        with open(content_filepath, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert test_content in saved_content, "테스트 내용이 포함되어야 함"
        assert chapter_title in saved_content, "장 제목이 포함되어야 함"
        
        print(f"\n💾 ChapterExtractionService save_chapter_content_to_folder 테스트 결과:")
        print(f"  - 장 제목: {chapter_title}")
        print(f"  - 정규화된 폴더명: {service.normalize_title(chapter_title)}")
        print(f"  - 목차 파일: {toc_filepath}")
        print(f"  - 내용 파일: {content_filepath}")
        print(f"  - 저장된 항목 수: {len(saved_toc)}")

    def test_service_full_workflow_without_ai(self, real_pdf_path, temp_directory):
        """
        요구사항: ChapterExtractionService의 AI 제외 전체 워크플로우 테스트
        입력: 실제 PDF 파일과 목차 데이터
        출력: 전체 처리 과정 검증 (AI 제외)
        """
        # Given: 완전한 서비스 설정
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        service = ChapterExtractionService(config_manager, logger)
        
        # 실제 목차 데이터 추출
        toc_service = TocService(config_manager, logger)
        toc_data = toc_service.extract_complete_toc(real_pdf_path)
        toc_structure = toc_data['toc_structure']
        
        # 첫 번째 장 데이터 준비
        root_items = [item for item in toc_structure if item['level'] == 0]
        first_chapter = root_items[0]
        
        # When: 전체 워크플로우 실행 (AI 제외)
        # 1. 제목 정규화
        normalized_title = service.normalize_title(first_chapter['title'])
        
        # 2. PDF 내용 추출 (첫 3페이지)
        extracted_content = service.extract_pdf_content(real_pdf_path, 1, 3)
        
        # 3. 장 항목들 찾기
        second_chapter_id = root_items[1]['id'] if len(root_items) > 1 else None
        chapter_items = service.find_chapter_items(toc_structure, first_chapter['id'], second_chapter_id)
        
        # 4. 폴더 생성 및 저장
        output_dir = Path(temp_directory) / "workflow_test"
        output_dir.mkdir(exist_ok=True)
        toc_filepath, content_filepath = service.save_chapter_content_to_folder(
            first_chapter['title'], chapter_items, extracted_content, output_dir
        )
        
        # Then: 전체 결과 검증
        assert len(normalized_title) > 0, "정규화된 제목이 생성되어야 함"
        assert len(extracted_content) > 0, "PDF 내용이 추출되어야 함"
        assert len(chapter_items) > 0, "장 항목들이 찾아져야 함"
        assert toc_filepath.exists(), "목차 파일이 생성되어야 함"
        assert content_filepath.exists(), "내용 파일이 생성되어야 함"
        
        print(f"\n🔄 ChapterExtractionService 전체 워크플로우 테스트 결과:")
        print(f"  - 원본 제목: {first_chapter['title']}")
        print(f"  - 정규화된 제목: {normalized_title}")
        print(f"  - 추출된 내용 길이: {len(extracted_content)} 문자")
        print(f"  - 장 항목 수: {len(chapter_items)}")
        print(f"  - 생성된 파일들: {toc_filepath.name}, {content_filepath.name}")
        print(f"  - 모든 단계 성공적으로 완료 ✅")