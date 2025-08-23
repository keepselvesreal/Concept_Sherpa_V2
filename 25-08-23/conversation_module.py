"""
# 목차
- 생성 시간: 2025년 8월 23일 16:54:09 KST
- 핵심 내용: 프롬프트, 질의, 파일 경로를 입력받아 Claude SDK로 문서 기반 답변을 생성하고 JSON 문자열로 반환하는 대화 모듈
- 상세 내용:
    - ConversationModule 클래스 (라인 25-132): 문서 기반 대화 처리를 담당하는 메인 클래스
    - _load_document_content 함수 (라인 30-43): 파일 경로에서 문서 내용을 로드하는 함수
    - _call_claude_api 함수 (라인 45-79): Claude SDK를 통해 API 호출하고 응답을 받는 비동기 함수
    - _save_result 함수 (라인 96-124): 결과를 JSON 파일로 저장하는 함수 (연속 대화 지원)
    - process_query 함수 (라인 126-162): 메인 처리 함수로 전체 플로우를 관리하고 JSON 문자열 반환
    - 오류 처리 로직 (라인 35-43, 82-94): 파일 없음, API 호출 실패 등의 오류 상황 처리
    - 타임스탬프 기록 (라인 153-162): 소요 시간 계산 기능
    - 연속 대화 지원 (라인 101-116): 같은 세션 내에서 대화 배열로 누적 저장
- 상태: active
- 참조: document_based_qa_system_v4.py, simple_qa_system.py에서 Claude SDK 연결 및 파일 처리 로직 참조
"""

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from claude_code_sdk import ClaudeSDKClient, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

class ConversationModule:
    """문서 기반 대화 처리를 담당하는 메인 클래스"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def _load_document_content(self, file_path: str) -> Dict[str, Any]:
        """파일 경로에서 문서 내용을 로드하는 함수"""
        try:
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f'파일을 찾을 수 없습니다: {file_path}',
                    'content': None
                }
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'file_name': os.path.basename(file_path)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'파일 읽기 오류: {str(e)}',
                'content': None
            }
    
    async def _call_claude_api(self, enhanced_prompt: str) -> Dict[str, Any]:
        """Claude SDK를 통해 API 호출하고 응답을 받는 비동기 함수"""
        try:
            async with ClaudeSDKClient() as client:
                await client.query(enhanced_prompt)
                text_parts = []
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                
                return {
                    'success': True,
                    'response': ''.join(text_parts)
                }
                
        except CLINotFoundError:
            return {
                'success': False,
                'error': 'Claude CLI가 설치되지 않았습니다. 설치 명령어: npm install -g @anthropic-ai/claude-code'
            }
        except ProcessError as e:
            return {
                'success': False,
                'error': f'Claude API 호출 오류: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'예상치 못한 오류: {str(e)}'
            }
    
    def _save_result(self, result_data: Dict[str, Any]) -> str:
        """결과를 JSON 파일로 저장하는 함수 (연속 대화 지원)"""
        try:
            filename = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/conversation_{self.session_id}.json"
            
            # 기존 대화 파일이 있는지 확인
            conversations = []
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    conversations = existing_data.get('conversations', [])
            
            # 새로운 대화 추가
            conversations.append(result_data)
            
            # 세션 정보와 함께 저장
            session_data = {
                'session_id': self.session_id,
                'total_conversations': len(conversations),
                'conversations': conversations
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            return filename
        except Exception as e:
            print(f"결과 저장 실패: {e}")
            return ""
    
    async def process_query(self, prompt: str, query: str, file_path: str) -> str:
        """메인 처리 함수로 전체 플로우를 관리하고 JSON 문자열 반환"""
        start_time = time.time()
        
        # 1. 문서 내용 로드
        doc_result = self._load_document_content(file_path)
        
        if not doc_result['success']:
            error_result = {
                'query': query,
                'model_response': '',
                'elapsed_time': 0.0
            }
            self._save_result(error_result)
            return json.dumps(error_result, ensure_ascii=False)
        
        # 2. 프롬프트 생성 (참고 문서 포함)
        enhanced_prompt = f"""{prompt}
        
참고 문서 (파일: {doc_result['file_name']}):
{doc_result['content']}

질의: {query}"""
        
        # 3. Claude API 호출
        api_result = await self._call_claude_api(enhanced_prompt)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 4. 결과 구성
        result_data = {
            'query': query,
            'model_response': api_result['response'] if api_result['success'] else '',
            'elapsed_time': round(elapsed_time, 2)
        }
        
        # 5. JSON 파일 저장
        self._save_result(result_data)
        
        # 6. JSON 문자열 반환
        return json.dumps(result_data, ensure_ascii=False)