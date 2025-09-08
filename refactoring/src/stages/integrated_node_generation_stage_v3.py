# 생성 시간: Sat Sep  6 16:33:30 KST 2025
# 핵심 내용: ContentDocumentService v3의 detect_section_content, extract_section_content 메서드를 사용하는 통합 노드 정보 문서 생성 단계 프로세서
# 상세 내용:
#   - IntegratedNodeGenerationStage (라인 31-203): 메인 통합 노드 생성 클래스
#   - process (라인 47-151): 메인 처리 로직 (3단계 순차 진행)
#   - generate_node_documents (라인 153-205): 1단계 - 노드 정보 문서 생성
#   - generate_content_documents (라인 207-292): 2단계 - AI 기반 콘텐츠 문서 생성 (detect + extract 통합)  
#   - integrate_documents (라인 294-357): 3단계 - unified_info_docs 폴더에 통합 문서 생성
# 상태: active
# 참조: integrated_node_generation_stage_v2.py (ContentDocumentService v3 적용)

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
                    
                    sections_result = await self.generate_content_documents(chapter_folder)
                    
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
    
    async def generate_content_documents(self, chapter_folder: str) -> Dict[str, Any]:
        """2단계: AI 기반 콘텐츠 문서 생성 (detect + extract 통합)"""
        
        folder_name = os.path.basename(chapter_folder)
        toc_file = os.path.join(chapter_folder, f"{folder_name}_toc.json")
        content_file = os.path.join(chapter_folder, f"{folder_name}_content.md")
        
        try:
            self.logger.info(f"콘텐츠 문서 생성 시작: {folder_name}")
            
            # 필수 파일 존재 검증
            if not os.path.exists(toc_file):
                error_msg = f"TOC 파일이 존재하지 않습니다: {toc_file}"
                self.logger.error(error_msg)
                return {'success': False, 'data': None, 'error': error_msg}
                
            if not os.path.exists(content_file):
                error_msg = f"Content 파일이 존재하지 않습니다: {content_file}"
                self.logger.error(error_msg)
                return {'success': False, 'data': None, 'error': error_msg}
            
            # 파일 로드
            with open(toc_file, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            with open(content_file, 'r', encoding='utf-8') as f:
                chapter_content = f.read()
            
            # TOC를 섹션 리스트로 변환 (필요한 필드만 추출)
            chapter_sections = []
            for node in toc_data:
                chapter_sections.append({
                    'id': node.get('id'),
                    'title': node.get('title', ''),
                    'level': node.get('level', 1)
                })
            
            self.logger.info(f"분석 대상 섹션: {len(chapter_sections)}개")
            
            # ContentDocumentService 초기화
            from services.content_document_service_v4 import ContentDocumentService
            content_service = ContentDocumentService(self.config_manager, self.logger)
            
            # 1단계: 섹션 내용 포함 여부 분석
            self.logger.info("1단계: 섹션 내용 분석 시작...")
            sections_with_content = await content_service.detect_section_content(
                chapter_sections, 
                chapter_content,
                "information_integration"
            )
            
            # content.json 저장
            content_service._save_content_json(sections_with_content, chapter_folder)
            
            # 내용이 있는 섹션들만 필터링
            content_sections = [s for s in sections_with_content if s.get('has_content', False)]
            content_count = len(content_sections)
            
            self.logger.info(f"1단계 완료 - 총 {len(sections_with_content)}개 중 {content_count}개 섹션에 내용 포함")
            
            # 2단계: 내용이 있는 섹션들의 실제 내용 추출
            if content_count > 0:
                self.logger.info("2단계: 섹션 내용 추출 시작...")
                extracted_sections = await content_service.extract_section_content(
                    content_sections,
                    chapter_content, 
                    "information_integration"
                )
                
                # sections 폴더에 개별 파일 저장
                content_service._save_section_files(extracted_sections, chapter_folder)
                
                self.logger.info(f"2단계 완료 - {len(extracted_sections)}개 섹션 파일 저장")
            else:
                self.logger.info("2단계 건너뜀 - 내용이 포함된 섹션이 없음")
                extracted_sections = []
            
            self.logger.info(f"{folder_name} 콘텐츠 문서 생성 완료")
            
            return {
                'success': True,
                'data': {
                    'total_sections': len(sections_with_content),
                    'content_sections': content_count,
                    'extracted_files': len(extracted_sections) if content_count > 0 else 0
                },
                'error': None
            }
            
        except Exception as e:
            error_msg = f"콘텐츠 문서 생성 중 예외: {str(e)}"
            self.logger.error(f"{folder_name} {error_msg}")
            return {
                'success': False,
                'data': None,
                'error': error_msg
            }
    
    async def integrate_documents(self, chapter_folder: str) -> Dict[str, Any]:
        """3단계: 문서 통합 (DocumentIntegrator 로직 이관)"""
        
        folder_name = os.path.basename(chapter_folder)
        folder_path = chapter_folder
        
        try:
            self.logger.info(f"문서 통합 시작: {folder_name}")
            
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
            
            self.logger.info(f"{folder_name} 문서 통합 완료: {success_count}/{total_nodes}개 문서")
            
            return {
                'success': True,
                'data': {
                    'total_nodes': total_nodes,
                    'integrated_count': success_count
                },
                'error': None
            }
                
        except Exception as e:
            error_msg = f"문서 통합 중 예외: {str(e)}"
            self.logger.error(f"{folder_name} {error_msg}")
            return {
                'success': False,
                'data': None,
                'error': error_msg
            }
    
    def _integrate_single_document(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                                  content_dir: str, node_docs_dir: str) -> bool:
        """단일 노드 문서 통합 - unified_info_docs 폴더에 통합 문서 생성"""
        try:
            # unified_info_docs 폴더 생성
            unified_dir = os.path.join(content_dir, "unified_info_docs")
            os.makedirs(unified_dir, exist_ok=True)
            
            # 파일 경로 구성
            title_clean = normalize_title(node['title'])
            node_doc_filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
            node_doc_path = os.path.join(node_docs_dir, node_doc_filename)
            unified_doc_path = os.path.join(unified_dir, node_doc_filename)
            
            # 기존 노드 문서 존재 확인
            if not os.path.exists(node_doc_path):
                self.logger.warning(f"노드 문서 없음: {node_doc_filename}")
                return False
            
            # sections 폴더에서 매칭되는 파일 찾기
            sections_dir = os.path.join(content_dir, "sections")
            section_content = ""
            
            if os.path.exists(sections_dir):
                section_file_path = os.path.join(sections_dir, f"{title_clean}.md")
                if os.path.exists(section_file_path):
                    try:
                        with open(section_file_path, 'r', encoding='utf-8') as f:
                            section_content = f.read().strip()
                        self.logger.info(f"매칭된 섹션 파일: {title_clean}.md")
                    except Exception as e:
                        self.logger.warning(f"섹션 파일 로드 실패: {e}")
                        section_content = ""
                else:
                    self.logger.info(f"매칭되는 섹션 파일 없음: {title_clean}.md")
            
            # 모든 하위 노드 정보 수집 (기존 로직)
            descendants_files = self._get_all_descendants_info(node, all_nodes)
            descendants_text = "\n".join(descendants_files) if descendants_files else ""
            
            # 레벨에 따른 헤더 생성
            header_prefix = "#" * node['level']  
            content_header = f"{header_prefix} {node['title']}"
            
            # 통합 문서 내용 생성 (헤더 바로 밑에 내용 삽입)
            unified_content = f"""# 속성
---
process_status: false

# 추출
---

# 내용
---
{content_header}
{section_content}

# 구성
---
{descendants_text}
"""
            
            # unified_info_docs에 통합 파일 저장
            with open(unified_doc_path, 'w', encoding='utf-8') as f:
                f.write(unified_content)
            
            self.logger.info(f"통합 문서 생성 완료: unified_info_docs/{node_doc_filename}")
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