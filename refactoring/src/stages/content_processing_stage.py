# 생성 시간: Sun Sep  7 21:21:09 KST 2025
# 핵심 내용: ContentProcessingStage - 통합 문서 처리 및 개선된 목차 생성
# 상세 내용:
#   - ContentProcessingStage (라인 25-150): 메인 컨텐츠 처리 클래스
#   - parse_unified_document (라인 45-75): 통합 문서 파싱
#   - generate_extract_section (라인 77-140): engines_v5.py 패턴 활용한 5개 섹션 추출
#   - parse_extraction_response (라인 142-180): AI 응답 5개 섹션으로 파싱
#   - load_and_sort_documents (라인 182-250): 문서 로드 및 리프/비리프 분리 정렬
#   - format_extraction_content (라인 252-270): 추출 결과 마크다운 포맷팅
#   - update_extraction_section (라인 272-320): 파일 추출 섹션 업데이트
# 상태: active

import os
import re
import glob
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# 실제 구현된 모듈 활용
import sys
import os
# refactoring 프로젝트 경로 추가
refactoring_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, refactoring_root)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from src.utils.text_utils import normalize_title
from src.services.ai_service_v4 import AIService

# content_processing 전용 유틸리티 함수들 import
from .content_processing_utils import (
    parse_extraction_response,
    format_extraction_content,
    update_file_extraction_section,
    update_file_process_status
)


class ContentProcessingStage:
    """컨텐츠 가공 단계 - 통합 문서 처리 및 개선된 목차 생성"""
    
    def __init__(self, config: Dict, ai_service: AIService):
        self.config = config
        self.ai_service = ai_service  
        self.processing_mode = config.get('processing_mode', 'unified_type_processing')
        self.max_parallel = config.get('max_parallel', 4)
        self.api_calls_counter = 0
        
        # 로깅 설정
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    async def parse_unified_document(self, file_path: str) -> Optional[Dict[str, Any]]:
        """📄 통합 문서 파싱"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 제목 추출 (파일명 기반)
            file_name = Path(file_path).name
            title_match = re.search(r'(\d+_lev\d+_.*?)_info\.md', file_name)
            title = title_match.group(1).replace('_', ' ') if title_match else file_name
            
            # level 추출 
            level_match = re.search(r'lev(\d+)', file_name)
            level = int(level_match.group(1)) if level_match else 0
            
            # 구성 섹션 추출
            composition_match = re.search(r'# 구성\n(.*?)(?=\n# |$)', content, re.DOTALL)
            composition_section = composition_match.group(1).strip() if composition_match else '---'
            
            # 내용 섹션 추출
            content_match = re.search(r'# 내용\n(.*?)(?=\n# |$)', content, re.DOTALL)
            content_section = content_match.group(1).strip() if content_match else ''
            
            # 추출 섹션 추출 (TOC 생성 시 필요)
            extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# |$)', content, re.DOTALL)
            extraction_section = extraction_match.group(1).strip() if extraction_match else ''
            
            # 속성 섹션에서 process_status 추출
            process_status = False
            attributes_match = re.search(r'# 속성\n(.*?)(?=\n# |$)', content, re.DOTALL)
            if attributes_match:
                attributes_content = attributes_match.group(1)
                if 'process_status: true' in attributes_content:
                    process_status = True
            
            return {
                'title': title,
                'level': level,
                'composition_section': composition_section,
                'content_section': content_section,
                'extraction_section': extraction_section,  # 추가
                'process_status': process_status,  # 추가
                'file_path': file_path,
                'full_content': content
            }
        except Exception as e:
            self.logger.error(f"❌ 문서 파싱 실패: {file_path} - {e}")
            return None

    def _build_extraction_prompt(self, content: str, title: str) -> str:
        """추출용 프롬프트 생성"""
        return f"""다음 문서에서 5가지 정보를 순서대로 추출해주세요.

문서 제목: {title}
문서 내용:
{content}

다음 순서로 각 정보를 추출하고, 반드시 다음 형식을 정확히 지켜서 출력해주세요:

## 핵심 내용
문서의 핵심 내용을 2-3문장으로 간결하게 요약

## 상세 핵심 내용
주요 개념과 중요한 세부사항을 포함하여 5-7문장으로 정리

## 상세 정보
문서의 모든 중요한 정보를 빠뜨리지 않고 체계적으로 정리

## 주요 화제
문서에서 다루는 핵심 주제들을 불렛 포인트로 나열

## 부차 화제
주요 주제 외에 언급되는 부차적인 주제들을 불렛 포인트로 나열

**중요 규칙**: 
1. 각 섹션 제목(## 핵심 내용, ## 상세 핵심 내용 등)을 한 번만 출력하고 바로 다음 줄에 내용을 작성하세요.
2. 빈 헤더 라인을 출력하지 마세요.
3. 섹션 내용을 작성할 때 헤더가 필요한 경우에는 반드시 ### (해시 3개) 이상의 헤더만 사용하세요.
4. ## 헤더는 섹션 제목과 구분하기 위해 절대 중복 사용하지 마세요."""

    def _get_system_prompt(self) -> str:
        """시스템 프롬프트 반환"""
        return """문서 분석 전문가. 주어진 5가지 정보 타입을 순서대로 정확하게 추출하세요.
- 핵심 내용: 간결하고 정확한 요약
- 상세 핵심 내용: 상세하면서도 핵심적인 내용
- 상세 정보: 체계적이고 포괄적인 정리
- 주요 화제: 핵심 주제들
- 부차 화제: 부차적이지만 의미있는 주제들

정확한 형식을 지켜서 출력하세요."""

    def _validate_extraction_sections(self, sections: Dict[str, str], title: str) -> bool:
        """추출된 섹션들의 유효성 검증"""
        success_count = sum(1 for content in sections.values() 
                           if content.strip() and content.startswith('##'))
        
        if success_count >= 3:  # engines_v5.py와 동일한 기준
            self.api_calls_counter += 1
            self.logger.info(f"✅ 추출 성공: {title} ({success_count}/5 섹션)")
            return True
        else:
            self.logger.warning(f"⚠️ 추출 섹션 불완전: {title} ({success_count}/5)")
            return False

    async def get_combined_content(self, doc: Dict) -> str:
        """📖 노드의 통합 콘텐츠 생성 (리프: 자신만, 비리프: 자신+구성노드들)"""
        base_content = doc.get('content_section', '').strip()
        composition_files = doc.get('composition_files', [])
        
        # 리프 노드인 경우 자신의 콘텐츠만 반환
        if not composition_files:
            return base_content
        
        # 비리프 노드인 경우: 자신의 내용 + 구성 노드들의 내용 결합
        combined_content = base_content if base_content else ""
        
        self.logger.info(f"🔗 비리프 노드 구성 파일 결합: {len(composition_files)}개 파일")
        
        # doc에 이미 구성 노드들의 정보가 포함되어 있는지 확인
        # composition_section을 파싱해서 각 구성 파일의 내용을 가져올 수 있음
        composition_section = doc.get('composition_section', '')
        
        if composition_section and composition_section.strip() != '---':
            # composition_section에서 구성 파일들 파싱
            for comp_file in composition_files:
                # TODO: 여기서 실제 구성 파일 읽기 또는 full_content에서 추출
                # 현재는 파일명만 표시
                combined_content += f"\n\n### 구성 파일: {comp_file}"
                self.logger.debug(f"  📄 구성 파일 추가: {comp_file}")
        
        return combined_content

    async def generate_extract_section(self, doc: Dict) -> Dict[str, str]:
        """🤖 engines_v5.py 패턴 활용한 5개 섹션 추출"""
        title = doc.get('title', '')
        
        # 통합 콘텐츠 생성 (리프: 자신만, 비리프: 자신+구성노드들)
        content = await self.get_combined_content(doc)
        
        if not content.strip():
            self.logger.warning(f"⚠️ 통합 콘텐츠가 비어있음: {title}")
            return {}
        
        try:
            self.logger.info(f"🤖 AI 추출 시작: {title}")
            
            # 함수로 분리된 프롬프트 생성
            prompt = self._build_extraction_prompt(content, title)
            system_prompt = self._get_system_prompt()
            
            # AI 서비스 호출 (content_processing 설정 활용)
            response = await self.ai_service.query_single_request(
                prompt=prompt,
                additional_data={'system_prompt': system_prompt}
            )
            
            # engines_v5.py 파싱 로직 활용 (utils 함수 사용)
            sections = parse_extraction_response(response)
            
            # 함수로 분리된 검증 로직
            if self._validate_extraction_sections(sections, title):
                return sections
            else:
                return {}
                
        except Exception as e:
            self.logger.error(f"❌ 추출 실패: {title} - {e}")
            return {}


    async def load_and_sort_documents(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """📚 통합 문서 로드 및 장별 그룹화 - 리프/비리프 분리"""
        try:
            # 입력 데이터 검증
            processed_chapters, unified_documents = self._extract_input_data(input_data)
            if not processed_chapters or not unified_documents:
                return self._create_empty_result()
            
            self.logger.info(f"📄 로드된 문서: {len(unified_documents)}개, 장 수: {len(processed_chapters)}")
            
            # 장별 처리
            chapters_result = await self._process_chapters(processed_chapters, unified_documents)
            
            self.logger.info(f"📋 장별 그룹화 완료: {len(chapters_result)}개 장")
            
            return {
                "output": {"chapters": chapters_result},
                "error": None
            }
            
        except Exception as e:
            return self._create_error_result(e)
    
    def _extract_input_data(self, input_data: Dict[str, Any]) -> tuple:
        """입력 데이터에서 필요한 정보 추출"""
        processed_chapters = input_data.get('processed_chapters', [])
        unified_documents = input_data.get('unified_documents', [])
        return processed_chapters, unified_documents
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """빈 결과 생성"""
        self.logger.warning("⚠️ 처리할 데이터가 없습니다")
        return {
            "output": {"chapters": []},
            "error": None
        }
    
    def _create_error_result(self, error: Exception) -> Dict[str, Any]:
        """오류 결과 생성"""
        error_msg = f"load_and_sort_documents 실행 오류: {str(error)}"
        self.logger.error(f"❌ {error_msg}")
        return {
            "output": {"chapters": []},
            "error": error_msg
        }
    
    async def _process_chapters(self, processed_chapters: List[Dict], unified_documents: List[Dict]) -> List[Dict]:
        """장별 문서 처리"""
        chapters_result = []
        
        for chapter_index, chapter_info in enumerate(processed_chapters):
            chapter_result = await self._process_single_chapter(
                chapter_index, chapter_info, unified_documents
            )
            if chapter_result:
                chapters_result.append(chapter_result)
        
        return chapters_result
    
    async def _process_single_chapter(self, chapter_index: int, chapter_info: Dict, unified_documents: List[Dict]) -> Optional[Dict]:
        """단일 장 처리"""
        normalized_title = chapter_info.get('normalized_title', '')
        chapter_title = chapter_info.get('chapter_title', '')
        
        # 해당 장의 문서들 찾기
        chapter_documents = await self._find_chapter_documents(
            normalized_title, chapter_title, unified_documents
        )
        
        if not chapter_documents:
            return None
        
        # 리프/비리프 분리
        leaf_nodes, non_leaf_nodes = self._separate_leaf_and_non_leaf(chapter_documents)
        
        # 결과 구성
        return {
            "leaf_nodes": leaf_nodes,
            "non_leaf_nodes": non_leaf_nodes
        }
    
    async def _find_chapter_documents(self, normalized_title: str, chapter_title: str, unified_documents: List[Dict]) -> List[Dict]:
        """특정 장의 문서들 찾기 및 파싱"""
        chapter_documents = []
        
        for doc in unified_documents:
            file_name = doc.get('file_name', '')
            if normalized_title in file_name:
                parsed_doc = await self.parse_unified_document_from_content(doc.get('content', ''), file_name)
                if parsed_doc:
                    # 장 정보 추가
                    parsed_doc['chapter_info'] = {
                        'chapter_title': chapter_title,
                        'normalized_title': normalized_title
                    }
                    chapter_documents.append(parsed_doc)
        
        return chapter_documents
    
    def _separate_leaf_and_non_leaf(self, chapter_documents: List[Dict]) -> tuple:
        """리프 노드와 비리프 노드 분리 - level별 그룹화"""
        leaf_nodes = []
        non_leaf_groups = {}
        
        for doc in chapter_documents:
            composition_files = doc.get('composition_files', [])
            if not composition_files:  # 빈 배열 = 리프 노드
                leaf_nodes.append(doc)
            else:  # 배열에 요소 있음 = 비리프 노드
                level = doc.get('level', 0)
                level_key = f"level_{level}"
                
                if level_key not in non_leaf_groups:
                    non_leaf_groups[level_key] = []
                non_leaf_groups[level_key].append(doc)
        
        # level 내림차순으로 정렬된 딕셔너리 생성
        sorted_non_leaf_groups = {}
        for level in sorted(non_leaf_groups.keys(), key=lambda x: int(x.split('_')[1]), reverse=True):
            sorted_non_leaf_groups[level] = non_leaf_groups[level]
        
        return leaf_nodes, sorted_non_leaf_groups
        
        self.logger.info(f"📋 장별 그룹화 완료: {len(chapter_groups)}개 장")
        return chapter_groups
    
    async def parse_unified_document_from_content(self, content: str, file_name: str) -> Optional[Dict[str, Any]]:
        """📄 메모리상 통합 문서 content에서 파싱"""
        try:
            # 제목 추출 (파일명 기반)
            title_match = re.search(r'(\d+_lev\d+_.*?)_info\.md', file_name)
            title = title_match.group(1).replace('_', ' ') if title_match else file_name
            
            # level 추출 
            level_match = re.search(r'lev(\d+)', file_name)
            level = int(level_match.group(1)) if level_match else 0
            
            # 구성 섹션 추출
            composition_match = re.search(r'# 구성\n(.*?)(?=\n# |$)', content, re.DOTALL)
            composition_section = composition_match.group(1).strip() if composition_match else '---'
            
            # 내용 섹션 추출
            content_match = re.search(r'# 내용\n(.*?)(?=\n# |$)', content, re.DOTALL)
            content_section = content_match.group(1).strip() if content_match else ''
            
            # 추출 섹션 추출
            extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# |$)', content, re.DOTALL)
            extraction_section = extraction_match.group(1).strip() if extraction_match else ''
            
            # 속성 섹션에서 process_status 추출
            process_status = False
            attributes_match = re.search(r'# 속성\n(.*?)(?=\n# |$)', content, re.DOTALL)
            if attributes_match:
                attributes_content = attributes_match.group(1)
                if 'process_status: true' in attributes_content:
                    process_status = True
            
            # composition_files 생성 (composition_section이 "---"가 아니면 파일 리스트 생성)
            composition_files = []
            if composition_section != "---" and composition_section.strip():
                # 구성 섹션에서 파일명들 추출
                lines = composition_section.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and line.endswith('.md'):
                        composition_files.append(line)
            
            return {
                'title': title,
                'level': level,
                'composition_section': composition_section,
                'content_section': content_section,
                'extraction_section': extraction_section,
                'process_status': process_status,
                'file_name': file_name,
                'full_content': content,
                'composition_files': composition_files
            }
        except Exception as e:
            self.logger.error(f"❌ 문서 파싱 실패: {file_name} - {e}")
            return None
    
    def sort_documents_by_level(self, documents: List[Dict]) -> List[List[Dict]]:
        """📊 문서들을 리프/비리프 분리 후 level별 정렬"""
        # 리프/비리프 분리
        leaf_nodes = []
        non_leaf_nodes = []
        
        for doc in documents:
            composition_section = doc.get('composition_section', '').strip()
            if composition_section and composition_section != '---':
                # 구성 노드 파일명들이 있는 경우 (비리프)
                composition_lines = [line.strip() for line in composition_section.split('\n') 
                                   if line.strip() and not line.startswith('---')]
                doc['composition_files'] = composition_lines
                non_leaf_nodes.append(doc)
            else:
                # 구성 섹션이 비어있는 경우 (리프)
                doc['composition_files'] = []
                leaf_nodes.append(doc)
        
        # level별 그룹화 (비리프 노드들)
        level_groups = {}
        for doc in non_leaf_nodes:
            level = doc.get('level', 0)
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(doc)
        
        # 최종 정렬된 그룹들 (리프 노드가 먼저, 그다음 level 내림차순)
        sorted_groups = []
        if leaf_nodes:
            sorted_groups.append(leaf_nodes)  # 리프 노드 그룹이 먼저
        
        for level in sorted(level_groups.keys(), reverse=True):  # level 내림차순
            sorted_groups.append(level_groups[level])
        
        return sorted_groups



    async def add_update_status_mark(self, file_path: str, mark: str):
        """🏷️ 파일에 상태 마킹 추가 - # 추출 --- 바로 다음 줄에 위치"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # # 추출 --- 바로 다음에 마킹 추가 (핵심내용 바로 위)
            extraction_pattern = r'(# 추출\n---\n)(.*?)(\n# 내용|$)'
            
            if re.search(extraction_pattern, content, re.DOTALL):
                new_content = re.sub(
                    extraction_pattern,
                    f'\\1{mark}\n\n\\2\\3',
                    content,
                    flags=re.DOTALL
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                self.logger.info(f"🏷️ 상태 마킹 추가: {Path(file_path).name} - {mark}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ 상태 마킹 실패: {file_path} - {e}")


    async def process(self, book_folder_path: str) -> Dict[str, Any]:
        """🚀 메인 처리 로직"""
        try:
            self.logger.info(f"🚀 ContentProcessingStage 시작: {book_folder_path}")
            
            # 1. 문서 로드 및 정렬
            sorted_groups = await self.load_and_sort_documents(book_folder_path)
            
            if not sorted_groups:
                return {'success': False, 'error': '처리할 문서가 없습니다'}
            
            # 2. 그룹별 가공 처리 (현재는 기본 추출만)
            total_processed = 0
            for i, group in enumerate(sorted_groups):
                self.logger.info(f"🔄 그룹 {i+1}/{len(sorted_groups)} 처리 시작: {len(group)}개 문서")
                
                for doc in group:
                    # process_status가 false인 문서에 대해서만 처리
                    if not doc.get('process_status', False):
                        # 기본 추출 작업
                        extraction_result = await self.generate_extract_section(doc)
                        if extraction_result:
                            formatted_content = format_extraction_content(extraction_result)
                            success = update_file_extraction_section(doc['file_path'], formatted_content)
                            if success:
                                # process_status를 true로 변경
                                update_file_process_status(doc['file_path'], True)
                            total_processed += 1
                        else:
                            self.logger.warning(f"⚠️ 추출 실패로 process_status 유지: {doc.get('title', 'Unknown')}")
                    else:
                        self.logger.info(f"⏭️ 이미 처리됨 (process_status: true): {doc.get('title', 'Unknown')}")
                
                self.logger.info(f"✅ 그룹 {i+1} 처리 완료")
            
            self.logger.info(f"🎉 ContentProcessingStage 완료: {total_processed}개 문서 처리, API 호출: {self.api_calls_counter}회")
            
            return {
                'success': True, 
                'error': None,
                'processed_count': total_processed,
                'api_calls': self.api_calls_counter
            }
            
        except Exception as e:
            self.logger.error(f"❌ ContentProcessingStage 실패: {e}")
            return {'success': False, 'error': str(e)}

    async def generate_enhanced_toc_file(self, book_folder_path: str) -> bool:
        """📖 개선된 목차 MD 파일 생성"""
        try:
            # 1. TOC 구조 파일 로드
            chapter_name = os.path.basename(book_folder_path)
            toc_file_path = os.path.join(book_folder_path, f"{chapter_name}_toc.json")
            
            if not os.path.exists(toc_file_path):
                self.logger.warning(f"⚠️ TOC 파일 없음: {toc_file_path}")
                return False
            
            with open(toc_file_path, 'r', encoding='utf-8') as f:
                toc_structure = json.load(f)
            
            self.logger.info(f"📋 TOC 구조 로드: {len(toc_structure)}개 항목")
            
            # 2. 모든 통합 문서 로드 및 매칭
            unified_docs_dir = os.path.join(book_folder_path, "unified_info_docs")
            all_docs = {}
            
            for file_path in glob.glob(f"{unified_docs_dir}/*_info.md"):
                doc_data = await self.parse_unified_document(file_path)
                if doc_data and doc_data.get('title'):
                    # 제목을 키로 사용하여 매칭
                    all_docs[doc_data['title']] = doc_data
            
            self.logger.info(f"📄 로드된 문서: {len(all_docs)}개")
            
            # 3. TOC 구조에 따라 MD 파일 생성
            enhanced_lines = []
            matched_count = 0
            
            for toc_item in toc_structure:
                title = toc_item.get('title', '')
                level = toc_item.get('level', 1)
                
                # 헤더 생성
                header_prefix = "#" * level
                header = f"{header_prefix} {title}"
                
                # 매칭되는 문서 찾기
                matched_doc = self.find_matching_document(all_docs, toc_item)
                
                if matched_doc:
                    extraction_content = self.get_extracted_information(matched_doc)
                    if extraction_content.strip():
                        enhanced_lines.append(f"{header}\n{extraction_content}")
                        matched_count += 1
                    else:
                        enhanced_lines.append(f"{header}\n[추출 내용 없음]")
                else:
                    enhanced_lines.append(f"{header}\n[매칭 문서 없음]")
                
                # 섹션 간 구분을 위한 빈 줄 추가
                enhanced_lines.append("")
                enhanced_lines.append("")
            
            # 4. 파일 저장
            output_file = os.path.join(book_folder_path, f"{chapter_name}_enhanced_ToC.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(enhanced_lines))
            
            self.logger.info(f"✅ 개선된 TOC 파일 생성: {output_file}")
            self.logger.info(f"📊 매칭된 문서: {matched_count}/{len(toc_structure)}개")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ TOC 파일 생성 실패: {e}")
            return False

    def find_matching_document(self, all_docs: Dict[str, Dict], toc_item: Dict) -> Optional[Dict]:
        """📍 TOC 항목과 매칭되는 문서 찾기 - text_utils.normalize_title 활용"""
        toc_title = toc_item.get('title', '').strip()
        
        # 1. 정확한 제목 매칭
        if toc_title in all_docs:
            return all_docs[toc_title]
        
        # 2. normalize_title 함수를 사용한 정규화 매칭
        normalized_toc_title = normalize_title(toc_title)
        
        for doc_title, doc_data in all_docs.items():
            normalized_doc_title = normalize_title(doc_title)
            
            # 정규화된 제목에 TOC 정규화 제목이 포함되어 있는지 확인
            if normalized_toc_title and normalized_toc_title in normalized_doc_title:
                self.logger.info(f"🎯 정규화 매칭 성공: '{toc_title}' → '{doc_title}'")
                self.logger.info(f"    정규화된 TOC: '{normalized_toc_title}'")
                self.logger.info(f"    정규화된 문서: '{normalized_doc_title}'")
                return doc_data
            
            # 역방향 매칭도 시도
            elif normalized_doc_title and normalized_doc_title in normalized_toc_title:
                self.logger.info(f"🎯 역정규화 매칭 성공: '{toc_title}' → '{doc_title}'")
                self.logger.info(f"    정규화된 TOC: '{normalized_toc_title}'")
                self.logger.info(f"    정규화된 문서: '{normalized_doc_title}'")
                return doc_data
        
        # 3. 부분 키워드 매칭 (정규화된 제목을 단어별로 분리하여 매칭)
        if normalized_toc_title:
            toc_words = set(normalized_toc_title.split('_'))  # 언더스코어로 분리
            toc_words.discard('')  # 빈 문자열 제거
            
            best_match = None
            best_score = 0
            
            for doc_title, doc_data in all_docs.items():
                normalized_doc_title = normalize_title(doc_title)
                if normalized_doc_title:
                    doc_words = set(normalized_doc_title.split('_'))
                    doc_words.discard('')
                    
                    if len(toc_words) > 0 and len(doc_words) > 0:
                        common_words = toc_words.intersection(doc_words)
                        score = len(common_words) / len(toc_words)
                        
                        if score > best_score and score >= 0.5:  # 50% 이상 일치
                            best_score = score
                            best_match = doc_data
            
            if best_match:
                self.logger.info(f"🎯 키워드 매칭 성공: '{toc_title}' → '{best_match.get('title')}' (일치율: {best_score:.1%})")
                return best_match
        
        # 4. 매칭 실패
        self.logger.warning(f"❌ 매칭 실패: '{toc_title}' (정규화: '{normalized_toc_title}')")
        return None

    def get_extracted_information(self, doc_data: Dict) -> str:
        """📝 문서에서 핵심 내용 추출"""
        extraction_section = doc_data.get('extraction_section', '').strip()
        
        if not extraction_section or extraction_section == '---':
            return "[추출 내용 없음]"
        
        # 모든 추출 섹션 포함 (핵심 내용, 상세 핵심 내용, 상세 정보, 주요 화제, 부차 화제)
        sections = self.parse_extraction_sections(extraction_section)
        
        selected_information_type = []
        for section_name in ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']:
            if section_name in sections and sections[section_name].strip():
                content = sections[section_name].strip()
                # 헤더 추가하여 섹션 구분
                if section_name == 'core_content':
                    selected_information_type.append(f"## 핵심 내용\n{content}")
                elif section_name == 'detailed_core_content':
                    selected_information_type.append(f"## 상세 핵심 내용\n{content}")
                elif section_name == 'detailed_content':
                    selected_information_type.append(f"## 상세 정보\n{content}")
                elif section_name == 'main_topics':
                    selected_information_type.append(f"## 주요 화제\n{content}")
                elif section_name == 'sub_topics':
                    selected_information_type.append(f"## 부차 화제\n{content}")
        
        if selected_information_type:
            return '\n\n'.join(selected_information_type)
        else:
            return extraction_section[:500] + "..." if len(extraction_section) > 500 else extraction_section

    def parse_extraction_sections(self, extraction_content: str) -> Dict[str, str]:
        """📋 추출 섹션을 파싱하여 딕셔너리로 변환"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in extraction_content.split('\n'):
            line = line.strip()
            
            # 섹션 헤더 감지 (## 로 시작하는 라인)
            if line.startswith('## '):
                # 이전 섹션 저장 (헤더 제외하고 내용만)
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # 새 섹션 시작
                section_title = line[3:].strip()  # ## 제거
                # 더 구체적인 패턴을 먼저 확인
                if '상세 핵심' in section_title:
                    current_section = 'detailed_core_content'
                elif '핵심 내용' in section_title:
                    current_section = 'core_content'
                elif '상세 정보' in section_title:
                    current_section = 'detailed_content'
                elif '주요 화제' in section_title:
                    current_section = 'main_topics'
                elif '부차 화제' in section_title:
                    current_section = 'sub_topics'
                else:
                    current_section = None
                
                current_content = []  # 헤더는 저장하지 않고 내용만 저장
            elif current_section:
                current_content.append(line)
        
        # 마지막 섹션 저장
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections

    async def save_extraction_result(self, doc: Dict, extraction_result: Dict[str, str], user_output_path: str):
        """📁 모든 노드의 추출 결과를 사용자 지정 경로에 저장 (공통 로직)"""
        if not extraction_result:
            self.logger.warning(f"⚠️ 저장할 추출 결과가 비어있음: {doc.get('title', 'Unknown')}")
            return
        
        try:
            # 1. 파일 경로 구성 및 디렉터리 생성
            doc_title = doc.get('title', 'Unknown')
            original_file_name = doc.get('file_name', f"{doc_title.replace(' ', '_')}_info.md")
            
            # file_name 구조: {책이름}/{장}/{통합문서파일명}
            # 저장 구조: user_output_path/{책이름}/{장}/{통합문서파일명}
            if '/' in original_file_name:
                # 전체 경로 구조 유지 (책이름/장/파일명)
                relative_path = Path(original_file_name)
                output_dir = Path(user_output_path) / relative_path.parent
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file_path = output_dir / relative_path.name
            else:
                # 경로가 없으면 사용자 지정 경로에 직접 저장
                output_dir = Path(user_output_path)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file_path = output_dir / original_file_name
            
            self.logger.info(f"📁 추출 결과 저장 시작: {output_file_path}")
            
            # 2. 추출 섹션 포맷팅
            formatted_content = format_extraction_content(extraction_result)
            
            # 3. 기존 문서 내용 가져오기 (doc의 full_content 사용)
            original_content = doc.get('full_content', '')
            
            if original_content:
                # 기존 추출 섹션이 있으면 교체, 없으면 추가
                extraction_pattern = r'(# 추출\n---\n)(.*?)(?=\n# |$)'
                
                if re.search(extraction_pattern, original_content, re.DOTALL):
                    # 기존 추출 섹션 교체
                    new_content = re.sub(
                        extraction_pattern,
                        f'\\1{formatted_content}\n',
                        original_content,
                        flags=re.DOTALL
                    )
                else:
                    # 추출 섹션이 없으면 # 내용 앞에 추가
                    content_pattern = r'(\n# 내용)'
                    if re.search(content_pattern, original_content):
                        new_content = re.sub(
                            content_pattern,
                            f'\n# 추출\n---\n{formatted_content}\n\\1',
                            original_content
                        )
                    else:
                        # # 내용 섹션도 없으면 파일 끝에 추가
                        new_content = original_content + f'\n\n# 추출\n---\n{formatted_content}\n'
            else:
                # 원본 내용이 없으면 추출 결과만 저장
                new_content = f'# 추출\n---\n{formatted_content}\n'
            
            # 4. 파일 저장
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"✅ 추출 결과 저장 완료: {output_file_path.name}")
            return str(output_file_path)
            
        except Exception as e:
            self.logger.error(f"❌ 추출 결과 저장 실패: {doc.get('title', 'Unknown')} - {e}")
            raise