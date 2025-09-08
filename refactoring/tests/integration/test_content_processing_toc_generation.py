# 생성 시간: Mon Sep  8 11:56:30 KST 2025
# 핵심 내용: ContentProcessingStage.generate_enhanced_toc_file() 실제 데이터 테스트
# 상세 내용:
#   - TestContentProcessingTOCGeneration (라인 25-80): 메인 테스트 클래스
#   - test_generate_enhanced_toc_file (라인 50-80): 목차 생성 테스트
# 상태: active

import os
import asyncio
import pytest
from pathlib import Path
import sys

# refactoring 프로젝트 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
refactoring_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, refactoring_root)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from src.stages.content_processing_stage import ContentProcessingStage
from src.services.ai_service_v4 import AIService
from src.utils.config_manager import ConfigManager
from src.utils.logger_v2 import Logger


class TestContentProcessingTOCGeneration:
    """
    ContentProcessingStage.generate_enhanced_toc_file() 실제 데이터 테스트
    - 실제 모듈과 데이터 사용 (목 금지)
    - 기존 처리 결과 데이터 활용
    - 목차 파일 생성 여부 확인
    """
    
    @pytest.fixture
    def existing_processed_data(self):
        """기존 처리 완료된 데이터 경로"""
        data_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/content_processing_result_20250908_115430/1_Complexity_of_object_oriented_programming"
        
        # 경로 존재 여부 확인
        assert os.path.exists(data_path), f"처리된 데이터 경로가 없음: {data_path}"
        
        # unified_info_docs 확인
        unified_docs_dir = os.path.join(data_path, "unified_info_docs")
        assert os.path.exists(unified_docs_dir), f"unified_info_docs 디렉터리가 없음: {unified_docs_dir}"
        
        # TOC 파일 확인
        toc_file = os.path.join(data_path, "1_Complexity_of_object_oriented_programming_toc.json")
        assert os.path.exists(toc_file), f"TOC 파일이 없음: {toc_file}"
        
        print(f"✅ 기존 처리 데이터 확인: {data_path}")
        return data_path
    
    @pytest.fixture
    def ai_service(self):
        """AIService 실제 인스턴스 생성 (gemini-2.0-flash-lite 사용)"""
        # 실제 ConfigManager 생성
        config_manager = ConfigManager()
        
        # 실제 Logger 생성  
        logger = Logger("test_toc_generation")
        
        return AIService(config_manager, logger, 'content_processing')
    
    @pytest.mark.asyncio
    async def test_generate_enhanced_toc_file(self, existing_processed_data, ai_service):
        """목차 파일 생성 테스트"""
        # ContentProcessingStage 인스턴스 생성
        config = {'processing_mode': 'unified_type_processing', 'max_parallel': 4}
        stage = ContentProcessingStage(config, ai_service)
        
        # generate_enhanced_toc_file() 실행
        print(f"🚀 목차 파일 생성 시작: {existing_processed_data}")
        result = await stage.generate_enhanced_toc_file(existing_processed_data)
        
        # 기본 결과 검증
        assert result is True, "목차 파일 생성 실패"
        
        # 생성된 목차 파일 확인
        chapter_name = os.path.basename(existing_processed_data)
        toc_file_path = os.path.join(existing_processed_data, f"{chapter_name}_enhanced_toc.md")
        
        assert os.path.exists(toc_file_path), f"목차 파일이 생성되지 않음: {toc_file_path}"
        
        # 파일 내용 확인 (기본적인 구조만)
        with open(toc_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 기본 헤더 구조 확인
        assert '# ' in content, "헤더가 없음"
        assert '## 핵심 내용' in content, "핵심 내용 섹션이 없음"
        
        print(f"✅ 목차 파일 생성 성공: {toc_file_path}")
        print(f"📄 파일 크기: {len(content)} 문자")
        print(f"📁 결과 확인: {toc_file_path}")
        
        return toc_file_path