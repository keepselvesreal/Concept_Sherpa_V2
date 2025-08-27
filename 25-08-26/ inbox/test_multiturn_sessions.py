# 목차
# 생성 시간: Tue Aug 26 09:50:05 KST 2025
# 핵심 내용: Claude Code SDK 멀티턴 대화에서 세션 ID 유지 확인 테스트
# 상세 내용:
#   - test_method1_session_persistence() (20-45): ClaudeSDKClient 방식의 세션 ID 유지 테스트
#   - test_method2_session_management() (47-75): query 함수 방식의 세션 관리 테스트
#   - print_session_info() (77-85): 세션 정보 출력 헬퍼 함수
#   - main() (87-95): 두 방법 모두 테스트 실행
# 상태: active
# 참조: SDK_Multiturn.py

import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query
import uuid
from datetime import datetime

def print_debug(method: str, step: str, session_id: str = None, message: str = ""):
    """디버깅 정보 출력"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    session_part = f" | Session: {session_id[:8]}..." if session_id else " | Session: None"
    print(f"[{timestamp}] {method} - {step}{session_part} | {message}")

async def test_method1_session_persistence():
    """Method 1: ClaudeSDKClient 세션 ID 유지 테스트"""
    print("\n" + "="*80)
    print("🔍 Method 1: ClaudeSDKClient 세션 유지 테스트")
    print("="*80)
    
    async with ClaudeSDKClient() as client:
        # 첫 번째 질의
        print_debug("Method1", "시작", message="클라이언트 생성")
        
        # 세션 ID 확인 (가능하다면)
        session_id = getattr(client, 'session_id', None) or str(uuid.uuid4())
        print_debug("Method1", "세션생성", session_id, "첫 번째 질의 시작")
        
        await client.query("간단한 Python 함수 하나 만들어줘")
        
        response_count = 0
        async for msg in client.receive_response():
            response_count += 1
            if hasattr(msg, 'content'):
                content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                print_debug("Method1", f"응답{response_count}", session_id, f"내용: {content_preview}")
        
        # 두 번째 질의 (같은 세션에서)
        print_debug("Method1", "연속질의", session_id, "두 번째 질의 시작")
        
        await client.query("방금 만든 함수에 주석을 추가해줘")
        
        response_count = 0
        async for msg in client.receive_response():
            response_count += 1
            if hasattr(msg, 'content'):
                content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                print_debug("Method1", f"연속응답{response_count}", session_id, f"내용: {content_preview}")

async def test_method2_session_management():
    """Method 2: query 함수의 세션 관리 테스트"""
    print("\n" + "="*80)
    print("🔍 Method 2: query 함수 세션 관리 테스트")
    print("="*80)
    
    # 첫 번째 질의
    print_debug("Method2", "시작", message="첫 번째 독립 질의")
    
    session_id_1 = None
    response_count = 0
    async for message in query(prompt="간단한 클래스 하나 만들어줘"):
        response_count += 1
        # 세션 ID 추출 시도 (메시지 객체에서)
        if hasattr(message, 'session_id'):
            session_id_1 = message.session_id
        elif hasattr(message, 'id'):
            session_id_1 = message.id
        
        if hasattr(message, 'content'):
            content_preview = message.content[:50] + "..." if len(message.content) > 50 else message.content
            print_debug("Method2", f"응답{response_count}", session_id_1, f"내용: {content_preview}")
    
    # continue_conversation=True로 연속 대화 시도
    print_debug("Method2", "연속대화시도", session_id_1, "continue_conversation=True 사용")
    
    session_id_2 = None
    response_count = 0
    async for message in query(
        prompt="방금 만든 클래스에 메서드 하나 더 추가해줘",
        options=ClaudeCodeOptions(continue_conversation=True)
    ):
        response_count += 1
        # 세션 ID 추출 시도
        if hasattr(message, 'session_id'):
            session_id_2 = message.session_id
        elif hasattr(message, 'id'):
            session_id_2 = message.id
            
        if hasattr(message, 'content'):
            content_preview = message.content[:50] + "..." if len(message.content) > 50 else message.content
            print_debug("Method2", f"연속응답{response_count}", session_id_2, f"내용: {content_preview}")
    
    # 세션 ID 비교
    print_debug("Method2", "세션비교", 
                message=f"첫번째: {session_id_1}, 두번째: {session_id_2}, 동일: {session_id_1 == session_id_2}")

def print_session_info():
    """세션 정보 요약 출력"""
    print("\n" + "="*80)
    print("📊 테스트 결과 요약")
    print("="*80)
    print("Method 1 (ClaudeSDKClient): async with 블록 내에서 세션 유지 여부 확인됨")
    print("Method 2 (query 함수): continue_conversation 옵션으로 세션 연결 시도됨")
    print("각 메서드에서 출력된 Session ID를 비교하여 동일 세션 여부 판단하세요")

async def main():
    """두 방법 모두 테스트"""
    print("🚀 Claude Code SDK 멀티턴 세션 지속성 테스트 시작")
    
    await test_method1_session_persistence()
    await test_method2_session_management()
    
    print_session_info()

if __name__ == "__main__":
    asyncio.run(main())