"""
# 목차
- 생성 시간: 2025년 8월 24일 23:50:12 KST
- 핵심 내용: 수정된 individual_answers 함수 테스트 스크립트
- 상세 내용:
    - test_individual_answers 함수 (라인 17-42): individual_answers 함수의 새로운 응답 형식 테스트
- 상태: active
- 주소: test_individual_answers
- 참조: document_query_processor.py의 수정된 individual_answers 함수 테스트
"""

import asyncio
from document_query_processor import DocumentQueryProcessor

async def test_individual_answers():
    """수정된 individual_answers 함수 테스트"""
    processor = DocumentQueryProcessor()
    
    # 테스트 데이터
    test_prompt = "다음 참고 문서를 바탕으로 질의에 대해 간결하고 정확하게 답변해주세요."
    test_query = "이 문서의 핵심 내용을 3줄로 요약해주세요."
    test_documents = [
        "첫 번째 문서: 파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다. 데이터 분석과 웹 개발에 널리 사용됩니다.",
        "두 번째 문서: 자바스크립트는 웹 개발에 필수적인 언어입니다. 프론트엔드와 백엔드 모두에서 사용할 수 있습니다.",
        "세 번째 문서: 데이터 분석에는 R과 파이썬이 널리 사용됩니다. 머신러닝과 통계 분석에 특화되어 있습니다."
    ]
    test_paths = [
        "/home/nadle/projects/test/python_doc.md",
        "/home/nadle/projects/test/javascript_doc.md", 
        "/home/nadle/projects/test/data_analysis_doc.md"
    ]
    
    print("=== Individual 답변 테스트 (수정된 형식) ===\n")
    print(f"질의: {test_query}")
    print(f"문서 개수: {len(test_documents)}개\n")
    
    try:
        results = await processor.individual_answers(
            prompt=test_prompt,
            query=test_query,
            document_list=test_documents,
            document_paths=test_paths
        )
        
        print("Individual 답변 생성 완료!")
        print(f"총 {len(results)}개 답변 생성\n")
        
        for i, result in enumerate(results):
            print(f"=== 문서 {i+1} 결과 ===")
            print(f"세션 ID: {result['session_id']}")
            print(f"질의 ID: {result['query_id']}")
            print(f"현재 질의: {result['current_query']}")
            print(f"문서 경로: {result['document_path']}")
            print(f"성공 여부: {result['success']}")
            print(f"소요 시간: {result['elapsed_time']}초")
            print(f"타임스탬프: {result['timestamp']}")
            print(f"저장된 파일: {result['saved_file']}")
            if result['success'] and result['answer']:
                print(f"답변 (처음 100자): {result['answer'][:100]}...")
            if 'error' in result:
                print(f"오류: {result['error']}")
            print()
        
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_individual_answers())