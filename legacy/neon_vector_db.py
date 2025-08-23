"""
Neon PostgreSQL + pgvector를 사용한 벡터 데이터베이스 관리 모듈
ChromaDB 데이터를 Neon으로 마이그레이션하고 벡터 검색 제공
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional, Tuple
import logging
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeonVectorDB:
    """
    Neon PostgreSQL + pgvector를 사용한 벡터 데이터베이스 관리자
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Neon 벡터 DB 관리자 초기화
        
        Args:
            connection_string: PostgreSQL 연결 문자열 (None이면 환경변수에서 로드)
        """
        self.connection_string = connection_string or os.getenv('NEON_DATABASE_URL')
        
        if not self.connection_string:
            raise ValueError("Neon 데이터베이스 연결 문자열이 필요합니다. NEON_DATABASE_URL 환경변수를 설정하세요.")
        
        self.conn = None
        self._connect()
        self._setup_database()
    
    def _connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = psycopg2.connect(self.connection_string)
            self.conn.autocommit = True
            logger.info("Neon PostgreSQL 연결 성공")
        except Exception as e:
            logger.error(f"Neon PostgreSQL 연결 실패: {e}")
            raise
    
    def _setup_database(self):
        """데이터베이스 초기 설정 (pgvector 확장 및 테이블 생성)"""
        try:
            with self.conn.cursor() as cur:
                # pgvector 확장 활성화
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                logger.info("pgvector 확장 활성화 완료")
                
                # 핵심 내용 테이블 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS core_content (
                        id VARCHAR(100) PRIMARY KEY,
                        embedding VECTOR(384),
                        document TEXT,
                        metadata JSONB,
                        doc_type VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 상세 내용 테이블 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS detailed_content (
                        id VARCHAR(100) PRIMARY KEY,
                        embedding VECTOR(384),
                        core_ref VARCHAR(100),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 벡터 검색을 위한 인덱스 생성 (HNSW 인덱스)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS core_content_embedding_idx 
                    ON core_content USING hnsw (embedding vector_cosine_ops);
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS detailed_content_embedding_idx 
                    ON detailed_content USING hnsw (embedding vector_cosine_ops);
                """)
                
                logger.info("테이블 및 인덱스 생성 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 설정 실패: {e}")
            raise
    
    def insert_core_content(self, id: str, embedding: List[float], document: str, 
                           metadata: Dict[str, Any], doc_type: str):
        """
        핵심 내용 데이터 삽입
        
        Args:
            id: 문서 ID
            embedding: 임베딩 벡터
            document: 문서 내용
            metadata: 메타데이터
            doc_type: 문서 타입
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO core_content (id, embedding, document, metadata, doc_type)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        embedding = EXCLUDED.embedding,
                        document = EXCLUDED.document,
                        metadata = EXCLUDED.metadata,
                        doc_type = EXCLUDED.doc_type,
                        created_at = CURRENT_TIMESTAMP;
                """, (id, embedding, document, json.dumps(metadata), doc_type))
                
                logger.info(f"핵심 내용 삽입 완료: {id}")
                
        except Exception as e:
            logger.error(f"핵심 내용 삽입 실패 ({id}): {e}")
            raise
    
    def insert_detailed_content(self, id: str, embedding: List[float], 
                               core_ref: str, metadata: Dict[str, Any]):
        """
        상세 내용 데이터 삽입
        
        Args:
            id: 문서 ID
            embedding: 임베딩 벡터
            core_ref: 원문 참조 ID
            metadata: 메타데이터
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO detailed_content (id, embedding, core_ref, metadata)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        embedding = EXCLUDED.embedding,
                        core_ref = EXCLUDED.core_ref,
                        metadata = EXCLUDED.metadata,
                        created_at = CURRENT_TIMESTAMP;
                """, (id, embedding, core_ref, json.dumps(metadata)))
                
                logger.info(f"상세 내용 삽입 완료: {id}")
                
        except Exception as e:
            logger.error(f"상세 내용 삽입 실패 ({id}): {e}")
            raise
    
    def search_core_content(self, query_embedding: List[float], 
                           n_results: int = 5) -> List[Dict[str, Any]]:
        """
        핵심 내용에서 벡터 유사도 검색
        
        Args:
            query_embedding: 쿼리 임베딩
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 리스트
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, document, metadata, doc_type,
                           (embedding <=> %s::vector) as distance
                    FROM core_content
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s;
                """, (query_embedding, query_embedding, n_results))
                
                results = cur.fetchall()
                
                # 결과를 딕셔너리 리스트로 변환
                formatted_results = []
                for row in results:
                    formatted_results.append({
                        'id': row['id'],
                        'document': row['document'],
                        'metadata': row['metadata'],
                        'doc_type': row['doc_type'],
                        'distance': float(row['distance'])
                    })
                
                logger.info(f"핵심 내용 검색 완료: {len(formatted_results)}개 결과")
                return formatted_results
                
        except Exception as e:
            logger.error(f"핵심 내용 검색 실패: {e}")
            raise
    
    def search_detailed_content(self, query_embedding: List[float], 
                               n_results: int = 5) -> List[Dict[str, Any]]:
        """
        상세 내용에서 벡터 유사도 검색
        
        Args:
            query_embedding: 쿼리 임베딩
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 리스트
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, core_ref, metadata,
                           (embedding <=> %s::vector) as distance
                    FROM detailed_content
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s;
                """, (query_embedding, query_embedding, n_results))
                
                results = cur.fetchall()
                
                # 결과를 딕셔너리 리스트로 변환
                formatted_results = []
                for row in results:
                    formatted_results.append({
                        'id': row['id'],
                        'core_ref': row['core_ref'],
                        'metadata': row['metadata'],
                        'distance': float(row['distance'])
                    })
                
                logger.info(f"상세 내용 검색 완료: {len(formatted_results)}개 결과")
                return formatted_results
                
        except Exception as e:
            logger.error(f"상세 내용 검색 실패: {e}")
            raise
    
    def get_core_content_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 핵심 내용 조회
        
        Args:
            id: 문서 ID
            
        Returns:
            문서 데이터 또는 None
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, document, metadata, doc_type
                    FROM core_content
                    WHERE id = %s;
                """, (id,))
                
                result = cur.fetchone()
                
                if result:
                    return {
                        'id': result['id'],
                        'document': result['document'],
                        'metadata': result['metadata'],
                        'doc_type': result['doc_type']
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"핵심 내용 조회 실패 ({id}): {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        데이터베이스 통계 정보 반환
        
        Returns:
            통계 정보 딕셔너리
        """
        try:
            with self.conn.cursor() as cur:
                # 핵심 내용 개수
                cur.execute("SELECT COUNT(*) FROM core_content;")
                core_count = cur.fetchone()[0]
                
                # 상세 내용 개수
                cur.execute("SELECT COUNT(*) FROM detailed_content;")
                detailed_count = cur.fetchone()[0]
                
                return {
                    'core_content_count': core_count,
                    'detailed_content_count': detailed_count,
                    'total_count': core_count + detailed_count,
                    'database': 'Neon PostgreSQL + pgvector'
                }
                
        except Exception as e:
            logger.error(f"통계 정보 조회 실패: {e}")
            return {}
    
    def clear_all_data(self):
        """모든 데이터 삭제 (주의: 복구 불가능)"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM detailed_content;")
                cur.execute("DELETE FROM core_content;")
                logger.info("모든 데이터 삭제 완료")
        except Exception as e:
            logger.error(f"데이터 삭제 실패: {e}")
            raise
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            logger.info("Neon PostgreSQL 연결 종료")

if __name__ == "__main__":
    # 테스트 코드
    try:
        # 환경변수에서 연결 문자열을 읽어서 초기화
        neon_db = NeonVectorDB()
        
        # 통계 정보 출력
        stats = neon_db.get_statistics()
        print("=== Neon PostgreSQL 통계 ===")
        print(f"핵심 내용: {stats['core_content_count']}")
        print(f"상세 내용: {stats['detailed_content_count']}")
        print(f"전체: {stats['total_count']}")
        
        # 연결 종료
        neon_db.close()
        
    except Exception as e:
        print(f"테스트 실행 실패: {e}")
        print("NEON_DATABASE_URL 환경변수를 설정했는지 확인하세요.")