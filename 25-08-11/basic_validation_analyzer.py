"""
생성 시간: 2025-08-11 15:35:13 KST
핵심 내용: 7_Basic_data_validation.md에 포함된 모든 파일 내용을 로딩하고 통합 분석하여 정보 파일 생성 
상세 내용:
    - load_included_files(base_file): 기본 파일에 나열된 파일들을 순차 로딩
    - combine_all_content(files_content): 모든 파일 내용을 하나로 결합
    - create_info_file(target_file): 정보 파일 기본 구조 생성
    - analyze_core_content(text): 통합 텍스트의 핵심 내용 분석
    - analyze_detailed_content(text): 통합 텍스트의 상세 핵심 내용 분석
    - analyze_main_topics(text): 통합 텍스트의 주요 화제 분석
    - analyze_sub_topics(text): 통합 텍스트의 부차 화제 분석
    - update_section(file_path, header, content): 특정 헤더 섹션에 내용 업데이트
    - process_basic_validation_files(): 메인 실행 함수 (병렬 분석)
상태: 활성
주소: basic_validation_analyzer
참조: text_info_processor.py (분석 로직 참고)
"""

import asyncio
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions

def load_included_files(base_file_path):
    """기본 파일에 나열된 파일들을 순차적으로 로딩"""
    base_path = Path(base_file_path)
    base_dir = base_path.parent
    
    # 기본 파일에서 파일 목록 읽기
    with open(base_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    files_content = {}
    file_order = []
    
    print(f"기본 파일 읽기: {base_file_path}")
    
    # 파일 목록 추출 (라인별로 .md로 끝나는 파일들)
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.endswith('.md') and line != base_path.name:
            file_path = base_dir / line
            file_order.append(line)
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    files_content[line] = file_content
                    print(f"  ✅ {line} 로딩 완료 ({len(file_content)}자)")
                except Exception as e:
                    print(f"  ❌ {line} 로딩 실패: {e}")
                    files_content[line] = f"로딩 실패: {e}"
            else:
                print(f"  ⚠️ {line} 파일 없음")
                files_content[line] = "파일 없음"
    
    return files_content, file_order

def combine_all_content(files_content, file_order):
    """모든 파일 내용을 하나로 결합"""
    combined_text = ""
    
    for filename in file_order:
        if filename in files_content:
            combined_text += f"\n\n=== {filename} ===\n\n"
            combined_text += files_content[filename]
    
    return combined_text.strip()

def create_info_file(target_file_path):
    """정보 파일 기본 구조 생성"""
    template = """# 추가 정보

## 핵심 내용

## 상세 핵심 내용

## 주요 화제

## 부차 화제
"""
    
    with open(target_file_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"정보 파일 생성: {target_file_path}")
    return target_file_path

async def analyze_core_content(text):
    """핵심 내용 분석"""
    prompt = f"""다음은 데이터 검증에 관한 여러 파일의 통합 내용입니다. 전체 내용의 핵심을 간결하게 정리해주세요:

{text}

전체 내용의 핵심 메시지를 2-3문장으로 요약해주세요. 응답에 '핵심 내용'이라는 제목이나 헤더는 포함하지 마세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="데이터 검증 전문가. 여러 파일의 통합 내용에서 핵심 메시지를 간결하고 정확하게 요약하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        # 응답 추출
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        
        return ('핵심 내용', content.strip())
        
    except Exception as e:
        print(f"핵심 내용 분석 중 오류 발생: {e}")
        return ('핵심 내용', f"분석 실패: {str(e)}")

async def analyze_detailed_content(text):
    """상세 핵심 내용 분석"""
    prompt = f"""다음은 데이터 검증에 관한 여러 파일의 통합 내용입니다. 상세 핵심 내용을 체계적으로 정리해주세요:

{text}

주요 개념, 기술, 방법론을 포함하여 상세하게 정리해주세요. 각 파일의 주요 내용을 통합적으로 다뤄주세요. 응답에 '상세 핵심 내용'이라는 제목이나 헤더는 포함하지 마세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="데이터 검증 전문가. 통합된 내용의 상세 개념을 체계적이고 포괄적으로 정리하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        # 응답 추출
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        
        return ('상세 핵심 내용', content.strip())
        
    except Exception as e:
        print(f"상세 내용 분석 중 오류 발생: {e}")
        return ('상세 핵심 내용', f"분석 실패: {str(e)}")

async def analyze_main_topics(text):
    """주요 화제 분석"""
    prompt = f"""다음은 데이터 검증에 관한 여러 파일의 통합 내용입니다. 전체 내용에서 다루는 주요 화제들을 추출해주세요:

{text}

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
                system_prompt="데이터 검증 전문가. 통합 내용에서 주요 화제를 정확히 식별하고 지정된 형식으로 정리하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        # 응답 추출
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        
        return ('주요 화제', content.strip())
        
    except Exception as e:
        print(f"주요 화제 분석 중 오류 발생: {e}")
        return ('주요 화제', f"분석 실패: {str(e)}")

async def analyze_sub_topics(text):
    """부차 화제 분석"""
    prompt = f"""다음은 데이터 검증에 관한 여러 파일의 통합 내용입니다. 전체 내용에서 다루는 부차적인 화제들을 추출해주세요:

{text}

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
                system_prompt="데이터 검증 전문가. 통합 내용에서 부차적 화제를 식별하고 지정된 형식으로 정리하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        # 응답 추출
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        
        return ('부차 화제', content.strip())
        
    except Exception as e:
        print(f"부차 화제 분석 중 오류 발생: {e}")
        return ('부차 화제', f"분석 실패: {str(e)}")

def update_section(file_path, header, content):
    """파일의 특정 헤더 섹션에 내용 업데이트 (헤더와 내용 사이 공백 없이)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 해당 헤더 찾기
    header_pattern = f"## {header}"
    header_start = text.find(header_pattern)
    
    if header_start == -1:
        print(f"헤더를 찾을 수 없습니다: {header}")
        return False
    
    # 다음 헤더 찾기 (## 로 시작하는 다음 줄)
    content_start = header_start + len(header_pattern)
    next_header_start = text.find("\n## ", content_start)
    
    if next_header_start == -1:
        # 마지막 섹션인 경우 - 헤더와 내용 사이 공백 없이
        new_text = text[:content_start] + f"\n{content}\n"
    else:
        # 중간 섹션인 경우 - 헤더와 내용 사이 공백 없이
        new_text = text[:content_start] + f"\n{content}\n" + text[next_header_start:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    
    print(f"'{header}' 섹션 업데이트 완료")
    return True

async def process_basic_validation_files():
    """7_Basic_data_validation에 포함된 파일들을 통합 분석하여 정보 파일 생성"""
    
    base_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections/7_Basic_data_validation.md"
    info_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections/7_Basic_data_validation_info.md"
    
    print("=== 7_Basic_data_validation 통합 분석 시작 ===")
    
    # 1. 포함된 파일들 로딩
    files_content, file_order = load_included_files(base_file)
    print(f"\n로딩된 파일 수: {len(files_content)}")
    
    # 2. 모든 내용을 하나로 결합
    combined_text = combine_all_content(files_content, file_order)
    print(f"통합 텍스트 길이: {len(combined_text)} 문자")
    
    # 3. 정보 파일 생성
    create_info_file(info_file)
    
    # 4. 4개 분석 작업을 병렬로 실행
    print("\n=== 4개 분석 작업을 병렬로 실행 중... ===")
    
    tasks = [
        analyze_core_content(combined_text),
        analyze_detailed_content(combined_text),
        analyze_main_topics(combined_text),
        analyze_sub_topics(combined_text)
    ]
    
    # 병렬 실행
    results = await asyncio.gather(*tasks)
    
    # 5. 결과를 파일에 업데이트
    print("\n=== 분석 결과를 파일에 업데이트 중... ===")
    for i, (header, content) in enumerate(results):
        print(f"결과 {i+1}: 헤더='{header}', 내용 길이={len(content)}자")
        if len(content) < 100:
            print(f"  내용 미리보기: {content[:100]}")
        update_section(info_file, header, content)
        print(f"'{header}' 섹션 업데이트 완료")
    
    print(f"\n=== 모든 분석 및 업데이트 완료 ===")
    print(f"정보 파일: {info_file}")
    
    # 6. 로딩된 파일 목록 출력
    print(f"\n=== 분석에 포함된 파일들 ===")
    for i, filename in enumerate(file_order, 1):
        content_length = len(files_content.get(filename, ""))
        print(f"{i}. {filename} ({content_length:,}자)")

async def main():
    await process_basic_validation_files()

if __name__ == "__main__":
    asyncio.run(main())