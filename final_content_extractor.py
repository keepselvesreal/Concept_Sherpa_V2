#!/usr/bin/env python3
"""
최종 Leaf Node Content Extractor
PDF에서 TOC leaf node들의 실제 내용을 추출하여 TOC_Structure에 저장하는 스크립트
"""

import re
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalContentExtractor:
    def __init__(self, toc_file_path: str, pdf_file_path: str, toc_structure_path: str):
        self.toc_file_path = Path(toc_file_path)
        self.pdf_file_path = Path(pdf_file_path)
        self.toc_structure_path = Path(toc_structure_path)
        self.leaf_nodes = []
        
    def parse_leaf_nodes(self) -> List[Dict]:
        """v4 TOC 파일에서 LEAF 태그가 있는 노드들을 추출한다"""
        logger.info("Leaf node 파싱 시작...")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        leaf_nodes = []
        
        for line_num, line in enumerate(lines, 1):
            if '**[LEAF]**' not in line:
                continue
                
            # 노드 정보 추출
            node_match = re.search(r'\(node(\d+)\)', line)
            if not node_match:
                continue
                
            node_type = int(node_match.group(1))
            
            # 제목 추출 (- 와 태그들 제거)
            stripped_line = line.lstrip()
            title_part = stripped_line.lstrip('- ')
            title = re.sub(r'\s*\(node\d+\).*$', '', title_part).strip()
            
            leaf_nodes.append({
                'line_num': line_num,
                'title': title,
                'node_type': node_type,
                'original_line': line.rstrip()
            })
        
        self.leaf_nodes = leaf_nodes
        logger.info(f"총 {len(leaf_nodes)}개의 leaf node 발견")
        return leaf_nodes
    
    def extract_section_content(self, title: str, max_pages_to_search: int = 100) -> str:
        """PDF에서 특정 섹션의 내용을 추출한다"""
        
        # 검색할 패턴들 생성
        search_patterns = [
            title,
            title.replace(" (사용자 추가)", ""),
            re.sub(r'\s*\([^)]*\)\s*', '', title).strip(),  # 괄호 내용 제거
        ]
        
        # 숫자 패턴이 있는 경우 추가 패턴 생성
        if re.match(r'^\d+\.\d+', title):
            section_num = re.match(r'^(\d+\.\d+(?:\.\d+)?)', title).group(1)
            search_patterns.append(section_num)
        
        try:
            with pdfplumber.open(self.pdf_file_path) as pdf:
                content_start_page = None
                content_lines = []
                
                # 섹션 시작점 찾기
                for page_num, page in enumerate(pdf.pages[:max_pages_to_search], 1):
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # 패턴 매칭
                    for pattern in search_patterns:
                        if pattern and len(pattern) > 2:
                            # 정확한 매칭을 위한 정규식
                            regex_pattern = re.escape(pattern)
                            if re.search(regex_pattern, text, re.IGNORECASE):
                                content_start_page = page_num
                                logger.info(f"'{pattern}' 패턴을 페이지 {page_num}에서 발견")
                                break
                    
                    if content_start_page:
                        break
                
                if not content_start_page:
                    logger.warning(f"'{title}' 섹션을 찾을 수 없음")
                    return ""
                
                # 내용 추출 (시작 페이지부터 최대 3페이지)
                for page_offset in range(3):
                    page_idx = content_start_page - 1 + page_offset
                    if page_idx >= len(pdf.pages):
                        break
                        
                    page = pdf.pages[page_idx]
                    text = page.extract_text()
                    if text:
                        content_lines.extend(text.split('\n'))
                
                # 내용 정리
                if content_lines:
                    content = self._clean_content(content_lines, title)
                    logger.info(f"'{title}' 내용 추출 완료: {len(content)} 문자")
                    return content
                else:
                    logger.warning(f"'{title}' 내용이 비어있음")
                    return ""
                
        except Exception as e:
            logger.error(f"PDF 추출 중 오류: {e}")
            return ""
    
    def _clean_content(self, lines: List[str], section_title: str) -> str:
        """추출된 내용을 정리한다"""
        cleaned_lines = []
        section_started = False
        
        for line in lines:
            line = line.strip()
            
            # 빈 줄이나 페이지 번호 스킵
            if not line or re.match(r'^\d+$', line):
                continue
            
            # 너무 짧은 줄 스킵 (헤더/푸터)
            if len(line) < 3:
                continue
            
            # 섹션 제목을 찾으면 시작
            if not section_started and section_title.lower() in line.lower():
                section_started = True
                cleaned_lines.append(f"# {section_title}")
                cleaned_lines.append("")
                continue
            
            if section_started:
                # 다음 메인 섹션이 시작되면 중단
                if re.match(r'^\d+\.\d+', line) and line != section_title:
                    break
                
                cleaned_lines.append(line)
                
                # 충분한 내용이 수집되면 중단
                if len('\n'.join(cleaned_lines)) > 2000:
                    break
        
        return '\n'.join(cleaned_lines)
    
    def find_content_file(self, title: str) -> Optional[Path]:
        """제목에 해당하는 [CONTENT].md 파일을 찾는다"""
        
        # 제목 정리
        clean_title = title.replace(" (사용자 추가)", "")
        clean_title = re.sub(r'[^\w\s\-\.]', ' ', clean_title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        
        # 패턴들
        patterns = [
            f"*{clean_title}*[CONTENT].md",
            f"*{clean_title.replace(' ', '*')}*[CONTENT].md"
        ]
        
        # 숫자로 시작하는 경우 숫자 패턴으로도 검색
        if re.match(r'^\d+', clean_title):
            number_part = re.match(r'^(\d+(?:\.\d+(?:\.\d+)?)?)', clean_title).group(1)
            patterns.append(f"*{number_part}*[CONTENT].md")
        
        for pattern in patterns:
            files = list(self.toc_structure_path.rglob(pattern))
            if files:
                logger.info(f"파일 찾기 성공: {files[0]}")
                return files[0]
        
        # 더 유연한 검색
        for content_file in self.toc_structure_path.rglob("*[CONTENT].md"):
            if clean_title.lower() in content_file.name.lower():
                logger.info(f"유연 검색으로 파일 발견: {content_file}")
                return content_file
        
        logger.warning(f"'{title}' 파일을 찾을 수 없음")
        return None
    
    def save_content_to_file(self, file_path: Path, content: str, title: str) -> bool:
        """내용을 파일에 저장한다"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                if content:
                    f.write("## 추출된 내용\n\n")
                    f.write(content)
                    f.write(f"\n\n---\n\n**추출 완료**: {len(content)} 문자\n")
                else:
                    f.write("## 내용 추출 실패\n\n")
                    f.write("PDF에서 해당 섹션을 찾을 수 없거나 내용을 추출할 수 없습니다.\n")
            
            logger.info(f"파일 저장 완료: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"파일 저장 실패: {e}")
            return False
    
    def process_single_node(self, node: Dict) -> bool:
        """단일 노드를 처리한다"""
        title = node['title']
        logger.info(f"처리 중: '{title}'")
        
        # 1. PDF에서 내용 추출
        content = self.extract_section_content(title)
        
        # 2. 해당 파일 찾기
        file_path = self.find_content_file(title)
        
        if file_path:
            # 3. 파일에 저장
            return self.save_content_to_file(file_path, content, title)
        else:
            logger.warning(f"'{title}' 파일 경로를 찾을 수 없음")
            return False
    
    def process_all_nodes(self, max_nodes: Optional[int] = None) -> Tuple[int, int]:
        """모든 노드를 처리한다"""
        if not self.leaf_nodes:
            self.parse_leaf_nodes()
        
        nodes_to_process = self.leaf_nodes[:max_nodes] if max_nodes else self.leaf_nodes
        
        success_count = 0
        total_count = len(nodes_to_process)
        
        for i, node in enumerate(nodes_to_process, 1):
            logger.info(f"\n=== [{i}/{total_count}] ===")
            if self.process_single_node(node):
                success_count += 1
        
        logger.info(f"\n처리 완료: {total_count}개 중 {success_count}개 성공")
        return total_count, success_count
    
    def test_extraction(self):
        """추출 테스트"""
        if not self.leaf_nodes:
            self.parse_leaf_nodes()
        
        # 처음 3개 노드로 테스트
        test_nodes = self.leaf_nodes[:3]
        
        logger.info("=== 추출 테스트 시작 ===")
        for i, node in enumerate(test_nodes, 1):
            logger.info(f"\n테스트 {i}: {node['title']}")
            content = self.extract_section_content(node['title'])
            
            if content:
                print(f"\n내용 미리보기 ({len(content)} 문자):")
                print(content[:300] + "..." if len(content) > 300 else content)
            else:
                print("내용 추출 실패")

def main():
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v4.md"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    toc_structure_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    # 추출기 초기화
    extractor = FinalContentExtractor(toc_file, pdf_file, toc_structure_dir)
    
    # 실행
    print("=== Final Content Extractor ===")
    print("1. 추출 테스트 (첫 3개)")
    print("2. 처음 10개 노드 처리")
    print("3. 모든 노드 처리")
    
    choice = input("선택하세요 (1-3): ").strip()
    
    if choice == '1':
        extractor.test_extraction()
    elif choice == '2':
        extractor.process_all_nodes(max_nodes=10)
    elif choice == '3':
        confirm = input("모든 노드를 처리하시겠습니까? (y/n): ").strip().lower()
        if confirm == 'y':
            extractor.process_all_nodes()
    else:
        print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()