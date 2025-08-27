# 생성 시간: 2025-08-27 15:20 KST
# 핵심 내용: Claude SDK를 사용한 콘텐츠 분석 및 추출 섹션 생성 모듈
# 상세 내용:
#   - analyze_content_with_claude() (라인 21-85): Claude SDK로 내용 분석하여 추출 섹션 생성
#   - create_extraction_section() (라인 87-120): 추출 섹션 마크다운 포맷 생성
#   - extract_content_length() (라인 122-135): 내용 길이 계산 함수
# 상태: active
# 주소: modules/content_analyzer
# 참조: transcript_improver.py의 Claude SDK 패턴 참조

import asyncio
import re
from typing import Dict, Any
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
from claude_code_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError


async def analyze_content_with_claude(content_text: str, max_retries: int = 2) -> Dict[str, Any]:
    """
    Claude SDK를 사용해 내용을 분석하고 추출 섹션 생성
    
    Args:
        content_text (str): 분석할 내용 텍스트
        max_retries (int): 최대 재시도 횟수
        
    Returns:
        Dict[str, Any]: 분석 결과
    """
    for attempt in range(max_retries + 1):
        try:
            options = ClaudeCodeOptions(
                system_prompt="당신은 YouTube 콘텐츠 분석 전문가입니다. 주어진 내용을 분석하여 핵심 내용, 상세 분석, 주요 화제를 추출합니다.",
                max_turns=1
            )
            
            # 내용 길이 계산
            content_length = extract_content_length(content_text)
            
            user_prompt = f"""다음 YouTube 콘텐츠를 분석해서 추출 섹션을 생성해주세요:

{content_text}

**요구사항:**
1. 핵심 내용: 1-2문장으로 전체 내용 요약 (길이: {content_length} 문자)
2. 상세 핵심 내용: 3-5문단으로 상세 분석 및 해석
3. 상세 내용: 깊이 있는 분석과 인사이트 (여러 문단)
4. 주요 화제: 주요 주제들을 불릿 포인트로 나열
5. 부차 화제: 세부적인 주제들을 불릿 포인트로 나열

**출력 형식:**
## 핵심 내용
[1-2문장 요약] (길이: {content_length} 문자)

## 상세 핵심 내용
[상세 분석 내용]

## 상세 내용  
[깊이 있는 해석과 인사이트]

## 주요 화제
- [주제 1]: [설명]
- [주제 2]: [설명]
...

## 부차 화제
- [부차 주제 1]: [설명]
- [부차 주제 2]: [설명]
...

추출 섹션만 반환하고, 다른 설명은 추가하지 마세요."""

            # Claude SDK 호출
            response_content = ""
            async for message in query(prompt=user_prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_content += block.text
            
            if response_content:
                print(f"✅ 내용 분석 완료 (시도 {attempt + 1}/{max_retries + 1})")
                return {
                    "success": True,
                    "extraction_section": response_content.strip(),
                    "content_length": content_length
                }
            else:
                print(f"❌ 빈 응답 수신 (시도 {attempt + 1}/{max_retries + 1})")
                
        except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
            print(f"❌ Claude SDK 오류 (시도 {attempt + 1}/{max_retries + 1}): {str(e)}")
        except Exception as e:
            print(f"❌ 분석 중 오류 (시도 {attempt + 1}/{max_retries + 1}): {str(e)}")
    
    return {"success": False, "error": "내용 분석 실패"}


def create_extraction_section(analysis_result: Dict[str, Any]) -> str:
    """
    분석 결과를 바탕으로 추출 섹션 마크다운 생성
    
    Args:
        analysis_result (Dict[str, Any]): 분석 결과
        
    Returns:
        str: 추출 섹션 마크다운 텍스트
    """
    if not analysis_result.get("success"):
        return "# 추출\n---\n## 오류\n내용 분석에 실패했습니다."
    
    extraction_section = analysis_result.get("extraction_section", "")
    
    # 추출 섹션 헤더 추가
    formatted_section = f"""# 추출
---
{extraction_section}
"""
    
    return formatted_section


def extract_content_length(content_text: str) -> int:
    """
    내용 텍스트의 길이 계산 (한글 기준)
    
    Args:
        content_text (str): 내용 텍스트
        
    Returns:
        int: 텍스트 길이
    """
    # 마크다운 헤더와 구분자 제거
    clean_text = re.sub(r'^#+\s.*$', '', content_text, flags=re.MULTILINE)
    clean_text = re.sub(r'^---+$', '', clean_text, flags=re.MULTILINE)
    clean_text = clean_text.strip()
    
    return len(clean_text)