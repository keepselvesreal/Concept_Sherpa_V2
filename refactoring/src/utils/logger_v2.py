# 생성 시간: Thu Sep  4 15:37:35 KST 2025
# 핵심 내용: 통합 Logger 클래스 (로깅 + 파일 저장 + 진행 관리)
# 상세 내용:
#   - Logger (라인 17-180): 통합 로거 클래스
#   - __init__ (라인 20-60): 로거 및 디렉토리 초기화
#   - 로깅 메서드들 (라인 62-80): info, error, warning, debug
#   - save_result (라인 82-130): 결과 파일 저장 (JSON/YAML/MD/TXT)
#   - list_results (라인 132-155): 저장된 결과 파일 목록
#   - log_stage_progress (라인 157-165): 단계별 진행 상황 로깅
#   - normalize_title (라인 12-15): 제목 정규화 유틸리티
# 상태: active
# 참조: logger.py (기존 LoggerFactory, ResultLogger 통합)

import logging
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# text_utils import
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from text_utils import normalize_title

class Logger:
    """통합 로거: 로깅 + 결과 저장 + 진행 상황 관리"""
    
    def __init__(self, project_name: str, base_dir: str = None, logs_base_dir: str = None):
        """
        Logger 초기화
        
        Args:
            project_name: 프로젝트명 (책 제목 등)
            base_dir: 결과 파일 저장 기본 디렉토리
            logs_base_dir: 로그 파일 저장 디렉토리
        """
        self.project_name = project_name
        self.normalized_name = normalize_title(project_name)
        
        # 디렉토리 설정
        self.results_dir = Path(base_dir or "./results") / self.normalized_name
        self.logs_dir = Path(logs_base_dir or "./logs") / self.normalized_name
        
        # 디렉토리 생성
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 로거 설정
        self.logger = logging.getLogger(f'logger_{self.normalized_name}')
        self.logger.setLevel(logging.INFO)
        
        # 기존 핸들러 제거 (중복 방지)
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # 로그 포맷터
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 파일 핸들러들 설정
        handlers_config = [
            ('pipeline.log', logging.INFO),
            ('processing_errors.log', logging.ERROR),
        ]
        
        for filename, level in handlers_config:
            handler = logging.FileHandler(self.logs_dir / filename, encoding='utf-8')
            handler.setFormatter(formatter)
            handler.setLevel(level)
            self.logger.addHandler(handler)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logger 초기화 완료: {self.project_name}")
    
    def info(self, message: str):
        """정보 로깅"""
        self.logger.info(message)
    
    def error(self, message: str):
        """에러 로깅"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """경고 로깅"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """디버그 로깅"""
        self.logger.debug(message)
    
    def save_result(self, result_name: str, data: Any, format: str = "json", custom_dir: str = None) -> Path:
        """
        결과 데이터를 지정된 형식으로 파일에 저장
        
        Args:
            result_name: 결과 파일명 (확장자 제외)
            data: 저장할 데이터
            format: 저장 형식 ('json', 'txt', 'md', 'yaml')
            custom_dir: 사용자 정의 저장 디렉토리 (절대 경로 또는 상대 경로)
            
        Returns:
            Path: 저장된 파일의 경로
        """
        normalized_name = normalize_title(result_name)
        
        # 사용자 정의 디렉토리가 있으면 사용, 없으면 기본 results_dir 사용
        if custom_dir:
            save_dir = Path(custom_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
            # 사용자 정의 디렉토리 사용 시 타임스탬프 제거
            file_name = normalized_name
        else:
            save_dir = self.results_dir
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # 기본 디렉토리 사용 시 타임스탬프 포함
            file_name = f"{normalized_name}_{timestamp}"
        
        if format.lower() == "json":
            file_path = save_dir / f"{file_name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        elif format.lower() == "txt":
            file_path = save_dir / f"{file_name}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                if isinstance(data, (dict, list)):
                    f.write(str(data))
                else:
                    f.write(str(data))
                    
        elif format.lower() == "md":
            file_path = save_dir / f"{file_name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                if isinstance(data, str):
                    f.write(data)
                else:
                    f.write(f"# {result_name}\n\n")
                    f.write(str(data))
                    
        elif format.lower() == "yaml":
            file_path = save_dir / f"{file_name}.yaml"
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
                
        else:
            raise ValueError(f"지원하지 않는 형식: {format}")
            
        self.info(f"결과 저장 완료: {file_path}")
        return file_path
    
    def list_results(self) -> List[Dict[str, Any]]:
        """
        저장된 결과 파일들의 목록 반환
        
        Returns:
            List[Dict]: 파일 정보 리스트
        """
        results = []
        
        for file_path in self.results_dir.iterdir():
            if file_path.is_file():
                file_info = {
                    "name": file_path.stem,
                    "format": file_path.suffix[1:],  # 확장자에서 점 제거
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "created": datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
                results.append(file_info)
                
        # 생성 시간 순으로 정렬 (최신 순)
        results.sort(key=lambda x: x["created"], reverse=True)
        
        return results
    
    def log_stage_progress(self, stage: str, status: str, details: str = None):
        """
        단계별 진행 상황 로깅
        
        Args:
            stage: 단계명 (예: "workspace_preparation", "chapter_extraction")
            status: 상태 (예: "start", "progress", "complete", "error")
            details: 추가 상세 정보
        """
        message = f"[{stage}] {status.upper()}"
        if details:
            message += f" - {details}"
            
        if status == "error":
            self.error(message)
        else:
            self.info(message)


class LoggerFactory:
    """Logger 팩토리 (기존 코드 호환성을 위한 래퍼)"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def create_book_logger(self, book_title: str, logs_base_dir: str = None) -> Logger:
        """책별 로거 생성 (기존 호환성)"""
        if logs_base_dir is None:
            logs_base_dir = self.config_manager.get("global.logs_base_dir", "./logs")
        
        return Logger(book_title, logs_base_dir=logs_base_dir)
    
    def create_result_logger(self, project_name: str, base_dir: str = None) -> Logger:
        """결과 로거 생성 (기존 호환성)"""
        if base_dir is None:
            base_dir = self.config_manager.get("global.results_base_dir", "./results")
        
        return Logger(project_name, base_dir=base_dir)