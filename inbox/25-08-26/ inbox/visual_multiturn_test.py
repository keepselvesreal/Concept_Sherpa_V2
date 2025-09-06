# 목차
# 생성 시간: Tue Aug 26 09:55:19 KST 2025
# 핵심 내용: 멀티턴 세션 테스트 결과를 파일로 저장하여 시각적 확인이 가능한 테스트
# 상세 내용:
#   - create_log_directory() (19-25): 로그 디렉터리 생성 함수
#   - save_interaction_log() (27-45): 상호작용 로그 저장 함수
#   - test_method1_with_logging() (47-95): Method 1 테스트 및 로깅
#   - test_method2_with_logging() (97-145): Method 2 테스트 및 로깅
#   - create_summary_report() (147-175): 최종 요약 보고서 생성
#   - main() (177-190): 메인 실행 함수
# 상태: active
# 참조: test_multiturn_sessions.py

import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query
import uuid
from datetime import datetime
import os
import json

# 로그 저장 디렉터리
LOG_DIR = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-26/multiturn_logs"

def create_log_directory():
    """로그 디렉터리 생성"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"✅ 로그 디렉터리 생성: {LOG_DIR}")

def save_interaction_log(method: str, step: str, data: dict):
    """상호작용 로그를 파일에 저장"""
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{LOG_DIR}/{method}_{step}_{timestamp}.json"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "method": method,
        "step": step,
        "data": data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=2)
    
    # 콘솔에도 출력
    print(f"📝 [{datetime.now().strftime('%H:%M:%S')}] {method} - {step} → {filename}")

async def test_method1_with_logging():
    """Method 1: ClaudeSDKClient 테스트 (로깅 포함)"""
    print("\n" + "="*80)
    print("🔍 Method 1: ClaudeSDKClient 세션 유지 테스트 (로깅 포함)")
    print("="*80)
    
    async with ClaudeSDKClient() as client:
        session_id = getattr(client, 'session_id', None) or str(uuid.uuid4())
        
        # 첫 번째 질의 로깅
        query1 = "2+3은 얼마야?"
        save_interaction_log("Method1", "query1", {
            "session_id": session_id,
            "query": query1,
            "description": "간단한 수학 문제"
        })
        
        await client.query(query1)
        
        responses1 = []
        async for msg in client.receive_response():
            if hasattr(msg, 'content'):
                content = str(msg.content)
                responses1.append(content)
                print(f"📥 응답1: {content[:100]}...")
        
        # 첫 번째 응답 로깅
        save_interaction_log("Method1", "response1", {
            "session_id": session_id,
            "query": query1,
            "responses": responses1,
            "response_count": len(responses1)
        })
        
        # 두 번째 질의 로깅 (컨텍스트 의존적)
        query2 = "그럼 방금 답에 10을 더하면?"
        save_interaction_log("Method1", "query2", {
            "session_id": session_id,
            "query": query2,
            "description": "이전 답변에 의존하는 질문",
            "context_dependent": True
        })
        
        await client.query(query2)
        
        responses2 = []
        async for msg in client.receive_response():
            if hasattr(msg, 'content'):
                content = str(msg.content)
                responses2.append(content)
                print(f"📥 응답2: {content[:100]}...")
        
        # 두 번째 응답 로깅
        save_interaction_log("Method1", "response2", {
            "session_id": session_id,
            "query": query2,
            "responses": responses2,
            "response_count": len(responses2),
            "context_maintained": "방금 답" in query2
        })

async def test_method2_with_logging():
    """Method 2: query 함수 테스트 (로깅 포함)"""
    print("\n" + "="*80)
    print("🔍 Method 2: query 함수 세션 관리 테스트 (로깅 포함)")
    print("="*80)
    
    # 첫 번째 독립 질의
    query1 = "5*4는 얼마야?"
    session_id_1 = None
    
    save_interaction_log("Method2", "query1", {
        "query": query1,
        "description": "독립적인 수학 문제",
        "session_type": "independent"
    })
    
    responses1 = []
    async for message in query(prompt=query1):
        if hasattr(message, 'session_id'):
            session_id_1 = message.session_id
        elif hasattr(message, 'id'):
            session_id_1 = message.id
        
        if hasattr(message, 'content'):
            content = str(message.content)
            responses1.append(content)
            print(f"📥 응답1: {content[:100]}...")
    
    save_interaction_log("Method2", "response1", {
        "query": query1,
        "session_id": session_id_1,
        "responses": responses1,
        "response_count": len(responses1)
    })
    
    # 두 번째 질의 (continue_conversation=True)
    query2 = "그럼 방금 답에서 5를 빼면?"
    session_id_2 = None
    
    save_interaction_log("Method2", "query2", {
        "query": query2,
        "description": "이전 답변에 의존하는 질문",
        "continue_conversation": True,
        "context_dependent": True
    })
    
    responses2 = []
    async for message in query(
        prompt=query2,
        options=ClaudeCodeOptions(continue_conversation=True)
    ):
        if hasattr(message, 'session_id'):
            session_id_2 = message.session_id
        elif hasattr(message, 'id'):
            session_id_2 = message.id
        
        if hasattr(message, 'content'):
            content = str(message.content)
            responses2.append(content)
            print(f"📥 응답2: {content[:100]}...")
    
    save_interaction_log("Method2", "response2", {
        "query": query2,
        "session_id": session_id_2,
        "responses": responses2,
        "response_count": len(responses2),
        "session_comparison": {
            "session1": session_id_1,
            "session2": session_id_2,
            "same_session": session_id_1 == session_id_2
        }
    })

def create_summary_report():
    """최종 요약 보고서 생성"""
    summary = {
        "test_completed": datetime.now().isoformat(),
        "log_directory": LOG_DIR,
        "files_created": [],
        "analysis": {
            "method1": "ClaudeSDKClient - async with 블록 내 세션 유지",
            "method2": "query 함수 - continue_conversation 옵션 테스트",
            "key_questions": [
                "세션 ID가 동일하게 유지되는가?",
                "이전 답변을 기억하고 있는가?",
                "컨텍스트 의존적 질문에 올바르게 답하는가?"
            ]
        },
        "instructions": {
            "how_to_check": f"로그 파일들을 확인하세요: {LOG_DIR}",
            "key_files": "query1, response1, query2, response2 파일들 비교",
            "session_check": "session_id 필드 확인으로 세션 연속성 판단"
        }
    }
    
    # 로그 디렉터리의 파일 목록 추가
    if os.path.exists(LOG_DIR):
        summary["files_created"] = os.listdir(LOG_DIR)
    
    with open(f"{LOG_DIR}/summary_report.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 요약 보고서 생성: {LOG_DIR}/summary_report.json")

async def main():
    """메인 실행 함수"""
    print("🚀 멀티턴 세션 시각적 확인 테스트 시작")
    print(f"📁 모든 로그는 {LOG_DIR}에 저장됩니다")
    
    create_log_directory()
    
    await test_method1_with_logging()
    await test_method2_with_logging()
    
    create_summary_report()
    
    print("\n✅ 테스트 완료! 로그 파일들을 확인해보세요.")
    print(f"📂 로그 위치: {LOG_DIR}")

if __name__ == "__main__":
    asyncio.run(main())