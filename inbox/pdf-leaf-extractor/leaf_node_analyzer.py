#!/usr/bin/env python3
"""
PDF Leaf Node Analyzer - Data-Oriented Programming 책의 리프 노드 추출 및 분석
"""

import pdfplumber
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class LeafNodeAnalyzer:
    def __init__(self, pdf_path: str, toc_path: str):
        self.pdf_path = Path(pdf_path)
        self.toc_path = Path(toc_path)
        self.pdf_doc = None
        self.total_pages = 0
        self.leaf_nodes = []
        self.chapters = {}
        self.page_content = {}
        
    def load_pdf(self):
        """PDF 파일을 로드합니다."""
        try:
            self.pdf_doc = pdfplumber.open(str(self.pdf_path))
            self.total_pages = len(self.pdf_doc.pages)
            print(f"PDF 로드 완료: {self.total_pages}페이지")
            return True
        except Exception as e:
            print(f"PDF 로드 실패: {e}")
            return False
    
    def extract_text_from_page(self, page_num: int) -> str:
        """특정 페이지에서 텍스트를 추출합니다."""
        if not self.pdf_doc or page_num >= self.total_pages:
            return ""
        
        try:
            page = self.pdf_doc.pages[page_num]
            text = page.extract_text()
            return text if text else ""
        except Exception as e:
            print(f"페이지 {page_num + 1} 텍스트 추출 실패: {e}")
            return ""
    
    def parse_toc_file(self):
        """TOC 파일에서 리프 노드를 파싱합니다."""
        try:
            with open(self.toc_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 리프 노드 패턴 매칭
            leaf_pattern = r'^(.*?)\*\*\[LEAF\]\*\*'
            lines = content.split('\n')
            
            current_chapter = None
            current_part = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Part 정보 추출
                if line.startswith('## Part') and '(node1)' in line:
                    current_part = line.split('(node1)')[0].strip().replace('##', '').strip()
                    continue
                
                # Chapter 정보 추출
                if line.startswith('### ') and '(node2)' in line:
                    current_chapter = line.split('(node2)')[0].strip().replace('###', '').strip()
                    continue
                
                # 리프 노드 검색
                if '**[LEAF]**' in line:
                    # 노드 정보 추출
                    node_match = re.match(r'^(.*?)\(node(\d+)\)\s*\*\*\[LEAF\]\*\*', line)
                    if node_match:
                        node_text = node_match.group(1).strip()
                        node_level = int(node_match.group(2))
                        
                        # 들여쓰기 레벨 계산
                        indent_level = len(line) - len(line.lstrip())
                        
                        leaf_node = {
                            'text': node_text,
                            'node_level': node_level,
                            'indent_level': indent_level,
                            'part': current_part,
                            'chapter': current_chapter,
                            'raw_line': line,
                            'is_part_intro': 'Part' in node_text and 'Introduction' in node_text
                        }
                        
                        self.leaf_nodes.append(leaf_node)
                        
            print(f"총 {len(self.leaf_nodes)}개의 리프 노드를 찾았습니다.")
            return True
            
        except Exception as e:
            print(f"TOC 파일 파싱 실패: {e}")
            return False
    
    def find_chapter_pages(self):
        """각 챕터의 시작 페이지를 찾습니다."""
        if not self.pdf_doc:
            return False
        
        chapter_patterns = [
            r'^\s*(?:Chapter\s+)?(\d+)\s+(.+?)(?:\s+\d+)?$',
            r'^(\d+)\s+(.+?)(?:\s+\d+)?$',
            r'Part\s*(\d+)',
            r'Appendix\s+([A-Z])',
        ]
        
        for page_num in range(min(50, self.total_pages)):  # 처음 50페이지만 검사
            text = self.extract_text_from_page(page_num)
            lines = text.split('\n')
            
            for line in lines[:10]:  # 페이지 상단 10줄만 확인
                line = line.strip()
                if not line:
                    continue
                
                for pattern in chapter_patterns:
                    match = re.search(pattern, line)
                    if match:
                        chapter_info = {
                            'page': page_num + 1,
                            'text': line,
                            'match': match.groups()
                        }
                        
                        # 챕터 번호별로 저장
                        if match.group(1).isdigit():
                            chapter_num = int(match.group(1))
                            self.chapters[chapter_num] = chapter_info
                        else:
                            self.chapters[match.group(1)] = chapter_info
        
        print(f"발견된 챕터: {list(self.chapters.keys())}")
        return True
    
    def extract_chapter_content(self, chapter_num: int, start_page: int, end_page: Optional[int] = None) -> str:
        """특정 챕터의 내용을 추출합니다."""
        if not self.pdf_doc:
            return ""
        
        content = []
        max_page = end_page if end_page else min(start_page + 30, self.total_pages)
        
        for page_num in range(start_page - 1, max_page):
            if page_num >= self.total_pages:
                break
                
            page_text = self.extract_text_from_page(page_num)
            content.append(f"\n--- Page {page_num + 1} ---\n")
            content.append(page_text)
        
        return '\n'.join(content)
    
    def analyze_leaf_nodes(self):
        """리프 노드들을 분석하고 페이지 범위를 추정합니다."""
        results = []
        
        for i, leaf in enumerate(self.leaf_nodes):
            analysis = {
                'id': i + 1,
                'text': leaf['text'],
                'node_level': leaf['node_level'],
                'part': leaf['part'],
                'chapter': leaf['chapter'],
                'is_part_intro': leaf['is_part_intro'],
                'estimated_page_range': None,
                'content_preview': None
            }
            
            # Part Introduction과 같은 특별한 노드 처리
            if leaf['is_part_intro']:
                analysis['special_note'] = "Part와 Chapter 사이의 서론 내용"
                
                # Part 번호 추출
                part_match = re.search(r'Part\s*(\d+)', leaf['part'] or '')
                if part_match:
                    part_num = int(part_match.group(1))
                    
                    # 해당 Part의 첫 번째 챕터 찾기
                    if part_num == 1:
                        chapter_start = 1
                    elif part_num == 2:
                        chapter_start = 7
                    elif part_num == 3:
                        chapter_start = 12
                    else:
                        chapter_start = None
                    
                    if chapter_start and chapter_start in self.chapters:
                        chapter_page = self.chapters[chapter_start]['page']
                        # Part Introduction은 해당 챕터 시작 전 몇 페이지로 추정
                        analysis['estimated_page_range'] = f"{max(1, chapter_page - 3)}-{chapter_page - 1}"
            
            results.append(analysis)
        
        return results
    
    def save_analysis_results(self, results: List[Dict]):
        """분석 결과를 저장합니다."""
        output_file = Path(self.pdf_path.parent) / 'pdf-leaf-extractor' / 'leaf_node_analysis.json'
        
        analysis_data = {
            'pdf_file': str(self.pdf_path),
            'total_pages': self.total_pages,
            'total_leaf_nodes': len(results),
            'chapters_found': self.chapters,
            'leaf_nodes': results,
            'special_nodes': [r for r in results if r.get('is_part_intro', False)]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"분석 결과가 저장되었습니다: {output_file}")
        return output_file
    
    def run_analysis(self):
        """전체 분석을 실행합니다."""
        print("=== PDF Leaf Node 분석 시작 ===")
        
        # 1. PDF 로드
        if not self.load_pdf():
            return False
        
        # 2. TOC 파싱
        if not self.parse_toc_file():
            return False
        
        # 3. 챕터 페이지 찾기
        if not self.find_chapter_pages():
            return False
        
        # 4. 리프 노드 분석
        results = self.analyze_leaf_nodes()
        
        # 5. 결과 저장
        output_file = self.save_analysis_results(results)
        
        print("=== 분석 완료 ===")
        print(f"결과 파일: {output_file}")
        
        # PDF 파일 닫기
        if self.pdf_doc:
            self.pdf_doc.close()
        
        return True

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    
    analyzer = LeafNodeAnalyzer(pdf_path, toc_path)
    success = analyzer.run_analysis()
    
    if success:
        print("분석이 성공적으로 완료되었습니다.")
    else:
        print("분석 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()