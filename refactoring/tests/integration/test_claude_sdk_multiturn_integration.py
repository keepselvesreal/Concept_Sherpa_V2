# 생성 시간: Thu Sep  4 21:44:15 KST 2025
# 핵심 내용: Claude SDK 멀티턴 대화 통합 테스트 (최종 검증)
# 상세 내용:
#   - test_final_claude_implementation (라인 18-75): Claude SDK 세션 기반 멀티턴 통합 테스트
#   - main (라인 77-115): 테스트 실행 및 컨텍스트 기억 능력 검증
# 상태: active

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

async def test_final_claude_implementation():
    """최종 수정된 Claude SDK 구현 테스트"""
    print("\n🚀 === 최종 수정된 Claude SDK 구현 검증 ===")
    print("🔧 첫 쿼리에서 세션 ID 획득 → 후속 쿼리에서 재사용 방식")
    
    try:
        # 필요한 모듈 임포트
        from utils.config_manager import ConfigManager
        from services.ai_service_v3 import AIService
        from utils.logger_v2 import Logger
        
        # 설정 및 로거 초기화
        config_manager = ConfigManager()
        logger = Logger("final_claude_test")
        
        # Claude 설정으로 강제 변경
        claude_config = {
            "provider": "claude",
            "model": "claude-3-5-sonnet-20241022",
            "temperature": 0.1,
            "max_tokens": 8192
        }
        
        # AI 서비스 생성
        ai_service = AIService(config_manager, logger, "test.final_claude_implementation")
        # Claude 제공자로 강제 설정
        from services.ai_service_v3 import ClaudeSDKProvider
        ai_service.provider = ClaudeSDKProvider(claude_config, logger)
        
        print(f"✅ 최종 Claude SDK 서비스 준비: {ai_service.get_name()}")
        
        # 세션 생성 (임시 세션 ID 생성)
        session_id = await ai_service.create_session()
        session_info = ai_service.get_session_info(session_id)
        print(f"✅ 세션 준비 완료: {session_id[:12]}... (Provider: {session_info.provider_type if session_info else 'unknown'})")
        print(f"   First Query Sent: {session_info.native_session_data.get('first_query_sent', 'unknown')}")
        
        # 1단계: 컨텍스트 설정 (이때 실제 세션 ID 획득)
        context_prompt = """안녕하세요! 저는 여러분에게 프로그래밍 교육을 제공할 강사입니다.
        
오늘 학습할 주제들:
1. Python 함수와 변수
2. 객체지향 프로그래밍
3. 데이터베이스 연동

위 3가지 주제를 차례대로 다룰 예정입니다. 기억해주세요!"""

        response1 = await ai_service.query_with_session(context_prompt, session_id)
        session_info = ai_service.get_session_info(session_id)  # 업데이트된 정보 가져오기
        print(f"✅ 1단계 컨텍스트 설정 완료 (응답 길이: {len(response1)} 문자)")
        print(f"   세션 ID 업데이트: {session_info.session_id[:12]}...")
        print(f"   First Query Sent: {session_info.native_session_data.get('first_query_sent', 'unknown')}")
        print(f"   Actual Session ID: {session_info.native_session_data.get('actual_session_id', 'none')[:12] if session_info.native_session_data.get('actual_session_id') else 'none'}...")
        
        # 2단계: 첫 번째 질문 (컨텍스트 활용 테스트)
        question1 = "앞서 말한 3가지 학습 주제 중에서 '객체지향 프로그래밍'에 대해서만 설명해주세요."
        response2 = await ai_service.query_with_session(question1, session_id)
        print(f"✅ 2단계 특정 주제 질문 완료 (응답 길이: {len(response2)} 문자)")
        
        # 3단계: 연관 질문 (이전 대화 기억 확인)
        question2 = "방금 설명한 객체지향 프로그래밍의 핵심 개념을 간단히 요약해주세요."
        response3 = await ai_service.query_with_session(question2, session_id)
        print(f"✅ 3단계 연관 질문 완료 (응답 길이: {len(response3)} 문자)")
        
        # 4단계: 컨텍스트 기억 확인 (가장 중요한 테스트)
        question3 = "처음에 제가 말한 오늘 학습할 주제 3가지를 정확히 다시 말해주세요."
        response4 = await ai_service.query_with_session(question3, session_id)
        print(f"✅ 4단계 컨텍스트 기억 테스트 완료 (응답 길이: {len(response4)} 문자)")
        
        # 컨텍스트 기억 검증
        topics_remembered = all(topic in response4 for topic in 
                               ["Python", "객체지향", "데이터베이스"])
        
        print(f"🎯 컨텍스트 기억 성공: {'✅ 예' if topics_remembered else '❌ 아니오'}")
        
        return True, {
            "session_id": session_info.session_id,
            "provider": ai_service.get_name(),
            "total_turns": 4,
            "responses": [len(response1), len(response2), len(response3), len(response4)],
            "context_remembered": topics_remembered,
            "memory_test_response": response4,
            "actual_session_id": session_info.native_session_data.get('actual_session_id'),
            "conversation_active": session_info.native_session_data.get('conversation_active')
        }
        
    except Exception as e:
        print(f"❌ 최종 Claude SDK 테스트 실패: {str(e)}")
        return False, {"error": str(e)}

async def main():
    """메인 실행 및 상세 분석"""
    print("🧪 최종 수정된 Claude SDK 멀티턴 구현 검증")
    print("🔍 첫 쿼리에서 세션 ID 획득, 후속 쿼리에서 ClaudeCodeOptions(resume) 사용")
    
    # 최종 구현 테스트
    success, result = await test_final_claude_implementation()
    
    # 결과 상세 분석
    print("\n" + "="*60)
    print("📊 최종 Claude SDK 구현 테스트 결과")
    print("="*60)
    
    if success and isinstance(result, dict):
        print(f"🔑 세션 ID: {result.get('session_id', 'Unknown')}")
        print(f"🎯 실제 세션 ID: {result.get('actual_session_id', 'Unknown')}")
        print(f"🤖 제공자: {result.get('provider', 'Unknown')}")
        print(f"🔢 총 턴 수: {result.get('total_turns', 0)}")
        print(f"📏 응답 길이들: {result.get('responses', [])}")
        print(f"🔄 대화 활성 상태: {result.get('conversation_active', False)}")
        
        context_remembered = result.get('context_remembered', False)
        print(f"🧠 컨텍스트 기억 성공: {'✅' if context_remembered else '❌'}")
        
        if 'memory_test_response' in result:
            memory_response = result['memory_test_response'][:300]
            print(f"💬 기억 테스트 응답 미리보기:\n   {memory_response}...")
        
        if context_remembered:
            print(f"\n🎉 성공! 최종 Claude SDK 구현이 완벽하게 작동합니다!")
            print("✅ 첫 쿼리에서 세션 ID 획득 → 후속 쿼리에서 재사용 방식 성공")
            print("🎯 이제 content_document_service_v3.py에서 안전하게 Claude SDK 사용 가능")
            return True
        else:
            print(f"\n⚠️  아직 컨텍스트 기억이 완벽하지 않습니다")
            print("🔍 추가 디버깅이 필요할 수 있습니다")
            return False
            
    else:
        print("❌ 최종 구현 테스트 실패")
        if isinstance(result, dict) and 'error' in result:
            print(f"   오류: {result['error']}")
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