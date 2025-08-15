"""
생성 시간: 2025-08-15 16:09:50
핵심 내용: Neon PostgreSQL + pgvector를 사용한 새로운 벡터 데이터베이스 관리 모듈 (V2)
상세 내용:
    - NeonVectorDBV2 클래스: 새로운 5개 테이블 스키마 관리
    - DocumentParser 클래스: 마크다운 문서 섹션별 파싱 기능
    - 4개 임베딩 테이블: core_content_embeddings, detailed_core_embeddings, main_topic_embeddings, sub_topic_embeddings
    - documents 테이블: 문서 메타데이터 및 내용 저장
    - CRUD 메서드들: 각 테이블별 삽입, 검색, 조회 기능
    - 벡터 검색 인덱스: HNSW 인덱스를 통한 효율적인 유사도 검색
상태: 
주소: neon_db_v2
참조: 
"""

import os
import json
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional, Tuple
import logging
from dotenv import load_dotenv
from pathlib import Path
from sentence_transformers import SentenceTransformer

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentParser:
    """
    마크다운 문서 파싱 클래스
    문서를 섹션별로 분리하여 추출
    """
    
    @staticmethod
    def parse_document(file_path: str) -> Dict[str, str]:
        """
        마크다운 문서를 섹션별로 파싱
        
        Args:
            file_path: 파싱할 문서 경로
            
        Returns:
            섹션별 내용이 담긴 딕셔너리
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # 파일명에서 제목 추출
            title = Path(file_path).name
            
            # 섹션 분리
            extracted_info = ""
            document_content = ""
            child_doc_ids = ""
            core_content = ""
            detailed_core = ""
            main_topics = ""
            sub_topics = ""
            
            current_section = None
            content_started = False
            
            in_extraction = False
            
            for i, line in enumerate(lines):
                # 메인 섹션 헤더 감지
                if line.strip() == "# 추출":
                    in_extraction = True
                    current_section = "extraction"
                    continue
                elif line.strip() == "# 내용":
                    in_extraction = False
                    current_section = "content"
                    continue
                elif line.strip() == "# 구성":
                    in_extraction = False
                    current_section = "components"
                    continue
                
                # 추출 섹션 내 서브섹션 헤더 감지
                elif line.strip() == "## 핵심 내용" and in_extraction:
                    current_section = "core_content"
                    continue
                elif line.strip() == "## 상세 핵심 내용" and in_extraction:
                    current_section = "detailed_core"
                    continue
                elif line.strip() == "## 주요 화제" and in_extraction:
                    current_section = "main_topics"
                    continue
                elif line.strip() == "## 부차 화제" and in_extraction:
                    current_section = "sub_topics"
                    continue
                
                # 내용 추가
                if current_section == "extraction":
                    # "---" 이후부터 섹션 헤더가 아닌 내용 추가
                    if line.strip() == "---":
                        continue
                    elif line.strip() not in ["# 내용"] and not line.strip().startswith("##"):
                        extracted_info += line + "\n"
                elif current_section == "content":
                    if line.strip() not in ["---"] and not line.strip().startswith("# 구성"):
                        document_content += line + "\n"
                elif current_section == "components":
                    child_doc_ids += line + "\n"
                elif current_section == "core_content":
                    if not line.strip().startswith("##") and line.strip() not in ["# 내용", "# 구성"]:
                        core_content += line + "\n"
                elif current_section == "detailed_core":
                    if not line.strip().startswith("##") and line.strip() not in ["# 내용", "# 구성"]:
                        detailed_core += line + "\n"
                elif current_section == "main_topics":
                    if not line.strip().startswith("##") and line.strip() not in ["# 내용", "# 구성"]:
                        main_topics += line + "\n"
                elif current_section == "sub_topics":
                    if not line.strip().startswith("##") and line.strip() not in ["# 내용", "# 구성"]:
                        sub_topics += line + "\n"
            
            return {
                'title': title,
                'extracted_info': extracted_info.strip(),
                'content': document_content.strip(),
                'child_doc_ids': child_doc_ids.strip() if child_doc_ids.strip() else None,
                'core_content': core_content.strip(),
                'detailed_core': detailed_core.strip(),
                'main_topics': main_topics.strip(),
                'sub_topics': sub_topics.strip()
            }
            
        except Exception as e:
            logger.error(f"문서 파싱 실패 ({file_path}): {e}")
            raise

class NeonVectorDBV2:
    """
    Neon PostgreSQL + pgvector를 사용한 벡터 데이터베이스 관리자 V2
    새로운 5개 테이블 스키마 지원
    """
    
    def __init__(self, connection_string: Optional[str] = None, embedding_model: str = None):
        """
        Neon 벡터 DB 관리자 초기화
        
        Args:
            connection_string: PostgreSQL 연결 문자열 (None이면 환경변수에서 로드)
            embedding_model: 임베딩 모델명 (None이면 기본 모델 사용)
        """
        self.connection_string = connection_string or os.getenv('NEON_DATABASE_URL')
        
        if not self.connection_string:
            raise ValueError("Neon 데이터베이스 연결 문자열이 필요합니다. NEON_DATABASE_URL 환경변수를 설정하세요.")
        
        self.conn = None
        self.embedding_model_name = embedding_model or "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.embedding_model = None
        
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
        """데이터베이스 초기 설정 (pgvector 확장 및 새 테이블 생성)"""
        try:
            with self.conn.cursor() as cur:
                # pgvector 확장 활성화
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                logger.info("pgvector 확장 활성화 완료")
                
                # 기존 테이블 삭제
                cur.execute("DROP TABLE IF EXISTS core_content CASCADE;")
                cur.execute("DROP TABLE IF EXISTS detailed_content CASCADE;")
                logger.info("기존 테이블 삭제 완료")
                
                # documents 테이블 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id VARCHAR(100) PRIMARY KEY,
                        title TEXT,
                        extracted_info TEXT,
                        content TEXT,
                        informed_toc TEXT,
                        child_doc_ids TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 4개 임베딩 테이블 생성
                embedding_tables = [
                    'core_content_embeddings',
                    'detailed_core_embeddings', 
                    'main_topic_embeddings',
                    'sub_topic_embeddings'
                ]
                
                for table in embedding_tables:
                    cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table} (
                            id VARCHAR(100) PRIMARY KEY,
                            embedding VECTOR(384),
                            document_id VARCHAR(100),
                            metadata JSONB,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
                        );
                    """)
                
                # 벡터 검색을 위한 HNSW 인덱스 생성
                for table in embedding_tables:
                    cur.execute(f"""
                        CREATE INDEX IF NOT EXISTS {table}_embedding_idx 
                        ON {table} USING hnsw (embedding vector_cosine_ops);
                    """)
                
                logger.info("새로운 5개 테이블 및 인덱스 생성 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 설정 실패: {e}")
            raise
    
    def _load_embedding_model(self):
        """임베딩 모델 로드 (지연 로딩)"""
        if self.embedding_model is None:
            logger.info(f"임베딩 모델 로드 중: {self.embedding_model_name}")
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            logger.info("임베딩 모델 로드 완료")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        텍스트 리스트에서 임베딩 생성
        
        Args:
            texts: 임베딩을 생성할 텍스트 리스트
            
        Returns:
            임베딩 벡터 리스트
        """
        try:
            self._load_embedding_model()
            
            # 빈 텍스트 필터링
            valid_texts = [text.strip() for text in texts if text.strip()]
            if not valid_texts:
                return []
            
            embeddings = self.embedding_model.encode(valid_texts)
            
            # numpy array를 list로 변환
            if hasattr(embeddings, 'tolist'):
                embeddings = embeddings.tolist()
            else:
                embeddings = [emb.tolist() if hasattr(emb, 'tolist') else list(emb) for emb in embeddings]
            
            logger.info(f"임베딩 생성 완료: {len(embeddings)}개")
            return embeddings
            
        except Exception as e:
            logger.error(f"임베딩 생성 실패: {e}")
            raise
    
    def insert_document(self, doc_id: str, title: str, extracted_info: str, 
                       content: str, informed_toc: str = None, child_doc_ids: str = None):
        """
        documents 테이블에 문서 데이터 삽입
        
        Args:
            doc_id: 문서 ID
            title: 문서 제목
            extracted_info: 추출된 정보
            content: 문서 내용
            informed_toc: 연결된 목차 ID
            child_doc_ids: 하위 문서 ID들
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO documents (id, title, extracted_info, content, informed_toc, child_doc_ids)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        extracted_info = EXCLUDED.extracted_info,
                        content = EXCLUDED.content,
                        informed_toc = EXCLUDED.informed_toc,
                        child_doc_ids = EXCLUDED.child_doc_ids,
                        created_at = CURRENT_TIMESTAMP;
                """, (doc_id, title, extracted_info, content, informed_toc, child_doc_ids))
                
                logger.info(f"문서 삽입 완료: {doc_id}")
                
        except Exception as e:
            logger.error(f"문서 삽입 실패 ({doc_id}): {e}")
            raise
    
    def insert_embedding(self, table_name: str, embedding_id: str, embedding: List[float], 
                        document_id: str, metadata: Dict[str, Any]):
        """
        임베딩 테이블에 데이터 삽입
        
        Args:
            table_name: 대상 테이블명
            embedding_id: 임베딩 ID
            embedding: 임베딩 벡터
            document_id: 연결된 문서 ID
            metadata: 메타데이터
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
                
                logger.info(f"{table_name} 임베딩 삽입 완료: {embedding_id}")
                
        except Exception as e:
            logger.error(f"{table_name} 임베딩 삽입 실패 ({embedding_id}): {e}")
            raise
    
    def search_embeddings(self, table_name: str, query_embedding: List[float], 
                         n_results: int = 5) -> List[Dict[str, Any]]:
        """
        특정 임베딩 테이블에서 벡터 유사도 검색
        
        Args:
            table_name: 검색할 테이블명
            query_embedding: 쿼리 임베딩
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 리스트
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(f"""
                    SELECT e.id, e.document_id, e.metadata, d.title, d.content,
                           (e.embedding <=> %s::vector) as distance
                    FROM {table_name} e
                    JOIN documents d ON e.document_id = d.id
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
                
                logger.info(f"{table_name} 검색 완료: {len(formatted_results)}개 결과")
                return formatted_results
                
        except Exception as e:
            logger.error(f"{table_name} 검색 실패: {e}")
            raise
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 문서 조회
        
        Args:
            doc_id: 문서 ID
            
        Returns:
            문서 데이터 또는 None
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, title, extracted_info, content, informed_toc, child_doc_ids
                    FROM documents
                    WHERE id = %s;
                """, (doc_id,))
                
                result = cur.fetchone()
                
                if result:
                    return dict(result)
                
                return None
                
        except Exception as e:
            logger.error(f"문서 조회 실패 ({doc_id}): {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        데이터베이스 통계 정보 반환
        
        Returns:
            통계 정보 딕셔너리
        """
        try:
            with self.conn.cursor() as cur:
                stats = {}
                
                # documents 테이블 개수
                cur.execute("SELECT COUNT(*) FROM documents;")
                stats['documents_count'] = cur.fetchone()[0]
                
                # 각 임베딩 테이블 개수
                embedding_tables = [
                    'core_content_embeddings',
                    'detailed_core_embeddings', 
                    'main_topic_embeddings',
                    'sub_topic_embeddings'
                ]
                
                total_embeddings = 0
                for table in embedding_tables:
                    cur.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cur.fetchone()[0]
                    stats[f'{table}_count'] = count
                    total_embeddings += count
                
                stats['total_embeddings'] = total_embeddings
                stats['database'] = 'Neon PostgreSQL + pgvector V2'
                
                return stats
                
        except Exception as e:
            logger.error(f"통계 정보 조회 실패: {e}")
            return {}
    
    def clear_all_data(self):
        """모든 데이터 삭제 (주의: 복구 불가능)"""
        try:
            with self.conn.cursor() as cur:
                # 임베딩 테이블들 먼저 삭제 (외래키 제약조건)
                embedding_tables = [
                    'core_content_embeddings',
                    'detailed_core_embeddings', 
                    'main_topic_embeddings',
                    'sub_topic_embeddings'
                ]
                
                for table in embedding_tables:
                    cur.execute(f"DELETE FROM {table};")
                
                cur.execute("DELETE FROM documents;")
                logger.info("모든 데이터 삭제 완료")
        except Exception as e:
            logger.error(f"데이터 삭제 실패: {e}")
            raise
    
    def process_document_file(self, file_path: str, doc_id: str = None, generate_embeddings: bool = True) -> str:
        """
        문서 파일을 파싱하여 데이터베이스에 저장 (임베딩 포함)
        
        Args:
            file_path: 문서 파일 경로
            doc_id: 문서 ID (None이면 파일명 사용)
            generate_embeddings: 임베딩을 생성할지 여부
            
        Returns:
            생성된 문서 ID
        """
        try:
            if doc_id is None:
                doc_id = Path(file_path).stem
            
            # 문서 파싱
            parsed_doc = DocumentParser.parse_document(file_path)
            
            # 전체 추출 섹션을 extracted_info로 구성
            extracted_sections = [
                f"## 핵심 내용\n{parsed_doc['core_content']}",
                f"## 상세 핵심 내용\n{parsed_doc['detailed_core']}",
                f"## 주요 화제\n{parsed_doc['main_topics']}",
                f"## 부차 화제\n{parsed_doc['sub_topics']}"
            ]
            extracted_info = "\n\n".join(extracted_sections)
            
            # documents 테이블에 삽입
            self.insert_document(
                doc_id=doc_id,
                title=parsed_doc['title'],
                extracted_info=extracted_info,
                content=parsed_doc['content'],
                child_doc_ids=parsed_doc['child_doc_ids']
            )
            
            # 임베딩 생성 및 저장
            if generate_embeddings:
                self._process_document_embeddings(doc_id, parsed_doc)
            
            logger.info(f"문서 처리 완료: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"문서 처리 실패 ({file_path}): {e}")
            raise
    
    def _process_document_embeddings(self, doc_id: str, parsed_doc: Dict[str, str]):
        """
        파싱된 문서의 각 섹션에서 임베딩을 생성하고 저장
        
        Args:
            doc_id: 문서 ID
            parsed_doc: 파싱된 문서 데이터
        """
        try:
            logger.info(f"임베딩 생성 시작: {doc_id}")
            
            # 임베딩을 생성할 섹션들
            section_data = [
                ("core_content_embeddings", "core", parsed_doc['core_content']),
                ("detailed_core_embeddings", "detailed", parsed_doc['detailed_core']),
                ("main_topic_embeddings", "main", parsed_doc['main_topics']),
                ("sub_topic_embeddings", "sub", parsed_doc['sub_topics'])
            ]
            
            for table_name, section_type, content in section_data:
                if content.strip():  # 내용이 있는 경우만 처리
                    # 임베딩 생성
                    embeddings = self.generate_embeddings([content])
                    if embeddings:
                        embedding_id = f"{doc_id}_{section_type}_001"
                        
                        # 메타데이터 구성
                        metadata = {
                            "section_type": section_type,
                            "language": "mixed",  # 한국어/영어 혼합
                            "file_name": parsed_doc['title'],
                            "content_length": len(content)
                        }
                        
                        # 임베딩 저장
                        self.insert_embedding(
                            table_name=table_name,
                            embedding_id=embedding_id,
                            embedding=embeddings[0],
                            document_id=doc_id,
                            metadata=metadata
                        )
                        
                        logger.info(f"임베딩 저장 완료: {table_name} - {embedding_id}")
            
            logger.info(f"모든 임베딩 처리 완료: {doc_id}")
            
        except Exception as e:
            logger.error(f"임베딩 처리 실패 ({doc_id}): {e}")
            raise
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            logger.info("Neon PostgreSQL 연결 종료")

if __name__ == "__main__":
    try:
        # 환경변수에서 연결 문자열을 읽어서 초기화
        neon_db = NeonVectorDBV2()
        
        # 통계 정보 출력
        stats = neon_db.get_statistics()
        print("=== Neon PostgreSQL V2 통계 ===")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # 연결 종료
        neon_db.close()
        
    except Exception as e:
        print(f"테스트 실행 실패: {e}")
        print("NEON_DATABASE_URL 환경변수를 설정했는지 확인하세요.")