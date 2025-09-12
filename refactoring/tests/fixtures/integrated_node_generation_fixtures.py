# 생성 시간: Fri Sep 12 12:35:22 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 테스트용 픽스처들 (workspace_result.json 기반)
# 상세 내용:
#   - integrated_stage (라인 16-22): 실제 IntegratedNodeGenerationStage 인스턴스
#   - integrated_stage_with_mock (라인 24-38): Mock AI 서비스를 사용하는 IntegratedNodeGenerationStage 인스턴스
#   - selected_chapters_data (라인 40-62): workspace_result.json에서 1, 2장 데이터 동적 로딩
#   - normalized_book_title (라인 64-67): 정규화된 책 제목
# 상태: active
# 참조: integrated_node_generation_fixtures.py (하드코딩 데이터 제거하고 동적 로딩으로 개선)

import pytest
import asyncio
from unittest.mock import AsyncMock

# 테스트 대상 임포트
from src.stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage

@pytest.fixture
def integrated_stage(config_manager):
    """실제 IntegratedNodeGenerationStage 인스턴스 (AI API 호출)"""
    return IntegratedNodeGenerationStage(config_manager)

@pytest.fixture  
def integrated_stage_with_mock(config_manager):
    """Mock AI 서비스를 사용하는 IntegratedNodeGenerationStage 인스턴스"""
    stage = IntegratedNodeGenerationStage(config_manager)
    
    # ContentDocumentService Mock 설정
    mock_service = AsyncMock()
    mock_service.detect_section_content.return_value = [
        {'section_title': '1.1 Test Section', 'has_content': True}
    ]
    mock_service.extract_section_content.return_value = [
        {'section_title': '1.1 Test Section', 'extracted_content': 'Mock content'}
    ]
    
    stage.content_document_service = mock_service
    
    return stage

@pytest.fixture
def selected_chapters_data():
    """설정 파일에서 선택된 챕터들만 동적 로딩"""
    import json
    from pathlib import Path
    
    # 설정 파일에서 선택된 챕터 인덱스 로드
    config_file = Path("tests/config/selected_chapters.json")
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        selected_indices = config.get('selected_chapter_indices', [0, 1])
    else:
        selected_indices = [0, 1]  # 기본값: 1,2장
    
    # workspace_result.json 파일 로드
    workspace_file = Path("tests/data/workspace_preparation/workspace_result.json")
    
    if not workspace_file.exists():
        raise FileNotFoundError(f"workspace_result.json 파일이 없습니다: {workspace_file}")
    
    with open(workspace_file, 'r', encoding='utf-8') as f:
        workspace_data = json.load(f)
    
    # 전체 chapters_data 추출
    all_chapters_data = workspace_data.get('data', {}).get('chapters_data', [])
    if not all_chapters_data:
        raise ValueError("chapters_data가 workspace_result.json에 없습니다")
    
    # 선택된 인덱스에 해당하는 챕터들만 반환
    selected_chapters = []
    for index in selected_indices:
        if index < len(all_chapters_data):
            selected_chapters.append(all_chapters_data[index])
        else:
            print(f"⚠️ 챕터 인덱스 {index}는 존재하지 않음 (총 {len(all_chapters_data)}개)")
    
    print(f"🔍 선택된 챕터: {len(selected_chapters)}개 (인덱스: {selected_indices})")
    return selected_chapters

@pytest.fixture 
def normalized_book_title():
    """정규화된 책 제목"""
    from src.utils.text_utils import normalize_title
    return normalize_title("Data-Oriented Programming")