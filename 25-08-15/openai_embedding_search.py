"""
생성 시간: 2025-08-15 17:15:00
핵심 내용: OpenAI 임베딩 모델을 사용한 문서 재임베딩 및 검색 시스템
상세 내용:
    - OpenAIEmbeddingProcessor 클래스(라인 27-82): 문서 임베딩 및 검색 처리
    - process_document_embeddings 메서드(라인 34-55): 기존 문서 OpenAI로 재임베딩
    - search_with_openai 메서드(라인 57-82): OpenAI 임베딩으로 검색 수행
    - main 함수(라인 84-125): 문서 재임베딩 후 검색 및 결과 저장
    - 임계값: 0.7로 설정
    - 결과 저장: openai_search_results.txt 파일에 저장
상태: 
주소: openai_embedding_search
참조: vector_search_system, neon_db_v2
"""

import os
import sys
import json
from typing import List, Dict, Any
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from neon_db_v2 import NeonVectorDBV2

# 환경변수 로드
load_dotenv(dotenv_path='/home/nadle/projects/Concept_Sherpa_V2/.env')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIEmbeddingProcessor:
    """
    OpenAI 임베딩 모델을 사용한 문서 처리 및 검색 클래스
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.db = NeonVectorDBV2()
        self.similarity_threshold = similarity_threshold
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API 키가 필요합니다. .env 파일의 OPENAI_API_KEY를 확인하세요.")
    
    def process_document_embeddings(self, doc_id: str):
        """
        기존 문서를 OpenAI 임베딩으로 재처리
        
        Args:
            doc_id: 재처리할 문서 ID
        """
        logger.info(f"문서 {doc_id}를 OpenAI 임베딩으로 재처리 중...")
        
        # 문서 조회
        document = self.db.get_document_by_id(doc_id)
        if not document:
            logger.error(f"문서를 찾을 수 없습니다: {doc_id}")
            return
        
        # 각 섹션별로 임베딩 생성
        sections = [
            ("core_content_embeddings", "core", document.get('extracted_info', '').split('## 핵심 내용\n')[-1].split('## 상세 핵심 내용')[0].strip()),
            ("detailed_core_embeddings", "detailed", document.get('extracted_info', '').split('## 상세 핵심 내용\n')[-1].split('## 주요 화제')[0].strip()),
            ("main_topic_embeddings", "main", document.get('extracted_info', '').split('## 주요 화제\n')[-1].split('## 부차 화제')[0].strip()),
            ("sub_topic_embeddings", "sub", document.get('extracted_info', '').split('## 부차 화제\n')[-1].strip())
        ]
        
        for table_name, section_type, content in sections:
            if content.strip():
                # OpenAI 임베딩 생성
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=content
                )
                embedding = response.data[0].embedding
                
                # 임베딩 저장
                embedding_id = f"{doc_id}_{section_type}_openai_001"
                metadata = {
                    "section_type": section_type,
                    "embedding_model": "text-embedding-3-small",
                    "language": "mixed",
                    "file_name": document['title'],
                    "content_length": len(content)
                }
                
                self.db.insert_embedding(
                    table_name=table_name,
                    embedding_id=embedding_id,
                    embedding=embedding,
                    document_id=doc_id,
                    metadata=metadata
                )
                
                logger.info(f"OpenAI 임베딩 저장 완료: {table_name} - {embedding_id}")
    
    def search_with_openai(self, question: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        OpenAI 임베딩을 사용한 검색 수행
        
        Args:
            question: 사용자 질문
            max_results: 최대 반환 결과 수
            
        Returns:
            검색된 문서들의 리스트
        """
        logger.info(f"OpenAI 임베딩으로 검색 시작: {question}")
        
        # 질문을 OpenAI 임베딩으로 변환
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=question
        )
        question_embedding = response.data[0].embedding
        
        found_documents = []
        
        # 계층적 검색 수행
        # 1. 핵심 내용 검색
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
        
        # 2. 화제 기반 검색
        logger.info("주요 화제 테이블에서 검색 중...")
        main_topic_results = self.db.search_embeddings(
            'main_topic_embeddings', 
            question_embedding, 
            max_results
        )
        
        if main_topic_results and any(result['distance'] < self.similarity_threshold for result in main_topic_results):
            logger.info(f"주요 화제에서 {len(main_topic_results)}개 결과 발견")
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
        
        # 중복 제거 및 정렬
        unique_docs = {}
        for doc in found_documents:
            doc_id = doc['document_id']
            if doc_id not in unique_docs or doc['distance'] < unique_docs[doc_id]['distance']:
                unique_docs[doc_id] = doc
        
        final_results = sorted(unique_docs.values(), key=lambda x: x['distance'])[:max_results]
        logger.info(f"최종 {len(final_results)}개 문서 반환")
        return final_results

def save_results_to_file(results: List[Dict[str, Any]], question: str, db: NeonVectorDBV2, filename: str = "openai_search_results.txt"):
    """
    검색 결과를 파일에 저장
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"OpenAI 임베딩 검색 결과\n")
            f.write(f"검색 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"질문: {question}\n")
            f.write(f"임계값: 0.7\n")
            f.write(f"임베딩 모델: text-embedding-3-small\n")
            f.write("=" * 80 + "\n\n")
            
            if not results:
                f.write("검색 결과가 없습니다.\n")
                return
            
            for i, result in enumerate(results, 1):
                f.write(f"### 결과 {i}\n")
                f.write(f"문서 ID: {result['document_id']}\n")
                f.write(f"유사도: {1 - result['distance']:.4f}\n")
                f.write(f"거리: {result['distance']:.4f}\n")
                f.write(f"메타데이터: {result.get('metadata', {})}\n")
                f.write("-" * 50 + "\n")
                
                # 문서 상세 내용
                document = db.get_document_by_id(result['document_id'])
                if document:
                    f.write(f"제목: {document.get('title', 'N/A')}\n")
                    f.write(f"추출 정보 (처음 500자):\n{document.get('extracted_info', 'N/A')[:500]}...\n")
                    f.write(f"내용 (처음 300자):\n{document.get('content', 'N/A')[:300]}...\n")
                
                f.write("\n" + "=" * 80 + "\n\n")
        
        logger.info(f"검색 결과가 {filename}에 저장되었습니다.")
        
    except Exception as e:
        logger.error(f"결과 저장 실패: {e}")

def main():
    """
    메인 실행 함수
    """
    try:
        # OpenAI 임베딩 프로세서 초기화
        processor = OpenAIEmbeddingProcessor(similarity_threshold=0.7)
        
        # 기존 문서를 OpenAI 임베딩으로 재처리
        doc_id = "00_lev0_gpt_5_agentic_coding_with_claude_code_info"
        logger.info(f"문서 재임베딩 시작: {doc_id}")
        processor.process_document_embeddings(doc_id)
        
        # 동일한 질문으로 검색 수행
        question = "에이전트 작업에서 핵심적으로 중요한 것이 뭐야?"
        logger.info(f"검색 시작: {question}")
        results = processor.search_with_openai(question, max_results=3)
        
        # 결과를 파일에 저장
        filename = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-15/openai_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        save_results_to_file(results, question, processor.db, filename)
        
        # 콘솔에도 간단한 결과 출력
        print(f"\n🔍 OpenAI 임베딩 검색 완료!")
        print(f"📊 검색된 문서 수: {len(results)}")
        print(f"💾 상세 결과 저장: {filename}")
        
        if results:
            print(f"\n📈 최고 유사도: {1 - results[0]['distance']:.4f}")
            print(f"📉 최저 유사도: {1 - results[-1]['distance']:.4f}")
        
        # 데이터베이스 연결 종료
        processor.db.close()
        
    except Exception as e:
        logger.error(f"실행 실패: {e}")
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()