#!/usr/bin/env python3
"""
생성 시간: 2025. 10. 31. (금) 16:26:40 KST
핵심 내용: toc.md를 기반으로 각 장의 content.md를 섹션별로 분할하여 별도 파일로 저장

상세 내용:
    - parse_toc(toc_path: str) -> dict (라인 1-50): toc.md 파싱하여 장/섹션 구조 추출
    - parse_content_pages(content_path: str) -> dict (라인 52-100): content.md에서 페이지별 내용 추출
    - extract_section_content(pages: dict, start_page: int, end_page: int) -> str (라인 102-130): 페이지 범위로 섹션 내용 추출
    - slugify(text: str) -> str (라인 132-145): 제목을 파일명으로 변환
    - split_chapters(base_dir: str) (라인 147-250): 전체 장 처리 메인 로직

상태: active
참조: None
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def parse_toc(toc_path: str) -> Dict[str, List[Dict]]:
    """
    toc.md를 파싱하여 장과 섹션 정보를 추출합니다.

    Returns:
        {
            'chapter-1': {
                'title': 'What Is the Point of Test-Driven Development?',
                'page_range': (3, 11),  # 장 전체 범위
                'sections': [
                    {'title': 'Software Development as a Learning Process', 'page': 3},
                    {'title': 'Feedback Is the Fundamental Tool', 'page': 4},
                    ...
                ]
            },
            ...
        }
    """
    with open(toc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chapters = {}
    current_chapter = None
    chapter_num = 0

    for i, line in enumerate(lines):
        line = line.strip()

        # Chapter 라인 매칭: ## Chapter N: Title (p.X)
        chapter_match = re.match(r'^##\s+Chapter\s+(\d+):\s+(.+?)\s+\(p\.(\d+)\)$', line)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            chapter_title = chapter_match.group(2)
            chapter_page = int(chapter_match.group(3))

            current_chapter = f'chapter-{chapter_num}'
            chapters[current_chapter] = {
                'title': chapter_title,
                'start_page': chapter_page,
                'sections': []
            }
            continue

        # Section 라인 매칭: ### Section Title (p.X)
        if current_chapter:
            section_match = re.match(r'^###\s+(.+?)\s+\(p\.(\d+)\)$', line)
            if section_match:
                section_title = section_match.group(1)
                section_page = int(section_match.group(2))
                chapters[current_chapter]['sections'].append({
                    'title': section_title,
                    'page': section_page
                })

    # 각 장의 종료 페이지 계산 (다음 장 시작 - 1)
    chapter_keys = sorted(chapters.keys(), key=lambda x: chapters[x]['start_page'])
    for i, key in enumerate(chapter_keys):
        if i + 1 < len(chapter_keys):
            next_key = chapter_keys[i + 1]
            chapters[key]['end_page'] = chapters[next_key]['start_page'] - 1
        else:
            # 마지막 장은 임시로 큰 값 설정 (실제 content에서 결정됨)
            chapters[key]['end_page'] = 9999

    return chapters


def parse_content_pages(content_path: str) -> Dict[int, str]:
    """
    content.md 파일을 페이지별로 파싱합니다.

    Returns:
        {page_num: content_text, ...}
    """
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # **Page N** 패턴으로 분할
    page_pattern = r'\*\*Page (\d+)\*\*'

    pages = {}
    matches = list(re.finditer(page_pattern, content))

    for i, match in enumerate(matches):
        page_num = int(match.group(1))
        start_pos = match.end()

        # 다음 페이지 시작 위치 찾기
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        page_content = content[start_pos:end_pos].strip()
        pages[page_num] = page_content

    return pages


def extract_section_content(pages: Dict[int, str], start_page: int, end_page: int) -> str:
    """
    페이지 범위로 섹션 내용을 추출합니다.
    보수적 추출: end_page를 포함합니다.
    """
    content_parts = []

    for page in range(start_page, end_page + 1):
        if page in pages:
            content_parts.append(f"**Page {page}**\n\n{pages[page]}")

    return "\n\n---\n".join(content_parts)


def slugify(text: str) -> str:
    """
    제목을 파일명으로 변환합니다.
    예: "A Minimal Introduction to JUnit 4" -> "a-minimal-introduction-to-junit-4"
    """
    # 소문자로 변환
    text = text.lower()
    # 특수문자를 하이픈으로 변환
    text = re.sub(r'[^\w\s-]', '', text)
    # 공백을 하이픈으로 변환
    text = re.sub(r'[\s_]+', '-', text)
    # 연속된 하이픈 제거
    text = re.sub(r'-+', '-', text)
    # 앞뒤 하이픈 제거
    return text.strip('-')


def split_chapters(base_dir: str):
    """
    모든 장의 content.md를 섹션별로 분할합니다.
    """
    base_path = Path(base_dir)
    toc_path = base_path / 'toc.md'
    book_dir = base_path / 'scouting/growing-object-oriented-software'

    if not toc_path.exists():
        print(f"❌ toc.md not found at {toc_path}")
        return

    print("📖 Parsing toc.md...")
    chapters = parse_toc(str(toc_path))

    print(f"✅ Found {len(chapters)} chapters\n")

    total_files = 0

    for chapter_key, chapter_info in sorted(chapters.items(),
                                           key=lambda x: x[1]['start_page']):
        chapter_dir = book_dir / chapter_key
        content_path = chapter_dir / 'content.md'

        if not content_path.exists():
            print(f"⚠️  Skipping {chapter_key}: content.md not found")
            continue

        print(f"📄 Processing {chapter_key}: {chapter_info['title']}")

        # content.md 파싱
        pages = parse_content_pages(str(content_path))

        if not pages:
            print(f"   ⚠️  No pages found in content.md")
            continue

        # 실제 장의 종료 페이지 업데이트
        max_page = max(pages.keys())
        if chapter_info['end_page'] == 9999:
            chapter_info['end_page'] = max_page

        sections = chapter_info['sections']

        if not sections:
            print(f"   ℹ️  No sections defined in toc.md")
            continue

        # 각 섹션 추출
        for i, section in enumerate(sections):
            section_title = section['title']
            start_page = section['page']

            # 다음 섹션의 시작 페이지 결정 (보수적 추출: 다음 페이지 포함)
            if i + 1 < len(sections):
                end_page = sections[i + 1]['page']
            else:
                # 마지막 섹션은 장의 끝까지
                end_page = chapter_info['end_page']

            # 섹션 내용 추출
            section_content = extract_section_content(pages, start_page, end_page)

            if not section_content:
                print(f"   ⚠️  No content for section: {section_title}")
                continue

            # 파일명 생성
            filename = f"{slugify(section_title)}.md"
            output_path = chapter_dir / filename

            # 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {section_title} (pp.{start_page}-{end_page})\n\n")
                f.write("---\n")
                f.write(section_content)

            print(f"   ✅ Created: {filename} (pages {start_page}-{end_page})")
            total_files += 1

        print()

    print(f"🎉 Done! Created {total_files} section files.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = '/home/nadle/para/projects/ai-powered-development/knowledge-sherpa/Concept_Sherpa_V2'

    split_chapters(base_dir)
