#!/usr/bin/env python3
"""
생성 시간: 2025-11-01 10:00 KST
핵심 내용: toc.md를 파싱하여 섹션 번호-파일 경로 매핑 JSON 생성
상세 내용:
  - slugify(text): 섹션 제목을 파일명으로 변환 (라인 20-32)
  - generate_section_mapping(toc_path, chapters_dir, output_path): 매핑 JSON 생성 (라인 35-110)
상태: active
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict


def slugify(text: str) -> str:
    """
    섹션 제목을 파일명 형식으로 변환 (kebab-case)

    Args:
        text: 섹션 제목 (예: "Software Development as a Learning Process")

    Returns:
        str: 파일명 (예: "software-development-as-a-learning-process")
    """
    # 소문자 변환 및 특수문자 제거
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def generate_section_mapping(toc_path: str, chapters_dir: str, output_path: str) -> None:
    """
    toc.md를 파싱하여 섹션 번호-파일 경로 매핑 JSON 생성

    Args:
        toc_path: toc.md 파일 경로
        chapters_dir: 장 폴더들이 있는 디렉토리
        output_path: 출력 JSON 파일 경로
    """
    toc_file = Path(toc_path)
    if not toc_file.exists():
        print(f"오류: {toc_path}를 찾을 수 없습니다")
        return

    chapters_path = Path(chapters_dir)
    if not chapters_path.exists():
        print(f"오류: {chapters_dir}를 찾을 수 없습니다")
        return

    # toc.md 읽기
    content = toc_file.read_text(encoding="utf-8")
    lines = content.split('\n')

    # 섹션 매핑 저장
    section_mapping = {}
    current_chapter = None

    for line in lines:
        # Chapter 라인 파싱 (## 1. Chapter 1: Title)
        chapter_match = re.match(r'^## (\d+)\. (Chapter \d+: .+) \(p\..+\)$', line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            continue

        # Section 라인 파싱 (### 1.1 Section Title (p.X))
        section_match = re.match(r'^### (\d+\.\d+) (.+) \(p\..+\)$', line)
        if section_match and current_chapter:
            section_num = section_match.group(1)
            section_title = section_match.group(2)

            # 파일명 생성
            filename = slugify(section_title) + ".md"

            # 파일 경로 구성
            chapter_folder = f"chapter-{current_chapter}"
            file_path = f"{chapters_dir}/{chapter_folder}/{filename}"

            # 실제 파일 존재 여부 확인
            full_path = Path(file_path)
            if not full_path.exists():
                print(f"⚠️  경고: 파일이 존재하지 않음 - {file_path}")
                print(f"    섹션: {section_num} {section_title}")
                # 존재하지 않아도 매핑에는 추가 (나중에 파일 생성 가능)

            # 매핑 저장
            section_mapping[section_num] = {
                "title": section_title,
                "path": file_path
            }

    # JSON 파일로 저장
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open('w', encoding='utf-8') as f:
        json.dump(section_mapping, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 성공: {output_path}에 섹션 매핑을 저장했습니다")
    print(f"  - 총 섹션 수: {len(section_mapping)}개")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("사용법: python generate_section_mapping.py <toc_path> <chapters_dir> <output_json>")
        print("예시: python generate_section_mapping.py toc.md ./chapters section_mapping.json")
        sys.exit(1)

    toc_path = sys.argv[1]
    chapters_dir = sys.argv[2]
    output_path = sys.argv[3]

    generate_section_mapping(toc_path, chapters_dir, output_path)
