"""
생성 시간: 2025-08-21 15:45:30 KST
핵심 내용: Claude SDK를 사용하여 YouTube 대본을 적절한 단위로 합치고 필러 워드를 제거하며 구조화하는 스크립트
상세 내용:
    - parse_transcript(file_path): 마크다운 파일에서 대본 데이터 파싱
    - improve_transcript_with_claude(transcript_entries): Claude SDK로 대본 개선 (필러 워드 제거, 구조화)
    - format_improved_transcript(improved_content, original_metadata): 개선된 대본을 마크다운으로 포맷팅
    - save_improved_transcript(content, output_file): 개선된 대본 저장
    - main(): 메인 실행 함수
상태: 활성
주소: transcript_improver
참조: youtube_transcript_extractor_v2
"""

import os
import re
import sys
import json
import asyncio
from datetime import datetime
from anthropic import Anthropic
from typing import List, Dict, Tuple


def parse_transcript(file_path: str) -> Tuple[Dict, List[Dict]]:
    """
    마크다운 파일에서 메타데이터와 대본 데이터를 파싱합니다.
    
    Args:
        file_path (str): 마크다운 파일 경로
        
    Returns:
        tuple: (metadata, transcript_entries)
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
            elif line.startswith('**Extracted Time:**'):
                metadata['extracted_time'] = line.split(':', 1)[1].strip()
            elif line.strip() == '---' and in_metadata:
                transcript_start_idx = i + 1
                break
        
        # 대본 데이터 추출 (라인 번호 포함)
        transcript_entries = []
        for line_idx, line in enumerate(lines[transcript_start_idx:], start=transcript_start_idx + 1):
            line = line.strip()
            if line and line.startswith('['):
                # [MM:SS] 형식의 타임스탬프와 텍스트 분리
                match = re.match(r'\[(\d{2}):(\d{2})\] (.+)', line)
                if match:
                    minutes = int(match.group(1))
                    seconds = int(match.group(2))
                    text = match.group(3).strip()
                    start_time = minutes * 60 + seconds
                    
                    transcript_entries.append({
                        'start': start_time,
                        'text': text,
                        'timestamp': f"[{minutes:02d}:{seconds:02d}]",
                        'line_number': line_idx
                    })
        
        return metadata, transcript_entries
        
    except Exception as e:
        print(f"❌ 파일 파싱 중 오류 발생: {str(e)}")
        return {}, []


def improve_transcript_with_claude(transcript_entries: List[Dict]) -> str:
    """
    Claude SDK를 사용하여 대본을 개선합니다.
    
    Args:
        transcript_entries (list): 대본 항목 리스트
        
    Returns:
        str: 개선된 대본 내용
    """
    try:
        # Claude Code 환경에서 Anthropic 클라이언트 초기화 (API 키 불필요)
        client = Anthropic()
        
        # 대본 텍스트 준비
        transcript_text = ""
        for entry in transcript_entries:
            transcript_text += f"Line {entry['line_number']}: {entry['timestamp']} {entry['text']}\n"
        
        # Claude에게 대본 개선 요청
        system_prompt = """당신은 YouTube 대본을 구조화하는 전문가입니다. 
주어진 대본에서 다음 작업만 수행해주세요:

**허용되는 작업:**
1. 의미적으로 연관된 문장들을 적절한 단위로 합치기
2. 필러 워드 제거 (um, uh, ah, you know, like 등)
3. 내용을 고려하여 5-7개 섹션으로 구분하고 ## 제목 추가
4. 각 합쳐진 문장의 시작 시간을 [MM:SS] 형식으로 표시
5. 각 문장 앞에 라인 번호 유지

**금지되는 작업:**
- 문법적 오류 수정
- 불완전한 문장 개선
- 반복 내용 제거
- 원문 내용 변경이나 의역
- 단어나 표현 바꾸기

출력 형식:
## 섹션 제목

Line X: [시간] 원문 내용 (필러 워드만 제거)

예시:
## Introduction to Claude Code Output Styles

Line 10: [00:00] engineers. Here we have six cloud code instances. In each instance we have six unique output styles.

Line 11: [00:25] Honestly, when I first saw the output styles feature drop, my first thought was, "This is useless."
"""

        user_prompt = f"""다음 YouTube 대본을 구조화해주세요:

{transcript_text}

위의 지침에 따라 필러 워드만 제거하고 의미 단위로 문장을 합치며 5-7개 섹션으로 구분해주세요. 원문 내용은 절대 변경하지 마세요."""

        # Claude API 호출
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.1,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"❌ Claude SDK 호출 중 오류 발생: {str(e)}")
        return ""


def format_improved_transcript(improved_content: str, original_metadata: Dict) -> str:
    """
    개선된 대본을 마크다운 형식으로 포맷팅합니다.
    
    Args:
        improved_content (str): Claude가 개선한 대본 내용
        original_metadata (dict): 원본 메타데이터
        
    Returns:
        str: 포맷팅된 마크다운 내용
    """
    title = original_metadata.get('title', 'YouTube Transcript')
    source_type = original_metadata.get('source_type', 'YouTube')
    source = original_metadata.get('source', '')
    source_language = original_metadata.get('source_language', 'en')
    extracted_time = original_metadata.get('extracted_time', '')
    
    # 기존 필드만 유지
    header = f"""# {title}

**Source Type:** {source_type}
**Source:** {source}
**Source Language:** {source_language}
**Extracted Time:** {extracted_time}

---

"""
    
    # 개선된 내용 그대로 사용
    full_content = header + improved_content.strip()
    return full_content


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


def main():
    """
    메인 실행 함수
    """
    print("🤖 Claude SDK 대본 구조화기")
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
    
    # Claude Code 환경에서는 API 키 체크 불필요
    print("🔑 Claude Code 환경에서 실행 중...")
    
    # 대본 파싱
    print("📖 대본 파싱 중...")
    metadata, transcript_entries = parse_transcript(input_file)
    
    if not transcript_entries:
        print("❌ 대본 데이터를 파싱할 수 없습니다.")
        return
    
    print(f"✅ {len(transcript_entries)}개의 대본 항목 파싱 완료")
    
    # Claude SDK로 대본 구조화
    print("🤖 Claude SDK로 대본 구조화 중...")
    print("   - 필러 워드 제거")
    print("   - 의미 단위 문장 합치기")
    print("   - 5-7개 섹션으로 구분")
    print("   - 라인 번호 유지")
    
    improved_content = improve_transcript_with_claude(transcript_entries)
    
    if not improved_content:
        print("❌ 대본 구조화에 실패했습니다.")
        return
    
    print("✅ 대본 구조화 완료")
    
    # 구조화된 대본 포맷팅
    print("📄 구조화된 대본 포맷팅 중...")
    formatted_content = format_improved_transcript(improved_content, metadata)
    
    # 출력 파일명 생성
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_structured.md"
    
    # 파일 저장
    print(f"💾 파일 저장 중: {output_file}")
    if save_improved_transcript(formatted_content, output_file):
        print(f"✅ 성공적으로 저장되었습니다: {output_file}")
        
        # 구조화 요약 출력
        sections = len([line for line in improved_content.split('\n') if line.strip().startswith('##')])
        print(f"📊 구조화 요약: {sections}개 섹션으로 구분")
    else:
        print("❌ 파일 저장에 실패했습니다.")


if __name__ == "__main__":
    main()