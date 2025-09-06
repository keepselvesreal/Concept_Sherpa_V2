"""
ChromaDB에서 Neon PostgreSQL로 데이터 마이그레이션 스크립트
벡터 임베딩과 메타데이터를 함께 이전
"""

from vector_db_v2 import VectorDBManagerV2
from neon_vector_db import NeonVectorDB
import json
import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaToNeonMigrator:
    """
    ChromaDB에서 Neon PostgreSQL로 데이터 마이그레이션
    """
    
    def __init__(self, chroma_db_path: str = "./chroma_db_v2", 
                 neon_connection_string: str = None):
        """
        마이그레이터 초기화
        
        Args:
            chroma_db_path: ChromaDB 경로
            neon_connection_string: Neon 연결 문자열
        """
        self.chroma_db_path = chroma_db_path
        
        # ChromaDB 및 Neon DB 초기화
        try:
            self.chroma_db = VectorDBManagerV2(chroma_db_path)
            self.neon_db = NeonVectorDB(neon_connection_string)
            logger.info("데이터베이스 연결 초기화 완료")
        except Exception as e:
            logger.error(f"데이터베이스 초기화 실패: {e}")
            raise
    
    def migrate_core_content(self) -> int:
        """
        핵심 내용 데이터 마이그레이션
        
        Returns:
            마이그레이션된 항목 수
        """
        logger.info("핵심 내용 마이그레이션 시작")
        migrated_count = 0
        
        try:
            # ChromaDB에서 모든 핵심 내용 데이터 조회
            core_data = self._get_all_chroma_data(self.chroma_db.core_collection)
            
            for item in core_data:
                try:
                    # Neon에 데이터 삽입
                    self.neon_db.insert_core_content(
                        id=item['id'],
                        embedding=item['embedding'],
                        document=item['document'],
                        metadata=item['metadata'],
                        doc_type=item['metadata'].get('doc_type', 'unknown')
                    )
                    
                    migrated_count += 1
                    logger.info(f"핵심 내용 마이그레이션: {item['id']}")
                    
                except Exception as e:
                    logger.error(f"핵심 내용 마이그레이션 실패 ({item['id']}): {e}")
                    continue
            
            logger.info(f"핵심 내용 마이그레이션 완료: {migrated_count}개 항목")
            return migrated_count
            
        except Exception as e:
            logger.error(f"핵심 내용 마이그레이션 실패: {e}")
            raise
    
    def migrate_detailed_content(self) -> int:
        """
        상세 내용 데이터 마이그레이션
        
        Returns:
            마이그레이션된 항목 수
        """
        logger.info("상세 내용 마이그레이션 시작")
        migrated_count = 0
        
        try:
            # ChromaDB에서 모든 상세 내용 데이터 조회
            detailed_data = self._get_all_chroma_data(self.chroma_db.detailed_collection)
            
            for item in detailed_data:
                try:
                    # Neon에 데이터 삽입
                    self.neon_db.insert_detailed_content(
                        id=item['id'],
                        embedding=item['embedding'],
                        core_ref=item['metadata'].get('core_ref', ''),
                        metadata=item['metadata']
                    )
                    
                    migrated_count += 1
                    logger.info(f"상세 내용 마이그레이션: {item['id']}")
                    
                except Exception as e:
                    logger.error(f"상세 내용 마이그레이션 실패 ({item['id']}): {e}")
                    continue
            
            logger.info(f"상세 내용 마이그레이션 완료: {migrated_count}개 항목")
            return migrated_count
            
        except Exception as e:
            logger.error(f"상세 내용 마이그레이션 실패: {e}")
            raise
    
    def _get_all_chroma_data(self, collection) -> List[Dict[str, Any]]:
        """
        ChromaDB 컬렉션에서 모든 데이터 조회
        
        Args:
            collection: ChromaDB 컬렉션
            
        Returns:
            모든 데이터 리스트
        """
        try:
            # 컬렉션의 모든 데이터 조회
            all_data = collection.get(
                include=['embeddings', 'documents', 'metadatas']
            )
            
            # 데이터 구조 변환
            formatted_data = []
            if all_data['ids'] is not None and len(all_data['ids']) > 0:
                for i in range(len(all_data['ids'])):
                    embedding = []
                    if all_data['embeddings'] is not None and len(all_data['embeddings']) > i:
                        raw_embedding = all_data['embeddings'][i]
                        # numpy.ndarray를 list로 변환
                        if hasattr(raw_embedding, 'tolist'):
                            embedding = raw_embedding.tolist()
                        else:
                            embedding = list(raw_embedding)
                    
                    document = ""
                    if all_data['documents'] is not None and len(all_data['documents']) > i:
                        document = all_data['documents'][i]
                    
                    metadata = {}
                    if all_data['metadatas'] is not None and len(all_data['metadatas']) > i:
                        metadata = all_data['metadatas'][i]
                    
                    formatted_data.append({
                        'id': all_data['ids'][i],
                        'embedding': embedding,
                        'document': document,
                        'metadata': metadata
                    })
            
            logger.info(f"ChromaDB에서 {len(formatted_data)}개 항목 조회")
            return formatted_data
            
        except Exception as e:
            logger.error(f"ChromaDB 데이터 조회 실패: {e}")
            raise
    
    def verify_migration(self) -> Dict[str, Any]:
        """
        마이그레이션 결과 검증
        
        Returns:
            검증 결과 딕셔너리
        """
        logger.info("마이그레이션 검증 시작")
        
        try:
            # ChromaDB 통계
            chroma_stats = self.chroma_db.get_collection_stats()
            
            # Neon 통계
            neon_stats = self.neon_db.get_statistics()
            
            # 검증 결과
            verification_result = {
                'chroma_stats': chroma_stats,
                'neon_stats': neon_stats,
                'core_content_match': chroma_stats['core_content_count'] == neon_stats['core_content_count'],
                'detailed_content_match': chroma_stats['detailed_content_count'] == neon_stats['detailed_content_count'],
                'total_match': chroma_stats['total_count'] == neon_stats['total_count']
            }
            
            logger.info(f"마이그레이션 검증 완료: {verification_result}")
            return verification_result
            
        except Exception as e:
            logger.error(f"마이그레이션 검증 실패: {e}")
            return {'error': str(e)}
    
    def run_full_migration(self, clear_neon_first: bool = True) -> Dict[str, Any]:
        """
        전체 마이그레이션 실행
        
        Args:
            clear_neon_first: Neon DB를 먼저 비울지 여부
            
        Returns:
            마이그레이션 결과
        """
        logger.info("전체 마이그레이션 시작")
        
        try:
            # Neon DB 초기화 (선택적)
            if clear_neon_first:
                logger.info("Neon DB 데이터 초기화")
                self.neon_db.clear_all_data()
            
            # 핵심 내용 마이그레이션
            core_migrated = self.migrate_core_content()
            
            # 상세 내용 마이그레이션
            detailed_migrated = self.migrate_detailed_content()
            
            # 마이그레이션 검증
            verification = self.verify_migration()
            
            result = {
                'success': True,
                'core_migrated': core_migrated,
                'detailed_migrated': detailed_migrated,
                'total_migrated': core_migrated + detailed_migrated,
                'verification': verification
            }
            
            logger.info(f"전체 마이그레이션 완료: {result}")
            return result
            
        except Exception as e:
            logger.error(f"전체 마이그레이션 실패: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def close(self):
        """데이터베이스 연결 종료"""
        try:
            self.chroma_db.close()
            self.neon_db.close()
            logger.info("모든 데이터베이스 연결 종료")
        except Exception as e:
            logger.error(f"연결 종료 실패: {e}")

def main():
    """메인 실행 함수"""
    print("ChromaDB → Neon PostgreSQL 마이그레이션 시작")
    
    try:
        # 마이그레이터 생성
        migrator = ChromaToNeonMigrator()
        
        # 현재 상태 확인
        print("\n=== 마이그레이션 전 상태 ===")
        chroma_stats = migrator.chroma_db.get_collection_stats()
        neon_stats = migrator.neon_db.get_statistics()
        
        print(f"ChromaDB - 핵심: {chroma_stats['core_content_count']}, 상세: {chroma_stats['detailed_content_count']}")
        print(f"Neon DB - 핵심: {neon_stats['core_content_count']}, 상세: {neon_stats['detailed_content_count']}")
        
        # 전체 마이그레이션 실행
        result = migrator.run_full_migration(clear_neon_first=True)
        
        # 결과 출력
        print("\n=== 마이그레이션 결과 ===")
        if result['success']:
            print(f"성공! 총 {result['total_migrated']}개 항목 마이그레이션")
            print(f"- 핵심 내용: {result['core_migrated']}개")
            print(f"- 상세 내용: {result['detailed_migrated']}개")
            
            verification = result['verification']
            if verification['total_match']:
                print("✅ 데이터 검증 성공: 모든 항목이 정확히 마이그레이션됨")
            else:
                print("⚠️ 데이터 검증 경고: 일부 항목이 누락될 수 있음")
        else:
            print(f"실패: {result['error']}")
        
        # 연결 종료
        migrator.close()
        
    except Exception as e:
        print(f"마이그레이션 실행 실패: {e}")
        print("NEON_DATABASE_URL 환경변수가 설정되었는지 확인하세요.")

if __name__ == "__main__":
    main()