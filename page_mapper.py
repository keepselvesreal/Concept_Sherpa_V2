#!/usr/bin/env python3
import pdfplumber
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class PageMapper:
    def __init__(self, pdf_path: str, toc_path: str):
        self.pdf_path = pdf_path
        self.toc_path = toc_path
        self.page_mappings = {}
        
    def find_section_pages(self) -> Dict[str, int]:
        """PDF에서 각 섹션의 시작 페이지를 찾기"""
        print("PDF에서 섹션 시작 페이지 매핑 중...")
        
        # 찾을 섹션 패턴들 정의
        section_patterns = {
            # Part 1 - Flexibility
            "Part 1": [r"Part\s+1", r"PART\s+1.*FLEXIBILITY"],
            "Chapter 1": [r"1\s+Complexity\s+of\s+object-oriented\s+programming", r"Complexity\s+of\s+object-\s*oriented\s+programming"],
            "Chapter 2": [r"2\s+Separation\s+between\s+code\s+and\s+data", r"Separation\s+between\s+code\s+and\s+data"],
            "Chapter 3": [r"3\s+Basic\s+data\s+manipulation", r"Basic\s+data\s+manipulation"],
            "Chapter 4": [r"4\s+State\s+management", r"State\s+management"],
            "Chapter 5": [r"5\s+Basic\s+concurrency\s+control", r"Basic\s+concurrency\s+control"],
            "Chapter 6": [r"6\s+Unit\s+tests", r"Unit\s+tests"],
            
            # Part 2 - Scalability  
            "Part 2": [r"Part\s+2", r"PART\s+2.*SCALABILITY"],
            "Chapter 7": [r"7\s+Basic\s+data\s+validation", r"Basic\s+data\s+validation"],
            "Chapter 8": [r"8\s+Advanced\s+concurrency\s+control", r"Advanced\s+concurrency\s+control"],
            "Chapter 9": [r"9\s+Persistent\s+data\s+structures", r"Persistent\s+data\s+structures"],
            "Chapter 10": [r"10\s+Database\s+operations", r"Database\s+operations"],
            "Chapter 11": [r"11\s+Web\s+services", r"Web\s+services"],
            
            # Part 3 - Maintainability
            "Part 3": [r"Part\s+3", r"PART\s+3.*MAINTAINABILITY"],
            "Chapter 12": [r"12\s+Advanced\s+data\s+validation", r"Advanced\s+data\s+validation"],
            "Chapter 13": [r"13\s+Polymorphism", r"Polymorphism"],
            "Chapter 14": [r"14\s+Advanced\s+data\s+manipulation", r"Advanced\s+data\s+manipulation"],
            "Chapter 15": [r"15\s+Debugging", r"Debugging"],
            
            # Appendices
            "Appendix A": [r"appendix\s+A", r"Principles\s+of\s+data-oriented\s+programming"],
            "Appendix B": [r"appendix\s+B", r"Generic\s+data\s+access\s+in\s+statically-typed\s+languages"],
            "Appendix C": [r"appendix\s+C", r"Data-oriented\s+programming:\s+A\s+link\s+in\s+the\s+chain"],
            "Appendix D": [r"appendix\s+D", r"Lodash\s+reference"],
        }
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"총 {total_pages}페이지 검색 중...")
            
            for page_num in range(total_pages):
                page = pdf.pages[page_num]
                text = page.extract_text() or ""
                
                # 각 섹션 패턴 확인
                for section_name, patterns in section_patterns.items():
                    if section_name not in self.page_mappings:
                        for pattern in patterns:
                            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                                # 실제 내용인지 확인 (목차나 헤더가 아닌)
                                if self._is_actual_content(text, section_name):
                                    self.page_mappings[section_name] = page_num + 1
                                    print(f"  {section_name}: 페이지 {page_num + 1}")
                                    break
                
                # 진행상황 표시
                if (page_num + 1) % 50 == 0:
                    print(f"  진행: {page_num + 1}/{total_pages} 페이지")
        
        return self.page_mappings
    
    def _is_actual_content(self, text: str, section_name: str) -> bool:
        """실제 내용인지 확인 (목차나 헤더가 아닌)"""
        # 목차 패턴 제외
        if re.search(r"contents|table\s+of\s+contents", text, re.IGNORECASE):
            return False
        
        # 헤더/푸터만 있는 경우 제외
        if len(text.strip()) < 100:
            return False
        
        # 챕터의 경우 충분한 내용이 있는지 확인
        if "Chapter" in section_name:
            # "This chapter covers" 등의 실제 챕터 시작 문구가 있는지 확인
            chapter_indicators = [
                r"This\s+chapter\s+covers",
                r"In\s+this\s+chapter",
                r"This\s+chapter\s+is\s+about",
                r"chapter\s+covers"
            ]
            for indicator in chapter_indicators:
                if re.search(indicator, text, re.IGNORECASE):
                    return True
            
            # 또는 충분한 양의 텍스트가 있는지 확인
            return len(text.strip()) > 500
        
        # Part의 경우
        if "Part" in section_name:
            return len(text.strip()) > 200
        
        # Appendix의 경우
        if "Appendix" in section_name:
            return len(text.strip()) > 300
        
        return True
    
    def generate_page_mapping_report(self) -> str:
        """페이지 매핑 보고서 생성"""
        if not self.page_mappings:
            self.find_section_pages()
        
        report = "# PDF 페이지 매핑 보고서\n\n"
        report += f"**PDF 파일**: {self.pdf_path}\n"
        report += f"**분석 일시**: {Path().absolute()}\n\n"
        
        # Part별로 정리
        parts = {
            "Front Matter": [],
            "Part 1 - Flexibility": [],
            "Part 2 - Scalability": [], 
            "Part 3 - Maintainability": [],
            "Appendices": []
        }
        
        for section, page in sorted(self.page_mappings.items(), key=lambda x: x[1]):
            if "Part 1" in section or any(f"Chapter {i}" in section for i in range(1, 7)):
                parts["Part 1 - Flexibility"].append((section, page))
            elif "Part 2" in section or any(f"Chapter {i}" in section for i in range(7, 12)):
                parts["Part 2 - Scalability"].append((section, page))
            elif "Part 3" in section or any(f"Chapter {i}" in section for i in range(12, 16)):
                parts["Part 3 - Maintainability"].append((section, page))
            elif "Appendix" in section:
                parts["Appendices"].append((section, page))
        
        for part_name, sections in parts.items():
            if sections:
                report += f"## {part_name}\n\n"
                for section, page in sections:
                    report += f"- **{section}**: 페이지 {page}\n"
                report += "\n"
        
        # 찾지 못한 섹션들
        expected_sections = [
            "Part 1", "Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5", "Chapter 6",
            "Part 2", "Chapter 7", "Chapter 8", "Chapter 9", "Chapter 10", "Chapter 11", 
            "Part 3", "Chapter 12", "Chapter 13", "Chapter 14", "Chapter 15",
            "Appendix A", "Appendix B", "Appendix C", "Appendix D"
        ]
        
        missing_sections = [s for s in expected_sections if s not in self.page_mappings]
        if missing_sections:
            report += "## 발견되지 않은 섹션\n\n"
            for section in missing_sections:
                report += f"- {section}\n"
            report += "\n"
        
        return report
    
    def save_mapping_report(self, output_path: str = "page_mapping_report.md"):
        """매핑 보고서를 파일로 저장"""
        report = self.generate_page_mapping_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"페이지 매핑 보고서 저장: {output_path}")

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_TOC.md"
    
    mapper = PageMapper(pdf_path, toc_path)
    mappings = mapper.find_section_pages()
    
    print(f"\n=== 발견된 섹션 페이지 매핑 ===")
    for section, page in sorted(mappings.items(), key=lambda x: x[1]):
        print(f"{section}: 페이지 {page}")
    
    # 보고서 저장
    mapper.save_mapping_report()

if __name__ == "__main__":
    main()