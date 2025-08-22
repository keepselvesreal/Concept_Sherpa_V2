#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 11:21:35
핵심 내용: Markdown 파일에서 노드 정보와 사용자 입력 정보를 추출하여 JSON 파일로 생성하는 스크립트
상세 내용: 
    - main() (line 15): 메인 실행 함수, 명령행 인수 처리 및 전체 플로우 제어
    - extract_headers() (line 30): MD 파일에서 # 헤더 추출 및 노드 정보 JSON 생성
    - extract_metadata() (line 50): MD 파일 상단 메타데이터 추출 및 사용자 입력 정보 JSON 생성
    - clean_title() (line 70): 헤더 텍스트에서 숫자 제거 및 정제
상태: active
참조: 없음
"""

import re
import json
import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python extract_md_data.py <markdown_file>")
        sys.exit(1)
    
    md_file_path = Path(sys.argv[1])
    
    if not md_file_path.exists():
        print(f"Error: File {md_file_path} not found")
        sys.exit(1)
    
    # MD 파일 읽기
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 노드 정보 추출
    nodes = extract_headers(content)
    
    # 출력 파일명 생성 (원본 파일명 기반)
    base_name = md_file_path.stem
    # 새로운 파일명 형식(날짜_순번_id)에서 확장자 부분만 변경
    nodes_file = md_file_path.parent / f"{base_name}_nodes.json"
    
    # JSON 파일로 저장
    with open(nodes_file, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)
    
    print(f"Nodes extracted: {len(nodes)} headers")
    print(f"Nodes saved to: {nodes_file}")


def extract_headers(content):
    """MD 파일에서 헤더를 추출하여 노드 정보 생성"""
    nodes = []
    node_id = 0
    
    # Content Processing 값 확인
    metadata = extract_metadata(content)
    is_unified = metadata.get("Content Processing") == "unified"
    
    # # 로 시작하는 헤더 찾기 (한 줄씩 처리)
    lines = content.split('\n')
    first_header_processed = False
    
    for line in lines:
        if line.strip().startswith('#'):
            # 헤더 레벨과 텍스트 추출
            match = re.match(r'^(#+)\s*(.+)', line.strip())
            if match:
                header_level = len(match.group(1))  # # 개수
                header_text = match.group(2).strip()
                cleaned_title = clean_title(header_text)
                
                # unified인 경우 첫 번째 헤더(제목)만 처리
                if is_unified:
                    if not first_header_processed:
                        node = {
                            "id": node_id,
                            "level": header_level - 1,  # 헤더 레벨 - 1
                            "title": cleaned_title
                        }
                        nodes.append(node)
                        node_id += 1
                        first_header_processed = True
                else:
                    # unified가 아닌 경우 모든 헤더 처리
                    node = {
                        "id": node_id,
                        "level": header_level - 1,  # 헤더 레벨 - 1
                        "title": cleaned_title
                    }
                    nodes.append(node)
                    node_id += 1
    
    return nodes


def extract_metadata(content):
    """MD 파일에서 메타데이터 추출하여 사용자 입력 정보 생성"""
    user_input = {}
    
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
                user_input[key] = value
            continue
        
        # 체크박스 형태의 값 추출 (- [x] 값)
        if current_key:
            checkbox_match = re.match(r'-\s*\[x\]\s*(.+)', line.strip())
            if checkbox_match:
                value = checkbox_match.group(1).strip()
                
                # "Extracted Time" 제외
                if current_key != "Extracted Time":
                    user_input[current_key] = value
                current_key = None  # 키 초기화
    
    return user_input


def clean_title(title):
    """헤더 텍스트에서 숫자 제거 및 정제"""
    # 맨 앞의 숫자와 점/공백 제거 (예: "1. Title" -> "Title")
    cleaned = re.sub(r'^\d+\.?\s*', '', title)
    
    # 추가적인 정리가 필요한 경우 여기에 추가
    cleaned = cleaned.strip()
    
    return cleaned


if __name__ == "__main__":
    main()