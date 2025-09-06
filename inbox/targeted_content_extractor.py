#!/usr/bin/env python3
"""
실제 PDF 섹션을 대상으로 하는 Content Extractor
"""

import re
import pdfplumber
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TargetedContentExtractor:
    def __init__(self, pdf_path: str, toc_structure_path: str):
        self.pdf_path = Path(pdf_path)
        self.toc_structure_path = Path(toc_structure_path)
        
        # 실제 PDF에서 발견된 주요 섹션들
        self.known_sections = {
            "Summary": {"pages": [30, 50, 80, 120], "pattern": "Summary"},
            "1.1.1 The design phase": {"pages": [32], "pattern": "1.1.1 The design phase"},
            "UML 101": {"pages": [10], "pattern": "UML 101"},
            "1.2.1 Many relations between classes": {"pages": [42], "pattern": "1.2.1 Many relations between classes"},
            "Introduction": {"pages": [17], "pattern": "Introduction"},
            "Flexibility": {"pages": [8], "pattern": "Flexibility"},
        }
    
    def extract_known_sections(self):
        """알려진 섹션들의 내용을 추출한다"""
        logger.info("알려진 섹션들 추출 시작...")
        
        results = {}
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for section_title, info in self.known_sections.items():
                logger.info(f"'{section_title}' 추출 중...")
                
                content = ""
                pattern = info["pattern"]
                start_pages = info["pages"]
                
                # 시작 페이지들에서 내용 찾기
                for start_page in start_pages:
                    if start_page <= len(pdf.pages):
                        # 해당 페이지와 다음 2페이지에서 내용 추출
                        for page_offset in range(3):
                            page_idx = start_page - 1 + page_offset
                            if page_idx < len(pdf.pages):
                                page = pdf.pages[page_idx]
                                text = page.extract_text()
                                
                                if text and pattern.lower() in text.lower():
                                    # 섹션 찾음 - 내용 추출
                                    content = self._extract_section_content(text, pattern)
                                    if content:
                                        break
                        
                        if content:
                            break
                
                results[section_title] = content
                
                if content:
                    logger.info(f"'{section_title}' 추출 성공: {len(content)} 문자")
                else:
                    logger.warning(f"'{section_title}' 추출 실패")
        
        return results
    
    def _extract_section_content(self, page_text: str, section_pattern: str) -> str:
        """페이지에서 특정 섹션의 내용을 추출한다"""
        lines = page_text.split('\n')
        content_lines = []
        section_found = False
        
        for line in lines:
            line = line.strip()
            
            # 섹션 시작점 찾기
            if not section_found and section_pattern.lower() in line.lower():
                section_found = True
                content_lines.append(f"# {section_pattern}")
                content_lines.append("")
                continue
            
            if section_found:
                # 빈 줄이나 너무 짧은 줄 스킵
                if not line or len(line) < 3:
                    continue
                
                # 페이지 번호 스킵
                if re.match(r'^\d+$', line):
                    continue
                
                # 다음 주요 섹션이 시작되면 중단
                if re.match(r'^\d+\.\d+', line) and line != section_pattern:
                    break
                
                content_lines.append(line)
                
                # 충분한 내용 수집시 중단
                if len(content_lines) > 50:
                    break
        
        return '\n'.join(content_lines) if content_lines else ""
    
    def save_sample_content(self, section_title: str, content: str):
        """샘플 내용을 파일에 저장한다"""
        # 해당하는 CONTENT 파일 찾기
        search_patterns = [
            f"*{section_title}*[CONTENT].md",
            f"*{section_title.replace(' ', '*')}*[CONTENT].md"
        ]
        
        # Summary의 경우 여러 파일이 있을 수 있음
        if section_title == "Summary":
            search_patterns.append("*Summary*[CONTENT].md")
        
        target_files = []
        for pattern in search_patterns:
            files = list(self.toc_structure_path.rglob(pattern))
            target_files.extend(files)
        
        if not target_files:
            logger.warning(f"'{section_title}'에 해당하는 [CONTENT].md 파일을 찾을 수 없음")
            return
        
        # 첫 번째 파일에 저장 (테스트용)
        target_file = target_files[0]
        
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(f"# {section_title}\n\n")
                f.write("## 추출된 내용\n\n")
                f.write(content)
                f.write(f"\n\n---\n\n**추출 완료**: {len(content)} 문자\n")
                f.write(f"**파일**: {target_file.name}\n")
            
            logger.info(f"내용 저장 완료: {target_file}")
            
        except Exception as e:
            logger.error(f"파일 저장 실패: {e}")
    
    def process_all_known_sections(self):
        """모든 알려진 섹션들을 처리하고 저장한다"""
        logger.info("=== 알려진 섹션들 처리 시작 ===")
        
        # 내용 추출
        results = self.extract_known_sections()
        
        # 결과 저장
        success_count = 0
        for section_title, content in results.items():
            if content:
                self.save_sample_content(section_title, content)
                success_count += 1
            
        logger.info(f"처리 완료: {len(results)}개 중 {success_count}개 성공")
        
        # 결과 미리보기
        print("\n=== 추출된 내용 미리보기 ===")
        for section_title, content in results.items():
            print(f"\n[{section_title}]")
            if content:
                preview = content[:200] + "..." if len(content) > 200 else content
                print(preview)
            else:
                print("추출 실패")

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_structure_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    extractor = TargetedContentExtractor(pdf_path, toc_structure_path)
    extractor.process_all_known_sections()

if __name__ == "__main__":
    main()