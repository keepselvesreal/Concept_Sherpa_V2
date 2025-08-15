"""
생성 시간: 2025-08-15 16:09:50
핵심 내용: 전체 시스템 테스트 - 문서 파싱부터 DB 저장까지
상세 내용:
    - 문서 파싱 테스트
    - DB 연결 및 저장 테스트
    - 각 임베딩 테이블 구조 확인
상태: 
주소: test_full_system
참조: neon_db_v2
"""

from neon_db_v2 import NeonVectorDBV2, DocumentParser

def main():
    print("=== 전체 시스템 테스트 ===")
    
    try:
        # 1. 문서 파싱 테스트
        print("\n1. 문서 파싱 중...")
        doc_path = "00_lev0_gpt_5_agentic_coding_with_claude_code_info.md"
        parsed_doc = DocumentParser.parse_document(doc_path)
        
        print(f"✓ 파싱 완료")
        print(f"  - 제목: {parsed_doc['title']}")
        print(f"  - 핵심 내용: {len(parsed_doc['core_content'])} 문자")
        print(f"  - 상세 핵심: {len(parsed_doc['detailed_core'])} 문자")
        print(f"  - 주요 화제: {len(parsed_doc['main_topics'])} 문자")
        print(f"  - 부차 화제: {len(parsed_doc['sub_topics'])} 문자")
        
        # 2. DB 연결 테스트
        print("\n2. DB 연결 중...")
        db = NeonVectorDBV2()
        print("✓ DB 연결 성공")
        
        # 3. 문서 저장 테스트
        print("\n3. 문서 저장 중...")
        doc_id = "test_doc_001"
        
        # 전체 추출 섹션을 extracted_info로 구성
        extracted_sections = [
            f"## 핵심 내용\n{parsed_doc['core_content']}",
            f"## 상세 핵심 내용\n{parsed_doc['detailed_core']}",
            f"## 주요 화제\n{parsed_doc['main_topics']}",
            f"## 부차 화제\n{parsed_doc['sub_topics']}"
        ]
        extracted_info = "\n\n".join(extracted_sections)
        
        db.insert_document(
            doc_id=doc_id,
            title=parsed_doc['title'],
            extracted_info=extracted_info,
            content=parsed_doc['content'],
            child_doc_ids=parsed_doc['child_doc_ids']
        )
        print(f"✓ 문서 저장 완료: {doc_id}")
        
        # 4. 임베딩 데이터 저장 테스트 (더미 임베딩)
        print("\n4. 임베딩 저장 테스트...")
        dummy_embedding = [0.1] * 384  # 384차원 더미 임베딩
        
        embedding_data = [
            ("core_content_embeddings", "core_001", parsed_doc['core_content']),
            ("detailed_core_embeddings", "detail_001", parsed_doc['detailed_core']),
            ("main_topic_embeddings", "main_001", parsed_doc['main_topics']),
            ("sub_topic_embeddings", "sub_001", parsed_doc['sub_topics'])
        ]
        
        for table_name, embedding_id, content in embedding_data:
            if content.strip():  # 내용이 있는 경우만 저장
                metadata = {
                    "section_type": table_name.replace("_embeddings", ""),
                    "language": "mixed",
                    "file_name": parsed_doc['title']
                }
                
                db.insert_embedding(
                    table_name=table_name,
                    embedding_id=embedding_id,
                    embedding=dummy_embedding,
                    document_id=doc_id,
                    metadata=metadata
                )
                print(f"  ✓ {table_name}: {embedding_id}")
        
        # 5. 데이터 확인
        print("\n5. 저장된 데이터 확인...")
        stats = db.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 6. 문서 조회 테스트
        print("\n6. 문서 조회 테스트...")
        retrieved_doc = db.get_document_by_id(doc_id)
        if retrieved_doc:
            print(f"✓ 문서 조회 성공: {retrieved_doc['title']}")
            print(f"  추출 정보 길이: {len(retrieved_doc['extracted_info'])} 문자")
        
        # 7. 검색 테스트 (더미 쿼리)
        print("\n7. 임베딩 검색 테스트...")
        dummy_query = [0.1] * 384
        
        for table_name in ["core_content_embeddings", "detailed_core_embeddings"]:
            results = db.search_embeddings(table_name, dummy_query, n_results=1)
            if results:
                print(f"  ✓ {table_name}: {len(results)}개 결과")
        
        db.close()
        print("\n✅ 전체 시스템 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()