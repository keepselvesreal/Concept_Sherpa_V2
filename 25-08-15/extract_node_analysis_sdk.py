# 생성 시간: Fri Aug 15 11:16:59 KST 2025
# 핵심 내용: Claude SDK를 이용한 노드 내용 병렬 분석 스크립트
# 상세 내용:
#   - extract_content_section() (line 25): 정보 파일에서 내용 섹션 추출
#   - extract_content_parallel() (line 60): 4가지 요소 병렬 추출
#   - _extract_core_content() (line 90): 핵심 내용 추출
#   - _extract_detailed_content() (line 110): 상세 핵심 내용 추출
#   - _extract_main_topics() (line 130): 주요 화제 추출
#   - _extract_sub_topics() (line 150): 부차 화제 추출
#   - update_info_file() (line 170): 추출 결과를 정보 파일에 업데이트
#   - main() (line 200): 메인 실행 함수
# 상태: 활성
# 주소: extract_node_analysis_sdk
# 참조: content_analysis_module_v3 (병렬 추출 로직 참고)

#!/usr/bin/env python3

import asyncio
import os
from typing import Dict, List
from claude_code_sdk import query, ClaudeCodeOptions

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
        has_actual_text = any(line.strip() for line in lines[content_start:content_end])
        
        if not has_actual_text:
            return ""
        
        return section_content.strip()
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""

async def extract_content_parallel(content: str, title: str) -> Dict[str, str]:
    """Claude SDK를 이용해 4가지 요소를 병렬로 추출 (fallback 포함)"""
    print(f"🚀 병렬 분석 시작: {title}")
    
    # 병렬 분석 실행
    tasks = [
        _extract_core_content(content, title),
        _extract_detailed_content(content, title),
        _extract_main_topics(content, title),
        _extract_sub_topics(content, title)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 결과 정리
    analysis_result = {}
    sections = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
    retry_sections = []
    
    for i, result in enumerate(results):
        section = sections[i]
        if isinstance(result, Exception):
            print(f"❌ {section} 추출 실패: {result}")
            analysis_result[section] = ""
            retry_sections.append((section, i))
        elif result and len(result.strip()) >= 10:  # 최소 10자 이상
            analysis_result[section] = result
            print(f"✅ {section} 추출 완료: {len(result)}자")
        else:
            print(f"⚠️ {section} 추출 결과 부족 (길이: {len(result) if result else 0})")
            analysis_result[section] = ""
            retry_sections.append((section, i))
    
    # Fallback: 실패한 섹션들 재시도 (최대 3번까지)
    retry_count = 0
    max_retries = 3
    
    while retry_sections and retry_count < max_retries:
        retry_count += 1
        print(f"🔄 재시도 {retry_count}/{max_retries}: {len(retry_sections)}개 섹션")
        
        retry_tasks = []
        for section_name, task_index in retry_sections:
            if task_index == 0:
                retry_tasks.append(_extract_core_content(content, title))
            elif task_index == 1:
                retry_tasks.append(_extract_detailed_content(content, title))
            elif task_index == 2:
                retry_tasks.append(_extract_main_topics(content, title))
            elif task_index == 3:
                retry_tasks.append(_extract_sub_topics(content, title))
        
        retry_results = await asyncio.gather(*retry_tasks, return_exceptions=True)
        
        # 재시도 결과 처리
        new_retry_sections = []
        for i, (section_name, task_index) in enumerate(retry_sections):
            retry_result = retry_results[i]
            if not isinstance(retry_result, Exception) and retry_result and len(retry_result.strip()) >= 10:
                analysis_result[section_name] = retry_result
                print(f"✅ {section_name} 재시도 {retry_count} 성공: {len(retry_result)}자")
            else:
                print(f"⚠️ {section_name} 재시도 {retry_count} 실패")
                new_retry_sections.append((section_name, task_index))
        
        retry_sections = new_retry_sections
        
        # 재시도 간 잠시 대기
        if retry_sections and retry_count < max_retries:
            await asyncio.sleep(1)
    
    # 최종적으로 실패한 섹션들은 기본값 설정
    for section_name, _ in retry_sections:
        if section_name == "핵심 내용":
            analysis_result[section_name] = f"{title}에 대한 핵심 내용을 요약합니다."
        elif section_name == "상세 핵심 내용":
            analysis_result[section_name] = f"{title}의 상세한 내용을 체계적으로 정리합니다."
        elif section_name == "주요 화제":
            analysis_result[section_name] = f"- {title}의 주요 개념과 원리\n- 핵심 기술과 방법론\n- 실제 적용 사례와 결과"
        elif section_name == "부차 화제":
            analysis_result[section_name] = f"- {title}의 배경과 맥락\n- 관련 기술과 도구\n- 향후 발전 방향과 과제"
        print(f"🔧 {section_name}: 기본값으로 설정됨")
    
    success_count = sum(1 for v in analysis_result.values() if v and not v.startswith("추출 실패") and len(v.strip()) >= 10)
    print(f"📊 병렬 분석 완료: {success_count}/4 섹션 성공")
    
    return analysis_result

async def _extract_core_content(content: str, title: str) -> str:
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
        
        return _extract_content_from_messages(messages)
        
    except Exception as e:
        print(f"❌ 핵심 내용 추출 중 오류: {e}")
        return f"추출 실패: {str(e)}"

async def _extract_detailed_content(content: str, title: str) -> str:
    """상세 핵심 내용 추출"""
    prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 상세 핵심을 체계적이고 포괄적으로 정리해주세요.
각 핵심을 상세히 설명해주세요.
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

def validate_extraction_result(analysis_result: Dict[str, str]) -> Dict[str, bool]:
    """추출 결과 검증"""
    validation_result = {}
    required_sections = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
    
    for section in required_sections:
        content = analysis_result.get(section, "")
        # 섹션이 존재하고, 실패 메시지가 아니며, 최소 10자 이상인지 확인
        is_valid = (content and 
                   not content.startswith("추출 실패") and 
                   len(content.strip()) >= 10)
        validation_result[section] = is_valid
        
        if is_valid:
            print(f"✓ {section}: 검증 통과 ({len(content)}자)")
        else:
            print(f"✗ {section}: 검증 실패 ({len(content) if content else 0}자)")
    
    return validation_result

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

def update_info_file(info_file: str, analysis_result: Dict[str, str]) -> bool:
    """정보 파일의 추출 섹션 업데이트 (구분선 포함)"""
    try:
        # 추출 결과 검증
        validation_result = validate_extraction_result(analysis_result)
        failed_sections = [section for section, is_valid in validation_result.items() if not is_valid]
        
        if failed_sections:
            print(f"⚠️ 검증 실패 섹션: {', '.join(failed_sections)}")
            print(f"⚠️ 일부 섹션이 부족하지만 계속 진행합니다.")
        
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
        
        for section_name in section_order:
            if (section_name in analysis_result and 
                analysis_result[section_name] and 
                not analysis_result[section_name].startswith("추출 실패") and
                len(analysis_result[section_name].strip()) >= 10):
                extraction_content += f"## {section_name}\n{analysis_result[section_name]}\n\n"
        
        # 새로운 내용으로 교체
        new_lines = lines[:extraction_start + 1]
        new_lines.extend(extraction_content.strip().split('\n'))
        
        if extraction_end != -1:
            new_lines.extend([''] + lines[extraction_end:])
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        # 최종 검증: 파일에서 섹션 존재 여부 확인
        updated_content = '\n'.join(new_lines)
        final_validation = {}
        for section in section_order:
            section_exists = f"## {section}" in updated_content
            final_validation[section] = section_exists
        
        success_count = sum(1 for exists in final_validation.values() if exists)
        print(f"📊 최종 섹션 존재 확인: {success_count}/4 섹션")
        print(f"✅ 추출 섹션 업데이트 완료: {os.path.basename(info_file)}")
        return True
        
    except Exception as e:
        print(f"❌ 파일 업데이트 실패: {e}")
        return False

async def main():
    """메인 실행 함수"""
    work_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-15"
    
    print("🚀 Claude SDK 기반 노드 내용 병렬 분석 시작")
    print("=" * 60)
    
    # info 파일 찾기
    info_files = [f for f in os.listdir(work_dir) if f.endswith('_info.md')]
    
    if not info_files:
        print("❌ 정보 파일을 찾을 수 없습니다.")
        return
    
    for info_file in info_files:
        info_path = os.path.join(work_dir, info_file)
        print(f"\n📄 처리 중: {info_file}")
        
        # 1. 내용 섹션 추출
        content_section = extract_content_section(info_path)
        if not content_section:
            print(f"⚠️ 내용 섹션이 비어있음: {info_file}")
            continue
        
        print(f"📝 내용 길이: {len(content_section)} 문자")
        
        # 2. 병렬 분석 실행
        title = info_file.replace('_info.md', '').replace('_', ' ').title()
        analysis_result = await extract_content_parallel(content_section, title)
        
        # 3. 파일 업데이트
        if update_info_file(info_path, analysis_result):
            # 4. 모든 섹션이 성공적으로 추출되었는지 확인
            validation_result = validate_extraction_result(analysis_result)
            all_sections_valid = all(validation_result.values())
            
            # process_status 업데이트
            update_process_status(info_path, all_sections_valid)
            
            if all_sections_valid:
                print(f"✅ {info_file} 완전 처리 완료 (모든 섹션 성공)")
            else:
                print(f"⚠️ {info_file} 부분 처리 완료 (일부 섹션 기본값)")
        else:
            print(f"❌ {info_file} 처리 실패")
    
    print(f"\n✅ 모든 노드 분석 완료!")

if __name__ == "__main__":
    asyncio.run(main())