#!/usr/bin/env python3
"""
생성 시간: 2025-08-08 11:02:11
핵심 내용: 리프 노드 텍스트 추출기 개선 버전 - PDF 파일 핸들링 문제 해결
상세 내용:
    - load_toc_data(): enhanced_toc_with_relationships.json 파일 로드 및 구조 분석
    - identify_leaf_nodes(): 자식이 없는 리프 노드 식별 로직 (children_ids가 빈 배열인 노드)
    - extract_page_text_with_pdfplumber(): pdfplumber를 사용한 안정적인 텍스트 추출
    - find_content_boundaries_fuzzy(): 퍼지 매칭 기반 정확한 텍스트 경계 설정
    - extract_leaf_content_safe(): 에러 복구 기능을 포함한 안전한 콘텐츠 추출
    - save_extracted_content(): 추출된 텍스트를 개별 파일로 저장
    - process_with_error_recovery(): 에러 복구 기능을 포함한 배치 처리
    - main(): 전체 처리 흐름 제어 및 리소스 관리
상태: 활성
주소: leaf_node_text_extractor_v2
참조: leaf_node_text_extractor에서 개선된 버전
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
import pdfplumber
from pathlib import Path
import logging
from difflib import SequenceMatcher
import gc

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeafNodeTextExtractorV2:
    def __init__(self, toc_file_path: str, pdf_file_path: str, output_dir: str):
        """
        리프 노드 텍스트 추출기 V2 초기화
        
        Args:
            toc_file_path: enhanced_toc_with_relationships.json 파일 경로
            pdf_file_path: PDF 파일 경로  
            output_dir: 추출된 텍스트를 저장할 디렉토리
        """
        self.toc_file_path = toc_file_path
        self.pdf_file_path = pdf_file_path
        self.output_dir = Path(output_dir)
        self.toc_data = []
        self.pdf_doc = None  # pdfplumber 문서 객체
        self.total_pages = 0
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 통계 정보
        self.stats = {
            'total_nodes': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'empty_content': 0
        }
        
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
            
    def open_pdf(self) -> bool:
        """
        pdfplumber를 사용하여 PDF 파일 열기
        
        Returns:
            bool: PDF 열기 성공 여부
        """
        try:
            self.pdf_doc = pdfplumber.open(self.pdf_file_path)
            self.total_pages = len(self.pdf_doc.pages)
            logger.info(f"PDF 파일 열기 완료: {self.total_pages}페이지")
            return True
        except Exception as e:
            logger.error(f"PDF 파일 열기 실패: {e}")
            return False
    
    def close_pdf(self):
        """PDF 파일 닫기"""
        if self.pdf_doc:
            self.pdf_doc.close()
            self.pdf_doc = None
            logger.info("PDF 파일 닫기 완료")
            
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
        
        self.stats['total_nodes'] = len(leaf_nodes)
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
    
    def extract_page_text_with_pdfplumber(self, start_page: int, end_page: int) -> str:
        """
        pdfplumber를 사용하여 지정된 페이지 범위의 텍스트 추출
        
        Args:
            start_page: 시작 페이지 (1-based)
            end_page: 끝 페이지 (1-based)
            
        Returns:
            str: 추출된 텍스트
        """
        if not self.pdf_doc:
            logger.error("PDF 파일이 열려있지 않습니다")
            return ""
            
        extracted_text = ""
        
        # pdfplumber 페이지는 0-based이므로 -1
        start_idx = max(0, start_page - 1)
        end_idx = min(self.total_pages, end_page)
        
        try:
            for page_idx in range(start_idx, end_idx):
                try:
                    page = self.pdf_doc.pages[page_idx]
                    page_text = page.extract_text()
                    
                    if page_text:
                        extracted_text += f"\n=== Page {page_idx + 1} ===\n{page_text.strip()}\n"
                    else:
                        logger.warning(f"페이지 {page_idx + 1}에서 텍스트를 추출할 수 없음")
                        
                except Exception as e:
                    logger.warning(f"페이지 {page_idx + 1} 추출 실패: {e}")
                    continue
                
        except Exception as e:
            logger.error(f"페이지 범위 {start_page}-{end_page} 추출 실패: {e}")
            
        return extracted_text.strip()
    
    def similarity_ratio(self, a: str, b: str) -> float:
        """
        두 문자열 간의 유사도 계산 (퍼지 매칭)
        
        Args:
            a: 첫 번째 문자열
            b: 두 번째 문자열
            
        Returns:
            float: 유사도 (0.0-1.0)
        """
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def clean_title_for_matching(self, title: str) -> str:
        """
        매칭을 위한 제목 정리
        
        Args:
            title: 원본 제목
            
        Returns:
            str: 정리된 제목
        """
        # 숫자, 점, 특수문자 제거
        cleaned = re.sub(r'^[\d\.\s\-—]+', '', title)  # 앞의 번호 제거
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)     # 특수문자를 공백으로
        cleaned = re.sub(r'\s+', ' ', cleaned)         # 연속 공백 제거
        return cleaned.strip()
    
    def find_content_boundaries_fuzzy(self, text: str, current_title: str, next_title: Optional[str] = None) -> str:
        """
        퍼지 매칭을 사용한 정확한 콘텐츠 경계 설정
        
        Args:
            text: 전체 추출된 텍스트
            current_title: 현재 노드 제목
            next_title: 다음 노드 제목 (선택적)
            
        Returns:
            str: 정제된 텍스트
        """
        current_clean = self.clean_title_for_matching(current_title)
        
        # 현재 제목 위치 찾기 (퍼지 매칭 사용)
        best_match_pos = -1
        best_match_ratio = 0.0
        
        # 텍스트를 라인별로 나누어 검색
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_clean = self.clean_title_for_matching(line)
            
            # 유사도 계산
            ratio = self.similarity_ratio(current_clean, line_clean)
            
            if ratio > best_match_ratio and ratio > 0.6:  # 60% 이상 유사할 때
                best_match_ratio = ratio
                # 라인 인덱스를 문자 위치로 변환
                best_match_pos = text.find(line)
        
        if best_match_pos == -1:
            logger.warning(f"제목 '{current_title}' 매칭 실패 (최고 유사도: {best_match_ratio:.2f})")
            return text  # 매칭 실패 시 전체 텍스트 반환
        
        # 현재 제목 이후부터 시작
        start_pos = best_match_pos + len(lines[0])  # 첫 번째 매칭 라인 길이만큼 건너뜀
        
        # 다음 제목 찾기
        if next_title:
            next_clean = self.clean_title_for_matching(next_title)
            
            # 다음 제목의 위치 찾기
            next_match_pos = -1
            next_best_ratio = 0.0
            
            # start_pos 이후의 텍스트에서 검색
            remaining_text = text[start_pos:]
            remaining_lines = remaining_text.split('\n')
            
            for line in remaining_lines:
                line_clean = self.clean_title_for_matching(line)
                ratio = self.similarity_ratio(next_clean, line_clean)
                
                if ratio > next_best_ratio and ratio > 0.6:
                    next_best_ratio = ratio
                    next_match_pos = remaining_text.find(line)
            
            if next_match_pos != -1:
                end_pos = start_pos + next_match_pos
                content = text[start_pos:end_pos]
            else:
                content = text[start_pos:]
                logger.info(f"다음 제목 '{next_title}' 매칭 실패, 끝까지 추출")
        else:
            content = text[start_pos:]
        
        # 페이지 구분선 제거 및 정리
        content = re.sub(r'\n=== Page \d+ ===\n', '\n', content)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # 과도한 줄바꿈 제거
        
        return content.strip()
    
    def extract_leaf_content_safe(self, leaf_node: Dict) -> Tuple[str, bool]:
        """
        안전한 리프 노드 콘텐츠 추출 (에러 복구 포함)
        
        Args:
            leaf_node: 리프 노드 정보
            
        Returns:
            Tuple[str, bool]: (추출된 콘텐츠, 성공 여부)
        """
        start_page = leaf_node.get('start_page', 1)
        end_page = leaf_node.get('end_page', start_page)
        title = leaf_node.get('title', '')
        
        try:
            # 관대한 페이지 범위로 텍스트 추출 (앞뒤로 1페이지씩 여유)
            extended_start = max(1, start_page - 1)
            extended_end = min(self.total_pages, end_page + 1)
            
            logger.info(f"'{title}' 추출 중 (페이지 {extended_start}-{extended_end})")
            
            # 페이지 텍스트 추출
            raw_text = self.extract_page_text_with_pdfplumber(extended_start, extended_end)
            
            if not raw_text:
                logger.warning(f"'{title}' 텍스트 추출 실패")
                return "", False
            
            # 다음 노드 찾기
            next_node = self.get_next_sibling_node(leaf_node)
            next_title = next_node.get('title') if next_node else None
            
            # 퍼지 매칭 기반 경계 설정으로 정확한 콘텐츠 추출
            refined_content = self.find_content_boundaries_fuzzy(raw_text, title, next_title)
            
            if len(refined_content.strip()) == 0:
                logger.warning(f"'{title}' 콘텐츠가 비어있음")
                return "", False
            
            return refined_content, True
            
        except Exception as e:
            logger.error(f"'{title}' 추출 중 예외 발생: {e}")
            return "", False
    
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
        safe_title = safe_title[:50]  # 파일명 길이 제한
        
        node_id = leaf_node.get('id', 0)
        filename = f"{node_id:03d}_{safe_title}.md"
        file_path = self.output_dir / filename
        
        # 메타데이터와 함께 저장
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"**메타데이터:**\n")
                f.write(f"- ID: {node_id}\n")
                f.write(f"- 레벨: {leaf_node.get('level', 0)}\n")
                f.write(f"- 페이지: {leaf_node.get('start_page')}-{leaf_node.get('end_page')}\n")
                f.write(f"- 페이지 수: {leaf_node.get('page_count', 0)}\n")
                f.write(f"- 부모 ID: {leaf_node.get('parent_id')}\n")
                f.write(f"- 텍스트 길이: {len(content)} 문자\n\n")
                f.write("---\n\n")
                f.write(content)
            
            logger.info(f"저장 완료: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"파일 저장 실패 {file_path}: {e}")
            return ""
    
    def process_with_error_recovery(self) -> List[str]:
        """
        에러 복구 기능을 포함한 모든 리프 노드 처리
        
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
                content, success = self.extract_leaf_content_safe(leaf_node)
                
                if success and content:
                    # 파일 저장
                    saved_file = self.save_extracted_content(leaf_node, content)
                    if saved_file:
                        saved_files.append(saved_file)
                        self.stats['successful_extractions'] += 1
                    else:
                        self.stats['failed_extractions'] += 1
                else:
                    if not content:
                        self.stats['empty_content'] += 1
                    else:
                        self.stats['failed_extractions'] += 1
                    logger.warning(f"'{title}' 처리 실패")
                    
            except Exception as e:
                logger.error(f"'{title}' 처리 중 예외: {e}")
                self.stats['failed_extractions'] += 1
                continue
            
            # 메모리 정리 (매 10개 노드마다)
            if i % 10 == 0:
                gc.collect()
        
        return saved_files
    
    def generate_extraction_report(self, saved_files: List[str]) -> str:
        """
        상세한 추출 결과 리포트 생성
        
        Args:
            saved_files: 저장된 파일 경로 리스트
            
        Returns:
            str: 리포트 파일 경로
        """
        report_path = self.output_dir / "extraction_report_v2.md"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"# 리프 노드 텍스트 추출 리포트 V2\n\n")
                f.write(f"**추출 시간:** 2025-08-08 11:02:11\n")
                f.write(f"**PDF 파일:** {self.pdf_file_path}\n")
                f.write(f"**총 PDF 페이지 수:** {self.total_pages}\n\n")
                
                f.write(f"## 추출 통계\n\n")
                f.write(f"- **총 리프 노드 수:** {self.stats['total_nodes']}\n")
                f.write(f"- **성공적 추출:** {self.stats['successful_extractions']}\n")
                f.write(f"- **추출 실패:** {self.stats['failed_extractions']}\n")
                f.write(f"- **빈 콘텐츠:** {self.stats['empty_content']}\n")
                
                success_rate = (self.stats['successful_extractions'] / max(1, self.stats['total_nodes'])) * 100
                f.write(f"- **성공률:** {success_rate:.1f}%\n\n")
                
                f.write("## 추출된 파일 목록\n\n")
                if saved_files:
                    for file_path in saved_files:
                        filename = Path(file_path).name
                        # 파일 크기 정보 추가
                        try:
                            file_size = Path(file_path).stat().st_size
                            f.write(f"- {filename} ({file_size:,} bytes)\n")
                        except:
                            f.write(f"- {filename}\n")
                else:
                    f.write("(추출된 파일이 없습니다)\n")
                
                f.write(f"\n## 처리 개선사항\n\n")
                f.write(f"- pdfplumber 사용으로 안정적인 PDF 처리\n")
                f.write(f"- 퍼지 매칭 기반 제목 찾기 (60% 이상 유사도)\n")
                f.write(f"- 에러 복구 및 부분 성공 처리\n")
                f.write(f"- 메모리 최적화 및 가비지 컬렉션\n")
                f.write(f"- 상세한 통계 및 로깅\n")
            
            logger.info(f"추출 리포트 생성: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"리포트 생성 실패: {e}")
            return ""


def main():
    """
    메인 함수 - 개선된 리프 노드 텍스트 추출 실행
    """
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/extracted_leaf_nodes_v2"
    
    # 추출기 초기화
    extractor = LeafNodeTextExtractorV2(toc_file, pdf_file, output_dir)
    
    try:
        logger.info("=== 리프 노드 텍스트 추출 V2 시작 ===")
        
        # 1. TOC 데이터 로드
        if not extractor.load_toc_data():
            logger.error("TOC 데이터 로드 실패로 종료")
            return
        
        # 2. PDF 파일 열기
        if not extractor.open_pdf():
            logger.error("PDF 파일 열기 실패로 종료")
            return
        
        try:
            # 3. 모든 리프 노드 처리 (에러 복구 포함)
            logger.info("에러 복구 기능이 포함된 리프 노드 추출 시작")
            saved_files = extractor.process_with_error_recovery()
            
            # 4. 결과 리포트 생성
            report_file = extractor.generate_extraction_report(saved_files)
            
            # 5. 최종 결과 출력
            logger.info(f"=== 추출 완료 ===")
            logger.info(f"성공: {extractor.stats['successful_extractions']}")
            logger.info(f"실패: {extractor.stats['failed_extractions']}")
            logger.info(f"빈 콘텐츠: {extractor.stats['empty_content']}")
            logger.info(f"성공률: {(extractor.stats['successful_extractions']/max(1, extractor.stats['total_nodes']))*100:.1f}%")
            logger.info(f"결과 디렉토리: {output_dir}")
            
        finally:
            # 6. PDF 파일 닫기 (리소스 정리)
            extractor.close_pdf()
        
    except Exception as e:
        logger.error(f"추출 과정에서 치명적 오류 발생: {e}")
        # 안전한 리소스 정리
        try:
            extractor.close_pdf()
        except:
            pass


if __name__ == "__main__":
    main()