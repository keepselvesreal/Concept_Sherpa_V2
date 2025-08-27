# 생성 시간: 2025-08-26 15:01:01 KST
# 핵심 내용: 직전 대화와 현재 질의의 연관성을 분석하고 보충 응답을 생성하는 스크립트
# 상세 내용:
#   - main(): 메인 실행 함수, 인자 처리 및 전체 플로우 관리 (line 25-50)
#   - load_config(): config.yaml 파일 로드 및 설정 반환 (line 52-65)
#   - setup_logging(): 로깅 시스템 초기화 (line 67-85)
#   - find_latest_session(): 현재 날짜 폴더에서 가장 최근 세션 폴더 찾기 (line 87-110)
#   - load_previous_context(): 이전 질의와 응답 로드 (line 112-135)
#   - analyze_relevance(): AI를 통한 연관성 분석 및 보충 질의 생성 (line 137-180)
#   - generate_supplementary_response(): 보충 응답 생성 (line 182-230)
#   - load_reference_documents(): 참조 문서 전체 로드 및 결합 (line 232-265)
#   - save_results(): 최종 결과를 supplementary_{query_number}_answer.json으로 저장 (line 267-290)
# 상태: active
# 주소: supplementary_context_analyzer
# 참조: config.yaml, individual_document_processor.py, understanding_gap_analyzer.py

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

try:
    from claude_code_sdk import ClaudeCodeOptions, query as claude_query
except ImportError as e:
    print(f"❌ claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    sys.exit(1)


async def analyze_supplementary_context(current_query: str, session_id: str = None, query_number: int = None, 
                                       config_path: str = "config.yaml", verbose: bool = False):
    """보충 분석 메인 로직 (매개변수 방식)"""
    try:
        # 설정 및 로깅 초기화
        config = load_config(config_path)
        logger = setup_logging(config, verbose)
        
        logger.info(f"보충 분석 시작: {current_query}")
        
        # 매개변수 우선, 없으면 기존 로직
        if session_id and query_number is not None:
            # 매개변수로 받은 정보 사용
            logger.info(f"매개변수 사용: session_id={session_id[:20]}..., query_number={query_number}")
            
            # 공통 유틸리티 함수로 세션 폴더 찾기
            try:
                from common_utils import find_session_folder
                session_folder = find_session_folder(session_id, config, __file__)
            except FileNotFoundError as e:
                logger.error(str(e))
                return {'success': False, 'error': f"세션 폴더를 찾을 수 없습니다: {session_id}"}
                
            current_query_number = query_number
            
        else:
            # 기존 로직: 최신 세션 폴더 찾기
            logger.info("기존 로직 사용: 최신 세션 폴더에서 정보 추출")
            session_folder = find_latest_session()
            if not session_folder:
                logger.error("활성 세션을 찾을 수 없습니다")
                return {'success': False, 'error': "활성 세션을 찾을 수 없습니다"}
            
            # 기존 방식에서는 캐시에서 current_query_number 계산
            # (매개변수 방식이 아닌 경우에만 실행됨)
            logger.warning("기존 방식은 더 이상 지원되지 않습니다. 매개변수를 사용하세요.")
            return {'success': False, 'error': "매개변수 방식으로 호출하세요"}
        
        # 파일 중복 검사 (중복시 시스템 오류로 처리)
        supplementary_file = session_folder / f"supplementary_{current_query_number}_answer.json"
        if supplementary_file.exists():
            error_msg = f"중복 파일 발견: {supplementary_file} - 시스템 오류 가능성 (동일 query_number로 중복 실행됨)"
            logger.error(error_msg)
            raise FileExistsError(error_msg)
        
        # 이전 대화 내용 로드 (연관성 분석용)
        if session_id and query_number is not None:
            # 매개변수 방식: 현재 query_number를 사용해서 직전 대화 로드
            previous_context = load_previous_context(session_folder, current_query_number, logger)
            if not previous_context:
                logger.warning("직전 대화 내용을 찾을 수 없어 연관성 분석을 건너뜁니다")
                return {'success': False, 'error': "직전 대화 내용을 찾을 수 없습니다"}
        
        # 연관성 분석 및 보충 질의 생성
        relevance_result = await analyze_relevance(
            previous_context['query'], 
            current_query, 
            config, 
            logger
        )
        
        # 결과 저장용 데이터 구성
        result_data = {
            "query_number": current_query_number,
            "outputs": {
                "relevance_analysis": relevance_result
            }
        }
        
        # 연관성이 있는 경우 보충 응답 생성
        if relevance_result.get('is_relevant', False):
            logger.info("연관성이 확인되어 보충 응답을 생성합니다")
            supplementary_response = await generate_supplementary_response(
                relevance_result['generated_query'],
                config,
                logger
            )
            result_data['outputs']['supplementary_response'] = supplementary_response
        else:
            logger.info("연관성이 없어 분석을 종료합니다")
        
        # 결과 저장
        save_results(result_data, session_folder, logger)
        
        logger.info("보충 분석이 완료되었습니다")
        return {
            'success': True,
            'session_folder': str(session_folder),
            'query_number': current_query_number,
            'relevance_result': relevance_result
        }
        
    except Exception as e:
        logger.error(f"보충 분석 중 오류: {e}")
        return {'success': False, 'error': str(e)}


async def main():
    """CLI 실행 함수"""
    try:
        # 명령행 인자 파싱
        parser = argparse.ArgumentParser(description='직전 대화 연관성 분석 및 보충 응답 생성')
        parser.add_argument('current_query', type=str, help='현재 질의')
        parser.add_argument('--config', type=str, default='config.yaml', help='설정 파일 경로')
        parser.add_argument('--verbose', action='store_true', help='상세 로그 출력')
        
        args = parser.parse_args()
        
        # 새로운 함수 호출 (CLI에서는 매개변수 없음, 캐시/파일 기반)
        result = await analyze_supplementary_context(
            current_query=args.current_query,
            session_id=None,  # CLI에서는 None, 기존 로직 사용
            query_number=None,  # CLI에서는 None, 기존 로직 사용
            config_path=args.config,
            verbose=args.verbose
        )
        
        return 0 if result['success'] else 1
        
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
        return 1


def load_config(config_path: str) -> Dict:
    """설정 파일 로드"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"설정 파일 형식이 올바르지 않습니다: {e}")


def setup_logging(config: Dict, verbose: bool = False) -> logging.Logger:
    """로깅 시스템 초기화"""
    logger = logging.getLogger('supplementary_analyzer')
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 로그 레벨 설정
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # 포맷터
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


def find_latest_session() -> Optional[Path]:
    """현재 날짜 폴더에서 가장 최근 세션 폴더 찾기"""
    try:
        current_dir = Path.cwd()
        session_folders = []
        
        # session_으로 시작하는 폴더들 찾기
        for item in current_dir.iterdir():
            if item.is_dir() and item.name.startswith('session_'):
                try:
                    # 타임스탬프 추출 (session_{prefix}_{timestamp} 형태)
                    parts = item.name.split('_')
                    if len(parts) >= 3:
                        timestamp = parts[-1]  # 마지막 부분이 타임스탬프
                        session_folders.append((item, timestamp))
                except (ValueError, IndexError):
                    continue
        
        if not session_folders:
            return None
            
        # 타임스탬프 기준으로 정렬해서 가장 최근 것 반환
        session_folders.sort(key=lambda x: x[1], reverse=True)
        return session_folders[0][0]
        
    except Exception:
        return None


def load_previous_context(session_folder: Path, current_query_number: int, logger: logging.Logger) -> Optional[Dict]:
    """이전 질의 로드 (세션 캐시에서)"""
    try:
        if current_query_number < 2:
            logger.error("첫 번째 질의이므로 직전 질의가 존재하지 않습니다")
            return None
        
        # 세션 캐시 파일에서 이전 질의 로드
        script_dir = session_folder.parent  # session_folder의 부모 디렉토리가 script_dir
        cache_file = script_dir / '.session_cache.json'
        
        if not cache_file.exists():
            logger.error(f"세션 캐시 파일을 찾을 수 없습니다: {cache_file}")
            return None
        
        # 세션 캐시 파일 로드
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
            
        previous_query = cache_data.get('previous_query', '')
        if not previous_query:
            logger.warning("세션 캐시에 이전 질의가 없습니다")
            return None
            
        logger.info(f"세션 캐시에서 이전 질의 로드: {previous_query[:50]}...")
        return {
            'query_number': current_query_number - 1,
            'query': previous_query,
            'response': ""  # 응답은 더 이상 사용하지 않음 (질의-질의 비교로 변경)
        }
            
    except Exception as e:
        logger.error(f"이전 질의 로드 중 오류: {e}")
        return None


async def analyze_relevance(previous_query: str, current_query: str, 
                           config: Dict, logger: logging.Logger) -> Dict:
    """AI를 통한 연관성 분석 및 보충 질의 생성 (질의-질의 비교)"""
    start_time = time.time()
    
    try:
        # 연관성 분석 프롬프트 (응답 제거, 질의만 비교)
        prompt = f"""다음 두 질의의 연관성을 분석하고, 사용자의 학습 맥락을 파악해주세요.

# 이전 질의
{previous_query}

# 현재 질의  
{current_query}

다음 JSON 형식으로 응답해주세요:
{{
    "is_relevant": true/false,
    "description": "연관성 분석 결과 설명",
    "generated_query": "사용자 학습을 위한 연결 질의 (연관성이 없으면 '관련 없음')"
}}

연관성 판단 기준:
1. 주제나 개념의 연속성 (같은 도메인, 관련 기술)
2. 학습 흐름의 자연스러움 (기초 → 심화, 개념 → 응용)
3. 비교나 대조의 의도 (A의 특징 → B와의 차이점)
4. 실무 적용이나 심화 학습의 맥락

사용자 이해 부족 부분 파악:
1. 이전 답변에서 충분히 설명되지 않은 부분
2. 사용자가 놓칠 수 있는 중요한 개념이나 배경 지식  
3. 실제 적용이나 예시가 필요한 부분
4. 관련된 다른 개념과의 연결점

연관성이 있다면 사용자의 이해를 돕기 위한 구체적이고 실용적인 질의를 생성해주세요."""

        # Claude Code SDK를 사용하여 질의 처리
        claude_config = config.get('query', {}).get('claude', {})
        max_retries = claude_config.get('max_retries', 3)
        retry_delay = claude_config.get('retry_delay', 1.0)
        
        for attempt in range(max_retries):
            try:
                responses = []
                
                async for message in claude_query(prompt=prompt):
                    if hasattr(message, 'content'):
                        content = message.content
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, 'text'):
                                    responses.append(block.text)
                        elif hasattr(content, 'text'):
                            responses.append(content.text)
                        else:
                            responses.append(str(content))
                
                raw_response = '\n'.join(responses) if responses else ''
                
                # JSON 파싱 시도
                try:
                    import re
                    json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{[^{}]*"is_relevant"[^{}]*\})', 
                                         raw_response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1) or json_match.group(2)
                        result = json.loads(json_str)
                    else:
                        # JSON 형태가 없으면 직접 파싱 시도
                        result = json.loads(raw_response)
                    
                    elapsed_time = time.time() - start_time
                    logger.info(f"연관성 분석 완료 ({elapsed_time:.2f}초)")
                    return result
                    
                except json.JSONDecodeError:
                    logger.warning(f"JSON 파싱 실패, 재시도 중... ({attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        # 최종 실패 시 기본값 반환
                        return {
                            "is_relevant": False,
                            "description": "분석 중 JSON 파싱 오류가 발생했습니다",
                            "generated_query": "관련 없음"
                        }
                        
            except Exception as e:
                logger.warning(f"API 호출 실패, 재시도 중... ({attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
                    
    except Exception as e:
        logger.error(f"연관성 분석 중 오류: {e}")
        elapsed_time = time.time() - start_time
        return {
            "is_relevant": False,
            "description": f"분석 중 오류가 발생했습니다: {str(e)}",
            "generated_query": "관련 없음"
        }


async def generate_supplementary_response(query: str, config: Dict, logger: logging.Logger) -> Dict:
    """보충 응답 생성"""
    start_time = time.time()
    
    try:
        # 참조 문서 로드
        reference_content, document_paths = load_reference_documents(config, logger)
        
        # 응답 생성 프롬프트
        prompt = f"""다음 질의에 대해 참조 문서를 바탕으로 답변해주세요.

# 질의
{query}

# 참조 문서 내용
{reference_content}

참조 문서에 질의와 관련된 내용이 있으면 그 내용을 바탕으로 답변하고, 없으면 일반적인 지식을 활용해서 답변해주세요.
답변은 한국어로 해주시고, 친근하면서도 전문적인 톤으로 작성해주세요."""

        # Claude Code SDK를 사용하여 응답 생성
        claude_config = config.get('query', {}).get('claude', {})
        max_retries = claude_config.get('max_retries', 3)
        retry_delay = claude_config.get('retry_delay', 1.0)
        
        for attempt in range(max_retries):
            try:
                responses = []
                
                async for message in claude_query(prompt=prompt):
                    if hasattr(message, 'content'):
                        content = message.content
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, 'text'):
                                    responses.append(block.text)
                        elif hasattr(content, 'text'):
                            responses.append(content.text)
                        else:
                            responses.append(str(content))
                
                response_text = '\n'.join(responses) if responses else ''
                elapsed_time = time.time() - start_time
                
                # 참조 내용 관련성 판단 (간단한 키워드 매칭)
                has_relevant_content = len(reference_content.strip()) > 100  # 기본적인 판단
                
                result = {
                    "query": query,
                    "response": response_text,
                    "has_relevant_content": has_relevant_content,
                    "elapsed_time": round(elapsed_time, 2),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "document_paths": document_paths,
                    "success": True
                }
                
                logger.info(f"보충 응답 생성 완료 ({elapsed_time:.2f}초)")
                return result
                
            except Exception as e:
                logger.warning(f"API 호출 실패, 재시도 중... ({attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
                    
    except Exception as e:
        logger.error(f"보충 응답 생성 중 오류: {e}")
        elapsed_time = time.time() - start_time
        
        return {
            "query": query,
            "response": f"응답 생성 중 오류가 발생했습니다: {str(e)}",
            "has_relevant_content": False,
            "elapsed_time": round(elapsed_time, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "document_paths": [],
            "success": False
        }


def load_reference_documents(config: Dict, logger: logging.Logger) -> Tuple[str, List[str]]:
    """참조 문서 전체 로드 및 결합"""
    try:
        references_config = config.get('references', {})
        folder_path = Path(references_config.get('folder_path', './references'))
        supported_extensions = references_config.get('supported_extensions', ['.md', '.txt'])
        exclude_patterns = references_config.get('exclude_patterns', ['.*'])
        
        # 상대 경로인 경우 스크립트 디렉토리 기준으로 절대 경로 계산
        if not folder_path.is_absolute():
            script_dir = Path(__file__).parent
            folder_path = script_dir / folder_path
        
        if not folder_path.exists():
            logger.warning(f"참조 문서 폴더가 존재하지 않습니다: {folder_path}")
            return "", []
        
        combined_content = []
        document_paths = []
        
        # 지원하는 확장자의 파일들 찾기
        for ext in supported_extensions:
            for file_path in folder_path.glob(f"**/*{ext}"):
                # 제외 패턴 검사
                should_exclude = False
                for pattern in exclude_patterns:
                    if pattern in str(file_path.name):
                        should_exclude = True
                        break
                
                if should_exclude:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:  # 빈 파일 제외
                            combined_content.append(f"=== {file_path.name} ===\n{content}")
                            document_paths.append(str(file_path))
                except Exception as e:
                    logger.warning(f"파일 읽기 실패: {file_path} - {e}")
        
        final_content = "\n\n".join(combined_content)
        
        # 최대 길이 제한
        max_length = config.get('supplementary_analysis', {}).get('max_context_length', 10000)
        if len(final_content) > max_length:
            final_content = final_content[:max_length] + "\n...(내용이 길어 생략됨)"
        
        logger.info(f"참조 문서 {len(document_paths)}개 로드 완료")
        return final_content, document_paths
        
    except Exception as e:
        logger.error(f"참조 문서 로드 중 오류: {e}")
        return "", []


def save_results(data: Dict, session_folder: Path, logger: logging.Logger):
    """결과를 supplementary_{query_number}_answer.json으로 저장"""
    try:
        query_number = data['query_number']
        filename = f"supplementary_{query_number}_answer.json"
        file_path = session_folder / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"결과 저장 완료: {file_path}")
        
    except Exception as e:
        logger.error(f"결과 저장 중 오류: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    sys.exit(asyncio.run(main()))