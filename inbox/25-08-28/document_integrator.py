# 생성 시간: Thu Aug 28 17:24:58 KST 2025
# 핵심 내용: 노드 정보 문서에 메타정보와 내용 문서를 통합하는 스크립트
# 상세 내용:
#   - load_nodes_data() (line 30): 노드 JSON 파일 로드
#   - get_node_meta_info() (line 47): 노드 메타정보 생성
#   - load_content_document() (line 68): 내용 문서 로드
#   - get_children_info() (line 85): 자식 노드 정보 문서 파일명 수집
#   - integrate_single_document() (line 101): 단일 노드 문서 통합
#   - integrate_all_documents() (line 161): 모든 노드 문서 통합
#   - main() (line 182): 메인 실행 함수
# 상태: active
# 주소: document_integrator
# 참조: node_processor.py와 연계

#!/usr/bin/env uv run python

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
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

def get_children_info(node: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> List[str]:
    """
    자식 노드들의 정보 문서 파일명을 수집합니다.
    
    Args:
        node: 대상 노드
        all_nodes: 전체 노드 리스트
        
    Returns:
        자식 노드 문서 파일명 리스트
    """
    children_files = []
    
    for child_id in node.get('children_ids', []):
        child_node = next((n for n in all_nodes if n.get('id') == child_id), None)
        if child_node:
            # 자식 노드의 문서 파일명 생성
            title_clean = re.sub(r'[^\w\s.-]', '', child_node['title'])
            title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
            filename = f"{child_node['id']:02d}_lev{child_node['level']}_{title_clean}_info.md"
            children_files.append(filename)
    
    return children_files

def integrate_single_document(node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                            process_dir: str, node_docs_dir: str, metadata: Dict[str, Any]) -> bool:
    """
    단일 노드 문서를 통합합니다.
    
    Args:
        node: 대상 노드
        all_nodes: 전체 노드 리스트
        process_dir: 내용 문서 디렉토리
        node_docs_dir: 노드 문서 디렉토리
        
    Returns:
        통합 성공 여부
    """
    try:
        # 파일 경로 생성
        title_clean = re.sub(r'[^\w\s.-]', '', node['title'])
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        node_doc_filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
        node_doc_path = os.path.join(node_docs_dir, node_doc_filename)
        
        # 내용 문서 파일 매핑
        content_file_map = {
            0: "chapter7_00_7_Basic_data_validation.md",
            1: "chapter7_01_7.1_Data validation_in_DOP.md", 
            2: "chapter7_02_7.2_JSON_Schema_in_a_nutshell.md",
            3: "chapter7_03_7.3_Schema_flexibility_and_strictness.md",
            4: "chapter7_04_7.4_Schema_composition.md",
            5: "chapter7_05_7.5_Details_about_data_validation_failures.md",
            6: "chapter7_06_Summary.md"
        }
        
        content_filename = content_file_map.get(node['id'], "")
        content_path = os.path.join(process_dir, content_filename) if content_filename else ""
        
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
        if content_path and os.path.exists(content_path):
            content_text = load_content_document(content_path)
        
        # 자식 노드 정보 수집
        children_files = get_children_info(node, all_nodes)
        children_text = "\n".join(children_files) if children_files else "없음 (리프 노드)"
        
        # 레벨에 따른 헤더 생성 (level 1 -> #, level 2 -> ##)
        header_prefix = "#" * node['level']  
        content_header = f"{header_prefix} {node['title']}"
        
        # 새로운 문서 내용 생성
        new_content = f"""# 속성
---
process_status: false
{meta_info}

# 추출
---

# 내용
---
{content_header}

{content_text}

# 구성
---
{children_text}
"""
        
        # 파일 저장
        with open(node_doc_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"   ✅ 통합 완료: {node_doc_filename}")
        return True
        
    except Exception as e:
        print(f"   ❌ 통합 실패 (ID: {node.get('id', '?')}): {e}")
        return False

def integrate_all_documents(nodes: List[Dict[str, Any]], process_dir: str, node_docs_dir: str, metadata: Dict[str, Any]) -> None:
    """
    모든 노드 문서를 통합합니다.
    
    Args:
        nodes: 노드 리스트
        process_dir: 내용 문서 디렉토리
        node_docs_dir: 노드 문서 디렉토리
    """
    print("📄 노드 문서 통합 시작...")
    
    success_count = 0
    for node in nodes:
        if integrate_single_document(node, nodes, process_dir, node_docs_dir, metadata):
            success_count += 1
    
    print(f"   ✅ {success_count}/{len(nodes)}개 문서 통합 완료")

def main():
    """메인 실행 함수"""
    print("🚀 문서 통합 스크립트 시작")
    
    # 경로 설정
    process_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process"
    nodes_file = os.path.join(process_dir, "nodes_updated.json")
    metadata_file = os.path.join(process_dir, "metadata.json")
    node_docs_dir = os.path.join(process_dir, "node_docs")
    
    # 1. 노드 데이터 로드
    nodes = load_nodes_data(nodes_file)
    if not nodes:
        return
    
    # 2. 메타데이터 로드
    metadata = load_metadata(metadata_file)
    
    # 3. 모든 문서 통합
    integrate_all_documents(nodes, process_dir, node_docs_dir, metadata)
    
    print("✅ 모든 문서 통합 완료!")

if __name__ == "__main__":
    main()