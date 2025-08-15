"""
생성 시간: 2025-08-12 15:00:45 KST
핵심 내용: 4가지 정보(핵심 내용, 상세 핵심 내용, 주요 화제, 부차 화제) 추출을 위한 공통 모듈
상세 내용:
    - ContentAnalyzer 클래스 (라인 18-): 4가지 정보 추출을 위한 핵심 클래스
    - analyze_content(content, title, context_type) (라인 28-): 4가지 정보를 병렬로 추출하는 메인 메서드
    - _analyze_core_content() (라인 65-): 핵심 내용 분석
    - _analyze_detailed_content() (라인 115-): 상세 핵심 내용 분석
    - _analyze_main_topics() (라인 165-): 주요 화제 분석
    - _analyze_sub_topics() (라인 215-): 부차 화제 분석
    - _extract_content_from_messages() (라인 265-): 메시지에서 텍스트 내용 추출 유틸리티
상태: 활성
주소: content_analysis_module
참조: dialectical_synthesis_processor.py (기존 분석 로직 참조)
"""

import asyncio
from typing import Dict, List, Tuple, Optional
from claude_code_sdk import query, ClaudeCodeOptions
import logging


class ContentAnalyzer:
    """4가지 정보 추출을 위한 공통 모듈 - 모든 노드 타입(리프, 내부, 루트)에서 사용 가능"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        
    async def analyze_content(self, content: str, title: str, context_type: str = "section") -> Dict[str, str]:
        """
        텍스트 내용에서 4가지 정보를 병렬로 추출
        
        Args:
            content: 분석할 텍스트 내용
            title: 섹션/노드 제목
            context_type: 컨텍스트 타입 
                - "section": 단일 섹션 분석
                - "combined": 여러 하위 요소 결합 분석 
                - "synthesis": 정반합 통합 분석
                - "enhancement": 기존 정보 개선 분석
            
        Returns:
            Dict[str, str]: {'핵심 내용': content, '상세 핵심 내용': content, '주요 화제': content, '부차 화제': content}
        """
        self.logger.info(f"4가지 정보 분석 시작: {title} (타입: {context_type})")
        
        # 병렬 분석 실행
        tasks = [
            self._analyze_core_content(content, title, context_type),
            self._analyze_detailed_content(content, title, context_type),
            self._analyze_main_topics(content, title, context_type),
            self._analyze_sub_topics(content, title, context_type)
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
        self.logger.info(f"📊 분석 완료: {success_count}/4 섹션 성공")
        
        return analysis_result
    
    async def _analyze_core_content(self, content: str, title: str, context_type: str) -> Tuple[str, str]:
        """핵심 내용 분석 - 컨텍스트 타입별 프롬프트 최적화"""
        prompt_templates = {
            "section": f"""다음은 "{title}" 섹션의 내용입니다:

{content}

이 섹션의 핵심 내용을 2-3문장으로 간결하게 요약해주세요.
응답에 '핵심 내용'이라는 헤더는 포함하지 마세요.""",
            
            "combined": f"""다음은 "{title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{content}

이 전체 내용을 바탕으로 "{title}"의 핵심 내용을 2-3문장으로 요약해주세요.
각 구성 요소의 핵심을 통합적으로 반영하여 전체적인 관점에서 정리해주세요.
응답에 '핵심 내용'이라는 헤더는 포함하지 마세요.""",
            
            "synthesis": f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{content}

기존 상위 섹션의 핵심 내용을 주된 내용으로 유지하면서, 업데이트된 각 구성 요소의 핵심을 반영하여 보다 통합적인 관점으로 개선해주세요.
2-3문장으로 간결하게 작성하고, 응답에 '핵심 내용'이라는 헤더는 포함하지 마세요.""",
            
            "enhancement": f"""다음은 "{title}"의 기존 정보와 보완 정보입니다:

{content}

기존 핵심 내용을 주된 내용으로 유지하면서, 보완 정보를 활용하여 더 나은 핵심 내용으로 개선해주세요.
2-3문장으로 간결하게 작성하고, 응답에 '핵심 내용'이라는 헤더는 포함하지 마세요."""
        }
        
        prompt = prompt_templates.get(context_type, prompt_templates["section"])
        
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

    async def _analyze_detailed_content(self, content: str, title: str, context_type: str) -> Tuple[str, str]:
        """상세 핵심 내용 분석 - 컨텍스트 타입별 프롬프트 최적화"""
        prompt_templates = {
            "section": f"""다음은 "{title}" 섹션의 내용입니다:

{content}

이 섹션의 상세 핵심 내용을 체계적으로 정리해주세요.
헤더를 사용할 경우 ### 3레벨부터 사용하고, 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요.""",
            
            "combined": f"""다음은 "{title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{content}

이 전체 내용을 바탕으로 "{title}"의 상세 핵심 내용을 체계적으로 정리해주세요.
각 구성 요소들 간의 관계와 전체적인 흐름을 고려하여 포괄적으로 설명해주세요.
헤더를 사용할 경우 ### 3레벨부터 사용하고, 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요.""",
            
            "synthesis": f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{content}

기존 상위 섹션의 상세 핵심 내용을 주된 내용으로 유지하면서, 업데이트된 각 구성 요소의 핵심을 반영하여 보다 통합적인 관점으로 개선해주세요.
전체의 구조와 흐름을 반영한 포괄적 설명을 제공하세요.
헤더를 사용할 경우 ### 3레벨부터 사용하고, 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요.""",
            
            "enhancement": f"""다음은 "{title}"의 기존 정보와 보완 정보입니다:

{content}

기존 상세 핵심 내용을 주된 내용으로 유지하면서, 보완 정보를 활용하여 더 포괄적이고 체계적인 상세 내용으로 개선해주세요.
헤더를 사용할 경우 ### 3레벨부터 사용하고, 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요."""
        }
        
        prompt = prompt_templates.get(context_type, prompt_templates["section"])
        
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

    async def _analyze_main_topics(self, content: str, title: str, context_type: str) -> Tuple[str, str]:
        """주요 화제 분석 - 컨텍스트 타입별 프롬프트 최적화"""
        prompt_templates = {
            "section": f"""다음은 "{title}" 섹션의 내용입니다:

{content}

이 섹션에서 다루는 주요 화제들을 추출해주세요.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
            
            "combined": f"""다음은 "{title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{content}

이 전체 내용을 바탕으로 "{title}"에서 다루는 주요 화제들을 추출해주세요.
각 구성 요소에서 나온 주요 화제들을 모두 포함하되, 전체적인 관점에서 통합적으로 정리해주세요.

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
            
            "synthesis": f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{content}

각 구성 요소의 주요 화제들을 모두 포함하되, 출처를 다음과 같이 표시:
- 대부분은 구체적인 구성 요소명으로 표시 (예: [출처: 7_Introduction])
- 일부 화제는 전체적 관점에서 통합된 것으로 표시 (예: [출처: 전체 관점])

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 7_Introduction]
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 전체 관점]

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
            
            "enhancement": f"""다음은 "{title}"의 기존 정보와 보완 정보입니다:

{content}

기존 주요 화제들을 주된 내용으로 유지하면서, 보완 정보를 활용하여 더 완전한 주요 화제 목록으로 개선해주세요.

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        }
        
        prompt = prompt_templates.get(context_type, prompt_templates["section"])
        
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

    async def _analyze_sub_topics(self, content: str, title: str, context_type: str) -> Tuple[str, str]:
        """부차 화제 분석 - 컨텍스트 타입별 프롬프트 최적화"""
        prompt_templates = {
            "section": f"""다음은 "{title}" 섹션의 내용입니다:

{content}

이 섹션에서 다루는 부차적인 화제들을 추출해주세요.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
            
            "combined": f"""다음은 "{title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{content}

이 전체 내용을 바탕으로 "{title}"에서 다루는 부차적인 화제들을 추출해주세요.
각 구성 요소에서 나온 부차 화제들을 모두 포함하되, 전체적인 관점에서 통합적으로 정리해주세요.

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
            
            "synthesis": f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{content}

각 구성 요소의 부차 화제들을 모두 포함하되, 출처를 다음과 같이 표시:
- 대부분은 구체적인 구성 요소명으로 표시 (예: [출처: 7_Introduction])
- 일부 화제는 전체적 관점에서 통합된 것으로 표시 (예: [출처: 전체 관점])

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 7_Introduction]
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 전체 관점]

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
            
            "enhancement": f"""다음은 "{title}"의 기존 정보와 보완 정보입니다:

{content}

기존 부차 화제들을 주된 내용으로 유지하면서, 보완 정보를 활용하여 더 완전한 부차 화제 목록으로 개선해주세요.

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        }
        
        prompt = prompt_templates.get(context_type, prompt_templates["section"])
        
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