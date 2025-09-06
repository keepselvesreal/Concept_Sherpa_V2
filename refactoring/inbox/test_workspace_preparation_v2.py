# 생성 시간: Thu Sep  4 17:44:08 KST 2025
# 구현 파일명: /home/nadle/projects/Knowledge_Sherpa/v2/refactoring/src/stages/workspace_preparation_v2.py
# 테스트 유형: social unit + integration (서비스 의존성 포함)
# 핵심 내용: WorkspacePreparationStage_v2의 모든 메서드 테스트 (기능 검증 및 회귀 방지)
# 상세 내용:
#   - TestWorkspacePreparationStageInit (라인 28-65): 초기화 테스트 그룹
#   - TestWorkspacePreparationProcess (라인 67-145): 메인 process 메서드 테스트 그룹  
#   - TestWorkspacePreparationTocExtraction (라인 147-178): PDF 목차 추출 테스트 그룹
#   - TestWorkspacePreparationLoggerSetup (라인 180-220): 로거 설정 테스트 그룹
#   - TestWorkspacePreparationDirectories (라인 222-255): 디렉토리 생성 테스트 그룹
#   - TestWorkspacePreparationTocSave (라인 257-285): 목차 저장 테스트 그룹
#   - TestWorkspacePreparationAiAnalysis (라인 287-320): AI 분석 테스트 그룹
#   - TestWorkspacePreparationChapterFolders (라인 322-410): 장별 폴더 생성 테스트 그룹
# 상태: active

import pytest
import asyncio
import json
import os
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from stages.workspace_preparation_v2 import WorkspacePreparationStage
from utils.logger_v2 import Logger

class TestWorkspacePreparationStageInit:
    """
    WorkspacePreparationStage 초기화 테스트
    
    요구사항:
    - config_manager와 logger_factory를 받아 정상 초기화
    - 모든 서비스 인스턴스는 None으로 시작
    - stage_name은 "workspace_preparation"으로 설정
    
    테스트 메서드 입출력:
    - test_init_success: Mock 객체들 → 정상 초기화된 인스턴스
    - test_init_attributes_default: Mock 객체들 → 기본값들 검증
    """
    
    def test_init_success(self):
        """정상 초기화 테스트"""
        # Given
        mock_config = Mock()
        mock_logger_factory = Mock()
        
        # When
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        
        # Then
        assert stage.config_manager == mock_config
        assert stage.logger_factory == mock_logger_factory
        assert stage.stage_name == "workspace_preparation"
        
    def test_init_attributes_default(self):
        """초기화 후 속성들이 기본값인지 검증"""
        # Given
        mock_config = Mock()
        mock_logger_factory = Mock()
        
        # When
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        
        # Then
        assert stage.ai_service is None
        assert stage.toc_service is None  
        assert stage.chapter_extraction_service is None
        assert stage.book_title is None
        assert stage.normalized_book_title is None

class TestWorkspacePreparationProcess:
    """
    WorkspacePreparationStage.process 메인 처리 로직 테스트
    
    요구사항:
    - PDF 경로 검증 → 목차 추출 → 로거 설정 → 디렉토리 생성 → 목차 저장 → AI 분석 → 장 폴더 생성 순차 진행
    - 각 단계 실패 시 적절한 에러 처리
    - 성공 시 완전한 결과 정보 반환
    
    테스트 메서드 입출력:
    - test_process_invalid_pdf_path: 잘못된 경로 → 에러 결과
    - test_process_toc_extraction_failure: 목차 추출 실패 → 에러 결과  
    - test_process_ai_analysis_failure: AI 분석 실패 → 에러 결과
    - test_process_success: 유효한 입력 → 성공 결과 딕셔너리
    """
    
    @pytest.fixture
    def stage_with_mocks(self):
        """모의 의존성이 설정된 스테이지 픽스처"""
        mock_config = Mock()
        mock_logger_factory = Mock()
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        
        # 내부 서비스들 모킹
        stage.toc_service = Mock()
        stage.logger = Mock()
        stage.ai_service = Mock()
        stage.chapter_extraction_service = Mock()
        
        return stage
    
    @pytest.mark.asyncio
    async def test_process_invalid_pdf_path(self, stage_with_mocks):
        """잘못된 PDF 경로 입력 시 에러 처리 테스트"""
        # Given
        invalid_input = {'pdf_path': '/nonexistent/file.pdf'}
        
        # When
        result = await stage_with_mocks.process(invalid_input)
        
        # Then
        assert result['success'] is False
        assert '유효하지 않은 PDF 경로' in result['error']
        
    @pytest.mark.asyncio  
    async def test_process_toc_extraction_failure(self, stage_with_mocks, temp_directory):
        """목차 추출 실패 시 에러 처리 테스트"""
        # Given
        pdf_path = Path(temp_directory) / "test.pdf"
        pdf_path.write_text("dummy pdf content")
        input_data = {'pdf_path': str(pdf_path)}
        
        # 목차 추출 실패 시뮬레이션
        stage_with_mocks.extract_toc_from_pdf = AsyncMock(return_value={'success': False, 'error': 'TOC extraction failed'})
        
        # When
        result = await stage_with_mocks.process(input_data)
        
        # Then
        assert result['success'] is False
        assert 'TOC extraction failed' in result['error']
    
    @pytest.mark.asyncio
    async def test_process_success(self, stage_with_mocks, temp_directory):
        """정상 처리 플로우 테스트"""
        # Given
        pdf_path = Path(temp_directory) / "test.pdf"
        pdf_path.write_text("dummy pdf content")
        input_data = {'pdf_path': str(pdf_path)}
        
        # 각 단계별 성공 응답 모킹
        stage_with_mocks.extract_toc_from_pdf = AsyncMock(return_value={
            'success': True,
            'data': {'toc_structure': [{'title': 'Test Book'}]}
        })
        stage_with_mocks.setup_book_logger = AsyncMock(return_value=Mock())
        stage_with_mocks.create_output_directories = AsyncMock(return_value={
            'book_dir': Path(temp_directory) / 'test_book'
        })
        stage_with_mocks.save_toc_file = AsyncMock(return_value=Path(temp_directory) / 'toc.json')
        stage_with_mocks.analyze_chapters_with_ai = AsyncMock(return_value={
            'success': True, 
            'chapters_info': [{'title': 'Chapter 1'}]
        })
        stage_with_mocks.create_chapter_folders = AsyncMock(return_value=[
            {'chapter_number': 1, 'chapter_title': 'Chapter 1'}
        ])
        
        # When
        result = await stage_with_mocks.process(input_data)
        
        # Then
        assert result['success'] is True
        assert 'book_title' in result
        assert 'total_chapters' in result
        assert 'created_folders' in result

class TestWorkspacePreparationTocExtraction:
    """
    WorkspacePreparationStage.extract_toc_from_pdf 테스트
    
    요구사항:
    - TocService.extract_complete_toc 메서드 호출
    - 성공 시 {'success': True, 'data': toc_data} 형식 반환
    - 실패 시 {'success': False, 'error': str} 형식 반환
    
    테스트 메서드 입출력:
    - test_extract_toc_success: PDF 경로 → 성공 결과 딕셔너리
    - test_extract_toc_failure: PDF 경로 → 에러 결과 딕셔너리
    """
    
    @pytest.fixture
    def stage_with_toc_service(self):
        """TocService가 모킹된 스테이지 픽스처"""
        mock_config = Mock()
        mock_logger_factory = Mock()
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        stage.toc_service = Mock()
        return stage
    
    @pytest.mark.asyncio
    async def test_extract_toc_success(self, stage_with_toc_service):
        """목차 추출 성공 테스트"""
        # Given
        pdf_path = "/test/path.pdf"
        expected_toc_data = {'toc_structure': [{'title': 'Chapter 1'}]}
        stage_with_toc_service.toc_service.extract_complete_toc.return_value = expected_toc_data
        
        # When
        result = await stage_with_toc_service.extract_toc_from_pdf(pdf_path)
        
        # Then
        assert result['success'] is True
        assert result['data'] == expected_toc_data
        stage_with_toc_service.toc_service.extract_complete_toc.assert_called_once_with(pdf_path)
    
    @pytest.mark.asyncio
    async def test_extract_toc_failure(self, stage_with_toc_service):
        """목차 추출 실패 테스트"""
        # Given
        pdf_path = "/test/path.pdf"
        stage_with_toc_service.toc_service.extract_complete_toc.side_effect = Exception("TOC extraction error")
        
        # When
        result = await stage_with_toc_service.extract_toc_from_pdf(pdf_path)
        
        # Then  
        assert result['success'] is False
        assert "TOC extraction error" in result['error']

class TestWorkspacePreparationLoggerSetup:
    """
    WorkspacePreparationStage.setup_book_logger 테스트
    
    요구사항:
    - 책 제목으로부터 정규화된 제목 생성
    - Logger 인스턴스 생성 및 설정  
    - AI, TOC, ChapterExtraction 서비스들 초기화
    - 설정된 Logger 인스턴스 반환
    
    테스트 메서드 입출력:
    - test_setup_logger_success: 책 제목 → Logger 인스턴스
    - test_setup_logger_normalizes_title: 특수문자 책 제목 → 정규화된 제목 설정
    """
    
    @pytest.fixture  
    def stage_for_logger_setup(self):
        """로거 설정 테스트용 스테이지 픽스처"""
        mock_config = Mock()
        mock_config.get.return_value = "./test_logs"
        mock_logger_factory = Mock()
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        return stage
    
    @pytest.mark.asyncio
    @patch('stages.workspace_preparation_v2.Logger')
    @patch('stages.workspace_preparation_v2.AIService')
    @patch('stages.workspace_preparation_v2.TocService')
    @patch('stages.workspace_preparation_v2.ChapterExtractionService')
    async def test_setup_logger_success(self, mock_chapter_service, mock_toc_service, 
                                       mock_ai_service, mock_logger, stage_for_logger_setup):
        """로거 설정 성공 테스트"""
        # Given
        book_title = "Test Book Title"
        mock_logger_instance = Mock()
        mock_logger.return_value = mock_logger_instance
        
        # When
        result = await stage_for_logger_setup.setup_book_logger(book_title)
        
        # Then
        assert result == mock_logger_instance
        assert stage_for_logger_setup.normalized_book_title == "Test_Book_Title"
        mock_logger.assert_called_once()
        mock_ai_service.assert_called_once()
        mock_toc_service.assert_called_once()
        mock_chapter_service.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_setup_logger_normalizes_title(self, stage_for_logger_setup):
        """특수문자가 포함된 책 제목의 정규화 테스트"""
        # Given  
        book_title = "Test Book: Special Characters & More!"
        
        with patch('stages.workspace_preparation_v2.Logger'), \
             patch('stages.workspace_preparation_v2.AIService'), \
             patch('stages.workspace_preparation_v2.TocService'), \
             patch('stages.workspace_preparation_v2.ChapterExtractionService'):
            
            # When
            await stage_for_logger_setup.setup_book_logger(book_title)
            
            # Then
            assert stage_for_logger_setup.normalized_book_title == "Test_Book_Special_Characters_More"

class TestWorkspacePreparationDirectories:
    """
    WorkspacePreparationStage.create_output_directories 테스트
    
    요구사항:
    - config에서 base_path 읽어와서 출력 디렉터리 생성
    - normalized_book_title로 책별 디렉터리 생성
    - 생성된 디렉터리 경로들 반환
    
    테스트 메서드 입출력:
    - test_create_directories_success: 정규화된 책 제목 → 생성된 디렉터리 정보 딕셔너리
    - test_create_directories_uses_config_path: 설정된 경로 → 해당 경로에 디렉터리 생성
    """
    
    @pytest.fixture
    def stage_with_normalized_title(self, temp_directory):
        """정규화된 제목이 설정된 스테이지 픽스처"""
        mock_config = Mock()
        mock_config.get.return_value = temp_directory
        mock_logger_factory = Mock()
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        stage.normalized_book_title = "Test_Book"
        stage.log_step = Mock()  # 로깅 메서드 모킹
        return stage
        
    @pytest.mark.asyncio
    async def test_create_directories_success(self, stage_with_normalized_title, temp_directory):
        """디렉터리 생성 성공 테스트"""
        # When
        result = await stage_with_normalized_title.create_output_directories()
        
        # Then
        assert 'output_dir' in result
        assert 'book_dir' in result
        assert result['output_dir'] == Path(temp_directory)
        assert result['book_dir'] == Path(temp_directory) / "Test_Book"
        assert result['book_dir'].exists()
    
    @pytest.mark.asyncio  
    async def test_create_directories_uses_config_path(self, stage_with_normalized_title, temp_directory):
        """설정 경로 사용 테스트"""
        # Given - 실제 존재하는 경로 사용
        expected_base_path = temp_directory
        stage_with_normalized_title.config_manager.get.return_value = expected_base_path
        
        # When
        result = await stage_with_normalized_title.create_output_directories()
        
        # Then
        stage_with_normalized_title.config_manager.get.assert_called_with(
            "workspace_preparation.folder_structure.base_path", "./output"
        )
        assert str(result['output_dir']) == expected_base_path

class TestWorkspacePreparationTocSave:
    """
    WorkspacePreparationStage.save_toc_file 테스트
    
    요구사항:  
    - 목차 데이터를 JSON 형식으로 지정된 디렉터리에 저장
    - 저장된 파일 경로 반환
    - UTF-8 인코딩으로 저장
    
    테스트 메서드 입출력:
    - test_save_toc_file_success: 목차 데이터, 디렉터리 경로 → 저장된 파일 경로
    - test_save_toc_file_creates_json: 목차 데이터, 디렉터리 경로 → JSON 파일 생성 및 내용 검증
    """
    
    @pytest.fixture
    def stage_with_logger(self):
        """로거가 설정된 스테이지 픽스처"""
        mock_config = Mock()
        mock_logger_factory = Mock()
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        stage.log_step = Mock()
        return stage
    
    @pytest.mark.asyncio
    async def test_save_toc_file_success(self, stage_with_logger, temp_directory):
        """목차 파일 저장 성공 테스트"""
        # Given
        toc_data = {'toc_structure': [{'title': 'Chapter 1', 'page': 10}]}
        book_dir = Path(temp_directory)
        
        # When
        result = await stage_with_logger.save_toc_file(toc_data, book_dir)
        
        # Then
        assert result == book_dir / "toc.json"
        assert result.exists()
    
    @pytest.mark.asyncio
    async def test_save_toc_file_creates_json(self, stage_with_logger, temp_directory):
        """JSON 파일 생성 및 내용 검증 테스트"""
        # Given
        toc_data = {'toc_structure': [{'title': 'Test Chapter', 'page': 5}]}
        book_dir = Path(temp_directory)
        
        # When  
        result = await stage_with_logger.save_toc_file(toc_data, book_dir)
        
        # Then
        with open(result, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        assert saved_data == toc_data

class TestWorkspacePreparationAiAnalysis:
    """
    WorkspacePreparationStage.analyze_chapters_with_ai 테스트
    
    요구사항:
    - ChapterExtractionService를 통한 AI 제공자 생성
    - AI 기반 장 개수 분석 수행
    - 성공 시 분석 결과 반환, 실패 시 에러 정보 반환
    
    테스트 메서드 입출력:  
    - test_ai_analysis_success: TOC 파일 경로 → 성공 분석 결과
    - test_ai_analysis_failure: TOC 파일 경로 → 에러 결과
    """
    
    @pytest.fixture
    def stage_with_chapter_service(self):
        """ChapterExtractionService가 모킹된 스테이지 픽스처"""
        mock_config = Mock()
        mock_logger_factory = Mock() 
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        stage.chapter_extraction_service = Mock()
        stage.log_step = Mock()
        return stage
        
    @pytest.mark.asyncio
    async def test_ai_analysis_success(self, stage_with_chapter_service):
        """AI 분석 성공 테스트"""
        # Given
        toc_filepath = "/test/toc.json"
        mock_ai_provider = Mock()
        expected_result = {
            'success': True,
            'chapters_info': [{'title': 'Chapter 1'}, {'title': 'Chapter 2'}]
        }
        
        stage_with_chapter_service.chapter_extraction_service.create_ai_provider.return_value = mock_ai_provider
        # AsyncMock으로 변경
        stage_with_chapter_service.chapter_extraction_service.count_chapters_with_ai = AsyncMock(return_value=expected_result)
        
        # When
        result = await stage_with_chapter_service.analyze_chapters_with_ai(toc_filepath)
        
        # Then
        assert result == expected_result
        stage_with_chapter_service.chapter_extraction_service.create_ai_provider.assert_called_once_with("gemini")
        stage_with_chapter_service.chapter_extraction_service.count_chapters_with_ai.assert_called_once_with(toc_filepath, mock_ai_provider)
    
    @pytest.mark.asyncio
    async def test_ai_analysis_failure(self, stage_with_chapter_service):
        """AI 분석 실패 테스트"""
        # Given
        toc_filepath = "/test/toc.json"
        stage_with_chapter_service.chapter_extraction_service.create_ai_provider.side_effect = Exception("AI service error")
        
        # When
        result = await stage_with_chapter_service.analyze_chapters_with_ai(toc_filepath)
        
        # Then
        assert result['success'] is False
        assert "AI service error" in result['error']

class TestWorkspacePreparationChapterFolders:
    """
    WorkspacePreparationStage.create_chapter_folders 테스트
    
    요구사항:
    - 각 장에 대해 목차 구조에서 해당 장 정보 찾기
    - ChapterExtractionService를 통한 장 폴더 및 파일 생성
    - 테스트 모드에서 선택된 장만 처리
    - 생성된 폴더 정보 리스트 반환
    
    테스트 메서드 입출력:
    - test_create_chapter_folders_success: 장 정보, 목차 구조, 디렉터리, PDF 경로 → 생성된 폴더 정보 리스트
    - test_create_chapter_folders_test_mode: 테스트 설정, 장 정보 → 선택된 장만 처리
    - test_create_chapter_folders_missing_chapter: 목차에 없는 장 → 경고 로그 및 건너뛰기
    - test_create_chapter_folders_with_error: 장 처리 오류 → 에러 로그 및 계속 진행
    """
    
    @pytest.fixture
    def stage_with_services_and_config(self, temp_directory):
        """모든 서비스가 설정된 스테이지 픽스처"""
        mock_config = Mock()
        mock_config.get_test_config.return_value = {"enabled": False}
        mock_config.is_chapter_selected.return_value = True
        mock_logger_factory = Mock()
        
        stage = WorkspacePreparationStage(mock_config, mock_logger_factory)
        stage.chapter_extraction_service = Mock()
        stage.log_step = Mock()
        
        # ChapterExtractionService 메서드들 모킹
        stage.chapter_extraction_service.find_chapter_items.return_value = [{'title': 'Section 1'}]
        stage.chapter_extraction_service.extract_pdf_content.return_value = "Test content"
        stage.chapter_extraction_service.save_chapter_content_to_folder.return_value = (
            Path(temp_directory) / "toc.json",
            Path(temp_directory) / "content.md"
        )
        
        return stage
    
    @pytest.mark.asyncio
    async def test_create_chapter_folders_success(self, stage_with_services_and_config, temp_directory):
        """장 폴더 생성 성공 테스트"""
        # Given  
        chapters_info = [
            {'title': 'Chapter 1', 'start_page': 1, 'end_page': 10}
        ]
        toc_structure = [
            {'id': 'ch1', 'title': 'Chapter 1'}
        ]
        book_dir = Path(temp_directory)
        pdf_path = "/test/book.pdf"
        
        # When  
        with patch('utils.text_utils.normalize_title', return_value='Chapter_1'):
            result = await stage_with_services_and_config.create_chapter_folders(
                chapters_info, toc_structure, book_dir, pdf_path
            )
        
        # Then
        assert len(result) == 1
        assert result[0]['chapter_number'] == 1
        assert result[0]['chapter_title'] == 'Chapter 1'
        assert result[0]['normalized_title'] == 'Chapter_1'
        
    @pytest.mark.asyncio
    async def test_create_chapter_folders_test_mode(self, stage_with_services_and_config, temp_directory):
        """테스트 모드에서 선택된 장만 처리하는 테스트"""
        # Given - 테스트 모드 설정 및 장 2번만 선택
        stage_with_services_and_config.config_manager.get_test_config.return_value = {"enabled": True}
        stage_with_services_and_config.config_manager.is_chapter_selected.side_effect = lambda x: x == 2
        
        chapters_info = [
            {'title': 'Chapter 1', 'start_page': 1, 'end_page': 10},
            {'title': 'Chapter 2', 'start_page': 11, 'end_page': 20}
        ]
        toc_structure = [
            {'id': 'ch1', 'title': 'Chapter 1'},
            {'id': 'ch2', 'title': 'Chapter 2'}
        ]
        
        # When
        with patch('utils.text_utils.normalize_title', side_effect=['Chapter_1', 'Chapter_2']):
            result = await stage_with_services_and_config.create_chapter_folders(
                chapters_info, toc_structure, Path(temp_directory), "/test/book.pdf"
            )
        
        # Then - 장 2번만 처리됨
        assert len(result) == 1
        assert result[0]['chapter_number'] == 2
        assert result[0]['chapter_title'] == 'Chapter 2'
    
    @pytest.mark.asyncio
    async def test_create_chapter_folders_missing_chapter(self, stage_with_services_and_config, temp_directory):
        """목차에서 장을 찾을 수 없는 경우 테스트"""
        # Given - 목차에 없는 장 정보
        chapters_info = [{'title': 'Missing Chapter', 'start_page': 1, 'end_page': 10}]
        toc_structure = [{'id': 'ch1', 'title': 'Different Chapter'}]
        
        # When
        result = await stage_with_services_and_config.create_chapter_folders(
            chapters_info, toc_structure, Path(temp_directory), "/test/book.pdf"
        )
        
        # Then
        assert len(result) == 0  # 처리된 장이 없음
        stage_with_services_and_config.log_step.assert_any_call(
            "⚠️ 목차에서 해당 장을 찾을 수 없음: Missing Chapter", "warning"
        )
    
    @pytest.mark.asyncio 
    async def test_create_chapter_folders_with_error(self, stage_with_services_and_config, temp_directory):
        """장 처리 중 오류 발생 시 테스트"""
        # Given
        chapters_info = [{'title': 'Chapter 1', 'start_page': 1, 'end_page': 10}]
        toc_structure = [{'id': 'ch1', 'title': 'Chapter 1'}]
        
        # ChapterExtractionService에서 오류 발생 시뮬레이션
        stage_with_services_and_config.chapter_extraction_service.find_chapter_items.side_effect = Exception("Processing error")
        
        # When
        result = await stage_with_services_and_config.create_chapter_folders(
            chapters_info, toc_structure, Path(temp_directory), "/test/book.pdf"
        )
        
        # Then
        assert len(result) == 0  # 에러로 인해 처리된 장이 없음
        stage_with_services_and_config.log_step.assert_any_call(
            "❌ 장 1 처리 중 오류: Processing error", "error"
        )