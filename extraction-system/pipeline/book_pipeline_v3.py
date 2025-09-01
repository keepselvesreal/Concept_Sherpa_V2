# 생성 시간: Mon Sep  1 16:50:39 KST 2025
# 핵심 내용: PDF/EPUB → 통합 노드 문서 생성 파이프라인 v3 (2단계: 장별정보처리준비 → 각장의정보통합)
# 상세 내용:
#   - BookPipeline (라인 20-600): 메인 파이프라인 클래스
#   - setup_logging_system (라인 70-120): 책별 로그 시스템 설정
#   - prepare_chapter_workspace (라인 121-280): 1단계 - 장별 정보 처리 준비
#   - integrate_chapter_information_sequentially (라인 281-450): 2단계 - 각 장의 정보 통합  
#   - integrate_single_chapter_information (라인 451-550): 개별 장 통합 처리
#   - execute (라인 551-600): 파이프라인 실행 메인 메서드
#   - PipelineResult (라인 50-65): 결과 반환 클래스
# 상태: active
# 주소: book_pipeline/v3
# 참조: book_pipeline/v2

import os
import json
import asyncio
import tempfile
import sys
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 기존 검증된 모듈들 임포트
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30')  # PyMuPDF toc_extractor
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31')

from toc_extractor import extract_toc_with_pymupdf, process_toc_items, calculate_page_ranges
from extract_chapters_v5 import count_chapters_with_ai, GeminiAPIProvider, normalize_title, extract_pdf_content, find_chapter_items, save_chapter_content_to_folder

# 콘텐츠 노드 분석 모듈 임포트
from content_node_analyzer_v2 import ContentNodeAnalyzer
# 노드 문서 생성 모듈 임포트
from node_document_generator import NodeDocumentGenerator
# 문서 통합 모듈 임포트
from document_integrator import DocumentIntegrator

class PipelineResult:
    """파이프라인 실행 결과"""
    def __init__(self):
        self.is_success = False
        self.error = None
        self.data = {}
        self.step_completed = 0
        self.total_steps = 2  # 2단계로 단순화: 장별정보처리준비 → 각장의정보통합
        self.progress_percent = 0

class BookPipeline:
    """PDF/EPUB → 통합 노드 문서 생성 파이프라인 v3"""
    
    def __init__(self, test_mode: bool = False, max_chapters: int = None):
        self.temp_dir = None
        self.output_dir = None
        self.logs_dir = None
        self.book_title = None
        self.normalized_book_title = None
        self.logger = None
        self.test_mode = test_mode
        self.max_chapters = max_chapters if max_chapters else (1 if test_mode else None)
        self.node_document_generator = NodeDocumentGenerator()
        self.document_integrator = DocumentIntegrator()
        
    def setup_logging_system(self, book_title: str) -> None:
        """책별 로그 시스템 설정"""
        try:
            # 책 제목 정규화
            self.book_title = book_title
            self.normalized_book_title = normalize_title(book_title)
            
            # logs 디렉토리 생성
            extraction_system_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system")
            self.logs_dir = extraction_system_dir / "logs" / self.normalized_book_title
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            
            # 로거 설정
            self.logger = logging.getLogger(f'book_pipeline_{self.normalized_book_title}')
            self.logger.setLevel(logging.INFO)
            
            # 기존 핸들러 제거
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
            
            # 파일 핸들러 설정
            log_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # pipeline.log - 전체 진행상황
            pipeline_handler = logging.FileHandler(
                self.logs_dir / 'pipeline.log', 
                encoding='utf-8'
            )
            pipeline_handler.setFormatter(log_formatter)
            self.logger.addHandler(pipeline_handler)
            
            # chapter_integration.log - 장별 통합 처리 상세
            chapter_handler = logging.FileHandler(
                self.logs_dir / 'chapter_integration.log',
                encoding='utf-8'
            )
            chapter_handler.setFormatter(log_formatter)
            
            # processing_errors.log - 정보 처리 관련 모든 에러
            error_handler = logging.FileHandler(
                self.logs_dir / 'processing_errors.log',
                encoding='utf-8'
            )
            error_handler.setFormatter(log_formatter)
            error_handler.setLevel(logging.ERROR)
            self.logger.addHandler(error_handler)
            
            # 콘솔 출력도 유지
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            self.logger.addHandler(console_handler)
            
            self.logger.info(f"로그 시스템 설정 완료: {self.logs_dir}")
            
            # 테스트 모드 정보 기록
            if self.test_mode:
                self.logger.info(f"🧪 테스트 모드 활성화 - 최대 {self.max_chapters}장 처리")
            
        except Exception as e:
            print(f"⚠️ 로그 시스템 설정 실패: {str(e)}")
            # 로그 설정 실패해도 계속 진행
    
    async def prepare_chapter_workspace(self, pdf_path: str) -> Dict[str, Any]:
        """1단계: 장별 정보 처리 준비 (목차 추출 + 장별 폴더 생성 + 로그 설정)"""
        try:
            print("1️⃣ 장별 정보 처리 준비 중... (목차 추출 + 폴더 생성 + 로그 설정)")
            
            # 1-1. PDF 목차 추출
            print("🔄 PDF 목차 추출 중...")
            try:
                raw_toc = extract_toc_with_pymupdf(pdf_path)
                if not raw_toc:
                    raise Exception("목차 추출 실패")
                
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
                
                print(f"✅ 목차 추출 완료: {len(complete_toc)}개 항목")
                
            except Exception as e:
                error_msg = f"PDF 목차 추출 실패: {str(e)}"
                print(f"❌ {error_msg}")
                raise Exception(error_msg)
            
            # 1-2. 책 제목 추출 및 로그 시스템 설정
            toc_structure = toc_data["toc_structure"]
            book_title = toc_structure[0]['title'] if toc_structure else "Unknown_Book"
            self.setup_logging_system(book_title)
            
            if self.logger:
                self.logger.info("=== 장별 정보 처리 준비 시작 ===")
                self.logger.info(f"처리 대상 PDF: {os.path.basename(pdf_path)}")
                self.logger.info(f"추출된 책 제목: {book_title}")
                self.logger.info(f"목차 항목 수: {len(complete_toc)}")
            
            # 1-3. 출력 디렉토리 설정
            extraction_system_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system")
            self.output_dir = extraction_system_dir
            book_dir = self.output_dir / self.normalized_book_title
            book_dir.mkdir(exist_ok=True)
            
            print(f"📖 책 폴더 생성: {self.normalized_book_title}")
            if self.logger:
                self.logger.info(f"책 폴더 생성: {book_dir}")
            
            # 1-4. 목차 파일 저장
            toc_filepath = book_dir / "toc.json"
            with open(toc_filepath, 'w', encoding='utf-8') as f:
                json.dump(toc_data, f, ensure_ascii=False, indent=2)
            print(f"💾 목차 파일 저장: {toc_filepath}")
            
            # 1-5. AI 기반 장 분석 및 폴더 생성
            print("🤖 AI 기반 장 분석 중...")
            if self.logger:
                self.logger.info("AI 기반 장 분석 시작")
            
            # Logger 설정 (기존 로직 호환)
            ai_logger = logging.getLogger('book_pipeline')
            ai_logger.setLevel(logging.INFO)
            
            # Gemini AI 제공자 초기화 (기존 방식으로 복원 - 환경변수 자동 읽기)
            ai_provider = GeminiAPIProvider(ai_logger)
            
            try:
                chapter_analysis = await count_chapters_with_ai(str(toc_filepath), ai_provider, ai_logger)
                
                if not chapter_analysis['success']:
                    error_msg = f"AI 장 분석 실패: {chapter_analysis.get('error', 'Unknown error')}"
                    print(f"⚠️ {error_msg}")
                    if self.logger:
                        self.logger.error(error_msg)
                    
                    # AI 실패 시에도 기본 정보 반환
                    return {
                        'success': False,
                        'book_title': book_title,
                        'normalized_book_title': self.normalized_book_title,
                        'book_folder': str(book_dir),
                        'toc_file': str(toc_filepath),
                        'ai_analysis_failed': True,
                        'error': error_msg,
                        'created_folders': []
                    }
                
                chapters_info = chapter_analysis['chapters_info']
                print(f"📚 AI 분석 결과: {len(chapters_info)}개 실제 장 식별")
                if self.logger:
                    self.logger.info(f"AI 분석 완료: {len(chapters_info)}개 장 식별")
                
            except Exception as ai_error:
                error_msg = f"AI 분석 중 예외 발생: {str(ai_error)}"
                print(f"⚠️ {error_msg}")
                if self.logger:
                    self.logger.error(error_msg)
                
                return {
                    'success': False,
                    'book_title': book_title,
                    'normalized_book_title': self.normalized_book_title,
                    'book_folder': str(book_dir),
                    'toc_file': str(toc_filepath),
                    'ai_analysis_failed': True,
                    'error': error_msg,
                    'created_folders': []
                }
            
            # 1-6. 각 장별 폴더 생성
            created_folders = []
            
            for i, chapter_info in enumerate(chapters_info):
                chapter_number = i + 1
                chapter_title = chapter_info['title']
                
                print(f"=== 장 {chapter_number} 폴더 생성: {chapter_title} ===")
                if self.logger:
                    self.logger.info(f"장 {chapter_number} 폴더 생성 시작: {chapter_title}")
                
                # 목차에서 해당 장 항목 찾기
                chapter_item = None
                for item in toc_structure:
                    if item['title'] == chapter_title:
                        chapter_item = item
                        break
                
                if not chapter_item:
                    error_msg = f"목차에서 해당 장을 찾을 수 없음: {chapter_title}"
                    print(f"⚠️ {error_msg}")
                    if self.logger:
                        self.logger.warning(error_msg)
                    continue
                
                # 다음 장 시작점 찾기
                next_chapter_start_id = None
                if i + 1 < len(chapters_info):
                    next_chapter_title = chapters_info[i + 1]['title']
                    for item in toc_structure:
                        if item['title'] == next_chapter_title:
                            next_chapter_start_id = item['id']
                            break
                
                try:
                    # 해당 장의 모든 하위 항목들 수집
                    chapter_items = find_chapter_items(toc_structure, chapter_item['id'], next_chapter_start_id, ai_logger)
                    
                    # PDF 내용 추출
                    chapter_content = extract_pdf_content(pdf_path, chapter_info['start_page'], chapter_info['end_page'], ai_logger)
                    
                    # 장별 폴더에 저장
                    chapter_toc_filepath, content_filepath = save_chapter_content_to_folder(
                        chapter_title, chapter_items, chapter_content, book_dir, ai_logger
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
                    
                    print(f"✅ 장 {chapter_number} 완료: {normalize_title(chapter_title)}")
                    if self.logger:
                        self.logger.info(f"장 {chapter_number} 폴더 생성 완료: {normalize_title(chapter_title)}")
                
                except Exception as chapter_error:
                    error_msg = f"장 {chapter_number} 처리 중 오류: {str(chapter_error)}"
                    print(f"❌ {error_msg}")
                    if self.logger:
                        self.logger.error(error_msg)
                    # 개별 장 실패해도 다음 장 계속 진행
                    continue
            
            success_count = len(created_folders)
            print(f"🎉 장별 정보 처리 준비 완료! {success_count}개 장 폴더 생성")
            if self.logger:
                self.logger.info(f"장별 정보 처리 준비 완료: {success_count}개 장 폴더 생성")
            
            return {
                'success': True,
                'book_title': book_title,
                'normalized_book_title': self.normalized_book_title,
                'book_folder': str(book_dir),
                'toc_file': str(toc_filepath),
                'total_chapters': len(chapters_info),
                'created_folders': created_folders,
                'output_directory': str(book_dir)
            }
            
        except Exception as e:
            error_msg = f"장별 정보 처리 준비 실패: {str(e)}"
            print(f"❌ {error_msg}")
            if self.logger:
                self.logger.error(error_msg)
            raise Exception(error_msg)
    
    async def integrate_chapter_information_sequentially(self, workspace_data: Dict[str, Any], pdf_path: str) -> Dict[str, Any]:
        """2단계: 각 장의 정보 통합 (순차 처리)"""
        try:
            print("2️⃣ 각 장의 정보 통합 시작...")
            if self.logger:
                self.logger.info("=== 각 장의 정보 통합 시작 ===")
                if self.test_mode:
                    self.logger.info(f"🧪 테스트 모드: 최대 {self.max_chapters}장만 처리")
            
            created_folders = workspace_data.get('created_folders', [])
            if not created_folders:
                error_msg = "통합할 장별 폴더가 없습니다"
                print(f"⚠️ {error_msg}")
                if self.logger:
                    self.logger.warning(error_msg)
                
                return {
                    'success': False,
                    'error': error_msg,
                    'processed_chapters': 0,
                    'total_chapters': 0,
                    'integration_results': []
                }
            
            total_chapters = len(created_folders)
            processed_chapters = 0
            integration_results = []
            
            # 테스트 모드에서는 제한된 수의 장만 처리
            chapters_to_process = created_folders
            if self.max_chapters:
                chapters_to_process = created_folders[:self.max_chapters]
                print(f"🧪 테스트 모드: {len(chapters_to_process)}/{total_chapters}장 처리 예정")
                if self.logger:
                    self.logger.info(f"테스트 모드: {len(chapters_to_process)}/{total_chapters}장 처리 예정")
            
            # 각 장을 순차적으로 처리
            for i, chapter_info in enumerate(created_folders):
                chapter_number = chapter_info.get('chapter_number')
                chapter_title = chapter_info.get('chapter_title', '')
                
                # 테스트 모드에서 제한 수를 넘으면 SKIP
                if self.max_chapters and i >= self.max_chapters:
                    skip_result = {
                        'chapter_number': chapter_number,
                        'chapter_title': chapter_title,
                        'success': False,
                        'status': 'SKIPPED',
                        'reason': f'테스트 모드 제한 ({self.max_chapters}장)'
                    }
                    integration_results.append(skip_result)
                    print(f"⏭️ 장 {chapter_number} 건너뜀 (테스트 모드 제한)")
                    if self.logger:
                        self.logger.info(f"장 {chapter_number} 건너뜀: 테스트 모드 제한")
                    continue
                
                print(f"📖 장 {chapter_number}/{total_chapters} 정보 통합 중: {chapter_title}")
                if self.logger:
                    self.logger.info(f"장 {chapter_number} 정보 통합 시작: {chapter_title}")
                
                print(f"🚀 장 {chapter_number} integrate_single_chapter_information 호출 준비")
                print(f"🚀 chapter_info: {chapter_info}")
                
                try:
                    # 개별 장 통합 처리
                    print(f"🚀 integrate_single_chapter_information 호출 중...")
                    chapter_result = await self.integrate_single_chapter_information(
                        chapter_info, pdf_path
                    )
                    print(f"🚀 integrate_single_chapter_information 완료!")
                    
                    if chapter_result.get('success', False):
                        processed_chapters += 1
                        print(f"✅ 장 {chapter_number} 통합 완료: {chapter_result.get('summary', '')}")
                        if self.logger:
                            self.logger.info(f"장 {chapter_number} 통합 완료: {chapter_title}")
                            
                        # 테스트 모드에서는 상세 결과 출력
                        if self.test_mode:
                            print(f"🧪 테스트 모드 상세 결과:")
                            print(f"   - 단계 완료: {chapter_result.get('steps_completed', [])}")
                            print(f"   - 통합 문서 수: {chapter_result.get('integrated_documents', 0)}")
                            if self.logger:
                                self.logger.info(f"테스트 모드 상세: {chapter_result}")
                    else:
                        error_msg = f"장 {chapter_number} 통합 실패: {chapter_result.get('error', '알 수 없는 오류')}"
                        print(f"❌ {error_msg}")
                        if self.logger:
                            self.logger.error(error_msg)
                    
                    integration_results.append(chapter_result)
                
                except Exception as chapter_error:
                    error_msg = f"장 {chapter_number} 처리 중 예외 발생: {str(chapter_error)}"
                    print(f"❌ {error_msg}")
                    if self.logger:
                        self.logger.error(error_msg)
                    
                    # 실패한 장도 결과에 기록하고 다음 장 계속 진행
                    integration_results.append({
                        'chapter_number': chapter_number,
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': str(chapter_error)
                    })
                
                # 테스트 모드에서 첫 번째 장 완료 후 중단 메시지
                if self.test_mode and i + 1 == self.max_chapters:
                    print(f"🧪 테스트 모드: {self.max_chapters}장 처리 완료로 중단")
                    if self.logger:
                        self.logger.info(f"테스트 모드: {self.max_chapters}장 처리 완료로 중단")
                    break
            
            # 최종 결과
            success_rate = (processed_chapters / total_chapters * 100) if total_chapters > 0 else 0
            skipped_chapters = len([r for r in integration_results if r.get('status') == 'SKIPPED'])
            
            print(f"🎉 각 장의 정보 통합 완료!")
            print(f"📊 성공: {processed_chapters}/{total_chapters} 장 ({success_rate:.1f}%)")
            if skipped_chapters > 0:
                print(f"⏭️ 건너뜀: {skipped_chapters} 장 (테스트 모드)")
            
            if self.logger:
                self.logger.info(f"각 장의 정보 통합 완료: {processed_chapters}/{total_chapters} 장 성공")
                if skipped_chapters > 0:
                    self.logger.info(f"테스트 모드로 {skipped_chapters} 장 건너뜀")
            
            return {
                'success': True,
                'processed_chapters': processed_chapters,
                'total_chapters': total_chapters,
                'skipped_chapters': skipped_chapters,
                'success_rate': success_rate,
                'test_mode': self.test_mode,
                'integration_results': integration_results
            }
            
        except Exception as e:
            error_msg = f"각 장의 정보 통합 실패: {str(e)}"
            print(f"❌ {error_msg}")
            if self.logger:
                self.logger.error(error_msg)
            raise Exception(error_msg)
    
    async def integrate_single_chapter_information(self, chapter_info: Dict[str, Any], pdf_path: str) -> Dict[str, Any]:
        """개별 장의 정보 통합 (노드 정보 문서 생성 → 콘텐츠 노드/내용 문서 생성 → 통합)"""
        chapter_number = chapter_info.get('chapter_number')
        chapter_title = chapter_info.get('chapter_title', '')
        folder_path = chapter_info.get('folder_path', '')
        toc_file = chapter_info.get('toc_file', '')
        
        try:
            print(f"🔥 장 {chapter_number} 개별 통합 진입! chapter_title={chapter_title}")
            print(f"🔥 folder_path={folder_path}")
            print(f"🔥 toc_file={toc_file}")
            
            if self.logger:
                self.logger.info(f"장 {chapter_number} 개별 통합 시작: {chapter_title}")
            
            if not folder_path or not os.path.exists(folder_path):
                error_msg = f"장별 폴더를 찾을 수 없음: {folder_path}"
                print(f"❌ {error_msg}")
                if self.logger:
                    self.logger.error(error_msg)
                return {
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'success': False,
                    'error': error_msg
                }
            
            print(f"🔥 폴더 경로 확인 완료!")
            
            # 통합 처리 단계별 진행
            steps_completed = []
            
            # 공통 파일 경로 설정
            toc_file = os.path.join(folder_path, f"{chapter_info['normalized_title']}_toc.json")
            
            # Step 1: 노드 정보 문서 생성
            print(f"  📋 장 {chapter_number}: 노드 정보 문서 생성 중...")
            print(f"    🔧 toc_file: {toc_file}")
            print(f"    🔧 folder_path: {folder_path}")
            try:
                print(f"    ⚡ NodeDocumentGenerator.generate_documents_for_chapter() 호출...")
                node_docs_result = self.node_document_generator.generate_documents_for_chapter(
                    toc_file=toc_file,
                    chapter_folder=folder_path
                )
                print(f"    ⚡ NodeDocumentGenerator 완료, 결과 확인 중...")
                if node_docs_result.success:
                    steps_completed.append("노드 정보 문서 생성")
                    print(f"  ✅ 장 {chapter_number}: 노드 정보 문서 생성 완료 ({node_docs_result.created_count}개 파일)")
                    if self.logger:
                        self.logger.info(f"장 {chapter_number} 노드 정보 문서 생성 완료: {node_docs_result.created_count}개 파일")
                else:
                    error_msg = f"노드 정보 문서 생성 실패: {node_docs_result.error or '알 수 없는 오류'}"
                    print(f"  ❌ 장 {chapter_number}: {error_msg}")
                    if self.logger:
                        self.logger.error(f"장 {chapter_number} {error_msg}")
                    raise Exception(error_msg)
                
            except Exception as e:
                error_msg = f"노드 정보 문서 생성 중 오류: {str(e)}"
                if self.logger:
                    self.logger.error(f"장 {chapter_number} {error_msg}")
                return {
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'success': False,
                    'error': error_msg,
                    'steps_completed': steps_completed
                }
            
            # Step 2: 콘텐츠 노드 분석 및 파일 생성
            print(f"  🔍 장 {chapter_number}: 콘텐츠 노드 분석 및 파일 생성 중...")
            try:
                # Logger 설정
                analyzer_logger = logging.getLogger(f'content_analyzer_ch{chapter_number}')
                analyzer_logger.setLevel(logging.INFO)
                
                # ContentNodeAnalyzer 초기화 (config_path 전달)
                config_path = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/extraction_config.yaml"
                analyzer = ContentNodeAnalyzer(config_path=config_path, logger=analyzer_logger)
                
                # 디버깅: pdf_path 확인
                print(f"    🔧 디버깅: toc_file = {toc_file}")
                print(f"    🔧 디버깅: toc_file exists = {os.path.exists(toc_file) if toc_file else False}")
                print(f"    🔧 디버깅: pdf_path = {pdf_path}")
                print(f"    🔧 디버깅: pdf_path exists = {os.path.exists(pdf_path) if pdf_path else False}")
                print(f"    🔧 디버깅: pdf_path type = {type(pdf_path)}")
                
                # content.md 파일 경로 찾기  
                content_md_path = os.path.join(folder_path, f"{chapter_info['normalized_title']}_content.md")
                
                print(f"    🔧 디버깅: content_md_path = {content_md_path}")
                print(f"    🔧 디버깅: content_md_path exists = {os.path.exists(content_md_path)}")
                
                if not os.path.exists(content_md_path):
                    error_msg = f"장별 마크다운 파일을 찾을 수 없음: {content_md_path}"
                    print(f"❌ {error_msg}")
                    raise Exception(error_msg)
                
                # 콘텐츠 노드 분석 및 파일 생성 (통합 처리)
                analysis_result = await analyzer.analyze_chapter_toc(toc_file, content_md_path)
                
                if analysis_result.get('success', False):
                    content_nodes_path = analysis_result.get('content_nodes_path', '')
                    extracted_files = analysis_result.get('extracted_files', [])
                    
                    steps_completed.append("콘텐츠 노드/내용 문서 생성")
                    if self.logger:
                        self.logger.info(f"장 {chapter_number} 콘텐츠 노드/내용 문서 생성 완료: {len(extracted_files)}개 파일")
                    
                    print(f"    ✅ 콘텐츠 노드 생성 완료: {len(extracted_files)}개 파일 → {content_nodes_path}")
                else:
                    error_msg = f"콘텐츠 노드 분석/생성 실패: {analysis_result.get('error', '알 수 없는 오류')}"
                    raise Exception(error_msg)
                
            except Exception as e:
                error_msg = f"콘텐츠 노드 분석/생성 중 오류: {str(e)}"
                if self.logger:
                    self.logger.error(f"장 {chapter_number} {error_msg}")
                return {
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'success': False,
                    'error': error_msg,
                    'steps_completed': steps_completed
                }
            
            # Step 3: 문서 통합
            print(f"  🔗 장 {chapter_number}: 문서 통합 중...")
            try:
                integration_result = self.document_integrator.integrate_documents_for_chapter(folder_path)
                
                if integration_result.get('success', False):
                    integrated_count = integration_result.get('integrated_count', 0)
                    steps_completed.append("문서 통합")
                    if self.logger:
                        self.logger.info(f"장 {chapter_number} 문서 통합 완료: {integrated_count}개 문서")
                else:
                    error_msg = f"문서 통합 실패: {integration_result.get('error', '알 수 없는 오류')}"
                    if self.logger:
                        self.logger.error(f"장 {chapter_number} {error_msg}")
                    raise Exception(error_msg)
                
            except Exception as e:
                error_msg = f"문서 통합 중 오류: {str(e)}"
                if self.logger:
                    self.logger.error(f"장 {chapter_number} {error_msg}")
                return {
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'success': False,
                    'error': error_msg,
                    'steps_completed': steps_completed
                }
            
            # 성공 완료
            summary = f"3단계 완료 ({' → '.join(steps_completed)})"
            if self.logger:
                self.logger.info(f"장 {chapter_number} 개별 통합 완료: {summary}")
            
            return {
                'chapter_number': chapter_number,
                'chapter_title': chapter_title,
                'success': True,
                'steps_completed': steps_completed,
                'integrated_documents': integrated_count,
                'summary': summary
            }
            
        except Exception as e:
            error_msg = f"개별 장 통합 처리 중 예외: {str(e)}"
            if self.logger:
                self.logger.error(f"장 {chapter_number} {error_msg}")
            
            return {
                'chapter_number': chapter_number,
                'chapter_title': chapter_title,
                'success': False,
                'error': error_msg,
                'steps_completed': steps_completed if 'steps_completed' in locals() else []
            }
    
    async def execute(self, file_path: str, metadata_info: Dict[str, Any] = None) -> PipelineResult:
        """파이프라인 실행"""
        result = PipelineResult()
        
        try:
            print("🚀 책 파이프라인 v3 실행 시작")
            
            # 1단계: 장별 정보 처리 준비
            workspace_data = await self.prepare_chapter_workspace(file_path)
            result.step_completed = 1
            result.progress_percent = 50
            
            if not workspace_data.get('success', False):
                result.is_success = False
                result.error = workspace_data.get('error', '장별 정보 처리 준비 실패')
                return result
            
            # 2단계: 각 장의 정보 통합
            integration_data = await self.integrate_chapter_information_sequentially(workspace_data, file_path)
            result.step_completed = 2
            result.progress_percent = 100
            
            # 성공 결과
            result.is_success = True
            result.data = {
                'workspace_info': workspace_data,
                'integration_info': integration_data,
                'pipeline_stage': '2단계 완료 (장별정보처리준비 → 각장의정보통합)',
                'logs_directory': str(self.logs_dir) if self.logs_dir else None
            }
            
            total_chapters = integration_data.get('total_chapters', 0)
            processed_chapters = integration_data.get('processed_chapters', 0)
            success_rate = integration_data.get('success_rate', 0)
            
            # 테스트 모드와 일반 모드에 따른 결과 출력
            if self.test_mode:
                print("🧪🎉 책 파이프라인 v3 테스트 모드 완료! 🎉🧪")
                print(f"📚 책: {workspace_data.get('book_title', '알 수 없음')}")
                print(f"🔬 테스트 결과: {processed_chapters}/{self.max_chapters} 장 처리 ({success_rate:.1f}%)")
                print(f"📁 출력: {workspace_data.get('output_directory', '')}")
                print(f"📋 로그: {self.logs_dir}")
                if self.logger:
                    self.logger.info(f"테스트 모드 완료: {processed_chapters}/{self.max_chapters} 장 처리")
            else:
                print("🎉🎉🎉 책 파이프라인 v3 전체 완료! 🎉🎉🎉")
                print(f"📚 책: {workspace_data.get('book_title', '알 수 없음')}")
                print(f"📊 성공: {processed_chapters}/{total_chapters} 장 ({success_rate:.1f}%)")
                print(f"📁 출력: {workspace_data.get('output_directory', '')}")
                print(f"📋 로그: {self.logs_dir}")
                if self.logger:
                    self.logger.info(f"책 파이프라인 v3 전체 완료: {processed_chapters}/{total_chapters} 장 성공")
            
            return result
            
        except Exception as e:
            result.is_success = False
            result.error = str(e)
            error_msg = f"책 파이프라인 v3 실패: {e}"
            print(f"❌ {error_msg}")
            if self.logger:
                self.logger.error(error_msg)
            return result