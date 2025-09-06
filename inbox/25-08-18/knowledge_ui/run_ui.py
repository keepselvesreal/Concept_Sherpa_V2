#!/usr/bin/env python3
"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: Knowledge Sherpa UI 실행 스크립트
상세 내용:
    - UI 실행을 위한 간단한 런처 스크립트
    - 필요한 의존성 체크
    - 에러 처리 및 사용자 안내
상태: 활성
주소: knowledge_ui/run_ui
참조: main_ui.py
"""

import sys
import os

def check_dependencies():
    """필요한 의존성을 체크합니다."""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import youtube_transcript_api
    except ImportError:
        missing_deps.append("youtube-transcript-api")
    
    return missing_deps

def main():
    """메인 실행 함수"""
    print("🚀 Knowledge Sherpa UI 시작 중...")
    
    # 의존성 체크
    missing = check_dependencies()
    if missing:
        print("❌ 필요한 라이브러리가 설치되지 않았습니다:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n설치 명령어:")
        if "youtube-transcript-api" in missing:
            print("   pip install youtube-transcript-api")
        if "tkinter" in missing:
            print("   tkinter는 Python 표준 라이브러리입니다. Python 재설치가 필요할 수 있습니다.")
        return
    
    # UI 실행
    try:
        from main_ui import main as run_ui
        print("✅ 의존성 확인 완료")
        print("🎯 UI 실행 중...")
        run_ui()
    except Exception as e:
        print(f"❌ UI 실행 중 오류 발생: {e}")
        print("\n문제 해결 방법:")
        print("1. Python 버전 확인 (3.7 이상 권장)")
        print("2. 필요한 라이브러리 설치 확인")
        print("3. 파일 권한 확인")

if __name__ == "__main__":
    main()