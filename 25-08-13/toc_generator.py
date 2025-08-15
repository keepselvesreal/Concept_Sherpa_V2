#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 17:04:53 KST
핵심 내용: JSON 노드 구조를 기반으로 마크다운 목차 파일을 생성하는 스크립트
상세 내용:
- load_nodes (라인 25-40): JSON 파일에서 노드 데이터 로드
- generate_toc_content (라인 45-85): 계층 구조 기반 목차 내용 생성
- should_add_spacing (라인 90-100): 하위 노드 뒤 상위 노드 올 때 줄바꿈 판단
- create_toc_file (라인 105-120): 마크다운 목차 파일 생성
- main (라인 125-140): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: toc_generator
참조: level에 따른 헤더 수준 매핑 및 영역 구분 로직
"""

import json
import sys
from typing import List, Dict, Any

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

def generate_toc_content(nodes: List[Dict[str, Any]]) -> str:
    """노드 구조를 기반으로 목차 내용을 생성합니다."""
    
    # 노드를 ID 순서대로 정렬
    sorted_nodes = sorted(nodes, key=lambda x: x.get('id', 0))
    
    toc_lines = []
    previous_level = None
    
    for i, node in enumerate(sorted_nodes):
        current_level = node.get('level', 0)
        title = node.get('title', 'Untitled')
        
        # 하위 노드 뒤에 상위 노드가 올 때 줄바꿈 추가
        if should_add_spacing(previous_level, current_level, i):
            toc_lines.append("")
        
        # 헤더 수준 생성 (level 0 -> #, level 1 -> ##, level 2 -> ###)
        header_level = '#' * (current_level + 1)
        toc_line = f"{header_level} {title}"
        
        toc_lines.append(toc_line)
        previous_level = current_level
    
    return '\n'.join(toc_lines)

def should_add_spacing(previous_level: int, current_level: int, index: int) -> bool:
    """적절한 위치에서 줄바꿈을 추가할지 판단합니다."""
    # 첫 번째 노드는 줄바꿈 없음
    if index == 0:
        return False
    
    # 이전 레벨이 None인 경우 줄바꿈 없음
    if previous_level is None:
        return False
    
    # 하위 노드(높은 숫자) 뒤에 상위 노드(낮은 숫자)가 올 때 줄바꿈
    if previous_level > current_level:
        return True
    
    # # 항목(level 0) 뒤에 ## 항목(level 1)이 올 때 줄바꿈
    if previous_level == 0 and current_level == 1:
        return True
    
    return False

def create_toc_file(nodes: List[Dict[str, Any]], output_file: str) -> None:
    """마크다운 목차 파일을 생성합니다."""
    
    print(f"총 {len(nodes)}개 노드로 목차 생성 중...")
    
    # 목차 내용 생성
    toc_content = generate_toc_content(nodes)
    
    # 파일 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(toc_content)
        
        print(f"목차가 {output_file}에 저장되었습니다.")
        
        # 생성된 라인 수와 구조 정보 출력
        lines = toc_content.split('\n')
        header_counts = {}
        for line in lines:
            if line.strip().startswith('#'):
                level = len(line.split()[0])  # # 개수 세기
                header_counts[level] = header_counts.get(level, 0) + 1
        
        print(f"총 {len([l for l in lines if l.strip()])}줄 생성")
        for level in sorted(header_counts.keys()):
            print(f"레벨 {level-1} ({'#' * level}): {header_counts[level]}개")
            
    except Exception as e:
        print(f"파일 저장 오류: {e}")

def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("사용법: python toc_generator.py <nodes_file> [output_file]")
        print("예시: python toc_generator.py script_node_structure.json table_of_contents.md")
        return
    
    nodes_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "table_of_contents.md"
    
    print(f"노드 파일: {nodes_file}")
    print(f"출력 파일: {output_file}")
    
    # 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("노드를 로드할 수 없습니다.")
        return
    
    # 목차 파일 생성
    create_toc_file(nodes, output_file)

if __name__ == "__main__":
    main()