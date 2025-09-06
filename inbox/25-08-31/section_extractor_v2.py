"""
생성 시간: 2025-08-31 21:22:23 KST
핵심 내용: config.yaml 통합 및 Claude SDK를 사용한 섹션별 마크다운 분리 도구
상세 내용:
    - import 구문 (24-37): 필요한 라이브러리 import 및 yaml 추가
    - ConfigLoader 클래스 (39-60): config.yaml 읽기 및 설정 관리
    - AIProvider 추상 클래스 (62-73): AI 제공자 인터페이스
    - ClaudeSDKProvider (75-104): Claude SDK 구현체
    - SectionExtractor 클래스 (106-320): 섹션 분리 및 저장 로직
        - __init__ (107-130): 초기화 및 config 기반 AI 제공자 설정
        - load_toc_json (132-140): JSON 목차 파일 읽기
        - load_markdown_document (142-150): 마크다운 문서 읽기
        - get_content_sections (152-162): has_content가 true인 섹션들 추출
        - extract_single_section_with_ai (164-205): AI로 특정 섹션 하나만 추출
        - extract_sections_with_ai_parallel (207-250): AI로 섹션별 개별 요청, 병렬 처리
        - save_sections_to_files (252-285): 각 섹션을 개별 .md 파일로 저장
        - process_and_extract (287-320): 전체 처리 워크플로우
    - main 함수 (322-350): 스크립트 실행 진입점
상태: active
참조: section_extractor
"""

import json
import os
import re
import sys
import asyncio
import argparse
import logging
import yaml
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

# 환경 변수 로드
try:
    from dotenv import load_dotenv
    load_dotenv("../.env")
except ImportError:
    print("⚠️  python-dotenv가 설치되지 않음. 환경변수 직접 설정 필요")

# Config Loader 클래스
class ConfigLoader:
    """config.yaml 파일 로드 및 설정 관리"""
    
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """config.yaml 파일 읽기"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"✅ 설정 파일 로드 완료: {self.config_path}")
            return config
        except FileNotFoundError:
            print(f"⚠️  설정 파일을 찾을 수 없습니다: {self.config_path}")
            return {}
        except Exception as e:
            print(f"❌ 설정 파일 로드 실패: {e}")
            return {}
    
    def get_script_config(self, script_name: str) -> Dict:
        """스크립트별 설정 추출"""
        return self.config.get('script_configs', {}).get(script_name, {})

# AI Provider 추상 클래스
class AIProvider(ABC):
    """AI 제공자 추상 베이스 클래스"""
    
    @abstractmethod
    async def query(self, prompt: str) -> str:
        """AI에게 쿼리를 보내고 응답을 받는 메서드"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        pass

# Claude SDK 구현체
class ClaudeSDKProvider(AIProvider):
    """Claude SDK 구현체"""
    
    def __init__(self):
        # Max Plan 사용자는 Claude Code CLI 기반 인증 사용
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
    
    async def query(self, prompt: str) -> str:
        try:
            from claude_code_sdk import query as claude_query
            
            responses = []
            async for message in claude_query(prompt=prompt):
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                    elif hasattr(content, 'text'):
                        responses.append(content.text)
            
            response_text = '\n'.join(responses) if responses else ''
            return response_text
            
        except Exception as e:
            print(f"Claude SDK 실행 실패: {str(e)}")
            raise

    def get_name(self) -> str:
        return "Claude SDK"

# 메인 섹션 추출 클래스
class SectionExtractor:
    def __init__(self, config_path="config.yaml", log_file=None):
        """초기화 및 설정 기반 AI 제공자 설정"""
        # 설정 로드
        self.config_loader = ConfigLoader(config_path)
        self.script_config = self.config_loader.get_script_config('section_extractor')
        
        # 로깅 설정
        self.setup_logging(log_file)
        
        # AI 제공자 설정 (config 우선, 기본값 claude)
        ai_provider_type = self.script_config.get('ai_provider', 'claude')
        
        if ai_provider_type.lower() == "claude":
            self.ai_provider = ClaudeSDKProvider()
        else:
            raise ValueError("현재는 Claude SDK만 지원합니다")
        
        self.markdown_content = ""
        self.toc_data = []
        self.ai_provider_type = ai_provider_type.lower()
        self.batch_size = self.script_config.get('batch_size', 4)
        
        log_msg = f"AI 제공자 초기화: {self.ai_provider.get_name()}"
        print(log_msg)
        self.logger.info(log_msg)
    
    def setup_logging(self, log_file=None):
        """로깅 시스템 설정"""
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"section_extractor_{timestamp}.log"
        
        # 로거 생성
        self.logger = logging.getLogger('SectionExtractor')
        self.logger.setLevel(logging.DEBUG)
        
        # 파일 핸들러 추가
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 기존 핸들러 제거 후 새로 추가
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        
        self.log_file = log_file
        print(f"📝 로그 파일: {log_file}")
    
    def load_toc_json(self, json_path):
        """JSON 목차 파일 읽기"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.toc_data = json.load(f)
            print(f"목차 JSON 로드 완료: {len(self.toc_data)} 항목")
            return True
        except Exception as e:
            print(f"JSON 파일 읽기 실패: {e}")
            return False
    
    def load_markdown_document(self, markdown_path):
        """마크다운 문서 읽기"""
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                self.markdown_content = f.read()
            print(f"마크다운 문서 로드 완료: {len(self.markdown_content)} 문자")
            return True
        except Exception as e:
            print(f"마크다운 파일 읽기 실패: {e}")
            return False
    
    def get_content_sections(self):
        """has_content가 true인 섹션들 추출"""
        content_sections = []
        for item in self.toc_data:
            if item.get('has_content', False):
                content_sections.append(item)
        
        print(f"콘텐츠 섹션 추출: {len(content_sections)}개 (전체 {len(self.toc_data)}개 중)")
        return content_sections

    def remove_section_title_from_content(self, content: str, section_title: str) -> str:
        """추출된 내용에서 불필요한 제목들을 제거합니다."""
        self.logger.debug(f"후처리 시작: '{section_title}' (내용 길이: {len(content)} 문자)")
        
        lines = content.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 장 제목 제거 (# 1 Complexity of object- oriented programming 등)
            if line_stripped.startswith('# ') and ('Complexity of object' in line_stripped or 'oriented programming' in line_stripped):
                self.logger.info(f"장 제목 제거: '{line_stripped}'")
                continue
            
            # 섹션 제목 중복 제거 (현재 섹션 제목과 일치하는 경우)
            # # 또는 ## 제거한 후 비교
            title_without_hash = section_title.lstrip('#').strip()
            line_without_hash = line_stripped.lstrip('#').strip()
            
            if line_without_hash == title_without_hash and line_stripped.startswith('#'):
                self.logger.info(f"섹션 제목 중복 제거: '{line_stripped}'")
                continue
            
            result_lines.append(line)
        
        result = '\n'.join(result_lines).strip()
        self.logger.debug(f"후처리 완료: '{section_title}' (결과 길이: {len(result)} 문자)")
        
        return result

    async def extract_single_section_with_ai(self, section_title, next_section_title=None):
        """AI로 특정 섹션 하나만 추출"""
        next_title_info = f"다음 섹션 제목: {next_section_title}" if next_section_title else "문서 끝까지"
        
        prompt = f"""다음 마크다운 문서에서 특정 섹션의 내용을 추출해주세요.

추출할 섹션: {section_title}
{next_title_info}

마크다운 문서:
```markdown
{self.markdown_content}
```

작업 지시:
1. '{section_title}' 제목을 문서에서 찾으세요
2. 해당 제목부터 {'다음 섹션(' + next_section_title + ')' if next_section_title else '문서 끝'} 전까지의 모든 내용을 추출하세요
3. 페이지 구분자(--- 페이지 X ---)도 포함해서 추출하세요
4. 섹션 내의 내용을 그대로 유지하세요
5. 제목과 문맥으로 섹션 범위를 판단하세요

중요한 제약사항:
- 어떤 설명이나 부가 정보도 추가하지 마세요
- "문서에서 ... 섹션의 내용을 추출하겠습니다" 같은 설명 금지
- "해당 섹션은..." 같은 부연설명 금지
- 오직 원본 문서의 해당 섹션 내용만 그대로 출력하세요

응답 형식:
섹션 내용을 그대로 복사하여 제공하세요. 어떤 추가 설명이나 마커 없이 원본 텍스트를 정확히 출력하세요.
"""

        try:
            self.logger.info(f"AI 요청 시작: '{section_title}'")
            response_text = await self.ai_provider.query(prompt)
            self.logger.info(f"AI 응답 받음: '{section_title}' (길이: {len(response_text)} 문자)")
            
            # 후처리: 섹션 제목 제거
            cleaned_content = self.remove_section_title_from_content(response_text.strip(), section_title)
            
            return cleaned_content
            
        except Exception as e:
            error_msg = f"AI 섹션 '{section_title}' 추출 실패: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            return None

    async def extract_sections_with_ai_parallel(self, content_sections):
        """AI로 섹션별 개별 요청, 병렬 처리"""
        print(f"\n🔍 AI로 {len(content_sections)}개 섹션 개별 추출 시작 ({self.batch_size}개씩 병렬 처리)")
        
        # 다음 섹션 제목 정보 준비
        section_pairs = []
        for i, section in enumerate(content_sections):
            next_section = content_sections[i + 1] if i + 1 < len(content_sections) else None
            next_title = next_section['title'] if next_section else None
            section_pairs.append((section, next_title))
        
        # 배치 단위로 그룹화
        batches = [section_pairs[i:i + self.batch_size] for i in range(0, len(section_pairs), self.batch_size)]
        
        all_results = []
        for batch_idx, batch in enumerate(batches):
            print(f"\n📦 배치 {batch_idx + 1}/{len(batches)} 처리 중 ({len(batch)}개 섹션)...")
            
            # 배치 내 병렬 처리
            tasks = []
            sections_in_batch = []
            for section, next_title in batch:
                task = self.extract_single_section_with_ai(section['title'], next_title)
                tasks.append(task)
                sections_in_batch.append(section)
            
            # 병렬 실행
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                batch_results = []
                
                for section, result in zip(sections_in_batch, results):
                    if isinstance(result, Exception):
                        print(f"❌ '{section['title']}' 추출 실패: {result}")
                        batch_results.append((section, None))
                    else:
                        print(f"✅ '{section['title']}' 추출 완료")
                        batch_results.append((section, result))
            except Exception as e:
                print(f"❌ 배치 처리 실패: {e}")
                batch_results = [(section, None) for section in sections_in_batch]
            
            all_results.extend(batch_results)
        
        print(f"🎉 전체 추출 완료: {len(all_results)}개 섹션")
        return all_results
    
    def save_sections_to_files(self, section_results, output_dir="."):
        """섹션별 추출 결과를 개별 .md 파일로 저장"""
        if not section_results:
            return []
        
        # 출력 디렉토리 생성
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        saved_files = []
        
        for section, content in section_results:
            if content is None:
                print(f"⚠️ 섹션 '{section['title']}' 내용이 없어 건너뜀")
                continue
            
            # 파일명 생성 (노드 문서와 동일한 정규화 로직 적용)
            section_title = section['title']
            title_clean = re.sub(r'[^\w\s.-]', '', section_title)  # 점(.)도 유지
            title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
            filename = f"{title_clean}.md"
            filepath = output_path / filename
            
            # 파일 저장
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ 섹션 저장: {filename}")
                saved_files.append(str(filepath))
            except Exception as e:
                print(f"❌ 섹션 '{section_title}' 저장 실패: {e}")
        
        return saved_files
    
    async def process_and_extract(self, json_path, markdown_path, output_dir="."):
        """전체 처리 워크플로우"""
        # 파일 로드
        if not self.load_toc_json(json_path):
            return None
        if not self.load_markdown_document(markdown_path):
            return None
        
        print("\n=== 섹션 분리 프로세스 시작 ===")
        
        # 콘텐츠 섹션 추출
        content_sections = self.get_content_sections()
        if not content_sections:
            print("❌ 콘텐츠 섹션이 없습니다")
            return None
        
        # AI로 섹션별 개별 추출 (병렬 처리)
        section_results = await self.extract_sections_with_ai_parallel(content_sections)
        if not section_results:
            print("❌ AI 섹션 추출 실패")
            return None
        
        # 개별 파일로 저장
        saved_files = self.save_sections_to_files(section_results, output_dir)
        
        print(f"\n=== 섹션 분리 완료: {len(saved_files)}개 파일 저장 ===")
        for file_path in saved_files:
            print(f"📄 {file_path}")
        
        return saved_files

async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="config.yaml 기반 AI 섹션 분리 도구")
    parser.add_argument("json_path", help="JSON 목차 파일 경로")
    parser.add_argument("markdown_path", help="마크다운 문서 파일 경로")
    parser.add_argument("-o", "--output", help="출력 디렉터리 (config.yaml에서 기본값 읽기)")
    parser.add_argument("--config", default="config.yaml", help="설정 파일 경로 (기본값: config.yaml)")
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not os.path.exists(args.json_path):
        print(f"JSON 파일을 찾을 수 없습니다: {args.json_path}")
        sys.exit(1)
        
    if not os.path.exists(args.markdown_path):
        print(f"마크다운 파일을 찾을 수 없습니다: {args.markdown_path}")
        sys.exit(1)
    
    # 섹션 분리 실행
    try:
        extractor = SectionExtractor(args.config)
        
        # 출력 디렉터리 결정 (CLI 인자 > config.yaml > 기본값)
        output_dir = args.output or extractor.script_config.get('output_directory', './sections')
        
        saved_files = await extractor.process_and_extract(
            args.json_path, 
            args.markdown_path, 
            output_dir
        )
        
        if saved_files:
            print(f"\n🎉 섹션 분리 완료! {len(saved_files)}개 파일 저장됨")
            print(f"🤖 사용된 AI: {extractor.ai_provider.get_name()}")
            print(f"📁 출력 디렉터리: {output_dir}")
        else:
            print("\n❌ 섹션 분리 실패")
            sys.exit(1)
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())