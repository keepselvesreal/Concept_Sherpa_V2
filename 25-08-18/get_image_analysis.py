"""
생성 시간: 2025-08-18 20:44:37 KST
핵심 내용: 이미지 분석 결과를 파일로 저장하는 스크립트
상세 내용:
    - 로그 출력 최소화
    - 분석 결과만 깔끔하게 출력
상태: 
주소: get_image_analysis
참조: image_analyzer_claude_sdk
"""

import asyncio
import logging
from image_analyzer_claude_sdk import ImageAnalyzer

async def main():
    # 로그 레벨을 ERROR로 설정해서 분석 결과만 출력
    logging.basicConfig(level=logging.ERROR)
    
    analyzer = ImageAnalyzer()
    result = await analyzer.analyze_image_from_url(
        "https://velog.io/@jungseokheo/hanghaeplus5thweek/image.2.png",
        "이미지 속 텍스트와 반응, 내용을 자세히 분석해주세요"
    )
    
    if result.success:
        print("=" * 50)
        print("이미지 분석 결과")
        print("=" * 50)
        print(result.content)
        print("=" * 50)
    else:
        print("분석 실패:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())