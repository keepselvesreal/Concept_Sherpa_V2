# 생성 시간: Mon Jan  2 16:30:00 KST 2025
# 핵심 내용: AI Provider 추상화 - Gemini, OpenAI, Claude SDK 통합 (로거 연동)
# 상세 내용:
#   - AIResponse (라인 17-25): AI 응답 통합 데이터 클래스
#   - AIProvider (라인 27-50): AI Provider 추상 기본 클래스 (로거 포함)
#   - GeminiProvider (라인 52-125): Gemini API Provider (로깅 연동)
#   - OpenAIProvider (라인 127-200): OpenAI API Provider (로깅 연동)
#   - ClaudeSDKProvider (라인 202-245): Claude SDK Provider (로깅 연동)
#   - AIProviderFactory (라인 247-290): Provider 팩토리 클래스 (로깅 포함)
# 상태: active

import os
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path
from dotenv import load_dotenv
from refactoring_logger import RefactoringLogger, RefactoringLogContext

@dataclass
class AIResponse:
    """AI 응답 통합 데이터 클래스"""
    text: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = None

class AIProvider(ABC):
    """AI Provider 추상 기본 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[RefactoringLogger] = None):
        self.config = config
        self.model = config.get('default_model')
        self.logger = logger
    
    def _get_log_context(self, method_name: str) -> RefactoringLogContext:
        """로그 컨텍스트 생성"""
        return RefactoringLogContext(
            stage="ai_provider",
            class_name=self.__class__.__name__,
            method_name=method_name,
            operation_id=""
        )
    
    @abstractmethod
    async def generate_content(self, prompt: str, **kwargs) -> AIResponse:
        """콘텐츠 생성"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Provider 사용 가능 여부"""
        pass

class GeminiProvider(AIProvider):
    """Gemini API Provider"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[RefactoringLogger] = None):
        super().__init__(config, logger)
        self._client = None
        self._api_key = os.getenv(config.get('api_key_env', 'GEMINI_API_KEY'))
    
    def is_available(self) -> bool:
        """Gemini API 사용 가능 여부 확인"""
        return bool(self._api_key and self.config.get('enabled', False))
    
    async def generate_content(self, prompt: str, **kwargs) -> AIResponse:
        """Gemini API로 콘텐츠 생성"""
        context = self._get_log_context("generate_content")
        inputs = {
            "prompt_length": len(prompt),
            "model": self.model,
            "kwargs": kwargs
        }
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            if not self.is_available():
                raise RuntimeError("Gemini Provider not available")
            
            # Gemini 클라이언트 lazy 초기화
            if not self._client:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=self._api_key)
                    self._client = genai.GenerativeModel(self.model)
                except ImportError as e:
                    if self.logger:
                        self.logger.operation_error(context, e, inputs)
                    raise RuntimeError("google-generativeai not installed")
            
            # 모델 설정 적용
            model_config = kwargs.get('model_config', {})
            generation_config = {
                'temperature': model_config.get('temperature', 0.1),
                'max_output_tokens': model_config.get('max_tokens', 8192),
            }
            
            # API 호출
            response = await asyncio.to_thread(
                self._client.generate_content,
                prompt,
                generation_config=generation_config
            )
            
            # tokens_used 안전하게 추출
            tokens_used = None
            try:
                if hasattr(response, 'usage_metadata'):
                    usage = getattr(response, 'usage_metadata')
                    if hasattr(usage, 'total_token_count'):
                        tokens_used = usage.total_token_count
            except Exception:
                tokens_used = None
            
            ai_response = AIResponse(
                text=response.text,
                model=self.model,
                provider="gemini",
                tokens_used=tokens_used,
                finish_reason=getattr(response, 'finish_reason', None),
                metadata={'raw_response': response}
            )
            
            outputs = {
                "success": True,
                "response_length": len(ai_response.text),
                "tokens_used": ai_response.tokens_used,
                "finish_reason": ai_response.finish_reason
            }
            
            if self.logger:
                self.logger.operation_success(context, outputs)
            
            return ai_response
            
        except Exception as e:
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            raise RuntimeError(f"Gemini API error: {str(e)}")

class OpenAIProvider(AIProvider):
    """OpenAI API Provider"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[RefactoringLogger] = None):
        super().__init__(config, logger)
        self._client = None
        self._api_key = os.getenv(config.get('api_key_env', 'OPENAI_API_KEY'))
    
    def is_available(self) -> bool:
        """OpenAI API 사용 가능 여부 확인"""
        return bool(self._api_key and self.config.get('enabled', False))
    
    async def generate_content(self, prompt: str, **kwargs) -> AIResponse:
        """OpenAI API로 콘텐츠 생성"""
        context = self._get_log_context("generate_content")
        inputs = {
            "prompt_length": len(prompt),
            "model": self.model,
            "kwargs": kwargs
        }
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            if not self.is_available():
                raise RuntimeError("OpenAI Provider not available")
            
            # OpenAI 클라이언트 lazy 초기화
            if not self._client:
                try:
                    from openai import AsyncOpenAI
                    self._client = AsyncOpenAI(api_key=self._api_key)
                except ImportError as e:
                    if self.logger:
                        self.logger.operation_error(context, e, inputs)
                    raise RuntimeError("openai not installed")
            
            # 모델 설정 적용
            model_config = kwargs.get('model_config', {})
            
            # API 호출
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=model_config.get('temperature', 0.1),
                max_tokens=model_config.get('max_tokens', 4096)
            )
            
            ai_response = AIResponse(
                text=response.choices[0].message.content,
                model=self.model,
                provider="openai",
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
                metadata={'raw_response': response}
            )
            
            outputs = {
                "success": True,
                "response_length": len(ai_response.text),
                "tokens_used": ai_response.tokens_used,
                "finish_reason": ai_response.finish_reason
            }
            
            if self.logger:
                self.logger.operation_success(context, outputs)
            
            return ai_response
            
        except Exception as e:
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            raise RuntimeError(f"OpenAI API error: {str(e)}")

class ClaudeSDKProvider(AIProvider):
    """Claude SDK Provider (API와 분리된 SDK 사용)"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[RefactoringLogger] = None):
        super().__init__(config, logger)
        self._client = None
    
    def is_available(self) -> bool:
        """Claude SDK 사용 가능 여부 확인"""
        return self.config.get('enabled', False)
    
    async def generate_content(self, prompt: str, **kwargs) -> AIResponse:
        """Claude SDK로 콘텐츠 생성"""
        context = self._get_log_context("generate_content")
        inputs = {
            "prompt_length": len(prompt),
            "model": self.model,
            "kwargs": kwargs
        }
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            if not self.is_available():
                error = RuntimeError("Claude SDK Provider not available")
                if self.logger:
                    self.logger.operation_error(context, error, inputs)
                raise error
            
            # Claude SDK 클라이언트 lazy 초기화
            if not self._client:
                try:
                    # Claude SDK 임포트 (실제 구현 시 수정 필요)
                    # import claude_sdk
                    # self._client = claude_sdk.Client()
                    error = NotImplementedError("Claude SDK integration not implemented yet")
                    if self.logger:
                        self.logger.operation_error(context, error, inputs)
                    raise error
                except ImportError as e:
                    if self.logger:
                        self.logger.operation_error(context, e, inputs)
                    raise RuntimeError("Claude SDK not available")
            
            # 실제 구현 시 Claude SDK API 호출
            error = NotImplementedError("Claude SDK integration not implemented yet")
            if self.logger:
                self.logger.operation_error(context, error, inputs)
            raise error
            
        except Exception as e:
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            raise

class AIProviderFactory:
    """AI Provider 팩토리"""
    
    def __init__(self, config_path: str, logger: Optional[RefactoringLogger] = None):
        # 기존 .env 파일 로드 (프로젝트 루트에서)
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        load_dotenv(env_path)
        
        self.config_path = Path(config_path)
        self.logger = logger
        self._config = None
        self._providers = {}
    
    def _get_log_context(self, method_name: str) -> RefactoringLogContext:
        """로그 컨텍스트 생성"""
        return RefactoringLogContext(
            stage="ai_factory",
            class_name=self.__class__.__name__,
            method_name=method_name,
            operation_id=""
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        if self._config is None:
            context = self._get_log_context("_load_config")
            inputs = {"config_path": str(self.config_path)}
            
            if self.logger:
                self.logger.operation_start(context, inputs)
            
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f)
                
                outputs = {
                    "success": True,
                    "providers_count": len(self._config.get('ai_providers', {}))
                }
                
                if self.logger:
                    self.logger.operation_success(context, outputs)
                    
            except Exception as e:
                if self.logger:
                    self.logger.operation_error(context, e, inputs)
                raise
                
        return self._config
    
    def get_provider(self, provider_name: Optional[str] = None) -> AIProvider:
        """Provider 인스턴스 반환"""
        context = self._get_log_context("get_provider")
        inputs = {"provider_name": provider_name}
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            config = self._load_config()
            
            # Provider 이름 결정
            if provider_name is None:
                provider_name = config.get('default_provider', 'gemini')
            
            # 캐시된 Provider 반환
            if provider_name in self._providers:
                outputs = {"success": True, "provider_name": provider_name, "cached": True}
                if self.logger:
                    self.logger.operation_success(context, outputs)
                return self._providers[provider_name]
            
            # Provider 생성
            provider_config = config['ai_providers'].get(provider_name)
            if not provider_config:
                error = ValueError(f"Unknown provider: {provider_name}")
                if self.logger:
                    self.logger.operation_error(context, error, inputs)
                raise error
            
            if provider_name == 'gemini':
                provider = GeminiProvider(provider_config, self.logger)
            elif provider_name == 'openai':
                provider = OpenAIProvider(provider_config, self.logger)
            elif provider_name == 'claude_sdk':
                provider = ClaudeSDKProvider(provider_config, self.logger)
            else:
                error = ValueError(f"Unsupported provider: {provider_name}")
                if self.logger:
                    self.logger.operation_error(context, error, inputs)
                raise error
            
            # 캐시에 저장
            self._providers[provider_name] = provider
            
            outputs = {
                "success": True, 
                "provider_name": provider_name, 
                "cached": False,
                "is_available": provider.is_available()
            }
            
            if self.logger:
                self.logger.operation_success(context, outputs)
            
            return provider
            
        except Exception as e:
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            raise
    
    def get_available_providers(self) -> List[str]:
        """사용 가능한 Provider 목록"""
        context = self._get_log_context("get_available_providers")
        inputs = {}
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            config = self._load_config()
            available = []
            
            for name, config_data in config['ai_providers'].items():
                try:
                    provider = self.get_provider(name)
                    if provider.is_available():
                        available.append(name)
                except Exception:
                    continue
            
            outputs = {"success": True, "available_providers": available}
            if self.logger:
                self.logger.operation_success(context, outputs)
            
            return available
            
        except Exception as e:
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            raise