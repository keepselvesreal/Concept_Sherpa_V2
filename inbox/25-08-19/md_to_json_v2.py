#!/usr/bin/env python3
"""
생성 시간: 2025-08-19 07:54:55 KST
핵심 내용: MD 파일에서 첫 번째 # 헤더를 추출하여 JSON 파일 생성하는 스크립트 (숫자 제거 버전)
상세 내용:
    - extract_first_header(md_file_path: str) -> str: MD 파일에서 첫 번째 # 헤더의 텍스트 추출 (숫자.형태 제거)
    - create_json_from_md(md_file_path: str) -> None: JSON 파일 생성 (id: 0, title: 정제된 헤더, level: 0)
    - main(): 명령행 인자 처리 및 실행
상태: 활성
주소: md_to_json_v2
참조: md_to_json
"""

import sys
import re
import json
import os


def extract_first_header(md_file_path: str) -> str:
    """MD 파일에서 첫 번째 # 헤더의 텍스트를 추출 (숫자. 형태 제거)"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 첫 번째 # 헤더 찾기 (## 등은 제외)
                match = re.match(r'^#\s+(.*)', line.strip())
                if match:
                    title = match.group(1).strip()
                    # 앞의 숫자. 형태 제거 (예: "1. Build a basic chatbot" -> "Build a basic chatbot")
                    clean_title = re.sub(r'^\d+\.\s*', '', title)
                    return clean_title
        return "제목 없음"
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다: {md_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"오류: 파일 읽기 실패: {e}")
        sys.exit(1)


def create_json_from_md(md_file_path: str) -> None:
    """MD 파일에서 JSON 파일 생성"""
    # 첫 번째 헤더 추출
    title = extract_first_header(md_file_path)
    
    # JSON 데이터 구성
    json_data = {
        "id": 0,
        "title": title,
        "level": 0
    }
    
    # 출력 파일명 생성 (확장자를 .json으로 변경)
    base_name = os.path.splitext(md_file_path)[0]
    json_file_path = f"{base_name}.json"
    
    # JSON 파일 생성
    try:
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)
        print(f"JSON 파일 생성 완료: {json_file_path}")
        print(f"추출된 제목: {title}")
    except Exception as e:
        print(f"오류: JSON 파일 생성 실패: {e}")
        sys.exit(1)


def main():
    """메인 함수"""
    if len(sys.argv) != 2:
        print("사용법: python md_to_json_v2.py <md_file_path>")
        sys.exit(1)
    
    md_file_path = sys.argv[1]
    
    # 파일 존재 확인
    if not os.path.exists(md_file_path):
        print(f"오류: 파일이 존재하지 않습니다: {md_file_path}")
        sys.exit(1)
    
    # JSON 생성
    create_json_from_md(md_file_path)


if __name__ == "__main__":
    main()