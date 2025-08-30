# 생성 시간: Sat Aug 30 15:42:56 KST 2025
# 핵심 내용: 범용 노드 JSON 파일을 읽어서 개별 노드 정보 문서를 생성하는 스크립트 (명령줄 인자로 JSON 경로 받음)
# 상세 내용:
#   - load_nodes() (line 28): JSON 노드 파일 로드
#   - generate_node_documents() (line 45): 개별 노드 정보 문서 생성 메인 함수
#   - create_single_node_document() (line 65): 단일 노드 문서 생성 (새로운 섹션 구조 적용)
#   - main() (line 112): 메인 실행 함수 (argparse로 JSON 경로 받음)
# 상태: active
# 주소: node_document_generator/v2
# 참조: node_document_generator

#!/usr/bin/env uv run python

import json
import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any

def load_nodes(nodes_file: str) -> List[Dict[str, Any]]:
    """
    노드 JSON 파일을 로드합니다.
    
    Args:
        nodes_file: 노드 JSON 파일 경로
        
    Returns:
        노드 리스트
    """
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"📊 {len(nodes)}개 노드 로드 완료: {nodes_file}")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 실패: {e}")
        return []

def generate_node_documents(nodes: List[Dict[str, Any]], output_dir: str) -> None:
    """
    각 노드에 대한 개별 정보 문서를 생성합니다.
    
    Args:
        nodes: 노드 리스트
        output_dir: 출력 디렉토리
    """
    print("📄 개별 노드 정보 문서 생성 중...")
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    created_count = 0
    for node in nodes:
        if create_single_node_document(node, nodes, output_dir):
            created_count += 1
    
    print(f"   ✅ {created_count}개 노드 문서 생성 완료")

def create_single_node_document(node: Dict[str, Any], all_nodes: List[Dict[str, Any]], output_dir: str) -> bool:
    """
    단일 노드 문서를 생성합니다.
    
    Args:
        node: 대상 노드
        all_nodes: 전체 노드 리스트 (관계 정보 참조용)
        output_dir: 출력 디렉토리
        
    Returns:
        생성 성공 여부
    """
    try:
        # 파일명 생성: {id}_lev{level}_title_info.md
        title_clean = re.sub(r'[^\w\s.-]', '', node['title'])  # 점(.)도 유지
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        
        filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
        filepath = os.path.join(output_dir, filename)
        
        # 문서 내용 생성 (새로운 섹션 구조)
        content = f"""# 속성
---
process_status: false

# 추출
---

## 핵심 내용

## 상세 핵심 내용

## 상세 내용

## 주요 화제

## 부차 화제

# 내용
---

# 구성
---
"""
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"   ❌ 노드 문서 생성 실패 (ID: {node.get('id', '?')}): {e}")
        return False

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='노드 JSON 파일로부터 개별 노드 정보 문서를 생성합니다.')
    parser.add_argument('json_file', help='노드 JSON 파일 경로')
    parser.add_argument('--output-dir', '-o', help='출력 디렉토리 (지정하지 않으면 JSON 파일과 같은 디렉토리에 자동 생성)')
    
    args = parser.parse_args()
    
    print("🚀 노드 문서 생성 스크립트 시작")
    
    # JSON 파일 경로 검증
    if not os.path.exists(args.json_file):
        print(f"❌ JSON 파일을 찾을 수 없습니다: {args.json_file}")
        return
    
    # 출력 디렉토리 설정
    if args.output_dir:
        output_docs_dir = args.output_dir
    else:
        # JSON 파일과 같은 디렉토리에 자동 생성
        json_dir = os.path.dirname(args.json_file)
        json_name = Path(args.json_file).stem  # 확장자 제외한 파일명
        output_docs_dir = os.path.join(json_dir, f"{json_name}_docs")
    
    print(f"📁 출력 디렉토리: {output_docs_dir}")
    
    # 1. 노드 로드
    nodes = load_nodes(args.json_file)
    if not nodes:
        return
    
    # 2. 개별 노드 문서 생성
    generate_node_documents(nodes, output_docs_dir)
    
    print("✅ 모든 작업 완료!")
    print(f"📂 생성된 문서 위치: {output_docs_dir}")

if __name__ == "__main__":
    main()