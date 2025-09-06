# 생성 시간: 2025-09-01 08:10:54 KST
# 핵심 내용: API 호출 최적화된 추출 및 업데이트 엔진 - 5개 정보 타입 단일 호출 처리
# 상세 내용:
#   - ExtractionEngineV5 클래스 (27-120): 5개 정보 타입을 단일 AI 호출로 순차 처리
#   - UpdateEngineV5 클래스 (122-260): 구성 노드 업데이트를 단일 AI 호출로 통합 처리
#   - API 호출 횟수 추적 기능 (calls_counter): 각 메서드별 API 호출 횟수 추적
#   - 디버깅 로그 저장 기능: 프롬프트, 시스템 프롬프트, 응답 저장
# 상태: active
# 주소: engines_v5
# 참조: engines.py (API 호출 최적화 이전 버전)

import asyncio
import logging
from typing import List, Dict

from .core import NodeInfo, ExtractionResult
from .ai_providers import AIProviderFactory
from .managers import UpdateLogger, NodeDocumentManager


class ExtractionEngineV5:
    """API 호출 최적화된 추출 엔진 - 5개 정보 타입 단일 호출 처리"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
        self.api_calls_counter = 0  # API 호출 횟수 추적
    
    async def extract_all_info(self, content: str, title: str, node: NodeInfo,
                              doc_manager: NodeDocumentManager,
                              update_logger: UpdateLogger = None) -> ExtractionResult:
        """5개 정보 타입을 단일 AI 호출로 순차 추출"""
        self.logger.info(f"🔍 통합 추출 시작: {title}")
        
        try:
            # 단일 통합 프롬프트로 5개 정보 타입 순차 처리
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
            
            # API 호출 (단일 호출)
            self.api_calls_counter += 1
            response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
            
            self.logger.info(f"📊 API 호출 횟수: {self.api_calls_counter}")
            
            # 디버깅 로그 저장
            if update_logger:
                await update_logger.log_extraction_with_prompt(
                    title, "통합추출", prompt, system_prompt, response.strip(),
                    self.ai_factory.provider_type, self.ai_factory.current_model
                )
            
            # AI 응답을 바로 추출 섹션에 저장
            if response.strip():
                await doc_manager.save_raw_extraction_content(node, response.strip())
                self.logger.info(f"✅ 통합 추출 및 저장 완료: {title}")
                # 성공 결과 반환
                result = ExtractionResult()
                result.success = True
                return result
            else:
                self.logger.error(f"❌ 통합 추출 실패 (빈 응답): {title}")
                return ExtractionResult(success=False, error="빈 응답")
            
        except Exception as e:
            self.logger.error(f"통합 추출 실패: {title} - {e}")
            return ExtractionResult(success=False, error=str(e))
    
    def _parse_integrated_response(self, response: str, title: str) -> ExtractionResult:
        """통합 응답을 파싱하여 ExtractionResult 생성 (헤더 포함)"""
        result = ExtractionResult()
        
        try:
            # 섹션별로 분할 (헤더 포함)
            sections = {
                'core_content': '',
                'detailed_core_content': '',
                'detailed_content': '',
                'main_topics': '',
                'sub_topics': ''
            }
            
            # 섹션 제목 매핑
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
            
            # ExtractionResult에 설정 (헤더 포함된 전체 내용)
            result.core_content = sections['core_content']
            result.detailed_core_content = sections['detailed_core_content']
            result.detailed_content = sections['detailed_content']
            result.main_topics = sections['main_topics']
            result.sub_topics = sections['sub_topics']
            
            # 성공 여부 판단 (5개 중 3개 이상 추출되었으면 성공)
            success_count = sum(1 for content in sections.values() if content.strip())
            result.success = success_count >= 3
            
            self.logger.info(f"📊 파싱 결과: {success_count}/5 섹션 추출 성공 (헤더 포함)")
            
        except Exception as e:
            self.logger.error(f"응답 파싱 실패: {title} - {e}")
            result.success = False
            result.error = str(e)
        
        return result
    
    def get_api_calls_count(self) -> int:
        """API 호출 횟수 반환"""
        return self.api_calls_counter


class UpdateEngineV5:
    """API 호출 최적화된 업데이트 엔진 - 구성 노드 업데이트 단일 호출 처리"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
        self.api_calls_counter = 0  # API 호출 횟수 추적
    
    async def update_composition_extractions(self, parent_node: NodeInfo, 
                                           doc_manager: NodeDocumentManager,
                                           update_logger: UpdateLogger = None):
        """구성 노드들의 추출 섹션 통합 업데이트 (단일 API 호출)"""
        self.logger.info(f"🔄 구성 노드들 통합 업데이트: {parent_node.title}")
        
        try:
            if not parent_node.children_ids:
                self.logger.info("🔄 구성 노드 없음 - 업데이트 스킵")
                return
            
            # 1. 노드 딕셔너리 확보
            if doc_manager._nodes_dict_cache is None:
                await doc_manager.load_nodes_info()
            
            composition_nodes = []
            for child_id in parent_node.children_ids:
                child_node = doc_manager._nodes_dict_cache.get(child_id)
                if child_node is None:
                    self.logger.warning("⚠️ 구성 노드를 찾을 수 없음")
                    continue
                composition_nodes.append(child_node)
            
            if not composition_nodes:
                return
            
            # 2. 단일 통합 업데이트 수행
            await self._update_all_composition_sections(
                parent_node, composition_nodes, doc_manager, update_logger
            )
            
            self.logger.info(f"✅ 모든 구성 노드 통합 업데이트 완료: {len(composition_nodes)}개")
            
        except Exception as e:
            self.logger.error(f"❌ 구성 노드 통합 업데이트 실패: {e}")
            raise
    
    async def _update_all_composition_sections(self, parent_node: NodeInfo,
                                             composition_nodes: List[NodeInfo],
                                             doc_manager: NodeDocumentManager,
                                             update_logger: UpdateLogger = None):
        """구성 노드의 핵심 3개 섹션만 단일 API 호출로 업데이트 (주요/부차 화제 보존)"""
        
        # 부모 노드의 핵심 3개 섹션 내용만 가져오기 (주요/부차 화제 제외)
        parent_doc_content = await doc_manager.load_node_document_content(parent_node)
        parent_sections = doc_manager.parse_extraction_section(parent_doc_content)
        
        # 부모 노드의 핵심 3개 정보만 추출 (헤더 제거)
        parent_core = parent_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
        parent_detailed_core = parent_sections.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
        parent_detailed_info = parent_sections.get('detailed_content', '').replace('## 상세 정보', '').strip()
        
        # 구성 노드들의 현재 핵심 3개 섹션 내용만 수집 (주요/부차 화제 제외)
        composition_info = []
        for child_node in composition_nodes:
            child_doc_content = await doc_manager.load_node_document_content(child_node)
            child_sections = doc_manager.parse_extraction_section(child_doc_content)
            
            # 핵심 3개 정보만 추출 (주요 화제, 부차 화제 완전 제외)
            core_content = child_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
            detailed_core = child_sections.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
            detailed_info = child_sections.get('detailed_content', '').replace('## 상세 정보', '').strip()
            
            child_info = f"""
구성노드{child_node.id} ({child_node.title}):
- 핵심 내용: {core_content}
- 상세 핵심 내용: {detailed_core}
- 상세 정보: {detailed_info}"""
            
            composition_info.append(child_info)
        
        prompt = f"""다음은 부모 노드의 업데이트된 내용을 바탕으로 구성 노드들의 핵심 3가지 정보 섹션만 개선하는 작업입니다.

**주의사항: 주요 화제, 부차 화제 섹션은 각 구성 노드의 고유한 내용이므로 업데이트하지 않습니다.**

**부모 노드 ({parent_node.title})의 업데이트된 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}

**구성 노드들의 현재 내용:**
{chr(10).join(composition_info)}

부모 노드의 업데이트된 내용을 반영하여 각 구성 노드의 **3가지 정보 섹션(핵심 내용, 상세 핵심 내용, 상세 정보)만** 개선해주세요.
각 구성 노드의 고유한 특성은 유지하되, 부모와의 일관성과 연결성을 반영해주세요.

반드시 다음 형식을 정확히 지켜서 출력해주세요:

구성노드[ID번호]:
## 핵심 내용
[개선된 핵심 내용]

## 상세 핵심 내용
[개선된 상세 핵심 내용]

## 상세 정보
[개선된 상세 정보]

구성노드[ID번호]:
## 핵심 내용
[개선된 핵심 내용]

## 상세 핵심 내용
[개선된 상세 핵심 내용]

## 상세 정보
[개선된 상세 정보]

**중요**: 
1. 각 섹션은 반드시 "## " (해시 2개 + 공백)으로 시작하는 제목을 포함해야 합니다.
2. 주요 화제, 부차 화제는 출력하지 마세요 (기존 내용 보존용)."""
        
        system_prompt = """문서 전문가. 부모-구성 노드 관계를 고려하여 정보의 일관성을 유지하면서 각 구성 노드의 특성을 살려 개선하세요.
핵심 내용 → 상세 핵심 내용 → 상세 정보의 3개 섹션만 처리하고, 주요 화제/부차 화제는 건드리지 마세요. 정확한 형식을 지켜서 출력하세요."""
        
        # API 호출 (단일 호출)
        self.api_calls_counter += 1
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        self.logger.info(f"📊 API 호출 횟수: {self.api_calls_counter}")
        
        # 디버깅 로그 저장
        if update_logger:
            await update_logger.log_update_with_prompt(
                parent_node.title, "구성노드통합업데이트", prompt, system_prompt, response.strip(),
                self.ai_factory.provider_type, self.ai_factory.current_model
            )
        
        if not response.strip():
            self.logger.warning(f"구성 노드 통합 업데이트 응답이 비어있음")
            return
        
        # 응답 파싱 및 각 구성 노드 업데이트
        await self._parse_and_update_all_composition_nodes(
            response, composition_nodes, doc_manager
        )
    
    async def _parse_and_update_all_composition_nodes(self, response: str,
                                                    composition_nodes: List[NodeInfo],
                                                    doc_manager: NodeDocumentManager):
        """AI 응답을 파싱하고 각 구성 노드의 모든 섹션 업데이트"""
        try:
            # 구성노드별로 분할 (라인 시작 패턴도 고려)
            node_sections = []
            if '\n구성노드' in response:
                node_sections = response.split('\n구성노드')
            elif '구성노드' in response:
                # 라인 시작에 구성노드가 있는 경우도 처리
                parts = response.split('구성노드')
                if len(parts) > 1:
                    node_sections = [''] + [f'구성노드{part}' for part in parts[1:]]
                    
            if len(node_sections) <= 1:
                self.logger.warning("구성노드 섹션을 찾을 수 없음")
                return
            
            updated_nodes = {}
            
            # 빈 섹션이 아닌 것만 처리
            for section in node_sections:
                if not section.strip():  # 빈 섹션은 건너뛰기
                    continue
                try:
                    # 노드 ID 추출
                    lines = section.strip().split('\n')
                    if not lines:
                        continue
                    
                    # 첫 줄에서 ID 추출 (예: "구성노드22:" → 22)
                    first_line = lines[0].strip().rstrip(':')
                    # "구성노드22" → "22" 추출
                    if first_line.startswith('구성노드'):
                        child_id_str = first_line[len('구성노드'):].strip()
                    else:
                        child_id_str = first_line.strip()
                    
                    if not child_id_str.isdigit():
                        self.logger.warning(f"유효하지 않은 노드 ID: '{first_line}' → '{child_id_str}'")
                        continue
                        
                    child_id = int(child_id_str)
                    self.logger.debug(f"구성노드 ID 추출: '{first_line}' → {child_id}")
                    
                    # 섹션 내용 파싱
                    sections_content = {
                        'core_content': '',
                        'detailed_core_content': '',
                        'detailed_content': ''
                    }
                    
                    current_section = None
                    current_content = []
                    
                    for line in lines[1:]:  # 첫 줄(ID) 제외
                        line_stripped = line.strip()
                        
                        if line_stripped == '## 핵심 내용':
                            if current_section and current_content:
                                sections_content[current_section] = '\n'.join(current_content).strip()
                            current_section = 'core_content'
                            current_content = [line_stripped]  # 헤더 포함
                        elif line_stripped == '## 상세 핵심 내용':
                            if current_section and current_content:
                                sections_content[current_section] = '\n'.join(current_content).strip()
                            current_section = 'detailed_core_content'
                            current_content = [line_stripped]  # 헤더 포함
                        elif line_stripped == '## 상세 정보':
                            if current_section and current_content:
                                sections_content[current_section] = '\n'.join(current_content).strip()
                            current_section = 'detailed_content'
                            current_content = [line_stripped]  # 헤더 포함
                        elif current_section and line.strip():  # 빈 줄이 아닌 경우만 추가
                            current_content.append(line)
                        elif current_section and not line.strip() and current_content:  # 빈 줄도 포함 (단, 시작이 아닌 경우)
                            current_content.append(line)
                    
                    # 마지막 섹션 저장
                    if current_section and current_content:
                        sections_content[current_section] = '\n'.join(current_content).strip()
                    
                    updated_nodes[child_id] = sections_content
                    self.logger.debug(f"✅ 구성노드{child_id} 파싱 완료")
                    
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"구성노드 파싱 오류: {section[:50]}... - {e}")
                    continue
            
            # 각 구성 노드의 모든 섹션 업데이트
            for child_node in composition_nodes:
                if child_node.id in updated_nodes:
                    node_sections = updated_nodes[child_node.id]
                    
                    # 핵심 3개 섹션만 업데이트 (주요/부차 화제 보존)
                    section_name_mapping = {
                        'core_content': '핵심 내용',
                        'detailed_core_content': '상세 핵심 내용',
                        'detailed_content': '상세 정보'
                    }
                    
                    for section_type, content in node_sections.items():
                        if content.strip():
                            korean_section_name = section_name_mapping.get(section_type, section_type)
                            await doc_manager.update_node_section(child_node, korean_section_name, content.strip())
                            self.logger.info(f"✅ 구성노드{child_node.id} {korean_section_name} 업데이트 완료 (주요/부차 화제 보존됨)")
                    
                    # 구성 노드에 부모 노드 반영 완료 상태 표시 추가
                    await doc_manager.add_update_status_mark(child_node, "<부모 노드 반영 완료>")
                    self.logger.info(f"✅ 구성노드{child_node.id} 상태 표시 추가: <부모 노드 반영 완료>")
        
        except Exception as e:
            self.logger.error(f"구성 노드 통합 업데이트 파싱 실패: {e}")
    
    async def update_parent_extraction_with_composition(self, parent_node: NodeInfo,
                                                      doc_manager: NodeDocumentManager,
                                                      update_logger: UpdateLogger = None):
        """구성 노드 내용을 반영하여 부모 노드의 추출 섹션 업데이트 (5개 섹션 모두)"""
        self.logger.info(f"🔄 부모 노드 추출 섹션 업데이트 (구성 노드 반영): {parent_node.title}")
        
        try:
            if not parent_node.children_ids:
                self.logger.info("🔄 구성 노드 없음 - 부모 노드 업데이트 스킵")
                return

            # 1. 노드 딕셔너리 확보
            if doc_manager._nodes_dict_cache is None:
                await doc_manager.load_nodes_info()

            # 2. 구성 노드들의 내용 수집
            composition_info = []
            for child_id in parent_node.children_ids:
                child_node = doc_manager._nodes_dict_cache.get(child_id)
                if child_node is None:
                    self.logger.warning(f"⚠️ 구성 노드를 찾을 수 없음: ID {child_id}")
                    continue
                
                child_doc_content = await doc_manager.load_node_document_content(child_node)
                child_sections = doc_manager.parse_extraction_section(child_doc_content)
                
                # 모든 5개 섹션 내용 수집 (헤더 제거)
                core_content = child_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
                detailed_core = child_sections.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
                detailed_info = child_sections.get('detailed_content', '').replace('## 상세 정보', '').strip()
                main_topics = child_sections.get('main_topics', '').replace('## 주요 화제', '').strip()
                sub_topics = child_sections.get('sub_topics', '').replace('## 부차 화제', '').strip()
                
                child_info = f"""
구성노드{child_node.id} ({child_node.title}):
- 핵심 내용: {core_content}
- 상세 핵심 내용: {detailed_core}
- 상세 정보: {detailed_info}
- 주요 화제: {main_topics}
- 부차 화제: {sub_topics}"""
                
                composition_info.append(child_info)

            if not composition_info:
                self.logger.warning("⚠️ 유효한 구성 노드가 없음")
                return

            # 3. 부모 노드의 현재 추출 섹션 내용
            parent_doc_content = await doc_manager.load_node_document_content(parent_node)
            parent_sections = doc_manager.parse_extraction_section(parent_doc_content)
            
            # 부모 노드의 현재 내용 (헤더 제거)
            parent_core = parent_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
            parent_detailed_core = parent_sections.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
            parent_detailed_info = parent_sections.get('detailed_content', '').replace('## 상세 정보', '').strip()
            parent_main_topics = parent_sections.get('main_topics', '').replace('## 주요 화제', '').strip()
            parent_sub_topics = parent_sections.get('sub_topics', '').replace('## 부차 화제', '').strip()

            # 4. 통합 프롬프트로 5개 섹션 모두 업데이트
            prompt = f"""다음은 부모 노드의 추출 섹션을 구성 노드들의 내용을 반영하여 업데이트하는 작업입니다.

**부모 노드 ({parent_node.title})의 현재 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}
주요 화제: {parent_main_topics}
부차 화제: {parent_sub_topics}

**구성 노드들의 내용:**
{chr(10).join(composition_info)}

부모 노드의 각 섹션을 구성 노드들의 내용을 종합적으로 반영하여 개선해주세요. 
부모 노드는 전체적인 개요와 통합적인 관점을 제공하되, 구성 노드들의 세부 내용이 잘 반영되도록 해주세요.

반드시 다음 형식을 정확히 지켜서 출력해주세요:

## 핵심 내용
[구성 노드들의 내용을 종합한 개선된 핵심 내용]

## 상세 핵심 내용
[구성 노드들의 내용을 종합한 개선된 상세 핵심 내용]

## 상세 정보
[구성 노드들의 내용을 종합한 개선된 상세 정보]

## 주요 화제
[구성 노드들의 주요 화제를 종합한 개선된 주요 화제]

## 부차 화제
[구성 노드들의 부차 화제를 종합한 개선된 부차 화제]

**중요**: 각 섹션은 반드시 "## " (해시 2개 + 공백)으로 시작하는 제목을 포함해야 하고, 제목 다음 줄부터 내용을 작성해주세요."""

            system_prompt = """문서 통합 전문가. 부모-구성 노드 관계를 이해하고 구성 노드들의 세부 내용을 종합하여 부모 노드의 각 섹션을 개선하세요.
부모 노드는 전체적인 통합 관점을 제공하되, 구성 노드들의 핵심 내용이 잘 반영되도록 하세요. 정확한 형식을 지켜서 출력하세요."""
            
            # 5. API 호출 (단일 호출)
            self.api_calls_counter += 1
            response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
            
            self.logger.info(f"📊 API 호출 횟수: {self.api_calls_counter}")
            
            # 6. 디버깅 로그 저장
            if update_logger:
                await update_logger.log_update_with_prompt(
                    parent_node.title, "부모노드구성반영업데이트", prompt, system_prompt, response.strip(),
                    self.ai_factory.provider_type, self.ai_factory.current_model
                )

            if not response.strip():
                self.logger.warning(f"부모 노드 업데이트 응답이 비어있음")
                return

            # 7. 응답 파싱 및 부모 노드의 5개 섹션 업데이트
            await self._parse_and_update_parent_sections(response, parent_node, doc_manager)
            
            # 8. 구성 노드 반영 완료 표시 추가
            await doc_manager.add_update_status_mark(parent_node, "<구성 노드 반영 완료>")
            
            self.logger.info(f"✅ 부모 노드 추출 섹션 업데이트 완료 (구성 노드 반영): {parent_node.title}")
            
        except Exception as e:
            self.logger.error(f"❌ 부모 노드 업데이트 실패: {parent_node.title} - {e}")
            raise
    
    async def _parse_and_update_parent_sections(self, response: str, parent_node: NodeInfo,
                                              doc_manager: NodeDocumentManager):
        """부모 노드의 5개 섹션 업데이트를 위한 응답 파싱"""
        try:
            sections = {
                'core_content': '',
                'detailed_core_content': '',
                'detailed_content': '',
                'main_topics': '',
                'sub_topics': ''
            }
            
            # 섹션 제목 매핑
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
            
            # 각 섹션별로 업데이트 (5개 섹션 모두)
            section_names = {
                'core_content': '핵심 내용',
                'detailed_core_content': '상세 핵심 내용',
                'detailed_content': '상세 정보',
                'main_topics': '주요 화제',
                'sub_topics': '부차 화제'
            }
            
            for section_type, content in sections.items():
                if content.strip():
                    korean_section_name = section_names[section_type]
                    await doc_manager.update_node_section(parent_node, korean_section_name, content.strip())
                    self.logger.info(f"✅ 부모노드{parent_node.id} {korean_section_name} 업데이트 완료")
            
        except Exception as e:
            self.logger.error(f"부모 노드 섹션 파싱 실패: {e}")

    def get_api_calls_count(self) -> int:
        """API 호출 횟수 반환"""
        return self.api_calls_counter