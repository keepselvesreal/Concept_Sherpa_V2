"""
생성 시간: 2025-08-18 15:30:00
핵심 내용: Chrome 세션 연결 및 Medium 접근 테스트
상세 내용:
    - ChromeSessionTester 클래스 (라인 25-120): Chrome 세션 연결 테스터
    - connect_to_chrome 메서드 (라인 35-55): Chrome 브라우저 연결
    - test_medium_access 메서드 (라인 57-85): Medium 유료 콘텐츠 접근 테스트
    - extract_content 메서드 (라인 87-105): 기본 콘텐츠 추출
    - run_verification 메서드 (라인 107-120): 전체 검증 실행
상태: 
주소: chrome_session_tester
참조: 
"""

import asyncio
import logging
from playwright.async_api import async_playwright, Browser, Page
from typing import Optional, Dict, Any
from dataclasses import dataclass
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """테스트 결과 데이터 구조"""
    success: bool
    message: str
    content_length: int = 0
    has_paywall: bool = False
    execution_time: float = 0.0

class ChromeSessionTester:
    """
    Chrome 세션 연결 및 콘텐츠 추출 테스터
    - 기존 Chrome 인스턴스에 연결
    - Medium 유료 콘텐츠 접근 테스트
    - 실제 콘텐츠 추출 검증
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def connect_to_chrome(self, debug_port: int = 9222) -> TestResult:
        """
        실행 중인 Chrome에 연결
        Chrome을 --remote-debugging-port=9222로 실행해야 함
        """
        start_time = time.time()
        
        try:
            playwright = await async_playwright().start()
            
            # Chrome에 연결 시도
            self.browser = await playwright.chromium.connect_over_cdp(
                f"http://localhost:{debug_port}"
            )
            
            # 기존 컨텍스트 가져오기 (첫 번째 컨텍스트 사용)
            contexts = self.browser.contexts
            if not contexts:
                # 새 컨텍스트 생성
                context = await self.browser.new_context()
            else:
                context = contexts[0]
            
            # 새 페이지 생성
            self.page = await context.new_page()
            
            execution_time = time.time() - start_time
            
            logger.info(f"Chrome 연결 성공! (실행시간: {execution_time:.2f}초)")
            return TestResult(
                success=True,
                message="Chrome 연결 성공",
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Chrome 연결 실패: {str(e)}"
            logger.error(error_msg)
            
            return TestResult(
                success=False,
                message=error_msg,
                execution_time=execution_time
            )
    
    async def test_medium_access(self, medium_url: str) -> TestResult:
        """
        Medium 유료 콘텐츠 접근 테스트
        페이월이 있는지, 전체 콘텐츠에 접근 가능한지 확인
        """
        if not self.page:
            return TestResult(success=False, message="Chrome 페이지가 연결되지 않음")
        
        start_time = time.time()
        
        try:
            logger.info(f"Medium 페이지 접근 중: {medium_url}")
            
            # 페이지 로드
            await self.page.goto(medium_url, wait_until="networkidle")
            
            # 페이지 제목 확인
            title = await self.page.title()
            logger.info(f"페이지 제목: {title}")
            
            # 페이월 감지
            paywall_indicators = [
                "text=Member-only",
                "text=Members-only", 
                "[data-testid='paywall']",
                ".paywall",
                "text=Become a member"
            ]
            
            has_paywall = False
            for indicator in paywall_indicators:
                try:
                    element = await self.page.wait_for_selector(indicator, timeout=2000)
                    if element:
                        has_paywall = True
                        logger.warning(f"페이월 감지됨: {indicator}")
                        break
                except:
                    continue
            
            # 메인 콘텐츠 추출
            content = await self.extract_content_basic()
            execution_time = time.time() - start_time
            
            if has_paywall:
                return TestResult(
                    success=False,
                    message="페이월이 감지됨 - 로그인 상태 확인 필요",
                    content_length=len(content),
                    has_paywall=True,
                    execution_time=execution_time
                )
            else:
                return TestResult(
                    success=True,
                    message="Medium 접근 성공",
                    content_length=len(content),
                    has_paywall=False,
                    execution_time=execution_time
                )
                
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Medium 접근 실패: {str(e)}"
            logger.error(error_msg)
            
            return TestResult(
                success=False,
                message=error_msg,
                execution_time=execution_time
            )
    
    async def extract_content_basic(self) -> str:
        """
        기본 콘텐츠 추출 (테스트용)
        article 태그나 main 태그에서 텍스트 추출
        """
        if not self.page:
            return ""
        
        try:
            # Medium의 주요 콘텐츠 영역들
            selectors = [
                "article",
                "[data-testid='storyContent']", 
                "main",
                ".postArticle-content"
            ]
            
            for selector in selectors:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=5000)
                    if element:
                        content = await element.inner_text()
                        logger.info(f"콘텐츠 추출 성공 ({selector}): {len(content)} 문자")
                        return content
                except:
                    continue
            
            # fallback: body 전체 텍스트
            body_content = await self.page.inner_text("body")
            logger.info(f"Fallback 콘텐츠 추출: {len(body_content)} 문자")
            return body_content
            
        except Exception as e:
            logger.error(f"콘텐츠 추출 실패: {str(e)}")
            return ""
    
    async def run_verification(self, medium_url: str) -> Dict[str, TestResult]:
        """
        전체 검증 프로세스 실행
        1. Chrome 연결
        2. Medium 접근
        3. 결과 종합
        """
        results = {}
        
        # 1단계: Chrome 연결
        logger.info("=== Chrome 연결 테스트 ===")
        connect_result = await self.connect_to_chrome()
        results["chrome_connection"] = connect_result
        
        if not connect_result.success:
            logger.error("Chrome 연결 실패로 테스트 중단")
            return results
        
        # 2단계: Medium 접근
        logger.info("=== Medium 접근 테스트 ===")
        medium_result = await self.test_medium_access(medium_url)
        results["medium_access"] = medium_result
        
        # 정리
        if self.browser:
            await self.browser.close()
        
        return results
    
    def print_results(self, results: Dict[str, TestResult]):
        """테스트 결과 출력"""
        print("\n" + "="*50)
        print("Chrome 세션 연결 테스트 결과")
        print("="*50)
        
        for test_name, result in results.items():
            status = "✅ 성공" if result.success else "❌ 실패"
            print(f"\n{test_name.upper()}:")
            print(f"  상태: {status}")
            print(f"  메시지: {result.message}")
            print(f"  실행시간: {result.execution_time:.2f}초")
            
            if hasattr(result, 'content_length') and result.content_length > 0:
                print(f"  콘텐츠 길이: {result.content_length} 문자")
            
            if hasattr(result, 'has_paywall'):
                paywall_status = "있음" if result.has_paywall else "없음"
                print(f"  페이월: {paywall_status}")

async def main():
    """테스트 실행 예시"""
    tester = ChromeSessionTester()
    
    # 테스트할 Medium URL (유료 콘텐츠로 변경하세요)
    test_url = "https://medium.com/@example/some-premium-article"
    
    print("Chrome 세션 테스터 시작")
    print("주의: Chrome을 다음 명령으로 실행해야 합니다:")
    print("chrome --remote-debugging-port=9222")
    print("")
    
    # 실제 URL 입력 받기
    url = input("테스트할 Medium URL을 입력하세요: ").strip()
    if url:
        test_url = url
    
    results = await tester.run_verification(test_url)
    tester.print_results(results)

if __name__ == "__main__":
    asyncio.run(main())