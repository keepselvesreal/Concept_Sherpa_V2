# 목차
# 생성 시간: Tue Aug 26 10:21:25 KST 2025
# 핵심 내용: resume=세션ID 간단 테스트 스크립트 - 첫 실행은 세션 생성, 두 번째는 resume 테스트
# 상세 내용:
#   - extract_session_id() (18-28): 메시지에서 세션 ID 추출
#   - create_session() (30-60): 새 세션 생성 및 정보 출력
#   - resume_session() (62-90): 기존 세션 재개 테스트
#   - main() (92-105): CLI 인자에 따른 실행 분기
# 상태: active
# 참조: 없음

import asyncio
import sys
from claude_code_sdk import ClaudeCodeOptions, query
from datetime import datetime

def extract_session_id(message):
    """메시지에서 세션 ID 추출"""
    for attr in ['session_id', 'id', 'conversation_id', 'thread_id']:
        if hasattr(message, attr):
            value = getattr(message, attr)
            if value and str(value) != "None":
                return str(value)
    return None

async def create_session():
    """새 세션 생성"""
    print("🚀 새 세션 생성 중...")
    print("-" * 50)
    
    query_text = "안녕! 나는 태수야. 7 * 8은 얼마지?"
    print(f"📤 질의: {query_text}")
    
    session_ids = []
    responses = []
    
    async for message in query(prompt=query_text):
        # 세션 ID 추출
        session_id = extract_session_id(message)
        if session_id:
            session_ids.append(session_id)
        
        # 응답 내용
        if hasattr(message, 'content'):
            content = str(message.content)
            responses.append(content)
            print(f"📥 응답: {content}")
    
    # 세션 정보 출력
    final_session_id = session_ids[-1] if session_ids else None
    print(f"\n🆔 생성된 세션 ID: {final_session_id}")
    print(f"📊 총 응답 수: {len(responses)}")
    
    if final_session_id:
        print(f"\n✅ 다음 명령어로 세션을 재개하세요:")
        print(f"python simple_resume_test.py {final_session_id}")
    
    return final_session_id

async def resume_session(session_id):
    """기존 세션 재개"""
    print(f"🔄 세션 재개 중... (ID: {session_id[:20]}...)")
    print("-" * 50)
    
    query_text = "내 이름이 뭐였지? 그리고 방금 계산 결과에 10을 더하면?"
    print(f"📤 재개 질의: {query_text}")
    print(f"🎯 사용할 세션 ID: {session_id}")
    
    resumed_ids = []
    responses = []
    
    async for message in query(
        prompt=query_text,
        options=ClaudeCodeOptions(resume=session_id, max_turns=5)
    ):
        # 재개된 세션 ID 추출
        resumed_id = extract_session_id(message)
        if resumed_id:
            resumed_ids.append(resumed_id)
        
        # 응답 내용
        if hasattr(message, 'content'):
            content = str(message.content)
            responses.append(content)
            print(f"📥 재개 응답: {content}")
    
    # 세션 비교 정보
    final_resumed_id = resumed_ids[-1] if resumed_ids else None
    print(f"\n🆔 원본 세션 ID: {session_id}")
    print(f"🆔 재개 세션 ID: {final_resumed_id}")
    print(f"🔗 세션 ID 일치: {'✅' if session_id == final_resumed_id else '❌'}")
    print(f"📊 총 응답 수: {len(responses)}")

async def main():
    """메인 실행 함수"""
    print(f"⏰ 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        # 첫 번째 실행: 새 세션 생성
        print("📝 모드: 새 세션 생성")
        await create_session()
    else:
        # 두 번째 실행: 세션 재개
        session_id = sys.argv[1]
        print("📝 모드: 세션 재개")
        await resume_session(session_id)
    
    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(main())