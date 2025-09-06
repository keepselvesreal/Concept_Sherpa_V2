"""
전체 임베딩 생성 및 벡터 DB 저장 파이프라인
content_processor로 파싱된 데이터를 임베딩하여 저장
"""

from embedding_service_v2 import get_embedding_service
from vector_db_v2 import VectorDBManagerV2
from content_processor import ContentProcessor
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingPipeline:
    """
    전체 임베딩 생성 및 저장 파이프라인
    """
    
    def __init__(self, content_file_path: str, db_path: str = "./chroma_db_v2"):
        """
        파이프라인 초기화
        
        Args:
            content_file_path: chapter1_core_content.md 파일 경로
            db_path: 벡터 DB 저장 경로
        """
        self.content_file_path = content_file_path
        self.db_path = db_path
        
        # 컴포넌트 초기화
        self.embedding_service = get_embedding_service()
        self.db_manager = VectorDBManagerV2(db_path)
        self.content_processor = ContentProcessor(content_file_path)
        
        # 컬렉션 재설정 (기존 데이터 삭제)
        self.db_manager.reset_collections()
        
        logger.info("임베딩 파이프라인 초기화 완료")
    
    def run_pipeline(self):
        """전체 파이프라인 실행"""
        try:
            logger.info("임베딩 파이프라인 시작")
            
            # 1. 컨텐츠 파싱
            logger.info("1. 컨텐츠 파싱 시작")
            core_content_list, detailed_content_list = self.content_processor.parse_core_content()
            logger.info(f"파싱 완료 - 핵심: {len(core_content_list)}, 상세: {len(detailed_content_list)}")
            
            # 2. 핵심 내용 임베딩 및 저장
            logger.info("2. 핵심 내용 임베딩 및 저장 시작")
            self._process_core_content(core_content_list)
            
            # 3. 상세 내용 임베딩 및 저장  
            logger.info("3. 상세 내용 임베딩 및 저장 시작")
            self._process_detailed_content(detailed_content_list)
            
            # 4. 결과 확인
            stats = self.db_manager.get_collection_stats()
            logger.info(f"파이프라인 완료 - 통계: {stats}")
            
        except Exception as e:
            logger.error(f"파이프라인 실행 실패: {e}")
            raise
    
    def _process_core_content(self, core_content_list: List[Dict[str, Any]]):
        """핵심 내용 처리"""
        for item in core_content_list:
            try:
                # 임베딩 생성
                embedding = self.embedding_service.create_embedding(item['embedding_text'])
                
                # 벡터 DB에 저장
                self.db_manager.add_core_content(
                    id=item['id'],
                    embedding=embedding,
                    document=item['document']
                )
                
                logger.info(f"핵심 내용 처리 완료: {item['id']}")
                
            except Exception as e:
                logger.error(f"핵심 내용 처리 실패 ({item['id']}): {e}")
                continue
    
    def _process_detailed_content(self, detailed_content_list: List[Dict[str, Any]]):
        """상세 내용 처리"""
        for item in detailed_content_list:
            try:
                # 임베딩 생성
                embedding = self.embedding_service.create_embedding(item['embedding_text'])
                
                # 벡터 DB에 저장 (document 필드 없음, core_ref만 포함)
                self.db_manager.add_detailed_content(
                    id=item['id'],
                    embedding=embedding,
                    core_ref=item['core_ref']
                )
                
                logger.info(f"상세 내용 처리 완료: {item['id']} (ref: {item['core_ref']})")
                
            except Exception as e:
                logger.error(f"상세 내용 처리 실패 ({item['id']}): {e}")
                continue
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 정보 반환"""
        return self.db_manager.get_collection_stats()

def main():
    """메인 함수"""
    # 파일 경로 설정
    content_file_path = "/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_Manning/Part1_Flexibility/Chapter1/chapter1_core_content.md"
    
    try:
        # 파이프라인 생성 및 실행
        pipeline = EmbeddingPipeline(content_file_path)
        pipeline.run_pipeline()
        
        # 최종 통계 출력
        stats = pipeline.get_stats()
        print("\n=== 최종 통계 ===")
        print(f"핵심 내용 개수: {stats['core_content_count']}")
        print(f"상세 내용 개수: {stats['detailed_content_count']}")
        print(f"전체 개수: {stats['total_count']}")
        print(f"DB 경로: {stats['db_path']}")
        
        # 임베딩 모델 정보 출력
        embedding_service = get_embedding_service()
        model_info = embedding_service.get_model_info()
        print(f"\n=== 모델 정보 ===")
        print(f"모델: {model_info['model_name']}")
        print(f"차원: {model_info['dimension']}")
        print(f"최대 시퀀스 길이: {model_info['max_seq_length']}")
        
        print("\n임베딩 생성 및 저장 완료!")
        
    except Exception as e:
        logger.error(f"메인 실행 실패: {e}")
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()