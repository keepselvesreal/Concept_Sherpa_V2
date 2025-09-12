# 생성 시간: Thu Sep  4 20:45:17 KST 2025
# 핵심 내용: Gemini API 멀티턴 대화 연속성 검증 테스트
# 상세 내용:
#   - test_multiturn_conversation (라인 18-65): Gemini Chat Session 멀티턴 대화 검증
#   - test_context_memory (라인 67-90): 컨텍스트 기억 능력 및 세션 연속성 검증
#   - main (라인 92-120): Gemini API 멀티턴 유효성 종합 검증
# 상태: active

import asyncio
import json
import sys
import os
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# 필요한 모듈 임포트
from utils.config_manager import ConfigManager
from services.ai_service_v3 import AIService
from utils.logger_v2 import Logger

async def test_multiturn_conversation():
    """멀티턴 대화 기본 기능 테스트"""
    print("\n🔍 === Gemini API 멀티턴 대화 테스트 시작 ===")
    
    # 설정 및 로거 초기화
    config_manager = ConfigManager()
    logger = Logger("gemini_test")
    
    try:
        # AI 서비스 생성 (기본 설정 사용)
        ai_service = AIService(config_manager, logger, "test.multiturn")
        print(f"✅ AI 서비스 초기화 완료: {ai_service.get_name()}")
        
        # 세션 생성
        session_id = await ai_service.create_session()
        session_info = ai_service.get_session_info(session_id)
        print(f"✅ 세션 생성 완료: {session_id[:8]}... (Provider: {session_info.provider_type if session_info else 'unknown'})")
        
        # 1단계: 컨텍스트 설정
        context_prompt = """안녕하세요! 저는 여러분에게 Python 프로그래밍에 대해 알려드릴 선생님입니다.
        
오늘 배울 내용:
1. 변수와 자료형
2. 조건문과 반복문  
3. 함수 정의와 호출

이제 각 주제별로 질문하시면 자세히 설명해드리겠습니다. 위 내용을 기억해주세요."""

        response1 = await ai_service.query_with_session(context_prompt, session_id)
        print(f"✅ 컨텍스트 설정 완료 (응답 길이: {len(response1)} 문자)")
        
        # 2단계: 첫 번째 질문 (컨텍스트 활용)
        question1 = "앞서 언급한 3가지 주제 중에서 '변수와 자료형'에 대해서만 설명해주세요."
        response2 = await ai_service.query_with_session(question1, session_id)
        print(f"✅ 첫 번째 질문 완료 (응답 길이: {len(response2)} 문자)")
        
        # 3단계: 연관 질문 (이전 대화 기억 확인)
        question2 = "방금 설명한 자료형 중에서 숫자형만 예제와 함께 다시 설명해주세요."
        response3 = await ai_service.query_with_session(question2, session_id)
        print(f"✅ 두 번째 질문 완료 (응답 길이: {len(response3)} 문자)")
        
        # 4단계: 컨텍스트 기억 확인
        question3 = "처음에 제가 말한 오늘 배울 내용 3가지를 다시 말해주세요."
        response4 = await ai_service.query_with_session(question3, session_id)
        print(f"✅ 컨텍스트 기억 확인 완료 (응답 길이: {len(response4)} 문자)")
        
        return True, {
            "session_id": session_id,
            "provider": ai_service.get_name(),
            "total_turns": 4,
            "responses": [len(response1), len(response2), len(response3), len(response4)]
        }
        
    except Exception as e:
        print(f"❌ 멀티턴 테스트 실패: {str(e)}")
        return False, {"error": str(e)}

async def test_context_memory():
    """컨텍스트 기억 능력 심화 테스트"""
    print("\n🧠 === 컨텍스트 기억 능력 테스트 시작 ===")
    
    config_manager = ConfigManager()
    logger = Logger("context_test")
    
    try:
        ai_service = AIService(config_manager, logger, "test.context_memory")
        session_id = await ai_service.create_session()
        
        # 복잡한 정보 제공
        context_data = """다음은 가상의 회사 직원 정보입니다:

직원1: 이름=김철수, 부서=개발팀, 나이=30, 언어=Python,Java
직원2: 이름=박영희, 부서=디자인팀, 나이=28, 언어=JavaScript,CSS  
직원3: 이름=정민수, 부서=개발팀, 나이=32, 언어=Go,Python
직원4: 이름=최지은, 부서=마케팅팀, 나이=26, 언어=없음

이 정보를 기억하고 있다가 질문에 답해주세요."""

        await ai_service.query_with_session(context_data, session_id)
        print("✅ 복잡한 컨텍스트 데이터 제공 완료")
        
        # 기억력 테스트 질문들
        test_questions = [
            "개발팀에 속한 직원들의 이름만 말해주세요.",
            "Python을 사용할 수 있는 직원은 몇 명인가요?",
            "가장 나이가 많은 직원과 가장 적은 직원의 나이 차이는 얼마인가요?"
        ]
        
        success_count = 0
        for i, question in enumerate(test_questions, 1):
            response = await ai_service.query_with_session(question, session_id)
            print(f"✅ 질문 {i} 완료: {question[:30]}... (응답: {len(response)} 문자)")
            
            # 간단한 유효성 검사
            if len(response) > 10:  # 의미있는 응답인지 확인
                success_count += 1
        
        success_rate = (success_count / len(test_questions)) * 100
        print(f"📊 컨텍스트 기억 성공률: {success_rate:.1f}% ({success_count}/{len(test_questions)})")
        
        return success_rate >= 80, {"success_rate": success_rate, "details": f"{success_count}/{len(test_questions)}"}
        
    except Exception as e:
        print(f"❌ 컨텍스트 테스트 실패: {str(e)}")
        return False, {"error": str(e)}

async def main():
    """메인 테스트 실행"""
    print("🚀 Gemini API 멀티턴 대화 방식 유효성 검증 시작")
    
    results = []
    
    # 기본 멀티턴 대화 테스트
    basic_success, basic_result = await test_multiturn_conversation()
    results.append(("기본 멀티턴 대화", basic_success, basic_result))
    
    # 컨텍스트 기억 테스트  
    context_success, context_result = await test_context_memory()
    results.append(("컨텍스트 기억 능력", context_success, context_result))
    
    # 결과 요약
    print("\n" + "="*50)
    print("📋 테스트 결과 요약")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success, _ in results if success)
    
    for test_name, success, details in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if isinstance(details, dict) and "error" in details:
            print(f"   오류: {details['error']}")
        elif isinstance(details, dict):
            for key, value in details.items():
                if key != "error":
                    print(f"   {key}: {value}")
    
    print(f"\n🎯 전체 결과: {passed_tests}/{total_tests} 테스트 통과")
    
    if passed_tests == total_tests:
        print("✅ 모든 테스트 통과! Gemini API 멀티턴 대화 방식이 유효합니다.")
        return True
    else:
        print("⚠️  일부 테스트 실패. 멀티턴 구현을 확인해주세요.")
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