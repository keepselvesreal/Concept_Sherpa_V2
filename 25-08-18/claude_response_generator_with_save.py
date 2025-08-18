"""
생성 시간: 2025-08-18 15:22:28 KST
핵심 내용: Claude SDK 기반 응답 생성 및 파일 저장 스크립트
상세 내용:
    - ClaudeResponseGenerator 클래스 (라인 35-175): 메인 응답 생성 엔진 (파일 저장 기능 추가)
    - generate_response 메서드 (라인 50-125): 핵심 응답 생성 함수
    - save_response_to_file 메서드 (라인 127-175): 응답 파일 저장 기능 (NEW)
    - _build_prompt 메서드 (라인 177-195): 프롬프트 조합 로직
    - main 함수 (라인 200-240): 테스트 및 사용 예제 (파일 저장 포함)
상태: 
주소: claude_response_generator_with_save
참조: claude_response_generator
"""

import asyncio
import logging
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os

from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
from claude_code_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError

logger = logging.getLogger(__name__)

@dataclass
class ResponseResult:
    """응답 생성 결과"""
    content: str                    # 생성된 응답
    success: bool                   # 성공 여부
    processing_time: float          # 처리 시간 (초)
    saved_file_path: Optional[str] = None    # 저장된 파일 경로 (NEW)
    error_message: Optional[str] = None      # 오류 메시지

class ClaudeResponseGenerator:
    """
    Claude SDK 기반 기본 응답 생성기 (파일 저장 기능 포함)
    - 프롬프트 지침 + 사용자 질의 + 조회된 문서로 응답 생성
    - 생성된 응답을 마크다운 파일로 저장
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
        retrieved_documents: str,
        save_to_file: bool = True,
        output_dir: str = "generated_responses"
    ) -> ResponseResult:
        """
        응답 생성 메인 함수 (파일 저장 옵션 추가)
        
        Args:
            prompt_instructions: 프롬프트 지침
            user_query: 사용자 질의
            retrieved_documents: 조회된 문서 문자열
            save_to_file: 파일 저장 여부 (기본값: True)
            output_dir: 출력 디렉토리 (기본값: "generated_responses")
            
        Returns:
            ResponseResult: 생성된 응답과 메타데이터 (파일 경로 포함)
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
                
                # 4. 파일 저장 (옵션)
                saved_file_path = None
                if save_to_file:
                    saved_file_path = await self.save_response_to_file(
                        response_content.strip(), user_query, output_dir
                    )
                
                return ResponseResult(
                    content=response_content.strip(),
                    success=True,
                    processing_time=processing_time,
                    saved_file_path=saved_file_path
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
    
    async def save_response_to_file(
        self, 
        response_content: str, 
        user_query: str, 
        output_dir: str = "generated_responses"
    ) -> str:
        """
        생성된 응답을 마크다운 파일로 저장 (NEW)
        
        Args:
            response_content: 생성된 응답 내용
            user_query: 사용자 질의 (파일명 생성용)
            output_dir: 출력 디렉토리
            
        Returns:
            저장된 파일의 절대 경로
        """
        try:
            # 출력 디렉토리 생성
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 파일명 생성 (타임스탬프 + 질의 키워드)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 질의에서 안전한 파일명 생성
            safe_query = "".join(c for c in user_query[:30] if c.isalnum() or c in ' -_').strip()
            safe_query = safe_query.replace(' ', '_')
            if not safe_query:
                safe_query = "response"
            
            filename = f"{timestamp}_{safe_query}.md"
            file_path = output_path / filename
            
            # 마크다운 형식으로 파일 내용 구성
            file_content = f"""# Claude 응답 생성 결과

## 생성 정보
- **생성 시간**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **사용자 질의**: {user_query}

## 생성된 응답

{response_content}

---
*이 응답은 Claude SDK를 통해 자동 생성되었습니다.*
"""
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            absolute_path = str(file_path.absolute())
            logger.info(f"응답 파일 저장 완료: {absolute_path}")
            
            return absolute_path
            
        except Exception as e:
            logger.error(f"파일 저장 실패: {e}")
            return None
    
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
    """테스트 및 사용 예제 (파일 저장 포함)"""
    print("🚀 Claude 응답 생성기 (파일 저장) 테스트 시작")
    
    # 응답 생성기 초기화
    generator = ClaudeResponseGenerator()
    
    # 실제 AI 코딩 질의 테스트
    instructions = '''
참고 정보(조회된 문서)를 바탕으로 사용자 질의에 적합한 답변을 생성하세요.
답변 내용에 출처를 명확히 표시하세요:
- 참고 정보 기반 답변: [참고 정보 기반]으로 표시
- 모델의 사전 지식 답변: [사전 지식 기반]으로 표시

답변은 한국어로 작성하고, 구체적이고 실용적인 내용으로 구성해주세요.
'''
    
    query = 'ai 코딩의 문제점 해결 도구들에 대해 알고 싶어'
    
    # 조회된 문서 로드
    try:
        with open('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-18/search_results/01_00_lev0_retrieval_agents_actually_solved_ai_codings_biggest_problem_infomd.md', 'r', encoding='utf-8') as f:
            documents = f.read()
    except FileNotFoundError:
        print("❌ 참고 문서를 찾을 수 없습니다. 기본 문서로 진행합니다.")
        documents = "AI 코딩 도구들에 대한 기본 정보..."
    
    # 응답 생성 및 파일 저장
    result = await generator.generate_response(
        instructions, query, documents, 
        save_to_file=True, 
        output_dir="/home/nadle/projects/Knowledge_Sherpa/v2/25-08-18/generated_responses"
    )
    
    # 결과 출력
    print(f"\n📊 테스트 결과:")
    print(f"성공: {result.success}")
    print(f"처리 시간: {result.processing_time:.2f}초")
    if result.saved_file_path:
        print(f"저장된 파일: {result.saved_file_path}")
    if result.error_message:
        print(f"오류: {result.error_message}")
    
    print(f"\n💬 생성된 응답 (처음 200자):")
    print(result.content[:200] + "...")

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 테스트 실행
    asyncio.run(main())