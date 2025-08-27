# 목차
# 생성 시간: Tue Aug 26 10:10:34 KST 2025
# 핵심 내용: 첫 번째 대화를 시작하고 세션 ID를 파일에 저장하는 스크립트
# 상세 내용:
#   - start_conversation_and_save_session() (18-55): 대화 시작 및 세션 ID 저장
#   - extract_session_id() (57-70): 메시지에서 세션 ID 추출
#   - main() (72-80): 메인 실행 함수
# 상태: active
# 참조: SDK_Multiturn.py

import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query
import json
from datetime import datetime
import os

SESSION_FILE = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-26/session_data.json"

async def start_conversation_and_save_session():
    """첫 대화를 시작하고 세션 ID를 저장"""
    print("🚀 첫 번째 대화 시작 - 세션 ID 추출 및 저장")
    
    # Method 1: ClaudeSDKClient 방식
    print("\n📝 Method 1: ClaudeSDKClient 세션 시작")
    method1_session = None
    async with ClaudeSDKClient() as client:
        # 세션 ID 추출 시도
        if hasattr(client, 'session_id'):
            method1_session = client.session_id
        else:
            method1_session = "client_session_unknown"
            
        print(f"🆔 Method1 세션 ID: {method1_session}")
        
        await client.query("안녕! 내 이름은 태수야. 간단한 덧셈 문제 하나 내줘.")
        
        responses = []
        async for msg in client.receive_response():
            if hasattr(msg, 'content'):
                content = str(msg.content)
                responses.append(content)
                print(f"📥 응답: {content[:100]}...")
    
    # Method 2: query 함수 방식
    print("\n📝 Method 2: query 함수 세션 시작")
    method2_session = None
    responses2 = []
    
    async for message in query(prompt="안녕! 내 이름은 태수야. 간단한 곱셈 문제 하나 내줘."):
        # 세션 ID 추출 시도
        method2_session = extract_session_id(message)
        
        if hasattr(message, 'content'):
            content = str(message.content)
            responses2.append(content)
            print(f"📥 응답: {content[:100]}...")
    
    print(f"🆔 Method2 세션 ID: {method2_session}")
    
    # 세션 데이터 저장
    session_data = {
        "created_at": datetime.now().isoformat(),
        "method1": {
            "session_id": method1_session,
            "last_query": "안녕! 내 이름은 태수야. 간단한 덧셈 문제 하나 내줘.",
            "responses": responses[:1] if responses else []  # 첫 번째 응답만 저장
        },
        "method2": {
            "session_id": method2_session,
            "last_query": "안녕! 내 이름은 태수야. 간단한 곱셈 문제 하나 내줘.",
            "responses": responses2[:1] if responses2 else []  # 첫 번째 응답만 저장
        }
    }
    
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 세션 데이터 저장 완료: {SESSION_FILE}")
    return session_data

def extract_session_id(message):
    """메시지 객체에서 세션 ID 추출"""
    # 다양한 속성 이름 시도
    for attr in ['session_id', 'id', 'conversation_id', 'thread_id']:
        if hasattr(message, attr):
            session_id = getattr(message, attr)
            if session_id:
                return str(session_id)
    
    # 메시지 타입이나 내용으로 추정
    message_type = type(message).__name__
    return f"{message_type}_unknown"

async def main():
    print("=" * 80)
    print("🔥 세션 시작 스크립트 - 첫 번째 대화 및 세션 ID 저장")
    print("=" * 80)
    
    session_data = await start_conversation_and_save_session()
    
    print(f"\n✅ 완료! 이제 session_resumer.py를 실행해서 대화를 이어가세요.")
    print(f"📂 세션 파일: {SESSION_FILE}")

if __name__ == "__main__":
    asyncio.run(main())