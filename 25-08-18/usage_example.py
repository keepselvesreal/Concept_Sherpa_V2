"""
생성 시간: 2025-08-18 15:16:30 KST
핵심 내용: Claude 응답 생성기 사용 예제
상세 내용:
    - 기본 사용법 예제 (라인 20-45)
    - 검색 시스템과 통합 사용법 (라인 47-85)
    - 다양한 프롬프트 스타일 예제 (라인 87-130)
상태: 
주소: usage_example
참조: claude_response_generator, document_search_engine
"""

import asyncio
from claude_response_generator import ClaudeResponseGenerator

async def basic_usage_example():
    """기본 사용법 예제"""
    print("=== 기본 사용법 예제 ===")
    
    generator = ClaudeResponseGenerator()
    
    # 예제 데이터
    instructions = """
    사용자의 질문에 대해 제공된 문서를 바탕으로 정확한 답변을 생성하세요.
    답변은 한국어로 작성하고, 구체적인 예시를 포함해주세요.
    """
    
    query = "JSON Schema의 장점은 무엇인가요?"
    
    documents = """
    JSON Schema는 데이터 유효성 검사를 위한 강력한 도구입니다.
    주요 장점:
    1. 데이터 구조 명세화
    2. 런타임 유효성 검사
    3. API 문서화 자동화
    4. 클라이언트-서버 간 계약 정의
    """
    
    result = await generator.generate_response(instructions, query, documents)
    
    print(f"성공: {result.success}")
    print(f"처리 시간: {result.processing_time:.2f}초")
    print(f"응답:\n{result.content}")
    print()

async def search_integration_example():
    """검색 시스템과 통합 사용법 예제"""
    print("=== 검색 시스템 통합 예제 ===")
    
    generator = ClaudeResponseGenerator()
    
    # 검색 결과를 받았다고 가정
    search_query = "함수형 프로그래밍의 특징"
    search_results = """
    함수형 프로그래밍은 다음과 같은 특징을 가집니다:
    
    1. 순수 함수(Pure Functions)
    - 동일한 입력에 대해 항상 동일한 출력 반환
    - 부작용(side effect) 없음
    
    2. 불변성(Immutability)
    - 데이터를 변경하지 않고 새로운 데이터 생성
    
    3. 고차 함수(Higher-Order Functions)
    - 함수를 인자로 받거나 함수를 반환하는 함수
    
    4. 합성(Composition)
    - 작은 함수들을 조합하여 복잡한 기능 구현
    """
    
    instructions = """
    검색된 문서 내용을 바탕으로 사용자 질문에 답변하세요.
    답변 형식:
    1. 핵심 개념 요약
    2. 각 특징의 구체적 설명
    3. 실무에서의 활용 방안
    """
    
    result = await generator.generate_response(
        instructions, search_query, search_results
    )
    
    print(f"질의: {search_query}")
    print(f"처리 시간: {result.processing_time:.2f}초")
    print(f"응답:\n{result.content}")
    print()

async def prompt_style_examples():
    """다양한 프롬프트 스타일 예제"""
    print("=== 다양한 프롬프트 스타일 예제 ===")
    
    generator = ClaudeResponseGenerator()
    
    # 문서 내용
    documents = """
    리팩토링의 주요 기법들:
    1. 메서드 추출 (Extract Method)
    2. 변수명 변경 (Rename Variable)
    3. 조건문 간소화 (Simplify Conditional)
    4. 중복 코드 제거 (Remove Duplication)
    """
    
    query = "코드 리팩토링 시 주의사항은?"
    
    # 스타일 1: 간결한 답변
    simple_instructions = "제공된 문서를 바탕으로 간단명료하게 답변하세요."
    
    # 스타일 2: 상세한 답변
    detailed_instructions = """
    다음 형식으로 상세한 답변을 작성하세요:
    1. 개요
    2. 주요 주의사항 (번호 매기기)
    3. 실무 팁
    4. 요약
    """
    
    # 스타일 3: 실무 중심 답변
    practical_instructions = """
    개발자에게 실무적으로 도움이 되는 관점에서 답변하세요.
    구체적인 예시와 경험담을 포함해주세요.
    """
    
    styles = [
        ("간결한 스타일", simple_instructions),
        ("상세한 스타일", detailed_instructions),
        ("실무 중심 스타일", practical_instructions)
    ]
    
    for style_name, instructions in styles:
        print(f"--- {style_name} ---")
        result = await generator.generate_response(instructions, query, documents)
        print(f"응답 길이: {len(result.content)}자")
        print(f"처리 시간: {result.processing_time:.2f}초")
        print(f"응답:\n{result.content[:200]}...")
        print()

async def main():
    """모든 예제 실행"""
    print("🚀 Claude 응답 생성기 사용 예제 모음\n")
    
    await basic_usage_example()
    await search_integration_example()
    await prompt_style_examples()
    
    print("✅ 모든 예제 실행 완료!")

if __name__ == "__main__":
    asyncio.run(main())