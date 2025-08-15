"""
생성 시간: 2025-08-14 16:40:30 KST
핵심 내용: 4가지 정보 추출 및 전체 추출 섹션 업데이트를 위한 단순화된 모듈
상세 내용:
    - ContentAnalyzer 클래스 (라인 18-): 4가지 정보 추출/업데이트를 위한 핵심 클래스
    - analyze_content() (라인 28-): 순수 추출 전용 메서드 - 4가지 정보 개별 추출
    - update_extraction_section() (라인 73-): 전체 추출 섹션 통째로 업데이트하는 함수
    - _extract_content_from_messages() (라인 112-): 메시지에서 텍스트 내용 추출 유틸리티
    - 추출용 메서드들 (라인 124-): 4가지 정보별 순수 추출 메서드
상태: 활성 (전체 섹션 업데이트 방식)
주소: content_analysis_module_v2
참조: content_analysis_module.py (원본 버전)
"""

import asyncio
from typing import Dict, List, Tuple, Optional
from claude_code_sdk import query, ClaudeCodeOptions
import logging


class ContentAnalyzer:
    """4가지 정보 추출 및 전체 추출 섹션 업데이트를 위한 단순화된 모듈"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        
    async def analyze_content(self, content: str, title: str) -> Dict[str, str]:
        """
        텍스트 내용에서 4가지 정보를 병렬로 추출 (순수 추출 전용)
        
        Args:
            content: 분석할 텍스트 내용 (이미 결합 완료된 상태)
            title: 섹션/노드 제목
            
        Returns:
            Dict[str, str]: {'핵심 내용': content, '상세 핵심 내용': content, '주요 화제': content, '부차 화제': content}
        """
        self.logger.info(f"순수 추출 분석 시작: {title}")
        
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
                self.logger.error(f"❌ {section} 분석 실패: {result}")
                analysis_result[section] = f"분석 실패: {str(result)}"
            elif result and len(result) == 2:
                header, content_result = result
                analysis_result[section] = content_result
                self.logger.info(f"✅ {section} 분석 완료: {len(content_result)}자")
            else:
                self.logger.warning(f"⚠️ {section} 분석 결과가 비어있음")
                analysis_result[section] = ""
        
        success_count = sum(1 for v in analysis_result.values() if v and not v.startswith("분석 실패"))
        self.logger.info(f"📊 추출 분석 완료: {success_count}/4 섹션 성공")
        
        return analysis_result
    
    async def update_extraction_section(self, prompt: str, base_extraction: str, 
                                      reference_extraction: str, title: str) -> str:
        """
        전체 추출 섹션을 통째로 업데이트하는 함수
        
        Args:
            prompt: 업데이트 지침이 담긴 프롬프트
            base_extraction: 기준 정보 (현재 노드의 전체 추출 섹션)
            reference_extraction: 참고 정보 (부모 또는 자식들의 전체 추출 섹션)
            title: 노드 제목
            
        Returns:
            str: 업데이트된 전체 추출 섹션 내용
        """
        self.logger.info(f"전체 추출 섹션 업데이트 시작: {title}")
        
        full_prompt = f"""{prompt}

**업데이트 대상:** {title}의 전체 추출 섹션

**기준 정보 (현재 추출 섹션):**
{base_extraction}

**참고 정보:**
{reference_extraction}

기준 정보를 바탕으로 참고 정보를 반영하여 더 완전하고 정확한 추출 섹션으로 업데이트해주세요.
응답은 다음 형식을 유지해주세요:

## 핵심 내용
[업데이트된 핵심 내용]

## 상세 핵심 내용
[업데이트된 상세 핵심 내용]

## 주요 화제
[업데이트된 주요 화제]

## 부차 화제
[업데이트된 부차 화제]"""
        
        try:
            messages = []
            async for message in query(
                prompt=full_prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 업데이트 전문가. {title}의 추출 섹션을 개선하고 업데이트하는 것이 목표입니다.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            updated_content = self._extract_content_from_messages(messages)
            self.logger.info(f"✅ 전체 추출 섹션 업데이트 완료: {len(updated_content)}자")
            return updated_content
            
        except Exception as e:
            self.logger.error(f"전체 추출 섹션 업데이트 중 오류 발생: {e}")
            return f"업데이트 실패: {str(e)}"
    
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
    
    # 순수 추출용 메서드들 (기존과 동일)
    async def _extract_core_content(self, content: str, title: str) -> Tuple[str, str]:
        """핵심 내용 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 핵심을 2-3문장으로 간결하게 요약해주세요.
응답에 '핵심 내용'이라는 헤더는 포함하지 마세요."""
        
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
            self.logger.error(f"핵심 내용 분석 중 오류 발생: {e}")
            return ('핵심 내용', f"분석 실패: {str(e)}")

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
            self.logger.error(f"상세 핵심 내용 분석 중 오류 발생: {e}")
            return ('상세 핵심 내용', f"분석 실패: {str(e)}")

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
            self.logger.error(f"주요 화제 분석 중 오류 발생: {e}")
            return ('주요 화제', f"분석 실패: {str(e)}")

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
            self.logger.error(f"부차 화제 분석 중 오류 발생: {e}")
            return ('부차 화제', f"분석 실패: {str(e)}")