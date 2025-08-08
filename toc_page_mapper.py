#!/usr/bin/env python3
"""
정규화된 목차에 PDF 페이지 정보를 추가하는 도구
"""

import pdfplumber
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class TOCPageMapper:
    def __init__(self, pdf_path: str, toc_path: str, chapter_mapping_path: str):
        self.pdf_path = pdf_path
        self.toc_path = toc_path
        self.chapter_mapping_path = chapter_mapping_path
        self.chapter_pages = {}
        self.section_pages = {}
        
    def parse_chapter_mappings(self) -> Dict[str, Dict[str, int]]:
        """chapter_page_mappings.md에서 챕터별 페이지 정보 파싱"""
        print("기존 챕터 페이지 매핑 정보 파싱 중...")
        
        with open(self.chapter_mapping_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 챕터 매핑 테이블 파싱
        chapter_pattern = r'\|\s*Chapter\s+(\d+)\s*\|\s*([^|]+)\s*\|\s*(\d+)\s*\|'
        chapters = re.findall(chapter_pattern, content)
        
        mappings = {}
        for chapter_num, title, start_page in chapters:
            chapter_key = f"Chapter {chapter_num}"
            mappings[chapter_key] = {
                'title': title.strip(),
                'start_page': int(start_page),
                'chapter_num': int(chapter_num)
            }
        
        # 페이지 범위 계산 (각 챕터의 끝 페이지 추정)
        sorted_chapters = sorted(mappings.items(), key=lambda x: x[1]['start_page'])
        
        for i, (chapter_key, info) in enumerate(sorted_chapters):
            if i < len(sorted_chapters) - 1:
                next_start = sorted_chapters[i + 1][1]['start_page']
                info['end_page'] = next_start - 1
            else:
                # 마지막 챕터는 추후 결정 (현재는 임시로 50페이지 할당)
                info['end_page'] = info['start_page'] + 50
        
        self.chapter_pages = mappings
        return mappings
    
    def find_section_in_pdf(self, section_title: str, chapter_range: Tuple[int, int]) -> Optional[int]:
        """PDF에서 특정 섹션의 시작 페이지 찾기"""
        start_page, end_page = chapter_range
        
        # 섹션 제목을 다양한 패턴으로 변환
        patterns = self._generate_section_patterns(section_title)
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
                    page = pdf.pages[page_num]
                    text = page.extract_text()
                    
                    if text:
                        # 각 패턴에 대해 매칭 시도
                        for pattern in patterns:
                            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                                return page_num + 1  # 1-based 페이지 번호
        except Exception as e:
            print(f"PDF 검색 중 오류: {e}")
            return None
        
        return None
    
    def _generate_section_patterns(self, section_title: str) -> List[str]:
        """섹션 제목에 대한 다양한 검색 패턴 생성"""
        patterns = []
        
        # 기본 제목 패턴
        clean_title = re.sub(r'[^\w\s]', '', section_title)
        patterns.append(re.escape(clean_title))
        
        # 번호가 포함된 경우 처리
        if re.match(r'^(\d+)\.?(\d+)?\.?(\d+)?\s+(.+)', section_title):
            match = re.match(r'^(\d+)\.?(\d+)?\.?(\d+)?\s+(.+)', section_title)
            if match:
                numbers = [g for g in match.groups()[:3] if g is not None]
                title_part = match.group(4)
                
                # 번호 패턴들
                if len(numbers) == 1:
                    patterns.append(rf'{numbers[0]}\s+{re.escape(title_part)}')
                elif len(numbers) == 2:
                    patterns.append(rf'{numbers[0]}\.{numbers[1]}\s+{re.escape(title_part)}')
                    patterns.append(rf'{numbers[0]}\s*{numbers[1]}\s+{re.escape(title_part)}')
                elif len(numbers) == 3:
                    patterns.append(rf'{numbers[0]}\.{numbers[1]}\.{numbers[2]}\s+{re.escape(title_part)}')
                    patterns.append(rf'{numbers[0]}\s*{numbers[1]}\s*{numbers[2]}\s+{re.escape(title_part)}')
        
        # 특수 문자 제거 버전
        simplified = re.sub(r'[^\w\s]', ' ', section_title)
        simplified = re.sub(r'\s+', r'\\s+', simplified.strip())
        patterns.append(simplified)
        
        return patterns
    
    def parse_toc_structure(self) -> List[Dict]:
        """정규화된 목차 구조 파싱"""
        print("정규화된 목차 구조 파싱 중...")
        
        with open(self.toc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        toc_items = []
        current_chapter = None
        
        for line_num, line in enumerate(lines):
            line = line.rstrip()
            if not line:
                continue
                
            # LEAF 노드인지 확인
            is_leaf = '**[LEAF]**' in line
            
            if not is_leaf:
                continue
            
            # 들여쓰기 레벨 계산
            indent_level = (len(line) - len(line.lstrip())) // 2
            
            # 제목 추출 (node 정보와 LEAF 표시 제거)
            title_match = re.search(r'^[\s-]*(.+?)\s*\(node\d+\)', line)
            if title_match:
                title = title_match.group(1).strip()
                
                # 챕터 정보 추출
                chapter_match = re.search(r'^(\d+(?:\.\d+)*)\s+(.+)', title)
                if chapter_match:
                    current_chapter = f"Chapter {chapter_match.group(1).split('.')[0]}"
                elif re.search(r'Chapter\s+\d+', title):
                    chapter_match = re.search(r'Chapter\s+(\d+)', title)
                    if chapter_match:
                        current_chapter = f"Chapter {chapter_match.group(1)}"
                
                toc_items.append({
                    'line_num': line_num,
                    'title': title,
                    'indent_level': indent_level,
                    'is_leaf': is_leaf,
                    'chapter': current_chapter,
                    'original_line': line
                })
        
        return toc_items
    
    def find_section_pages(self, toc_items: List[Dict]) -> Dict[str, int]:
        """TOC 아이템들의 페이지 정보 찾기"""
        print("섹션별 페이지 정보 탐지 중...")
        
        section_pages = {}
        
        for item in toc_items:
            title = item['title']
            chapter = item.get('chapter')
            
            if chapter and chapter in self.chapter_pages:
                chapter_info = self.chapter_pages[chapter]
                start_page = chapter_info['start_page']
                end_page = chapter_info['end_page']
                
                print(f"  {title} 검색 중 (페이지 {start_page}-{end_page})...")
                
                # PDF에서 섹션 찾기
                found_page = self.find_section_in_pdf(title, (start_page, end_page))
                
                if found_page:
                    section_pages[title] = found_page
                    print(f"    → 페이지 {found_page}에서 발견")
                else:
                    print(f"    → 찾을 수 없음")
            
        return section_pages
    
    def estimate_page_ranges(self, toc_items: List[Dict], section_pages: Dict[str, int]) -> Dict[str, Tuple[int, int]]:
        """섹션별 페이지 범위 추정"""
        print("페이지 범위 추정 중...")
        
        page_ranges = {}
        
        # 페이지가 발견된 섹션들을 정렬
        found_sections = [(title, page) for title, page in section_pages.items()]
        found_sections.sort(key=lambda x: x[1])
        
        for i, (title, start_page) in enumerate(found_sections):
            if i < len(found_sections) - 1:
                end_page = found_sections[i + 1][1] - 1
            else:
                # 마지막 섹션은 챕터 끝까지
                chapter = None
                for item in toc_items:
                    if item['title'] == title:
                        chapter = item.get('chapter')
                        break
                
                if chapter and chapter in self.chapter_pages:
                    end_page = self.chapter_pages[chapter]['end_page']
                else:
                    end_page = start_page + 5  # 기본 5페이지
            
            page_ranges[title] = (start_page, end_page)
        
        return page_ranges
    
    def run(self) -> Dict[str, any]:
        """전체 프로세스 실행"""
        print("=== TOC 페이지 매핑 시작 ===")
        
        # 1. 챕터 매핑 정보 파싱
        chapter_mappings = self.parse_chapter_mappings()
        print(f"챕터 매핑 정보: {len(chapter_mappings)}개 챕터")
        
        # 2. TOC 구조 파싱  
        toc_items = self.parse_toc_structure()
        print(f"LEAF 노드: {len(toc_items)}개")
        
        # 3. 섹션 페이지 찾기
        section_pages = self.find_section_pages(toc_items)
        print(f"페이지 발견: {len(section_pages)}개 섹션")
        
        # 4. 페이지 범위 추정
        page_ranges = self.estimate_page_ranges(toc_items, section_pages)
        print(f"페이지 범위 추정: {len(page_ranges)}개 섹션")
        
        return {
            'chapter_mappings': chapter_mappings,
            'toc_items': toc_items,
            'section_pages': section_pages,
            'page_ranges': page_ranges
        }

if __name__ == "__main__":
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    chapter_mapping_path = "/home/nadle/projects/Knowledge_Sherpa/v2/chapter_page_mappings.md"
    
    mapper = TOCPageMapper(pdf_path, toc_path, chapter_mapping_path)
    result = mapper.run()
    
    # 결과 저장
    output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/toc_page_mapping_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        # toc_items는 직렬화할 수 없으므로 제외
        result_to_save = {
            'chapter_mappings': result['chapter_mappings'],
            'section_pages': result['section_pages'],
            'page_ranges': result['page_ranges']
        }
        json.dump(result_to_save, f, ensure_ascii=False, indent=2)
    
    print(f"\n결과가 {output_path}에 저장되었습니다.")