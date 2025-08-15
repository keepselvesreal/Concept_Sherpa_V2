#!/usr/bin/env python3
"""
생성 시간: 2025-08-13 20:24:04 KST
핵심 내용: Medium 포스팅의 모든 구조와 내용을 완전히 보존하여 추출하는 최종 도구
상세 내용:
    - extract_complete_medium_post(): 완전한 포스트 추출 함수
    - preserve_text_structure(): 텍스트 구조 보존 함수
    - extract_clean_paragraphs(): 깔끔한 문단 추출 함수
    - main(): 메인 실행 함수
상태: 활성
주소: medium_post_extractor_final
참조: medium_post_extractor_v3
"""

import re
from bs4 import BeautifulSoup
import sys
import os

def extract_clean_paragraphs(soup):
    """깔끔하게 문단을 추출합니다."""
    
    # Medium의 주요 콘텐츠 영역 찾기
    content_selectors = [
        'article',
        '[data-testid="storyContent"]', 
        'section[data-field="body"]',
        '.postArticle-content',
        'main'
    ]
    
    main_content = None
    for selector in content_selectors:
        elements = soup.select(selector)
        if elements:
            main_content = elements[0]
            break
    
    if not main_content:
        main_content = soup.find('body') or soup
    
    # 모든 텍스트 요소를 순서대로 추출
    all_elements = main_content.find_all([
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # 제목들
        'p',                                   # 문단
        'blockquote',                         # 인용
        'ul', 'ol', 'li',                     # 리스트
        'div'                                 # 일부 div
    ])
    
    structured_content = []
    current_section = None
    
    for elem in all_elements:
        if not elem:
            continue
            
        # 부모 요소가 이미 처리된 요소인지 확인
        if any(parent in [e.get('processed_elem') for e in structured_content if isinstance(e, dict)] for parent in elem.parents):
            continue
            
        text = elem.get_text().strip()
        
        # 너무 짧거나 불필요한 텍스트 필터링
        if len(text) < 5:
            continue
            
        # Medium 특유의 불필요한 텍스트 제거
        if any(phrase in text.lower() for phrase in [
            'medium member', 'keep reading for free', 'sign in', 'follow',
            'subscribe', 'clap for this story', 'written by', 'read more',
            'view original', 'see all from'
        ]):
            continue
            
        # 숫자나 날짜만 있는 텍스트 제거
        if re.match(r'^[\d\s\-.:,]+$', text):
            continue
            
        tag_name = elem.name.lower()
        
        # 제목 처리
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag_name[1])
            structured_content.append({
                'type': 'heading',
                'level': level,
                'text': text,
                'formatted': '#' * level + ' ' + text,
                'processed_elem': elem
            })
            current_section = text
            
        # 문단 처리
        elif tag_name == 'p':
            # 인라인 포맷팅 보존
            formatted_text = preserve_inline_formatting(elem)
            if len(formatted_text) > 10:
                structured_content.append({
                    'type': 'paragraph',
                    'text': text,
                    'formatted': formatted_text,
                    'section': current_section,
                    'processed_elem': elem
                })
                
        # 인용문 처리
        elif tag_name == 'blockquote':
            structured_content.append({
                'type': 'quote',
                'text': text,
                'formatted': '> ' + text,
                'section': current_section,
                'processed_elem': elem
            })
            
        # 리스트 처리
        elif tag_name in ['ul', 'ol']:
            list_items = elem.find_all('li', recursive=False)
            if list_items:
                list_content = []
                for i, li in enumerate(list_items):
                    li_text = li.get_text().strip()
                    if li_text:
                        if tag_name == 'ul':
                            list_content.append(f"• {li_text}")
                        else:
                            list_content.append(f"{i+1}. {li_text}")
                
                if list_content:
                    structured_content.append({
                        'type': 'list',
                        'list_type': tag_name,
                        'text': text,
                        'formatted': '\n'.join(list_content),
                        'section': current_section,
                        'processed_elem': elem
                    })
                    
        # 특별한 div (highlight, callout 등)
        elif tag_name == 'div':
            div_class = ' '.join(elem.get('class', [])).lower()
            if any(cls in div_class for cls in ['highlight', 'pullquote', 'callout', 'graf']):
                if len(text) > 15:
                    structured_content.append({
                        'type': 'special',
                        'text': text,
                        'formatted': f"📌 {text}",
                        'section': current_section,
                        'class': div_class,
                        'processed_elem': elem
                    })
    
    return structured_content

def preserve_inline_formatting(element):
    """인라인 포맷팅을 보존합니다."""
    result = []
    
    for item in element.children:
        if hasattr(item, 'name') and item.name:
            tag_name = item.name.lower()
            text_content = item.get_text().strip()
            
            if tag_name in ['strong', 'b']:
                result.append(f"**{text_content}**")
            elif tag_name in ['em', 'i']:
                result.append(f"*{text_content}*")
            elif tag_name == 'code':
                result.append(f"`{text_content}`")
            elif tag_name == 'a':
                href = item.get('href', '')
                if href and not href.startswith('#'):
                    result.append(f"[{text_content}]({href})")
                else:
                    result.append(text_content)
            else:
                result.append(text_content)
        else:
            # 일반 텍스트
            text = str(item).strip()
            if text:
                result.append(text)
    
    return ' '.join(result)

def extract_complete_medium_post(html_file_path):
    """완전한 Medium 포스트를 추출합니다."""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 메타데이터 추출
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else "제목 없음"
        
        # 작성자 추출 (여러 방법)
        author = "작성자 정보 없음"
        
        # title에서 먼저 추출
        if "by " in title:
            author_match = re.search(r'by\s+([^|]+)', title)
            if author_match:
                author = author_match.group(1).strip()
        
        # HTML에서 작성자 정보 찾기
        author_selectors = [
            'span[data-testid="authorName"]',
            'a[rel="author"]', 
            '.author-name',
            '[data-testid="storyAuthorName"]',
            'a[href*="/@"]'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem and author == "작성자 정보 없음":
                potential_author = author_elem.get_text().strip()
                if potential_author and len(potential_author) < 50:
                    author = potential_author
                    break
        
        # 발행 날짜 추출
        date = "날짜 정보 없음"
        date_selectors = [
            'time',
            '[data-testid="storyPublishDate"]',
            '.published-date'
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text().strip()
                datetime_attr = date_elem.get('datetime', '')
                date = date_text or datetime_attr
                if date != "날짜 정보 없음":
                    break
        
        # 이미지 정보 추출 (간단하게)
        images = []
        img_tags = soup.find_all('img')
        for i, img in enumerate(img_tags):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src and not src.startswith('data:image/svg'):
                images.append({
                    'index': i + 1,
                    'src': src,
                    'alt': alt,
                    'is_embedded': src.startswith('data:image')
                })
        
        # 구조화된 콘텐츠 추출
        structured_content = extract_clean_paragraphs(soup)
        
        return {
            'title': title,
            'author': author,
            'date': date,
            'images': images,
            'content': structured_content,
            'total_elements': len(structured_content),
            'image_count': len(images)
        }
        
    except Exception as e:
        return {'error': f"파일 처리 중 오류 발생: {str(e)}"}

def main():
    if len(sys.argv) != 2:
        print("사용법: python medium_post_extractor_final.py <html_file_path>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)
    
    print("Medium 포스트 완전 추출 중...")
    result = extract_complete_medium_post(html_file)
    
    if 'error' in result:
        print(f"오류: {result['error']}")
        sys.exit(1)
    
    print("=" * 100)
    print(f"제목: {result['title']}")
    print(f"작성자: {result['author']}")
    print(f"날짜: {result['date']}")
    print(f"추출된 요소 수: {result['total_elements']}")
    print(f"이미지 수: {result['image_count']}")
    print("=" * 100)
    print()
    
    # 마크다운 파일로 저장
    base_name = os.path.basename(html_file)
    output_file = base_name.replace('.html', '_complete_final.md')
    output_path = os.path.join(os.path.dirname(html_file), output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # 헤더 정보
        f.write(f"# {result['title']}\n\n")
        f.write(f"**작성자:** {result['author']}  \n")
        f.write(f"**날짜:** {result['date']}  \n")
        f.write(f"**이미지 수:** {result['image_count']}  \n\n")
        f.write("---\n\n")
        
        # 구조화된 콘텐츠
        for item in result['content']:
            f.write(item['formatted'] + "\n\n")
        
        # 이미지 정보
        if result['images']:
            f.write("---\n\n## 이미지 목록\n\n")
            for img in result['images']:
                f.write(f"**이미지 {img['index']}:**  \n")
                f.write(f"- URL: {img['src']}  \n")
                if img['alt']:
                    f.write(f"- 설명: {img['alt']}  \n")
                f.write(f"- 타입: {'임베디드' if img['is_embedded'] else '외부'}\n\n")
    
    print(f"완전한 포스트가 마크다운으로 저장되었습니다: {output_path}")
    
    # 간단한 텍스트 버전도 저장
    txt_output_path = output_path.replace('.md', '.txt')
    with open(txt_output_path, 'w', encoding='utf-8') as f:
        f.write(f"{result['title']}\n")
        f.write(f"작성자: {result['author']}\n")
        f.write(f"날짜: {result['date']}\n")
        f.write("=" * 80 + "\n\n")
        
        for item in result['content']:
            if item['type'] == 'heading':
                f.write(f"\n{item['text']}\n")
                f.write("-" * len(item['text']) + "\n\n")
            else:
                f.write(f"{item['text']}\n\n")
    
    print(f"텍스트 버전도 저장되었습니다: {txt_output_path}")

if __name__ == "__main__":
    main()