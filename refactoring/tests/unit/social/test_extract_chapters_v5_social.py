# 생성 시간: Thu Sep  4 08:57:20 KST 2025
# 핵심 내용: extract_chapters_v5 기존 함수들의 Social Unit 테스트 (내부 의존성 포함, 실제 데이터 사용)
# 상세 내용:
#   - TestExtractChaptersV5Social (라인 27-200): extract_chapters_v5 함수들의 사회적 단위 테스트 클래스
#   - test_normalize_title_with_various_inputs (라인 32-50): normalize_title 함수 테스트
#   - test_extract_pdf_content_with_real_pdf (라인 52-75): PDF 내용 추출 기능 테스트
#   - test_count_chapters_with_ai_real_data (라인 77-105): AI 기반 장 분석 테스트
#   - test_find_chapter_items_with_real_toc (라인 107-130): 장별 목차 항목 찾기 테스트
#   - test_save_chapter_content_to_folder_real_data (라인 132-160): 폴더 생성 및 저장 기능 테스트
# 상태: active
# 주소: tests/unit/social/test_extract_chapters_v5_social
# 참조: 기존 extract_chapters_v5 로직과 동일한 결과 검증

import pytest
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

# extract_chapters_v5 import를 위한 경로 설정
sys.path.insert(0, "/home/nadle/projects/Knowledge_Sherpa/v2/inbox/25-08-31")

from extract_chapters_v5 import (
    normalize_title, extract_pdf_content, count_chapters_with_ai, 
    find_chapter_items, save_chapter_content_to_folder, GeminiAPIProvider
)

@pytest.mark.social_unit
class TestExtractChaptersV5Social:
    """
    extract_chapters_v5 함수들의 Social Unit 테스트
    - 실제 데이터와 로거 사용
    - 내부 의존성 포함한 협력 테스트
    - 기존 extract_chapters_v5 로직과 동일한 동작 검증
    """
    
    def test_normalize_title_with_various_inputs(self):
        """
        요구사항: normalize_title()이 다양한 제목 입력에 대해 정규화된 문자열 반환
        입력: 다양한 형태의 제목 문자열 (str)
        출력: 정규화된 제목 문자열 (str) - 특수문자 제거, 공백을 언더스코어로 변환
        """
        # Given: 다양한 형태의 제목들
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
            # When: normalize_title 함수 실행
            result = normalize_title(original)
            
            # Then: 예상된 정규화 결과와 일치
            assert result == expected, f"입력: '{original}' → 기대: '{expected}', 결과: '{result}'"

    def test_extract_pdf_content_with_real_pdf(self, real_pdf_path, temp_directory):
        """
        요구사항: extract_pdf_content()가 PDF에서 지정된 페이지 범위의 텍스트 추출
        입력: PDF 파일 경로 (str), 시작 페이지 (int), 끝 페이지 (int), 로거
        출력: 추출된 텍스트 내용 (str) - 페이지별로 마크다운 형식
        """
        # Given: 실제 PDF와 로거
        import logging
        logger = logging.getLogger("test")
        
        # When: PDF에서 첫 3페이지 내용 추출 (실제로는 2페이지만 - index vs 1-based 차이)
        extracted_content = extract_pdf_content(real_pdf_path, 1, 3, logger)
        
        # Then: 추출된 내용 검증
        assert isinstance(extracted_content, str), "추출된 내용은 문자열이어야 함"
        assert len(extracted_content) > 0, "내용이 추출되어야 함"
        assert "## Page" in extracted_content, "페이지 마커가 포함되어야 함"
        
        # 페이지별 구조 확인
        pages = extracted_content.split("## Page")
        assert len(pages) >= 2, "최소 2개 페이지가 추출되어야 함"  # 첫 번째는 빈 문자열
        
        print(f"\n📄 PDF 내용 추출 테스트 결과:")
        print(f"  - 추출된 텍스트 길이: {len(extracted_content)} 문자")
        print(f"  - 페이지 섹션 수: {len(pages) - 1}")
        print(f"  - 첫 100자: {extracted_content[:100]}...")

    def test_count_chapters_with_ai_real_data(self, real_pdf_path, temp_directory):
        """
        요구사항: count_chapters_with_ai()가 실제 목차 데이터에서 숫자 장들을 AI로 분석
        입력: 목차 JSON 파일 경로 (str), AI 제공자, 로거
        출력: 장 분석 결과 (Dict) - chapters_info와 성공 여부 포함
        """
        pytest.skip("AI 제공자 없이는 실행할 수 없음 - 통합 테스트에서 다룰 예정")
        
        # # Given: 실제 목차 데이터와 Mock AI 제공자
        # from services.toc_service import TocService
        # from utils.config_manager import ConfigManager
        # from utils.logger import LoggerFactory
        # 
        # config_manager = ConfigManager()
        # logger_factory = LoggerFactory(config_manager)
        # logger = logger_factory.create_book_logger("test_book", temp_directory)
        # 
        # toc_service = TocService(config_manager, logger)
        # toc_data = toc_service.extract_complete_toc(real_pdf_path)
        # 
        # # 임시 목차 파일 생성
        # toc_file = Path(temp_directory) / "test_toc.json"
        # with open(toc_file, 'w', encoding='utf-8') as f:
        #     json.dump(toc_data, f, ensure_ascii=False, indent=2)
        # 
        # # Mock AI 제공자 생성
        # mock_ai_provider = Mock()
        # mock_response = {
        #     "chapters": [
        #         {"title": "1 Complexity of object- oriented programming", "start_page": 31, "end_page": 53},
        #         {"title": "2 Separation between code and data", "start_page": 54, "end_page": 70}
        #     ]
        # }
        # mock_ai_provider.query.return_value = json.dumps(mock_response)
        # mock_ai_provider.get_name.return_value = "Mock AI"
        # 
        # # When: AI로 장 분석 실행
        # import asyncio
        # result = asyncio.run(count_chapters_with_ai(str(toc_file), mock_ai_provider, logger))
        # 
        # # Then: 분석 결과 검증
        # assert result['success'] == True, "장 분석이 성공해야 함"
        # assert 'chapters_info' in result, "chapters_info가 포함되어야 함"
        # assert len(result['chapters_info']) > 0, "최소 1개 장이 식별되어야 함"

    def test_find_chapter_items_with_real_toc(self, real_pdf_path, temp_directory):
        """
        요구사항: find_chapter_items()가 실제 목차에서 특정 장의 하위 항목들을 찾아 반환
        입력: 목차 구조 (List[Dict]), 장 시작 ID (int), 다음 장 시작 ID (int), 로거  
        출력: 해당 장의 모든 하위 목차 항목들 (List[Dict])
        """
        # Given: 실제 목차 데이터 추출
        from services.toc_service import TocService
        from utils.config_manager import ConfigManager
        from utils.logger import LoggerFactory
        
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        
        toc_service = TocService(config_manager, logger)
        toc_data = toc_service.extract_complete_toc(real_pdf_path)
        toc_structure = toc_data['toc_structure']
        
        # 첫 번째와 두 번째 최상위 항목 찾기 (실제 장 항목)
        root_items = [item for item in toc_structure if item['level'] == 0]
        assert len(root_items) >= 2, "최소 2개의 최상위 항목이 있어야 함"
        
        first_chapter_id = root_items[0]['id']
        second_chapter_id = root_items[1]['id'] 
        
        # When: 첫 번째 장의 하위 항목들 찾기
        chapter_items = find_chapter_items(toc_structure, first_chapter_id, second_chapter_id, logger)
        
        # Then: 하위 항목들 검증
        assert isinstance(chapter_items, list), "결과는 리스트여야 함"
        assert len(chapter_items) > 0, "최소 1개의 하위 항목이 있어야 함"
        
        # 모든 항목이 첫 번째 장에 속하는지 확인
        for item in chapter_items:
            assert isinstance(item, dict), "각 항목은 딕셔너리여야 함"
            assert 'id' in item, "각 항목에 id가 있어야 함"
            assert 'title' in item, "각 항목에 title이 있어야 함"
        
        print(f"\n🔍 find_chapter_items 테스트 결과:")
        print(f"  - 첫 번째 장 ID: {first_chapter_id}")
        print(f"  - 두 번째 장 ID: {second_chapter_id}")
        print(f"  - 찾은 하위 항목 수: {len(chapter_items)}")
        print(f"  - 첫 번째 하위 항목: {chapter_items[0]['title'] if chapter_items else 'None'}")

    def test_save_chapter_content_to_folder_real_data(self, real_pdf_path, temp_directory):
        """
        요구사항: save_chapter_content_to_folder()가 장별 폴더를 생성하고 목차와 내용을 저장
        입력: 장 제목 (str), 장 항목들 (List[Dict]), 장 내용 (str), 출력 디렉터리 (Path), 로거
        출력: 장별 폴더에 저장된 TOC 및 내용 파일들
        """
        # Given: 실제 데이터 준비
        from services.toc_service import TocService
        from utils.config_manager import ConfigManager
        from utils.logger import LoggerFactory
        import logging
        
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)  
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        
        toc_service = TocService(config_manager, logger)
        toc_data = toc_service.extract_complete_toc(real_pdf_path)
        toc_structure = toc_data['toc_structure']
        
        # 첫 번째 장 데이터 준비
        root_items = [item for item in toc_structure if item['level'] == 0]
        first_chapter = root_items[0]
        chapter_title = first_chapter['title']
        
        # 간단한 테스트 항목들과 내용
        test_items = [first_chapter]
        test_content = "# 테스트 장 내용\n\n이것은 테스트 내용입니다."
        
        output_dir = Path(temp_directory) / "test_chapters"
        output_dir.mkdir(exist_ok=True)
        
        # When: 장별 폴더 생성 및 저장
        toc_filepath, content_filepath = save_chapter_content_to_folder(
            chapter_title, test_items, test_content, output_dir, logger
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
        
        print(f"\n💾 save_chapter_content_to_folder 테스트 결과:")
        print(f"  - 장 제목: {chapter_title}")
        print(f"  - 정규화된 폴더명: {normalize_title(chapter_title)}")
        print(f"  - 목차 파일: {toc_filepath}")
        print(f"  - 내용 파일: {content_filepath}")
        print(f"  - 저장된 항목 수: {len(saved_toc)}")