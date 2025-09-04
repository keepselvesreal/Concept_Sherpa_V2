# 생성 시간: Thu Sep  4 08:17:51 KST 2025
# 핵심 내용: pytest 전역 설정 및 실제 데이터 픽스처 정의
# 상세 내용:
#   - sys.path 설정 (라인 14-15): src 모듈 import 경로 추가
#   - real_pdf_path (라인 17-22): 실제 테스트용 PDF 파일 경로 픽스처
#   - temp_directory (라인 24-29): 임시 디렉터리 픽스처 (테스트 후 자동 정리)
# 상태: active
# 주소: tests/conftest
# 참조: N/A

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest

# src 모듈 import를 위한 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def real_pdf_path():
    """실제 테스트용 PDF 파일 경로"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip(f"실제 PDF 파일이 없습니다: {pdf_path}")
    return pdf_path

@pytest.fixture
def temp_directory():
    """임시 디렉터리 픽스처 - 테스트 후 자동 정리"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)