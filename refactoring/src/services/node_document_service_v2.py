# 생성 시간: Wed Sep 10 14:59:03 KST 2025
# 핵심 내용: 데이터 기반 노드 정보 문서 생성 서비스 (메모리 내 처리, 파일 저장 제거)
# 상세 내용:
#   - NodeDocumentTemplate (라인 23-50): 노드 문서 템플릿 관리 클래스
#   - NodeDocumentService (라인 52-120): 메인 노드 문서 생성 서비스 클래스 (데이터 기반)
#   - generate_documents_for_chapter (라인 72-110): 챕터별 노드 문서 생성 (List[Dict] 반환)
#   - create_single_document (라인 112-120): 개별 노드 문서 생성 (메모리 내)
# 상태: active
# 참조: node_document_service.py (데이터 기반 처리로 완전 개편)

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# text_utils import
sys.path.append(str(Path(__file__).parent.parent))
from utils.text_utils import normalize_title

class NodeDocumentTemplate:
    """노드 문서 템플릿 관리 클래스"""
    
    # 템플릿 상수들
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

class NodeDocumentService:
    """데이터 기반 노드 정보 문서 생성 서비스"""
    
    def __init__(self, config_manager=None, logger=None):
        """
        Args:
            config_manager: 설정 관리자
            logger: 로거 인스턴스
        """
        self.config_manager = config_manager
        self.logger = logger
        self.template = NodeDocumentTemplate()
    
    def generate_documents_for_chapter(self, chapter_info: Dict[str, Any], 
                                     custom_template: Optional[str] = None) -> List[Dict[str, str]]:
        """
        챕터별 노드 정보 문서 생성 (메모리 내 처리)
        
        Args:
            chapter_info: {
                'chapter_title': str,
                'chapter_toc': List[Dict],
                'content_text': str (사용 안함)
            }
            custom_template: 사용자 정의 템플릿
            
        Returns:
            List[Dict]: [{'file_name': str, 'content': str}, ...]
        """
        try:
            chapter_title = chapter_info.get('chapter_title', 'Unknown Chapter')
            chapter_toc = chapter_info.get('chapter_toc', [])
            
            if self.logger:
                self.logger.info(f"노드 문서 생성 시작: {chapter_title} (노드 수: {len(chapter_toc)})")
            
            if not chapter_toc:
                if self.logger:
                    self.logger.warning(f"⚠️ {chapter_title}: chapter_toc가 비어있습니다")
                return []
            
            generated_documents = []
            
            # 각 노드별 문서 생성
            for node in chapter_toc:
                document_data = self.create_single_document(node, custom_template)
                if document_data:
                    generated_documents.append(document_data)
            
            if self.logger:
                self.logger.info(f"✅ 노드 문서 생성 완료: {len(generated_documents)}개")
            
            return generated_documents
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ 노드 문서 생성 중 오류: {str(e)}")
            return []
    
    def create_single_document(self, node: Dict[str, Any], 
                             custom_template: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        개별 노드 문서 생성 (메모리 내)
        
        Args:
            node: TOC 노드 정보
            custom_template: 사용자 정의 템플릿
            
        Returns:
            Dict: {'file_name': str, 'content': str} or None
        """
        try:
            # 파일명 생성
            filename = self.template.get_filename(node)
            
            # 문서 내용 생성 (기존 방식)
            content = self.template.get_content(custom_template)
            
            return {
                'file_name': f"node_info_docs/{filename}",
                'content': content
            }
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ 개별 노드 문서 생성 실패 (노드 ID: {node.get('id', 'Unknown')}): {str(e)}")
            return None