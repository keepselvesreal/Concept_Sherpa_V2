# 목차
# 생성 시간: Tue Aug 26 10:17:18 KST 2025
# 핵심 내용: resume=세션ID 전용 테스트로 세션 연속성을 정확히 검증하는 스크립트
# 상세 내용:
#   - extract_session_id() (21-35): 메시지 객체에서 세션 ID 추출
#   - save_session_log() (37-53): 세션 로그 저장 
#   - create_initial_session() (55-90): 초기 세션 생성 및 세션 ID 저장
#   - test_resume_functionality() (92-145): resume 기능 테스트 및 세션 ID 비교
#   - analyze_session_continuity() (147-170): 세션 연속성 분석
#   - main() (172-185): 메인 실행 함수
# 상태: active
# 참조: session_starter.py, session_resumer.py

import asyncio
from claude_code_sdk import ClaudeCodeOptions, query
import json
from datetime import datetime
import os

# 로그 디렉터리
RESUME_LOG_DIR = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-26/resume_test_logs"
SESSION_STORAGE = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-26/resume_session.json"

def extract_session_id(message):
    """메시지 객체에서 세션 ID를 정확히 추출"""
    session_id = None
    
    # 다양한 속성 시도
    for attr in ['session_id', 'id', 'conversation_id', 'thread_id', 'message_id']:
        if hasattr(message, attr):
            value = getattr(message, attr)
            if value and str(value) != "None":
                session_id = str(value)
                break
    
    # 메시지 타입도 기록
    msg_type = type(message).__name__
    return session_id, msg_type

def save_session_log(step: str, data: dict):
    """세션 테스트 로그 저장"""
    if not os.path.exists(RESUME_LOG_DIR):
        os.makedirs(RESUME_LOG_DIR)
    
    timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
    filename = f"{RESUME_LOG_DIR}/{step}_{timestamp}.json"
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "data": data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"📝 로그 저장: {filename}")

async def create_initial_session():
    """초기 세션 생성 및 정보 저장"""
    print("🚀 1단계: 초기 세션 생성")
    print("-" * 50)
    
    query1 = "안녕! 나는 태수야. 12 + 8은 얼마지?"
    print(f"📤 질의: {query1}")
    
    session_ids = []
    responses = []
    
    async for message in query(prompt=query1):
        session_id, msg_type = extract_session_id(message)
        if session_id:
            session_ids.append(session_id)
        
        if hasattr(message, 'content'):
            content = str(message.content)
            responses.append(content)
            print(f"📥 응답: {content}")
            print(f"🆔 세션 ID: {session_id} (타입: {msg_type})")
    
    # 가장 최신 세션 ID 사용
    primary_session_id = session_ids[-1] if session_ids else None
    
    # 세션 데이터 저장
    session_data = {
        "created_at": datetime.now().isoformat(),
        "initial_query": query1,
        "primary_session_id": primary_session_id,
        "all_session_ids": session_ids,
        "responses": responses
    }
    
    with open(SESSION_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    save_session_log("initial_session", session_data)
    
    print(f"💾 주 세션 ID: {primary_session_id}")
    return session_data

async def test_resume_functionality(initial_data):
    """resume 기능 테스트 및 세션 ID 비교"""
    print("\n🔄 2단계: resume 기능으로 세션 재개")
    print("-" * 50)
    
    original_session_id = initial_data["primary_session_id"]
    query2 = "내 이름이 뭐였지? 그리고 방금 계산 결과에 5를 더하면?"
    
    print(f"🎯 원본 세션 ID: {original_session_id}")
    print(f"📤 재개 질의: {query2}")
    
    # resume으로 세션 재개
    resumed_session_ids = []
    resumed_responses = []
    
    async for message in query(
        prompt=query2,
        options=ClaudeCodeOptions(
            resume=original_session_id,
            max_turns=3
        )
    ):
        session_id, msg_type = extract_session_id(message)
        if session_id:
            resumed_session_ids.append(session_id)
            
        if hasattr(message, 'content'):
            content = str(message.content)
            resumed_responses.append(content)
            print(f"📥 재개 응답: {content}")
            print(f"🆔 재개 세션 ID: {session_id} (타입: {msg_type})")
    
    # 재개 데이터 저장
    resume_data = {
        "resume_at": datetime.now().isoformat(),
        "original_session_id": original_session_id,
        "resume_query": query2,
        "resumed_session_ids": resumed_session_ids,
        "resumed_responses": resumed_responses,
        "session_id_match": {
            "original": original_session_id,
            "resumed": resumed_session_ids[-1] if resumed_session_ids else None,
            "is_same": original_session_id in resumed_session_ids if original_session_id and resumed_session_ids else False
        }
    }
    
    save_session_log("resume_test", resume_data)
    
    return resume_data

def analyze_session_continuity(initial_data, resume_data):
    """세션 연속성 분석"""
    print("\n📊 3단계: 세션 연속성 분석")
    print("=" * 60)
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "session_id_analysis": {},
        "content_analysis": {},
        "overall_continuity": {}
    }
    
    # 세션 ID 분석
    original_id = initial_data["primary_session_id"]
    resumed_ids = resume_data["resumed_session_ids"]
    
    analysis["session_id_analysis"] = {
        "original_session_id": original_id,
        "resumed_session_ids": resumed_ids,
        "id_continuity": original_id in resumed_ids if original_id and resumed_ids else False
    }
    
    # 내용 분석
    resumed_content = " ".join(resume_data["resumed_responses"])
    analysis["content_analysis"] = {
        "remembers_name": "태수" in resumed_content,
        "remembers_calculation": any(num in resumed_content for num in ["12", "8", "20"]),
        "performed_new_calculation": "25" in resumed_content,  # 20 + 5 = 25
        "contextual_response": "방금" in resume_data["resume_query"] and any(word in resumed_content for word in ["계산", "결과", "더하"])
    }
    
    # 전체 연속성 판단
    id_match = analysis["session_id_analysis"]["id_continuity"]
    content_match = analysis["content_analysis"]["remembers_name"] and analysis["content_analysis"]["remembers_calculation"]
    
    analysis["overall_continuity"] = {
        "session_id_continuity": id_match,
        "content_continuity": content_match,
        "full_continuity": id_match and content_match,
        "verdict": "✅ 완전한 세션 연속성" if (id_match and content_match) else 
                 "⚠️ 부분적 연속성" if (id_match or content_match) else 
                 "❌ 연속성 없음"
    }
    
    save_session_log("analysis", analysis)
    
    # 결과 출력
    print(f"🆔 세션 ID 연속성: {'✅' if id_match else '❌'} ({original_id} → {resumed_ids})")
    print(f"📝 내용 연속성: {'✅' if content_match else '❌'}")
    print(f"🎯 최종 판정: {analysis['overall_continuity']['verdict']}")
    
    return analysis

async def main():
    """메인 실행 함수"""
    print("🧪 resume=세션ID 전용 테스트")
    print("=" * 60)
    
    # 1단계: 초기 세션 생성
    initial_data = await create_initial_session()
    
    # 2단계: resume으로 세션 재개
    resume_data = await test_resume_functionality(initial_data)
    
    # 3단계: 연속성 분석
    analysis = analyze_session_continuity(initial_data, resume_data)
    
    print(f"\n📂 모든 로그 저장 위치: {RESUME_LOG_DIR}")
    print("✅ 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(main())