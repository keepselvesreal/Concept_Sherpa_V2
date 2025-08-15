"""
생성 시간: 2025-08-15 16:09:50
핵심 내용: 실제 임베딩을 사용한 전체 시스템 테스트
상세 내용:
    - sentence-transformers 모델 사용
    - 실제 임베딩 생성 및 저장
    - 의미 기반 검색 테스트
상태: 
주소: test_real_embeddings
참조: neon_db_v2
"""

from neon_db_v2 import NeonVectorDBV2

def main():
    print("=== 실제 임베딩을 사용한 시스템 테스트 ===")
    
    try:
        # DB 초기화 (임베딩 모델 포함)
        print("\n1. DB 및 임베딩 모델 초기화...")
        db = NeonVectorDBV2()
        print("✓ 초기화 완료")
        
        # 문서 처리 (실제 임베딩 생성)
        print("\n2. 문서 처리 및 임베딩 생성...")
        doc_path = "00_lev0_gpt_5_agentic_coding_with_claude_code_info.md"
        doc_id = db.process_document_file(doc_path, generate_embeddings=True)
        print(f"✓ 문서 처리 완료: {doc_id}")
        
        # 통계 확인
        print("\n3. 저장된 데이터 확인...")
        stats = db.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 실제 쿼리로 검색 테스트
        print("\n4. 의미 기반 검색 테스트...")
        
        test_queries = [
            "GPT-5와 Opus 4.1의 성능 비교",
            "에이전트 코딩이란?",
            "비용 효율성 분석",
            "로컬 모델 성능"
        ]
        
        for query in test_queries:
            print(f"\n쿼리: '{query}'")
            
            # 쿼리 임베딩 생성
            query_embeddings = db.generate_embeddings([query])
            if query_embeddings:
                query_embedding = query_embeddings[0]
                
                # 각 테이블에서 검색
                tables = [
                    ("core_content_embeddings", "핵심 내용"),
                    ("detailed_core_embeddings", "상세 핵심"),
                    ("main_topic_embeddings", "주요 화제"),
                    ("sub_topic_embeddings", "부차 화제")
                ]
                
                for table_name, table_desc in tables:
                    results = db.search_embeddings(table_name, query_embedding, n_results=1)
                    if results:
                        result = results[0]
                        distance = result['distance']
                        print(f"  {table_desc}: 유사도 {1-distance:.3f} (거리: {distance:.3f})")
                    else:
                        print(f"  {table_desc}: 결과 없음")
        
        db.close()
        print("\n✅ 실제 임베딩 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()