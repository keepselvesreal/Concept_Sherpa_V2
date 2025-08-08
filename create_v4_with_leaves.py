#!/usr/bin/env python3
"""
v4 TOC 문서 생성기: leaf node들을 식별하고 표시
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

class TOCLeafIdentifier:
    def __init__(self, toc_file_path: str):
        self.toc_file_path = Path(toc_file_path)
        self.nodes = {}
        self.leaf_nodes = set()
        
    def parse_toc_structure(self) -> Dict:
        """TOC 파일을 파싱해서 구조를 분석하고 leaf node들을 찾는다"""
        print("TOC 구조 파싱 시작...")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 각 라인을 분석해서 노드 정보 추출
        nodes = {}
        ordered_nodes = []  # 순서를 유지하기 위한 리스트
        
        for line_num, line in enumerate(lines, 1):
            original_line = line.rstrip()
            
            if not line.strip() or line.strip().startswith('#'):
                continue
                
            # 노드 정보 추출 (노드 타입과 제목)
            node_match = re.search(r'\(node(\d+)\)', line)
            if not node_match:
                continue
                
            node_type = int(node_match.group(1))
            
            # 들여쓰기 레벨 계산
            stripped_line = line.lstrip()
            indent_level = len(line) - len(stripped_line)
            
            # '- ' 제거 후 제목 추출
            title_part = stripped_line.lstrip('- ')
            title = re.sub(r'\s*\(node\d+\)\s*$', '', title_part).strip()
            
            node_info = {
                'line_num': line_num,
                'title': title,
                'node_type': node_type,
                'indent_level': indent_level,
                'children': [],
                'parent': None,
                'original_line': original_line,
                'is_leaf': False  # 초기값
            }
            
            node_id = f"line_{line_num}"
            nodes[node_id] = node_info
            ordered_nodes.append((node_id, node_info))
        
        # 부모-자식 관계 설정 (순서대로 처리)
        node_stack = []  # (node_id, indent_level) 스택
        
        for node_id, node in ordered_nodes:
            current_indent = node['indent_level']
            
            # 현재 노드보다 들여쓰기가 같거나 큰 노드들을 스택에서 제거
            while node_stack and node_stack[-1][1] >= current_indent:
                node_stack.pop()
            
            # 부모 설정
            if node_stack:
                parent_id = node_stack[-1][0]
                node['parent'] = parent_id
                nodes[parent_id]['children'].append(node_id)
            
            node_stack.append((node_id, current_indent))
        
        # leaf node 식별 (자식이 없는 노드들)
        leaf_nodes = set()
        for node_id, node in nodes.items():
            if not node['children']:  # 자식이 없으면 leaf node
                node['is_leaf'] = True
                leaf_nodes.add(node_id)
        
        self.nodes = nodes
        self.leaf_nodes = leaf_nodes
        
        print(f"전체 노드 수: {len(nodes)}")
        print(f"Leaf 노드 수: {len(leaf_nodes)}")
        
        return nodes
    
    def create_v4_document(self, output_path: str):
        """v4 문서를 생성한다 (leaf node 표시)"""
        print(f"v4 문서 생성 중: {output_path}")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        output_lines = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line.rstrip()
            
            # 빈 줄이나 헤더는 그대로 유지
            if not line.strip() or line.strip().startswith('#'):
                output_lines.append(original_line + '\n')
                continue
            
            # 노드가 있는 줄인지 확인
            node_match = re.search(r'\(node(\d+)\)', line)
            if not node_match:
                output_lines.append(original_line + '\n')
                continue
            
            # 해당 노드가 leaf인지 확인
            node_id = f"line_{line_num}"
            if node_id in self.nodes and self.nodes[node_id]['is_leaf']:
                # leaf node 표시 추가
                modified_line = original_line.replace(f"(node{node_match.group(1)})", f"(node{node_match.group(1)}) **[LEAF]**")
                output_lines.append(modified_line + '\n')
            else:
                output_lines.append(original_line + '\n')
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        
        print(f"v4 문서가 성공적으로 생성되었습니다: {output_path}")
    
    def print_leaf_summary(self):
        """Leaf node 요약 정보를 출력한다"""
        print(f"\n=== Leaf Node 요약 ({len(self.leaf_nodes)}개) ===")
        
        # node_type별로 그룹화
        by_type = {}
        for node_id in self.leaf_nodes:
            node = self.nodes[node_id]
            node_type = node['node_type']
            if node_type not in by_type:
                by_type[node_type] = []
            by_type[node_type].append(node)
        
        for node_type in sorted(by_type.keys()):
            print(f"\nnode{node_type} ({len(by_type[node_type])}개):")
            for i, node in enumerate(by_type[node_type][:10]):  # 처음 10개만 표시
                print(f"  - {node['title']}")
            if len(by_type[node_type]) > 10:
                print(f"  ... 및 {len(by_type[node_type]) - 10}개 더")

def main():
    # 파일 경로 설정
    input_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v3.md"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    
    # leaf 식별기 초기화
    identifier = TOCLeafIdentifier(input_file)
    
    # TOC 구조 파싱
    identifier.parse_toc_structure()
    
    # leaf node 요약 출력
    identifier.print_leaf_summary()
    
    # v4 문서 생성
    identifier.create_v4_document(output_file)

if __name__ == "__main__":
    main()