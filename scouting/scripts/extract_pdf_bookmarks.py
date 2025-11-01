#!/usr/bin/env python3
"""
PDF 북마크를 추출해서 마크다운으로 저장하는 스크립트

생성 시간: 2025-10-31
핵심 내용: PDF의 북마크/아웃라인을 마크다운 헤딩 구조로 변환하여 저장
상태: active
"""

import sys
from pathlib import Path
import fitz  # PyMuPDF


def extract_pdf_bookmarks(pdf_path: str, output_md_path: str) -> None:
    """
    PDF 북마크를 추출해서 마크다운 파일로 저장

    Args:
        pdf_path: PDF 파일 경로
        output_md_path: 출력 마크다운 파일 경로
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    # PDF 파일 열기
    doc = fitz.open(pdf_file)

    # TOC(Table of Contents) 추출
    toc = doc.get_toc()

    if not toc:
        print("오류: PDF에 북마크가 없습니다")
        sys.exit(1)

    # 마크다운으로 변환
    markdown_lines = []
    for level, title, page_num in toc:
        # level은 1부터 시작 (1 = H1, 2 = H2, 등)
        heading = "#" * level
        markdown_lines.append(f"{heading} {title} (p.{page_num})")

    # 마크다운 파일로 저장
    output_file = Path(output_md_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n\n".join(markdown_lines), encoding="utf-8")

    print(f"✓ 성공: {output_file}에 저장했습니다")
    print(f"✓ 추출된 북마크: {len(toc)}개")

    # 문서 종료
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python extract_pdf_bookmarks.py <pdf_path> <output_md_path>")
        print("예시: python extract_pdf_bookmarks.py book.pdf book_toc.md")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_md_path = sys.argv[2]
    extract_pdf_bookmarks(pdf_path, output_md_path)
