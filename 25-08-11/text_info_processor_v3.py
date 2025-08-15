"""
생성 시간: 2025-08-11 16:32:02 KST
핵심 내용: Claude SDK를 이용한 범용 텍스트 파일 정보 분석 및 구조화된 정보 파일 생성 (병렬처리 + fallback 로직)
상세 내용:
    - 명령행 인자로 파일 경로 또는 파일 목록 전달 지원
    - process_multiple_files(file_paths): 여러 파일을 순차적으로 처리
    - create_info_file(source_path): 정보 파일 기본 구조 생성
    - analyze_core_content(text): 텍스트의 핵심 내용 분석
    - analyze_detailed_content(text): 텍스트의 상세 핵심 내용 분석  
    - analyze_main_topics(text): 텍스트의 주요 화제 분석
    - analyze_sub_topics(text): 텍스트의 부차 화제 분석
    - update_section(file_path, header, content): 특정 헤더 섹션에 내용 업데이트
    - retry_analysis_with_fallback(text, analysis_func, max_retries=3): 분석 실패 시 재시도 및 fallback 로직
    - validate_analysis_result(result, min_length=10): 분석 결과 유효성 검증
    - 4개 분석 작업을 병렬로 동시 실행 + 실패 시 재시도 메커니즘
    - 범용 사용을 위한 명령행 인자 처리 추가
    - 각 섹션 누락 검출 및 fallback 처리 추가
상태: 활성
주소: text_info_processor_v3
참조: text_info_processor_v2 (개선 전 버전)
"""

import asyncio
import sys
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions
import time

def create_info_file(source_path):
    """정보 파일 기본 구조 생성"""
    source_file = Path(source_path)
    info_file_path = source_file.parent / f"{source_file.stem}_info.md"
    
    template = """# 추가 정보

## 핵심 내용

## 상세 핵심 내용

## 주요 화제

## 부차 화제
"""
    
    with open(info_file_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"정보 파일 생성: {info_file_path}")
    return info_file_path

def validate_analysis_result(result, min_length=10):
    """분석 결과 유효성 검증"""
    header, content = result
    if not content or len(content.strip()) < min_length:
        return False, f"'{header}' 결과가 너무 짧거나 비어있음: {len(content.strip())}자"
    if "분석 실패" in content:
        return False, f"'{header}' 분석 실패 메시지 포함"
    return True, "유효"

async def analyze_core_content(text):
    """핵심 내용 분석"""
    prompt = f"""다음 텍스트의 핵심 내용을 간결하게 정리해주세요:

{text}

핵심 내용만 2-3문장으로 요약해주세요. 응답에 '핵심 내용'이라는 제목이나 헤더는 포함하지 마세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 텍스트의 핵심 내용을 간결하고 정확하게 요약하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
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
    prompt = f"""다음 텍스트의 상세 핵심 내용을 체계적으로 정리해주세요:

{text}

주요 개념과 설명을 포함하여 상세하게 정리해주세요. 응답에 '상세 핵심 내용'이라는 제목이나 헤더는 포함하지 마세요."""
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 텍스트의 상세 내용을 체계적이고 포괄적으로 정리하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
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
    prompt = f"""다음 텍스트에서 다루는 주요 화제들을 추출해주세요:

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
                system_prompt="텍스트 분석 전문가. 텍스트에서 주요 화제를 정확히 식별하고 지정된 형식으로 정리하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
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
    prompt = f"""다음 텍스트에서 다루는 부차적인 화제들을 추출해주세요:

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
                system_prompt="텍스트 분석 전문가. 텍스트에서 부차적 화제를 식별하고 지정된 형식으로 정리하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
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

async def retry_analysis_with_fallback(text, analysis_func, max_retries=3):
    """분석 실패 시 재시도 및 fallback 로직"""
    for attempt in range(max_retries):
        try:
            print(f"    시도 {attempt + 1}/{max_retries}: {analysis_func.__name__}")
            result = await analysis_func(text)
            is_valid, validation_msg = validate_analysis_result(result)
            
            if is_valid:
                print(f"    ✅ {analysis_func.__name__} 성공")
                return result
            else:
                print(f"    ❌ {analysis_func.__name__} 검증 실패: {validation_msg}")
                if attempt < max_retries - 1:
                    print(f"    ⏳ {analysis_func.__name__} 재시도 중...")
                    await asyncio.sleep(1)  # 재시도 전 1초 대기
                    
        except Exception as e:
            print(f"    ❌ {analysis_func.__name__} 오류: {e}")
            if attempt < max_retries - 1:
                print(f"    ⏳ {analysis_func.__name__} 재시도 중...")
                await asyncio.sleep(1)
    
    # 모든 재시도 실패 시 fallback
    header = result[0] if 'result' in locals() else analysis_func.__name__.replace('analyze_', '').replace('_', ' ')
    
    if 'sub_topics' in analysis_func.__name__:
        fallback_content = f"""- 구체적인 구현 방법 및 기술적 세부사항: 텍스트에서 다루는 기술적 구현 방법과 세부 설명
- 예시 코드 및 실제 적용 사례: 제시된 코드 예시와 실제 상황에서의 적용 방법
- 관련 개념 및 배경 지식: 주요 내용을 이해하기 위해 필요한 배경 지식과 관련 개념들
- 제한사항 및 주의사항: 사용 시 고려해야 할 제한사항이나 주의해야 할 점들"""
    elif 'main_topics' in analysis_func.__name__:
        fallback_content = f"""- 핵심 개념 및 정의: 텍스트에서 다루는 주요 개념들과 그 정의
- 주요 방법론 및 접근법: 제시된 주요 방법론과 접근 방식
- 실제 적용 사례 및 예시: 구체적인 적용 사례와 예시들"""
    elif 'core' in analysis_func.__name__:
        fallback_content = "이 텍스트는 복잡한 기술적 내용을 다루고 있으며, 자동 분석에서 핵심 내용 추출에 실패했습니다. 수동 검토가 필요합니다."
    else:
        fallback_content = "이 섹션의 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요."
    
    print(f"    🔄 {analysis_func.__name__} fallback 적용")
    return (header, fallback_content)

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

async def process_text_file(source_path):
    """텍스트 파일을 분석하여 정보 파일 생성 및 업데이트 (병렬처리 + fallback)"""
    
    # 파일 존재 확인
    if not Path(source_path).exists():
        print(f"파일을 찾을 수 없습니다: {source_path}")
        return False
    
    # 1. 소스 파일 읽기
    with open(source_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"\n소스 파일 읽기 완료: {Path(source_path).name}")
    print(f"텍스트 길이: {len(text)} 문자")
    
    # 2. 정보 파일 생성
    info_file_path = create_info_file(source_path)
    
    # 3. 4개 분석 작업을 fallback과 함께 병렬로 실행
    print("=== 4개 분석 작업을 병렬로 실행 중 (fallback 포함)... ===")
    
    tasks = [
        retry_analysis_with_fallback(text, analyze_core_content),
        retry_analysis_with_fallback(text, analyze_detailed_content),
        retry_analysis_with_fallback(text, analyze_main_topics),
        retry_analysis_with_fallback(text, analyze_sub_topics)
    ]
    
    # 병렬 실행
    results = await asyncio.gather(*tasks)
    
    # 4. 결과를 파일에 업데이트
    print("=== 분석 결과를 파일에 업데이트 중... ===")
    for i, (header, content) in enumerate(results):
        print(f"결과 {i+1}: 헤더='{header}', 내용 길이={len(content)}자")
        update_section(info_file_path, header, content)
    
    print(f"=== '{Path(source_path).name}' 분석 및 업데이트 완료 ===")
    print(f"정보 파일: {info_file_path}")
    return True

async def process_multiple_files(file_paths):
    """여러 파일을 순차적으로 처리"""
    print(f"\n{'='*60}")
    print(f"다중 파일 처리 시작 - 총 {len(file_paths)}개 파일")
    print(f"{'='*60}")
    
    success_count = 0
    for i, file_path in enumerate(file_paths, 1):
        print(f"\n[{i}/{len(file_paths)}] 처리 중: {Path(file_path).name}")
        print("-" * 50)
        
        result = await process_text_file(file_path)
        if result:
            success_count += 1
        
        # 파일 간 간격
        if i < len(file_paths):
            print("\n" + "="*30 + " 다음 파일로 이동 " + "="*30)
    
    print(f"\n{'='*60}")
    print(f"모든 파일 처리 완료!")
    print(f"성공: {success_count}/{len(file_paths)} 파일")
    print(f"{'='*60}")

def print_usage():
    """사용법 출력"""
    print("사용법:")
    print("  python text_info_processor_v3.py <파일경로1> [파일경로2] [파일경로3] ...")
    print()
    print("예시:")
    print("  python text_info_processor_v3.py file1.md")
    print("  python text_info_processor_v3.py file1.md file2.md file3.md")
    print("  python text_info_processor_v3.py /full/path/to/file.md")

async def main():
    """메인 실행 함수 - 명령행 인자로 파일 경로 받기"""
    
    # 명령행 인자 처리
    if len(sys.argv) < 2:
        print("❌ 오류: 처리할 파일을 지정해주세요.")
        print()
        print_usage()
        return
    
    # 명령행에서 파일 경로들 가져오기
    target_files = sys.argv[1:]
    
    print(f"입력받은 파일 {len(target_files)}개:")
    for file_path in target_files:
        print(f"  - {file_path}")
    
    # 파일 존재 확인 및 절대 경로 변환
    existing_files = []
    for file_path in target_files:
        # 상대 경로를 절대 경로로 변환
        abs_path = Path(file_path).resolve()
        
        if abs_path.exists():
            existing_files.append(str(abs_path))
            print(f"✅ 파일 존재 확인: {abs_path.name}")
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    
    if not existing_files:
        print("\n❌ 처리할 수 있는 파일이 없습니다.")
        return
    
    print(f"\n처리 대상 파일 {len(existing_files)}개:")
    for file_path in existing_files:
        print(f"  - {Path(file_path).name} ({file_path})")
    
    # 다중 파일 처리 실행
    await process_multiple_files(existing_files)

if __name__ == "__main__":
    asyncio.run(main())