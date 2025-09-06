"""
생성 시간: 2025-08-11 한국 시간 
핵심 내용: 7장 전체 내용을 대상으로 작성된 추가 정보를 바탕으로 각 섹션 info 파일의 핵심 내용과 상세 핵심 내용만 개선 (병렬처리)
상세 내용:
    - load_chapter_comprehensive_info(): 7장 전체 내용을 대상으로 작성된 추가 정보 로드
    - enhance_core_content(section_text, comprehensive_info): 기존 핵심 내용을 전체 대상 정보로 개선
    - enhance_detailed_content(section_text, comprehensive_info): 기존 상세 내용을 전체 대상 정보로 개선  
    - preserve_original_topics(file_path): 주요 화제와 부차 화제는 그대로 유지
    - process_section_file(section_file, comprehensive_info): 개별 섹션 파일 처리
    - process_all_sections(): 모든 섹션 파일을 병렬로 처리
    - 기존 내용 우선, 전체 대상 정보 보완적 추가 원칙 적용
상태: 활성
주소: section_info_enhancer
참조: text_info_processor_v3 (참고 구조)
"""

import asyncio
import sys
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions
import time

def load_chapter_comprehensive_info():
    """7장 전체 내용을 대상으로 작성된 추가 정보 로드"""
    comprehensive_info_file = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections/7_Basic_data_validation_info.md")
    
    if not comprehensive_info_file.exists():
        print(f"❌ 7장 전체 내용 대상 추가 정보 파일을 찾을 수 없습니다: {comprehensive_info_file}")
        return None
    
    with open(comprehensive_info_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✅ 7장 전체 내용을 대상으로 작성된 추가 정보 로드 완료: {len(content)} 문자")
    return content

async def enhance_core_content(section_text, comprehensive_info):
    """기존 핵심 내용을 7장 전체 내용 대상 추가 정보로 개선"""
    prompt = f"""다음은 7장 전체 내용을 대상으로 작성된 추가 정보입니다:

{comprehensive_info}

그리고 다음은 특정 섹션의 기존 추가 정보입니다:

{section_text}

**작업 요청:**
기존 섹션의 핵심 내용을 **주된 내용으로 유지**하면서, 7장 전체 내용을 대상으로 작성된 추가 정보를 **보완적으로 반영**하여 개선해주세요.

**중요한 원칙:**
1. 기존 각 섹션의 핵심 내용이 주가 되어야 함
2. 전체 내용 대상 추가 정보는 보완적으로만 활용
3. 해당 섹션의 고유한 특성과 내용 유지
4. 전체적인 맥락에서 해당 섹션의 위치와 역할 반영
5. 2-3문장으로 간결하게 작성
6. 응답에 '핵심 내용'이라는 헤더는 포함하지 마세요

개선된 핵심 내용만 작성해주세요:"""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 기존 섹션 내용을 주로 유지하면서 전체 내용 대상 추가 정보를 보완적으로 반영하여 개선하세요.",
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

async def enhance_detailed_content(section_text, comprehensive_info):
    """기존 상세 내용을 7장 전체 내용 대상 추가 정보로 개선"""
    prompt = f"""다음은 7장 전체 내용을 대상으로 작성된 추가 정보입니다:

{comprehensive_info}

그리고 다음은 특정 섹션의 기존 추가 정보입니다:

{section_text}

**작업 요청:**
기존 섹션의 상세 핵심 내용을 **주된 내용으로 유지**하면서, 7장 전체 내용을 대상으로 작성된 추가 정보를 **보완적으로 반영**하여 개선해주세요.

**중요한 원칙:**
1. 기존 각 섹션의 상세 핵심 내용이 주가 되어야 함
2. 전체 내용 대상 추가 정보는 맥락적 보완만 제공
3. 해당 섹션의 고유한 특성과 세부 설명 유지
4. 전체적인 관점에서 해당 섹션이 7장 내에서 어떤 역할을 하는지 반영
5. 체계적이고 포괄적으로 정리
6. 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요
7. 헤더 사용 시 ### 3레벨부터 사용

개선된 상세 핵심 내용만 작성해주세요:"""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 기존 섹션의 상세 내용을 주로 유지하면서 전체 내용 대상 추가 정보를 보완적으로 반영하여 개선하세요. 헤더는 ### 레벨부터 사용하세요.",
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
        print(f"상세 내용 개선 중 오류 발생: {e}")
        return None

def preserve_original_topics(file_path):
    """기존 주요 화제와 부차 화제를 추출하여 보존"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 주요 화제 추출
    main_topics_start = content.find("## 주요 화제")
    sub_topics_start = content.find("## 부차 화제")
    
    main_topics = ""
    sub_topics = ""
    
    if main_topics_start != -1:
        if sub_topics_start != -1:
            main_topics = content[main_topics_start:sub_topics_start].replace("## 주요 화제\n", "").strip()
        else:
            main_topics = content[main_topics_start:].replace("## 주요 화제\n", "").strip()
    
    if sub_topics_start != -1:
        sub_topics = content[sub_topics_start:].replace("## 부차 화제\n", "").strip()
    
    return main_topics, sub_topics

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

async def process_section_file(section_file, comprehensive_info):
    """개별 섹션 파일 처리"""
    file_path = Path(section_file)
    print(f"\n📄 처리 중: {file_path.name}")
    print("-" * 50)
    
    # 기존 내용 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        section_content = f.read()
    
    # 기존 주요/부차 화제 보존
    original_main_topics, original_sub_topics = preserve_original_topics(file_path)
    print(f"    📋 기존 주요/부차 화제 보존 완료")
    
    # 핵심 내용과 상세 내용을 병렬로 개선
    print(f"    🔄 핵심 내용 및 상세 핵심 내용 개선 중...")
    
    tasks = [
        enhance_core_content(section_content, comprehensive_info),
        enhance_detailed_content(section_content, comprehensive_info)
    ]
    
    enhanced_core, enhanced_detailed = await asyncio.gather(*tasks)
    
    # 개선된 내용 업데이트
    if enhanced_core:
        update_section(file_path, "핵심 내용", enhanced_core)
    else:
        print(f"    ❌ 핵심 내용 개선 실패")
    
    if enhanced_detailed:
        update_section(file_path, "상세 핵심 내용", enhanced_detailed)
    else:
        print(f"    ❌ 상세 핵심 내용 개선 실패")
    
    # 기존 화제들 복원 (왜곡 방지)
    if original_main_topics:
        update_section(file_path, "주요 화제", original_main_topics)
        print(f"    🔄 주요 화제 복원 완료")
    
    if original_sub_topics:
        update_section(file_path, "부차 화제", original_sub_topics) 
        print(f"    🔄 부차 화제 복원 완료")
    
    print(f"    ✅ {file_path.name} 처리 완료")

async def process_all_sections():
    """모든 섹션 파일을 순차 처리 (내부적으로 병렬)"""
    
    # 1. 7장 전체 내용 대상 추가 정보 로드
    print("=" * 60)
    print("7장 섹션별 info 파일 개선 시작")
    print("기존 섹션 내용 우선 + 전체 대상 정보 보완적 반영")
    print("=" * 60)
    
    comprehensive_info = load_chapter_comprehensive_info()
    if not comprehensive_info:
        return
    
    # 2. 처리할 섹션 파일 목록
    sections_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections")
    
    section_files = [
        sections_dir / "7.1_Data_validation_in_DOP_info.md",
        sections_dir / "7.2_JSON_Schema_in_a_nutshell_info_v2.md", 
        sections_dir / "7.3_Schema_flexibility_and_strictness_info.md",
        sections_dir / "7.4_Schema_composition_info.md",
        sections_dir / "7.5_Details_about_data_validation_failures_info.md",
        sections_dir / "7_Introduction_info.md",
        sections_dir / "Summary_info.md"
    ]
    
    # 존재하는 파일만 필터링
    existing_files = [f for f in section_files if f.exists()]
    
    print(f"처리 대상 파일 {len(existing_files)}개:")
    for f in existing_files:
        print(f"  - {f.name}")
    
    if not existing_files:
        print("❌ 처리할 파일이 없습니다.")
        return
    
    # 3. 각 섹션 순차 처리 (내부적으로 핵심/상세 내용은 병렬)
    print(f"\n{'=' * 30} 개선 작업 시작 {'=' * 30}")
    
    success_count = 0
    for i, section_file in enumerate(existing_files, 1):
        print(f"\n[{i}/{len(existing_files)}]")
        try:
            await process_section_file(section_file, comprehensive_info)
            success_count += 1
        except Exception as e:
            print(f"❌ {section_file.name} 처리 실패: {e}")
    
    # 4. 완료 메시지
    print(f"\n{'=' * 60}")
    print(f"모든 섹션 개선 완료!")
    print(f"성공: {success_count}/{len(existing_files)} 파일")
    print(f"{'=' * 60}")
    
    print(f"\n📋 적용된 개선 원칙:")
    print(f"  ✅ 기존 각 섹션 내용을 주된 내용으로 유지")
    print(f"  ✅ 전체 내용 대상 추가 정보를 보완적으로만 반영") 
    print(f"  ✅ 주요 화제와 부차 화제는 그대로 보존 (왜곡 방지)")
    print(f"  ✅ 핵심 내용 + 상세 핵심 내용만 개선")
    print(f"  ✅ 각 섹션의 고유한 특성과 역할 유지")

if __name__ == "__main__":
    asyncio.run(process_all_sections())