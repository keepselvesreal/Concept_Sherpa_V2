# 생성 시간: Thu Sep  4 11:55:47 KST 2025
# 핵심 내용: 노드 정보 문서 생성 서비스 (기존 NodeDocumentGenerator 로직을 새 아키텍처로 이관)
# 상세 내용:
#   - NodeDocumentService (라인 XX-XX): 노드 정보 문서 생성 서비스 클래스
#   - generate_documents_for_chapter (라인 XX-XX): 장별 노드 정보 문서 생성 메인 메서드
#   - create_single_document (라인 XX-XX): 개별 노드 문서 생성
#   - load_toc_file (라인 XX-XX): TOC 파일 로드 및 검증
#   - NodeDocumentTemplate (라인 XX-XX): 노드 문서 템플릿 관리 클래스
#   - NodeDocumentResult (라인 XX-XX): 생성 결과 데이터 클래스
# 상태: active
# 참조: extraction-system/pipeline/node_document_generator.py의 로직 이관

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.text_utils import normalize_title

class NodeDocumentTemplate:
    """노드 문서 템플릿 관리 클래스 (기존 NodeDocumentTemplate 로직 이관)"""
    
    # 템플릿 상수들
    NODE_INFO_FOLDER_NAME = "node_info_docs"
    FILE_NAME_FORMAT = "{id:02d}_lev{level}_{title}_info.md"
    
    # 기본 템플릿
    DEFAULT_TEMPLATE = """# 속성
---
process_status: false

# 추출
---

# 내용
---

# 구성
---
"""
    
    @classmethod
    def get_clean_title(cls, title: str) -> str:
        """제목을 파일명에 사용할 수 있도록 정리"""
        return normalize_title(title)
    
    @classmethod
    def get_filename(cls, node: Dict[str, Any]) -> str:
        """노드 정보로부터 파일명 생성"""
        clean_title = cls.get_clean_title(node['title'])
        return cls.FILE_NAME_FORMAT.format(
            id=node['id'],
            level=node['level'],
            title=clean_title
        )
    
    @classmethod
    def get_content(cls, custom_template: Optional[str] = None) -> str:
        """문서 내용 반환"""
        return custom_template if custom_template else cls.DEFAULT_TEMPLATE

class NodeDocumentResult:
    """노드 문서 생성 결과 데이터 클래스 (기존 NodeDocumentResult 로직 이관)"""
    
    def __init__(self):
        self.success = False
        self.created_count = 0
        self.failed_count = 0
        self.total_nodes = 0
        self.output_dir = ""
        self.error = None
        self.created_files = []
        self.failed_files = []
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리 형태로 변환"""
        return {
            'success': self.success,
            'created_count': self.created_count,
            'failed_count': self.failed_count,
            'total_nodes': self.total_nodes,
            'output_dir': self.output_dir,
            'error': self.error,
            'created_files': self.created_files,
            'failed_files': self.failed_files
        }

class NodeDocumentService:
    """노드 정보 문서 생성 서비스 (기존 NodeDocumentGenerator 로직 이관)"""
    
    def __init__(self, config_manager=None, logger=None):
        """
        Args:
            config_manager: 설정 관리자 (새 아키텍처 호환)
            logger: 로거 인스턴스 (새 아키텍처 호환)
        """
        self.config_manager = config_manager
        self.logger = logger
        self.template = NodeDocumentTemplate()
    
    def load_toc_file(self, toc_file_path: str) -> List[Dict[str, Any]]:
        """TOC 파일 로드 및 노드 리스트 반환 (기존 로직 이관)"""
        try:
            with open(toc_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # toc_structure가 있으면 그것을 반환, 없으면 전체 데이터가 노드 리스트라고 가정
            if isinstance(data, dict) and 'toc_structure' in data:
                return data['toc_structure']
            elif isinstance(data, list):
                return data
            else:
                raise ValueError(f"예상하지 못한 TOC 파일 형식: {toc_file_path}")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"TOC 파일을 찾을 수 없습니다: {toc_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"TOC 파일 JSON 파싱 실패: {e}")
        except Exception as e:
            raise Exception(f"TOC 파일 로드 실패: {e}")
    
    def create_single_document(self, node: Dict[str, Any], output_dir: str, 
                             custom_template: Optional[str] = None) -> bool:
        """단일 노드 문서 생성 (기존 로직 이관)"""
        try:
            # 필수 필드 검증
            required_fields = ['id', 'level', 'title']
            missing_fields = [field for field in required_fields if field not in node]
            if missing_fields:
                raise ValueError(f"노드에 필수 필드가 없습니다: {missing_fields}")
            
            # 출력 디렉토리 생성
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # 파일명 및 경로 생성
            filename = self.template.get_filename(node)
            filepath = os.path.join(output_dir, filename)
            
            # 문서 내용 생성
            content = self.template.get_content(custom_template)
            
            # 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.logger:
                self.logger.debug(f"노드 문서 생성 완료: {filename}")
            
            return True
            
        except Exception as e:
            error_msg = f"노드 문서 생성 실패 (ID: {node.get('id', '?')}): {e}"
            if self.logger:
                self.logger.error(error_msg)
            else:
                print(f"   ❌ {error_msg}")
            return False
    
    def generate_documents_for_chapter(self, chapter_folder: str, toc_file: str, 
                                     custom_template: Optional[str] = None) -> NodeDocumentResult:
        """특정 장의 TOC 파일을 기반으로 노드 정보 문서들 생성 (기존 로직 이관)"""
        result = NodeDocumentResult()
        
        try:
            if self.logger:
                self.logger.info(f"장별 노드 문서 생성 시작: {toc_file}")
            
            # TOC 파일 로드
            nodes = self.load_toc_file(toc_file)
            if not nodes:
                result.error = "TOC 파일에서 노드를 로드할 수 없음"
                return result
            
            result.total_nodes = len(nodes)
            
            if self.logger:
                self.logger.info(f"로드된 노드 수: {result.total_nodes}")
            
            # 노드 정보 문서 출력 디렉토리 생성
            node_docs_dir = os.path.join(chapter_folder, self.template.NODE_INFO_FOLDER_NAME)
            result.output_dir = node_docs_dir
            
            # 각 노드별 문서 생성
            for node in nodes:
                filename = self.template.get_filename(node)
                filepath = os.path.join(node_docs_dir, filename)
                
                if self.create_single_document(node, node_docs_dir, custom_template):
                    result.created_count += 1
                    result.created_files.append(filepath)
                else:
                    result.failed_count += 1
                    result.failed_files.append({
                        'node_id': node.get('id'),
                        'filename': filename,
                        'node_title': node.get('title')
                    })
            
            result.success = result.created_count > 0
            
            if self.logger:
                self.logger.info(f"노드 문서 생성 완료: 성공 {result.created_count}, 실패 {result.failed_count}")
            
            return result
            
        except Exception as e:
            result.error = str(e)
            result.success = False
            if self.logger:
                self.logger.error(f"노드 문서 생성 중 오류: {e}")
            return result