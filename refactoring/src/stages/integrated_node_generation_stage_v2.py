# 생성 시간: Thu Sep  4 18:17:00 KST 2025
# 핵심 내용: 통합 노드 정보 문서 생성 단계 프로세서 (logger_v2.py 통합 적용)
# 상세 내용:
#   - IntegratedNodeGenerationStage (라인 29-203): 메인 통합 노드 생성 클래스
#   - process (라인 37-144): 메인 처리 로직 (3단계 순차 진행)
#   - generate_node_documents (라인 146-191): 1단계 - 노드 정보 문서 생성
#   - extract_content_nodes (라인 193-197): 2단계 - has_content 할당 및 콘텐츠 노드 추출  
#   - integrate_documents (라인 199-203): 3단계 - 문서 통합
# 상태: active
# 참조: integrated_node_generation_stage.py (로거 통합 적용)

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 기본 클래스 임포트
sys.path.append(str(Path(__file__).parent.parent))
from core.base.base_processor import BaseProcessor

# 새 아키텍처 서비스 임포트  
from services.node_document_service import NodeDocumentService
# 통합 로거 임포트
from utils.logger_v2 import Logger
# 텍스트 유틸리티 임포트
from utils.text_utils import normalize_title
import re

class IntegratedNodeGenerationStage(BaseProcessor):
    """통합 노드 정보 문서 생성 단계 프로세서 (3단계: 노드정보문서생성 → 콘텐츠노드추출 → 문서통합)"""
    
    def __init__(self, config_manager, logger_factory=None):
        super().__init__(config_manager, logger_factory, "integrated_node_generation")
        
        # 새로운 통합 Logger 사용 (logger_factory 무시)
        self.logger = Logger(
            project_name="integrated_node_stage",
            base_dir="./results",
            logs_base_dir="./logs"
        )
        
        # 새 아키텍처 NodeDocumentService 초기화 (로거 전달)
        self.node_document_service = NodeDocumentService(config_manager, self.logger)
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        메인 통합 노드 생성 처리 - 책 폴더 기반 자율 처리
        
        Args:
            input_data: {
                'book_directory': str  # 책 폴더 경로만 전달
            }
            
        Returns:
            Dict: {success, data, error} 형식
        """
        try:
            self.logger.info("=== 통합 노드 정보 문서 생성 시작 ===")
            
            book_directory = input_data.get('book_directory', '')
            if not book_directory or not os.path.exists(book_directory):
                return {
                    'success': False,
                    'data': None,
                    'error': f'유효하지 않은 책 폴더 경로: {book_directory}'
                }
            
            # 1. 책 폴더 내 모든 하위 폴더 순회 (모든 폴더가 장 폴더)
            processed_results = []
            success_count = 0
            total_count = 0
            
            for item in os.listdir(book_directory):
                chapter_folder = os.path.join(book_directory, item)
                
                # 폴더만 처리
                if not os.path.isdir(chapter_folder):
                    continue
                
                total_count += 1
                self.logger.info(f"장 폴더 처리 시작: {item}")
                
                try:
                    # 3단계 순차 처리
                    node_docs_result = await self.generate_node_documents(chapter_folder)
                    
                    if not node_docs_result.get('success', False):
                        raise Exception(f"노드 정보 문서 생성 실패: {node_docs_result.get('error', '')}")
                    
                    sections_result = await self.extract_content_nodes(chapter_folder)
                    
                    if not sections_result.get('success', False):
                        raise Exception(f"섹션 추출 실패: {sections_result.get('error', '')}")
                    
                    integration_result = await self.integrate_documents(chapter_folder)
                    
                    if not integration_result.get('success', False):
                        raise Exception(f"문서 통합 실패: {integration_result.get('error', '')}")
                    
                    # 성공 처리
                    processed_results.append({
                        'folder_name': item,
                        'folder_path': chapter_folder,
                        'success': True,
                        'stages': {
                            'node_docs': node_docs_result,
                            'sections': sections_result, 
                            'integration': integration_result
                        }
                    })
                    
                    success_count += 1
                    self.logger.info(f"장 폴더 처리 완료: {item}")
                    
                except Exception as e:
                    error_msg = str(e)
                    processed_results.append({
                        'folder_name': item,
                        'folder_path': chapter_folder,
                        'success': False,
                        'error': error_msg
                    })
                    
                    self.logger.error(f"장 폴더 처리 실패: {item} - {error_msg}")
            
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0
            
            self.logger.info(f"통합 노드 정보 문서 생성 완료: {success_count}/{total_count} 장 성공")
            
            return {
                'success': True,
                'data': {
                    'book_directory': book_directory,
                    'processed_chapters': success_count,
                    'total_chapters': total_count, 
                    'success_rate': success_rate,
                    'results': processed_results
                },
                'error': None
            }
            
        except Exception as e:
            error_msg = f"통합 노드 정보 문서 생성 실패: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'data': None, 
                'error': error_msg
            }
    
    async def generate_node_documents(self, chapter_folder: str) -> Dict[str, Any]:
        """1단계: 노드 정보 문서 생성 (NodeDocumentService 사용)"""
        
        # 장 폴더에서 필요한 파일들 자동 탐지
        folder_name = os.path.basename(chapter_folder)
        toc_file = os.path.join(chapter_folder, f"{folder_name}_toc.json")
        
        try:
            self.logger.info(f"노드 정보 문서 생성 시작: {folder_name}")
            
            # 필수 파일 존재 검증
            if not os.path.exists(toc_file):
                error_msg = f"TOC 파일이 존재하지 않습니다: {toc_file}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            if not os.path.exists(chapter_folder):
                error_msg = f"장 폴더가 존재하지 않습니다: {chapter_folder}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # NodeDocumentService를 사용한 노드 정보 문서 생성
            self.logger.info(f"NodeDocumentService.generate_documents_for_chapter() 호출...")
            node_docs_result = self.node_document_service.generate_documents_for_chapter(
                chapter_folder=chapter_folder,
                toc_file=toc_file
            )
            
            self.logger.info(f"NodeDocumentService 완료, 결과 확인 중...")
            
            if node_docs_result.success:
                created_count = node_docs_result.created_count
                self.logger.info(f"{folder_name} 노드 정보 문서 생성 완료: {created_count}개 파일")
                
                return {
                    'success': True,
                    'error': None
                }
            else:
                error_msg = f"노드 정보 문서 생성 실패: {node_docs_result.error or '알 수 없는 오류'}"
                self.logger.error(f"{folder_name} {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"노드 정보 문서 생성 중 예외: {str(e)}"
            self.logger.error(f"{folder_name} {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    async def extract_content_nodes(self, chapter_folder: str) -> Dict[str, Any]:
        """2단계: AI 기반 has_content 필드 할당 및 content.json 저장"""
        
        folder_name = os.path.basename(chapter_folder)
        toc_file = os.path.join(chapter_folder, f"{folder_name}_toc.json")
        content_file = os.path.join(chapter_folder, f"{folder_name}_content.md")
        
        try:
            self.logger.info(f"has_content 분석 시작: {folder_name}")
            
            # 필수 파일 존재 검증
            if not os.path.exists(toc_file):
                error_msg = f"TOC 파일이 존재하지 않습니다: {toc_file}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
                
            if not os.path.exists(content_file):
                error_msg = f"Content 파일이 존재하지 않습니다: {content_file}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # TOC 데이터 로드
            with open(toc_file, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            # Content 데이터 로드
            with open(content_file, 'r', encoding='utf-8') as f:
                chapter_content = f.read()
            
            # TOC를 섹션 리스트로 변환 (title 정보만)
            chapter_sections = []
            for node in toc_data:
                chapter_sections.append({
                    'title': node.get('title', '')
                })
            
            self.logger.info(f"분석 대상 섹션: {len(chapter_sections)}개")
            
            # ContentDocumentService를 사용한 실제 콘텐츠 분석
            from services.content_document_service_v3 import ContentDocumentService
            content_service = ContentDocumentService(self.config_manager, self.logger)
            
            self.logger.info(f"ContentDocumentService로 섹션 분석 시작...")
            content_result = await content_service.extract_sections(
                chapter_sections, 
                chapter_content,
                "information_integration"
            )
            
            if content_result.success:
                # 원본 TOC 데이터에 has_content 필드만 추가해서 content.json 생성
                content_nodes = []
                updated_sections_dict = {s.get('title'): s for s in content_result.updated_chapter_sections}
                
                for node in toc_data:
                    title = node.get('title', '')
                    updated_section = updated_sections_dict.get(title, {})
                    
                    # 원본 노드 정보 복사 후 has_content 추가
                    content_node = node.copy()
                    content_node['has_content'] = updated_section.get('has_content', False)
                    content_nodes.append(content_node)
                
                # content.json 파일 저장
                content_json_file = os.path.join(chapter_folder, "content.json")
                with open(content_json_file, 'w', encoding='utf-8') as f:
                    json.dump(content_nodes, f, ensure_ascii=False, indent=2)
                
                content_count = len([n for n in content_nodes if n.get('has_content', False)])
                
                self.logger.info(f"{folder_name} has_content 분석 완료: {len(content_nodes)}개 섹션 중 {content_count}개 내용 포함")
                self.logger.info(f"content.json 파일 저장 완료: {content_json_file}")
                
                return {
                    'success': True,
                    'error': None
                }
            else:
                error_msg = f"has_content 분석 실패: {'; '.join(content_result.errors)}"
                self.logger.error(f"{folder_name} {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            error_msg = f"has_content 분석 중 예외: {str(e)}"
            self.logger.error(f"{folder_name} {error_msg}")
            return {'success': False, 'error': error_msg}
    
    async def integrate_documents(self, chapter_result: Dict[str, Any], 
                                content_nodes_result: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """3단계: 문서 통합 (DocumentIntegrator 로직 이관)"""
        chapter_number = chapter_result.get('chapter_number')
        chapter_title = chapter_result.get('chapter_title', '')
        folder_path = chapter_result.get('folder_path', '')
        
        try:
            self.logger.info(f"장 {chapter_number} 문서 통합 시작: {chapter_title}")
            
            # 필수 폴더 존재 검증
            if not os.path.exists(folder_path):
                error_msg = f"장 폴더가 존재하지 않습니다: {folder_path}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # 필수 디렉토리 확인
            node_docs_dir = os.path.join(folder_path, "node_info_docs")
            if not os.path.exists(node_docs_dir):
                error_msg = f'노드 문서 디렉토리가 없음: {node_docs_dir}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # TOC 파일 자동 탐지 (*_toc.json 패턴)
            import glob
            toc_files = glob.glob(os.path.join(folder_path, "*_toc.json"))
            if not toc_files:
                error_msg = f'TOC 파일을 찾을 수 없음: {folder_path}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # 첫 번째 TOC 파일 사용
            toc_file = toc_files[0]
            self.logger.info(f"TOC 파일 탐지: {os.path.basename(toc_file)}")
            
            # TOC 파일 로드
            with open(toc_file, 'r', encoding='utf-8') as f:
                nodes = json.load(f)
            
            # 내용 문서 디렉토리는 장별 폴더 자체
            content_dir = folder_path
            
            # 각 노드별 통합 실행
            success_count = 0
            total_nodes = len(nodes)
            
            for node in nodes:
                if self._integrate_single_document(node, nodes, content_dir, node_docs_dir):
                    success_count += 1
            
            self.logger.info(f"장 {chapter_number} 문서 통합 완료: {success_count}/{total_nodes}개 문서")
            
            return {
                'success': True,
                'integrated_count': success_count,
                'total_nodes': total_nodes,
                'toc_file_used': toc_file,
                'chapter_folder': folder_path
            }
                
        except Exception as e:
            error_msg = f"문서 통합 중 예외: {str(e)}"
            self.logger.error(f"장 {chapter_number} {error_msg}")
            return {'success': False, 'error': error_msg}
    
    def _integrate_single_document(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                                  content_dir: str, node_docs_dir: str) -> bool:
        """단일 노드 문서 통합 (DocumentIntegrator 로직 이관)"""
        try:
            # 노드 문서 파일 경로 생성
            title_clean = normalize_title(node['title'])
            node_doc_filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
            node_doc_path = os.path.join(node_docs_dir, node_doc_filename)
            
            # title 기반으로 내용 문서 자동 탐지
            content_file_path = self._find_content_file_by_title(node['title'], content_dir)
            
            # 기존 노드 문서 존재 확인
            if not os.path.exists(node_doc_path):
                self.logger.warning(f"노드 문서 없음: {node_doc_filename}")
                return False
            
            # 내용 문서 로드 (콘텐츠가 없어도 통합 진행)
            content_text = ""
            if content_file_path:
                try:
                    with open(content_file_path, 'r', encoding='utf-8') as f:
                        content_text = f.read().strip()
                    self.logger.info(f"매칭된 내용 문서: {os.path.basename(content_file_path)}")
                except Exception as e:
                    self.logger.warning(f"내용 문서 로드 실패: {e}")
                    content_text = ""  # 로드 실패시 빈 문자열로 계속 진행
            else:
                self.logger.warning(f"매칭되는 내용 문서 없음: {node['title']}")
                # 내용 문서가 없어도 통합 진행 (빈 내용으로)
            
            # 모든 하위 노드 정보 수집 (재귀적)
            descendants_files = self._get_all_descendants_info(node, all_nodes)
            descendants_text = "\n".join(descendants_files) if descendants_files else ""
            
            # 레벨에 따른 헤더 생성
            header_prefix = "#" * node['level']  
            content_header = f"{header_prefix} {node['title']}"
            
            # 새로운 문서 내용 생성 (메타정보 제외)
            new_content = f"""# 속성
---
process_status: false

# 추출
---

# 내용
---
{content_header}

{content_text}

# 구성
---
{descendants_text}
"""
            
            # 파일 저장
            with open(node_doc_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"통합 완료: {node_doc_filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"통합 실패 (ID: {node.get('id', '?')}): {e}")
            return False
    
    def _find_content_file_by_title(self, node_title: str, content_dir: str) -> Optional[str]:
        """노드 title을 기반으로 내용 문서 파일을 자동으로 찾습니다."""
        import glob
        # 디렉토리 내 모든 .md 파일 탐색
        md_files = glob.glob(os.path.join(content_dir, "*.md"))
        
        # 정규화된 title 생성
        normalized_title = normalize_title(node_title)
        
        for file_path in md_files:
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            normalized_filename = normalize_title(filename_without_ext)
            
            # 정규화된 제목과 파일명 매칭
            if normalized_title == normalized_filename:
                return file_path
        
        return None
    
    def _get_all_descendants_info(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> List[str]:
        """노드의 모든 하위 노드들의 정보 문서 파일명을 재귀적으로 수집합니다."""
        # 모든 하위 노드 ID를 재귀적으로 수집
        descendant_ids = self._collect_descendant_ids(node, all_nodes, set())
        
        # ID로 정렬
        descendant_ids = sorted(descendant_ids)
        
        # 각 노드 ID에 대응하는 파일명 생성
        descendant_files = []
        for node_id in descendant_ids:
            descendant_node = next((n for n in all_nodes if n.get('id') == node_id), None)
            if descendant_node:
                # 파일명 생성
                title_clean = normalize_title(descendant_node['title'])
                filename = f"{descendant_node['id']:02d}_lev{descendant_node['level']}_{title_clean}_info.md"
                descendant_files.append(filename)
        
        return descendant_files
    
    def _collect_descendant_ids(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], visited: set) -> set:
        """노드의 모든 하위 노드 ID를 재귀적으로 수집합니다."""
        descendant_ids = set()
        
        # 현재 노드가 이미 방문된 경우 무한 루프 방지
        if node.get('id') in visited:
            return descendant_ids
        
        visited.add(node.get('id'))
        
        # 직접 자식 노드들 처리
        for child_id in node.get('children_ids', []):
            child_node = next((n for n in all_nodes if n.get('id') == child_id), None)
            if child_node:
                # 자식 노드 ID 추가
                descendant_ids.add(child_id)
                # 자식 노드의 하위 노드들을 재귀적으로 수집
                grandchildren_ids = self._collect_descendant_ids(child_node, all_nodes, visited.copy())
                descendant_ids.update(grandchildren_ids)
        
        return descendant_ids
    
    def _save_content_extraction_results(self, chapter_number: int, content_result) -> None:
        """로거를 사용해 콘텐츠 추출 결과를 테스트 데이터로 저장"""
        try:
            from datetime import datetime
            
            # hhmm 형식 폴더명 생성
            current_time = datetime.now()
            folder_name = f"content_extraction_{current_time.strftime('%H%M')}"
            
            # 저장 경로 생성
            custom_dir = f"/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/{folder_name}"
            
            self.logger.info(f"콘텐츠 추출 결과 저장 시작: {custom_dir}")
            
            # 디버그: 실제 데이터 구조 확인
            self.logger.info(f"DEBUG - section_documents 개수: {len(content_result.section_documents)}")
            if content_result.section_documents:
                sample_doc = content_result.section_documents[0]
                self.logger.info(f"DEBUG - 샘플 문서 키: {list(sample_doc.keys()) if isinstance(sample_doc, dict) else type(sample_doc)}")
                self.logger.info(f"DEBUG - 샘플 문서 내용: {sample_doc}")
            
            # 1. content.json 저장 (has_content 필드가 추가된 콘텐츠 노드들)
            content_nodes = []
            for doc in content_result.section_documents:
                content_nodes.append({
                    'id': doc.get('section_id', ''),
                    'title': doc.get('section_title', ''),
                    'level': 0,  # section_documents에는 level 정보가 없음
                    'has_content': doc.get('has_content', False),
                    'page_count': 0  # section_documents에는 page_count 정보가 없음
                })
            
            # content.json 파일 저장 (콘텐츠 노드 배열만)
            self.logger.save_result("content", content_nodes, "json", custom_dir)
            
            # 2. 섹션별 MD 파일 저장 (has_content=True인 것만)
            saved_sections = 0
            for doc in content_result.section_documents:
                if doc.get('has_content', False) and doc.get('extracted_content'):
                    # 안전한 파일명 생성 (기존 normalize_title 함수 활용)
                    title = doc.get('section_title', '').strip()
                    safe_filename = normalize_title(title)
                    
                    # MD 형식으로 내용 구성
                    md_content = f"# {title}\n\n"
                    md_content += f"- ID: {doc.get('section_id', '')}\n"
                    md_content += f"- Level: 0\n"
                    md_content += f"- Page Count: 0\n\n"
                    md_content += "## Content\n\n"
                    md_content += doc.get('extracted_content', '')
                    
                    # 로거의 save_result로 MD 파일 저장
                    self.logger.save_result(safe_filename, md_content, "md", custom_dir)
                    saved_sections += 1
            
            self.logger.info(f"콘텐츠 추출 결과 저장 완료: {custom_dir}")
            self.logger.info(f"- content.json: 콘텐츠 노드 {len(content_nodes)}개")
            self.logger.info(f"- 섹션 MD 파일: {saved_sections}개")
            
        except Exception as e:
            self.logger.error(f"콘텐츠 추출 결과 저장 실패: {str(e)}")