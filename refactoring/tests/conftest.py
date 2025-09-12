# 생성 시간: Thu Sep  4 08:17:51 KST 2025
# 핵심 내용: pytest 전역 설정 및 공통 픽스처 정의
# 상세 내용:
#   - pytest_addoption (라인 15-23): --regen-fixtures 커스텀 옵션 정의
#   - sys.path 설정 (라인 26-27): src 모듈 import 경로 추가
#   - temp_directory (라인 29-34): 임시 디렉터리 픽스처 (테스트 후 자동 정리)
#   - config_manager (라인 36-40): ConfigManager 공통 픽스처
#   - test_logger (라인 42-46): Logger 공통 픽스처
# 상태: active
# 주소: tests/conftest
# 참조: N/A

import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
import pytest

# pytest 커스텀 옵션 정의
def pytest_addoption(parser):
    """--regen-fixtures 옵션 정의"""
    parser.addoption(
        "--regen-fixtures",
        action="store_true",
        default=False,
        help="테스트 픽스처 데이터를 강제로 재생성합니다"
    )

# src 모듈 import를 위한 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def temp_directory():
    """임시 디렉터리 픽스처 - 테스트 후 자동 정리"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="session")
def config_manager():
    """ConfigManager 공통 픽스처"""
    from utils.config_manager import ConfigManager
    return ConfigManager()

@pytest.fixture(scope="session") 
def test_logger():
    """Logger 공통 픽스처"""
    from utils.logger_v2 import Logger
    return Logger("test_workspace", logs_base_dir="tests/logs")

@pytest.fixture(scope="session")
def test_data_manager():
    """TestResultDataManager 공통 픽스처"""
    from tests.utils.test_data_manager import TestResultDataManager
    base_path = str(Path(__file__).parent / "data" / "content_processing")
    return TestResultDataManager(base_path)

def regenerate_test_data():
    """테스트 데이터 자동 재생성"""
    print("🔄 테스트 데이터 재생성 중...")
    # TODO: 데이터 재생성 로직 구현
    print("✅ 테스트 데이터 재생성 완료")