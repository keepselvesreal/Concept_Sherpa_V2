"""
생성 시간: 2025-08-30 14:58:59 KST
핵심 내용: Claude SDK를 사용해 장 전체를 섹션별로 분리하여 개별 마크다운 파일로 저장
상세 내용:
    - import 구문 (24-35): 필요한 라이브러리 import
    - AIProvider 추상 클래스 (37-48): AI 제공자 인터페이스
    - ClaudeSDKProvider (50-88): Claude SDK 구현체
    - SectionExtractor 클래스 (90-220): 섹션 분리 및 저장 로직
        - __init__ (91-98): 초기화 및 AI 제공자 설정
        - load_toc_json (100-108): JSON 목차 파일 읽기
        - load_markdown_document (110-118): 마크다운 문서 읽기
        - get_content_sections (120-130): has_content가 true인 섹션들 추출
        - extract_sections_with_ai (132-170): AI로 전체 장을 섹션별로 분리
        - save_sections_to_files (172-195): 각 섹션을 개별 .md 파일로 저장
        - process_and_extract (197-220): 전체 처리 워크플로우
    - main 함수 (222-250): 스크립트 실행 진입점
상태: active
주소: section_extractor
참조: content_node_extractor
"""

import json
import os
import re
import sys
import asyncio
import argparse
import logging
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

# Gemini API 구현체
class GeminiAPIProvider(AIProvider):
    """Gemini API 구현체 - gemini-2.5-flash-lite"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다")
        self.model_name = "models/gemini-2.5-flash-lite"
    
    async def query(self, prompt: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            return response_text
            
        except Exception as e:
            print(f"Gemini API 실행 실패: {e}")
            raise

    def get_name(self) -> str:
        return f"Gemini API ({self.model_name})"

# Claude SDK 구현체 (기존 방식)
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
    def __init__(self, ai_provider_type="claude", log_file=None):
        """초기화 및 AI 제공자 설정"""
        # 로깅 설정
        self.setup_logging(log_file)
        
        if ai_provider_type.lower() == "claude":
            self.ai_provider = ClaudeSDKProvider()
        elif ai_provider_type.lower() == "gemini":
            self.ai_provider = GeminiAPIProvider()
        else:
            raise ValueError("지원되는 AI 제공자: 'claude' 또는 'gemini'")
        
        self.markdown_content = ""
        self.toc_data = []
        self.ai_provider_type = ai_provider_type.lower()
        
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
        """추출된 내용에서 섹션 제목을 제거합니다."""
        self.logger.debug(f"후처리 시작: '{section_title}' (내용 길이: {len(content)} 문자)")
        
        lines = content.split('\n')
        
        # 첫 번째 줄이 섹션 제목과 일치하는지 확인 (# 포함 또는 미포함)
        if lines:
            first_line = lines[0].strip()
            # # 제거한 제목과 비교
            title_without_hash = section_title.lstrip('#').strip()
            first_line_without_hash = first_line.lstrip('#').strip()
            
            self.logger.debug(f"제목 매칭 확인: '{title_without_hash}' vs '{first_line_without_hash}'")
            
            if first_line_without_hash == title_without_hash:
                # 첫 번째 줄이 제목이면 제거
                result = '\n'.join(lines[1:]).strip()
                self.logger.info(f"섹션 제목 제거됨: '{section_title}' (결과 길이: {len(result)} 문자)")
                return result
            else:
                self.logger.info(f"섹션 제목 매칭 실패, 원본 반환: '{section_title}'")
        
        return content

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
            
            # 후처리는 일단 제외하고 원본 그대로 반환
            return response_text.strip()
            
        except Exception as e:
            error_msg = f"AI 섹션 '{section_title}' 추출 실패: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            return None

    async def extract_sections_with_ai_parallel(self, content_sections, batch_size=4):
        """AI로 섹션별 개별 요청, 병렬 처리"""
        print(f"\n🔍 AI로 {len(content_sections)}개 섹션 개별 추출 시작 ({batch_size}개씩 병렬 처리)")
        
        # 다음 섹션 제목 정보 준비
        section_pairs = []
        for i, section in enumerate(content_sections):
            next_section = content_sections[i + 1] if i + 1 < len(content_sections) else None
            next_title = next_section['title'] if next_section else None
            section_pairs.append((section, next_title))
        
        # 배치 단위로 그룹화
        batches = [section_pairs[i:i + batch_size] for i in range(0, len(section_pairs), batch_size)]
        
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
        section_results = await self.extract_sections_with_ai_parallel(content_sections, batch_size=4)
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
    parser = argparse.ArgumentParser(description="AI 기반 장 섹션별 분리 및 파일 저장")
    parser.add_argument("json_path", help="JSON 목차 파일 경로")
    parser.add_argument("markdown_path", help="마크다운 문서 파일 경로")
    parser.add_argument("-o", "--output", default="sections", help="출력 디렉터리 (기본값: sections)")
    parser.add_argument("--ai-provider", default="claude", choices=["claude", "gemini"], help="AI 제공자 선택 (기본값: claude)")
    parser.add_argument("--batch-size", type=int, default=4, help="병렬 처리 배치 크기 (기본값: 4)")
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not os.path.exists(args.json_path):
        print(f"JSON 파일을 찾을 수 없습니다: {args.json_path}")
        sys.exit(1)
        
    if not os.path.exists(args.markdown_path):
        print(f"마크다운 파일을 찾을 수 없습니다: {args.markdown_path}")
        sys.exit(1)
    
    # AI 제공자 검증
    print(f"🤖 선택된 AI 제공자: {args.ai_provider.upper()}")
    if args.ai_provider == "gemini":
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다")
            sys.exit(1)
    
    # 섹션 분리 실행
    try:
        extractor = SectionExtractor(args.ai_provider)
        saved_files = await extractor.process_and_extract(
            args.json_path, 
            args.markdown_path, 
            args.output
        )
        
        if saved_files:
            print(f"\n🎉 섹션 분리 완료! {len(saved_files)}개 파일 저장됨")
            print(f"🤖 사용된 AI: {extractor.ai_provider.get_name()}")
            print(f"📁 출력 디렉터리: {args.output}")
        else:
            print("\n❌ 섹션 분리 실패")
            sys.exit(1)
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())