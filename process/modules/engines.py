# 생성 시간: 2025-08-30 16:58:49 KST
# 핵심 내용: 추출 및 업데이트 엔진 클래스들 - 5개 정보 타입 병렬 처리 및 구성 노드 업데이트
# 상세 내용:
#   - ExtractionEngine (20-120): 5개 정보 타입 병렬 추출 엔진
#   - UpdateEngine (122-250): 구성 노드 기반 정보 타입별 업데이트 엔진
# 상태: active
# 주소: engines
# 참조: unified_node_processor_v3.py

import asyncio
import logging
from typing import List

from .core import NodeInfo, ExtractionResult
from .ai_providers import AIProviderFactory
from .managers import UpdateLogger, NodeDocumentManager


class ExtractionEngine:
    """추출 엔진 - 5개 정보 타입 병렬 처리"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
    
    async def extract_all_info(self, content: str, title: str, 
                              update_logger: UpdateLogger = None) -> ExtractionResult:
        """5개 정보 타입 병렬 추출"""
        self.logger.info(f"🔍 추출 시작: {title}")
        
        try:
            # 5개 추출 작업을 병렬로 실행
            tasks = [
                self._extract_core_content(content, title, update_logger),
                self._extract_detailed_core_content(content, title, update_logger),
                self._extract_detailed_content(content, title, update_logger),
                self._extract_main_topics(content, title, update_logger),
                self._extract_sub_topics(content, title, update_logger)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 병합
            result = ExtractionResult()
            
            if not isinstance(results[0], Exception):
                result.core_content = results[0]
            if not isinstance(results[1], Exception):
                result.detailed_core_content = results[1]
            if not isinstance(results[2], Exception):
                result.detailed_content = results[2]
            if not isinstance(results[3], Exception):
                result.main_topics = results[3]
            if not isinstance(results[4], Exception):
                result.sub_topics = results[4]
            
            # 성공 여부 판단
            success_count = sum(1 for r in results if not isinstance(r, Exception))
            result.success = success_count >= 3  # 5개 중 3개 이상 성공
            
            self.logger.info(f"✅ 추출 완료: {title} ({success_count}/5 성공)")
            return result
            
        except Exception as e:
            self.logger.error(f"추출 실패: {title} - {e}")
            return ExtractionResult(success=False, error=str(e))
    
    async def _extract_core_content(self, content: str, title: str,
                                   update_logger: UpdateLogger = None) -> str:
        """핵심 내용 추출"""
        prompt = f"""다음 문서의 핵심 내용을 간결하게 요약해주세요.

문서 제목: {title}
문서 내용:
{content}

핵심 내용을 2-3문장으로 요약해주세요."""
        
        system_prompt = "문서 요약 전문가. 핵심 내용을 정확하고 간결하게 요약하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        # 로그 저장
        if update_logger:
            await update_logger.log_extraction_with_prompt(
                title, "핵심내용", prompt, system_prompt, response.strip()
            )
        
        return response.strip()
    
    async def _extract_detailed_core_content(self, content: str, title: str,
                                           update_logger: UpdateLogger = None) -> str:
        """상세 핵심 내용 추출"""
        prompt = f"""다음 문서의 상세 핵심 내용을 정리해주세요.

문서 제목: {title}
문서 내용:
{content}

주요 개념과 중요한 세부사항을 포함하여 5-7문장으로 정리해주세요."""
        
        system_prompt = "문서 분석 전문가. 상세하면서도 핵심적인 내용을 정리하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        # 로그 저장
        if update_logger:
            await update_logger.log_extraction_with_prompt(
                title, "상세핵심내용", prompt, system_prompt, response.strip()
            )
        
        return response.strip()
    
    async def _extract_detailed_content(self, content: str, title: str,
                                       update_logger: UpdateLogger = None) -> str:
        """상세 정보 추출"""
        prompt = f"""다음 문서의 상세 정보를 체계적으로 정리해주세요.

문서 제목: {title}
문서 내용:
{content}

문서의 모든 중요한 정보를 빠뜨리지 않고 체계적으로 정리해주세요."""
        
        system_prompt = "문서 정리 전문가. 상세하고 체계적으로 정보를 정리하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        # 로그 저장
        if update_logger:
            await update_logger.log_extraction_with_prompt(
                title, "상세정보", prompt, system_prompt, response.strip()
            )
        
        return response.strip()
    
    async def _extract_main_topics(self, content: str, title: str,
                                  update_logger: UpdateLogger = None) -> str:
        """주요 화제 추출"""
        prompt = f"""다음 문서의 주요 화제들을 추출해주세요.

문서 제목: {title}
문서 내용:
{content}

문서에서 다루는 핵심 주제들을 불렛 포인트로 나열해주세요."""
        
        system_prompt = "주제 분석 전문가. 문서의 핵심 주제들을 정확히 파악하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        # 로그 저장
        if update_logger:
            await update_logger.log_extraction_with_prompt(
                title, "주요화제", prompt, system_prompt, response.strip()
            )
        
        return response.strip()
    
    async def _extract_sub_topics(self, content: str, title: str,
                                 update_logger: UpdateLogger = None) -> str:
        """부차 화제 추출"""
        prompt = f"""다음 문서의 부차적인 화제들을 추출해주세요.

문서 제목: {title}
문서 내용:
{content}

주요 주제 외에 언급되는 부차적인 주제들을 불렛 포인트로 나열해주세요."""
        
        system_prompt = "주제 분석 전문가. 부차적이지만 의미있는 주제들을 파악하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        # 로그 저장
        if update_logger:
            await update_logger.log_extraction_with_prompt(
                title, "부차화제", prompt, system_prompt, response.strip()
            )
        
        return response.strip()


class UpdateEngine:
    """업데이트 엔진 - 구성 노드 기반 정보 타입별 업데이트"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
    
    async def update_parent_extraction_with_composition(self, parent_node: NodeInfo,
                                                      doc_manager: NodeDocumentManager,
                                                      update_logger: UpdateLogger = None):
        """구성 노드 추출 내용을 반영한 부모 노드 추출 섹션 업데이트"""
        self.logger.info(f"🔄 부모 노드 추출 섹션 업데이트: {parent_node.title}")
        
        try:
            if not parent_node.children_ids:
                self.logger.info("🔄 구성 노드 없음 - 부모 노드 업데이트 스킵")
                return
            
            # 1. 노드 딕셔너리 확보
            if doc_manager._nodes_dict_cache is None:
                await doc_manager.load_nodes_info()
            
            composition_nodes = []
            for child_id in parent_node.children_ids:
                child_node = doc_manager._nodes_dict_cache.get(child_id)
                if child_node is None:
                    self.logger.warning(f"⚠️ 구성 노드를 찾을 수 없음: {child_id}")
                    continue
                composition_nodes.append(child_node)
            
            if not composition_nodes:
                return
            
            # 2. 각 정보 타입별로 부모 노드 업데이트 (5개 섹션 모두)
            section_types = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
            
            for section_type in section_types:
                await self._update_parent_section_with_composition(
                    parent_node, composition_nodes, section_type, 
                    doc_manager, update_logger
                )
            
            # 부모 노드에 구성 노드 반영 완료 상태 표시 추가
            await doc_manager.add_update_status_mark(parent_node, "<구성 노드 반영 완료>")
            
            self.logger.info(f"✅ 부모 노드 추출 섹션 업데이트 완료: {parent_node.title}")
            
        except Exception as e:
            self.logger.error(f"❌ 부모 노드 추출 섹션 업데이트 실패: {e}")
            raise

    async def update_composition_extractions(self, parent_node: NodeInfo, 
                                           doc_manager: NodeDocumentManager,
                                           update_logger: UpdateLogger = None):
        """구성 노드들의 추출 섹션 배치 업데이트"""
        self.logger.info(f"🔄 구성 노드들 배치 업데이트: {parent_node.title}")
        
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
            
            # 2. 각 정보 타입별로 구성 노드들 업데이트
            section_types = ['core_content', 'detailed_core_content', 'detailed_content']
            
            for section_type in section_types:
                await self._update_composition_section_batch(
                    parent_node, composition_nodes, section_type, 
                    doc_manager, update_logger
                )
            
            # 각 구성 노드에 부모 노드 반영 완료 상태 표시 추가
            for child_node in composition_nodes:
                await doc_manager.add_update_status_mark(child_node, "<부모 노드 반영 완료>")
            
            self.logger.info(f"✅ 모든 구성 노드 배치 업데이트 완료: {len(composition_nodes)}개")
            
        except Exception as e:
            self.logger.error(f"❌ 구성 노드 배치 업데이트 실패: {e}")
            raise
    
    async def _update_composition_section_batch(self, parent_node: NodeInfo,
                                              composition_nodes: List[NodeInfo],
                                              section_type: str,
                                              doc_manager: NodeDocumentManager,
                                              update_logger: UpdateLogger = None):
        """특정 정보 타입에 대해 모든 구성 노드를 배치 업데이트"""
        
        section_names = {
            'core_content': '핵심 내용',
            'detailed_core_content': '상세 핵심 내용',  
            'detailed_content': '상세 정보'
        }
        
        section_name = section_names.get(section_type, section_type)
        
        # 부모 노드의 해당 섹션 내용 가져오기
        parent_doc_content = await doc_manager.load_node_document_content(parent_node)
        parent_sections = doc_manager.parse_extraction_section(parent_doc_content)
        parent_section = parent_sections.get(section_type, "")
        
        if not parent_section:
            self.logger.warning(f"부모 노드 {section_name} 섹션이 비어있음")
            return
        
        # 구성 노드들의 해당 섹션 내용 수집
        composition_info = []
        for child_node in composition_nodes:
            child_doc_content = await doc_manager.load_node_document_content(child_node)
            child_sections = doc_manager.parse_extraction_section(child_doc_content)
            child_section = child_sections.get(section_type, "")
            composition_info.append(f"구성노드{child_node.id}({child_node.title}): {child_section}")
        
        prompt = f"""다음은 부모 노드의 업데이트된 {section_name}을 바탕으로 구성 노드들의 {section_name}을 개선하는 작업입니다.

**부모 노드 ({parent_node.title})의 {section_name}:**
{parent_section}

**구성 노드들의 현재 {section_name}:**
{chr(10).join(composition_info)}

부모 노드의 업데이트된 {section_name}을 반영하여 각 구성 노드의 {section_name}을 개선해주세요.
각 구성 노드의 고유한 특성은 유지하되, 부모와의 일관성과 연결성을 반영해주세요.

다음 형식으로 출력해주세요:
구성노드[ID]: [개선된 {section_name}]
구성노드[ID]: [개선된 {section_name}]
..."""
        
        system_prompt = f"문서 전문가. 부모-구성 노드 관계를 고려하여 {section_name}의 일관성을 유지하면서 각 구성 노드의 특성을 살려 개선하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        if not response.strip():
            self.logger.warning(f"구성 노드 {section_name} 업데이트 응답이 비어있음")
            return
        
        # 로그 저장
        if update_logger:
            await update_logger.log_update_with_prompt(
                parent_node.title, f"구성노드{section_name}업데이트", prompt, system_prompt, response.strip()
            )
        
        # 응답 파싱 및 각 구성 노드 업데이트
        await self._parse_and_update_composition_nodes(
            response, composition_nodes, section_type, doc_manager
        )
    
    async def _parse_and_update_composition_nodes(self, response: str,
                                                composition_nodes: List[NodeInfo],
                                                section_type: str,
                                                doc_manager: NodeDocumentManager):
        """AI 응답을 파싱하고 각 구성 노드 업데이트"""
        try:
            # 구성노드별로 분할하여 다중 라인 내용 처리
            updated_contents = {}
            
            # "구성노드N:" 패턴으로 분할
            parts = response.split('\n구성노드')
            
            if len(parts) > 1:
                for i in range(1, len(parts)):
                    try:
                        # 첫 번째 줄에서 노드 ID 추출
                        lines = parts[i].split('\n', 1)
                        first_line = lines[0]
                        
                        # ID 추출
                        id_match = first_line.split(':', 1)
                        if len(id_match) >= 2:
                            child_id = int(id_match[0].strip())
                            content = id_match[1].strip()
                            
                            # 나머지 줄들 추가
                            if len(lines) > 1:
                                content += '\n' + lines[1]
                            
                            updated_contents[child_id] = content
                            self.logger.debug(f"✅ 구성노드{child_id} 내용 파싱 완료: {len(content)} 문자")
                    except (ValueError, IndexError) as e:
                        self.logger.warning(f"결과 파싱 오류: 구성노드{parts[i] if i < len(parts) else 'Unknown'} - {e}")
            
            # 각 구성 노드 업데이트
            for child_node in composition_nodes:
                if child_node.id in updated_contents:
                    new_content = updated_contents[child_node.id].strip()
                    if new_content:
                        await doc_manager.update_node_section(child_node, section_type, new_content)
                        self.logger.info(f"✅ 구성노드{child_node.id} {section_type} 업데이트 완료")
        
        except Exception as e:
            self.logger.error(f"구성 노드 업데이트 파싱 실패: {e}")
    
    async def _update_parent_section_with_composition(self, parent_node: NodeInfo,
                                                    composition_nodes: List[NodeInfo],
                                                    section_type: str,
                                                    doc_manager: NodeDocumentManager,
                                                    update_logger: UpdateLogger = None):
        """구성 노드 추출 내용을 반영하여 부모 노드의 특정 섹션 업데이트"""
        
        section_names = {
            'core_content': '핵심 내용',
            'detailed_core_content': '상세 핵심 내용',  
            'detailed_content': '상세 정보',
            'main_topics': '주요 화제',
            'sub_topics': '부차 화제'
        }
        
        section_name = section_names.get(section_type, section_type)
        
        # 부모 노드의 현재 해당 섹션 내용 가져오기
        parent_doc_content = await doc_manager.load_node_document_content(parent_node)
        parent_sections = doc_manager.parse_extraction_section(parent_doc_content)
        current_parent_section = parent_sections.get(section_type, "")
        
        # 구성 노드들의 해당 섹션 내용 수집
        composition_info = []
        for child_node in composition_nodes:
            child_doc_content = await doc_manager.load_node_document_content(child_node)
            child_sections = doc_manager.parse_extraction_section(child_doc_content)
            child_section = child_sections.get(section_type, "")
            if child_section:
                composition_info.append(f"구성노드{child_node.id} ({child_node.title})의 {section_name}:\n{child_section}")
        
        if not composition_info:
            self.logger.warning(f"구성 노드들의 {section_name} 섹션이 모두 비어있음")
            return
        
        prompt = f"""다음은 부모 노드의 {section_name}을 구성 노드들의 {section_name} 내용을 반영하여 통합 개선하는 작업입니다.

**부모 노드 ({parent_node.title})의 현재 {section_name}:**
{current_parent_section}

**구성 노드들의 {section_name}:**
{chr(10).join(composition_info)}

구성 노드들의 {section_name} 내용을 종합하여 부모 노드의 {section_name}을 개선해주세요.
- 구성 노드들에서 공통적으로 나타나는 중요한 내용들을 반영
- 부모 노드만의 전체적인 관점 유지
- 기존 부모 노드 내용의 핵심은 보존하되 구성 노드 정보로 보완

개선된 {section_name}만 출력해주세요."""
        
        system_prompt = f"문서 전문가. 부모-구성 노드 관계를 고려하여 정보의 일관성을 유지하면서 {section_name}을 통합 개선하세요."
        
        response, _, _ = await self.ai_factory.generate_content(prompt, system_prompt)
        
        if not response.strip():
            self.logger.warning(f"부모 노드 {section_name} 업데이트 응답이 비어있음")
            return
        
        # 부모 노드 섹션 업데이트
        await doc_manager.update_node_section(parent_node, section_type, response.strip())
        
        # 로그 저장
        if update_logger:
            await update_logger.log_update_with_prompt(
                parent_node.title, f"부모노드{section_name}업데이트", prompt, system_prompt, response.strip()
            )
        
        self.logger.info(f"✅ 부모 노드 {section_name} 업데이트 완료: {parent_node.title}")