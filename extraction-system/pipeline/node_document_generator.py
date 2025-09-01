# 생성 시간: Mon Sep  1 16:30:15 KST 2025
# 핵심 내용: 노드 정보 문서 생성 전담 모듈 (템플릿과 생성기 클래스 분리)
# 상세 내용:
#   - NodeDocumentTemplate (line 15-35): 노드 문서 템플릿 관리 클래스
#   - NodeDocumentGenerator (line 37-150): 노드 문서 생성 전담 클래스
#   - NodeDocumentResult (line 152-165): 생성 결과 데이터 클래스
# 상태: active
# 주소: node_document_generator
# 참조: book_pipeline_v2.py에서 분리하여 독립 모듈화

import os
import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class NodeDocumentTemplate:
    """노드 문서 템플릿 관리 클래스"""
    
    # 템플릿 상수들
    NODE_INFO_FOLDER_NAME = "node_info_docs"
    FILE_NAME_FORMAT = "{id:02d}_lev{level}_{title}_info.md"
    
    # 기본 템플릿 (추출 섹션 하위 내용 제거된 버전)
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
        """제목을 파일명에 사용할 수 있도록 정리합니다."""
        title_clean = re.sub(r'[^\w\s.-]', '', title)  # 점(.)도 유지
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        return title_clean
    
    @classmethod
    def get_filename(cls, node: Dict[str, Any]) -> str:
        """노드 정보로부터 파일명을 생성합니다."""
        clean_title = cls.get_clean_title(node['title'])
        return cls.FILE_NAME_FORMAT.format(
            id=node['id'],
            level=node['level'],
            title=clean_title
        )
    
    @classmethod
    def get_content(cls, custom_template: Optional[str] = None) -> str:
        """문서 내용을 반환합니다."""
        return custom_template if custom_template else cls.DEFAULT_TEMPLATE

class NodeDocumentResult:
    """노드 문서 생성 결과 데이터 클래스"""
    
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
        """딕셔너리 형태로 변환합니다."""
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

class NodeDocumentGenerator:
    """노드 정보 문서 생성 전담 클래스"""
    
    def __init__(self, template: Optional[NodeDocumentTemplate] = None):
        """
        Args:
            template: 사용할 템플릿 클래스 (기본값: NodeDocumentTemplate)
        """
        self.template = template or NodeDocumentTemplate()
    
    def load_toc_file(self, toc_file_path: str) -> List[Dict[str, Any]]:
        """TOC 파일을 로드하여 노드 리스트를 반환합니다."""
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
        """단일 노드 문서를 생성합니다."""
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
            
            return True
            
        except Exception as e:
            print(f"   ❌ 노드 문서 생성 실패 (ID: {node.get('id', '?')}): {e}")
            return False
    
    def generate_documents_for_chapter(self, chapter_folder: str, toc_file: str, 
                                     custom_template: Optional[str] = None) -> NodeDocumentResult:
        """특정 장의 TOC 파일을 기반으로 노드 정보 문서들을 생성합니다."""
        result = NodeDocumentResult()
        
        try:
            # TOC 파일 로드
            nodes = self.load_toc_file(toc_file)
            if not nodes:
                result.error = "TOC 파일에서 노드를 로드할 수 없음"
                return result
            
            result.total_nodes = len(nodes)
            
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
            return result
            
        except Exception as e:
            result.error = str(e)
            result.success = False
            return result
    
    def generate_documents_for_multiple_chapters(self, chapters_data: Dict[str, Any], 
                                               custom_template: Optional[str] = None) -> Dict[str, Any]:
        """모든 장별 폴더에 노드 정보 문서들을 생성합니다."""
        try:
            created_folders = chapters_data.get('created_folders', [])
            if not created_folders:
                return {
                    'success': False,
                    'error': '처리할 장별 폴더가 없음',
                    'processed_chapters': 0,
                    'total_documents_created': 0
                }
            
            processed_chapters = 0
            total_documents_created = 0
            chapter_results = []
            
            for chapter_info in created_folders:
                chapter_title = chapter_info.get('chapter_title', '')
                folder_path = chapter_info.get('folder_path', '')
                toc_file = chapter_info.get('toc_file', '')
                
                print(f"\n📖 {chapter_title} 노드 문서 생성 중...")
                
                # 폴더와 TOC 파일 검증
                if not folder_path or not os.path.exists(folder_path):
                    chapter_results.append({
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': '장별 폴더 없음'
                    })
                    continue
                
                if not toc_file or not os.path.exists(toc_file):
                    chapter_results.append({
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': 'TOC 파일 없음'
                    })
                    continue
                
                try:
                    # 각 장별 노드 문서 생성
                    result = self.generate_documents_for_chapter(folder_path, toc_file, custom_template)
                    
                    if result.success:
                        total_documents_created += result.created_count
                        processed_chapters += 1
                        
                        chapter_results.append({
                            'chapter_title': chapter_title,
                            'success': True,
                            'documents_created': result.created_count,
                            'total_nodes': result.total_nodes,
                            'output_dir': result.output_dir,
                            'failed_count': result.failed_count,
                            'created_files': result.created_files
                        })
                        
                        print(f"✅ {chapter_title}: {result.created_count}개 노드 문서 생성 완료")
                    else:
                        print(f"❌ {chapter_title}: {result.error}")
                        chapter_results.append({
                            'chapter_title': chapter_title,
                            'success': False,
                            'error': result.error
                        })
                
                except Exception as e:
                    print(f"❌ {chapter_title} 처리 중 오류: {str(e)}")
                    chapter_results.append({
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': str(e)
                    })
            
            successful_chapters = len([r for r in chapter_results if r.get('success', False)])
            
            return {
                'success': True,
                'processed_chapters': successful_chapters,
                'total_chapters': len(created_folders),
                'total_documents_created': total_documents_created,
                'chapter_results': chapter_results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processed_chapters': 0,
                'total_documents_created': 0
            }