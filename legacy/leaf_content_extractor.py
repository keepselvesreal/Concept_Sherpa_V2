#!/usr/bin/env python3
"""
Leaf Node Content Extractor
PDF에서 TOC leaf node들의 실제 내용을 추출하여 TOC_Structure에 저장하는 스크립트
"""

import re
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeafContentExtractor:
    def __init__(self, toc_file_path: str, pdf_file_path: str, toc_structure_path: str):
        self.toc_file_path = Path(toc_file_path)
        self.pdf_file_path = Path(pdf_file_path)
        self.toc_structure_path = Path(toc_structure_path)
        self.nodes = {}
        self.leaf_nodes = []
        
    def parse_toc_structure(self) -> Dict:
        """TOC 파일을 파싱해서 구조를 분석하고 leaf node들을 찾는다"""
        logger.info("TOC 구조 파싱 시작...")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 각 라인을 분석해서 노드 정보 추출
        nodes = {}
        parent_child_map = {}
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 들여쓰기 레벨 계산
            indent_level = len(line) - len(line.lstrip(' -'))
            
            # 노드 정보 추출 (노드 타입과 제목)
            node_match = re.search(r'\(node(\d+)\)', line)
            if node_match:
                node_type = int(node_match.group(1))
                title = re.sub(r'\(node\d+\)', '', line).strip(' -').strip()
                
                node_info = {
                    'line_num': line_num,
                    'title': title,
                    'node_type': node_type,
                    'indent_level': indent_level,
                    'children': [],
                    'parent': None,
                    'original_line': line
                }
                
                node_id = f"line_{line_num}"
                nodes[node_id] = node_info
        
        # 부모-자식 관계 설정
        node_stack = []  # (node_id, indent_level) 스택
        
        for node_id in nodes.keys():
            node = nodes[node_id]
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
        leaf_nodes = []
        for node_id, node in nodes.items():
            if not node['children']:  # 자식이 없으면 leaf node
                leaf_nodes.append({
                    'node_id': node_id,
                    'title': node['title'],
                    'node_type': node['node_type'],
                    'line_num': node['line_num']
                })
        
        self.nodes = nodes
        self.leaf_nodes = leaf_nodes
        
        logger.info(f"전체 노드 수: {len(nodes)}")
        logger.info(f"Leaf 노드 수: {len(leaf_nodes)}")
        
        return nodes
    
    def extract_content_from_pdf(self, section_title: str, start_page: Optional[int] = None) -> str:
        """PDF에서 특정 섹션의 내용을 추출한다"""
        try:
            with pdfplumber.open(self.pdf_file_path) as pdf:
                content = ""
                found_section = False
                
                for page_num, page in enumerate(pdf.pages, 1):
                    if start_page and page_num < start_page:
                        continue
                        
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # 섹션 제목을 찾았을 때
                    if section_title.lower() in text.lower() and not found_section:
                        found_section = True
                        logger.info(f"'{section_title}' 섹션을 {page_num}페이지에서 발견")
                    
                    if found_section:
                        content += text + "\n"
                        
                        # 다음 주요 섹션이 시작되면 중단 (간단한 휴리스틱)
                        # 이 부분은 더 정교하게 개선할 수 있습니다
                        if len(content) > 5000:  # 임시로 길이 제한
                            break
                
                return content.strip()
                
        except Exception as e:
            logger.error(f"PDF 내용 추출 중 오류 발생: {e}")
            return ""
    
    def extract_all_leaf_content(self) -> Dict:
        """모든 leaf node의 내용을 추출한다"""
        logger.info("Leaf node 내용 추출 시작...")
        
        if not self.leaf_nodes:
            self.parse_toc_structure()
        
        results = {}
        
        for i, leaf in enumerate(self.leaf_nodes, 1):
            logger.info(f"[{i}/{len(self.leaf_nodes)}] '{leaf['title']}' 처리 중...")
            
            # PDF에서 해당 섹션 내용 추출
            content = self.extract_content_from_pdf(leaf['title'])
            
            results[leaf['node_id']] = {
                'title': leaf['title'],
                'node_type': leaf['node_type'],
                'line_num': leaf['line_num'],
                'content': content,
                'content_length': len(content)
            }
        
        return results
    
    def save_results_to_file(self, results: Dict, output_path: str):
        """결과를 파일로 저장한다"""
        logger.info(f"결과를 {output_path}에 저장 중...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Data-Oriented Programming - Leaf Node Contents\n\n")
            
            for node_id, data in results.items():
                f.write(f"## {data['title']} (node{data['node_type']}) - Line {data['line_num']}\n\n")
                
                if data['content']:
                    f.write("### 추출된 내용:\n")
                    f.write(f"```\n{data['content']}\n```\n\n")
                else:
                    f.write("### 내용 추출 실패\n\n")
                    
                f.write(f"**내용 길이**: {data['content_length']} 문자\n\n")
                f.write("---\n\n")
    
    def print_leaf_nodes_summary(self):
        """Leaf node 요약 정보를 출력한다"""
        if not self.leaf_nodes:
            self.parse_toc_structure()
            
        print(f"\n=== Leaf Node 요약 ({len(self.leaf_nodes)}개) ===")
        
        # node_type별로 그룹화
        by_type = {}
        for leaf in self.leaf_nodes:
            node_type = leaf['node_type']
            if node_type not in by_type:
                by_type[node_type] = []
            by_type[node_type].append(leaf)
        
        for node_type in sorted(by_type.keys()):
            print(f"\nnode{node_type} ({len(by_type[node_type])}개):")
            for leaf in by_type[node_type][:5]:  # 처음 5개만 표시
                print(f"  - {leaf['title']}")
            if len(by_type[node_type]) > 5:
                print(f"  ... 및 {len(by_type[node_type]) - 5}개 더")


def main():
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v3.md"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/leaf_nodes_with_content.md"
    
    # 추출기 초기화
    extractor = LeafContentExtractor(toc_file, pdf_file)
    
    # TOC 구조 파싱 및 leaf node 요약 출력
    extractor.parse_toc_structure()
    extractor.print_leaf_nodes_summary()
    
    # 사용자 확인
    print("\n위의 leaf node들에 대해 PDF 내용을 추출하시겠습니까? (y/n): ", end="")
    if input().lower().strip() == 'y':
        # 모든 leaf node 내용 추출
        results = extractor.extract_all_leaf_content()
        
        # 결과 저장
        extractor.save_results_to_file(results, output_file)
        
        print(f"\n작업 완료! 결과가 {output_file}에 저장되었습니다.")
    else:
        print("작업이 취소되었습니다.")


if __name__ == "__main__":
    main()