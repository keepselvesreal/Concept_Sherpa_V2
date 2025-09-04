# 생성 시간: Thu Sep  4 08:45:12 KST 2025
# 핵심 내용: 장 추출 및 처리 서비스 (extract_chapters_v5 함수들 이관)
# 상세 내용:
#   - ChapterExtractionService (라인 30-280): 메인 장 추출 서비스 클래스
#   - normalize_title (라인 35-40): 제목 정규화 메서드
#   - extract_pdf_content (라인 42-78): PDF 페이지별 텍스트 추출 메서드
#   - count_chapters_with_ai (라인 80-165): AI 기반 장 분석 메서드
#   - find_chapter_items (라인 167-210): 장별 목차 항목 찾기 메서드
#   - save_chapter_content_to_folder (라인 212-280): 장별 폴더 생성 및 저장 메서드
# 상태: active
# 참조: extract_chapters_v5.py 원본 함수들

import asyncio
import json
import os
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

# 환경변수 로드
try:
    from dotenv import load_dotenv
    load_dotenv(".env")
except ImportError:
    print("⚠️  python-dotenv가 설치되지 않음. 환경변수 직접 설정 필요")

# PDF 처리를 위한 라이브러리
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# AI 제공자 인터페이스 (원본에서 이관)
class AIProvider(ABC):
    """AI 제공자 추상 베이스 클래스"""
    
    @abstractmethod
    async def query(self, prompt: str) -> str:
        """AI에 질의하고 응답을 반환"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        pass

class ClaudeSDKProvider(AIProvider):
    """Claude SDK 구현체"""
    
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        # Max Plan 사용자는 Claude Code CLI 기반 인증 사용 - API 키 환경변수 제거
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
            self.logger.info("ANTHROPIC_API_KEY 환경변수 제거됨 - Claude Code CLI 인증 사용")
    
    async def query(self, prompt: str) -> str:
        try:
            self.logger.info("Claude SDK 임포트 시도 중...")
            from claude_code_sdk import query as claude_query
            self.logger.info("Claude SDK 임포트 성공")
            
            self.logger.info("Claude SDK 쿼리 실행 중...")
            responses = []
            
            async for message in claude_query(prompt=prompt):
                self.logger.info(f"메시지 타입: {type(message).__name__}")
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                                self.logger.info(f"응답 받음: {block.text[:100]}...")
                    elif hasattr(content, 'text'):
                        responses.append(content.text)
                        self.logger.info(f"응답 받음: {content.text[:100]}...")
            
            response_text = '\n'.join(responses) if responses else ''
            self.logger.info(f"Claude SDK 응답 길이: {len(response_text)} 문자")
            return response_text
            
        except Exception as e:
            self.logger.error(f"Claude SDK 실행 실패: {str(e)}")
            raise

    def get_name(self) -> str:
        return "Claude SDK"

class GeminiAPIProvider(AIProvider):
    """Gemini API 구현체"""
    
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        # ConfigManager를 통해 AI 설정에서 API 키 가져오기
        ai_config = self.config_manager.get_ai_config()
        self.api_key = ai_config.get('gemini', {}).get('api_key') or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. config/ai_config.yaml 또는 환경변수를 확인하세요")
    
    async def query(self, prompt: str) -> str:
        try:
            self.logger.info("Gemini API 클라이언트 초기화 중...")
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            self.logger.info("Gemini API 클라이언트 초기화 성공")
            
            self.logger.info("Gemini API 쿼리 실행 중...")
            response = model.generate_content(prompt)
            
            response_text = response.text if hasattr(response, 'text') else str(response)
            self.logger.info(f"Gemini API 응답 길이: {len(response_text)} 문자")
            self.logger.info(f"응답 받음: {response_text[:100]}...")
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Gemini API 실행 실패: {str(e)}")
            raise

    def get_name(self) -> str:
        return "Gemini API"

class ChapterExtractionService:
    """장 추출 및 처리 서비스"""
    
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
    
    def create_ai_provider(self, provider_type: str = "gemini") -> AIProvider:
        """AI 제공자 생성 팩토리 메서드"""
        if provider_type.lower() == "gemini":
            return GeminiAPIProvider(self.config_manager, self.logger)
        elif provider_type.lower() == "claude":
            return ClaudeSDKProvider(self.config_manager, self.logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공자: {provider_type}")
        
    def normalize_title(self, title: str) -> str:
        """제목 정규화 함수 - 특수문자 제거 및 언더스코어 변환"""
        title_clean = re.sub(r'[^\w\s.-]', '', title)  # 점(.)도 유지
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        return title_clean

    def extract_pdf_content(self, pdf_path: str, start_page: int, end_page: int) -> str:
        """PDF에서 특정 페이지 범위의 텍스트 추출"""
        if fitz is None:
            self.logger.error("PyMuPDF가 설치되지 않아 PDF 내용 추출을 할 수 없습니다")
            return ""
        
        try:
            # PDF 열기
            doc = fitz.open(pdf_path)
            self.logger.info(f"PDF 열기 성공: {pdf_path} (총 {len(doc)} 페이지)")
            
            extracted_text = []
            
            # 페이지 범위 조정 (1-based → 0-based)
            start_idx = max(0, start_page - 1)
            end_idx = min(len(doc), end_page)
            
            self.logger.info(f"페이지 범위: {start_page}-{end_page} (실제: {start_idx+1}-{end_idx})")
            
            for page_num in range(start_idx, end_idx):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():  # 빈 페이지가 아닌 경우에만 추가
                    extracted_text.append(f"## Page {page_num + 1}\n\n{text}\n")
            
            doc.close()
            
            full_text = "\n".join(extracted_text)
            self.logger.info(f"추출된 텍스트 길이: {len(full_text)} 문자")
            
            return full_text
            
        except Exception as e:
            self.logger.error(f"PDF 내용 추출 실패: {str(e)}")
            return ""

    async def count_chapters_with_ai(self, toc_json_path: str, ai_provider: AIProvider) -> Dict[str, Any]:
        """간소화된 AI를 통한 장 개수 및 페이지 정보 확인 - 숫자 장만 찾기"""
        try:
            # 목차 파일 읽기
            self.logger.info(f"목차 파일 읽는 중: {toc_json_path}")
            with open(toc_json_path, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            # 목차 구조에서 toc_structure 추출
            if "toc_structure" in toc_data:
                toc_structure = toc_data["toc_structure"]
            else:
                toc_structure = toc_data
            
            self.logger.info(f"목차 항목 총 개수: {len(toc_structure)}")
            
            # 간소화된 AI 프롬프트 - 숫자 장만 찾기
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
            
            prompt = prompt + "\n\n" + json_template

            self.logger.info(f"AI({ai_provider.get_name()})에게 간소화된 장 분석 요청 중...")
            response_text = await ai_provider.query(prompt)
            
            self.logger.info(f"AI 응답 길이: {len(response_text)} 문자")
            
            # JSON 파싱 시도
            try:
                # ```json으로 감싸진 경우 처리
                if '```json' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start != -1 and json_end > json_start:
                        json_text = response_text[json_start:json_end]
                    else:
                        json_text = response_text
                else:
                    json_text = response_text
                
                parsed_result = json.loads(json_text)
                self.logger.info(f"파싱 성공: {parsed_result}")
                
                # 결과 검증 및 변환
                if 'chapters' in parsed_result and isinstance(parsed_result['chapters'], list):
                    chapters_info = parsed_result['chapters']
                    chapter_titles = [ch['title'] for ch in chapters_info]
                    
                    self.logger.info(f"분석 결과: {len(chapters_info)}개 장 식별")
                    
                    return {
                        'success': True,
                        'total_chapters': len(chapters_info),
                        'chapter_titles': chapter_titles,
                        'chapters_info': chapters_info,
                        'raw_response': response_text,
                        'ai_provider': ai_provider.get_name()
                    }
                else:
                    self.logger.error("응답에 유효한 'chapters' 배열이 없습니다")
                    return {
                        'success': False,
                        'error': "응답에 유효한 'chapters' 배열이 없습니다",
                        'raw_response': response_text,
                        'ai_provider': ai_provider.get_name()
                    }
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON 파싱 실패: {str(e)}")
                self.logger.error(f"원본 응답: {response_text}")
                
                return {
                    'success': False,
                    'error': f"JSON 파싱 실패: {str(e)}",
                    'raw_response': response_text,
                    'ai_provider': ai_provider.get_name()
                }
        
        except Exception as e:
            self.logger.error(f"장 개수 확인 실패: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'ai_provider': ai_provider.get_name() if ai_provider else "Unknown"
            }

    def find_chapter_items(self, toc_structure: List[Dict], chapter_start_id: int, next_chapter_start_id: Optional[int]) -> List[Dict]:
        """각 장에 속하는 목차 항목들을 찾는 함수 - v2 방식 유지"""
        chapter_items = []
        
        # ID로 항목을 빠르게 찾기 위한 딕셔너리 생성
        id_to_item = {item['id']: item for item in toc_structure}
        
        self.logger.info(f"장 시작 ID: {chapter_start_id}, 다음 장 시작 ID: {next_chapter_start_id}")
        
        # 해당 장의 시작 항목 찾기
        if chapter_start_id not in id_to_item:
            self.logger.error(f"장 시작 ID {chapter_start_id}를 찾을 수 없습니다")
            return chapter_items
            
        start_item = id_to_item[chapter_start_id]
        chapter_items.append(start_item)
        self.logger.info(f"장 시작 항목: {start_item['title']}")
        
        # 재귀적으로 하위 항목들을 수집하는 함수
        def collect_children(parent_id: int):
            if parent_id not in id_to_item:
                return
                
            parent_item = id_to_item[parent_id]
            children_ids = parent_item.get('children_ids', [])
            
            for child_id in children_ids:
                # 다음 장의 시작점에 도달하면 중단
                if next_chapter_start_id is not None and child_id >= next_chapter_start_id:
                    break
                    
                if child_id in id_to_item:
                    child_item = id_to_item[child_id]
                    chapter_items.append(child_item)
                    self.logger.debug(f"하위 항목 추가: {child_item['title']}")
                    
                    # 재귀적으로 하위 항목의 자식들도 수집
                    collect_children(child_id)
        
        # 장 시작 항목의 모든 하위 항목들 수집
        collect_children(chapter_start_id)
        
        self.logger.info(f"총 {len(chapter_items)}개 항목 수집됨")
        return chapter_items

    def save_chapter_content_to_folder(self, chapter_title: str, chapter_items: List[Dict], chapter_content: str, output_dir: Path):
        """장별 폴더에 정규화된 목차와 PDF 내용 저장"""
        # 장 제목 정규화
        normalized_chapter_title = self.normalize_title(chapter_title)
        self.logger.info(f"장 제목 정규화: '{chapter_title}' → '{normalized_chapter_title}'")
        
        # 장별 폴더 생성
        chapter_dir = output_dir / normalized_chapter_title
        chapter_dir.mkdir(exist_ok=True)
        self.logger.info(f"장 폴더 생성: {chapter_dir}")
        
        # 목차 항목들의 title도 정규화하여 저장
        normalized_items = []
        for item in chapter_items:
            normalized_item = item.copy()
            normalized_item['title'] = self.normalize_title(item['title'])
            normalized_items.append(normalized_item)
        
        # 1. 목차 파일 저장
        toc_filename = f"{normalized_chapter_title}_toc.json"
        toc_filepath = chapter_dir / toc_filename
        
        with open(toc_filepath, 'w', encoding='utf-8') as f:
            json.dump(normalized_items, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"장 '{chapter_title}' 목차 저장 완료: {toc_filepath}")
        
        # 2. PDF 내용 파일 저장
        content_filename = f"{normalized_chapter_title}_content.md"
        content_filepath = chapter_dir / content_filename
        
        if chapter_content:
            with open(content_filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {chapter_title}\n\n")
                f.write(chapter_content)
            self.logger.info(f"장 '{chapter_title}' 내용 저장 완료: {content_filepath}")
        else:
            self.logger.warning(f"장 '{chapter_title}' 내용이 비어있어 저장하지 않음")
            content_filepath = None
        
        return toc_filepath, content_filepath