"""
생성 시간: 2025-08-15 17:25:00
핵심 내용: OpenAI 1536차원 임베딩을 사용한 문서 재임베딩 및 검색 시스템
상세 내용:
    - OpenAIEmbeddingProcessor 클래스(라인 29-131): OpenAI 임베딩 처리
    - process_document_embeddings 메서드(라인 36-80): 문서를 OpenAI로 재임베딩
    - search_with_openai 메서드(라인 82-131): 계층적 벡터 검색
    - save_results_to_file 함수(라인 133-180): 결과를 파일에 상세 저장
    - main 함수(라인 182-220): 전체 워크플로우 실행
    - 임계값: 0.7 설정, 1536차원 OpenAI 임베딩 사용
상태: 
주소: openai_embedding_search_v2
참조: openai_neon_db
"""

import os
import sys
import json
from typing import List, Dict, Any
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from openai_neon_db import OpenAINeonVectorDB
from neon_db_v2 import NeonVectorDBV2, DocumentParser

# 환경변수 로드
load_dotenv(dotenv_path='/home/nadle/projects/Concept_Sherpa_V2/.env')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIEmbeddingProcessor:
    """
    OpenAI 임베딩 모델을 사용한 문서 처리 및 검색 클래스 (1536차원)
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.openai_db = OpenAINeonVectorDB()  # OpenAI 전용 DB
        self.similarity_threshold = similarity_threshold
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API 키가 필요합니다. .env 파일의 OPENAI_API_KEY를 확인하세요.")
    
    def process_document_embeddings(self, file_path: str, doc_id: str):
        """
        문서 파일을 파싱하고 OpenAI 임베딩으로 처리
        
        Args:
            file_path: 문서 파일 경로
            doc_id: 문서 ID
        """
        logger.info(f"문서 {doc_id}를 OpenAI 임베딩으로 처리 중...")
        
        # 문서 파싱
        parsed_doc = DocumentParser.parse_document(file_path)
        
        # 전체 추출 섹션 구성
        extracted_sections = [
            f"## 핵심 내용\n{parsed_doc['core_content']}",
            f"## 상세 핵심 내용\n{parsed_doc['detailed_core']}",
            f"## 주요 화제\n{parsed_doc['main_topics']}",
            f"## 부차 화제\n{parsed_doc['sub_topics']}"
        ]
        extracted_info = "\n\n".join(extracted_sections)
        
        # documents 테이블에 삽입
        self.openai_db.insert_document(
            doc_id=doc_id,
            title=parsed_doc['title'],
            extracted_info=extracted_info,
            content=parsed_doc['content'],
            child_doc_ids=parsed_doc['child_doc_ids']
        )
        
        # 각 섹션별로 OpenAI 임베딩 생성
        sections = [
            ("openai_core_content_embeddings", "core", parsed_doc['core_content']),
            ("openai_detailed_core_embeddings", "detailed", parsed_doc['detailed_core']),
            ("openai_main_topic_embeddings", "main", parsed_doc['main_topics']),
            ("openai_sub_topic_embeddings", "sub", parsed_doc['sub_topics'])
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
                    "dimensions": 1536,
                    "language": "mixed",
                    "file_name": parsed_doc['title'],
                    "content_length": len(content)
                }
                
                self.openai_db.insert_embedding(
                    table_name=table_name,
                    embedding_id=embedding_id,
                    embedding=embedding,
                    document_id=doc_id,
                    metadata=metadata
                )
                
                logger.info(f"OpenAI 임베딩 저장 완료: {table_name} - {embedding_id}")
    
    def search_with_openai(self, question: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        OpenAI 임베딩을 사용한 계층적 검색 수행
        
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
        search_log = []
        
        # 1. 내용 기반 계층적 검색 (핵심 → 상세)
        logger.info("핵심 내용 테이블에서 검색 중...")
        core_results = self.openai_db.search_embeddings(
            'openai_core_content_embeddings', 
            question_embedding, 
            max_results
        )
        
        if core_results and any(result['distance'] < self.similarity_threshold for result in core_results):
            logger.info(f"핵심 내용에서 {len(core_results)}개 결과 발견 (임계값 {self.similarity_threshold} 통과)")
            found_documents.extend(core_results)
            search_log.append(f"✅ 핵심 내용 테이블: {len(core_results)}개 결과 (최고 유사도: {1-min(r['distance'] for r in core_results):.4f})")
        else:
            logger.info("핵심 내용에서 유사한 결과 없음, 상세 핵심 내용 검색 중...")
            search_log.append(f"⚠️ 핵심 내용 테이블: 임계값 미달, 상세 검색으로 이동")
            
            detailed_results = self.openai_db.search_embeddings(
                'openai_detailed_core_embeddings', 
                question_embedding, 
                max_results
            )
            if detailed_results:
                logger.info(f"상세 핵심 내용에서 {len(detailed_results)}개 결과 발견")
                found_documents.extend(detailed_results)
                search_log.append(f"✅ 상세 핵심 내용 테이블: {len(detailed_results)}개 결과 (최고 유사도: {1-min(r['distance'] for r in detailed_results):.4f})")
            else:
                search_log.append(f"❌ 상세 핵심 내용 테이블: 결과 없음")
        
        # 2. 화제 기반 계층적 검색 (주요 → 부차) - 독립적으로 수행
        logger.info("주요 화제 테이블에서 검색 중...")
        main_topic_results = self.openai_db.search_embeddings(
            'openai_main_topic_embeddings', 
            question_embedding, 
            max_results
        )
        
        if main_topic_results and any(result['distance'] < self.similarity_threshold for result in main_topic_results):
            logger.info(f"주요 화제에서 {len(main_topic_results)}개 결과 발견")
            found_documents.extend(main_topic_results)
            search_log.append(f"✅ 주요 화제 테이블: {len(main_topic_results)}개 결과 (최고 유사도: {1-min(r['distance'] for r in main_topic_results):.4f})")
        else:
            logger.info("주요 화제에서 유사한 결과 없음, 부차 화제 검색 중...")
            search_log.append(f"⚠️ 주요 화제 테이블: 임계값 미달, 부차 검색으로 이동")
            
            sub_topic_results = self.openai_db.search_embeddings(
                'openai_sub_topic_embeddings', 
                question_embedding, 
                max_results
            )
            if sub_topic_results:
                logger.info(f"부차 화제에서 {len(sub_topic_results)}개 결과 발견")
                found_documents.extend(sub_topic_results)
                search_log.append(f"✅ 부차 화제 테이블: {len(sub_topic_results)}개 결과 (최고 유사도: {1-min(r['distance'] for r in sub_topic_results):.4f})")
            else:
                search_log.append(f"❌ 부차 화제 테이블: 결과 없음")
        
        # 3. 중복 제거 및 정렬
        unique_docs = {}
        for doc in found_documents:
            doc_id = doc['document_id']
            if doc_id not in unique_docs or doc['distance'] < unique_docs[doc_id]['distance']:
                unique_docs[doc_id] = doc
        
        final_results = sorted(unique_docs.values(), key=lambda x: x['distance'])[:max_results]
        logger.info(f"최종 {len(final_results)}개 문서 반환")
        
        # 검색 로그도 결과에 포함
        for result in final_results:
            result['search_log'] = search_log
        
        return final_results

def save_results_to_file(results: List[Dict[str, Any]], question: str, db: OpenAINeonVectorDB, filename: str):
    """
    검색 결과를 파일에 상세 저장
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("OpenAI 임베딩 벡터 검색 결과 보고서\n")
            f.write("=" * 100 + "\n")
            f.write(f"검색 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"질문: {question}\n")
            f.write(f"임계값: 0.7\n")
            f.write(f"임베딩 모델: text-embedding-3-small (1536차원)\n")
            f.write(f"총 검색 결과: {len(results)}개\n")
            f.write("=" * 100 + "\n\n")
            
            # 검색 로그 출력
            if results and 'search_log' in results[0]:
                f.write("🔍 검색 과정 로그:\n")
                for log_entry in results[0]['search_log']:
                    f.write(f"  {log_entry}\n")
                f.write("\n" + "-" * 80 + "\n\n")
            
            if not results:
                f.write("❌ 검색 결과가 없습니다.\n")
                return
            
            for i, result in enumerate(results, 1):
                f.write(f"📄 검색 결과 {i}/{len(results)}\n")
                f.write("-" * 50 + "\n")
                f.write(f"문서 ID: {result['document_id']}\n")
                f.write(f"임베딩 ID: {result['id']}\n")
                f.write(f"유사도: {1 - result['distance']:.6f}\n")
                f.write(f"코사인 거리: {result['distance']:.6f}\n")
                f.write(f"메타데이터: {json.dumps(result.get('metadata', {}), ensure_ascii=False, indent=2)}\n")
                f.write("\n")
                
                # 문서 상세 내용
                document = db.get_document_by_id(result['document_id'])
                if document:
                    f.write(f"📋 문서 상세 정보:\n")
                    f.write(f"  제목: {document.get('title', 'N/A')}\n")
                    f.write(f"  추출 정보 길이: {len(document.get('extracted_info', ''))}\n")
                    f.write(f"  내용 길이: {len(document.get('content', ''))}\n")
                    f.write("\n")
                    f.write("📝 추출 정보 (처음 1000자):\n")
                    f.write(f"{document.get('extracted_info', 'N/A')[:1000]}...\n\n")
                
                f.write("=" * 100 + "\n\n")
        
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
        
        # 문서 파일 경로와 ID
        file_path = "/home/nadle/projects/Concept_Sherpa_V2/25-08-15/00_lev0_gpt_5_agentic_coding_with_claude_code_info.md"
        doc_id = "00_lev0_gpt_5_agentic_coding_with_claude_code_info"
        
        # 문서를 OpenAI 임베딩으로 처리
        logger.info(f"문서 OpenAI 임베딩 처리 시작: {doc_id}")
        processor.process_document_embeddings(file_path, doc_id)
        
        # 동일한 질문으로 검색 수행
        question = "에이전트 작업에서 핵심적으로 중요한 것이 뭐야?"
        logger.info(f"OpenAI 임베딩 검색 시작: {question}")
        results = processor.search_with_openai(question, max_results=3)
        
        # 결과를 파일에 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-15/openai_search_results_{timestamp}.txt"
        save_results_to_file(results, question, processor.openai_db, filename)
        
        # 콘솔 출력
        print(f"\n🎉 OpenAI 임베딩 검색 완료!")
        print(f"🔧 임베딩 모델: text-embedding-3-small (1536차원)")
        print(f"⚡ 임계값: 0.7")
        print(f"📊 검색된 문서 수: {len(results)}")
        print(f"💾 상세 결과 저장: {filename}")
        
        if results:
            print(f"\n📈 최고 유사도: {1 - results[0]['distance']:.6f}")
            print(f"📉 최저 유사도: {1 - results[-1]['distance']:.6f}")
            print(f"🎯 사용된 벡터 테이블: {results[0]['search_log']}")
        
        # 데이터베이스 연결 종료
        processor.openai_db.close()
        
    except Exception as e:
        logger.error(f"실행 실패: {e}")
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()