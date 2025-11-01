#!/usr/bin/env python3
"""
생성 시간: 2025. 10. 31. (금) 16:47:13 KST
핵심 내용: 섹션별 마크다운 파일의 각 줄 앞에 줄 번호 추가

상세 내용:
    - add_line_numbers_to_file(file_path: str) (라인 1-30): 파일에 줄 번호 추가
    - process_all_sections(base_dir: str) (라인 32-80): 모든 섹션 파일 처리

상태: active
참조: None
"""

from pathlib import Path
from typing import List


def add_line_numbers_to_file(file_path: Path) -> bool:
    """
    파일의 각 줄 앞에 줄 번호를 추가합니다.
    형식: "Line1 원본내용"

    Returns:
        성공 여부
    """
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 줄 번호 추가
        numbered_lines = []
        for i, line in enumerate(lines, start=1):
            # 개행 문자 제거 후 줄 번호 추가
            line_content = line.rstrip('\n\r')
            numbered_line = f"Line{i} {line_content}\n"
            numbered_lines.append(numbered_line)

        # 파일 덮어쓰기
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(numbered_lines)

        return True

    except Exception as e:
        print(f"   ❌ Error processing {file_path.name}: {e}")
        return False


def process_all_sections(base_dir: str):
    """
    모든 섹션 파일에 줄 번호를 추가합니다.
    content.md는 제외합니다.
    """
    base_path = Path(base_dir)
    book_dir = base_path / 'scouting/growing-object-oriented-software'

    if not book_dir.exists():
        print(f"❌ Directory not found: {book_dir}")
        return

    print("🔢 Adding line numbers to section files...\n")

    total_files = 0
    success_count = 0

    # 모든 chapter 디렉토리 순회
    chapter_dirs = sorted([d for d in book_dir.iterdir()
                          if d.is_dir() and d.name.startswith('chapter-')],
                         key=lambda x: int(x.name.split('-')[1]))

    for chapter_dir in chapter_dirs:
        print(f"📁 Processing {chapter_dir.name}")

        # content.md를 제외한 모든 .md 파일 찾기
        section_files = [f for f in chapter_dir.glob('*.md')
                        if f.name != 'content.md']

        if not section_files:
            print(f"   ℹ️  No section files found")
            continue

        for section_file in sorted(section_files):
            total_files += 1

            if add_line_numbers_to_file(section_file):
                print(f"   ✅ {section_file.name}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {section_file.name}")

        print()

    print(f"🎉 Done! Processed {success_count}/{total_files} files successfully.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = '/home/nadle/para/projects/ai-powered-development/knowledge-sherpa/Concept_Sherpa_V2'

    process_all_sections(base_dir)
