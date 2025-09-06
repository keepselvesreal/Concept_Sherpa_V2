# 1단계: AIProvider 인터페이스 개선 안내 문서

## 🎯 목표
AIProvider 추상클래스와 구현체들의 메서드를 새로운 인터페이스로 교체하여 SessionInfo 객체 기반 세션 관리 구현

## 수정 대상 파일
- `/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/src/services/ai_service_v3.py`

---

## 1. AIProvider 추상클래스 수정

### 기존 메서드 제거
```python
# 제거할 메서드들
@abstractmethod
async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:

@abstractmethod  
async def query_with_native_session(self, prompt: str, session_info: SessionInfo, 
                                  additional_data: Optional[Dict[str, Any]] = None) -> str:

async def query_with_session(self, prompt: str, session_id: str, 
                           additional_data: Optional[Dict[str, Any]] = None) -> str:
```

### 새로운 메서드 추가
```python
@abstractmethod
async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
    """
    일회성 AI 쿼리 - 세션을 사용하지 않는 단발성 요청
    
    Args:
        prompt: 질의 프롬프트
        additional_data: 추가 입력 데이터 (파일 경로, 구조화된 데이터 등)
    """
    pass

@abstractmethod
async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
    """
    세션 유지 AI 쿼리 - SessionInfo 객체를 직접 사용
    
    Args:
        prompt: 질의 프롬프트
        session_info: SessionInfo 객체 (제공자별 네이티브 세션 데이터 포함)
        additional_data: 추가 입력 데이터
    """
    pass
```

### 수정할 메서드
```python
@abstractmethod
async def create_session(self) -> SessionInfo:
    """새로운 대화 세션 생성 - 각 provider가 구체 구현"""
    pass

@abstractmethod
def get_name(self) -> str:
    """AI 제공자 이름 반환"""
    pass

def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
    """세션 정보 조회"""
    return self.sessions.get(session_id)
```

### SessionInfo 클래스 추가
```python
class SessionInfo:
    """AI 제공자별 세션 정보를 담는 단순 래퍼 클래스"""
    
    def __init__(self, provider_type: str, session_data: Any):
        self.provider_type = provider_type  # "claude", "gemini", "openai"
        self.session_data = session_data    # 각 provider의 네이티브 세션 데이터
```

---

## 2. ClaudeSDKProvider 수정

### create_session 구현
```python
async def create_session(self) -> SessionInfo:
    """Claude 세션 생성 - session_id 문자열을 SessionInfo로 래핑"""
    try:
        session_id = await self._create_claude_session()  # 기존 내부 로직
        self.logger.info(f"Claude 세션 생성: {session_id[:12]}...")
        return SessionInfo("claude", session_id)
    except Exception as e:
        self.logger.error(f"Claude 세션 생성 실패: {e}")
        raise
```

### query_single_request 구현
- 기존 `query()` 메서드 로직을 그대로 사용
- 메서드명만 변경

### query_with_persistent_session 구현
```python
async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
    try:
        from claude_code_sdk import query, ClaudeCodeOptions
        
        # additional_data 처리 (기존 로직 유지)
        enhanced_prompt = prompt
        if additional_data:
            # Claude 방식 additional_data 처리 (기존 로직)
            for key, value in additional_data.items():
                if key == "toc_data":
                    enhanced_prompt += f"\n\n구조 정보:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                elif key == "file_paths":
                    enhanced_prompt += f"\n\n관련 파일들:\n{', '.join(value)}"
        
        # SessionInfo에서 Claude session_id 추출
        session_id = session_info.session_data
        
        # Claude SDK 직접 호출 (기존 내부 로직)
        options = ClaudeCodeOptions(session_id=session_id)
        response = await query(enhanced_prompt, options)
        
        return response.text
        
    except Exception as e:
        self.logger.error(f"Claude 세션 쿼리 실패: {e}")
        raise
```

---

## 3. GeminiProvider 수정

### create_session 구현
```python
async def create_session(self) -> SessionInfo:
    """Gemini 채팅 세션 생성 - chat 객체를 SessionInfo로 래핑"""
    try:
        chat_object = self._create_gemini_chat()  # 기존 내부 로직
        self.logger.info(f"Gemini 세션 생성: {id(chat_object)}")
        return SessionInfo("gemini", chat_object)
    except Exception as e:
        self.logger.error(f"Gemini 세션 생성 실패: {e}")
        raise
```

### query_single_request 구현
- 기존 `query()` 메서드 로직을 그대로 사용
- 메서드명만 변경

### query_with_persistent_session 구현
```python
async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
    try:
        # additional_data 처리 (기존 로직)
        enhanced_prompt = prompt
        if additional_data:
            # Gemini 방식 additional_data 처리 (기존 로직)
            for key, value in additional_data.items():
                if key == "toc_data":
                    enhanced_prompt += f"\n\n목차 구조:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                elif key == "context_info":
                    enhanced_prompt += f"\n\n맥락 정보:\n{value}"
        
        # SessionInfo에서 Gemini chat 객체 추출
        chat_session = session_info.session_data
        
        # Gemini 직접 호출 (기존 내부 로직)
        response = chat_session.send_message(enhanced_prompt)
        result = response.text if response.text else "응답이 비어있습니다"
        
        return result
        
    except Exception as e:
        self.logger.error(f"Gemini 세션 쿼리 실패: {e}")
        raise
```

---

## 4. OpenAIProvider 수정

### create_session 구현
```python
async def create_session(self) -> SessionInfo:
    """OpenAI 스레드 세션 생성 - thread_id를 SessionInfo로 래핑"""
    try:
        thread_id = await self._create_openai_thread()  # 기존 내부 로직
        self.logger.info(f"OpenAI 세션 생성: {thread_id}")
        return SessionInfo("openai", thread_id)
    except Exception as e:
        self.logger.error(f"OpenAI 세션 생성 실패: {e}")
        raise
```

### query_single_request 구현
- 기존 `query()` 메서드 로직을 그대로 사용
- 메서드명만 변경

### query_with_persistent_session 구현
```python
async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
    try:
        # additional_data 처리 (기존 로직)
        enhanced_prompt = prompt
        if additional_data:
            # OpenAI 방식 additional_data 처리 (기존 로직)
            for key, value in additional_data.items():
                if key == "system_message":
                    enhanced_prompt = f"시스템: {value}\n\n사용자: {enhanced_prompt}"
                elif key == "context_data":
                    enhanced_prompt += f"\n\n참고 데이터:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
        
        # SessionInfo에서 OpenAI thread_id 추출
        thread_id = session_info.session_data
        
        # OpenAI 직접 호출 (기존 내부 로직)
        message = await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=enhanced_prompt
        )
        
        run = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        
        # 실행 완료 대기 및 응답 처리 (기존 로직)
        # ... 기존 OpenAI 응답 처리 로직
        
        return response_text
        
    except Exception as e:
        self.logger.error(f"OpenAI 세션 쿼리 실패: {e}")
        raise
```

---

## 5. AIService 클래스 수정

### 기존 메서드 제거
```python
# 제거할 메서드들
async def query(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:

async def query_with_session(self, prompt: str, session_id: str, 
                           additional_data: Optional[Dict[str, Any]] = None) -> str:
```

### 새로운 메서드 추가
```python
async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
    """
    AI 쿼리 실행 (단발성)
    
    Args:
        prompt: 질의 프롬프트
        additional_data: 추가 입력 데이터 (파일 경로, TOC 데이터, 설정값 등)
    """
    try:
        self.logger.info(f"[{self.stage_name}] AI 단발성 쿼리 시작 - {self.provider.get_name()}")
        return await self.provider.query_single_request(prompt, additional_data)
    except Exception as e:
        error_msg = f"AI 단발성 쿼리 실패: {e}"
        self.logger.error(error_msg)
        return error_msg

async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                      additional_data: Optional[Dict[str, Any]] = None) -> str:
    """
    세션을 유지하면서 AI 쿼리 실행
    
    Args:
        prompt: 질의 프롬프트
        session_info: SessionInfo 객체 (create_session()에서 반환된 객체)
        additional_data: 추가 입력 데이터
    """
    try:
        self.logger.info(f"[{self.stage_name}] 세션 쿼리 시작 - {self.provider.get_name()} ({session_info.provider_type})")
        return await self.provider.query_with_persistent_session(prompt, session_info, additional_data)
    except Exception as e:
        error_msg = f"세션 쿼리 실패: {e}"
        self.logger.error(error_msg)
        raise Exception(error_msg)
```

### 수정할 메서드들
```python
async def create_session(self) -> SessionInfo:
    """새로운 AI 세션 생성 - provider가 SessionInfo 반환"""
    try:
        self.logger.info(f"[{self.stage_name}] 세션 생성 시작 - {self.provider.get_name()}")
        return await self.provider.create_session()  # SessionInfo 객체 반환
    except Exception as e:
        error_msg = f"세션 생성 실패: {e}"
        self.logger.error(error_msg)
        raise Exception(error_msg)
```

### 유지할 메서드들
```python
# 이 메서드들은 그대로 유지
def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
def get_name(self) -> str:
def get_config_summary(self) -> Dict[str, Any]:
```

---

## 6. 검증 포인트

### 구현 완료 후 확인사항
1. **메서드 시그니처**: 모든 추상 메서드가 올바르게 구현되었는지
2. **기존 로직 보존**: 각 제공자의 핵심 로직이 손실되지 않았는지
3. **SessionInfo 활용**: native_session_data에서 올바른 정보를 추출하는지
4. **에러 처리**: 기존 예외 처리 패턴이 유지되는지
5. **로깅**: 기존 로깅 패턴이 유지되는지

### 테스트 방법
```python
# 간단한 테스트 코드 예시
from services.ai_service_v3 import AIService

# 단발성 쿼리 테스트
ai_service = AIService(config_manager, logger, "test_stage")
response = await ai_service.query_single_request("간단한 테스트 질문")
print(f"단발성 응답: {response[:100]}...")

# 세션 쿼리 테스트  
session_id = await ai_service.create_session()
response = await ai_service.query_with_persistent_session("첫 번째 질문", session_id)
print(f"세션 응답: {response[:100]}...")
```

---

## 7. 주의사항

### ⚠️ 반드시 지킬 것
- **기존 로직 보존**: 각 제공자의 세션 관리 로직을 그대로 유지
- **에러 처리 유지**: 기존 try-catch 블록과 에러 메시지 형식 유지
- **로깅 패턴**: 기존 로깅 방식과 메시지 형식 유지

### 🔴 추가 제안 (태수 승인 필요)
없음 - 모든 변경사항은 요청된 내용에 기반함

---

## 8. 완료 조건
- [ ] AIProvider 추상클래스의 메서드 시그니처 변경
- [ ] ClaudeSDKProvider의 새 메서드 구현
- [ ] GeminiProvider의 새 메서드 구현  
- [ ] OpenAIProvider의 새 메서드 구현
- [ ] AIService 클래스의 새 메서드 구현
- [ ] 기존 메서드들 제거
- [ ] 간단한 동작 테스트 통과