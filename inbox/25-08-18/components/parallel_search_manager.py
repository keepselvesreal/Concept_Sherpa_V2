"""
생성 시간: 2025-08-18 12:22:54
핵심 내용: 병렬 검색 관리 및 결과 통합 컴포넌트
상세 내용:
    - ParallelSearchManager 클래스 (라인 25-140): 내용/화제 차원 병렬 검색 관리
    - parallel_search 메서드 (라인 40-75): 메인 병렬 검색 로직
    - merge_search_results 메서드 (라인 77-105): 검색 결과 통합 및 중복 제거
    - rank_results 메서드 (라인 107-125): 유사도 기반 결과 순위 매기기
    - SearchDimensionResult 클래스 (라인 142-155): 차원별 검색 결과 구조
상태: 
주소: parallel_search_manager
참조: waterfall_searcher
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .waterfall_searcher import WaterfallSearcher, SearchResult

logger = logging.getLogger(__name__)

@dataclass
class SearchDimensionResult:
    """차원별 검색 결과"""
    dimension: str  # 'content' or 'topic'
    results: List[SearchResult]
    search_time: float

class ParallelSearchManager:
    """
    병렬 검색 관리자
    - 내용 차원과 화제 차원 동시 검색
    - 결과 통합 및 중복 제거
    """
    
    def __init__(self, db_adapter, config: Dict[str, Any]):
        self.db_adapter = db_adapter
        self.config = config
        self.waterfall_searcher = WaterfallSearcher(db_adapter, config)
        self.max_total_results = config.get('max_total_results', 10)
    
    async def parallel_search(
        self, 
        query_embedding: List[float], 
        project_name: str
    ) -> Dict[str, List[SearchResult]]:
        """
        내용 차원과 화제 차원 병렬 검색
        
        Args:
            query_embedding: 질의 임베딩 벡터
            project_name: 프로젝트명
            
        Returns:
            차원별 검색 결과 딕셔너리
        """
        logger.info("병렬 검색 시작: 내용 차원 + 화제 차원")
        
        # 테이블명 구성 (프로젝트별)
        content_tables = self._get_content_table_names(project_name)
        topic_tables = self._get_topic_table_names(project_name)
        
        # 두 차원 병렬 실행
        start_time = asyncio.get_event_loop().time()
        
        content_task = asyncio.create_task(
            self.waterfall_searcher.search_with_waterfall(
                content_tables['primary'],
                content_tables['secondary'],
                query_embedding,
                'content'
            )
        )
        
        topic_task = asyncio.create_task(
            self.waterfall_searcher.search_with_waterfall(
                topic_tables['primary'],
                topic_tables['secondary'],
                query_embedding,
                'topic'
            )
        )
        
        # 병렬 실행 결과 수집
        try:
            content_results, topic_results = await asyncio.gather(
                content_task, topic_task, return_exceptions=True
            )
            
            end_time = asyncio.get_event_loop().time()
            search_time = end_time - start_time
            
            # 예외 처리
            if isinstance(content_results, Exception):
                logger.error(f"내용 차원 검색 오류: {content_results}")
                content_results = []
            
            if isinstance(topic_results, Exception):
                logger.error(f"화제 차원 검색 오류: {topic_results}")
                topic_results = []
            
            logger.info(f"병렬 검색 완료 ({search_time:.2f}초): 내용 {len(content_results)}개, 화제 {len(topic_results)}개")
            
            return {
                'content': content_results,
                'topic': topic_results,
                'search_time': search_time
            }
            
        except Exception as e:
            logger.error(f"병렬 검색 오류: {e}")
            return {'content': [], 'topic': [], 'search_time': 0.0}
    
    def merge_search_results(
        self, 
        content_results: List[SearchResult], 
        topic_results: List[SearchResult]
    ) -> List[SearchResult]:
        """
        내용 차원과 화제 차원 검색 결과 통합
        
        Args:
            content_results: 내용 차원 검색 결과
            topic_results: 화제 차원 검색 결과
            
        Returns:
            통합된 검색 결과 (중복 제거, 유사도 순 정렬)
        """
        logger.info(f"검색 결과 통합: 내용 {len(content_results)}개 + 화제 {len(topic_results)}개")
        
        # 모든 결과 통합
        all_results = content_results + topic_results
        
        # 문서 ID 기준 중복 제거 (더 높은 유사도 유지)
        unique_results = {}
        for result in all_results:
            doc_id = result.document_id
            if doc_id not in unique_results or result.similarity_score > unique_results[doc_id].similarity_score:
                unique_results[doc_id] = result
        
        # 유사도 기준 정렬
        merged_results = self.rank_results(list(unique_results.values()))
        
        # 최대 결과 수 제한
        final_results = merged_results[:self.max_total_results]
        
        logger.info(f"통합 완료: {len(unique_results)}개 (중복 제거) → {len(final_results)}개 (최종)")
        
        return final_results
    
    def rank_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        검색 결과를 유사도 기준으로 순위 매기기
        
        Args:
            results: 정렬할 검색 결과들
            
        Returns:
            유사도 순으로 정렬된 결과
        """
        try:
            # 유사도 기준 내림차순 정렬
            ranked_results = sorted(
                results, 
                key=lambda x: x.similarity_score, 
                reverse=True
            )
            
            return ranked_results
            
        except Exception as e:
            logger.error(f"결과 순위 매기기 오류: {e}")
            return results
    
    def _get_content_table_names(self, project_name: str) -> Dict[str, str]:
        """내용 차원 테이블명 반환"""
        if project_name == "knowledge_sherpa":
            return {
                'primary': 'core_content_embeddings',
                'secondary': 'detailed_core_content_embeddings'
            }
        else:
            return {
                'primary': f'{project_name}_core_content_embeddings',
                'secondary': f'{project_name}_detailed_core_embeddings'
            }
    
    def _get_topic_table_names(self, project_name: str) -> Dict[str, str]:
        """화제 차원 테이블명 반환"""
        if project_name == "knowledge_sherpa":
            return {
                'primary': 'main_topics_embeddings',
                'secondary': 'sub_topic_embeddings'
            }
        else:
            return {
                'primary': f'{project_name}_main_topic_embeddings',
                'secondary': f'{project_name}_sub_topic_embeddings'
            }
    
    async def get_search_statistics(self, project_name: str) -> Dict[str, Any]:
        """
        프로젝트의 검색 통계 정보 조회
        
        Args:
            project_name: 프로젝트명
            
        Returns:
            테이블별 문서 수 통계
        """
        try:
            content_tables = self._get_content_table_names(project_name)
            topic_tables = self._get_topic_table_names(project_name)
            
            stats = {}
            for dimension, tables in [('content', content_tables), ('topic', topic_tables)]:
                for level, table_name in tables.items():
                    try:
                        count_query = f"SELECT COUNT(*) as count FROM {table_name}"
                        result = await self.db_adapter.query_data(
                            table_name, 
                            custom_query=count_query
                        )
                        stats[f"{dimension}_{level}"] = result[0]['count'] if result else 0
                    except:
                        stats[f"{dimension}_{level}"] = 0
            
            logger.info(f"검색 통계: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"검색 통계 조회 오류: {e}")
            return {}