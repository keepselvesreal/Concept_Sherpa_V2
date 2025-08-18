"""
생성 시간: 2025-08-18 20:40:37 KST
핵심 내용: 마크다운 파일의 상대 경로를 웹 URL과 결합하여 절대 이미지 URL 생성
상세 내용:
    - MarkdownImageResolver 클래스 (라인 20-80): 이미지 URL 해결 엔진
    - resolve_image_url 메서드 (라인 35-65): 상대→절대 경로 변환
    - extract_images_from_markdown 메서드 (라인 67-80): MD에서 이미지 추출
    - test_resolution 함수 (라인 85-110): 테스트 및 검증
상태: 
주소: markdown_image_url_resolver
참조: image_analyzer_claude_sdk
"""

import re
import urllib.parse
from typing import List, Tuple
from pathlib import Path

class MarkdownImageResolver:
    """
    마크다운 파일의 상대 이미지 경로를 웹 URL과 결합하여 절대 URL 생성
    """
    
    def __init__(self, base_web_url: str):
        """
        Args:
            base_web_url: 기본 웹페이지 URL (예: https://velog.io/@jungseokheo/hanghaeplus5thweek)
        """
        self.base_web_url = base_web_url.rstrip('/')
        
    def resolve_image_url(self, relative_path: str) -> str:
        """
        상대 경로를 절대 URL로 변환
        
        Args:
            relative_path: MD 파일 내 상대 이미지 경로
            
        Returns:
            절대 이미지 URL
        """
        # URL 인코딩된 경로 처리
        if '%' in relative_path:
            # 이미 URL 인코딩된 경우 그대로 사용
            encoded_path = relative_path
        else:
            # URL 인코딩 필요한 경우
            encoded_path = urllib.parse.quote(relative_path, safe='/')
        
        # 기본 URL에서 마지막 세그먼트 제거하고 이미지 경로 추가
        # 예: https://velog.io/@jungseokheo/hanghaeplus5thweek + /상대경로
        absolute_url = f"{self.base_web_url}/{encoded_path}"
        
        return absolute_url
    
    def extract_images_from_markdown(self, markdown_content: str) -> List[Tuple[str, str]]:
        """
        마크다운에서 이미지 정보 추출
        
        Args:
            markdown_content: 마크다운 파일 내용
            
        Returns:
            List[(alt_text, relative_path)]: 이미지 정보 리스트
        """
        # 마크다운 이미지 패턴: ![alt](path)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(pattern, markdown_content)
        return matches

def test_resolution():
    """테스트 함수"""
    base_url = "https://velog.io/@jungseokheo/hanghaeplus5thweek"
    resolver = MarkdownImageResolver(base_url)
    
    # 실제 MD 파일에서 추출한 상대 경로들
    test_paths = [
        "image.png",
        "image.1.png", 
        "image.2.png",
        "%EB%93%B1%EA%B0%80%EA%B5%90%ED%99%98%EC%9D%B4%EB%8B%A4!%20%EB%82%B4%2010%EC%A3%BC%EC%9D%98%20%EB%B0%98%EC%9D%84%20%EC%A4%84%20%ED%85%8C%EB%8B%88%EA%B9%8C%20OO%EC%9D%84%20%EB%82%98%EC%97%90%EA%B2%8C%20%EC%A4%98!(%ED%95%AD%ED%95%B4%20%ED%94%8C%EB%9F%AC%EC%8A%A4%20%ED%94%84%EB%A1%A0%ED%8A%B8%206%EA%B8%B0%20%ED%9A%8C%EA%B3%A0%205%EF%B8%8F%E2%83%A3%EC%A3%BC%EC%B0%A8)/image.2.png"
    ]
    
    print("🔗 이미지 URL 해결 테스트")
    print(f"기본 URL: {base_url}")
    print("-" * 80)
    
    for i, path in enumerate(test_paths, 1):
        absolute_url = resolver.resolve_image_url(path)
        print(f"{i}. 상대 경로: {path}")
        print(f"   절대 URL: {absolute_url}")
        print()

if __name__ == "__main__":
    test_resolution()