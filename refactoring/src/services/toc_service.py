# 생성 시간: Thu Sep  4 08:17:51 KST 2025
# 핵심 내용: PDF 목차 추출 서비스 (기존 toc_extractor 로직을 새 아키텍처로 이관)
# 상세 내용:
#   - TocService (라인 20-210): 목차 추출 서비스 메인 클래스
#   - __init__ (라인 25-31): 의존성 주입 (config_manager, logger)
#   - extract_toc_structure (라인 33-85): PyMuPDF로 기본 목차 구조 추출 (기존 extract_toc_with_pymupdf 로직)
#   - process_toc_hierarchy (라인 87-130): 부모-자식 관계 설정 (기존 process_toc_items 로직)
#   - calculate_toc_page_ranges (라인 132-175): 페이지 범위 계산 (기존 calculate_page_ranges 로직)
#   - extract_complete_toc (라인 177-210): 전체 워크플로우 실행 메서드
# 상태: active
# 주소: services/toc_service
# 참조: /home/nadle/projects/Knowledge_Sherpa/v2/inbox/25-08-30/toc_extractor.py

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("⚠️  PyMuPDF가 설치되지 않음. 'uv add PyMuPDF'를 실행하세요")
    fitz = None

class TocService:
    """PDF 목차 추출 서비스 - 기존 toc_extractor 로직을 새 아키텍처로 이관"""
    
    def __init__(self, config_manager, logger):
        """
        의존성 주입으로 초기화
        Args:
            config_manager: 설정 관리자
            logger: 로거 인스턴스
        """
        self.config_manager = config_manager
        self.logger = logger

    def extract_toc_structure(self, pdf_path: str) -> List[Dict]:
        """
        PyMuPDF를 사용하여 기본 목차 구조 추출 
        (기존 extract_toc_with_pymupdf 로직 이관)
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            List[Dict]: 기본 목차 항목 리스트
        """
        if fitz is None:
            self.logger.error("PyMuPDF가 설치되지 않아 목차 추출을 할 수 없습니다")
            return []
            
        toc_items = []
        
        try:
            # PDF 열기
            doc = fitz.open(pdf_path)
            self.logger.info(f"전체 페이지 수: {doc.page_count}")
            
            # 목차(Table of Contents) 추출
            toc = doc.get_toc(simple=False)  # simple=False로 완전한 정보 가져오기
            self.logger.info(f"발견된 TOC 항목: {len(toc)}개")
            
            if not toc:
                self.logger.warning("PDF에서 목차 정보를 찾을 수 없습니다")
                doc.close()
                return []
            
            # TOC 항목 처리
            for i, item in enumerate(toc):
                try:
                    # PyMuPDF TOC 형식: [level, title, page, destination_dict]
                    if len(item) >= 3:
                        level = item[0] - 1  # PyMuPDF는 1부터 시작하므로 0부터 시작하도록 조정
                        title = item[1].strip()
                        page = item[2]  # PyMuPDF는 이미 1부터 시작하는 페이지 번호
                        
                        # 유효성 검사
                        if title and page > 0:
                            toc_item = {
                                'id': i,
                                'title': title,
                                'level': max(0, level),  # 음수 레벨 방지
                                'page': page,
                                'parent_id': None,  # 나중에 설정
                                'children_ids': []
                            }
                            
                            toc_items.append(toc_item)
                            self.logger.debug(f"Level {level}: {title} (page {page})")
                        
                except Exception as e:
                    self.logger.error(f"TOC 항목 {i} 처리 오류: {e}")
                    continue
            
            doc.close()
            self.logger.info(f"목차 구조 추출 완료: {len(toc_items)}개 항목")
            
        except Exception as e:
            self.logger.error(f"PDF 처리 오류: {e}")
            return []
        
        return toc_items

    def process_toc_hierarchy(self, toc_items: List[Dict]) -> List[Dict]:
        """
        목차 항목의 부모-자식 관계 설정 
        (기존 process_toc_items 로직 이관)
        
        Args:
            toc_items: 기본 목차 항목 리스트
            
        Returns:
            List[Dict]: 부모-자식 관계가 설정된 목차 항목 리스트
        """
        if not toc_items:
            return []
        
        self.logger.info("목차 항목 처리 및 관계 설정 시작")
        
        # 레벨별 통계
        level_stats = {}
        for item in toc_items:
            level = item['level']
            level_stats[level] = level_stats.get(level, 0) + 1
        
        self.logger.info("추출된 레벨별 통계:")
        for level in sorted(level_stats.keys()):
            self.logger.info(f"  Level {level}: {level_stats[level]}개 항목")
        
        # 부모-자식 관계 설정
        for i, item in enumerate(toc_items):
            current_level = item['level']
            
            # 부모 찾기: 이전 항목들 중 레벨이 정확히 하나 낮은 가장 가까운 항목
            parent_id = None
            for j in range(i - 1, -1, -1):
                if toc_items[j]['level'] == current_level - 1:
                    parent_id = toc_items[j]['id']
                    break
            
            item['parent_id'] = parent_id
            
            # 부모의 자식 리스트에 추가
            if parent_id is not None:
                toc_items[parent_id]['children_ids'].append(item['id'])
        
        # 계층 구조 검증
        root_items = [item for item in toc_items if item['parent_id'] is None]
        self.logger.info(f"최상위 항목: {len(root_items)}개")
        
        return toc_items

    def calculate_toc_page_ranges(self, toc_items: List[Dict]) -> List[Dict]:
        """
        각 목차 항목의 페이지 범위 계산 
        (기존 calculate_page_ranges 로직 이관)
        
        Args:
            toc_items: 부모-자식 관계가 설정된 목차 항목 리스트
            
        Returns:
            List[Dict]: 페이지 범위가 계산된 완전한 목차 항목 리스트
        """
        if not toc_items:
            return []
        
        self.logger.info("페이지 범위 계산 시작")
        enhanced_items = []
        
        for i, item in enumerate(toc_items):
            enhanced_item = item.copy()
            start_page = item['page']
            current_level = item['level']
            
            # 끝 페이지 찾기 로직
            end_page = None
            
            # 다음 항목들 검사
            for j in range(i + 1, len(toc_items)):
                next_item = toc_items[j]
                next_level = next_item['level']
                
                # 같은 레벨이거나 상위 레벨인 경우 → 현재 섹션 종료
                if next_level <= current_level:
                    end_page = next_item['page'] - 1
                    break
            
            # 적절한 끝 페이지를 찾지 못한 경우 기본값 설정
            if end_page is None:
                # 레벨에 따른 기본 페이지 수
                if current_level == 0:  # Part, Appendix 등
                    end_page = start_page + 50
                elif current_level == 1:  # Chapter
                    end_page = start_page + 25
                elif current_level == 2:  # Section
                    end_page = start_page + 8
                else:  # Subsection
                    end_page = start_page + 3
                
                # 마지막 항목인 경우 더 보수적으로
                if i == len(toc_items) - 1:
                    end_page = start_page + 2
            
            # 최소 1페이지 보장
            if end_page < start_page:
                end_page = start_page
            
            enhanced_item.update({
                'start_page': start_page,
                'end_page': end_page,
                'page_count': end_page - start_page + 1
            })
            
            enhanced_items.append(enhanced_item)
        
        self.logger.info(f"페이지 범위 계산 완료: {len(enhanced_items)}개 항목")
        return enhanced_items

    def extract_complete_toc(self, pdf_path: str) -> Dict[str, Any]:
        """
        완전한 목차 추출 (전체 워크플로우 실행)
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            Dict[str, Any]: extraction_info와 toc_structure를 포함한 완전한 목차 데이터
        """
        try:
            # Step 1: 기본 목차 구조 추출
            raw_toc_items = self.extract_toc_structure(pdf_path)
            
            if not raw_toc_items:
                self.logger.error("목차 구조 추출 실패")
                return {'extraction_info': {}, 'toc_structure': []}
            
            # Step 2: 부모-자식 관계 처리
            processed_items = self.process_toc_hierarchy(raw_toc_items)
            
            # Step 3: 페이지 범위 계산
            complete_items = self.calculate_toc_page_ranges(processed_items)
            
            # 완전한 목차 데이터 구성
            complete_toc_data = {
                "extraction_info": {
                    "source_pdf": os.path.basename(pdf_path),
                    "extraction_method": "PyMuPDF complete TOC extraction with hierarchy",
                    "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                    "total_items": len(complete_items),
                    "note": "Complete hierarchy extracted using PyMuPDF library"
                },
                "toc_structure": complete_items
            }
            
            self.logger.info(f"완전한 목차 추출 완료: {len(complete_items)}개 항목")
            return complete_toc_data
            
        except Exception as e:
            self.logger.error(f"완전한 목차 추출 중 오류: {e}")
            return {'extraction_info': {}, 'toc_structure': []}