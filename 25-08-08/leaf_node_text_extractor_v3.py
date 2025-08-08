#!/usr/bin/env python3
"""
생성 시간: 2025-08-08 11:19:30
핵심 내용: 리프 노드 텍스트 추출기 V3 - ID 범위 제한 및 정확한 텍스트 경계 설정 개선
상세 내용:
    - filter_nodes_by_id_range(): ID 0-16 범위 노드 필터링 및 리프 노드 식별
    - extract_exact_page_range(): 정확한 페이지 범위만 추출 (여유 페이지 제거)
    - enhance_title_matching(): 개선된 제목 정규화 및 다중 패턴 매칭
    - format_clean_content(): 간결한 출력 형식 (content_level, title, content)
    - save_clean_content(): Level에 따른 마크다운 헤더 적용 저장
    - process_limited_range(): ID 범위 제한 배치 처리
    - main(): 전체 처리 흐름 제어 및 리소스 관리
상태: 활성
주소: leaf_node_text_extractor_v3
참조: leaf_node_text_extractor_v2에서 개선된 버전
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

class LeafNodeTextExtractorV3:
    def __init__(self, toc_file_path: str, pdf_file_path: str, output_dir: str, max_id: int = 16):
        """
        리프 노드 텍스트 추출기 V3 초기화
        
        Args:
            toc_file_path: enhanced_toc_with_relationships.json 파일 경로
            pdf_file_path: PDF 파일 경로  
            output_dir: 추출된 텍스트를 저장할 디렉토리
            max_id: 처리할 최대 노드 ID (기본값: 16)
        """
        self.toc_file_path = toc_file_path
        self.pdf_file_path = pdf_file_path
        self.output_dir = Path(output_dir)
        self.max_id = max_id
        self.toc_data = []
        self.pdf_doc = None  # pdfplumber 문서 객체
        self.total_pages = 0
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 통계 정보
        self.stats = {
            'total_nodes_in_range': 0,
            'leaf_nodes_in_range': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'empty_content': 0,
            'title_match_failures': 0
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
            
            # ID 범위 내 노드 수 계산
            nodes_in_range = [node for node in self.toc_data if node['id'] <= self.max_id]
            self.stats['total_nodes_in_range'] = len(nodes_in_range)
            
            logger.info(f"TOC 데이터 로드 완료: 전체 {len(self.toc_data)}개, ID {self.max_id} 이하 {len(nodes_in_range)}개")
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
            
    def filter_nodes_by_id_range(self) -> List[Dict]:
        """
        ID 범위 내 리프 노드 식별
        
        Returns:
            List[Dict]: ID 범위 내 리프 노드 리스트
        """
        leaf_nodes = []
        for node in self.toc_data:
            # ID 범위 체크
            if node['id'] <= self.max_id:
                # children_ids가 빈 배열이면 리프 노드
                if not node.get('children_ids', []):
                    leaf_nodes.append(node)
        
        self.stats['leaf_nodes_in_range'] = len(leaf_nodes)
        logger.info(f"ID {self.max_id} 이하 리프 노드 식별 완료: {len(leaf_nodes)}개")
        
        # 리프 노드 목록 출력
        for node in leaf_nodes:
            logger.info(f"  - ID {node['id']}: {node['title']} (레벨 {node['level']}, 페이지 {node['start_page']}-{node['end_page']})")
        
        return leaf_nodes
    
    def get_next_sibling_node(self, current_node: Dict) -> Optional[Dict]:
        """
        현재 노드의 다음 형제 노드 또는 다음 노드 찾기 (ID 범위 내에서)
        
        Args:
            current_node: 현재 노드
            
        Returns:
            Optional[Dict]: 다음 노드 (없으면 None)
        """
        current_id = current_node['id']
        
        # ID 범위 내에서 다음 노드 찾기
        filtered_nodes = [node for node in self.toc_data if node['id'] <= self.max_id]
        
        for i, node in enumerate(filtered_nodes):
            if node['id'] == current_id and i + 1 < len(filtered_nodes):
                next_node = filtered_nodes[i + 1]
                # 같은 레벨이거나 상위 레벨의 노드 반환
                if next_node['level'] <= current_node['level']:
                    return next_node
                    
        return None
    
    def extract_exact_page_range(self, start_page: int, end_page: int) -> str:
        """
        정확한 페이지 범위의 텍스트 추출 (여유 페이지 제거)
        
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
    
    def enhance_title_matching(self, title: str) -> List[str]:
        """
        향상된 제목 정규화 - 다중 패턴 생성
        
        Args:
            title: 원본 제목
            
        Returns:
            List[str]: 매칭용 패턴들
        """
        patterns = []
        
        # 원본 제목
        patterns.append(title.strip())
        
        # 기본 정리 (숫자, 점, 특수문자 제거)
        cleaned = re.sub(r'^[\d\.\s\-—]+', '', title)  # 앞의 번호 제거
        cleaned = re.sub(r'[^가-힣\w\s]', ' ', cleaned)  # 특수문자를 공백으로 (한글 보존)
        cleaned = re.sub(r'\s+', ' ', cleaned)  # 연속 공백 제거
        patterns.append(cleaned.strip())
        
        # 핵심 키워드만 추출
        words = cleaned.strip().split()
        if len(words) > 1:
            # 첫 단어와 마지막 단어
            patterns.append(f"{words[0]} {words[-1]}")
            # 처음 두 단어
            if len(words) >= 2:
                patterns.append(f"{words[0]} {words[1]}")
        
        # 중복 제거 및 빈 문자열 제거
        patterns = list(set([p for p in patterns if p.strip()]))
        
        return patterns
    
    def find_title_boundaries_enhanced(self, text: str, current_title: str, next_title: Optional[str] = None) -> str:
        """
        향상된 퍼지 매칭을 사용한 정확한 콘텐츠 경계 설정
        
        Args:
            text: 전체 추출된 텍스트
            current_title: 현재 노드 제목
            next_title: 다음 노드 제목 (선택적)
            
        Returns:
            str: 정제된 텍스트
        """
        current_patterns = self.enhance_title_matching(current_title)
        
        # 현재 제목 위치 찾기 (다중 패턴 매칭)
        best_match_pos = -1
        best_match_ratio = 0.0
        best_pattern = ""
        
        # 텍스트를 라인별로 나누어 검색
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # 각 패턴에 대해 유사도 계산
            for pattern in current_patterns:
                if not pattern:
                    continue
                    
                ratio = SequenceMatcher(None, pattern.lower(), line_clean.lower()).ratio()
                
                # 부분 매칭도 고려 (패턴이 라인에 포함되어 있는지)
                if pattern.lower() in line_clean.lower():
                    ratio = max(ratio, 0.8)  # 부분 매칭시 최소 0.8 점수
                
                if ratio > best_match_ratio and ratio > 0.5:  # 임계값을 0.5로 낮춤
                    best_match_ratio = ratio
                    best_match_pos = text.find(line)
                    best_pattern = pattern
        
        if best_match_pos == -1:
            logger.warning(f"제목 '{current_title}' 매칭 실패 (최고 유사도: {best_match_ratio:.2f})")
            self.stats['title_match_failures'] += 1
            return text  # 매칭 실패 시 전체 텍스트 반환
        
        logger.info(f"제목 '{current_title}' 매칭 성공 (패턴: '{best_pattern}', 유사도: {best_match_ratio:.2f})")
        
        # 현재 제목 이후부터 시작
        # 매칭된 라인의 끝부분을 찾아서 그 이후부터 시작
        matched_line_end = best_match_pos
        for line in lines:
            if text.find(line) == best_match_pos:
                matched_line_end = best_match_pos + len(line)
                break
        
        start_pos = matched_line_end
        
        # 다음 제목 찾기
        if next_title:
            next_patterns = self.enhance_title_matching(next_title)
            
            next_match_pos = -1
            next_best_ratio = 0.0
            
            # start_pos 이후의 텍스트에서 검색
            remaining_text = text[start_pos:]
            remaining_lines = remaining_text.split('\n')
            
            for line in remaining_lines:
                line_clean = line.strip()
                
                for pattern in next_patterns:
                    if not pattern:
                        continue
                        
                    ratio = SequenceMatcher(None, pattern.lower(), line_clean.lower()).ratio()
                    
                    # 부분 매칭도 고려
                    if pattern.lower() in line_clean.lower():
                        ratio = max(ratio, 0.8)
                    
                    if ratio > next_best_ratio and ratio > 0.5:
                        next_best_ratio = ratio
                        next_match_pos = remaining_text.find(line)
            
            if next_match_pos != -1:
                end_pos = start_pos + next_match_pos
                content = text[start_pos:end_pos]
                logger.info(f"다음 제목 '{next_title}' 매칭 성공 (유사도: {next_best_ratio:.2f})")
            else:
                content = text[start_pos:]
                logger.info(f"다음 제목 '{next_title}' 매칭 실패, 끝까지 추출")
        else:
            content = text[start_pos:]
        
        # 페이지 구분선 제거 및 정리
        content = re.sub(r'\n=== Page \d+ ===\n', '\n', content)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # 과도한 줄바꿈 제거
        content = content.strip()
        
        return content
    
    def format_clean_content(self, node: Dict, content: str) -> str:
        """
        간결한 출력 형식으로 변환
        
        Args:
            node: 노드 정보
            content: 추출된 콘텐츠
            
        Returns:
            str: 형식화된 콘텐츠
        """
        level = node.get('level', 1)
        title = node.get('title', 'Untitled')
        
        # Level에 따른 마크다운 헤더 생성
        header_prefix = '#' * (level + 1)  # level 0 → ##, level 1 → ###, level 2 → ####
        
        formatted_content = f"{header_prefix} {title}\n\n{content}"
        
        return formatted_content.strip()
    
    def extract_leaf_content_precise(self, leaf_node: Dict) -> Tuple[str, bool]:
        """
        정확한 리프 노드 콘텐츠 추출 (개선된 버전)
        
        Args:
            leaf_node: 리프 노드 정보
            
        Returns:
            Tuple[str, bool]: (추출된 콘텐츠, 성공 여부)
        """
        start_page = leaf_node.get('start_page', 1)
        end_page = leaf_node.get('end_page', start_page)
        title = leaf_node.get('title', '')
        
        try:
            logger.info(f"'{title}' 추출 중 (정확한 페이지 {start_page}-{end_page})")
            
            # 정확한 페이지 범위만 텍스트 추출 (여유 페이지 제거)
            raw_text = self.extract_exact_page_range(start_page, end_page)
            
            if not raw_text:
                logger.warning(f"'{title}' 텍스트 추출 실패")
                return "", False
            
            # 다음 노드 찾기
            next_node = self.get_next_sibling_node(leaf_node)
            next_title = next_node.get('title') if next_node else None
            
            # 향상된 퍼지 매칭 기반 경계 설정으로 정확한 콘텐츠 추출
            refined_content = self.find_title_boundaries_enhanced(raw_text, title, next_title)
            
            if len(refined_content.strip()) == 0:
                logger.warning(f"'{title}' 콘텐츠가 비어있음")
                return "", False
            
            # 간결한 형식으로 변환
            formatted_content = self.format_clean_content(leaf_node, refined_content)
            
            return formatted_content, True
            
        except Exception as e:
            logger.error(f"'{title}' 추출 중 예외 발생: {e}")
            return "", False
    
    def save_clean_content(self, leaf_node: Dict, content: str) -> str:
        """
        간결한 형식으로 콘텐츠 저장
        
        Args:
            leaf_node: 리프 노드 정보
            content: 형식화된 콘텐츠
            
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
        
        # 간결한 형식으로 저장
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"저장 완료: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"파일 저장 실패 {file_path}: {e}")
            return ""
    
    def process_limited_range(self) -> List[str]:
        """
        ID 범위 제한 모든 리프 노드 처리
        
        Returns:
            List[str]: 생성된 파일 경로 리스트
        """
        leaf_nodes = self.filter_nodes_by_id_range()
        saved_files = []
        
        for i, leaf_node in enumerate(leaf_nodes, 1):
            title = leaf_node.get('title', 'untitled')
            logger.info(f"[{i}/{len(leaf_nodes)}] 처리 중: {title}")
            
            try:
                # 콘텐츠 추출
                content, success = self.extract_leaf_content_precise(leaf_node)
                
                if success and content:
                    # 파일 저장
                    saved_file = self.save_clean_content(leaf_node, content)
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
            
            # 메모리 정리 (매 5개 노드마다)
            if i % 5 == 0:
                gc.collect()
        
        return saved_files
    
    def generate_extraction_report_v3(self, saved_files: List[str]) -> str:
        """
        V3 추출 결과 리포트 생성
        
        Args:
            saved_files: 저장된 파일 경로 리스트
            
        Returns:
            str: 리포트 파일 경로
        """
        report_path = self.output_dir / "extraction_report_v3.md"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"# 리프 노드 텍스트 추출 리포트 V3 (ID 0-{self.max_id})\n\n")
                f.write(f"**추출 시간:** 2025-08-08 11:19:30\n")
                f.write(f"**PDF 파일:** {self.pdf_file_path}\n")
                f.write(f"**총 PDF 페이지 수:** {self.total_pages}\n")
                f.write(f"**처리 범위:** ID 0-{self.max_id}\n\n")
                
                f.write(f"## 추출 통계\n\n")
                f.write(f"- **범위 내 총 노드 수:** {self.stats['total_nodes_in_range']}\n")
                f.write(f"- **범위 내 리프 노드 수:** {self.stats['leaf_nodes_in_range']}\n")
                f.write(f"- **성공적 추출:** {self.stats['successful_extractions']}\n")
                f.write(f"- **추출 실패:** {self.stats['failed_extractions']}\n")
                f.write(f"- **빈 콘텐츠:** {self.stats['empty_content']}\n")
                f.write(f"- **제목 매칭 실패:** {self.stats['title_match_failures']}\n")
                
                success_rate = (self.stats['successful_extractions'] / max(1, self.stats['leaf_nodes_in_range'])) * 100
                f.write(f"- **성공률:** {success_rate:.1f}%\n\n")
                
                f.write("## 추출된 파일 목록\n\n")
                if saved_files:
                    for file_path in saved_files:
                        filename = Path(file_path).name
                        try:
                            file_size = Path(file_path).stat().st_size
                            f.write(f"- {filename} ({file_size:,} bytes)\n")
                        except:
                            f.write(f"- {filename}\n")
                else:
                    f.write("(추출된 파일이 없습니다)\n")
                
                f.write(f"\n## V3 개선사항\n\n")
                f.write(f"- ID 범위 제한 처리 (0-{self.max_id})\n")
                f.write(f"- 정확한 페이지 범위 추출 (여유 페이지 제거)\n")
                f.write(f"- 향상된 제목 매칭 (다중 패턴, 부분 매칭)\n")
                f.write(f"- 간결한 출력 형식 (Level별 마크다운 헤더)\n")
                f.write(f"- 상세한 매칭 로그 및 통계\n")
            
            logger.info(f"V3 추출 리포트 생성: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"리포트 생성 실패: {e}")
            return ""


def main():
    """
    메인 함수 - V3 리프 노드 텍스트 추출 실행 (ID 0-16 범위)
    """
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/extracted_leaf_nodes_v3"
    
    # 추출기 초기화 (ID 16까지로 제한)
    extractor = LeafNodeTextExtractorV3(toc_file, pdf_file, output_dir, max_id=16)
    
    try:
        logger.info("=== 리프 노드 텍스트 추출 V3 시작 (ID 0-16) ===")
        
        # 1. TOC 데이터 로드
        if not extractor.load_toc_data():
            logger.error("TOC 데이터 로드 실패로 종료")
            return
        
        # 2. PDF 파일 열기
        if not extractor.open_pdf():
            logger.error("PDF 파일 열기 실패로 종료")
            return
        
        try:
            # 3. ID 범위 제한 리프 노드 처리
            logger.info("ID 범위 제한 리프 노드 추출 시작")
            saved_files = extractor.process_limited_range()
            
            # 4. 결과 리포트 생성
            report_file = extractor.generate_extraction_report_v3(saved_files)
            
            # 5. 최종 결과 출력
            logger.info(f"=== V3 추출 완료 ===")
            logger.info(f"범위 내 리프 노드: {extractor.stats['leaf_nodes_in_range']}")
            logger.info(f"성공: {extractor.stats['successful_extractions']}")
            logger.info(f"실패: {extractor.stats['failed_extractions']}")
            logger.info(f"빈 콘텐츠: {extractor.stats['empty_content']}")
            logger.info(f"제목 매칭 실패: {extractor.stats['title_match_failures']}")
            logger.info(f"성공률: {(extractor.stats['successful_extractions']/max(1, extractor.stats['leaf_nodes_in_range']))*100:.1f}%")
            logger.info(f"결과 디렉토리: {output_dir}")
            
        finally:
            # 6. PDF 파일 닫기 (리소스 정리)
            extractor.close_pdf()
        
    except Exception as e:
        logger.error(f"V3 추출 과정에서 치명적 오류 발생: {e}")
        # 안전한 리소스 정리
        try:
            extractor.close_pdf()
        except:
            pass


if __name__ == "__main__":
    main()