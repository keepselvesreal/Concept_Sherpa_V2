"""
Knowledge Sherpa 데모 스크립트
미리 정의된 질문들로 시스템 기능을 보여주는 데모
"""

from knowledge_chat import KnowledgeChat
import time

def demo_conversation():
    """데모 대화 실행"""
    print("🤖 Knowledge Sherpa 데모 시작!")
    print("=" * 60)
    
    # 시스템 초기화
    chat = KnowledgeChat()
    
    # 데모 질문들
    demo_questions = [
        {
            "question": "OOP의 주요 문제점은 무엇인가요?",
            "search_type": "both",
            "description": "OOP 복잡성에 대한 종합적 검색"
        },
        {
            "question": "클래스 설계에서 어떤 어려움이 있나요?", 
            "search_type": "core",
            "description": "핵심 내용만 검색"
        },
        {
            "question": "데이터와 코드를 분리하면 어떤 장점이 있나요?",
            "search_type": "detailed", 
            "description": "상세 분석만 검색"
        },
        {
            "question": "상속 구조가 복잡해지는 이유는?",
            "search_type": "both",
            "description": "전체 검색으로 심층 분석"
        }
    ]
    
    try:
        for i, demo in enumerate(demo_questions, 1):
            print(f"\n{'='*20} 데모 {i} {'='*20}")
            print(f"📝 {demo['description']}")
            print(f"❓ 질문: {demo['question']}")
            print("\n🔍 검색 중...")
            
            # 시뮬레이션을 위한 잠시 대기
            time.sleep(1)
            
            # 답변 생성
            answer = chat.ask(
                demo['question'], 
                search_type=demo['search_type'],
                max_results=2
            )
            
            print(answer)
            print("\n" + "─" * 60)
        
        # 시스템 통계 및 이력 표시
        print(f"\n{'='*20} 시스템 정보 {'='*20}")
        print(chat.show_stats())
        
        print(f"\n{'='*20} 대화 이력 {'='*20}")
        print(chat.get_history())
        
    except Exception as e:
        print(f"❌ 데모 실행 중 오류: {e}")
    
    finally:
        chat.close()
        print("\n👋 데모를 종료합니다.")

if __name__ == "__main__":
    demo_conversation()