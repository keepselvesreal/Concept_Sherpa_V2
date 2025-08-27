"""
생성 시간: 2025-08-27 16:50 KST
핵심 내용: 마크다운 파일에서 첫 번째 # 헤더 이전 내용을 제거하는 범용 스크립트
상세 내용:
    - main(): 메인 실행 함수, 명령행 인수 처리 및 전체 플로우 제어 (라인 20-50)
    - clean_markdown_file(input_file): 마크다운 파일 정리 메인 로직 (라인 52-85)
    - find_first_header(lines): 첫 번째 # 헤더 위치 탐지 (라인 87-100)
    - save_cleaned_file(input_file, cleaned_lines): 정리된 내용을 새 파일로 저장 (라인 102-120)
상태: active
주소: header_cleaner
참조: 신규 생성
"""

import sys
import re
from pathlib import Path
from typing import List, Optional, Tuple


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python header_cleaner.py <markdown_file.md>")
        print("Example: python header_cleaner.py source.md")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    # 파일 존재 확인
    if not input_file.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)
    
    if not input_file.suffix.lower() in ['.md', '.markdown']:
        print(f"❌ 마크다운 파일이 아닙니다: {input_file}")
        sys.exit(1)
    
    print(f"📁 처리할 파일: {input_file}")
    
    # 마크다운 파일 정리
    try:
        result = clean_markdown_file(input_file)
        if result:
            cleaned_file, removed_lines = result
            print(f"✅ 정리 완료!")
            print(f"📊 제거된 줄 수: {removed_lines}줄")
            print(f"💾 새 파일: {cleaned_file}")
        else:
            print("⚠️ 처리할 내용이 없습니다.")
    
    except Exception as e:
        print(f"❌ 처리 중 오류 발생: {str(e)}")
        sys.exit(1)


def clean_markdown_file(input_file: Path) -> Optional[Tuple[Path, int]]:
    """마크다운 파일 정리 메인 로직"""
    try:
        # 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📝 전체 줄 수: {len(lines)}줄")
        
        # 첫 번째 헤더 위치 찾기
        header_line_index = find_first_header(lines)
        
        if header_line_index is None:
            print("⚠️ # 헤더를 찾을 수 없습니다. 파일을 그대로 복사합니다.")
            cleaned_lines = lines
            removed_lines = 0
        else:
            print(f"🎯 첫 번째 헤더 위치: {header_line_index + 1}번째 줄")
            # 헤더부터 끝까지 추출
            cleaned_lines = lines[header_line_index:]
            removed_lines = header_line_index
        
        # 새 파일로 저장
        cleaned_file = save_cleaned_file(input_file, cleaned_lines)
        
        return cleaned_file, removed_lines
    
    except Exception as e:
        raise Exception(f"파일 처리 중 오류: {str(e)}")


def find_first_header(lines: List[str]) -> Optional[int]:
    """첫 번째 # 헤더 위치 탐지"""
    header_pattern = re.compile(r'^#+\s+')
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line and header_pattern.match(stripped_line):
            return i
    
    return None


def save_cleaned_file(input_file: Path, cleaned_lines: List[str]) -> Path:
    """정리된 내용을 새 파일로 저장"""
    # 출력 파일명 생성 (원본명_cleaned.md)
    output_file = input_file.parent / f"{input_file.stem}_cleaned{input_file.suffix}"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        
        print(f"💾 저장된 줄 수: {len(cleaned_lines)}줄")
        return output_file
    
    except Exception as e:
        raise Exception(f"파일 저장 중 오류: {str(e)}")


if __name__ == "__main__":
    main()