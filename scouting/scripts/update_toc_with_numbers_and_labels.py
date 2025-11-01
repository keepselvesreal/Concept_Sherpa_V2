#!/usr/bin/env python3
"""
생성 시간: 2025-11-01 09:50 KST
핵심 내용: toc.md에 섹션 번호 추가 및 페이지 레이블 변환을 통합 처리
상세 내용:
  - get_page_label(doc, page_index): PDF 페이지 레이블 추출 (라인 18-30)
  - update_toc_with_numbers_and_labels(pdf_path, toc_path): toc.md 통합 업데이트 (라인 33-100)
상태: active
"""

import sys
from pathlib import Path
import fitz  # PyMuPDF
import re


def get_page_label(doc, page_index: int) -> str:
    """
    페이지의 실제 책 페이지 번호 추출 (페이지 레이블)

    Args:
        doc: fitz Document 객체
        page_index: 페이지 인덱스 (0-indexed)

    Returns:
        str: 페이지 레이블 (예: "3", "xv", "Cover" 등)
    """
    try:
        page = doc[page_index]
        label = page.get_label()
        return label if label else str(page_index + 1)
    except:
        return str(page_index + 1)


def update_toc_with_numbers_and_labels(pdf_path: str, toc_path: str) -> None:
    """
    toc.md에 섹션 번호 추가 및 PDF 페이지 번호를 인쇄된 페이지 레이블로 변환

    Args:
        pdf_path: PDF 파일 경로
        toc_path: toc.md 파일 경로
    """
    # PDF 문서 열기
    doc = fitz.open(pdf_path)

    # toc.md 읽기
    toc_file = Path(toc_path)
    if not toc_file.exists():
        print(f"오류: {toc_path}를 찾을 수 없습니다")
        doc.close()
        return

    content = toc_file.read_text(encoding="utf-8")
    lines = content.split('\n')

    # 섹션 번호 카운터
    chapter_num = 0
    section_num = 0

    # 각 라인 처리
    updated_lines = []
    for line in lines:
        updated_line = line

        # Chapter 라인 처리 (## Chapter X:)
        chapter_match = re.match(r'^(## )(Chapter \d+:.+)$', line)
        if chapter_match:
            chapter_num += 1
            section_num = 0  # 섹션 카운터 리셋
            prefix = chapter_match.group(1)
            title_part = chapter_match.group(2)
            updated_line = f"{prefix}{chapter_num}. {title_part}"

        # Section 라인 처리 (### Section Title)
        elif re.match(r'^###\s+.+$', line):
            section_num += 1
            # ### 다음의 공백을 제거하고 제목 추출
            section_title = re.sub(r'^###\s+', '', line)
            updated_line = f"### {chapter_num}.{section_num} {section_title}"

        # 페이지 번호를 페이지 레이블로 변환
        page_match = re.search(r'\(p\.(\d+)\)$', updated_line)
        if page_match:
            pdf_page_num = int(page_match.group(1))
            page_index = pdf_page_num - 1  # 0-indexed
            page_label = get_page_label(doc, page_index)
            updated_line = re.sub(r'\(p\.\d+\)$', f'(p.{page_label})', updated_line)

        updated_lines.append(updated_line)

    # 업데이트된 내용 저장
    updated_content = '\n'.join(updated_lines)
    toc_file.write_text(updated_content, encoding="utf-8")

    print(f"✓ 성공: {toc_path}를 업데이트했습니다")
    print(f"  - 추가된 장 번호: {chapter_num}개")
    print(f"  - 섹션 번호 및 페이지 레이블 변환 완료")

    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python update_toc_with_numbers_and_labels.py <pdf_path> <toc_path>")
        print("예시: python update_toc_with_numbers_and_labels.py book.pdf toc.md")
        sys.exit(1)

    pdf_path = sys.argv[1]
    toc_path = sys.argv[2]

    # PDF 파일 존재 여부 확인
    if not Path(pdf_path).exists():
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    update_toc_with_numbers_and_labels(pdf_path, toc_path)
