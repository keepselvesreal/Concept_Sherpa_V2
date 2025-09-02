# 생성 시간: Mon Jan  2 16:50:00 KST 2025
# 핵심 내용: 목차 추출기 - 기존 파이프라인 1단계 로직 이관 (PyMuPDF + AI 장 식별)
# 상세 내용:
#   - TocExtractionResult (라인 18-26): 목차 추출 결과 데이터 클래스
#   - ChapterAnalysisResult (라인 28-35): 장 분석 결과 데이터 클래스
#   - TocExtractor (라인 37-190): 목차 추출기 메인 클래스
#   - extract_toc (라인 65-110): PyMuPDF 목차 추출
#   - analyze_chapters_with_ai (라인 112-155): AI 기반 장 식별 (페이지 정보는 기존 목차 사용)
#   - _generate_chapter_analysis_prompt (라인 157-175): AI 프롬프트 생성
#   - normalize_title (라인 177-190): 제목 정규화 (기존 로직)
# 상태: active

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# 기존 모듈들 임포트 경로 추가 (임시)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/inbox/25-08-30')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/inbox/25-08-31')

from .refactoring_logger import RefactoringLogger, RefactoringLogContext
from .ai_providers import AIProviderFactory

@dataclass
class TocExtractionResult:
    """목차 추출 결과"""
    success: bool
    toc_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class ChapterAnalysisResult:
    """장 분석 결과"""
    success: bool
    chapters_info: List[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.chapters_info is None:
            self.chapters_info = []

class TocExtractor:
    """목차 추출기 - PyMuPDF + AI 장 식별"""
    
    def __init__(self, logger: Optional[RefactoringLogger] = None, 
                 ai_factory: Optional[AIProviderFactory] = None):
        self.logger = logger
        self.ai_factory = ai_factory
    
    def _get_log_context(self, method_name: str) -> RefactoringLogContext:
        """로그 컨텍스트 생성"""
        return RefactoringLogContext(
            stage="toc_extraction",
            class_name=self.__class__.__name__,
            method_name=method_name,
            operation_id=""
        )
    
    def extract_toc(self, pdf_path: str) -> TocExtractionResult:
        """PDF에서 목차 추출 (기존 로직 이관)"""
        context = self._get_log_context("extract_toc")
        inputs = {"pdf_path": pdf_path}
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            # 파일 존재 확인
            if not os.path.exists(pdf_path):
                error = f"파일을 찾을 수 없습니다: {pdf_path}"
                if self.logger:
                    self.logger.operation_error(context, FileNotFoundError(error), inputs)
                return TocExtractionResult(success=False, error=error)
            
            # 기존 모듈 임포트 (동적 임포트로 오류 처리)
            try:
                from toc_extractor import extract_toc_with_pymupdf, process_toc_items, calculate_page_ranges
            except ImportError as e:
                error = f"기존 목차 추출 모듈 임포트 실패: {str(e)}"
                if self.logger:
                    self.logger.operation_error(context, e, inputs)
                return TocExtractionResult(success=False, error=error)
            
            # PyMuPDF 목차 추출 (기존 로직)
            raw_toc = extract_toc_with_pymupdf(pdf_path)
            if not raw_toc:
                error = "목차 추출 실패 - 목차가 없거나 PDF 형식이 잘못됨"
                if self.logger:
                    self.logger.operation_error(context, RuntimeError(error), inputs)
                return TocExtractionResult(success=False, error=error)
            
            # 목차 처리 (기존 로직)
            processed_toc = process_toc_items(raw_toc)
            complete_toc = calculate_page_ranges(processed_toc)
            
            # 목차 데이터 구조 생성 (기존 로직)
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
            
            outputs = {
                "success": True,
                "toc_items_count": len(complete_toc),
                "pdf_filename": os.path.basename(pdf_path)
            }
            
            if self.logger:
                self.logger.operation_success(context, outputs)
                # 추출된 목차 결과를 파일로 저장 (사용자 확인용)
                saved_file = self.logger.save_result(
                    context, toc_data, 
                    filename="toc_extraction_result.json",
                    description="PDF 목차 추출 결과 (PyMuPDF + 페이지 범위 계산)"
                )
                if saved_file:
                    print(f"📁 목차 추출 결과 저장됨: {saved_file}")
            
            return TocExtractionResult(success=True, toc_data=toc_data)
            
        except Exception as e:
            error = f"목차 추출 중 예외 발생: {str(e)}"
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            return TocExtractionResult(success=False, error=error)
    
    async def analyze_chapters_with_ai(self, toc_data: Dict[str, Any]) -> ChapterAnalysisResult:
        """AI 기반 장 식별 - 페이지 정보는 기존 목차에서 가져옴"""
        context = self._get_log_context("analyze_chapters_with_ai")
        inputs = {
            "toc_items_count": len(toc_data.get("toc_structure", [])),
            "has_ai_factory": self.ai_factory is not None
        }
        
        if self.logger:
            self.logger.operation_start(context, inputs)
        
        try:
            if not self.ai_factory:
                error = "AI Factory가 설정되지 않음"
                if self.logger:
                    self.logger.operation_error(context, ValueError(error), inputs)
                return ChapterAnalysisResult(success=False, error=error)
            
            # AI Provider 획득
            ai_provider = self.ai_factory.get_provider()
            
            # AI 프롬프트 생성 (장 식별만)
            prompt = self._generate_chapter_analysis_prompt(toc_data)
            
            # AI 분석 요청
            ai_response = await ai_provider.generate_content(prompt)
            
            
            # AI 응답 파싱 (장 제목 리스트)
            try:
                if not ai_response.text or ai_response.text.strip() == "":
                    error = "AI가 빈 응답을 반환함"
                    if self.logger:
                        self.logger.operation_error(context, ValueError(error), inputs)
                    return ChapterAnalysisResult(success=False, error=error)
                
                # Gemini 응답에서 JSON 코드블록 제거
                response_text = ai_response.text.strip()
                if response_text.startswith('```json'):
                    # ```json으로 시작하는 경우 코드블록 제거
                    lines = response_text.split('\n')
                    # 첫 번째 줄(```json)과 마지막 줄(```) 제거
                    if len(lines) > 2 and lines[-1].strip() == '```':
                        response_text = '\n'.join(lines[1:-1])
                    else:
                        # 마지막 줄이 ```이 아닌 경우, 첫 번째 줄만 제거
                        response_text = '\n'.join(lines[1:])
                elif response_text.startswith('```'):
                    # ```으로만 시작하는 경우도 처리
                    lines = response_text.split('\n')
                    if len(lines) > 2 and lines[-1].strip() == '```':
                        response_text = '\n'.join(lines[1:-1])
                    else:
                        response_text = '\n'.join(lines[1:])
                
                identified_chapters = json.loads(response_text.strip())
                
                if not isinstance(identified_chapters, list):
                    raise ValueError("AI 응답이 리스트 형태가 아님")
                
                # 기존 목차에서 식별된 장들의 정보 추출
                toc_structure = toc_data.get("toc_structure", [])
                chapters_info = []
                
                for chapter_title in identified_chapters:
                    # 목차에서 해당 제목 찾기
                    for toc_item in toc_structure:
                        if toc_item['title'] == chapter_title:
                            chapters_info.append({
                                'title': chapter_title,
                                'start_page': toc_item.get('start_page', toc_item.get('page')),
                                'end_page': toc_item.get('end_page'),
                                'level': toc_item.get('level', 1),
                                'id': toc_item.get('id')
                            })
                            break
                
            except (json.JSONDecodeError, ValueError) as e:
                error = f"AI 응답 파싱 실패: {str(e)}"
                if self.logger:
                    self.logger.operation_error(context, e, inputs)
                return ChapterAnalysisResult(success=False, error=error)
            
            outputs = {
                "success": True,
                "chapters_identified": len(chapters_info),
                "ai_tokens_used": ai_response.tokens_used
            }
            
            if self.logger:
                self.logger.operation_success(context, outputs)
                # AI 장 식별 결과를 파일로 저장 (사용자 확인용)
                saved_file = self.logger.save_result(
                    context, {
                        "identified_chapters": identified_chapters,
                        "chapters_info": chapters_info,
                        "ai_metadata": {
                            "provider": ai_response.provider,
                            "model": ai_response.model,
                            "tokens_used": ai_response.tokens_used,
                            "finish_reason": ai_response.finish_reason
                        }
                    },
                    filename="ai_chapter_identification_result.json",
                    description="AI 기반 장 식별 결과 (Gemini API)"
                )
                if saved_file:
                    print(f"🤖 AI 장 식별 결과 저장됨: {saved_file}")
            
            return ChapterAnalysisResult(success=True, chapters_info=chapters_info)
            
        except Exception as e:
            error = f"AI 장 식별 중 예외 발생: {str(e)}"
            if self.logger:
                self.logger.operation_error(context, e, inputs)
            return ChapterAnalysisResult(success=False, error=error)
    
    def _generate_chapter_analysis_prompt(self, toc_data: Dict[str, Any]) -> str:
        """AI 장 식별 프롬프트 생성"""
        toc_structure = toc_data.get("toc_structure", [])
        
        prompt = f"""
다음 목차 구조에서 실제 본문 '장(Chapter)'에 해당하는 항목들의 제목만 식별해주세요.

목차 구조:
{json.dumps(toc_structure, ensure_ascii=False, indent=2)}

요구사항:
1. 실제 본문 내용이 있는 '장' 수준의 항목만 식별
2. 목차, 서문, 부록, 색인, 참고문헌 등은 제외
3. 제목만 반환 (페이지 정보는 기존 목차에서 가져옴)

응답 형식 (JSON):
["장 제목1", "장 제목2", "장 제목3", ...]
"""
        return prompt.strip()
    
    @staticmethod
    def normalize_title(title: str) -> str:
        """제목 정규화 (기존 로직 이관)"""
        import re
        
        # 기본 정규화
        normalized = title.strip()
        
        # 특수문자 제거 및 공백을 언더스코어로 변경
        normalized = re.sub(r'[^\w\s-]', '', normalized)
        normalized = re.sub(r'[-\s]+', '_', normalized)
        
        # 연속된 언더스코어 정리
        normalized = re.sub(r'_+', '_', normalized)
        
        # 시작/끝 언더스코어 제거
        normalized = normalized.strip('_')
        
        return normalized if normalized else "untitled"