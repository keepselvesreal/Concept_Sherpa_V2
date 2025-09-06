"""
생성 시간: 2025-08-30 12:51:51 KST (최종 수정)
핵심 내용: AI 기반 콘텐츠 노드 추출 및 분석 시스템
상세 내용:
    - import 구문 (1-12): 필요한 라이브러리 import
    - AIProvider 추상 클래스 (14-25): AI 제공자 인터페이스
    - ClaudeSDKProvider (27-65): Claude SDK 구현체
    - ContentNodeExtractor 클래스 (67-220): AI 기반 콘텐츠 노드 추출 로직
        - __init__ (68-75): 초기화 및 AI 제공자 설정
        - load_toc_json (77-85): JSON 목차 파일 읽기
        - load_markdown_document (87-95): 마크다운 문서 읽기
        - get_max_level (97-103): 최대 레벨 찾기
        - find_items_with_subordinates (105-120): 하위 항목이 있는 항목들 식별
        - analyze_content_with_ai (122-160): AI를 통한 콘텐츠 존재 여부 분석
        - extract_content_nodes (162-175): has_content true 노드들만 필터링
        - save_content_nodes_json (177-185): content_nodes.json 저장
        - process_and_extract (187-220): 전체 처리 및 콘텐츠 노드 추출
    - main 함수 (222-250): 스크립트 실행 진입점
상태: active
주소: content_node_extractor
참조: extract_chapters, content_analyzer (삭제됨)
"""

import json
import os
import sys
import asyncio
import argparse
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

# Gemini API 구현체  
class GeminiAPIProvider(AIProvider):
    """Gemini API 구현체"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다")
    
    async def query(self, prompt: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            return response_text
            
        except Exception as e:
            print(f"Gemini API 실행 실패: {str(e)}")
            raise

    def get_name(self) -> str:
        return "Gemini API"

# 메인 콘텐츠 노드 추출 클래스
class ContentNodeExtractor:
    def __init__(self, ai_provider_type="claude"):
        """초기화 및 AI 제공자 설정"""
        if ai_provider_type.lower() == "gemini":
            self.ai_provider = GeminiAPIProvider()
        else:
            self.ai_provider = ClaudeSDKProvider()
        
        self.markdown_content = ""
        self.toc_data = []
        print(f"AI 제공자 초기화: {self.ai_provider.get_name()}")
    
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
    
    def get_max_level(self):
        """최대 레벨 찾기"""
        max_level = 0
        for item in self.toc_data:
            level = item.get('level', 0)
            if level > max_level:
                max_level = level
        return max_level
    
    def find_items_to_analyze(self):
        """최대 레벨을 제외한 모든 항목들 식별"""
        max_level = self.get_max_level()
        items_to_analyze = []
        
        for i, item in enumerate(self.toc_data):
            current_level = item.get('level', 0)
            
            # 최대 레벨이 아닌 모든 항목 분석
            if current_level < max_level:
                next_item = None
                if i < len(self.toc_data) - 1:
                    next_item = self.toc_data[i + 1]
                
                items_to_analyze.append({
                    'index': i,
                    'current_item': item,
                    'next_item': next_item
                })
        
        return items_to_analyze
    
    async def analyze_content_with_ai(self, current_item, next_item, markdown_content):
        """AI를 통한 콘텐츠 존재 여부 분석"""
        current_title = current_item.get('title', '')
        next_title = next_item.get('title', '') if next_item else '문서 끝'
        
        prompt = f"""다음 마크다운 문서에서 '{current_title}' 제목과 '{next_title}' 제목 사이에 실제 텍스트 내용이 있는지 분석해주세요.

현재 항목: {current_title}
다음 항목: {next_title}

마크다운 문서:
```markdown
{markdown_content}
```

작업:
1. '{current_title}' 제목을 찾으세요
2. '{next_title}' 제목을 찾으세요  
3. 두 제목 사이에 의미있는 텍스트 내용이 있는지 확인하세요
4. 단순한 페이지 구분자(--- 페이지 X ---)나 챕터 헤더는 제외하고 판단하세요

판단 기준:
- 30자 이상의 의미있는 텍스트가 있으면 true
- 단순 제목이나 페이지 번호만 있으면 false
- NOTE, 설명문, 대화문 등이 있으면 true

응답 형식 (JSON만):
{{
    "has_content": true/false
}}"""

        try:
            response_text = await self.ai_provider.query(prompt)
            
            # JSON 파싱 시도
            if '```json' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text
            else:
                json_text = response_text
            
            result = json.loads(json_text)
            return result.get('has_content', False)
            
        except json.JSONDecodeError as e:
            print(f"AI 응답 JSON 파싱 실패: {e}")
            return False
        except Exception as e:
            print(f"AI 분석 실패: {e}")
            return False
    
    def extract_content_nodes(self):
        """has_content가 true인 노드들만 필터링하여 반환"""
        content_nodes = []
        for item in self.toc_data:
            if item.get('has_content', False):
                content_nodes.append(item)
        
        print(f"콘텐츠 노드 추출 완료: {len(content_nodes)}개 (전체 {len(self.toc_data)}개 중)")
        return content_nodes
    
    def save_content_nodes_json(self, content_nodes, output_dir="."):
        """content_nodes.json으로 저장"""
        try:
            output_path = os.path.join(output_dir, "content_nodes.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(content_nodes, f, ensure_ascii=False, indent=2)
            print(f"콘텐츠 노드 저장 완료: {output_path}")
            return output_path
        except Exception as e:
            print(f"콘텐츠 노드 저장 실패: {e}")
            return None
    
    def save_updated_json(self, output_path):
        """업데이트된 전체 JSON 저장 (has_content 필드 포함)"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.toc_data, f, ensure_ascii=False, indent=2)
            print(f"업데이트된 JSON 저장 완료: {output_path}")
        except Exception as e:
            print(f"JSON 저장 실패: {e}")
    
    async def process_and_extract(self, json_path, markdown_path, output_dir="."):
        """전체 처리 및 콘텐츠 노드 추출 워크플로우"""
        # 파일 로드
        if not self.load_toc_json(json_path):
            return None
        if not self.load_markdown_document(markdown_path):
            return None
        
        print("\n=== 콘텐츠 노드 추출 프로세스 시작 ===")
        
        # 1단계: 최대 레벨 항목들 has_content = true 설정
        max_level = self.get_max_level()
        print(f"최대 레벨: {max_level}")
        
        max_level_count = 0
        for item in self.toc_data:
            if item.get('level', 0) == max_level:
                item['has_content'] = True
                max_level_count += 1
                print(f"✅ [{item['title']}] - 최대 레벨({max_level}) → has_content: true")
        
        print(f"최대 레벨 항목 {max_level_count}개 처리 완료\n")
        
        # 2단계: 최대 레벨을 제외한 모든 항목들 AI 분석
        items_to_analyze = self.find_items_to_analyze()
        print(f"AI 분석 대상: {len(items_to_analyze)}개 항목")
        
        for analysis_item in items_to_analyze:
            current_item = analysis_item['current_item']
            next_item = analysis_item['next_item']
            
            print(f"\n🔍 [{current_item['title']}] 분석 중...")
            
            has_content = await self.analyze_content_with_ai(
                current_item, next_item, self.markdown_content
            )
            
            current_item['has_content'] = has_content
            status = "✅" if has_content else "❌"
            print(f"{status} [{current_item['title']}] → has_content: {has_content}")
        
        # 3단계: 원본 JSON 업데이트
        self.save_updated_json(json_path)
        
        # 4단계: 콘텐츠 노드 추출 및 저장
        content_nodes = self.extract_content_nodes()
        output_path = self.save_content_nodes_json(content_nodes, output_dir)
        
        print(f"\n=== 콘텐츠 노드 추출 완료: {len(content_nodes)}개 노드 ===")
        return output_path

async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="AI 기반 콘텐츠 노드 추출 및 분석")
    parser.add_argument("json_path", help="JSON 목차 파일 경로")
    parser.add_argument("markdown_path", help="마크다운 문서 파일 경로")
    parser.add_argument("-o", "--output", default=".", help="출력 디렉터리 (기본값: 현재 디렉터리)")
    parser.add_argument("--ai-provider", default="claude", choices=["claude", "gemini"], help="AI 제공자 선택 (기본값: claude)")
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not os.path.exists(args.json_path):
        print(f"JSON 파일을 찾을 수 없습니다: {args.json_path}")
        sys.exit(1)
        
    if not os.path.exists(args.markdown_path):
        print(f"마크다운 파일을 찾을 수 없습니다: {args.markdown_path}")
        sys.exit(1)
    
    # 콘텐츠 노드 추출 실행
    try:
        extractor = ContentNodeExtractor(args.ai_provider)
        output_path = await extractor.process_and_extract(
            args.json_path, 
            args.markdown_path, 
            args.output
        )
        
        if output_path:
            print(f"\n🎉 콘텐츠 노드 추출 완료!")
            print(f"📄 결과 파일: {output_path}")
        else:
            print("\n❌ 콘텐츠 노드 추출 실패")
            sys.exit(1)
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())