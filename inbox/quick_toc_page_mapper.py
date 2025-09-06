#!/usr/bin/env python3
"""
정규화된 목차에 페이지 정보를 빠르게 추가하는 간단한 도구
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class QuickTOCPageMapper:
    def __init__(self, toc_path: str, chapter_mapping_path: str):
        self.toc_path = toc_path
        self.chapter_mapping_path = chapter_mapping_path
        self.chapter_pages = {}
        
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
                # 마지막 챕터는 추후 결정
                info['end_page'] = info['start_page'] + 50
        
        self.chapter_pages = mappings
        return mappings
    
    def generate_enhanced_toc(self) -> str:
        """페이지 정보가 추가된 목차 생성"""
        print("페이지 정보가 추가된 목차 생성 중...")
        
        with open(self.toc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        enhanced_lines = []
        current_chapter = None
        current_chapter_info = None
        
        # 챕터별 기본 페이지 할당을 위한 카운터
        chapter_section_counts = {}
        
        for chapter_key, info in self.chapter_pages.items():
            chapter_section_counts[chapter_key] = {
                'total_pages': info['end_page'] - info['start_page'] + 1,
                'sections': []
            }
        
        # 첫 번째 패스: 섹션 수 카운트
        for line in lines:
            line = line.rstrip()
            if not line:
                continue
                
            # LEAF 노드인지 확인
            is_leaf = '**[LEAF]**' in line
            
            # 챕터 정보 추출
            title_match = re.search(r'^[\s-]*(.+?)\s*\(node\d+\)', line)
            if title_match:
                title = title_match.group(1).strip()
                
                # 챕터 식별
                chapter_match = re.search(r'^(\d+(?:\.\d+)*)\s+(.+)', title)
                if chapter_match:
                    chapter_num = chapter_match.group(1).split('.')[0]
                    current_chapter = f"Chapter {chapter_num}"
                elif 'Chapter' in title:
                    chapter_match = re.search(r'Chapter\s+(\d+)', title)
                    if chapter_match:
                        current_chapter = f"Chapter {chapter_match.group(1)}"
                elif re.match(r'^\d+\s+', title):
                    chapter_match = re.match(r'^(\d+)\s+', title)
                    if chapter_match:
                        current_chapter = f"Chapter {chapter_match.group(1)}"
                
                if current_chapter and current_chapter in chapter_section_counts and is_leaf:
                    chapter_section_counts[current_chapter]['sections'].append(title)
        
        # 두 번째 패스: 페이지 정보 추가
        current_chapter = None
        section_counter = 0
        
        for line_num, line in enumerate(lines):
            original_line = line.rstrip()
            if not original_line:
                enhanced_lines.append('')
                continue
            
            # LEAF 노드가 아닌 경우 그대로 추가
            if '**[LEAF]**' not in original_line:
                # 챕터나 파트 헤더의 경우 페이지 정보 추가
                if original_line.startswith('#'):
                    enhanced_lines.append(original_line)
                else:
                    enhanced_lines.append(original_line)
                continue
            
            # 제목 추출
            title_match = re.search(r'^[\s-]*(.+?)\s*\(node\d+\)', original_line)
            if not title_match:
                enhanced_lines.append(original_line)
                continue
                
            title = title_match.group(1).strip()
            
            # 챕터 식별
            chapter_match = re.search(r'^(\d+(?:\.\d+)*)\s+(.+)', title)
            if chapter_match:
                chapter_num = chapter_match.group(1).split('.')[0]
                current_chapter = f"Chapter {chapter_num}"
                section_counter = 0
            elif 'Chapter' in title:
                chapter_match = re.search(r'Chapter\s+(\d+)', title)
                if chapter_match:
                    current_chapter = f"Chapter {chapter_match.group(1)}"
                    section_counter = 0
            elif re.match(r'^\d+\s+', title):
                chapter_match = re.match(r'^(\d+)\s+', title)
                if chapter_match:
                    current_chapter = f"Chapter {chapter_match.group(1)}"
                    section_counter = 0
            
            # 페이지 정보 추가
            page_info = ""
            if current_chapter and current_chapter in self.chapter_pages:
                chapter_info = self.chapter_pages[current_chapter]
                chapter_sections = chapter_section_counts[current_chapter]['sections']
                
                if title in chapter_sections:
                    section_index = chapter_sections.index(title)
                    total_sections = len(chapter_sections)
                    
                    if total_sections > 0:
                        # 챕터 내에서 섹션의 상대적 위치 계산
                        pages_per_section = chapter_info['end_page'] - chapter_info['start_page'] + 1
                        section_start = chapter_info['start_page'] + int((section_index / total_sections) * pages_per_section)
                        
                        if section_index < total_sections - 1:
                            section_end = chapter_info['start_page'] + int(((section_index + 1) / total_sections) * pages_per_section) - 1
                        else:
                            section_end = chapter_info['end_page']
                        
                        # 최소 1페이지는 보장
                        if section_end <= section_start:
                            section_end = section_start + 1
                        
                        page_info = f" **[Pages: {section_start}-{section_end}]**"
            
            # 새 라인 생성
            enhanced_line = original_line.replace('**[LEAF]**', f'**[LEAF]**{page_info}')
            enhanced_lines.append(enhanced_line)
        
        return '\n'.join(enhanced_lines)
    
    def run(self):
        """전체 프로세스 실행"""
        print("=== 빠른 TOC 페이지 매핑 시작 ===")
        
        # 1. 챕터 매핑 정보 파싱
        chapter_mappings = self.parse_chapter_mappings()
        print(f"챕터 매핑 정보: {len(chapter_mappings)}개 챕터")
        
        # 2. 향상된 TOC 생성
        enhanced_toc = self.generate_enhanced_toc()
        
        # 3. 결과 저장
        output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_and_pages_v5.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_toc)
        
        print(f"향상된 TOC가 {output_path}에 저장되었습니다.")
        
        return output_path

if __name__ == "__main__":
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    chapter_mapping_path = "/home/nadle/projects/Knowledge_Sherpa/v2/chapter_page_mappings.md"
    
    mapper = QuickTOCPageMapper(toc_path, chapter_mapping_path)
    result_path = mapper.run()
    print(f"\n완료! 결과: {result_path}")