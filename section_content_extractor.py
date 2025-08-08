#!/usr/bin/env python3
"""
페이지 정보가 포함된 목차를 기반으로 PDF에서 섹션별 내용을 추출하고 폴더 구조로 저장
"""

import pdfplumber
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

class SectionContentExtractor:
    def __init__(self, pdf_path: str, toc_path: str, output_base_dir: str):
        self.pdf_path = pdf_path
        self.toc_path = toc_path
        self.output_base_dir = output_base_dir
        self.extracted_sections = {}
        self.extraction_stats = {
            'total_sections': 0,
            'extracted_successfully': 0,
            'extraction_failed': 0,
            'start_time': None,
            'end_time': None
        }
        
    def parse_toc_with_pages(self) -> List[Dict]:
        """페이지 정보가 포함된 목차 파싱"""
        print("페이지 정보가 포함된 목차 파싱 중...")
        
        with open(self.toc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        sections = []
        current_hierarchy = []
        
        for line_num, line in enumerate(lines):
            line = line.rstrip()
            if not line:
                continue
            
            # LEAF 노드만 처리
            if '**[LEAF]**' not in line:
                # 계층 구조 추적을 위해 헤더 정보 저장
                if line.startswith('#'):
                    header_level = len(line) - len(line.lstrip('#'))
                    header_title = line.lstrip('#').strip()
                    # 현재 레벨 이하의 계층 정보 제거
                    current_hierarchy = current_hierarchy[:header_level-1]
                    current_hierarchy.append(header_title)
                continue
            
            # 들여쓰기 레벨 계산
            indent_level = (len(line) - len(line.lstrip())) // 2
            
            # 제목과 페이지 정보 추출
            title_match = re.search(r'^[\s-]*(.+?)\s*\(node\d+\)\s*\*\*\[LEAF\]\*\*(?:\s*\*\*\[Pages?:\s*(\d+)(?:-(\d+))?\]\*\*)?', line)
            
            if title_match:
                title = title_match.group(1).strip()
                start_page = title_match.group(2)
                end_page = title_match.group(3)
                
                if start_page:
                    start_page = int(start_page)
                    end_page = int(end_page) if end_page else start_page
                    
                    # 계층 구조 정보 생성
                    hierarchy_path = current_hierarchy.copy()
                    
                    # 챕터 정보 추출
                    chapter_match = re.search(r'^(\d+(?:\.\d+)*)\s+(.+)', title)
                    if chapter_match:
                        chapter_num = chapter_match.group(1).split('.')[0]
                        chapter_title = f"Chapter {chapter_num}"
                        if chapter_title not in hierarchy_path:
                            hierarchy_path.append(chapter_title)
                    
                    # 폴더 경로 생성
                    folder_path = self._generate_folder_path(title, hierarchy_path, indent_level)
                    
                    sections.append({
                        'title': title,
                        'start_page': start_page,
                        'end_page': end_page,
                        'indent_level': indent_level,
                        'hierarchy': hierarchy_path,
                        'folder_path': folder_path,
                        'line_num': line_num,
                        'original_line': line
                    })
        
        print(f"파싱 완료: {len(sections)}개 섹션")
        self.extraction_stats['total_sections'] = len(sections)
        return sections
    
    def _generate_folder_path(self, title: str, hierarchy: List[str], indent_level: int) -> str:
        """섹션 제목과 계층에 따른 폴더 경로 생성"""
        path_parts = []
        
        # 기본 폴더 구조
        path_parts.append("extracted_sections_with_pages")
        
        # 계층 구조 추가
        for level, item in enumerate(hierarchy):
            safe_name = self._sanitize_folder_name(item)
            path_parts.append(safe_name)
        
        # 섹션별 폴더
        safe_title = self._sanitize_folder_name(title)
        path_parts.append(safe_title)
        
        return "/".join(path_parts)
    
    def _sanitize_folder_name(self, name: str) -> str:
        """폴더명에서 특수문자 제거"""
        # 특수문자를 언더스코어로 변경
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # 연속된 공백을 언더스코어로
        sanitized = re.sub(r'\s+', '_', sanitized)
        # 길이 제한 (80자)
        if len(sanitized) > 80:
            sanitized = sanitized[:77] + "..."
        return sanitized.strip('_')
    
    def extract_section_content(self, section: Dict) -> Optional[str]:
        """PDF에서 특정 섹션 내용 추출"""
        start_page = section['start_page']
        end_page = section['end_page']
        title = section['title']
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                content_parts = []
                
                for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
                    page = pdf.pages[page_num]
                    text = page.extract_text()
                    
                    if text:
                        # 페이지 헤더 추가
                        content_parts.append(f"\n--- 페이지 {page_num + 1} ---\n")
                        content_parts.append(text)
                        content_parts.append(f"\n--- 페이지 {page_num + 1} 끝 ---\n")
                
                if content_parts:
                    full_content = "\n".join(content_parts)
                    return full_content
                    
        except Exception as e:
            print(f"내용 추출 실패 ({title}): {e}")
            return None
        
        return None
    
    def create_folder_structure(self, sections: List[Dict]):
        """폴더 구조 생성"""
        print("폴더 구조 생성 중...")
        
        created_folders = set()
        
        for section in sections:
            folder_path = os.path.join(self.output_base_dir, section['folder_path'])
            
            if folder_path not in created_folders:
                os.makedirs(folder_path, exist_ok=True)
                created_folders.add(folder_path)
        
        print(f"생성된 폴더: {len(created_folders)}개")
        return created_folders
    
    def extract_and_save_sections(self, sections: List[Dict]):
        """섹션별 내용 추출 및 저장"""
        print(f"섹션별 내용 추출 시작 ({len(sections)}개)...")
        
        self.extraction_stats['start_time'] = datetime.now()
        
        for i, section in enumerate(sections):
            title = section['title']
            print(f"  [{i+1}/{len(sections)}] {title} 추출 중...")
            
            # 내용 추출
            content = self.extract_section_content(section)
            
            if content:
                # 파일 저장
                folder_path = os.path.join(self.output_base_dir, section['folder_path'])
                safe_filename = self._sanitize_folder_name(title) + "_content.md"
                file_path = os.path.join(folder_path, safe_filename)
                
                # 메타데이터와 함께 저장
                full_content = self._create_section_file_content(section, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                # 메타데이터 파일도 저장
                metadata_path = os.path.join(folder_path, "metadata.json")
                metadata = {
                    'title': section['title'],
                    'start_page': section['start_page'],
                    'end_page': section['end_page'],
                    'indent_level': section['indent_level'],
                    'hierarchy': section['hierarchy'],
                    'extraction_time': datetime.now().isoformat(),
                    'content_length': len(content),
                    'file_path': file_path
                }
                
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                self.extracted_sections[title] = {
                    'file_path': file_path,
                    'metadata': metadata,
                    'content_preview': content[:200] + "..." if len(content) > 200 else content
                }
                
                self.extraction_stats['extracted_successfully'] += 1
                print(f"    → 저장 완료: {file_path}")
            else:
                print(f"    → 추출 실패")
                self.extraction_stats['extraction_failed'] += 1
        
        self.extraction_stats['end_time'] = datetime.now()
    
    def _create_section_file_content(self, section: Dict, content: str) -> str:
        """섹션 파일 내용 생성"""
        header = f"""# {section['title']}

**페이지**: {section['start_page']}-{section['end_page']}
**계층**: {' > '.join(section['hierarchy'])}
**추출 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        return header + content
    
    def generate_extraction_report(self) -> str:
        """추출 결과 보고서 생성"""
        print("추출 결과 보고서 생성 중...")
        
        duration = None
        if self.extraction_stats['start_time'] and self.extraction_stats['end_time']:
            duration = self.extraction_stats['end_time'] - self.extraction_stats['start_time']
        
        report = f"""# 섹션 내용 추출 보고서

**추출 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**소요 시간**: {duration}

## 추출 통계

- **총 섹션 수**: {self.extraction_stats['total_sections']}
- **성공적으로 추출**: {self.extraction_stats['extracted_successfully']}
- **추출 실패**: {self.extraction_stats['extraction_failed']}
- **성공률**: {(self.extraction_stats['extracted_successfully'] / self.extraction_stats['total_sections'] * 100):.1f}%

## 추출된 섹션 목록

"""
        
        for title, info in self.extracted_sections.items():
            report += f"### {title}\n"
            report += f"- **파일 경로**: `{info['file_path']}`\n"
            report += f"- **페이지**: {info['metadata']['start_page']}-{info['metadata']['end_page']}\n"
            report += f"- **내용 길이**: {info['metadata']['content_length']:,} 문자\n"
            report += f"- **미리보기**: {info['content_preview']}\n\n"
        
        # 보고서 저장
        report_path = os.path.join(self.output_base_dir, "extraction_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"보고서 저장: {report_path}")
        return report_path
    
    def run(self):
        """전체 추출 프로세스 실행"""
        print("=== 섹션 내용 추출 시작 ===")
        
        # 1. 목차 파싱
        sections = self.parse_toc_with_pages()
        
        # 2. 폴더 구조 생성
        self.create_folder_structure(sections)
        
        # 3. 내용 추출 및 저장
        self.extract_and_save_sections(sections)
        
        # 4. 보고서 생성
        report_path = self.generate_extraction_report()
        
        print(f"\n=== 추출 완료 ===")
        print(f"성공: {self.extraction_stats['extracted_successfully']}/{self.extraction_stats['total_sections']}")
        print(f"보고서: {report_path}")
        
        return {
            'extracted_sections': self.extracted_sections,
            'stats': self.extraction_stats,
            'report_path': report_path
        }

if __name__ == "__main__":
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_accurate_pages_v6.md"
    output_base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    extractor = SectionContentExtractor(pdf_path, toc_path, output_base_dir)
    result = extractor.run()
    
    print(f"\n추출 결과:")
    print(f"- 성공: {result['stats']['extracted_successfully']}개")
    print(f"- 실패: {result['stats']['extraction_failed']}개")
    print(f"- 보고서: {result['report_path']}")