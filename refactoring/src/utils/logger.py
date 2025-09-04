# 생성 시간: Mon Sep  3 16:58:20 KST 2025
# 핵심 내용: 체계화된 로깅 팩토리 (책별, 단계별, 용도별 로거 생성)
# 상세 내용:
#   - LoggerFactory (라인 17-123): 로거 팩토리 클래스
#   - create_book_logger (라인 22-65): 책별 로거 생성
#   - create_stage_logger (라인 67-85): 단계별 로거 생성
#   - create_chapter_logger (라인 87-105): 장별 로거 생성
#   - _setup_handlers (라인 107-123): 로그 핸들러 설정
#   - normalize_title (라인 13-15): 제목 정규화 유틸리티
# 상태: active

import logging
import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

def normalize_title(title: str) -> str:
    """제목을 파일명으로 사용할 수 있게 정규화"""
    return "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

class LoggerFactory:
    """체계화된 로깅 팩토리"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
    def create_book_logger(self, book_title: str, logs_base_dir: str = None) -> logging.Logger:
        """책별 로거 생성"""
        normalized_title = normalize_title(book_title)
        
        # 로그 디렉토리 설정
        if logs_base_dir is None:
            logs_base_dir = self.config_manager.get("global.logs_base_dir", "./logs")
            
        logs_dir = Path(logs_base_dir) / normalized_title
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 책별 로거 생성
        logger = logging.getLogger(f'book_{normalized_title}')
        logger.setLevel(logging.INFO)
        
        # 기존 핸들러 제거 (중복 방지)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 로그 포맷터
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 파일 핸들러들 설정
        handlers_config = [
            ('pipeline.log', logging.INFO, '전체 파이프라인 진행상황'),
            ('chapter_integration.log', logging.INFO, '장별 통합 처리 상세'),
            ('processing_errors.log', logging.ERROR, '정보 처리 관련 모든 에러'),
        ]
        
        for filename, level, description in handlers_config:
            handler = logging.FileHandler(logs_dir / filename, encoding='utf-8')
            handler.setFormatter(formatter)
            handler.setLevel(level)
            logger.addHandler(handler)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.info(f"책별 로거 설정 완료: {logs_dir} ({book_title})")
        return logger
        
    def create_stage_logger(self, stage_name: str, book_logger: logging.Logger = None) -> logging.Logger:
        """단계별 로거 생성"""
        logger_name = f'stage_{stage_name}'
        
        if book_logger:
            # 책별 로거를 상속받아서 같은 핸들러들 사용
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            
            # 부모 로거 설정으로 핸들러 자동 상속
            logger.parent = book_logger
            logger.propagate = True
        else:
            # 독립 로거
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            
        return logger
        
    def create_chapter_logger(self, chapter_number: int, chapter_title: str, book_logger: logging.Logger = None) -> logging.Logger:
        """장별 로거 생성"""
        normalized_title = normalize_title(chapter_title)
        logger_name = f'chapter_{chapter_number:02d}_{normalized_title}'
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        
        if book_logger:
            # 부모 로거로 설정
            logger.parent = book_logger
            logger.propagate = True
        else:
            # 기본 핸들러 설정
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
        
        return logger
        
    def create_result_logger(self, project_name: str, base_dir: str = None) -> 'ResultLogger':
        """결과 저장 전용 로거 생성"""
        if base_dir is None:
            base_dir = self.config_manager.get("global.results_base_dir", "./results")
        
        results_dir = Path(base_dir) / normalize_title(project_name)
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # 기본 로거 생성 (결과 저장 관련 로그용)
        logger = logging.getLogger(f'result_logger_{normalize_title(project_name)}')
        logger.setLevel(logging.INFO)
        
        # 기존 핸들러 제거
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            
        # 콘솔 핸들러만 추가 (파일 핸들러는 필요시 추가)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return ResultLogger(results_dir, logger)
        
    def _setup_handlers(self, logger: logging.Logger, logs_dir: Path, log_configs: list):
        """로그 핸들러 설정 공통 로직"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        for filename, level in log_configs:
            handler = logging.FileHandler(logs_dir / filename, encoding='utf-8')
            handler.setFormatter(formatter)
            handler.setLevel(level)
            logger.addHandler(handler)


class ResultLogger:
    """처리 결과 저장 전용 로거"""
    
    def __init__(self, results_dir: Path, logger: logging.Logger):
        """
        ResultLogger 초기화
        
        Args:
            results_dir: 결과 파일들이 저장될 기본 디렉토리
            logger: 로깅용 로거 인스턴스
        """
        self.results_dir = results_dir
        self.logger = logger
        
    def save_result(self, result_name: str, data: Any, format: str = "json") -> Path:
        """
        결과 데이터를 지정된 형식으로 파일에 저장
        
        Args:
            result_name: 결과 파일명 (확장자 제외)
            data: 저장할 데이터
            format: 저장 형식 ('json', 'txt', 'md', 'yaml')
            
        Returns:
            Path: 저장된 파일의 경로
        """
        normalized_name = normalize_title(result_name)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 파일명에 타임스탬프 포함
        file_name = f"{normalized_name}_{timestamp}"
        
        if format.lower() == "json":
            file_path = self.results_dir / f"{file_name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        elif format.lower() == "txt":
            file_path = self.results_dir / f"{file_name}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                if isinstance(data, (dict, list)):
                    f.write(str(data))
                else:
                    f.write(str(data))
                    
        elif format.lower() == "md":
            file_path = self.results_dir / f"{file_name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                if isinstance(data, str):
                    f.write(data)
                else:
                    f.write(f"# {result_name}\n\n")
                    f.write(str(data))
                    
        elif format.lower() == "yaml":
            file_path = self.results_dir / f"{file_name}.yaml"
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
                
        else:
            raise ValueError(f"지원하지 않는 형식: {format}")
            
        self.logger.info(f"결과 저장 완료: {file_path}")
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