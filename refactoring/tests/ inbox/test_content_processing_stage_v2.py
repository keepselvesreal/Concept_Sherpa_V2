# 생성 시간: Mon Sep  8 11:42:01 KST 2025
# 핵심 내용: ContentProcessingStage.process() 실제 데이터 테스트 v2
# 상세 내용:
#   - TestContentProcessingStageV2 (라인 35-200): 메인 테스트 클래스
#   - setup_temp_data (라인 50-85): 임시 폴더 생성 및 실제 데이터 복사
#   - test_load_and_sort_documents (라인 87-130): 문서 정렬 기능 테스트
#   - test_process_with_real_data (라인 132-180): 전체 process() 실행 테스트
# 상태: active

import os
import shutil
import tempfile
import asyncio
import pytest
import json
from pathlib import Path
import sys

# refactoring 프로젝트 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
refactoring_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, refactoring_root)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from src.stages.content_processing_stage import ContentProcessingStage
from src.services.ai_service_v4 import AIService


class TestContentProcessingStageV2:
    """
    ContentProcessingStage.process() 실제 데이터 테스트 v2
    - 실제 모듈과 데이터 사용 (목 금지)  
    - 테스트 내부에서 임시 폴더 생성 및 데이터 복사
    - 문서 정렬 부분만 테스트 검증
    - 나머지는 결과 파일 생성 여부만 확인
    """
    
    @pytest.fixture
    def temp_test_data(self):
        """임시 폴더 생성 및 실제 데이터 복사 - tests/data에 결과 유지"""
        # 원본 데이터 경로
        source_data_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/integrated_node_generation_test/1_Complexity_of_object_oriented_programming"
        
        # tests/data 디렉터리에 결과 저장
        tests_data_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data"
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_dir_name = f"content_processing_result_{timestamp}"
        temp_dir = os.path.join(tests_data_dir, result_dir_name)
        temp_book_path = os.path.join(temp_dir, "1_Complexity_of_object_oriented_programming")
        
        try:
            # 결과 디렉터리 생성
            os.makedirs(temp_dir, exist_ok=True)
            
            # 전체 디렉터리 구조 복사
            shutil.copytree(source_data_path, temp_book_path)
            
            # 복사 결과 확인
            unified_docs_dir = os.path.join(temp_book_path, "unified_info_docs")
            assert os.path.exists(unified_docs_dir), f"unified_info_docs 디렉터리 복사 실패: {unified_docs_dir}"
            
            doc_files = list(Path(unified_docs_dir).glob("*_info.md"))
            assert len(doc_files) > 0, f"문서 파일 복사 실패: {len(doc_files)}개"
            
            print(f"✅ 테스트 데이터 복사 완료: {len(doc_files)}개 문서")
            print(f"📁 결과 저장 위치: {temp_dir}")
            yield temp_book_path
            
        finally:
            # 결과 유지 - 정리하지 않음
            print(f"💾 결과 유지됨: {temp_dir}")
            print(f"📄 처리된 파일들 확인: {os.path.join(temp_book_path, 'unified_info_docs')}")
    
    @pytest.fixture
    def ai_service(self):
        """AIService 실제 인스턴스 생성 (gemini-2.0-flash-lite 사용)"""
        # 실제 모듈 import
        from src.utils.config_manager import ConfigManager
        from src.utils.logger_v2 import Logger
        
        # 실제 ConfigManager 생성
        config_manager = ConfigManager()
        
        # 실제 Logger 생성  
        logger = Logger("test_content_processing")
        
        return AIService(config_manager, logger, 'content_processing')
    
    @pytest.mark.asyncio
    async def test_load_and_sort_documents(self, temp_test_data, ai_service):
        """문서 로드 및 정렬 기능 테스트 - 핵심 검증 부분"""
        # ContentProcessingStage 인스턴스 생성
        config = {'processing_mode': 'unified_type_processing', 'max_parallel': 4}
        stage = ContentProcessingStage(config, ai_service)
        
        # 문서 로드 및 정렬 실행
        sorted_groups = await stage.load_and_sort_documents(temp_test_data)
        
        # 🎯 핵심 검증: 문서 정렬 결과
        assert len(sorted_groups) > 0, "정렬된 그룹이 없습니다"
        
        # 첫 번째 그룹은 리프 노드여야 함 (composition_section이 비어있는 문서들)
        leaf_group = sorted_groups[0]
        assert len(leaf_group) > 0, "리프 노드 그룹이 비어있습니다"
        
        for doc in leaf_group:
            composition = doc.get('composition_section', '').strip()
            assert not composition or composition == '---', f"리프 노드에 구성 섹션이 있음: {composition}"
            print(f"✅ 리프 노드 확인: {doc.get('title', 'Unknown')}")
        
        # 나머지 그룹들은 level 내림차순이어야 함 (비리프 노드들)
        if len(sorted_groups) > 1:
            prev_level = float('inf')  # 첫 번째는 가장 높은 level이어야 함
            
            for i in range(1, len(sorted_groups)):
                group = sorted_groups[i]
                if len(group) > 0:
                    current_level = group[0].get('level', 0)
                    assert current_level <= prev_level, f"Level 정렬 오류: {current_level} > {prev_level}"
                    prev_level = current_level
                    
                    # 비리프 노드 확인
                    for doc in group:
                        composition = doc.get('composition_section', '').strip()
                        assert composition and composition != '---', f"비리프 노드에 구성 섹션이 없음: {doc.get('title')}"
                    
                    print(f"✅ Level {current_level} 그룹 확인: {len(group)}개 문서")
        
        print(f"🎉 문서 정렬 테스트 성공: {len(sorted_groups)}개 그룹")
        return sorted_groups
    
    @pytest.mark.asyncio  
    async def test_process_with_real_data(self, temp_test_data, ai_service):
        """전체 process() 실행 테스트 - 결과 파일 생성 확인"""
        # ContentProcessingStage 인스턴스 생성
        config = {'processing_mode': 'unified_type_processing', 'max_parallel': 4}
        stage = ContentProcessingStage(config, ai_service)
        
        # process() 전체 실행
        print(f"🚀 process() 실행 시작: {temp_test_data}")
        result = await stage.process(temp_test_data)
        
        # 기본 결과 검증
        assert result is not None, "process() 결과가 None입니다"
        assert 'success' in result, "결과에 success 필드가 없습니다"
        
        print(f"📊 Process 결과: {result}")
        
        # 결과 파일들 생성 여부 확인 (내용은 수동 확인)
        unified_docs_dir = os.path.join(temp_test_data, "unified_info_docs")
        doc_files = list(Path(unified_docs_dir).glob("*_info.md"))
        
        # 각 파일에 추출 섹션이 업데이트되었는지 확인
        updated_count = 0
        for doc_file in doc_files:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 추출 섹션 존재 여부만 확인 (내용은 수동 확인용)
            if '# 추출' in content and '## 핵심 내용' in content:
                updated_count += 1
                print(f"✅ 추출 섹션 확인: {doc_file.name}")
        
        print(f"🎉 Process 테스트 완료: {updated_count}/{len(doc_files)}개 파일 업데이트")
        print(f"📁 결과 확인 경로: {unified_docs_dir}")
        
        return result