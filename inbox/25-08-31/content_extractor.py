# 생성 시간: 2025-08-31 21:05 KST
# 핵심 내용: content_nodes.json 파일을 읽어 각 노드의 start_page~end_page 범위 PDF 내용을 추출하여 개별 MD 파일로 저장
# 상세 내용:
#   - main() (라인 12): 전체 프로세스를 제어하는 메인 함수
#   - extract_pdf_content() (라인 30): PDF에서 특정 페이지 범위의 텍스트를 추출
#   - save_content_to_md() (라인 52): 추출된 내용을 마크다운 파일로 저장
#   - process_content_nodes() (라인 64): content_nodes.json을 처리하여 각 노드별로 내용 추출 및 저장
# 상태: active

import json
import fitz  # PyMuPDF
import argparse
import os
from pathlib import Path
import sys

def main():
    """메인 함수 - 명령줄 인자를 처리하고 전체 프로세스를 실행"""
    parser = argparse.ArgumentParser(description="content_nodes.json에서 PDF 내용을 추출해 개별 MD 파일로 저장")
    parser.add_argument("content_nodes_path", help="content_nodes.json 파일 경로")
    parser.add_argument("pdf_path", help="PDF 파일 경로")
    parser.add_argument("--output-dir", "-o", help="출력 디렉토리 (기본값: content_nodes.json과 같은 디렉토리)")
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not os.path.exists(args.content_nodes_path):
        print(f"❌ content_nodes.json 파일이 없습니다: {args.content_nodes_path}")
        sys.exit(1)
        
    if not os.path.exists(args.pdf_path):
        print(f"❌ PDF 파일이 없습니다: {args.pdf_path}")
        sys.exit(1)
    
    # 출력 디렉토리 설정
    output_dir = args.output_dir or os.path.dirname(args.content_nodes_path)
    
    process_content_nodes(args.content_nodes_path, args.pdf_path, output_dir)

def extract_pdf_content(pdf_path, start_page, end_page):
    """PDF에서 지정된 페이지 범위의 텍스트를 추출
    
    Args:
        pdf_path (str): PDF 파일 경로
        start_page (int): 시작 페이지 (1-based)
        end_page (int): 끝 페이지 (1-based, 포함)
    
    Returns:
        str: 추출된 텍스트
    """
    try:
        doc = fitz.open(pdf_path)
        content = ""
        
        # PyMuPDF는 0-based 인덱스 사용
        for page_num in range(start_page - 1, end_page):
            if page_num < len(doc):
                page = doc.load_page(page_num)
                text = page.get_text()
                content += f"--- 페이지 {page_num + 1} ---\n{text}\n\n"
            else:
                print(f"⚠️ 페이지 {page_num + 1}는 PDF 범위를 벗어납니다.")
        
        doc.close()
        return content
        
    except Exception as e:
        print(f"❌ PDF 추출 오류 ({start_page}-{end_page}): {e}")
        return ""

def save_content_to_md(content, title, output_dir):
    """추출된 내용을 마크다운 파일로 저장
    
    Args:
        content (str): 저장할 내용
        title (str): 파일명이 될 제목
        output_dir (str): 출력 디렉토리
    """
    filename = f"{title}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n{content}")
    
    print(f"✅ 저장 완료: {filepath}")

def process_content_nodes(content_nodes_path, pdf_path, output_dir):
    """content_nodes.json을 처리하여 각 노드별로 내용 추출 및 저장
    
    Args:
        content_nodes_path (str): content_nodes.json 파일 경로
        pdf_path (str): PDF 파일 경로  
        output_dir (str): 출력 디렉토리
    """
    try:
        # content_nodes.json 로드
        with open(content_nodes_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🚀 {len(nodes)}개 노드 처리 시작...")
        print(f"📖 PDF: {pdf_path}")
        print(f"📁 출력 디렉토리: {output_dir}")
        print("-" * 50)
        
        for i, node in enumerate(nodes, 1):
            title = node.get('title', f'node_{node.get("id", i)}')
            start_page = node.get('start_page')
            end_page = node.get('end_page')
            level = node.get('level', 0)
            
            if not start_page or not end_page:
                print(f"⚠️ 스킵 ({i}/{len(nodes)}): {title} - 페이지 정보 없음")
                continue
            
            print(f"🔍 처리 중 ({i}/{len(nodes)}): {title} (레벨 {level}, 페이지 {start_page}-{end_page})")
            
            # PDF에서 내용 추출
            content = extract_pdf_content(pdf_path, start_page, end_page)
            
            if content:
                # 마크다운 파일로 저장
                save_content_to_md(content, title, output_dir)
            else:
                print(f"❌ 내용 추출 실패: {title}")
        
        print("-" * 50)
        print(f"🎉 처리 완료! 총 {len(nodes)}개 노드 처리됨")
        
    except Exception as e:
        print(f"❌ 처리 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()