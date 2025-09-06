"""
생성 시간: 2025-08-18 12:22:54
핵심 내용: 폭포수식 벡터 검색 로직 구현
상세 내용:
    - WaterfallSearcher 클래스 (라인 25-150): 계층적 우선순위 검색
    - search_with_waterfall 메서드 (라인 35-65): 메인 폭포수 검색 로직
    - search_embeddings 메서드 (라인 67-100): 개별 테이블 벡터 검색
    - calculate_similarity 메서드 (라인 102-120): 코사인 유사도 계산
    - SearchResult 클래스 (라인 152-165): 검색 결과 데이터 구조
상태: 
주소: waterfall_searcher
참조: 
"""

import asyncio
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """검색 결과 데이터 구조"""
    document_id: str
    similarity_score: float
    table_name: str
    search_level: str  # 'primary' or 'secondary'
    content: str
    metadata: Dict[str, Any]

class WaterfallSearcher:
    """
    폭포수식 벡터 검색 수행
    - 우선 테이블에서 먼저 검색
    - 결과 없으면 보조 테이블 검색
    """
    
    def __init__(self, db_adapter, config: Dict[str, Any]):
        self.db_adapter = db_adapter
        self.config = config
        self.similarity_threshold = config.get('similarity_threshold', 0.7)
        self.max_results = config.get('max_results_per_search', 5)
    
    async def search_with_waterfall(
        self, 
        table_primary: str, 
        table_secondary: str, 
        query_embedding: List[float],
        dimension_name: str
    ) -> List[SearchResult]:
        """
        폭포수식 검색 수행
        
        Args:
            table_primary: 우선 검색 테이블
            table_secondary: 보조 검색 테이블
            query_embedding: 질의 임베딩 벡터
            dimension_name: 검색 차원명 (content/topic)
            
        Returns:
            검색 결과 리스트
        """
        logger.info(f"{dimension_name} 차원 폭포수 검색 시작: {table_primary} → {table_secondary}")
        
        # 1단계: 우선 테이블 검색
        primary_results = await self.search_embeddings(
            table_primary, 
            query_embedding, 
            search_level="primary",
            dimension_name=dimension_name
        )
        
        if primary_results:
            logger.info(f"{table_primary}에서 {len(primary_results)}개 결과 발견, 보조 검색 생략")
            return primary_results
        
        # 2단계: 보조 테이블 검색 (우선 테이블에서 결과 없을 때만)
        logger.info(f"{table_primary}에서 결과 없음, {table_secondary}에서 검색")
        secondary_results = await self.search_embeddings(
            table_secondary, 
            query_embedding, 
            search_level="secondary",
            dimension_name=dimension_name
        )
        
        logger.info(f"{table_secondary}에서 {len(secondary_results)}개 결과 발견")
        return secondary_results
    
    async def search_embeddings(
        self, 
        table_name: str, 
        query_embedding: List[float],
        search_level: str,
        dimension_name: str
    ) -> List[SearchResult]:
        """
        개별 테이블에서 벡터 유사도 검색 (비동기 어댑터 사용)
        
        Args:
            table_name: 검색할 테이블명
            query_embedding: 질의 임베딩 벡터
            search_level: 검색 레벨 (primary/secondary)
            dimension_name: 검색 차원명
            
        Returns:
            검색 결과 리스트
        """
        try:
            # 비동기 어댑터의 벡터 검색 메서드 사용
            results = await self.db_adapter.vector_similarity_search(
                table_name=table_name,
                query_embedding=query_embedding,
                similarity_threshold=self.similarity_threshold,
                limit=self.max_results
            )
            
            search_results = []
            for row in results:
                # content 컬럼이 없는 경우 빈 문자열 사용 (실제 content는 documents 테이블에서 조회)
                content = row.get('content', '')
                
                search_result = SearchResult(
                    document_id=row['document_id'],
                    similarity_score=row['similarity_score'],
                    table_name=table_name,
                    search_level=search_level,
                    content=content,
                    metadata=row.get('metadata', {})
                )
                search_results.append(search_result)
            
            logger.info(f"{table_name}에서 {len(search_results)}개 결과 (임계값: {self.similarity_threshold})")
            return search_results
            
        except Exception as e:
            logger.error(f"{table_name} 검색 오류: {e}")
            return []
    
    def calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        두 벡터 간 코사인 유사도 계산
        
        Args:
            vec1: 첫 번째 벡터
            vec2: 두 번째 벡터
            
        Returns:
            코사인 유사도 (0~1)
        """
        try:
            # numpy 배열로 변환
            a = np.array(vec1)
            b = np.array(vec2)
            
            # 코사인 유사도 계산
            cosine_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            
            # NaN 처리
            if np.isnan(cosine_sim):
                return 0.0
                
            return float(cosine_sim)
            
        except Exception as e:
            logger.error(f"유사도 계산 오류: {e}")
            return 0.0
    
    async def batch_search_multiple_tables(
        self, 
        table_pairs: List[Tuple[str, str]], 
        query_embedding: List[float],
        dimension_names: List[str]
    ) -> Dict[str, List[SearchResult]]:
        """
        여러 테이블 쌍에 대해 병렬 폭포수 검색
        
        Args:
            table_pairs: (우선_테이블, 보조_테이블) 쌍들
            query_embedding: 질의 임베딩 벡터
            dimension_names: 각 쌍에 대응하는 차원명들
            
        Returns:
            차원별 검색 결과 딕셔너리
        """
        tasks = []
        for (primary, secondary), dimension in zip(table_pairs, dimension_names):
            task = self.search_with_waterfall(
                primary, secondary, query_embedding, dimension
            )
            tasks.append((dimension, task))
        
        results = {}
        for dimension, task in tasks:
            try:
                search_results = await task
                results[dimension] = search_results
            except Exception as e:
                logger.error(f"{dimension} 차원 검색 오류: {e}")
                results[dimension] = []
        
        return results