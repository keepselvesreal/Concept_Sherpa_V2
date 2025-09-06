"""
생성 시간: 2025-08-31 20:15:09 KST
핵심 내용: 스크립트별 독립적인 AI 제공업체 설정을 위한 통합 설정 관리자
상세 내용:
    - import 구문 (20-25): 필요한 라이브러리 import
    - ConfigManager 클래스 (27-120): 설정 파일 로드 및 검증
        - __init__ (28-35): 설정 파일 경로 초기화
        - load_config (37-55): YAML 설정 파일 로드
        - validate_config (57-85): 설정 파일 구조 및 값 검증
        - get_script_config (87-105): 스크립트별 설정 조회 (fallback 로직)
        - get_ai_provider (107-115): AI 제공업체 설정 조회
        - get_model_config (117-130): 모델별 상세 설정 조회
    - 설정 검증 함수들 (132-160): AI 제공업체 및 모델 유효성 검증
상태: active
주소: config_manager
참조: config.yaml
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    """스크립트별 독립적인 설정을 관리하는 클래스"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """설정 관리자 초기화"""
        self.config_path = Path(config_path)
        self.config = None
        self.load_config()
    
    def load_config(self) -> None:
        """YAML 설정 파일을 로드"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            # 설정 검증
            self.validate_config()
            logging.info(f"✅ 설정 파일 로드 완료: {self.config_path}")
            
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 파일 파싱 오류: {e}")
        except Exception as e:
            raise RuntimeError(f"설정 파일 로드 실패: {e}")
    
    def validate_config(self) -> None:
        """설정 파일의 구조와 값들을 검증"""
        if not self.config:
            raise ValueError("설정이 로드되지 않았습니다")
        
        # 필수 섹션 검증
        required_sections = ['models', 'providers']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"필수 섹션이 누락되었습니다: {section}")
        
        # AI 제공업체 검증
        valid_providers = {'claude', 'gemini', 'openai'}
        
        # 전역 AI 제공업체 검증
        global_provider = self.config.get('ai_provider')
        if global_provider and global_provider not in valid_providers:
            raise ValueError(f"유효하지 않은 전역 AI 제공업체: {global_provider}")
        
        # 스크립트별 AI 제공업체 검증
        script_configs = self.config.get('script_configs', {})
        for script_name, script_config in script_configs.items():
            if 'ai_provider' in script_config:
                provider = script_config['ai_provider']
                if provider not in valid_providers:
                    raise ValueError(f"{script_name}의 유효하지 않은 AI 제공업체: {provider}")
        
        logging.info("✅ 설정 검증 완료")
    
    def get_script_config(self, script_name: str) -> Dict[str, Any]:
        """
        스크립트별 설정을 조회 (fallback 로직 적용)
        우선순위: 스크립트별 설정 → 전역 설정 → 기본값
        """
        # 기본 설정
        default_config = {
            'ai_provider': 'gemini',
            'temperature': 0.7
        }
        
        # 전역 설정 적용
        global_config = {
            'ai_provider': self.config.get('ai_provider', default_config['ai_provider']),
            'temperature': default_config['temperature']
        }
        
        # 스크립트별 설정 적용
        script_configs = self.config.get('script_configs', {})
        script_config = script_configs.get(script_name, {})
        
        # 최종 설정 생성 (우선순위 적용)
        final_config = {**default_config, **global_config, **script_config}
        
        return final_config
    
    def get_ai_provider(self, script_name: str) -> str:
        """스크립트의 AI 제공업체 설정 조회"""
        script_config = self.get_script_config(script_name)
        return script_config['ai_provider']
    
    def get_model_config(self, provider: str) -> Dict[str, Any]:
        """AI 제공업체의 모델 설정 조회"""
        providers = self.config.get('providers', {})
        if provider not in providers:
            # 기본 설정 반환
            default_configs = {
                'claude': {'model': 'claude-3-sonnet', 'temperature': 0.7},
                'gemini': {'model': 'gemini-2.0-flash-exp', 'temperature': 0.7},
                'openai': {'model': 'gpt-4', 'temperature': 0.7}
            }
            return default_configs.get(provider, {})
        
        return providers[provider]

def validate_ai_provider(provider: str) -> bool:
    """AI 제공업체 유효성 검증"""
    valid_providers = {'claude', 'gemini', 'openai'}
    return provider in valid_providers

def validate_model_name(provider: str, model: str) -> bool:
    """모델명 유효성 검증"""
    valid_models = {
        'claude': ['claude-3-sonnet', 'claude-3-haiku', 'claude-3-opus'],
        'gemini': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash'],
        'openai': ['gpt-4', 'gpt-3.5-turbo']
    }
    
    if provider not in valid_models:
        return False
    
    return model in valid_models[provider] or model.startswith(('models/', 'claude-', 'gpt-'))