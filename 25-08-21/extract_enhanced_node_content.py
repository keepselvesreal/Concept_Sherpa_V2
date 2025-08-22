#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 20:31:04
핵심 내용: 노드 정보 문서에서 4개 추출 작업을 순차/병렬 처리하여 향상된 분석 결과를 생성하는 스크립트
상세 내용: 
    - ExtractionConfig() (line 25): 설정 파일 관리 클래스
    - AIProvider (line 60): AI 모델 추상화 기본 클래스
    - ClaudeProvider (line 65): Claude SDK 구현체
    - GeminiProvider (line 110): Gemini API 구현체 (향후 확장)
    - get_source_language() (line 140): source_language 추출
    - extract_content_section() (line 160): 내용 섹션 추출
    - extract_with_fallback() (line 200): 재시도 로직이 포함된 추출 함수
    - extract_core_and_detailed_sequential() (line 220): 핵심+상세핵심 순차 처리
    - extract_content_parallel() (line 250): 4개 작업 그룹 병렬 실행
    - update_extraction_section() (line 340): 추출 결과를 문서에 삽입
    - main() (line 395): 메인 실행 함수
상태: active
참조: extract_node_analysis_v4.py
"""

import asyncio
import os
import time
import argparse
import yaml
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pathlib import Path


class ExtractionConfig:
    """설정 파일 관리 클래스"""
    
    def __init__(self, config_path: str = "extraction_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """설정 파일 로드"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            print(f"⚠️ 설정 파일 로드 실패, 기본값 사용: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """기본 설정 반환"""
        return {
            'extraction': {
                'ai_provider': 'claude',
                'fallback': {
                    'max_attempts': 3,
                    'retry_delay_base': 1.0,
                    'default_language': 'korean'
                }
            }
        }
    
    def get_ai_provider(self) -> str:
        return self.config['extraction']['ai_provider']
    
    def get_fallback_config(self) -> dict:
        return self.config['extraction']['fallback']


class AIProvider(ABC):
    """AI 모델 추상화 기본 클래스"""
    
    @abstractmethod
    async def extract_content(self, prompt: str, system_prompt: str) -> str:
        """내용 추출 메소드"""
        pass


class ClaudeProvider(AIProvider):
    """Claude SDK 구현체"""
    
    def __init__(self, config: dict):
        self.config = config
        try:
            from claude_code_sdk import query, ClaudeCodeOptions
            self.query = query
            self.ClaudeCodeOptions = ClaudeCodeOptions
        except ImportError:
            raise ImportError("claude_code_sdk를 찾을 수 없습니다. Claude Code에서 실행해주세요.")
    
    async def extract_content(self, prompt: str, system_prompt: str) -> str:
        """Claude를 사용한 내용 추출"""
        try:
            messages = []
            async for message in self.query(
                prompt=prompt,
                options=self.ClaudeCodeOptions(
                    max_turns=self.config.get('max_turns', 1),
                    system_prompt=system_prompt,
                    allowed_tools=self.config.get('allowed_tools', [])
                )
            ):
                messages.append(message)
            
            if messages:
                last_message = messages[-1]
                message_type = type(last_message).__name__
                
                # ResultMessage 타입 처리
                if message_type == "ResultMessage":
                    if hasattr(last_message, 'IsError') and last_message.IsError:
                        error_info = f"API Error (Session: {getattr(last_message, 'SessionID', 'Unknown')})"
                        print(f"❌ Claude API 오류 응답: {error_info}")
                        raise Exception(f"Claude API Error: {error_info}")
                    
                    if hasattr(last_message, 'Result') and last_message.Result:
                        return str(last_message.Result).strip()
                
                # 기존 처리 로직 (다른 메시지 타입들)
                if hasattr(last_message, 'result') and last_message.result:
                    return last_message.result.strip()
                elif hasattr(last_message, 'text'):
                    return last_message.text.strip()
                elif hasattr(last_message, 'content'):
                    if isinstance(last_message.content, list):
                        content = ""
                        for block in last_message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                        return content.strip()
                    else:
                        return str(last_message.content).strip()
                else:
                    # 디버깅 정보 출력
                    print(f"⚠️ 알 수 없는 메시지 타입: {message_type}")
                    if hasattr(last_message, '__dict__'):
                        available_attrs = list(last_message.__dict__.keys())[:5]  # 처음 5개 속성만
                        print(f"   사용 가능한 속성: {available_attrs}")
                    return str(last_message).strip()
            else:
                raise Exception("Claude API에서 응답을 받지 못했습니다")
                
        except Exception as e:
            print(f"❌ Claude API 호출 실패: {e}")
            raise  # Exception을 다시 발생시켜 재시도 로직 작동


class GeminiProvider(AIProvider):
    """Gemini API 구현체 (향후 확장)"""
    
    def __init__(self, config: dict):
        self.config = config
        # TODO: Gemini API 초기화
    
    async def extract_content(self, prompt: str, system_prompt: str) -> str:
        """Gemini를 사용한 내용 추출 - 구현 예정"""
        # TODO: Gemini API 구현
        return "❌ Gemini 지원 예정"


def get_source_language(info_file: str, default_language: str = "korean") -> str:
    """정보 파일에서 source_language 추출"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('source_language:'):
                lang = line.split(':', 1)[1].strip()
                if lang in ["korean", "english"]:
                    return lang
        
        return default_language
        
    except Exception as e:
        print(f"⚠️ source_language 추출 실패, 기본값 사용: {e}")
        return default_language


def extract_content_section(info_file: str) -> str:
    """정보 파일에서 '# 내용' 섹션 추출"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        content_start = -1
        content_end = len(lines)
        
        # '# 내용' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_start = i + 1
                break
        
        # 다음 구조 섹션 찾기
        structure_sections = ['# 구성', '# 속성', '# 추출']
        for i in range(content_start, len(lines)):
            line = lines[i].strip()
            if any(line.startswith(section) for section in structure_sections):
                content_end = i
                break
        
        if content_start == -1:
            return ""
        
        # 구분선(---)까지 스킵
        while content_start < content_end and lines[content_start].strip() == '---':
            content_start += 1
        
        # 실제 텍스트가 있는지 확인
        section_content = '\n'.join(lines[content_start:content_end])
        has_actual_text = any(line.strip() and not line.strip() == '---' for line in lines[content_start:content_end])
        
        if not has_actual_text:
            return ""
        
        return section_content.strip()
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""


async def extract_with_fallback(task_func, max_attempts: int, retry_delay: float, task_name: str):
    """재시도 로직이 포함된 추출 함수"""
    for attempt in range(max_attempts):
        try:
            result = await task_func()
            if result and len(result.strip()) >= 10:
                return result
        except Exception as e:
            print(f"⚠️ {task_name} 추출 시도 {attempt + 1} 실패: {e}")
        
        if attempt < max_attempts - 1:
            await asyncio.sleep(retry_delay * (2 ** attempt))  # 지수 백오프
    
    return f"❌ {task_name} 추출 실패 (최대 재시도 횟수 초과)"


async def extract_core_and_detailed_sequential(content: str, title: str, provider: AIProvider, source_language: str, fallback_config: dict) -> Dict[str, str]:
    """핵심 내용과 상세 핵심 내용을 순차적으로 추출"""
    result = {}
    max_attempts = fallback_config.get('max_attempts', 3)
    retry_delay = fallback_config.get('retry_delay_base', 1.0)
    
    # 1단계: 핵심 내용 추출 (Fallback 적용)
    core_content = await extract_with_fallback(
        lambda: _extract_core_content(content, title, provider, source_language),
        max_attempts, retry_delay, "핵심 내용"
    )
    result["핵심 내용"] = core_content
    
    # 2단계: 핵심 내용 성공 시에만 상세 핵심 내용 추출
    if not core_content.startswith("❌"):
        detailed_core = await extract_with_fallback(
            lambda: _extract_detailed_core_content(content, core_content, title, provider, source_language),
            max_attempts, retry_delay, "상세 핵심 내용"
        )
        result["상세 핵심 내용"] = detailed_core
    else:
        result["상세 핵심 내용"] = "❌ 핵심 내용 추출 실패로 인한 상세 내용 추출 불가"
    
    return result


async def extract_content_parallel(content: str, title: str, provider: AIProvider, source_language: str, fallback_config: dict) -> Dict[str, str]:
    """4개 추출 작업을 순차+병렬로 실행"""
    print(f"🚀 향상된 추출 시작 (source_language: {source_language})")
    start_time = time.time()
    
    max_attempts = fallback_config.get('max_attempts', 3)
    retry_delay = fallback_config.get('retry_delay_base', 1.0)
    
    # 4개 그룹을 병렬로 실행
    tasks = [
        # 그룹 1: 핵심 + 상세 핵심 (순차)
        extract_core_and_detailed_sequential(content, title, provider, source_language, fallback_config),
        
        # 그룹 2: 상세 내용 (독립)
        extract_with_fallback(
            lambda: _extract_detailed_content(content, title, provider, source_language),
            max_attempts, retry_delay, "상세 내용"
        ),
        
        # 그룹 3: 주요 화제 (독립)
        extract_with_fallback(
            lambda: _extract_main_topics(content, title, provider, source_language),
            max_attempts, retry_delay, "주요 화제"
        ),
        
        # 그룹 4: 부차 화제 (독립)
        extract_with_fallback(
            lambda: _extract_sub_topics(content, title, provider, source_language),
            max_attempts, retry_delay, "부차 화제"
        )
    ]
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 결과 통합 (순서 보장)
        final_result = {}
        
        # 그룹 1 결과 (핵심 + 상세 핵심)
        if isinstance(results[0], dict):
            final_result.update(results[0])
        else:
            final_result["핵심 내용"] = f"❌ 핵심 내용 그룹 처리 실패: {results[0]}"
            final_result["상세 핵심 내용"] = "❌ 핵심 내용 그룹 실패로 인한 추출 불가"
        
        # 나머지 독립 작업 결과
        task_names = ["상세 내용", "주요 화제", "부차 화제"]
        for i, task_name in enumerate(task_names, 1):
            if i < len(results):
                if isinstance(results[i], str):
                    final_result[task_name] = results[i]
                else:
                    final_result[task_name] = f"❌ {task_name} 처리 중 예외 발생: {results[i]}"
        
        end_time = time.time()
        print(f"✅ 향상된 추출 완료 ({end_time - start_time:.2f}초)")
        
        return final_result
        
    except Exception as e:
        print(f"❌ 추출 실행 실패: {e}")
        return {}


async def _extract_core_content(content: str, title: str, provider: AIProvider, source_language: str) -> str:
    """핵심 내용 추출"""
    language_instruction = "영어로" if source_language == "english" else "한국어로"
    
    prompt = f"""다음은 "{title}"의 내용입니다:
{content}

이 내용의 핵심을 2-3문장으로 간결하게 {language_instruction} 요약해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_prompt = f"텍스트 분석 전문가. {title}의 핵심 내용을 {language_instruction} 간결하고 명확하게 요약하세요."
    
    return await provider.extract_content(prompt, system_prompt)


async def _extract_detailed_core_content(content: str, core_content: str, title: str, provider: AIProvider, source_language: str) -> str:
    """상세 핵심 내용 추출 - 핵심 내용을 더 자세히 부연 설명"""
    language_instruction = "영어로" if source_language == "english" else "한국어로"
    
    prompt = f"""핵심 내용: "{core_content}"

원본 내용: "{title}"
{content}

핵심 내용에서 언급된 요점들을 300단어 이내로 더 상세하게 {language_instruction} 설명해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_prompt = f"내용 해설 전문가. {title}의 핵심 내용을 더 자세하게 {language_instruction} 부연 설명하세요."
    
    return await provider.extract_content(prompt, system_prompt)


async def _extract_detailed_content(content: str, title: str, provider: AIProvider, source_language: str) -> str:
    """상세 내용 추출 (길이 제한 없음)"""
    language_instruction = "영어로" if source_language == "english" else "한국어로"
    
    prompt = f"""다음은 "{title}"의 내용입니다:
{content}

이 내용에서 중요한 세부사항들을 상세하게 {language_instruction} 추출해주세요.
충분히 자세하게 설명해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_prompt = f"상세 분석 전문가. {title}의 중요한 세부사항을 {language_instruction} 충분히 자세하게 설명하세요."
    
    return await provider.extract_content(prompt, system_prompt)


async def _extract_main_topics(content: str, title: str, provider: AIProvider, source_language: str) -> str:
    """주요 화제 추출"""
    language_instruction = "영어로" if source_language == "english" else "한국어로"
    
    prompt = f"""다음은 "{title}"의 내용입니다:
{content}

이 내용에서 다루어지는 3-5개의 주요 화제나 주제를 {language_instruction} 추출해주세요.
각 항목은 반드시 "-" 문자로 시작하는 목록 형태로 작성하세요.
추가 내용 없이 바로 목록만 작성하세요.

형식:
- 주제1: 설명
- 주제2: 설명

응답에 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_prompt = f"Extract main themes {language_instruction} in dash list format without additional text."
    
    return await provider.extract_content(prompt, system_prompt)


async def _extract_sub_topics(content: str, title: str, provider: AIProvider, source_language: str) -> str:
    """부차 화제 추출"""
    language_instruction = "영어로" if source_language == "english" else "한국어로"
    
    prompt = f"""다음은 "{title}"의 내용입니다:
{content}

주요 테마를 보완하는 3-5개의 부차적 주제, 세부 주제, 또는 지원 세부사항을 {language_instruction} 추출해주세요.
각 항목은 반드시 "-" 문자로 시작하는 목록 형태로 작성하세요.
추가 내용 없이 바로 목록만 작성하세요.

형식:
- 부차주제1: 설명
- 부차주제2: 설명

응답에 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_prompt = f"Extract secondary themes {language_instruction} in dash list format without additional text."
    
    return await provider.extract_content(prompt, system_prompt)


def update_extraction_section(info_file: str, extracted_data: Dict[str, str]) -> bool:
    """추출 결과를 문서에 삽입"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        extraction_start = -1
        extraction_end = len(lines)
        
        # '# 추출' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 추출':
                extraction_start = i
                break
        
        if extraction_start == -1:
            print(f"⚠️ '# 추출' 섹션을 찾을 수 없음")
            return False
        
        # 다음 섹션 찾기
        for i in range(extraction_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 추출':
                extraction_end = i
                break
        
        # 추출 섹션 재구성 (순서 보장)
        new_extraction_lines = ['# 추출', '---']
        
        # 정확한 순서로 삽입: 핵심 내용 → 상세 핵심 내용 → 상세 내용 → 주요 화제 → 부차 화제
        extraction_order = ["핵심 내용", "상세 핵심 내용", "상세 내용", "주요 화제", "부차 화제"]
        for key in extraction_order:
            if key in extracted_data:
                new_extraction_lines.append(f"## {key}")
                new_extraction_lines.append(extracted_data[key])
                new_extraction_lines.append("")
        
        # 파일 재구성
        new_lines = (
            lines[:extraction_start] +
            new_extraction_lines +
            lines[extraction_end:]
        )
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"❌ 추출 섹션 업데이트 실패: {e}")
        return False


def create_ai_provider(provider_type: str, config: ExtractionConfig) -> AIProvider:
    """AI 모델 팩토리"""
    providers_config = config.config.get('providers', {})
    
    if provider_type == "claude":
        provider_config = providers_config.get('claude', {})
        return ClaudeProvider(provider_config)
    elif provider_type == "gemini":
        provider_config = providers_config.get('gemini', {})
        return GeminiProvider(provider_config)
    else:
        raise ValueError(f"지원되지 않는 AI 모델: {provider_type}")


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='노드 정보 문서에서 향상된 4개 추출 작업을 순차+병렬 처리')
    parser.add_argument('info_file', help='처리할 정보 파일 경로')
    parser.add_argument('--config', default='extraction_config.yaml', help='설정 파일 경로')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.info_file):
        print(f"❌ 파일을 찾을 수 없습니다: {args.info_file}")
        return
    
    # 설정 로드
    config = ExtractionConfig(args.config)
    print(f"🔧 설정 로드 완료: {config.get_ai_provider()} 모델 사용")
    
    print(f"🚀 향상된 노드 분석 시작: {os.path.basename(args.info_file)}")
    
    # source_language 감지
    fallback_config = config.get_fallback_config()
    source_language = get_source_language(args.info_file, fallback_config.get('default_language', 'korean'))
    print(f"🌍 감지된 source_language: {source_language}")
    
    # 내용 섹션 추출
    content = extract_content_section(args.info_file)
    if not content:
        print("❌ 내용 섹션이 비어있거나 추출할 수 없습니다.")
        return
    
    print(f"📄 내용 길이: {len(content)} 문자")
    
    # 제목 추출
    title = os.path.basename(args.info_file).replace('_info.md', '').replace('_', ' ')
    
    async def run_extraction():
        # AI 모델 생성
        try:
            provider = create_ai_provider(config.get_ai_provider(), config)
        except Exception as e:
            print(f"❌ AI 모델 생성 실패: {e}")
            return
        
        # 추출 실행
        extracted_data = await extract_content_parallel(content, title, provider, source_language, fallback_config)
        
        if not extracted_data:
            print("❌ 추출된 데이터가 없습니다.")
            return
        
        # 추출 섹션 업데이트
        if update_extraction_section(args.info_file, extracted_data):
            print("✅ 향상된 추출 섹션 업데이트 완료")
            
            # 결과 요약
            print("\n📊 추출 결과:")
            for key, value in extracted_data.items():
                status = "✅" if not value.startswith("❌") else "❌"
                preview = value[:100] + "..." if len(value) > 100 else value
                print(f"  {status} {key}: {preview}")
        else:
            print("❌ 추출 섹션 업데이트 실패")
    
    # 비동기 실행
    asyncio.run(run_extraction())


if __name__ == "__main__":
    main()