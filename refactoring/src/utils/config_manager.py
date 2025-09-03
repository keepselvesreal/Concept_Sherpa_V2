# 생성 시간: Mon Sep  3 16:55:45 KST 2025  
# 핵심 내용: 설정 파일 통합 관리자 (AI, 파이프라인, 로깅 설정 통합)
# 상세 내용:
#   - ConfigManager (라인 15-86): 메인 설정 관리 클래스
#   - load_config (라인 20-35): YAML 설정 파일 로드
#   - get (라인 37-48): 점표기법으로 중첩 설정값 접근
#   - get_test_config (라인 50-59): 테스트 모드 설정 반환
#   - is_chapter_selected (라인 61-71): 선택된 장인지 확인
#   - get_ai_config (라인 73-80): AI 설정 반환
#   - get_logging_config (라인 82-86): 로깅 설정 반환
# 상태: active

import yaml
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

class ConfigManager:
    """설정 파일 통합 관리자"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = Path(__file__).parent.parent.parent / "config"
        
        self.config_dir = Path(config_dir)
        self.pipeline_config = self.load_config("pipeline_config.yaml")
        self.ai_config = self.load_config("ai_config.yaml") 
        self.logging_config = self.load_config("logging_config.yaml")
        
    def load_config(self, filename: str) -> Dict[str, Any]:
        """YAML 설정 파일 로드"""
        config_path = self.config_dir / filename
        
        if not config_path.exists():
            print(f"⚠️ 설정 파일을 찾을 수 없음: {config_path}")
            return {}
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ 설정 파일 로드 실패 ({filename}): {e}")
            return {}
    
    def get(self, key_path: str, default_value: Any = None, config_type: str = "pipeline") -> Any:
        """점표기법으로 중첩 설정값 접근"""
        config_map = {
            "pipeline": self.pipeline_config,
            "ai": self.ai_config, 
            "logging": self.logging_config
        }
        
        config = config_map.get(config_type, self.pipeline_config)
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default_value
        return value
    
    def get_test_config(self) -> Dict[str, Any]:
        """테스트 모드 설정 반환"""
        return self.get("test_mode", {
            "enabled": False,
            "selected_chapters": [],
            "debug_verbose": True,
            "skip_on_error": False
        })
    
    def is_chapter_selected(self, chapter_number: int) -> bool:
        """선택된 장인지 확인 (테스트 모드에서)"""
        test_config = self.get_test_config()
        
        if not test_config.get("enabled", False):
            return True  # 테스트 모드 비활성화면 모든 장 처리
            
        selected_chapters = test_config.get("selected_chapters", [])
        if not selected_chapters:  # 빈 리스트면 모든 장 처리
            return True
            
        return chapter_number in selected_chapters
    
    def get_ai_config(self) -> Dict[str, Any]:
        """AI 설정 반환"""
        return self.ai_config
        
    def get_logging_config(self) -> Dict[str, Any]:
        """로깅 설정 반환"""
        return self.logging_config