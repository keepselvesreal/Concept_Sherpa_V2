# 생성 시간: Thu Sep  4 21:02:45 KST 2025
# 핵심 내용: Claude SDK 세션 ID 기반 대화 연속성 검증 테스트
# 상세 내용:
#   - get_session_id_from_first_conversation (라인 19-77): 첫 대화에서 세션 ID 획득 검증
#   - continue_with_session_id (라인 79-149): 세션 ID 재사용으로 대화 연속성 검증
#   - main (라인 151-191): ClaudeCodeOptions(resume) 방식 유효성 검증
# 상태: active

import asyncio
import sys
import uuid
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

async def get_session_id_from_first_conversation():
    """첫 번째 대화에서 세션 ID 획득"""
    print("\n🔍 === 1단계: 첫 대화에서 세션 ID 획득 ===")
    
    try:
        from claude_code_sdk import query, ClaudeCodeOptions
        
        # 첫 번째 대화 시작
        context_prompt = """안녕하세요! 저는 데이터 분석가입니다.

오늘 공부할 내용:
1. 판다스 데이터 조작
2. 시각화 기법
3. 통계 분석 방법

이 3가지 주제를 기억해주시고, 각각에 대해 질문할 예정입니다."""

        print("📝 컨텍스트 설정 쿼리 전송 중...")
        
        session_id = None
        responses = []
        
        async for message in query(prompt=context_prompt):
            print(f"메시지 타입: {type(message).__name__}")
            
            # 세션 ID 추출 시도 (다양한 방법으로)
            if hasattr(message, 'session_id'):
                session_id = message.session_id
                print(f"✅ 세션 ID 발견 (session_id 속성): {session_id}")
            elif hasattr(message, 'id'):
                session_id = message.id
                print(f"✅ 세션 ID 발견 (id 속성): {session_id}")
            elif hasattr(message, 'conversation_id'):
                session_id = message.conversation_id
                print(f"✅ 세션 ID 발견 (conversation_id 속성): {session_id}")
            
            # 응답 내용 수집
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            responses.append(block.text)
                elif hasattr(message.content, 'text'):
                    responses.append(message.content.text)
            elif hasattr(message, 'result'):
                responses.append(str(message.result))
        
        response_text = '\n'.join(responses)
        print(f"✅ 첫 번째 응답 받음 (길이: {len(response_text)} 문자)")
        print(f"🔑 획득한 세션 ID: {session_id}")
        
        return session_id, response_text, len(response_text) > 0
        
    except ImportError:
        print("❌ Claude SDK를 사용할 수 없습니다")
        return None, "", False
    except Exception as e:
        print(f"❌ 첫 대화 실패: {str(e)}")
        return None, "", False

async def continue_with_session_id(session_id):
    """동일 세션 ID로 대화 이어가기"""
    print(f"\n🔄 === 2단계: 세션 ID {session_id[:12] if session_id else 'None'}...로 대화 이어가기 ===")
    
    if not session_id:
        print("❌ 세션 ID가 없어서 대화를 이어갈 수 없습니다")
        return [], False
    
    try:
        from claude_code_sdk import query, ClaudeCodeOptions
        
        responses_list = []
        
        # 두 번째 쿼리: 특정 주제 질문
        print("❓ 특정 주제에 대한 질문...")
        question1 = "앞서 말한 3가지 주제 중 '시각화 기법'에 대해서만 자세히 설명해주세요."
        
        responses1 = []
        async for message in query(
            prompt=question1,
            options=ClaudeCodeOptions(resume=session_id)
        ):
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            responses1.append(block.text)
                elif hasattr(message.content, 'text'):
                    responses1.append(message.content.text)
            elif hasattr(message, 'result'):
                responses1.append(str(message.result))
        
        response1_text = '\n'.join(responses1)
        print(f"✅ 두 번째 응답 받음 (길이: {len(response1_text)} 문자)")
        responses_list.append(response1_text)
        
        # 세 번째 쿼리: 기억력 테스트 (가장 중요)
        print("🧠 기억력 테스트...")
        memory_test = "처음에 제가 말한 오늘 공부할 내용 3가지를 정확히 다시 말해주세요."
        
        responses2 = []
        async for message in query(
            prompt=memory_test,
            options=ClaudeCodeOptions(resume=session_id)
        ):
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            responses2.append(block.text)
                elif hasattr(message.content, 'text'):
                    responses2.append(message.content.text)
            elif hasattr(message, 'result'):
                responses2.append(str(message.result))
        
        response2_text = '\n'.join(responses2)
        print(f"✅ 기억력 테스트 응답 받음 (길이: {len(response2_text)} 문자)")
        responses_list.append(response2_text)
        
        # 컨텍스트 기억 검증
        topics_remembered = all(topic in response2_text for topic in 
                               ["판다스", "시각화", "통계"])
        
        print(f"🎯 컨텍스트 기억 성공: {'✅ 예' if topics_remembered else '❌ 아니오'}")
        print(f"💬 기억 테스트 응답 미리보기: {response2_text[:150]}...")
        
        return responses_list, topics_remembered
        
    except Exception as e:
        print(f"❌ 세션 ID 기반 대화 실패: {str(e)}")
        return [], False

async def main():
    """메인 실행 및 맥락 유지 검증"""
    print("🚀 Claude SDK 세션 ID 기반 멀티턴 대화 검증")
    print("🔑 첫 대화에서 세션 ID를 획득하고, 그 ID로 대화를 이어가는 방식입니다")
    
    # 1단계: 첫 대화에서 세션 ID 획득
    session_id, first_response, first_success = await get_session_id_from_first_conversation()
    
    if not first_success:
        print("\n❌ 첫 대화 실패로 테스트 중단")
        return False
    
    # 2단계: 세션 ID로 대화 이어가기
    follow_up_responses, context_remembered = await continue_with_session_id(session_id)
    
    # 결과 요약
    print("\n" + "="*50)
    print("📋 세션 ID 기반 멀티턴 대화 결과")
    print("="*50)
    
    print(f"🔑 세션 ID: {session_id}")
    print(f"📊 첫 대화 성공: {'✅' if first_success else '❌'}")
    print(f"📊 후속 대화 수: {len(follow_up_responses)}개")
    print(f"🧠 컨텍스트 기억 성공: {'✅' if context_remembered else '❌'}")
    
    if first_success and len(follow_up_responses) > 0:
        print(f"📏 응답 길이들: {[len(resp) for resp in follow_up_responses]}")
        
        if context_remembered:
            print("\n✅ 세션 ID 기반 멀티턴 대화 성공!")
            print("🎯 동일한 세션 ID로 맥락이 완벽히 유지됨")
            print("🔧 현재 구현에 이 방식을 적용하면 문제 해결 가능")
            return True
        else:
            print("\n⚠️  세션 ID는 유지되지만 컨텍스트 기억 실패")
            print("🔍 세션 ID 활용 방식 재검토 필요")
            return False
    else:
        print("\n❌ 세션 ID 기반 대화 자체가 실패")
        print("🔍 Claude SDK 환경 또는 API 접근 문제 확인 필요")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⏹️  사용자에 의해 중단됨")
        sys.exit(1)
    except Exception as e:
        print(f"💥 예상치 못한 오류: {str(e)}")
        sys.exit(1)