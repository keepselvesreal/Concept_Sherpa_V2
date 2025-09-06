"""
생성 시간: 2025-08-18 21:15:42 KST
핵심 내용: Claude SDK 기반 URL 직접 이미지 분석 스크립트 (anthropic SDK 사용)
상세 내용:
    - ImageAnalyzer 클래스 (라인 35-120): 메인 이미지 분석 엔진
    - analyze_image_from_url 메서드 (라인 55-100): URL 기반 직접 이미지 분석 함수
    - _validate_url 메서드 (라인 102-115): URL 유효성 검사 함수
    - main 함수 (라인 120-160): CLI 인터페이스 및 사용 예제
상태: 
주소: image_analyzer_claude_sdk/v2
참조: image_analyzer_claude_sdk
"""

import asyncio
import sys
import logging
import os
import urllib.parse
from typing import Optional
import anthropic

logger = logging.getLogger(__name__)

class ImageAnalysisResult:
    """이미지 분석 결과"""
    def __init__(self, content: str, success: bool, error_message: Optional[str] = None):
        self.content = content
        self.success = success
        self.error_message = error_message

class ImageAnalyzer:
    """
    Claude SDK 기반 URL 직접 이미지 분석기
    - URL 이미지를 Claude API에 직접 전달하여 분석
    - 다운로드나 임시 파일 없이 바로 처리
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        이미지 분석기 초기화
        
        Args:
            api_key: Claude API 키 (None이면 환경변수에서 가져옴)
        """
        self.client = anthropic.Anthropic(
            api_key=api_key or os.getenv('ANTHROPIC_API_KEY')
        )
        logger.info("ImageAnalyzer 초기화 완료")
    
    async def analyze_image_from_url(
        self, 
        image_url: str, 
        custom_prompt: Optional[str] = None
    ) -> ImageAnalysisResult:
        """
        URL 이미지를 Claude에게 직접 분석 요청
        
        Args:
            image_url: 분석할 이미지 URL
            custom_prompt: 추가 분석 요청사항
            
        Returns:
            ImageAnalysisResult: 분석 결과
        """
        logger.info(f"이미지 분석 시작 - URL: {image_url}")
        
        try:
            # URL 유효성 검사
            if not self._validate_url(image_url):
                return ImageAnalysisResult(
                    content="유효하지 않은 이미지 URL입니다.",
                    success=False,
                    error_message="Invalid image URL"
                )
            
            # 기본 프롬프트 설정
            base_prompt = """이 이미지를 자세히 분석하고 다음 정보를 한국어로 제공하세요:
1. 이미지의 전체적인 내용과 구성
2. 포함된 텍스트가 있다면 정확히 추출
3. 주요 객체, 인물, 장면 설명
4. 색상, 스타일, 레이아웃 특징
5. 전체적인 맥락과 의미 해석"""
            
            # 사용자 추가 요청사항이 있으면 추가
            if custom_prompt:
                analysis_prompt = f"{base_prompt}\n\n추가 요청사항: {custom_prompt}"
            else:
                analysis_prompt = base_prompt
            
            # Claude API 호출
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "url",
                                    "url": image_url
                                }
                            },
                            {
                                "type": "text",
                                "text": analysis_prompt
                            }
                        ]
                    }
                ]
            )
            
            # 응답 처리
            if message.content and len(message.content) > 0:
                response_text = message.content[0].text
                logger.info("이미지 분석 성공")
                return ImageAnalysisResult(
                    content=response_text.strip(),
                    success=True
                )
            else:
                return ImageAnalysisResult(
                    content="Claude로부터 빈 응답을 받았습니다.",
                    success=False,
                    error_message="Empty response from Claude"
                )
                
        except Exception as e:
            error_msg = f"이미지 분석 중 오류 발생: {e}"
            logger.error(error_msg)
            return ImageAnalysisResult(
                content="이미지 분석 중 오류가 발생했습니다.",
                success=False,
                error_message=error_msg
            )
    
    def _validate_url(self, url: str) -> bool:
        """
        URL 유효성 검사
        
        Args:
            url: 검사할 URL
            
        Returns:
            유효성 여부
        """
        try:
            parsed = urllib.parse.urlparse(url)
            return parsed.scheme in ['http', 'https'] and parsed.netloc
        except Exception:
            return False

# CLI 인터페이스
async def main():
    """메인 함수 - CLI 인터페이스"""
    if len(sys.argv) < 2:
        print("사용법: python image_analyzer_claude_sdk_v2.py <이미지_URL> [추가_요청사항]")
        print("예시: python image_analyzer_claude_sdk_v2.py 'https://example.com/image.jpg' '이미지의 텍스트만 추출해주세요'")
        print("\n환경변수 설정 필요: ANTHROPIC_API_KEY")
        return
    
    # API 키 확인
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("export ANTHROPIC_API_KEY='your-api-key' 로 설정해주세요.")
        return
    
    # 인자 파싱
    image_url = sys.argv[1]
    custom_prompt = sys.argv[2] if len(sys.argv) > 2 else None
    
    # URL 디코딩 (필요한 경우)
    if '%' in image_url:
        image_url = urllib.parse.unquote(image_url)
        print(f"URL 디코딩됨: {image_url}")
    
    print(f"🔍 이미지 분석 시작")
    print(f"📎 URL: {image_url}")
    if custom_prompt:
        print(f"📋 추가 요청: {custom_prompt}")
    print("-" * 50)
    
    # 이미지 분석 실행
    analyzer = ImageAnalyzer()
    result = await analyzer.analyze_image_from_url(image_url, custom_prompt)
    
    # 결과 출력
    if result.success:
        print("✅ 분석 성공!")
        print("\n📊 분석 결과:")
        print("-" * 50)
        print(result.content)
    else:
        print("❌ 분석 실패!")
        if result.error_message:
            print(f"오류: {result.error_message}")
        print(f"내용: {result.content}")

# 사용 예제 함수
def example_usage():
    """사용 예제"""
    print("📚 사용 예제:")
    print("1. 기본 분석:")
    print("   python image_analyzer_claude_sdk_v2.py 'https://example.com/image.jpg'")
    print("\n2. 텍스트 추출:")
    print("   python image_analyzer_claude_sdk_v2.py 'https://example.com/screenshot.png' '이미지의 텍스트만 추출해주세요'")
    print("\n3. 광고 여부 판단:")
    print("   python image_analyzer_claude_sdk_v2.py 'https://example.com/content.png' '이 이미지는 광고인가요? 아니면 콘텐츠 이미지인가요?'")

if __name__ == "__main__":
    # 도움말 요청 처리
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        example_usage()
        sys.exit(0)
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 실행
    asyncio.run(main())