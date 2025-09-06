"""
# 목차
- 생성 시간: 2025년 8월 23일 16:03:54 KST
- 핵심 내용: 대화형 학습 시스템으로 1차 질문-답변, 2차 질문 처리, 자동 갭 분석 및 보완 답변 생성을 통합한 완전 자동화 워크플로우
- 상세 내용:
    - InteractiveLearningSystem 클래스 (라인 31-258): 전체 대화형 학습 프로세스를 관리하는 메인 클래스
    - answer_first_question 함수 (라인 36-95): 1차 질문에 대한 답변을 생성하고 파일로 저장하는 함수
    - answer_followup_question 함수 (라인 97-156): 2차 질문에 대한 답변을 생성하는 함수
    - analyze_knowledge_gap 함수 (라인 158-191): 1차, 2차 QA를 바탕으로 갭 분석을 수행하는 함수
    - process_gap_questions 함수 (라인 193-226): 갭 분석 결과로 생성된 질의문을 처리하는 함수
    - run_complete_workflow 함수 (라인 228-258): 전체 워크플로우를 순차 실행하는 함수
    - test_interactive_learning 함수 (라인 260-306): 시스템 전체 테스트 함수
    - 워크플로우 자동화 (라인 228-258): 1차→2차→갭분석→보완답변 자동 연계
    - 파일 기반 결과 저장 (전체): 모든 단계의 결과를 구조화된 파일로 저장
- 상태: active
- 참조: document_based_qa_system_v4.py, knowledge_gap_analyzer_v2.py, question_answering_processor.py 통합
"""

import asyncio
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from claude_code_sdk import ClaudeSDKClient, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

class InteractiveLearningSystem:
    """전체 대화형 학습 프로세스를 관리하는 메인 클래스"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.reference_document = "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref.md"
        
    async def answer_first_question(self, question: str) -> Dict[str, Any]:
        """1차 질문에 대한 답변을 생성하고 파일로 저장하는 함수"""
        
        # 참고 문서 읽기
        if not os.path.exists(self.reference_document):
            return {'status': 'error', 'error': f'참고 문서를 찾을 수 없습니다: {self.reference_document}'}
        
        with open(self.reference_document, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 답변 생성 프롬프트
        prompt = f"""태수야, 다음 질문에 대해 참고 문서를 바탕으로 답변해줘:

**질문:** {question}

**참고 문서:**
{doc_content}

참고 문서의 내용을 바탕으로 질문에 대해 구체적이고 실용적인 답변을 제공해줘.
답변에는 해당 정보가 문서의 어느 부분에서 나왔는지 출처를 명시해주고,
가능하다면 예시나 활용 방법도 포함해줘."""
        
        try:
            async with ClaudeSDKClient() as client:
                await client.query(prompt)
                text_parts = []
                total_cost = 0.0
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                    
                    if type(msg).__name__ == "ResultMessage":
                        total_cost = getattr(msg, 'total_cost_usd', 0.0)
                
                result = {
                    'user_question': question,
                    'model_response': ''.join(text_parts),
                    'reference_document': {
                        'name': 'ref.md',
                        'path': self.reference_document,
                        'content': doc_content
                    },
                    'metadata': {
                        'cost': total_cost,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'success',
                        'type': 'first_answer'
                    }
                }
                
                # 1차 답변 파일로 저장
                first_answer_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/first_answer_{self.session_id}.json"
                with open(first_answer_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                result['saved_file'] = first_answer_file
                return result
                
        except Exception as e:
            return {
                'user_question': question,
                'model_response': '',
                'metadata': {
                    'cost': 0.0,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e),
                    'type': 'first_answer'
                }
            }
    
    async def answer_followup_question(self, second_question: str, first_qa: Dict[str, Any]) -> Dict[str, Any]:
        """2차 질문에 대한 답변을 생성하는 함수"""
        
        with open(self.reference_document, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 2차 답변 생성 프롬프트
        prompt = f"""태수야, 다음 질문에 대해 참고 문서를 바탕으로 답변해줘:

**이전 질문:** {first_qa['user_question']}
**이전 답변:** {first_qa['model_response']}

**현재 질문:** {second_question}

**참고 문서:**
{doc_content}

이전 질문과 답변을 참고하여 현재 질문에 대해 구체적이고 실용적인 답변을 제공해줘.
답변에는 해당 정보가 문서의 어느 부분에서 나왔는지 출처를 명시해주고,
가능하다면 예시나 활용 방법도 포함해줘."""
        
        try:
            async with ClaudeSDKClient() as client:
                await client.query(prompt)
                text_parts = []
                total_cost = 0.0
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                    
                    if type(msg).__name__ == "ResultMessage":
                        total_cost = getattr(msg, 'total_cost_usd', 0.0)
                
                result = {
                    'user_question': second_question,
                    'model_response': ''.join(text_parts),
                    'reference_document': {
                        'name': 'ref.md',
                        'path': self.reference_document,
                        'content': doc_content
                    },
                    'metadata': {
                        'cost': total_cost,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'success',
                        'type': 'second_answer'
                    }
                }
                
                # 2차 답변 파일로 저장
                second_answer_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/second_answer_{self.session_id}.json"
                with open(second_answer_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                result['saved_file'] = second_answer_file
                return result
                
        except Exception as e:
            return {
                'user_question': second_question,
                'model_response': '',
                'metadata': {
                    'cost': 0.0,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e),
                    'type': 'second_answer'
                }
            }
    
    async def analyze_knowledge_gap(self, first_qa: Dict[str, Any], second_question: str) -> Dict[str, Any]:
        """1차, 2차 QA를 바탕으로 갭 분석을 수행하는 함수"""
        
        with open(self.reference_document, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 갭 분석 프롬프트 (knowledge_gap_analyzer_v2.py와 동일한 로직)
        prompt = f"""태수야, 다음 상황을 분석해서 사용자가 여전히 이해하지 못한 부분을 찾고 보완 질의문을 생성해줘:

**이전 사용자 질문:** {first_qa['user_question']}
**이전 AI 응답:** {first_qa['model_response']}
**현재 사용자 질문:** {second_question}

**참고 문서:**
{doc_content}

1단계: 갭 분석 (JSON 형태로)
2단계: 보완 질의문 생성 (JSON 형태로)

다음 형식으로 답변해줘:
```json
{{
  "gap_analysis": {{
    "missing_concepts": ["개념1", "개념2"],
    "unclear_details": ["모호한부분1", "모호한부분2"], 
    "depth_gaps": ["깊이부족영역1", "깊이부족영역2"],
    "practical_gaps": ["실용성부족부분1", "실용성부족부분2"]
  }},
  "followup_questions": [
    {{
      "category": "missing_concepts|unclear_details|depth_gaps|practical_gaps",
      "gap_description": "어떤 갭인지 설명",
      "question": "구체적인 질의문",
      "expected_benefit": "이 질문의 답을 알면 사용자에게 어떤 도움이 되는지"
    }}
  ]
}}
```"""
        
        try:
            async with ClaudeSDKClient() as client:
                await client.query(prompt)
                text_parts = []
                total_cost = 0.0
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                    
                    if type(msg).__name__ == "ResultMessage":
                        total_cost = getattr(msg, 'total_cost_usd', 0.0)
                
                response_text = ''.join(text_parts)
                
                # 갭 분석 파일로 저장
                gap_analysis_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/gap_analysis_{self.session_id}.json"
                gap_result = {
                    'session_id': self.session_id,
                    'first_qa': first_qa,
                    'second_question': second_question,
                    'gap_analysis_response': response_text,
                    'metadata': {
                        'cost': total_cost,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'success'
                    }
                }
                
                with open(gap_analysis_file, 'w', encoding='utf-8') as f:
                    json.dump(gap_result, f, ensure_ascii=False, indent=2)
                
                return {**gap_result, 'saved_file': gap_analysis_file}
                
        except Exception as e:
            return {
                'session_id': self.session_id,
                'gap_analysis_response': '',
                'metadata': {
                    'cost': 0.0,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e)
                }
            }
    
    async def process_gap_questions(self, gap_analysis_response: str) -> Dict[str, Any]:
        """갭 분석 결과로 생성된 질의문을 처리하는 함수"""
        
        # JSON에서 질의문 추출
        try:
            json_match = re.search(r'\{.*\}', gap_analysis_response, re.DOTALL)
            if json_match:
                gap_data = json.loads(json_match.group())
                questions = gap_data.get('followup_questions', [])
            else:
                return {'status': 'error', 'error': '갭 분석 결과에서 질의문을 찾을 수 없습니다.'}
        except Exception as e:
            return {'status': 'error', 'error': f'갭 분석 파싱 오류: {e}'}
        
        with open(self.reference_document, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 각 질의문에 대해 답변 생성
        answers = []
        for i, question_data in enumerate(questions):
            prompt = f"""태수야, 다음 질문에 대해 참고 문서를 바탕으로 구체적이고 실용적인 답변을 해줘:

**질문:** {question_data.get('question', '')}
**카테고리:** {question_data.get('category', '')}
**갭 설명:** {question_data.get('gap_description', '')}

**참고 문서:**
{doc_content}

참고 문서에서 관련 정보를 찾아서 구체적이고 실용적인 답변을 제공해줘."""
            
            try:
                async with ClaudeSDKClient() as client:
                    await client.query(prompt)
                    text_parts = []
                    total_cost = 0.0
                    
                    async for msg in client.receive_response():
                        if hasattr(msg, 'content'):
                            for block in msg.content:
                                if hasattr(block, 'text'):
                                    text_parts.append(block.text)
                        
                        if type(msg).__name__ == "ResultMessage":
                            total_cost = getattr(msg, 'total_cost_usd', 0.0)
                    
                    answer_result = {
                        'question_index': i,
                        'original_question': question_data,
                        'answer': ''.join(text_parts),
                        'metadata': {
                            'cost': total_cost,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'success'
                        }
                    }
                    
                    # 개별 답변 파일로 저장
                    answer_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/gap_answer_{self.session_id}_q{i:02d}.json"
                    with open(answer_file, 'w', encoding='utf-8') as f:
                        json.dump(answer_result, f, ensure_ascii=False, indent=2)
                    
                    answer_result['saved_file'] = answer_file
                    answers.append(answer_result)
                    
            except Exception as e:
                answers.append({
                    'question_index': i,
                    'original_question': question_data,
                    'answer': '',
                    'metadata': {
                        'cost': 0.0,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'error',
                        'error': str(e)
                    }
                })
        
        return {
            'status': 'success',
            'answers': answers,
            'total_questions': len(questions)
        }
    
    async def run_complete_workflow(self, first_question: str, second_question: str) -> Dict[str, Any]:
        """전체 워크플로우를 순차 실행하는 함수"""
        
        print(f"🚀 대화형 학습 시스템 시작 (세션 ID: {self.session_id})")
        print("="*70)
        
        # 1단계: 1차 질문 답변
        print("1️⃣ 1차 질문 처리 중...")
        first_result = await self.answer_first_question(first_question)
        if first_result['metadata']['status'] != 'success':
            return {'status': 'error', 'step': '1차 질문', 'error': first_result}
        print(f"   ✅ 완료 - 저장: {os.path.basename(first_result['saved_file'])}")
        
        # 2단계: 2차 질문 답변
        print("2️⃣ 2차 질문 처리 중...")
        second_result = await self.answer_followup_question(second_question, first_result)
        if second_result['metadata']['status'] != 'success':
            return {'status': 'error', 'step': '2차 질문', 'error': second_result}
        print(f"   ✅ 완료 - 저장: {os.path.basename(second_result['saved_file'])}")
        
        # 3단계: 갭 분석
        print("3️⃣ 지식 갭 분석 중...")
        gap_result = await self.analyze_knowledge_gap(first_result, second_question)
        if gap_result['metadata']['status'] != 'success':
            return {'status': 'error', 'step': '갭 분석', 'error': gap_result}
        print(f"   ✅ 완료 - 저장: {os.path.basename(gap_result['saved_file'])}")
        
        # 4단계: 갭 기반 보완 답변 생성
        print("4️⃣ 보완 답변 생성 중...")
        gap_answers = await self.process_gap_questions(gap_result['gap_analysis_response'])
        if gap_answers['status'] != 'success':
            return {'status': 'error', 'step': '보완 답변', 'error': gap_answers}
        print(f"   ✅ 완료 - {gap_answers['total_questions']}개 답변 생성")
        
        return {
            'status': 'success',
            'session_id': self.session_id,
            'first_result': first_result,
            'second_result': second_result,
            'gap_analysis': gap_result,
            'gap_answers': gap_answers,
            'summary': {
                'total_cost': (first_result['metadata']['cost'] + 
                             second_result['metadata']['cost'] + 
                             gap_result['metadata']['cost'] +
                             sum(a['metadata']['cost'] for a in gap_answers['answers'])),
                'completion_time': datetime.now().isoformat()
            }
        }

async def test_interactive_learning():
    """시스템 전체 테스트 함수"""
    print("=== Interactive Learning System 테스트 시작 ===\n")
    
    # 테스트 질문들
    first_question = "DOP의 핵심이 뭐야?"
    second_question = "왜 데이터를 수정하지 않고 새로운 데이터를 만드는 거야?"
    
    system = InteractiveLearningSystem()
    
    try:
        result = await system.run_complete_workflow(first_question, second_question)
        
        if result['status'] == 'success':
            print("\n🎉 전체 워크플로우 완료!")
            print(f"💰 총 비용: ${result['summary']['total_cost']:.4f}")
            print(f"⏰ 완료 시간: {result['summary']['completion_time']}")
            print(f"📁 세션 ID: {result['session_id']}")
            
            print(f"\n📋 생성된 파일들:")
            print(f"  - 1차 답변: {os.path.basename(result['first_result']['saved_file'])}")
            print(f"  - 2차 답변: {os.path.basename(result['second_result']['saved_file'])}")
            print(f"  - 갭 분석: {os.path.basename(result['gap_analysis']['saved_file'])}")
            print(f"  - 보완 답변: {result['gap_answers']['total_questions']}개 파일")
        else:
            print(f"❌ 워크플로우 실패 ({result['step']}): {result['error']}")
        
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_interactive_learning())