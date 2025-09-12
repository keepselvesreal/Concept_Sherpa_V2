# 생성 시간: Thu Sep 11 11:55:51 KST 2025
# 핵심 내용: ContentProcessingStage.load_and_sort_documents TDD 테스트 (unit/sociable)
# 상세 내용:
#   - test_load_and_sort_documents_returns_chapter_groups (라인 25-40): 장별 그룹화 테스트
#   - test_load_and_sort_documents_separates_leaf_and_nonleaf_nodes (라인 42-60): 리프/비리프 분리 테스트
#   - test_load_and_sort_documents_sorts_nonleaf_by_level_desc (라인 62-80): level별 정렬 테스트
# 상태: active

"""
구현 파일명: content_processing_stage.py
"""

import pytest
import asyncio
import logging
from typing import Dict, Any, List

import sys
from pathlib import Path
# refactoring 프로젝트 경로 추가
refactoring_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(refactoring_root))

from stages.content_processing_stage import ContentProcessingStage
from utils.logger_v2 import Logger
sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from content_processing_fixtures import integrated_node_generation_stage_data


class TestContentProcessingStageLoadAndSort:
    """ContentProcessingStage.load_and_sort_documents 메서드 테스트"""
    
    @pytest.mark.unit
    @pytest.mark.sociable
    def test_load_and_sort_documents_returns_chapter_groups(self, integrated_node_generation_stage_data):
        """
        요구사항: load_and_sort_documents는 장별로 그룹화된 결과를 반환한다
        
        입력: IntegratedNodeGenerationStage v4 결과 데이터
        출력: {"output": {"chapters": [...]}, "error": None} 구조
        """
        # Given
        config = {}
        logger = Logger("test_project")
        stage = ContentProcessingStage(config, logger)
        
        # When
        result = asyncio.run(stage.load_and_sort_documents(integrated_node_generation_stage_data))
        
        # Then
        assert isinstance(result, dict), "반환값은 딕셔너리여야 함"
        assert "output" in result, "output 필드가 있어야 함"
        assert "error" in result, "error 필드가 있어야 함"
        assert result["error"] is None, "성공 시 error는 None이어야 함"
        
        chapters = result["output"]["chapters"]
        assert isinstance(chapters, list), "chapters는 리스트여야 함"
        
        # 예상 장 수만큼 그룹이 생성되어야 함
        processed_chapters = integrated_node_generation_stage_data.get('processed_chapters', [])
        expected_chapter_count = len(processed_chapters)
        assert len(chapters) == expected_chapter_count, f"장 수만큼 그룹이 생성되어야 함: 예상 {expected_chapter_count}, 실제 {len(chapters)}"

    @pytest.mark.unit
    @pytest.mark.sociable
    def test_load_and_sort_documents_separates_leaf_and_nonleaf_nodes(self, integrated_node_generation_stage_data):
        """
        요구사항: 각 장 내에서 리프 노드와 비리프 노드를 분리한다
        
        입력: 통합 문서 데이터
        출력: 각 장별로 leaf_nodes, non_leaf_nodes 필드로 분리
        """
        # Given
        config = {}
        logger = Logger("test_project")
        stage = ContentProcessingStage(config, logger)
        
        # When
        result = asyncio.run(stage.load_and_sort_documents(integrated_node_generation_stage_data))
        
        # Then
        chapters = result["output"]["chapters"]
        for chapter in chapters:
            assert isinstance(chapter, dict), "각 장은 딕셔너리여야 함"
            assert "leaf_nodes" in chapter, "leaf_nodes 필드가 있어야 함"
            assert "non_leaf_nodes" in chapter, "non_leaf_nodes 필드가 있어야 함"
            
            # 리프 노드들 검증 (리스트 구조)
            assert isinstance(chapter["leaf_nodes"], list), "leaf_nodes는 리스트여야 함"
            for doc in chapter["leaf_nodes"]:
                composition_files = doc.get('composition_files', [])
                assert len(composition_files) == 0, "리프 노드는 composition_files가 비어있어야 함"
            
            # 비리프 노드들 검증 (딕셔너리 구조)
            assert isinstance(chapter["non_leaf_nodes"], dict), "non_leaf_nodes는 딕셔너리여야 함"
            for level_key, nodes in chapter["non_leaf_nodes"].items():
                assert level_key.startswith("level_"), f"level 키는 'level_'로 시작해야 함: {level_key}"
                assert isinstance(nodes, list), f"{level_key}의 값은 리스트여야 함"
                for doc in nodes:
                    composition_files = doc.get('composition_files', [])
                    assert len(composition_files) > 0, f"비리프 노드는 composition_files가 있어야 함: {doc.get('title', 'Unknown')}"

    @pytest.mark.unit
    @pytest.mark.sociable
    def test_load_and_sort_documents_sorts_nonleaf_by_level_desc(self, integrated_node_generation_stage_data):
        """
        요구사항: 비리프 노드들은 level 내림차순으로 정렬된다
        
        입력: 통합 문서 데이터  
        출력: non_leaf_nodes 리스트가 level 높은 순서로 정렬됨
        """
        # Given
        config = {}
        logger = Logger("test_project")
        stage = ContentProcessingStage(config, logger)
        
        # When
        result = asyncio.run(stage.load_and_sort_documents(integrated_node_generation_stage_data))
        
        # Then
        chapters = result["output"]["chapters"]
        for chapter in chapters:
            non_leaf_nodes = chapter["non_leaf_nodes"]
            
            if len(non_leaf_nodes) > 1:  # 비리프 노드가 여러 개인 경우
                prev_level = float('inf')
                for doc in non_leaf_nodes:
                    current_level = doc.get('level', 0)
                    assert current_level <= prev_level, f"level이 내림차순으로 정렬되어야 함: 이전 {prev_level}, 현재 {current_level}"
                    prev_level = current_level