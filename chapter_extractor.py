#!/usr/bin/env python3
import pdfplumber
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class ChapterExtractor:
    def __init__(self, pdf_path: str, output_dir: str = "extracted_content"):
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.chapter_content = {}
        
    def extract_chapter_1(self) -> Dict[str, any]:
        """1장 'Complexity of object-oriented programming' 추출"""
        print("PDF에서 1장 텍스트 추출 중...")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            chapter_text = ""
            chapter_start_page = None
            chapter_end_page = None
            
            # 1장은 31페이지부터 시작하는 것을 확인했음
            # PDF 탐색 결과를 바탕으로 직접 페이지 범위 설정
            for page_num in range(30, min(80, len(pdf.pages))):  # 31-80페이지 범위에서 검색
                page = pdf.pages[page_num]
                text = page.extract_text() or ""
                
                # 1장 시작 감지 
                if not chapter_start_page and self._is_actual_chapter_1_start(text):
                    chapter_start_page = page_num
                    print(f"1장 시작 페이지 발견: {page_num + 1}")
                    print(f"페이지 내용 미리보기: {text[:200]}...")
                
                # 1장 끝 감지 (2장 시작)
                if chapter_start_page and not chapter_end_page:
                    if self._is_chapter_1_end(text):
                        chapter_end_page = page_num
                        print(f"1장 끝 페이지 발견: {page_num + 1}")
                        break
            
            # 페이지 범위가 확정되면 텍스트 추출
            if chapter_start_page is not None:
                end_page = chapter_end_page or min(chapter_start_page + 25, len(pdf.pages) - 1)
                
                for page_num in range(chapter_start_page, end_page + 1):
                    page_text = pdf.pages[page_num].extract_text() or ""
                    chapter_text += f"=== PAGE {page_num + 1} ===\n{page_text}\n\n"
                    
                print(f"1장 텍스트 추출 완료: {chapter_start_page + 1}-{end_page + 1}페이지")
            
            return {
                "chapter_number": 1,
                "title": "Complexity of object-oriented programming",
                "start_page": chapter_start_page + 1 if chapter_start_page else None,
                "end_page": (chapter_end_page or end_page) + 1 if chapter_start_page else None,
                "full_text": chapter_text.strip(),
                "sections": self._parse_sections(chapter_text)
            }
    
    def _is_actual_chapter_1_start(self, text: str) -> bool:
        """실제 1장 내용 시작 감지"""
        # 31페이지 패턴: "Complexity of object-oriented programming" 제목으로 시작
        patterns = [
            r"Complexity\s+of\s+object-\s*oriented\s+programming",
            r"A\s+capricious\s+entrepreneur",  # 31페이지 부제목
            r"This\s+chapter\s+covers"  # 31페이지 내용
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # 목차가 아닌 실제 내용인지 확인 - 충분한 텍스트가 있어야 함
                if len(text.strip()) > 800:
                    return True
        return False
    
    def _is_chapter_1_start(self, text: str) -> bool:
        """1장 시작 페이지 감지"""
        patterns = [
            r"1\s+Complexity\s+of\s+object-oriented\s+programming",
            r"Chapter\s+1.*Complexity.*object-oriented",
            r"1\..*Complexity.*of.*object-oriented.*programming",
            r"^\s*1\s*$.*complexity.*object.*oriented",  # 숫자 1만 있는 경우
            r"complexity\s+of\s+object-oriented\s+programming",  # 제목만 있는 경우
        ]
        
        # 실제 챕터 내용인지 확인 (목차가 아닌)
        content_indicators = [
            r"OOP\s+design",
            r"Sources\s+of\s+complexity", 
            r"1\.1\s+OOP",
            r"1\.2\s+Sources"
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                # 목차가 아닌 실제 내용인지 확인
                for content_pattern in content_indicators:
                    if re.search(content_pattern, text, re.IGNORECASE):
                        return True
                # 또는 충분한 양의 텍스트가 있는지 확인
                if len(text.strip()) > 500:  # 목차 페이지보다 내용이 많음
                    return True
        return False
    
    def _is_chapter_1_end(self, text: str) -> bool:
        """1장 끝 페이지 감지"""
        patterns = [
            r"2\s+Separation\s+between\s+code\s+and\s+data",
            r"Chapter\s+2",
            r"^\s*2\s*$",  # 숫자 2만 있는 경우
            r"Separation\s+between\s+code\s+and\s+data",  # 2장 제목
            r"Summary\s*\n.*2\s+"  # Summary 다음에 2가 나오는 경우
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                return True
        return False
    
    def _parse_sections(self, chapter_text: str) -> Dict[str, any]:
        """1장 내의 섹션들을 파싱"""
        sections = {}
        
        # 1.1과 1.2 섹션 분리
        section_patterns = {
            "1.1": r"1\.1\s+OOP\s+design:\s+Classic\s+or\s+classical\?",
            "1.2": r"1\.2\s+Sources\s+of\s+complexity"
        }
        
        # 하위 섹션 패턴
        subsection_patterns = {
            "1.1.1": r"1\.1\.1\s+The\s+design\s+phase",
            "1.1.2": r"1\.1\.2\s+UML\s+101",
            "1.1.3": r"1\.1\.3\s+Explaining\s+each\s+piece\s+of\s+the\s+class\s+diagram",
            "1.1.4": r"1\.1\.4\s+The\s+implementation\s+phase",
            "1.2.1": r"1\.2\.1\s+Many\s+relations\s+between\s+classes",
            "1.2.2": r"1\.2\.2\s+Unpredictable\s+code\s+behavior",
            "1.2.3": r"1\.2\.3\s+Not\s+trivial\s+data\s+serialization",
            "1.2.4": r"1\.2\.4\s+Complex\s+class\s+hierarchies"
        }
        
        # 섹션별 텍스트 추출
        text_positions = []
        
        # 모든 패턴의 위치 찾기
        all_patterns = {**section_patterns, **subsection_patterns}
        for section_id, pattern in all_patterns.items():
            match = re.search(pattern, chapter_text, re.IGNORECASE)
            if match:
                text_positions.append((match.start(), section_id, pattern))
        
        # 위치순으로 정렬
        text_positions.sort()
        
        # 각 섹션의 텍스트 추출
        for i, (start_pos, section_id, pattern) in enumerate(text_positions):
            # 다음 섹션까지의 텍스트 또는 끝까지
            if i + 1 < len(text_positions):
                end_pos = text_positions[i + 1][0]
                section_text = chapter_text[start_pos:end_pos].strip()
            else:
                section_text = chapter_text[start_pos:].strip()
            
            sections[section_id] = {
                "title": self._extract_section_title(section_text),
                "content": section_text
            }
        
        return sections
    
    def _extract_section_title(self, section_text: str) -> str:
        """섹션 텍스트에서 제목 추출"""
        lines = section_text.split('\n')
        for line in lines[:3]:  # 처음 3줄에서 제목 찾기
            line = line.strip()
            if re.match(r'^\d+\.\d*\s+', line):
                return line
        return lines[0].strip() if lines else ""
    
    def save_extracted_content(self, chapter_data: Dict[str, any]) -> None:
        """추출된 내용을 파일로 저장"""
        chapter_dir = self.output_dir / "chapter1"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        # 1장 전체 원본 텍스트 저장
        with open(chapter_dir / "raw_text.md", "w", encoding="utf-8") as f:
            f.write(f"# Chapter 1: {chapter_data['title']}\n\n")
            f.write(f"**페이지:** {chapter_data['start_page']}-{chapter_data['end_page']}\n\n")
            f.write(chapter_data['full_text'])
        
        # 섹션별 저장
        for section_id, section_data in chapter_data['sections'].items():
            # 메인 섹션 (1.1, 1.2)인지 하위 섹션인지 구분
            if len(section_id.split('.')) == 2:  # 1.1, 1.2
                section_dir = chapter_dir / f"section_{section_id.replace('.', '_')}"
                section_dir.mkdir(exist_ok=True)
                
                with open(section_dir / "section_overview.md", "w", encoding="utf-8") as f:
                    f.write(f"# {section_data['title']}\n\n")
                    f.write(section_data['content'])
            
            else:  # 1.1.1, 1.1.2 등 하위 섹션
                parent_section = '.'.join(section_id.split('.')[:2])  # 1.1 또는 1.2
                section_dir = chapter_dir / f"section_{parent_section.replace('.', '_')}"
                section_dir.mkdir(exist_ok=True)
                
                filename = f"subsection_{section_id.replace('.', '_')}.md"
                with open(section_dir / filename, "w", encoding="utf-8") as f:
                    f.write(f"# {section_data['title']}\n\n")
                    f.write(section_data['content'])
        
        # 메타데이터 저장
        metadata = {
            "chapter": chapter_data['chapter_number'],
            "title": chapter_data['title'],
            "page_range": f"{chapter_data['start_page']}-{chapter_data['end_page']}",
            "sections_found": list(chapter_data['sections'].keys()),
            "extraction_timestamp": str(Path().absolute())
        }
        
        with open(chapter_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"추출 완료: {chapter_dir}")
        print(f"발견된 섹션: {list(chapter_data['sections'].keys())}")

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    extractor = ChapterExtractor(pdf_path)
    
    # 1장 추출
    chapter_1_data = extractor.extract_chapter_1()
    
    if chapter_1_data['full_text']:
        extractor.save_extracted_content(chapter_1_data)
        print("1장 추출 및 저장 완료!")
    else:
        print("1장을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()