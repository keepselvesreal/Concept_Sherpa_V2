"""
# 목차
- 생성 시간: 2025년 8월 24일 20:35:21 KST
- 핵심 내용: DOP.md 파일을 사용한 collective_answer 테스트 스크립트
- 상세 내용:
    - test_dop_collective 함수 (라인 17-42): DOP 문서에 대한 2개 질문 테스트
    - 질문 1: DOP의 핵심 원리와 장점 요약
    - 질문 2: DOP와 OOP의 차이점 분석
- 상태: active
- 주소: test_dop_queries
- 참조: document_query_processor.py의 collective_answer 함수 사용
"""

import asyncio
from document_query_processor import DocumentQueryProcessor

async def test_dop_collective():
    """DOP.md 파일로 collective 답변 테스트"""
    processor = DocumentQueryProcessor()
    
    # DOP.md 파일 읽기
    dop_file_path = "/home/nadle/projects/Concept_Sherpa_V2/25-08-24/DOP.md"
    
    with open(dop_file_path, 'r', encoding='utf-8') as f:
        dop_content = f.read()
    
    # 테스트용 프롬프트
    prompt = "다음 참고 문서를 바탕으로 질의에 대해 정확하고 상세하게 답변해주세요."
    
    # 첫 번째 질문
    query1 = "데이터 지향 프로그래밍(DOP)의 핵심 원리 3가지와 주요 장점들을 설명해주세요."
    
    print("=== DOP 문서 collective 답변 테스트 ===\n")
    print("첫 번째 질문:", query1)
    
    result1 = await processor.collective_answer(
        prompt=prompt,
        query=query1,
        document_list=[dop_content],
        document_paths=[dop_file_path]
    )
    
    print(f"답변 생성 완료: {result1['success']}")
    print(f"소요 시간: {result1['elapsed_time']}초")
    print(f"세션 ID: {result1['session_id']}")
    print(f"질의 ID: {result1['query_id']}")
    print(f"저장된 파일: {result1['saved_file']}\n")
    
    # 두 번째 질문 (같은 세션)
    query2 = "DOP와 객체지향 프로그래밍(OOP)의 주요 차이점을 비교하고, 각각 언제 사용하는 것이 좋을지 설명해주세요."
    
    print("두 번째 질문:", query2)
    
    result2 = await processor.collective_answer(
        prompt=prompt,
        query=query2,
        document_list=[dop_content],
        document_paths=[dop_file_path]
    )
    
    print(f"답변 생성 완료: {result2['success']}")
    print(f"소요 시간: {result2['elapsed_time']}초")
    print(f"세션 ID: {result2['session_id']}")
    print(f"질의 ID: {result2['query_id']}")
    print(f"저장된 파일: {result2['saved_file']}\n")
    
    print("=== 세션 요약 ===")
    print(f"세션 ID: {result2['session_id']}")
    print(f"총 질의 수: {result2['query_id']}")
    print(f"세션 파일: collective_answer_{result2['session_id']}.json")

if __name__ == "__main__":
    asyncio.run(test_dop_collective())