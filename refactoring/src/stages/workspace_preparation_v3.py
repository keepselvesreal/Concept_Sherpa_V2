# 생성 시간: Tue Sep  9 22:36:23 KST 2025
# 핵심 내용: 1단계 기본 작업 준비 프로세서 - 메모리 기반 처리 (파일/폴더 생성 제거)
# 상세 내용:
#   - WorkspacePreparationStage (라인 25-180): 메인 워크스페이스 준비 클래스
#   - process (라인 43-118): 메인 처리 로직 (메모리 기반, 3단계 진행)
#   - extract_toc_from_pdf (라인 120-133): PDF 목차 추출
#   - analyze_chapters_with_ai (라인 135-151): AI 기반 장 분석 (v4 서비스 사용)
#   - _extract_chapter_toc_items (라인 192-252): 장별 목차 항목 추출 메서드 (chapters_info 기반 정확한 범위 추출)
#   - _validate_chapter_page_ranges (라인 254-292): AI 분석 페이지 범위와 목차 페이지 범위 비교 검증
# 상태: active
# 참조: workspace_preparation_v2.py (메모리 기반 처리로 완전 개편, ChapterExtractionService_v4 사용)

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 기본 클래스와 서비스 임포트
sys.path.append(str(Path(__file__).parent.parent))
from core.base.base_processor import BaseProcessor
from services.toc_service import TocService  
from services.chapter_extraction_service_v4 import ChapterExtractionService
from utils.logger_v2 import Logger
from utils.text_utils import normalize_title

class WorkspacePreparationStage(BaseProcessor):
    """1단계: 메모리 기반 워크스페이스 준비 프로세서"""
    
    def __init__(self, config_manager, logger_factory):
        super().__init__(config_manager, logger_factory, "workspace_preparation")
        self.toc_service = None
        self.chapter_extraction_service = None
        self.book_title = None
        self.normalized_book_title = None
        
    async def process(self, stage_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        메모리 기반 워크스페이스 준비 처리
        
        Args:
            stage_input: {'data': {'pdf_path': str}, 'error': str}
            
        Returns:
            Dict: {'data': dict, 'error': str}
        """
        try:
            # 입력 데이터에서 error 체크
            if stage_input.get('error'):
                return {
                    'data': None,
                    'error': stage_input['error']
                }
            
            input_data = stage_input.get('data', {})
            pdf_path = input_data.get('pdf_path')
            if not pdf_path or not os.path.exists(pdf_path):
                return {
                    'data': None,
                    'error': "유효하지 않은 PDF 경로"
                }
            
            self.log_step("1단계 메모리 기반 워크스페이스 준비 시작", "info")
            
            # 🟢 Step 1: PDF 목차 추출 (메모리에 저장)
            self.log_step("📖 PDF 목차 추출 중...")
            toc_data = await self.extract_toc_from_pdf(pdf_path)
            if not toc_data.get('success'):
                return {
                    'data': None,
                    'error': toc_data.get('error', '목차 추출 실패')
                }
            
            # 책 제목 추출 및 정규화
            toc_structure = toc_data['data']['toc_structure']
            self.book_title = toc_structure[0]['title'] if toc_structure else "Unknown_Book"
            self.normalized_book_title = normalize_title(self.book_title)
            
            self.log_step(f"📋 책 제목 설정: {self.book_title}")
            
            # 🟢 Step 2: AI 기반 장 분석 (실제 목차 데이터 전달)
            self.log_step("🤖 AI 기반 장 분석 중...")
            chapters_analysis_result = await self.analyze_chapters_with_ai(toc_data['data'])
            if not chapters_analysis_result.get('success'):
                return {
                    'data': None,
                    'error': chapters_analysis_result.get('error', 'AI 분석 실패')
                }
            
            # 🟢 Step 3: 장별 콘텐츠 추출 (메모리에 저장)
            # 장 선택 설정 확인 및 필터링
            chapter_selection_config = self.config_manager.pipeline_config.get('workspace_preparation', {}).get('chapter_selection', {})
            selection_mode = chapter_selection_config.get('mode', 'all')
            selected_chapters = chapter_selection_config.get('selected_chapters', [])
            
            individual_chapter_information = chapters_analysis_result['individual_chapter_information']
            
            # 장 선택에 따른 필터링
            if selection_mode == 'partial' and selected_chapters:
                # 선택된 장만 필터링 (1-based index를 0-based로 변환)
                individual_chapter_information = [
                    chapter_info for i, chapter_info in enumerate(individual_chapter_information)
                    if (i + 1) in selected_chapters
                ]
                self.log_step(f"📄 선택된 장 콘텐츠 추출 중... (장 {selected_chapters})")
            else:
                self.log_step("📄 장별 콘텐츠 추출 중...")
            
            chapters_data = []
            
            for i, chapter_info in enumerate(individual_chapter_information):
                chapter_title = chapter_info['title']
                
                content_text = self.chapter_extraction_service.extract_pdf_content(
                    pdf_path, chapter_info['start_page'], chapter_info['end_page']
                )
                
                # 해당 장의 목차 항목들 추출 (현재 장과 다음 장 사이의 항목들)
                chapter_toc = self._extract_chapter_toc_items(
                    toc_data['data']['toc_structure'], 
                    chapter_title,
                    individual_chapter_information,
                    i
                )
                
                # 🟢 새로 추가: AI 분석 페이지 범위와 실제 목차 페이지 범위 검증
                self._validate_chapter_page_ranges(chapter_info, chapter_toc, i)
                
                chapters_data.append({
                    'chapter_title': chapter_title,
                    'chapter_toc': chapter_toc,  # 🟢 수정: chapter_toc로 변경
                    'content_text': content_text,
                    'metadata': {
                        'start_page': chapter_info['start_page'],
                        'end_page': chapter_info['end_page']
                    }
                })
            
            if selection_mode == 'partial' and selected_chapters:
                self.log_step(f"✅ 메모리 기반 워크스페이스 준비 완료: {len(chapters_data)}개 장 (선택: {selected_chapters})")
            else:
                self.log_step(f"✅ 메모리 기반 워크스페이스 준비 완료: {len(chapters_data)}개 장")
            
            return {
                'data': {
                    'book_information': {
                        'title': self.book_title,
                        'normalized_title': self.normalized_book_title,
                        'chapter_titles': [chapter['title'] for chapter in individual_chapter_information]
                    },
                    'raw_toc_data': toc_data['data'],
                    'chapters_data': chapters_data
                },
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"워크스페이스 준비 실패: {str(e)}")
            return {
                'data': None,
                'error': str(e)
            }

    async def extract_toc_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """PDF 목차 추출"""
        if not self.toc_service:
            temp_logger = Logger("temp_toc", logs_base_dir="./logs")
            self.toc_service = TocService(self.config_manager, temp_logger)
        
        try:
            # 🟢 올바른 메서드명 사용: extract_complete_toc
            toc_result = self.toc_service.extract_complete_toc(pdf_path)
            
            # TOC 추출 성공 여부 확인 (toc_structure가 있고 비어있지 않으면 성공)
            if toc_result and 'toc_structure' in toc_result and len(toc_result['toc_structure']) > 0:
                return {
                    'success': True,
                    'data': toc_result,
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'error': 'TOC 구조가 비어있거나 추출 실패'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'data': None,
                'error': f"TOC 추출 중 오류: {str(e)}"
            }
        
    async def analyze_chapters_with_ai(self, toc_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI 기반 장 분석 (메모리 내 목차 데이터 직접 사용)"""
        try:
            # ChapterExtractionService_v4 초기화
            if not self.chapter_extraction_service:
                temp_logger = Logger("temp_chapter", logs_base_dir="./logs")
                self.chapter_extraction_service = ChapterExtractionService(self.config_manager, temp_logger)
            
            # 🟢 메모리 내 데이터 직접 AI에 전달 (기존처럼 파일 경로가 아닌 데이터 직접 전달)
            # 임시 파일 생성해서 기존 메서드 재활용
            temp_toc_file = Path("./logs/temp_toc.json")
            temp_toc_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(temp_toc_file, 'w', encoding='utf-8') as f:
                json.dump(toc_data, f, ensure_ascii=False, indent=2)
            
            chapters_analysis = await self.chapter_extraction_service.count_chapters_with_ai(str(temp_toc_file))
            
            # 임시 파일 정리
            if temp_toc_file.exists():
                temp_toc_file.unlink()
                
            return chapters_analysis
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _extract_chapter_toc_items(self, full_toc_structure: List[Dict], chapter_title: str, chapters_info: List[Dict], current_chapter_index: int) -> List[Dict]:
        """
        해당 장에 속하는 목차 항목들만 추출
        
        Args:
            full_toc_structure: 전체 목차 구조
            chapter_title: 장 제목 (예: "1 Introduction")
            chapters_info: 전체 장 정보 리스트
            current_chapter_index: 현재 장의 인덱스
            
        Returns:
            List[Dict]: 해당 장의 목차 항목들
        """
        # 목차에서 해당 장 항목 찾기
        chapter_item = None
        for item in full_toc_structure:
            if item['title'] == chapter_title:
                chapter_item = item
                break
        
        if not chapter_item:
            error_msg = f"목차에서 해당 장을 찾을 수 없음: {chapter_title}"
            print(f"⚠️ {error_msg}")
            if self.logger:
                self.logger.warning(error_msg)
            return []
        
        # 다음 장 시작점 찾기
        next_chapter_start_id = None
        if current_chapter_index + 1 < len(chapters_info):
            next_chapter_title = chapters_info[current_chapter_index + 1]['title']
            for item in full_toc_structure:
                if item['title'] == next_chapter_title:
                    next_chapter_start_id = item['id']
                    break
        
        try:
            # 해당 장의 모든 하위 항목들 수집
            chapter_items = self.chapter_extraction_service.find_chapter_items(
                full_toc_structure, 
                chapter_item['id'], 
                next_chapter_start_id
            )
            
            if self.logger:
                self.logger.info(f"장별 목차 추출 완료 ({chapter_title}): {len(chapter_items)}개 항목")
            
            return chapter_items
            
        except Exception as e:
            error_msg = f"장별 목차 추출 실패 ({chapter_title}): {str(e)}"
            print(f"⚠️ {error_msg}")
            if self.logger:
                self.logger.error(error_msg)
            return []

    def _validate_chapter_page_ranges(self, chapter_info: Dict, chapter_toc: List[Dict], chapter_index: int):
        """
        AI 분석 페이지 범위와 실제 목차 페이지 범위 비교 검증
        
        Args:
            chapter_info: AI가 분석한 장 정보 (start_page, end_page 포함)
            chapter_toc: 추출된 장 목차 항목들
            chapter_index: 장 인덱스 (로깅용)
        """
        if not chapter_toc:
            return
        
        # AI 분석 결과
        ai_start_page = chapter_info['start_page']
        ai_end_page = chapter_info['end_page']
        chapter_title = chapter_info['title']
        
        # 목차 첫 번째 항목의 실제 페이지 범위
        first_toc_item = chapter_toc[0]
        actual_start_page = first_toc_item.get('start_page', first_toc_item.get('page'))
        actual_end_page = first_toc_item.get('end_page')
        
        # 페이지 범위 불일치 검사
        warnings = []
        
        if actual_start_page and ai_start_page != actual_start_page:
            warnings.append(f"시작 페이지 불일치: AI={ai_start_page} vs TOC={actual_start_page}")
        
        if actual_end_page and ai_end_page != actual_end_page:
            warnings.append(f"종료 페이지 불일치: AI={ai_end_page} vs TOC={actual_end_page}")
        
        # 경고 출력
        if warnings:
            print(f"⚠️ [{chapter_index+1}장] {chapter_title}")
            for warning in warnings:
                print(f"   📄 {warning}")
            
            if self.logger:
                self.logger.warning(f"장 {chapter_index+1} 페이지 범위 불일치: {', '.join(warnings)}")