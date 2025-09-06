"""
생성 시간: 2025-08-11 한국 시간 
핵심 내용: 개선된 각 섹션의 추가 정보를 결합하여 상위 섹션(7_Basic_data_validation_info.md) 업데이트
상세 내용:
    - collect_all_section_infos(): 개선된 모든 섹션 추가 정보 수집
    - combine_section_contents(): 수집된 섹션 정보들을 하나로 결합
    - enhance_upper_section_with_combined(): 결합된 정보를 바탕으로 상위 섹션 개선
    - update_topics_comprehensively(): 주요/부차 화제를 모든 섹션 + 전체 관점 내용으로 업데이트
    - 기존 상위 섹션 백업 후 업데이트 수행
상태: 활성
주소: upper_section_enhancer
참조: section_info_enhancer (각 섹션 개선 스크립트)
"""

import asyncio
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions

def collect_all_section_infos():
    """개선된 모든 섹션의 추가 정보를 순서대로 수집"""
    
    sections_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections")
    
    section_files = [
        ("7_Introduction", sections_dir / "7_Introduction_info.md"),
        ("7.1_Data_validation_in_DOP", sections_dir / "7.1_Data_validation_in_DOP_info.md"),
        ("7.2_JSON_Schema_in_a_nutshell", sections_dir / "7.2_JSON_Schema_in_a_nutshell_info_v2.md"), 
        ("7.3_Schema_flexibility_and_strictness", sections_dir / "7.3_Schema_flexibility_and_strictness_info.md"),
        ("7.4_Schema_composition", sections_dir / "7.4_Schema_composition_info.md"),
        ("7.5_Details_about_data_validation_failures", sections_dir / "7.5_Details_about_data_validation_failures_info.md"),
        ("Summary", sections_dir / "Summary_info.md")
    ]
    
    collected_sections = {}
    
    print("📂 각 섹션의 개선된 추가 정보 수집 중...")
    
    for section_name, file_path in section_files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            collected_sections[section_name] = content
            print(f"    ✅ {section_name}: {len(content)} 문자")
        else:
            print(f"    ❌ {section_name}: 파일 없음")
    
    return collected_sections

def combine_section_contents(collected_sections):
    """수집된 섹션 정보들을 하나로 결합"""
    
    combined_content = "# 7장 모든 섹션의 개선된 추가 정보 결합\n\n"
    
    for section_name, content in collected_sections.items():
        combined_content += f"## ========== {section_name} ==========\n\n"
        combined_content += content + "\n\n"
        combined_content += "=" * 100 + "\n\n"
    
    print(f"📋 섹션 정보들 결합 완료: {len(combined_content)} 문자")
    return combined_content

async def enhance_core_content(combined_sections_content, original_upper_content):
    """상위 섹션의 핵심 내용을 결합된 섹션 정보로 개선"""
    
    prompt = f"""다음은 개선된 7장의 모든 섹션 추가 정보들을 결합한 내용입니다:

{combined_sections_content}

그리고 다음은 기존 상위 섹션(7_Basic_data_validation_info.md)의 내용입니다:

{original_upper_content}

**작업 요청:**
기존 상위 섹션의 핵심 내용을 **주된 내용으로 유지**하면서, 각 구성 요소의 핵심을 반영하여 **보다 통합적인 관점**으로 개선해주세요.

**중요한 원칙:**
1. 기존 상위 섹션의 핵심 내용이 주가 되어야 함
2. 각 섹션의 개선된 정보들을 통합적으로 활용
3. 7장 전체의 구성 요소들을 아우르는 통합적 관점 반영
4. 2-3문장으로 간결하게 작성
5. 응답에 '핵심 내용'이라는 헤더는 포함하지 마세요

개선된 핵심 내용만 작성해주세요:"""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 기존 상위 섹션 내용을 주로 유지하면서 각 구성 요소의 핵심을 반영하여 통합적 관점으로 개선하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
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
        
    except Exception as e:
        print(f"핵심 내용 개선 중 오류 발생: {e}")
        return None

async def enhance_detailed_content(combined_sections_content, original_upper_content):
    """상위 섹션의 상세 핵심 내용을 결합된 섹션 정보로 개선"""
    
    prompt = f"""다음은 개선된 7장의 모든 섹션 추가 정보들을 결합한 내용입니다:

{combined_sections_content}

그리고 다음은 기존 상위 섹션(7_Basic_data_validation_info.md)의 내용입니다:

{original_upper_content}

**작업 요청:**
기존 상위 섹션의 상세 핵심 내용을 **주된 내용으로 유지**하면서, 각 구성 요소의 핵심을 반영하여 **보다 통합적인 관점**으로 개선해주세요.

**중요한 원칙:**
1. 기존 상위 섹션의 상세 핵심 내용이 주가 되어야 함
2. 각 섹션의 개선된 정보들을 통합적으로 활용
3. 7장 전체의 구조와 흐름을 반영한 포괄적 설명
4. 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요
5. 헤더 사용 시 ### 3레벨부터 사용

개선된 상세 핵심 내용만 작성해주세요:"""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 기존 상위 섹션의 상세 내용을 주로 유지하면서 각 구성 요소의 핵심을 반영하여 통합적 관점으로 개선하세요. 헤더는 ### 레벨부터 사용하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
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
        
    except Exception as e:
        print(f"상세 핵심 내용 개선 중 오류 발생: {e}")
        return None

async def enhance_main_topics(combined_sections_content):
    """모든 섹션의 주요 화제 + 전체적 관점에서 추가된 주요 화제"""
    
    prompt = f"""다음은 개선된 7장의 모든 섹션 추가 정보들을 결합한 내용입니다:

{combined_sections_content}

**작업 요청:**
각 섹션의 주요 화제들을 **모두 포함**하되, 출처를 다음과 같이 표시:
- 대부분은 구체적인 섹션명으로 표시 (예: [출처: 7_Introduction])
- 일부 화제는 전체적 관점에서 통합된 것으로 표시 (예: [출처: 전체 관점])

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 7_Introduction]
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 전체 관점]

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 각 섹션의 주요 화제를 모두 포함하면서 전체적 관점에서 추가 화제를 식별하여 종합적으로 정리하되, 반드시 각 화제의 출처 섹션을 표시하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
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
        
    except Exception as e:
        print(f"주요 화제 개선 중 오류 발생: {e}")
        return None

async def enhance_sub_topics(combined_sections_content):
    """모든 섹션의 부차 화제 + 전체적 관점에서 추가된 부차 화제"""
    
    prompt = f"""다음은 개선된 7장의 모든 섹션 추가 정보들을 결합한 내용입니다:

{combined_sections_content}

**작업 요청:**
각 섹션의 부차 화제들을 **모두 포함**하되, 출처를 다음과 같이 표시:
- 대부분은 구체적인 섹션명으로 표시 (예: [출처: 7_Introduction])
- 일부 화제는 전체적 관점에서 통합된 것으로 표시 (예: [출처: 전체 관점])

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 7_Introduction]
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 전체 관점]

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 각 섹션의 부차 화제를 모두 포함하면서 전체적 관점에서 추가 화제를 식별하여 종합적으로 정리하되, 반드시 각 화제의 출처 섹션을 표시하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
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
        
    except Exception as e:
        print(f"부차 화제 개선 중 오류 발생: {e}")
        return None

def update_section(file_path, header, content):
    """파일의 특정 헤더 섹션에 내용 업데이트"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    header_pattern = f"## {header}"
    header_start = text.find(header_pattern)
    
    if header_start == -1:
        print(f"헤더를 찾을 수 없습니다: {header}")
        return False
    
    content_start = header_start + len(header_pattern)
    next_header_start = text.find("\n## ", content_start)
    
    if next_header_start == -1:
        new_text = text[:content_start] + f"\n{content}\n"
    else:
        new_text = text[:content_start] + f"\n{content}\n" + text[next_header_start:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    
    print(f"    ✅ '{header}' 섹션 업데이트 완료")
    return True

async def main():
    """메인 실행 함수"""
    
    print("=" * 60)
    print("상위 섹션(7_Basic_data_validation_info.md) 업데이트 시작")
    print("각 섹션의 개선된 정보를 결합하여 통합적 관점에서 개선")
    print("=" * 60)
    
    # 1. 각 섹션의 개선된 추가 정보 수집
    collected_sections = collect_all_section_infos()
    
    if not collected_sections:
        print("❌ 수집된 섹션 정보가 없습니다.")
        return
    
    # 2. 섹션 정보들 결합
    combined_content = combine_section_contents(collected_sections)
    
    # 3. 기존 상위 섹션 내용 읽기
    upper_section_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections/7_Basic_data_validation_info.md")
    
    if not upper_section_path.exists():
        print(f"❌ 상위 섹션 파일을 찾을 수 없습니다: {upper_section_path}")
        return
    
    with open(upper_section_path, 'r', encoding='utf-8') as f:
        original_upper_content = f.read()
    
    print(f"📄 기존 상위 섹션 내용 로드: {len(original_upper_content)} 문자")
    
    # 4. 핵심 내용, 상세 내용, 주요/부차 화제를 병렬로 개선
    print(f"\n🔄 상위 섹션 4개 영역 병렬 개선 중...")
    
    tasks = [
        enhance_core_content(combined_content, original_upper_content),
        enhance_detailed_content(combined_content, original_upper_content),
        enhance_main_topics(combined_content),
        enhance_sub_topics(combined_content)
    ]
    
    enhanced_core, enhanced_detailed, enhanced_main_topics, enhanced_sub_topics = await asyncio.gather(*tasks)
    
    # 5. 개선된 내용들을 파일에 업데이트
    print(f"\n📝 상위 섹션 파일 업데이트 중...")
    
    success_count = 0
    
    if enhanced_core:
        update_section(upper_section_path, "핵심 내용", enhanced_core)
        success_count += 1
    else:
        print(f"    ❌ 핵심 내용 개선 실패")
    
    if enhanced_detailed:
        update_section(upper_section_path, "상세 핵심 내용", enhanced_detailed)
        success_count += 1
    else:
        print(f"    ❌ 상세 핵심 내용 개선 실패")
    
    if enhanced_main_topics:
        update_section(upper_section_path, "주요 화제", enhanced_main_topics)
        success_count += 1
    else:
        print(f"    ❌ 주요 화제 개선 실패")
    
    if enhanced_sub_topics:
        update_section(upper_section_path, "부차 화제", enhanced_sub_topics)
        success_count += 1
    else:
        print(f"    ❌ 부차 화제 개선 실패")
    
    # 6. 완료 메시지
    print(f"\n{'=' * 60}")
    print(f"상위 섹션 업데이트 완료!")
    print(f"성공한 섹션: {success_count}/4")
    print(f"업데이트된 파일: {upper_section_path}")
    print(f"{'=' * 60}")
    
    print(f"\n📋 적용된 개선 원칙:")
    print(f"  ✅ 기존 상위 섹션 내용을 주로 유지")
    print(f"  ✅ 각 구성 요소의 핵심을 반영하여 통합적 관점으로 개선")
    print(f"  ✅ 주요/부차 화제는 모든 섹션 포함 + 전체 관점 추가")

if __name__ == "__main__":
    asyncio.run(main())