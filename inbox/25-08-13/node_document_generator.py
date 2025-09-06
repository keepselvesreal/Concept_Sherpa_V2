#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 16:30:54 KST
핵심 내용: 노드 구조를 기반으로 개별 문서 파일을 생성하는 재사용 가능한 스크립트
상세 내용:
- load_nodes (라인 25-40): JSON 파일에서 노드 데이터 로드
- create_filename (라인 45-55): 레벨과 제목 기반으로 파일명 생성
- generate_document_content (라인 60-85): 간단한 마크다운 문서 내용 생성
- find_node_by_id (라인 90-100): ID로 특정 노드 검색
- create_node_documents (라인 105-135): 모든 노드에 대한 문서 생성
- main (라인 140-155): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: node_document_generator
참조: # 속성, # 추출, # 내용, # 구성 섹션 형식 (속성에 process_status 추가)
"""

import json
import os
import sys
import re
from typing import List, Dict, Any, Optional

def load_nodes(file_path: str) -> List[Dict[str, Any]]:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # headers 키가 있는 경우 추출
        if isinstance(nodes, dict) and 'headers' in nodes:
            nodes = nodes['headers']
            
        return nodes
    except Exception as e:
        print(f"파일 로드 오류: {e}")
        return []

def create_filename(node: Dict[str, Any]) -> str:
    """레벨과 제목을 기반으로 파일명을 생성합니다."""
    level = node.get('level', 0)
    title = node.get('title', 'Untitled')
    
    # 제목을 파일명으로 사용할 수 있게 정리
    clean_title = re.sub(r'[^\w\s-]', '', title).strip()
    clean_title = re.sub(r'[-\s]+', '_', clean_title)
    
    return f"{level}_{clean_title}_info.md"

def generate_document_content(node: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> str:
    """노드 정보를 기반으로 간단한 마크다운 문서 내용을 생성합니다."""
    
    # 자식 노드들의 파일명 생성
    children_filenames = ""
    if node.get('children_ids'):
        for child_id in node['children_ids']:
            child_node = find_node_by_id(all_nodes, child_id)
            if child_node:
                child_filename = create_filename(child_node)
                children_filenames += f"{child_filename}\n"
    
    content = f"""# 속성
process_status:

# 추출


# 내용


# 구성
{children_filenames}"""

    return content

def find_node_by_id(nodes: List[Dict[str, Any]], node_id: int) -> Optional[Dict[str, Any]]:
    """ID로 특정 노드를 찾습니다."""
    for node in nodes:
        if node.get('id') == node_id:
            return node
    return None

def create_node_documents(nodes: List[Dict[str, Any]], output_dir: str) -> None:
    """모든 노드에 대한 문서를 생성합니다."""
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"총 {len(nodes)}개 노드에 대한 문서 생성 시작...")
    print(f"출력 디렉토리: {output_dir}")
    
    created_count = 0
    
    for node in nodes:
        try:
            # 파일명 생성
            filename = create_filename(node)
            filepath = os.path.join(output_dir, filename)
            
            # 문서 내용 생성
            content = generate_document_content(node, nodes)
            
            # 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"생성: {filename}")
            created_count += 1
            
        except Exception as e:
            print(f"노드 ID {node.get('id', 'N/A')} 문서 생성 오류: {e}")
    
    print(f"\n총 {created_count}개 문서가 생성되었습니다.")

def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("사용법: python node_document_generator.py <nodes_file> [output_directory]")
        print("예시: python node_document_generator.py script_node_structure.json ./generated_docs")
        return
    
    nodes_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./generated_docs"
    
    print(f"노드 파일: {nodes_file}")
    print(f"출력 디렉토리: {output_dir}")
    
    # 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("노드를 로드할 수 없습니다.")
        return
    
    # 문서 생성
    create_node_documents(nodes, output_dir)

if __name__ == "__main__":
    main()