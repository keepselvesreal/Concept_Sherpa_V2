"""
생성 시간: 2025-08-18 11:09:48
핵심 내용: 프로젝트 설정 파일 로더 모듈
상세 내용:
    - ConfigLoader 클래스 (라인 22-120): YAML/JSON 설정 파일 관리
    - load_config 메서드 (라인 35-55): 설정 파일 로드
    - get_project_config 메서드 (라인 57-75): 특정 프로젝트 설정 반환
    - list_projects 메서드 (라인 77-85): 프로젝트 목록 반환
    - save_config 메서드 (라인 87-105): 설정 파일 저장
    - create_default_config 메서드 (라인 107-120): 기본 설정 생성
상태: 
주소: config_loader
참조: 
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    프로젝트 설정 파일을 로드하고 관리하는 클래스
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        설정 로더 초기화
        
        Args:
            config_dir: 설정 파일 디렉토리 (None이면 현재 디렉토리/config)
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path(__file__).parent.parent / 'config'
        
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'projects.yaml'
        self._config_cache = None
    
    def load_config(self) -> Dict[str, Any]:
        """
        설정 파일 로드
        
        Returns:
            설정 딕셔너리
        """
        if self._config_cache is not None:
            return self._config_cache
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    if self.config_file.suffix.lower() == '.yaml':
                        self._config_cache = yaml.safe_load(f) or {}
                    else:
                        self._config_cache = json.load(f)
            else:
                # 기본 설정 생성
                self._config_cache = self.create_default_config()
                self.save_config(self._config_cache)
            
            return self._config_cache
        except Exception as e:
            logger.error(f"설정 파일 로드 실패: {e}")
            return {}
    
    def get_project_config(self, project_name: str) -> Optional[Dict[str, Any]]:
        """
        특정 프로젝트의 설정 반환
        
        Args:
            project_name: 프로젝트명
            
        Returns:
            프로젝트 설정 딕셔너리 또는 None
        """
        config = self.load_config()
        projects = config.get('projects', {})
        return projects.get(project_name)
    
    def list_projects(self) -> List[str]:
        """
        설정된 프로젝트 목록 반환
        
        Returns:
            프로젝트명 리스트
        """
        config = self.load_config()
        projects = config.get('projects', {})
        return list(projects.keys())
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        설정을 파일에 저장
        
        Args:
            config: 저장할 설정 딕셔너리
            
        Returns:
            저장 성공 여부
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.suffix.lower() == '.yaml':
                    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
                else:
                    json.dump(config, f, indent=2, ensure_ascii=False)
            
            self._config_cache = config
            logger.info(f"설정 저장 완료: {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"설정 저장 실패: {e}")
            return False
    
    def create_default_config(self) -> Dict[str, Any]:
        """
        기본 설정 구조 생성
        
        Returns:
            기본 설정 딕셔너리
        """
        return {
            'projects': {
                'knowledge_sherpa': {
                    'name': 'Knowledge Sherpa',
                    'description': 'AI-powered knowledge extraction system',
                    'adapter': 'postgresql',
                    'connection': {
                        'url': 'from_env:NEON_DATABASE_URL'
                    },
                    'tables': [
                        'documents',
                        'core_content_embeddings',
                        'detailed_core_embeddings',
                        'main_topic_embeddings',
                        'sub_topic_embeddings'
                    ]
                }
            }
        }
    
    def add_project(self, project_name: str, project_config: Dict[str, Any]) -> bool:
        """
        새 프로젝트 설정 추가
        
        Args:
            project_name: 프로젝트명
            project_config: 프로젝트 설정
            
        Returns:
            추가 성공 여부
        """
        try:
            config = self.load_config()
            if 'projects' not in config:
                config['projects'] = {}
            
            config['projects'][project_name] = project_config
            return self.save_config(config)
        except Exception as e:
            logger.error(f"프로젝트 추가 실패 ({project_name}): {e}")
            return False
    
    def remove_project(self, project_name: str) -> bool:
        """
        프로젝트 설정 제거
        
        Args:
            project_name: 프로젝트명
            
        Returns:
            제거 성공 여부
        """
        try:
            config = self.load_config()
            if 'projects' in config and project_name in config['projects']:
                del config['projects'][project_name]
                return self.save_config(config)
            else:
                logger.warning(f"프로젝트를 찾을 수 없습니다: {project_name}")
                return False
        except Exception as e:
            logger.error(f"프로젝트 제거 실패 ({project_name}): {e}")
            return False
    
    def clear_cache(self):
        """설정 캐시 초기화"""
        self._config_cache = None


def load_config(config_path: str = "config/projects.yaml") -> Dict[str, Any]:
    """
    설정 파일을 로드하는 편의 함수
    
    Args:
        config_path: 설정 파일 경로
        
    Returns:
        설정 딕셔너리
    """
    config_loader = ConfigLoader()
    return config_loader.load_config()