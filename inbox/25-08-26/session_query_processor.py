# 목차
# 생성 시간: 2025-08-26 10:28:15 KST
# 핵심 내용: 세션 기반 질의응답 시스템 - 참조 문서 결합 및 세션 관리 통합
# 상세 내용:
#   - SessionQueryProcessor 클래스 (51-297): 메인 질의 처리 시스템
#   - DocumentCombiner 클래스 (299-374): references 폴더 파일 결합
#   - SessionManager 클래스 (376-453): 세션 생성/재개 관리
#   - OutputManager 클래스 (455-540): 저장 및 터미널 출력
#   - QueryProcessor 클래스 (542-628): Claude SDK 기반 질의 처리
#   - main() 함수 (630-662): CLI 인터페이스
# 상태: active
# 주소: session_query_processor
# 참조: document_query_processor.py, query_processor_v2.py, simple_resume_test.py, latest_session_reader_v2.py

import asyncio
import argparse
import json
import logging
import os
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

try:
    from claude_code_sdk import ClaudeCodeOptions, query as claude_query
except ImportError as e:
    print(f"❌ claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    sys.exit(1)

# 새로운 session_manager 모듈 임포트
from session_manager import SessionManager as NewSessionManager, SessionCacheManager

console = Console()

class SessionQueryProcessor:
    """세션 기반 질의응답 시스템 메인 클래스"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self.script_dir = Path(__file__).parent
        
        # 로깅 설정
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # 컴포넌트 초기화
        self.doc_combiner = DocumentCombiner(self.config, self.logger)
        self.session_manager = NewSessionManager(self.script_dir, self.config, self.logger)
        self.query_processor = QueryProcessor(self.config, self.logger)
        self.output_manager = OutputManager(self.config, self.logger)
        
        self.logger.info("SessionQueryProcessor 초기화 완료")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            console.print(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}", style="red")
            sys.exit(1)
        except yaml.YAMLError as e:
            console.print(f"❌ 설정 파일 파싱 오류: {e}", style="red")
            sys.exit(1)
    
    def _setup_logging(self):
        """로깅 시스템 설정"""
        log_config = self.config.get('logging', {})
        log_dir = Path(log_config.get('file_path', './logs/session_query_processor.log')).parent
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_config.get('level', 'INFO')),
            format=log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            handlers=[
                logging.FileHandler(log_config.get('file_path', './logs/session_query_processor.log')),
                logging.StreamHandler()
            ]
        )
    
    async def process_first_query(self, query: str, session_id: str = None, query_number: int = None) -> Dict[str, Any]:
        """첫 번째 질의 처리 (참조 문서 결합 + 새 세션 생성)"""
        try:
            self.logger.info(f"첫 번째 질의 처리 시작: {query[:50]}...")
            
            # 1. 참조 문서 결합
            if self.config.get('output', {}).get('enable_progress', True):
                console.print("🔍 참조 문서 결합 중...", style="yellow")
            
            combined_content, document_paths = await self.doc_combiner.combine_documents()
            
            if not combined_content:
                raise ValueError("참조 문서를 찾을 수 없습니다")
            
            self.logger.info(f"문서 {len(document_paths)}개 결합 완료")
            
            # 2. 질의 처리
            if self.config.get('output', {}).get('enable_progress', True):
                console.print("🤖 질의 처리 중...", style="yellow")
            
            response_result = await self.query_processor.process_query(query, combined_content)
            
            # 3. 세션 ID 처리 (새 세션이면 None일 수 있음, Claude SDK가 생성)
            current_session_id = session_id  # 새 세션이면 None
            if session_id:
                self.logger.info(f"매개변수로 받은 세션 ID 사용: {session_id}")
            else:
                self.logger.info("새 세션 시작 - Claude SDK가 세션 ID 생성")
            
            # 4. 질의 번호 처리 (첫 번째 질의는 항상 1)
            current_query_number = query_number if query_number is not None else 1
            self.logger.info(f"질의 번호 설정: {current_query_number}")
            
            # Claude SDK에서 실제 생성된 세션 ID 확인 및 업데이트
            actual_session_id = response_result.get('session_id') or current_session_id
            if actual_session_id and actual_session_id != current_session_id:
                self.logger.info(f"Claude SDK 실제 세션 ID로 업데이트: {current_session_id} -> {actual_session_id}")
                # 캐시를 실제 세션 ID로 업데이트
                from session_manager import SessionCacheManager
                cache_manager = SessionCacheManager(self.script_dir, self.logger)
                cache_manager.save_current_session(actual_session_id, current_query_number)
                current_session_id = actual_session_id
            
            # 새로운 통합 save_query_result 사용 (실제 세션 ID 사용)
            save_result = self.session_manager.save_query_result(
                session_id=current_session_id,
                query_number=current_query_number,
                query=query,
                response_result=response_result,
                document_paths=document_paths,
                file_prefix="collective"
            )
            
            # 4. 결과 출력
            await self.output_manager.display_first_query_result(
                query=query,
                response_result=response_result,
                session_id=current_session_id,
                document_count=len(document_paths),
                save_path=save_result['file_path']
            )
            
            self.logger.info(f"첫 번째 질의 처리 완료 - 세션 ID: {current_session_id}")
            
            return {
                'success': True,
                'session_id': current_session_id,
                'query_number': current_query_number,
                'query': query,
                'response': response_result.get('response', ''),
                'document_count': len(document_paths),
                'save_path': save_result['file_path']
            }
            
        except Exception as e:
            self.logger.error(f"첫 번째 질의 처리 오류: {str(e)}")
            if self.config.get('error_handling', {}).get('detailed_errors', True):
                console.print(f"❌ 오류 발생: {str(e)}", style="red")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def process_resume_query(self, query: str, session_id: str, query_number: int = None) -> Dict[str, Any]:
        """세션 재개 질의 처리"""
        try:
            self.logger.info(f"세션 재개 질의 처리 시작: {session_id[:20]}...")
            
            # 1. 세션 검증
            if not self.session_manager.validate_session(session_id):
                raise ValueError(f"유효하지 않은 세션 ID: {session_id}")
            
            # 2. 질의 번호 처리 (매개변수로만 처리)
            if query_number is None:
                raise ValueError("query_number가 필수 매개변수입니다. 통합 프로세서에서 세션 관리가 먼저 이루어져야 합니다.")
            
            current_query_number = query_number
            self.logger.info(f"매개변수로 받은 질의 번호 사용: {query_number}")
            
            # 3. 재개 질의 처리
            if self.config.get('output', {}).get('enable_progress', True):
                console.print(f"🔄 세션 재개 중... (ID: {session_id[:20]}...)", style="yellow")
            
            response_result = await self.query_processor.process_resume_query(query, session_id)
            
            # 4. 결과 저장 - 통합 save_query_result 사용
            save_result = self.session_manager.save_query_result(
                session_id=session_id,
                query_number=current_query_number,
                query=query,
                response_result=response_result,
                file_prefix="collective"
            )
            
            # 4. 결과 출력
            await self.output_manager.display_resume_query_result(
                query=query,
                response_result=response_result,
                session_id=session_id,
                save_path=save_result['file_path']
            )
            
            self.logger.info(f"세션 재개 질의 처리 완료 - 세션 ID: {session_id}")
            
            return {
                'success': True,
                'session_id': session_id,
                'query_number': current_query_number,
                'query': query,
                'response': response_result.get('response', ''),
                'save_path': save_result['file_path']
            }
            
        except Exception as e:
            self.logger.error(f"세션 재개 질의 처리 오류: {str(e)}")
            if self.config.get('error_handling', {}).get('detailed_errors', True):
                console.print(f"❌ 오류 발생: {str(e)}", style="red")
            return {
                'success': False,
                'error': str(e)
            }


class DocumentCombiner:
    """references 폴더 파일 결합 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.ref_config = config.get('references', {})
    
    async def combine_documents(self) -> Tuple[str, List[str]]:
        """참조 문서들을 결합하여 하나의 텍스트로 반환"""
        try:
            folder_path = Path(self.ref_config.get('folder_path', './references'))
            
            # 절대 경로로 변환
            if not folder_path.is_absolute():
                folder_path = Path(__file__).parent / folder_path
            
            if not folder_path.exists():
                raise FileNotFoundError(f"참조 폴더가 존재하지 않습니다: {folder_path}")
            
            # 파일 목록 수집
            files_data = await self._collect_files(folder_path)
            
            if not files_data:
                raise ValueError(f"참조 폴더에 읽을 수 있는 파일이 없습니다: {folder_path}")
            
            # 문서 내용 결합
            combined_content = self._combine_file_contents(files_data)
            document_paths = [file_data['path'] for file_data in files_data]
            
            self.logger.info(f"문서 {len(files_data)}개 결합 완료")
            return combined_content, document_paths
            
        except Exception as e:
            self.logger.error(f"문서 결합 오류: {str(e)}")
            raise
    
    async def _collect_files(self, folder_path: Path) -> List[Dict[str, str]]:
        """폴더에서 파일들을 수집"""
        files_data = []
        supported_extensions = self.ref_config.get('supported_extensions', ['.md', '.txt'])
        exclude_patterns = self.ref_config.get('exclude_patterns', ['.*'])
        
        for file_path in folder_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            # 확장자 검사
            if file_path.suffix not in supported_extensions:
                continue
            
            # 제외 패턴 검사
            if any(file_path.match(pattern) for pattern in exclude_patterns):
                continue
            
            try:
                content = await self._read_file_content(file_path)
                files_data.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'content': content
                })
                self.logger.debug(f"파일 수집 완료: {file_path.name}")
            except Exception as e:
                self.logger.warning(f"파일 읽기 실패: {file_path.name} - {str(e)}")
                continue
        
        return files_data
    
    async def _read_file_content(self, file_path: Path) -> str:
        """파일 내용 읽기 (다중 인코딩 지원)"""
        encodings = ['utf-8', 'cp949', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        raise UnicodeDecodeError(f"지원하지 않는 인코딩: {file_path}")
    
    def _combine_file_contents(self, files_data: List[Dict[str, str]]) -> str:
        """파일 내용들을 하나로 결합"""
        combined_parts = []
        
        for i, file_data in enumerate(files_data):
            part = f"=== 참조문서 {i+1}: {file_data['name']} ===\n{file_data['content']}"
            combined_parts.append(part)
        
        return "\n\n" + "="*50 + "\n\n".join([""] + combined_parts) + "\n\n" + "="*50


class SessionCacheManager:
    """세션 캐시 자동 관리 클래스"""
    
    def __init__(self, script_dir: Path, logger: logging.Logger):
        self.script_dir = script_dir
        self.logger = logger
        self.cache_file = script_dir / '.session_cache.json'
    
    def save_current_session(self, session_id: str, query_number: int = 1):
        """현재 세션 ID를 캐시 파일에 저장"""
        try:
            cache_data = {
                'session_id': session_id,
                'query_number': query_number,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"세션 ID 캐시 저장: {session_id} (질의 번호: {query_number})")
            
        except Exception as e:
            self.logger.error(f"세션 캐시 저장 오류: {str(e)}")
            raise
    
    def load_current_session(self) -> Optional[str]:
        """캐시 파일에서 현재 세션 ID 로드"""
        try:
            if not self.cache_file.exists():
                self.logger.info("세션 캐시 파일이 존재하지 않음 - 새 세션 필요")
                return None
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            session_id = cache_data.get('session_id')
            if session_id:
                self.logger.info(f"캐시에서 세션 ID 로드: {session_id}")
            
            return session_id
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.logger.warning(f"세션 캐시 로드 오류: {str(e)} - 새 세션으로 진행")
            return None
        except Exception as e:
            self.logger.error(f"세션 캐시 로드 중 예상치 못한 오류: {str(e)}")
            return None
    
    def update_session_timestamp(self, session_id: str, query_number: int):
        """세션의 마지막 업데이트 시간 및 질의 번호 갱신"""
        try:
            if not self.cache_file.exists():
                return
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            if cache_data.get('session_id') == session_id:
                cache_data['last_updated'] = datetime.now().isoformat()
                cache_data['query_number'] = query_number
                
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                self.logger.info(f"세션 업데이트: {session_id} (질의 번호: {query_number})")
            
        except Exception as e:
            self.logger.warning(f"세션 업데이트 오류: {str(e)}")
    
    def get_cached_query_number(self) -> int:
        """캐시된 질의 번호 가져오기"""
        try:
            if not self.cache_file.exists():
                return 1
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            return cache_data.get('query_number', 1)
            
        except Exception as e:
            self.logger.warning(f"캐시된 질의 번호 로드 오류: {str(e)}")
            return 1
    
    def clear_session_cache(self):
        """세션 캐시 파일 삭제"""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
                self.logger.info("세션 캐시 파일 삭제됨")
            
        except Exception as e:
            self.logger.error(f"세션 캐시 삭제 오류: {str(e)}")
            raise


class OldSessionManager:
    """세션 생성/재개 관리 클래스 (DEPRECATED - 새로운 session_manager.py 사용)"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.session_config = config.get('session', {})
        self.script_dir = Path(__file__).parent
        
        # 세션 캐시 매니저 추가
        self.cache_manager = SessionCacheManager(self.script_dir, logger)
    
    def extract_session_id_from_response(self, response_result: Dict[str, Any]) -> Optional[str]:
        """응답에서 세션 ID 추출"""
        # Claude SDK 응답에서 세션 ID를 추출하는 로직
        # 실제 구현은 Claude SDK의 응답 구조에 따라 달라짐
        return response_result.get('session_id')
    
    def generate_session_id(self) -> str:
        """새 세션 ID 생성"""
        import uuid
        session_id = str(uuid.uuid4())
        self.logger.info(f"새 세션 ID 생성: {session_id}")
        return session_id
    
    def get_session_prefix(self, session_id: str) -> str:
        """세션 ID에서 prefix 추출"""
        separator = self.session_config.get('id_separator', '-')
        return session_id.split(separator)[0]
    
    def create_session_folder(self, session_id: str) -> Path:
        """세션 폴더 생성 (session ID의 첫 번째 - 앞 부분만 사용)"""
        session_prefix = self.get_session_prefix(session_id)
        timestamp = datetime.now().strftime('%H%M')
        folder_name = f"session_{session_prefix}_{timestamp}"
        
        folder_path = self.script_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        
        self.logger.info(f"세션 폴더 생성: {folder_path} (원본 ID: {session_id})")
        return folder_path
    
    def get_cached_session_id(self) -> Optional[str]:
        """캐시된 세션 ID 가져오기"""
        return self.cache_manager.load_current_session()
    
    async def save_first_query_result(self, session_id: str, query: str, 
                                     response_result: Dict[str, Any], 
                                     document_paths: List[str]) -> Dict[str, Any]:
        """첫 번째 질의 결과 저장"""
        try:
            session_folder = self.create_session_folder(session_id)
            
            query_number = self.session_config.get('initial_query_number', 1)
            file_prefix = self.session_config.get('file_prefix', 'collective')
            filename = f"{file_prefix}_{query_number}_answer.json"
            
            file_path = session_folder / filename
            
            # 저장할 데이터 구성 (요구사항에 맞는 필드 구성)
            save_data = {
                'query_number': query_number,
                'query': query,
                'model_response': response_result.get('response', ''),
                'has_relevant_content': response_result.get('has_relevant_content', True),
                'elapsed_time': response_result.get('elapsed_time', 0.0),
                'timestamp': datetime.now().isoformat(),
                'document_paths': document_paths,  # 요구사항: document_paths 필드
                'success': response_result.get('success', True)
            }
            
            # JSON 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            # 세션 ID를 캐시에 저장
            self.cache_manager.save_current_session(session_id, query_number)
            
            self.logger.info(f"첫 번째 질의 결과 저장: {file_path}")
            
            return {
                'success': True,
                'file_path': str(file_path),
                'session_folder': str(session_folder)
            }
            
        except Exception as e:
            self.logger.error(f"첫 번째 질의 결과 저장 오류: {str(e)}")
            raise
    
    async def save_resume_query_result(self, session_id: str, query: str, 
                                      response_result: Dict[str, Any]) -> Dict[str, Any]:
        """세션 재개 질의 결과 저장"""
        try:
            # 기존 세션 폴더 찾기
            session_folder = self._find_existing_session_folder(session_id)
            if not session_folder:
                raise FileNotFoundError(f"세션 폴더를 찾을 수 없습니다: {session_id}")
            
            # 다음 질의 번호 계산
            query_number = self._get_next_query_number(session_folder)
            
            file_prefix = self.session_config.get('file_prefix', 'collective')
            filename = f"{file_prefix}_{query_number}_answer.json"
            file_path = session_folder / filename
            
            # 저장할 데이터 구성
            save_data = {
                'query_number': query_number,
                'query': query,
                'model_response': response_result.get('response', ''),
                'has_relevant_content': response_result.get('has_relevant_content', True),
                'elapsed_time': response_result.get('elapsed_time', 0.0),
                'timestamp': datetime.now().isoformat(),
                'success': response_result.get('success', True)
            }
            
            # JSON 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            # 세션 타임스탬프 및 질의 번호 업데이트
            self.cache_manager.update_session_timestamp(session_id, query_number)
            
            self.logger.info(f"재개 질의 결과 저장: {file_path}")
            
            return {
                'success': True,
                'file_path': str(file_path),
                'session_folder': str(session_folder)
            }
            
        except Exception as e:
            self.logger.error(f"재개 질의 결과 저장 오류: {str(e)}")
            raise
    
    def _find_existing_session_folder(self, session_id: str) -> Optional[Path]:
        """기존 세션 폴더 찾기 (session ID의 첫 번째 - 앞 부분으로 매칭)"""
        session_prefix = self.get_session_prefix(session_id)
        pattern = f"session_{session_prefix}_*"
        
        matching_folders = list(self.script_dir.glob(pattern))
        if matching_folders:
            # 가장 최신 폴더 반환 (타임스탬프 기준)
            return max(matching_folders, key=lambda x: x.name.split('_')[-1])
        
        return None
    
    def _get_next_query_number(self, session_folder: Path) -> int:
        """세션 폴더에서 다음 질의 번호 계산 (캐시 우선 사용)"""
        # 캐시에서 질의 번호 가져오기 (더 정확함)
        cached_query_number = self.cache_manager.get_cached_query_number()
        next_number = cached_query_number + 1
        
        # 폴더 파일과 대조하여 검증
        file_prefix = self.session_config.get('file_prefix', 'collective')
        pattern = f"{file_prefix}_*_answer.json"
        
        existing_files = list(session_folder.glob(pattern))
        if existing_files:
            # 파일명에서 숫자 추출하여 최대값 + 1 반환
            numbers = []
            for file_path in existing_files:
                try:
                    number_part = file_path.stem.split('_')[1]  # collective_{number}_answer
                    numbers.append(int(number_part))
                except (IndexError, ValueError):
                    continue
            
            file_based_next = max(numbers) + 1 if numbers else 1
            
            # 캐시와 파일 기반 번호 중 더 큰 값 사용 (안전성 보장)
            return max(next_number, file_based_next)
        
        return next_number
    
    def validate_session(self, session_id: str) -> bool:
        """세션 유효성 검증"""
        session_folder = self._find_existing_session_folder(session_id)
        return session_folder is not None and session_folder.exists()


class OutputManager:
    """저장 및 터미널 출력 관리 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.output_config = config.get('output', {})
    
    async def display_first_query_result(self, query: str, response_result: Dict[str, Any],
                                        session_id: str, document_count: int, save_path: str):
        """첫 번째 질의 결과 출력"""
        if not self.output_config.get('enable_console', True):
            return
        
        console.print("\n" + "="*80, style="bold green")
        console.print("🎯 첫 번째 질의 처리 완료", style="bold green")
        console.print("="*80, style="bold green")
        
        # 질의 내용 표시
        query_panel = Panel(
            query,
            title="🔍 질의 내용",
            title_align="left",
            border_style="blue"
        )
        console.print(query_panel)
        
        # 처리 정보 표시
        info_text = f"""
📂 참조 문서 수: {document_count}개
🆔 생성된 세션 ID: {session_id}
💾 저장 위치: {save_path}
⏱️ 처리 시간: {response_result.get('elapsed_time', 0.0):.2f}초
        """.strip()
        
        info_panel = Panel(
            info_text,
            title="📊 처리 정보",
            title_align="left",
            border_style="yellow"
        )
        console.print(info_panel)
        
        # 응답 내용 표시
        response_content = response_result.get('response', '응답 없음')
        response_panel = Panel(
            Markdown(response_content),
            title="💬 응답 내용",
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )
        console.print(response_panel)
        
        # 재개 명령어 안내
        console.print(f"\n✅ 세션이 생성되었습니다. 다음 명령어로 대화를 이어가세요:", style="bold green")
        console.print(f"python session_query_processor.py \"다음 질문\" --session-id {session_id}", style="cyan")
    
    async def display_resume_query_result(self, query: str, response_result: Dict[str, Any],
                                         session_id: str, save_path: str):
        """세션 재개 질의 결과 출력"""
        if not self.output_config.get('enable_console', True):
            return
        
        console.print("\n" + "="*80, style="bold green")
        console.print("🔄 세션 재개 질의 처리 완료", style="bold green")
        console.print("="*80, style="bold green")
        
        # 질의 내용 표시
        query_panel = Panel(
            query,
            title="🔍 질의 내용",
            title_align="left",
            border_style="blue"
        )
        console.print(query_panel)
        
        # 처리 정보 표시
        info_text = f"""
🆔 세션 ID: {session_id}
💾 저장 위치: {save_path}
⏱️ 처리 시간: {response_result.get('elapsed_time', 0.0):.2f}초
        """.strip()
        
        info_panel = Panel(
            info_text,
            title="📊 처리 정보",
            title_align="left",
            border_style="yellow"
        )
        console.print(info_panel)
        
        # 응답 내용 표시
        response_content = response_result.get('response', '응답 없음')
        response_panel = Panel(
            Markdown(response_content),
            title="💬 응답 내용",
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )
        console.print(response_panel)


class QueryProcessor:
    """Claude SDK 기반 질의 처리 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.query_config = config.get('query', {})
        self.claude_config = self.query_config.get('claude', {})
    
    async def process_query(self, query: str, combined_content: str) -> Dict[str, Any]:
        """첫 번째 질의 처리 (참조 문서 기반)"""
        start_time = time.time()
        
        try:
            # AI 관련성 판단 기반 조건부 응답 프롬프트
            enhanced_prompt = f"""다음 사용자 질의와 참조 문서를 분석하여 단계적으로 작업해주세요.

사용자 질의: {query}

참조 문서:
{combined_content}

작업 단계:
1. 먼저 참조 문서에 질의와 관련된 내용이 있는지 판단하세요
2. 관련 내용이 있으면 참조 문서를 바탕으로 정확하고 구체적으로 답변하세요
3. 관련 내용이 없으면 당신의 사전 지식을 바탕으로 답변하세요

응답 형식은 다음 JSON 구조로 작성해주세요:
{{
    "has_relevant_content": true 또는 false,
    "model_response": "실제 답변 내용"
}}"""

            # Claude SDK로 질의 처리 (세션 생성 옵션 추가)
            responses = []
            session_id = None
            
            # 첫 번째 질의에서 새 대화 세션 시작
            options = ClaudeCodeOptions(
                max_turns=10  # 다중 턴 대화를 위한 설정
            )
            
            async for message in claude_query(prompt=enhanced_prompt, options=options):
                # 세션 ID 추출 시도
                if hasattr(message, 'session_id') and message.session_id:
                    session_id = str(message.session_id)
                elif hasattr(message, 'id') and message.id:
                    session_id = str(message.id)
                
                # 응답 내용 수집 (TextBlock 래퍼 제거)
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        # TextBlock 리스트에서 텍스트만 추출
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                    elif hasattr(content, 'text'):
                        # 단일 TextBlock에서 텍스트 추출
                        responses.append(content.text)
                    else:
                        # 일반 문자열인 경우
                        responses.append(str(content))
            
            elapsed_time = time.time() - start_time
            raw_response = '\n'.join(responses) if responses else ''
            
            # JSON 응답 파싱 시도
            try:
                import re
                # JSON 블록 추출 시도 (```json ... ``` 또는 { ... } 패턴)
                json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{[^{}]*"has_relevant_content"[^{}]*\})', 
                                     raw_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1) or json_match.group(2)
                    parsed_response = json.loads(json_str)
                    
                    result = {
                        'success': True,
                        'response': parsed_response.get('model_response', raw_response),
                        'session_id': session_id,
                        'has_relevant_content': parsed_response.get('has_relevant_content', False),
                        'elapsed_time': elapsed_time,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    # JSON 파싱 실패 시 전체 응답에서 true/false 키워드 추출
                    has_relevant = 'true' in raw_response.lower() and 'has_relevant_content' in raw_response.lower()
                    result = {
                        'success': True,
                        'response': raw_response,
                        'session_id': session_id,
                        'has_relevant_content': has_relevant,
                        'elapsed_time': elapsed_time,
                        'timestamp': datetime.now().isoformat()
                    }
                    
            except (json.JSONDecodeError, AttributeError):
                # JSON 파싱 완전 실패 시 기본값
                result = {
                    'success': True,
                    'response': raw_response,
                    'session_id': session_id,
                    'has_relevant_content': False,
                    'elapsed_time': elapsed_time,
                    'timestamp': datetime.now().isoformat()
                }
            
            self.logger.info(f"질의 처리 완료 - {elapsed_time:.2f}초")
            return result
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(f"질의 처리 오류: {str(e)}")
            
            return {
                'success': False,
                'response': f'질의 처리 중 오류가 발생했습니다: {str(e)}',
                'session_id': None,
                'has_relevant_content': False,
                'elapsed_time': elapsed_time,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    async def process_resume_query(self, query: str, session_id: str) -> Dict[str, Any]:
        """세션 재개 질의 처리"""
        start_time = time.time()
        
        try:
            # 세션 재개를 위한 옵션 설정
            options = ClaudeCodeOptions(
                resume=session_id,
                max_turns=10  # 설정 가능한 값
            )
            
            # 세션 재개 시에도 관련성 판단이 포함된 프롬프트 사용
            enhanced_resume_prompt = f"""이전 대화 맥락을 바탕으로 다음 질의에 답변해주세요.

사용자 질의: {query}

작업 단계:
1. 이전 대화에서 제공된 참조 문서와 현재 질의의 관련성을 판단하세요
2. 관련성이 있으면 참조 문서와 이전 맥락을 바탕으로 답변하세요
3. 관련성이 없으면 일반적인 지식을 바탕으로 답변하세요

응답 형식은 다음 JSON 구조로 작성해주세요:
{{
    "has_relevant_content": true 또는 false,
    "model_response": "실제 답변 내용"
}}"""
            
            # Claude SDK로 세션 재개 질의 처리
            responses = []
            resumed_session_id = None
            
            async for message in claude_query(prompt=enhanced_resume_prompt, options=options):
                # 세션 ID 추출
                if hasattr(message, 'session_id') and message.session_id:
                    resumed_session_id = str(message.session_id)
                elif hasattr(message, 'id') and message.id:
                    resumed_session_id = str(message.id)
                
                # 응답 내용 수집 (TextBlock 래퍼 제거)
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        # TextBlock 리스트에서 텍스트만 추출
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                    elif hasattr(content, 'text'):
                        # 단일 TextBlock에서 텍스트 추출
                        responses.append(content.text)
                    else:
                        # 일반 문자열인 경우
                        responses.append(str(content))
            
            elapsed_time = time.time() - start_time
            raw_response = '\n'.join(responses) if responses else ''
            
            # JSON 응답 파싱 시도 (첫 번째 질의와 동일한 로직)
            try:
                import re
                # JSON 블록 추출 시도 (```json ... ``` 또는 { ... } 패턴)
                json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{[^{}]*"has_relevant_content"[^{}]*\})', 
                                     raw_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1) or json_match.group(2)
                    parsed_response = json.loads(json_str)
                    
                    result = {
                        'success': True,
                        'response': parsed_response.get('model_response', raw_response),
                        'session_id': resumed_session_id or session_id,
                        'has_relevant_content': parsed_response.get('has_relevant_content', False),
                        'elapsed_time': elapsed_time,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    # JSON 파싱 실패 시 전체 응답에서 true/false 키워드 추출
                    has_relevant = 'true' in raw_response.lower() and 'has_relevant_content' in raw_response.lower()
                    result = {
                        'success': True,
                        'response': raw_response,
                        'session_id': resumed_session_id or session_id,
                        'has_relevant_content': has_relevant,
                        'elapsed_time': elapsed_time,
                        'timestamp': datetime.now().isoformat()
                    }
                    
            except (json.JSONDecodeError, AttributeError):
                # JSON 파싱 완전 실패 시 기본값
                result = {
                    'success': True,
                    'response': raw_response,
                    'session_id': resumed_session_id or session_id,
                    'has_relevant_content': False,
                    'elapsed_time': elapsed_time,
                    'timestamp': datetime.now().isoformat()
                }
            
            self.logger.info(f"세션 재개 질의 처리 완료 - {elapsed_time:.2f}초")
            return result
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(f"세션 재개 질의 처리 오류: {str(e)}")
            
            return {
                'success': False,
                'response': f'세션 재개 질의 처리 중 오류가 발생했습니다: {str(e)}',
                'session_id': session_id,
                'has_relevant_content': False,
                'elapsed_time': elapsed_time,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }


async def main():
    """CLI 인터페이스 메인 함수"""
    parser = argparse.ArgumentParser(
        description="세션 기반 질의응답 시스템",
        epilog="""
사용 예시:
  첫 번째 질의: python session_query_processor.py "데이터 지향 프로그래밍의 특징은?"
  자동 재개:   python session_query_processor.py "더 자세한 예시를 들어줘"
  새 세션:     python session_query_processor.py "새로운 주제로 시작" --new-session
  수동 재개:   python session_query_processor.py "질문" --session-id abc123-def456
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('query', help='처리할 질의문')
    parser.add_argument('--session-id', help='재개할 세션 ID (수동 지정)')
    parser.add_argument('--new-session', action='store_true', help='강제로 새 세션 시작')
    parser.add_argument('--config', default='./config.yaml', help='설정 파일 경로')
    
    args = parser.parse_args()
    
    try:
        # SessionQueryProcessor 초기화
        processor = SessionQueryProcessor(args.config)
        
        # 세션 결정 로직
        session_id = None
        
        if args.session_id:
            # 수동으로 세션 ID가 지정된 경우
            session_id = args.session_id
            console.print(f"🔧 수동 지정 세션으로 재개: {session_id[:20]}...", style="cyan")
        elif args.new_session:
            # 강제로 새 세션 시작
            console.print("🆕 새 세션 강제 시작", style="green")
            session_id = None
        else:
            # 자동 세션 감지 (캐시에서 로드)
            cached_session_id = processor.session_manager.get_cached_session_id()
            if cached_session_id:
                console.print(f"🔄 캐시된 세션 자동 재개: {cached_session_id[:20]}...", style="yellow")
                session_id = cached_session_id
            else:
                console.print("🆕 새 세션 자동 시작 (캐시된 세션 없음)", style="green")
                session_id = None
        
        # 세션 모드에 따른 처리
        if session_id:
            # 세션 재개 모드
            result = await processor.process_resume_query(args.query, session_id)
        else:
            # 첫 번째 질의 모드
            result = await processor.process_first_query(args.query)
        
        # 결과에 따른 종료 코드 설정
        sys.exit(0 if result['success'] else 1)
        
    except KeyboardInterrupt:
        console.print("\n❌ 사용자에 의해 중단되었습니다.", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ 예상치 못한 오류: {str(e)}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())