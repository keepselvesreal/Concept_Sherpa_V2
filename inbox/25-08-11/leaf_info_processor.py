#!/usr/bin/env python3
"""
생성 시간: 2025-08-11 21:15:27 KST
핵심 내용: 리프 노드 정보 처리기 - 모든 리프 노드 파일에 구조화된 추가 정보 생성
상세 내용:
    - find_leaf_files (20-35행): 디렉토리에서 모든 리프 노드 파일 찾기
    - create_info_file (37-55행): 정보 파일 기본 구조 생성
    - analyze_content (57-95행): Claude SDK를 이용한 콘텐츠 분석
    - validate_result (97-105행): 분석 결과 유효성 검증
    - retry_with_fallback (107-130행): 재시도 및 fallback 로직
    - update_section (132-160행): 정보 파일 섹션 업데이트
    - process_single_leaf (162-205행): 단일 리프 파일 처리
    - process_all_leaves (207-245행): 모든 리프 파일 일괄 처리
    - main (247-275행): CLI 인터페이스 및 실행
상태: active
주소: leaf_info_processor
참조: text_info_processor_v3 (구조 참고)
"""

import asyncio
import argparse
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions
import glob


def find_leaf_files(directory):
    """디렉토리에서 모든 리프 노드 파일 찾기"""
    directory = Path(directory)
    if not directory.exists():
        return []
    
    # leaf_*.md 패턴으로 파일 찾기
    leaf_pattern = str(directory / "leaf_*.md")
    leaf_files = glob.glob(leaf_pattern)
    
    return sorted(leaf_files)


def create_info_file(leaf_file_path):
    """정보 파일 기본 구조 생성"""
    leaf_file = Path(leaf_file_path)
    info_file_path = leaf_file.parent / f"{leaf_file.stem}_info.md"
    
    template = """# 추가 정보

## 핵심 내용

## 상세 핵심 내용

## 주요 화제

## 부차 화제
"""
    
    with open(info_file_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    return info_file_path


async def analyze_content(text, analysis_type):
    """Claude SDK를 이용한 콘텐츠 분석"""
    
    prompts = {
        '핵심 내용': f"""다음 텍스트의 핵심 내용을 간결하게 정리해주세요:

{text}

핵심 내용만 2-3문장으로 요약해주세요. 응답에 '핵심 내용'이라는 제목이나 헤더는 포함하지 마세요.""",
        
        '상세 핵심 내용': f"""다음 텍스트의 상세 핵심 내용을 체계적으로 정리해주세요:

{text}

주요 개념과 설명을 포함하여 상세하게 정리해주세요. 응답에 '상세 핵심 내용'이라는 제목이나 헤더는 포함하지 마세요.""",
        
        '주요 화제': f"""다음 텍스트에서 다루는 주요 화제들을 추출해주세요:

{text}

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요.""",
        
        '부차 화제': f"""다음 텍스트에서 다루는 부차적인 화제들을 추출해주세요:

{text}

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
    }
    
    prompt = prompts.get(analysis_type, "")
    if not prompt:
        return f"알 수 없는 분석 타입: {analysis_type}"
    
    try:
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="텍스트 분석 전문가. 텍스트의 내용을 정확하고 체계적으로 분석하세요. 헤더 사용 시 # 1레벨과 ## 2레벨은 사용하지 말고 반드시 ### 3레벨부터 사용하세요.",
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
        
        return content.strip()
        
    except Exception as e:
        return f"분석 실패: {str(e)}"


def validate_result(content, min_length=10):
    """분석 결과 유효성 검증"""
    if not content or len(content.strip()) < min_length:
        return False
    if "분석 실패" in content:
        return False
    return True


async def retry_with_fallback(text, analysis_type, max_retries=3, verbose=True):
    """재시도 및 fallback 로직"""
    for attempt in range(max_retries):
        if verbose:
            print(f"    시도 {attempt + 1}/{max_retries}: {analysis_type}")
        
        result = await analyze_content(text, analysis_type)
        
        if validate_result(result):
            if verbose:
                print(f"    ✅ {analysis_type} 성공")
            return result
        else:
            if verbose:
                print(f"    ❌ {analysis_type} 검증 실패")
                if attempt < max_retries - 1:
                    print(f"    ⏳ {analysis_type} 재시도 중...")
            await asyncio.sleep(0.5)  # 재시도 간격 단축
    
    # Fallback 콘텐츠
    fallback_contents = {
        '핵심 내용': "이 섹션의 핵심 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요.",
        '상세 핵심 내용': "이 섹션의 상세 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요.",
        '주요 화제': "- 주요 개념 및 정의: 텍스트에서 다루는 주요 개념들과 그 정의\n- 실제 적용 사례: 구체적인 적용 사례와 예시들",
        '부차 화제': "- 구체적인 구현 방법: 텍스트에서 다루는 구현 방법과 세부사항\n- 관련 개념 및 배경: 주요 내용을 이해하기 위한 배경 지식"
    }
    
    if verbose:
        print(f"    🔄 {analysis_type} fallback 적용")
    return fallback_contents.get(analysis_type, "분석에 실패했습니다.")


def update_section(file_path, header, content, verbose=True):
    """파일의 특정 헤더 섹션에 내용 업데이트"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 해당 헤더 찾기
    header_pattern = f"## {header}"
    header_start = text.find(header_pattern)
    
    if header_start == -1:
        if verbose:
            print(f"헤더를 찾을 수 없습니다: {header}")
        return False
    
    # 다음 헤더 찾기
    content_start = header_start + len(header_pattern)
    next_header_start = text.find("\n## ", content_start)
    
    if next_header_start == -1:
        # 마지막 섹션인 경우
        new_text = text[:content_start] + f"\n{content}\n"
    else:
        # 중간 섹션인 경우
        new_text = text[:content_start] + f"\n{content}\n" + text[next_header_start:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    
    if verbose:
        print(f"  ✅ '{header}' 섹션 업데이트 완료")
    return True


async def process_single_leaf(leaf_file_path):
    """단일 리프 파일 처리"""
    filename = Path(leaf_file_path).name
    print(f"🔄 {filename}")
    
    # 원본 파일 읽기
    try:
        with open(leaf_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ {filename}: 파일 읽기 실패 - {e}")
        return False
    
    # 정보 파일 생성
    info_file_path = create_info_file(leaf_file_path)
    
    # 4가지 분석 병렬 실행
    analysis_types = ['핵심 내용', '상세 핵심 내용', '주요 화제', '부차 화제']
    
    tasks = [
        retry_with_fallback(text, analysis_type, verbose=False) 
        for analysis_type in analysis_types
    ]
    
    results = await asyncio.gather(*tasks)
    
    # 결과를 파일에 업데이트
    for analysis_type, content in zip(analysis_types, results):
        update_section(info_file_path, analysis_type, content, verbose=False)
    
    print(f"✅ {filename}")
    return True


async def process_all_leaves(directory):
    """모든 리프 파일 병렬 처리"""
    leaf_files = find_leaf_files(directory)
    
    if not leaf_files:
        print(f"❌ '{directory}'에서 리프 파일을 찾을 수 없습니다.")
        return
    
    print(f"🎯 리프 노드 정보 처리기 (병렬 처리)")
    print("=" * 50)
    print(f"📁 디렉토리: {directory}")
    print(f"📄 리프 파일: {len(leaf_files)}개")
    print(f"🚀 병렬 처리 시작...")
    print()
    
    import time
    start_time = time.time()
    
    # 모든 리프 파일을 병렬로 처리
    tasks = [process_single_leaf(file_path) for file_path in leaf_files]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed_time = time.time() - start_time
    
    # 결과 집계
    successful = sum(1 for result in results if result is True)
    failed = len(results) - successful
    
    print(f"\n✨ 모든 리프 노드 처리 완료!")
    print(f"   - 총 파일: {len(leaf_files)}개")
    print(f"   - 성공: {successful}개")
    print(f"   - 실패: {failed}개")
    print(f"   - 소요 시간: {elapsed_time:.1f}초")
    print(f"   - 평균 처리 시간: {elapsed_time/len(leaf_files):.1f}초/파일")


def main():
    """CLI 인터페이스 및 실행"""
    parser = argparse.ArgumentParser(
        description='리프 노드 파일들에 구조화된 추가 정보 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python leaf_info_processor.py sections/
  python leaf_info_processor.py /path/to/sections/
        """
    )
    
    parser.add_argument('directory', help='리프 노드 파일들이 있는 디렉토리 경로')
    
    args = parser.parse_args()
    
    if not Path(args.directory).exists():
        print(f"❌ 디렉토리를 찾을 수 없습니다: {args.directory}")
        return
    
    # 비동기 실행
    asyncio.run(process_all_leaves(args.directory))


if __name__ == "__main__":
    main()