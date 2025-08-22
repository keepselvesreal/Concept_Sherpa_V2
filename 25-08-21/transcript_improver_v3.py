"""
생성 시간: 2025-08-21 16:00:30 KST
핵심 내용: 대본 내용만 Claude에게 전달하여 구조화한 후 라인 번호를 매핑하는 스크립트
상세 내용:
    - extract_transcript_content(file_path): 메타데이터와 대본 내용 분리
    - improve_transcript_with_claude(transcript_content): 순수 대본 내용만으로 Claude SDK 호출
    - map_line_numbers(improved_content, original_lines): 구조화된 결과에 실제 라인 번호 매핑
    - combine_with_metadata(metadata, improved_with_lines): 메타데이터와 개선된 대본 결합
    - main(): 메인 실행 함수
상태: 활성
주소: transcript_improver_v3
참조: transcript_improver_v2
"""

import os
import re
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

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
        
        # 메타데이터 추출
        metadata = {}
        title = ""
        in_metadata = False
        transcript_start_idx = 0
        
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line[2:].strip()
                metadata['title'] = title
            elif line.startswith('**Source Type:**'):
                metadata['source_type'] = line.split(':', 1)[1].strip()
                in_metadata = True
            elif line.startswith('**Source:**'):
                metadata['source'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Source Language:**'):
                metadata['source_language'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Structure Type:**'):
                metadata['structure_type'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Extracted Time:**'):
                metadata['extracted_time'] = line.split(':', 1)[1].strip()
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


async def improve_transcript_with_claude(transcript_content: str) -> str:
    """
    순수 대본 내용만으로 Claude Code SDK를 사용하여 구조화합니다.
    
    Args:
        transcript_content (str): 순수 대본 내용
        
    Returns:
        str: 구조화된 대본 내용
    """
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

**FORBIDDEN OPERATIONS:**
- Fix grammatical errors
- Improve incomplete sentences  
- Remove repetitive content
- Change or paraphrase original content
- Replace words or expressions

OUTPUT FORMAT:
## English Section Title

[time] Original content (with filler words removed and semantically combined)

Please follow these guidelines to only remove filler words, combine sentences by semantic units, and divide into 5-7 sections with ENGLISH section titles. Never change the original content."""

        # Claude Code SDK 호출
        response_content = ""
        async for message in query(prompt=user_prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_content += block.text
        
        return response_content.strip()
        
    except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
        print(f"❌ Claude Code SDK 오류: {str(e)}")
        return ""
    except Exception as e:
        print(f"❌ Claude SDK 호출 중 오류 발생: {str(e)}")
        return ""


def map_line_numbers(improved_content: str, original_lines: List[str], transcript_start_line: int) -> str:
    """
    구조화된 결과에 실제 파일 라인 번호를 매핑합니다.
    
    Args:
        improved_content (str): Claude가 구조화한 내용
        original_lines (List[str]): 원본 파일의 모든 라인
        transcript_start_line (int): 대본 시작 라인 번호
        
    Returns:
        str: 라인 번호가 매핑된 구조화된 내용
    """
    try:
        # 원본 파일에서 타임스탬프별 실제 라인 번호 매핑 생성 (1-based indexing)
        timestamp_to_line = {}
        for i, line in enumerate(original_lines, start=1):  # 1-based line numbering
            line = line.strip()
            if line and line.startswith('['):
                match = re.match(r'\[(\d{2}):(\d{2})\]', line)
                if match:
                    timestamp = f"[{match.group(1)}:{match.group(2)}]"
                    if timestamp not in timestamp_to_line:
                        timestamp_to_line[timestamp] = i
        
        # 구조화된 내용에 실제 라인 번호 추가
        result_lines = []
        for line in improved_content.split('\n'):
            if line.strip().startswith('##'):
                # 헤더는 그대로
                result_lines.append(line)
            elif line.strip().startswith('['):
                # 타임스탬프가 있는 라인에 실제 라인 번호 추가
                match = re.match(r'\[(\d{2}):(\d{2})\]', line.strip())
                if match:
                    timestamp = f"[{match.group(1)}:{match.group(2)}]"
                    if timestamp in timestamp_to_line:
                        actual_line_num = timestamp_to_line[timestamp]
                        result_lines.append(f"Line {actual_line_num}: {line.strip()}")
                    else:
                        result_lines.append(line)
                else:
                    result_lines.append(line)
            elif line.strip() == "":
                # 빈 라인은 그대로
                result_lines.append(line)
            else:
                # 기타 라인은 그대로
                result_lines.append(line)
        
        return '\n'.join(result_lines)
        
    except Exception as e:
        print(f"❌ 라인 번호 매핑 중 오류 발생: {str(e)}")
        return improved_content


def combine_with_metadata(metadata: Dict, improved_with_lines: str) -> str:
    """
    메타데이터와 구조화된 대본을 결합합니다.
    
    Args:
        metadata (Dict): 원본 메타데이터
        improved_with_lines (str): 라인 번호가 매핑된 구조화된 대본
        
    Returns:
        str: 최종 마크다운 내용
    """
    title = metadata.get('title', 'YouTube Transcript')
    source_type = metadata.get('source_type', 'YouTube')
    source = metadata.get('source', '')
    source_language = metadata.get('source_language', 'en')
    structure_type = metadata.get('structure_type', 'standalone')
    extracted_time = metadata.get('extracted_time', '')
    
    # 기존 필드 유지 (Structure Type 포함)
    header = f"""# {title}

**Source Type:** {source_type}
**Source:** {source}
**Source Language:** {source_language}
**Structure Type:** {structure_type}
**Extracted Time:** {extracted_time}

---

"""
    
    return header + improved_with_lines


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
    print("🤖 Claude Code SDK 대본 구조화기 v3")
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
    
    # Claude Code SDK로 대본 구조화 (전체 내용)
    print("🤖 Claude Code SDK로 전체 대본 구조화 중...")
    print("   - 필러 워드 제거")
    print("   - 의미 단위 문장 합치기")  
    print("   - 5-7개 섹션으로 구분")
    print("   - 전체 대본 처리")
    
    improved_content = await improve_transcript_with_claude(transcript_content)
    
    if not improved_content:
        print("❌ 대본 구조화에 실패했습니다.")
        return
    
    print("✅ 대본 구조화 완료")
    
    # 라인 번호 매핑
    print("📍 실제 파일 라인 번호 매핑 중...")
    improved_with_lines = map_line_numbers(improved_content, original_lines, transcript_start_line)
    print("✅ 라인 번호 매핑 완료")
    
    # 메타데이터와 결합
    print("🔗 메타데이터와 구조화된 대본 결합 중...")
    final_content = combine_with_metadata(metadata, improved_with_lines)
    
    # 출력 파일명 생성
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_structured.md"
    
    # 파일 저장
    print(f"💾 파일 저장 중: {output_file}")
    if save_improved_transcript(final_content, output_file):
        print(f"✅ 성공적으로 저장되었습니다: {output_file}")
        
        # 구조화 요약 출력
        sections = len([line for line in improved_content.split('\n') if line.strip().startswith('##')])
        print(f"📊 구조화 요약: {sections}개 섹션으로 구분")
        print(f"📍 라인 번호: 원본 파일과 매핑됨")
    else:
        print("❌ 파일 저장에 실패했습니다.")


if __name__ == "__main__":
    asyncio.run(main())