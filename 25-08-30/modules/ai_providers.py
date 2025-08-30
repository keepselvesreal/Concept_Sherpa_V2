# 생성 시간: 2025-08-30 16:58:49 KST
# 핵심 내용: AI 프로바이더 추상화 팩토리 클래스 - 다중 AI 서비스 지원
# 상세 내용:
#   - AIProviderFactory (40-75): 메인 팩토리 클래스 및 프로바이더 설정
#   - _setup_gemini (77-85): Gemini API 설정 및 인증
#   - _setup_claude (87-92): Claude SDK 설정
#   - _setup_openai (94-102): OpenAI API 설정 및 인증
#   - generate_content (104-118): 통합 콘텐츠 생성 인터페이스
#   - _generate_gemini (120-135): Gemini 전용 생성 로직
#   - _generate_claude (137-150): Claude 전용 생성 로직
#   - _generate_openai (152-170): OpenAI 전용 생성 로직
# 상태: active
# 주소: ai_providers
# 참조: unified_node_processor_v3.py

import logging
import os
from typing import Dict, Any, Tuple

from core import UpdateLogEntry

# .env 파일 로딩
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv가 없으면 무시

# AI 프로바이더 임포트 (조건부)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from claude_code_sdk import query as claude_query, ClaudeCodeOptions
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class UpdateLogger:
    """업데이트 로그 관리 (임시 - managers 모듈로 이동 예정)"""
    pass  # 임시로 빈 클래스


class AIProviderFactory:
    """AI 프로바이더 추상화 팩토리"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        
        # AI 프로바이더 설정
        provider_config = config.get('ai_provider', {})
        if isinstance(provider_config, str):
            # 기존 방식 (문자열)
            self.provider_type = provider_config
            self.model_config = config.get('providers', {})
        else:
            # 새로운 방식 (딕셔너리)
            self.provider_type = provider_config.get('type', 'gemini')
            self.model_config = config.get('models', {})
        
        self._setup_provider()
    
    def _setup_provider(self):
        """프로바이더 설정"""
        if self.provider_type == 'gemini':
            self._setup_gemini()
        elif self.provider_type == 'claude':
            self._setup_claude()
        elif self.provider_type == 'openai':
            self._setup_openai()
    
    def _setup_gemini(self):
        """Gemini 설정"""
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai 패키지가 필요합니다")
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 필요합니다")
        
        genai.configure(api_key=api_key)
    
    def _setup_claude(self):
        """Claude 설정"""
        if not CLAUDE_AVAILABLE:
            raise ImportError("claude_code_sdk 패키지가 필요합니다")
    
    def _setup_openai(self):
        """OpenAI 설정"""
        if not OPENAI_AVAILABLE:
            raise ImportError("openai 패키지가 필요합니다")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 필요합니다")
        
        openai.api_key = api_key
    
    async def generate_content(self, prompt: str, system_prompt: str = "", 
                             update_logger: UpdateLogger = None) -> Tuple[str, int, int]:
        """내용 생성"""
        try:
            if self.provider_type == 'gemini':
                return await self._generate_gemini(prompt, system_prompt)
            elif self.provider_type == 'claude':
                return await self._generate_claude(prompt, system_prompt)
            elif self.provider_type == 'openai':
                return await self._generate_openai(prompt, system_prompt)
            else:
                raise ValueError(f"지원되지 않는 프로바이더: {self.provider_type}")
        except Exception as e:
            self.logger.error(f"내용 생성 실패 ({self.provider_type}): {e}")
            return "", 0, 0
    
    async def _generate_gemini(self, prompt: str, system_prompt: str = "") -> Tuple[str, int, int]:
        """Gemini로 내용 생성"""
        try:
            model_name = self.model_config.get('gemini', 'gemini-2.0-flash-exp')
            model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
            
            response = await model.generate_content_async(prompt)
            
            # 토큰 사용량 추정 (Gemini는 정확한 토큰 카운트를 제공하지 않음)
            prompt_tokens = len(prompt.split()) + len(system_prompt.split())
            response_tokens = len(response.text.split()) if response.text else 0
            
            return response.text, prompt_tokens, response_tokens
        except Exception as e:
            self.logger.error(f"Gemini 생성 실패: {e}")
            return "", 0, 0
    
    async def _generate_claude(self, prompt: str, system_prompt: str = "") -> Tuple[str, int, int]:
        """Claude로 내용 생성"""
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            options = ClaudeCodeOptions()
            response = await claude_query(full_prompt, options)
            
            # 토큰 사용량 추정
            prompt_tokens = len(full_prompt.split())
            response_tokens = len(response.split()) if response else 0
            
            return response, prompt_tokens, response_tokens
        except Exception as e:
            self.logger.error(f"Claude 생성 실패: {e}")
            return "", 0, 0
    
    async def _generate_openai(self, prompt: str, system_prompt: str = "") -> Tuple[str, int, int]:
        """OpenAI로 내용 생성"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            model_name = self.model_config.get('openai', 'gpt-4')
            response = await openai.ChatCompletion.acreate(
                model=model_name,
                messages=messages
            )
            
            content = response.choices[0].message.content
            prompt_tokens = response.usage.prompt_tokens
            response_tokens = response.usage.completion_tokens
            
            return content, prompt_tokens, response_tokens
        except Exception as e:
            self.logger.error(f"OpenAI 생성 실패: {e}")
            return "", 0, 0