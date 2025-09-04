# 생성 시간: Thu Sep  4 08:17:51 KST 2025
# 핵심 내용: TocService의 Social Unit 테스트 (내부 의존성 포함, 실제 유틸리티 사용)
# 상세 내용:
#   - TestTocServiceSocial (라인 18-135): TocService의 사회적 단위 테스트 클래스
#   - test_extract_toc_structure_with_valid_pdf (라인 23-48): PDF 목차 추출 기본 동작 테스트
#   - test_process_toc_hierarchy_with_extracted_data (라인 50-78): 목차 계층 구조 처리 테스트
#   - test_calculate_toc_page_ranges_with_processed_data (라인 80-108): 페이지 범위 계산 테스트
#   - test_extract_complete_toc_full_workflow (라인 110-135): 완전한 목차 추출 워크플로우 테스트
# 상태: active
# 주소: tests/unit/social/test_toc_service_social
# 참조: 기존 toc_extractor 로직과 동일한 결과 검증

import pytest
import sys
from pathlib import Path

# TocService와 기존 유틸리티 import를 위한 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.toc_service import TocService
from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory

@pytest.mark.social_unit
class TestTocServiceSocial:
    """
    TocService의 Social Unit 테스트
    - 실제 ConfigManager, LoggerFactory 사용
    - 내부 의존성 포함한 협력 테스트
    - 기존 toc_extractor 로직과 동일한 동작 검증
    """
    
    def test_extract_toc_structure_with_valid_pdf(self, real_pdf_path, temp_directory):
        """
        요구사항: TocService.extract_toc_structure()가 PDF에서 기본 목차 구조 추출
        입력: PDF 파일 경로 (str)
        출력: 기본 목차 항목 리스트 (List[Dict]) - id, title, level, page, parent_id, children_ids 포함
        """
        # Given: TocService 인스턴스 생성 (실제 config_manager와 logger 사용)
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        toc_service = TocService(config_manager, logger)
        
        # When: PDF에서 목차 구조 추출
        raw_toc_items = toc_service.extract_toc_structure(real_pdf_path)
        
        # Then: 기본 목차 구조 검증
        assert isinstance(raw_toc_items, list), "목차 항목은 리스트여야 함"
        assert len(raw_toc_items) > 0, "실제 PDF에서 목차 항목이 추출되어야 함"
        
        # 기존 toc_extractor와 동일한 필드 구조 검증
        first_item = raw_toc_items[0]
        required_fields = ['id', 'title', 'level', 'page', 'parent_id', 'children_ids']
        for field in required_fields:
            assert field in first_item, f"목차 항목에 {field} 필드가 있어야 함"
        
        # 실제 데이터와 비교 검증 (218개 항목)
        assert len(raw_toc_items) == 218, "기존 로직과 동일한 수의 항목이 추출되어야 함"

    def test_process_toc_hierarchy_with_extracted_data(self, real_pdf_path, temp_directory):
        """
        요구사항: TocService.process_toc_hierarchy()가 부모-자식 관계 설정
        입력: 추출된 기본 목차 항목 리스트 (List[Dict])
        출력: 부모-자식 관계가 설정된 목차 항목 리스트 (List[Dict])
        """
        # Given: 추출된 기본 목차 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        toc_service = TocService(config_manager, logger)
        
        raw_toc_items = toc_service.extract_toc_structure(real_pdf_path)
        assert len(raw_toc_items) > 0, "전제조건: 목차 항목이 있어야 함"
        
        # When: 부모-자식 관계 처리
        processed_items = toc_service.process_toc_hierarchy(raw_toc_items)
        
        # Then: 처리 결과 검증
        assert isinstance(processed_items, list), "처리된 항목은 리스트여야 함"
        assert len(processed_items) == len(raw_toc_items), "항목 수는 동일해야 함"
        
        # 부모-자식 관계 논리 검증
        root_items = [item for item in processed_items if item['parent_id'] is None]
        assert len(root_items) == 18, "기존 로직과 동일한 수의 최상위 항목 (18개)"
        
        # 계층 구조 일관성 검증
        for item in processed_items:
            if item['parent_id'] is not None:
                parent_found = any(p['id'] == item['parent_id'] for p in processed_items)
                assert parent_found, f"항목 {item['id']}의 부모가 존재해야 함"

    def test_calculate_toc_page_ranges_with_processed_data(self, real_pdf_path, temp_directory):
        """
        요구사항: TocService.calculate_toc_page_ranges()가 페이지 범위 계산
        입력: 부모-자식 관계가 설정된 목차 항목 리스트 (List[Dict])
        출력: 페이지 범위가 계산된 완전한 목차 항목 리스트 (List[Dict])
        """
        # Given: 부모-자식 관계가 설정된 목차 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        toc_service = TocService(config_manager, logger)
        
        raw_toc_items = toc_service.extract_toc_structure(real_pdf_path)
        processed_items = toc_service.process_toc_hierarchy(raw_toc_items)
        assert len(processed_items) > 0, "전제조건: 처리된 목차 항목이 있어야 함"
        
        # When: 페이지 범위 계산
        complete_items = toc_service.calculate_toc_page_ranges(processed_items)
        
        # Then: 페이지 범위 검증
        assert isinstance(complete_items, list), "완성된 항목은 리스트여야 함"
        assert len(complete_items) == len(processed_items), "항목 수는 동일해야 함"
        
        # 페이지 범위 필드 존재 검증
        page_range_fields = ['start_page', 'end_page', 'page_count']
        for item in complete_items:
            for field in page_range_fields:
                assert field in item, f"완성된 항목에 {field} 필드가 있어야 함"
            
            # 페이지 범위 논리 검증
            assert item['start_page'] <= item['end_page'], "시작 페이지는 끝 페이지보다 작거나 같아야 함"
            assert item['page_count'] >= 1, "페이지 수는 최소 1이어야 함"

    def test_extract_complete_toc_full_workflow(self, real_pdf_path, temp_directory):
        """
        요구사항: TocService.extract_complete_toc()가 전체 워크플로우 실행
        입력: PDF 파일 경로 (str)
        출력: 완전한 목차 구조 데이터 (Dict) - extraction_info와 toc_structure 포함
        """
        # Given: TocService 인스턴스
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        logger = logger_factory.create_book_logger("test_book", temp_directory)
        toc_service = TocService(config_manager, logger)
        
        # When: 완전한 목차 추출 (전체 워크플로우)
        complete_toc_data = toc_service.extract_complete_toc(real_pdf_path)
        
        # Then: 완전한 목차 데이터 구조 검증
        assert isinstance(complete_toc_data, dict), "완전한 목차 데이터는 딕셔너리여야 함"
        assert 'extraction_info' in complete_toc_data, "extraction_info가 포함되어야 함"
        assert 'toc_structure' in complete_toc_data, "toc_structure가 포함되어야 함"
        
        # extraction_info 검증
        extraction_info = complete_toc_data['extraction_info']
        info_fields = ['source_pdf', 'extraction_method', 'extraction_timestamp', 'total_items', 'note']
        for field in info_fields:
            assert field in extraction_info, f"extraction_info에 {field} 필드가 있어야 함"
        
        # toc_structure 검증 (기존 로직과 동일한 결과)
        toc_structure = complete_toc_data['toc_structure']
        assert isinstance(toc_structure, list), "toc_structure는 리스트여야 함"
        assert len(toc_structure) == 218, "기존 로직과 동일한 수의 항목"
        assert extraction_info['total_items'] == 218, "extraction_info의 total_items 일치"
        
        # 레벨별 분포 검증 (기존 로직과 동일)
        level_counts = {}
        for item in toc_structure:
            level = item['level']
            level_counts[level] = level_counts.get(level, 0) + 1
        
        expected_level_distribution = {0: 18, 1: 56, 2: 127, 3: 17}
        assert level_counts == expected_level_distribution, "기존 로직과 동일한 레벨별 분포"
        
        print(f"\n📊 TocService 완전한 목차 추출 결과:")
        print(f"  - 총 항목 수: {len(toc_structure)}")
        print(f"  - 레벨별 분포: {dict(sorted(level_counts.items()))}")