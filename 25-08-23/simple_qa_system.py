"""
# 목차
- 생성 시간: 2025년 8월 23일 16:15:21 KST
- 핵심 내용: 단순한 프롬프트 방식으로 사용자 미이해 부분을 분석하고 답변에 포함시키는 시스템 (복잡한 갭 분석 시스템과 비교용)
- 상세 내용:
    - SimpleQASystem 클래스 (라인 31-159): 단순 프롬프트 기반 질의응답 시스템
    - answer_first_question 함수 (라인 36-95): 1차 질문에 대한 기본 답변을 생성하고 저장하는 함수
    - answer_with_gap_analysis 함수 (라인 97-159): 2차 질문 시 미이해 부분을 프롬프트로 분석하고 포함하여 답변하는 함수
    - test_simple_qa_system 함수 (라인 161-207): 시스템 테스트 함수
    - 단순 갭 분석 로직 (라인 123-159): 별도 시스템 없이 프롬프트 내에서 미이해 부분 분석
    - 파일 저장 기능 (라인 84-95, 150-159): 각 답변을 개별 JSON 파일로 저장
- 상태: active  
- 참조: interactive_learning_system.py와 비교하기 위한 단순화된 버전
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from claude_code_sdk import ClaudeSDKClient, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

class SimpleQASystem:
    """단순 프롬프트 기반 질의응답 시스템"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.reference_document = "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref.md"
        
    async def answer_first_question(self, question: str) -> Dict[str, Any]:
        """1차 질문에 대한 기본 답변을 생성하고 저장하는 함수"""
        
        # 참고 문서 읽기
        if not os.path.exists(self.reference_document):
            return {'status': 'error', 'error': f'참고 문서를 찾을 수 없습니다: {self.reference_document}'}
        
        with open(self.reference_document, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 기본 답변 생성 프롬프트
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
                        'method': 'simple_first_answer'
                    }
                }
                
                # 1차 답변 파일로 저장
                first_answer_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/simple_first_answer_{self.session_id}.json"
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
                    'method': 'simple_first_answer'
                }
            }
    
    async def answer_with_gap_analysis(self, second_question: str, first_qa: Dict[str, Any]) -> Dict[str, Any]:
        """2차 질문 시 미이해 부분을 프롬프트로 분석하고 포함하여 답변하는 함수"""
        
        with open(self.reference_document, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 네가 제시한 프롬프트 사용
        prompt = f"""문서를 바탕으로 답변해줘. 답변 시 직전 사용자 질문과 모델의 응답, 그리고 현재 사용자 질문을 바탕으로 현재 사용자가 충분히 이해하지 못한 내용을 분석하여 현재 질문에 대한 응답 작성 시 해당 내용에 대한 정보도 제공해줘.

**직전 사용자 질문:** {first_qa['user_question']}

**직전 모델 응답:** {first_qa['model_response']}

**현재 사용자 질문:** {second_question}

**참고 문서:**
{doc_content}

위 내용을 바탕으로:
1. 현재 사용자가 충분히 이해하지 못한 내용을 분석하여
2. 현재 질문에 대한 답변과 함께
3. 미이해 부분에 대한 추가 정보도 함께 제공해줘.

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
                    'first_qa_context': first_qa,
                    'reference_document': {
                        'name': 'ref.md',
                        'path': self.reference_document,
                        'content': doc_content
                    },
                    'metadata': {
                        'cost': total_cost,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'success',
                        'method': 'simple_with_gap_analysis'
                    }
                }
                
                # 2차 답변 파일로 저장
                second_answer_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/simple_second_answer_{self.session_id}.json"
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
                    'method': 'simple_with_gap_analysis'
                }
            }

async def test_simple_qa_system():
    """시스템 테스트 함수"""
    print("=== Simple QA System (프롬프트 방식) 테스트 시작 ===\n")
    
    # 테스트 질문들
    first_question = "DOP의 핵심이 뭐야?"
    second_question = "왜 데이터를 수정하지 않고 새로운 데이터를 만드는 거야?"
    
    system = SimpleQASystem()
    
    try:
        print(f"🚀 단순 QA 시스템 시작 (세션 ID: {system.session_id})")
        print("="*70)
        
        # 1단계: 1차 질문 답변
        print("1️⃣ 1차 질문 처리 중...")
        first_result = await system.answer_first_question(first_question)
        if first_result['metadata']['status'] != 'success':
            print(f"❌ 1차 질문 실패: {first_result}")
            return
        print(f"   ✅ 완료 - 저장: {os.path.basename(first_result['saved_file'])}")
        
        # 2단계: 2차 질문 답변 (미이해 부분 분석 포함)
        print("2️⃣ 2차 질문 처리 중 (미이해 부분 분석 포함)...")
        second_result = await system.answer_with_gap_analysis(second_question, first_result)
        if second_result['metadata']['status'] != 'success':
            print(f"❌ 2차 질문 실패: {second_result}")
            return
        print(f"   ✅ 완료 - 저장: {os.path.basename(second_result['saved_file'])}")
        
        # 결과 요약
        total_cost = first_result['metadata']['cost'] + second_result['metadata']['cost']
        
        print("\n🎉 단순 QA 시스템 완료!")
        print(f"💰 총 비용: ${total_cost:.4f}")
        print(f"⏰ 완료 시간: {datetime.now().isoformat()}")
        print(f"📁 세션 ID: {system.session_id}")
        
        print(f"\n📋 생성된 파일들:")
        print(f"  - 1차 답변: {os.path.basename(first_result['saved_file'])}")
        print(f"  - 2차 답변 (갭 분석 포함): {os.path.basename(second_result['saved_file'])}")
        
        print(f"\n📊 비교를 위해 복잡한 갭 분석 시스템과 결과를 비교해보세요!")
        
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_qa_system())