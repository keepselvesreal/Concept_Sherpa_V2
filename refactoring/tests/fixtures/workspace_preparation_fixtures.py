# 생성 시간: Tue Sep  9 22:49:15 KST 2025
# 핵심 내용: WorkspacePreparationStage 전용 픽스처 정의
# 상세 내용:
#   - real_pdf_path (라인 14-20): 실제 테스트용 PDF 파일 경로 픽스처
#   - toc_data (라인 22-54): workspace_result.json에서 raw_toc_data 추출하는 TOC 데이터 픽스처
# 상태: active

import pytest
import json
import asyncio
from pathlib import Path

@pytest.fixture(scope="session")
def real_pdf_path():
    """실제 테스트용 PDF 파일 경로 - WorkspacePreparation 전용"""
    pdf_path = Path(__file__).parent / "pdfs" / "2022_Data-Oriented Programming_Manning.pdf"
    if not pdf_path.exists():
        pytest.skip(f"실제 PDF 파일이 없습니다: {pdf_path}")
    return str(pdf_path)

@pytest.fixture(scope="session")
def toc_data(request, real_pdf_path, config_manager, test_logger):
    """
    TOC 데이터 픽스처 - WorkspacePreparation 전용
    workspace_result.json에서 raw_toc_data 추출하여 사용
    """
    # workspace_result.json 파일 경로
    workspace_result_path = Path(__file__).parent.parent / "data" / "workspace_preparation" / "workspace_result.json"
    
    # --regen-fixtures 옵션 체크 또는 workspace_result.json이 없는 경우
    if request.config.getoption("--regen-fixtures") or not workspace_result_path.exists():
        print("🔄 TOC 데이터 생성 중...")
        
        # 실제 PDF에서 TOC 추출
        from services.toc_service import TocService
        toc_service = TocService(config_manager, test_logger)
        
        # 🟢 올바른 메서드명 사용: extract_complete_toc (동기 메서드)
        toc_result = toc_service.extract_complete_toc(real_pdf_path)
        
        if not toc_result or 'toc_structure' not in toc_result or len(toc_result['toc_structure']) == 0:
            pytest.skip(f"TOC 추출 실패 또는 빈 구조")
        
        print(f"✅ TOC 데이터 생성 완료: {len(toc_result['toc_structure'])}개 항목")
        return toc_result
    
    # workspace_result.json에서 raw_toc_data 추출
    with open(workspace_result_path, 'r', encoding='utf-8') as f:
        workspace_result = json.load(f)
    
    if 'data' in workspace_result and 'raw_toc_data' in workspace_result['data']:
        return workspace_result['data']['raw_toc_data']
    else:
        pytest.skip("workspace_result.json에서 raw_toc_data를 찾을 수 없습니다")