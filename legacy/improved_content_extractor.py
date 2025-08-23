#!/usr/bin/env python3
"""
개선된 Leaf Node Content Extractor
PDF에서 TOC leaf node들의 실제 내용을 추출하여 TOC_Structure에 저장하는 스크립트
"""

import re
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImprovedContentExtractor:
    def __init__(self, toc_file_path: str, pdf_file_path: str, toc_structure_path: str):
        self.toc_file_path = Path(toc_file_path)
        self.pdf_file_path = Path(pdf_file_path)
        self.toc_structure_path = Path(toc_structure_path)
        self.nodes = {}
        self.leaf_nodes = []
        
    def parse_toc_structure(self) -> Dict:
        """TOC 파일을 파싱해서 구조를 분석하고 leaf node들을 찾는다"""
        logger.info("TOC 구조 파싱 시작...")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        nodes = {}
        ordered_nodes = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line.rstrip()
            
            if not line.strip() or line.strip().startswith('#'):
                continue
                
            # [LEAF] 태그가 있는 라인만 처리
            if '**[LEAF]**' not in line:
                continue
                
            # 노드 정보 추출
            node_match = re.search(r'\(node(\d+)\)', line)
            if not node_match:
                continue
                
            node_type = int(node_match.group(1))
            
            # 들여쓰기 레벨 계산
            stripped_line = line.lstrip()
            indent_level = len(line) - len(stripped_line)
            
            # 제목 추출 (- 와 **[LEAF]** 태그 제거)
            title_part = stripped_line.lstrip('- ')
            title = re.sub(r'\s*\(node\d+\).*$', '', title_part).strip()
            
            node_info = {
                'line_num': line_num,
                'title': title,
                'node_type': node_type,
                'indent_level': indent_level,
                'original_line': original_line,
                'is_leaf': True
            }
            
            node_id = f"line_{line_num}"
            nodes[node_id] = node_info
            ordered_nodes.append((node_id, node_info))
        
        self.nodes = nodes
        self.leaf_nodes = [{'node_id': nid, **info} for nid, info in nodes.items()]
        
        logger.info(f"Leaf 노드 수: {len(self.leaf_nodes)}")
        return nodes
    
    def extract_content_from_pdf(self, section_title: str) -> str:
        """PDF에서 특정 섹션의 내용을 추출한다"""
        logger.info(f"PDF에서 '{section_title}' 섹션 내용 추출 중...")
        
        try:
            with pdfplumber.open(self.pdf_file_path) as pdf:
                content = ""
                found_section = False
                section_start_page = None
                
                # 정확한 섹션 제목으로 검색
                search_patterns = [
                    section_title,
                    section_title.replace(" (사용자 추가)", ""),
                    re.sub(r'\d+\.\d+\.\d+', '', section_title).strip(),
                    re.sub(r'\d+\.\d+', '', section_title).strip(),
                    re.sub(r'\d+', '', section_title).strip()
                ]
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # 섹션 제목 찾기
                    if not found_section:
                        for pattern in search_patterns:
                            if pattern.strip() and pattern.lower() in text.lower():
                                found_section = True
                                section_start_page = page_num
                                logger.info(f"'{pattern}' 패턴이 {page_num}페이지에서 발견됨")
                                break
                    
                    if found_section:
                        content += text + "\n"
                        
                        # 충분한 내용을 수집했으면 중단 (최대 3페이지)
                        if section_start_page and (page_num - section_start_page) >= 2:
                            break
                
                # 내용 정리
                if content:
                    # 불필요한 헤더/푸터 제거
                    content = self._clean_extracted_content(content, section_title)
                
                if not content:
                    logger.warning(f"'{section_title}' 섹션의 내용을 찾을 수 없습니다.")
                    return ""
                
                logger.info(f"추출된 내용 길이: {len(content)} 문자")
                return content.strip()
                
        except Exception as e:
            logger.error(f"PDF 내용 추출 중 오류 발생: {e}")
            return ""
    
    def _clean_extracted_content(self, content: str, section_title: str) -> str:
        """추출된 내용을 정리한다"""
        lines = content.split('\n')
        cleaned_lines = []
        
        # 섹션 시작점 찾기
        section_started = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 페이지 번호나 헤더/푸터 제거
            if re.match(r'^\d+$', line) or len(line) < 3:
                continue
            
            # 섹션 제목을 찾으면 시작
            if not section_started and section_title.lower() in line.lower():
                section_started = True
                cleaned_lines.append(f"# {section_title}")
                cleaned_lines.append("")
                continue
            
            if section_started:
                # 다음 주요 섹션이 시작되면 중단
                if re.match(r'^\d+\.\d+', line) and line not in section_title:
                    break
                    
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def find_content_file_path(self, title: str, node_type: int) -> Optional[Path]:
        """제목과 노드 타입을 기반으로 해당 [CONTENT].md 파일 경로를 찾는다"""
        
        # 제목 정리 (파일명에 사용할 수 있도록)
        clean_title = title.replace(" (사용자 추가)", "")
        clean_title = re.sub(r'[^\w\s\-\.]', ' ', clean_title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        
        # TOC_Structure에서 해당 파일 찾기
        search_patterns = [
            f"{clean_title} [CONTENT].md",
            f"{clean_title}[CONTENT].md",
            f"*{clean_title}*[CONTENT].md"
        ]
        
        for pattern in search_patterns:
            files = list(self.toc_structure_path.rglob(pattern))
            if files:
                return files[0]
        
        # 더 유연한 검색
        for content_file in self.toc_structure_path.rglob("*[CONTENT].md"):
            if clean_title.lower() in content_file.name.lower():
                return content_file
        
        logger.warning(f"'{title}'에 해당하는 [CONTENT].md 파일을 찾을 수 없습니다.")
        return None
    
    def save_content_to_file(self, file_path: Path, content: str, title: str):
        """추출된 내용을 파일에 저장한다"""
        try:
            # 디렉토리가 존재하는지 확인
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 내용 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write("## 추출된 내용\n\n")
                f.write(content)
                f.write(f"\n\n---\n\n**추출 완료**: {len(content)} 문자")
            
            logger.info(f"내용이 저장되었습니다: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"파일 저장 중 오류 발생: {e}")
            return False
    
    def process_all_leaf_nodes(self, max_nodes: int = None):
        """모든 leaf node들을 처리한다"""
        logger.info("모든 leaf node 처리 시작...")
        
        if not self.leaf_nodes:
            self.parse_toc_structure()
        
        processed_count = 0
        success_count = 0
        
        # 처리할 노드 수 제한 (테스트용)
        nodes_to_process = self.leaf_nodes[:max_nodes] if max_nodes else self.leaf_nodes
        
        for i, leaf in enumerate(nodes_to_process, 1):
            logger.info(f"[{i}/{len(nodes_to_process)}] '{leaf['title']}' 처리 중...")
            
            # PDF에서 내용 추출
            content = self.extract_content_from_pdf(leaf['title'])
            
            if content:
                # 해당 [CONTENT].md 파일 경로 찾기
                file_path = self.find_content_file_path(leaf['title'], leaf['node_type'])
                
                if file_path:
                    # 내용 저장
                    if self.save_content_to_file(file_path, content, leaf['title']):
                        success_count += 1
                else:
                    logger.warning(f"파일 경로를 찾을 수 없습니다: {leaf['title']}")
            
            processed_count += 1
        
        logger.info(f"처리 완료: {processed_count}개 중 {success_count}개 성공")
        return processed_count, success_count
    
    def test_single_extraction(self, test_title: str = "Summary"):
        """단일 섹션 추출 테스트"""
        logger.info(f"단일 추출 테스트: '{test_title}'")
        
        # 여러 테스트 제목 시도
        test_titles = [
            test_title,
            "Summary", 
            "1.1.1 The design phase",
            "Introduction",
            "UML 101"
        ]
        
        for title in test_titles:
            logger.info(f"테스트 중: '{title}'")
            content = self.extract_content_from_pdf(title)
            
            if content:
                logger.info(f"추출 성공! 내용 길이: {len(content)} 문자")
                print(f"\n=== '{title}' 추출된 내용 미리보기 ===")
                print(content[:500] + "..." if len(content) > 500 else content)
                
                # 파일 경로 찾기 테스트
                file_path = self.find_content_file_path(title, 3)
                if file_path:
                    logger.info(f"파일 경로 찾기 성공: {file_path}")
                    return  # 성공하면 테스트 종료
                else:
                    logger.warning(f"파일 경로 찾기 실패: {title}")
                    
                return  # 내용은 추출되었으므로 성공으로 간주
            else:
                logger.warning(f"'{title}' 내용 추출 실패")
        
        logger.error("모든 테스트 제목에서 내용 추출 실패!")

def main():
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_structure_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    # 추출기 초기화
    extractor = ImprovedContentExtractor(toc_file, pdf_file, toc_structure_dir)
    
    # TOC 구조 파싱
    extractor.parse_toc_structure()
    
    print(f"\n발견된 leaf node: {len(extractor.leaf_nodes)}개")
    
    # 메뉴 선택
    while True:
        print("\n=== 메뉴 ===")
        print("1. 단일 추출 테스트")
        print("2. 처음 5개 노드만 처리")
        print("3. 모든 노드 처리")
        print("4. 종료")
        
        choice = input("선택하세요 (1-4): ").strip()
        
        if choice == '1':
            extractor.test_single_extraction()
        elif choice == '2':
            extractor.process_all_leaf_nodes(max_nodes=5)
        elif choice == '3':
            confirm = input("모든 노드를 처리하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                extractor.process_all_leaf_nodes()
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()