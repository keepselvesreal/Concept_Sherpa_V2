"""
# 목차
- 생성 시간: 2025년 8월 23일 16:59:42 KST
- 핵심 내용: 프롬프트 파일을 불러와서 반환하는 범용 유틸리티 모듈
- 상세 내용:
    - PromptLoader 클래스 (라인 20-52): 프롬프트 파일 로딩을 담당하는 클래스
    - load_prompt 함수 (라인 25-45): 지정된 파일에서 프롬프트 텍스트를 로드하는 함수
    - get_prompt 함수 (라인 47-52): 기본 경로에서 프롬프트 파일을 불러오는 함수
- 상태: active
- 참조: conversation_module.py와 함께 사용하기 위한 범용 유틸리티
"""

import os
from typing import Optional

class PromptLoader:
    """프롬프트 파일 로딩을 담당하는 클래스"""
    
    BASE_PATH = "/home/nadle/projects/Concept_Sherpa_V2/25-08-23"
    
    @classmethod
    def load_prompt(cls, prompt_file: str) -> Optional[str]:
        """지정된 파일에서 프롬프트 텍스트를 로드하는 함수"""
        try:
            if not os.path.isabs(prompt_file):
                prompt_file = os.path.join(cls.BASE_PATH, prompt_file)
            
            if not os.path.exists(prompt_file):
                print(f"프롬프트 파일을 찾을 수 없습니다: {prompt_file}")
                return None
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                print(f"프롬프트 파일이 비어있습니다: {prompt_file}")
                return None
            
            return content
            
        except Exception as e:
            print(f"프롬프트 파일 읽기 오류: {e}")
            return None
    
    @classmethod
    def get_prompt(cls, filename: str) -> Optional[str]:
        """기본 경로에서 프롬프트 파일을 불러오는 함수"""
        return cls.load_prompt(filename)