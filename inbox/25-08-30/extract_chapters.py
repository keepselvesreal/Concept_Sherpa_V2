# 생성 시간: 2025-08-30 11:12:46 KST
# 핵심 내용: SDK와 AI API 교체 가능한 통합 목차 추출 모듈
# 상세 내용:
#   - setup_logging (라인 35): 로깅 설정 및 로그 파일 생성
#   - AIProvider (라인 55): AI 제공자 추상 베이스 클래스
#   - ClaudeSDKProvider (라인 75): Claude SDK 구현체
#   - GeminiAPIProvider (라인 115): Gemini API 구현체
#   - count_chapters_with_ai (라인 175): AI를 통한 장 개수 확인
#   - find_chapter_items (라인 235): 각 장에 속하는 목차 항목들을 찾는 함수
#   - save_chapter_toc_simple (라인 285): 간단한 JSON 배열로 장별 목차 저장
#   - extract_chapters_programmatically (라인 305): 프로그래밍적 목차 추출
#   - process_chapters (라인 385): 전체 처리 워크플로우
#   - main (라인 455): 메인 실행 함수
# 상태: active
# 주소: extract_chapters
# 참조: step1_count_chapters.py, step2_extract_by_chapters_v2.py

import asyncio
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

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
    """AI를 통한 장 개수 확인"""
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
        
        # AI에게 장 개수 확인 요청
        prompt = f"""다음 목차 데이터를 분석하여 총 몇 개의 장(chapter)이 있는지 확인해주세요.

목차 데이터:
{json.dumps(toc_structure, ensure_ascii=False, indent=2)}

작업:
1. 메인 장(chapter)에 해당하는 항목들을 식별하세요
2. 총 장의 개수를 계산하세요
3. 각 장의 제목을 나열하세요

응답 형식:
{{
    "total_chapters": 숫자,
    "chapter_titles": ["장1 제목", "장2 제목", ...]
}}"""

        logger.info(f"AI({ai_provider.get_name()})에게 장 개수 확인 요청 중...")
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
            
            return {
                'success': True,
                'total_chapters': parsed_result.get('total_chapters', 0),
                'chapter_titles': parsed_result.get('chapter_titles', []),
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
    """각 장에 속하는 목차 항목들을 찾는 함수"""
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

def save_chapter_toc_simple(chapter_title: str, chapter_items: List[Dict], output_dir: Path, logger):
    """간단한 JSON 배열로 장별 목차 저장"""
    # 파일명 생성 (장 제목만 사용, 특수문자 제거)
    safe_title = chapter_title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    filename = f"{safe_title}.json"
    filepath = output_dir / filename
    
    # toc_items만 저장 (간단한 배열 형식)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chapter_items, f, ensure_ascii=False, indent=2)
    
    logger.info(f"장 '{chapter_title}' 저장 완료: {filepath}")
    return filepath

def extract_chapters_programmatically(toc_structure: List[Dict], chapter_titles: List[str], logger, config: Dict[str, Any]):
    """프로그래밍적으로 각 장별 목차 추출"""
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
        
        # 각 장 제목으로 목차에서 해당 항목 찾기
        chapter_mappings = []
        for i, chapter_title in enumerate(chapter_titles):
            chapter_number = i + 1
            
            # 목차에서 해당 장 제목을 가진 항목 찾기
            chapter_item = None
            for item in toc_structure:
                if item['title'] == chapter_title:
                    chapter_item = item
                    break
            
            if chapter_item:
                chapter_mappings.append({
                    'chapter_number': chapter_number,
                    'title': chapter_title,
                    'id': chapter_item['id'],
                    'item': chapter_item
                })
                logger.info(f"장 {chapter_number}: {chapter_title} (ID: {chapter_item['id']})")
            else:
                logger.warning(f"장 {chapter_number} '{chapter_title}'에 해당하는 목차 항목을 찾을 수 없습니다.")
        
        # 각 장별로 목차 항목 추출 및 저장
        extracted_files = []
        for i, chapter_info in enumerate(chapter_mappings):
            logger.info(f"=== 장 {chapter_info['chapter_number']} 추출 시작 ===")
            
            # 다음 장의 시작 ID 찾기
            next_chapter_start_id = None
            if i + 1 < len(chapter_mappings):
                next_chapter_start_id = chapter_mappings[i + 1]['id']
            
            # 해당 장의 목차 항목들 추출
            chapter_items = find_chapter_items(
                toc_structure, 
                chapter_info['id'], 
                next_chapter_start_id, 
                logger
            )
            
            if chapter_items:
                # 간단한 형식으로 파일 저장
                saved_file = save_chapter_toc_simple(
                    chapter_info['title'], 
                    chapter_items, 
                    output_dir, 
                    logger
                )
                extracted_files.append(saved_file)
                logger.info(f"장 {chapter_info['chapter_number']} 추출 완료: {len(chapter_items)}개 항목")
            else:
                logger.error(f"장 {chapter_info['chapter_number']} 추출 실패")
        
        return {
            'success': True,
            'extracted_chapters': len(extracted_files),
            'extracted_files': [str(f) for f in extracted_files],
            'output_directory': str(output_dir)
        }
        
    except Exception as e:
        logger.error(f"장별 목차 추출 실패: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

async def process_chapters(toc_json_path: str, config: Dict[str, Any], logger):
    """전체 처리 워크플로우: AI로 장 확인 → 프로그래밍적으로 목차 추출"""
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
        ai_provider_type = config.get('ai_provider', {}).get('type', 'claude').lower()
        if ai_provider_type == 'claude':
            ai_provider = ClaudeSDKProvider(logger)
        elif ai_provider_type == 'gemini':
            ai_provider = GeminiAPIProvider(logger)
        else:
            raise ValueError(f"지원하지 않는 AI 제공자: {ai_provider_type}. 'claude' 또는 'gemini'를 사용하세요.")
        
        logger.info(f"AI 제공자: {ai_provider.get_name()} (config에서 설정됨)")
        
        # 1단계: AI로 장 개수 확인
        logger.info("=== 1단계: 전체 장 개수 확인 시작 ===")
        count_result = await count_chapters_with_ai(toc_json_path, ai_provider, logger)
        
        if not count_result['success']:
            logger.error("❌ 장 개수 확인 실패")
            return count_result
        
        chapter_titles = count_result['chapter_titles']
        logger.info(f"✅ {count_result['total_chapters']}개 장 발견")
        logger.info("=== 1단계: 전체 장 개수 확인 완료 ===")
        
        # 2단계: 프로그래밍적으로 각 장별 목차 추출
        logger.info("=== 2단계: 각 장별 목차 추출 시작 ===")
        extract_result = extract_chapters_programmatically(toc_structure, chapter_titles, logger, config)
        
        if not extract_result['success']:
            logger.error("❌ 장별 목차 추출 실패")
            return extract_result
        
        logger.info("✅ 장별 목차 추출 성공")
        logger.info("=== 2단계: 각 장별 목차 추출 완료 ===")
        
        # 최종 결과 합성
        final_result = {
            'success': True,
            'ai_provider': ai_provider.get_name(),
            'total_chapters': count_result['total_chapters'],
            'chapter_titles': chapter_titles,
            'extracted_chapters': extract_result['extracted_chapters'],
            'extracted_files': extract_result['extracted_files'],
            'output_directory': extract_result['output_directory'],
            'processing_time': datetime.now().isoformat(),
            'config_used': config.get('ai_provider', {}).get('type', 'claude')
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
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("사용법: python extract_chapters.py <목차JSON파일> [config파일]")
        print("예시: python extract_chapters.py toc.json")
        print("예시: python extract_chapters.py toc.json config.yaml")
        print()
        print("AI 제공자는 config.yaml 파일에서 설정:")
        print("  ai_provider:")
        print("    type: 'claude'  # 또는 'gemini'")
        sys.exit(1)
    
    toc_file = sys.argv[1]
    config_file = sys.argv[2] if len(sys.argv) == 3 else "config.yaml"
    
    if not Path(toc_file).exists():
        print(f"❌ 목차 파일을 찾을 수 없습니다: {toc_file}")
        sys.exit(1)
    
    # 설정 파일 로드
    config = load_config(config_file)
    ai_provider_type = config.get('ai_provider', {}).get('type', 'claude')
    
    if ai_provider_type.lower() not in ['claude', 'gemini']:
        print(f"❌ config 파일의 AI 제공자가 잘못되었습니다: {ai_provider_type}")
        print("config.yaml에서 ai_provider.type을 'claude' 또는 'gemini'로 설정하세요.")
        sys.exit(1)
    
    # 로거 설정 (config 기반)
    logger = setup_logging("extract_chapters", config)
    logger.info(f"=== 통합 목차 추출 시작 (AI: {ai_provider_type.upper()}, Config: {config_file}) ===")
    logger.info(f"설정 파일: {config_file}")
    
    # 전체 처리 실행
    result = await process_chapters(toc_file, config, logger)
    
    if result['success']:
        logger.info("✅ 전체 처리 성공")
        print(f"✅ {result['ai_provider']}를 사용하여 {result['extracted_chapters']}개 장의 목차가 추출되었습니다")
        print(f"📁 출력 디렉토리: {result['output_directory']}")
        print(f"\n📚 총 {len(result['chapter_titles'])}개 장:")
        for i, title in enumerate(result['chapter_titles'], 1):
            print(f"  {i}. {title}")
        
        # 결과를 파일로 저장
        result_file = f"extract_chapters_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"결과 저장: {result_file}")
        print(f"\n💾 결과가 {result_file}에 저장되었습니다")
        
    else:
        logger.error("❌ 전체 처리 실패")
        print(f"❌ 전체 처리 실패: {result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    logger.info("=== 통합 목차 추출 완료 ===")

if __name__ == "__main__":
    asyncio.run(main())