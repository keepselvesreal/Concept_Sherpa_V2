"""
ChromaDB 기반 벡터 데이터베이스 관리 모듈
목차 형태 핵심 내용과 상세 핵심 내용을 분리하여 저장
"""

import chromadb
from chromadb.config import Settings
import json
from typing import Dict, List, Any, Optional, Union
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDBManagerV2:
    """
    ChromaDB를 사용한 벡터 데이터베이스 관리자
    core_content와 detailed_content 두 개의 컬렉션으로 분리 관리
    """
    
    def __init__(self, db_path: str = "./chroma_db_v2"):
        """
        벡터 DB 관리자 초기화
        
        Args:
            db_path: ChromaDB 데이터베이스 저장 경로
        """
        self.db_path = db_path
        self.client = None
        self.core_collection = None  # 목차 형태 핵심 내용
        self.detailed_collection = None  # 상세 핵심 내용
        
        self._initialize_db()
    
    def _initialize_db(self):
        """데이터베이스 및 컬렉션 초기화"""
        try:
            # ChromaDB 클라이언트 생성
            self.client = chromadb.PersistentClient(path=self.db_path)
            
            # 기존 컬렉션이 있으면 가져오고, 없으면 새로 생성
            try:
                self.core_collection = self.client.get_collection("core_content")
                logger.info("기존 core_content 컬렉션 로드")
            except:
                self.core_collection = self.client.create_collection(
                    name="core_content",
                    metadata={"description": "목차 형태 핵심 내용 저장소"}
                )
                logger.info("새 core_content 컬렉션 생성")
            
            try:
                self.detailed_collection = self.client.get_collection("detailed_content")
                logger.info("기존 detailed_content 컬렉션 로드")
            except:
                self.detailed_collection = self.client.create_collection(
                    name="detailed_content", 
                    metadata={"description": "상세 핵심 내용 저장소"}
                )
                logger.info("새 detailed_content 컬렉션 생성")
            
            logger.info("벡터 DB 및 컬렉션 초기화 완료")
            
        except Exception as e:
            logger.error(f"DB 초기화 실패: {e}")
            raise
    
    def add_core_content(self, 
                        id: str,
                        embedding: List[float],
                        document: Union[str, Dict[str, Any]],
                        metadata: Optional[Dict[str, Any]] = None):
        """
        핵심 내용을 core_content 컬렉션에 추가
        
        Args:
            id: 문서 ID
            embedding: 임베딩 벡터
            document: 문서 내용 (str: 원문, Dict: 메타데이터 구조체)
            metadata: 추가 메타데이터
        """
        try:
            # document가 dict인 경우 JSON 문자열로 변환
            if isinstance(document, dict):
                document_str = json.dumps(document, ensure_ascii=False, indent=2)
                doc_type = "composite_section"
            else:
                document_str = document
                doc_type = "leaf_section"
            
            # 메타데이터 준비
            final_metadata = {
                "doc_type": doc_type,
                "collection": "core_content"
            }
            if metadata:
                final_metadata.update(metadata)
            
            self.core_collection.add(
                ids=[id],
                embeddings=[embedding],
                documents=[document_str],
                metadatas=[final_metadata]
            )
            
            logger.info(f"핵심 내용 추가: {id} ({doc_type})")
            
        except Exception as e:
            logger.error(f"핵심 내용 추가 실패 ({id}): {e}")
            raise
    
    def add_detailed_content(self,
                           id: str, 
                           embedding: List[float],
                           core_ref: str,
                           metadata: Optional[Dict[str, Any]] = None):
        """
        상세 내용을 detailed_content 컬렉션에 추가
        
        Args:
            id: 문서 ID
            embedding: 임베딩 벡터  
            core_ref: 원문이 포함된 핵심 내용 인스턴스 ID
            metadata: 추가 메타데이터
        """
        try:
            # 메타데이터 준비
            final_metadata = {
                "core_ref": core_ref,
                "collection": "detailed_content",
                "type": "detailed_analysis"
            }
            if metadata:
                final_metadata.update(metadata)
            
            # detailed_content는 document 필드가 없음 (빈 문자열로 처리)
            self.detailed_collection.add(
                ids=[id],
                embeddings=[embedding], 
                documents=[""],  # 빈 문서
                metadatas=[final_metadata]
            )
            
            logger.info(f"상세 내용 추가: {id} (core_ref: {core_ref})")
            
        except Exception as e:
            logger.error(f"상세 내용 추가 실패 ({id}): {e}")
            raise
    
    def search_core_content(self, 
                          query_embedding: List[float],
                          n_results: int = 5) -> Dict[str, Any]:
        """
        핵심 내용에서 유사도 검색
        
        Args:
            query_embedding: 쿼리 임베딩 벡터
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 딕셔너리
        """
        try:
            results = self.core_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return self._format_search_results(results, "core_content")
        except Exception as e:
            logger.error(f"핵심 내용 검색 실패: {e}")
            raise
    
    def search_detailed_content(self,
                              query_embedding: List[float], 
                              n_results: int = 5) -> Dict[str, Any]:
        """
        상세 내용에서 유사도 검색
        
        Args:
            query_embedding: 쿼리 임베딩 벡터
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 딕셔너리
        """
        try:
            results = self.detailed_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return self._format_search_results(results, "detailed_content")
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
            results = self.core_collection.get(ids=[id])
            if results['ids']:
                return {
                    'id': results['ids'][0], 
                    'document': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
            return None
        except Exception as e:
            logger.error(f"핵심 내용 조회 실패 ({id}): {e}")
            return None
    
    def _format_search_results(self, results: Dict, collection_type: str) -> Dict[str, Any]:
        """
        검색 결과 포맷팅
        
        Args:
            results: ChromaDB 검색 결과
            collection_type: 컬렉션 타입
            
        Returns:
            포맷팅된 검색 결과
        """
        formatted_results = []
        
        if results['ids'] and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'distance': results['distances'][0][i] if results['distances'] else None,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                }
                
                # core_content의 경우만 document 포함
                if collection_type == "core_content" and results['documents']:
                    result['document'] = results['documents'][0][i]
                
                formatted_results.append(result)
        
        return {
            'collection': collection_type,
            'results': formatted_results,
            'total_results': len(formatted_results)
        }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        컬렉션 통계 정보 반환
        
        Returns:
            통계 정보 딕셔너리
        """
        try:
            core_count = self.core_collection.count()
            detailed_count = self.detailed_collection.count()
            
            return {
                'core_content_count': core_count,
                'detailed_content_count': detailed_count,
                'total_count': core_count + detailed_count,
                'db_path': self.db_path
            }
        except Exception as e:
            logger.error(f"통계 정보 조회 실패: {e}")
            return {}
    
    def reset_collections(self):
        """컬렉션 초기화 (기존 데이터 삭제)"""
        try:
            # 기존 컬렉션 삭제
            try:
                self.client.delete_collection("core_content")
                logger.info("기존 core_content 컬렉션 삭제")
            except:
                pass
            
            try:
                self.client.delete_collection("detailed_content")
                logger.info("기존 detailed_content 컬렉션 삭제")
            except:
                pass
            
            # 새 컬렉션 생성
            self.core_collection = self.client.create_collection(
                name="core_content",
                metadata={"description": "목차 형태 핵심 내용 저장소"}
            )
            
            self.detailed_collection = self.client.create_collection(
                name="detailed_content", 
                metadata={"description": "상세 핵심 내용 저장소"}
            )
            
            logger.info("컬렉션 재설정 완료")
            
        except Exception as e:
            logger.error(f"컬렉션 재설정 실패: {e}")
            raise
    
    def close(self):
        """데이터베이스 연결 종료"""
        # ChromaDB는 자동으로 연결을 관리하므로 별도 종료 작업 불필요
        logger.info("벡터 DB 연결 종료")

if __name__ == "__main__":
    # 테스트 코드
    db_manager = VectorDBManagerV2()
    
    # 테스트 데이터
    test_embedding = [0.1] * 384  # 가상의 384차원 임베딩
    
    # 핵심 내용 추가 테스트 (상위 섹션)
    composite_doc = {
        "type": "composite_section",
        "title": "Chapter 1", 
        "composed_of": ["chapter_intro", "section_1_1", "section_1_2"],
        "content_summary": "OOP의 구조적 복잡성과 DOP 대안의 필요성"
    }
    
    db_manager.add_core_content("chapter1", test_embedding, composite_doc)
    
    # 핵심 내용 추가 테스트 (하위 섹션)
    leaf_doc = "# 1.1.1 The design phase\n\n실제 원문 내용..."
    db_manager.add_core_content("section_1_1_1", test_embedding, leaf_doc)
    
    # 상세 내용 추가 테스트
    db_manager.add_detailed_content("chapter_intro_detail", test_embedding, "chapter_intro")
    
    # 통계 정보 출력
    stats = db_manager.get_collection_stats()
    print("컬렉션 통계:", stats)