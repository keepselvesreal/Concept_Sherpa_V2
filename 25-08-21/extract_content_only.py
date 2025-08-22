#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 12:45:15
핵심 내용: MD 파일에서 메타데이터를 제외하고 순수 내용만 추출하는 스크립트
상세 내용: 
    - main() (line 15): 메인 실행 함수, 명령행 인수 처리
    - extract_content() (line 35): 메타데이터 영역을 제외하고 본문 내용만 추출
    - clean_content() (line 65): 추출된 내용을 정리 (빈 줄 정리 등)
상태: active
참조: Engineers… Claude Code Output Styles Are Here. Don_mJhsWrEv-Go_structured.md
"""

import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python extract_content_only.py <markdown_file>")
        sys.exit(1)
    
    md_file_path = Path(sys.argv[1])
    
    if not md_file_path.exists():
        print(f"Error: File {md_file_path} not found")
        sys.exit(1)
    
    # MD 파일 읽기
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 순수 내용만 추출
    extracted_content = extract_content(content)
    cleaned_content = clean_content(extracted_content)
    
    # 출력 파일명 생성 (원본 파일명 기반)
    base_name = md_file_path.stem
    # 새로운 파일명 형식(날짜_순번_id)에서 확장자 부분만 변경
    output_file = md_file_path.parent / f"{base_name}_content_only.md"
    
    # 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Content extracted from: {md_file_path}")
    print(f"Content saved to: {output_file}")
    print(f"Content length: {len(cleaned_content)} characters")


def extract_content(content):
    """메타데이터 영역을 제외하고 본문 내용만 추출"""
    lines = content.split('\n')
    content_lines = []
    skip_metadata = True
    
    for line in lines:
        # 첫 번째 --- 구분자를 만나면 메타데이터 영역 끝
        if line.strip() == '---' and skip_metadata:
            skip_metadata = False
            continue
        
        # 메타데이터 영역이 끝난 후의 내용만 수집
        if not skip_metadata:
            content_lines.append(line)
    
    return '\n'.join(content_lines)


def clean_content(content):
    """추출된 내용을 정리 (연속된 빈 줄 정리, 앞뒤 공백 제거)"""
    lines = content.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        # 빈 줄 처리
        if line.strip() == '':
            if not prev_empty:  # 연속된 빈 줄 중 첫 번째만 유지
                cleaned_lines.append('')
                prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    
    # 맨 앞과 뒤의 빈 줄 제거
    while cleaned_lines and cleaned_lines[0].strip() == '':
        cleaned_lines.pop(0)
    
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()
    
    return '\n'.join(cleaned_lines)


if __name__ == "__main__":
    main()