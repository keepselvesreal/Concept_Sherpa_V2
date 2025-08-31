# 생성 시간: 2025-08-31 20:50:00 KST
# 핵심 내용: 간소화된 AI 프롬프트로 실제 장만 추출하는 모듈 (v2 기반 + PDF 내용 추출)
# 상세 내용:
#   - normalize_title (라인 35): 제목 정규화 함수 (특수문자 제거 및 언더스코어 변환)
#   - extract_pdf_content (라인 40): PDF에서 페이지 범위별 텍스트 추출 함수
#   - setup_logging (라인 55): 로깅 설정 및 로그 파일 생성
#   - AIProvider (라인 75): AI 제공자 추상 베이스 클래스
#   - ClaudeSDKProvider (라인 95): Claude SDK 구현체
#   - GeminiAPIProvider (라인 135): Gemini API 구현체
#   - count_chapters_with_ai (라인 195): 간소화된 AI를 통한 장 개수 및 페이지 정보 확인
#   - find_chapter_items (라인 265): 각 장에 속하는 목차 항목들을 찾는 함수 (v2 방식)
#   - save_chapter_content_to_folder (라인 315): 장별 폴더에 PDF 내용과 정규화된 목차 저장
#   - extract_chapters_programmatically (라인 355): 프로그래밍적 목차 및 내용 추출 (폴더 생성 포함)
#   - process_chapters (라인 455): 전체 처리 워크플로우 (PDF 내용 추출 포함)
#   - main (라인 525): 메인 실행 함수
# 상태: active
# 참조: extract_chapters_v2

import asyncio
import json
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# PDF 처리를 위한 추가 라이브러리
try:
    import fitz  # PyMuPDF
except ImportError:
    print("⚠️  PyMuPDF가 설치되지 않음. 'uv add PyMuPDF'를 실행하세요")
    fitz = None

def normalize_title(title: str) -> str:
    """제목 정규화 함수 - 특수문자 제거 및 언더스코어 변환"""
    title_clean = re.sub(r'[^\w\s.-]', '', title)  # 점(.)도 유지
    title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
    return title_clean

def extract_pdf_content(pdf_path: str, start_page: int, end_page: int, logger) -> str:
    """PDF에서 특정 페이지 범위의 텍스트 추출"""
    if fitz is None:
        logger.error("PyMuPDF가 설치되지 않아 PDF 내용 추출을 할 수 없습니다")
        return ""
    
    try:
        # PDF 열기
        doc = fitz.open(pdf_path)
        logger.info(f"PDF 열기 성공: {pdf_path} (총 {len(doc)} 페이지)")
        
        extracted_text = []
        
        # 페이지 범위 조정 (1-based → 0-based)
        start_idx = max(0, start_page - 1)
        end_idx = min(len(doc), end_page)
        
        logger.info(f"페이지 범위: {start_page}-{end_page} (실제: {start_idx+1}-{end_idx})")
        
        for page_num in range(start_idx, end_idx):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():  # 빈 페이지가 아닌 경우에만 추가
                extracted_text.append(f"## Page {page_num + 1}\n\n{text}\n")
        
        doc.close()
        
        full_text = "\n".join(extracted_text)
        logger.info(f"추출된 텍스트 길이: {len(full_text)} 문자")
        
        return full_text
        
    except Exception as e:
        logger.error(f"PDF 내용 추출 실패: {str(e)}")
        return ""

# 환경 변수 로드
try:
    from dotenv import load_dotenv
    load_dotenv("../.env")
except ImportError:
    print("⚠️  python-dotenv가 설치되지 않음. 환경변수 직접 설정 필요")

# YAML 설정 파일 로드
try:
    import yaml
except ImportError:
    print("⚠️  PyYAML이 설치되지 않음. 'uv add PyYAML'를 실행하세요")
    yaml = None

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """설정 파일 로드"""
    if yaml is None:
        return {
            'ai_provider': {'type': 'claude'},
            'models': {'claude': 'claude-3-sonnet-20240229', 'gemini': 'gemini-2.0-flash-exp'},
            'logging': {'level': 'INFO', 'save_logs': True},
            'output': {'directory': 'chapters', 'clean_before_run': True}
        }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"⚠️  설정 파일 {config_path}를 찾을 수 없음. 기본 설정 사용")
        return {
            'ai_provider': {'type': 'claude'},
            'models': {'claude': 'claude-3-sonnet-20240229', 'gemini': 'gemini-2.0-flash-exp'},
            'logging': {'level': 'INFO', 'save_logs': True},
            'output': {'directory': 'chapters', 'clean_before_run': True}
        }

def setup_logging(operation_name: str = "extract_chapters", config: Dict[str, Any] = None):
    """로깅 설정 및 로그 파일 생성"""
    if config is None:
        config = load_config()
    
    # 로그 레벨 설정
    log_level = getattr(logging, config.get('logging', {}).get('level', 'INFO'))
    
    handlers = [logging.StreamHandler()]
    
    # 파일 로그 저장 설정
    if config.get('logging', {}).get('save_logs', True):
        # 로그 디렉토리 생성
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 로그 파일명 (타임스탬프 포함)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"{operation_name}_{timestamp}.log"
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    # 로깅 설정
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    logger = logging.getLogger(__name__)
    if config.get('logging', {}).get('save_logs', True):
        logger.info(f"로그 파일: {log_file}")
    return logger

class AIProvider(ABC):
    """AI 제공자 추상 베이스 클래스"""
    
    @abstractmethod
    async def query(self, prompt: str) -> str:
        """AI에게 쿼리를 보내고 응답을 받는 메서드"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        pass

class ClaudeSDKProvider(AIProvider):
    """Claude SDK 구현체"""
    
    def __init__(self, logger):
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
    
    def __init__(self, logger):
        self.logger = logger
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다")
    
    async def query(self, prompt: str) -> str:
        try:
            self.logger.info("Gemini API 클라이언트 초기화 중...")
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
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

async def count_chapters_with_ai(toc_json_path: str, ai_provider: AIProvider, logger) -> Dict[str, Any]:
    """간소화된 AI를 통한 장 개수 및 페이지 정보 확인 - 숫자 장만 찾기"""
    try:
        # 목차 파일 읽기
        logger.info(f"목차 파일 읽는 중: {toc_json_path}")
        with open(toc_json_path, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        
        # 목차 구조에서 toc_structure 추출
        if "toc_structure" in toc_data:
            toc_structure = toc_data["toc_structure"]
        else:
            toc_structure = toc_data
        
        logger.info(f"목차 항목 총 개수: {len(toc_structure)}")
        
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

        logger.info(f"AI({ai_provider.get_name()})에게 간소화된 장 분석 요청 중...")
        response_text = await ai_provider.query(prompt)
        
        logger.info(f"AI 응답 길이: {len(response_text)} 문자")
        
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
            logger.info(f"파싱 성공: {parsed_result}")
            
            # 결과 검증 및 변환
            if 'chapters' in parsed_result and isinstance(parsed_result['chapters'], list):
                chapters_info = parsed_result['chapters']
                chapter_titles = [ch['title'] for ch in chapters_info]
                
                logger.info(f"분석 결과: {len(chapters_info)}개 장 식별")
                
                return {
                    'success': True,
                    'total_chapters': len(chapters_info),
                    'chapter_titles': chapter_titles,
                    'chapters_info': chapters_info,
                    'raw_response': response_text,
                    'ai_provider': ai_provider.get_name()
                }
            else:
                logger.error("응답에 유효한 'chapters' 배열이 없습니다")
                return {
                    'success': False,
                    'error': "응답에 유효한 'chapters' 배열이 없습니다",
                    'raw_response': response_text,
                    'ai_provider': ai_provider.get_name()
                }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}")
            logger.error(f"원본 응답: {response_text}")
            
            return {
                'success': False,
                'error': f"JSON 파싱 실패: {str(e)}",
                'raw_response': response_text,
                'ai_provider': ai_provider.get_name()
            }
    
    except Exception as e:
        logger.error(f"장 개수 확인 실패: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'ai_provider': ai_provider.get_name() if ai_provider else "Unknown"
        }

def find_chapter_items(toc_structure: List[Dict], chapter_start_id: int, next_chapter_start_id: Optional[int], logger) -> List[Dict]:
    """각 장에 속하는 목차 항목들을 찾는 함수 - v2 방식 유지"""
    chapter_items = []
    
    # ID로 항목을 빠르게 찾기 위한 딕셔너리 생성
    id_to_item = {item['id']: item for item in toc_structure}
    
    logger.info(f"장 시작 ID: {chapter_start_id}, 다음 장 시작 ID: {next_chapter_start_id}")
    
    # 해당 장의 시작 항목 찾기
    if chapter_start_id not in id_to_item:
        logger.error(f"장 시작 ID {chapter_start_id}를 찾을 수 없습니다.")
        return []
    
    chapter_start_item = id_to_item[chapter_start_id]
    chapter_items.append(chapter_start_item)
    logger.info(f"장 시작 항목: {chapter_start_item['title']}")
    
    # 해당 장에 속하는 모든 하위 항목들을 재귀적으로 수집
    def collect_children(item_id: int):
        """주어진 항목의 모든 하위 항목들을 재귀적으로 수집"""
        if item_id not in id_to_item:
            return
        
        item = id_to_item[item_id]
        children_ids = item.get('children_ids', [])
        
        for child_id in children_ids:
            # 다음 장 시작점에 도달하면 중단
            if next_chapter_start_id and child_id == next_chapter_start_id:
                logger.info(f"다음 장 시작점 도달: {child_id}")
                return
                
            if child_id in id_to_item:
                child_item = id_to_item[child_id]
                chapter_items.append(child_item)
                logger.debug(f"하위 항목 추가: {child_item['title']}")
                
                # 재귀적으로 하위 항목의 자식들도 수집
                collect_children(child_id)
    
    # 장 시작 항목의 모든 하위 항목들 수집
    collect_children(chapter_start_id)
    
    logger.info(f"총 {len(chapter_items)}개 항목 수집됨")
    return chapter_items

def save_chapter_content_to_folder(chapter_title: str, chapter_items: List[Dict], chapter_content: str, output_dir: Path, logger):
    """장별 폴더에 정규화된 목차와 PDF 내용 저장"""
    # 장 제목 정규화
    normalized_chapter_title = normalize_title(chapter_title)
    logger.info(f"장 제목 정규화: '{chapter_title}' → '{normalized_chapter_title}'")
    
    # 장별 폴더 생성
    chapter_dir = output_dir / normalized_chapter_title
    chapter_dir.mkdir(exist_ok=True)
    logger.info(f"장 폴더 생성: {chapter_dir}")
    
    # 목차 항목들의 title도 정규화하여 저장
    normalized_items = []
    for item in chapter_items:
        normalized_item = item.copy()
        normalized_item['title'] = normalize_title(item['title'])
        normalized_items.append(normalized_item)
    
    # 1. 목차 파일 저장
    toc_filename = f"{normalized_chapter_title}_toc.json"
    toc_filepath = chapter_dir / toc_filename
    
    with open(toc_filepath, 'w', encoding='utf-8') as f:
        json.dump(normalized_items, f, ensure_ascii=False, indent=2)
    
    logger.info(f"장 '{chapter_title}' 목차 저장 완료: {toc_filepath}")
    
    # 2. PDF 내용 파일 저장
    content_filename = f"{normalized_chapter_title}_content.md"
    content_filepath = chapter_dir / content_filename
    
    if chapter_content:
        with open(content_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter_title}\n\n")
            f.write(chapter_content)
        logger.info(f"장 '{chapter_title}' 내용 저장 완료: {content_filepath}")
    else:
        logger.warning(f"장 '{chapter_title}' 내용이 비어있어 저장하지 않음")
    
    return toc_filepath, content_filepath if chapter_content else None

def extract_chapters_programmatically(toc_structure: List[Dict], chapters_info: List[Dict], logger, config: Dict[str, Any]):
    """프로그래밍적으로 각 장별 목차 및 내용 추출 - v2 기반"""
    try:
        # 출력 디렉토리 설정
        output_dir_name = config.get('output', {}).get('directory', 'chapters')
        output_dir = Path(output_dir_name)
        
        # 기존 디렉토리 정리 설정
        if config.get('output', {}).get('clean_before_run', True) and output_dir.exists():
            import shutil
            shutil.rmtree(output_dir)
            logger.info(f"기존 {output_dir_name} 디렉토리 정리 완료")
        
        output_dir.mkdir(exist_ok=True)
        logger.info(f"출력 디렉토리: {output_dir}")
        
        # ID로 항목을 빠르게 찾기 위한 딕셔너리 생성
        id_to_item = {item['id']: item for item in toc_structure}
        
        # 각 장별로 목차 항목 추출 및 저장
        extracted_files = []
        for i, chapter_info in enumerate(chapters_info):
            chapter_number = i + 1
            chapter_title = chapter_info['title']
            
            logger.info(f"=== 장 {chapter_number} 추출 시작: {chapter_title} ===")
            
            # 목차에서 해당 장 제목을 가진 항목 찾기
            chapter_item = None
            for item in toc_structure:
                if item['title'] == chapter_title:
                    chapter_item = item
                    break
            
            if not chapter_item:
                logger.warning(f"장 {chapter_number} '{chapter_title}'에 해당하는 목차 항목을 찾을 수 없습니다.")
                continue
            
            chapter_id = chapter_item['id']
            
            # 다음 장의 ID 찾기
            next_chapter_id = None
            if i + 1 < len(chapters_info):
                next_chapter_title = chapters_info[i + 1]['title']
                for item in toc_structure:
                    if item['title'] == next_chapter_title:
                        next_chapter_id = item['id']
                        break
            
            # 해당 장의 목차 항목들 추출
            chapter_items = find_chapter_items(
                toc_structure, 
                chapter_id, 
                next_chapter_id, 
                logger
            )
            
            if chapter_items:
                # PDF 내용 추출 (페이지 정보가 있는 경우)
                chapter_content = ""
                if 'start_page' in chapter_info and 'end_page' in chapter_info:
                    pdf_path = config.get('pdf_path', '')
                    if pdf_path and Path(pdf_path).exists():
                        logger.info(f"장 {chapter_number} PDF 내용 추출 시작: 페이지 {chapter_info['start_page']}-{chapter_info['end_page']}")
                        chapter_content = extract_pdf_content(
                            pdf_path, 
                            chapter_info['start_page'], 
                            chapter_info['end_page'], 
                            logger
                        )
                    else:
                        logger.warning(f"PDF 파일을 찾을 수 없음: {pdf_path}")
                
                # 장별 폴더에 목차와 내용 저장
                saved_files = save_chapter_content_to_folder(
                    chapter_title, 
                    chapter_items, 
                    chapter_content,
                    output_dir, 
                    logger
                )
                extracted_files.extend([f for f in saved_files if f is not None])
                logger.info(f"장 {chapter_number} 추출 완료: {len(chapter_items)}개 항목")
            else:
                logger.error(f"장 {chapter_number} 추출 실패")
        
        return {
            'success': True,
            'extracted_chapters': len([f for f in extracted_files if f]),
            'extracted_files': [str(f) for f in extracted_files if f],
            'output_directory': str(output_dir)
        }
        
    except Exception as e:
        logger.error(f"장별 목차 추출 실패: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

async def process_chapters(toc_json_path: str, config: Dict[str, Any], logger):
    """전체 처리 워크플로우: AI로 숫자 장 확인 → 프로그래밍적으로 목차 및 내용 추출"""
    try:
        # 목차 파일 읽기
        logger.info(f"목차 파일 읽는 중: {toc_json_path}")
        with open(toc_json_path, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        
        # 목차 구조에서 toc_structure 추출
        if "toc_structure" in toc_data:
            toc_structure = toc_data["toc_structure"]
        else:
            toc_structure = toc_data
        
        # AI 제공자 초기화 (config에서 설정 읽기)
        ai_provider_setting = config.get('ai_provider', 'claude')
        if isinstance(ai_provider_setting, dict):
            ai_provider_type = ai_provider_setting.get('type', 'claude').lower()
        else:
            ai_provider_type = str(ai_provider_setting).lower()
        if ai_provider_type == 'claude':
            ai_provider = ClaudeSDKProvider(logger)
        elif ai_provider_type == 'gemini':
            ai_provider = GeminiAPIProvider(logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공자: {ai_provider_type}. 'claude' 또는 'gemini'를 사용하세요.")
        
        logger.info(f"AI 제공자: {ai_provider.get_name()} (config에서 설정됨)")
        
        # 1단계: AI로 숫자 장만 확인
        logger.info("=== 1단계: 숫자 장 확인 시작 ===")
        count_result = await count_chapters_with_ai(toc_json_path, ai_provider, logger)
        
        if not count_result['success']:
            logger.error("❌ 장 개수 확인 실패")
            return count_result
        
        chapters_info = count_result.get('chapters_info', [])
        chapter_titles = count_result['chapter_titles']
        logger.info(f"✅ {count_result['total_chapters']}개 숫자 장 발견")
        
        if chapters_info:
            logger.info("AI가 식별한 장별 페이지 정보:")
            for i, chapter_info in enumerate(chapters_info, 1):
                logger.info(f"  장 {i}: {chapter_info.get('title', 'N/A')} (페이지 {chapter_info.get('start_page', 'N/A')}-{chapter_info.get('end_page', 'N/A')})")
        
        logger.info("=== 1단계: 숫자 장 확인 완료 ===")
        
        # 2단계: 프로그래밍적으로 각 장별 목차 및 내용 추출
        logger.info("=== 2단계: 각 장별 목차 및 내용 추출 시작 ===")
        extract_result = extract_chapters_programmatically(toc_structure, chapters_info, logger, config)
        
        if not extract_result['success']:
            logger.error("❌ 장별 목차 추출 실패")
            return extract_result
        
        logger.info("✅ 장별 목차 및 내용 추출 성공")
        logger.info("=== 2단계: 각 장별 목차 및 내용 추출 완료 ===")
        
        # 최종 결과 합성
        final_result = {
            'success': True,
            'ai_provider': ai_provider.get_name(),
            'total_chapters': count_result['total_chapters'],
            'chapter_titles': chapter_titles,
            'chapters_info': chapters_info,
            'extracted_chapters': extract_result['extracted_chapters'],
            'extracted_files': extract_result['extracted_files'],
            'output_directory': extract_result['output_directory'],
            'processing_time': datetime.now().isoformat(),
            'config_used': ai_provider_type
        }
        
        return final_result
        
    except Exception as e:
        logger.error(f"전체 처리 실패: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

async def main():
    """메인 실행 함수"""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("사용법: python extract_chapters_v5.py <목차JSON파일> <PDF파일> [config파일]")
        print("예시: python extract_chapters_v5.py toc.json book.pdf")
        print("예시: python extract_chapters_v5.py toc.json book.pdf config.yaml")
        print()
        print("AI 제공자는 config.yaml 파일에서 설정:")
        print("  ai_provider:")
        print("    type: 'claude'  # 또는 'gemini'")
        sys.exit(1)
    
    toc_file = sys.argv[1]
    pdf_file = sys.argv[2]
    config_file = sys.argv[3] if len(sys.argv) == 4 else "config.yaml"
    
    if not Path(toc_file).exists():
        print(f"❌ 목차 파일을 찾을 수 없습니다: {toc_file}")
        sys.exit(1)
    
    if not Path(pdf_file).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_file}")
        sys.exit(1)
    
    # 설정 파일 로드
    config = load_config(config_file)
    
    if not isinstance(config, dict):
        config = {'ai_provider': {'type': 'claude'}}  # 기본값 설정
    
    config['pdf_path'] = pdf_file  # PDF 경로 추가
    
    # AI 제공자 설정 처리 (문자열 또는 딕셔너리 형태)
    ai_provider_setting = config.get('ai_provider', 'claude')
    if isinstance(ai_provider_setting, dict):
        ai_provider_type = ai_provider_setting.get('type', 'claude')
    else:
        ai_provider_type = str(ai_provider_setting)
    
    if ai_provider_type.lower() not in ['claude', 'gemini']:
        print(f"❌ config 파일의 AI 제공자가 잘못되었습니다: {ai_provider_type}")
        print("config.yaml에서 ai_provider.type을 'claude' 또는 'gemini'로 설정하세요.")
        sys.exit(1)
    
    # 로거 설정 (config 기반)
    logger = setup_logging("extract_chapters_v5", config)
    logger.info(f"=== 간소화된 숫자 장 추출 시작 (AI: {ai_provider_type.upper()}, Config: {config_file}) ===")
    logger.info(f"설정 파일: {config_file}")
    logger.info(f"PDF 파일: {pdf_file}")
    
    # 전체 처리 실행
    result = await process_chapters(toc_file, config, logger)
    
    if result['success']:
        logger.info("✅ 전체 처리 성공")
        print(f"✅ {result['ai_provider']}를 사용하여 {result['extracted_chapters']}개 장의 목차 및 내용이 추출되었습니다")
        print(f"📁 출력 디렉토리: {result['output_directory']}")
        print(f"\n📚 총 {len(result['chapter_titles'])}개 장:")
        for i, title in enumerate(result['chapter_titles'], 1):
            print(f"  {i}. {title}")
        
        # 결과를 파일로 저장
        result_file = f"extract_chapters_v5_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"결과 저장: {result_file}")
        print(f"\n💾 결과가 {result_file}에 저장되었습니다")
        
    else:
        logger.error("❌ 전체 처리 실패")
        print(f"❌ 전체 처리 실패: {result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    logger.info("=== 간소화된 숫자 장 추출 완료 ===")

if __name__ == "__main__":
    asyncio.run(main())