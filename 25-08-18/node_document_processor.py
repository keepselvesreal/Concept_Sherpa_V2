"""
생성 시간: 2025-08-18 11:12:45
핵심 내용: 노드 정보 문서를 파싱하여 데이터베이스에 저장하는 처리기
상세 내용:
    - NodeDocumentProcessor 클래스 (라인 30-250): 노드 문서 처리 메인 클래스
    - Enhanced DocumentParser 클래스 (라인 252-380): 메타데이터 포함 문서 파싱
    - parse_metadata 메서드 (라인 50-80): YAML 메타데이터 파싱
    - parse_document_sections 메서드 (라인 82-150): 문서 섹션별 파싱
    - process_node_document 메서드 (라인 152-220): 문서 처리 및 DB 저장
    - generate_and_store_embeddings 메서드 (라인 222-250): 임베딩 생성 및 저장
    - 새 필드 지원: source, source_type, structure_type, document_language
상태: 
주소: node_document_processor
참조: neon_db_v2, database_interface
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv('/home/nadle/projects/Knowledge_Sherpa/v2/.env')

# 프로젝트 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from adapters.postgresql_adapter import PostgreSQLAdapter
from utils.config_loader import ConfigLoader

# 임베딩 관련 imports
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDocumentParser:
    """
    메타데이터를 포함한 노드 문서 파싱 클래스
    """
    
    @staticmethod
    def parse_metadata(content: str) -> Dict[str, Any]:
        """
        YAML 메타데이터 파싱
        
        Args:
            content: 전체 문서 내용
            
        Returns:
            메타데이터 딕셔너리
        """
        metadata = {}
        lines = content.split('\n')
        
        # 첫 번째 # 속성 섹션에서 메타데이터 추출
        in_metadata = False
        for line in lines:
            line = line.strip()
            
            if line == "# 속성":
                in_metadata = True
                continue
            elif line.startswith("# ") and in_metadata:
                break
            elif line == "---" and in_metadata:
                continue
            elif in_metadata and line and ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        return metadata
    
    @staticmethod
    def parse_document_sections(content: str) -> Dict[str, str]:
        """
        문서 섹션별 파싱
        
        Args:
            content: 전체 문서 내용
            
        Returns:
            섹션별 내용 딕셔너리
        """
        lines = content.split('\n')
        
        # 섹션 분리
        sections = {
            'core_content': "",
            'detailed_core': "",
            'main_topics': "",
            'sub_topics': "",
            'document_content': "",
            'child_doc_ids': ""
        }
        
        current_section = None
        in_extraction = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # 메인 섹션 헤더 감지
            if line_stripped == "# 추출":
                in_extraction = True
                current_section = "extraction"
                continue
            elif line_stripped == "# 내용":
                in_extraction = False
                current_section = "content"
                continue
            elif line_stripped == "# 구성":
                in_extraction = False
                current_section = "components"
                continue
            
            # 추출 섹션 내 서브섹션 헤더 감지
            elif line_stripped == "## 핵심 내용" and in_extraction:
                current_section = "core_content"
                continue
            elif line_stripped == "## 상세 핵심 내용" and in_extraction:
                current_section = "detailed_core"
                continue
            elif line_stripped == "## 주요 화제" and in_extraction:
                current_section = "main_topics"
                continue
            elif line_stripped == "## 부차 화제" and in_extraction:
                current_section = "sub_topics"
                continue
            
            # 내용 추가
            if current_section == "core_content":
                if not line_stripped.startswith("##") and line_stripped not in ["# 내용", "# 구성", "---"]:
                    sections['core_content'] += line + "\n"
            elif current_section == "detailed_core":
                if not line_stripped.startswith("##") and line_stripped not in ["# 내용", "# 구성", "---"]:
                    sections['detailed_core'] += line + "\n"
            elif current_section == "main_topics":
                if not line_stripped.startswith("##") and line_stripped not in ["# 내용", "# 구성", "---"]:
                    sections['main_topics'] += line + "\n"
            elif current_section == "sub_topics":
                if not line_stripped.startswith("##") and line_stripped not in ["# 내용", "# 구성", "---"]:
                    sections['sub_topics'] += line + "\n"
            elif current_section == "content":
                if line_stripped not in ["---"] and not line_stripped.startswith("# 구성"):
                    sections['document_content'] += line + "\n"
            elif current_section == "components":
                sections['child_doc_ids'] += line + "\n"
        
        # 문자열 정리
        for key in sections:
            sections[key] = sections[key].strip()
        
        return sections

class NodeDocumentProcessor:
    """
    노드 정보 문서를 처리하여 데이터베이스에 저장하는 클래스
    """
    
    def __init__(self, project_name: str = "knowledge_sherpa"):
        """
        노드 문서 처리기 초기화
        
        Args:
            project_name: 사용할 프로젝트명
        """
        self.project_name = project_name
        self.config_loader = ConfigLoader()
        self.db_adapter = None
        self.embedding_model = None
        
        # 프로젝트 로드
        self._load_project()
    
    def _load_project(self):
        """프로젝트 설정을 로드하고 DB 어댑터 초기화"""
        try:
            project_config = self.config_loader.get_project_config(self.project_name)
            if not project_config:
                raise ValueError(f"프로젝트 '{self.project_name}'을 찾을 수 없습니다.")
            
            # PostgreSQL 어댑터 초기화
            adapter_type = project_config.get('adapter', 'postgresql')
            if adapter_type == 'postgresql':
                self.db_adapter = PostgreSQLAdapter(project_config)
                if not self.db_adapter.connect():
                    raise ConnectionError("데이터베이스 연결에 실패했습니다.")
            else:
                raise ValueError(f"지원되지 않는 어댑터 타입: {adapter_type}")
            
            logger.info(f"프로젝트 '{self.project_name}' 로드 완료")
            
        except Exception as e:
            logger.error(f"프로젝트 로드 실패: {e}")
            raise
    
    def _load_embedding_model(self):
        """임베딩 모델 로드 (지연 로딩)"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning("sentence-transformers가 설치되지 않았습니다. 임베딩 생성을 건너뜁니다.")
            return
        
        if self.embedding_model is None:
            model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            logger.info(f"임베딩 모델 로드 중: {model_name}")
            self.embedding_model = SentenceTransformer(model_name)
            logger.info("임베딩 모델 로드 완료")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        텍스트 리스트에서 임베딩 생성
        
        Args:
            texts: 임베딩을 생성할 텍스트 리스트
            
        Returns:
            임베딩 벡터 리스트
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE or not texts:
            return []
        
        try:
            self._load_embedding_model()
            if self.embedding_model is None:
                return []
            
            # 빈 텍스트 필터링
            valid_texts = [text.strip() for text in texts if text.strip()]
            if not valid_texts:
                return []
            
            embeddings = self.embedding_model.encode(valid_texts)
            
            # numpy array를 list로 변환
            if hasattr(embeddings, 'tolist'):
                embeddings = embeddings.tolist()
            else:
                embeddings = [emb.tolist() if hasattr(emb, 'tolist') else list(emb) for emb in embeddings]
            
            logger.info(f"임베딩 생성 완료: {len(embeddings)}개")
            return embeddings
            
        except Exception as e:
            logger.error(f"임베딩 생성 실패: {e}")
            return []
    
    def process_node_document(self, file_path: str, doc_id: Optional[str] = None, 
                             generate_embeddings: bool = True) -> str:
        """
        노드 문서 파일을 처리하여 데이터베이스에 저장
        
        Args:
            file_path: 문서 파일 경로
            doc_id: 문서 ID (None이면 파일명 사용)
            generate_embeddings: 임베딩을 생성할지 여부
            
        Returns:
            생성된 문서 ID
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
            # 문서 ID 생성
            if doc_id is None:
                doc_id = file_path.stem
            
            # 문서 내용 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 메타데이터 파싱
            metadata = EnhancedDocumentParser.parse_metadata(content)
            
            # 문서 섹션 파싱
            sections = EnhancedDocumentParser.parse_document_sections(content)
            
            # 전체 추출 정보 구성
            extracted_sections = []
            if sections['core_content']:
                extracted_sections.append(f"## 핵심 내용\n{sections['core_content']}")
            if sections['detailed_core']:
                extracted_sections.append(f"## 상세 핵심 내용\n{sections['detailed_core']}")
            if sections['main_topics']:
                extracted_sections.append(f"## 주요 화제\n{sections['main_topics']}")
            if sections['sub_topics']:
                extracted_sections.append(f"## 부차 화제\n{sections['sub_topics']}")
            
            extracted_info = "\n\n".join(extracted_sections)
            
            # 파일명에서 source 정보 추출
            source = file_path.name
            
            # 문서 데이터 준비
            document_data = {
                'id': doc_id,
                'title': file_path.name,
                'extracted_info': extracted_info,
                'content': sections['document_content'],
                'informed_toc': None,  # 필요시 설정
                'child_doc_ids': sections['child_doc_ids'] if sections['child_doc_ids'] else None,
                'source': source,
                'source_type': metadata.get('source_type', 'unknown'),
                'structure_type': metadata.get('structure_type', 'unknown'),
                'document_language': metadata.get('document_language', 'unknown')
            }
            
            # documents 테이블에 삽입
            success = self.db_adapter.insert_data('documents', document_data)
            if not success:
                raise Exception("문서 삽입 실패")
            
            logger.info(f"문서 저장 완료: {doc_id}")
            
            # 임베딩 생성 및 저장
            if generate_embeddings:
                self._generate_and_store_embeddings(doc_id, sections, metadata)
            
            return doc_id
            
        except Exception as e:
            logger.error(f"문서 처리 실패 ({file_path}): {e}")
            raise
    
    def _generate_and_store_embeddings(self, doc_id: str, sections: Dict[str, str], 
                                      metadata: Dict[str, Any]):
        """
        각 섹션의 임베딩을 생성하고 해당 테이블에 저장
        
        Args:
            doc_id: 문서 ID
            sections: 파싱된 섹션들
            metadata: 문서 메타데이터
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning("임베딩 생성을 건너뜁니다 (sentence-transformers 미설치)")
            return
        
        try:
            logger.info(f"임베딩 생성 시작: {doc_id}")
            
            # 임베딩을 생성할 섹션들
            embedding_data = [
                ("core_content_embeddings", "core", sections['core_content']),
                ("detailed_core_embeddings", "detailed", sections['detailed_core']),
                ("main_topic_embeddings", "main", sections['main_topics']),
                ("sub_topic_embeddings", "sub", sections['sub_topics'])
            ]
            
            for table_name, section_type, content in embedding_data:
                if content.strip():  # 내용이 있는 경우만 처리
                    # 임베딩 생성
                    embeddings = self.generate_embeddings([content])
                    if embeddings:
                        embedding_id = f"{doc_id}_{section_type}_001"
                        
                        # 메타데이터 구성
                        embedding_metadata = {
                            "section_type": section_type,
                            "source_type": metadata.get('source_type', 'unknown'),
                            "structure_type": metadata.get('structure_type', 'unknown'),
                            "document_language": metadata.get('document_language', 'unknown'),
                            "content_length": len(content),
                            "created_at": datetime.now().isoformat()
                        }
                        
                        # 임베딩 데이터 준비
                        embedding_data_row = {
                            'id': embedding_id,
                            'embedding': embeddings[0],
                            'document_id': doc_id,
                            'metadata': embedding_metadata
                        }
                        
                        # 임베딩 저장
                        success = self.db_adapter.insert_data(table_name, embedding_data_row)
                        if success:
                            logger.info(f"임베딩 저장 완료: {table_name} - {embedding_id}")
                        else:
                            logger.error(f"임베딩 저장 실패: {table_name} - {embedding_id}")
            
            logger.info(f"모든 임베딩 처리 완료: {doc_id}")
            
        except Exception as e:
            logger.error(f"임베딩 처리 실패 ({doc_id}): {e}")
            raise
    
    def process_directory(self, directory_path: str, pattern: str = "*_info.md") -> List[str]:
        """
        디렉토리 내의 모든 노드 문서를 처리
        
        Args:
            directory_path: 처리할 디렉토리 경로
            pattern: 파일 패턴 (기본값: *_info.md)
            
        Returns:
            처리된 문서 ID 리스트
        """
        try:
            directory = Path(directory_path)
            if not directory.exists():
                raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {directory_path}")
            
            # 패턴에 맞는 파일 찾기
            files = list(directory.glob(pattern))
            if not files:
                logger.warning(f"패턴 '{pattern}'에 맞는 파일이 없습니다: {directory_path}")
                return []
            
            processed_docs = []
            for file_path in files:
                try:
                    doc_id = self.process_node_document(file_path)
                    processed_docs.append(doc_id)
                    logger.info(f"처리 완료: {file_path.name} -> {doc_id}")
                except Exception as e:
                    logger.error(f"파일 처리 실패 ({file_path}): {e}")
                    continue
            
            logger.info(f"디렉토리 처리 완료: {len(processed_docs)}/{len(files)}개 파일")
            return processed_docs
            
        except Exception as e:
            logger.error(f"디렉토리 처리 실패 ({directory_path}): {e}")
            raise
    
    def close(self):
        """리소스 정리"""
        if self.db_adapter:
            self.db_adapter.close()
            logger.info("데이터베이스 연결 종료")

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='노드 문서 처리기')
    parser.add_argument('--file', '-f', help='처리할 단일 파일 경로')
    parser.add_argument('--directory', '-d', help='처리할 디렉토리 경로')
    parser.add_argument('--pattern', '-p', default='*_info.md', help='파일 패턴 (기본값: *_info.md)')
    parser.add_argument('--project', default='knowledge_sherpa', help='사용할 프로젝트명')
    parser.add_argument('--no-embeddings', action='store_true', help='임베딩 생성 건너뛰기')
    
    args = parser.parse_args()
    
    if not args.file and not args.directory:
        parser.print_help()
        return
    
    processor = None
    try:
        # 처리기 초기화
        processor = NodeDocumentProcessor(args.project)
        
        generate_embeddings = not args.no_embeddings
        
        if args.file:
            # 단일 파일 처리
            doc_id = processor.process_node_document(args.file, generate_embeddings=generate_embeddings)
            print(f"문서 처리 완료: {doc_id}")
        
        if args.directory:
            # 디렉토리 처리
            processed_docs = processor.process_directory(args.directory, args.pattern)
            print(f"처리 완료: {len(processed_docs)}개 문서")
            for doc_id in processed_docs:
                print(f"  - {doc_id}")
        
    except Exception as e:
        logger.error(f"처리 실패: {e}")
        print(f"오류 발생: {e}")
    finally:
        if processor:
            processor.close()

if __name__ == "__main__":
    main()