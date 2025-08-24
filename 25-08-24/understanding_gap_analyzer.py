"""
# 목차
- 생성 시간: 2025년 8월 24일 23:38:12 KST
- 핵심 내용: 사용자의 이해 부족 부분을 분석하고 보완 질의를 생성하여 참고문헌 기반 답변을 제공하는 시스템
- 상세 내용:
    - UnderstandingGapAnalyzer 클래스 (라인 28-177): 메인 클래스로 이해 부족 분석 및 질의 생성을 담당
    - analyze_understanding_gap 함수 (라인 34-67): 이해 부족 분석 후 질의 생성하는 함수
    - generate_supplementary_answer 함수 (라인 69-103): 생성된 질의로 참고문헌 기반 답변 생성
    - process_complete_analysis 함수 (라인 105-177): 전체 분석 프로세스를 수행하고 결과를 저장하는 메인 함수
    - test_understanding_gap_analysis 함수 (라인 179-213): 테스트 실행 함수
- 상태: active
- 주소: understanding_gap_analyzer
- 참조: understanding_deficiency_analyzer_v2.py의 분석 패턴과 document_query_processor.py의 Claude SDK 호출 패턴 결합
"""

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List

try:
    from claude_code_sdk import ClaudeSDKClient, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

class UnderstandingGapAnalyzer:
    """사용자의 이해 부족 부분을 분석하고 보완 질의를 생성하여 참고문헌 기반 답변을 제공하는 시스템"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.work_dir = "/home/nadle/projects/Concept_Sherpa_V2/25-08-24"
        self.query_count = 0
    
    async def analyze_understanding_gap(self, previous_query: str, previous_answer: str, current_query: str) -> Dict[str, Any]:
        """이해 부족 분석 후 질의 생성하는 함수"""
        try:
            analysis_prompt = """다음 대화를 분석하여 사용자가 이해하지 못한 부분을 파악하고, 이를 보완할 수 있는 구체적인 질의를 생성해주세요.

이전 질의: {previous_query}
이전 답변: {previous_answer}
현재 질의: {current_query}

분석 결과를 다음 JSON 형식으로 정확히 반환해주세요:
{{
    "analysis": "사용자가 이해하지 못한 부분에 대한 상세한 분석",
    "generated_query": "이해 부족 부분을 보완하기 위한 구체적인 질의문"
}}""".format(
                previous_query=previous_query,
                previous_answer=previous_answer, 
                current_query=current_query
            )

            async with ClaudeSDKClient() as client:
                await client.query(analysis_prompt)
                text_parts = []
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                
                response_text = ''.join(text_parts)
                
                # JSON 응답 파싱 시도
                try:
                    result = json.loads(response_text)
                    return {
                        'success': True,
                        'analysis': result.get('analysis', ''),
                        'generated_query': result.get('generated_query', '')
                    }
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'analysis': response_text,
                        'generated_query': f"{current_query}에 대한 보완 설명을 더 상세히 해주세요."
                    }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': '',
                'generated_query': ''
            }
    
    async def generate_supplementary_answer(self, generated_query: str, document_content: str) -> Dict[str, Any]:
        """생성된 질의로 참고문헌 기반 답변 생성"""
        try:
            answer_prompt = f"""다음 참고 문서를 바탕으로 질의에 대해 정확하고 상세하게 답변해주세요.

참고 문서:
{document_content}

질의: {generated_query}"""

            async with ClaudeSDKClient() as client:
                await client.query(answer_prompt)
                text_parts = []
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                
                return {
                    'success': True,
                    'answer': ''.join(text_parts)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'answer': ''
            }
    
    async def process_complete_analysis(self, previous_query: str, previous_answer: str, current_query: str, 
                                      document_list: List[str], document_paths: List[str] = None) -> Dict[str, Any]:
        """전체 분석 프로세스를 수행하고 결과를 저장하는 메인 함수"""
        self.query_count += 1
        start_time = time.time()
        
        # 1. 이해 부족 분석 및 질의 생성
        gap_analysis = await self.analyze_understanding_gap(previous_query, previous_answer, current_query)
        
        if not gap_analysis['success']:
            error_result = {
                'session_id': self.session_id,
                'previous_query': previous_query,
                'previous_answer': previous_answer,
                'query_id': self.query_count,
                'current_query': current_query,
                'understanding_gap': '',
                'generated_query': '',
                'supplementary_answer': '',
                'timestamp': datetime.now().isoformat(),
                'document_paths': document_paths or [f"document_{i}" for i in range(len(document_list))],
                'success': False,
                'error': gap_analysis['error'],
                'elapsed_time': round(time.time() - start_time, 2)
            }
            
            # JSON 파일 저장
            saved_file = self._save_analysis_result(error_result)
            error_result['saved_file'] = saved_file
            return error_result
        
        # 2. 생성된 질의로 참고문헌 기반 답변 생성
        combined_documents = "\n\n=== 문서 구분선 ===\n\n".join(document_list)
        answer_result = await self.generate_supplementary_answer(gap_analysis['generated_query'], combined_documents)
        
        elapsed_time = round(time.time() - start_time, 2)
        
        # 3. 최종 결과 구성
        final_result = {
            'session_id': self.session_id,
            'previous_query': previous_query,
            'previous_answer': previous_answer,
            'query_id': self.query_count,
            'current_query': current_query,
            'understanding_gap': gap_analysis['analysis'],
            'generated_query': gap_analysis['generated_query'],
            'supplementary_answer': answer_result['answer'] if answer_result['success'] else '',
            'timestamp': datetime.now().isoformat(),
            'document_paths': document_paths or [f"document_{i}" for i in range(len(document_list))],
            'success': answer_result['success'],
            'elapsed_time': elapsed_time
        }
        
        if not answer_result['success']:
            final_result['error'] = answer_result['error']
        
        # 4. JSON 파일 저장
        saved_file = self._save_analysis_result(final_result)
        final_result['saved_file'] = saved_file
        
        return final_result
    
    def _save_analysis_result(self, result_data: Dict[str, Any]) -> str:
        """분석 결과를 JSON 파일로 저장"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.work_dir}/understanding_gap_analysis_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            return filename
        except Exception as e:
            print(f"결과 저장 실패: {e}")
            return ""

async def test_understanding_gap_analysis():
    """테스트 실행 함수"""
    analyzer = UnderstandingGapAnalyzer()
    
    # DOP.md 파일 읽기
    dop_file_path = "/home/nadle/projects/Concept_Sherpa_V2/25-08-24/DOP.md"
    
    with open(dop_file_path, 'r', encoding='utf-8') as f:
        dop_content = f.read()
    
    # 테스트 데이터
    previous_query = "데이터 지향 프로그래밍의 핵심 원리가 뭐야?"
    previous_answer = "데이터 지향 프로그래밍의 핵심 원리는 1) 데이터 우선 설계, 2) 불변성, 3) 데이터와 로직 분리입니다."
    current_query = "불변성이 왜 중요한지 잘 모르겠어. 그냥 데이터 바꾸면 안 되나?"
    
    print("=== 이해 부족 분석 및 보완 답변 생성 테스트 ===\n")
    print(f"이전 질의: {previous_query}")
    print(f"이전 답변: {previous_answer}")
    print(f"현재 질의: {current_query}\n")
    
    try:
        result = await analyzer.process_complete_analysis(
            previous_query=previous_query,
            previous_answer=previous_answer,
            current_query=current_query,
            document_list=[dop_content],
            document_paths=[dop_file_path]
        )
        
        print("분석 완료!")
        print(f"성공 여부: {result['success']}")
        print(f"소요 시간: {result['elapsed_time']}초")
        print(f"세션 ID: {result['session_id']}")
        print(f"질의 ID: {result['query_id']}")
        print(f"저장된 파일: {result['saved_file']}")
        print(f"\n이해 부족 분석: {result['understanding_gap'][:100]}...")
        print(f"생성된 질의: {result['generated_query']}")
        
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_understanding_gap_analysis())