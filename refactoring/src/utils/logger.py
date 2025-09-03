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
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

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