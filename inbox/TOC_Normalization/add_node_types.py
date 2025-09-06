#!/usr/bin/env python3
"""
TOC에 노드 타입 표시 추가
- root node: 최상위 노드 (자식은 있지만 부모가 없음)
- internal node: 중간 노드 (부모와 자식 모두 있음)  
- leaf node: 말단 노드 (부모는 있지만 자식이 없음)
"""

import re
from pathlib import Path
from typing import List, Dict, Optional

class TOCNode:
    """TOC 노드 클래스"""
    
    def __init__(self, level: int, number: str, title: str, raw_line: str, line_index: int):
        self.level = level
        self.number = number
        self.title = title
        self.raw_line = raw_line
        self.line_index = line_index
        self.number_parts = self._parse_number_parts(number) if number else []
        self.children: List['TOCNode'] = []
        self.parent: Optional['TOCNode'] = None
        
    def _parse_number_parts(self, number: str) -> List:
        """번호를 파싱하여 비교 가능한 형태로 변환"""
        parts = []
        for part in number.split('.'):
            if part.isdigit():
                parts.append(('num', int(part)))
            elif len(part) > 0:
                parts.append(('str', part))
        return parts
    
    def get_node_type(self) -> str:
        """노드 타입 반환"""
        has_parent = self.parent is not None
        has_children = len(self.children) > 0
        
        if not has_parent and has_children:
            return "root node"
        elif has_parent and has_children:
            return "internal node"
        elif has_parent and not has_children:
            return "leaf node"
        else:  # 고립된 노드 (이론적으로 발생하지 않아야 함)
            return "isolated node"
    
    def __repr__(self):
        return f"TOCNode(level={self.level}, number='{self.number}', title='{self.title[:30]}...', type={self.get_node_type()})"

class NodeTypeAdder:
    """노드 타입 추가 클래스"""
    
    def __init__(self):
        self.nodes: List[TOCNode] = []
        
    def parse_toc_file(self, file_path: str) -> None:
        """TOC 파일 파싱"""
        print(f"TOC 파일 파싱 중: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self.nodes = []
        
        for line_idx, line in enumerate(lines):
            original_line = line.rstrip()
            if not original_line.strip():
                continue
            
            # 들여쓰기 레벨 계산
            indent_match = re.match(r'^(\s*)', original_line)
            if indent_match:
                indent = len(indent_match.group(1).replace('\t', '    '))
                if '- ' in original_line:
                    level = (indent + original_line.find('- ') + 2) // 2
                else:
                    level = indent // 2
            else:
                level = 0
            
            # 다양한 패턴 매칭
            patterns = [
                # Part 패턴
                r'^#+\s*Part\s+(\d+)\s*[—\-]\s*(.+)$',
                # Chapter 패턴  
                r'^#+\s*(\d+)\s+(.+)$',
                # Introduction 패턴
                r'^#+\s*(Part\s+\d+\s+Introduction)\s*\((.+)\)$',
                # 일반 섹션 패턴
                r'^#+\s*([A-Z]?\d+(?:\.\d+)*)\s+(.+)$',
                r'^\s*-\s*([A-Z]?\d+(?:\.\d+)*)\s+(.+)$',
                r'^\s*([A-Z]?\d+(?:\.\d+)*)\s+(.+)$',
                # 번호 없는 항목
                r'^#+\s*(.+)$',
                r'^\s*-\s*(.+)$',
            ]
            
            matched = False
            for pattern in patterns:
                match = re.search(pattern, original_line, re.IGNORECASE)
                if match:
                    if len(match.groups()) >= 2:
                        number = match.group(1).strip()
                        title = match.group(2).strip()
                    else:
                        # 번호 없는 경우
                        number = ""
                        title = match.group(1).strip()
                    
                    # Part Introduction은 특별 처리
                    if "Introduction" in number:
                        # "Part 1 Introduction"을 "Part1_Intro"로 변환
                        number = number.replace(" ", "").replace("Introduction", "_Intro")
                    
                    node = TOCNode(level, number, title, original_line, line_idx)
                    self.nodes.append(node)
                    matched = True
                    break
            
            if not matched and (re.search(r'[A-Z]?\d+', original_line) or 'Part' in original_line or 'Introduction' in original_line):
                print(f"Warning: 파싱 실패 라인 {line_idx + 1}: {original_line}")
        
        print(f"파싱된 노드 수: {len(self.nodes)}")
    
    def build_hierarchy(self) -> None:
        """계층 구조 구축"""
        print("계층 구조 구축 중...")
        
        # 부모-자식 관계 설정
        for i, node in enumerate(self.nodes):
            # 부모 찾기 (바로 위 레벨에서 가장 가까운 노드)
            for j in range(i - 1, -1, -1):
                potential_parent = self.nodes[j]
                if potential_parent.level < node.level:
                    node.parent = potential_parent
                    potential_parent.children.append(node)
                    break
        
        # 통계 출력
        root_count = sum(1 for node in self.nodes if node.get_node_type() == "root node")
        internal_count = sum(1 for node in self.nodes if node.get_node_type() == "internal node")
        leaf_count = sum(1 for node in self.nodes if node.get_node_type() == "leaf node")
        
        print(f"노드 타입별 통계:")
        print(f"  Root nodes: {root_count}개")
        print(f"  Internal nodes: {internal_count}개")
        print(f"  Leaf nodes: {leaf_count}개")
    
    def add_node_types_to_toc(self, input_file: str, output_file: str) -> None:
        """TOC에 노드 타입 표시 추가"""
        print(f"노드 타입 표시 추가 중...")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 노드별 인덱스 매핑
        node_by_line = {}
        for node in self.nodes:
            node_by_line[node.line_index] = node
        
        result_lines = []
        
        for line_idx, line in enumerate(lines):
            original_line = line.rstrip()
            
            if line_idx in node_by_line:
                node = node_by_line[line_idx]
                node_type = node.get_node_type()
                
                # 노드 타입을 제목 뒤에 추가
                if node_type != "leaf node":  # leaf node가 아닌 경우만 표시
                    modified_line = f"{original_line} ({node_type})"
                else:
                    modified_line = original_line
                
                result_lines.append(modified_line + '\n')
            else:
                result_lines.append(line)
        
        # 결과 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(result_lines)
        
        print(f"결과 저장 완료: {output_file}")

def main():
    input_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_final_corrected.md"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types.md"
    
    adder = NodeTypeAdder()
    
    # 1단계: TOC 파싱
    adder.parse_toc_file(input_file)
    
    # 2단계: 계층 구조 구축
    adder.build_hierarchy()
    
    # 3단계: 노드 타입 표시 추가
    adder.add_node_types_to_toc(input_file, output_file)
    
    print("노드 타입 표시 작업 완료!")

if __name__ == "__main__":
    main()