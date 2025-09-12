# 생성 시간: Wed Sep 10 12:34:15 KST 2025
# 핵심 내용: 데이터 기반 통합 노드 정보 문서 생성 단계 프로세서 (메모리 내 처리, 파일 저장 제거)
# 상세 내용:
#   - IntegratedNodeGenerationStage (라인 31-200): 메인 통합 노드 생성 클래스 (완전 데이터 기반)
#   - process (라인 47-120): 메인 처리 로직 (workspace_result의 chapters_data 순회)
#   - generate_node_documents (라인 122-160): 노드 정보 문서 생성 (file_name + content 반환)
#   - generate_content_documents (라인 162-200): AI 기반 콘텐츠 문서 생성 (file_name + content 반환)  
#   - integrate_documents (라인 202-240): 통합 문서 생성 (file_name + content 반환)
# 상태: active
# 참조: integrated_node_generation_stage_v3.py (데이터 기반 처리로 완전 개편)

import sys
from pathlib import Path
from typing import Dict, Any, List

# 기본 클래스 임포트
sys.path.append(str(Path(__file__).parent.parent))
from core.base.base_processor import BaseProcessor

# 서비스 임포트  
from services.content_document_service_v4 import ContentDocumentService
from services.node_document_service_v2 import NodeDocumentService
# 통합 로거 임포트
from utils.logger_v2 import Logger
# 텍스트 유틸리티 임포트
from utils.text_utils import normalize_title

class IntegratedNodeGenerationStage(BaseProcessor):
    """데이터 기반 통합 노드 정보 문서 생성 단계 프로세서 (3단계: 노드정보문서생성 → 콘텐츠노드추출 → 문서통합)"""
    
    def __init__(self, config_manager, logger_factory=None):
        super().__init__(config_manager, logger_factory, "integrated_node_generation")
        
        # 새로운 통합 Logger 사용
        self.logger = Logger(
            project_name="integrated_node_stage_v4",
            base_dir="./results",
            logs_base_dir="./logs"
        )
        
        # 서비스 초기화
        self.content_document_service = ContentDocumentService(config_manager, self.logger)
        self.node_document_service = NodeDocumentService(config_manager, self.logger)
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        메인 통합 노드 생성 처리 - workspace_result의 chapters_data 기반 처리
        
        Args:
            input_data: {'data': workspace_result}
        
        Returns:
            Dict: {
                'success': bool,
                'data': {
                    'processed_chapters': List[Dict],  # 처리된 장들의 정보 (chapter_title + normalized_title)
                    'unified_documents': List[Dict]    # 생성된 통합 문서들
                },
                'error': str
            }
        """
        try:
            self.logger.info("🚀 **통합 노드 정보 문서 생성 단계 시작** (데이터 기반 처리)")
            
            # workspace_result에서 chapters_data 추출
            workspace_data = input_data.get('data', {})
            chapters_analysis = workspace_data.get('chapters_analysis', {})
            chapters_data = chapters_analysis.get('chapters_info', [])
            
            if not chapters_data:
                error_msg = "chapters_info 데이터가 없습니다"
                self.logger.error(f"❌ {error_msg}")
                return {
                    'success': False,
                    'data': {
                        'processed_chapters': [],
                        'unified_documents': []
                    },
                    'error': error_msg
                }
            
            self.logger.info(f"📊 처리할 챕터 수: {len(chapters_data)}")
            
            # 🔍 **3단계 순차 처리**
            all_node_documents = []
            all_content_documents = []
            all_unified_documents = []
            processed_chapters = []  # 처리된 챕터들 정보 수집
            
            # 각 챕터별로 3단계 처리
            for i, chapter_info in enumerate(chapters_data, 1):
                chapter_title = chapter_info.get('chapter_title', f'Chapter {i}')
                self.logger.info(f"📖 **{i}/{len(chapters_data)} 챕터 처리 시작**: {chapter_title}")
                
                # 처리된 챕터 정보 수집
                processed_chapters.append({
                    'chapter_title': chapter_title,
                    'normalized_title': normalize_title(chapter_title)
                })
                
                # 1단계: 노드 정보 문서 생성
                self.logger.info(f"📝 **1단계**: 노드 정보 문서 생성 - {chapter_title}")
                node_documents = await self.generate_node_documents(chapter_info)
                all_node_documents.extend(node_documents)
                self.logger.info(f"✅ 노드 문서 생성 완료: {len(node_documents)}개")
                
                # 2단계: 콘텐츠 문서 생성  
                self.logger.info(f"🔍 **2단계**: 콘텐츠 문서 생성 - {chapter_title}")
                content_documents = await self.generate_content_documents(chapter_info)
                all_content_documents.extend(content_documents)
                self.logger.info(f"✅ 콘텐츠 문서 생성 완료: {len(content_documents)}개")
                
                # 3단계: 문서 통합
                self.logger.info(f"🔗 **3단계**: 문서 통합 - {chapter_title}")
                unified_documents = await self.integrate_documents(chapter_info, node_documents, content_documents)
                all_unified_documents.extend(unified_documents)
                self.logger.info(f"✅ 문서 통합 완료: {len(unified_documents)}개")
            
            # 📊 **최종 결과**
            self.logger.info(f"🎉 **통합 노드 생성 완료**")
            self.logger.info(f"   - 노드 문서: {len(all_node_documents)}개")
            self.logger.info(f"   - 콘텐츠 문서: {len(all_content_documents)}개")
            self.logger.info(f"   - 통합 문서: {len(all_unified_documents)}개")
            
            return {
                'success': True,
                'data': {
                    'processed_chapters': processed_chapters,
                    'unified_documents': all_unified_documents
                },
                'error': None
            }
            
        except Exception as e:
            error_msg = f"통합 노드 생성 처리 중 예외: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'data': {
                    'processed_chapters': [],
                    'unified_documents': []
                },
                'error': error_msg
            }
    
    async def generate_node_documents(self, chapter_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        1단계: 노드 정보 문서 생성 (NodeDocumentService 사용)
        
        Args:
            chapter_info: {
                'chapter_title': str,
                'chapter_toc': List[Dict],
                'content_text': str
            }
        
        Returns:
            List[Dict]: [{'file_name': str, 'content': str}, ...]
        """
        try:
            # NodeDocumentService를 사용하여 문서 생성
            documents = self.node_document_service.generate_documents_for_chapter(chapter_info)
            
            # 디렉토리 구조 변경: {정규화된장이름}/info_docs/
            normalized_chapter = normalize_title(chapter_info.get('chapter_title', 'Unknown'))
            
            for doc in documents:
                old_path = doc['file_name']  # "node_info_docs/filename"
                filename = old_path.replace('node_info_docs/', '')  # "filename"
                doc['file_name'] = f"{normalized_chapter}/info_docs/{filename}"
            
            return documents
            
        except Exception as e:
            self.logger.error(f"❌ 노드 문서 생성 중 오류: {str(e)}")
            return []
    
    async def generate_content_documents(self, chapter_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        2단계: AI 기반 콘텐츠 문서 생성 (메모리 내 처리)
        
        Args:
            chapter_info: {
                'chapter_title': str,
                'chapter_toc': List[Dict],
                'content_text': str
            }
        
        Returns:
            List[Dict]: [{'file_name': str, 'content': str}, ...]
        """
        try:
            chapter_title = chapter_info.get('chapter_title', 'Unknown Chapter')
            chapter_toc = chapter_info.get('chapter_toc', [])
            content_text = chapter_info.get('content_text', '')
            
            if not chapter_toc or not content_text:
                self.logger.warning(f"⚠️ {chapter_title}: 필요한 데이터가 없습니다")
                return []
            
            # 1단계: 섹션별 내용 포함 여부 분석
            sections_with_content = await self.content_document_service.detect_section_content(
                chapter_sections=chapter_toc,
                chapter_content=content_text,
                stage_name="integrated_node_generation"
            )
            
            # 2단계: 내용이 있는 섹션들의 실제 내용 추출
            content_sections = [section for section in sections_with_content if section.get('has_content', False)]
            
            if content_sections:
                # AI로 모든 섹션 내용 추출 (멀티턴 방식)
                extraction_results = await self.content_document_service.extract_section_content(
                    content_sections=content_sections,
                    chapter_content=content_text,
                    stage_name="integrated_node_generation"
                )
                
                generated_documents = []
                # 디렉토리 구조 변경: {정규화된장이름}/sections/
                normalized_chapter = normalize_title(chapter_info.get('chapter_title', 'Unknown'))
                
                for result in extraction_results:
                    section_title = result.get('section_title', 'Unknown')
                    content = result.get('extracted_content', '')  # ✅ 올바른 필드명 사용
                    
                    if content:
                        # 파일명 생성
                        normalized_title = normalize_title(section_title)
                        file_name = f"{normalized_chapter}/sections/{normalized_title}.md"
                        
                        generated_documents.append({
                            'file_name': file_name,
                            'content': content
                        })
                
                return generated_documents
            else:
                return []
            
        except Exception as e:
            self.logger.error(f"❌ 콘텐츠 문서 생성 중 오류: {str(e)}")
            return []
    
    async def integrate_documents(self, chapter_info: Dict[str, Any], 
                                node_documents: List[Dict[str, str]], 
                                content_documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        3단계: 노드 문서와 콘텐츠 문서 통합 (노드별 매칭하여 통합)
        
        각 노드 정보 문서의 내용 섹션에 대응되는 콘텐츠 문서를 삽입
        
        Args:
            chapter_info: 챕터 정보
            node_documents: 1단계 생성된 노드 문서들
            content_documents: 2단계 생성된 콘텐츠 문서들
        
        Returns:
            List[Dict]: [{'file_name': str, 'content': str}, ...]
        """
        try:
            chapter_title = chapter_info.get('chapter_title', 'Unknown Chapter')
            chapter_toc = chapter_info.get('chapter_toc', [])
            
            if not node_documents:
                self.logger.warning(f"⚠️ {chapter_title}: 노드 문서가 없습니다")
                return []
            
            # 콘텐츠 문서를 섹션 제목으로 매핑
            content_map = {}
            for content_doc in content_documents:
                # {정규화된장이름}/sections/{섹션title}.md에서 섹션 제목 추출
                file_path = content_doc['file_name']
                if '/sections/' in file_path and file_path.endswith('.md'):
                    # 파일명에서 섹션 제목 추출 (마지막 / 이후부터 .md 제거)
                    section_title = file_path.split('/')[-1][:-3]  # .md 제거
                    content_map[section_title] = content_doc['content']
            
            unified_documents = []
            
            # 각 노드 문서별로 통합 문서 생성
            for node_doc in node_documents:
                node_file_name = node_doc['file_name']
                node_content = node_doc['content']
                
                # 노드 정보 문서 파일명에서 노드 정보 추출
                # {정규화된장이름}/info_docs/{filename} → {filename}
                base_filename = node_file_name.split('/info_docs/')[-1]
                
                # 해당 노드의 TOC 정보 찾기
                corresponding_node = None
                for node in chapter_toc:
                    node_title_normalized = normalize_title(node.get('title', ''))
                    if node_title_normalized in base_filename:
                        corresponding_node = node
                        break
                
                # 통합 문서 내용 생성 - 항상 내용과 구성 섹션 처리
                integrated_content = node_content
                
                # 해당 노드 정보가 있으면 내용과 구성 섹션 모두 처리
                if corresponding_node:
                    node_title = corresponding_node.get('title', '')
                    node_level = corresponding_node.get('level', 1)
                    node_title_normalized = normalize_title(node_title)
                    
                    # 레벨에 따른 헤더 생성
                    header_prefix = "#" * node_level
                    content_header = f"{header_prefix} {node_title}"
                    
                    # 콘텐츠 가져오기 (있으면 사용, 없으면 헤더만)
                    if node_title_normalized in content_map:
                        content_to_insert = f"{content_header}\n{content_map[node_title_normalized]}"
                    else:
                        content_to_insert = content_header
                    
                    # "# 내용" 섹션과 "# 구성" 섹션 모두 처리
                    lines = integrated_content.split('\n')
                    new_lines = []
                    content_section_found = False
                    config_section_found = False
                    prev_line = ""
                    
                    for i, line in enumerate(lines):
                        new_lines.append(line)
                        
                        # 기본 템플릿의 구분선 바로 아래에 내용 삽입
                        if line.strip() == "---" and prev_line.strip() == "# 내용" and not content_section_found:
                            new_lines.append(content_to_insert)
                            content_section_found = True
                            
                        # 기본 템플릿의 구분선 바로 아래에 구성 정보 삽입
                        elif line.strip() == "---" and prev_line.strip() == "# 구성" and not config_section_found:
                            # 자식 노드들의 정보 문서 파일명 추가
                            descendants_files = self._get_all_descendants_info(corresponding_node, chapter_toc)
                            descendants_text = "\n".join(descendants_files) if descendants_files else ""
                            new_lines.append(descendants_text)
                            config_section_found = True
                        
                        prev_line = line
                    
                    integrated_content = '\n'.join(new_lines)
                
                # 통합 문서로 저장 ({정규화된장이름}/unified_info_docs/ 폴더에)
                normalized_chapter = normalize_title(chapter_info.get('chapter_title', 'Unknown'))
                unified_file_name = f"{normalized_chapter}/unified_info_docs/{base_filename}"
                
                unified_documents.append({
                    'file_name': unified_file_name,
                    'content': integrated_content
                })
            
            return unified_documents
            
        except Exception as e:
            self.logger.error(f"❌ 문서 통합 중 오류: {str(e)}")
            return []
    
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
    
