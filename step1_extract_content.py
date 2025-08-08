#!/usr/bin/env python3
"""
1단계: PDF에서 내용만 추출하여 JSON으로 저장
"""

import json
import re
import pdfplumber
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentExtractor:
    def __init__(self, pdf_path: str, output_file: str):
        self.pdf_path = Path(pdf_path)
        self.output_file = Path(output_file)
        
        # 실제 PDF에서 확인된 섹션들
        self.target_sections = {
            "Summary": {"pages": [30, 50, 80, 120, 150], "pattern": "Summary"},
            "Introduction": {"pages": [17, 25, 35], "pattern": "Introduction"},
            "1.1.1 The design phase": {"pages": [32], "pattern": "1.1.1 The design phase"},
            "1.1.2 UML 101": {"pages": [10, 33], "pattern": "UML 101"},
            "1.1.3 Explaining each piece of the class diagram": {"pages": [35], "pattern": "Explaining each piece"},
            "1.1.4 The implementation phase": {"pages": [38], "pattern": "implementation phase"},
            "1.2.1 Many relations between classes": {"pages": [42], "pattern": "1.2.1 Many relations"},
            "1.2.2 Unpredictable code behavior": {"pages": [44], "pattern": "Unpredictable code"},
            "1.2.3 Not trivial data serialization": {"pages": [46], "pattern": "Not trivial data"},
            "1.2.4 Complex class hierarchies": {"pages": [48], "pattern": "Complex class"},
            "6.2.1 The tree of function calls": {"pages": [180], "pattern": "tree of function"},
            "6.2.2 Unit tests for functions down the tree": {"pages": [182], "pattern": "functions down the tree"},
            "6.2.3 Unit tests for nodes in the tree": {"pages": [184], "pattern": "nodes in the tree"},
        }
    
    def extract_content_from_pages(self, section_info: dict, section_title: str) -> str:
        """특정 섹션의 내용을 PDF에서 추출한다"""
        
        with pdfplumber.open(self.pdf_path) as pdf:
            pattern = section_info["pattern"]
            pages_to_search = section_info["pages"]
            
            for start_page in pages_to_search:
                if start_page > len(pdf.pages):
                    continue
                
                # 해당 페이지와 다음 2페이지에서 내용 찾기
                for page_offset in range(3):
                    page_idx = start_page - 1 + page_offset
                    if page_idx >= len(pdf.pages):
                        break
                    
                    page = pdf.pages[page_idx]
                    text = page.extract_text()
                    
                    if text and pattern.lower() in text.lower():
                        # 섹션 내용 추출
                        content = self._extract_section_text(text, pattern, section_title)
                        if content:
                            logger.info(f"'{section_title}' 추출 성공 (페이지 {page_idx + 1}): {len(content)} 문자")
                            return content
            
            logger.warning(f"'{section_title}' 추출 실패")
            return ""
    
    def _extract_section_text(self, page_text: str, pattern: str, section_title: str) -> str:
        """페이지 텍스트에서 섹션 내용을 추출한다"""
        lines = page_text.split('\n')
        content_lines = []
        section_started = False
        
        for line in lines:
            line = line.strip()
            
            # 섹션 시작점 찾기
            if not section_started and pattern.lower() in line.lower():
                section_started = True
                content_lines.append(line)  # 섹션 제목 포함
                continue
            
            if section_started:
                # 빈 줄이나 너무 짧은 줄 처리
                if not line:
                    content_lines.append("")
                    continue
                
                if len(line) < 3:
                    continue
                
                # 페이지 번호 스킵
                if re.match(r'^\d+$', line):
                    continue
                
                # 다음 주요 섹션이 시작되면 중단
                if (re.match(r'^\d+\.\d+', line) and 
                    line.lower() != section_title.lower() and 
                    pattern.lower() not in line.lower()):
                    break
                
                content_lines.append(line)
                
                # 충분한 내용 수집시 중단 (너무 길어지지 않도록)
                if len('\n'.join(content_lines)) > 2000:
                    break
        
        return '\n'.join(content_lines) if content_lines else ""
    
    def extract_all_sections(self) -> dict:
        """모든 대상 섹션의 내용을 추출한다"""
        logger.info(f"총 {len(self.target_sections)}개 섹션 추출 시작...")
        
        extracted_content = {}
        success_count = 0
        
        for section_title, section_info in self.target_sections.items():
            logger.info(f"추출 중: {section_title}")
            
            content = self.extract_content_from_pages(section_info, section_title)
            
            extracted_content[section_title] = {
                "title": section_title,
                "content": content,
                "length": len(content),
                "extracted_at": datetime.now().isoformat(),
                "status": "success" if content else "failed"
            }
            
            if content:
                success_count += 1
        
        logger.info(f"추출 완료: {len(self.target_sections)}개 중 {success_count}개 성공")
        return extracted_content
    
    def save_extracted_content(self, content_data: dict):
        """추출된 내용을 JSON 파일로 저장한다"""
        
        # 메타데이터 추가
        output_data = {
            "extraction_info": {
                "timestamp": datetime.now().isoformat(),
                "total_sections": len(content_data),
                "successful_extractions": len([v for v in content_data.values() if v["status"] == "success"]),
                "pdf_source": str(self.pdf_path)
            },
            "sections": content_data
        }
        
        # JSON으로 저장
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"추출 결과 저장 완료: {self.output_file}")
        
        # 요약 출력
        print(f"\n=== 추출 결과 요약 ===")
        print(f"총 섹션: {output_data['extraction_info']['total_sections']}")
        print(f"성공: {output_data['extraction_info']['successful_extractions']}")
        print(f"저장 파일: {self.output_file}")
        
        # 각 섹션 상태 출력
        print(f"\n=== 섹션별 상태 ===")
        for title, info in content_data.items():
            status_emoji = "✅" if info["status"] == "success" else "❌"
            print(f"{status_emoji} {title}: {info['length']} 문자")

def main():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extracted_content.json"
    
    extractor = ContentExtractor(pdf_path, output_file)
    
    # 내용 추출
    extracted_data = extractor.extract_all_sections()
    
    # 결과 저장
    extractor.save_extracted_content(extracted_data)
    
    print(f"\n1단계 완료! 추출된 내용이 {output_file}에 저장되었습니다.")
    print("다음은 step2_save_to_files.py를 실행하여 실제 파일들에 저장하세요.")

if __name__ == "__main__":
    main()