#!/usr/bin/env python3
"""
Final Leaf Extractor - 실제 챕터 내용을 기반으로 한 정확한 리프 노드 추출
"""

import pdfplumber
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class FinalLeafExtractor:
    def __init__(self, pdf_path: str, toc_path: str):
        self.pdf_path = Path(pdf_path)
        self.toc_path = Path(toc_path)
        self.pdf_doc = None
        self.total_pages = 0
        self.leaf_nodes = []
        self.actual_chapters = {}
        
        # 실제 챕터 제목들 (매뉴얼로 정의)
        self.known_chapters = {
            "1": {"title": "Complexity of object-oriented programming", "expected_page": 50},
            "2": {"title": "Separation between code and data", "expected_page": 75},
            "3": {"title": "Basic data manipulation", "expected_page": 100},
            "4": {"title": "State management", "expected_page": 125},
            "5": {"title": "Basic concurrency control", "expected_page": 150},
            "6": {"title": "Unit tests", "expected_page": 175},
            "7": {"title": "Basic data validation", "expected_page": 200},
            "8": {"title": "Advanced concurrency control", "expected_page": 225},
            "9": {"title": "Persistent data structures", "expected_page": 250},
            "10": {"title": "Database operations", "expected_page": 275},
            "11": {"title": "Web services", "expected_page": 300},
            "12": {"title": "Advanced data validation", "expected_page": 325},
            "13": {"title": "Polymorphism", "expected_page": 350},
            "14": {"title": "Advanced data manipulation", "expected_page": 375},
            "15": {"title": "Debugging", "expected_page": 400},
        }
    
    def load_data(self):
        """PDF와 목차 데이터를 로드합니다."""
        try:
            # PDF 로드
            self.pdf_doc = pdfplumber.open(str(self.pdf_path))
            self.total_pages = len(self.pdf_doc.pages)
            print(f"PDF 로드 완료: {self.total_pages}페이지")
            
            # TOC 파싱
            self.parse_toc_file()
            
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
    
    def parse_toc_file(self):
        """TOC 파일에서 리프 노드를 파싱합니다."""
        try:
            with open(self.toc_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
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
                    node_match = re.match(r'^(.*?)\(node(\d+)\)\s*\*\*\[LEAF\]\*\*', line)
                    if node_match:
                        node_text = node_match.group(1).strip()
                        node_level = int(node_match.group(2))
                        
                        leaf_node = {
                            'text': node_text,
                            'node_level': node_level,
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
    
    def find_actual_chapters(self):
        """실제 챕터 시작 페이지를 찾습니다."""
        print("실제 챕터 페이지를 찾고 있습니다...")
        
        for chapter_num, info in self.known_chapters.items():
            chapter_title = info['title']
            expected_page = info['expected_page']
            
            # 예상 페이지 주변에서 검색
            search_range = range(max(25, expected_page - 25), min(self.total_pages, expected_page + 25))
            
            for page_num in search_range:
                text = self.extract_text_from_page(page_num)
                if not text:
                    continue
                
                # 챕터 제목을 포함하는 패턴들 검색
                patterns = [
                    f"Chapter {chapter_num}",
                    f"CHAPTER {chapter_num}",
                    f"{chapter_num}\\s+{re.escape(chapter_title[:20])}",  # 제목 앞부분
                    f"^\\s*{chapter_num}\\s*$",  # 단독 숫자
                ]
                
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                        self.actual_chapters[chapter_num] = {
                            'page': page_num + 1,
                            'title': chapter_title,
                            'pattern_matched': pattern,
                            'text_preview': text[:200]
                        }
                        print(f"Chapter {chapter_num} 발견: 페이지 {page_num + 1}")
                        break
                
                if chapter_num in self.actual_chapters:
                    break
    
    def extract_chapter_sections(self, chapter_num: str, start_page: int) -> Dict:
        """특정 챕터의 섹션들을 추출합니다."""
        # 다음 챕터 페이지 찾기
        next_chapter_num = str(int(chapter_num) + 1)
        if next_chapter_num in self.actual_chapters:
            end_page = self.actual_chapters[next_chapter_num]['page'] - 1
        else:
            end_page = min(self.total_pages, start_page + 30)
        
        # 챕터 내용 추출
        chapter_content = ""
        for page_num in range(start_page - 1, end_page):
            if page_num >= self.total_pages:
                break
            text = self.extract_text_from_page(page_num)
            chapter_content += f"\n--- Page {page_num + 1} ---\n{text}"
        
        return {
            'start_page': start_page,
            'end_page': end_page,
            'content': chapter_content,
            'sections_found': []
        }
    
    def map_leaf_nodes_to_content(self) -> List[Dict]:
        """리프 노드들을 실제 내용에 매핑합니다."""
        # 실제 챕터 찾기
        self.find_actual_chapters()
        
        mapped_nodes = []
        
        for i, leaf in enumerate(self.leaf_nodes):
            mapped_node = leaf.copy()
            mapped_node['id'] = i + 1
            
            # Part Introduction 노드들의 특별 처리
            if leaf.get('is_part_intro', False):
                part_text = leaf.get('part', '')
                
                if 'Part1' in part_text:
                    if '1' in self.actual_chapters:
                        ch1_page = self.actual_chapters['1']['page']
                        start_page = max(30, ch1_page - 5)
                        end_page = ch1_page - 1
                        mapped_node['accurate_page_range'] = f"{start_page}-{end_page}"
                        mapped_node['extracted_content'] = self.extract_specific_content(start_page, end_page)
                
                elif 'Part2' in part_text:
                    if '7' in self.actual_chapters:
                        ch7_page = self.actual_chapters['7']['page']
                        start_page = ch7_page - 5
                        end_page = ch7_page - 1
                        mapped_node['accurate_page_range'] = f"{start_page}-{end_page}"
                        mapped_node['extracted_content'] = self.extract_specific_content(start_page, end_page)
                
                elif 'Part3' in part_text:
                    if '12' in self.actual_chapters:
                        ch12_page = self.actual_chapters['12']['page']
                        start_page = ch12_page - 5
                        end_page = ch12_page - 1
                        mapped_node['accurate_page_range'] = f"{start_page}-{end_page}"
                        mapped_node['extracted_content'] = self.extract_specific_content(start_page, end_page)
            
            # 일반 챕터 노드들
            else:
                chapter_text = leaf.get('chapter', '')
                chapter_match = re.search(r'(\d+)', chapter_text)
                
                if chapter_match:
                    chapter_num = chapter_match.group(1)
                    
                    if chapter_num in self.actual_chapters:
                        chapter_info = self.actual_chapters[chapter_num]
                        chapter_sections = self.extract_chapter_sections(
                            chapter_num, chapter_info['page']
                        )
                        
                        mapped_node['chapter_info'] = chapter_info
                        mapped_node['chapter_sections'] = chapter_sections
                        mapped_node['accurate_page_range'] = f"{chapter_sections['start_page']}-{chapter_sections['end_page']}"
            
            mapped_nodes.append(mapped_node)
        
        return mapped_nodes
    
    def extract_specific_content(self, start_page: int, end_page: int) -> str:
        """특정 페이지 범위의 내용을 추출합니다."""
        content = []
        for page_num in range(start_page - 1, min(end_page, self.total_pages)):
            if page_num < 0:
                continue
            text = self.extract_text_from_page(page_num)
            content.append(f"\n=== Page {page_num + 1} ===\n{text}")
        return '\n'.join(content)
    
    def save_final_results(self, mapped_nodes: List[Dict]):
        """최종 결과를 저장합니다."""
        output_dir = self.pdf_path.parent / 'pdf-leaf-extractor'
        
        # 전체 결과
        final_results = {
            'pdf_file': str(self.pdf_path),
            'total_pages': self.total_pages,
            'chapters_found': self.actual_chapters,
            'total_leaf_nodes': len(mapped_nodes),
            'leaf_nodes': mapped_nodes,
            'part_intro_nodes': [node for node in mapped_nodes if node.get('is_part_intro', False)]
        }
        
        output_file = output_dir / 'final_leaf_extraction.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
        
        print(f"최종 결과 저장: {output_file}")
        
        # 각 챕터별로 개별 파일 저장
        for chapter_num, chapter_info in self.actual_chapters.items():
            chapter_nodes = [
                node for node in mapped_nodes 
                if node.get('chapter', '').startswith(chapter_num)
            ]
            
            if chapter_nodes:
                chapter_file = output_dir / f'chapter_{chapter_num}_content.json'
                chapter_data = {
                    'chapter': chapter_num,
                    'title': chapter_info['title'],
                    'page_info': chapter_info,
                    'leaf_nodes': chapter_nodes
                }
                
                with open(chapter_file, 'w', encoding='utf-8') as f:
                    json.dump(chapter_data, f, ensure_ascii=False, indent=2)
                
                print(f"Chapter {chapter_num} 저장: {chapter_file}")
        
        # Part Introduction 노드들 별도 저장
        part_intro_nodes = [node for node in mapped_nodes if node.get('is_part_intro', False)]
        if part_intro_nodes:
            part_intro_file = output_dir / 'part_introductions.json'
            with open(part_intro_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'part_introductions': part_intro_nodes,
                    'total_count': len(part_intro_nodes)
                }, f, ensure_ascii=False, indent=2)
            
            print(f"Part Introduction 노드들 저장: {part_intro_file}")
        
        return output_file
    
    def run_extraction(self):
        """전체 추출 프로세스 실행"""
        print("=== Final Leaf Node 추출 시작 ===")
        
        if not self.load_data():
            return False
        
        # 리프 노드 매핑
        mapped_nodes = self.map_leaf_nodes_to_content()
        
        # 결과 저장
        output_file = self.save_final_results(mapped_nodes)
        
        # PDF 닫기
        if self.pdf_doc:
            self.pdf_doc.close()
        
        print("=== 추출 완료 ===")
        print(f"총 리프 노드: {len(mapped_nodes)}")
        print(f"발견된 챕터: {list(self.actual_chapters.keys())}")
        print(f"Part Introduction 노드: {len([n for n in mapped_nodes if n.get('is_part_intro', False)])}")
        print(f"최종 결과 파일: {output_file}")
        
        return True

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    
    extractor = FinalLeafExtractor(pdf_path, toc_path)
    success = extractor.run_extraction()
    
    if success:
        print("리프 노드 추출이 성공적으로 완료되었습니다.")
    else:
        print("추출 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()