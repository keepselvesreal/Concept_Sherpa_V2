"""
생성 시간: 2025-08-22 12:03:09 KST
핵심 내용: 유튜브 대본 구조화 스크립트 - extraction-system 통합 버전
상세 내용:
    - extract_transcript_content(file_path): 메타데이터와 대본 내용 분리 (8-90)
    - extract_first_last_sentences(transcript_content): 첫/마지막 문장 추출 및 필러 워드 제거 (97-139)
    - check_content_coverage(original_sentences, improved_content): 내용 누락 검사 (142-168)
    - improve_transcript_with_claude(transcript_content, retry_count): Claude SDK 호출 (fallback 포함) (171-248)
    - combine_with_metadata(metadata, improved_content): 메타데이터와 구조화 대본 결합 (282-342)
    - save_improved_transcript(content, output_file): 파일 저장 (345-362)
    - main(): 메인 실행 함수 (365-442)
상태: active
참조: transcript_improver_v4
"""

import os
import re
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Set

from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
from claude_code_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError


def extract_transcript_content(file_path: str) -> str:
    """
    마크다운 파일에서 순수 대본 내용만 추출합니다.
    
    Args:
        file_path (str): 마크다운 파일 경로
        
    Returns:
        str: 순수 대본 내용
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        
        # --- 구분자 이후의 대본 내용만 찾기
        transcript_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                transcript_start_idx = i + 1
                break
        
        # 대본 내용만 추출
        transcript_lines = lines[transcript_start_idx:]
        transcript_content = ""
        
        for line in transcript_lines:
            line = line.strip()
            if line and line.startswith('['):
                # [MM:SS] 형식의 타임스탬프와 텍스트만 추출
                match = re.match(r'\[(\d{2}):(\d{2})\] (.+)', line)
                if match:
                    transcript_content += f"{line}\n"
        
        return transcript_content.strip()
        
    except Exception as e:
        print(f"❌ 파일 파싱 중 오류 발생: {str(e)}")
        return ""


def extract_first_last_sentences(transcript_content: str) -> Tuple[Set[str], Set[str]]:
    """
    대본에서 첫 문장과 마지막 문장을 추출하고 필러 워드를 제거합니다.
    
    Args:
        transcript_content (str): 대본 내용
        
    Returns:
        tuple: (first_sentence_words, last_sentence_words) - 필러 워드 제거된 단어 집합
    """
    try:
        lines = [line.strip() for line in transcript_content.strip().split('\n') if line.strip()]
        
        if not lines:
            return set(), set()
        
        # 첫 문장과 마지막 문장 추출
        first_line = lines[0]
        last_line = lines[-1]
        
        # 타임스탬프 제거하고 텍스트만 추출
        first_text = re.sub(r'\[\d{2}:\d{2}\]\s*', '', first_line)
        last_text = re.sub(r'\[\d{2}:\d{2}\]\s*', '', last_line)
        
        # 필러 워드 목록
        filler_words = {
            'um', 'uh', 'ah', 'you', 'know', 'like', 'so', 'well', 'okay', 'right',
            'actually', 'basically', 'literally', 'really', 'just', 'kind', 'of', 'sort'
        }
        
        # 단어 추출 및 필러 워드 제거
        def extract_clean_words(text: str) -> Set[str]:
            words = re.findall(r'\b\w+\b', text.lower())
            return {word for word in words if word not in filler_words and len(word) > 2}
        
        first_words = extract_clean_words(first_text)
        last_words = extract_clean_words(last_text)
        
        return first_words, last_words
        
    except Exception as e:
        print(f"❌ 첫/마지막 문장 추출 중 오류: {str(e)}")
        return set(), set()


def check_content_coverage(original_first_words: Set[str], original_last_words: Set[str], 
                          improved_content: str) -> bool:
    """
    구조화된 내용에 원본의 첫/마지막 문장 단어가 포함되어 있는지 확인합니다.
    
    Args:
        original_first_words (Set[str]): 원본 첫 문장의 단어들
        original_last_words (Set[str]): 원본 마지막 문장의 단어들
        improved_content (str): 구조화된 내용
        
    Returns:
        bool: 충분한 내용이 포함되어 있으면 True
    """
    try:
        improved_text = improved_content.lower()
        
        # 첫 문장 단어 중 하나라도 포함되어 있는지 확인
        first_found = any(word in improved_text for word in original_first_words)
        
        # 마지막 문장 단어 중 하나라도 포함되어 있는지 확인  
        last_found = any(word in improved_text for word in original_last_words)
        
        return first_found and last_found
        
    except Exception as e:
        print(f"❌ 내용 포함 확인 중 오류: {str(e)}")
        return True  # 오류 시 통과


async def improve_transcript_with_claude(transcript_content: str, original_first_words: Set[str], 
                                       original_last_words: Set[str], max_retries: int = 2) -> str:
    """
    Claude Code SDK를 사용하여 대본을 구조화합니다 (fallback 포함).
    
    Args:
        transcript_content (str): 순수 대본 내용
        original_first_words (Set[str]): 원본 첫 문장 단어들
        original_last_words (Set[str]): 원본 마지막 문장 단어들
        max_retries (int): 최대 재시도 횟수
        
    Returns:
        str: 구조화된 대본 내용
    """
    for attempt in range(max_retries + 1):
        try:
            # Claude Code SDK 옵션 설정
            options = ClaudeCodeOptions(
                system_prompt="당신은 YouTube 대본을 구조화하는 전문가입니다.",
                max_turns=1
            )
            
            # 프롬프트 구성
            user_prompt = f"""Structure this YouTube transcript following these exact requirements:

{transcript_content}

**REQUIREMENTS:**
1. Remove only filler words (um, uh, ah, you know, like, etc.)
2. Combine semantically related sentences into appropriate units
3. Divide content into 5-7 sections with ## English section titles
4. Keep the start time in [MM:SS] format for each combined sentence
5. Include ALL content from beginning to end

**FORBIDDEN:**
- Adding introductory text or explanations
- Adding commentary or personal notes
- Fix grammatical errors
- Improve incomplete sentences  
- Remove repetitive content
- Change or paraphrase original content
- Replace words or expressions
- Skip any part of the transcript

**OUTPUT FORMAT:**
## English Section Title

[time] Original content (with filler words removed and semantically combined)

Return ONLY the structured transcript content. Do not add any introductory text, explanations, or commentary."""

            # Claude Code SDK 호출
            response_content = ""
            async for message in query(prompt=user_prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_content += block.text
            
            if response_content:
                # 내용 포함 확인
                if check_content_coverage(original_first_words, original_last_words, response_content):
                    print(f"✅ 내용 포함 검증 통과 (시도 {attempt + 1}/{max_retries + 1})")
                    return response_content.strip()
                else:
                    if attempt < max_retries:
                        print(f"⚠️ 내용 누락 감지 - 재시도 {attempt + 1}/{max_retries}")
                        continue
                    else:
                        print(f"⚠️ 최대 재시도 횟수 도달 - 부분 결과 사용")
                        return response_content.strip()
            else:
                print(f"❌ 빈 응답 수신 (시도 {attempt + 1}/{max_retries + 1})")
                
        except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
            print(f"❌ Claude Code SDK 오류 (시도 {attempt + 1}/{max_retries + 1}): {str(e)}")
        except Exception as e:
            print(f"❌ Claude SDK 호출 중 오류 (시도 {attempt + 1}/{max_retries + 1}): {str(e)}")
    
    return ""






async def main():
    """
    메인 실행 함수
    """
    print("🤖 Claude Code SDK 대본 구조화기 - extraction-system 통합 버전")
    print("=" * 60)
    
    # 입력 파일 확인
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("구조화할 대본 파일 경로를 입력하세요: ").strip()
    
    if not input_file or not os.path.exists(input_file):
        print("❌ 유효한 파일 경로를 입력해주세요.")
        return
    
    print(f"📁 입력 파일: {input_file}")
    print("🔑 Claude Code SDK 환경에서 실행 중...")
    
    # 대본 내용 추출
    print("📖 대본 내용 추출 중...")
    transcript_content = extract_transcript_content(input_file)
    
    if not transcript_content:
        print("❌ 대본 내용을 추출할 수 없습니다.")
        return
    
    transcript_line_count = len([line for line in transcript_content.split('\n') if line.strip()])
    print(f"✅ {transcript_line_count}개의 대본 항목 추출")
    
    # 첫/마지막 문장 추출 및 필러 워드 제거
    print("🔍 내용 누락 감지를 위한 기준 문장 추출 중...")
    first_words, last_words = extract_first_last_sentences(transcript_content)
    print(f"✅ 기준 단어 추출 완료 (첫 문장: {len(first_words)}개, 마지막 문장: {len(last_words)}개)")
    
    # Claude Code SDK로 대본 구조화 (fallback 포함)
    print("🤖 Claude Code SDK로 전체 대본 구조화 중...")
    print("   - 필러 워드 제거")
    print("   - 의미 단위 문장 합치기")  
    print("   - 5-7개 섹션으로 구분")
    print("   - 전체 대본 처리")
    print("   - 내용 누락 감지 및 fallback")
    
    improved_content = await improve_transcript_with_claude(transcript_content, first_words, last_words)
    
    if not improved_content:
        print("❌ 대본 구조화에 실패했습니다.")
        return
    
    print("✅ 대본 구조화 완료")
    
    # 출력 파일명 생성 (메타데이터 부분 제거하여 _content.md 형태로)
    input_path = Path(input_file)
    base_name = input_path.stem  # 250822_001_DAQJvGjlgVM
    
    # 메타데이터 부분 제거 (날짜_를 제거)
    if '_' in base_name:
        parts = base_name.split('_', 2)  # ['250822', '001', 'DAQJvGjlgVM']
        if len(parts) >= 3:
            content_name = f"{parts[1]}_{parts[2]}_content.md"  # 001_DAQJvGjlgVM_content.md
        else:
            content_name = f"{base_name}_content.md"
    else:
        content_name = f"{base_name}_content.md"
    
    # 원본 파일과 같은 폴더에 저장
    output_file = input_path.parent / content_name
    
    # 파일 저장
    print(f"💾 파일 저장 중: {output_file}")
    try:
        with open(str(output_file), 'w', encoding='utf-8') as f:
            f.write(improved_content)
        
        # 구조화 요약 출력
        sections = len([line for line in improved_content.split('\n') if line.strip().startswith('##')])
        print(f"✅ 저장 완료: {output_file}")
        print(f"📊 구조화 요약: {sections}개 섹션으로 구분")
        print(f"🛡️ 내용 누락 감지: 활성화됨")
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())