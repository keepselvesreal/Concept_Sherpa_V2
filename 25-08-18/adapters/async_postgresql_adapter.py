"""
생성 시간: 2025-08-18 12:34:35
핵심 내용: 비동기 PostgreSQL 데이터베이스 어댑터 (병렬 처리 지원)
상세 내용:
    - AsyncPostgreSQLAdapter 클래스 (라인 35-300): 비동기 DB 작업 지원
    - async_connect 메서드 (라인 55-75): 비동기 연결 관리
    - async_query_data 메서드 (라인 85-130): 비동기 데이터 조회
    - async_execute_query 메서드 (라인 135-170): 원시 SQL 실행
    - connection_pool 지원 (라인 180-220): 연결 풀링으로 성능 최적화
    - 벡터 유사도 검색 최적화 (라인 225-280): PostgreSQL pgvector 전용 메서드
상태: 
주소: async_postgresql_adapter
참조: postgresql_adapter
"""

import asyncio
import os
import json
import logging
from typing import List, Dict, Any, Optional, Union
from contextlib import asynccontextmanager
import time

try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False

logger = logging.getLogger(__name__)

class AsyncPostgreSQLAdapter:
    """
    비동기 PostgreSQL 데이터베이스 어댑터
    - asyncpg를 사용한 고성능 비동기 처리
    - 병렬 벡터 검색 최적화
    - 연결 풀링 지원
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        비동기 PostgreSQL 어댑터 초기화
        
        Args:
            config: 데이터베이스 연결 설정
        """
        if not ASYNCPG_AVAILABLE:
            raise ImportError("asyncpg가 설치되지 않았습니다. uv add asyncpg")
        
        self.config = config
        self.connection_pool = None
        self.connection_string = None
        self._build_connection_string()
        
        # 성능 설정
        self.min_pool_size = 2
        self.max_pool_size = 10
        self.command_timeout = 30
    
    def _build_connection_string(self):
        """연결 설정에서 연결 문자열 구성"""
        connection_config = self.config.get('connection', {})
        
        # 직접 URL이 제공된 경우
        if 'url' in connection_config:
            url = connection_config['url']
            # 환경변수 참조인지 확인
            if url.startswith('from_env:'):
                env_var = url.replace('from_env:', '')
                self.connection_string = os.getenv(env_var)
                if not self.connection_string:
                    raise ValueError(f"환경변수 {env_var}가 설정되지 않았습니다.")
            else:
                self.connection_string = url
        else:
            raise ValueError("연결 URL이 필요합니다.")
        
        logger.info(f"연결 문자열 구성 완료")
    
    async def connect(self) -> bool:
        """비동기 데이터베이스 연결 풀 생성"""
        try:
            self.connection_pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=self.min_pool_size,
                max_size=self.max_pool_size,
                command_timeout=self.command_timeout
            )
            
            # 연결 테스트
            async with self.connection_pool.acquire() as conn:
                await conn.fetchval('SELECT 1')
            
            logger.info(f"비동기 PostgreSQL 연결 풀 생성 완료 (크기: {self.min_pool_size}-{self.max_pool_size})")
            return True
            
        except Exception as e:
            logger.error(f"비동기 PostgreSQL 연결 실패: {e}")
            return False
    
    async def close(self):
        """연결 풀 종료"""
        if self.connection_pool:
            await self.connection_pool.close()
            logger.info("비동기 PostgreSQL 연결 풀 종료")
    
    async def test_connection(self) -> bool:
        """연결 테스트"""
        try:
            if not self.connection_pool:
                return False
                
            async with self.connection_pool.acquire() as conn:
                result = await conn.fetchval('SELECT 1')
                return result == 1
                
        except Exception as e:
            logger.error(f"연결 테스트 실패: {e}")
            return False
    
    async def query_data(
        self, 
        table_name: str,
        where_clause: Optional[str] = None,
        params: Optional[List[Any]] = None,
        custom_query: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        비동기 데이터 조회
        
        Args:
            table_name: 테이블명
            where_clause: WHERE 조건
            params: 쿼리 파라미터
            custom_query: 커스텀 SQL 쿼리
            limit: 결과 제한
            
        Returns:
            조회 결과 리스트
        """
        try:
            async with self.connection_pool.acquire() as conn:
                if custom_query:
                    # 커스텀 쿼리 실행
                    if params:
                        rows = await conn.fetch(custom_query, *params)
                    else:
                        rows = await conn.fetch(custom_query)
                else:
                    # 기본 SELECT 쿼리 구성
                    query = f"SELECT * FROM {table_name}"
                    
                    if where_clause:
                        query += f" WHERE {where_clause}"
                    
                    if limit:
                        query += f" LIMIT {limit}"
                    
                    if params:
                        rows = await conn.fetch(query, *params)
                    else:
                        rows = await conn.fetch(query)
                
                # asyncpg Row 객체를 딕셔너리로 변환
                results = []
                for row in rows:
                    result_dict = dict(row)
                    results.append(result_dict)
                
                logger.debug(f"데이터 조회 완료: {len(results)}행")
                return results
                
        except Exception as e:
            logger.error(f"데이터 조회 오류 ({table_name}): {e}")
            return []
    
    async def execute_query(
        self, 
        query: str, 
        params: Optional[List[Any]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        원시 SQL 쿼리 실행
        
        Args:
            query: SQL 쿼리
            params: 쿼리 파라미터
            
        Returns:
            실행 결과 (SELECT인 경우)
        """
        try:
            async with self.connection_pool.acquire() as conn:
                if params:
                    if query.strip().upper().startswith('SELECT'):
                        rows = await conn.fetch(query, *params)
                        return [dict(row) for row in rows]
                    else:
                        await conn.execute(query, *params)
                        return None
                else:
                    if query.strip().upper().startswith('SELECT'):
                        rows = await conn.fetch(query)
                        return [dict(row) for row in rows]
                    else:
                        await conn.execute(query)
                        return None
                        
        except Exception as e:
            logger.error(f"쿼리 실행 오류: {e}")
            raise
    
    async def vector_similarity_search(
        self,
        table_name: str,
        query_embedding: List[float],
        similarity_threshold: float = 0.7,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        벡터 유사도 검색 전용 메서드 (PostgreSQL pgvector 최적화)
        
        Args:
            table_name: 임베딩 테이블명
            query_embedding: 질의 벡터
            similarity_threshold: 유사도 임계값
            limit: 결과 제한
            
        Returns:
            유사도 검색 결과
        """
        try:
            # 벡터를 PostgreSQL vector 형식으로 변환
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            
            # 코사인 유사도 검색 쿼리 (pgvector 연산자 사용)
            query = f"""
            SELECT 
                id,
                document_id,
                embedding,
                metadata,
                (1 - (embedding <=> $1::vector)) as similarity_score
            FROM {table_name}
            WHERE (1 - (embedding <=> $1::vector)) >= $2
            ORDER BY similarity_score DESC
            LIMIT $3
            """
            
            start_time = time.time()
            
            async with self.connection_pool.acquire() as conn:
                rows = await conn.fetch(query, embedding_str, similarity_threshold, limit)
                
                results = []
                for row in rows:
                    result_dict = dict(row)
                    results.append(result_dict)
            
            search_time = time.time() - start_time
            logger.info(f"벡터 검색 완료: {table_name} - {len(results)}개 결과 ({search_time:.3f}초)")
            
            return results
            
        except Exception as e:
            logger.error(f"벡터 유사도 검색 오류 ({table_name}): {e}")
            return []
    
    async def batch_vector_search(
        self,
        table_configs: List[Dict[str, Any]],
        query_embedding: List[float]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        여러 테이블에 대한 병렬 벡터 검색
        
        Args:
            table_configs: 테이블별 검색 설정 리스트
                [{"table": "table1", "threshold": 0.7, "limit": 5}, ...]
            query_embedding: 질의 벡터
            
        Returns:
            테이블별 검색 결과 딕셔너리
        """
        start_time = time.time()
        
        # 병렬 검색 태스크 생성
        tasks = []
        table_names = []
        
        for config in table_configs:
            table_name = config['table']
            threshold = config.get('threshold', 0.7)
            limit = config.get('limit', 5)
            
            task = self.vector_similarity_search(
                table_name, query_embedding, threshold, limit
            )
            tasks.append(task)
            table_names.append(table_name)
        
        # 병렬 실행
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 정리
            search_results = {}
            for i, (table_name, result) in enumerate(zip(table_names, results)):
                if isinstance(result, Exception):
                    logger.error(f"테이블 {table_name} 검색 오류: {result}")
                    search_results[table_name] = []
                else:
                    search_results[table_name] = result
            
            total_time = time.time() - start_time
            total_results = sum(len(r) for r in search_results.values())
            
            logger.info(f"병렬 벡터 검색 완료: {len(table_configs)}개 테이블 - "
                       f"{total_results}개 결과 ({total_time:.3f}초)")
            
            return search_results
            
        except Exception as e:
            logger.error(f"병렬 벡터 검색 오류: {e}")
            return {}
    
    @asynccontextmanager
    async def get_connection(self):
        """연결 컨텍스트 매니저"""
        if not self.connection_pool:
            raise RuntimeError("연결 풀이 초기화되지 않았습니다.")
        
        async with self.connection_pool.acquire() as conn:
            yield conn
    
    async def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        테이블 정보 조회
        
        Args:
            table_name: 테이블명
            
        Returns:
            테이블 정보 딕셔너리
        """
        try:
            async with self.get_connection() as conn:
                # 테이블 존재 확인
                exists_query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = $1
                )
                """
                exists = await conn.fetchval(exists_query, table_name)
                
                if not exists:
                    return {'exists': False}
                
                # 행 수 조회
                count_query = f"SELECT COUNT(*) FROM {table_name}"
                row_count = await conn.fetchval(count_query)
                
                # 스키마 정보 조회
                schema_query = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' 
                AND table_name = $1
                ORDER BY ordinal_position
                """
                columns = await conn.fetch(schema_query, table_name)
                
                return {
                    'exists': True,
                    'row_count': row_count,
                    'columns': [dict(col) for col in columns]
                }
                
        except Exception as e:
            logger.error(f"테이블 정보 조회 오류 ({table_name}): {e}")
            return {'exists': False, 'error': str(e)}