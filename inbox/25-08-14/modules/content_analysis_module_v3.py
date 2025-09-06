"""
생성 시간: 2025-08-14 20:11:03 KST
핵심 내용: 추출/업데이트 분리 및 핵심 섹션 분리 처리를 위한 분석 모듈 V3
상세 내용:
    - ContentAnalyzer 클래스 (라인 25-): 추출과 업데이트 함수 완전 분리
    - extract_content() (라인 35-): 순수 추출 작업 - 내용 섹션에서 4가지 정보 추출
    - update_child_extraction() (라인 80-): 자식 노드 업데이트 - 기준/참고 모두 핵심/상세핵심만
    - update_parent_extraction() (라인 140-): 부모 노드 업데이트 - 전체 섹션, 출처 명시
    - format_extraction_section() (라인 185-): "# 추출" + "## 섹션명" 헤더 형식
    - _extract_core_sections() (라인 205-): 추출 섹션에서 핵심/상세핵심만 분리
    - _extract_all_sections() (라인 245-): 추출 섹션에서 모든 섹션 분리
상태: 활성
주소: content_analysis_module_v3/core_sections_separated
참조: content_analysis_module_v2.py
"""

import asyncio
from typing import Dict, List, Tuple, Optional
from claude_code_sdk import query, ClaudeCodeOptions
import logging


class ContentAnalyzer:
    """추출/업데이트 분리 및 핵심 섹션 분리 처리를 위한 분석 모듈 V3"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        
    async def extract_content(self, content: str, title: str) -> Dict[str, str]:
        """
        순수 추출 작업: 내용 섹션에서 4가지 정보 추출
        
        Args:
            content: 분석할 텍스트 내용 (내용 섹션 + 자식 내용 섹션들 결합)
            title: 노드 제목
            
        Returns:
            Dict[str, str]: {'핵심 내용': content, '상세 핵심 내용': content, '주요 화제': content, '부차 화제': content}
        """
        self.logger.info(f"내용 추출 시작: {title}")
        
        # 병렬 분석 실행
        tasks = [
            self._extract_core_content(content, title),
            self._extract_detailed_content(content, title),
            self._extract_main_topics(content, title),
            self._extract_sub_topics(content, title)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 결과 정리
        analysis_result = {}
        sections = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        
        for i, result in enumerate(results):
            section = sections[i]
            if isinstance(result, Exception):
                self.logger.error(f"❌ {section} 추출 실패: {result}")
                analysis_result[section] = f"추출 실패: {str(result)}"
            elif result and len(result) == 2:
                header, content_result = result
                analysis_result[section] = content_result
                self.logger.info(f"✅ {section} 추출 완료: {len(content_result)}자")
            else:
                self.logger.warning(f"⚠️ {section} 추출 결과가 비어있음")
                analysis_result[section] = ""
        
        success_count = sum(1 for v in analysis_result.values() if v and not v.startswith("추출 실패"))
        self.logger.info(f"📊 내용 추출 완료: {success_count}/4 섹션 성공")
        
        return analysis_result
    
    async def update_child_extraction(self, base_extraction: str, reference_extraction: str, 
                                    title: str) -> str:
        """
        자식 노드 추출 섹션 업데이트 - 기준/참고 모두 핵심/상세핵심만 사용
        
        Args:
            base_extraction: 자식 노드의 현재 추출 섹션 전체
            reference_extraction: 부모 노드의 추출 섹션 전체
            title: 자식 노드 제목
            
        Returns:
            str: 업데이트된 추출 섹션 전체 (핵심/상세핵심 업데이트 + 기존 주요/부차 화제 유지)
        """
        self.logger.info(f"자식 노드 추출 업데이트 시작: {title}")
        
        # 기준 문서: 자식 노드에서 핵심/상세핵심만 추출
        base_core_sections = self._extract_core_sections(base_extraction)
        base_core_text = f"""## 핵심 내용
{base_core_sections.get('핵심 내용', '')}

## 상세 핵심 내용
{base_core_sections.get('상세 핵심 내용', '')}"""
        
        # 참고 문서: 부모 노드에서 핵심/상세핵심만 추출
        reference_core_sections = self._extract_core_sections(reference_extraction)
        reference_core_text = f"""## 핵심 내용
{reference_core_sections.get('핵심 내용', '')}

## 상세 핵심 내용
{reference_core_sections.get('상세 핵심 내용', '')}"""
        
        prompt = f"""다음은 자식 노드의 핵심 정보 업데이트 작업입니다.

**기준 문서 (현재 자식 노드의 핵심 정보):**
{base_core_text}

**참고 문서 (부모 노드의 핵심 정보):**
{reference_core_text}

기준 문서를 바탕으로 참고 문서의 정보를 반영하여 더 완전하고 정확한 핵심 정보로 업데이트해주세요.

응답은 반드시 다음 형식을 따라주세요:

## 핵심 내용
[업데이트된 핵심 내용]

## 상세 핵심 내용
[업데이트된 상세 핵심 내용]"""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"추출 섹션 업데이트 전문가. {title}의 핵심 내용과 상세 핵심 내용을 개선하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            updated_core_content = self._extract_content_from_messages(messages)
            
            # 기존 주요/부차 화제와 결합하여 완전한 추출 섹션 생성
            all_base_sections = self._extract_all_sections(base_extraction)
            complete_extraction = f"""{updated_core_content}

## 주요 화제
{all_base_sections.get('주요 화제', '')}

## 부차 화제
{all_base_sections.get('부차 화제', '')}"""
            
            self.logger.info(f"✅ 자식 노드 추출 업데이트 완료: {title}")
            return complete_extraction.strip()
            
        except Exception as e:
            self.logger.error(f"자식 노드 추출 업데이트 중 오류 발생: {e}")
            return f"업데이트 실패: {str(e)}"
    
    async def update_parent_extraction(self, base_extraction: str, children_extractions: List[str], 
                                     title: str) -> str:
        """
        부모 노드 추출 섹션 업데이트 - 전체 섹션 업데이트, 주요/부차 화제는 출처 명시
        
        Args:
            base_extraction: 기준 문서 (부모 노드의 현재 추출 섹션)
            children_extractions: 참고 문서들 (자식 노드들의 추출 섹션들)
            title: 부모 노드 제목
            
        Returns:
            str: 업데이트된 추출 섹션 전체
        """
        self.logger.info(f"부모 노드 추출 업데이트 시작: {title}")
        
        # 자식 추출 섹션들을 하나로 결합
        combined_children = "\n\n".join([f"=== 자식 노드 {i+1} ===\n{extraction}" 
                                       for i, extraction in enumerate(children_extractions)])
        
        prompt = f"""다음은 부모 노드의 추출 섹션 업데이트 작업입니다.

**기준 문서 (현재 부모 노드의 추출 섹션):**
{base_extraction}

**참고 문서들 (자식 노드들의 추출 섹션들):**
{combined_children}

기준 문서를 바탕으로 참고 문서들의 정보를 반영하여 부모 노드의 전체 추출 섹션을 업데이트해주세요.

**업데이트 지침:**
1. 핵심 내용: 전체적인 핵심을 종합하여 업데이트
2. 상세 핵심 내용: 자식들의 정보를 반영하여 더 상세하게 업데이트  
3. 주요 화제: 자식들의 주요 화제를 포함하되 출처 명시 (예: "화제명 (출처: 자식노드1)")
4. 부차 화제: 자식들의 부차 화제를 포함하되 출처 명시 (예: "화제명 (출처: 자식노드2)")

응답은 반드시 다음 형식을 따라주세요:

## 핵심 내용
[업데이트된 핵심 내용]

## 상세 핵심 내용
[업데이트된 상세 핵심 내용]

## 주요 화제
[출처가 명시된 주요 화제들]

## 부차 화제
[출처가 명시된 부차 화제들]"""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"추출 섹션 업데이트 전문가. {title}의 전체 추출 섹션을 자식 정보를 반영하여 종합적으로 개선하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            updated_content = self._extract_content_from_messages(messages)
            self.logger.info(f"✅ 부모 노드 추출 업데이트 완료: {title}")
            return updated_content
            
        except Exception as e:
            self.logger.error(f"부모 노드 추출 업데이트 중 오류 발생: {e}")
            return f"업데이트 실패: {str(e)}"
    
    def format_extraction_section(self, data: Dict[str, str]) -> str:
        """
        새로운 헤더 형식으로 추출 섹션 내용 구성
        ## 핵심 내용 (서브 헤더)
        ## 상세 핵심 내용 (서브 헤더)
        ## 주요 화제 (서브 헤더)
        ## 부차 화제 (서브 헤더)
        """
        content = ""
        section_order = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        
        for section_name in section_order:
            if section_name in data and data[section_name] and data[section_name] != "추출 실패":
                content += f"## {section_name}\n{data[section_name]}\n\n"
        
        return content.strip()
    
    def _extract_core_sections(self, extraction_text: str) -> Dict[str, str]:
        """
        추출 섹션에서 핵심 내용, 상세 핵심 내용만 분리
        
        Args:
            extraction_text: 전체 추출 섹션 텍스트
            
        Returns:
            Dict[str, str]: 핵심 내용, 상세 핵심 내용만 포함
        """
        core_sections = {"핵심 내용": "", "상세 핵심 내용": ""}
        
        if not extraction_text.strip():
            return core_sections
        
        # ## 헤더로 분리
        current_section = None
        current_content = []
        
        for line in extraction_text.split('\n'):
            line_stripped = line.strip()
            
            # ## 헤더 감지
            if line_stripped.startswith('## '):
                # 이전 섹션 저장
                if current_section and current_content:
                    if current_section in core_sections:
                        core_sections[current_section] = '\n'.join(current_content).strip()
                
                # 새 섹션 시작
                section_name = line_stripped[3:].strip()  # "## " 제거
                if section_name in core_sections:
                    current_section = section_name
                    current_content = []
                else:
                    current_section = None
            elif current_section:
                current_content.append(line)
        
        # 마지막 섹션 저장
        if current_section and current_content:
            if current_section in core_sections:
                core_sections[current_section] = '\n'.join(current_content).strip()
        
        return core_sections
    
    def _extract_all_sections(self, extraction_text: str) -> Dict[str, str]:
        """
        추출 섹션에서 모든 섹션 분리
        
        Args:
            extraction_text: 전체 추출 섹션 텍스트
            
        Returns:
            Dict[str, str]: 모든 섹션 포함
        """
        all_sections = {"핵심 내용": "", "상세 핵심 내용": "", "주요 화제": "", "부차 화제": ""}
        
        if not extraction_text.strip():
            return all_sections
        
        # ## 헤더로 분리
        current_section = None
        current_content = []
        
        for line in extraction_text.split('\n'):
            line_stripped = line.strip()
            
            # ## 헤더 감지
            if line_stripped.startswith('## '):
                # 이전 섹션 저장
                if current_section and current_content:
                    if current_section in all_sections:
                        all_sections[current_section] = '\n'.join(current_content).strip()
                
                # 새 섹션 시작
                section_name = line_stripped[3:].strip()  # "## " 제거
                if section_name in all_sections:
                    current_section = section_name
                    current_content = []
                else:
                    current_section = None
            elif current_section:
                current_content.append(line)
        
        # 마지막 섹션 저장
        if current_section and current_content:
            if current_section in all_sections:
                all_sections[current_section] = '\n'.join(current_content).strip()
        
        return all_sections
    
    def _extract_content_from_messages(self, messages: List) -> str:
        """메시지에서 텍스트 내용 추출 유틸리티"""
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        return content.strip()
    
    # 순수 추출용 메서드들
    async def _extract_core_content(self, content: str, title: str) -> Tuple[str, str]:
        """핵심 내용 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 핵심을 2-3문장으로 간결하게 요약해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {title}의 핵심 내용을 간결하고 명확하게 요약하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content_result = self._extract_content_from_messages(messages)
            return ('핵심 내용', content_result)
            
        except Exception as e:
            self.logger.error(f"핵심 내용 추출 중 오류 발생: {e}")
            return ('핵심 내용', f"추출 실패: {str(e)}")

    async def _extract_detailed_content(self, content: str, title: str) -> Tuple[str, str]:
        """상세 핵심 내용 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 상세 핵심 내용을 체계적으로 정리해주세요.
헤더를 사용할 경우 ### 3레벨부터 사용하고, 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {title}의 상세한 내용을 체계적이고 포괄적으로 정리하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content_result = self._extract_content_from_messages(messages)
            return ('상세 핵심 내용', content_result)
            
        except Exception as e:
            self.logger.error(f"상세 핵심 내용 추출 중 오류 발생: {e}")
            return ('상세 핵심 내용', f"추출 실패: {str(e)}")

    async def _extract_main_topics(self, content: str, title: str) -> Tuple[str, str]:
        """주요 화제 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 다루는 주요 화제들을 추출해주세요.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {title}에서 다루는 주요 화제를 체계적으로 식별하고 정리하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content_result = self._extract_content_from_messages(messages)
            return ('주요 화제', content_result)
            
        except Exception as e:
            self.logger.error(f"주요 화제 추출 중 오류 발생: {e}")
            return ('주요 화제', f"추출 실패: {str(e)}")

    async def _extract_sub_topics(self, content: str, title: str) -> Tuple[str, str]:
        """부차 화제 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 다루는 부차적인 화제들을 추출해주세요.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {title}에서 다루는 부차 화제를 체계적으로 식별하고 정리하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content_result = self._extract_content_from_messages(messages)
            return ('부차 화제', content_result)
            
        except Exception as e:
            self.logger.error(f"부차 화제 추출 중 오류 발생: {e}")
            return ('부차 화제', f"추출 실패: {str(e)}")