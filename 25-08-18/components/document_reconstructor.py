"""
생성 시간: 2025-08-18 12:22:54
핵심 내용: 검색 결과를 원본 문서 형식으로 재구성하는 컴포넌트
상세 내용:
    - DocumentReconstructor 클래스 (라인 25-180): 문서 재구성 및 포맷팅
    - reconstruct_documents 메서드 (라인 40-75): 메인 문서 재구성 로직
    - get_document_metadata 메서드 (라인 77-105): DB에서 문서 메타데이터 조회
    - format_document 메서드 (라인 107-145): 마크다운 형식으로 문서 포맷팅
    - determine_search_dimension 메서드 (라인 147-165): 검색 차원 결정
    - ReconstructedDocument 클래스 (라인 182-195): 재구성된 문서 데이터 구조
상태: 
주소: document_reconstructor
참조: waterfall_searcher
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .waterfall_searcher import SearchResult

logger = logging.getLogger(__name__)

@dataclass
class ReconstructedDocument:
    """재구성된 문서 데이터 구조"""
    document_id: str
    title: str
    formatted_content: str
    similarity_score: float
    search_dimension: str
    metadata: Dict[str, Any]

class DocumentReconstructor:
    """
    검색 결과를 원본 문서 형식으로 재구성
    - DB에서 완전한 문서 데이터 조회
    - 표준 마크다운 형식으로 포맷팅
    """
    
    def __init__(self, db_adapter, config: Dict[str, Any]):
        self.db_adapter = db_adapter
        self.config = config
    
    async def reconstruct_documents(
        self, 
        search_results: List[SearchResult],
        project_name: str
    ) -> List[ReconstructedDocument]:
        """
        검색 결과를 완전한 문서로 재구성
        
        Args:
            search_results: 벡터 검색 결과들
            project_name: 프로젝트명
            
        Returns:
            재구성된 문서들
        """
        logger.info(f"문서 재구성 시작: {len(search_results)}개 결과")
        
        reconstructed_docs = []
        
        for result in search_results:
            try:
                # 문서 메타데이터 및 전체 내용 조회
                document_data = await self.get_document_metadata(
                    result.document_id, 
                    project_name
                )
                
                if not document_data:
                    logger.warning(f"문서 데이터 없음: {result.document_id}")
                    continue
                
                # 검색 차원 결정
                search_dimension = self.determine_search_dimension(result)
                
                # 문서 포맷팅
                formatted_content = await self.format_document(
                    document_data, 
                    result.similarity_score,
                    search_dimension
                )
                
                reconstructed_doc = ReconstructedDocument(
                    document_id=result.document_id,
                    title=document_data.get('title', 'Untitled'),
                    formatted_content=formatted_content,
                    similarity_score=result.similarity_score,
                    search_dimension=search_dimension,
                    metadata=document_data
                )
                
                reconstructed_docs.append(reconstructed_doc)
                logger.info(f"문서 재구성 완료: {result.document_id}")
                
            except Exception as e:
                logger.error(f"문서 재구성 오류 ({result.document_id}): {e}")
                continue
        
        logger.info(f"문서 재구성 완료: {len(reconstructed_docs)}개 문서")
        return reconstructed_docs
    
    async def get_document_metadata(
        self, 
        document_id: str, 
        project_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        DB에서 문서의 완전한 메타데이터 및 내용 조회
        
        Args:
            document_id: 문서 ID
            project_name: 프로젝트명
            
        Returns:
            문서 데이터 딕셔너리
        """
        try:
            # documents 테이블에서 기본 정보 조회
            query = """
            SELECT *
            FROM documents
            WHERE id = $1
            """
            
            results = await self.db_adapter.query_data(
                "documents",
                custom_query=query,
                params=[document_id]
            )
            
            if not results:
                return None
            
            document_data = results[0]
            logger.info(f"문서 메타데이터 조회 완료: {document_id}")
            
            return document_data
            
        except Exception as e:
            logger.error(f"문서 메타데이터 조회 오류 ({document_id}): {e}")
            return None
    
    async def format_document(
        self, 
        document_data: Dict[str, Any], 
        similarity_score: float,
        search_dimension: str
    ) -> str:
        """
        문서를 표준 마크다운 형식으로 포맷팅
        
        Args:
            document_data: 문서 데이터
            similarity_score: 유사도 점수
            search_dimension: 검색 차원
            
        Returns:
            포맷팅된 마크다운 문서
        """
        try:
            # 속성 섹션 구성
            attributes = []
            attributes.append(f"source_type: {document_data.get('source_type', 'unknown')}")
            attributes.append(f"structure_type: {document_data.get('structure_type', 'unknown')}")
            attributes.append(f"document_language: {document_data.get('document_language', 'unknown')}")
            attributes.append(f"similarity_score: {similarity_score:.4f}")
            attributes.append(f"search_dimension: {search_dimension}")
            
            # 추출 섹션 구성 (실제 데이터 필드 사용)
            extraction_sections = []
            
            # extracted_info에서 추출된 정보 사용
            if document_data.get('extracted_info'):
                extraction_sections.append(document_data['extracted_info'])
                extraction_sections.append("")
            
            # 원본 content 추가
            if document_data.get('content'):
                extraction_sections.append("# 내용")
                extraction_sections.append("---")
                extraction_sections.append(document_data['content'])
                extraction_sections.append("")
            
            # 구성 섹션 추가 (항상 포함)
            extraction_sections.append("# 구성")
            extraction_sections.append("---")
            child_docs = document_data.get('child_doc_ids')
            if child_docs:
                extraction_sections.append(str(child_docs))
            else:
                extraction_sections.append("")
            extraction_sections.append("")
            
            # 최종 문서 조합 (제목 제거)
            formatted_doc = f"""# 속성
---
{chr(10).join(attributes)}

# 추출
---
{chr(10).join(extraction_sections)}"""
            
            return formatted_doc
            
        except Exception as e:
            logger.error(f"문서 포맷팅 오류: {e}")
            return f"# 문서 포맷팅 오류\n\n오류 발생: {str(e)}"
    
    def determine_search_dimension(self, search_result: SearchResult) -> str:
        """
        검색 결과에서 검색 차원 결정
        
        Args:
            search_result: 검색 결과
            
        Returns:
            검색 차원 ('content', 'topic', 'both')
        """
        table_name = search_result.table_name.lower()
        
        if 'content' in table_name:
            return 'content'
        elif 'topic' in table_name:
            return 'topic'
        else:
            return 'unknown'
    
    async def batch_reconstruct_by_dimension(
        self,
        content_results: List[SearchResult],
        topic_results: List[SearchResult],
        project_name: str
    ) -> Dict[str, List[ReconstructedDocument]]:
        """
        차원별로 분리하여 문서 재구성
        
        Args:
            content_results: 내용 차원 검색 결과
            topic_results: 화제 차원 검색 결과  
            project_name: 프로젝트명
            
        Returns:
            차원별 재구성된 문서들
        """
        results = {}
        
        if content_results:
            results['content'] = await self.reconstruct_documents(content_results, project_name)
        
        if topic_results:
            results['topic'] = await self.reconstruct_documents(topic_results, project_name)
        
        return results
    
    def calculate_relevance_score(
        self, 
        search_result: SearchResult, 
        query_terms: List[str]
    ) -> float:
        """
        검색 결과의 관련성 점수 계산
        
        Args:
            search_result: 검색 결과
            query_terms: 질의 용어들
            
        Returns:
            관련성 점수 (0~1)
        """
        try:
            content = search_result.content.lower()
            relevance_score = 0.0
            
            for term in query_terms:
                if term.lower() in content:
                    relevance_score += 1.0
            
            # 정규화
            if query_terms:
                relevance_score = relevance_score / len(query_terms)
            
            # 유사도 점수와 가중 평균
            final_score = (search_result.similarity_score * 0.7) + (relevance_score * 0.3)
            
            return final_score
            
        except Exception as e:
            logger.error(f"관련성 점수 계산 오류: {e}")
            return search_result.similarity_score