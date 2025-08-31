# 생성 시간: Sun Aug 31 15:03:43 KST 2025
# 핵심 내용: 범용 노드 정보 문서와 내용 문서 통합 스크립트 (재귀적 하위 노드 수집 기능 추가)
# 상세 내용:
#   - load_nodes_data() (line 33): JSON 노드 파일 로드
#   - load_metadata() (line 50): 메타데이터 JSON 파일 로드
#   - get_node_meta_info() (line 66): 노드 메타정보 생성
#   - find_content_file_by_title() (line 84): title 기반 내용 문서 자동 탐지
#   - normalize_title() (line 108): 제목 정규화 함수
#   - load_content_document() (line 119): 내용 문서 로드
#   - get_all_descendants_info() (line 135): 재귀적 하위 노드 정보 수집 (기존 get_children_info 수정)
#   - collect_descendant_ids() (line 159): 재귀적 하위 노드 ID 수집 헬퍼 함수
#   - integrate_single_document() (line 174): 단일 노드 문서 통합 (title 기반 매칭 적용)
#   - integrate_all_documents() (line 243): 모든 노드 문서 통합
#   - main() (line 264): 메인 실행 함수 (argparse 지원)
# 상태: active
# 주소: document_integrator/v3
# 참조: document_integrator/v2

#!/usr/bin/env uv run python

import json
import os
import re
import argparse
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime

def load_nodes_data(nodes_file: str) -> List[Dict[str, Any]]:
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
        print(f"📊 {len(nodes)}개 노드 데이터 로드 완료")
        return nodes
    except Exception as e:
        print(f"❌ 노드 데이터 로드 실패: {e}")
        return []

def load_metadata(metadata_file: str) -> Dict[str, Any]:
    """
    메타데이터 JSON 파일을 로드합니다.
    
    Args:
        metadata_file: 메타데이터 JSON 파일 경로
        
    Returns:
        메타데이터 딕셔너리
    """
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        print(f"⚠️ 메타데이터 로드 실패: {e}")
        return {}

def get_node_meta_info(metadata: Dict[str, Any]) -> str:
    """
    메타데이터 정보를 텍스트로 생성합니다.
    
    Args:
        metadata: 메타데이터 딕셔너리
        
    Returns:
        메타정보 텍스트
    """
    meta_info = f"""
source: {metadata.get('source', 'N/A')}
source_type: {metadata.get('source_type', 'N/A')}
source_language: {metadata.get('source_language', 'N/A')}
structure_type: {metadata.get('structure_type', 'N/A')}
content_processing: {metadata.get('content_processing', 'N/A')}
title: {metadata.get('title', 'N/A')}
folder_name: {metadata.get('folder_name', 'N/A')}
created_at: {metadata.get('created_at', 'N/A')}
"""
    return meta_info.strip()

def find_content_file_by_title(node_title: str, content_dir: str) -> Optional[str]:
    """
    노드 title을 기반으로 내용 문서 파일을 자동으로 찾습니다.
    
    Args:
        node_title: 노드 제목
        content_dir: 내용 문서 디렉토리
        
    Returns:
        매칭된 파일 경로 (없으면 None)
    """
    # 디렉토리 내 모든 .md 파일 탐색
    md_files = glob.glob(os.path.join(content_dir, "*.md"))
    
    # 정규화된 title 생성
    normalized_title = normalize_title(node_title)
    
    for file_path in md_files:
        filename = os.path.basename(file_path)
        filename_without_ext = os.path.splitext(filename)[0]
        normalized_filename = normalize_title(filename_without_ext)
        
        # 정규화된 제목과 파일명 매칭
        if normalized_title == normalized_filename:
            return file_path
    
    return None

def normalize_title(title: str) -> str:
    """
    제목을 정규화합니다 (node_document_generator와 동일한 로직 적용).
    
    Args:
        title: 원본 제목
        
    Returns:
        정규화된 제목
    """
    # node_document_generator와 동일한 정규화 로직
    title_clean = re.sub(r'[^\w\s.-]', '', title)  # 점(.)도 유지
    title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
    return title_clean

def load_content_document(content_file: str) -> str:
    """
    내용 문서를 로드합니다.
    
    Args:
        content_file: 내용 문서 파일 경로
        
    Returns:
        내용 텍스트
    """
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip()
    except Exception as e:
        print(f"   ⚠️ 내용 문서 로드 실패 ({content_file}): {e}")
        return ""

def get_all_descendants_info(node: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> List[str]:
    """
    노드의 모든 하위 노드들의 정보 문서 파일명을 재귀적으로 수집합니다.
    
    Args:
        node: 대상 노드
        all_nodes: 전체 노드 리스트
        
    Returns:
        모든 하위 노드 문서 파일명 리스트 (ID 순서)
    """
    # 모든 하위 노드 ID를 재귀적으로 수집
    descendant_ids = collect_descendant_ids(node, all_nodes, set())
    
    # ID로 정렬
    descendant_ids = sorted(descendant_ids)
    
    # 각 노드 ID에 대응하는 파일명 생성
    descendant_files = []
    for node_id in descendant_ids:
        descendant_node = next((n for n in all_nodes if n.get('id') == node_id), None)
        if descendant_node:
            # 파일명 생성
            title_clean = re.sub(r'[^\w\s.-]', '', descendant_node['title'])
            title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
            filename = f"{descendant_node['id']:02d}_lev{descendant_node['level']}_{title_clean}_info.md"
            descendant_files.append(filename)
    
    return descendant_files

def collect_descendant_ids(node: Dict[str, Any], all_nodes: List[Dict[str, Any]], visited: Set[int]) -> Set[int]:
    """
    노드의 모든 하위 노드 ID를 재귀적으로 수집합니다.
    
    Args:
        node: 현재 노드
        all_nodes: 전체 노드 리스트
        visited: 이미 방문한 노드 ID 집합 (무한 루프 방지)
        
    Returns:
        하위 노드 ID 집합
    """
    descendant_ids = set()
    
    # 현재 노드가 이미 방문된 경우 무한 루프 방지
    if node.get('id') in visited:
        return descendant_ids
    
    visited.add(node.get('id'))
    
    # 직접 자식 노드들 처리
    for child_id in node.get('children_ids', []):
        child_node = next((n for n in all_nodes if n.get('id') == child_id), None)
        if child_node:
            # 자식 노드 ID 추가
            descendant_ids.add(child_id)
            # 자식 노드의 하위 노드들을 재귀적으로 수집
            grandchildren_ids = collect_descendant_ids(child_node, all_nodes, visited.copy())
            descendant_ids.update(grandchildren_ids)
    
    return descendant_ids

def integrate_single_document(node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                            content_dir: str, node_docs_dir: str, metadata: Dict[str, Any]) -> bool:
    """
    단일 노드 문서를 통합합니다.
    
    Args:
        node: 대상 노드
        all_nodes: 전체 노드 리스트
        content_dir: 내용 문서 디렉토리
        node_docs_dir: 노드 문서 디렉토리
        metadata: 메타데이터 딕셔너리
        
    Returns:
        통합 성공 여부
    """
    try:
        # 노드 문서 파일 경로 생성
        title_clean = re.sub(r'[^\w\s.-]', '', node['title'])
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        node_doc_filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
        node_doc_path = os.path.join(node_docs_dir, node_doc_filename)
        
        # title 기반으로 내용 문서 자동 탐지
        content_file_path = find_content_file_by_title(node['title'], content_dir)
        
        # 기존 노드 문서 읽기
        if not os.path.exists(node_doc_path):
            print(f"   ❌ 노드 문서 없음: {node_doc_filename}")
            return False
            
        with open(node_doc_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 메타정보 생성
        meta_info = get_node_meta_info(metadata)
        
        # 내용 문서 로드
        content_text = ""
        if content_file_path:
            content_text = load_content_document(content_file_path)
            print(f"   ✅ 매칭된 내용 문서: {os.path.basename(content_file_path)}")
        else:
            print(f"   ⚠️ 매칭되는 내용 문서 없음: {node['title']}")
        
        # 모든 하위 노드 정보 수집 (재귀적)
        descendants_files = get_all_descendants_info(node, all_nodes)
        descendants_text = "\n".join(descendants_files) if descendants_files else ""
        
        # 레벨에 따른 헤더 생성
        header_prefix = "#" * node['level']  
        content_header = f"{header_prefix} {node['title']}"
        
        # 새로운 문서 내용 생성 (추출 섹션에 5개 하위 섹션 포함)
        new_content = f"""# 속성
---
process_status: false
{meta_info}

# 추출
---

## 핵심 내용

## 상세 핵심 내용

## 상세 내용

## 주요 화제

## 부차 화제

# 내용
---
{content_header}

{content_text}

# 구성
---
{descendants_text}
"""
        
        # 파일 저장
        with open(node_doc_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"   ✅ 통합 완료: {node_doc_filename}")
        return True
        
    except Exception as e:
        print(f"   ❌ 통합 실패 (ID: {node.get('id', '?')}): {e}")
        return False

def integrate_all_documents(nodes: List[Dict[str, Any]], content_dir: str, node_docs_dir: str, metadata: Dict[str, Any]) -> None:
    """
    모든 노드 문서를 통합합니다.
    
    Args:
        nodes: 노드 리스트
        content_dir: 내용 문서 디렉토리
        node_docs_dir: 노드 문서 디렉토리
        metadata: 메타데이터 딕셔너리
    """
    print("📄 노드 문서 통합 시작...")
    
    success_count = 0
    for node in nodes:
        if integrate_single_document(node, nodes, content_dir, node_docs_dir, metadata):
            success_count += 1
    
    print(f"   ✅ {success_count}/{len(nodes)}개 문서 통합 완료")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='노드 정보 문서와 내용 문서를 통합합니다.')
    parser.add_argument('json_file', help='노드 JSON 파일 경로')
    parser.add_argument('content_dir', help='내용 문서 디렉토리 경로')
    parser.add_argument('node_docs_dir', help='노드 정보 문서 디렉토리 경로')
    parser.add_argument('--metadata', '-m', help='메타데이터 JSON 파일 경로')
    
    args = parser.parse_args()
    
    print("🚀 문서 통합 스크립트 시작")
    
    # 경로 검증
    if not os.path.exists(args.json_file):
        print(f"❌ JSON 파일을 찾을 수 없습니다: {args.json_file}")
        return
    
    if not os.path.exists(args.content_dir):
        print(f"❌ 내용 문서 디렉토리를 찾을 수 없습니다: {args.content_dir}")
        return
    
    if not os.path.exists(args.node_docs_dir):
        print(f"❌ 노드 문서 디렉토리를 찾을 수 없습니다: {args.node_docs_dir}")
        return
    
    # 1. 노드 데이터 로드
    nodes = load_nodes_data(args.json_file)
    if not nodes:
        return
    
    # 2. 메타데이터 로드
    metadata = {}
    if args.metadata and os.path.exists(args.metadata):
        metadata = load_metadata(args.metadata)
    else:
        print("⚠️ 메타데이터 파일이 지정되지 않았거나 존재하지 않습니다.")
    
    # 3. 모든 문서 통합
    integrate_all_documents(nodes, args.content_dir, args.node_docs_dir, metadata)
    
    print("✅ 모든 문서 통합 완료!")

if __name__ == "__main__":
    main()