#!/usr/bin/env python3
"""
생성 시간: 2025-08-13 20:24:04 KST
핵심 내용: HTML 파일에서 Medium 포스팅의 모든 내용과 구조를 완전히 보존하여 추출하는 도구
상세 내용:
    - extract_medium_content_complete(): 완전한 HTML 파싱 및 구조 보존 함수
    - preserve_formatting(): 원본 텍스트 형식 보존 함수
    - extract_images(): 이미지 정보 추출 함수
    - reconstruct_structure(): 원본 구조 재구성 함수
    - main(): 메인 실행 함수
상태: 활성
주소: medium_post_extractor_v3
참조: medium_post_extractor_v2
"""

import re
from bs4 import BeautifulSoup, NavigableString
import sys
import os
from urllib.parse import urljoin, urlparse
import base64

def extract_images(soup, base_url=""):
    """이미지 정보를 추출합니다."""
    images = []
    img_tags = soup.find_all('img')
    
    for i, img in enumerate(img_tags):
        img_info = {
            'index': i + 1,
            'src': img.get('src', ''),
            'alt': img.get('alt', ''),
            'title': img.get('title', ''),
            'width': img.get('width', ''),
            'height': img.get('height', ''),
            'data_src': img.get('data-src', ''),
            'srcset': img.get('srcset', '')
        }
        
        # 상대 URL을 절대 URL로 변환
        if img_info['src'] and not img_info['src'].startswith('http'):
            img_info['src'] = urljoin(base_url, img_info['src'])
        
        # base64 이미지인지 확인
        if img_info['src'].startswith('data:image'):
            img_info['is_embedded'] = True
        else:
            img_info['is_embedded'] = False
        
        images.append(img_info)
    
    return images

def preserve_formatting(element):
    """요소의 텍스트와 포맷팅을 보존합니다."""
    if not element:
        return ""
    
    result = []
    
    for item in element.children:
        if isinstance(item, NavigableString):
            text = str(item).strip()
            if text:
                result.append(text)
        else:
            tag_name = item.name.lower()
            text_content = item.get_text().strip()
            
            if not text_content:
                continue
            
            # 다양한 태그별 포맷팅 처리
            if tag_name in ['strong', 'b']:
                result.append(f"**{text_content}**")
            elif tag_name in ['em', 'i']:
                result.append(f"*{text_content}*")
            elif tag_name == 'code':
                result.append(f"`{text_content}`")
            elif tag_name == 'a':
                href = item.get('href', '')
                if href:
                    result.append(f"[{text_content}]({href})")
                else:
                    result.append(text_content)
            elif tag_name in ['ul', 'ol']:
                # 리스트 처리
                list_items = item.find_all('li')
                for li in list_items:
                    li_text = li.get_text().strip()
                    if li_text:
                        if tag_name == 'ul':
                            result.append(f"• {li_text}")
                        else:
                            result.append(f"1. {li_text}")
            elif tag_name == 'blockquote':
                quote_text = text_content.replace('\n', '\n> ')
                result.append(f"> {quote_text}")
            elif tag_name == 'pre':
                result.append(f"```\n{text_content}\n```")
            else:
                result.append(text_content)
    
    return " ".join(result)

def extract_medium_content_complete(html_file_path):
    """
    Medium HTML 파일에서 모든 내용과 구조를 완전히 추출합니다.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 기본 메타데이터 추출
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else "제목을 찾을 수 없음"
        
        # 작성자 정보 추출 (여러 방법 시도)
        author = "작성자 정보 없음"
        
        # 방법 1: title에서 추출
        if "by " in title:
            author_match = re.search(r'by\s+([^|]+)', title)
            if author_match:
                author = author_match.group(1).strip()
        
        # 방법 2: author 관련 태그에서 추출
        author_selectors = [
            'span[data-testid="authorName"]',
            'a[rel="author"]',
            '.author-name',
            '[data-testid="storyAuthorName"]'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem and author == "작성자 정보 없음":
                author = author_elem.get_text().strip()
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
                date = date_elem.get_text().strip() or date_elem.get('datetime', '')
                break
        
        # 이미지 정보 추출
        images = extract_images(soup)
        
        # 본문 추출 - 더 정교한 방법
        content_structure = []
        
        # Medium의 다양한 콘텐츠 선택자들
        content_selectors = [
            'article',
            '[data-testid="storyContent"]',
            'section[data-field="body"]',
            '.postArticle-content',
            '.story-body',
            '.post-content',
            'main'
        ]
        
        main_content = None
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                main_content = elements[0]
                break
        
        # 모든 p 태그 대안
        if not main_content:
            main_content = soup
        
        # 구조적 요소들을 순차적으로 추출
        content_elements = main_content.find_all([
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # 헤딩
            'p',                                    # 문단
            'blockquote',                          # 인용
            'ul', 'ol',                            # 리스트
            'pre', 'code',                         # 코드
            'img',                                 # 이미지
            'figure',                              # 피처
            'div'                                  # div (특정 클래스만)
        ])
        
        # 의미있는 콘텐츠만 필터링
        processed_elements = []
        img_counter = 1
        
        for elem in content_elements:
            if not elem:
                continue
            
            tag_name = elem.name.lower()
            text_content = elem.get_text().strip()
            
            # 너무 짧거나 의미없는 내용 필터링
            if tag_name != 'img' and len(text_content) < 10:
                continue
            
            # Medium 특화 불필요 요소 제거
            if any(phrase in text_content.lower() for phrase in [
                'medium member', 'keep reading for free', 'sign in', 'follow',
                'subscribe', 'clap for this story', 'written by'
            ]):
                continue
            
            element_info = {
                'type': tag_name,
                'level': None,
                'content': '',
                'formatted_content': '',
                'attributes': {}
            }
            
            if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                element_info['level'] = int(tag_name[1])
                element_info['content'] = text_content
                element_info['formatted_content'] = f"{'#' * element_info['level']} {text_content}"
            
            elif tag_name == 'p':
                formatted_text = preserve_formatting(elem)
                if formatted_text and len(formatted_text) > 15:
                    element_info['content'] = text_content
                    element_info['formatted_content'] = formatted_text
            
            elif tag_name == 'blockquote':
                element_info['content'] = text_content
                element_info['formatted_content'] = f"> {text_content}"
            
            elif tag_name in ['ul', 'ol']:
                list_items = elem.find_all('li')
                if list_items:
                    formatted_list = []
                    for i, li in enumerate(list_items):
                        li_text = li.get_text().strip()
                        if li_text:
                            if tag_name == 'ul':
                                formatted_list.append(f"• {li_text}")
                            else:
                                formatted_list.append(f"{i+1}. {li_text}")
                    
                    if formatted_list:
                        element_info['content'] = text_content
                        element_info['formatted_content'] = '\n'.join(formatted_list)
            
            elif tag_name == 'img':
                img_src = elem.get('src', '')
                img_alt = elem.get('alt', '')
                img_title = elem.get('title', '')
                
                element_info['content'] = f"[이미지 {img_counter}]"
                element_info['formatted_content'] = f"![{img_alt or f'이미지 {img_counter}'}]({img_src})"
                element_info['attributes'] = {
                    'src': img_src,
                    'alt': img_alt,
                    'title': img_title
                }
                img_counter += 1
            
            elif tag_name == 'figure':
                # figure 내의 img나 caption 처리
                fig_img = elem.find('img')
                fig_caption = elem.find(['figcaption', 'caption'])
                
                if fig_img:
                    img_src = fig_img.get('src', '')
                    img_alt = fig_img.get('alt', '')
                    caption_text = fig_caption.get_text().strip() if fig_caption else ''
                    
                    element_info['content'] = f"[그림 {img_counter}]{': ' + caption_text if caption_text else ''}"
                    element_info['formatted_content'] = f"![{img_alt or f'그림 {img_counter}'}]({img_src})"
                    if caption_text:
                        element_info['formatted_content'] += f"\n*{caption_text}*"
                    
                    element_info['attributes'] = {
                        'src': img_src,
                        'alt': img_alt,
                        'caption': caption_text
                    }
                    img_counter += 1
            
            elif tag_name in ['pre', 'code']:
                element_info['content'] = text_content
                if tag_name == 'pre':
                    element_info['formatted_content'] = f"```\n{text_content}\n```"
                else:
                    element_info['formatted_content'] = f"`{text_content}`"
            
            elif tag_name == 'div':
                # 특별한 div만 처리 (예: 인용문, 특별한 콘텐츠)
                div_class = ' '.join(elem.get('class', []))
                if any(cls in div_class.lower() for cls in ['highlight', 'pullquote', 'callout']):
                    formatted_text = preserve_formatting(elem)
                    if formatted_text and len(formatted_text) > 15:
                        element_info['content'] = text_content
                        element_info['formatted_content'] = f"📌 {formatted_text}"
            
            # 유효한 요소만 추가
            if element_info['content'] or element_info['formatted_content']:
                processed_elements.append(element_info)
        
        return {
            'title': title,
            'author': author,
            'date': date,
            'images': images,
            'content_structure': processed_elements,
            'total_elements': len(processed_elements),
            'image_count': len(images)
        }
        
    except Exception as e:
        return {'error': f"파일 처리 중 오류 발생: {str(e)}"}

def main():
    if len(sys.argv) != 2:
        print("사용법: python medium_post_extractor_v3.py <html_file_path>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)
    
    print("Medium 포스트의 완전한 내용과 구조를 추출 중...")
    result = extract_medium_content_complete(html_file)
    
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
    
    # 완전한 구조로 출력
    for i, element in enumerate(result['content_structure'], 1):
        print(f"[{i}] {element['type'].upper()}")
        if element['level']:
            print(f"    레벨: {element['level']}")
        
        if element['formatted_content']:
            print(f"    내용: {element['formatted_content']}")
        elif element['content']:
            print(f"    내용: {element['content']}")
        
        if element.get('attributes'):
            print(f"    속성: {element['attributes']}")
        
        print()
    
    # 이미지 정보 출력
    if result['images']:
        print("=" * 50 + " 이미지 정보 " + "=" * 50)
        for img in result['images']:
            print(f"이미지 {img['index']}:")
            print(f"  URL: {img['src']}")
            if img['alt']:
                print(f"  설명: {img['alt']}")
            if img['title']:
                print(f"  제목: {img['title']}")
            if img['is_embedded']:
                print(f"  타입: 임베디드 이미지")
            print()
    
    # 마크다운 형식으로 저장
    base_name = os.path.basename(html_file)
    output_file = base_name.replace('.html', '_complete_extracted.md')
    output_path = os.path.join(os.path.dirname(html_file), output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # 메타데이터
        f.write(f"# {result['title']}\n\n")
        f.write(f"**작성자:** {result['author']}  \n")
        f.write(f"**날짜:** {result['date']}  \n")
        f.write(f"**이미지 수:** {result['image_count']}\n\n")
        f.write("---\n\n")
        
        # 본문 내용
        for element in result['content_structure']:
            if element['formatted_content']:
                f.write(element['formatted_content'] + "\n\n")
            elif element['content']:
                f.write(element['content'] + "\n\n")
        
        # 이미지 정보 추가
        if result['images']:
            f.write("\n---\n\n## 이미지 정보\n\n")
            for img in result['images']:
                f.write(f"### 이미지 {img['index']}\n")
                f.write(f"- **URL:** {img['src']}\n")
                if img['alt']:
                    f.write(f"- **설명:** {img['alt']}\n")
                if img['title']:
                    f.write(f"- **제목:** {img['title']}\n")
                f.write(f"- **임베디드:** {'예' if img['is_embedded'] else '아니오'}\n\n")
    
    print(f"완전한 구조가 보존된 마크다운 파일이 저장되었습니다: {output_path}")

if __name__ == "__main__":
    main()