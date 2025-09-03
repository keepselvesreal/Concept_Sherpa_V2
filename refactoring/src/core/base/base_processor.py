# 생성 시간: Mon Sep  3 17:01:10 KST 2025
# 핵심 내용: 모든 프로세서의 기본 추상 클래스 (공통 인터페이스 제공)
# 상세 내용:
#   - BaseProcessor (라인 13-61): 추상 기본 프로세서 클래스
#   - __init__ (라인 18-25): 설정과 로거 초기화
#   - process (라인 27-35): 추상 메서드 - 각 단계에서 구현 필요
#   - validate_input (라인 37-44): 입력 검증 (하위 클래스에서 오버라이드)
#   - handle_error (라인 46-52): 에러 처리 공통 로직
#   - log_step (라인 54-61): 단계별 로그 기록
# 상태: active

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime

class BaseProcessor(ABC):
    """모든 프로세서의 기본 추상 클래스"""
    
    def __init__(self, config_manager, logger_factory, stage_name: str):
        """
        Args:
            config_manager: 설정 관리자
            logger_factory: 로거 팩토리
            stage_name: 단계 이름
        """
        self.config_manager = config_manager
        self.logger_factory = logger_factory
        self.stage_name = stage_name
        self.logger = None  # 하위 클래스에서 설정
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        메인 처리 로직 (하위 클래스에서 구현 필요)
        
        Args:
            input_data: 입력 데이터
            
        Returns:
            Dict[str, Any]: 처리 결과
        """
        pass
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        입력 데이터 검증 (하위 클래스에서 오버라이드 가능)
        
        Args:
            input_data: 검증할 입력 데이터
            
        Returns:
            bool: 유효성 검증 결과
        """
        return input_data is not None
        
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        에러 처리 공통 로직
        
        Args:
            error: 발생한 예외
            context: 에러 발생 컨텍스트
            
        Returns:
            Dict[str, Any]: 에러 결과
        """
        error_msg = f"{self.stage_name} 실패"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        
        if self.logger:
            self.logger.error(error_msg)
        else:
            print(f"❌ {error_msg}")
            
        return {
            'success': False,
            'error': error_msg,
            'stage': self.stage_name,
            'timestamp': datetime.now().isoformat()
        }
        
    def log_step(self, message: str, level: str = "info"):
        """단계별 로그 기록"""
        if self.logger:
            getattr(self.logger, level.lower())(f"[{self.stage_name}] {message}")
        else:
            print(f"[{self.stage_name}] {message}")