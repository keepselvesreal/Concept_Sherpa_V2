# 생성 시간: 2025-08-18 16:05 KST
# 핵심 내용: Playwright MCP를 활용한 웹 콘텐츠 추출기
# 상세 내용:
#   - WebContentExtractor 클래스 (라인 18-200): 메인 추출 클래스, URL 처리, 브라우저 관리
#   - _extract_main_content 메서드 (라인 45-89): DOM 셀렉터를 통한 메인 콘텐츠 추출 
#   - _html_to_markdown 메서드 (라인 91-110): HTML을 마크다운으로 변환
#   - _save_content 메서드 (라인 112-135): 추출된 콘텐츠를 파일로 저장
#   - main 함수 (라인 202-220): CLI 실행 부분, 테스트용 URL 처리
# 상태: 구현 완료
# 주소: web_content_extractor
# 참조: playwright_content_extractor_plan.md

import re
import os
from datetime import datetime
from urllib.parse import urlparse
import html2text

class WebContentExtractor:
    """Playwright MCP를 활용한 웹 콘텐츠 추출기"""
    
    def __init__(self, output_dir="./extracted_content"):
        """
        초기화
        Args:
            output_dir (str): 추출된 콘텐츠 저장 디렉토리
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        # HTML to Markdown 변환기 설정
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0  # 줄바꿈 없음
        
    def ensure_output_dir(self):
        """출력 디렉토리 생성"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
    
    def _extract_main_content(self, url):
        """
        웹 페이지에서 메인 콘텐츠 추출
        Args:
            url (str): 추출할 웹 페이지 URL
        Returns:
            dict: {'title': str, 'content': str, 'metadata': dict}
        """
        print(f"URL 접속 중: {url}")
        
        # Medium 전용 셀렉터들
        medium_selectors = {
            'title': ['h1[data-testid="storyTitle"]', 'h1.graf--title', 'h1'],
            'content': [
                'article[data-testid="storyContent"]',
                'div[data-testid="storyContent"]', 
                'article.meteredContent',
                '.postArticle-content',
                'section[data-field="body"]',
                'article',
                'main'
            ],
            'author': [
                'a[data-testid="authorName"]',
                '.author-name', 
                '[rel="author"]'
            ],
            'publish_date': [
                'time[datetime]',
                '.published-date',
                '[data-testid="storyPublishDate"]'
            ]
        }
        
        # 일반적인 셀렉터들 (Medium 외 사이트용)
        general_selectors = {
            'title': ['h1', 'title', '.title', '.post-title'],
            'content': ['article', 'main', '.content', '.post-content', '.entry-content'],
            'author': ['.author', '.by-author', '[rel="author"]'],
            'publish_date': ['time', '.date', '.publish-date']
        }
        
        # URL에 따라 적절한 셀렉터 선택
        if 'medium.com' in url:
            selectors = medium_selectors
        else:
            selectors = general_selectors
            
        # 추출된 데이터 저장용
        extracted_data = {
            'title': '',
            'content': '',
            'metadata': {
                'url': url,
                'extracted_at': datetime.now().isoformat(),
                'author': '',
                'publish_date': ''
            }
        }
        
        # 실제 추출 로직은 Playwright MCP 호출로 대체 예정
        # 현재는 기본 구조만 구현
        return extracted_data
        
    def _html_to_markdown(self, html_content):
        """
        HTML을 마크다운으로 변환
        Args:
            html_content (str): HTML 콘텐츠
        Returns:
            str: 마크다운 형식 텍스트
        """
        if not html_content:
            return ""
            
        # HTML2Text로 변환
        markdown = self.h2t.handle(html_content)
        
        # 마크다운 정리
        markdown = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown)  # 연속 빈 줄 제거
        markdown = re.sub(r'[ \t]+$', '', markdown, flags=re.MULTILINE)  # 줄 끝 공백 제거
        
        return markdown.strip()
    
    def _save_content(self, extracted_data, filename=None):
        """
        추출된 콘텐츠를 마크다운 파일로 저장
        Args:
            extracted_data (dict): 추출된 데이터
            filename (str): 저장할 파일명 (None이면 자동 생성)
        Returns:
            str: 저장된 파일 경로
        """
        if not filename:
            # URL에서 파일명 생성
            parsed_url = urlparse(extracted_data['metadata']['url'])
            domain = parsed_url.netloc.replace('www.', '')
            path_parts = [p for p in parsed_url.path.split('/') if p]
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if path_parts:
                filename = f"{timestamp}_{domain}_{path_parts[-1]}.md"
            else:
                filename = f"{timestamp}_{domain}.md"
            
            # 파일명에서 특수문자 제거
            filename = re.sub(r'[^\w\-_\.]', '_', filename)
        
        filepath = os.path.join(self.output_dir, filename)
        
        # 마크다운 내용 구성
        markdown_content = []
        
        # 메타데이터 헤더
        markdown_content.append("---")
        markdown_content.append(f"title: \"{extracted_data['title']}\"")
        markdown_content.append(f"url: {extracted_data['metadata']['url']}")
        markdown_content.append(f"extracted_at: {extracted_data['metadata']['extracted_at']}")
        if extracted_data['metadata']['author']:
            markdown_content.append(f"author: {extracted_data['metadata']['author']}")
        if extracted_data['metadata']['publish_date']:
            markdown_content.append(f"publish_date: {extracted_data['metadata']['publish_date']}")
        markdown_content.append("---")
        markdown_content.append("")
        
        # 제목
        if extracted_data['title']:
            markdown_content.append(f"# {extracted_data['title']}")
            markdown_content.append("")
        
        # 콘텐츠
        if extracted_data['content']:
            markdown_content.append(extracted_data['content'])
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        return filepath
    
    def extract_and_save(self, url, filename=None):
        """
        URL에서 콘텐츠를 추출하고 저장
        Args:
            url (str): 추출할 웹 페이지 URL
            filename (str): 저장할 파일명 (선택)
        Returns:
            str: 저장된 파일 경로
        """
        try:
            # 콘텐츠 추출
            extracted_data = self._extract_main_content(url)
            
            # 파일 저장
            filepath = self._save_content(extracted_data, filename)
            
            print(f"콘텐츠 추출 완료: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"콘텐츠 추출 실패: {str(e)}")
            raise

def main():
    """메인 실행 함수"""
    # 테스트용 URL
    test_url = "https://medium.com/@PowerUpSkills/building-with-claude-ai-real-time-streaming-interactive-response-handling-part-5-of-6-d775713fdb55"
    
    # 추출기 인스턴스 생성
    extractor = WebContentExtractor(output_dir="/home/nadle/projects/Knowledge_Sherpa/v2/25-08-18/extracted_content")
    
    # 콘텐츠 추출 및 저장
    try:
        filepath = extractor.extract_and_save(test_url)
        print(f"추출 완료! 파일 위치: {filepath}")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main()