"""
# 목차
- 생성 시간: 2025년 08월 23일 23:51:53 KST
- 핵심 내용: 세션의 직전 질문/응답과 현재 질문을 분석해 사용자 이해 부족 부분을 파악하고 보완 질의문을 생성하는 모듈 (실행 가능한 메인 함수 포함)
- 상세 내용:
    - UnderstandingDeficiencyAnalyzer 클래스 (라인 26-155): 사용자 이해 부족 분석 및 질의문 생성을 담당하는 메인 클래스
    - _extract_previous_conversation 함수 (라인 35-69): 세션 JSON에서 직전 대화를 추출하는 함수
    - _analyze_understanding 함수 (라인 71-125): 통합된 이해 부족 분석 함수 (참고문서 여부에 따라 내부 분기)
    - _save_result 함수 (라인 127-139): 분석 결과를 JSON 파일로 저장하는 함수
    - analyze_understanding_deficiency 함수 (라인 141-185): 메인 분석 함수 (프롬프트 인자 추가)
    - main 함수 (라인 188-209): 실행 가능한 메인 함수
- 상태: active
- 참조: understanding_deficiency_analyzer.py에서 메인 실행부 추가한 버전
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

class UnderstandingDeficiencyAnalyzer:
    """사용자 이해 부족 분석 및 질의문 생성을 담당하는 메인 클래스"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def _extract_previous_conversation(self, session_file: str) -> Dict[str, Any]:
        """세션 JSON에서 직전 대화를 추출하는 함수"""
        try:
            if not os.path.exists(session_file):
                return {
                    'success': False,
                    'error': f'세션 파일을 찾을 수 없습니다: {session_file}'
                }
            
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            conversations = session_data.get('conversations', [])
            if len(conversations) < 2:
                return {
                    'success': False,
                    'error': '직전 대화가 없습니다. 최소 2개의 대화가 필요합니다.'
                }
            
            # 마지막 대화가 현재, 마지막에서 두번째가 직전
            previous_conv = conversations[-2]
            current_conv = conversations[-1]
            
            return {
                'success': True,
                'previous_question': previous_conv.get('query', ''),
                'previous_answer': previous_conv.get('model_response', ''),
                'current_question': current_conv.get('query', '')
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'세션 데이터 추출 오류: {str(e)}'
            }
    
    async def _analyze_understanding(self, prompt: str, prev_q: str, prev_a: str, curr_q: str, file_path: Optional[str]) -> Dict[str, Any]:
        """통합된 이해 부족 분석 함수 (참고문서 여부에 따라 내부 분기)"""
        
        # 참고문서가 있는 경우 문서 내용 포함
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    doc_content = f.read()
                
                full_prompt = f"""{prompt}

**이전 질문:** {prev_q}

**이전 답변:** {prev_a}

**현재 질문:** {curr_q}

**참고 문서:**
{doc_content}"""
            
            except Exception as e:
                return {
                    'success': False,
                    'error': f'참고문서 읽기 오류: {str(e)}'
                }
        else:
            # 대화만으로 분석
            full_prompt = f"""{prompt}

**이전 질문:** {prev_q}

**이전 답변:** {prev_a}

**현재 질문:** {curr_q}"""
        
        try:
            async with ClaudeSDKClient() as client:
                await client.query(full_prompt)
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
        except Exception as e:
            return {
                'success': False,
                'error': f'Claude API 호출 오류: {str(e)}'
            }
    
    def _save_result(self, result_data: Dict[str, Any]) -> str:
        """분석 결과를 JSON 파일로 저장하는 함수"""
        try:
            filename = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/understanding_analysis_{self.session_id}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            return filename
        except Exception as e:
            print(f"결과 저장 실패: {e}")
            return ""
    
    async def analyze_understanding_deficiency(self, prompt: str, session_file: str, current_question: str, file_path: Optional[str] = None) -> str:
        """메인 분석 함수 - 프롬프트를 인자로 받아 일반적 사용 가능 - JSON 문자열 반환"""
        start_time = time.time()
        
        # 1. 세션에서 직전 대화 추출
        conv_result = self._extract_previous_conversation(session_file)
        
        if not conv_result['success']:
            error_result = {
                'previous_question': '',
                'previous_answer': '',
                'current_question': current_question,
                'understanding_deficiencies': [],
                'error': conv_result['error']
            }
            self._save_result(error_result)
            return json.dumps(error_result, ensure_ascii=False)
        
        # 2. 분석 실행 (file_path 여부에 따라 내부 분기)
        analysis_result = await self._analyze_understanding(
            prompt,
            conv_result['previous_question'],
            conv_result['previous_answer'],
            current_question,
            file_path
        )
        
        # 3. 결과 구성
        if analysis_result['success']:
            result_data = {
                'previous_question': conv_result['previous_question'],
                'previous_answer': conv_result['previous_answer'],
                'current_question': current_question,
                'analysis_response': analysis_result['response']
            }
        else:
            result_data = {
                'previous_question': conv_result['previous_question'],
                'previous_answer': conv_result['previous_answer'],
                'current_question': current_question,
                'understanding_deficiencies': [],
                'error': analysis_result['error']
            }
        
        # 4. 저장 및 반환
        saved_file = self._save_result(result_data)
        print(f"분석 결과가 저장되었습니다: {saved_file}")
        return json.dumps(result_data, ensure_ascii=False)

# 메인 실행부
if __name__ == "__main__":
    async def main():
        analyzer = UnderstandingDeficiencyAnalyzer()
        
        # 프롬프트 파일 읽기
        with open('/home/nadle/projects/Concept_Sherpa_V2/25-08-23/understanding_analysis_prompt.txt', 'r', encoding='utf-8') as f:
            prompt = f.read()
        
        # 분석 실행
        result = await analyzer.analyze_understanding_deficiency(
            prompt=prompt,
            session_file='/home/nadle/projects/Concept_Sherpa_V2/25-08-23/conversation_20250823_172759.json',
            current_question='왜 데이터를 수정하지 않고 새로운 데이터를 만드는 거야?',
            file_path='/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref.md'
        )
        
        print("분석 완료!")
        print("결과:", result)
    
    asyncio.run(main())