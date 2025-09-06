#!/usr/bin/env python3
"""
Precise Page Mapper - PDF의 실제 챕터 페이지와 리프 노드 매핑
"""

import pdfplumber
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class PrecisePageMapper:
    def __init__(self, pdf_path: str, analysis_file: str):
        self.pdf_path = Path(pdf_path)
        self.analysis_file = Path(analysis_file)
        self.pdf_doc = None
        self.total_pages = 0
        self.analysis_data = None
        self.chapter_pages = {}
        self.toc_pages = {}
        
    def load_data(self):
        """PDF와 분석 데이터를 로드합니다."""
        try:
            # PDF 로드
            self.pdf_doc = pdfplumber.open(str(self.pdf_path))
            self.total_pages = len(self.pdf_doc.pages)
            print(f"PDF 로드 완료: {self.total_pages}페이지")
            
            # 분석 데이터 로드
            with open(self.analysis_file, 'r', encoding='utf-8') as f:
                self.analysis_data = json.load(f)
            print(f"분석 데이터 로드 완료: {self.analysis_data['total_leaf_nodes']}개 리프 노드")
            
            return True
        except Exception as e:
            print(f"데이터 로드 실패: {e}")
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
    
    def find_toc_pages(self) -> Dict[int, str]:
        """목차(Table of Contents) 페이지들을 찾습니다."""
        toc_indicators = [
            'Contents',
            'Table of contents',
            'CONTENTS',
            'Part 1',
            'PART 1',
            'Chapter 1',
            'CHAPTER 1'
        ]
        
        toc_pages = {}
        
        # 처음 30페이지에서 목차 찾기
        for page_num in range(min(30, self.total_pages)):
            text = self.extract_text_from_page(page_num)
            if not text:
                continue
            
            # 목차 지시자 확인
            for indicator in toc_indicators:
                if indicator in text:
                    toc_pages[page_num + 1] = text[:500]  # 처음 500자만 저장
                    print(f"목차 페이지 발견: {page_num + 1}")
                    break
        
        return toc_pages
    
    def find_accurate_chapter_pages(self) -> Dict[int, Dict]:
        """정확한 챕터 시작 페이지를 찾습니다."""
        chapter_data = {}
        
        # 챕터 패턴들
        patterns = {
            'chapter': [
                r'^\s*(\d+)\s*$',  # 숫자만 있는 경우
                r'^(\d+)\s+(.+?)$',  # "1 Complexity..." 형태
                r'CHAPTER\s+(\d+)',  # "CHAPTER 1" 형태
                r'Chapter\s+(\d+)',  # "Chapter 1" 형태
            ],
            'part': [
                r'Part\s+(\d+)',
                r'PART\s+(\d+)',
            ],
            'appendix': [
                r'Appendix\s+([A-Z])',
                r'APPENDIX\s+([A-Z])',
            ]
        }
        
        # 전체 PDF 스캔 (목차 이후부터)
        start_page = 25  # 일반적으로 목차 이후
        
        for page_num in range(start_page, self.total_pages):
            text = self.extract_text_from_page(page_num)
            if not text:
                continue
                
            lines = text.split('\n')
            
            # 페이지 상단 부분만 확인 (첫 20줄)
            for i, line in enumerate(lines[:20]):
                line = line.strip()
                if not line or len(line) < 2:
                    continue
                
                # 챕터 패턴 확인
                for pattern_type, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            chapter_key = match.group(1)
                            
                            # 중복 방지 - 더 좋은 매칭만 유지
                            if chapter_key not in chapter_data or i < chapter_data[chapter_key].get('line_position', 999):
                                chapter_data[chapter_key] = {
                                    'page': page_num + 1,
                                    'text': line,
                                    'pattern_type': pattern_type,
                                    'line_position': i,
                                    'full_text_preview': text[:300]
                                }
                                print(f"{pattern_type.capitalize()} {chapter_key} 발견: 페이지 {page_num + 1}")
                                break
                    else:
                        continue
                    break
        
        return chapter_data
    
    def extract_specific_content(self, page_start: int, page_end: int) -> str:
        """특정 페이지 범위의 내용을 추출합니다."""
        content = []
        
        for page_num in range(page_start - 1, min(page_end, self.total_pages)):
            if page_num < 0:
                continue
                
            text = self.extract_text_from_page(page_num)
            content.append(f"\n=== Page {page_num + 1} ===\n")
            content.append(text)
        
        return '\n'.join(content)
    
    def map_leaf_nodes_to_pages(self) -> List[Dict]:
        """리프 노드들을 실제 PDF 페이지에 매핑합니다."""
        if not self.analysis_data:
            return []
        
        # 정확한 챕터 페이지 찾기
        self.chapter_pages = self.find_accurate_chapter_pages()
        self.toc_pages = self.find_toc_pages()
        
        mapped_nodes = []
        
        for leaf_node in self.analysis_data['leaf_nodes']:
            mapped_node = leaf_node.copy()
            
            # Part Introduction 노드들의 특별 처리
            if leaf_node.get('is_part_intro', False):
                part_text = leaf_node.get('part', '')
                
                if 'Part1' in part_text:
                    # Part 1 시작 페이지 찾기
                    if '1' in self.chapter_pages:
                        ch1_page = self.chapter_pages['1']['page']
                        mapped_node['accurate_page_range'] = f"{max(30, ch1_page - 5)}-{ch1_page - 1}"
                        mapped_node['content_preview'] = self.extract_specific_content(
                            max(30, ch1_page - 3), ch1_page - 1
                        )[:500]
                elif 'Part2' in part_text:
                    # Part 2 시작 페이지 찾기 (Chapter 7 전)
                    if '7' in self.chapter_pages:
                        ch7_page = self.chapter_pages['7']['page']
                        mapped_node['accurate_page_range'] = f"{ch7_page - 5}-{ch7_page - 1}"
                        mapped_node['content_preview'] = self.extract_specific_content(
                            ch7_page - 3, ch7_page - 1
                        )[:500]
                elif 'Part3' in part_text:
                    # Part 3 시작 페이지 찾기 (Chapter 12 전)
                    if '12' in self.chapter_pages:
                        ch12_page = self.chapter_pages['12']['page']
                        mapped_node['accurate_page_range'] = f"{ch12_page - 5}-{ch12_page - 1}"
                        mapped_node['content_preview'] = self.extract_specific_content(
                            ch12_page - 3, ch12_page - 1
                        )[:500]
            
            # 일반 챕터 노드들
            else:
                chapter_text = leaf_node.get('chapter', '')
                
                # 챕터 번호 추출
                chapter_match = re.search(r'(\d+)', chapter_text)
                if chapter_match:
                    chapter_num = chapter_match.group(1)
                    
                    if chapter_num in self.chapter_pages:
                        chapter_info = self.chapter_pages[chapter_num]
                        start_page = chapter_info['page']
                        
                        # 다음 챕터까지의 범위 계산
                        next_chapter_num = str(int(chapter_num) + 1)
                        if next_chapter_num in self.chapter_pages:
                            end_page = self.chapter_pages[next_chapter_num]['page'] - 1
                        else:
                            end_page = start_page + 20  # 기본 20페이지
                        
                        mapped_node['accurate_page_range'] = f"{start_page}-{end_page}"
                        mapped_node['chapter_start_page'] = start_page
                        mapped_node['content_preview'] = self.extract_specific_content(
                            start_page, min(start_page + 2, end_page)
                        )[:500]
            
            mapped_nodes.append(mapped_node)
        
        return mapped_nodes
    
    def save_mapping_results(self, mapped_nodes: List[Dict]):
        """매핑 결과를 저장합니다."""
        output_file = self.pdf_path.parent / 'pdf-leaf-extractor' / 'precise_page_mapping.json'
        
        mapping_data = {
            'pdf_file': str(self.pdf_path),
            'total_pages': self.total_pages,
            'chapter_pages_found': self.chapter_pages,
            'toc_pages_found': self.toc_pages,
            'total_leaf_nodes': len(mapped_nodes),
            'mapped_leaf_nodes': mapped_nodes,
            'special_part_intro_nodes': [
                node for node in mapped_nodes 
                if node.get('is_part_intro', False)
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_data, f, ensure_ascii=False, indent=2)
        
        print(f"정확한 페이지 매핑 결과 저장: {output_file}")
        return output_file
    
    def run_mapping(self):
        """전체 매핑 프로세스 실행"""
        print("=== 정확한 페이지 매핑 시작 ===")
        
        if not self.load_data():
            return False
        
        # 리프 노드 매핑
        mapped_nodes = self.map_leaf_nodes_to_pages()
        
        # 결과 저장
        output_file = self.save_mapping_results(mapped_nodes)
        
        # PDF 닫기
        if self.pdf_doc:
            self.pdf_doc.close()
        
        print("=== 매핑 완료 ===")
        print(f"매핑된 노드 수: {len(mapped_nodes)}")
        print(f"발견된 챕터: {list(self.chapter_pages.keys())}")
        print(f"결과 파일: {output_file}")
        
        return True

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    analysis_file = "/home/nadle/projects/Knowledge_Sherpa/v2/pdf-leaf-extractor/leaf_node_analysis.json"
    
    mapper = PrecisePageMapper(pdf_path, analysis_file)
    success = mapper.run_mapping()
    
    if success:
        print("정확한 페이지 매핑이 성공적으로 완료되었습니다.")
    else:
        print("매핑 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()