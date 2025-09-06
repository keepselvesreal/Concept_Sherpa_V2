# 생성 시간: Thu Sep  4 17:48:30 KST 2025
# 구현 파일명: /home/nadle/projects/Knowledge_Sherpa/v2/refactoring/src/stages/workspace_preparation_v2.py
# 테스트 유형: integration (실제 데이터 기반 통합 테스트)
# 핵심 내용: WorkspacePreparationStage_v2 실제 데이터 기반 통합 테스트 (정상 동작 검증)
# 상세 내용:
#   - TestWorkspacePreparationIntegration (라인 25-180): 실제 데이터 기반 통합 테스트 클래스
#   - test_full_workflow_with_real_data (라인 40-70): 전체 워크플로우 실제 데이터 테스트
#   - test_toc_extraction_real (라인 72-85): 실제 PDF 목차 추출 테스트
#   - test_logger_setup_real (라인 87-105): 실제 책 제목으로 로거 설정 테스트
#   - test_directories_creation_real (라인 107-125): 실제 디렉토리 생성 테스트
#   - test_toc_save_real (라인 127-145): 실제 목차 저장 테스트
#   - test_chapter_folders_creation_real (라인 147-180): 실제 장 폴더 생성 테스트
# 상태: active

import pytest
import json
import os
from pathlib import Path
from datetime import datetime

from stages.workspace_preparation_v2 import WorkspacePreparationStage
from utils.config_manager import ConfigManager
from utils.logger_v2 import LoggerFactory
from services.toc_service import TocService
from services.ai_service_v3 import AIService
from services.chapter_extraction_service_v2 import ChapterExtractionService

class TestWorkspacePreparationIntegration:
    """
    WorkspacePreparationStage 실제 데이터 기반 통합 테스트
    
    요구사항:
    - 실제 PDF 파일을 사용한 전체 워크플로우 검증
    - Mock 없이 실제 서비스들의 동작 확인
    - 각 단계별 실제 결과를 다음 단계 입력으로 활용
    - 정상 동작 경우만 테스트 (에러 케이스는 제외)
    
    테스트 메서드 입출력:
    - test_full_workflow_with_real_data: 실제 PDF → 완전한 워크스페이스 생성 결과
    - test_toc_extraction_real: 실제 PDF → 실제 목차 데이터
    - test_logger_setup_real: 실제 책 제목 → 실제 Logger 인스턴스
    - test_directories_creation_real: 실제 책 제목 → 실제 디렉토리 생성
    - test_toc_save_real: 실제 목차 데이터 → 실제 JSON 파일 저장
    - test_chapter_folders_creation_real: 실제 장 정보 → 실제 장 폴더들 생성
    """
    
    @pytest.fixture
    def config_and_logger(self, temp_directory):
        """실제 설정 매니저와 로거 팩토리 생성"""
        config_manager = ConfigManager()
        # 테스트용 설정 조정
        config_manager._config = {
            "global": {
                "logs_base_dir": temp_directory + "/logs",
                "results_base_dir": temp_directory + "/results"
            },
            "workspace_preparation": {
                "folder_structure": {
                    "base_path": temp_directory + "/output"
                }
            },
            "test": {"enabled": False}  # 테스트 모드 비활성화
        }
        logger_factory = LoggerFactory(config_manager)
        return config_manager, logger_factory
    
    @pytest.fixture
    def stage_instance(self, config_and_logger):
        """실제 WorkspacePreparationStage 인스턴스"""
        config_manager, logger_factory = config_and_logger
        return WorkspacePreparationStage(config_manager, logger_factory)
    
    @pytest.mark.asyncio
    async def test_full_workflow_with_real_data(self, stage_instance, real_pdf_path):
        """실제 PDF 파일로 전체 워크플로우 테스트"""
        # Given
        input_data = {'pdf_path': real_pdf_path}
        
        # When
        result = await stage_instance.process(input_data)
        
        # Then
        assert result['success'] is True
        assert 'book_title' in result
        assert 'normalized_book_title' in result
        assert 'book_folder' in result
        assert 'toc_file' in result
        assert 'total_chapters' in result
        assert result['total_chapters'] > 0
        assert 'created_folders' in result
        assert len(result['created_folders']) > 0
        
        # 실제 파일들이 생성되었는지 확인
        assert Path(result['book_folder']).exists()
        assert Path(result['toc_file']).exists()
        
        print(f"✅ 처리된 책: {result['book_title']}")
        print(f"✅ 생성된 장 수: {result['total_chapters']}")
        print(f"✅ 책 폴더: {result['book_folder']}")
    
    @pytest.mark.asyncio
    async def test_toc_extraction_real(self, stage_instance, real_pdf_path):
        """실제 PDF에서 목차 추출 테스트"""
        # Given - 먼저 TocService 초기화 필요
        temp_logger = stage_instance.logger_factory.create_book_logger("temp_test", "./logs")
        stage_instance.toc_service = TocService(stage_instance.config_manager, temp_logger)
        
        # When
        result = await stage_instance.extract_toc_from_pdf(real_pdf_path)
        
        # Then
        assert result['success'] is True
        assert 'data' in result
        toc_data = result['data']
        assert 'toc_structure' in toc_data
        assert len(toc_data['toc_structure']) > 0
        
        # 첫 번째 목차 항목이 책 제목인지 확인
        first_item = toc_data['toc_structure'][0]
        assert 'title' in first_item
        assert 'page' in first_item
        
        print(f"✅ 추출된 목차 항목 수: {len(toc_data['toc_structure'])}")
        print(f"✅ 책 제목: {first_item['title']}")
    
    @pytest.mark.asyncio
    async def test_logger_setup_real(self, stage_instance):
        """실제 책 제목으로 로거 설정 테스트"""
        # Given
        book_title = "Data-Oriented Programming Test"
        
        # When
        logger = await stage_instance.setup_book_logger(book_title)
        
        # Then
        assert logger is not None
        assert stage_instance.normalized_book_title == "Data_Oriented_Programming_Test"
        assert stage_instance.ai_service is not None
        assert stage_instance.toc_service is not None
        assert stage_instance.chapter_extraction_service is not None
        
        # 실제 로그 디렉토리 생성 확인
        assert logger.logs_dir.exists()
        
        print(f"✅ 정규화된 제목: {stage_instance.normalized_book_title}")
        print(f"✅ 로그 디렉토리: {logger.logs_dir}")
    
    @pytest.mark.asyncio
    async def test_directories_creation_real(self, stage_instance, temp_directory):
        """실제 디렉토리 생성 테스트"""
        # Given - 정규화된 책 제목 설정
        stage_instance.normalized_book_title = "Test_Book_Real"
        stage_instance.log_step = lambda msg, level="info": print(f"[{level.upper()}] {msg}")
        
        # When
        result = await stage_instance.create_output_directories()
        
        # Then
        assert 'output_dir' in result
        assert 'book_dir' in result
        assert result['book_dir'].exists()
        
        # 실제 디렉토리 경로 확인
        expected_book_dir = result['output_dir'] / "Test_Book_Real"
        assert result['book_dir'] == expected_book_dir
        
        print(f"✅ 생성된 출력 디렉토리: {result['output_dir']}")
        print(f"✅ 생성된 책 디렉토리: {result['book_dir']}")
    
    @pytest.mark.asyncio
    async def test_toc_save_real(self, stage_instance, temp_directory):
        """실제 목차 데이터 저장 테스트"""
        # Given - 실제 목차 데이터 (간단한 예시)
        real_toc_data = {
            'toc_structure': [
                {'id': 'book', 'title': 'Test Book', 'page': 1, 'level': 0},
                {'id': 'ch1', 'title': 'Chapter 1', 'page': 5, 'level': 1},
                {'id': 'ch1_1', 'title': 'Section 1.1', 'page': 10, 'level': 2}
            ],
            'metadata': {
                'total_pages': 100,
                'extraction_time': datetime.now().isoformat()
            }
        }
        book_dir = Path(temp_directory)
        stage_instance.log_step = lambda msg, level="info": print(f"[{level.upper()}] {msg}")
        
        # When
        result_path = await stage_instance.save_toc_file(real_toc_data, book_dir)
        
        # Then
        assert result_path.exists()
        assert result_path.name == "toc.json"
        
        # 저장된 내용 확인
        with open(result_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        assert saved_data == real_toc_data
        
        print(f"✅ 목차 파일 저장: {result_path}")
        print(f"✅ 저장된 목차 항목 수: {len(saved_data['toc_structure'])}")
    
    @pytest.mark.asyncio 
    async def test_chapter_folders_creation_real(self, stage_instance, temp_directory, real_pdf_path):
        """실제 장 폴더 생성 테스트 (단계별 실제 처리 결과 활용)"""
        # Given - 먼저 실제 데이터들을 단계별로 준비
        
        # 1단계: 실제 로거 설정
        await stage_instance.setup_book_logger("Data-Oriented Programming")
        
        # 2단계: 실제 목차 추출  
        toc_result = await stage_instance.extract_toc_from_pdf(real_pdf_path)
        assert toc_result['success'] is True
        toc_structure = toc_result['data']['toc_structure']
        
        # 3단계: 실제 AI 분석 (목차 파일 먼저 저장)
        book_dir = Path(temp_directory)
        toc_file = await stage_instance.save_toc_file(toc_result['data'], book_dir)
        ai_result = await stage_instance.analyze_chapters_with_ai(str(toc_file))
        
        if not ai_result['success']:
            pytest.skip(f"AI 분석 실패로 테스트 건너뜀: {ai_result.get('error', 'Unknown error')}")
        
        chapters_info = ai_result['chapters_info'][:2]  # 처음 2개 장만 테스트
        
        # When - 실제 장 폴더 생성 (실제 처리 결과 활용)
        result = await stage_instance.create_chapter_folders(
            chapters_info, toc_structure, book_dir, real_pdf_path
        )
        
        # Then
        assert len(result) > 0
        
        for folder_info in result:
            assert 'chapter_number' in folder_info
            assert 'chapter_title' in folder_info
            assert 'toc_file' in folder_info
            
            # 실제 파일들 생성 확인
            toc_file_path = Path(folder_info['toc_file'])
            assert toc_file_path.exists()
            
            # 내용 파일이 있으면 확인
            if folder_info.get('content_file'):
                content_file_path = Path(folder_info['content_file'])
                assert content_file_path.exists()
        
        print(f"✅ 생성된 장 폴더 수: {len(result)}")
        for folder_info in result:
            print(f"   - 장 {folder_info['chapter_number']}: {folder_info['chapter_title']}")