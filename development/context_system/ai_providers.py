# 생성 시간: 2025-09-03 10:51:18 KST
# 핵심 내용: AI Provider 추상화 인터페이스 구현 - Gemini, OpenAI, Anthropic 등 여러 AI 서비스 통합
# 상세 내용:
#   - AIProvider (라인 23-31): AI 서비스 추상화 기본 클래스
#   - GeminiProvider (라인 34-59): Google Gemini API 구현체
#   - OpenAIProvider (라인 62-87): OpenAI GPT API 구현체
#   - AnthropicProvider (라인 90-115): Anthropic Claude API 구현체
#   - AIProviderFactory (라인 118-131): AI Provider 팩토리 클래스
# 상태: active
# 주소: ai_providers
# 참조: 없음

"""
AI Provider 추상화 모듈

여러 AI 서비스 (Gemini, OpenAI, Anthropic)를 통합하여
콘텍스트 분석을 수행할 수 있는 추상화 인터페이스 제공
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("ai_providers")


class AIProvider(ABC):
    """AI 서비스 추상화 기본 클래스"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    def analyze_context(self, content: str) -> Dict[str, Any]:
        """콘텍스트 분석 수행"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """단순 텍스트 생성"""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI Provider"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
            logger.info("Gemini provider 초기화 완료")
        except ImportError as e:
            logger.error(f"google-generativeai 패키지 설치 필요: {e}")
            raise
        except Exception as e:
            logger.error(f"Gemini 초기화 실패: {e}")
            raise
    
    def analyze_context(self, content: str) -> Dict[str, Any]:
        """Gemini로 콘텍스트 분석"""
        prompt = self._build_analysis_prompt(content)
        
        try:
            logger.info(f"Gemini 요청 시작 - 입력 길이: {len(content)} 글자")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise ValueError("Gemini에서 빈 응답을 받았습니다")
            
            logger.info(f"Gemini 응답 완료 - 응답 길이: {len(response.text)} 글자")
            logger.debug(f"Gemini 원본 응답: {response.text[:500]}...")
            
            parsed_result = self._parse_response(response.text)
            logger.info(f"응답 파싱 완료 - 파싱 결과 키: {list(parsed_result.keys())}")
            
            return parsed_result
            
        except Exception as e:
            logger.error(f"Gemini 분석 실패: {e}")
            logger.error(f"입력 콘텐츠 (첫 200글자): {content[:200]}...")
            raise
    
    def generate_text(self, prompt: str) -> str:
        """Gemini로 단순 텍스트 생성"""
        try:
            logger.info(f"Gemini 텍스트 생성 요청 - 프롬프트 길이: {len(prompt)} 글자")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return "응답을 받지 못했습니다"
            
            logger.info(f"Gemini 텍스트 생성 완료 - 응답 길이: {len(response.text)} 글자")
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Gemini 텍스트 생성 실패: {e}")
            return f"오류 발생: {str(e)}"
    
    def _build_analysis_prompt(self, content: str) -> str:
        return f"""
다음 사용자 질의 로그를 분석하여 향후 작업에 활용할 수 있는 콘텍스트 주제들을 추출해주세요.

사용자 질의 내용:
{content}

출력 형식:
1. Epic (모든 추출 맥락을 아우르는 주요 주제)
2. 각 맥락별로:
   - 맥락 이름
   - 맥락에 대한 간단한 설명
   - 맥락 추출이 필요한 이유

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "epic": "주요 주제",
  "contexts": [
    {{
      "name": "맥락 이름",
      "description": "맥락 설명", 
      "reason": "추출 필요 이유"
    }}
  ]
}}
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """응답 파싱"""
        try:
            import json
            # JSON 추출 시도
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_text = response_text[start:end]
                logger.debug(f"JSON 추출 시도: {json_text[:200]}...")
                parsed = json.loads(json_text)
                logger.info(f"JSON 파싱 성공 - 키: {list(parsed.keys())}")
                return parsed
            else:
                logger.warning("응답에서 JSON 구조를 찾을 수 없음")
                logger.debug(f"원본 응답: {response_text}")
                return {"raw_response": response_text, "parse_error": "JSON 구조 없음"}
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            logger.debug(f"파싱 시도한 텍스트: {response_text[start:end] if 'start' in locals() and 'end' in locals() else response_text[:200]}")
            return {"raw_response": response_text, "parse_error": f"JSON 디코딩 실패: {str(e)}"}


class OpenAIProvider(AIProvider):
    """OpenAI GPT Provider"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI provider 초기화 완료")
        except ImportError as e:
            logger.error(f"openai 패키지 설치 필요: {e}")
            raise
        except Exception as e:
            logger.error(f"OpenAI 초기화 실패: {e}")
            raise
    
    def analyze_context(self, content: str) -> Dict[str, Any]:
        """OpenAI로 콘텍스트 분석"""
        prompt = self._build_analysis_prompt(content)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            logger.info("OpenAI 분석 완료")
            return self._parse_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"OpenAI 분석 실패: {e}")
            raise
    
    def _build_analysis_prompt(self, content: str) -> str:
        return f"""
다음 사용자 질의 로그를 분석하여 향후 작업에 활용할 수 있는 콘텍스트 주제들을 추출해주세요.

사용자 질의 내용:
{content}

출력 형식:
1. Epic (모든 추출 맥락을 아우르는 주요 주제)
2. 각 맥락별로:
   - 맥락 이름
   - 맥락에 대한 간단한 설명
   - 맥락 추출이 필요한 이유

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "epic": "주요 주제",
  "contexts": [
    {{
      "name": "맥락 이름",
      "description": "맥락 설명", 
      "reason": "추출 필요 이유"
    }}
  ]
}}
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """응답 파싱 (Gemini와 동일한 로직)"""
        try:
            import json
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_text = response_text[start:end]
                return json.loads(json_text)
            else:
                return {"raw_response": response_text}
        except json.JSONDecodeError:
            logger.warning("JSON 파싱 실패, 원본 텍스트 반환")
            return {"raw_response": response_text}


class AnthropicProvider(AIProvider):
    """Anthropic Claude Provider"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            logger.info("Anthropic provider 초기화 완료")
        except ImportError as e:
            logger.error(f"anthropic 패키지 설치 필요: {e}")
            raise
        except Exception as e:
            logger.error(f"Anthropic 초기화 실패: {e}")
            raise
    
    def analyze_context(self, content: str) -> Dict[str, Any]:
        """Anthropic Claude로 콘텍스트 분석"""
        prompt = self._build_analysis_prompt(content)
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("Anthropic 분석 완료")
            return self._parse_response(response.content[0].text)
        except Exception as e:
            logger.error(f"Anthropic 분석 실패: {e}")
            raise
    
    def _build_analysis_prompt(self, content: str) -> str:
        return f"""
다음 사용자 질의 로그를 분석하여 향후 작업에 활용할 수 있는 콘텍스트 주제들을 추출해주세요.

사용자 질의 내용:
{content}

출력 형식:
1. Epic (모든 추출 맥락을 아우르는 주요 주제)
2. 각 맥락별로:
   - 맥락 이름
   - 맥락에 대한 간단한 설명
   - 맥락 추출이 필요한 이유

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "epic": "주요 주제",
  "contexts": [
    {{
      "name": "맥락 이름",
      "description": "맥락 설명", 
      "reason": "추출 필요 이유"
    }}
  ]
}}
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """응답 파싱 (동일한 로직)"""
        try:
            import json
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_text = response_text[start:end]
                return json.loads(json_text)
            else:
                return {"raw_response": response_text}
        except json.JSONDecodeError:
            logger.warning("JSON 파싱 실패, 원본 텍스트 반환")
            return {"raw_response": response_text}


class ClaudeSDKProvider(AIProvider):
    """Claude SDK Provider - Max Plan 사용자용"""
    
    def __init__(self, api_key: str = None):
        # Max Plan 사용자는 API 키 불필요
        super().__init__(api_key or "")
        try:
            import asyncio
            from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
            self.ClaudeSDKClient = ClaudeSDKClient
            self.ClaudeCodeOptions = ClaudeCodeOptions
            logger.info("Claude SDK provider 초기화 완료 (Max Plan)")
        except ImportError as e:
            logger.error(f"claude-code-sdk 패키지 설치 필요: {e}")
            raise
        except Exception as e:
            logger.error(f"Claude SDK 초기화 실패: {e}")
            raise
    
    def analyze_context(self, content: str) -> Dict[str, Any]:
        """Claude SDK로 콘텍스트 분석"""
        import asyncio
        
        try:
            if asyncio.get_event_loop().is_running():
                # 이미 실행 중인 이벤트 루프가 있을 때
                import nest_asyncio
                nest_asyncio.apply()
                result = asyncio.get_event_loop().run_until_complete(self._analyze_async(content))
            else:
                # 새로운 이벤트 루프 생성
                result = asyncio.run(self._analyze_async(content))
            
            return result
        except Exception as e:
            logger.error(f"Claude SDK 분석 실패: {e}")
            raise
    
    async def _analyze_async(self, content: str) -> Dict[str, Any]:
        """비동기 콘텍스트 분석"""
        prompt = self._build_analysis_prompt(content)
        
        logger.info(f"Claude SDK 요청 시작 - 입력 길이: {len(content)} 글자")
        
        try:
            async with self.ClaudeSDKClient(
                options=self.ClaudeCodeOptions(
                    system_prompt="당신은 콘텍스트 분석 전문가입니다. 사용자의 질의 로그를 분석하여 향후 작업에 활용할 수 있는 주제들을 추출합니다.",
                    allowed_tools=[],  # 도구 사용 없이 텍스트 분석만
                    max_turns=1,
                    model="claude-3-5-haiku-20241022"
                )
            ) as client:
                await client.query(prompt)
                
                # 응답 수집
                response_text = ""
                message_count = 0
                async for message in client.receive_response():
                    message_count += 1
                    logger.debug(f"메시지 {message_count} 수신: {type(message)}")
                    
                    if hasattr(message, 'content'):
                        logger.debug(f"content 속성 존재, 타입: {type(message.content)}")
                        for i, block in enumerate(message.content):
                            logger.debug(f"블록 {i}: {type(block)}, 속성: {dir(block)}")
                            if hasattr(block, 'text'):
                                text_content = block.text
                                logger.debug(f"텍스트 블록 발견: {text_content[:100]}...")
                                response_text += text_content
                            elif hasattr(block, 'content'):
                                # 다른 형태의 content 속성이 있을 수 있음
                                logger.debug(f"content 속성 발견: {str(block.content)[:100]}...")
                                response_text += str(block.content)
                    else:
                        logger.debug(f"메시지 속성들: {dir(message)}")
                        # content 속성이 없는 경우 직접 텍스트 확인
                        if hasattr(message, 'text'):
                            response_text += message.text
                        elif hasattr(message, 'delta') and hasattr(message.delta, 'text'):
                            response_text += message.delta.text
                
                logger.debug(f"총 {message_count}개 메시지 수신, 최종 텍스트 길이: {len(response_text)}")
                
                logger.info(f"Claude SDK 응답 완료 - 응답 길이: {len(response_text)} 글자")
                logger.debug(f"Claude SDK 원본 응답: {response_text[:500]}...")
                
                parsed_result = self._parse_response(response_text)
                logger.info(f"응답 파싱 완료 - 파싱 결과 키: {list(parsed_result.keys())}")
                
                return parsed_result
                
        except Exception as e:
            logger.error(f"Claude SDK 비동기 분석 실패: {e}")
            logger.error(f"입력 콘텐츠 (첫 200글자): {content[:200]}...")
            raise
    
    def _build_analysis_prompt(self, content: str) -> str:
        return f"""
다음 사용자 질의 로그를 분석하여 향후 작업에 활용할 수 있는 콘텍스트 주제들을 추출해주세요.

사용자 질의 내용:
{content}

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "epic": "주요 주제",
  "contexts": [
    {{
      "name": "맥락 이름",
      "description": "맥락 설명", 
      "reason": "추출 필요 이유"
    }}
  ]
}}
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """응답 파싱"""
        try:
            import json
            import re
            
            # JSON 코드 블록에서 추출
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
                logger.debug(f"JSON 코드 블록에서 추출: {json_text[:200]}...")
                parsed = json.loads(json_text)
                logger.info(f"JSON 파싱 성공 - 키: {list(parsed.keys())}")
                return parsed
            
            # 일반 JSON 추출
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_text = response_text[start:end]
                logger.debug(f"JSON 추출 시도: {json_text[:200]}...")
                parsed = json.loads(json_text)
                logger.info(f"JSON 파싱 성공 - 키: {list(parsed.keys())}")
                return parsed
            else:
                logger.warning("응답에서 JSON 구조를 찾을 수 없음")
                logger.debug(f"원본 응답: {response_text}")
                return {"raw_response": response_text, "parse_error": "JSON 구조 없음"}
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            logger.debug(f"파싱 시도한 텍스트: {response_text[:500]}")
            return {"raw_response": response_text, "parse_error": f"JSON 디코딩 실패: {str(e)}"}


class AIProviderFactory:
    """AI Provider 팩토리"""
    
    @staticmethod
    def create_provider(provider_type: str, api_key: Optional[str] = None) -> AIProvider:
        """AI Provider 생성"""
        if provider_type.lower() == 'claude-sdk':
            # Claude SDK는 Max Plan 사용자용으로 API 키 불필요
            return ClaudeSDKProvider()
        
        # 다른 provider들은 API 키 필요
        if api_key is None:
            api_key = AIProviderFactory._get_api_key(provider_type)
        
        if provider_type.lower() == 'gemini':
            return GeminiProvider(api_key)
        elif provider_type.lower() == 'openai':
            return OpenAIProvider(api_key)
        elif provider_type.lower() == 'anthropic':
            return AnthropicProvider(api_key)
        else:
            raise ValueError(f"지원하지 않는 provider: {provider_type}")
    
    @staticmethod
    def _get_api_key(provider_type: str) -> str:
        """환경변수에서 API 키 가져오기"""
        key_map = {
            'gemini': 'GEMINI_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY'
        }
        
        env_key = key_map.get(provider_type.lower())
        if not env_key:
            raise ValueError(f"지원하지 않는 provider: {provider_type}")
        
        api_key = os.getenv(env_key)
        if not api_key:
            raise ValueError(f"{env_key} 환경변수가 설정되지 않았습니다")
        
        return api_key