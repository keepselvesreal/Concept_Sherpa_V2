# 생성 시간: Wed Sep 11 17:15:32 KST 2025
# 핵심 내용: ContentProcessingStage 메인 테스트 파일 (JSON 직접 로드 방식)
# 상세 내용:
#   - TestContentProcessingStage (라인 25-60): ContentProcessingStage 클래스 메인 테스트
#   - test_generate_extract_section_success (라인 35-55): generate_extract_section 정상 동작 테스트
# 상태: active

"""
구현 파일명: content_processing_stage.py
"""

import pytest
import asyncio
import logging
import json
from typing import Dict, Any
from unittest.mock import AsyncMock

import sys
from pathlib import Path
# refactoring 프로젝트 경로 추가
refactoring_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(refactoring_root))

from stages.content_processing_stage import ContentProcessingStage
from services.ai_service_v4 import AIService


def load_test_document(chapter_idx: int = 0, node_type: str = "leaf", node_idx: int = 0) -> Dict[str, Any]:
    """
    테스트용 문서 데이터 로더
    
    Args:
        chapter_idx: 장 인덱스 (0부터 시작)
        node_type: 노드 타입 ("leaf" 또는 "non_leaf")
        node_idx: 노드 인덱스 (0부터 시작, -1이면 모든 노드 반환)
    
    Returns:
        Dict[str, Any]: 선택된 문서 데이터 또는 문서 리스트
    """
    data_path = Path(__file__).parent.parent / "data" / "content_processing" / "load_and_sort_result.json"
    assert data_path.exists(), f"테스트 데이터 파일이 없습니다: {data_path}"
    
    with open(data_path, 'r', encoding='utf-8') as f:
        load_and_sort_data = json.load(f)
    
    # 데이터 구조: result.output.chapters[].leaf_nodes[] 또는 non_leaf_nodes[]
    chapters = load_and_sort_data.get('result', {}).get('output', {}).get('chapters', [])
    assert chapters and len(chapters) > chapter_idx, f"{chapter_idx + 1}장 데이터가 없습니다 (총 {len(chapters)}장)"
    
    target_chapter = chapters[chapter_idx]
    
    if node_type == "leaf":
        nodes = target_chapter.get('leaf_nodes', [])
        node_type_desc = "리프 노드"
    elif node_type == "non_leaf":
        nodes = target_chapter.get('non_leaf_nodes', [])
        node_type_desc = "비리프 노드"
    else:
        raise ValueError(f"지원하지 않는 노드 타입: {node_type}. 'leaf' 또는 'non_leaf'를 사용하세요.")
    
    assert nodes, f"{chapter_idx + 1}장에 {node_type_desc} 데이터가 없습니다"
    
    if node_idx == -1:
        # 모든 노드 반환
        print(f"📚 {chapter_idx + 1}장 {node_type_desc} 전체 로드: {len(nodes)}개")
        return nodes
    else:
        # 특정 노드 반환
        assert len(nodes) > node_idx, f"{chapter_idx + 1}장 {node_type_desc}에서 {node_idx + 1}번째 데이터가 없습니다 (총 {len(nodes)}개)"
        selected_node = nodes[node_idx]
        print(f"📄 {chapter_idx + 1}장 {node_type_desc} {node_idx + 1}번째 데이터 로드: {selected_node.get('title', 'Unknown')}")
        return selected_node


class TestContentProcessingStage:
    """ContentProcessingStage 메인 테스트 클래스"""
    
    @pytest.mark.component
    @pytest.mark.expensive
    @pytest.mark.asyncio
    async def test_generate_extract_section_success(self):
        """
        요구사항: generate_extract_section은 실제 문서 데이터로 5개 섹션을 모두 성공적으로 추출한다
        
        입력: 실제 문서 데이터 (title, content_section 포함)
        출력: Dict[str, str] - 5개 섹션이 모두 포함된 딕셔너리
        
        사용 예시:
        - 1장 리프 노드 첫 번째: load_test_document(0, "leaf", 0)
        - 1장 비리프 노드 첫 번째: load_test_document(0, "non_leaf", 0)  
        - 2장 모든 리프 노드: load_test_document(1, "leaf", -1)
        """
        # Given - 1장 리프 노드 첫 번째 데이터 사용
        sample_document = load_test_document(chapter_idx=0, node_type="leaf", node_idx=0)
        
        config = {}
        
        # 로거 생성
        logger = logging.getLogger("test_content_processing_stage")
        logger.setLevel(logging.INFO)
        
        # 실제 AI 서비스 사용
        ai_service = AIService(config, logger, "content_processing")
        stage = ContentProcessingStage(config, ai_service)
        
        # When
        result = await stage.generate_extract_section(sample_document)
        
        # Then
        assert isinstance(result, dict), "결과는 딕셔너리여야 함"
        
        # 5개 섹션 키 존재 확인
        expected_keys = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
        for key in expected_keys:
            assert key in result, f"{key} 섹션이 결과에 없음"
        
        # 각 섹션이 적절한 헤더로 시작하는지 확인 - 5개 모두 성공해야 함
        section_headers = {
            'core_content': '## 핵심 내용',
            'detailed_core_content': '## 상세 핵심 내용', 
            'detailed_content': '## 상세 정보',
            'main_topics': '## 주요 화제',
            'sub_topics': '## 부차 화제'
        }
        
        # 모든 섹션이 성공해야 함
        for key, expected_header in section_headers.items():
            assert key in result, f"{key} 섹션이 결과에 없음"
            assert result[key].strip(), f"{key} 섹션이 비어있음"
            assert result[key].strip().startswith(expected_header), f"{key} 섹션이 올바른 헤더로 시작하지 않음"
        
        # AI 호출 카운터 증가 확인
        assert stage.api_calls_counter > 0, "AI 호출 카운터가 증가하지 않음"
        
        print(f"✅ 모든 섹션 추출 성공: 5/5 섹션")
        print(f"📊 AI 호출 횟수: {stage.api_calls_counter}")