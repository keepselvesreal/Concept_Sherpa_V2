#!/usr/bin/env python3
"""
생성 시간: 2025-08-08 11:36:39
핵심 내용: 하이브리드 리프 노드 텍스트 추출기 V4 - Part 파일 기반 페이지 추출 + 제목 기반 정밀 구간 분리
상세 내용:
    - load_part_file(): Part 파일 로드 및 전처리
    - extract_page_range_from_part(): 페이지 번호 기반 1차 범위 추출
    - find_title_section_in_range(): 제목 기반 2차 정밀 구간 추출
    - clean_title_for_matching(): 제목 정규화 및 매칭 패턴 생성
    - format_extracted_content(): Level별 마크다운 헤더 적용
    - save_clean_extract(): 간결한 형식으로 저장
    - process_hybrid_extraction(): 하이브리드 2단계 추출 처리
    - main(): 전체 처리 흐름 제어
상태: 활성
주소: leaf_node_text_extractor_v4
참조: leaf_node_text_extractor_v3에서 개선된 하이브리드 버전
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from difflib import SequenceMatcher
import gc

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HybridLeafNodeExtractorV4:
    def __init__(self, toc_file_path: str, part_file_path: str, output_dir: str, max_id: int = 16):
        """
        하이브리드 리프 노드 텍스트 추출기 V4 초기화
        
        Args:
            toc_file_path: enhanced_toc_with_relationships.json 파일 경로
            part_file_path: Part 파일 경로 (이미 정제된 텍스트)
            output_dir: 추출된 텍스트를 저장할 디렉토리
            max_id: 처리할 최대 노드 ID (기본값: 16)
        """
        self.toc_file_path = toc_file_path
        self.part_file_path = part_file_path
        self.output_dir = Path(output_dir)
        self.max_id = max_id
        self.toc_data = []
        self.part_content = ""  # Part 파일 전체 내용
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 통계 정보
        self.stats = {
            'total_nodes_in_range': 0,
            'leaf_nodes_in_range': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'empty_content': 0,
            'page_range_failures': 0,
            'title_match_failures': 0,
            'title_match_successes': 0
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
    
    def load_part_file(self) -> bool:
        """
        Part 파일 로드
        
        Returns:
            bool: 로드 성공 여부
        """
        try:
            with open(self.part_file_path, 'r', encoding='utf-8') as f:
                self.part_content = f.read()
            
            # 페이지 개수 확인
            page_count = len(re.findall(r'## 페이지 \d+', self.part_content))
            logger.info(f"Part 파일 로드 완료: {len(self.part_content):,} 문자, {page_count}개 페이지")
            return True
        except Exception as e:
            logger.error(f"Part 파일 로드 실패: {e}")
            return False
            
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
    
    def extract_page_range_from_part(self, start_page: int, end_page: int) -> str:
        """
        Part 파일에서 페이지 번호 기반 1차 범위 추출
        
        Args:
            start_page: 시작 페이지
            end_page: 끝 페이지
            
        Returns:
            str: 추출된 페이지 범위 텍스트
        """
        if not self.part_content:
            logger.error("Part 파일이 로드되지 않았습니다")
            return ""
        
        try:
            # 시작 페이지부터 끝 페이지+1 전까지 추출
            start_pattern = f"## 페이지 {start_page}"
            end_pattern = f"## 페이지 {end_page + 1}"
            
            # 시작 지점 찾기
            start_match = re.search(re.escape(start_pattern), self.part_content)
            if not start_match:
                logger.warning(f"시작 페이지 {start_page} 패턴을 찾을 수 없음")
                self.stats['page_range_failures'] += 1
                return ""
            
            start_pos = start_match.start()
            
            # 끝 지점 찾기
            end_match = re.search(re.escape(end_pattern), self.part_content[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.start()
                content = self.part_content[start_pos:end_pos]
            else:
                # 다음 페이지가 없으면 파일 끝까지
                content = self.part_content[start_pos:]
                logger.info(f"페이지 {end_page + 1}이 없어 파일 끝까지 추출")
            
            logger.info(f"페이지 범위 {start_page}-{end_page} 추출 성공 ({len(content):,} 문자)")
            return content.strip()
            
        except Exception as e:
            logger.error(f"페이지 범위 {start_page}-{end_page} 추출 실패: {e}")
            self.stats['page_range_failures'] += 1
            return ""
    
    def clean_title_for_matching(self, title: str) -> List[str]:
        """
        제목 정규화 및 다중 매칭 패턴 생성
        
        Args:
            title: 원본 제목
            
        Returns:
            List[str]: 매칭용 패턴들
        """
        patterns = []
        
        # 원본 제목 (완전 매칭용)
        patterns.append(title.strip())
        
        # 기본 정리 버전
        cleaned = re.sub(r'^[\d\.\s\-—]+', '', title)  # 앞의 번호 제거
        cleaned = re.sub(r'[^가-힣\w\s]', ' ', cleaned)  # 특수문자를 공백으로
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()  # 연속 공백 제거
        if cleaned:
            patterns.append(cleaned)
        
        # 핵심 키워드 추출
        words = cleaned.split() if cleaned else title.split()
        if len(words) > 1:
            # 처음 두 단어
            patterns.append(f"{words[0]} {words[1]}")
            # 첫 단어와 마지막 단어
            if len(words) > 2:
                patterns.append(f"{words[0]} {words[-1]}")
        
        # 숫자만 있는 경우 (예: "1", "1.1", "1.1.1")
        number_match = re.match(r'^([\d\.]+)', title.strip())
        if number_match:
            patterns.append(number_match.group(1))
        
        # 중복 제거 및 빈 문자열 제거
        patterns = list(set([p for p in patterns if p.strip()]))
        
        return patterns
    
    def find_title_section_in_range(self, content: str, current_title: str, next_title: Optional[str] = None) -> str:
        """
        추출된 범위에서 제목 기반 2차 정밀 구간 추출
        
        Args:
            content: 페이지 범위에서 추출된 텍스트
            current_title: 현재 노드 제목
            next_title: 다음 노드 제목 (선택적)
            
        Returns:
            str: 정밀 추출된 텍스트
        """
        current_patterns = self.clean_title_for_matching(current_title)
        
        # 현재 제목 위치 찾기
        best_match_pos = -1
        best_match_ratio = 0.0
        best_pattern = ""
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # 각 패턴에 대해 매칭 시도
            for pattern in current_patterns:
                if not pattern:
                    continue
                    
                # 완전 매칭 우선
                if pattern in line_clean:
                    ratio = 1.0
                else:
                    # 유사도 매칭
                    ratio = SequenceMatcher(None, pattern.lower(), line_clean.lower()).ratio()
                
                if ratio > best_match_ratio and ratio > 0.6:  # 임계값 0.6
                    best_match_ratio = ratio
                    best_match_pos = content.find(line)
                    best_pattern = pattern
        
        if best_match_pos == -1:
            logger.warning(f"제목 '{current_title}' 매칭 실패 (최고 유사도: {best_match_ratio:.2f})")
            self.stats['title_match_failures'] += 1
            return content  # 매칭 실패 시 전체 범위 반환
        
        logger.info(f"제목 '{current_title}' 매칭 성공 (패턴: '{best_pattern}', 유사도: {best_match_ratio:.2f})")
        self.stats['title_match_successes'] += 1
        
        # 매칭된 라인의 끝부분부터 시작
        matched_line_start = best_match_pos
        matched_line_end = best_match_pos
        for line in lines:
            if content.find(line) == best_match_pos:
                matched_line_end = best_match_pos + len(line)
                break
        
        start_pos = matched_line_end
        
        # 다음 제목 찾기
        if next_title:
            next_patterns = self.clean_title_for_matching(next_title)
            
            next_match_pos = -1
            next_best_ratio = 0.0
            
            # start_pos 이후의 텍스트에서 검색
            remaining_text = content[start_pos:]
            remaining_lines = remaining_text.split('\n')
            
            for line in remaining_lines:
                line_clean = line.strip()
                
                for pattern in next_patterns:
                    if not pattern:
                        continue
                        
                    if pattern in line_clean:
                        ratio = 1.0
                    else:
                        ratio = SequenceMatcher(None, pattern.lower(), line_clean.lower()).ratio()
                    
                    if ratio > next_best_ratio and ratio > 0.6:
                        next_best_ratio = ratio
                        next_match_pos = remaining_text.find(line)
            
            if next_match_pos != -1:
                end_pos = start_pos + next_match_pos
                section_content = content[start_pos:end_pos]
                logger.info(f"다음 제목 '{next_title}' 매칭 성공 (유사도: {next_best_ratio:.2f})")
            else:
                section_content = content[start_pos:]
                logger.info(f"다음 제목 '{next_title}' 매칭 실패, 끝까지 추출")
        else:
            section_content = content[start_pos:]
        
        return section_content.strip()
    
    def format_extracted_content(self, node: Dict, content: str) -> str:
        """
        Level별 마크다운 헤더 적용 및 콘텐츠 형식화
        
        Args:
            node: 노드 정보
            content: 추출된 콘텐츠
            
        Returns:
            str: 형식화된 콘텐츠
        """
        level = node.get('level', 1)
        title = node.get('title', 'Untitled')
        
        # Level에 따른 마크다운 헤더 생성 (level + 1)
        header_prefix = '#' * (level + 1)
        
        formatted_content = f"{header_prefix} {title}\n\n{content}"
        
        return formatted_content.strip()
    
    def extract_node_content_hybrid(self, leaf_node: Dict) -> Tuple[str, bool]:
        """
        하이브리드 방식으로 리프 노드 콘텐츠 추출
        
        Args:
            leaf_node: 리프 노드 정보
            
        Returns:
            Tuple[str, bool]: (추출된 콘텐츠, 성공 여부)
        """
        start_page = leaf_node.get('start_page', 1)
        end_page = leaf_node.get('end_page', start_page)
        title = leaf_node.get('title', '')
        
        try:
            logger.info(f"'{title}' 하이브리드 추출 중 (페이지 {start_page}-{end_page})")
            
            # 1단계: Part 파일에서 페이지 범위 추출
            page_range_content = self.extract_page_range_from_part(start_page, end_page)
            
            if not page_range_content:
                logger.warning(f"'{title}' 페이지 범위 추출 실패")
                return "", False
            
            # 다음 노드 찾기
            next_node = self.get_next_sibling_node(leaf_node)
            next_title = next_node.get('title') if next_node else None
            
            # 2단계: 제목 기반 정밀 구간 추출
            section_content = self.find_title_section_in_range(page_range_content, title, next_title)
            
            if len(section_content.strip()) == 0:
                logger.warning(f"'{title}' 최종 콘텐츠가 비어있음")
                return "", False
            
            # 3단계: 형식화
            formatted_content = self.format_extracted_content(leaf_node, section_content)
            
            return formatted_content, True
            
        except Exception as e:
            logger.error(f"'{title}' 하이브리드 추출 중 예외 발생: {e}")
            return "", False
    
    def save_clean_extract(self, leaf_node: Dict, content: str) -> str:
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
        
        # 저장
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"저장 완료: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"파일 저장 실패 {file_path}: {e}")
            return ""
    
    def process_hybrid_extraction(self) -> List[str]:
        """
        하이브리드 방식으로 ID 범위 제한 모든 리프 노드 처리
        
        Returns:
            List[str]: 생성된 파일 경로 리스트
        """
        leaf_nodes = self.filter_nodes_by_id_range()
        saved_files = []
        
        for i, leaf_node in enumerate(leaf_nodes, 1):
            title = leaf_node.get('title', 'untitled')
            logger.info(f"[{i}/{len(leaf_nodes)}] 하이브리드 처리 중: {title}")
            
            try:
                # 하이브리드 콘텐츠 추출
                content, success = self.extract_node_content_hybrid(leaf_node)
                
                if success and content:
                    # 파일 저장
                    saved_file = self.save_clean_extract(leaf_node, content)
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
                    logger.warning(f"'{title}' 하이브리드 처리 실패")
                    
            except Exception as e:
                logger.error(f"'{title}' 처리 중 예외: {e}")
                self.stats['failed_extractions'] += 1
                continue
            
            # 메모리 정리 (매 5개 노드마다)
            if i % 5 == 0:
                gc.collect()
        
        return saved_files
    
    def generate_extraction_report_v4(self, saved_files: List[str]) -> str:
        """
        V4 하이브리드 추출 결과 리포트 생성
        
        Args:
            saved_files: 저장된 파일 경로 리스트
            
        Returns:
            str: 리포트 파일 경로
        """
        report_path = self.output_dir / "extraction_report_v4.md"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"# 하이브리드 리프 노드 텍스트 추출 리포트 V4 (ID 0-{self.max_id})\n\n")
                f.write(f"**추출 시간:** 2025-08-08 11:36:39\n")
                f.write(f"**Part 파일:** {self.part_file_path}\n")
                f.write(f"**처리 범위:** ID 0-{self.max_id}\n\n")
                
                f.write(f"## 추출 통계\n\n")
                f.write(f"- **범위 내 총 노드 수:** {self.stats['total_nodes_in_range']}\n")
                f.write(f"- **범위 내 리프 노드 수:** {self.stats['leaf_nodes_in_range']}\n")
                f.write(f"- **성공적 추출:** {self.stats['successful_extractions']}\n")
                f.write(f"- **추출 실패:** {self.stats['failed_extractions']}\n")
                f.write(f"- **빈 콘텐츠:** {self.stats['empty_content']}\n")
                f.write(f"- **페이지 범위 실패:** {self.stats['page_range_failures']}\n")
                f.write(f"- **제목 매칭 성공:** {self.stats['title_match_successes']}\n")
                f.write(f"- **제목 매칭 실패:** {self.stats['title_match_failures']}\n")
                
                success_rate = (self.stats['successful_extractions'] / max(1, self.stats['leaf_nodes_in_range'])) * 100
                title_match_rate = (self.stats['title_match_successes'] / max(1, self.stats['title_match_successes'] + self.stats['title_match_failures'])) * 100
                f.write(f"- **성공률:** {success_rate:.1f}%\n")
                f.write(f"- **제목 매칭 성공률:** {title_match_rate:.1f}%\n\n")
                
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
                
                f.write(f"\n## V4 하이브리드 개선사항\n\n")
                f.write(f"- Part 파일 기반 안정적 페이지 범위 추출\n")
                f.write(f"- 2단계 하이브리드 접근: 페이지 범위 → 제목 매칭\n")
                f.write(f"- PDF 파싱 제거로 성능 및 안정성 향상\n")
                f.write(f"- 작은 범위에서의 정확한 제목 매칭\n")
                f.write(f"- Level별 마크다운 헤더 자동 적용\n")
                f.write(f"- 상세한 단계별 로깅 및 통계\n")
            
            logger.info(f"V4 하이브리드 추출 리포트 생성: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"리포트 생성 실패: {e}")
            return ""


def main():
    """
    메인 함수 - V4 하이브리드 리프 노드 텍스트 추출 실행 (ID 0-16 범위)
    """
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json"
    part_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/extracted_leaf_nodes_v4"
    
    # 추출기 초기화 (ID 16까지로 제한)
    extractor = HybridLeafNodeExtractorV4(toc_file, part_file, output_dir, max_id=16)
    
    try:
        logger.info("=== 하이브리드 리프 노드 텍스트 추출 V4 시작 (ID 0-16) ===")
        
        # 1. TOC 데이터 로드
        if not extractor.load_toc_data():
            logger.error("TOC 데이터 로드 실패로 종료")
            return
        
        # 2. Part 파일 로드
        if not extractor.load_part_file():
            logger.error("Part 파일 로드 실패로 종료")
            return
        
        # 3. 하이브리드 방식 리프 노드 처리
        logger.info("하이브리드 방식 리프 노드 추출 시작")
        saved_files = extractor.process_hybrid_extraction()
        
        # 4. 결과 리포트 생성
        report_file = extractor.generate_extraction_report_v4(saved_files)
        
        # 5. 최종 결과 출력
        logger.info(f"=== V4 하이브리드 추출 완료 ===")
        logger.info(f"범위 내 리프 노드: {extractor.stats['leaf_nodes_in_range']}")
        logger.info(f"성공: {extractor.stats['successful_extractions']}")
        logger.info(f"실패: {extractor.stats['failed_extractions']}")
        logger.info(f"빈 콘텐츠: {extractor.stats['empty_content']}")
        logger.info(f"페이지 범위 실패: {extractor.stats['page_range_failures']}")
        logger.info(f"제목 매칭 성공: {extractor.stats['title_match_successes']}")
        logger.info(f"제목 매칭 실패: {extractor.stats['title_match_failures']}")
        
        success_rate = (extractor.stats['successful_extractions']/max(1, extractor.stats['leaf_nodes_in_range']))*100
        title_match_rate = (extractor.stats['title_match_successes']/max(1, extractor.stats['title_match_successes'] + extractor.stats['title_match_failures']))*100
        
        logger.info(f"성공률: {success_rate:.1f}%")
        logger.info(f"제목 매칭 성공률: {title_match_rate:.1f}%")
        logger.info(f"결과 디렉토리: {output_dir}")
        
    except Exception as e:
        logger.error(f"V4 하이브리드 추출 과정에서 치명적 오류 발생: {e}")


if __name__ == "__main__":
    main()