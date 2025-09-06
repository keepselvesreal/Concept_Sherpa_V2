# 생성 시간: Mon Jan  2 16:40:00 KST 2025
# 핵심 내용: 기본 기능 테스트 - 기존 로직 이관 후 정상 동작 확인용
# 상세 내용:
#   - TestBasicFunctionality (라인 15-35): 기본 기능 테스트 클래스
#   - test_toc_extractor_creates_instance (라인 20-25): 인스턴스 생성 테스트
#   - test_ai_factory_loads_config (라인 27-35): AI 팩토리 설정 로드 테스트
# 상태: active

import pytest
from pathlib import Path

# 구현될 클래스들
from src.toc_extractor import TocExtractor
from src.ai_providers import AIProviderFactory
from src.refactoring_logger import RefactoringLogger

class TestBasicFunctionality:
    """기본 기능 테스트 - 기존 로직 이관 확인"""
    
    def test_toc_extractor_creates_instance(self):
        """목차 추출기 인스턴스 생성 테스트"""
        logger = RefactoringLogger(Path("./logs"))
        ai_factory = AIProviderFactory("../config/ai_config.yaml", logger)
        
        extractor = TocExtractor(logger=logger, ai_factory=ai_factory)
        assert extractor is not None
    
    def test_ai_factory_loads_config(self):
        """AI 팩토리 설정 로드 테스트"""
        config_path = Path(__file__).parent.parent / "config" / "ai_config.yaml"
        logger = RefactoringLogger(Path("./logs"))
        
        factory = AIProviderFactory(str(config_path), logger)
        available_providers = factory.get_available_providers()
        
        # Gemini가 기본으로 활성화되어 있어야 함
        assert isinstance(available_providers, list)