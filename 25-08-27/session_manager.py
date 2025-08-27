# 목차
# 생성 시간: 2025-08-26 15:26:50 KST
# 핵심 내용: 세션 캐시 및 세션 폴더 관리 모듈 - 모든 스크립트에서 공통 사용
# 상세 내용:
#   - SessionCacheManager 클래스 (25-122): 세션 캐시 파일 CRUD 작업
#   - SessionManager 클래스 (124-252): 세션 폴더 관리 및 결과 저장
#   - load_session_cache() 함수 (254-270): 편의 함수 - 캐시 로드
#   - find_session_folder() 함수 (272-290): 편의 함수 - 세션 폴더 찾기
# 상태: active
# 주소: session_manager
# 참조: session_query_processor.py (원본 SessionCacheManager, SessionManager)

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from common_utils import find_session_folder as common_find_session_folder


class SessionCacheManager:
    """세션 캐시 파일 관리 클래스 - CRUD 작업 전담"""
    
    def __init__(self, script_dir: Path, logger: Optional[logging.Logger] = None):
        self.script_dir = script_dir
        self.logger = logger or logging.getLogger(__name__)
        self.cache_file = script_dir / '.session_cache.json'
    
    def save_current_session(self, session_id: str, query_number: int = 1, previous_query: str = "") -> bool:
        """현재 세션 ID를 캐시 파일에 저장"""
        try:
            cache_data = {
                'session_id': session_id,
                'query_number': query_number,
                'previous_query': previous_query,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"세션 ID 캐시 저장: {session_id} (질의 번호: {query_number})")
            return True
            
        except Exception as e:
            self.logger.error(f"세션 캐시 저장 오류: {str(e)}")
            return False
    
    def load_current_session(self) -> Optional[Dict[str, Any]]:
        """캐시 파일에서 현재 세션 정보 로드"""
        try:
            if not self.cache_file.exists():
                self.logger.info("세션 캐시 파일이 존재하지 않음 - 새 세션 필요")
                return None
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            session_id = cache_data.get('session_id')
            if session_id:
                self.logger.info(f"캐시에서 세션 정보 로드: {session_id}")
            
            return cache_data
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.logger.warning(f"세션 캐시 로드 오류: {str(e)} - 새 세션으로 진행")
            return None
        except Exception as e:
            self.logger.error(f"세션 캐시 로드 중 예상치 못한 오류: {str(e)}")
            return None
    
    def update_session_timestamp(self, session_id: str, query_number: int) -> bool:
        """세션의 마지막 업데이트 시간 및 질의 번호 갱신"""
        try:
            if not self.cache_file.exists():
                return False
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            if cache_data.get('session_id') == session_id:
                cache_data['last_updated'] = datetime.now().isoformat()
                cache_data['query_number'] = query_number
                
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                self.logger.info(f"세션 업데이트: {session_id} (질의 번호: {query_number})")
                return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"세션 업데이트 오류: {str(e)}")
            return False
    
    def get_cached_query_number(self) -> int:
        """캐시된 질의 번호 가져오기"""
        try:
            cache_data = self.load_current_session()
            if cache_data:
                return cache_data.get('query_number', 1)
            return 1
            
        except Exception as e:
            self.logger.warning(f"캐시된 질의 번호 로드 오류: {str(e)}")
            return 1
    
    def clear_session_cache(self) -> bool:
        """세션 캐시 파일 삭제"""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
                self.logger.info("세션 캐시 파일 삭제됨")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"세션 캐시 삭제 오류: {str(e)}")
            return False


class SessionManager:
    """세션 폴더 생성/관리 및 결과 저장 클래스"""
    
    def __init__(self, script_dir: Path, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.script_dir = script_dir
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.session_config = config.get('session', {})
        
        # 캐시 매니저 초기화
        self.cache_manager = SessionCacheManager(script_dir, logger)
    
    def generate_session_id(self) -> str:
        """새 세션 ID 생성"""
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
    
    def ensure_session_folder(self, session_id: str) -> Path:
        """세션 폴더 확보 (존재하면 찾고, 없으면 생성)"""
        # 먼저 기존 폴더 찾기
        existing_folder = self.find_session_folder(session_id)
        if existing_folder:
            self.logger.info(f"기존 세션 폴더 발견: {existing_folder}")
            return existing_folder
        
        # 없으면 새로 생성
        new_folder = self.create_session_folder(session_id)
        self.logger.info(f"새 세션 폴더 생성: {new_folder}")
        return new_folder
    
    def find_session_folder(self, session_id: str) -> Optional[Path]:
        """기존 세션 폴더 찾기 (session ID의 첫 번째 - 앞 부분으로 매칭)"""
        try:
            return common_find_session_folder(session_id, self.config, __file__)
        except Exception as e:
            self.logger.error(f"세션 폴더 검색 오류: {e}")
            return None
    
    def get_next_query_number(self, session_folder: Path) -> int:
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
    
    def save_query_result(self, session_id: str, query_number: int, query: str, 
                         response_result: Dict[str, Any], document_paths: Optional[List[str]] = None,
                         file_prefix: str = "collective") -> Dict[str, Any]:
        """질의 결과 저장 (첫 번째 질의 및 재개 질의 공통)"""
        try:
            # 세션 폴더 확인 (기존 폴더가 있으면 사용, 없으면 생성)
            session_folder = self.find_session_folder(session_id)
            if not session_folder:
                session_folder = self.create_session_folder(session_id)
            
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
            
            # document_paths가 제공된 경우 추가
            if document_paths:
                save_data['document_paths'] = document_paths
            
            # 에러 정보가 있으면 추가
            if response_result.get('error'):
                save_data['error'] = response_result['error']
            
            # JSON 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            # 세션 캐시 업데이트
            self.cache_manager.save_current_session(session_id, query_number)
            
            self.logger.info(f"질의 결과 저장: {file_path}")
            
            return {
                'success': True,
                'file_path': str(file_path),
                'session_folder': str(session_folder)
            }
            
        except Exception as e:
            self.logger.error(f"질의 결과 저장 오류: {str(e)}")
            raise
    
    def validate_session(self, session_id: str) -> bool:
        """세션 유효성 검증"""
        session_folder = self.find_session_folder(session_id)
        return session_folder is not None and session_folder.exists()
    


# 편의 함수들 (기존 코드와의 호환성을 위해)
def load_session_cache(script_dir: Path = None) -> Optional[Dict[str, Any]]:
    """세션 캐시 로드 편의 함수"""
    if script_dir is None:
        script_dir = Path.cwd()
    
    cache_manager = SessionCacheManager(script_dir)
    return cache_manager.load_current_session()


def find_session_folder(session_id: str, script_dir: Path = None) -> Optional[Path]:
    """세션 폴더 찾기 편의 함수 - common_utils로 위임"""
    try:
        # config가 없는 경우 기본 설정 생성
        default_config = {'session': {'base_folder': '.'}}
        return common_find_session_folder(session_id, default_config, script_dir)
    except Exception:
        return None