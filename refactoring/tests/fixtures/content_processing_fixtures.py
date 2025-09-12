# 생성 시간: Thu Sep 11 11:24:41 KST 2025
# 핵심 내용: ContentProcessingStage.load_and_sort_documents 테스트용 픽스처
# 상세 내용:
#   - integrated_node_generation_stage_data (라인 10-25): IntegratedNodeGenerationStage v4 처리 결과 데이터
# 상태: active

import json
import pytest
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def integrated_node_generation_stage_data() -> Dict[str, Any]:
    """IntegratedNodeGenerationStage v4 처리 결과 데이터 (실제 테스트 데이터 활용)"""
    test_data_path = Path(__file__).parent.parent / "data" / "integrated_node_generation" / "process_result.json"
    
    if not test_data_path.exists():
        pytest.skip(f"테스트 데이터 파일이 없습니다: {test_data_path}")
    
    with open(test_data_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # documents 필드의 data 필드 데이터를 픽스처로 제공
    documents_result = raw_data.get('documents', {})
    return documents_result.get('data', {})


@pytest.fixture
def sample_document_for_extraction() -> Dict[str, Any]:
    """generate_extract_section 테스트용 실제 문서 데이터"""
    load_and_sort_data_path = Path(__file__).parent.parent / "data" / "content_processing" / "load_and_sort_result.json"
    
    if not load_and_sort_data_path.exists():
        pytest.skip(f"테스트 데이터 파일이 없습니다: {load_and_sort_data_path}")
    
    with open(load_and_sort_data_path, 'r', encoding='utf-8') as f:
        load_and_sort_data = json.load(f)
    
    # 첫 번째 문서 그룹에서 첫 번째 문서 반환 (실제 데이터)
    result = load_and_sort_data.get('result', [])
    if result and len(result) > 0 and len(result[0]) > 0 and len(result[0][0]) > 0:
        return result[0][0][0]  # 첫 번째 그룹, 첫 번째 서브그룹, 첫 번째 문서
    
    pytest.skip("load_and_sort_result.json에서 테스트용 문서를 찾을 수 없습니다")


@pytest.fixture
def extraction_result() -> Dict[str, str]:
    """AI 추출 결과 데이터 (extract_section_result.json의 result 필드 활용)"""
    extract_data_path = Path(__file__).parent.parent / "data" / "content_processing" / "extract_section_result.json"
    
    if not extract_data_path.exists():
        pytest.skip(f"테스트 데이터 파일이 없습니다: {extract_data_path}")
    
    with open(extract_data_path, 'r', encoding='utf-8') as f:
        extract_data = json.load(f)
    
    # result 필드 추출 (AI 추출 섹션 5개)
    result = extract_data.get('result', {})
    if not result:
        pytest.skip("extract_section_result.json에서 result 필드를 찾을 수 없습니다")
    
    return result