# 생성 시간: Tue Sep  9 22:35:23 KST 2025
# 핵심 내용: 장 추출 및 처리 서비스 v4 (AI 서비스 v4 적용)
# 상세 내용:
#   - ChapterExtractionService (라인 30-226): 메인 장 추출 서비스 클래스
#   - extract_pdf_content (라인 39-63): PDF 페이지별 텍스트 추출 메서드
#   - count_chapters_with_ai (라인 65-180): AI 기반 장 분석 메서드 (ai_service_v4 + query_single_request 사용)
#   - find_chapter_items (라인 182-197): 장별 목차 항목 찾기 메서드
#   - save_chapter_content_to_folder (라인 199-226): 장별 폴더 생성 및 저장 메서드
# 상태: active
# 참조: chapter_extraction_service_v3.py (AI 서비스 v4 적용)

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# AI 서비스 및 텍스트 유틸리티 임포트
from services.ai_service_v4 import AIService
from utils.text_utils import normalize_title

# PDF 처리를 위한 라이브러리
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

class ChapterExtractionService:
    """장 추출 및 처리 서비스 - AI 서비스 v4 적용"""
    
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        # AI 서비스 초기화 (chapter_toc_extraction 단계용)
        self.ai_service = AIService(config_manager, logger, "chapter_toc_extraction")

    def extract_pdf_content(self, pdf_path: str, start_page: int, end_page: int) -> str:
        """PDF에서 특정 페이지 범위의 텍스트 추출"""
        if fitz is None:
            self.logger.error("PyMuPDF가 설치되지 않아 PDF 내용 추출을 할 수 없습니다")
            return ""
        
        try:
            doc = fitz.open(pdf_path)
            content = ""
            
            # 페이지 번호는 0 기반이므로 조정
            for page_num in range(start_page - 1, min(end_page, doc.page_count)):
                page = doc[page_num]
                text = page.get_text()
                content += f"\n--- 페이지 {page_num + 1} ---\n"
                content += text
                
            doc.close()
            
            self.logger.info(f"PDF 내용 추출 완료: 페이지 {start_page}-{end_page}, 총 {len(content)} 문자")
            return content
            
        except Exception as e:
            self.logger.error(f"PDF 내용 추출 실패: {e}")
            return ""

    async def count_chapters_with_ai(self, toc_file_path: str) -> Dict[str, Any]:
        """AI를 사용하여 목차에서 장 개수 분석"""
        try:
            # 목차 파일 읽기
            with open(toc_file_path, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            # 목차 구조 확인
            if isinstance(toc_data, dict) and 'toc_structure' in toc_data:
                toc_structure = toc_data['toc_structure']
            else:
                toc_structure = toc_data
            
            self.logger.info(f"목차 항목 총 개수: {len(toc_structure)}")
            
            # AI 프롬프트 구성
            toc_json_str = json.dumps(toc_structure, ensure_ascii=False, indent=2)
            
            prompt = f"""다음 목차에서 숫자로 된 장(chapter)만 찾아주세요.

목차 데이터:
{toc_json_str}

조건:
- 제목이 "1", "2", "3" 같은 숫자로 시작하는 장만 포함
- "A.1", "B.1", "C.1" 같은 부록은 제외
- "preface", "introduction", "contents", "index" 등은 제외

각 장의 페이지 범위 계산:
- 시작 페이지: 해당 항목의 page 값
- 종료 페이지: 다음 장의 시작 페이지 - 1

JSON만 응답:"""

            # JSON 템플릿 추가
            json_template = """{
    "chapters": [
        {
            "title": "1 Complexity of object- oriented programming",
            "start_page": 31,
            "end_page": 53
        },
        {
            "title": "2 Separation between code and data", 
            "start_page": 54,
            "end_page": 70
        }
    ]
}"""
            
            full_prompt = f"{prompt}\n\n응답 형식:\n{json_template}"
            
            # 추가 데이터 구성
            additional_data = {
                "toc_file_path": toc_file_path,
                "total_items": len(toc_structure),
                "task_type": "chapter_analysis"
            }
            
            # AI 서비스로 쿼리 실행 (🟢 변경: query → query_single_request)
            self.logger.info(f"AI 장 분석 시작 - {self.ai_service.get_name()}")
            response_text = await self.ai_service.query_single_request(full_prompt, additional_data)
            
            # JSON 응답 파싱
            try:
                # JSON 블록 찾기
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1)
                else:
                    # JSON 블록이 없으면 전체 응답에서 JSON 찾기
                    json_text = response_text.strip()
                
                result_data = json.loads(json_text)
                
                if 'chapters' in result_data and isinstance(result_data['chapters'], list):
                    individual_chapter_information = result_data['chapters']
                    chapter_titles = [chapter['title'] for chapter in individual_chapter_information]
                    
                    self.logger.info(f"장 분석 완료: 총 {len(individual_chapter_information)}개 장 발견")
                    
                    return {
                        'success': True,
                        'chapter_titles': chapter_titles,
                        'individual_chapter_information': individual_chapter_information,
                        'raw_response': response_text,
                        'ai_provider': self.ai_service.get_name()
                    }
                else:
                    self.logger.error("응답에 유효한 'chapters' 배열이 없습니다")
                    return {
                        'success': False,
                        'error': "응답에 유효한 'chapters' 배열이 없습니다",
                        'raw_response': response_text,
                        'ai_provider': self.ai_service.get_name()
                    }
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON 파싱 실패: {str(e)}")
                self.logger.error(f"원본 응답: {response_text}")
                
                return {
                    'success': False,
                    'error': f"JSON 파싱 실패: {str(e)}",
                    'raw_response': response_text,
                    'ai_provider': self.ai_service.get_name()
                }
        
        except Exception as e:
            self.logger.error(f"장 개수 확인 실패: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'ai_provider': self.ai_service.get_name() if hasattr(self, 'ai_service') else "Unknown"
            }

    def find_chapter_items(self, toc_structure: List[Dict], chapter_start_id: int, next_chapter_start_id: Optional[int]) -> List[Dict]:
        """각 장에 속하는 목차 항목들을 찾는 함수 - 마지막 장 페이지 범위 제한"""
        chapter_items = []
        
        # 마지막 장일 경우에만 페이지 범위 찾기
        chapter_end_page = None
        if not next_chapter_start_id:
            for item in toc_structure:
                if item.get('id') == chapter_start_id:
                    chapter_end_page = item.get('end_page')
                    break
        
        for item in toc_structure:
            item_id = item.get('id')
            if item_id is None:
                continue
                
            # 기본 ID 범위 체크
            if item_id < chapter_start_id:
                continue
                
            # 다음 장이 있으면 ID로 제한
            if next_chapter_start_id and item_id >= next_chapter_start_id:
                break
                
            # 마지막 장이면 페이지 범위로 제한
            if not next_chapter_start_id and chapter_end_page:
                item_start_page = item.get('start_page')
                if item_start_page and item_start_page > chapter_end_page:
                    break
            
            chapter_items.append(item)
                
        return chapter_items

    def save_chapter_content_to_folder(self, chapter_title: str, chapter_items: List[Dict], 
                                     chapter_content: str, output_base_dir: str) -> str:
        """장별 폴더 생성 및 내용 저장 - 정규화된 제목의 .md 파일로 저장"""
        try:
            # 폴더명 정규화
            normalized_title = normalize_title(chapter_title)
            chapter_folder = Path(output_base_dir) / f"{normalized_title}"
            chapter_folder.mkdir(parents=True, exist_ok=True)
            
            # 장 내용을 정규화된 제목의 .md 파일로 저장
            content_file = chapter_folder / f"{normalized_title}_content.md"
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(f"# {chapter_title}\n\n")
                f.write(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(chapter_content)
            
            # 목차 항목 저장
            items_file = chapter_folder / f"{normalized_title}_toc.json"
            with open(items_file, 'w', encoding='utf-8') as f:
                json.dump(chapter_items, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"장 폴더 생성 완료: {chapter_folder}")
            return str(chapter_folder)
            
        except Exception as e:
            self.logger.error(f"장 폴더 생성 실패: {e}")
            return ""