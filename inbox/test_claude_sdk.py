#!/usr/bin/env python3
import asyncio
import os
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions, Message

# .env 파일 로드
def load_env():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

async def test_claude_simple():
    """가장 간단한 Claude Code SDK 테스트"""
    print("Claude Code SDK 간단 테스트 시작...")
    
    try:
        prompt = "안녕하세요! 간단한 테스트입니다. '테스트 성공!'이라고 응답해주세요."
        
        print("Claude에게 요청 전송 중...")
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(max_turns=1)
        ):
            messages.append(message)
            print(f"메시지 수신: {type(message)}")
        
        print(f"총 {len(messages)}개 메시지 수신")
        
        if messages:
            last_message = messages[-1]
            print(f"마지막 메시지 타입: {type(last_message)}")
            print(f"메시지 내용: {last_message}")
            
            # 메시지 속성 확인
            print("메시지 속성들:")
            for attr in dir(last_message):
                if not attr.startswith('_'):
                    try:
                        value = getattr(last_message, attr)
                        print(f"  {attr}: {value}")
                    except:
                        print(f"  {attr}: <접근 불가>")
        
        return True
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print(f"오류 타입: {type(e)}")
        return False

async def test_claude_book_analysis():
    """책 내용 분석 테스트"""
    print("\n책 내용 분석 테스트 시작...")
    
    try:
        sample_text = """
        1.1 OOP design: Classic or classical?
        
        Theo gets back to the office with Nancy's napkin in his pocket and a lot of anxiety in his
        heart because he knows he has committed to a tough deadline. But he had no choice! Last
        week, Monica, his boss, told him quite clearly that he had to close the deal with Nancy no
        matter what.
        """
        
        prompt = f"""
다음 텍스트의 핵심 내용을 3줄로 요약해주세요:

{sample_text}

형식:
1. [첫 번째 핵심 내용]
2. [두 번째 핵심 내용]  
3. [세 번째 핵심 내용]
"""
        
        print("분석 요청 전송 중...")
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(max_turns=1)
        ):
            messages.append(message)
        
        if messages:
            response = str(messages[-1])
            print("분석 결과:")
            print(response)
            return True
        else:
            print("응답을 받지 못했습니다.")
            return False
            
    except Exception as e:
        print(f"분석 테스트 오류: {e}")
        return False

async def main():
    # 환경 변수 로드
    load_env()
    
    # API 키 확인
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        return
    
    print(f"API 키 확인됨: {api_key[:20]}...")
    
    # 테스트 실행
    test1_result = await test_claude_simple()
    
    if test1_result:
        test2_result = await test_claude_book_analysis()
        
        if test2_result:
            print("\n✅ 모든 테스트 성공! Claude Code SDK가 정상 동작합니다.")
        else:
            print("\n❌ 책 분석 테스트 실패")
    else:
        print("\n❌ 기본 테스트 실패")

if __name__ == "__main__":
    asyncio.run(main())