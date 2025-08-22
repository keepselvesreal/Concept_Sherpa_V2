#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 12:15:30
핵심 내용: MD 파일에서 사용자 확인 필요 메타데이터 정보를 추출하여 JSON 파일 생성
상세 내용: 
    - main() (line 15): 메인 실행 함수, 명령행 인수 처리
    - extract_metadata() (line 35): MD 파일에서 체크박스 형태 메타데이터 추출
    - clean_key() (line 75): 키 이름 정리 (공백을 언더스코어로 변환)
상태: active
참조: extract_md_data.py
"""

import re
import json
import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python create_user_verification_data.py <markdown_file>")
        sys.exit(1)
    
    md_file_path = Path(sys.argv[1])
    
    if not md_file_path.exists():
        print(f"Error: File {md_file_path} not found")
        sys.exit(1)
    
    # MD 파일 읽기
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 사용자 확인 필요 정보 추출
    user_verification_data = extract_metadata(content)
    
    # 출력 파일명 생성 (원본 파일명 기반)
    base_name = md_file_path.stem
    # 새로운 파일명 형식(날짜_순번_id)에서 확장자 부분만 변경
    output_file = md_file_path.parent / f"{base_name}_user_verification.json"
    
    # JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(user_verification_data, f, ensure_ascii=False, indent=2)
    
    print(f"User verification data extracted: {len(user_verification_data)} fields")
    print(f"Saved to: {output_file}")


def extract_metadata(content):
    """MD 파일에서 사용자 확인 필요 메타데이터 추출 (Extracted Time 제외)"""
    user_verification_data = {}
    
    # 첫 번째 --- 구분자까지의 메타데이터 영역 찾기
    lines = content.split('\n')
    current_key = None
    
    for line in lines:
        if line.strip() == '---':
            break
        
        # **키:** 형태의 메타데이터 키 추출
        key_match = re.match(r'\*\*([^*]+):\*\*', line.strip())
        if key_match:
            current_key = key_match.group(1).strip()
            continue
        
        # 기존 **키:** **값 형태도 지원 (단순한 값)
        simple_match = re.match(r'\*\*([^*]+):\*\*\s*(.+)', line.strip())
        if simple_match:
            key = simple_match.group(1).strip()
            value = simple_match.group(2).strip()
            
            # "Extracted Time" 제외
            if key != "Extracted Time":
                clean_key_name = clean_key(key)
                user_verification_data[clean_key_name] = value
            continue
        
        # 체크박스 형태의 값 추출 (- [x] 값)
        if current_key:
            checkbox_match = re.match(r'-\s*\[x\]\s*(.+)', line.strip())
            if checkbox_match:
                value = checkbox_match.group(1).strip()
                
                # "Extracted Time" 제외
                if current_key != "Extracted Time":
                    clean_key_name = clean_key(current_key)
                    user_verification_data[clean_key_name] = value
                current_key = None  # 키 초기화
    
    return user_verification_data


def clean_key(key):
    """키 이름 정리 (공백을 언더스코어로 변환, 소문자화)"""
    return key.lower().replace(" ", "_")


if __name__ == "__main__":
    main()