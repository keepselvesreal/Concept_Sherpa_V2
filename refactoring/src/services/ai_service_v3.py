# 생성 시간: Thu Sep  4 17:15:30 KST 2025
# 핵심 내용: 통합 AI 서비스 (네이티브 세션 관리 지원)
# 상세 내용:
#   - SessionInfo (라인 23-35): 세션 상태 추상화 데이터 클래스
#   - AIProvider (라인 37-85): 네이티브 세션 지원 추상 클래스
#   - ClaudeSDKProvider (라인 87-180): Claude SDK 네이티브 세션 구현
#   - GeminiProvider (라인 182-275): Gemini Chat Session 구현  
#   - OpenAIProvider (라인 277-370): OpenAI Assistant Thread 구현
#   - AIService (라인 372-450): 통합 AI 서비스 클래스
# 상태: active
# 참조: ai_service_v2.py (네이티브 세션 관리로 개선)

import os
import logging
import uuid
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

@dataclass
class SessionInfo:
    """AI 제공자별 세션 정보를 담는 공통 데이터 클래스"""
    session_id: str
    provider_type: str
    native_session_data: Dict[str, Any] = field(default_factory=dict)  # 제공자별 네이티브 세션 정보
    created_at: Optional[float] = None
    last_used: Optional[float] = None
    message_count: int = 0
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
        self.last_used = time.time()
    
    def update_usage(self):
        """세션 사용 시간 업데이트"""
        self.last_used = time.time()
        self.message_count += 1

class AIProvider(ABC):
    """AI 제공자 추상 클래스 - 네이티브 세션 관리 지원"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.sessions: Dict[str, SessionInfo] = {}  # 세션 정보 저장
    
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
    async def create_native_session(self) -> SessionInfo:
        """제공자별 네이티브 세션 생성"""
        pass
    
    @abstractmethod
    async def query_with_native_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
        """네이티브 세션을 사용한 쿼리"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        pass
    
    async def create_session(self) -> str:
        """새로운 대화 세션 생성 (공통 인터페이스)"""
        session_info = await self.create_native_session()
        self.sessions[session_info.session_id] = session_info
        self.logger.info(f"새 세션 생성: {session_info.session_id[:8]}... (제공자: {self.get_name()})")
        return session_info.session_id
    
    async def query_with_session(self, prompt: str, session_id: str, 
                               additional_data: Optional[Dict[str, Any]] = None) -> str:
        """세션을 유지하면서 쿼리 실행 (공통 인터페이스)"""
        if session_id not in self.sessions:
            raise ValueError(f"세션을 찾을 수 없습니다: {session_id}")
        
        session_info = self.sessions[session_id]
        response = await self.query_with_native_session(prompt, session_info, additional_data)
        session_info.update_usage()
        
        return response
    
    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """세션 정보 조회"""
        return self.sessions.get(session_id)

class ClaudeSDKProvider(AIProvider):
    """Claude SDK 구현체 - 네이티브 세션 지원"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        # Max Plan 사용자는 Claude Code CLI 기반 인증 사용 - API 키 환경변수 제거
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
            self.logger.info("ANTHROPIC_API_KEY 환경변수 제거됨 - Claude Code CLI 인증 사용")
    
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Claude SDK를 사용한 AI 쿼리 (단발성)"""
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
    
    async def create_native_session(self) -> SessionInfo:
        """Claude SDK 네이티브 세션 생성 - 첫 번째 쿼리에서 세션 ID 획득 방식"""
        try:
            # Claude SDK에서는 첫 번째 쿼리에서 세션 ID가 생성됨
            # 따라서 세션 생성 시에는 메타데이터만 준비하고
            # 실제 세션 ID는 첫 번째 쿼리 시에 획득
            
            # 임시 세션 ID 생성 (첫 번째 쿼리에서 실제 ID로 교체)
            temp_session_id = f"claude_pending_{str(uuid.uuid4())}"
            
            # 세션 메타데이터 저장
            native_data = {
                "client_type": "query_with_options", 
                "conversation_active": False,  # 아직 실제 대화 시작 안함
                "first_query_sent": False,     # 첫 번째 쿼리 대기 중
                "actual_session_id": None      # 실제 세션 ID 대기
            }
            
            session_info = SessionInfo(
                session_id=temp_session_id,
                provider_type="claude",
                native_session_data=native_data
            )
            
            self.logger.info(f"Claude SDK 세션 준비: {temp_session_id[:12]}... (실제 ID는 첫 쿼리에서 획득)")
            return session_info
            
        except Exception as e:
            raise Exception(f"Claude SDK 세션 준비 실패: {e}")
    
    async def query_with_native_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Claude SDK 네이티브 세션을 사용한 쿼리 - 첫 쿼리에서 세션 ID 획득, 이후 재사용"""
        try:
            from claude_code_sdk import query, ClaudeCodeOptions
            
            # additional_data가 있으면 프롬프트에 포함
            enhanced_prompt = prompt
            if additional_data:
                context_parts = []
                for key, value in additional_data.items():
                    context_parts.append(f"{key}: {value}")
                if context_parts:
                    enhanced_prompt = f"{prompt}\n\n추가 정보:\n" + "\n".join(context_parts)
            
            responses = []
            native_data = session_info.native_session_data
            
            # 첫 번째 쿼리인지 확인
            if not native_data["first_query_sent"]:
                # 첫 번째 쿼리: 세션 ID 획득
                self.logger.info("첫 번째 Claude SDK 쿼리 - 세션 ID 획득 중...")
                
                actual_session_id = None
                
                async for message in query(prompt=enhanced_prompt):
                    # 세션 ID 추출 시도
                    if hasattr(message, 'session_id'):
                        actual_session_id = message.session_id
                        self.logger.info(f"✅ 세션 ID 획득 (session_id): {actual_session_id}")
                    elif hasattr(message, 'id'):
                        actual_session_id = message.id
                        self.logger.info(f"✅ 세션 ID 획득 (id): {actual_session_id}")
                    elif hasattr(message, 'conversation_id'):
                        actual_session_id = message.conversation_id
                        self.logger.info(f"✅ 세션 ID 획득 (conversation_id): {actual_session_id}")
                    
                    # 응답 내용 수집
                    if hasattr(message, 'content'):
                        content = message.content
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, 'text'):
                                    responses.append(block.text)
                        elif hasattr(content, 'text'):
                            responses.append(content.text)
                    elif hasattr(message, 'result'):
                        responses.append(str(message.result))
                
                # 획득한 세션 ID로 업데이트
                if actual_session_id:
                    session_info.session_id = actual_session_id
                    native_data["actual_session_id"] = actual_session_id
                    self.logger.info(f"🔄 세션 ID 업데이트: {actual_session_id[:12]}...")
                else:
                    self.logger.warning("⚠️ 세션 ID를 획득하지 못했습니다")
                
                # 상태 업데이트
                native_data["first_query_sent"] = True
                native_data["conversation_active"] = True
                
            else:
                # 후속 쿼리: 기존 세션 ID로 대화 이어가기
                actual_session_id = native_data["actual_session_id"]
                self.logger.info(f"🔗 기존 세션으로 대화 이어가기: {actual_session_id[:12]}...")
                
                # 검증된 방식: ClaudeCodeOptions(resume=session_id) 사용
                async for message in query(
                    prompt=enhanced_prompt,
                    options=ClaudeCodeOptions(resume=actual_session_id)
                ):
                    # 응답 내용 수집
                    if hasattr(message, 'content'):
                        content = message.content
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, 'text'):
                                    responses.append(block.text)
                        elif hasattr(content, 'text'):
                            responses.append(content.text)
                    elif hasattr(message, 'result'):
                        responses.append(str(message.result))
            
            response_text = '\n'.join(responses) if responses else ''
            self.logger.info(f"✅ Claude SDK 응답 길이: {len(response_text)} 문자")
            
            # 세션 사용량 업데이트
            session_info.update_usage()
            
            return response_text
                
        except Exception as e:
            error_msg = f"❌ Claude SDK 세션 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_name(self) -> str:
        return "Claude SDK"

class GeminiProvider(AIProvider):
    """Gemini AI 제공자 - Chat Session 지원"""
    
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
        """Gemini를 사용한 AI 쿼리 (단발성)"""
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
    
    async def create_native_session(self) -> SessionInfo:
        """Gemini Chat Session 생성"""
        try:
            import google.generativeai as genai
            
            # API 키 설정
            genai.configure(api_key=self.api_key)
            
            # 모델 생성 및 채팅 세션 시작
            model = genai.GenerativeModel(self.model_name)
            chat = model.start_chat(history=[])  # 빈 히스토리로 시작
            
            session_id = f"gemini_session_{str(uuid.uuid4())}"
            
            native_data = {
                "chat_session": chat,  # Gemini 채팅 세션 객체 저장
                "model_name": self.model_name,
                "message_history": []  # 히스토리 추적용
            }
            
            session_info = SessionInfo(
                session_id=session_id,
                provider_type="gemini",
                native_session_data=native_data
            )
            
            self.logger.info(f"Gemini 채팅 세션 생성: {session_id[:8]}...")
            return session_info
            
        except Exception as e:
            raise Exception(f"Gemini 세션 생성 실패: {e}")
    
    async def query_with_native_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Gemini Chat Session을 사용한 쿼리"""
        try:
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
            
            # 저장된 채팅 세션 사용
            chat_session = session_info.native_session_data["chat_session"]
            
            self.logger.info(f"Gemini 채팅 세션 쿼리 실행 중... (모델: {self.model_name})")
            
            # 채팅 세션으로 응답 생성 (히스토리 자동 관리)
            response = chat_session.send_message(enhanced_prompt)
            
            result = response.text if response.text else "응답이 비어있습니다"
            self.logger.info(f"Gemini 세션 응답 길이: {len(result)} 문자")
            
            # 히스토리 추적 업데이트
            session_info.native_session_data["message_history"].append({
                "prompt": enhanced_prompt,
                "response": result,
                "timestamp": time.time()
            })
            
            return result
            
        except Exception as e:
            error_msg = f"Gemini 세션 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_name(self) -> str:
        return f"Gemini Chat ({self.model_name})"

class OpenAIProvider(AIProvider):
    """OpenAI AI 제공자 - Assistant Thread 지원"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        
        # API 키 설정
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다 (OPENAI_API_KEY)")
        
        # 모델 설정
        self.model_name = self.config.get("model", "gpt-4")
        self.temperature = self.config.get("temperature", 0.1)
        self.max_tokens = self.config.get("max_tokens", 4096)
        
        self.logger.info(f"OpenAI 설정: 모델={self.model_name}, 온도={self.temperature}")
    
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """OpenAI를 사용한 AI 쿼리 (단발성)"""
        try:
            import openai
            
            # API 키 설정
            openai.api_key = self.api_key
            
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
            
            self.logger.info(f"OpenAI 쿼리 실행 중... (모델: {self.model_name})")
            
            # Chat Completions API 사용
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": enhanced_prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            self.logger.info(f"OpenAI 응답 길이: {len(result)} 문자")
            return result
            
        except Exception as e:
            error_msg = f"OpenAI 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    async def create_native_session(self) -> SessionInfo:
        """OpenAI Assistant Thread 생성"""
        try:
            import openai
            
            # API 키 설정
            openai.api_key = self.api_key
            
            # Assistant Thread 생성
            thread = openai.beta.threads.create()
            thread_id = thread.id
            
            session_id = f"openai_thread_{thread_id}"
            
            native_data = {
                "thread_id": thread_id,  # OpenAI Thread ID 저장
                "model_name": self.model_name,
                "message_history": []  # 히스토리 추적용
            }
            
            session_info = SessionInfo(
                session_id=session_id,
                provider_type="openai",
                native_session_data=native_data
            )
            
            self.logger.info(f"OpenAI Thread 생성: {thread_id}")
            return session_info
            
        except Exception as e:
            raise Exception(f"OpenAI Thread 생성 실패: {e}")
    
    async def query_with_native_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
        """OpenAI Assistant Thread를 사용한 쿼리"""
        try:
            import openai
            
            # API 키 설정
            openai.api_key = self.api_key
            
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
            
            # 저장된 Thread ID 사용
            thread_id = session_info.native_session_data["thread_id"]
            
            self.logger.info(f"OpenAI Thread 쿼리 실행 중... (Thread: {thread_id})")
            
            # Thread에 메시지 추가
            openai.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=enhanced_prompt
            )
            
            # Assistant 실행 (간단한 구현 - 실제로는 Assistant ID 필요)
            # 여기서는 Chat Completions로 대체
            messages = openai.beta.threads.messages.list(thread_id=thread_id)
            
            # 최근 메시지들을 Chat Completions 형태로 변환
            chat_messages = []
            for msg in reversed(messages.data[-10:]):  # 최근 10개만
                role = "assistant" if msg.role == "assistant" else "user"
                chat_messages.append({"role": role, "content": msg.content[0].text.value})
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=chat_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            self.logger.info(f"OpenAI Thread 응답 길이: {len(result)} 문자")
            
            # 응답을 Thread에도 추가
            openai.beta.threads.messages.create(
                thread_id=thread_id,
                role="assistant",
                content=result
            )
            
            # 히스토리 추적 업데이트
            session_info.native_session_data["message_history"].append({
                "prompt": enhanced_prompt,
                "response": result,
                "timestamp": time.time()
            })
            
            return result
            
        except Exception as e:
            error_msg = f"OpenAI Thread 쿼리 실패: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_name(self) -> str:
        return f"OpenAI Assistant ({self.model_name})"

class AIService:
    """통합 AI 서비스 - 네이티브 세션 관리 지원"""
    
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
        """설정 파일 기반으로 AI 제공자 선택
        
        Fallback 순서:
        1. 구체적 단계별 설정 (예: stage_specific_ai.workspace_preparation.chapter_toc_extraction)
        2. 기본 설정 (default_ai)
        3. 설정이 없으면 예외 발생
        """
        config = self._resolve_ai_config()
        provider_type = config.get("provider", "gemini").lower()
        
        # Provider 인스턴스 생성
        if provider_type == "claude":
            return ClaudeSDKProvider(config, self.logger)
        elif provider_type == "gemini":
            return GeminiProvider(config, self.logger)
        elif provider_type == "openai":
            return OpenAIProvider(config, self.logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공자: {provider_type}")
        
    def _resolve_ai_config(self) -> dict:
        """AI 설정 해결 - 단계별 설정 → 기본 설정 순으로 확인"""
        # 1. 구체적 단계별 설정 확인
        stage_config_path = f"stage_specific_ai.{self.stage_name}"
        stage_config = self.config_manager.get(stage_config_path, config_type="ai")
        
        if stage_config:
            self.logger.debug(f"단계별 AI 설정 사용: {self.stage_name}")
            return stage_config
            
        # 2. 기본 설정 사용
        default_config = self.config_manager.get("default_ai", config_type="ai")
        if default_config:
            self.logger.debug(f"기본 AI 설정 사용: {self.stage_name}")
            return default_config
            
        # 3. 설정이 없으면 예외 발생
        raise ValueError(f"AI 설정을 찾을 수 없습니다. ai_config.yaml을 확인하세요. 단계: {self.stage_name}")
    
    async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        AI 쿼리 실행 (단발성)
        
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
    
    async def create_session(self) -> str:
        """새로운 네이티브 세션 생성"""
        return await self.provider.create_session()
    
    async def query_with_session(self, prompt: str, session_id: str, 
                               additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        네이티브 세션을 유지하면서 AI 쿼리 실행
        
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
    
    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """세션 정보 조회"""
        return self.provider.get_session_info(session_id)
    
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