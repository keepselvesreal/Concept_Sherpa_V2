#!/usr/bin/env python3
"""
toc.md의 페이지 번호를 인쇄된 페이지 레이블로 변환

생성 시간: 2025-10-31
핵심 내용: PDF 페이지 번호를 책에 인쇄된 페이지 번호(레이블)로 변환하여 toc.md 업데이트
상세 내용:
  - get_page_label(): 페이지 레이블 추출 (라인 18-30)
  - update_toc_to_labels(): toc.md 업데이트 (라인 33-70)
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
        str: 페이지 레이블 (예: "3", "21", 등)
    """
    try:
        page = doc[page_index]
        label = page.get_label()
        return label if label else str(page_index + 1)
    except:
        return str(page_index + 1)


def update_toc_to_labels(pdf_path: str, toc_path: str) -> None:
    """
    toc.md의 PDF 페이지 번호를 인쇄된 페이지 레이블로 변환

    Args:
        pdf_path: PDF 파일 경로
        toc_path: toc.md 파일 경로
    """
    doc = fitz.open(pdf_path)

    toc_file = Path(toc_path)
    if not toc_file.exists():
        print(f"오류: {toc_path}를 찾을 수 없습니다")
        return

    content = toc_file.read_text(encoding="utf-8")
    lines = content.split('\n')

    # 각 라인의 페이지 번호를 페이지 레이블로 변환
    updated_lines = []
    for line in lines:
        # 페이지 번호 패턴: (p.28), (p.10) 등
        match = re.search(r'\(p\.(\d+)\)$', line)
        if match:
            pdf_page_num = int(match.group(1))
            page_index = pdf_page_num - 1  # 0-indexed
            page_label = get_page_label(doc, page_index)

            # 페이지 번호를 레이블로 변경
            updated_line = re.sub(r'\(p\.\d+\)$', f'(p.{page_label})', line)
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # 업데이트된 내용 저장
    updated_content = '\n'.join(updated_lines)
    toc_file.write_text(updated_content, encoding="utf-8")

    print(f"✓ 성공: {toc_path}를 인쇄된 페이지 번호로 업데이트했습니다")

    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python update_toc_to_labels.py <pdf_path> <toc_path>")
        print("예시: python update_toc_to_labels.py book.pdf toc.md")
        sys.exit(1)

    pdf_path = sys.argv[1]
    toc_path = sys.argv[2]
    update_toc_to_labels(pdf_path, toc_path)
