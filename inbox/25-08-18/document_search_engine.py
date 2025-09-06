"""
생성 시간: 2025-08-18 12:22:54
핵심 내용: 문서 벡터 검색 엔진 메인 클래스
상세 내용:
    - DocumentSearchEngine 클래스 (라인 30-180): 통합 문서 검색 엔진
    - search 메서드 (라인 45-90): 메인 검색 인터페이스
    - initialize_components 메서드 (라인 92-115): 컴포넌트 초기화
    - get_search_config 메서드 (라인 117-140): 설정 로드
    - log_search_metrics 메서드 (라인 142-165): 검색 성능 로깅
    - SearchConfig 클래스 (라인 182-200): 검색 설정 데이터 구조
상태: 
주소: document_search_engine
참조: query_processor, parallel_search_manager, document_reconstructor
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# 로컬 컴포넌트 임포트
from components import (
    QueryProcessor, 
    ParallelSearchManager, 
    DocumentReconstructor,
    ReconstructedDocument
)
from adapters.async_postgresql_adapter import AsyncPostgreSQLAdapter
from utils.config_loader import load_config

logger = logging.getLogger(__name__)

@dataclass
class SearchConfig:
    """검색 엔진 설정"""
    similarity_threshold: float = 0.3  # 실제 관련 문서들이 검색되도록 임계값 조정
    max_results_per_search: int = 5
    max_total_results: int = 10
    enable_translation: bool = True
    log_search_metrics: bool = True

class DocumentSearchEngine:
    """
    통합 문서 벡터 검색 엔진
    - 사용자 질의 처리 및 임베딩
    - 병렬 벡터 검색 (내용/화제 차원)
    - 문서 재구성 및 반환
    """
    
    def __init__(self, config_path: str = "config/projects.yaml"):
        self.config_path = config_path
        self.db_adapter = None
        self.query_processor = None
        self.search_manager = None
        self.reconstructor = None
        self.search_config = SearchConfig()
        
        # 검색 통계
        self.search_stats = {
            'total_searches': 0,
            'avg_search_time': 0.0,
            'success_rate': 0.0
        }
    
    async def initialize(self, project_name: str = "knowledge_sherpa"):
        """
        검색 엔진 초기화
        
        Args:
            project_name: 프로젝트명
        """
        logger.info(f"DocumentSearchEngine 초기화 시작: {project_name}")
        
        try:
            # 설정 로드
            config = load_config(self.config_path)
            project_config = config['projects'][project_name]
            
            # 비동기 DB 어댑터 초기화
            self.db_adapter = AsyncPostgreSQLAdapter(project_config)
            await self.db_adapter.connect()
            
            # 컴포넌트 초기화
            await self.initialize_components(project_config)
            
            logger.info("DocumentSearchEngine 초기화 완료")
            
        except Exception as e:
            logger.error(f"DocumentSearchEngine 초기화 오류: {e}")
            raise
    
    async def search(
        self, 
        query: str, 
        project_name: str = "knowledge_sherpa",
        max_results: Optional[int] = None
    ) -> List[ReconstructedDocument]:
        """
        사용자 질의로 문서 검색
        
        Args:
            query: 사용자 질의 (한국어)
            project_name: 프로젝트명
            max_results: 최대 결과 수
            
        Returns:
            재구성된 문서 리스트
        """
        start_time = time.time()
        logger.info(f"검색 시작: '{query}' (프로젝트: {project_name})")
        
        try:
            # 1. 질의 처리 및 임베딩 생성
            query_embedding = await self.query_processor.process_query(query, project_name)
            
            # 2. 병렬 벡터 검색 (내용 + 화제 차원)
            search_results = await self.search_manager.parallel_search(
                query_embedding, project_name
            )
            
            # 3. 검색 결과 통합
            content_results = search_results.get('content', [])
            topic_results = search_results.get('topic', [])
            
            merged_results = self.search_manager.merge_search_results(
                content_results, topic_results
            )
            
            # 4. 결과 수 제한
            if max_results:
                merged_results = merged_results[:max_results]
            
            # 5. 문서 재구성
            reconstructed_docs = await self.reconstructor.reconstruct_documents(
                merged_results, project_name
            )
            
            # 6. 검색 통계 로깅
            search_time = time.time() - start_time
            await self.log_search_metrics(query, search_time, len(reconstructed_docs))
            
            logger.info(f"검색 완료: {len(reconstructed_docs)}개 문서 ({search_time:.2f}초)")
            return reconstructed_docs
            
        except Exception as e:
            search_time = time.time() - start_time
            logger.error(f"검색 오류 ({search_time:.2f}초): {e}")
            await self.log_search_metrics(query, search_time, 0, error=str(e))
            return []
    
    async def initialize_components(self, project_config: Dict[str, Any]):
        """
        검색 엔진 컴포넌트들 초기화
        
        Args:
            project_config: 프로젝트 설정
        """
        search_config_dict = {
            'similarity_threshold': self.search_config.similarity_threshold,
            'max_results_per_search': self.search_config.max_results_per_search,
            'max_total_results': self.search_config.max_total_results
        }
        
        # 컴포넌트 초기화
        self.query_processor = QueryProcessor(self.db_adapter, search_config_dict)
        self.search_manager = ParallelSearchManager(self.db_adapter, search_config_dict)
        self.reconstructor = DocumentReconstructor(self.db_adapter, search_config_dict)
        
        logger.info("모든 컴포넌트 초기화 완료")
    
    async def search_with_filters(
        self,
        query: str,
        project_name: str = "knowledge_sherpa",
        document_type: Optional[str] = None,
        language: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None
    ) -> List[ReconstructedDocument]:
        """
        필터 조건을 적용한 검색
        
        Args:
            query: 검색 질의
            project_name: 프로젝트명
            document_type: 문서 타입 필터
            language: 언어 필터
            date_range: 날짜 범위 필터
            
        Returns:
            필터링된 검색 결과
        """
        # 기본 검색 수행
        results = await self.search(query, project_name)
        
        # 필터 적용
        filtered_results = []
        for doc in results:
            # 문서 타입 필터
            if document_type and doc.metadata.get('source_type') != document_type:
                continue
                
            # 언어 필터
            if language and doc.metadata.get('document_language') != language:
                continue
                
            # 날짜 범위 필터 (구현 필요시)
            if date_range:
                # TODO: 날짜 필터 로직 구현
                pass
            
            filtered_results.append(doc)
        
        logger.info(f"필터 적용 후: {len(filtered_results)}개 문서")
        return filtered_results
    
    async def log_search_metrics(
        self, 
        query: str, 
        search_time: float, 
        result_count: int, 
        error: Optional[str] = None
    ):
        """
        검색 성능 및 통계 로깅
        
        Args:
            query: 검색 질의
            search_time: 검색 소요 시간
            result_count: 결과 수
            error: 오류 메시지 (있을 경우)
        """
        if not self.search_config.log_search_metrics:
            return
            
        try:
            # 통계 업데이트
            self.search_stats['total_searches'] += 1
            
            if error is None:
                # 성공한 검색만 평균 시간에 포함
                prev_avg = self.search_stats['avg_search_time']
                total_success = self.search_stats['total_searches']
                self.search_stats['avg_search_time'] = (
                    (prev_avg * (total_success - 1) + search_time) / total_success
                )
            
            # 성공률 계산 (간단한 버전)
            success_searches = self.search_stats['total_searches']
            if error is not None:
                success_searches -= 1
                
            self.search_stats['success_rate'] = (
                success_searches / self.search_stats['total_searches']
            ) * 100
            
            # 로그 기록
            log_msg = (
                f"검색 통계 - 질의: '{query[:50]}...', "
                f"시간: {search_time:.2f}초, 결과: {result_count}개"
            )
            
            if error:
                log_msg += f", 오류: {error}"
                logger.warning(log_msg)
            else:
                logger.info(log_msg)
                
            # 통계 요약 (매 10회마다)
            if self.search_stats['total_searches'] % 10 == 0:
                logger.info(
                    f"검색 통계 요약 - "
                    f"총 검색: {self.search_stats['total_searches']}회, "
                    f"평균 시간: {self.search_stats['avg_search_time']:.2f}초, "
                    f"성공률: {self.search_stats['success_rate']:.1f}%"
                )
                
        except Exception as e:
            logger.error(f"검색 통계 로깅 오류: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        시스템 상태 정보 반환
        
        Returns:
            시스템 상태 딕셔너리
        """
        try:
            status = {
                'database_connected': self.db_adapter is not None,
                'components_initialized': all([
                    self.query_processor is not None,
                    self.search_manager is not None,
                    self.reconstructor is not None
                ]),
                'search_stats': self.search_stats.copy(),
                'config': {
                    'similarity_threshold': self.search_config.similarity_threshold,
                    'max_total_results': self.search_config.max_total_results
                }
            }
            
            # DB 연결 테스트
            if self.db_adapter:
                try:
                    await self.db_adapter.test_connection()
                    status['database_status'] = 'connected'
                except:
                    status['database_status'] = 'disconnected'
            else:
                status['database_status'] = 'not_initialized'
            
            return status
            
        except Exception as e:
            logger.error(f"시스템 상태 조회 오류: {e}")
            return {'error': str(e)}
    
    async def close(self):
        """
        검색 엔진 종료 및 리소스 정리
        """
        try:
            if self.db_adapter:
                await self.db_adapter.close()
                logger.info("데이터베이스 연결 종료")
                
            logger.info("DocumentSearchEngine 종료 완료")
            
        except Exception as e:
            logger.error(f"검색 엔진 종료 오류: {e}")
    
    def __del__(self):
        """소멸자 - 리소스 정리"""
        if hasattr(self, 'db_adapter') and self.db_adapter:
            # 비동기 close 메서드는 소멸자에서 호출할 수 없으므로 경고만 출력
            logger.warning("DocumentSearchEngine이 정리되지 않고 종료됨. close() 메서드를 명시적으로 호출하세요.")