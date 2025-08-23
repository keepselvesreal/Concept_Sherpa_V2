"""
KURE 기반 임베딩 시스템을 위한 임베딩 서비스 모듈
sentence-transformers 모델을 사용하여 텍스트 임베딩 생성
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingServiceV2:
    """
    sentence-transformers를 사용한 임베딩 생성 서비스
    """
    
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        임베딩 서비스 초기화
        
        Args:
            model_name: 사용할 sentence-transformers 모델명
                      다국어 지원을 위해 multilingual 모델 사용
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """모델 로딩"""
        try:
            logger.info(f"임베딩 모델 로딩 중: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("모델 로딩 완료")
        except Exception as e:
            logger.error(f"모델 로딩 실패: {e}")
            raise
    
    def create_embedding(self, text: str) -> List[float]:
        """
        단일 텍스트에 대한 임베딩 생성
        
        Args:
            text: 임베딩을 생성할 텍스트
            
        Returns:
            임베딩 벡터 (List[float])
        """
        if not text or not text.strip():
            raise ValueError("빈 텍스트는 임베딩을 생성할 수 없습니다")
        
        try:
            embedding = self.model.encode(text.strip())
            return embedding.tolist()
        except Exception as e:
            logger.error(f"임베딩 생성 실패: {e}")
            raise
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        여러 텍스트에 대한 배치 임베딩 생성
        
        Args:
            texts: 임베딩을 생성할 텍스트 리스트
            
        Returns:
            임베딩 벡터 리스트 (List[List[float]])
        """
        if not texts:
            return []
        
        # 빈 텍스트 필터링
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        
        if not valid_texts:
            raise ValueError("유효한 텍스트가 없습니다")
        
        try:
            logger.info(f"배치 임베딩 생성 중: {len(valid_texts)}개 텍스트")
            embeddings = self.model.encode(valid_texts)
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            logger.error(f"배치 임베딩 생성 실패: {e}")
            raise
    
    def get_model_info(self) -> dict:
        """
        모델 정보 반환
        
        Returns:
            모델 정보 딕셔너리
        """
        return {
            "model_name": self.model_name,
            "dimension": self.model.get_sentence_embedding_dimension(),
            "max_seq_length": self.model.max_seq_length
        }

# 전역 임베딩 서비스 인스턴스
_embedding_service = None

def get_embedding_service() -> EmbeddingServiceV2:
    """
    전역 임베딩 서비스 인스턴스 반환 (싱글톤 패턴)
    
    Returns:
        EmbeddingServiceV2 인스턴스
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingServiceV2()
    return _embedding_service

if __name__ == "__main__":
    # 테스트 코드
    service = EmbeddingServiceV2()
    
    # 모델 정보 출력
    print("모델 정보:", service.get_model_info())
    
    # 단일 임베딩 테스트
    test_text = "OOP의 구조적 복잡성과 DOP 대안의 필요성"
    embedding = service.create_embedding(test_text)
    print(f"임베딩 차원: {len(embedding)}")
    print(f"임베딩 처음 5개 값: {embedding[:5]}")
    
    # 배치 임베딩 테스트
    test_texts = [
        "체계적 OOP 설계의 시작",
        "UML 관계의 복잡성",
        "클래스 상세 구조와 책임 분산"
    ]
    batch_embeddings = service.create_embeddings_batch(test_texts)
    print(f"배치 임베딩 개수: {len(batch_embeddings)}")