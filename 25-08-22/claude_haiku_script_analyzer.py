# -*- coding: utf-8 -*-
"""
생성 시간: 2025-08-22 16:38:04 KST
핵심 내용: Claude SDK를 사용해 Haiku 3.5 모델로 스크립트 파일의 핵심 내용을 추출하는 도구
상세 내용:
    - main() (라인 77-95): 메인 실행 함수, 인자 처리 및 전체 프로세스 관리
    - analyze_script_with_haiku() (라인 30-72): Claude Haiku 3.5를 사용한 스크립트 분석 함수
    - setup_argument_parser() (라인 13-27): 명령행 인자 파싱 설정
    - 클래스 및 상수 정의 (라인 1-11): 필수 임포트 및 설정
상태: active
주소: claude_haiku_script_analyzer
참조: 없음
"""

import argparse
import sys
import os
from pathlib import Path
from anthropic import Anthropic
from typing import Optional

# Claude 모델 설정
HAIKU_MODEL = "claude-3-haiku-20240307"

def setup_argument_parser() -> argparse.ArgumentParser:
    """명령행 인자 파싱을 위한 ArgumentParser 설정"""
    parser = argparse.ArgumentParser(
        description="Claude Haiku 3.5를 사용해 스크립트 파일의 핵심 내용을 추출합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "script_path",
        type=str,
        help="분석할 스크립트 파일의 경로"
    )
    
    return parser

def analyze_script_with_haiku(script_path: str) -> Optional[str]:
    """Claude Haiku 3.5를 사용해 스크립트의 핵심 내용을 추출"""
    
    # 파일 존재 확인
    if not os.path.exists(script_path):
        print(f"❌ 오류: 파일을 찾을 수 없습니다 - {script_path}")
        return None
    
    # 파일 읽기
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            script_content = file.read()
    except UnicodeDecodeError:
        try:
            with open(script_path, 'r', encoding='cp949') as file:
                script_content = file.read()
        except Exception as e:
            print(f"❌ 파일 읽기 오류: {e}")
            return None
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return None
    
    # Claude API 클라이언트 초기화
    try:
        client = Anthropic()
    except Exception as e:
        print(f"❌ Claude API 초기화 오류: {e}")
        print("💡 ANTHROPIC_API_KEY 환경변수를 설정했는지 확인하세요.")
        return None
    
    # 분석 프롬프트 구성
    prompt = f"""다음 스크립트의 핵심 내용을 추출해주세요. 분석 결과는 한국어로 작성하고 다음 형식으로 제공해주세요:

## 📋 스크립트 개요
- **파일명**: {os.path.basename(script_path)}
- **타입**: [스크립트 유형 판별]
- **주요 기능**: [핵심 기능 요약]

## 🎯 핵심 내용
[스크립트의 가장 중요한 3-5가지 내용을 간결하게 정리]

## 🔧 주요 구성요소
[주요 함수, 클래스, 변수 등의 핵심 구성요소]

## 💡 특이사항
[주목할 만한 특징이나 패턴이 있다면 언급]

스크립트 내용:
{script_content}
"""

    # Claude API 호출
    try:
        message = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        print(f"❌ Claude API 호출 오류: {e}")
        return None

def main():
    """메인 실행 함수"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    print("🔍 Claude Haiku 3.5 스크립트 분석기")
    print("=" * 50)
    print(f"📁 분석 대상: {args.script_path}")
    print()
    
    # 스크립트 분석 실행
    analysis_result = analyze_script_with_haiku(args.script_path)
    
    if analysis_result:
        print("✅ 분석 완료!")
        print()
        print(analysis_result)
    else:
        print("❌ 분석에 실패했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()