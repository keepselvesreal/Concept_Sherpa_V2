#!/usr/bin/env python3
"""
생성 시간: 2025-08-13 20:24:04 KST
핵심 내용: Medium 포스팅을 효율적으로 추출하는 최적화된 도구 (이미지는 참조만 포함)
상세 내용:
    - extract_medium_post_optimized(): 최적화된 포스트 추출 함수
    - handle_images_efficiently(): 이미지 효율적 처리 함수  
    - preserve_structure(): 구조 보존 함수
    - main(): 메인 실행 함수
상태: 활성
주소: medium_post_extractor_optimized
참조: medium_post_extractor_final
"""

import re
from bs4 import BeautifulSoup
import sys
import os
from urllib.parse import urlparse

def handle_images_efficiently(soup):
    """이미지를 효율적으로 처리합니다 - 메타데이터만 추출."""
    images = []
    img_tags = soup.find_all('img')
    
    for i, img in enumerate(img_tags):
        src = img.get('src', '')
        alt = img.get('alt', '')
        
        # 의미있는 이미지만 포함 (SVG 아이콘, 매우 작은 이미지 제외)
        if (src and 
            not src.startswith('data:image/svg') and
            not 'icon' in src.lower() and
            not 'avatar' in src.lower()):
            
            # URL 파싱하여 파일명 추출
            parsed_url = urlparse(src)
            filename = os.path.basename(parsed_url.path) or f"image_{i+1}"
            
            images.append({
                'index': i + 1,
                'filename': filename,
                'alt': alt,
                'caption': img.get('title', ''),
                'position_marker': f"[IMAGE_{i+1}]"
            })
    
    return images

def preserve_structure(soup):
    """구조를 보존하면서 텍스트를 추출합니다."""
    
    # Medium 콘텐츠 영역 찾기
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
    
    # 구조적 요소들 추출
    elements = main_content.find_all([
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # 제목
        'p',                                   # 문단
        'blockquote',                         # 인용
        'ul', 'ol',                           # 리스트
        'pre', 'code',                        # 코드
        'img'                                 # 이미지 (위치 표시용)
    ])
    
    structured_content = []
    image_counter = 1
    
    for elem in elements:
        if not elem:
            continue
            
        tag_name = elem.name.lower()
        text = elem.get_text().strip()
        
        # 짧거나 불필요한 내용 필터링
        if tag_name != 'img' and len(text) < 5:
            continue
            
        # Medium 특유의 불필요한 텍스트 제거
        if any(phrase in text.lower() for phrase in [
            'medium member', 'keep reading for free', 'sign in', 'follow',
            'subscribe', 'clap for this story', 'written by', 'read more'
        ]):
            continue
            
        # 숫자나 날짜만 있는 텍스트 제거
        if re.match(r'^[\d\s\-.:,]+$', text):
            continue
            
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag_name[1])
            structured_content.append({
                'type': 'heading',
                'level': level,
                'content': text,
                'markdown': '#' * level + ' ' + text
            })
            
        elif tag_name == 'p':
            # 인라인 포맷팅 보존
            formatted_text = preserve_inline_formatting(elem)
            if len(formatted_text) > 10:
                structured_content.append({
                    'type': 'paragraph', 
                    'content': text,
                    'markdown': formatted_text
                })
                
        elif tag_name == 'blockquote':
            structured_content.append({
                'type': 'quote',
                'content': text,
                'markdown': '> ' + text.replace('\n', '\n> ')
            })
            
        elif tag_name in ['ul', 'ol']:
            list_items = elem.find_all('li', recursive=False)
            if list_items:
                list_content = []
                for li_idx, li in enumerate(list_items):
                    li_text = li.get_text().strip()
                    if li_text:
                        if tag_name == 'ul':
                            list_content.append(f"• {li_text}")
                        else:
                            list_content.append(f"{li_idx+1}. {li_text}")
                
                if list_content:
                    structured_content.append({
                        'type': 'list',
                        'list_type': tag_name,
                        'content': text,
                        'markdown': '\n'.join(list_content)
                    })
                    
        elif tag_name in ['pre', 'code']:
            if tag_name == 'pre':
                structured_content.append({
                    'type': 'code_block',
                    'content': text,
                    'markdown': f"```\n{text}\n```"
                })
            else:
                structured_content.append({
                    'type': 'inline_code',
                    'content': text,
                    'markdown': f"`{text}`"
                })
                
        elif tag_name == 'img':
            # 이미지 위치만 표시
            alt = elem.get('alt', '')
            src = elem.get('src', '')
            
            if (src and 
                not src.startswith('data:image/svg') and
                not 'icon' in src.lower()):
                
                structured_content.append({
                    'type': 'image',
                    'content': f"[이미지 {image_counter}: {alt}]",
                    'markdown': f"[IMAGE_{image_counter}: {alt or '설명 없음'}]",
                    'image_index': image_counter
                })
                image_counter += 1
    
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
            text = str(item).strip()
            if text:
                result.append(text)
    
    return ' '.join(result)

def extract_medium_post_optimized(html_file_path):
    """최적화된 방식으로 Medium 포스트를 추출합니다."""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 메타데이터 추출
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else "제목 없음"
        
        # 작성자 추출
        author = "작성자 정보 없음"
        if "by " in title:
            author_match = re.search(r'by\s+([^|]+)', title)
            if author_match:
                author = author_match.group(1).strip()
        
        # 날짜 추출
        date = "날짜 정보 없음"
        date_selectors = ['time', '[data-testid="storyPublishDate"]']
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date = date_elem.get_text().strip() or date_elem.get('datetime', '')
                break
        
        # 이미지 메타데이터만 추출
        images_metadata = handle_images_efficiently(soup)
        
        # 구조화된 콘텐츠 추출
        structured_content = preserve_structure(soup)
        
        return {
            'title': title,
            'author': author,
            'date': date,
            'images_metadata': images_metadata,
            'content': structured_content,
            'stats': {
                'total_elements': len(structured_content),
                'image_count': len(images_metadata),
                'estimated_reading_time': estimate_reading_time(structured_content)
            }
        }
        
    except Exception as e:
        return {'error': f"파일 처리 중 오류 발생: {str(e)}"}

def estimate_reading_time(content):
    """읽는 시간을 추정합니다."""
    word_count = 0
    for item in content:
        if item['type'] in ['paragraph', 'quote']:
            word_count += len(item['content'].split())
    
    # 평균 읽기 속도: 250 words/minute
    minutes = max(1, round(word_count / 250))
    return f"{minutes}분"

def main():
    if len(sys.argv) != 2:
        print("사용법: python medium_post_extractor_optimized.py <html_file_path>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)
    
    print("Medium 포스트를 최적화된 방식으로 추출 중...")
    result = extract_medium_post_optimized(html_file)
    
    if 'error' in result:
        print(f"오류: {result['error']}")
        sys.exit(1)
    
    # 결과 출력
    print("=" * 80)
    print(f"제목: {result['title']}")
    print(f"작성자: {result['author']}")
    print(f"날짜: {result['date']}")
    print(f"추정 읽기 시간: {result['stats']['estimated_reading_time']}")
    print(f"콘텐츠 요소 수: {result['stats']['total_elements']}")
    print(f"이미지 수: {result['stats']['image_count']}")
    print("=" * 80)
    print()
    
    # 마크다운 파일로 저장
    base_name = os.path.basename(html_file)
    output_file = base_name.replace('.html', '_optimized.md')
    output_path = os.path.join(os.path.dirname(html_file), output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # 헤더
        f.write(f"# {result['title']}\n\n")
        f.write(f"**작성자:** {result['author']}  \n")
        f.write(f"**날짜:** {result['date']}  \n")
        f.write(f"**읽기 시간:** {result['stats']['estimated_reading_time']}  \n")
        f.write(f"**이미지:** {result['stats']['image_count']}개\n\n")
        f.write("---\n\n")
        
        # 본문
        for item in result['content']:
            f.write(item['markdown'] + "\n\n")
        
        # 이미지 참조 목록
        if result['images_metadata']:
            f.write("---\n\n## 이미지 참조\n\n")
            for img in result['images_metadata']:
                f.write(f"**IMAGE_{img['index']}:** {img['filename']}")
                if img['alt']:
                    f.write(f" - {img['alt']}")
                f.write("\n\n")
    
    print(f"최적화된 마크다운이 저장되었습니다: {output_path}")
    
    # 간단한 텍스트 버전
    txt_output = output_path.replace('.md', '.txt')
    with open(txt_output, 'w', encoding='utf-8') as f:
        f.write(f"{result['title']}\n")
        f.write(f"작성자: {result['author']}\n")
        f.write(f"날짜: {result['date']}\n")
        f.write("=" * 60 + "\n\n")
        
        for item in result['content']:
            if item['type'] == 'heading':
                f.write(f"\n{item['content']}\n")
                f.write("-" * len(item['content']) + "\n\n")
            elif item['type'] == 'image':
                f.write(f"{item['content']}\n\n")
            else:
                f.write(f"{item['content']}\n\n")
    
    print(f"텍스트 버전도 저장되었습니다: {txt_output}")

if __name__ == "__main__":
    main()