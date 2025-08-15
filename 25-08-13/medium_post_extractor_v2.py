#!/usr/bin/env python3
"""
생성 시간: 2025-08-13 20:24:04 KST
핵심 내용: HTML 파일에서 Medium 포스팅 내용을 깔끔하게 추출하는 개선된 도구
상세 내용:
    - extract_medium_content(): 중복 제거 및 개선된 HTML 파싱 함수
    - remove_duplicates(): 중복 문단 제거 함수
    - clean_and_format(): 텍스트 정리 및 포맷팅 함수  
    - main(): 메인 실행 함수
상태: 활성
주소: medium_post_extractor_v2
참조: medium_post_extractor
"""

import re
from bs4 import BeautifulSoup
import sys
import os

def remove_duplicates(paragraphs):
    """중복된 문단을 제거합니다."""
    seen = set()
    unique_paragraphs = []
    
    for p in paragraphs:
        # 텍스트 정규화 (공백, 특수문자 정리)
        normalized = re.sub(r'\s+', ' ', p.strip().lower())
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        # 너무 짧은 텍스트나 의미없는 텍스트 필터링
        if len(normalized) < 20:
            continue
            
        # "medium member" 관련 텍스트 제거
        if 'medium member' in normalized or 'keep reading for free' in normalized:
            continue
            
        # 중복 체크 (70% 이상 유사하면 중복으로 간주)
        is_duplicate = False
        for seen_text in seen:
            similarity = calculate_similarity(normalized, seen_text)
            if similarity > 0.7:
                is_duplicate = True
                break
        
        if not is_duplicate:
            seen.add(normalized)
            unique_paragraphs.append(p.strip())
    
    return unique_paragraphs

def calculate_similarity(text1, text2):
    """두 텍스트의 유사도를 계산합니다."""
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union

def extract_medium_content(html_file_path):
    """
    Medium HTML 파일에서 포스팅 본문을 추출합니다.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 제목 추출 (title 태그에서)
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else "제목을 찾을 수 없음"
        
        # 작성자 정보 추출
        author = "작성자 정보 없음"
        if "by " in title:
            author_match = re.search(r'by\s+([^|]+)', title)
            if author_match:
                author = author_match.group(1).strip()
        
        # 본문 추출을 위한 여러 방법 시도
        content_parts = []
        
        # 방법 1: article 태그 찾기
        article_tag = soup.find('article')
        if article_tag:
            paragraphs = article_tag.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for p in paragraphs:
                text = p.get_text().strip()
                if text and len(text) > 20:  
                    content_parts.append(text)
        
        # 방법 2: 특정 클래스나 ID로 찾기
        if not content_parts:
            selectors = [
                'div[data-testid="storyContent"]',
                'div[class*="postArticle"]',
                'section[data-field="body"]',
                'div[class*="story-body"]',
                'div[class*="postContent"]',
                'main'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for elem in elements:
                        paragraphs = elem.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        for p in paragraphs:
                            text = p.get_text().strip()
                            if text and len(text) > 20:
                                content_parts.append(text)
                    if content_parts:  # 첫 번째 성공한 selector만 사용
                        break
        
        # 방법 3: 모든 p 태그에서 의미있는 내용만 추출
        if not content_parts:
            all_paragraphs = soup.find_all('p')
            for p in all_paragraphs:
                text = p.get_text().strip()
                # 길이가 충분하고 의미있는 내용인지 확인
                if (text and len(text) > 30 and 
                    not text.startswith('http') and
                    not re.match(r'^[\d\s\-.:]+$', text)):  # 숫자/날짜만 있는 텍스트 제외
                    content_parts.append(text)
        
        # 중복 제거
        unique_content = remove_duplicates(content_parts)
        
        return {
            'title': title,
            'author': author,
            'content': unique_content,
            'total_paragraphs': len(unique_content)
        }
        
    except Exception as e:
        return {'error': f"파일 처리 중 오류 발생: {str(e)}"}

def clean_and_format(text):
    """텍스트를 정리하고 포맷팅합니다."""
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    # 불필요한 문구 제거
    text = re.sub(r'Press enter or click to view image in full size', '', text, flags=re.IGNORECASE)
    return text

def main():
    if len(sys.argv) != 2:
        print("사용법: python medium_post_extractor_v2.py <html_file_path>")
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
        cleaned_text = clean_and_format(paragraph)
        if cleaned_text:  # 빈 텍스트가 아닌 경우만 출력
            print(f"{i}. {cleaned_text}")
            print()
    
    # 텍스트 파일로 저장
    base_name = os.path.basename(html_file)
    output_file = base_name.replace('.html', '_clean_extracted.txt')
    output_path = os.path.join(os.path.dirname(html_file), output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"제목: {result['title']}\n")
        f.write(f"작성자: {result['author']}\n")
        f.write("=" * 80 + "\n\n")
        
        for paragraph in result['content']:
            cleaned_text = clean_and_format(paragraph)
            if cleaned_text:
                f.write(cleaned_text + "\n\n")
    
    print(f"깔끔하게 추출된 내용이 저장되었습니다: {output_path}")

if __name__ == "__main__":
    main()