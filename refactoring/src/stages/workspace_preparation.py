# 생성 시간: Mon Sep  3 17:09:40 KST 2025
# 핵심 내용: 1단계 기본 작업 준비 프로세서 (원본 prepare_chapter_workspace 로직 모듈화)
# 상세 내용:
#   - WorkspacePreparationStage (라인 16-184): 메인 워크스페이스 준비 클래스
#   - process (라인 25-74): 메인 처리 로직 (6단계 순차 진행)
#   - extract_toc_from_pdf (라인 76-99): PDF 목차 추출
#   - setup_book_logger (라인 101-118): 책별 로거 설정
#   - create_output_directories (라인 120-138): 출력 디렉토리 생성
#   - save_toc_file (라인 140-152): 목차 파일 저장
#   - analyze_chapters_with_ai (라인 154-169): AI 기반 장 분석
#   - create_chapter_folders (라인 171-184): 장별 폴더 생성
# 상태: active

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# 기본 클래스와 서비스 임포트
from ..core.base.base_processor import BaseProcessor
from ..services.ai_service import AIService

# 기존 검증된 모듈들 임포트 (원본 경로 유지)
import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31')
from toc_extractor import extract_toc_with_pymupdf, process_toc_items, calculate_page_ranges
from extract_chapters_v5 import count_chapters_with_ai, GeminiAPIProvider, normalize_title, extract_pdf_content, find_chapter_items, save_chapter_content_to_folder

class WorkspacePreparationStage(BaseProcessor):
    """1단계: 기본 작업 준비 프로세서"""
    
    def __init__(self, config_manager, logger_factory):
        super().__init__(config_manager, logger_factory, "workspace_preparation")
        self.ai_service = None
        self.book_title = None
        self.normalized_book_title = None
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        메인 워크스페이스 준비 처리
        
        Args:
            input_data: {'pdf_path': str}
            
        Returns:
            Dict: 처리 결과
        """
        try:
            pdf_path = input_data.get('pdf_path')
            if not pdf_path or not os.path.exists(pdf_path):
                return self.handle_error(ValueError("유효하지 않은 PDF 경로"), "입력 검증")
            
            self.log_step("1단계 기본 작업 준비 시작", "info")
            
            # Step 1: PDF 목차 추출
            self.log_step("📖 PDF 목차 추출 중...")
            toc_data = await self.extract_toc_from_pdf(pdf_path)
            if not toc_data.get('success'):
                return self.handle_error(Exception(toc_data.get('error', '목차 추출 실패')), "PDF 목차 추출")
            
            # Step 2: 책 제목 추출 및 로거 설정
            self.log_step("📋 책별 로거 설정 중...")
            toc_structure = toc_data['data']['toc_structure']
            self.book_title = toc_structure[0]['title'] if toc_structure else "Unknown_Book"
            book_logger = await self.setup_book_logger(self.book_title)
            self.logger = book_logger
            
            # Step 3: 출력 디렉토리 생성
            self.log_step("📁 출력 디렉토리 설정 중...")
            directories = await self.create_output_directories()
            
            # Step 4: 목차 파일 저장
            self.log_step("💾 목차 파일 저장 중...")
            toc_filepath = await self.save_toc_file(toc_data['data'], directories['book_dir'])
            
            # Step 5: AI 기반 장 분석
            self.log_step("🤖 AI 기반 장 분석 중...")
            chapters_analysis = await self.analyze_chapters_with_ai(str(toc_filepath))
            if not chapters_analysis.get('success'):
                return self.handle_error(Exception(chapters_analysis.get('error', 'AI 분석 실패')), "AI 장 분석")
            
            # Step 6: 장별 폴더 생성
            self.log_step("📂 장별 폴더 생성 중...")
            created_folders = await self.create_chapter_folders(
                chapters_analysis['chapters_info'], 
                toc_structure, 
                directories['book_dir'], 
                pdf_path
            )
            
            # 성공 결과 반환
            success_count = len(created_folders)
            self.log_step(f"🎉 워크스페이스 준비 완료! {success_count}개 장 폴더 생성", "info")
            
            return {
                'success': True,
                'book_title': self.book_title,
                'normalized_book_title': self.normalized_book_title,
                'book_folder': str(directories['book_dir']),
                'toc_file': str(toc_filepath),
                'total_chapters': len(chapters_analysis['chapters_info']),
                'created_folders': created_folders,
                'output_directory': str(directories['book_dir'])
            }
            
        except Exception as e:
            return self.handle_error(e, "워크스페이스 준비")
            
    async def extract_toc_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """PDF 목차 추출 (기존 로직 이관)"""
        try:
            raw_toc = extract_toc_with_pymupdf(pdf_path)
            if not raw_toc:
                return {'success': False, 'error': '목차 추출 실패'}
            
            processed_toc = process_toc_items(raw_toc)
            complete_toc = calculate_page_ranges(processed_toc)
            
            toc_data = {
                "extraction_info": {
                    "source_pdf": os.path.basename(pdf_path),
                    "extraction_method": "PyMuPDF complete TOC extraction with hierarchy",
                    "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                    "total_items": len(complete_toc),
                    "note": "Complete hierarchy extracted using PyMuPDF library"
                },
                "toc_structure": complete_toc
            }
            
            return {'success': True, 'data': toc_data}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def setup_book_logger(self, book_title: str):
        """책별 로거 설정"""
        self.normalized_book_title = normalize_title(book_title)
        
        # 로그 기본 디렉토리
        logs_base_dir = self.config_manager.get("global.logs_base_dir", "./logs")
        
        # 책별 로거 생성
        book_logger = self.logger_factory.create_book_logger(book_title, logs_base_dir)
        
        # AI 서비스 초기화 (단계별 설정)
        self.ai_service = AIService(self.config_manager, book_logger, "workspace_preparation")
        
        return book_logger
        
    async def create_output_directories(self) -> Dict[str, Path]:
        """출력 디렉토리 생성"""
        base_path = self.config_manager.get("workspace_preparation.folder_structure.base_path", "./output")
        output_dir = Path(base_path)
        book_dir = output_dir / self.normalized_book_title
        book_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_step(f"책 폴더 생성: {self.normalized_book_title}")
        
        return {
            'output_dir': output_dir,
            'book_dir': book_dir
        }
        
    async def save_toc_file(self, toc_data: Dict[str, Any], book_dir: Path) -> Path:
        """목차 파일 저장"""
        toc_filepath = book_dir / "toc.json"
        
        with open(toc_filepath, 'w', encoding='utf-8') as f:
            json.dump(toc_data, f, ensure_ascii=False, indent=2)
            
        self.log_step(f"목차 파일 저장: {toc_filepath}")
        return toc_filepath
        
    async def analyze_chapters_with_ai(self, toc_filepath: str) -> Dict[str, Any]:
        """AI 기반 장 분석 (기존 로직 활용)"""
        try:
            # 기존 AI 제공자 방식 사용 (호환성 유지)
            # TODO: 향후 ai_service로 완전 이관
            ai_provider = GeminiAPIProvider(self.logger)
            chapters_analysis = await count_chapters_with_ai(toc_filepath, ai_provider, self.logger)
            
            if chapters_analysis['success']:
                chapters_count = len(chapters_analysis['chapters_info'])
                self.log_step(f"AI 분석 결과: {chapters_count}개 실제 장 식별")
                
            return chapters_analysis
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def create_chapter_folders(self, chapters_info: List[Dict], toc_structure: List[Dict], book_dir: Path, pdf_path: str) -> List[Dict]:
        """장별 폴더 생성 (기존 로직 이관, selected_chapters 고려)"""
        created_folders = []
        
        # 테스트 모드 설정 확인
        test_config = self.config_manager.get_test_config()
        is_test_mode = test_config.get("enabled", False)
        
        for i, chapter_info in enumerate(chapters_info):
            chapter_number = i + 1
            chapter_title = chapter_info['title']
            
            # 테스트 모드에서 선택된 장만 처리
            if is_test_mode and not self.config_manager.is_chapter_selected(chapter_number):
                self.log_step(f"⏭️ 장 {chapter_number} 건너뜀 (테스트 모드 - 선택되지 않은 장)")
                continue
                
            self.log_step(f"장 {chapter_number} 폴더 생성: {chapter_title}")
            
            try:
                # 기존 로직 사용 (목차에서 해당 장 찾기 → 폴더 생성)
                # TODO: 이 부분도 서비스로 분리 가능
                chapter_item = None
                for item in toc_structure:
                    if item['title'] == chapter_title:
                        chapter_item = item
                        break
                        
                if not chapter_item:
                    self.log_step(f"⚠️ 목차에서 해당 장을 찾을 수 없음: {chapter_title}", "warning")
                    continue
                
                # 다음 장 시작점 찾기
                next_chapter_start_id = None
                if i + 1 < len(chapters_info):
                    next_chapter_title = chapters_info[i + 1]['title']
                    for item in toc_structure:
                        if item['title'] == next_chapter_title:
                            next_chapter_start_id = item['id']
                            break
                
                # 기존 함수들 활용해서 폴더 생성
                chapter_items = find_chapter_items(toc_structure, chapter_item['id'], next_chapter_start_id, self.logger)
                chapter_content = extract_pdf_content(pdf_path, chapter_info['start_page'], chapter_info['end_page'], self.logger)
                
                chapter_toc_filepath, content_filepath = save_chapter_content_to_folder(
                    chapter_title, chapter_items, chapter_content, book_dir, self.logger
                )
                
                created_folders.append({
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'normalized_title': normalize_title(chapter_title),
                    'folder_path': str(book_dir / normalize_title(chapter_title)),
                    'toc_file': str(chapter_toc_filepath),
                    'content_file': str(content_filepath) if content_filepath else None,
                    'page_range': f"{chapter_info['start_page']}-{chapter_info['end_page']}",
                    'items_count': len(chapter_items)
                })
                
                self.log_step(f"✅ 장 {chapter_number} 완료: {normalize_title(chapter_title)}")
                
            except Exception as chapter_error:
                self.log_step(f"❌ 장 {chapter_number} 처리 중 오류: {chapter_error}", "error")
                continue
                
        return created_folders