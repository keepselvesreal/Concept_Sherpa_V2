# 생성 시간: Thu Sep  4 09:30:22 KST 2025
# 핵심 내용: ResultLogger의 Social Unit 테스트 (일반적 결과 저장 기능 검증)
# 상세 내용:
#   - TestResultLoggerSocial (라인 18-120): ResultLogger의 사회적 단위 테스트 클래스
#   - test_save_as_json (라인 23-45): JSON 형식 저장 기능 테스트
#   - test_save_as_text (라인 47-65): 텍스트 형식 저장 기능 테스트
#   - test_save_as_markdown (라인 67-85): 마크다운 형식 저장 기능 테스트
#   - test_save_as_yaml (라인 87-105): YAML 형식 저장 기능 테스트
#   - test_list_saved_results (라인 107-120): 저장된 결과 목록 조회 테스트
# 상태: active
# 주소: tests/unit/social/test_result_logger_social
# 참조: TDD 기반 일반적 결과 저장 로거 요구사항 정의

import pytest
import sys
import json
from pathlib import Path
from datetime import datetime

# ResultLogger import를 위한 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory

@pytest.mark.social_unit
class TestResultLoggerSocial:
    """
    ResultLogger의 Social Unit 테스트
    - 실제 ConfigManager, LoggerFactory 사용
    - 일반적 데이터를 다양한 형식으로 저장
    - 간단한 메타데이터와 함께 결과 저장 및 조회
    """
    
    def test_save_as_json(self, temp_directory):
        """
        요구사항: ResultLogger.save_result()가 데이터를 JSON 형식으로 저장
        입력: 결과 이름 (str), 데이터 (Any), 형식='json'
        출력: JSON 파일 경로 (Path)
        """
        # Given: ResultLogger 인스턴스 생성
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("test_project", temp_directory)
        
        # When: JSON 형식으로 데이터 저장
        test_data = {
            "items_processed": 218,
            "success_rate": 0.95,
            "errors": ["error1", "error2"],
            "metadata": {"version": "1.0", "timestamp": "2025-09-04"}
        }
        
        saved_path = result_logger.save_result("test_analysis", test_data, format="json")
        
        # Then: JSON 파일 저장 및 내용 검증
        assert saved_path.exists(), "JSON 파일이 생성되어야 함"
        assert saved_path.suffix == ".json", "파일 확장자가 .json이어야 함"
        
        with open(saved_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == test_data, "저장된 데이터가 원본과 일치해야 함"

    def test_save_as_text(self, temp_directory):
        """
        요구사항: ResultLogger.save_result()가 데이터를 텍스트 형식으로 저장
        입력: 결과 이름 (str), 데이터 (str/dict), 형식='txt'
        출력: 텍스트 파일 경로 (Path)
        """
        # Given: 텍스트로 저장할 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("test_project", temp_directory)
        
        # When: 텍스트 형식으로 저장
        text_data = """처리 결과 요약:
- 전체 항목: 218개
- 성공률: 95%
- 처리 시간: 3.5초
- 상태: 완료"""
        
        saved_path = result_logger.save_result("processing_summary", text_data, format="txt")
        
        # Then: 텍스트 파일 검증
        assert saved_path.exists(), "텍스트 파일이 생성되어야 함"
        assert saved_path.suffix == ".txt", "파일 확장자가 .txt여야 함"
        
        with open(saved_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        
        assert text_data in saved_content, "원본 텍스트가 포함되어야 함"

    def test_save_as_markdown(self, temp_directory):
        """
        요구사항: ResultLogger.save_result()가 데이터를 마크다운 형식으로 저장
        입력: 결과 이름 (str), 데이터 (str), 형식='md'
        출력: 마크다운 파일 경로 (Path)
        """
        # Given: 마크다운 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("test_project", temp_directory)
        
        # When: 마크다운 형식으로 저장
        markdown_data = """# 분석 결과 보고서

## 개요
- **처리 일시**: 2025-09-04
- **처리 항목**: 218개

## 결과
| 항목 | 값 |
|------|-----|
| 성공 | 207개 |
| 실패 | 11개 |

## 결론
전체적으로 성공적인 처리 결과를 얻었습니다."""
        
        saved_path = result_logger.save_result("analysis_report", markdown_data, format="md")
        
        # Then: 마크다운 파일 검증
        assert saved_path.exists(), "마크다운 파일이 생성되어야 함"
        assert saved_path.suffix == ".md", "파일 확장자가 .md여야 함"
        
        with open(saved_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        
        assert "# 분석 결과 보고서" in saved_content, "마크다운 헤더가 포함되어야 함"
        assert "## 개요" in saved_content, "섹션이 보존되어야 함"

    def test_save_as_yaml(self, temp_directory):
        """
        요구사항: ResultLogger.save_result()가 데이터를 YAML 형식으로 저장
        입력: 결과 이름 (str), 데이터 (dict), 형식='yaml'
        출력: YAML 파일 경로 (Path)
        """
        # Given: YAML로 저장할 구조화된 데이터
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("test_project", temp_directory)
        
        # When: YAML 형식으로 저장
        yaml_data = {
            "processing_config": {
                "input_file": "test.pdf",
                "output_format": "json",
                "settings": {
                    "quality": "high",
                    "timeout": 300
                }
            },
            "results": {
                "items_processed": 218,
                "processing_time": 3.5,
                "errors": []
            }
        }
        
        saved_path = result_logger.save_result("config_and_results", yaml_data, format="yaml")
        
        # Then: YAML 파일 검증
        assert saved_path.exists(), "YAML 파일이 생성되어야 함"
        assert saved_path.suffix == ".yaml", "파일 확장자가 .yaml이어야 함"
        
        # YAML 파싱해서 데이터 검증
        import yaml
        with open(saved_path, 'r', encoding='utf-8') as f:
            loaded_data = yaml.safe_load(f)
        
        assert loaded_data == yaml_data, "저장된 YAML 데이터가 원본과 일치해야 함"
        assert loaded_data["processing_config"]["input_file"] == "test.pdf", "중첩 데이터 보존"

    def test_list_saved_results(self, temp_directory):
        """
        요구사항: ResultLogger.list_results()가 저장된 결과 파일들의 목록 반환
        입력: 없음
        출력: 저장된 결과 파일들의 정보 리스트
        """
        # Given: 여러 형식으로 저장된 결과들
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("test_project", temp_directory)
        
        # 다양한 형식으로 결과 저장
        result_logger.save_result("data1", {"test": "json"}, format="json")
        result_logger.save_result("data2", "텍스트 내용", format="txt")
        result_logger.save_result("data3", "# 마크다운", format="md")
        
        # When: 저장된 결과 목록 조회
        results_list = result_logger.list_results()
        
        # Then: 결과 목록 검증
        assert len(results_list) >= 3, "저장된 파일 개수가 일치해야 함"
        
        # 파일 형식별 확인
        formats_found = [result["format"] for result in results_list]
        assert "json" in formats_found, "JSON 파일이 목록에 있어야 함"
        assert "txt" in formats_found, "텍스트 파일이 목록에 있어야 함"
        assert "md" in formats_found, "마크다운 파일이 목록에 있어야 함"