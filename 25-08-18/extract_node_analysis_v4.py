# 생성 시간: 2025-08-18 10:49:52 KST
# 핵심 내용: 노드 정보 문서에서 Claude SDK로 핵심 정보를 병렬 추출하여 추출 섹션에 삽입하는 스크립트 (언어 명시 기능 추가)
# 상세 내용:
#   - get_document_language 함수 (라인 25-40): 정보 파일에서 문서 언어 감지
#   - extract_content_section 함수 (라인 43-80): 정보 파일에서 내용 섹션 추출
#   - _extract_core_and_detailed_content 함수 (라인 83-117): 핵심 내용 → 상세 핵심 내용 순차 추출 (언어 지정)
#   - _extract_main_topics_task 함수 (라인 120-134): 주요 화제 추출 작업 (언어 지정)
#   - _extract_sub_topics_task 함수 (라인 137-151): 부차 화제 추출 작업 (언어 지정)
#   - extract_content_parallel 함수 (라인 154-199): 3개 작업을 병렬 처리
#   - update_extraction_section 함수 (라인 352-409): 추출 섹션에 결과 삽입
#   - main 함수 (라인 412-464): 메인 실행 함수
# 상태: 활성
# 주소: extract_node_analysis_v4/language_aware
# 참조: extract_node_analysis (원본 파일)

#!/usr/bin/env python3

import asyncio
import os
import time
import argparse
from typing import Dict, List
from pathlib import Path

# Claude SDK 임포트
try:
    from claude_code_sdk import query, ClaudeCodeOptions
except ImportError:
    print("❌ claude_code_sdk를 찾을 수 없습니다. Claude Code에서 실행해주세요.")
    exit(1)


def get_document_language(info_file: str) -> str:
    """정보 파일에서 문서 언어 감지"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 속성 섹션에서 document_language 찾기
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('document_language:'):
                lang = line.split(':', 1)[1].strip()
                return lang
        
        # 기본값은 english
        return "english"
        
    except Exception as e:
        print(f"⚠️ 언어 감지 실패, 영어로 기본 설정: {e}")
        return "english"


def extract_content_section(info_file: str) -> str:
    """정보 파일에서 '# 내용' 섹션 추출"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        content_start = -1
        content_end = len(lines)
        
        # '# 내용' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_start = i + 1
                break
        
        # 다음 구조 섹션 찾기
        structure_sections = ['# 구성', '# 속성', '# 추출']
        for i in range(content_start, len(lines)):
            line = lines[i].strip()
            if any(line.startswith(section) for section in structure_sections):
                content_end = i
                break
        
        if content_start == -1:
            return ""
        
        # 구분선(---)까지 스킵
        while content_start < content_end and lines[content_start].strip() == '---':
            content_start += 1
        
        # 실제 텍스트가 있는지 확인
        section_content = '\n'.join(lines[content_start:content_end])
        has_actual_text = any(line.strip() and not line.strip() == '---' for line in lines[content_start:content_end])
        
        if not has_actual_text:
            return ""
        
        return section_content.strip()
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""


async def _extract_core_and_detailed_content(content: str, title: str, language: str) -> Dict[str, str]:
    """핵심 내용과 상세 핵심 내용을 순차적으로 추출하는 독립 작업 (언어 지정)"""
    result = {}
    
    # 1. 핵심 내용 추출 (원문 기반)
    core_content = await _extract_core_content(content, title, language)
    if core_content and len(core_content.strip()) >= 10:
        result["핵심 내용"] = core_content
    else:
        core_content = f"❌ 핵심 내용 추출 실패: Claude API 응답 부족"
        result["핵심 내용"] = core_content
    
    # 2. 상세 핵심 내용 추출 (추출된 핵심 내용 + 원문 기반, 300단어 이내)
    if not core_content.startswith("❌"):
        detailed_content = await _extract_detailed_content(content, core_content, title, language)
        if detailed_content and len(detailed_content.strip()) >= 10:
            result["상세 핵심 내용"] = detailed_content
        else:
            result["상세 핵심 내용"] = f"❌ 상세 핵심 내용 추출 실패: Claude API 응답 부족"
    else:
        result["상세 핵심 내용"] = "❌ 핵심 내용 추출 실패로 인한 상세 내용 추출 불가"
    
    return result


async def _extract_main_topics_task(content: str, title: str, language: str) -> Dict[str, str]:
    """주요 화제 추출 독립 작업 (언어 지정)"""
    result = {}
    
    main_topics = await _extract_main_topics(content, title, language)
    if main_topics and len(main_topics.strip()) >= 10:
        result["주요 화제"] = main_topics
    else:
        result["주요 화제"] = f"❌ 주요 화제 추출 실패: Claude API 응답 부족"
    
    return result


async def _extract_sub_topics_task(content: str, title: str, language: str) -> Dict[str, str]:
    """부차 화제 추출 독립 작업 (언어 지정)"""
    result = {}
    
    sub_topics = await _extract_sub_topics(content, title, language)
    if sub_topics and len(sub_topics.strip()) >= 10:
        result["부차 화제"] = sub_topics
    else:
        result["부차 화제"] = f"❌ 부차 화제 추출 실패: Claude API 응답 부족"
    
    return result


async def extract_content_parallel(content: str, title: str, language: str) -> Dict[str, str]:
    """3개 작업을 병렬로 실행하여 핵심 정보 추출 (언어 지정)"""
    print(f"🚀 병렬 추출 시작 (언어: {language})")
    start_time = time.time()
    
    # 3개 독립 작업을 병렬로 실행
    tasks = [
        _extract_core_and_detailed_content(content, title, language),
        _extract_main_topics_task(content, title, language),
        _extract_sub_topics_task(content, title, language)
    ]
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 결과 통합
        final_result = {}
        for result in results:
            if isinstance(result, dict):
                final_result.update(result)
            else:
                print(f"⚠️ 작업 실행 중 예외 발생: {result}")
        
        end_time = time.time()
        print(f"✅ 병렬 추출 완료 ({end_time - start_time:.2f}초)")
        
        return final_result
        
    except Exception as e:
        print(f"❌ 병렬 추출 실패: {e}")
        return {}


async def _extract_core_content(content: str, title: str, language: str) -> str:
    """핵심 내용 추출 (원문 기반, 언어 지정)"""
    
    # 언어별 프롬프트 설정
    language_prompts = {
        "english": {
            "prompt": f"""The following is the content of "{title}":
{content}

Please summarize the core essence of this content in 2-3 concise sentences.
Do not use headers or markdown formatting in your response.""",
            "system": f"Text analysis expert. Provide a concise and clear summary of the core content of {title} in English."
        },
        "korean": {
            "prompt": f"""다음은 "{title}"의 내용입니다:
{content}

이 내용의 핵심을 2-3문장으로 간결하게 요약해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"텍스트 분석 전문가. {title}의 핵심 내용을 한국어로 간결하고 명확하게 요약하세요."
        },
        "mixed": {
            "prompt": f"""다음은 "{title}"의 내용입니다:
{content}

이 내용의 핵심을 2-3문장으로 간결하게 요약해주세요. 원문이 영어라면 영어로, 한국어라면 한국어로 응답해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"텍스트 분석 전문가. {title}의 핵심 내용을 원문 언어에 맞게 간결하고 명확하게 요약하세요."
        }
    }
    
    # 언어가 지원되지 않으면 영어 기본값 사용
    lang_config = language_prompts.get(language, language_prompts["english"])
    
    try:
        messages = []
        async for message in query(
            prompt=lang_config["prompt"],
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt=lang_config["system"],
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        if messages:
            # Handle different message formats - check for result attribute first
            last_message = messages[-1]
            if hasattr(last_message, 'result') and last_message.result:
                return last_message.result.strip()
            elif hasattr(last_message, 'text'):
                return last_message.text.strip()
            elif hasattr(last_message, 'content'):
                if isinstance(last_message.content, list):
                    content = ""
                    for block in last_message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                    return content.strip()
                else:
                    return str(last_message.content).strip()
            else:
                return str(last_message).strip()
        else:
            return ""
            
    except Exception as e:
        print(f"❌ 핵심 내용 추출 중 오류: {e}")
        return ""


async def _extract_detailed_content(content: str, core_content: str, title: str, language: str) -> str:
    """상세 핵심 내용 추출 (300단어 이내, 언어 지정)"""
    
    # 언어별 프롬프트 설정
    language_prompts = {
        "english": {
            "prompt": f"""Based on the core summary: "{core_content}"
And the original content of "{title}":
{content}

Please provide a detailed analysis in 300 words or less that expands on the core summary.
Focus on key insights, important details, and actionable information.
Do not use headers or markdown formatting in your response.""",
            "system": f"Content analysis expert. Provide detailed insights about {title} in English within 300 words."
        },
        "korean": {
            "prompt": f"""핵심 요약을 바탕으로: "{core_content}"
그리고 "{title}"의 원본 내용:
{content}

핵심 요약을 확장하여 300단어 이내로 상세 분석을 제공해주세요.
주요 통찰, 중요한 세부사항, 실행 가능한 정보에 집중해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"내용 분석 전문가. {title}에 대한 상세한 통찰을 한국어로 300단어 이내로 제공하세요."
        },
        "mixed": {
            "prompt": f"""핵심 요약을 바탕으로: "{core_content}"
그리고 "{title}"의 원본 내용:
{content}

핵심 요약을 확장하여 300단어 이내로 상세 분석을 제공해주세요. 원문이 영어라면 영어로, 한국어라면 한국어로 응답해주세요.
주요 통찰, 중요한 세부사항, 실행 가능한 정보에 집중해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"내용 분석 전문가. {title}에 대한 상세한 통찰을 원문 언어에 맞게 300단어 이내로 제공하세요."
        }
    }
    
    # 언어가 지원되지 않으면 영어 기본값 사용
    lang_config = language_prompts.get(language, language_prompts["english"])
    
    try:
        messages = []
        async for message in query(
            prompt=lang_config["prompt"],
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt=lang_config["system"],
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        if messages:
            # Handle different message formats - check for result attribute first
            last_message = messages[-1]
            if hasattr(last_message, 'result') and last_message.result:
                return last_message.result.strip()
            elif hasattr(last_message, 'text'):
                return last_message.text.strip()
            elif hasattr(last_message, 'content'):
                if isinstance(last_message.content, list):
                    content = ""
                    for block in last_message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                    return content.strip()
                else:
                    return str(last_message.content).strip()
            else:
                return str(last_message).strip()
        else:
            return ""
            
    except Exception as e:
        print(f"❌ 상세 핵심 내용 추출 중 오류: {e}")
        return ""


async def _extract_main_topics(content: str, title: str, language: str) -> str:
    """주요 화제 추출 (언어 지정)"""
    
    # 언어별 프롬프트 설정
    language_prompts = {
        "english": {
            "prompt": f"""From the content of "{title}":
{content}

Please extract 3-5 main topics or themes discussed in this content.
Present them as a bulleted list with brief explanations.
Do not use headers or markdown formatting in your response.""",
            "system": f"Topic extraction expert. Identify the main themes and topics from {title} in English."
        },
        "korean": {
            "prompt": f""""{title}"의 내용에서:
{content}

이 내용에서 다루어지는 3-5개의 주요 화제나 주제를 추출해주세요.
간단한 설명과 함께 목록 형태로 제시해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"주제 추출 전문가. {title}에서 주요 테마와 주제를 한국어로 식별하세요."
        },
        "mixed": {
            "prompt": f""""{title}"의 내용에서:
{content}

이 내용에서 다루어지는 3-5개의 주요 화제나 주제를 추출해주세요. 원문이 영어라면 영어로, 한국어라면 한국어로 응답해주세요.
간단한 설명과 함께 목록 형태로 제시해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"주제 추출 전문가. {title}에서 주요 테마와 주제를 원문 언어에 맞게 식별하세요."
        }
    }
    
    # 언어가 지원되지 않으면 영어 기본값 사용
    lang_config = language_prompts.get(language, language_prompts["english"])
    
    try:
        messages = []
        async for message in query(
            prompt=lang_config["prompt"],
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt=lang_config["system"],
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        if messages:
            # Handle different message formats - check for result attribute first
            last_message = messages[-1]
            if hasattr(last_message, 'result') and last_message.result:
                return last_message.result.strip()
            elif hasattr(last_message, 'text'):
                return last_message.text.strip()
            elif hasattr(last_message, 'content'):
                if isinstance(last_message.content, list):
                    content = ""
                    for block in last_message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                    return content.strip()
                else:
                    return str(last_message.content).strip()
            else:
                return str(last_message).strip()
        else:
            return ""
            
    except Exception as e:
        print(f"❌ 주요 화제 추출 중 오류: {e}")
        return ""


async def _extract_sub_topics(content: str, title: str, language: str) -> str:
    """부차 화제 추출 (언어 지정)"""
    
    # 언어별 프롬프트 설정
    language_prompts = {
        "english": {
            "prompt": f"""From the content of "{title}":
{content}

Please extract 3-5 secondary topics, subtopics, or supporting details that complement the main themes.
Present them as a bulleted list with brief explanations.
Do not use headers or markdown formatting in your response.""",
            "system": f"Subtopic extraction expert. Identify secondary themes and supporting details from {title} in English."
        },
        "korean": {
            "prompt": f""""{title}"의 내용에서:
{content}

주요 테마를 보완하는 3-5개의 부차적 주제, 세부 주제, 또는 지원 세부사항을 추출해주세요.
간단한 설명과 함께 목록 형태로 제시해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"부주제 추출 전문가. {title}에서 부차적 테마와 지원 세부사항을 한국어로 식별하세요."
        },
        "mixed": {
            "prompt": f""""{title}"의 내용에서:
{content}

주요 테마를 보완하는 3-5개의 부차적 주제, 세부 주제, 또는 지원 세부사항을 추출해주세요. 원문이 영어라면 영어로, 한국어라면 한국어로 응답해주세요.
간단한 설명과 함께 목록 형태로 제시해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요.""",
            "system": f"부주제 추출 전문가. {title}에서 부차적 테마와 지원 세부사항을 원문 언어에 맞게 식별하세요."
        }
    }
    
    # 언어가 지원되지 않으면 영어 기본값 사용
    lang_config = language_prompts.get(language, language_prompts["english"])
    
    try:
        messages = []
        async for message in query(
            prompt=lang_config["prompt"],
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt=lang_config["system"],
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        if messages:
            # Handle different message formats - check for result attribute first
            last_message = messages[-1]
            if hasattr(last_message, 'result') and last_message.result:
                return last_message.result.strip()
            elif hasattr(last_message, 'text'):
                return last_message.text.strip()
            elif hasattr(last_message, 'content'):
                if isinstance(last_message.content, list):
                    content = ""
                    for block in last_message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                    return content.strip()
                else:
                    return str(last_message.content).strip()
            else:
                return str(last_message).strip()
        else:
            return ""
            
    except Exception as e:
        print(f"❌ 부차 화제 추출 중 오류: {e}")
        return ""


def update_extraction_section(info_file: str, extracted_data: Dict[str, str]) -> bool:
    """추출 섹션에 결과 삽입"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        extraction_start = -1
        extraction_end = len(lines)
        
        # '# 추출' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 추출':
                extraction_start = i
                break
        
        if extraction_start == -1:
            print(f"⚠️ '# 추출' 섹션을 찾을 수 없음")
            return False
        
        # 다음 섹션 찾기
        for i in range(extraction_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 추출':
                extraction_end = i
                break
        
        # 추출 섹션 재구성
        new_extraction_lines = ['# 추출', '---']
        
        for key, value in extracted_data.items():
            new_extraction_lines.append(f"## {key}")
            new_extraction_lines.append(value)
            new_extraction_lines.append("")
        
        # 파일 재구성
        new_lines = (
            lines[:extraction_start] +
            new_extraction_lines +
            lines[extraction_end:]
        )
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"❌ 추출 섹션 업데이트 실패: {e}")
        return False


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='노드 정보 문서에서 핵심 정보를 추출하여 추출 섹션에 삽입 (언어 지정 지원)')
    parser.add_argument('info_file', help='처리할 정보 파일 경로')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.info_file):
        print(f"❌ 파일을 찾을 수 없습니다: {args.info_file}")
        return
    
    print(f"🚀 노드 분석 시작: {os.path.basename(args.info_file)}")
    
    # 문서 언어 감지
    language = get_document_language(args.info_file)
    print(f"🌍 감지된 언어: {language}")
    
    # 내용 섹션 추출
    content = extract_content_section(args.info_file)
    if not content:
        print("❌ 내용 섹션이 비어있거나 추출할 수 없습니다.")
        return
    
    print(f"📄 내용 길이: {len(content)} 문자")
    
    # 제목 추출
    title = os.path.basename(args.info_file).replace('_info.md', '').replace('_', ' ')
    
    async def run_extraction():
        # 병렬 추출 실행
        extracted_data = await extract_content_parallel(content, title, language)
        
        if not extracted_data:
            print("❌ 추출된 데이터가 없습니다.")
            return
        
        # 추출 섹션 업데이트
        if update_extraction_section(args.info_file, extracted_data):
            print("✅ 추출 섹션 업데이트 완료")
            
            # 결과 요약
            print("\n📊 추출 결과:")
            for key, value in extracted_data.items():
                preview = value[:100] + "..." if len(value) > 100 else value
                print(f"  - {key}: {preview}")
        else:
            print("❌ 추출 섹션 업데이트 실패")
    
    # 비동기 실행
    asyncio.run(run_extraction())


if __name__ == "__main__":
    main()