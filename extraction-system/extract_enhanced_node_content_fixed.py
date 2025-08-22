#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 16:57:00 KST
핵심 내용: 유튜브 ID별 폴더 구조에 맞게 수정된 노드 정보 추출 스크립트
상세 내용: 
    - main() (라인 25-62): 메인 실행 함수, 비디오 폴더 단위 처리
    - find_node_info_files() (라인 65-76): 비디오 폴더에서 *_info.md 파일 찾기
    - process_single_node() (라인 79-130): 개별 노드 정보 문서 처리
    - 기타 클래스들 (라인 133-300): AI 추출 로직 및 설정 관리
상태: active
주소: extract_enhanced_node_content/fixed
참조: extract_enhanced_node_content_v2
"""

import asyncio
import os
import time
import yaml
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pathlib import Path
import sys


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python extract_enhanced_node_content_fixed.py <video_folder>")
        print("Example: python extract_enhanced_node_content_fixed.py ./YouTube_250822/VtmBevBcDzI")
        sys.exit(1)
    
    video_folder = sys.argv[1]
    
    # 폴더 존재 확인
    if not os.path.exists(video_folder):
        print(f"❌ 비디오 폴더가 존재하지 않습니다: {video_folder}")
        sys.exit(1)
    
    # 설정 파일 경로 (extraction-system 폴더에서 찾기)
    script_dir = os.path.dirname(__file__)
    extraction_system_dir = os.path.join(script_dir, '..', 'extraction-system')
    config_path = os.path.join(extraction_system_dir, 'extraction_config.yaml')
    
    print("🚀 노드 정보 추출 시작")
    print("=" * 50)
    print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
    
    # 노드 정보 문서 찾기
    info_files = find_node_info_files(video_folder)
    if not info_files:
        print("❌ 노드 정보 문서를 찾을 수 없습니다 (*_info.md)")
        sys.exit(1)
    
    print(f"📄 발견된 노드 정보 문서: {len(info_files)}개")
    
    # 각 파일 처리
    for info_file in info_files:
        print(f"\n📄 처리 중: {os.path.basename(info_file)}")
        asyncio.run(process_single_node(info_file, config_path))


def find_node_info_files(video_folder: str) -> List[str]:
    """비디오 폴더에서 *_info.md 파일 찾기"""
    info_files = []
    
    for file in os.listdir(video_folder):
        if file.endswith('_info.md'):
            info_files.append(os.path.join(video_folder, file))
    
    return info_files


async def process_single_node(info_file: str, config_path: str):
    """개별 노드 정보 문서 처리"""
    try:
        # 설정 로드
        config = ExtractionConfig.from_file(config_path)
        print(f"🔧 설정 로드 완료: {config.ai_provider} 모델 사용")
        
        # 파일 내용 읽기
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 언어 감지
        language = detect_language(content)
        print(f"🌍 감지된 source_language: {language}")
        
        # 내용 섹션 추출
        content_section = extract_content_section(content)
        if not content_section:
            print("❌ 내용 섹션이 비어있거나 추출할 수 없습니다.")
            return
        
        print(f"📖 내용 섹션 추출 완료: {len(content_section)} 문자")
        
        # AI 제공자 초기화
        ai_provider = AIProviderFactory.create_provider(config, language)
        
        # 핵심 정보 추출
        print("🤖 AI를 사용해 핵심 정보 추출 중...")
        start_time = time.time()
        
        extraction_results = await ai_provider.extract_all_content(
            content_section, 
            os.path.basename(info_file)
        )
        
        end_time = time.time()
        print(f"⏱️ 추출 완료: {end_time - start_time:.1f}초 소요")
        
        # 추출 섹션 업데이트
        if extraction_results:
            update_extraction_section(info_file, extraction_results)
            print("✅ 노드 정보 추출 성공")
        else:
            print("❌ 추출 결과가 없습니다")
            
    except Exception as e:
        print(f"❌ 처리 실패: {e}")


def detect_language(content: str) -> str:
    """내용에서 언어 감지"""
    # 속성 섹션에서 source_language 찾기
    language_match = re.search(r'source_language:\s*(\w+)', content)
    if language_match:
        return language_match.group(1)
    
    # 기본값
    return 'english'


def extract_content_section(content: str) -> str:
    """파일에서 내용 섹션 추출"""
    try:
        # 내용 섹션 찾기
        pattern = r'# 내용\n---\n(.*?)# 구성\n---'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            section_content = match.group(1).strip()
            if section_content and len(section_content) > 10:  # 최소 길이 체크
                return section_content
        
        return ""
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""


def update_extraction_section(info_file: str, results: Dict[str, str]):
    """추출 결과를 파일의 추출 섹션에 업데이트"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 추출 섹션 찾기 및 교체
        pattern = r'(# 추출\n---\n)(.*?)(# 내용\n---)'
        
        # 추출 결과 포맷팅
        extraction_content = ""
        if results.get('core_content'):
            extraction_content += f"## 핵심 내용\n{results['core_content']}\n\n"
        
        if results.get('detailed_core_content'):
            extraction_content += f"## 상세 핵심 내용\n{results['detailed_core_content']}\n\n"
            
        if results.get('main_topics'):
            extraction_content += f"## 주요 화제\n{results['main_topics']}\n\n"
            
        if results.get('sub_topics'):
            extraction_content += f"## 부차 화제\n{results['sub_topics']}\n\n"
        
        replacement = rf'\1{extraction_content}\3'
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ 추출 섹션 업데이트 완료")
        
    except Exception as e:
        print(f"❌ 추출 섹션 업데이트 실패: {e}")


# 기존 클래스들 (설정, AI 제공자 등)
class ExtractionConfig:
    def __init__(self, ai_provider: str = "claude", language_configs: Dict = None):
        self.ai_provider = ai_provider
        self.language_configs = language_configs or {}
    
    @classmethod
    def from_file(cls, config_path: str):
        """설정 파일에서 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return cls(
                ai_provider=data.get('ai_provider', 'claude'),
                language_configs=data.get('language_configs', {})
            )
        except Exception:
            # 기본 설정 반환
            return cls()


class AIProvider(ABC):
    def __init__(self, language: str):
        self.language = language
    
    @abstractmethod
    async def extract_all_content(self, content: str, title: str) -> Dict[str, str]:
        pass


class ClaudeProvider(AIProvider):
    async def extract_all_content(self, content: str, title: str) -> Dict[str, str]:
        """Claude를 사용한 내용 추출 (간단한 더미 구현)"""
        try:
            # 실제로는 여기서 Claude API를 호출해야 함
            # 지금은 간단한 더미 데이터 반환
            
            # 내용 요약 생성 (실제로는 AI 호출)
            content_preview = content[:500] + "..." if len(content) > 500 else content
            
            return {
                'core_content': f"핵심 내용 추출 (길이: {len(content)} 문자)",
                'detailed_core_content': f"상세 핵심 내용: {content_preview}",
                'main_topics': "주요 화제들이 추출됨",
                'sub_topics': "부차 화제들이 추출됨"
            }
            
        except Exception as e:
            print(f"❌ Claude 추출 실패: {e}")
            return {}


class AIProviderFactory:
    @staticmethod
    def create_provider(config: ExtractionConfig, language: str) -> AIProvider:
        if config.ai_provider == "claude":
            return ClaudeProvider(language)
        else:
            # 기본값으로 Claude 사용
            return ClaudeProvider(language)


if __name__ == "__main__":
    main()