# 목차
# 생성 시간: Tue Aug 26 10:10:34 KST 2025
# 핵심 내용: 저장된 세션 ID를 이용해 이전 대화를 이어가는 스크립트
# 상세 내용:
#   - load_session_data() (18-30): 저장된 세션 데이터 로드
#   - resume_method1_session() (32-55): Method 1 방식으로 세션 이어가기 시도
#   - resume_method2_session() (57-85): Method 2 방식으로 세션 이어가기
#   - test_context_memory() (87-95): 컨텍스트 기억 여부 테스트
#   - main() (97-110): 메인 실행 함수
# 상태: active
# 참조: session_starter.py

import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query
import json
from datetime import datetime
import os

SESSION_FILE = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-26/session_data.json"

def load_session_data():
    """저장된 세션 데이터 로드"""
    if not os.path.exists(SESSION_FILE):
        print(f"❌ 세션 파일이 없습니다: {SESSION_FILE}")
        print("먼저 session_starter.py를 실행하세요.")
        return None
    
    with open(SESSION_FILE, 'r', encoding='utf-8') as f:
        session_data = json.load(f)
    
    print(f"📂 세션 데이터 로드 완료")
    print(f"🆔 Method1 세션 ID: {session_data['method1']['session_id']}")
    print(f"🆔 Method2 세션 ID: {session_data['method2']['session_id']}")
    
    return session_data

async def resume_method1_session(session_data):
    """Method 1: ClaudeSDKClient로 세션 이어가기 시도"""
    print("\n" + "="*60)
    print("🔄 Method 1: ClaudeSDKClient 세션 재개 시도")
    print("="*60)
    
    # Method 1은 같은 클라이언트 객체 내에서만 작동하므로 
    # 새로운 세션으로 시작하고 이름을 기억하는지 테스트
    async with ClaudeSDKClient() as client:
        print("⚠️ Method 1은 새로운 클라이언트 객체이므로 이전 컨텍스트가 없을 것으로 예상")
        
        # 이전 대화를 기억하는지 테스트
        await client.query("내 이름이 뭐였지? 그리고 방금 낸 문제의 답은?")
        
        async for msg in client.receive_response():
            if hasattr(msg, 'content'):
                content = str(msg.content)
                print(f"📥 응답: {content[:200]}...")
                
                # 이름 기억 여부 체크
                if "태수" in content:
                    print("✅ 이름을 기억하고 있음!")
                else:
                    print("❌ 이전 대화 컨텍스트를 기억하지 못함")

async def resume_method2_session(session_data):
    """Method 2: query 함수로 세션 재개"""
    print("\n" + "="*60)
    print("🔄 Method 2: query 함수로 세션 재개")
    print("="*60)
    
    method2_session_id = session_data['method2']['session_id']
    print(f"🎯 재개할 세션 ID: {method2_session_id}")
    
    # continue_conversation=True로 이전 대화 이어가기
    print("\n🔗 continue_conversation=True로 대화 이어가기:")
    async for message in query(
        prompt="내 이름이 뭐였지? 그리고 방금 낸 문제의 답은?",
        options=ClaudeCodeOptions(continue_conversation=True)
    ):
        if hasattr(message, 'content'):
            content = str(message.content)
            print(f"📥 continue 응답: {content[:200]}...")
            
            if "태수" in content:
                print("✅ continue_conversation으로 이름을 기억!")
            else:
                print("❌ continue_conversation이 작동하지 않음")
    
    # 특정 세션 ID로 재개 시도
    print(f"\n🎯 특정 세션 ID ({method2_session_id[:20]}...)로 재개 시도:")
    try:
        async for message in query(
            prompt="아까 낸 곱셈 문제 기억해? 답에 2를 곱하면?",
            options=ClaudeCodeOptions(
                resume=method2_session_id,
                max_turns=3
            )
        ):
            if hasattr(message, 'content'):
                content = str(message.content)
                print(f"📥 resume 응답: {content[:200]}...")
                
                if "태수" in content or "곱셈" in content:
                    print("✅ 특정 세션 ID로 컨텍스트 재개 성공!")
                else:
                    print("❓ 부분적으로 기억하거나 새로운 대화로 처리됨")
    except Exception as e:
        print(f"❌ resume 옵션 오류: {e}")

def test_context_memory(content):
    """컨텍스트 기억 여부 테스트"""
    memory_indicators = ["태수", "덧셈", "곱셈", "문제", "아까", "방금"]
    found_indicators = [indicator for indicator in memory_indicators if indicator in content]
    
    if found_indicators:
        print(f"✅ 기억 지표 발견: {found_indicators}")
        return True
    else:
        print("❌ 이전 컨텍스트를 기억하지 못함")
        return False

async def main():
    print("=" * 80)
    print("🔥 세션 재개 스크립트 - 저장된 세션 ID로 대화 이어가기")
    print("=" * 80)
    
    session_data = load_session_data()
    if not session_data:
        return
    
    await resume_method1_session(session_data)
    await resume_method2_session(session_data)
    
    print("\n" + "="*80)
    print("📊 테스트 결과 요약:")
    print("- Method 1: 새 클라이언트 객체는 이전 컨텍스트 없음 (예상됨)")
    print("- Method 2: continue_conversation과 resume 옵션의 실제 작동 확인")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())