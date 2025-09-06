"""
벡터 검색 기능 테스트 스크립트
핵심 내용 검색과 상세 내용 검색을 테스트하고 원문 접근을 확인
"""

from embedding_service_v2 import get_embedding_service
from vector_db_v2 import VectorDBManagerV2
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchTester:
    """
    검색 기능 테스트 클래스
    """
    
    def __init__(self, db_path: str = "./chroma_db_v2"):
        """
        검색 테스터 초기화
        
        Args:
            db_path: 벡터 DB 경로
        """
        self.embedding_service = get_embedding_service()
        self.db_manager = VectorDBManagerV2(db_path)
        
        logger.info("검색 테스터 초기화 완료")
    
    def test_core_content_search(self, query: str, n_results: int = 3):
        """
        핵심 내용 검색 테스트
        
        Args:
            query: 검색 쿼리
            n_results: 반환할 결과 개수
        """
        print(f"\n=== 핵심 내용 검색: '{query}' ===")
        
        try:
            # 쿼리 임베딩 생성
            query_embedding = self.embedding_service.create_embedding(query)
            
            # 검색 실행
            results = self.db_manager.search_core_content(query_embedding, n_results)
            
            # 결과 출력
            print(f"검색 결과: {results['total_results']}개")
            
            for i, result in enumerate(results['results'], 1):
                print(f"\n--- 결과 {i} ---")
                print(f"ID: {result['id']}")
                print(f"유사도 거리: {result['distance']:.4f}")
                print(f"메타데이터: {result['metadata']}")
                
                # document 내용 출력 (구조에 따라 다르게 처리)
                if 'document' in result:
                    doc = result['document']
                    if doc.startswith('{'):  # JSON 형태인 경우
                        try:
                            doc_obj = json.loads(doc)
                            print(f"문서 타입: {doc_obj.get('type', 'unknown')}")
                            print(f"제목: {doc_obj.get('title', 'N/A')}")
                            print(f"요약: {doc_obj.get('content_summary', 'N/A')}")
                            if 'composed_of' in doc_obj:
                                print(f"구성 요소: {doc_obj['composed_of']}")
                        except:
                            print(f"문서 (처음 200자): {doc[:200]}...")
                    else:  # 일반 텍스트인 경우
                        print(f"문서 (처음 200자): {doc[:200]}...")
                        
        except Exception as e:
            print(f"핵심 내용 검색 실패: {e}")
    
    def test_detailed_content_search(self, query: str, n_results: int = 3):
        """
        상세 내용 검색 테스트
        
        Args:
            query: 검색 쿼리  
            n_results: 반환할 결과 개수
        """
        print(f"\n=== 상세 내용 검색: '{query}' ===")
        
        try:
            # 쿼리 임베딩 생성
            query_embedding = self.embedding_service.create_embedding(query)
            
            # 검색 실행
            results = self.db_manager.search_detailed_content(query_embedding, n_results)
            
            # 결과 출력
            print(f"검색 결과: {results['total_results']}개")
            
            for i, result in enumerate(results['results'], 1):
                print(f"\n--- 결과 {i} ---")
                print(f"ID: {result['id']}")
                print(f"유사도 거리: {result['distance']:.4f}")
                print(f"메타데이터: {result['metadata']}")
                
                # core_ref를 통해 원문 접근 테스트
                if 'core_ref' in result['metadata']:
                    core_ref = result['metadata']['core_ref']
                    print(f"원문 참조: {core_ref}")
                    
                    # 원문 조회
                    original_content = self.db_manager.get_core_content_by_id(core_ref)
                    if original_content:
                        print(f"원문 찾음: {original_content['id']}")
                        doc = original_content['document']
                        if isinstance(doc, str) and len(doc) > 200:
                            print(f"원문 (처음 200자): {doc[:200]}...")
                        else:
                            print(f"원문: {doc}")
                    else:
                        print(f"원문을 찾을 수 없음: {core_ref}")
                        
        except Exception as e:
            print(f"상세 내용 검색 실패: {e}")
    
    def test_combined_search(self, query: str):
        """
        핵심 내용과 상세 내용을 모두 검색하여 비교
        
        Args:
            query: 검색 쿼리
        """
        print(f"\n=== 통합 검색 비교: '{query}' ===")
        
        try:
            # 쿼리 임베딩 생성
            query_embedding = self.embedding_service.create_embedding(query)
            
            # 핵심 내용 검색
            core_results = self.db_manager.search_core_content(query_embedding, 2)
            
            # 상세 내용 검색  
            detailed_results = self.db_manager.search_detailed_content(query_embedding, 2)
            
            print(f"핵심 내용 검색 결과: {core_results['total_results']}개")
            for result in core_results['results']:
                print(f"  - {result['id']} (거리: {result['distance']:.4f})")
            
            print(f"상세 내용 검색 결과: {detailed_results['total_results']}개")
            for result in detailed_results['results']:
                core_ref = result['metadata'].get('core_ref', 'N/A')
                print(f"  - {result['id']} → {core_ref} (거리: {result['distance']:.4f})")
                
        except Exception as e:
            print(f"통합 검색 실패: {e}")
    
    def show_collection_stats(self):
        """컬렉션 통계 정보 출력"""
        stats = self.db_manager.get_collection_stats()
        print("\n=== 벡터 DB 통계 ===")
        print(f"핵심 내용 개수: {stats['core_content_count']}")
        print(f"상세 내용 개수: {stats['detailed_content_count']}")
        print(f"전체 개수: {stats['total_count']}")
        print(f"DB 경로: {stats['db_path']}")

def main():
    """메인 테스트 함수"""
    print("벡터 검색 기능 테스트 시작")
    
    try:
        # 테스터 초기화
        tester = SearchTester()
        
        # 컬렉션 통계 확인
        tester.show_collection_stats()
        
        # 테스트 쿼리들
        test_queries = [
            "OOP 복잡성의 원인은 무엇인가?",
            "클래스 설계 과정에서 발생하는 문제점",
            "데이터와 코드의 분리가 왜 중요한가?",
            "상속 구조의 복잡성 문제"
        ]
        
        for query in test_queries:
            # 핵심 내용 검색 테스트
            tester.test_core_content_search(query)
            
            # 상세 내용 검색 테스트
            tester.test_detailed_content_search(query)
            
            # 통합 검색 비교
            tester.test_combined_search(query)
            
            print("\n" + "="*80)
        
        print("\n검색 기능 테스트 완료!")
        
    except Exception as e:
        logger.error(f"테스트 실행 실패: {e}")
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()