# 생성 시간: Sat Sep 13 12:42:32 KST 2025
# 핵심 내용: update_composition_extraction_sections TDD 구현 - engines_v5.py 일괄 업데이트 패턴 적용
# 상세 내용:
#   - TempContentProcessingImpl (라인 30-75): 메인 클래스 및 초기화
#   - update_composition_extraction_sections (라인 77-100): 메인 함수 - 간소화된 플로우
#   - _update_all_composition_sections (라인 102-140): AI 일괄 호출 (engines_v5.py 패턴)
#   - _parse_and_update_all_composition_nodes (라인 142-200): AI 응답 파싱 및 개별 저장
#   - _get_composition_file_path (라인 202-215): 구성 파일 경로 구성 (기존 패턴)
#   - _load_existing_extraction (라인 217-240): 기존 추출 섹션 로드 (주요/부차 화제 보존용)
#   - _merge_with_preserved_topics (라인 242-265): 업데이트된 섹션과 기존 주요/부차 화제 결합
#   - _parse_ai_response (라인 267-300): AI 응답을 구성 노드별로 파싱
#   - _parse_extraction_section (라인 302-325): 추출 섹션 파싱 유틸리티
#   - _save_updated_extraction_to_file (라인 327-350): 기존 저장 로직 재활용
# 상태: active

import os
import re
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# 실제 구현된 모듈 활용
import sys
refactoring_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, refactoring_root)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from src.utils.text_utils import normalize_title
from src.services.ai_service_v4 import AIService

# content_processing 전용 유틸리티 함수들 - 직접 구현 (임포트 이슈 회피)
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


class TempContentProcessingImpl:
    """TEMP 구현: update_composition_extraction_sections - engines_v5.py 일괄 업데이트 패턴"""
    
    def __init__(self, config: Dict, ai_service: AIService):
        self.config = config
        self.ai_service = ai_service
        self.api_calls_counter = 0
        
        # 로깅 설정
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

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
            await self.save_each_composition_node(
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
        self.api_calls_counter += 1
        self.logger.info(f"✅ AI 일괄 호출 완료 (호출 횟수: {self.api_calls_counter})")
        
        return response

    async def _parse_ai_response_to_node_sections(self, response: str) -> List[Dict[str, str]]:
        """
        AI 응답을 구성 노드별로 파싱 (SRP: 파싱만 담당)
        """
        try:
            # AI 응답을 구성 노드별로 파싱
            node_sections = self._parse_ai_response(response)
            
            self.logger.info(f"🔍 최종 파싱 결과: {len(node_sections)}개 노드")
            return node_sections
            
        except Exception as e:
            self.logger.error(f"❌ AI 응답 파싱 실패: {e}")
            raise

    async def save_each_composition_node(self, 
                                       node_sections: List[Dict[str, str]],
                                       parent_doc: Dict,
                                       composition_files: List[str],
                                       user_output_path: str) -> None:
        """
        파싱된 노드 섹션들을 각각 개별 저장 (SRP: 저장만 담당)
        """
        try:
            # 🔍 검증: 파싱된 섹션 수와 구성 파일 수 비교
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
                
            parsed_sections = self._parse_extraction_section(extraction_content)
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
            'main_topics': existing_extraction.get('main_topics', ''),      # 🔥 보존
            'sub_topics': existing_extraction.get('sub_topics', '')        # 🔥 보존
        }

    def _parse_ai_response(self, response: str) -> List[Dict[str, str]]:
        """
        AI 응답을 구성 노드별로 파싱 (engines_v5.py 패턴)
        """
        node_sections = []
        
        # 정규표현식을 사용한 개선된 분할 방식 (구성노드{숫자}: 패턴)
        import re
        sections = []
        
        # 구성노드1:, 구성노드2:, 구성노드3:, 구성노드4: 패턴으로 분할
        pattern = r'구성노드\d+:'
        parts = re.split(pattern, response)
        
        if len(parts) > 1:
            # 첫 번째 부분은 구성노드 이전의 내용이므로 제외
            sections = parts[1:]  # 구성노드 내용만 추출
        
        # 🔍 파싱 디버깅
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
            parsed_sections = self._parse_extraction_section(section)
            if parsed_sections:
                node_sections.append(parsed_sections)
                self.logger.info(f"  - 구성노드 {i}: 파싱 성공 (키: {list(parsed_sections.keys())})")
            else:
                self.logger.warning(f"  - 구성노드 {i}: 파싱 실패")
        
        self.logger.info(f"🔍 최종 파싱 결과: {len(node_sections)}개 노드")
        return node_sections

    def _parse_extraction_section(self, extraction_content: str) -> Dict[str, str]:
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
            match = re.search(pattern, extraction_content, re.DOTALL)
            if match:
                section_title = section_key.replace('_', ' ').replace('content', '내용').replace('detailed core', '상세 핵심').replace('detailed', '상세 정보').replace('main topics', '주요 화제').replace('sub topics', '부차 화제')
                sections[section_key] = f"## {section_title.title()}\n{match.group(1).strip()}"
        
        return sections

    async def _save_updated_extraction_to_file(self, file_path: Path, updated_extraction: Dict, status_marker: str):
        """
        기존 ContentProcessingStage._save_updated_extraction_to_file 로직 재활용
        """
        try:
            # 새로운 추출 섹션 내용 포맷팅 - 상태 마킹 포함
            formatted_extraction = combine_extraction_sections(updated_extraction)
            # 상태 마킹을 추출 섹션 맨 앞에 추가
            formatted_extraction = f"{status_marker}\n\n{formatted_extraction}"
            
            # 기존 추출 섹션 교체 (update_file_extraction_section은 boolean 반환)
            success = update_extraction_section(str(file_path), formatted_extraction)
            
            if success:
                self.logger.info(f"💾 업데이트된 추출 섹션 저장 완료: {file_path.name}")
            else:
                raise Exception("추출 섹션 업데이트 함수가 실패를 반환했습니다")
            
        except Exception as e:
            self.logger.error(f"❌ 업데이트된 추출 섹션 저장 실패: {file_path} - {e}")
            raise