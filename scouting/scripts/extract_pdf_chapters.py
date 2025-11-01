#!/usr/bin/env python3
"""
PDF의 각 장 내용을 추출해서 폴더 구조로 저장하는 스크립트

생성 시간: 2025-10-31
핵심 내용: toc.md 기반으로 PDF의 각 Chapter를 개별 폴더에 content.md로 저장
상세 내용:
  - extract_chapters_from_toc(): toc.md에서 Chapter 정보 추출 (라인 20-65)
  - get_page_label(): 페이지 레이블 추출 (라인 68-80)
  - extract_text_with_format(): 페이지 범위의 텍스트 추출 (라인 83-125)
  - create_folder_structure(): 폴더 구조 생성 및 파일 저장 (라인 128-175)
상태: active
"""

import sys
from pathlib import Path
import fitz  # PyMuPDF
import re


def extract_chapters_from_toc(toc_path: str) -> list:
    """
    toc.md 파일에서 Chapter별 정보 추출 (Part 정보 활용하여 정확한 범위 계산)

    Args:
        toc_path: toc.md 파일 경로

    Returns:
        list: [{'chapter_num': 1, 'title': '...', 'start_bookmark': X, 'end_bookmark': Y}, ...]
    """
    toc_file = Path(toc_path)
    if not toc_file.exists():
        print(f"오류: {toc_path}를 찾을 수 없습니다")
        return []

    content = toc_file.read_text(encoding="utf-8")
    lines = content.split('\n')

    # Chapter와 Part를 추출
    chapters = []
    parts = []

    for line in lines:
        # Chapter 라인 찾기: "## Chapter N: ... (p.XXX)" 또는 (p.xxx) 같은 로마자
        chapter_match = re.match(r'##\s+Chapter\s+(\d+):\s+(.+?)\s+\(p\.([ivxlcdmIVXLCDM\d]+)\)', line)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            title = f"Chapter {chapter_num}: {chapter_match.group(2)}"
            page_str = chapter_match.group(3)
            # 숫자인지 확인
            try:
                page_num = int(page_str)
                chapters.append({
                    'chapter_num': chapter_num,
                    'title': title,
                    'bookmark_page': page_num
                })
            except ValueError:
                # 로마자 페이지는 스킵
                pass

        # Part 라인 찾기: "# Part I: ... (p.XXX)" 또는 "# Part II: ... (p.XXX)"
        part_match = re.match(r'#\s+Part\s+[IVX]+:\s+.+?\s+\(p\.([ivxlcdmIVXLCDM\d]+)\)', line)
        if part_match:
            page_str = part_match.group(1)
            try:
                page_num = int(page_str)
                parts.append({
                    'type': 'part',
                    'page': page_num
                })
            except ValueError:
                # 로마자 페이지는 스킵
                pass

    # 각 장의 시작/종료 북마크 페이지 설정 (Part 정보 활용)
    chapter_info = []
    for i, ch in enumerate(chapters):
        start_bookmark = ch['bookmark_page']

        # 다음 Chapter나 Part 중 가장 먼저 나오는 것의 이전 페이지를 끝으로 설정
        next_page = 999

        # 다음 Chapter 확인
        if i + 1 < len(chapters):
            next_page = min(next_page, chapters[i + 1]['bookmark_page'])

        # 현재 Chapter 이후의 Part 확인
        for part in parts:
            if part['page'] > start_bookmark:
                next_page = min(next_page, part['page'])

        end_bookmark = next_page - 1

        chapter_info.append({
            'chapter_num': ch['chapter_num'],
            'title': ch['title'],
            'start_bookmark': start_bookmark,
            'end_bookmark': end_bookmark,
            'start_page': start_bookmark - 1,  # 0-indexed (PDF 페이지로 변환 필요)
            'end_page': end_bookmark - 1  # 0-indexed (PDF 페이지로 변환 필요)
        })

    return chapter_info


def get_page_label(doc, page_index: int) -> str:
    """
    페이지의 실제 책 페이지 번호 추출 (페이지 레이블)

    Args:
        doc: fitz Document 객체
        page_index: 페이지 인덱스 (0-indexed)

    Returns:
        str: 페이지 레이블 (예: "3", "12", 등)
    """
    try:
        page = doc[page_index]
        label = page.get_label()
        return label if label else str(page_index + 1)
    except:
        return str(page_index + 1)


def extract_text_with_format(pdf_path: str, start_page: int, end_page: int, chapter_title: str) -> str:
    """
    페이지 범위의 텍스트 추출 (인쇄된 페이지 정보 포함)

    Args:
        pdf_path: PDF 파일 경로
        start_page: 시작 페이지 (0-indexed)
        end_page: 종료 페이지 (0-indexed)
        chapter_title: 장 제목

    Returns:
        str: 추출된 텍스트 (마크다운 형식, 인쇄된 페이지 번호 포함)
    """
    doc = fitz.open(pdf_path)

    # 시작과 종료 페이지의 레이블 가져오기
    start_label = get_page_label(doc, start_page)
    end_label = get_page_label(doc, end_page)

    # 제목 추가 (인쇄된 페이지 번호, pp. 형식)
    text = f"# {chapter_title} (pp.{start_label}-{end_label})\n\n"

    # 각 페이지에서 텍스트 추출
    for page_num in range(start_page, end_page + 1):
        page = doc[page_num]
        page_text = page.get_text()
        page_label = get_page_label(doc, page_num)

        # 페이지 번호를 먼저 표시하고, 그 다음에 페이지 내용 추가
        text += f"---\n**Page {page_label}**\n\n"
        text += page_text
        text += "\n\n"

    doc.close()
    return text


def build_label_to_index_map(doc) -> dict:
    """
    페이지 레이블 → PDF 인덱스 매핑 생성

    Args:
        doc: fitz Document 객체

    Returns:
        dict: {page_label: page_index} 매핑
    """
    label_map = {}
    for i in range(doc.page_count):
        label = get_page_label(doc, i)
        # 숫자 레이블만 매핑 (로마자는 제외)
        try:
            int(label)
            label_map[label] = i
        except ValueError:
            pass
    return label_map


def create_folder_structure(pdf_path: str, toc_path: str, output_base_dir: str) -> None:
    """
    toc.md 기반으로 PDF의 각 Chapter별 폴더 구조 생성 및 content.md 저장

    Args:
        pdf_path: PDF 파일 경로
        toc_path: toc.md 파일 경로
        output_base_dir: 출력 기본 디렉토리
    """
    doc = fitz.open(pdf_path)

    # 페이지 레이블 → 인덱스 매핑 생성
    label_to_index = build_label_to_index_map(doc)

    chapters = extract_chapters_from_toc(toc_path)

    if not chapters:
        print("오류: toc.md에서 Chapter를 찾을 수 없습니다")
        return

    base_path = Path(output_base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    for ch in chapters:
        # 폴더명: chapter-1, chapter-2, ...
        folder_name = f"chapter-{ch['chapter_num']}"
        chapter_dir = base_path / folder_name
        chapter_dir.mkdir(exist_ok=True)

        # 인쇄된 페이지 번호 → PDF 인덱스 변환
        start_label = str(ch['start_bookmark'])
        end_label = str(ch['end_bookmark'])

        start_page = label_to_index.get(start_label, ch['start_page'])
        end_page = label_to_index.get(end_label, ch['end_page'])

        # 실제 페이지 인덱스 계산 (끝 페이지가 문서를 넘어가면 실제 문서 끝)
        actual_end_page = min(end_page, doc.page_count - 1)

        # content.md에 장 내용 저장
        content = extract_text_with_format(
            pdf_path,
            start_page,
            actual_end_page,
            ch['title']
        )

        content_file = chapter_dir / "content.md"
        content_file.write_text(content, encoding="utf-8")

        # 실제 페이지 레이블로 출력
        actual_start_label = get_page_label(doc, start_page)
        actual_end_label = get_page_label(doc, actual_end_page)
        print(f"✓ {folder_name}/content.md 저장됨 (pp.{actual_start_label}-{actual_end_label})")

    doc.close()
    print(f"\n✓ 완료: 총 {len(chapters)}개 장을 저장했습니다")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("사용법: python extract_pdf_chapters.py <pdf_path> <toc_path> <output_base_dir>")
        print("예시: python extract_pdf_chapters.py book.pdf toc.md ./scouting/growing-object-oriented-software")
        sys.exit(1)

    pdf_path = sys.argv[1]
    toc_path = sys.argv[2]
    output_base_dir = sys.argv[3]
    create_folder_structure(pdf_path, toc_path, output_base_dir)
