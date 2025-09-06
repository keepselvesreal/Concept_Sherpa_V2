# 생성 시간: Tue Sep  2 14:57:29 KST 2025
# 핵심 내용: pytest 테스트 설정 및 공통 픽스처 정의
# 상세 내용:
#   - pytest_configure (라인 15-19): pytest 실행 전 설정
#   - test_environment fixture (라인 21-35): 테스트 환경 설정 픽스처
#   - cleanup_test_files fixture (라인 37-50): 테스트 후 정리 픽스처
# 상태: active
# 주소: conftest
# 참조: -

import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def pytest_configure(config):
    """pytest 실행 전 설정"""
    # 테스트용 환경변수 설정
    os.environ['PYTEST_RUNNING'] = 'true'

@pytest.fixture
def test_environment():
    """테스트 환경 설정"""
    test_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/tests")
    
    # 기본 경로 정보
    env_info = {
        'test_dir': test_dir,
        'config_path': test_dir / "test_extraction_config.yaml",
        'fixtures_dir': test_dir / "fixtures",
        'logs_dir': test_dir / "logs"
    }
    
    # 필수 디렉토리 생성
    for path in env_info.values():
        if isinstance(path, Path) and path.name != path.name.split('.')[0]:  # 파일이 아닌 경우
            continue
        if isinstance(path, Path):
            path.mkdir(parents=True, exist_ok=True)
    
    return env_info

@pytest.fixture(scope="function", autouse=True)
def cleanup_test_files():
    """테스트 후 임시 파일 정리"""
    yield
    
    # 테스트 후 정리 작업
    test_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/tests")
    
    # 임시 설정 파일들 정리
    temp_configs = list(test_dir.glob("**/temp_config_*.yaml"))
    for config_file in temp_configs:
        try:
            config_file.unlink()
        except:
            pass  # 이미 삭제되었거나 권한 문제 무시