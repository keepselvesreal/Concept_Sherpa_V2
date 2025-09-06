"""
생성 시간: 2025-08-15 16:45:02
핵심 내용: 사용자 질문을 임베딩하여 계층적 벡터 검색을 수행하고 문서를 반환하는 시스템
상세 내용:
    - EmbeddingProvider 추상 클래스(라인 31-40): 임베딩 모델 인터페이스 정의
    - SentenceTransformerProvider 클래스(라인 42-67): sentence-transformers 구현체
    - OpenAIProvider 클래스(라인 69-94): OpenAI API 구현체
    - VectorSearchSystem 클래스(라인 96-216): 계층적 벡터 검색 수행
    - search_documents 메서드(라인 120-182): 핵심→상세, 주요→부차 순서 검색
    - _format_document_response 메서드(라인 219-246): lev0_ 형식 문서 응답 포맷팅
    - main 함수(라인 248-282): 커맨드라인 인터페이스
    - 유사도 임계값: 0.8 (기본값) - 이보다 높으면 다음 단계 검색 건너뜀
상태: 
주소: vector_search_system
참조: neon_db_v2
"""

import os
import sys
import argparse
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
import re
from dotenv import load_dotenv
from neon_db_v2 import NeonVectorDBV2

# 선택적 import들
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingProvider(ABC):
    """
    임베딩 생성을 위한 추상 클래스
    """
    
    @abstractmethod
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """텍스트를 임베딩 벡터로 변환"""
        pass

class SentenceTransformerProvider(EmbeddingProvider):
    """
    sentence-transformers 기반 임베딩 프로바이더
    """
    
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers가 설치되지 않았습니다. pip install sentence-transformers")
        
        self.model_name = model_name
        self.model = None
        
    def _load_model(self):
        """모델 지연 로딩"""
        if self.model is None:
            logger.info(f"SentenceTransformer 모델 로드 중: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("모델 로드 완료")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        try:
            self._load_model()
            embedding = self.model.encode([text])[0]
            return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
        except Exception as e:
            logger.error(f"SentenceTransformer 임베딩 생성 실패: {e}")
            return None

class OpenAIProvider(EmbeddingProvider):
    """
    OpenAI API 기반 임베딩 프로바이더
    """
    
    def __init__(self, model_name: str = "text-embedding-3-small"):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai가 설치되지 않았습니다. pip install openai")
        
        self.model_name = model_name
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API 키가 필요합니다. OPENAI_API_KEY 환경변수를 설정하세요.")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI 임베딩 생성 실패: {e}")
            return None

class VectorSearchSystem:
    """
    질문 임베딩 및 계층적 벡터 검색 시스템
    """
    
    def __init__(self, embedding_provider: EmbeddingProvider, similarity_threshold: float = 0.8):
        """
        벡터 검색 시스템 초기화
        
        Args:
            embedding_provider: 임베딩 생성 프로바이더
            similarity_threshold: 유사도 임계값 (이보다 높으면 다음 단계 검색 건너뜀)
        """
        self.db = NeonVectorDBV2()
        self.embedding_provider = embedding_provider
        self.similarity_threshold = similarity_threshold
    
    def search_documents(self, question: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        사용자 질문에 대한 계층적 벡터 검색 수행
        
        Args:
            question: 사용자 질문
            max_results: 최대 반환 결과 수
            
        Returns:
            검색된 문서들의 리스트
        """
        logger.info(f"질문 검색 시작: {question}")
        
        # 1. 질문을 임베딩으로 변환
        question_embedding = self.embedding_provider.get_embedding(question)
        if not question_embedding:
            logger.error("질문 임베딩 생성 실패")
            return []
        
        found_documents = []
        
        # 2. 내용 기반 검색 (핵심 → 상세)
        logger.info("핵심 내용 테이블에서 검색 중...")
        core_results = self.db.search_embeddings(
            'core_content_embeddings', 
            question_embedding, 
            max_results
        )
        
        if core_results and any(result['distance'] < self.similarity_threshold for result in core_results):
            logger.info(f"핵심 내용에서 {len(core_results)}개 결과 발견 (유사도 >= {1-self.similarity_threshold:.1f})")
            found_documents.extend(core_results)
        else:
            logger.info("핵심 내용에서 유사한 결과 없음, 상세 핵심 내용 검색 중...")
            detailed_results = self.db.search_embeddings(
                'detailed_core_embeddings', 
                question_embedding, 
                max_results
            )
            if detailed_results:
                logger.info(f"상세 핵심 내용에서 {len(detailed_results)}개 결과 발견")
                found_documents.extend(detailed_results)
        
        # 3. 화제 기반 검색 (주요 → 부차) - 내용 기반 검색과 독립적으로 수행
        logger.info("주요 화제 테이블에서 검색 중...")
        main_topic_results = self.db.search_embeddings(
            'main_topic_embeddings', 
            question_embedding, 
            max_results
        )
        
        if main_topic_results and any(result['distance'] < self.similarity_threshold for result in main_topic_results):
            logger.info(f"주요 화제에서 {len(main_topic_results)}개 결과 발견 (유사도 >= {1-self.similarity_threshold:.1f})")
            found_documents.extend(main_topic_results)
        else:
            logger.info("주요 화제에서 유사한 결과 없음, 부차 화제 검색 중...")
            sub_topic_results = self.db.search_embeddings(
                'sub_topic_embeddings', 
                question_embedding, 
                max_results
            )
            if sub_topic_results:
                logger.info(f"부차 화제에서 {len(sub_topic_results)}개 결과 발견")
                found_documents.extend(sub_topic_results)
        
        # 4. 중복 제거 (document_id 기준)
        unique_docs = {}
        for doc in found_documents:
            doc_id = doc['document_id']
            if doc_id not in unique_docs or doc['distance'] < unique_docs[doc_id]['distance']:
                unique_docs[doc_id] = doc
        
        # 5. 거리 기준으로 정렬하여 반환
        final_results = sorted(unique_docs.values(), key=lambda x: x['distance'])[:max_results]
        
        logger.info(f"최종 {len(final_results)}개 문서 반환")
        return final_results
    
    def format_response(self, search_results: List[Dict[str, Any]]) -> str:
        """
        검색 결과를 사용자에게 보여줄 형식으로 포맷팅
        
        Args:
            search_results: 검색 결과 리스트
            
        Returns:
            포맷된 응답 문자열
        """
        if not search_results:
            return "검색 결과가 없습니다."
        
        response = "## 검색 결과\n\n"
        
        for i, result in enumerate(search_results, 1):
            # 문서 상세 정보 조회
            document = self.db.get_document_by_id(result['document_id'])
            if document:
                formatted_doc = self._format_document_response(document)
                response += f"### {i}. {formatted_doc}\n\n"
                response += f"**유사도**: {1 - result['distance']:.3f}\n\n"
                response += "---\n\n"
        
        return response
    
    def _format_document_response(self, document: Dict[str, Any]) -> str:
        """
        문서를 요청된 형식으로 포맷팅
        
        Args:
            document: 문서 데이터
            
        Returns:
            포맷된 문서 문자열
        """
        title = document.get('title', '')
        
        # lev0_와 _info 사이의 텍스트 추출
        match = re.search(r'lev0_(.+?)_info', title)
        if match:
            extracted_title = match.group(1)
        else:
            extracted_title = title
        
        # 포맷된 응답 생성
        response = f"**제목**: {extracted_title}\n\n"
        response += "# 추출\n"
        response += f"{document.get('extracted_info', '')}\n\n"
        response += "# 내용\n"
        response += f"{document.get('content', '')}"
        
        return response

def create_embedding_provider(provider_type: str = "sentence-transformers", model_name: str = None) -> EmbeddingProvider:
    """
    임베딩 프로바이더 팩토리 함수
    
    Args:
        provider_type: "sentence-transformers" 또는 "openai"
        model_name: 모델명 (None이면 기본값 사용)
        
    Returns:
        임베딩 프로바이더 인스턴스
    """
    if provider_type == "sentence-transformers":
        default_model = "paraphrase-multilingual-MiniLM-L12-v2"
        return SentenceTransformerProvider(model_name or default_model)
    elif provider_type == "openai":
        default_model = "text-embedding-3-small"
        return OpenAIProvider(model_name or default_model)
    else:
        raise ValueError(f"지원되지 않는 프로바이더 타입: {provider_type}")

def main():
    """
    커맨드라인 인터페이스
    """
    parser = argparse.ArgumentParser(description='벡터 검색 시스템')
    parser.add_argument('question', help='검색할 질문')
    parser.add_argument('--max-results', type=int, default=3, help='최대 결과 수 (기본값: 3)')
    parser.add_argument('--threshold', type=float, default=0.8, help='유사도 임계값 (기본값: 0.8)')
    parser.add_argument('--provider', choices=['sentence-transformers', 'openai'], 
                       default='sentence-transformers', help='임베딩 프로바이더 (기본값: sentence-transformers)')
    parser.add_argument('--model', help='사용할 모델명 (기본값: 프로바이더별 기본 모델)')
    
    args = parser.parse_args()
    
    search_system = None
    try:
        # 임베딩 프로바이더 생성
        embedding_provider = create_embedding_provider(args.provider, args.model)
        
        # 검색 시스템 초기화
        search_system = VectorSearchSystem(embedding_provider, similarity_threshold=args.threshold)
        
        # 검색 수행
        results = search_system.search_documents(args.question, args.max_results)
        
        # 결과 출력
        formatted_response = search_system.format_response(results)
        print(formatted_response)
        
    except Exception as e:
        logger.error(f"검색 실행 실패: {e}")
        print(f"오류 발생: {e}")
        sys.exit(1)
    finally:
        # 데이터베이스 연결 종료
        if search_system:
            search_system.db.close()

if __name__ == "__main__":
    main()