"""
생성 시간: 2025-08-18 20:30:37 KST
핵심 내용: Claude SDK 기반 URL 이미지 분석 스크립트
상세 내용:
    - ImageAnalyzer 클래스 (라인 45-150): 메인 이미지 분석 엔진
    - analyze_image_from_url 메서드 (라인 65-120): URL 기반 이미지 분석 함수
    - _download_image 메서드 (라인 122-140): 이미지 다운로드 유틸리티
    - _encode_image_to_base64 메서드 (라인 142-150): Base64 인코딩 함수
    - main 함수 (라인 155-190): CLI 인터페이스 및 사용 예제
상태: 
주소: image_analyzer_claude_sdk
참조: claude_response_generator
"""

import asyncio
import sys
import logging
import base64
import urllib.parse
import tempfile
import os
from typing import Optional, Tuple
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

logger = logging.getLogger(__name__)

class ImageAnalysisResult:
    """이미지 분석 결과"""
    def __init__(self, content: str, success: bool, error_message: Optional[str] = None):
        self.content = content
        self.success = success
        self.error_message = error_message

class ImageAnalyzer:
    """
    Claude SDK 기반 URL 이미지 분석기
    - URL에서 이미지를 다운로드하고 Claude에게 분석 요청
    - 이미지 내용 추출, 설명, 텍스트 인식 등 지원
    """
    
    def __init__(self):
        """이미지 분석기 초기화"""
        self.options = ClaudeCodeOptions(
            system_prompt="""당신은 이미지 분석 전문가입니다. 
제공된 이미지를 자세히 분석하고 다음 정보를 한국어로 제공하세요:
1. 이미지의 전체적인 내용과 구성
2. 포함된 텍스트가 있다면 정확히 추출
3. 주요 객체, 인물, 장면 설명
4. 색상, 스타일, 레이아웃 특징
5. 전체적인 맥락과 의미 해석""",
            max_turns=1
        )
        logger.info("ImageAnalyzer 초기화 완료")
    
    async def analyze_image_from_url(
        self, 
        image_url: str, 
        custom_prompt: Optional[str] = None
    ) -> ImageAnalysisResult:
        """
        URL에서 이미지를 다운로드하여 분석
        
        Args:
            image_url: 분석할 이미지 URL
            custom_prompt: 추가 분석 요청사항
            
        Returns:
            ImageAnalysisResult: 분석 결과
        """
        logger.info(f"이미지 분석 시작 - URL: {image_url}")
        
        temp_file_path = None
        try:
            # 1. 이미지 다운로드
            image_data, content_type = await self._download_image(image_url)
            if not image_data:
                return ImageAnalysisResult(
                    content="이미지 다운로드에 실패했습니다.",
                    success=False,
                    error_message="Image download failed"
                )
            
            # 2. 임시 파일로 저장
            temp_file_path = await self._save_temp_image(image_data)
            
            # 3. 프롬프트 구성
            prompt_text = f"다음 이미지 파일을 분석해주세요: {temp_file_path}"
            if custom_prompt:
                prompt_text += f"\n\n추가 요청사항: {custom_prompt}"
            
            # 4. Claude에게 이미지 분석 요청
            response_content = ""
            async for message in query(
                prompt=prompt_text,
                options=self.options
            ):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_content += block.text
            
            if response_content:
                logger.info("이미지 분석 성공")
                return ImageAnalysisResult(
                    content=response_content.strip(),
                    success=True
                )
            else:
                logger.warning("Claude로부터 빈 응답 수신")
                return ImageAnalysisResult(
                    content="이미지 분석에 실패했습니다.",
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
        finally:
            # 임시 파일 정리
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.info(f"임시 파일 삭제: {temp_file_path}")
                except Exception as e:
                    logger.warning(f"임시 파일 삭제 실패: {e}")
    
    async def _download_image(self, url: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        URL에서 이미지 다운로드
        
        Args:
            url: 이미지 URL
            
        Returns:
            Tuple[이미지 데이터, content-type]
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content, response.headers.get('content-type')
        except Exception as e:
            logger.error(f"이미지 다운로드 실패: {e}")
            return None, None
    
    async def _save_temp_image(self, image_data: bytes) -> str:
        """
        이미지 데이터를 임시 파일로 저장
        
        Args:
            image_data: 이미지 바이트 데이터
            
        Returns:
            임시 파일 경로
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(image_data)
            temp_path = tmp_file.name
        logger.info(f"임시 파일 저장: {temp_path}")
        return temp_path
    
    def _encode_image_to_base64(self, image_data: bytes) -> str:
        """
        이미지 데이터를 Base64로 인코딩
        
        Args:
            image_data: 이미지 바이트 데이터
            
        Returns:
            Base64 인코딩된 문자열
        """
        return base64.b64encode(image_data).decode('utf-8')

# CLI 인터페이스
async def main():
    """메인 함수 - CLI 인터페이스"""
    if len(sys.argv) < 2:
        print("사용법: python image_analyzer_claude_sdk.py <이미지_URL> [추가_요청사항]")
        print("예시: python image_analyzer_claude_sdk.py 'https://example.com/image.jpg' '이미지의 텍스트만 추출해주세요'")
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

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 실행
    asyncio.run(main())