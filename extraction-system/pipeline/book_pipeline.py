# 생성 시간: 2025-09-01 12:14:24 KST
# 핵심 내용: PDF/EPUB → 통합 노드 문서 생성 파이프라인 (1단계: 목차 추출 → 장별 폴더)
# 상세 내용:
#   - BookPipeline (라인 15-200): 메인 파이프라인 클래스 
#   - extract_toc_from_pdf (라인 25-85): PDF 북마크 → 목차 JSON 추출
#   - create_chapters_folders (라인 87-140): 목차 → 장별 폴더 생성
#   - execute (라인 142-185): 파이프라인 실행 메인 메서드
#   - PipelineResult (라인 187-200): 결과 반환 클래스
# 상태: active
# 주소: book_pipeline
# 참조: toc_extractor_with_fixed_levels.py, extract_chapters_v5.py 핵심 로직 통합

import os
import json
import asyncio
import tempfile
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 기존 검증된 모듈들 임포트
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30')  # PyMuPDF toc_extractor
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31')

from toc_extractor import extract_toc_with_pymupdf, process_toc_items, calculate_page_ranges
from extract_chapters_v5 import count_chapters_with_ai, GeminiAPIProvider, normalize_title, extract_pdf_content, find_chapter_items, save_chapter_content_to_folder

# 콘텐츠 노드 분석 모듈 임포트
from .content_node_analyzer import ContentNodeAnalyzer

class PipelineResult:
    """파이프라인 실행 결과"""
    def __init__(self):
        self.is_success = False
        self.error = None
        self.data = {}
        self.step_completed = 0
        self.total_steps = 4  # 4단계로 확장: 목차추출 → 장별폴더 → 콘텐츠노드분석 → 실제콘텐츠추출
        self.progress_percent = 0

class BookPipeline:
    """PDF/EPUB → 통합 노드 문서 생성 파이프라인"""
    
    def __init__(self):
        self.temp_dir = None
        self.output_dir = None
        
    def extract_toc_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """PDF에서 목차 추출 (PyMuPDF 기존 검증된 로직 사용)"""
        try:
            print("🔄 기존 검증된 PyMuPDF 목차 추출 로직 사용")
            
            # 1단계: PyMuPDF로 목차 추출 (기존 로직)
            raw_toc = extract_toc_with_pymupdf(pdf_path)
            if not raw_toc:
                raise Exception("목차 추출 실패")
            
            # 2단계: 목차 항목 처리 및 정리 (기존 로직)  
            processed_toc = process_toc_items(raw_toc)
            
            # 3단계: 페이지 범위 계산 (기존 로직)
            complete_toc = calculate_page_ranges(processed_toc)
            
            return {
                "extraction_info": {
                    "source_pdf": os.path.basename(pdf_path),
                    "extraction_method": "PyMuPDF complete TOC extraction with hierarchy",
                    "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                    "total_items": len(complete_toc),
                    "note": "Complete hierarchy extracted using PyMuPDF library"
                },
                "toc_structure": complete_toc
            }
            
        except Exception as e:
            raise Exception(f"PDF 목차 추출 실패: {str(e)}")
    
    async def create_chapters_folders(self, toc_data: Dict[str, Any], pdf_path: str) -> Dict[str, Any]:
        """목차 기반 장별 폴더 생성 (기존 검증된 AI 로직 사용)"""
        try:
            toc_structure = toc_data["toc_structure"]
            
            # 책 제목 (id=0) 추출하여 최상위 폴더 생성
            book_title = toc_structure[0]['title'] if toc_structure else "Unknown_Book"
            book_folder_name = normalize_title(book_title)
            book_dir = self.output_dir / book_folder_name
            book_dir.mkdir(exist_ok=True)
            print(f"📖 책 폴더 생성: {book_folder_name}")
            
            # 목차 파일을 책 폴더에 저장
            toc_filepath = book_dir / "toc.json" 
            with open(toc_filepath, 'w', encoding='utf-8') as f:
                json.dump(toc_data, f, ensure_ascii=False, indent=2)
            print(f"💾 목차 파일 저장: {toc_filepath}")
            
            # AI 분석을 위한 목차 파일 경로
            temp_toc_path = str(toc_filepath)
            
            # 기존 검증된 AI 로직으로 실제 장들만 식별
            print("🤖 기존 검증된 AI 로직으로 장 분석 중...")
            
            # Logger 설정 (기존 로직에서 필요)
            import logging
            logger = logging.getLogger('book_pipeline')
            logger.setLevel(logging.INFO)
            
            # Gemini AI 제공자 초기화 (기존 로직)
            ai_provider = GeminiAPIProvider(logger)
            
            # AI 기반 장 분석 (기존 검증된 함수 사용)
            try:
                chapter_analysis = await count_chapters_with_ai(temp_toc_path, ai_provider, logger)
                
                if not chapter_analysis['success']:
                    print(f"⚠️ AI 장 분석 실패: {chapter_analysis.get('error', 'Unknown error')}")
                    print("📝 목차 파일은 저장되었습니다. AI 분석은 실패했지만 계속 진행합니다.")
                    # AI 실패 시에도 기본 정보 반환
                    return {
                        'book_title': book_title,
                        'book_folder': book_folder_name,
                        'total_chapters': 0,
                        'created_folders': [],
                        'output_directory': str(book_dir),
                        'toc_file': str(toc_filepath),
                        'ai_analysis_failed': True,
                        'error': chapter_analysis.get('error', 'AI 분석 실패')
                    }
                
                chapters_info = chapter_analysis['chapters_info']
                print(f"📚 AI 분석 결과: {len(chapters_info)}개 실제 장 식별")
                
            except Exception as ai_error:
                print(f"⚠️ AI 분석 중 예외 발생: {str(ai_error)}")
                print("📝 목차 파일은 저장되었습니다. AI 분석 실패로 종료합니다.")
                # 예외 발생 시에도 기본 정보 반환
                return {
                    'book_title': book_title,
                    'book_folder': book_folder_name,
                    'total_chapters': 0,
                    'created_folders': [],
                    'output_directory': str(book_dir),
                    'toc_file': str(toc_filepath),
                    'ai_analysis_failed': True,
                    'error': str(ai_error)
                }
            
            created_folders = []
            
            # 각 장별 폴더 생성 (기존 검증된 로직 사용)
            for i, chapter_info in enumerate(chapters_info):
                chapter_number = i + 1
                chapter_title = chapter_info['title']
                
                print(f"=== 장 {chapter_number} 처리 시작: {chapter_title} ===")
                
                # 목차에서 해당 장 항목 찾기
                chapter_item = None
                for item in toc_structure:
                    if item['title'] == chapter_title:
                        chapter_item = item
                        break
                
                if not chapter_item:
                    print(f"⚠️ 목차에서 해당 장을 찾을 수 없음: {chapter_title}")
                    continue
                
                # 다음 장 시작점 찾기
                next_chapter_start_id = None
                if i + 1 < len(chapters_info):
                    next_chapter_title = chapters_info[i + 1]['title']
                    for item in toc_structure:
                        if item['title'] == next_chapter_title:
                            next_chapter_start_id = item['id']
                            break
                
                # 해당 장의 모든 하위 항목들 수집 (기존 검증된 함수)
                chapter_items = find_chapter_items(toc_structure, chapter_item['id'], next_chapter_start_id, logger)
                
                # PDF 내용 추출 (기존 검증된 함수)
                chapter_content = extract_pdf_content(pdf_path, chapter_info['start_page'], chapter_info['end_page'], logger)
                
                # 장별 폴더에 저장 (기존 검증된 함수)
                toc_filepath, content_filepath = save_chapter_content_to_folder(
                    chapter_title, chapter_items, chapter_content, book_dir, logger
                )
                
                created_folders.append({
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'normalized_title': normalize_title(chapter_title),
                    'folder_path': str(book_dir / normalize_title(chapter_title)),
                    'toc_file': str(toc_filepath),
                    'content_file': str(content_filepath) if content_filepath else None,
                    'page_range': f"{chapter_info['start_page']}-{chapter_info['end_page']}",
                    'items_count': len(chapter_items)
                })
                
                print(f"✅ 장 {chapter_number} 완료: {normalize_title(chapter_title)}")
            
            return {
                'book_title': book_title,
                'book_folder': book_folder_name,
                'total_chapters': len(chapters_info),
                'created_folders': created_folders,
                'output_directory': str(book_dir)
            }
            
        except Exception as e:
            raise Exception(f"장별 폴더 생성 실패: {str(e)}")
    
    async def analyze_content_nodes(self, chapters_data: Dict[str, Any], pdf_path: str) -> Dict[str, Any]:
        """장별 TOC 파일들에 has_content 필드 추가 및 콘텐츠 노드 추출"""
        try:
            print("🔍 === 장별 콘텐츠 노드 분석 시작 ===")
            
            created_folders = chapters_data.get('created_folders', [])
            if not created_folders:
                print("⚠️ 분석할 장별 폴더가 없습니다.")
                return {
                    'success': False,
                    'error': '분석할 장별 폴더가 없음',
                    'processed_chapters': 0,
                    'content_nodes_found': 0
                }
            
            # Logger 설정 (기존 로직에서 필요)
            import logging
            logger = logging.getLogger('content_node_analyzer')
            logger.setLevel(logging.INFO)
            
            # ContentNodeAnalyzer 초기화 (Gemini API 사용)
            analyzer = ContentNodeAnalyzer(
                ai_provider=GeminiAPIProvider(logger),
                logger=logger
            )
            
            processed_chapters = 0
            total_content_nodes = 0
            chapter_results = []
            
            for chapter_info in created_folders:
                chapter_title = chapter_info.get('chapter_title', '')
                toc_file = chapter_info.get('toc_file', '')
                
                print(f"\n📖 장 {chapter_info.get('chapter_number')}: {chapter_title}")
                
                if not toc_file or not os.path.exists(toc_file):
                    print(f"⚠️ TOC 파일을 찾을 수 없음: {toc_file}")
                    continue
                
                try:
                    # 각 장별 TOC 분석
                    analysis_result = await analyzer.analyze_chapter_toc(toc_file, pdf_path)
                    
                    if analysis_result.get('success', False):
                        content_nodes_count = analysis_result.get('content_nodes_count', 0)
                        total_content_nodes += content_nodes_count
                        processed_chapters += 1
                        
                        chapter_results.append({
                            'chapter_number': chapter_info.get('chapter_number'),
                            'chapter_title': chapter_title,
                            'content_nodes_count': content_nodes_count,
                            'content_nodes_path': analysis_result.get('content_nodes_path', ''),
                            'success': True
                        })
                        
                        print(f"✅ {chapter_title}: {content_nodes_count}개 콘텐츠 노드 발견")
                    else:
                        print(f"❌ {chapter_title}: {analysis_result.get('error', '분석 실패')}")
                        chapter_results.append({
                            'chapter_number': chapter_info.get('chapter_number'),
                            'chapter_title': chapter_title,
                            'success': False,
                            'error': analysis_result.get('error', '분석 실패')
                        })
                
                except Exception as e:
                    print(f"❌ {chapter_title} 분석 중 오류: {str(e)}")
                    chapter_results.append({
                        'chapter_number': chapter_info.get('chapter_number'),
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': str(e)
                    })
            
            print(f"\n🎉 콘텐츠 노드 분석 완료!")
            print(f"📊 처리된 장: {processed_chapters}개")
            print(f"📝 발견된 콘텐츠 노드: {total_content_nodes}개")
            
            return {
                'success': True,
                'processed_chapters': processed_chapters,
                'total_chapters': len(created_folders),
                'content_nodes_found': total_content_nodes,
                'chapter_results': chapter_results
            }
            
        except Exception as e:
            raise Exception(f"콘텐츠 노드 분석 실패: {str(e)}")
    
    async def extract_content_files(self, content_analysis_data: Dict[str, Any], pdf_path: str) -> Dict[str, Any]:
        """콘텐츠 노드를 실제 파일로 추출"""
        try:
            print("📄 === 실제 콘텐츠 파일 추출 시작 ===")
            
            if not content_analysis_data.get('success', False):
                print("⚠️ 콘텐츠 분석이 완료되지 않음")
                return {
                    'success': False,
                    'error': '콘텐츠 분석이 완료되지 않음',
                    'processed_chapters': 0,
                    'extracted_files': 0
                }
            
            # Logger 설정
            import logging
            logger = logging.getLogger('content_extractor')
            logger.setLevel(logging.INFO)
            
            # ContentNodeAnalyzer 초기화 (콘텐츠 추출용)
            analyzer = ContentNodeAnalyzer(logger=logger)
            
            chapter_results = content_analysis_data.get('chapter_results', [])
            total_extracted_files = 0
            extraction_results = []
            
            for chapter_result in chapter_results:
                if not chapter_result.get('success', False):
                    continue
                
                chapter_title = chapter_result.get('chapter_title', '')
                content_nodes_path = chapter_result.get('content_nodes_path', '')
                
                print(f"\n📖 {chapter_title} 콘텐츠 추출 중...")
                
                if not content_nodes_path or not os.path.exists(content_nodes_path):
                    print(f"⚠️ Content nodes 파일을 찾을 수 없음: {content_nodes_path}")
                    extraction_results.append({
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': 'Content nodes 파일 없음'
                    })
                    continue
                
                try:
                    # 각 장별 콘텐츠 추출
                    extraction_result = await analyzer.extract_content_nodes_to_files(content_nodes_path, pdf_path)
                    
                    if extraction_result.get('success', False):
                        extracted_count = extraction_result.get('successful_extractions', 0)
                        total_extracted_files += extracted_count
                        
                        extraction_results.append({
                            'chapter_title': chapter_title,
                            'success': True,
                            'extracted_files_count': extracted_count,
                            'total_nodes': extraction_result.get('total_nodes', 0),
                            'extracted_files': extraction_result.get('extracted_files', [])
                        })
                        
                        print(f"✅ {chapter_title}: {extracted_count}개 파일 추출 완료")
                    else:
                        print(f"❌ {chapter_title}: {extraction_result.get('error', '추출 실패')}")
                        extraction_results.append({
                            'chapter_title': chapter_title,
                            'success': False,
                            'error': extraction_result.get('error', '추출 실패')
                        })
                
                except Exception as e:
                    print(f"❌ {chapter_title} 추출 중 오류: {str(e)}")
                    extraction_results.append({
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': str(e)
                    })
            
            successful_chapters = len([r for r in extraction_results if r.get('success', False)])
            
            print(f"\n🎉 콘텐츠 파일 추출 완료!")
            print(f"📊 성공한 장: {successful_chapters}개")
            print(f"📄 추출된 파일: {total_extracted_files}개")
            
            return {
                'success': True,
                'processed_chapters': successful_chapters,
                'total_chapters': len(chapter_results),
                'extracted_files_count': total_extracted_files,
                'extraction_results': extraction_results
            }
            
        except Exception as e:
            raise Exception(f"콘텐츠 파일 추출 실패: {str(e)}")
    
    async def execute(self, file_path: str, metadata_info: Dict[str, Any]) -> PipelineResult:
        """파이프라인 실행"""
        result = PipelineResult()
        
        try:
            print("🚀 책 파이프라인 실행 시작")
            
            # extraction-system에 직접 출력 디렉토리 생성
            extraction_system_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system")
            self.output_dir = extraction_system_dir
            self.temp_dir = str(extraction_system_dir)  # 문자열로 유지 (기존 로직 호환)
            
            print(f"📁 작업 디렉토리: {self.output_dir}")
            
            # 1단계: PDF 목차 추출
            print("1️⃣ PDF 목차 추출 중...")
            toc_data = self.extract_toc_from_pdf(file_path)
            result.step_completed = 1
            result.progress_percent = 25
            
            # 2단계: 장별 폴더 생성 (async 호출)
            print("2️⃣ 장별 폴더 생성 중...")
            chapters_data = await self.create_chapters_folders(toc_data, file_path)
            result.step_completed = 2
            result.progress_percent = 50
            
            # 3단계: 콘텐츠 노드 분석 (has_content 필드 추가)
            print("3️⃣ 콘텐츠 노드 분석 중...")
            content_analysis_data = await self.analyze_content_nodes(chapters_data, file_path)
            result.step_completed = 3
            result.progress_percent = 75
            
            # 4단계: 실제 콘텐츠 파일 추출
            print("4️⃣ 실제 콘텐츠 파일 추출 중...")
            content_extraction_data = await self.extract_content_files(content_analysis_data, file_path)
            result.step_completed = 4
            result.progress_percent = 100
            
            # 성공 결과
            result.is_success = True
            result.data = {
                'toc_info': {
                    'total_items': len(toc_data["toc_structure"]),
                    'extraction_timestamp': toc_data["extraction_info"]["extraction_timestamp"]
                },
                'chapters_info': chapters_data,
                'content_analysis': content_analysis_data,
                'content_extraction': content_extraction_data,
                'output_directory': str(self.output_dir),
                'pipeline_stage': '4단계 완료 (목차 → 장별폴더 → 콘텐츠노드분석 → 실제콘텐츠추출)'
            }
            
            print("🎉🎉🎉 책 파이프라인 전체 완료! 🎉🎉🎉")
            print(f"📊 총 {content_analysis_data.get('processed_chapters', 0)}개 장 처리")
            print(f"📝 총 {content_analysis_data.get('content_nodes_found', 0)}개 콘텐츠 노드 발견")
            print(f"📄 총 {content_extraction_data.get('extracted_files_count', 0)}개 콘텐츠 파일 생성")
            return result
            
        except Exception as e:
            result.is_success = False
            result.error = str(e)
            print(f"❌ 책 파이프라인 실패: {e}")
            return result