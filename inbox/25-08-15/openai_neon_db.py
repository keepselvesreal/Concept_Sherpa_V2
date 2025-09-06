"""
생성 시간: 2025-08-15 17:20:00
핵심 내용: OpenAI 임베딩(1536차원)을 지원하는 Neon 데이터베이스 관리자
상세 내용:
    - OpenAINeonVectorDB 클래스(라인 27-200): 1536차원 임베딩을 지원하는 DB 관리자
    - _setup_database 메서드(라인 51-85): 1536차원 벡터 테이블 생성
    - 모든 임베딩 테이블: VECTOR(1536)으로 설정
    - 기존 384차원 테이블과 독립적으로 운영
상태: 
주소: openai_neon_db
참조: neon_db_v2
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import logging
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='/home/nadle/projects/Concept_Sherpa_V2/.env')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAINeonVectorDB:
    """
    OpenAI 임베딩(1536차원)을 지원하는 Neon PostgreSQL + pgvector 관리자
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        OpenAI 임베딩 지원 DB 관리자 초기화
        
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
        """OpenAI 임베딩용 데이터베이스 설정 (1536차원)"""
        try:
            with self.conn.cursor() as cur:
                # pgvector 확장 활성화
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                logger.info("pgvector 확장 활성화 완료")
                
                # OpenAI 임베딩용 테이블 삭제 (기존 테이블과 구분)
                openai_tables = [
                    'openai_documents',
                    'openai_core_content_embeddings',
                    'openai_detailed_core_embeddings',
                    'openai_main_topic_embeddings',
                    'openai_sub_topic_embeddings'
                ]
                
                for table in openai_tables:
                    cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                logger.info("기존 OpenAI 테이블 삭제 완료")
                
                # documents 테이블 생성 (OpenAI 전용)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS openai_documents (
                        id VARCHAR(100) PRIMARY KEY,
                        title TEXT,
                        extracted_info TEXT,
                        content TEXT,
                        informed_toc TEXT,
                        child_doc_ids TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 4개 임베딩 테이블 생성 (1536차원)
                embedding_tables = [
                    'openai_core_content_embeddings',
                    'openai_detailed_core_embeddings', 
                    'openai_main_topic_embeddings',
                    'openai_sub_topic_embeddings'
                ]
                
                for table in embedding_tables:
                    cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table} (
                            id VARCHAR(100) PRIMARY KEY,
                            embedding VECTOR(1536),
                            document_id VARCHAR(100),
                            metadata JSONB,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (document_id) REFERENCES openai_documents(id) ON DELETE CASCADE
                        );
                    """)
                
                # 벡터 검색을 위한 HNSW 인덱스 생성
                for table in embedding_tables:
                    cur.execute(f"""
                        CREATE INDEX IF NOT EXISTS {table}_embedding_idx 
                        ON {table} USING hnsw (embedding vector_cosine_ops);
                    """)
                
                logger.info("OpenAI 1536차원 테이블 및 인덱스 생성 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 설정 실패: {e}")
            raise
    
    def insert_document(self, doc_id: str, title: str, extracted_info: str, 
                       content: str, informed_toc: str = None, child_doc_ids: str = None):
        """
        documents 테이블에 문서 데이터 삽입
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO openai_documents (id, title, extracted_info, content, informed_toc, child_doc_ids)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        extracted_info = EXCLUDED.extracted_info,
                        content = EXCLUDED.content,
                        informed_toc = EXCLUDED.informed_toc,
                        child_doc_ids = EXCLUDED.child_doc_ids,
                        created_at = CURRENT_TIMESTAMP;
                """, (doc_id, title, extracted_info, content, informed_toc, child_doc_ids))
                
                logger.info(f"OpenAI 문서 삽입 완료: {doc_id}")
                
        except Exception as e:
            logger.error(f"문서 삽입 실패 ({doc_id}): {e}")
            raise
    
    def insert_embedding(self, table_name: str, embedding_id: str, embedding: List[float], 
                        document_id: str, metadata: Dict[str, Any]):
        """
        임베딩 테이블에 데이터 삽입 (1536차원)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {table_name} (id, embedding, document_id, metadata)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        embedding = EXCLUDED.embedding,
                        document_id = EXCLUDED.document_id,
                        metadata = EXCLUDED.metadata,
                        created_at = CURRENT_TIMESTAMP;
                """, (embedding_id, embedding, document_id, json.dumps(metadata)))
                
                logger.info(f"OpenAI {table_name} 임베딩 삽입 완료: {embedding_id}")
                
        except Exception as e:
            logger.error(f"{table_name} 임베딩 삽입 실패 ({embedding_id}): {e}")
            raise
    
    def search_embeddings(self, table_name: str, query_embedding: List[float], 
                         n_results: int = 5) -> List[Dict[str, Any]]:
        """
        특정 임베딩 테이블에서 벡터 유사도 검색
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(f"""
                    SELECT e.id, e.document_id, e.metadata, d.title, d.content,
                           (e.embedding <=> %s::vector) as distance
                    FROM {table_name} e
                    JOIN openai_documents d ON e.document_id = d.id
                    ORDER BY e.embedding <=> %s::vector
                    LIMIT %s;
                """, (query_embedding, query_embedding, n_results))
                
                results = cur.fetchall()
                
                formatted_results = []
                for row in results:
                    formatted_results.append({
                        'id': row['id'],
                        'document_id': row['document_id'],
                        'document_title': row['title'],
                        'document_content': row['content'],
                        'metadata': row['metadata'],
                        'distance': float(row['distance'])
                    })
                
                logger.info(f"OpenAI {table_name} 검색 완료: {len(formatted_results)}개 결과")
                return formatted_results
                
        except Exception as e:
            logger.error(f"{table_name} 검색 실패: {e}")
            raise
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 문서 조회
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, title, extracted_info, content, informed_toc, child_doc_ids
                    FROM openai_documents
                    WHERE id = %s;
                """, (doc_id,))
                
                result = cur.fetchone()
                
                if result:
                    return dict(result)
                
                return None
                
        except Exception as e:
            logger.error(f"문서 조회 실패 ({doc_id}): {e}")
            return None
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            logger.info("OpenAI Neon PostgreSQL 연결 종료")

if __name__ == "__main__":
    try:
        # 테스트 실행
        db = OpenAINeonVectorDB()
        logger.info("OpenAI 임베딩 지원 데이터베이스 초기화 완료")
        db.close()
        
    except Exception as e:
        print(f"테스트 실행 실패: {e}")
        print("NEON_DATABASE_URL 환경변수를 설정했는지 확인하세요.")