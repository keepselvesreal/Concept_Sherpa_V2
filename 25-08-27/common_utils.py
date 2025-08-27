# 목차
# 생성 시간: 2025-08-26 15:26:50 KST
# 핵심 내용: 공통 유틸리티 모듈 - 에러 핸들링, 로깅 시스템, 설정 관리 통합
# 상세 내용:
#   - ConfigManager 클래스 (24-68): 설정 파일 로드 및 검증
#   - LoggingManager 클래스 (70-145): 통합 로깅 시스템 관리
#   - ErrorHandler 클래스 (147-210): 에러 핸들링 및 복구 로직
#   - load_config() 함수 (212-220): 설정 로드 편의 함수
#   - setup_logging() 함수 (222-230): 로깅 설정 편의 함수
# 상태: active
# 주소: common_utils
# 참조: session_manager.py, output_formatter.py, unified_processor.py

import json
import logging
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union


class ConfigManager:
    """설정 파일 관리 클래스"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config_path = Path(config_path)
        self.config_data = None
        self._load_config()
    
    def _load_config(self):
        """설정 파일 로드"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
            
            # 기본값 설정
            self._set_defaults()
            
        except yaml.YAMLError as e:
            raise ValueError(f"설정 파일 파싱 오류: {e}")
        except Exception as e:
            raise RuntimeError(f"설정 파일 로드 중 오류: {e}")
    
    def _set_defaults(self):
        """기본 설정값 설정"""
        defaults = {
            'logging': {
                'level': 'INFO',
                'file_path': './logs/app.log',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'output': {
                'enable_console': True,
                'enable_progress': True
            },
            'error_handling': {
                'detailed_errors': True,
                'max_retries': 3,
                'retry_delay': 1.0
            },
            'session': {
                'id_separator': '-',
                'file_prefix': 'collective',
                'initial_query_number': 1
            },
            'parallel': {
                'max_concurrent': 3
            }
        }
        
        # 기본값으로 누락된 설정 채우기
        for key, value in defaults.items():
            if key not in self.config_data:
                self.config_data[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in self.config_data[key]:
                        self.config_data[key][sub_key] = sub_value
    
    def get_config(self) -> Dict[str, Any]:
        """전체 설정 반환"""
        return self.config_data.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정값 가져오기 (중첩 키 지원)"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value


class LoggingManager:
    """통합 로깅 시스템 관리"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.log_config = config.get('logging', {})
        self.loggers = {}
    
    def setup_logger(self, name: str, level: Optional[str] = None) -> logging.Logger:
        """로거 설정"""
        if name in self.loggers:
            return self.loggers[name]
        
        logger = logging.getLogger(name)
        
        # 기존 핸들러 제거
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 로그 레벨 설정
        log_level = level or self.log_config.get('level', 'INFO')
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # 로그 디렉토리 생성
        log_file_path = Path(self.log_config.get('file_path', './logs/app.log'))
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # 포맷터
        formatter = logging.Formatter(
            self.log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 핸들러 추가
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # 상위 로거로의 전파 방지 (중복 출력 방지)
        logger.propagate = False
        
        self.loggers[name] = logger
        return logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """기존 로거 가져오기 또는 새로 생성"""
        if name not in self.loggers:
            return self.setup_logger(name)
        return self.loggers[name]
    
    def set_log_level(self, name: str, level: str):
        """로거의 로그 레벨 변경"""
        if name in self.loggers:
            self.loggers[name].setLevel(getattr(logging, level.upper()))


class ErrorHandler:
    """에러 핸들링 및 복구 로직"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.config = config
        self.error_config = config.get('error_handling', {})
        self.logger = logger or logging.getLogger(__name__)
        
        # 에러 통계
        self.error_stats = {
            'total_errors': 0,
            'error_types': {},
            'last_error_time': None
        }
    
    def handle_exception(self, exception: Exception, context: str = "", 
                        critical: bool = False) -> Dict[str, Any]:
        """예외 처리 및 로깅"""
        error_type = type(exception).__name__
        error_message = str(exception)
        timestamp = datetime.now().isoformat()
        
        # 에러 통계 업데이트
        self.error_stats['total_errors'] += 1
        self.error_stats['error_types'][error_type] = self.error_stats['error_types'].get(error_type, 0) + 1
        self.error_stats['last_error_time'] = timestamp
        
        # 로그 레벨 결정
        log_level = logging.CRITICAL if critical else logging.ERROR
        
        # 에러 로깅
        error_details = f"[{context}] {error_type}: {error_message}"
        self.logger.log(log_level, error_details)
        
        # 상세 에러 정보 (설정에 따라)
        if self.error_config.get('detailed_errors', True):
            import traceback
            traceback_info = traceback.format_exc()
            self.logger.debug(f"상세 스택 트레이스:\n{traceback_info}")
        
        return {
            'error_type': error_type,
            'error_message': error_message,
            'context': context,
            'timestamp': timestamp,
            'critical': critical,
            'stats': self.error_stats.copy()
        }
    
    def retry_operation(self, operation_func, *args, max_retries: Optional[int] = None,
                       retry_delay: Optional[float] = None, **kwargs):
        """재시도 로직이 포함된 작업 실행"""
        max_retries = max_retries or self.error_config.get('max_retries', 3)
        retry_delay = retry_delay or self.error_config.get('retry_delay', 1.0)
        
        last_exception = None
        
        for attempt in range(max_retries + 1):  # +1 for initial attempt
            try:
                return operation_func(*args, **kwargs)
                
            except Exception as e:
                last_exception = e
                
                if attempt < max_retries:
                    self.logger.warning(f"작업 실패, 재시도 중... ({attempt + 1}/{max_retries}): {str(e)}")
                    import time
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"최대 재시도 횟수 초과: {str(e)}")
        
        # 모든 재시도 실패 시 마지막 예외 발생
        raise last_exception
    
    def get_error_stats(self) -> Dict[str, Any]:
        """에러 통계 반환"""
        return self.error_stats.copy()
    
    def reset_error_stats(self):
        """에러 통계 초기화"""
        self.error_stats = {
            'total_errors': 0,
            'error_types': {},
            'last_error_time': None
        }


# 편의 함수들
def load_config(config_path: str = "./config.yaml") -> Dict[str, Any]:
    """설정 로드 편의 함수"""
    try:
        config_manager = ConfigManager(config_path)
        return config_manager.get_config()
    except Exception as e:
        print(f"❌ 설정 로드 실패: {str(e)}")
        sys.exit(1)


def setup_logging(config: Dict[str, Any], name: str = "app", level: Optional[str] = None) -> logging.Logger:
    """로깅 설정 편의 함수"""
    logging_manager = LoggingManager(config)
    return logging_manager.setup_logger(name, level)


def handle_startup_error(error: Exception, context: str = "시스템 시작"):
    """시작 시 치명적 오류 처리"""
    print(f"❌ {context} 중 오류가 발생했습니다: {str(error)}")
    import traceback
    print(f"상세 정보:\n{traceback.format_exc()}")
    sys.exit(1)


def validate_python_version(min_version: tuple = (3, 8)):
    """Python 버전 검증"""
    current_version = sys.version_info[:2]
    if current_version < min_version:
        raise RuntimeError(f"Python {'.'.join(map(str, min_version))} 이상이 필요합니다. 현재 버전: {'.'.join(map(str, current_version))}")


def check_required_files(file_paths: list, base_dir: Path = None):
    """필수 파일 존재 확인"""
    base_dir = base_dir or Path.cwd()
    missing_files = []
    
    for file_path in file_paths:
        full_path = base_dir / file_path if not Path(file_path).is_absolute() else Path(file_path)
        if not full_path.exists():
            missing_files.append(str(full_path))
    
    if missing_files:
        raise FileNotFoundError(f"필수 파일들이 없습니다: {', '.join(missing_files)}")


def safe_json_load(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """안전한 JSON 파일 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        logging.getLogger(__name__).warning(f"JSON 파일 로드 실패: {file_path} - {str(e)}")
        return None


def safe_file_write(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
    """안전한 파일 쓰기"""
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
        
    except Exception as e:
        logging.getLogger(__name__).error(f"파일 쓰기 실패: {file_path} - {str(e)}")
        return False


# === 세션 경로 관리 유틸리티 ===

def find_session_folder(session_id: str, config: Dict[str, Any], 
                       script_path: Union[str, Path] = None) -> Path:
    """
    config 기반으로 세션 폴더 찾기 - 실행 위치와 무관한 범용적 해결책
    
    Args:
        session_id: 세션 ID (예: '3d1f50b8-4e4d-445b-...')
        config: 설정 딕셔너리
        script_path: 스크립트 경로 (None이면 자동 감지)
    
    Returns:
        Path: 찾은 세션 폴더 경로
        
    Raises:
        FileNotFoundError: 세션 폴더를 찾을 수 없는 경우
    """
    # 스크립트 디렉토리 기준점 설정
    if script_path is None:
        # 이 함수를 호출한 스크립트의 위치를 기준으로 함
        import inspect
        caller_frame = inspect.currentframe().f_back
        caller_file = caller_frame.f_globals['__file__']
        script_dir = Path(caller_file).parent
    else:
        script_dir = Path(script_path).parent
    
    # 세션 ID에서 prefix 추출
    session_prefix = session_id.split('-')[0]
    
    # config에서 세션 기본 경로 읽기
    session_config = config.get('session', {})
    base_folder = session_config.get('base_folder', '.')
    
    # 검색 기준 경로 설정
    search_base = script_dir / base_folder
    pattern = f"session_{session_prefix}_*"
    
    # 패턴 매칭으로 세션 폴더 찾기
    matching_folders = list(search_base.glob(pattern))
    
    if not matching_folders:
        raise FileNotFoundError(f"세션 폴더를 찾을 수 없습니다: {pattern} (검색 경로: {search_base})")
    
    # 가장 최신 폴더 반환 (timestamp 기준)
    latest_folder = max(matching_folders, key=lambda x: x.name.split('_')[-1])
    return latest_folder


def get_session_folder_path(session_id: str, config: Dict[str, Any], 
                           script_path: Union[str, Path] = None) -> str:
    """
    세션 폴더 경로를 문자열로 반환하는 편의 함수
    
    Args:
        session_id: 세션 ID
        config: 설정 딕셔너리  
        script_path: 스크립트 경로
    
    Returns:
        str: 세션 폴더 경로 문자열
    """
    try:
        folder_path = find_session_folder(session_id, config, script_path)
        return str(folder_path)
    except FileNotFoundError as e:
        logging.getLogger(__name__).error(str(e))
        raise


def ensure_session_folder_exists(session_id: str, config: Dict[str, Any],
                                script_path: Union[str, Path] = None) -> Path:
    """
    세션 폴더가 존재하지 않으면 생성하고 경로 반환
    
    Args:
        session_id: 세션 ID
        config: 설정 딕셔너리
        script_path: 스크립트 경로
    
    Returns:
        Path: 세션 폴더 경로 (생성됨)
    """
    try:
        # 기존 폴더 찾기 시도
        return find_session_folder(session_id, config, script_path)
    except FileNotFoundError:
        # 폴더가 없으면 새로 생성
        if script_path is None:
            import inspect
            caller_frame = inspect.currentframe().f_back
            caller_file = caller_frame.f_globals['__file__']
            script_dir = Path(caller_file).parent
        else:
            script_dir = Path(script_path).parent
        
        session_config = config.get('session', {})
        base_folder = session_config.get('base_folder', '.')
        
        # 새 폴더 생성 (timestamp 기반)
        from datetime import datetime
        timestamp = datetime.now().strftime('%H%M')
        session_prefix = session_id.split('-')[0]
        folder_name = f"session_{session_prefix}_{timestamp}"
        
        new_folder_path = script_dir / base_folder / folder_name
        new_folder_path.mkdir(parents=True, exist_ok=True)
        
        logging.getLogger(__name__).info(f"새 세션 폴더 생성: {new_folder_path}")
        return new_folder_path