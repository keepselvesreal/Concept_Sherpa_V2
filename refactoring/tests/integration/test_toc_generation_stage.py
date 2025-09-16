# 생성 시간: Mon Sep 15 22:29:53 KST 2025
# 핵심 내용: ToCGenerationStage pytest 테스트 코드 (generate_chapter_toc, generate_book_toc 테스트)
# 상세 내용:
#   - test_generate_chapter_toc (라인 35-70): 장 수준 목차 생성 테스트
#   - test_generate_book_toc (라인 72-105): 책 수준 목차 생성 테스트
#   - setup (라인 15-33): 테스트 설정 및 데이터 로드
# 상태: active

import sys
import json
import pytest
from pathlib import Path

# 프로젝트 경로를 sys.path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / "src"))

from stages.toc_generation_stage import ToCGenerationStage
from utils.config_manager import ConfigManager
from utils.text_utils import normalize_title

@pytest.fixture
def toc_stage():
    """ToCGenerationStage 인스턴스 생성"""
    config_path = project_root / "config" / "pipeline_config.yaml"
    config_manager = ConfigManager(str(config_path))
    return ToCGenerationStage(config_manager)

@pytest.fixture
def test_data():
    """테스트 데이터 로드"""
    test_data_path = Path('/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/content_processing_stage/process_result.json')
    
    with open(test_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

@pytest.mark.asyncio
async def test_generate_chapter_toc(toc_stage, test_data):
    """장 수준 목차 생성 테스트"""
    # 테스트 데이터에서 첫 번째 장 정보 가져오기
    chapter_info_docs = test_data['data']['chapter_info_docs']
    first_chapter_name = list(chapter_info_docs.keys())[0]
    first_chapter_files = chapter_info_docs[first_chapter_name]
    normalized_book_title = "Data_Oriented_Programming"
    
    # 장 목차 생성 실행
    result = await toc_stage.generate_chapter_toc(
        first_chapter_name, 
        first_chapter_files, 
        normalized_book_title
    )
    
    # 결과 검증
    assert 'error' not in result, f"오류 발생: {result.get('error')}"
    
    # 기대값 검증
    expected_keys = ['chapter_name', 'normalized_chapter_name', 'toc_file_path', 'sections_count']
    for key in expected_keys:
        assert key in result, f"결과에 '{key}' 키가 없음"
    
    # 파일 생성 확인
    toc_file_path = Path(result['toc_file_path'])
    assert toc_file_path.exists(), f"목차 파일이 생성되지 않음: {toc_file_path}"
    
    # 파일 내용 확인
    with open(toc_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert len(content) > 0, "생성된 목차 파일이 비어있음"
    # 파일명이 헤더로 사용되므로, 해당 장의 파일명이 포함되어 있는지 확인
    chapter_files = test_data['data']['chapter_info_docs'][first_chapter_name]
    chapter_file_found = any(Path(file_path).name in content for file_path in chapter_files)
    assert chapter_file_found, "장 관련 파일명이 목차에 포함되지 않음"
    
    print(f"✅ 장 목차 생성 성공: {toc_file_path}")
    print(f"✅ 추출된 섹션 수: {result['sections_count']}")

@pytest.mark.asyncio
async def test_generate_book_toc(toc_stage, test_data):
    """책 수준 목차 생성 테스트"""
    # 테스트 데이터
    book_title = test_data['data']['book_title']
    chapter_info_docs = test_data['data']['chapter_info_docs']
    normalized_book_title = "Data_Oriented_Programming"
    
    # 책 목차 생성 실행
    result = await toc_stage.generate_book_toc(
        book_title,
        chapter_info_docs,
        normalized_book_title
    )
    
    # 결과 검증
    assert 'error' not in result, f"오류 발생: {result.get('error')}"
    
    # 기대값 검증
    expected_keys = ['book_title', 'normalized_book_title', 'toc_file_path', 'chapters_count']
    for key in expected_keys:
        assert key in result, f"결과에 '{key}' 키가 없음"
    
    # 파일 생성 확인
    toc_file_path = Path(result['toc_file_path'])
    assert toc_file_path.exists(), f"목차 파일이 생성되지 않음: {toc_file_path}"
    
    # 파일 내용 확인
    with open(toc_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert len(content) > 0, "생성된 목차 파일이 비어있음"
    assert book_title in content, "책 제목이 목차에 포함되지 않음"
    
    # 각 장의 정규화된 제목이 목차에 포함되는지 확인 (정규화된 장 제목이 헤더로 사용됨)
    for chapter_name in chapter_info_docs.keys():
        normalized_chapter_name = normalize_title(chapter_name)
        assert normalized_chapter_name in content, f"장 '{chapter_name}'의 정규화된 제목 '{normalized_chapter_name}'이 책 목차에 포함되지 않음"
    
    print(f"✅ 책 목차 생성 성공: {toc_file_path}")
    print(f"✅ 처리된 장 개수: {result['chapters_count']}")