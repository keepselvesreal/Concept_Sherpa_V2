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

# utils 파일 삭제로 인해 필요한 함수들을 클래스 내부에 구현 (TEMP_IMPL에서 가져옴)

def combine_extraction_sections(extraction_result: Dict[str, str]) -> str:
    """추출 결과를 마크다운 형식으로 포맷팅"""
    if not extraction_result:
        return ""
    
    formatted_parts = []
    
    # 섹션 순서대로 포맷팅
    section_keys = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
    
    for key in section_keys:
        if key in extraction_result and extraction_result[key].strip():
            formatted_parts.append(extraction_result[key])
            formatted_parts.append("")  # 섹션 간 빈 줄
    
    return "\n".join(formatted_parts)

def update_extraction_section(file_path: str, formatted_content: str) -> bool:
    """파일의 추출 섹션 업데이트"""
    if not formatted_content:
        print(f"⚠️ 업데이트할 내용이 비어있음: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 추출 섹션 패턴 찾기
        extraction_pattern = r'(# 추출\n---\n)(.*?)(?=\n# 내용|$)'
        
        if re.search(extraction_pattern, content, re.DOTALL):
            # 기존 추출 섹션 업데이트
            new_content = re.sub(
                extraction_pattern,
                f'\\1{formatted_content}\n',
                content,
                flags=re.DOTALL
            )
        else:
            # 추출 섹션이 없으면 # 내용 앞에 추가
            content_pattern = r'(\n# 내용)'
            if re.search(content_pattern, content):
                new_content = re.sub(
                    content_pattern,
                    f'\n# 추출\n---\n{formatted_content}\n\\1',
                    content
                )
            else:
                # # 내용 섹션도 없으면 끝에 추가
                new_content = content + f'\n\n# 추출\n---\n{formatted_content}\n'
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 추출 섹션 업데이트 완료: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 추출 섹션 업데이트 실패: {file_path} - {e}")
        return False

def parse_extraction_response(response: str) -> Dict[str, str]:
    """추출 섹션 파싱 유틸리티"""
    sections = {}
    
    # 각 섹션별로 내용 추출
    patterns = {
        'core_content': r'## 핵심 내용\n(.*?)(?=\n## |$)',
        'detailed_core_content': r'## 상세 핵심 내용\n(.*?)(?=\n## |$)',
        'detailed_content': r'## 상세 정보\n(.*?)(?=\n## |$)',
        'main_topics': r'## 주요 화제\n(.*?)(?=\n## |$)',
        'sub_topics': r'## 부차 화제\n(.*?)(?=\n## |$)'
    }
    
    for section_key, pattern in patterns.items():
        match = re.search(pattern, response, re.DOTALL)
        if match:
            section_title = section_key.replace('_', ' ').replace('content', '내용').replace('detailed core', '상세 핵심').replace('detailed', '상세 정보').replace('main topics', '주요 화제').replace('sub topics', '부차 화제')
            sections[section_key] = f"## {section_title.title()}\n{match.group(1).strip()}"
    
    return sections

def update_file_process_status(file_path: str, status: bool) -> bool:
    """파일의 process_status 업데이트"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        status_value = 'true' if status else 'false'
        
        # 속성 섹션이 있는지 확인
        attributes_pattern = r'(# 속성\n)(.*?)(?=\n# |$)'
        attributes_match = re.search(attributes_pattern, content, re.DOTALL)
        
        if attributes_match:
            # 기존 속성 섹션 업데이트
            attributes_content = attributes_match.group(2)
            
            # process_status가 이미 있는지 확인
            if 'process_status:' in attributes_content:
                # 기존 process_status 값 업데이트
                updated_attributes = re.sub(
                    r'process_status:\s*(true|false)',
                    f'process_status: {status_value}',
                    attributes_content
                )
            else:
                # process_status 추가
                updated_attributes = attributes_content.strip() + f'\nprocess_status: {status_value}'
            
            new_content = re.sub(
                attributes_pattern,
                f'\\1{updated_attributes}\n',
                content,
                flags=re.DOTALL
            )
        else:
            # 속성 섹션이 없으면 추가 (# 내용 앞에)
            content_pattern = r'(\n# 내용)'
            if re.search(content_pattern, content):
                new_content = re.sub(
                    content_pattern,
                    f'\n# 속성\n---\nprocess_status: {status_value}\n\\1',
                    content
                )
            else:
                # # 내용 섹션도 없으면 파일 시작에 추가
                new_content = f'# 속성\n---\nprocess_status: {status_value}\n\n{content}'
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ process_status 업데이트 완료: {file_path} -> {status_value}")
        return True
        
    except Exception as e:
        print(f"❌ process_status 업데이트 실패: {file_path} - {e}")
        return False


class TaskTracker:
    """병렬 처리 태스크 추적 클래스 - 테스트용"""
    
    def __init__(self):
        self.active_count = 0
        self.max_concurrent = 0
        self.task_start_times = {}
        self.task_end_times = {}
        self.task_counter = 0
    
    def task_start(self, task_id: str = None):
        """태스크 시작 추적"""
        if task_id is None:
            self.task_counter += 1
            task_id = f"task_{self.task_counter}"
        
        self.active_count += 1
        self.max_concurrent = max(self.max_concurrent, self.active_count)
        self.task_start_times[task_id] = asyncio.get_event_loop().time()
        return task_id
    
    def task_end(self, task_id: str):
        """태스크 종료 추적"""
        self.active_count -= 1
        self.task_end_times[task_id] = asyncio.get_event_loop().time()
    
    def get_stats(self):
        """추적 통계 반환"""
        return {
            'max_concurrent': self.max_concurrent,
            'total_tasks': self.task_counter,
            'completed_tasks': len(self.task_end_times),
            'task_durations': {
                task_id: self.task_end_times[task_id] - start_time 
                for task_id, start_time in self.task_start_times.items() 
                if task_id in self.task_end_times
            }
        }


class ContentProcessingStage:
    """컨텐츠 가공 단계 - 통합 문서 처리 및 개선된 목차 생성"""
    
    def __init__(self, config: Dict, ai_service: AIService):
        self.config = config
        self.ai_service = ai_service  
        self.processing_mode = config.get('processing_mode', 'unified_type_processing')
        self.max_parallel = config.get('max_parallel', 4)
        self.api_calls_counter = 0
        
        # config_manager 초기화
        from src.utils.config_manager import ConfigManager
        self.config_manager = ConfigManager()
        
        # logger_v2 사용
        from src.utils.logger_v2 import Logger
        self.logger = Logger(self.__class__.__name__)
    
    def get_user_output_path(self) -> str:
        """Config Manager를 통해 사용자 출력 경로 가져오기"""
        return self.config_manager.get(
            'content_processing.output_paths.user_output_path', 
            '/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data'
        )

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
            "chapter_title": normalized_title,  # normalized_title 사용
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

    async def process_group_sequential(self, group: List[Dict], user_output_path: str) -> Dict[str, Any]:
        """
        그룹 내 순차 처리 - 단일 그룹의 문서들을 순차적으로 처리
        
        Args:
            group: 처리할 문서 그룹 (리스트)
            user_output_path: 사용자 지정 출력 경로
            
        Returns:
            {"output": "success", "error": None} 형식의 딕셔너리
        """
        try:
            self.logger.info(f"🔄 그룹 순차 처리 시작: {len(group)}개 문서")
            
            processed_count = 0
            for doc in group:
                try:
                    # process_single_document 호출
                    result = await self.process_single_document(doc, user_output_path)
                    
                    if result.get('error') is None:
                        processed_count += 1
                        self.logger.info(f"✅ 문서 처리 완료: {doc.get('title', 'Unknown')}")
                    else:
                        self.logger.warning(f"⚠️ 문서 처리 실패: {doc.get('title', 'Unknown')} - {result.get('error')}")
                        
                except Exception as e:
                    self.logger.error(f"❌ 문서 처리 중 오류: {doc.get('title', 'Unknown')} - {e}")
                    continue
            
            self.logger.info(f"✅ 그룹 순차 처리 완료: {processed_count}/{len(group)}개 성공")
            
            return {
                "output": f"success: {processed_count}/{len(group)} documents processed",
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"❌ 그룹 순차 처리 실패: {e}")
            return {
                "output": None,
                "error": str(e)
            }

    async def process_group_parallel(self, group: List[Dict], user_output_path: str) -> Dict[str, Any]:
        """
        그룹 내 병렬 처리 - 단일 그룹의 문서들을 병렬로 처리
        
        Args:
            group: 처리할 문서 그룹 (리스트)
            user_output_path: 사용자 지정 출력 경로
            
        Returns:
            {"output": "success: X/Y documents processed", "error": None} 형식의 딕셔너리
        """
        try:
            self.logger.info(f"🔄 그룹 병렬 처리 시작: {len(group)}개 문서")
            
            # 세마포어로 동시 처리 개수 제한 (max_parallel 기본값: 4)
            semaphore = asyncio.Semaphore(self.max_parallel)
            
            async def process_single_doc(doc):
                async with semaphore:
                    return await self.process_single_document(doc, user_output_path)
            
            # 모든 문서 병렬 처리
            tasks = [process_single_doc(doc) for doc in group]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 집계
            processed_count = 0
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"❌ 문서 처리 중 예외: {group[i].get('title', 'Unknown')} - {result}")
                    continue
                elif result and result.get('error') is None:
                    processed_count += 1
                    self.logger.info(f"✅ 문서 처리 완료: {group[i].get('title', 'Unknown')}")
                else:
                    self.logger.warning(f"⚠️ 문서 처리 실패: {group[i].get('title', 'Unknown')} - {result.get('error') if result else 'Unknown error'}")
            
            self.logger.info(f"✅ 그룹 병렬 처리 완료: {processed_count}/{len(group)}개 성공")
            
            return {
                "output": f"success: {processed_count}/{len(group)} documents processed",
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"❌ 그룹 병렬 처리 실패: {e}")
            return {
                "output": None,
                "error": str(e)
            }

    async def process_group_parallel_with_tracking(self, group: List[Dict], user_output_path: str) -> tuple[Dict[str, Any], TaskTracker]:
        """
        테스트용 - 태스크 추적 기능이 있는 병렬 처리
        
        Args:
            group: 처리할 문서 그룹 (리스트)
            user_output_path: 사용자 지정 출력 경로
            
        Returns:
            (result, tracker): 처리 결과와 태스크 추적 정보
        """
        tracker = TaskTracker()
        
        try:
            self.logger.info(f"🔄 그룹 병렬 처리 시작 (추적 모드): {len(group)}개 문서")
            
            # 세마포어로 동시 처리 개수 제한 (max_parallel 기본값: 4)
            semaphore = asyncio.Semaphore(self.max_parallel)
            
            async def process_single_doc_tracked(doc):
                task_id = tracker.task_start(f"doc_{doc.get('title', 'unknown')}")
                async with semaphore:
                    try:
                        # 현재 활성 태스크 수 로깅
                        self.logger.info(f"🔄 활성 태스크 수: {tracker.active_count} (최대: {tracker.max_concurrent})")
                        result = await self.process_single_document(doc, user_output_path)
                        return result
                    finally:
                        tracker.task_end(task_id)
            
            # 모든 문서 병렬 처리
            tasks = [process_single_doc_tracked(doc) for doc in group]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 집계
            processed_count = 0
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"❌ 문서 처리 중 예외: {group[i].get('title', 'Unknown')} - {result}")
                    continue
                elif result and result.get('error') is None:
                    processed_count += 1
                    self.logger.info(f"✅ 문서 처리 완료: {group[i].get('title', 'Unknown')}")
                else:
                    self.logger.warning(f"⚠️ 문서 처리 실패: {group[i].get('title', 'Unknown')} - {result.get('error') if result else 'Unknown error'}")
            
            # 추적 통계 로깅
            stats = tracker.get_stats()
            self.logger.info(f"📊 병렬 처리 통계: 최대 동시 실행 {stats['max_concurrent']}개, 완료 {stats['completed_tasks']}/{stats['total_tasks']}개")
            
            self.logger.info(f"✅ 그룹 병렬 처리 완료: {processed_count}/{len(group)}개 성공")
            
            result = {
                "output": f"success: {processed_count}/{len(group)} documents processed",
                "error": None
            }
            
            return result, tracker
            
        except Exception as e:
            self.logger.error(f"❌ 그룹 병렬 처리 실패: {e}")
            result = {
                "output": None,
                "error": str(e)
            }
            return result, tracker

    async def process_document_groups(self, sorted_data: Dict, user_output_path: str, parallel: bool = False) -> Dict[str, Any]:
        """
        챕터별 그룹 처리 - 각 챕터마다 [리프] -> [레벨3] -> [레벨2] -> [레벨1] 순서
        
        Args:
            sorted_data: load_and_sort_documents 결과 데이터
            user_output_path: 사용자 지정 출력 경로
            parallel: True면 그룹 내 병렬 처리, False면 순차 처리 (기본값)
            
        Returns:
            {"output": "success: X documents processed in Y groups across Z chapters", "error": None} 형식의 딕셔너리
        """
        try:
            chapters_data = sorted_data.get('output', {}).get('chapters', [])
            
            if not chapters_data:
                self.logger.warning("⚠️ 처리할 장이 없습니다")
                return {"output": "success: no chapters to process", "error": None}
            
            total_processed = 0
            total_groups = 0
            
            # 장별 순차 처리
            for chapter_idx, chapter in enumerate(chapters_data):
                self.logger.info(f"📚 제{chapter_idx + 1}장 처리 시작")
                
                # 1. 리프 노드 그룹 처리 (최우선)
                leaf_nodes = chapter.get('leaf_nodes', [])
                if leaf_nodes:
                    self.logger.info(f"  🍃 리프노드 그룹: {len(leaf_nodes)}개 문서 처리")
                    if parallel:
                        result = await self.process_group_parallel(leaf_nodes, user_output_path)
                    else:
                        result = await self.process_group_sequential(leaf_nodes, user_output_path)
                    total_groups += 1
                    if result.get('error') is None:
                        # 처리된 문서 수 추출 (예: "success: 3/3 documents processed")
                        output_str = result.get('output', '')
                        if 'success:' in output_str and 'documents processed' in output_str:
                            processed_part = output_str.split('success:')[1].split('documents processed')[0].strip()
                            if '/' in processed_part:
                                processed_count = int(processed_part.split('/')[0])
                                total_processed += processed_count
                    self.logger.info(f"  ✅ 리프노드 처리 완료")
                
                # 2. 비리프 노드 - 레벨 내림차순 처리
                non_leaf_nodes = chapter.get('non_leaf_nodes', {})
                
                # level_3 -> level_2 -> level_1 순서로 처리
                for level_key in sorted(non_leaf_nodes.keys(), 
                                      key=lambda x: int(x.split('_')[1]), 
                                      reverse=True):
                    nodes = non_leaf_nodes[level_key]
                    if nodes:
                        level_num = level_key.split('_')[1]
                        self.logger.info(f"  🔢 레벨 {level_num} 그룹: {len(nodes)}개 문서 처리")
                        if parallel:
                            result = await self.process_group_parallel(nodes, user_output_path)
                        else:
                            result = await self.process_group_sequential(nodes, user_output_path)
                        total_groups += 1
                        if result.get('error') is None:
                            # 처리된 문서 수 추출
                            output_str = result.get('output', '')
                            if 'success:' in output_str and 'documents processed' in output_str:
                                processed_part = output_str.split('success:')[1].split('documents processed')[0].strip()
                                if '/' in processed_part:
                                    processed_count = int(processed_part.split('/')[0])
                                    total_processed += processed_count
                        self.logger.info(f"  ✅ 레벨 {level_num} 처리 완료")
                
                self.logger.info(f"🎯 제{chapter_idx + 1}장 처리 완료")
            
            self.logger.info(f"🏆 전체 {len(chapters_data)}개 장, {total_groups}개 그룹 처리 완료! (총 {total_processed}개 문서)")
            
            return {
                "output": f"success: {total_processed} documents processed in {total_groups} groups across {len(chapters_data)} chapters",
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"❌ 챕터별 문서 처리 실패: {e}")
            return {
                "output": None,
                "error": str(e)
            }
    
    def _extract_chapter_files_from_prev_result(self, prev_stage_result: Dict[str, Any]) -> Dict[str, Any]:
        """prev_stage_result에서 장별로 파일명 그룹화해서 반환"""
        chapter_files = {}
        
        data = prev_stage_result.get('data', {})
        processed_chapters = data.get('processed_chapters', [])
        unified_documents = data.get('unified_documents', [])
        
        # 각 장별로 처리
        for chapter in processed_chapters:
            normalized_title = chapter.get('normalized_title', '')
            chapter_title = chapter.get('chapter_title', 'Unknown')
            
            # 해당 장의 문서들 찾기 (normalized_title로 매칭)
            file_names = []
            for doc in unified_documents:
                file_name = doc.get('file_name', '')
                if normalized_title in file_name:
                    file_names.append(file_name)
            
            # chapter_title을 키로 사용
            chapter_files[chapter_title] = file_names
        
        return chapter_files

    async def process(self, prev_stage_result: Dict[str, Any]) -> Dict[str, Any]:
        """🚀 메인 처리 로직 - prev_stage_result 기반"""
        try:
            self.logger.info("🚀 ContentProcessingStage 시작")
            
            # 1. 가독성을 위한 변수 추출
            unified_documents = prev_stage_result['data']
            
            # 2. 문서 로드 및 정렬 
            sorted_data = await self.load_and_sort_documents(unified_documents)
            
            if not sorted_data or not sorted_data.get('output', {}).get('chapters'):
                return {'data': {}, 'error': '처리할 문서가 없습니다'}
            
            # 3. config_manager 기반 경로 사용
            result = await self.process_document_groups(sorted_data, self.get_user_output_path())
            
            if result.get('error'):
                self.logger.error(f"❌ 그룹 처리 실패: {result.get('error')}")
                return {'data': {}, 'error': result.get('error')}
            
            # 4. prev_stage_result에서 직접 장별 파일명 그룹화
            chapter_files = self._extract_chapter_files_from_prev_result(prev_stage_result)
            
            # 5. book_title 정보 추가
            book_information = prev_stage_result.get('data', {}).get('book_information', {})
            book_title = book_information.get('title', 'Unknown Book')
            
            self.logger.info(f"🎉 ContentProcessingStage 완료")
            
            return {
                'data': {
                    'book_title': book_title,
                    'chapter_info_docs': chapter_files
                }, 
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"❌ ContentProcessingStage 실패: {e}")
            return {'data': {}, 'error': str(e)}

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
            formatted_content = combine_extraction_sections(extraction_result)
            
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

    async def update_current_extraction_section(self, doc: Dict, user_output_path: str) -> tuple:
        """
        현재 비리프 노드의 추출 섹션을 구성 파일들의 내용을 바탕으로 업데이트
        
        Args:
            doc: 비리프 노드 문서 정보
            user_output_path: 사용자 지정 출력 경로
            
        Returns:
            tuple: (updated_current_extraction: Dict, used_composition_extractions: str)
            
        처리 과정:
        1. 사용자 지정 경로에서 현재 노드 파일 읽기
        2. 구성 노드들의 추출 섹션 수집 (파일에서 읽기)
        3. AI 서비스로 부모 노드 업데이트 수행
        4. 업데이트된 내용을 파일에 저장
        5. 명시적으로 두 값 반환
        """
        try:
            self.logger.info(f"🔄 현재 추출 섹션 업데이트 시작: {doc.get('title', 'Unknown')}")
            
            # 1. 현재 노드 파일 경로 구성
            file_name = doc.get('file_name', '')
            # {user_output_path}/{전체경로}로 구성
            current_file_path = Path(user_output_path) / file_name
            
            if not current_file_path.exists():
                raise FileNotFoundError(f"현재 노드 파일이 존재하지 않습니다: {current_file_path}")
            
            # 2. 현재 노드의 기존 추출 섹션 읽기
            with open(current_file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            current_extraction = self._parse_extraction_section_from_content(current_content)
            self.logger.info(f"📄 현재 추출 섹션 로드: {len(current_extraction)} 섹션")
            
            # 3. 구성 노드들의 추출 섹션 수집
            composition_extractions = []
            composition_files = doc.get('composition_files', [])
            
            # file_name에서 디렉터리 경로 추출 ({책폴더}/{장폴더})
            file_name = doc.get('file_name', '')
            file_dir = Path(file_name).parent  # Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/unified_info_docs
            
            for comp_file in composition_files:
                # {user_output_path}/{책폴더}/{장폴더}/{구성파일명}
                comp_file_path = Path(user_output_path) / file_dir / comp_file
                if comp_file_path.exists():
                    with open(comp_file_path, 'r', encoding='utf-8') as f:
                        comp_content = f.read()
                    
                    comp_extraction = self._parse_extraction_section_from_content(comp_content)
                    if comp_extraction:
                        # 컴포지션 정보 구성
                        comp_title = self._extract_title_from_filename(comp_file)
                        composition_extractions.append({
                            'title': comp_title,
                            'extraction': comp_extraction
                        })
                        self.logger.info(f"✅ 구성 파일 추출 섹션 로드: {comp_file}")
                    else:
                        self.logger.warning(f"⚠️ 구성 파일 추출 섹션 없음: {comp_file}")
                else:
                    self.logger.warning(f"⚠️ 구성 파일 없음: {comp_file_path}")
            
            if not composition_extractions:
                raise ValueError("사용할 수 있는 구성 노드 추출 섹션이 없습니다")
            
            # 4. AI 서비스로 부모 노드 업데이트 수행 (engines_v5.py 로직 활용)
            updated_current_extraction = await self._update_parent_with_composition_logic(
                current_doc=doc,
                current_extraction=current_extraction,
                composition_extractions=composition_extractions
            )
            
            # 5. 구성 노드들의 추출 섹션을 문자열로 결합
            used_composition_extractions = self._combine_composition_extractions(composition_extractions)
            
            # 6. 업데이트된 내용을 파일에 저장 (상태 마킹 포함)
            await self._save_updated_extraction_to_file(current_file_path, updated_current_extraction, "<구성 노드 반영 완료>")
            
            self.logger.info(f"✅ 현재 추출 섹션 업데이트 완료: {doc.get('title', 'Unknown')}")
            
            return updated_current_extraction, used_composition_extractions
            
        except Exception as e:
            self.logger.error(f"❌ 현재 추출 섹션 업데이트 실패: {doc.get('title', 'Unknown')} - {e}")
            raise

    def _parse_extraction_section_from_content(self, content: str) -> Dict:
        """파일 내용에서 추출 섹션을 파싱하여 딕셔너리로 반환"""
        try:
            # # 추출 섹션 찾기
            extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# |$)', content, re.DOTALL)
            if not extraction_match:
                return {}
            
            extraction_content = extraction_match.group(1).strip()
            if not extraction_content:
                return {}
            
            # engines_v5.py의 parse_extraction_response 로직 활용
            return parse_extraction_response(extraction_content)
            
        except Exception as e:
            self.logger.warning(f"⚠️ 추출 섹션 파싱 실패: {e}")
            return {}

    def _extract_title_from_filename(self, filename: str) -> str:
        """파일명에서 제목 추출"""
        try:
            # 예: "17_lev3_1.1.1_The_design_phase_info.md" -> "17 lev3 1.1.1 The design phase"
            title_match = re.search(r'(\d+_lev\d+_.*?)_info\.md', filename)
            if title_match:
                return title_match.group(1).replace('_', ' ')
            return filename.replace('_info.md', '').replace('_', ' ')
        except Exception:
            return filename

    async def _update_parent_with_composition_logic(self, current_doc: Dict, current_extraction: Dict, composition_extractions: List[Dict]) -> Dict:
        """engines_v5.py의 update_parent_extraction_with_composition 로직 활용하여 부모 노드 업데이트"""
        try:
            # 현재 추출 섹션 내용 추출
            parent_core = current_extraction.get('core_content', '').replace('## 핵심 내용', '').strip()
            parent_detailed_core = current_extraction.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
            parent_detailed_info = current_extraction.get('detailed_content', '').replace('## 상세 정보', '').strip()
            parent_main_topics = current_extraction.get('main_topics', '').replace('## 주요 화제', '').strip()
            parent_sub_topics = current_extraction.get('sub_topics', '').replace('## 부차 화제', '').strip()
            
            # 구성 정보 포맷팅 (engines_v5.py와 동일)
            composition_info = []
            for comp in composition_extractions:
                comp_sections = comp['extraction']
                comp_core = comp_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
                comp_detailed_core = comp_sections.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
                comp_detailed_info = comp_sections.get('detailed_content', '').replace('## 상세 정보', '').strip()
                comp_main_topics = comp_sections.get('main_topics', '').replace('## 주요 화제', '').strip()
                comp_sub_topics = comp_sections.get('sub_topics', '').replace('## 부차 화제', '').strip()
                
                child_info = f"""
구성노드 ({comp['title']}):
- 핵심 내용: {comp_core}
- 상세 핵심 내용: {comp_detailed_core}
- 상세 정보: {comp_detailed_info}
- 주요 화제: {comp_main_topics}
- 부차 화제: {comp_sub_topics}"""
                
                composition_info.append(child_info)
            
            # engines_v5.py 프롬프트 패턴 사용
            prompt = f"""다음은 부모 노드의 추출 섹션을 구성 노드들의 내용을 반영하여 업데이트하는 작업입니다.

**부모 노드 ({current_doc.get('title', 'Unknown')})의 현재 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}
주요 화제: {parent_main_topics}
부차 화제: {parent_sub_topics}

**구성 노드들의 내용:**
{chr(10).join(composition_info)}

부모 노드의 각 섹션을 구성 노드들의 내용을 종합적으로 반영하여 개선해주세요. 
부모 노드는 전체적인 개요와 통합적인 관점을 제공하되, 구성 노드들의 세부 내용이 잘 반영되도록 해주세요.

다음 5개 섹션 형식으로 응답해주세요:

## 핵심 내용
[개선된 핵심 내용]

## 상세 핵심 내용  
[개선된 상세 핵심 내용]

## 상세 정보
[개선된 상세 정보]

## 주요 화제
[개선된 주요 화제]

## 부차 화제
[개선된 부차 화제]"""
            
            # AI 서비스 호출
            response = await self.ai_service.query_single_request(prompt)
            
            # 응답 파싱
            parsed_response = parse_extraction_response(response)
            
            if len(parsed_response) >= 3:  # 최소한 핵심 3개 섹션은 있어야 함
                self.logger.info(f"✅ 부모 노드 업데이트 성공: {len(parsed_response)} 섹션")
                return parsed_response
            else:
                self.logger.warning("⚠️ AI 응답 품질 부족, 기존 추출 섹션 유지")
                return current_extraction
                
        except Exception as e:
            self.logger.error(f"❌ 부모 노드 업데이트 실패: {e}")
            return current_extraction

    def _combine_composition_extractions(self, composition_extractions: List[Dict]) -> str:
        """구성 노드들의 추출 섹션을 하나의 문자열로 결합"""
        try:
            combined_parts = []
            for comp in composition_extractions:
                comp_title = comp['title']
                comp_sections = comp['extraction']
                
                # 각 구성 노드의 추출 섹션을 포맷팅
                section_text = f"=== {comp_title} ===\n"
                for section_content in comp_sections.values():
                    section_text += f"{section_content}\n"
                
                combined_parts.append(section_text)
            
            return "\n".join(combined_parts)
            
        except Exception as e:
            self.logger.warning(f"⚠️ 구성 추출 섹션 결합 실패: {e}")
            return ""

    async def _save_updated_extraction_to_file(self, file_path: Path, updated_extraction: Dict, status_marker: str):
        """업데이트된 추출 섹션을 파일에 저장 (상태 마킹 포함)"""
        try:
            # 새로운 추출 섹션 내용 포맷팅 - 상태 마킹 포함
            formatted_extraction = combine_extraction_sections(updated_extraction)
            # 상태 마킹을 추출 섹션 맨 앞에 추가
            formatted_extraction = f"{status_marker}\n\n{formatted_extraction}"
            
            # 기존 추출 섹션 교체 (update_extraction_section은 boolean 반환)
            success = update_extraction_section(str(file_path), formatted_extraction)
            
            if success:
                self.logger.info(f"💾 업데이트된 추출 섹션 저장 완료: {file_path.name}")
            else:
                raise Exception("추출 섹션 업데이트 함수가 실패를 반환했습니다")
            
        except Exception as e:
            self.logger.error(f"❌ 업데이트된 추출 섹션 저장 실패: {file_path} - {e}")
            raise

    async def update_composition_extraction_sections(self, 
                                                   parent_doc: Dict,
                                                   parent_extraction: Dict,
                                                   used_composition_extractions: str,
                                                   composition_files: List[str],
                                                   user_output_path: str) -> None:
        """
        구성 노드들의 추출 섹션을 부모 노드 업데이트 내용 반영하여 일괄 업데이트
        engines_v5.py 패턴: 한 번의 AI 호출로 모든 구성 노드 업데이트
        
        Args:
            parent_doc: 부모 노드 문서 (filename 정보 포함)
            parent_extraction: 업데이트된 부모 노드 추출 섹션 
            used_composition_extractions: 사용된 구성 노드들의 결합된 추출 섹션
            composition_files: 구성 파일명 리스트
            user_output_path: 사용자 지정 저장 경로
        """
        self.logger.info(f"🔄 구성 노드 일괄 업데이트 시작")
        
        if not composition_files:
            self.logger.info("구성 파일이 없어 업데이트를 건너뜁니다")
            return
            
        self.logger.info(f"📁 처리할 구성 파일 수: {len(composition_files)}개")
        
        try:
            # 1단계: 한 번의 AI 호출로 모든 구성 노드 업데이트
            response = await self._update_all_composition_sections(
                parent_extraction=parent_extraction,
                used_composition_extractions=used_composition_extractions,
                composition_files=composition_files
            )
            
            # 2단계: AI 응답 파싱
            node_sections = await self._parse_ai_response_to_node_sections(response)
            
            # 3단계: 각 구성 노드 개별 저장
            await self._save_each_composition_node(
                node_sections=node_sections,
                parent_doc=parent_doc,
                composition_files=composition_files,
                user_output_path=user_output_path
            )
            
            self.logger.info(f"🎉 구성 노드 일괄 업데이트 완료: {len(composition_files)}개")
            
        except Exception as e:
            self.logger.error(f"❌ 구성 노드 일괄 업데이트 실패: {e}")
            raise

    async def _update_all_composition_sections(self, 
                                             parent_extraction: Dict,
                                             used_composition_extractions: str,
                                             composition_files: List[str]) -> str:
        """
        engines_v5.py 패턴: 한 번의 AI 호출로 모든 구성 노드의 핵심 3개 섹션 업데이트
        """
        # 부모 노드의 핵심 3개 섹션만 추출 (engines_v5.py 동일)
        parent_core = parent_extraction.get('core_content', '').replace('## 핵심 내용', '').strip()
        parent_detailed_core = parent_extraction.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
        parent_detailed_info = parent_extraction.get('detailed_content', '').replace('## 상세 정보', '').strip()
        
        # 구성 파일 수 정보 추가로 AI 응답 품질 개선
        composition_count = len(composition_files)
        
        # engines_v5.py에서 수정 요청된 간소화된 프롬프트 - 구성 파일 수 명시
        prompt = f"""다음은 부모 노드의 업데이트된 내용을 바탕으로 **총 {composition_count}개** 구성 노드들의 핵심 3가지 정보 섹션만 개선하는 작업입니다.

**부모 노드의 업데이트된 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}

**구성 노드들의 현재 내용:**
{used_composition_extractions}

부모 노드의 업데이트된 내용을 반영하여 각 구성 노드의 **3가지 정보 섹션(핵심 내용, 상세 핵심 내용, 상세 정보)만** 개선해주세요.
각 구성 노드의 고유한 특성은 유지하되, 부모와의 일관성과 연결성을 반영해주세요.

**중요: 반드시 {composition_count}개 모든 구성노드에 대해 응답해주세요.**

반드시 다음 형식을 정확히 지켜서 출력해주세요:

구성노드1:
## 핵심 내용
[개선된 핵심 내용]

## 상세 핵심 내용
[개선된 상세 핵심 내용]

## 상세 정보
[개선된 상세 정보]

구성노드2:
## 핵심 내용
[개선된 핵심 내용]

## 상세 핵심 내용
[개선된 상세 핵심 내용]

## 상세 정보
[개선된 상세 정보]

**중요**: 각 섹션은 반드시 "## " (해시 2개 + 공백)으로 시작하는 제목을 포함해야 합니다."""

        # 단일 AI 호출
        response = await self.ai_service.query_single_request(prompt)
        self.logger.info(f"✅ AI 일괄 호출 완료")
        
        return response

    async def _parse_ai_response_to_node_sections(self, response: str) -> List[Dict[str, str]]:
        """
        AI 응답을 구성 노드별로 파싱 (SRP: 파싱만 담당)
        """
        try:
            # AI 응답을 구성 노드별로 파싱
            node_sections = self._parse_ai_response_for_composition(response)
            
            self.logger.info(f"🔍 최종 파싱 결과: {len(node_sections)}개 노드")
            return node_sections
            
        except Exception as e:
            self.logger.error(f"❌ AI 응답 파싱 실패: {e}")
            raise

    async def _save_each_composition_node(self, 
                                       node_sections: List[Dict[str, str]],
                                       parent_doc: Dict,
                                       composition_files: List[str],
                                       user_output_path: str) -> None:
        """
        파싱된 노드 섹션들을 각각 개별 저장 (SRP: 저장만 담당)
        """
        try:
            # 검증: 파싱된 섹션 수와 구성 파일 수 비교
            expected_count = len(composition_files)
            parsed_count = len(node_sections)
            
            self.logger.info(f"📊 AI 응답 파싱 결과: 예상 {expected_count}개, 파싱 {parsed_count}개")
            
            if parsed_count < expected_count:
                self.logger.warning(f"⚠️ AI 응답에서 {expected_count - parsed_count}개 구성노드 섹션 누락")
            elif parsed_count == expected_count:
                self.logger.info("✅ AI 응답 파싱 완료: 모든 섹션 정상")
            
            successful_updates = 0
            
            # 각 구성 파일별로 개별 처리
            for i, comp_file in enumerate(composition_files):
                try:
                    if i >= len(node_sections):
                        self.logger.warning(f"⚠️ AI 응답에서 {comp_file}에 해당하는 섹션을 찾을 수 없음")
                        continue
                    
                    # 파일 경로 구성
                    comp_file_path = self._get_composition_file_path(comp_file, user_output_path, parent_doc)
                    
                    # 기존 추출 섹션 로드 (주요/부차 화제 보존용)
                    existing_extraction = await self._load_parent_topic_extractions(comp_file_path)
                    
                    # 업데이트된 섹션과 기존 주요/부차 화제 결합
                    final_sections = self._merge_with_preserved_topics(node_sections[i], existing_extraction)
                    
                    # 개별 저장 (기존 로직 재활용)
                    await self._save_updated_extraction_to_file(
                        file_path=comp_file_path,
                        updated_extraction=final_sections,
                        status_marker="<부모 노드 반영 완료>"
                    )
                    
                    successful_updates += 1
                    self.logger.info(f"✅ 구성 노드 저장 완료: {comp_file}")
                    
                except Exception as e:
                    self.logger.error(f"❌ 구성 노드 {comp_file} 처리 실패: {e}")
                    continue
            
            self.logger.info(f"📊 구성 노드 개별 저장 완료: {successful_updates}/{len(composition_files)}개")
            
        except Exception as e:
            self.logger.error(f"❌ AI 응답 파싱 및 저장 실패: {e}")
            raise

    def _get_composition_file_path(self, comp_file: str, user_output_path: str, parent_doc: Dict) -> Path:
        """
        구성 파일 경로 구성 (parent_doc file_name에서 경로 추출)
        parent_doc의 file_name에서 {책폴더}/{장폴더}/unified_info_docs 경로를 추출하여 활용
        """
        # parent_doc의 file_name에서 경로 정보 추출
        parent_filename = parent_doc.get('file_name', '')
        if not parent_filename:
            raise ValueError("parent_doc에 file_name이 없습니다")
        
        # file_name에서 디렉토리 부분만 추출 (파일명 제외)
        # 예: "Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/unified_info_docs/16_lev2_1.1_OOP_design_Classic_or_classical_info.md"
        # -> "Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/unified_info_docs"
        parent_dir = '/'.join(parent_filename.split('/')[:-1])
        
        comp_file_path = Path(user_output_path) / parent_dir / comp_file
        return comp_file_path

    async def _load_parent_topic_extractions(self, comp_file_path: Path) -> Dict[str, str]:
        """기존 추출 섹션에서 주요/부차 화제 로드 (보존용)"""
        try:
            if not comp_file_path.exists():
                raise FileNotFoundError(f"구성 파일을 찾을 수 없음: {comp_file_path}")
            
            with open(comp_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 추출
            extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# |$)', content, re.DOTALL)
            if not extraction_match:
                raise ValueError(f"추출 섹션을 찾을 수 없음: {comp_file_path}")
                
            extraction_content = extraction_match.group(1).strip()
            if not extraction_content:
                raise ValueError(f"추출 섹션이 비어있음: {comp_file_path}")
                
            parsed_sections = parse_extraction_response(extraction_content)
            if not parsed_sections:
                raise ValueError(f"추출 섹션 파싱 실패: {comp_file_path}")
                
            return parsed_sections
            
        except Exception as e:
            self.logger.error(f"❌ 부모 화제 추출 실패: {comp_file_path} - {e}")
            raise RuntimeError(f"부모 화제 추출 실패: {comp_file_path} - {e}")

    def _merge_with_preserved_topics(self, updated_sections: Dict[str, str], existing_extraction: Dict[str, str]) -> Dict[str, str]:
        """
        업데이트된 핵심 3개 섹션과 기존 주요/부차 화제 결합
        engines_v5.py 보존 로직
        """
        return {
            'core_content': updated_sections.get('core_content', existing_extraction.get('core_content', '')),
            'detailed_core_content': updated_sections.get('detailed_core_content', existing_extraction.get('detailed_core_content', '')),
            'detailed_content': updated_sections.get('detailed_content', existing_extraction.get('detailed_content', '')),
            'main_topics': existing_extraction.get('main_topics', ''),      # 보존
            'sub_topics': existing_extraction.get('sub_topics', '')        # 보존
        }

    def _parse_ai_response_for_composition(self, response: str) -> List[Dict[str, str]]:
        """
        AI 응답을 구성 노드별로 파싱 (engines_v5.py 패턴)
        """
        node_sections = []
        
        # 정규표현식을 사용한 개선된 분할 방식 (구성노드{숫자}: 패턴)
        sections = []
        
        # 구성노드1:, 구성노드2:, 구성노드3:, 구성노드4: 패턴으로 분할
        pattern = r'구성노드\d+:'
        parts = re.split(pattern, response)
        
        if len(parts) > 1:
            # 첫 번째 부분은 구성노드 이전의 내용이므로 제외
            sections = parts[1:]  # 구성노드 내용만 추출
        
        # 파싱 디버깅
        self.logger.info(f"🔍 AI 응답 파싱 디버깅:")
        self.logger.info(f"  - 전체 섹션 수: {len(sections)}")
        for i, section in enumerate(sections):
            self.logger.info(f"  - 섹션 {i}: 길이={len(section)}, 시작={repr(section[:50])}...")
        
        # 구성노드 내용만 처리 (정규표현식으로 깔끔하게 분할됨)
        for i, section in enumerate(sections, 1):
            if not section.strip():
                self.logger.warning(f"  - 구성노드 {i}: 빈 섹션 스킵")
                continue
                
            # 각 섹션에서 핵심 3개 섹션 추출
            parsed_sections = parse_extraction_response(section)
            if parsed_sections:
                node_sections.append(parsed_sections)
                self.logger.info(f"  - 구성노드 {i}: 파싱 성공 (키: {list(parsed_sections.keys())})")
            else:
                self.logger.warning(f"  - 구성노드 {i}: 파싱 실패")
        
        self.logger.info(f"🔍 최종 파싱 결과: {len(node_sections)}개 노드")
        return node_sections

    async def process_single_document(self, doc: Dict, user_output_path: str) -> Dict[str, Any]:
        """
        단일 문서 처리 - 문서 명세서의 통합 로직 구현
        
        Args:
            doc: 문서 정보 (title, level, composition_files, content_section 등)
            user_output_path: 사용자 지정 저장 경로
            
        Returns:
            Dict: {output: {...}, error: str|None}
            
        처리 과정:
        1. 모든 노드: 추출 작업 수행 (generate_extract_section)
        2. 모든 노드: 추출 결과 저장 (save_extraction_result)
        3. 비리프 노드만: 업데이트 과정 
           - update_current_extraction_section
           - update_composition_extraction_sections
        """
        try:
            doc_title = doc.get('title', 'Unknown')
            is_non_leaf = len(doc.get('composition_files', [])) > 0
            
            self.logger.info(f"🔄 단일 문서 처리 시작: {doc_title} ({'비리프' if is_non_leaf else '리프'})")
            
            # 1단계: 모든 노드에서 추출 작업 수행
            self.logger.info(f"🤖 추출 작업 시작: {doc_title}")
            extraction_result = await self.generate_extract_section(doc)
            
            if not extraction_result:
                self.logger.warning(f"⚠️ 추출 실패: {doc_title}")
                return {
                    'output': {},
                    'error': f"추출 실패: {doc_title}"
                }
            
            self.logger.info(f"✅ 추출 성공: {doc_title} ({len(extraction_result)} 섹션)")
            
            # 2단계: 모든 노드에서 추출 결과 저장 (공통)
            self.logger.info(f"💾 추출 결과 저장 시작: {doc_title}")
            saved_file_path = await self.save_extraction_result(
                doc=doc,
                extraction_result=extraction_result,
                user_output_path=user_output_path
            )
            
            if not saved_file_path:
                self.logger.warning(f"⚠️ 저장 실패: {doc_title}")
                return {
                    'output': {},
                    'error': f"저장 실패: {doc_title}"
                }
            
            self.logger.info(f"✅ 저장 완료: {doc_title}")
            
            # 3단계: 비리프 노드만 업데이트 과정 진행
            if is_non_leaf:
                self.logger.info(f"🔄 비리프 노드 업데이트 시작: {doc_title}")
                
                # 현재 노드 업데이트 (파일에서 읽어서 처리)
                updated_extraction, used_composition = await self.update_current_extraction_section(
                    doc=doc,
                    user_output_path=user_output_path
                )
                
                self.logger.info(f"✅ 현재 노드 업데이트 완료: {doc_title}")
                
                # 구성 노드들 업데이트 (파일에서 읽어서 처리)
                await self.update_composition_extraction_sections(
                    parent_doc=doc,
                    parent_extraction=updated_extraction,
                    used_composition_extractions=used_composition,
                    composition_files=doc.get('composition_files', []),
                    user_output_path=user_output_path
                )
                
                self.logger.info(f"✅ 구성 노드 업데이트 완료: {doc_title}")
            else:
                self.logger.info(f"⏭️ 리프 노드로 업데이트 단계 건너뜀: {doc_title}")
            
            # 성공 결과 반환
            self.logger.info(f"🎉 단일 문서 처리 완료: {doc_title}")
            return {
                'output': {
                    'doc_title': doc_title,
                    'node_type': 'non_leaf' if is_non_leaf else 'leaf',
                    'composition_files_count': len(doc.get('composition_files', []))
                },
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"❌ 단일 문서 처리 실패: {doc.get('title', 'Unknown')} - {e}")
            return {
                'output': {},
                'error': f"처리 실패: {doc.get('title', 'Unknown')} - {str(e)}"
            }

