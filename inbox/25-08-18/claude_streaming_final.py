#!/usr/bin/env python3
"""
Claude 스트리밍 응답 생성기 - 최종 완성 버전
사용법: python3 claude_streaming_final.py

프롬프트, 사용자 질의, 조회된 문서를 입력으로 받아 Claude SDK로 실시간 스트리밍 응답 생성
"""

import sys
import os
import anyio
from datetime import datetime
from pathlib import Path
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

# 출력 설정
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(line_buffering=False, write_through=True)

class ClaudeStreamingGenerator:
    """Claude SDK를 사용한 실시간 스트리밍 응답 생성기"""
    
    def __init__(self, typing_speed=0.03):
        """
        초기화
        
        Args:
            typing_speed: 문자 간 출력 간격 (초, 기본값: 0.03 = 33문자/초)
        """
        self.typing_speed = typing_speed
        self.options = ClaudeCodeOptions(
            system_prompt="당신은 정확하고 도움이 되는 답변을 제공하는 AI 어시스턴트입니다.",
            max_turns=1
        )
    
    async def generate_streaming_response(
        self, 
        prompt_instructions: str, 
        user_query: str, 
        retrieved_documents: str,
        save_to_file: bool = True,
        output_dir: str = "streaming_responses"
    ) -> str:
        """
        실시간 스트리밍 응답 생성
        
        Args:
            prompt_instructions: 프롬프트 지침
            user_query: 사용자 질의
            retrieved_documents: 조회된 문서 문자열
            save_to_file: 파일 저장 여부
            output_dir: 출력 디렉토리
            
        Returns:
            str: 생성된 응답 텍스트
        """
        
        print("🚀 Claude 스트리밍 응답 생성")
        print("=" * 60)
        print(f"📝 질의: {user_query}")
        print("=" * 60)
        print()
        
        # 프롬프트 구성
        full_prompt = f"""다음은 답변 생성을 위한 지침입니다:

{prompt_instructions}

---

사용자 질의:
{user_query}

---

관련 문서 내용:
{retrieved_documents}

---

위의 지침에 따라 사용자 질의에 대한 답변을 생성해주세요."""
        
        accumulated_content = ""
        start_time = datetime.now()
        
        try:
            async with ClaudeSDKClient() as client:
                print("🔄 Claude에 질의 전송 중...")
                sys.stdout.flush()
                
                await client.query(full_prompt)
                
                print("💬 실시간 응답:\n")
                sys.stdout.flush()
                
                block_count = 0
                char_count = 0
                
                async for message in client.receive_response():
                    if hasattr(message, 'content'):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                block_count += 1
                                block_text = block.text
                                
                                # 실시간 타이핑 효과
                                for char in block_text:
                                    sys.stdout.write(char)
                                    sys.stdout.flush()
                                    char_count += 1
                                    await anyio.sleep(self.typing_speed)
                                
                                accumulated_content += block_text
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                print(f"\n\n{'='*60}")
                print("✅ 스트리밍 완료!")
                print(f"📊 처리 시간: {processing_time:.1f}초")
                print(f"📊 응답 길이: {len(accumulated_content)}자")
                print(f"📊 평균 속도: {len(accumulated_content)/processing_time:.1f}문자/초")
                
                # 파일 저장
                if save_to_file and accumulated_content:
                    saved_file = await self.save_response_to_file(
                        accumulated_content.strip(), user_query, output_dir
                    )
                    if saved_file:
                        print(f"💾 파일 저장: {saved_file}")
                
                return accumulated_content.strip()
                
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return None
    
    async def save_response_to_file(self, response_content: str, user_query: str, output_dir: str = "streaming_responses") -> str:
        """응답을 마크다운 파일로 저장"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_query = "".join(c for c in user_query[:30] if c.isalnum() or c in ' -_').strip()
            safe_query = safe_query.replace(' ', '_')
            if not safe_query:
                safe_query = "streaming_response"
            
            filename = f"{timestamp}_{safe_query}.md"
            file_path = output_path / filename
            
            file_content = f"""# Claude 스트리밍 응답

## 생성 정보
- **생성 시간**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **사용자 질의**: {user_query}
- **타이핑 속도**: {1/self.typing_speed:.0f}문자/초

## 응답 내용

{response_content}

---
*Claude SDK 실시간 스트리밍으로 생성됨*
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            return str(file_path.absolute())
            
        except Exception as e:
            print(f"파일 저장 실패: {e}")
            return None

async def main():
    """메인 실행 함수"""
    
    print("🔧 Claude 스트리밍 생성기 시작")
    print("=" * 60)
    
    # 생성기 초기화 (33문자/초)
    generator = ClaudeStreamingGenerator(typing_speed=0.03)
    
    # 기본 테스트 데이터
    instructions = '''
간결하고 핵심적인 답변을 생성하세요.
답변은 한국어로 작성해주세요.
구체적이고 실용적인 내용으로 구성해주세요.
'''
    
    query = 'AI 코딩의 핵심 장점 3가지는 무엇인가요?'
    
    documents = """
AI 코딩의 주요 장점:
1. 개발 속도 향상: 반복 작업 자동화, 코드 생성 가속화
2. 품질 향상: 버그 감소, 코드 리뷰 지원, 모범 사례 적용
3. 학습 지원: 새로운 기술 학습, 문서화 자동화, 지식 공유

활용 사례:
- Claude Code: 프로젝트 전체 관리 및 컨텍스트 인식
- GitHub Copilot: 실시간 코드 완성
- ChatGPT: 문제 해결과 설명
"""
    
    # 스트리밍 응답 생성
    result = await generator.generate_streaming_response(
        instructions, query, documents, 
        save_to_file=True, 
        output_dir="streaming_responses"
    )
    
    if result:
        print("🎉 테스트 완료!")
    else:
        print("❌ 테스트 실패")

if __name__ == "__main__":
    print("💡 실시간 타이핑 효과를 확인하세요!")
    
    try:
        anyio.run(main)
    except KeyboardInterrupt:
        print("\n🛑 사용자가 중단했습니다.")
    except Exception as e:
        print(f"\n❌ 실행 오류: {e}")