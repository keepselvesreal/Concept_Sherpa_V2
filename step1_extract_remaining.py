#!/usr/bin/env python3
"""
나머지 3개 섹션을 추출하여 기존 JSON에 추가
"""

import json
import re
import pdfplumber
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_remaining_sections():
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    json_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extracted_content.json"
    
    # 누락된 섹션들 (정확한 페이지 정보 포함)
    remaining_sections = {
        "6.2.1 The tree of function calls": {"pages": [141], "pattern": "6.2.1 The tree of function calls"},
        "6.2.2 Unit tests for functions down the tree": {"pages": [143], "pattern": "6.2.2 Unit tests for functions down the tree"},
        "6.2.3 Unit tests for nodes in the tree": {"pages": [147], "pattern": "6.2.3 Unit tests for nodes in the tree"}
    }
    
    # 기존 JSON 로드
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"기존 데이터 로드: {len(data['sections'])}개 섹션")
    
    # 새로운 섹션 추출
    new_extractions = {}
    success_count = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        for section_title, section_info in remaining_sections.items():
            logger.info(f"추출 중: {section_title}")
            
            pattern = section_info["pattern"]
            pages = section_info["pages"]
            
            content = ""
            
            for start_page in pages:
                if start_page > len(pdf.pages):
                    continue
                
                # 해당 페이지와 다음 2페이지에서 내용 추출
                for page_offset in range(3):
                    page_idx = start_page - 1 + page_offset
                    if page_idx >= len(pdf.pages):
                        break
                    
                    page = pdf.pages[page_idx]
                    text = page.extract_text()
                    
                    if text and pattern.lower() in text.lower():
                        # 섹션 내용 추출
                        content = extract_section_text(text, pattern, section_title)
                        if content:
                            logger.info(f"'{section_title}' 추출 성공 (페이지 {page_idx + 1}): {len(content)} 문자")
                            break
                
                if content:
                    break
            
            # 결과 저장
            new_extractions[section_title] = {
                "title": section_title,
                "content": content,
                "length": len(content),
                "extracted_at": datetime.now().isoformat(),
                "status": "success" if content else "failed"
            }
            
            if content:
                success_count += 1
            else:
                logger.warning(f"'{section_title}' 추출 실패")
    
    # 기존 데이터에 추가
    data["sections"].update(new_extractions)
    data["extraction_info"]["total_sections"] = len(data["sections"])
    data["extraction_info"]["successful_extractions"] = len([v for v in data["sections"].values() if v["status"] == "success"])
    data["extraction_info"]["last_updated"] = datetime.now().isoformat()
    
    # 업데이트된 데이터 저장
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"업데이트 완료: {json_file}")
    
    print(f"\n=== 추가 추출 결과 ===")
    print(f"새로 추출된 섹션: {len(remaining_sections)}개 중 {success_count}개 성공")
    print(f"전체: {data['extraction_info']['total_sections']}개 중 {data['extraction_info']['successful_extractions']}개 성공")
    
    for title, info in new_extractions.items():
        status_emoji = "✅" if info["status"] == "success" else "❌"
        print(f"{status_emoji} {title}: {info['length']} 문자")

def extract_section_text(page_text: str, pattern: str, section_title: str) -> str:
    """페이지 텍스트에서 섹션 내용을 추출한다"""
    lines = page_text.split('\n')
    content_lines = []
    section_started = False
    
    for line in lines:
        line = line.strip()
        
        # 섹션 시작점 찾기
        if not section_started and pattern.lower() in line.lower():
            section_started = True
            content_lines.append(line)
            continue
        
        if section_started:
            # 빈 줄 처리
            if not line:
                content_lines.append("")
                continue
            
            if len(line) < 3:
                continue
            
            # 페이지 번호 스킵
            if re.match(r'^\d+$', line):
                continue
            
            # 다음 주요 섹션이 시작되면 중단 (6.2.4나 6.3 등)
            if re.match(r'^6\.\d+', line) and line.lower() != section_title.lower():
                break
            
            # Chapter 헤더가 나오면 중단
            if "CHAPTER" in line.upper():
                break
            
            content_lines.append(line)
            
            # 충분한 내용 수집시 중단
            if len('\n'.join(content_lines)) > 2000:
                break
    
    return '\n'.join(content_lines) if content_lines else ""

if __name__ == "__main__":
    extract_remaining_sections()