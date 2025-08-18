#!/usr/bin/env python3
"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: Knowledge Sherpa FastAPI 서버 실행 스크립트
상세 내용:
    - 의존성 체크 및 자동 설치
    - 서버 실행 및 상태 모니터링
    - 브라우저 자동 열기 옵션
    - 에러 처리 및 사용자 안내
상태: 활성
주소: knowledge_web/run_server
참조: app.py
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def check_and_install_dependencies():
    """필요한 의존성을 체크하고 필요시 설치합니다."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'python-multipart',
        'jinja2',
        'youtube-transcript-api',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("📦 필요한 패키지 설치 중...")
        for package in missing_packages:
            print(f"   - {package} 설치 중...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ {package} 설치 완료")
            except subprocess.CalledProcessError:
                print(f"   ❌ {package} 설치 실패")
                return False
        print("✅ 모든 패키지 설치 완료!")
    else:
        print("✅ 모든 의존성이 이미 설치되어 있습니다.")
    
    return True

def main():
    """메인 실행 함수"""
    print("🚀 Knowledge Sherpa 웹 서버 시작 중...")
    print("=" * 50)
    
    # 의존성 체크 및 설치
    if not check_and_install_dependencies():
        print("❌ 의존성 설치에 실패했습니다.")
        print("수동 설치: pip install -r requirements.txt")
        return 1
    
    # 서버 실행
    try:
        print("🌐 웹 서버 시작 중...")
        print("📍 서버 주소: http://localhost:8000")
        print("📍 API 문서: http://localhost:8000/docs")
        print("⏹️  종료하려면 Ctrl+C를 누르세요")
        print("=" * 50)
        
        # 브라우저 자동 열기 (선택적)
        try:
            # 3초 후 브라우저 열기
            import threading
            def open_browser():
                time.sleep(3)
                webbrowser.open('http://localhost:8000')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            print("🌐 3초 후 브라우저가 자동으로 열립니다...")
        except:
            print("💡 브라우저를 수동으로 열어 http://localhost:8000 에 접속하세요.")
        
        # uvicorn 서버 실행
        os.system(f"{sys.executable} -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
        
    except KeyboardInterrupt:
        print("\n🛑 서버가 사용자에 의해 중단되었습니다.")
        return 0
    except Exception as e:
        print(f"❌ 서버 실행 중 오류 발생: {e}")
        print("\n문제 해결 방법:")
        print("1. Python 버전 확인 (3.7 이상 권장)")
        print("2. 포트 8000이 사용 중인지 확인")
        print("3. 수동 실행: uvicorn app:app --reload")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)