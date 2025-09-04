# 생성 시간: Thu Sep  4 09:30:22 KST 2025
# 핵심 내용: ResultLogger를 활용한 장 추출 결과 저장 통합 테스트
# 상세 내용:
#   - TestChapterExtractionWithResultLogger (라인 17-85): ResultLogger 통합 사용 테스트 클래스
#   - test_save_chapter_1_toc_and_content (라인 22-60): 1장 목차(JSON)와 내용(MD) 저장 테스트
#   - test_save_multiple_chapters_results (라인 62-85): 여러 장 결과 저장 및 조회 테스트
# 상태: active
# 참조: TDD 기반 ResultLogger 구현 완료 후 통합 테스트

import pytest
import sys
import json
from pathlib import Path
from datetime import datetime

# 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory

@pytest.mark.integration
class TestChapterExtractionWithResultLogger:
    """
    ResultLogger를 활용한 장 추출 결과 저장 통합 테스트
    - 실제 워크플로우에서 결과 저장 기능 검증
    - 장 목차는 JSON, 장 내용은 마크다운으로 저장하는 실제 시나리오
    """
    
    def test_save_chapter_1_toc_and_content(self, temp_directory):
        """
        요구사항: 1장 목차와 내용을 각각 JSON과 마크다운 형식으로 저장
        - 장 목차: JSON 형식으로 구조화된 데이터 저장
        - 장 내용: 마크다운 형식으로 읽기 쉬운 문서 저장
        """
        # Given: 1장 추출 결과 데이터 (예시)
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("dop_book_extraction", temp_directory)
        
        # 1장 목차 데이터 (JSON으로 저장)
        chapter1_toc = {
            "chapter_info": {
                "number": 1,
                "title": "Complexity of object-oriented programming",
                "start_page": 25,
                "end_page": 68
            },
            "sections": [
                {
                    "id": 5,
                    "title": "1.1 Introduction",
                    "level": 1,
                    "page": 25,
                    "children_ids": [6, 11]
                },
                {
                    "id": 6,
                    "title": "1.1.1 The design phase",
                    "level": 2, 
                    "page": 26,
                    "children_ids": []
                },
                {
                    "id": 11,
                    "title": "1.2 Introduction",
                    "level": 1,
                    "page": 35,
                    "children_ids": [12, 13, 14, 15]
                }
            ],
            "extraction_metadata": {
                "extracted_at": "2025-09-04 09:30:22",
                "extraction_method": "AI-enhanced PDF processing",
                "total_sections": 3
            }
        }
        
        # 1장 내용 데이터 (마크다운으로 저장)
        chapter1_content = """# 1장: Complexity of object-oriented programming

## 1.1 Introduction

객체지향 프로그래밍의 복잡성에 대한 소개입니다.

### 주요 내용
- 객체지향 프로그래밍의 한계점
- 복잡성이 발생하는 이유
- 데이터 지향 프로그래밍과의 차이점

## 1.1.1 The design phase

설계 단계에서 발생하는 주요 이슈들:

1. **클래스 계층구조의 복잡성**
   - 상속 관계의 깊이
   - 다중 상속 문제

2. **의존성 관리**
   - 객체 간 결합도
   - 순환 의존성 문제

## 1.2 Introduction

두 번째 섹션의 소개 내용...

### 핵심 개념
- 캡슐화의 한계
- 다형성의 오버헤드
- 코드 재사용성 문제

---
**추출 정보:**
- 페이지 범위: 25-68
- 추출 일시: 2025-09-04 09:30:22
- 총 섹션 수: 3개
"""
        
        # When: 장 목차를 JSON으로, 장 내용을 마크다운으로 저장
        toc_path = result_logger.save_result("chapter_1_toc", chapter1_toc, format="json")
        content_path = result_logger.save_result("chapter_1_content", chapter1_content, format="md")
        
        # Then: 파일들이 정상적으로 저장되고 내용 검증
        assert toc_path.exists(), "장 목차 JSON 파일이 생성되어야 함"
        assert content_path.exists(), "장 내용 마크다운 파일이 생성되어야 함"
        
        # JSON 파일 검증
        assert toc_path.suffix == ".json"
        with open(toc_path, 'r', encoding='utf-8') as f:
            saved_toc = json.load(f)
        assert saved_toc["chapter_info"]["title"] == "Complexity of object-oriented programming"
        assert saved_toc["chapter_info"]["number"] == 1
        assert len(saved_toc["sections"]) == 3
        
        # 마크다운 파일 검증
        assert content_path.suffix == ".md"
        with open(content_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert "# 1장: Complexity of object-oriented programming" in saved_content
        assert "## 1.1 Introduction" in saved_content
        assert "객체지향 프로그래밍의 복잡성" in saved_content

    def test_save_multiple_chapters_results(self, temp_directory):
        """
        요구사항: 여러 장의 결과를 저장하고 저장된 결과 목록 조회
        - 실제 워크플로우에서 여러 장을 처리한 후 결과 확인
        """
        # Given: 여러 장 처리 결과
        config_manager = ConfigManager()
        logger_factory = LoggerFactory(config_manager)
        result_logger = logger_factory.create_result_logger("multi_chapter_test", temp_directory)
        
        # When: 여러 장의 결과를 다양한 형식으로 저장
        result_logger.save_result("chapter_2_toc", {"chapter": 2, "sections": 5}, format="json")
        result_logger.save_result("chapter_3_summary", "# 3장 요약\n\n주요 내용...", format="md")
        result_logger.save_result("processing_log", "Chapter processing completed successfully.", format="txt")
        
        # Then: 저장된 결과 목록 확인
        results = result_logger.list_results()
        
        assert len(results) >= 3, "최소 3개 파일이 저장되어야 함"
        
        # 형식별 파일 확인
        formats = [r["format"] for r in results]
        assert "json" in formats, "JSON 파일이 있어야 함"
        assert "md" in formats, "마크다운 파일이 있어야 함"
        assert "txt" in formats, "텍스트 파일이 있어야 함"
        
        # 파일명에 타임스탬프가 포함되어 중복 방지 확인
        names = [r["name"] for r in results]
        assert len(names) == len(set(names)), "모든 파일명이 고유해야 함"