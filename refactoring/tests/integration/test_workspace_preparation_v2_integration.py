# 생성 시간: Fri Sep  5 11:48:04 KST 2025
# 핵심 내용: WorkspacePreparationStage v2 전체 프로세스 integration 테스트
# 상세 내용:
#   - TestWorkspacePreparationV2Integration (라인 23-): integration 테스트 클래스
#   - test_full_workspace_preparation_process (라인 35-): 전체 워크스페이스 준비 프로세스 테스트 및 출력 저장
# 상태: active
# 참조: workspace_preparation_v2.py

import os
import json
import pytest
import asyncio
import shutil
from pathlib import Path
from datetime import datetime

# 시스템 경로 설정
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from utils.config_manager import ConfigManager
from utils.logger_v2 import Logger
from stages.workspace_preparation_v2 import WorkspacePreparationStage

# 구현 파일명: test_workspace_preparation_v2_integration.py
# 테스트 유형: integration test
class TestWorkspacePreparationV2Integration:
    """
    WorkspacePreparationStage v2 전체 프로세스 integration 테스트
    
    요구사항:
    1. 실제 PDF 파일을 사용한 전체 워크스페이스 준비 프로세스 테스트
    2. 장별 폴더와 내용을 data 폴더에 저장
    3. 최종 출력 결과를 data 폴더에 저장
    """
    
    @pytest.fixture
    def test_config_manager(self):
        """실제 설정을 사용하는 ConfigManager"""
        config_dir = Path(__file__).parent.parent.parent / "config"
        return ConfigManager(str(config_dir))
    
    @pytest.fixture
    def test_logger_factory(self):
        """실제 Logger를 생성하는 팩토리 함수"""
        class LoggerFactory:
            def create_logger(self, name):
                return Logger(name)
        return LoggerFactory()
    
    @pytest.fixture
    def test_output_dir(self):
        """테스트 출력 디렉토리 설정"""
        output_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data")
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    @pytest.fixture
    def workspace_stage(self, test_config_manager, test_logger_factory):
        """WorkspacePreparationStage 인스턴스"""
        return WorkspacePreparationStage(test_config_manager, test_logger_factory)
    
    @pytest.mark.asyncio
    async def test_full_workspace_preparation_process(self, workspace_stage, real_pdf_path, test_output_dir):
        """
        전체 워크스페이스 준비 프로세스 테스트
        
        요구사항:
        - 실제 PDF 파일을 사용한 전체 프로세스 테스트
        - 장별 폴더와 내용을 data 폴더에 저장
        - 최종 출력 결과를 data 폴더에 저장
        """
        print("🚀 전체 워크스페이스 준비 프로세스 테스트 시작")
        
        # Given: 실제 PDF 파일 경로 및 기존 결과 정리
        input_data = {'pdf_path': real_pdf_path}
        
        # 기존 결과 정리
        if test_output_dir.exists():
            for item in test_output_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        
        # ConfigManager에서 출력 경로를 테스트 디렉토리로 설정
        workspace_stage.config_manager.pipeline_config['workspace_preparation'] = {
            'folder_structure': {
                'base_path': str(test_output_dir)
            }
        }
        
        # When: 워크스페이스 준비 프로세스 실행
        print("📖 PDF 프로세싱 시작...")
        result = await workspace_stage.process(input_data)
        
        # Then: 전체 프로세스 성공 검증
        assert result['success'] is True, "워크스페이스 준비 프로세스가 실패했습니다"
        assert 'normalized_book_title' in result
        assert 'total_chapters' in result
        assert 'output_directory' in result
        assert 'created_folders' in result
        
        # 출력 디렉토리 검증
        output_path = Path(result['output_directory'])
        assert output_path.parent == test_output_dir
        assert output_path.exists()
        
        # 장 개수 검증
        assert result['total_chapters'] > 0
        assert len(result['created_folders']) > 0
        
        print(f"✅ 성공: {result['total_chapters']}개 장 처리 완료")
        print(f"✅ 출력 디렉토리: {result['output_directory']}")
        
        # 생성된 구조 검증
        # 1. toc.json 파일 존재 및 유효성 확인
        toc_file = output_path / "toc.json"
        assert toc_file.exists(), "toc.json 파일이 생성되지 않았습니다"
        
        with open(toc_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
            assert 'toc_structure' in toc_data
        
        print("✅ toc.json 파일 검증 완료")
        
        # 2. 장별 폴더 및 내용 검증
        for folder_info in result['created_folders']:
            # 필수 필드 확인
            required_fields = ['normalized_title', 'folder_path', 'items_count', 'toc_file', 'content_file']
            for field in required_fields:
                assert field in folder_info, f"{field} 필드가 없습니다"
            
            # 제거된 필드들이 없는지 확인
            removed_fields = ['chapter_number', 'chapter_title', 'page_range']
            for field in removed_fields:
                assert field not in folder_info, f"제거되어야 할 {field} 필드가 여전히 존재합니다"
            
            # 폴더 존재 확인
            folder_path = Path(folder_info['folder_path'])
            assert folder_path.exists(), f"장 폴더가 생성되지 않았습니다: {folder_path}"
            assert folder_path.is_dir()
            
            # toc 파일 존재 및 유효성 확인
            toc_file_path = Path(folder_info['toc_file'])
            if toc_file_path.exists():
                with open(toc_file_path, 'r', encoding='utf-8') as f:
                    toc_items = json.load(f)
                    assert isinstance(toc_items, list)
            
            # content 파일 존재 확인
            if folder_info['content_file']:
                content_file_path = Path(folder_info['content_file'])
                if content_file_path.exists():
                    assert content_file_path.stat().st_size > 0
                    
            print(f"✅ 장 폴더 검증 완료: {folder_info['normalized_title']} (items: {folder_info['items_count']})")
        
        # 3. 서비스 초기화 확인
        assert workspace_stage.toc_service is not None
        assert workspace_stage.ai_service is not None  
        assert workspace_stage.chapter_extraction_service is not None
        assert workspace_stage.logger is not None
        assert workspace_stage.normalized_book_title is not None
        assert workspace_stage.book_title is not None
        
        print(f"✅ 서비스 통합 확인: {workspace_stage.book_title}")
        print(f"✅ 정규화된 제목: {workspace_stage.normalized_book_title}")
        
        # 4. 최종 출력 결과를 data 폴더에 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = test_output_dir / f"workspace_preparation_result_{timestamp}.json"
        
        # 결과를 JSON 파일로 저장
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"💾 최종 출력 결과 저장: {result_file}")
        print(f"🎉 전체 워크스페이스 준비 프로세스 테스트 완료!")