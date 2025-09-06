"""
생성 시간: 2025-08-18 15:13:22 KST
핵심 내용: Claude SDK 기반 기본 응답 생성 스크립트
상세 내용:
    - ClaudeResponseGenerator 클래스 (라인 35-120): 메인 응답 생성 엔진
    - generate_response 메서드 (라인 50-85): 핵심 응답 생성 함수
    - _build_prompt 메서드 (라인 87-105): 프롬프트 조합 로직
    - _process_claude_response 메서드 (라인 107-120): Claude 응답 처리
    - main 함수 (라인 125-145): 테스트 및 사용 예제
상태: 
주소: claude_response_generator
참조: claude_sdk_test
"""

import asyncio
import logging
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
from claude_code_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError

logger = logging.getLogger(__name__)

@dataclass
class ResponseResult:
    """응답 생성 결과"""
    content: str                    # 생성된 응답
    success: bool                   # 성공 여부
    processing_time: float          # 처리 시간 (초)
    error_message: Optional[str] = None   # 오류 메시지

class ClaudeResponseGenerator:
    """
    Claude SDK 기반 기본 응답 생성기
    - 프롬프트 지침 + 사용자 질의 + 조회된 문서로 응답 생성
    """
    
    def __init__(self):
        """응답 생성기 초기화"""
        self.options = ClaudeCodeOptions(
            system_prompt="당신은 정확하고 도움이 되는 답변을 제공하는 AI 어시스턴트입니다.",
            max_turns=1
        )
        logger.info("ClaudeResponseGenerator 초기화 완료")
    
    async def generate_response(
        self,
        prompt_instructions: str,
        user_query: str, 
        retrieved_documents: str
    ) -> ResponseResult:
        """
        응답 생성 메인 함수
        
        Args:
            prompt_instructions: 프롬프트 지침
            user_query: 사용자 질의
            retrieved_documents: 조회된 문서 문자열
            
        Returns:
            ResponseResult: 생성된 응답과 메타데이터
        """
        start_time = datetime.now()
        logger.info(f"응답 생성 시작 - 질의: '{user_query[:50]}...'")
        
        try:
            # 1. 프롬프트 구성
            full_prompt = self._build_prompt(
                prompt_instructions, user_query, retrieved_documents
            )
            
            # 2. Claude SDK 호출
            response_content = ""
            async for message in query(prompt=full_prompt, options=self.options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_content += block.text
            
            # 3. 응답 처리
            if response_content:
                processing_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"응답 생성 성공 ({processing_time:.2f}초)")
                
                return ResponseResult(
                    content=response_content.strip(),
                    success=True,
                    processing_time=processing_time
                )
            else:
                logger.warning("Claude로부터 빈 응답 수신")
                return ResponseResult(
                    content="죄송합니다. 응답을 생성할 수 없었습니다.",
                    success=False,
                    processing_time=(datetime.now() - start_time).total_seconds(),
                    error_message="Empty response from Claude"
                )
                
        except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Claude SDK 오류: {e}"
            logger.error(f"응답 생성 실패 ({processing_time:.2f}초): {error_msg}")
            
            return ResponseResult(
                content="죄송합니다. 기술적 문제로 응답을 생성할 수 없었습니다.",
                success=False,
                processing_time=processing_time,
                error_message=error_msg
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"예상치 못한 오류: {e}"
            logger.error(f"응답 생성 실패 ({processing_time:.2f}초): {error_msg}")
            
            return ResponseResult(
                content="죄송합니다. 문제가 발생했습니다.",
                success=False,
                processing_time=processing_time,
                error_message=error_msg
            )
    
    def _build_prompt(
        self, 
        instructions: str, 
        query: str, 
        documents: str
    ) -> str:
        """
        프롬프트 구성
        
        Args:
            instructions: 프롬프트 지침
            query: 사용자 질의
            documents: 조회된 문서
            
        Returns:
            완성된 프롬프트
        """
        prompt = f"""다음은 답변 생성을 위한 지침입니다:

{instructions}

---

사용자 질의:
{query}

---

관련 문서 내용:
{documents}

---

위의 지침에 따라 사용자 질의에 대한 답변을 생성해주세요."""

        return prompt

# 사용 예제 및 테스트 함수
async def main():
    """테스트 및 사용 예제"""
    print("🚀 Claude 응답 생성기 테스트 시작")
    
    # 응답 생성기 초기화
    generator = ClaudeResponseGenerator()
    
    # 테스트 데이터
    test_instructions = """
    사용자의 질문에 대해 제공된 문서를 바탕으로 정확하고 도움이 되는 답변을 생성하세요.
    답변은 한국어로 작성하고, 명확하고 이해하기 쉽게 설명해주세요.
    """
    
    test_query = "데이터 지향 프로그래밍의 주요 원칙은 무엇인가요?"
    
    test_documents = """
    데이터 지향 프로그래밍(DOP)의 4가지 핵심 원칙:
    1. 코드와 데이터의 분리
    2. 제네릭 데이터 구조로 데이터 표현
    3. 데이터의 불변성
    4. 데이터 스키마와 데이터 표현의 분리
    """
    
    # 응답 생성 테스트
    result = await generator.generate_response(
        test_instructions, test_query, test_documents
    )
    
    # 결과 출력
    print(f"\n📊 테스트 결과:")
    print(f"성공: {result.success}")
    print(f"처리 시간: {result.processing_time:.2f}초")
    if result.error_message:
        print(f"오류: {result.error_message}")
    
    print(f"\n💬 생성된 응답:")
    print(result.content)

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 테스트 실행
    asyncio.run(main())