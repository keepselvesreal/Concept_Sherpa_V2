#!/usr/bin/env python3
"""
생성 시간: 2025-08-13 20:24:04 KST
핵심 내용: HTML 파일에서 Medium 포스팅 내용을 추출하는 도구
상세 내용:
    - extract_medium_content(): HTML 파싱 및 본문 추출 함수
    - clean_text(): 텍스트 정리 및 포맷팅 함수  
    - main(): 메인 실행 함수
상태: 활성
주소: medium_post_extractor
참조: 없음
"""

import re
from bs4 import BeautifulSoup
import sys
import os

def extract_medium_content(html_file_path):
    """
    Medium HTML 파일에서 포스팅 본문을 추출합니다.
    
    Args:
        html_file_path (str): HTML 파일 경로
    
    Returns:
        dict: 제목, 작성자, 본문 등 추출된 내용
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 제목 추출 (title 태그에서)
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else "제목을 찾을 수 없음"
        
        # Medium 포스트의 일반적인 구조를 기반으로 본문 추출
        content_parts = []
        
        # 방법 1: article 태그 찾기
        article_tag = soup.find('article')
        if article_tag:
            paragraphs = article_tag.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for p in paragraphs:
                text = p.get_text().strip()
                if text and len(text) > 10:  # 너무 짧은 텍스트는 제외
                    content_parts.append(text)
        
        # 방법 2: div 태그에서 data-testid나 특정 클래스로 찾기
        if not content_parts:
            # Medium의 일반적인 content selector들을 시도
            selectors = [
                'div[data-testid="storyContent"]',
                'div[class*="postArticle"]',
                'section[data-field="body"]',
                'div[class*="story-body"]',
                'div[class*="postContent"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for elem in elements:
                        paragraphs = elem.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        for p in paragraphs:
                            text = p.get_text().strip()
                            if text and len(text) > 10:
                                content_parts.append(text)
                    break
        
        # 방법 3: 모든 p 태그에서 긴 텍스트만 추출
        if not content_parts:
            all_paragraphs = soup.find_all('p')
            for p in all_paragraphs:
                text = p.get_text().strip()
                # 길이가 충분하고 의미있는 내용인지 확인
                if text and len(text) > 50 and not text.startswith('http'):
                    content_parts.append(text)
        
        # 제목에서 작성자 정보 추출
        author = "작성자 정보 없음"
        if "by " in title:
            author_match = re.search(r'by\s+([^|]+)', title)
            if author_match:
                author = author_match.group(1).strip()
        
        return {
            'title': title,
            'author': author,
            'content': content_parts,
            'total_paragraphs': len(content_parts)
        }
        
    except Exception as e:
        return {'error': f"파일 처리 중 오류 발생: {str(e)}"}

def clean_text(text):
    """
    추출된 텍스트를 정리합니다.
    """
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text

def main():
    if len(sys.argv) != 2:
        print("사용법: python medium_post_extractor.py <html_file_path>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)
    
    print("Medium 포스트 내용을 추출 중...")
    result = extract_medium_content(html_file)
    
    if 'error' in result:
        print(f"오류: {result['error']}")
        sys.exit(1)
    
    print("=" * 80)
    print(f"제목: {result['title']}")
    print(f"작성자: {result['author']}")
    print(f"추출된 문단 수: {result['total_paragraphs']}")
    print("=" * 80)
    print()
    
    print("포스트 본문:")
    print("-" * 40)
    
    for i, paragraph in enumerate(result['content'], 1):
        cleaned_text = clean_text(paragraph)
        print(f"{i}. {cleaned_text}")
        print()
    
    # 텍스트 파일로 저장
    output_file = html_file.replace('.html', '_extracted.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"제목: {result['title']}\n")
        f.write(f"작성자: {result['author']}\n")
        f.write("=" * 80 + "\n\n")
        
        for paragraph in result['content']:
            f.write(clean_text(paragraph) + "\n\n")
    
    print(f"추출된 내용이 저장되었습니다: {output_file}")

if __name__ == "__main__":
    main()