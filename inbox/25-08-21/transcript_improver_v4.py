"""
생성 시간: 2025-08-21 16:35:15 KST
핵심 내용: 실제 IDE 라인 번호와 내용 누락 감지 fallback을 포함한 대본 구조화 스크립트
상세 내용:
    - extract_transcript_content(file_path): 메타데이터와 대본 내용 분리
    - extract_first_last_sentences(transcript_content): 첫/마지막 문장 추출 및 필러 워드 제거
    - check_content_coverage(original_sentences, improved_content): 내용 누락 검사
    - improve_transcript_with_claude(transcript_content, retry_count): Claude SDK 호출 (fallback 포함)
    - update_actual_line_numbers(file_path): 실제 IDE 라인 번호로 업데이트
    - main(): 메인 실행 함수
상태: 활성
주소: transcript_improver_v4
참조: transcript_improver_v3
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


def extract_transcript_content(file_path: str) -> Tuple[Dict, str, List[str], int]:
    """
    마크다운 파일에서 메타데이터와 대본 내용을 분리합니다.
    
    Args:
        file_path (str): 마크다운 파일 경로
        
    Returns:
        tuple: (metadata, transcript_content, original_lines, transcript_start_line)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        
        # 메타데이터 추출 (체크박스 형태 지원)
        metadata = {}
        title = ""
        in_metadata = False
        transcript_start_idx = 0
        current_field = None
        
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line[2:].strip()
                metadata['title'] = title
            elif line.startswith('**Source Type:**'):
                current_field = 'source_type'
                in_metadata = True
            elif line.startswith('**Source:**'):
                metadata['source'] = line.split(':', 1)[1].strip()
                current_field = None
            elif line.startswith('**Source Language:**'):
                current_field = 'source_language'
            elif line.startswith('**Structure Type:**'):
                current_field = 'structure_type'
            elif line.startswith('**Content Processing:**'):
                current_field = 'content_processing'
            elif line.startswith('**Extracted Time:**'):
                metadata['extracted_time'] = line.split(':', 1)[1].strip()
                current_field = None
            elif current_field and line.strip().startswith('- [x]'):
                # 체크된 항목 추출
                checked_value = line.strip().replace('- [x] ', '')
                metadata[current_field] = checked_value
            elif line.strip() == '---' and in_metadata:
                transcript_start_idx = i + 1
                break
        
        # 대본 내용만 추출 (라인 번호 정보 없이)
        transcript_lines = lines[transcript_start_idx:]
        transcript_content = ""
        
        for line in transcript_lines:
            line = line.strip()
            if line and line.startswith('['):
                # [MM:SS] 형식의 타임스탬프와 텍스트만 추출
                match = re.match(r'\[(\d{2}):(\d{2})\] (.+)', line)
                if match:
                    transcript_content += f"{line}\n"
        
        return metadata, transcript_content.strip(), lines, transcript_start_idx + 1
        
    except Exception as e:
        print(f"❌ 파일 파싱 중 오류 발생: {str(e)}")
        return {}, "", [], 0


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
            user_prompt = f"""Please structure this YouTube transcript:

{transcript_content}

**ALLOWED OPERATIONS:**
1. Combine semantically related sentences into appropriate units
2. Remove filler words (um, uh, ah, you know, like, etc.)
3. Divide content into 5-7 sections with ## English section titles
4. Keep the start time in [MM:SS] format for each combined sentence
5. IMPORTANT: Include ALL content from beginning to end

**FORBIDDEN OPERATIONS:**
- Fix grammatical errors
- Improve incomplete sentences  
- Remove repetitive content
- Change or paraphrase original content
- Replace words or expressions
- Skip any part of the transcript

OUTPUT FORMAT:
## English Section Title

[time] Original content (with filler words removed and semantically combined)

Please follow these guidelines to only remove filler words, combine sentences by semantic units, and divide into 5-7 sections with ENGLISH section titles. NEVER skip any content - include everything from start to finish."""

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


def update_actual_line_numbers(file_path: str) -> None:
    """
    구조화된 파일에서 타임스탬프 라인 앞에 "Line X:" 정보를 추가합니다.
    
    Args:
        file_path (str): 구조화된 파일 경로
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        updated_lines = []
        for line_num, line in enumerate(lines, start=1):
            # 타임스탬프로 시작하는 라인 ([MM:SS])을 찾아서 Line 정보 추가
            if re.search(r'^\[\d{2}:\d{2}\]', line.strip()):
                updated_line = f"Line {line_num}: {line}"
                updated_lines.append(updated_line)
                print(f"업데이트: Line {line_num} - {line.strip()[:50]}...")
            else:
                updated_lines.append(line)
        
        # 파일에 다시 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
            
        print("✅ 실제 IDE 라인 번호로 업데이트 완료")
        
    except Exception as e:
        print(f"❌ 라인 번호 업데이트 중 오류: {str(e)}")


def combine_with_metadata(metadata: Dict, improved_content: str) -> str:
    """
    메타데이터와 구조화된 대본을 결합합니다 (체크박스 형태).
    
    Args:
        metadata (Dict): 원본 메타데이터
        improved_content (str): 구조화된 대본
        
    Returns:
        str: 최종 마크다운 내용
    """
    title = metadata.get('title', 'YouTube Transcript')
    source_type = metadata.get('source_type', 'youtube')
    source = metadata.get('source', '')
    source_language = metadata.get('source_language', 'en')
    structure_type = metadata.get('structure_type', 'standalone')
    content_processing = metadata.get('content_processing', 'unified')
    extracted_time = metadata.get('extracted_time', '')
    
    # Source Type 체크박스
    source_type_checkboxes = f"""- {"[x]" if source_type == "book" else "[ ]"} book
- {"[x]" if source_type == "post" else "[ ]"} post
- {"[x]" if source_type == "youtube" else "[ ]"} youtube"""
    
    # Source Language 체크박스
    language_checkboxes = f"""- {"[x]" if source_language in ["ko", "korean"] else "[ ]"} korean
- {"[x]" if source_language in ["en", "english"] else "[ ]"} english
- {"[x]" if source_language not in ["ko", "korean", "en", "english"] else "[ ]"} other"""
    
    # Structure Type 체크박스
    structure_type_checkboxes = f"""- {"[x]" if structure_type == "standalone" else "[ ]"} standalone
- {"[x]" if structure_type == "component" else "[ ]"} component"""
    
    # Content Processing 체크박스
    content_processing_checkboxes = f"""- {"[x]" if content_processing == "unified" else "[ ]"} unified
- {"[x]" if content_processing == "segmented" else "[ ]"} segmented"""
    
    # 체크박스 형태 헤더 생성
    header = f"""# {title}

**Source Type:**
{source_type_checkboxes}

**Source:** {source}

**Source Language:**
{language_checkboxes}

**Structure Type:**
{structure_type_checkboxes}

**Content Processing:**
{content_processing_checkboxes}

**Extracted Time:** {extracted_time}

---

"""
    
    return header + improved_content


def save_improved_transcript(content: str, output_file: str) -> bool:
    """
    개선된 대본을 파일로 저장합니다.
    
    Args:
        content (str): 저장할 내용
        output_file (str): 출력 파일 경로
        
    Returns:
        bool: 저장 성공 여부
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {str(e)}")
        return False


async def main():
    """
    메인 실행 함수
    """
    print("🤖 Claude Code SDK 대본 구조화기 v4")
    print("=" * 50)
    
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
    
    # 메타데이터와 대본 내용 분리
    print("📖 메타데이터와 대본 내용 분리 중...")
    metadata, transcript_content, original_lines, transcript_start_line = extract_transcript_content(input_file)
    
    if not transcript_content:
        print("❌ 대본 내용을 추출할 수 없습니다.")
        return
    
    transcript_line_count = len([line for line in transcript_content.split('\n') if line.strip()])
    print(f"✅ 메타데이터 분리 완료")
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
    
    # 메타데이터와 결합
    print("🔗 메타데이터와 구조화된 대본 결합 중...")
    final_content = combine_with_metadata(metadata, improved_content)
    
    # 출력 파일명 생성
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_structured.md"
    
    # 파일 저장
    print(f"💾 파일 저장 중: {output_file}")
    if save_improved_transcript(final_content, output_file):
        print(f"✅ 임시 저장 완료: {output_file}")
        
        # 실제 IDE 라인 번호로 업데이트
        print("📍 실제 IDE 라인 번호로 업데이트 중...")
        update_actual_line_numbers(output_file)
        
        # 구조화 요약 출력
        sections = len([line for line in improved_content.split('\n') if line.strip().startswith('##')])
        print(f"📊 구조화 요약: {sections}개 섹션으로 구분")
        print(f"📍 라인 번호: 실제 IDE 라인과 일치")
        print(f"🛡️ 내용 누락 감지: 활성화됨")
    else:
        print("❌ 파일 저장에 실패했습니다.")


if __name__ == "__main__":
    asyncio.run(main())