#!/usr/bin/env python3
"""
생성 시간: 2025-08-08 10:58:05
핵심 내용: 리프 노드에 해당하는 부분들의 텍스트를 PDF에서 정확하게 추출하는 스크립트
상세 내용:
    - load_toc_data(): enhanced_toc_with_relationships.json 파일 로드 및 구조 분석
    - identify_leaf_nodes(): 자식이 없는 리프 노드 식별 로직 (children_ids가 빈 배열인 노드)
    - extract_page_text(): 추측된 페이지 정보 기반 텍스트 추출 (관대한 페이지 범위)  
    - find_content_boundaries(): 현재 노드와 다음 노드 제목을 활용한 정확한 텍스트 경계 설정
    - extract_leaf_content(): 메인 추출 함수 - 페이지 추출 후 제목 매칭으로 정제
    - save_extracted_content(): 추출된 텍스트를 개별 파일로 저장
    - main(): 전체 처리 흐름 제어
상태: 활성
주소: leaf_node_text_extractor
참조: enhanced_toc_with_relationships.json에서 목차 구조 참조
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
import PyPDF2
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeafNodeTextExtractor:
    def __init__(self, toc_file_path: str, pdf_file_path: str, output_dir: str):
        """
        리프 노드 텍스트 추출기 초기화
        
        Args:
            toc_file_path: enhanced_toc_with_relationships.json 파일 경로
            pdf_file_path: PDF 파일 경로  
            output_dir: 추출된 텍스트를 저장할 디렉토리
        """
        self.toc_file_path = toc_file_path
        self.pdf_file_path = pdf_file_path
        self.output_dir = Path(output_dir)
        self.toc_data = []
        self.pdf_reader = None
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_toc_data(self) -> bool:
        """
        enhanced_toc_with_relationships.json 파일 로드
        
        Returns:
            bool: 로드 성공 여부
        """
        try:
            with open(self.toc_file_path, 'r', encoding='utf-8') as f:
                self.toc_data = json.load(f)
            logger.info(f"TOC 데이터 로드 완료: {len(self.toc_data)}개 노드")
            return True
        except Exception as e:
            logger.error(f"TOC 데이터 로드 실패: {e}")
            return False
            
    def load_pdf(self) -> bool:
        """
        PDF 파일 로드
        
        Returns:
            bool: 로드 성공 여부
        """
        try:
            with open(self.pdf_file_path, 'rb') as pdf_file:
                self.pdf_reader = PyPDF2.PdfReader(pdf_file)
                logger.info(f"PDF 로드 완료: {len(self.pdf_reader.pages)}페이지")
            return True
        except Exception as e:
            logger.error(f"PDF 로드 실패: {e}")
            return False
            
    def identify_leaf_nodes(self) -> List[Dict]:
        """
        자식이 없는 리프 노드 식별
        
        Returns:
            List[Dict]: 리프 노드 리스트
        """
        leaf_nodes = []
        for node in self.toc_data:
            # children_ids가 빈 배열이면 리프 노드
            if not node.get('children_ids', []):
                leaf_nodes.append(node)
        
        logger.info(f"리프 노드 식별 완료: {len(leaf_nodes)}개")
        return leaf_nodes
    
    def get_next_sibling_node(self, current_node: Dict) -> Optional[Dict]:
        """
        현재 노드의 다음 형제 노드 또는 다음 노드 찾기
        
        Args:
            current_node: 현재 노드
            
        Returns:
            Optional[Dict]: 다음 노드 (없으면 None)
        """
        current_id = current_node['id']
        
        # 같은 레벨의 다음 노드 찾기
        for i, node in enumerate(self.toc_data):
            if node['id'] == current_id and i + 1 < len(self.toc_data):
                next_node = self.toc_data[i + 1]
                # 같은 레벨이거나 상위 레벨의 노드 반환
                if next_node['level'] <= current_node['level']:
                    return next_node
                    
        return None
    
    def extract_page_text(self, start_page: int, end_page: int) -> str:
        """
        지정된 페이지 범위의 텍스트 추출 (관대한 추출)
        
        Args:
            start_page: 시작 페이지 (1-based)
            end_page: 끝 페이지 (1-based)
            
        Returns:
            str: 추출된 텍스트
        """
        if not self.pdf_reader:
            return ""
            
        extracted_text = ""
        
        # PDF 페이지는 0-based이므로 -1
        start_idx = max(0, start_page - 1)
        end_idx = min(len(self.pdf_reader.pages), end_page)
        
        try:
            for page_idx in range(start_idx, end_idx):
                page = self.pdf_reader.pages[page_idx]
                page_text = page.extract_text()
                extracted_text += f"\n=== Page {page_idx + 1} ===\n{page_text}\n"
                
        except Exception as e:
            logger.error(f"페이지 {start_page}-{end_page} 추출 실패: {e}")
            
        return extracted_text
    
    def find_content_boundaries(self, text: str, current_title: str, next_title: Optional[str] = None) -> str:
        """
        제목을 기준으로 정확한 콘텐츠 경계 설정
        
        Args:
            text: 전체 추출된 텍스트
            current_title: 현재 노드 제목
            next_title: 다음 노드 제목 (선택적)
            
        Returns:
            str: 정제된 텍스트
        """
        # 제목에서 특수문자 제거하여 검색용 패턴 생성
        def clean_title_for_search(title: str) -> str:
            # 숫자, 점, 공백 제거하고 핵심 단어만 추출
            cleaned = re.sub(r'^[\d\.\s]+', '', title)  # 앞의 숫자와 점 제거
            cleaned = re.sub(r'[^\w\s]', '', cleaned)   # 특수문자 제거
            return cleaned.strip()
        
        current_clean = clean_title_for_search(current_title)
        
        # 현재 제목 위치 찾기 (대소문자 무시, 유연한 매칭)
        current_pattern = re.compile(re.escape(current_clean), re.IGNORECASE)
        current_match = current_pattern.search(text)
        
        if not current_match:
            # 제목을 찾을 수 없으면 전체 텍스트 반환
            logger.warning(f"제목 '{current_title}' 매칭 실패")
            return text
            
        # 현재 제목 이후부터 시작
        start_pos = current_match.end()
        
        # 다음 제목이 있으면 그 위치까지만 추출
        if next_title:
            next_clean = clean_title_for_search(next_title)
            next_pattern = re.compile(re.escape(next_clean), re.IGNORECASE)
            next_match = next_pattern.search(text, start_pos)
            
            if next_match:
                end_pos = next_match.start()
                content = text[start_pos:end_pos]
            else:
                content = text[start_pos:]
        else:
            content = text[start_pos:]
        
        # 페이지 구분선 제거 및 정리
        content = re.sub(r'\n=== Page \d+ ===\n', '\n', content)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # 과도한 줄바꿈 제거
        
        return content.strip()
    
    def extract_leaf_content(self, leaf_node: Dict) -> str:
        """
        리프 노드의 콘텐츠 추출
        
        Args:
            leaf_node: 리프 노드 정보
            
        Returns:
            str: 추출된 콘텐츠
        """
        start_page = leaf_node.get('start_page', 1)
        end_page = leaf_node.get('end_page', start_page)
        title = leaf_node.get('title', '')
        
        # 관대한 페이지 범위로 텍스트 추출 (앞뒤로 1페이지씩 여유)
        extended_start = max(1, start_page - 1)
        extended_end = end_page + 1
        
        logger.info(f"'{title}' 추출 중 (페이지 {extended_start}-{extended_end})")
        
        # 페이지 텍스트 추출
        raw_text = self.extract_page_text(extended_start, extended_end)
        
        if not raw_text:
            logger.warning(f"'{title}' 텍스트 추출 실패")
            return ""
        
        # 다음 노드 찾기
        next_node = self.get_next_sibling_node(leaf_node)
        next_title = next_node.get('title') if next_node else None
        
        # 제목 기반 경계 설정으로 정확한 콘텐츠 추출
        refined_content = self.find_content_boundaries(raw_text, title, next_title)
        
        return refined_content
    
    def save_extracted_content(self, leaf_node: Dict, content: str) -> str:
        """
        추출된 콘텐츠를 파일로 저장
        
        Args:
            leaf_node: 리프 노드 정보
            content: 추출된 콘텐츠
            
        Returns:
            str: 저장된 파일 경로
        """
        # 안전한 파일명 생성
        title = leaf_node.get('title', 'untitled')
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title)
        
        node_id = leaf_node.get('id', 0)
        filename = f"{node_id:03d}_{safe_title}.md"
        file_path = self.output_dir / filename
        
        # 메타데이터와 함께 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"**메타데이터:**\n")
            f.write(f"- ID: {node_id}\n")
            f.write(f"- 레벨: {leaf_node.get('level', 0)}\n")
            f.write(f"- 페이지: {leaf_node.get('start_page')}-{leaf_node.get('end_page')}\n")
            f.write(f"- 페이지 수: {leaf_node.get('page_count', 0)}\n")
            f.write(f"- 부모 ID: {leaf_node.get('parent_id')}\n\n")
            f.write("---\n\n")
            f.write(content)
        
        logger.info(f"저장 완료: {file_path}")
        return str(file_path)
    
    def process_all_leaf_nodes(self) -> List[str]:
        """
        모든 리프 노드 처리
        
        Returns:
            List[str]: 생성된 파일 경로 리스트
        """
        leaf_nodes = self.identify_leaf_nodes()
        saved_files = []
        
        for i, leaf_node in enumerate(leaf_nodes, 1):
            title = leaf_node.get('title', 'untitled')
            logger.info(f"[{i}/{len(leaf_nodes)}] 처리 중: {title}")
            
            try:
                # 콘텐츠 추출
                content = self.extract_leaf_content(leaf_node)
                
                if content:
                    # 파일 저장
                    saved_file = self.save_extracted_content(leaf_node, content)
                    saved_files.append(saved_file)
                else:
                    logger.warning(f"'{title}' 콘텐츠가 비어있음")
                    
            except Exception as e:
                logger.error(f"'{title}' 처리 실패: {e}")
                continue
        
        return saved_files
    
    def generate_extraction_report(self, saved_files: List[str]) -> str:
        """
        추출 결과 리포트 생성
        
        Args:
            saved_files: 저장된 파일 경로 리스트
            
        Returns:
            str: 리포트 파일 경로
        """
        report_path = self.output_dir / "extraction_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 리프 노드 텍스트 추출 리포트\n\n")
            f.write(f"**추출 시간:** {logging.Formatter().formatTime(logging.LogRecord('', 0, '', 0, '', (), None))}\n")
            f.write(f"**총 리프 노드 수:** {len(self.identify_leaf_nodes())}\n")
            f.write(f"**성공적으로 추출된 파일 수:** {len(saved_files)}\n\n")
            
            f.write("## 추출된 파일 목록\n\n")
            for file_path in saved_files:
                filename = Path(file_path).name
                f.write(f"- {filename}\n")
        
        logger.info(f"추출 리포트 생성: {report_path}")
        return str(report_path)


def main():
    """
    메인 함수 - 리프 노드 텍스트 추출 실행
    """
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/extracted_leaf_nodes"
    
    # 추출기 초기화
    extractor = LeafNodeTextExtractor(toc_file, pdf_file, output_dir)
    
    try:
        # 1. TOC 데이터 로드
        if not extractor.load_toc_data():
            logger.error("TOC 데이터 로드 실패로 종료")
            return
        
        # 2. PDF 로드
        if not extractor.load_pdf():
            logger.error("PDF 로드 실패로 종료")
            return
        
        # 3. 모든 리프 노드 처리
        logger.info("리프 노드 텍스트 추출 시작")
        saved_files = extractor.process_all_leaf_nodes()
        
        # 4. 결과 리포트 생성
        report_file = extractor.generate_extraction_report(saved_files)
        
        logger.info(f"추출 완료! 총 {len(saved_files)}개 파일 생성")
        logger.info(f"결과 확인: {output_dir}")
        
    except Exception as e:
        logger.error(f"추출 과정에서 오류 발생: {e}")


if __name__ == "__main__":
    main()