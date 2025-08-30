# 생성 시간: Sat Aug 30 15:11:48 KST 2025
# 핵심 내용: 노드 JSON 파일을 읽어서 개별 노드 정보 문서를 생성하는 스크립트 (추출 섹션 하위에 5개 하위 섹션 포함)
# 상세 내용:
#   - load_nodes() (line 25): JSON 노드 파일 로드
#   - generate_node_documents() (line 42): 개별 노드 정보 문서 생성 메인 함수
#   - create_single_node_document() (line 62): 단일 노드 문서 생성 (새로운 섹션 구조 적용)
#   - main() (line 106): 메인 실행 함수
# 상태: active
# 주소: node_document_generator
# 참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/node_processor.py의 노드 문서 생성 부분

#!/usr/bin/env uv run python

import json
import os
import re
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
        print(f"📊 {len(nodes)}개 노드 로드 완료")
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
    print("🚀 노드 문서 생성 스크립트 시작")
    
    # 경로 설정
    process_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process"
    nodes_file = os.path.join(process_dir, "nodes_updated.json")
    output_docs_dir = os.path.join("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30", "node_docs")
    
    # 1. 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        return
    
    # 2. 개별 노드 문서 생성
    generate_node_documents(nodes, output_docs_dir)
    
    print("✅ 모든 작업 완료!")

if __name__ == "__main__":
    main()