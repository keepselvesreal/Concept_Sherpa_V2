#!/usr/bin/env python3
"""
실제 PDF 검색을 통한 정확한 페이지 정보로 목차 업데이트
"""

import pdfplumber
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class AccurateTOCPageMapper:
    def __init__(self, pdf_path: str, toc_path: str, chapter_mapping_path: str):
        self.pdf_path = pdf_path
        self.toc_path = toc_path  
        self.chapter_mapping_path = chapter_mapping_path
        self.chapter_pages = {}
        self.verified_pages = {}
        
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
        
        # 페이지 범위 계산
        sorted_chapters = sorted(mappings.items(), key=lambda x: x[1]['start_page'])
        
        for i, (chapter_key, info) in enumerate(sorted_chapters):
            if i < len(sorted_chapters) - 1:
                next_start = sorted_chapters[i + 1][1]['start_page']
                info['end_page'] = next_start - 1
            else:
                info['end_page'] = info['start_page'] + 50
        
        self.chapter_pages = mappings
        return mappings
    
    def find_section_in_pdf(self, section_title: str, chapter_range: Tuple[int, int]) -> Optional[int]:
        """PDF에서 특정 섹션의 정확한 페이지 찾기"""
        start_page, end_page = chapter_range
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
                                # 실제 섹션 헤더인지 검증
                                lines = text.split('\n')
                                for line in lines:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        stripped_line = line.strip()
                                        # 섹션 제목 라인은 보통 짧고 독립적임
                                        if len(stripped_line) < 120:
                                            return page_num + 1
                                return page_num + 1
        except Exception as e:
            print(f"PDF 검색 중 오류 ({section_title}): {e}")
            return None
        
        return None
        
    def _generate_section_patterns(self, section_title: str) -> List[str]:
        """섹션 제목에 대한 다양한 검색 패턴 생성"""
        patterns = []
        
        # 번호가 있는 경우 처리
        if re.match(r'^\d+', section_title):
            match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)', section_title)
            if match:
                number_part = match.group(1)
                title_part = match.group(2)
                
                escaped_number = re.escape(number_part)
                escaped_title = re.escape(title_part)
                
                patterns.extend([
                    f"{escaped_number}\\s+{escaped_title}",
                    f"{escaped_number}\\.?\\s+{escaped_title}",
                    escaped_title  # 번호 없이 제목만
                ])
        else:
            # 번호가 없는 경우
            escaped_title = re.escape(section_title)
            patterns.append(escaped_title)
        
        # 공백을 유연하게 처리
        for i, pattern in enumerate(patterns[:]):
            flexible = re.sub(r'\\?\s+', r'\\s+', pattern)
            patterns.append(flexible)
            
        return list(set(patterns))
    
    def collect_leaf_sections(self) -> List[Dict]:
        """TOC에서 LEAF 노드들 수집"""
        print("LEAF 섹션들 수집 중...")
        
        with open(self.toc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        leaf_sections = []
        current_chapter = None
        
        for line_num, line in enumerate(lines):
            line = line.rstrip()
            if not line or '**[LEAF]**' not in line:
                continue
                
            # 제목 추출
            title_match = re.search(r'^[\s-]*(.+?)\s*\(node\d+\)', line)
            if not title_match:
                continue
                
            title = title_match.group(1).strip()
            
            # 챕터 식별
            chapter_match = re.search(r'^(\d+(?:\.\d+)*)\s+(.+)', title)
            if chapter_match:
                chapter_num = chapter_match.group(1).split('.')[0]
                current_chapter = f"Chapter {chapter_num}"
            elif re.match(r'^\d+\s+', title):
                chapter_match = re.match(r'^(\d+)\s+', title)
                if chapter_match:
                    current_chapter = f"Chapter {chapter_match.group(1)}"
            
            if current_chapter and current_chapter in self.chapter_pages:
                leaf_sections.append({
                    'title': title,
                    'chapter': current_chapter,
                    'line_num': line_num,
                    'original_line': line
                })
        
        print(f"수집된 LEAF 섹션: {len(leaf_sections)}개")
        return leaf_sections
    
    def verify_section_pages(self, leaf_sections: List[Dict]) -> Dict[str, int]:
        """중요한 섹션들의 페이지를 실제 PDF에서 검증"""
        print("중요 섹션들의 페이지 검증 중...")
        
        # 우선순위가 높은 섹션들만 선별 (번호가 있는 주요 섹션들)
        priority_sections = []
        for section in leaf_sections:
            title = section['title']
            # 번호가 있는 섹션들만 (예: 1.1.1, 6.2.1 등)
            if re.match(r'^\d+\.\d+(\.\d+)?\s+', title):
                priority_sections.append(section)
        
        print(f"우선 검증할 섹션: {len(priority_sections)}개")
        
        verified_pages = {}
        for i, section in enumerate(priority_sections[:30]):  # 처음 30개만 검증
            title = section['title']
            chapter = section['chapter']
            
            if chapter in self.chapter_pages:
                chapter_info = self.chapter_pages[chapter]
                start_page = chapter_info['start_page']
                end_page = chapter_info['end_page']
                
                print(f"  [{i+1}/{len(priority_sections[:30])}] {title} 검증 중...")
                
                found_page = self.find_section_in_pdf(title, (start_page, end_page))
                
                if found_page:
                    verified_pages[title] = found_page
                    print(f"    → 페이지 {found_page}에서 발견")
                else:
                    print(f"    → 찾을 수 없음")
        
        return verified_pages
    
    def estimate_page_ranges_with_verification(self, leaf_sections: List[Dict], verified_pages: Dict[str, int]) -> Dict[str, Tuple[int, int]]:
        """검증된 페이지 정보를 바탕으로 다른 섹션들의 페이지 범위 추정"""
        print("페이지 범위 추정 중...")
        
        page_ranges = {}
        
        # 챕터별로 섹션들을 그룹화
        chapter_sections = {}
        for section in leaf_sections:
            chapter = section['chapter']
            if chapter not in chapter_sections:
                chapter_sections[chapter] = []
            chapter_sections[chapter].append(section)
        
        # 각 챕터별로 페이지 추정
        for chapter, sections in chapter_sections.items():
            if chapter not in self.chapter_pages:
                continue
                
            chapter_info = self.chapter_pages[chapter]
            chapter_start = chapter_info['start_page']
            chapter_end = chapter_info['end_page']
            
            # 해당 챕터에서 검증된 섹션들만 수집
            verified_in_chapter = []
            for section in sections:
                if section['title'] in verified_pages:
                    verified_in_chapter.append((section['title'], verified_pages[section['title']]))
            
            # 검증된 페이지들을 정렬
            verified_in_chapter.sort(key=lambda x: x[1])
            
            if verified_in_chapter:
                # 검증된 섹션들 사이의 페이지를 추정
                for i, section in enumerate(sections):
                    title = section['title']
                    
                    if title in verified_pages:
                        # 이미 검증된 경우
                        start_page = verified_pages[title]
                        
                        # 다음 검증된 섹션까지의 페이지 계산
                        next_page = None
                        current_page = verified_pages[title]
                        
                        for verified_title, verified_page in verified_in_chapter:
                            if verified_page > current_page:
                                next_page = verified_page - 1
                                break
                        
                        if next_page is None:
                            next_page = chapter_end
                            
                        end_page = min(start_page + 3, next_page)  # 최대 3페이지
                        page_ranges[title] = (start_page, end_page)
                        
                    else:
                        # 검증되지 않은 경우 상대적 위치로 추정
                        section_index = i
                        total_sections = len(sections)
                        
                        relative_pos = section_index / total_sections
                        estimated_page = int(chapter_start + relative_pos * (chapter_end - chapter_start))
                        
                        page_ranges[title] = (estimated_page, estimated_page + 2)
            else:
                # 검증된 섹션이 없는 경우 균등 분배
                for i, section in enumerate(sections):
                    section_index = i
                    total_sections = len(sections)
                    
                    relative_start = section_index / total_sections
                    relative_end = (section_index + 1) / total_sections
                    
                    start_page = int(chapter_start + relative_start * (chapter_end - chapter_start))
                    end_page = int(chapter_start + relative_end * (chapter_end - chapter_start)) - 1
                    
                    page_ranges[section['title']] = (start_page, max(start_page + 1, end_page))
        
        return page_ranges
    
    def generate_enhanced_toc(self, page_ranges: Dict[str, Tuple[int, int]]) -> str:
        """페이지 정보가 추가된 최종 목차 생성"""
        print("최종 목차 생성 중...")
        
        with open(self.toc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        enhanced_lines = []
        
        for line in lines:
            original_line = line.rstrip()
            if not original_line:
                enhanced_lines.append('')
                continue
            
            # LEAF 노드가 아닌 경우 그대로 추가
            if '**[LEAF]**' not in original_line:
                enhanced_lines.append(original_line)
                continue
                
            # 제목 추출
            title_match = re.search(r'^[\s-]*(.+?)\s*\(node\d+\)', original_line)
            if not title_match:
                enhanced_lines.append(original_line)
                continue
                
            title = title_match.group(1).strip()
            
            # 페이지 정보 추가
            page_info = ""
            if title in page_ranges:
                start_page, end_page = page_ranges[title]
                if start_page == end_page:
                    page_info = f" **[Page: {start_page}]**"
                else:
                    page_info = f" **[Pages: {start_page}-{end_page}]**"
            
            # 새 라인 생성 (기존 페이지 정보가 있다면 대체)
            enhanced_line = re.sub(r'\s*\*\*\[Pages?:.*?\]\*\*', '', original_line)
            enhanced_line = enhanced_line.replace('**[LEAF]**', f'**[LEAF]**{page_info}')
            enhanced_lines.append(enhanced_line)
        
        return '\n'.join(enhanced_lines)
    
    def run(self):
        """전체 프로세스 실행"""
        print("=== 정확한 TOC 페이지 매핑 시작 ===")
        
        # 1. 챕터 매핑 정보 파싱
        self.parse_chapter_mappings()
        
        # 2. LEAF 섹션들 수집
        leaf_sections = self.collect_leaf_sections()
        
        # 3. 중요 섹션들의 페이지 검증
        verified_pages = self.verify_section_pages(leaf_sections)
        
        # 4. 페이지 범위 추정
        page_ranges = self.estimate_page_ranges_with_verification(leaf_sections, verified_pages)
        
        # 5. 최종 목차 생성
        enhanced_toc = self.generate_enhanced_toc(page_ranges)
        
        # 6. 결과 저장
        output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_accurate_pages_v6.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_toc)
        
        print(f"\n최종 목차가 {output_path}에 저장되었습니다.")
        print(f"검증된 섹션: {len(verified_pages)}개")
        print(f"페이지 범위 추정: {len(page_ranges)}개")
        
        # 검증 결과도 저장
        results = {
            'verified_pages': verified_pages,
            'page_ranges': page_ranges
        }
        
        results_path = "/home/nadle/projects/Knowledge_Sherpa/v2/accurate_page_mapping_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return output_path

if __name__ == "__main__":
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    chapter_mapping_path = "/home/nadle/projects/Knowledge_Sherpa/v2/chapter_page_mappings.md"
    
    mapper = AccurateTOCPageMapper(pdf_path, toc_path, chapter_mapping_path)
    result_path = mapper.run()
    print(f"\n완료! 결과: {result_path}")