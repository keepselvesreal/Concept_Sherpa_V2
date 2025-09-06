# 생성 시간: Thu Sep  4 17:33:39 KST 2025
# 핵심 내용: 1단계 기본 작업 준비 프로세서 (logger_v2 및 최신 서비스 반영)
# 상세 내용:
#   - WorkspacePreparationStage (라인 17-325): 메인 워크스페이스 준비 클래스
#   - process (라인 26-110): 메인 처리 로직 (6단계 순차 진행)
#   - extract_toc_from_pdf (라인 112-125): PDF 목차 추출
#   - setup_book_logger (라인 127-158): 책별 로거 설정 (Logger 클래스 사용)
#   - create_output_directories (라인 160-178): 출력 디렉토리 생성
#   - save_toc_file (라인 180-192): 목차 파일 저장
#   - analyze_chapters_with_ai (라인 194-209): AI 기반 장 분석
#   - create_chapter_folders (라인 211-260): 장별 폴더 생성
# 상태: active
# 참조: workspace_preparation.py (LoggerFactory → Logger 클래스로 업데이트)

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# 기본 클래스와 서비스 임포트
sys.path.append(str(Path(__file__).parent.parent))
from core.base.base_processor import BaseProcessor
from services.ai_service_v3 import AIService
from services.toc_service import TocService  
from services.chapter_extraction_service_v3 import ChapterExtractionService
from utils.logger_v2 import Logger

class WorkspacePreparationStage(BaseProcessor):
    """1단계: 기본 작업 준비 프로세서"""
    
    def __init__(self, config_manager, logger_factory):
        super().__init__(config_manager, logger_factory, "workspace_preparation")
        self.ai_service = None
        self.toc_service = None
        self.chapter_extraction_service = None
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
            
            # Step 1: 기본 서비스 초기화 (임시)
            self.log_step("🔧 기본 서비스 초기화 중...")
            temp_logger = Logger("temp_book", logs_base_dir="./logs")
            
            # TocService만 먼저 초기화
            self.toc_service = TocService(self.config_manager, temp_logger)
            
            # Step 2: PDF 목차 추출
            self.log_step("📖 PDF 목차 추출 중...")
            toc_data = await self.extract_toc_from_pdf(pdf_path)
            if not toc_data.get('success'):
                return self.handle_error(Exception(toc_data.get('error', '목차 추출 실패')), "PDF 목차 추출")
            
            # Step 3: 책 제목 추출 및 로거 설정
            self.log_step("📋 책별 로거 설정 중...")
            toc_structure = toc_data['data']['toc_structure']
            self.book_title = toc_structure[0]['title'] if toc_structure else "Unknown_Book"
            logger = await self.setup_logger(self.book_title)
            self.logger = logger
            
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
                'normalized_book_title': self.normalized_book_title,
                'total_chapters': len(chapters_analysis['chapters_info']),
                'output_directory': str(directories['book_dir']),
                'created_folders': created_folders
            }
            
        except Exception as e:
            return self.handle_error(e, "워크스페이스 준비")
            
    async def extract_toc_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """PDF 목차 추출 (TocService 사용)"""
        try:
            toc_data = self.toc_service.extract_complete_toc(pdf_path)
            return {'success': True, 'data': toc_data}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def setup_logger(self, book_title: str) -> Logger:
        """책별 로거 설정 (Logger 클래스 사용)"""
        # 🔴 유틸리티 함수 사용
        from utils.text_utils import normalize_title
        self.normalized_book_title = normalize_title(book_title)
        
        # 로그 기본 디렉토리
        logs_base_dir = self.config_manager.get("global.logs_base_dir", "./logs")
        
        # Logger 생성
        logger = Logger(
            project_name=book_title,
            logs_base_dir=logs_base_dir  # 로그 저장 경로
        )
        
        # 서비스들 초기화
        self.ai_service = AIService(self.config_manager, logger, "workspace_preparation")
        self.toc_service = TocService(self.config_manager, logger)
        self.chapter_extraction_service = ChapterExtractionService(self.config_manager, logger)
        
        return logger
        
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
        """AI 기반 장 분석 (ChapterExtractionService 사용)"""
        try:
            # ChapterExtractionService의 내장 AI 서비스 사용
            chapters_analysis = await self.chapter_extraction_service.count_chapters_with_ai(toc_filepath)
            
            if chapters_analysis['success']:
                chapters_count = len(chapters_analysis['chapters_info'])
                self.log_step(f"AI 분석 결과: {chapters_count}개 실제 장 식별")
                
            return chapters_analysis
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def create_chapter_folders(self, chapters_info: List[Dict], toc_structure: List[Dict], book_dir: Path, pdf_path: str) -> List[Dict]:
        """장별 폴더 생성 (Logger.save_result 활용)"""
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
                
                # 서비스들 활용해서 폴더 생성
                chapter_items = self.chapter_extraction_service.find_chapter_items(toc_structure, chapter_item['id'], next_chapter_start_id)
                chapter_content = self.chapter_extraction_service.extract_pdf_content(pdf_path, chapter_info['start_page'], chapter_info['end_page'])
                
                chapter_folder_path = self.chapter_extraction_service.save_chapter_content_to_folder(
                    chapter_title, chapter_items, chapter_content, book_dir
                )
                
                # 파일 경로들 구성
                from utils.text_utils import normalize_title
                normalized_title = normalize_title(chapter_title)
                chapter_folder = Path(chapter_folder_path) if chapter_folder_path else book_dir / f"{normalized_title}"
                chapter_toc_filepath = chapter_folder / f"{normalized_title}_toc.json" 
                content_filepath = chapter_folder / f"{normalized_title}_content.md"
                
                created_folders.append({
                    'normalized_title': normalize_title(chapter_title),
                    'folder_path': str(chapter_folder),
                    'items_count': len(chapter_items),
                    'toc_file': str(chapter_toc_filepath),
                    'content_file': str(content_filepath) if content_filepath else None
                })
                
                self.log_step(f"✅ 장 {chapter_number} 완료: {normalize_title(chapter_title)}")
                
            except Exception as chapter_error:
                self.log_step(f"❌ 장 {chapter_number} 처리 중 오류: {chapter_error}", "error")
                continue
                
        return created_folders