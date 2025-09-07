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
import yaml

# 실제 구현된 모듈 활용
import sys
import os
# refactoring 프로젝트 경로 추가
refactoring_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, refactoring_root)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from src.utils.text_utils import normalize_title

from src.services.ai_service_v4 import AIService


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
            
            return {
                'title': title,
                'level': level,
                'composition_section': composition_section,
                'content_section': content_section,
                'extraction_section': extraction_section,  # 추가
                'file_path': file_path,
                'full_content': content
            }
        except Exception as e:
            self.logger.error(f"❌ 문서 파싱 실패: {file_path} - {e}")
            return None

    async def generate_extract_section(self, doc: Dict) -> Dict[str, str]:
        """🤖 engines_v5.py 패턴 활용한 5개 섹션 추출"""
        content = doc.get('content_section', '')
        title = doc.get('title', '')
        
        if not content.strip():
            self.logger.warning(f"⚠️ 내용 섹션이 비어있음: {title}")
            return {}
        
        # engines_v5.py 프롬프트 패턴 활용
        prompt = f"""다음 문서에서 5가지 정보를 순서대로 추출해주세요.

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

        system_prompt = """문서 분석 전문가. 주어진 5가지 정보 타입을 순서대로 정확하게 추출하세요.
- 핵심 내용: 간결하고 정확한 요약
- 상세 핵심 내용: 상세하면서도 핵심적인 내용
- 상세 정보: 체계적이고 포괄적인 정리
- 주요 화제: 핵심 주제들
- 부차 화제: 부차적이지만 의미있는 주제들

정확한 형식을 지켜서 출력하세요."""
        
        try:
            self.logger.info(f"🤖 AI 추출 시작: {title}")
            
            # AI 서비스 호출 (content_processing 설정 활용)
            response = await self.ai_service.query_single_request(
                prompt=prompt,
                additional_data={'system_prompt': system_prompt}
            )
            
            # engines_v5.py 파싱 로직 활용
            sections = self.parse_extraction_response(response)
            
            # 성공 판정 (5개 모두 추출되었는지 확인)
            success_count = sum(1 for content in sections.values() if content.strip() and content.startswith('##'))
            if success_count >= 3:  # engines_v5.py와 동일한 기준
                self.api_calls_counter += 1
                self.logger.info(f"✅ 추출 성공: {title} ({success_count}/5 섹션)")
                return sections
            else:
                self.logger.warning(f"⚠️ 추출 섹션 불완전: {title} ({success_count}/5)")
                return {}
                
        except Exception as e:
            self.logger.error(f"❌ 추출 실패: {title} - {e}")
            return {}

    def parse_extraction_response(self, response: str) -> Dict[str, str]:
        """📋 AI 응답을 5개 섹션으로 파싱 (engines_v5.py 로직 활용)"""
        sections = {
            'core_content': '',
            'detailed_core_content': '',
            'detailed_content': '',
            'main_topics': '',
            'sub_topics': ''
        }
        
        # 섹션 헤더 매핑 (engines_v5.py와 동일)
        section_headers = {
            '## 핵심 내용': 'core_content',
            '## 상세 핵심 내용': 'detailed_core_content', 
            '## 상세 정보': 'detailed_content',
            '## 주요 화제': 'main_topics',
            '## 부차 화제': 'sub_topics'
        }
        
        lines = response.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # 섹션 헤더 확인
            if line_stripped in section_headers:
                # 이전 섹션 저장 (헤더 포함)
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # 새 섹션 시작 (헤더부터 시작)
                current_section = section_headers[line_stripped]
                current_content = [line_stripped]  # 헤더 포함
            elif current_section and line.strip():  # 빈 줄이 아닌 경우만 추가
                current_content.append(line)
            elif current_section and not line.strip() and current_content:  # 빈 줄도 포함 (단, 시작이 아닌 경우)
                current_content.append(line)
        
        # 마지막 섹션 저장
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections

    async def load_and_sort_documents(self, book_folder_path: str) -> List[List[Dict]]:
        """📚 문서 로드 및 정렬 - 리프/비리프 분리"""
        unified_docs_dir = os.path.join(book_folder_path, "unified_info_docs")
        
        if not os.path.exists(unified_docs_dir):
            self.logger.error(f"❌ 통합 문서 디렉터리 없음: {unified_docs_dir}")
            return []
        
        # *_info.md 파일들 검색
        documents = []
        for file_path in glob.glob(f"{unified_docs_dir}/*_info.md"):
            doc_data = await self.parse_unified_document(file_path)
            if doc_data:
                documents.append(doc_data)
        
        if not documents:
            self.logger.warning("⚠️ 처리할 문서가 없습니다")
            return []
        
        self.logger.info(f"📄 로드된 문서: {len(documents)}개")
        
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
        
        self.logger.info(f"📊 리프 노드: {len(leaf_nodes)}개, 비리프 노드: {len(non_leaf_nodes)}개")
        
        # level별 그룹화 (비리프 노드들)
        level_groups = {}
        for doc in non_leaf_nodes:
            level = doc.get('level', 0)
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(doc)
        
        # 최종 정렬된 그룹들 (리프 노드가 먼저, 그다음 level 내림차순)
        sorted_groups = [leaf_nodes]  # 리프 노드 그룹이 먼저
        for level in sorted(level_groups.keys(), reverse=True):  # level 내림차순
            sorted_groups.append(level_groups[level])
        
        # 빈 그룹 제거
        final_groups = [group for group in sorted_groups if group]
        
        self.logger.info(f"📋 정렬 완료: {len(final_groups)}개 그룹")
        return final_groups

    def format_extraction_content(self, extraction_result: Dict[str, str]) -> str:
        """📝 추출 결과를 마크다운 형식으로 포맷팅"""
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

    async def update_extraction_section(self, file_path: str, formatted_content: str):
        """💾 파일의 추출 섹션 업데이트"""
        if not formatted_content.strip():
            self.logger.warning(f"⚠️ 업데이트할 내용이 비어있음: {file_path}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 패턴 찾기
            extraction_pattern = r'(# 추출\n---\n)(.*?)(?=\n# 내용|$)'
            
            if re.search(extraction_pattern, content, re.DOTALL):
                # 기존 추출 섹션 교체
                new_content = re.sub(
                    extraction_pattern,
                    f'\\1{formatted_content}\n',
                    content,
                    flags=re.DOTALL
                )
            else:
                # 추출 섹션이 없으면 추가 (# 내용 앞에)
                content_pattern = r'(\n# 내용)'
                if re.search(content_pattern, content):
                    new_content = re.sub(
                        content_pattern,
                        f'\n# 추출\n---\n{formatted_content}\n\\1',
                        content
                    )
                else:
                    # # 내용 섹션도 없으면 파일 끝에 추가
                    new_content = content + f'\n\n# 추출\n---\n{formatted_content}\n'
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            self.logger.info(f"💾 추출 섹션 업데이트 완료: {Path(file_path).name}")
                
        except Exception as e:
            self.logger.error(f"❌ 파일 업데이트 실패: {file_path} - {e}")
            raise

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
                    # 기본 추출 작업
                    extraction_result = await self.generate_extract_section(doc)
                    if extraction_result:
                        formatted_content = self.format_extraction_content(extraction_result)
                        await self.update_extraction_section(doc['file_path'], formatted_content)
                        total_processed += 1
                
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
                    extraction_content = self.extract_core_content_from_doc(matched_doc)
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
            output_file = os.path.join(book_folder_path, f"{chapter_name}_enhanced_toc.md")
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

    def extract_core_content_from_doc(self, doc_data: Dict) -> str:
        """📝 문서에서 핵심 내용 추출"""
        extraction_section = doc_data.get('extraction_section', '').strip()
        
        if not extraction_section or extraction_section == '---':
            return "[추출 내용 없음]"
        
        # 핵심 내용, 상세 핵심 내용, 상세 정보 섹션만 추출
        sections = self.parse_extraction_sections(extraction_section)
        
        core_sections = []
        for section_name in ['core_content', 'detailed_core_content', 'detailed_content']:
            if section_name in sections and sections[section_name].strip():
                content = sections[section_name].strip()
                if content.startswith('##'):
                    core_sections.append(content)
        
        if core_sections:
            return '\n\n'.join(core_sections)
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
                # 이전 섹션 저장
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # 새 섹션 시작
                section_title = line[3:].strip()  # ## 제거
                if '핵심 내용' in section_title:
                    current_section = 'core_content'
                elif '상세 핵심' in section_title:
                    current_section = 'detailed_core_content'
                elif '상세 정보' in section_title:
                    current_section = 'detailed_content'
                elif '주요 화제' in section_title:
                    current_section = 'main_topics'
                elif '부차 화제' in section_title:
                    current_section = 'sub_topics'
                else:
                    current_section = None
                
                current_content = [line]  # 헤더 포함
            elif current_section:
                current_content.append(line)
        
        # 마지막 섹션 저장
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections