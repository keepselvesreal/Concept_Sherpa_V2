#!/usr/bin/env python3
"""
Claude 스트리밍 - 이전 성공 방식 + 강화된 디버그 출력
"""

import sys
import os
import anyio
import time
from datetime import datetime
from pathlib import Path
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

# 강제 출력 설정
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(line_buffering=False, write_through=True)

def debug_print(msg):
    """디버그 메시지 강제 출력"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[DEBUG {timestamp}] {msg}")
    sys.stdout.flush()

def force_print(msg):
    """강제 일반 메시지 출력"""  
    print(msg)
    sys.stdout.flush()

def force_char(char):
    """강제 문자 출력"""
    sys.stdout.write(char)
    sys.stdout.flush()

class ClaudeStreamingDebug:
    def __init__(self, typing_speed=0.03):
        self.typing_speed = typing_speed
        self.options = ClaudeCodeOptions(
            system_prompt="당신은 정확하고 도움이 되는 답변을 제공하는 AI 어시스턴트입니다.",
            max_turns=1
        )
        debug_print(f"ClaudeStreamingDebug 초기화 완료, 타이핑 속도: {1/typing_speed:.1f}문자/초")
    
    async def generate_streaming_response(self, prompt_instructions, user_query, retrieved_documents):
        """이전 성공 방식 기반 스트리밍 응답 생성"""
        
        debug_print("=== 스트리밍 응답 생성 시작 ===")
        
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
        
        debug_print(f"프롬프트 길이: {len(full_prompt)}자")
        debug_print(f"사용자 질의: {user_query}")
        
        accumulated_content = ""
        start_time = datetime.now()
        
        try:
            debug_print("ClaudeSDKClient 연결 시도...")
            
            # 이전 성공 방식: ClaudeSDKClient 컨텍스트 매니저
            async with ClaudeSDKClient() as client:
                debug_print("✅ ClaudeSDKClient 연결 성공!")
                
                debug_print("질의 전송 중...")
                await client.query(full_prompt)
                debug_print("✅ 질의 전송 완료!")
                
                debug_print("응답 수신 시작... (receive_response 호출)")
                
                force_print("\n🚀 실시간 스트리밍 응답:")
                force_print("=" * 60)
                force_print("")
                
                message_count = 0
                block_count = 0
                char_count = 0
                
                # 이전 성공 방식: receive_response() 사용
                async for message in client.receive_response():
                    message_count += 1
                    
                    if hasattr(message, 'content'):
                        debug_print(f"메시지 {message_count} 수신: {type(message)}")
                        debug_print(f"content 속성 발견, 블록 수: {len(message.content)}")
                        
                        for i, block in enumerate(message.content):
                            block_count += 1
                            debug_print(f"블록 {i+1} 처리 중: {type(block)}")
                            
                            if hasattr(block, 'text'):
                                block_text = block.text
                                debug_print(f"✅ 텍스트 블록 발견: {len(block_text)}자")
                                debug_print(f"텍스트 내용: '{block_text[:50]}...'")
                                
                                # 블록 시작 알림
                                force_print(f"\n[블록 {block_count}: {len(block_text)}자 수신]")
                                
                                # 이전 성공 방식: 문자 단위 타이핑 효과
                                for char in block_text:
                                    force_char(char)
                                    char_count += 1
                                    
                                    # 진행률 표시 (매 25자마다)
                                    if char_count % 25 == 0:
                                        debug_print(f"진행률: {char_count}자 출력 완료")
                                    
                                    await anyio.sleep(self.typing_speed)
                                
                                accumulated_content += block_text
                                debug_print(f"블록 {block_count} 출력 완료")
                                
                            else:
                                debug_print(f"❌ 블록에 text 속성 없음: {dir(block)}")
                    # SystemMessage나 ResultMessage는 조용히 무시
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                force_print(f"\n\n=" * 60)
                force_print("✅ 스트리밍 완료!")
                debug_print(f"총 처리 시간: {processing_time:.1f}초")
                debug_print(f"총 메시지 수: {message_count}")
                debug_print(f"총 블록 수: {block_count}")
                debug_print(f"총 문자 수: {len(accumulated_content)}")
                debug_print(f"평균 속도: {len(accumulated_content)/processing_time:.1f}문자/초")
                
                # 파일 저장
                saved_file = await self.save_response_to_file(
                    accumulated_content.strip(), user_query
                )
                if saved_file:
                    force_print(f"💾 파일 저장: {saved_file}")
                    debug_print(f"파일 저장 완료: {saved_file}")
                
                return accumulated_content.strip()
                
        except Exception as e:
            debug_print(f"❌ 오류 발생: {e}")
            debug_print(f"오류 타입: {type(e)}")
            import traceback
            debug_print(f"상세 오류:\n{traceback.format_exc()}")
            return None
    
    async def save_response_to_file(self, response_content, user_query):
        """응답을 마크다운 파일로 저장"""
        try:
            output_dir = Path("debug_streaming_responses")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_query = "".join(c for c in user_query[:30] if c.isalnum() or c in ' -_').strip()
            safe_query = safe_query.replace(' ', '_')
            if not safe_query:
                safe_query = "debug_streaming_response"
            
            filename = f"{timestamp}_debug_{safe_query}.md"
            file_path = output_dir / filename
            
            file_content = f"""# Claude 디버그 스트리밍 응답

## 생성 정보
- **생성 시간**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **사용자 질의**: {user_query}
- **방식**: ClaudeSDKClient + receive_response() + 강화 디버그
- **타이핑 속도**: {1/self.typing_speed:.0f}문자/초

## 생성된 응답

{response_content}

---
*Claude SDK 디버그 스트리밍으로 생성됨*
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            return str(file_path.absolute())
            
        except Exception as e:
            debug_print(f"파일 저장 실패: {e}")
            return None

# anyio 기반 메인 함수
async def main():
    debug_print("=== 메인 함수 시작 ===")
    
    force_print("🔧 Claude SDK 디버그 스트리밍 테스트")
    force_print("=" * 60)
    
    # 적당한 속도로 설정 (33문자/초)
    generator = ClaudeStreamingDebug(typing_speed=0.03)
    
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
    
    debug_print("테스트 데이터 설정 완료")
    debug_print(f"질의: {query}")
    debug_print(f"지침 길이: {len(instructions)}자")
    debug_print(f"문서 길이: {len(documents)}자")
    
    # 스트리밍 실행
    debug_print("스트리밍 응답 생성 호출...")
    result = await generator.generate_streaming_response(instructions, query, documents)
    
    if result:
        force_print(f"\n📊 최종 결과:")
        force_print(f"• 성공: ✅")
        force_print(f"• 응답 길이: {len(result)}자")
        force_print("🎉 디버그 스트리밍 테스트 완료!")
        debug_print(f"최종 응답 길이: {len(result)}자")
    else:
        force_print("❌ 스트리밍 실패")
        debug_print("최종 결과: 실패")

if __name__ == "__main__":
    debug_print("프로그램 시작")
    force_print("🚀 Claude 디버그 스트리밍 모드")
    force_print("💡 디버그 메시지와 함께 실시간 출력을 확인하세요!")
    
    try:
        anyio.run(main)
        debug_print("프로그램 정상 종료")
    except KeyboardInterrupt:
        debug_print("사용자 중단")
        force_print("\n🛑 사용자가 중단했습니다.")
    except Exception as e:
        debug_print(f"실행 오류: {e}")
        force_print(f"\n❌ 실행 오류: {e}")