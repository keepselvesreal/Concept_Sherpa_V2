"""
생성 시간: 2025-08-18 12:22:54
핵심 내용: 사용자 질의 처리 및 임베딩 생성 컴포넌트
상세 내용:
    - QueryProcessor 클래스 (라인 25-120): 질의 전처리, 번역, 임베딩 담당
    - process_query 메서드 (라인 35-55): 메인 질의 처리 로직
    - translate_to_document_language 메서드 (라인 57-75): Claude SDK 기반 번역
    - generate_embedding 메서드 (라인 77-95): OpenAI 임베딩 생성
    - get_document_language 메서드 (라인 97-115): DB에서 문서 언어 조회
상태: 
주소: query_processor
참조: 
"""

import asyncio
import logging
import os
from typing import List, Dict, Any, Optional
import openai

# Sentence transformers for local embedding generation
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️ sentence-transformers를 찾을 수 없습니다. uv add sentence-transformers")

# Claude SDK 임포트
try:
    from claude_code_sdk import query, ClaudeCodeOptions
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("⚠️ claude_code_sdk를 찾을 수 없습니다. 번역 기능이 제한됩니다.")

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    사용자 질의 처리 및 임베딩 생성
    - 한국어 질의를 문서 언어로 번역 (필요시)
    - OpenAI 임베딩 생성
    """
    
    def __init__(self, db_adapter, config: Dict[str, Any]):
        self.db_adapter = db_adapter
        self.config = config
        self.user_language = "korean"  # 사용자 언어 고정
        
        # 임베딩 모델 선택 (환경변수 또는 기본값)
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        # Sentence Transformers 모델 초기화 (우선순위)
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
                self.use_local_model = True
                logger.info(f"✅ Sentence Transformers 모델 로드됨: {self.embedding_model_name}")
            except Exception as e:
                logger.warning(f"⚠️ Sentence Transformers 모델 로드 실패: {e}")
                self.use_local_model = False
        else:
            self.use_local_model = False
        
        # OpenAI 클라이언트 초기화 (백업)
        if not self.use_local_model:
            self.openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("✅ OpenAI 임베딩 클라이언트 사용")
        
        # Claude SDK 사용 가능 여부 확인
        self.claude_sdk_available = CLAUDE_SDK_AVAILABLE
    
    async def process_query(self, query: str, project_name: str) -> List[float]:
        """
        사용자 질의를 처리하여 임베딩 벡터 반환
        
        Args:
            query: 사용자 질의 (한국어)
            project_name: 프로젝트 이름
            
        Returns:
            임베딩 벡터
        """
        logger.info(f"질의 처리 시작: {query}")
        
        # 문서 언어 확인
        document_languages = await self.get_document_languages()
        
        if not document_languages:
            # 기본 언어 설정
            primary_doc_language = "english"
        else:
            # 가장 많이 사용되는 문서 언어 선택
            primary_doc_language = max(document_languages.items(), key=lambda x: x[1])[0]
        logger.info(f"주요 문서 언어: {primary_doc_language}")
        
        if primary_doc_language == "korean":
            # 한국어 문서 → 번역 불필요
            embedding_query = query
            logger.info("번역 불필요 (한국어 문서)")
        else:
            # 외국어 문서 → 한국어 질의를 문서 언어로 번역
            embedding_query = await self.translate_to_document_language(
                query, target_language=primary_doc_language
            )
            logger.info(f"번역 완료: {query} → {embedding_query}")
        
        # 임베딩 생성
        embedding = await self.generate_embedding(embedding_query)
        logger.info(f"임베딩 생성 완료: {len(embedding)}차원")
        
        return embedding
    
    async def translate_to_document_language(self, query: str, target_language: str) -> str:
        """
        Claude SDK를 사용하여 한국어 질의를 문서 언어로 번역
        
        Args:
            query: 한국어 질의
            target_language: 목표 언어
            
        Returns:
            번역된 질의
        """
        if not self.claude_sdk_available:
            logger.warning("Claude SDK 사용 불가, 원본 질의 반환")
            return query
            
        try:
            language_map = {
                "english": "English",
                "japanese": "Japanese", 
                "chinese": "Chinese",
                "spanish": "Spanish",
                "french": "French"
            }
            
            target_lang_name = language_map.get(target_language, target_language.title())
            
            prompt = f"다음 한국어 질의를 {target_lang_name}로 정확히 번역해주세요. 번역문만 출력하세요:\n\n{query}"
            system_prompt = f"번역 전문가. 한국어를 {target_lang_name}로 정확하고 자연스럽게 번역하세요."
            
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=system_prompt,
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            if messages:
                # 메시지 결과 추출 (참조 파일의 패턴 사용)
                last_message = messages[-1]
                if hasattr(last_message, 'result') and last_message.result:
                    return last_message.result.strip()
                elif hasattr(last_message, 'text'):
                    return last_message.text.strip()
                elif hasattr(last_message, 'content'):
                    if isinstance(last_message.content, list):
                        content = ""
                        for block in last_message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                        return content.strip()
                    else:
                        return str(last_message.content).strip()
                else:
                    return str(last_message).strip()
            else:
                logger.warning("Claude SDK 응답 없음")
                return query
            
        except Exception as e:
            logger.error(f"번역 오류: {e}")
            # 번역 실패시 원본 반환
            return query
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        로컬 Sentence Transformers 또는 OpenAI API를 사용하여 텍스트 임베딩 생성
        
        Args:
            text: 임베딩할 텍스트
            
        Returns:
            임베딩 벡터
        """
        try:
            if self.use_local_model:
                # Sentence Transformers 모델 사용 (기존 데이터와 호환)
                embedding = self.embedding_model.encode(text).tolist()
                logger.debug(f"로컬 모델 임베딩 생성: {len(embedding)}차원")
                return embedding
            else:
                # OpenAI API 사용 (백업)
                response = self.openai_client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                embedding = response.data[0].embedding
                logger.debug(f"OpenAI 임베딩 생성: {len(embedding)}차원")
                return embedding
            
        except Exception as e:
            logger.error(f"임베딩 생성 오류: {e}")
            raise
    
    async def get_document_languages(self) -> Dict[str, int]:
        """
        문서 언어 분포 조회
        
        Returns:
            언어별 문서 수 딕셔너리
        """
        try:
            query = """
            SELECT document_language, COUNT(*) as count 
            FROM documents 
            WHERE document_language IS NOT NULL
            GROUP BY document_language
            """
            
            results = await self.db_adapter.query_data(
                "documents", 
                custom_query=query
            )
            
            language_counts = {row['document_language']: row['count'] for row in results}
            logger.info(f"문서 언어 분포: {language_counts}")
            
            return language_counts
            
        except Exception as e:
            logger.error(f"문서 언어 조회 오류: {e}")
            # 기본값으로 한국어 반환
            return {"korean": 1}