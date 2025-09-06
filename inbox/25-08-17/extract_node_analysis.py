# 생성 시간: 2025-08-17 22:45:30 KST
# 핵심 내용: 노드 정보 문서에서 Claude SDK로 핵심 정보를 병렬 추출하여 추출 섹션에 삽입하는 스크립트
# 상세 내용:
#   - extract_content_section 함수 (라인 22-55): 정보 파일에서 내용 섹션 추출
#   - _extract_core_and_detailed_content 함수 (라인 58-88): 핵심 내용 → 상세 핵심 내용 순차 추출
#   - _extract_main_topics_task 함수 (라인 91-105): 주요 화제 추출 작업
#   - _extract_sub_topics_task 함수 (라인 108-122): 부차 화제 추출 작업
#   - extract_content_parallel 함수 (라인 125-170): 3개 작업을 병렬 처리
#   - update_extraction_section 함수 (라인 268-325): 추출 섹션에 결과 삽입
#   - main 함수 (라인 328-380): 메인 실행 함수
# 상태: 활성
# 주소: extract_node_analysis
# 참조: extract_node_analysis_sdk_v3 (일반적인 노드 정보 문서 처리용으로 확장)

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
            line_stripped = lines[i].strip()
            if line_stripped in structure_sections:
                content_end = i
                break
        
        if content_start == -1:
            return ""
        
        # 실제 텍스트가 있는지 확인
        section_content = '\n'.join(lines[content_start:content_end])
        has_actual_text = any(line.strip() and not line.strip() == '---' for line in lines[content_start:content_end])
        
        if not has_actual_text:
            return ""
        
        return section_content.strip()
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""


async def _extract_core_and_detailed_content(content: str, title: str) -> Dict[str, str]:
    """핵심 내용과 상세 핵심 내용을 순차적으로 추출하는 독립 작업"""
    result = {}
    
    # 1. 핵심 내용 추출 (원문 기반)
    core_content = await _extract_core_content(content, title)
    if core_content and len(core_content.strip()) >= 10:
        result["핵심 내용"] = core_content
    else:
        core_content = f"❌ 핵심 내용 추출 실패: Claude API 응답 부족"
        result["핵심 내용"] = core_content
    
    # 2. 상세 핵심 내용 추출 (추출된 핵심 내용 + 원문 기반, 300단어 이내)
    if not core_content.startswith("❌"):
        detailed_content = await _extract_detailed_content(content, core_content, title)
        if detailed_content and len(detailed_content.strip()) >= 10:
            result["상세 핵심 내용"] = detailed_content
        else:
            result["상세 핵심 내용"] = f"❌ 상세 핵심 내용 추출 실패: Claude API 응답 부족"
    else:
        result["상세 핵심 내용"] = "❌ 핵심 내용 추출 실패로 인한 상세 내용 추출 불가"
    
    return result


async def _extract_main_topics_task(content: str, title: str) -> Dict[str, str]:
    """주요 화제 추출 독립 작업"""
    result = {}
    
    main_topics = await _extract_main_topics(content, title)
    if main_topics and len(main_topics.strip()) >= 10:
        result["주요 화제"] = main_topics
    else:
        result["주요 화제"] = f"❌ 주요 화제 추출 실패: Claude API 응답 부족"
    
    return result


async def _extract_sub_topics_task(content: str, title: str) -> Dict[str, str]:
    """부차 화제 추출 독립 작업"""
    result = {}
    
    sub_topics = await _extract_sub_topics(content, title)
    if sub_topics and len(sub_topics.strip()) >= 10:
        result["부차 화제"] = sub_topics
    else:
        result["부차 화제"] = f"❌ 부차 화제 추출 실패: Claude API 응답 부족"
    
    return result


async def extract_content_parallel(content: str, title: str) -> Dict[str, str]:
    """Claude SDK를 이용해 3개 작업을 병렬 처리 (내용추출, 주요화제, 부차화제)"""
    print(f"🚀 노드 병렬 분석 시작: {title}")
    start_time = time.time()
    
    print("📝 3개 작업 병렬 처리 시작...")
    print("   🔧 작업1: 내용 추출 (핵심→상세핵심 순차)")
    print("   🔧 작업2: 주요 화제 추출")
    print("   🔧 작업3: 부차 화제 추출")
    
    # 3개 독립 작업을 병렬로 실행
    tasks = [
        _extract_core_and_detailed_content(content, title),  # 작업1: 내용 추출
        _extract_main_topics_task(content, title),           # 작업2: 주요 화제
        _extract_sub_topics_task(content, title)             # 작업3: 부차 화제
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 결과 통합
    analysis_result = {}
    
    # 작업1 결과 (내용 추출)
    if not isinstance(results[0], Exception):
        analysis_result.update(results[0])
        core_len = len(results[0].get("핵심 내용", ""))
        detailed_len = len(results[0].get("상세 핵심 내용", ""))
        print(f"   ✅ 작업1 완료: 핵심({core_len}자), 상세핵심({detailed_len}자)")
    else:
        print(f"   ❌ 작업1 실패: {results[0]}")
        analysis_result["핵심 내용"] = "❌ 시스템 오류로 추출 실패"
        analysis_result["상세 핵심 내용"] = "❌ 시스템 오류로 추출 실패"
    
    # 작업2 결과 (주요 화제)
    if not isinstance(results[1], Exception):
        analysis_result.update(results[1])
        main_len = len(results[1].get("주요 화제", ""))
        print(f"   ✅ 작업2 완료: 주요화제({main_len}자)")
    else:
        print(f"   ❌ 작업2 실패: {results[1]}")
        analysis_result["주요 화제"] = "❌ 시스템 오류로 추출 실패"
    
    # 작업3 결과 (부차 화제)
    if not isinstance(results[2], Exception):
        analysis_result.update(results[2])
        sub_len = len(results[2].get("부차 화제", ""))
        print(f"   ✅ 작업3 완료: 부차화제({sub_len}자)")
    else:
        print(f"   ❌ 작업3 실패: {results[2]}")
        analysis_result["부차 화제"] = "❌ 시스템 오류로 추출 실패"
    
    total_duration = time.time() - start_time
    success_count = sum(1 for v in analysis_result.values() if v and not v.startswith("❌"))
    print(f"📊 병렬 분석 완료: {success_count}/4 섹션 성공")
    print(f"⏱️ 총 소요시간: {total_duration:.2f}초 (3개 작업 병렬 처리)")
    
    return analysis_result


async def _extract_core_content(content: str, title: str) -> str:
    """핵심 내용 추출 (원문 기반)"""
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
        
        return _extract_content_from_messages(messages)
        
    except Exception as e:
        print(f"❌ 핵심 내용 추출 중 오류: {e}")
        return f"추출 실패: {str(e)}"


async def _extract_detailed_content(content: str, core_content: str, title: str) -> str:
    """상세 핵심 내용 추출 (추출된 핵심 내용 + 원문 기반, 300단어 이내)"""
    prompt = f"""다음은 "{title}"의 원문 내용입니다:

{content}

그리고 이미 추출된 핵심 내용은 다음과 같습니다:
{core_content}

위의 핵심 내용을 바탕으로, 원문을 참조하여 300단어 이내로 자세히 부연 설명해주세요.
핵심 내용에 언급된 주요 개념들을 원문의 구체적인 내용으로 뒷받침하여 상세히 설명하되,
300단어를 초과하지 않도록 간결하면서도 포괄적으로 정리해주세요.
응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt=f"텍스트 분석 전문가. {title}의 핵심 내용을 300단어 이내로 자세히 부연 설명하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        return _extract_content_from_messages(messages)
        
    except Exception as e:
        print(f"❌ 상세 핵심 내용 추출 중 오류: {e}")
        return f"추출 실패: {str(e)}"


async def _extract_main_topics(content: str, title: str) -> str:
    """주요 화제 추출"""
    prompt = f"""다음은 "{title}"의 내용입니다:

{content}

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용을 한 문장으로 설명
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용을 한 문장으로 설명

각 항목은 한 줄에 하나씩, 반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
    
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
        
        return _extract_content_from_messages(messages)
        
    except Exception as e:
        print(f"❌ 주요 화제 추출 중 오류: {e}")
        return f"추출 실패: {str(e)}"


async def _extract_sub_topics(content: str, title: str) -> str:
    """부차 화제 추출"""
    prompt = f"""다음은 "{title}"의 내용입니다:

{content}

부차 화제는 주요 화제를 뒷받침하거나 보완하는 세부 내용들입니다.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용을 한 문장으로 설명
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용을 한 문장으로 설명

각 항목은 한 줄에 하나씩, 반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
    
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
        
        return _extract_content_from_messages(messages)
        
    except Exception as e:
        print(f"❌ 부차 화제 추출 중 오류: {e}")
        return f"추출 실패: {str(e)}"


def _extract_content_from_messages(messages: List) -> str:
    """메시지에서 텍스트 내용 추출"""
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


def update_extraction_section(info_file: str, analysis_result: Dict[str, str]) -> bool:
    """정보 파일의 추출 섹션 업데이트 (구분선 포함)"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        extraction_start = -1
        
        # '# 추출' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 추출':
                extraction_start = i
                break
        
        if extraction_start == -1:
            print(f"⚠️ '# 추출' 섹션을 찾을 수 없음: {os.path.basename(info_file)}")
            return False
        
        # 다음 # 섹션 찾기
        extraction_end = -1
        for i in range(extraction_start + 1, len(lines)):
            if lines[i].strip().startswith('# '):
                extraction_end = i
                break
        
        # 추출 결과 포맷 (구분선 포함)
        extraction_content = "---\n"  # 구분선 추가
        section_order = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        
        success_count = 0
        for section_name in section_order:
            if (section_name in analysis_result and 
                analysis_result[section_name] and 
                not analysis_result[section_name].startswith("❌") and
                len(analysis_result[section_name].strip()) >= 10):
                extraction_content += f"## {section_name}\n{analysis_result[section_name]}\n\n"
                success_count += 1
        
        # 새로운 내용으로 교체
        new_lines = lines[:extraction_start + 1]
        new_lines.extend(extraction_content.strip().split('\n'))
        
        if extraction_end != -1:
            new_lines.extend([''] + lines[extraction_end:])
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"📊 추출 섹션 업데이트: {success_count}/4 섹션 성공")
        print(f"✅ 추출 섹션 업데이트 완료: {os.path.basename(info_file)}")
        return True
        
    except Exception as e:
        print(f"❌ 파일 업데이트 실패: {e}")
        return False


def update_process_status(info_file: str, status: bool) -> bool:
    """process_status 필드 업데이트"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # process_status 라인 찾고 업데이트
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('process_status:'):
                lines[i] = f'process_status: {str(status).lower()}'
                break
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"📝 process_status를 {status}로 업데이트")
        return True
        
    except Exception as e:
        print(f"❌ process_status 업데이트 실패: {e}")
        return False


async def process_single_file(info_file: str) -> bool:
    """단일 노드 정보 파일 처리"""
    # 파일 존재 확인
    if not os.path.exists(info_file):
        print(f"❌ 정보 파일을 찾을 수 없습니다: {info_file}")
        return False
    
    print(f"📄 처리 중: {os.path.basename(info_file)}")
    
    # 1. 내용 섹션 추출
    content_section = extract_content_section(info_file)
    if not content_section:
        print(f"⚠️ 내용 섹션이 비어있음: {info_file}")
        return False
    
    print(f"📝 내용 길이: {len(content_section)} 문자")
    
    # 2. 병렬 분석 실행 (핵심+상세핵심 순차, 주요+부차 병렬)
    title = os.path.basename(info_file).replace('_info.md', '').replace('_', ' ').title()
    analysis_result = await extract_content_parallel(content_section, title)
    
    # 3. 추출 섹션 업데이트
    if update_extraction_section(info_file, analysis_result):
        # 4. 모든 섹션이 성공적으로 추출되었는지 확인
        success_count = sum(1 for v in analysis_result.values() if v and not v.startswith("❌"))
        all_sections_success = success_count == 4
        
        # process_status 업데이트
        update_process_status(info_file, all_sections_success)
        
        if all_sections_success:
            print(f"✅ {os.path.basename(info_file)} 완전 처리 완료 (모든 섹션 성공)")
        else:
            print(f"⚠️ {os.path.basename(info_file)} 부분 처리 완료 ({success_count}/4 섹션 성공)")
        return True
    else:
        print(f"❌ {os.path.basename(info_file)} 처리 실패")
        return False


async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='노드 정보 문서에서 Claude SDK로 핵심 정보 병렬 추출')
    parser.add_argument('input_path', help='노드 정보 파일 경로 또는 디렉토리 경로')
    
    args = parser.parse_args()
    
    print("🚀 노드 Claude SDK 기반 핵심 정보 병렬 추출 시작")
    print("=" * 60)
    
    input_path = args.input_path
    
    # 경로 존재 확인
    if not os.path.exists(input_path):
        print(f"❌ 경로를 찾을 수 없습니다: {input_path}")
        return
    
    # 단일 파일 처리
    if os.path.isfile(input_path):
        if input_path.endswith('_info.md'):
            await process_single_file(input_path)
        else:
            print(f"⚠️ '_info.md'로 끝나는 파일이 아닙니다: {input_path}")
        return
    
    # 디렉토리 처리 - 현재 디렉토리만 검색
    info_files = []
    for file in os.listdir(input_path):
        if file.endswith('_info.md'):
            info_files.append(os.path.join(input_path, file))
    
    if not info_files:
        print(f"❌ '_info.md' 파일을 찾을 수 없습니다: {input_path}")
        return
    
    print(f"📁 총 {len(info_files)}개 파일 발견")
    
    # 모든 파일 처리
    success_count = 0
    for info_file in info_files:
        print(f"\n{'='*40}")
        if await process_single_file(info_file):
            success_count += 1
    
    print(f"\n✅ 노드 분석 완료!")
    print(f"📈 처리 결과: {success_count}/{len(info_files)} 파일 성공")


if __name__ == "__main__":
    asyncio.run(main())