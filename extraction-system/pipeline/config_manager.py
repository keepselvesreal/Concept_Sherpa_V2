# 생성 시간: 2025-09-01 14:15:42 KST
# 핵심 내용: extraction_config.yaml 구조에 맞는 책 파이프라인 전용 설정 관리자
# 상세 내용:
#   - ConfigManager 클래스 (라인 25-150): extraction_config.yaml 전용 설정 관리
#     - __init__ (라인 30-40): 설정 파일 경로 초기화 및 로드
#     - load_config (라인 42-60): YAML 설정 파일 로드 및 검증
#     - get_book_pipeline_config (라인 62-75): 책 파이프라인 설정 조회
#     - get_content_analyzer_config (라인 77-90): 콘텐츠 분석기 설정 조회
#     - get_content_extractor_config (라인 92-105): 콘텐츠 추출기 설정 조회
#     - get_ai_provider_config (라인 107-125): AI 제공자별 모델 설정 조회
#     - create_ai_provider (라인 127-150): AI 제공자 인스턴스 생성
# 상태: active
# 참조: extraction_config.yaml, content_node_extractor_v3.py

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# AI 제공자 클래스들 (기존과 동일)
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """AI 제공자 추상 베이스 클래스"""
    
    @abstractmethod
    async def query(self, prompt: str) -> str:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class GeminiAPIProvider(AIProvider):
    """Gemini API 구현체 (모델 선택 가능)"""
    
    def __init__(self, model="gemini-2.0-flash-exp", logger=None):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = model
        self.logger = logger
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다")
    
    async def query(self, prompt: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            return response_text
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Gemini API ({self.model}) 실행 실패: {str(e)}")
            else:
                print(f"Gemini API ({self.model}) 실행 실패: {str(e)}")
            raise

    def get_name(self) -> str:
        return f"Gemini API ({self.model})"

class ClaudeSDKProvider(AIProvider):
    """Claude SDK 구현체 (content_node_extractor_v3.py와 동일한 로직)"""
    
    def __init__(self, logger=None):
        # Max Plan 사용자는 Claude Code CLI 기반 인증 사용
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
        self.logger = logger
    
    async def query(self, prompt: str) -> str:
        try:
            from claude_code_sdk import query as claude_query
            
            responses = []
            async for message in claude_query(prompt=prompt):
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                    elif hasattr(content, 'text'):
                        responses.append(content.text)
            
            response_text = '\n'.join(responses) if responses else ''
            return response_text
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Claude SDK 실행 실패: {str(e)}")
            else:
                print(f"Claude SDK 실행 실패: {str(e)}")
            raise

    def get_name(self) -> str:
        return "Claude SDK"

class ConfigManager:
    """extraction_config.yaml 전용 설정 관리자"""
    
    def __init__(self, config_path: str = "extraction_config.yaml"):
        """설정 관리자 초기화"""
        self.config_path = Path(config_path)
        self.config = None
        self.load_config()
    
    def load_config(self) -> None:
        """YAML 설정 파일을 로드"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            print(f"✅ 설정 파일 로드 완료: {self.config_path}")
            
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 파일 파싱 오류: {e}")
        except Exception as e:
            raise RuntimeError(f"설정 파일 로드 실패: {e}")
    
    def get_book_pipeline_config(self, stage: str) -> Dict[str, Any]:
        """책 파이프라인의 특정 단계 설정 조회"""
        book_config = self.config.get('book_pipeline', {})
        stage_config = book_config.get(stage, {})
        
        # 기본값 설정
        defaults = {
            'ai_provider': 'gemini',
            'model': 'gemini-2.0-flash-lite',
            'temperature': 0.5,
            'max_retries': 2
        }
        
        return {**defaults, **stage_config}
    
    def get_content_analyzer_config(self) -> Dict[str, Any]:
        """콘텐츠 노드 분석기 설정 조회"""
        return self.get_book_pipeline_config('content_node_analyzer')
    
    def get_content_extractor_config(self) -> Dict[str, Any]:
        """콘텐츠 추출기 설정 조회"""
        return self.get_book_pipeline_config('content_extractor')
    
    def get_ai_provider_config(self, provider: str) -> Dict[str, Any]:
        """AI 제공자별 설정 조회"""
        providers = self.config.get('providers', {})
        provider_config = providers.get(provider, {})
        
        # 기본값 설정
        defaults = {
            'temperature': 0.7,
            'max_retries': 2
        }
        
        return {**defaults, **provider_config}
    
    def create_ai_provider(self, provider_type: str, model: str = None, logger=None) -> AIProvider:
        """설정에 따른 AI 제공자 생성"""
        if provider_type.lower() == "gemini":
            provider_config = self.get_ai_provider_config('gemini')
            
            # 모델 결정 (우선순위: 인자 > 설정 > 기본값)
            if model is None:
                model = provider_config.get('lite_model', 'gemini-2.0-flash-lite')
            
            return GeminiAPIProvider(model=model, logger=logger)
        elif provider_type.lower() == "claude":
            return ClaudeSDKProvider(logger=logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공업체: {provider_type}")
    
    def create_content_analyzer(self, logger=None):
        """콘텐츠 노드 분석기용 AI 제공자 생성"""
        config = self.get_content_analyzer_config()
        provider_type = config.get('ai_provider', 'claude')
        model = config.get('model', None)  # Claude SDK는 모델 지정 불필요
        
        return self.create_ai_provider(provider_type, model, logger)
    
    def create_content_node_analyzer(self, logger=None):
        """has_content 분석용 AI 제공자 생성 (content_node_extractor_v3.py 로직)"""
        config = self.get_content_analyzer_config()
        provider_type = config.get('ai_provider', 'claude')
        model = config.get('model', None)  # 모델 명시적 설정
        
        return self.create_ai_provider(provider_type, model, logger)
    
    def create_content_extractor(self, logger=None):
        """콘텐츠 추출기용 AI 제공자 생성"""
        config = self.get_content_extractor_config()
        provider_type = config.get('ai_provider', 'claude')
        model = config.get('model', None)  # Claude SDK는 모델 지정 불필요
        
        return self.create_ai_provider(provider_type, model, logger)