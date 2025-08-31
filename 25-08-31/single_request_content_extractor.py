# 생성 시간: 2025-08-31 22:38:59 KST
# 핵심 내용: 장 전체 내용을 입력받아 한 번의 AI 요청으로 5가지 추출 항목을 동시에 처리하는 통합 추출기
# 상세 내용:
#   - SingleRequestExtractor 클래스 (36-180): 메인 단일 요청 추출 시스템
#   - unified_extract_all_content() (42-85): 5가지 항목 동시 추출 메서드
#   - 추출 항목: 핵심내용, 상세핵심내용, 상세정보, 주요화제, 부차화제
#   - modules 패키지의 AIProviderFactory 활용
# 상태: active
# 참조: unified_node_processor_v5.py

import asyncio
import json
import logging
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# 모듈화된 컴포넌트들 import
from modules import AIProviderFactory, ProcessingMode, AIProvider


class SingleRequestExtractor:
    """단일 요청으로 모든 내용을 추출하는 시스템"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logger()
        self.ai_factory = AIProviderFactory(self.config, self.logger)
        
        self.logger.info("✅ SingleRequestExtractor 초기화 완료")
    
    async def unified_extract_all_content(self, chapter_content: str) -> Dict[str, str]:
        """장 전체 내용에서 5가지 항목을 한 번에 추출"""
        
        system_prompt = """당신은 교육 콘텐츠 분석 전문가입니다. 
주어진 장 전체 내용을 분석하여 다음 5가지 항목을 추출해주세요.

응답은 반드시 아래 JSON 형식으로만 제공해주세요:

{
    "핵심내용": "장의 핵심 개념과 주제를 간결하게 요약 (2-3문장)",
    "상세핵심내용": "핵심내용을 더 자세히 설명 (4-6문장, 구체적 예시 포함)",
    "상세정보": "장의 전체적인 구조와 세부 내용을 체계적으로 정리 (10-15문장, 논리적 흐름 중심)",
    "주요화제": "장에서 다루는 핵심 주제들을 키워드 형태로 나열 (5-8개 항목, 쉼표로 구분)",
    "부차화제": "주요화제와 관련된 부가적인 개념들을 키워드 형태로 나열 (8-12개 항목, 쉼표로 구분)"
}

JSON 형식을 정확히 지켜주시고, 다른 설명이나 텍스트는 포함하지 마세요."""

        user_prompt = f"""다음 장 내용을 분석해주세요:

{chapter_content}"""

        try:
            self.logger.info("🔄 AI에 통합 추출 요청 전송 중...")
            
            response, prompt_tokens, response_tokens = await self.ai_factory.generate_content(
                user_prompt, system_prompt
            )
            
            self.logger.info(f"🔍 토큰 사용량 - 입력: {prompt_tokens}, 출력: {response_tokens}")
            
            # JSON 파싱 시도
            try:
                # JSON 추출 (코드 블록 제거)
                if "```json" in response:
                    json_start = response.find("```json") + 7
                    json_end = response.find("```", json_start)
                    json_content = response[json_start:json_end].strip()
                elif "```" in response:
                    json_start = response.find("```") + 3
                    json_end = response.find("```", json_start)
                    json_content = response[json_start:json_end].strip()
                else:
                    json_content = response.strip()
                
                result = json.loads(json_content)
                
                # 필수 키 확인
                required_keys = ["핵심내용", "상세핵심내용", "상세정보", "주요화제", "부차화제"]
                for key in required_keys:
                    if key not in result:
                        raise ValueError(f"필수 키 '{key}'가 응답에 없습니다")
                
                self.logger.info("✅ 통합 추출 완료")
                return result
                
            except json.JSONDecodeError as e:
                self.logger.error(f"❌ JSON 파싱 실패: {e}")
                self.logger.error(f"원본 응답: {response}")
                return self._create_fallback_result()
                
        except Exception as e:
            self.logger.error(f"❌ AI 요청 실패: {e}")
            return self._create_fallback_result()
    
    def _create_fallback_result(self) -> Dict[str, str]:
        """오류 발생시 기본 결과 반환"""
        return {
            "핵심내용": "추출 실패 - 수동 작업 필요",
            "상세핵심내용": "추출 실패 - 수동 작업 필요",  
            "상세정보": "추출 실패 - 수동 작업 필요",
            "주요화제": "추출 실패",
            "부차화제": "추출 실패"
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로딩"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # 기본 설정 적용
            defaults = {
                'ai_provider': 'gemini'
            }
            for key, value in defaults.items():
                if key not in config:
                    config[key] = value
                    
            return config
        except Exception as e:
            print(f"❌ 설정 파일 로딩 실패: {e}")
            raise
    
    def _setup_logger(self) -> logging.Logger:
        """로거 설정"""
        logger = logging.getLogger('single_request_extractor')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger


async def process_chapter_file(chapter_file_path: str, config_path: str = None) -> Dict[str, str]:
    """장 파일을 처리하여 모든 내용을 추출하는 편의 함수"""
    
    if config_path is None:
        config_path = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31/config.yaml'
    
    try:
        # 장 내용 파일 읽기
        with open(chapter_file_path, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        # 추출기 생성 및 실행
        extractor = SingleRequestExtractor(config_path)
        result = await extractor.unified_extract_all_content(chapter_content)
        
        return result
        
    except Exception as e:
        print(f"❌ 장 파일 처리 실패: {e}")
        return {}


# CLI 인터페이스
async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='단일 요청 내용 추출기')
    parser.add_argument('chapter_file', help='장 내용 파일 경로')
    parser.add_argument('--config', default='/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31/config.yaml', help='설정 파일 경로')
    parser.add_argument('--output', help='결과 저장 파일 경로 (JSON)')
    parser.add_argument('--ai-provider', choices=['gemini', 'claude', 'openai'], help='AI 프로바이더 선택')
    
    args = parser.parse_args()
    
    try:
        # 설정 오버라이드
        config_path = args.config
        if args.ai_provider:
            # 설정 파일 읽고 오버라이드
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            config['ai_provider'] = args.ai_provider
            # 임시 설정 파일 생성
            temp_config_path = f"{config_path}.temp"
            with open(temp_config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, ensure_ascii=False, default_flow_style=False)
            config_path = temp_config_path
        
        print(f"🚀 단일 요청 내용 추출 시작")
        print(f"📄 입력 파일: {args.chapter_file}")
        print(f"🤖 AI 프로바이더: {args.ai_provider or 'config 기본값'}")
        
        # 처리 실행
        result = await process_chapter_file(args.chapter_file, config_path)
        
        if result:
            print(f"\n✅ 추출 완료!")
            
            # 결과 출력
            for key, value in result.items():
                print(f"\n📋 {key}:")
                print(f"   {value}")
            
            # 파일 저장
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"\n💾 결과 저장: {args.output}")
        else:
            print(f"\n❌ 추출 실패!")
        
        # 임시 설정 파일 정리
        if args.ai_provider:
            Path(temp_config_path).unlink(missing_ok=True)
    
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))