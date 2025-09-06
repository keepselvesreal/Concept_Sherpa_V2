# 생성 시간: Thu Sep  4 16:01:00 KST 2025
# 핵심 내용: 통합 AI 서비스 (query 기반 + 추가 입력 데이터 지원)
# 상세 내용:
#   - AIProvider (라인 20-35): AI 제공자 추상 클래스 (query + 추가 데이터 지원)
#   - ClaudeSDKProvider (라인 37-90): Claude SDK 구현체
#   - GeminiProvider (라인 92-145): Gemini AI 구현체 (설정 파일 기반)
#   - AIService (라인 147-210): 통합 AI 서비스 클래스
#   - _get_provider (라인 160-180): 설정 기반 제공자 선택
#   - query (라인 182-195): 메인 쿼리 메서드 (추가 데이터 지원)
#   - get_name (라인 197-200): AI 제공자 이름 반환
# 상태: active
# 참조: ai_service.py, chapter_extraction_service.py AI 부분 통합

import os
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class AIProvider(ABC):
    """AI 제공자 추상 클래스 - query 기반 + 추가 입력 데이터 + 세션 관리 지원"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.sessions = {}  # 세션 ID별 대화 히스토리
    
    @abstractmethod
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        AI에 질의하고 응답을 반환
        
        Args:
            prompt: 질의 프롬프트
            additional_data: 추가 입력 데이터 (파일 경로, 구조화된 데이터 등)
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        pass
    
    def create_session(self) -> str:
        """새로운 대화 세션 생성"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'messages': [],
            'created_at': None,
            'last_used': None
        }
        self.logger.info(f"새 세션 생성: {session_id}")
        return session_id
    
    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """세션 대화 히스토리 조회"""
        return self.sessions.get(session_id, {}).get('messages', [])
    
    def add_to_session(self, session_id: str, prompt: str, response: str):
        """세션에 대화 추가"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {'messages': [], 'created_at': None, 'last_used': None}
        
        import time
        self.sessions[session_id]['messages'].append({
            'prompt': prompt,
            'response': response,
            'timestamp': time.time()
        })
        self.sessions[session_id]['last_used'] = time.time()
    
    async def query_with_session(self, prompt: str, session_id: str, 
                               additional_data: Optional[Dict[str, Any]] = None) -> str:
        """세션을 유지하면서 쿼리 실행"""
        # 기본 구현: 세션 히스토리를 포함한 프롬프트 구성
        session_history = self.get_session_history(session_id)
        
        if session_history:
            # 이전 대화 히스토리 포함
            history_prompt = "이전 대화:\n"
            for msg in session_history[-3:]:  # 최근 3개 대화만 포함
                history_prompt += f"사용자: {msg['prompt'][:200]}...\n"
                history_prompt += f"AI: {msg['response'][:200]}...\n\n"
            
            enhanced_prompt = f"{history_prompt}\n현재 질문: {prompt}"
        else:
            enhanced_prompt = prompt
        
        response = await self.query(enhanced_prompt, additional_data)
        self.add_to_session(session_id, prompt, response)
        
        return response

class ClaudeSDKProvider(AIProvider):
    """Claude SDK 구현체"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        # Max Plan 사용자는 Claude Code CLI 기반 인증 사용 - API 키 환경변수 제거
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
            self.logger.info("ANTHROPIC_API_KEY 환경변수 제거됨 - Claude Code CLI 인증 사용")
    
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Claude SDK를 사용한 AI 쿼리"""
        try:
            self.logger.info("Claude SDK 임포트 시도 중...")
            from claude_code_sdk import query as claude_query
            self.logger.info("Claude SDK 임포트 성공")
            
            # additional_data가 있으면 프롬프트에 포함
            enhanced_prompt = prompt
            if additional_data:
                context_parts = []
                for key, value in additional_data.items():
                    context_parts.append(f"{key}: {value}")
                if context_parts:
                    enhanced_prompt = f"{prompt}\n\n추가 정보:\n" + "\n".join(context_parts)
            
            self.logger.info("Claude SDK 쿼리 실행 중...")
            responses = []
            
            async for message in claude_query(prompt=enhanced_prompt):
                self.logger.info(f"메시지 타입: {type(message).__name__}")
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                                self.logger.info(f"응답 받음: {block.text[:100]}...")
                    elif hasattr(content, 'text'):
                        responses.append(content.text)
                        self.logger.info(f"응답 받음: {content.text[:100]}...")
            
            response_text = '\n'.join(responses) if responses else ''
            self.logger.info(f"Claude SDK 응답 길이: {len(response_text)} 문자")
            return response_text
            
        except Exception as e:
            error_msg = f"Claude SDK 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_name(self) -> str:
        return "Claude SDK"

class GeminiProvider(AIProvider):
    """Gemini AI 제공자 - 설정 파일 기반"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        
        # API 키 설정
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API 키가 설정되지 않았습니다 (GEMINI_API_KEY)")
            
        # 모델 설정 (설정 파일에서 읽음)
        self.model_name = self.config.get("model", "gemini-2.0-flash-lite")
        self.temperature = self.config.get("temperature", 0.1)
        self.max_tokens = self.config.get("max_tokens", 8192)
        
        self.logger.info(f"Gemini 설정: 모델={self.model_name}, 온도={self.temperature}")
    
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Gemini를 사용한 AI 쿼리"""
        try:
            import google.generativeai as genai
            
            # API 키 설정
            genai.configure(api_key=self.api_key)
            
            # 모델 생성 (설정 파일 기반)
            model = genai.GenerativeModel(self.model_name)
            
            # additional_data가 있으면 프롬프트에 포함
            enhanced_prompt = prompt
            if additional_data:
                context_parts = []
                for key, value in additional_data.items():
                    if isinstance(value, (dict, list)):
                        context_parts.append(f"{key}: {str(value)}")
                    else:
                        context_parts.append(f"{key}: {value}")
                if context_parts:
                    enhanced_prompt = f"{prompt}\n\n추가 정보:\n" + "\n".join(context_parts)
            
            self.logger.info(f"Gemini 쿼리 실행 중... (모델: {self.model_name})")
            
            # 응답 생성
            response = model.generate_content(
                enhanced_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            
            result = response.text if response.text else "응답이 비어있습니다"
            self.logger.info(f"Gemini 응답 길이: {len(result)} 문자")
            return result
            
        except Exception as e:
            error_msg = f"Gemini 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_name(self) -> str:
        return f"Gemini ({self.model_name})"

class AIService:
    """통합 AI 서비스 - 설정 기반 제공자 선택 + query 기반 인터페이스"""
    
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
        # 1. 단계별 하위 설정 먼저 확인 (예: workspace_preparation.chapter_toc_extraction)
        sub_stage_config = self.config_manager.get(f"stage_specific_ai.workspace_preparation.{self.stage_name}", config_type="ai")
        
        # 2. 단계별 설정 확인 (예: workspace_preparation)
        if not sub_stage_config:
            stage_config = self.config_manager.get(f"stage_specific_ai.{self.stage_name.split('.')[0]}", config_type="ai")
            sub_stage_config = stage_config
        
        # 3. 기본 설정 사용
        if not sub_stage_config:
            sub_stage_config = self.config_manager.get("default_ai", config_type="ai")
        
        # 4. 최종 fallback
        if not sub_stage_config:
            sub_stage_config = {
                "provider": "gemini",
                "model": "gemini-2.0-flash-lite", 
                "temperature": 0.1,
                "max_tokens": 8192
            }
            self.logger.warning(f"AI 설정을 찾을 수 없어 기본값 사용: {self.stage_name}")
            
        provider_type = sub_stage_config.get("provider", "gemini").lower()
        
        if provider_type == "claude":
            return ClaudeSDKProvider(sub_stage_config, self.logger)
        elif provider_type == "gemini":
            return GeminiProvider(sub_stage_config, self.logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공자: {provider_type}")
    
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        AI 쿼리 실행
        
        Args:
            prompt: 질의 프롬프트
            additional_data: 추가 입력 데이터 (파일 경로, TOC 데이터, 설정값 등)
        """
        try:
            self.logger.info(f"[{self.stage_name}] AI 쿼리 시작 - {self.provider.get_name()}")
            return await self.provider.query(prompt, additional_data)
        except Exception as e:
            error_msg = f"AI 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def create_session(self) -> str:
        """새로운 대화 세션 생성"""
        return self.provider.create_session()
    
    async def query_with_session(self, prompt: str, session_id: str, 
                               additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        세션을 유지하면서 AI 쿼리 실행
        
        Args:
            prompt: 질의 프롬프트
            session_id: 세션 ID
            additional_data: 추가 입력 데이터
        """
        try:
            self.logger.info(f"[{self.stage_name}] 세션 쿼리 시작 - {self.provider.get_name()} (세션: {session_id[:8]}...)")
            return await self.provider.query_with_session(prompt, session_id, additional_data)
        except Exception as e:
            error_msg = f"세션 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """세션 대화 히스토리 조회"""
        return self.provider.get_session_history(session_id)
    
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        return self.provider.get_name()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """현재 AI 설정 요약 반환 (디버깅용)"""
        return {
            'stage_name': self.stage_name,
            'provider_type': type(self.provider).__name__,
            'provider_name': self.provider.get_name(),
            'config': self.provider.config
        }