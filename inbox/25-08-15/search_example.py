"""
생성 시간: 2025-08-15 16:45:02
핵심 내용: 벡터 검색 시스템 사용법 예시 및 테스트 스크립트
상세 내용:
    - search_with_different_providers 함수(라인 22-40): 다양한 임베딩 프로바이더 테스트
    - interactive_search 함수(라인 42-63): 대화형 검색 인터페이스
    - test_search_system 함수(라인 65-88): 자동화된 검색 테스트
    - main 함수(라인 90-110): 메인 실행 로직
상태: 
주소: search_example
참조: vector_search_system
"""

import sys
import os
from vector_search_system import VectorSearchSystem, create_embedding_provider
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_with_question(question: str, provider_type: str = "sentence-transformers"):
    """
    특정 질문으로 검색 수행
    
    Args:
        question: 검색할 질문
        provider_type: 임베딩 프로바이더 타입
    """
    try:
        # 임베딩 프로바이더 생성
        embedding_provider = create_embedding_provider(provider_type)
        
        # 검색 시스템 초기화
        search_system = VectorSearchSystem(embedding_provider, similarity_threshold=0.8)
        
        print(f"\n🔍 질문: {question}")
        print(f"📊 프로바이더: {provider_type}")
        print("=" * 50)
        
        # 검색 수행
        results = search_system.search_documents(question, max_results=3)
        
        # 결과 출력
        formatted_response = search_system.format_response(results)
        print(formatted_response)
        
        # 데이터베이스 연결 종료
        search_system.db.close()
        
    except Exception as e:
        logger.error(f"검색 실패: {e}")
        print(f"❌ 오류 발생: {e}")

def interactive_search():
    """
    대화형 검색 인터페이스
    """
    print("🤖 벡터 검색 시스템에 오신 것을 환영합니다!")
    print("👆 'quit' 또는 'exit'를 입력하면 종료됩니다.")
    print()
    
    while True:
        try:
            question = input("❓ 질문을 입력하세요: ").strip()
            
            if question.lower() in ['quit', 'exit', '종료']:
                print("👋 검색을 종료합니다.")
                break
            
            if not question:
                print("⚠️ 질문을 입력해주세요.")
                continue
            
            search_with_question(question)
            
        except KeyboardInterrupt:
            print("\n\n👋 검색을 종료합니다.")
            break
        except Exception as e:
            logger.error(f"오류 발생: {e}")
            print(f"❌ 오류가 발생했습니다: {e}")

def test_search_system():
    """
    검색 시스템 테스트
    """
    print("🧪 검색 시스템 테스트 시작")
    print("=" * 50)
    
    # 테스트 질문들
    test_questions = [
        "GPT-5와 Claude의 성능 비교는 어떻게 되나요?",
        "에이전트 코딩이란 무엇인가요?", 
        "로컬 AI 모델의 성능은 어떤가요?",
        "비용 효율적인 AI 모델 선택 방법은?",
        "프롬프트 오케스트레이션 기법에 대해 알려주세요"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 테스트 {i}/{len(test_questions)}")
        search_with_question(question)
        
        # 사용자가 중간에 중단할 수 있도록
        if i < len(test_questions):
            input("\n⏭️ 다음 테스트로 넘어가려면 Enter를 누르세요...")

def main():
    """
    메인 함수
    """
    print("🚀 벡터 검색 시스템")
    print("=" * 30)
    print("1. 대화형 검색")
    print("2. 테스트 실행")
    print("3. 단일 질문 검색")
    print()
    
    try:
        choice = input("선택하세요 (1-3): ").strip()
        
        if choice == "1":
            interactive_search()
        elif choice == "2":
            test_search_system()
        elif choice == "3":
            question = input("질문을 입력하세요: ").strip()
            if question:
                search_with_question(question)
            else:
                print("⚠️ 질문을 입력해주세요.")
        else:
            print("❌ 잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        logger.error(f"실행 오류: {e}")
        print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()