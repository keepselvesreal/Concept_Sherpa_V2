# 생성 시간: Mon Sep  3 17:06:15 KST 2025
# 핵심 내용: AI 서비스 독립적 설정 및 처리 (각 스크립트마다 다른 AI 도구 설정 가능)
# 상세 내용:
#   - AIProvider (라인 15-25): AI 제공자 추상 클래스
#   - GeminiProvider (라인 27-61): Gemini AI 제공자 구현
#   - AIService (라인 63-121): AI 서비스 메인 클래스
#   - get_provider (라인 73-84): 설정에 따른 AI 제공자 선택
#   - analyze_chapters (라인 86-104): 장 분석 AI 처리
#   - process_content (라인 106-121): 콘텐츠 처리 AI 호출
# 상태: active

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class AIProvider(ABC):
    """AI 제공자 추상 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    async def analyze_chapters(self, toc_data: Dict[str, Any]) -> Dict[str, Any]:
        """장 분석 처리"""
        pass
        
    @abstractmethod
    async def process_content(self, content: str, task_type: str) -> Dict[str, Any]:
        """콘텐츠 처리"""
        pass

class GeminiProvider(AIProvider):
    """Gemini AI 제공자"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        
        # API 키 설정
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API 키가 설정되지 않았습니다")
            
        # 모델 설정
        self.model_name = self.config.get("model", "gemini-1.5-flash")
        self.temperature = self.config.get("temperature", 0.1)
        self.max_tokens = self.config.get("max_tokens", 8192)
        
        self.logger.info(f"Gemini AI 제공자 초기화: {self.model_name}")
        
    async def analyze_chapters(self, toc_data: Dict[str, Any]) -> Dict[str, Any]:
        """장 분석 처리 (기존 count_chapters_with_ai 로직 이관)"""
        try:
            # 기존 25-08-31의 extract_chapters_v5.py 로직 활용
            # 실제 구현은 기존 코드를 이곳으로 이관
            self.logger.info("Gemini를 사용한 장 분석 시작")
            
            # TODO: 기존 count_chapters_with_ai 함수 로직을 여기로 이관
            # 임시로 기본 구조만 반환
            return {
                'success': True,
                'chapters_info': [],  # 실제 구현에서는 분석된 장 정보
                'provider': 'gemini'
            }
            
        except Exception as e:
            self.logger.error(f"Gemini 장 분석 실패: {e}")
            return {'success': False, 'error': str(e), 'provider': 'gemini'}
            
    async def process_content(self, content: str, task_type: str) -> Dict[str, Any]:
        """콘텐츠 처리"""
        try:
            self.logger.info(f"Gemini 콘텐츠 처리 시작: {task_type}")
            
            # TODO: 각 task_type에 따른 처리 로직 구현
            # 예: content_analysis, node_extraction, toc_generation 등
            
            return {
                'success': True,
                'processed_content': content,  # 실제 처리 결과
                'task_type': task_type,
                'provider': 'gemini'
            }
            
        except Exception as e:
            self.logger.error(f"Gemini 콘텐츠 처리 실패: {e}")
            return {'success': False, 'error': str(e), 'provider': 'gemini'}

class AIService:
    """AI 서비스 메인 클래스 - 각 스크립트마다 다른 설정 가능"""
    
    def __init__(self, config_manager, logger: logging.Logger, stage_name: str = "default"):
        """
        Args:
            config_manager: 설정 관리자
            logger: 로거
            stage_name: 단계 이름 (각 단계마다 다른 AI 설정 사용 가능)
        """
        self.config_manager = config_manager
        self.logger = logger
        self.stage_name = stage_name
        self.provider = self._get_provider()
        
    def _get_provider(self) -> AIProvider:
        """설정에 따른 AI 제공자 선택"""
        # 단계별 AI 설정 (stage_specific_ai.{stage_name} 형태)
        stage_ai_config = self.config_manager.get(f"stage_specific_ai.{self.stage_name}", config_type="ai")
        
        # 전역 AI 설정 fallback (default_ai)
        if not stage_ai_config:
            stage_ai_config = self.config_manager.get("default_ai", config_type="ai")
        
        # 설정이 여전히 없으면 기본값 사용
        if not stage_ai_config:
            stage_ai_config = {
                "provider": "gemini",
                "model": "gemini-1.5-flash", 
                "temperature": 0.1,
                "max_tokens": 8192
            }
            self.logger.warning(f"AI 설정을 찾을 수 없어 기본값 사용: {self.stage_name}")
            
        provider_type = stage_ai_config.get("provider", "gemini").lower()
        
        if provider_type == "gemini":
            return GeminiProvider(stage_ai_config, self.logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공자: {provider_type}")
            
    async def analyze_chapters(self, toc_data: Dict[str, Any]) -> Dict[str, Any]:
        """장 분석 처리"""
        self.logger.info(f"[{self.stage_name}] AI 장 분석 시작")
        return await self.provider.analyze_chapters(toc_data)
        
    async def process_content(self, content: str, task_type: str) -> Dict[str, Any]:
        """콘텐츠 처리 (각 단계에서 다른 AI 설정으로 호출 가능)"""
        self.logger.info(f"[{self.stage_name}] AI 콘텐츠 처리: {task_type}")
        return await self.provider.process_content(content, task_type)
    
    def get_config_summary(self) -> Dict[str, Any]:
        """현재 AI 설정 요약 반환 (디버깅용)"""
        return {
            'stage_name': self.stage_name,
            'provider_type': type(self.provider).__name__,
            'config': self.provider.config
        }