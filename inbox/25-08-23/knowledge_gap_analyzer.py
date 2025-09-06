"""
# 목차
- 생성 시간: 2025년 8월 23일 15:37:59 KST
- 핵심 내용: 이전 질문-답변과 현재 질문을 분석해 사용자 미이해 부분을 도출하고 보완 질의문을 생성하는 시스템
- 상세 내용:
    - KnowledgeGapAnalyzer 클래스 (라인 31-158): 사용자 이해도 분석 및 질의문 생성을 담당하는 메인 클래스
    - analyze_knowledge_gap 함수 (라인 36-87): 이전 QA와 현재 질문을 비교해 미이해 부분을 분석하는 비동기 함수
    - generate_followup_questions 함수 (라인 89-141): 미이해 부분에 대한 보완 질의문을 생성하는 비동기 함수
    - process_gap_analysis 함수 (라인 143-158): 전체 갭 분석 프로세스를 관리하는 함수
    - test_knowledge_gap_analyzer 함수 (라인 160-224): 시스템 테스트 함수
    - 갭 분석 로직 (라인 56-87): 이전 응답과 현재 질문의 차이점을 Claude로 분석
    - 질의문 생성 로직 (라인 109-141): 미이해 부분을 구체적 질문으로 변환
- 상태: active
- 참조: document_based_qa_system_v4.py의 구조를 참고하여 갭 분석 전용으로 설계
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

class KnowledgeGapAnalyzer:
    """사용자 이해도 분석 및 질의문 생성을 담당하는 메인 클래스"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    async def analyze_knowledge_gap(self, previous_qa: Dict[str, str], 
                                  current_question: str, 
                                  reference_documents: List[str]) -> Dict[str, Any]:
        """이전 QA와 현재 질문을 비교해 미이해 부분을 분석하는 비동기 함수"""
        
        # 참고 문서 내용 로드
        doc_contents = []
        for doc_path in reference_documents:
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    doc_name = os.path.basename(doc_path)
                    doc_contents.append(f"=== {doc_name} ===\n{f.read()}")
        
        reference_text = "\n\n".join(doc_contents)
        
        # 갭 분석 프롬프트
        prompt = f"""태수야, 다음 상황을 분석해서 사용자가 여전히 이해하지 못한 부분을 찾아줘:

**이전 사용자 질문:** {previous_qa.get('user_question', '없음')}

**이전 AI 응답:** {previous_qa.get('model_response', '없음')}

**현재 사용자 질문:** {current_question}

**참고 문서:**
{reference_text}

이전 응답을 받고도 사용자가 추가로 질문한다는 건, 뭔가 충분히 이해하지 못했거나 더 구체적인 정보가 필요하다는 뜻이야.

다음 사항들을 분석해서 JSON 형태로 답변해줘:

1. **missing_concepts**: 이전 응답에서 언급되지 않았지만 현재 질문과 관련된 중요한 개념들
2. **unclear_details**: 이전 응답에서 추상적으로만 언급되어 구체적 설명이 부족한 부분들  
3. **depth_gaps**: 이전 응답이 표면적이어서 더 깊은 이해가 필요한 영역들
4. **practical_gaps**: 이론적 설명은 있었지만 실제 활용법이나 예시가 부족한 부분들

JSON 형식:
{{
  "missing_concepts": ["개념1", "개념2", ...],
  "unclear_details": ["모호한부분1", "모호한부분2", ...], 
  "depth_gaps": ["깊이부족영역1", "깊이부족영역2", ...],
  "practical_gaps": ["실용성부족부분1", "실용성부족부분2", ...]
}}"""
        
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
                
                return {
                    'gap_analysis': response_text,
                    'cost': total_cost,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success'
                }
                
        except Exception as e:
            return {
                'gap_analysis': '',
                'cost': 0.0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def generate_followup_questions(self, gap_analysis: str, 
                                        reference_documents: List[str]) -> Dict[str, Any]:
        """미이해 부분에 대한 보완 질의문을 생성하는 비동기 함수"""
        
        # 참고 문서 내용 로드 
        doc_contents = []
        for doc_path in reference_documents:
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    doc_name = os.path.basename(doc_path)
                    doc_contents.append(f"=== {doc_name} ===\n{f.read()}")
        
        reference_text = "\n\n".join(doc_contents)
        
        # 질의문 생성 프롬프트
        prompt = f"""태수야, 다음 갭 분석 결과를 바탕으로 사용자 이해도를 높일 수 있는 구체적인 질의문들을 생성해줘:

**갭 분석 결과:**
{gap_analysis}

**참고 문서:**
{reference_text}

각 갭 유형별로 참고 문서에서 답을 찾을 수 있는 구체적이고 실용적인 질의문들을 생성해줘. 
질의문은 AI가 문서를 검색해서 명확하고 도움이 되는 답변을 제공할 수 있도록 구체적이어야 해.

JSON 형식으로 답변해줘:
{{
  "followup_questions": [
    {{
      "category": "missing_concepts|unclear_details|depth_gaps|practical_gaps",
      "gap_description": "어떤 갭인지 설명",
      "question": "구체적인 질의문",
      "expected_benefit": "이 질문의 답을 알면 사용자에게 어떤 도움이 되는지"
    }},
    ...
  ]
}}"""
        
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
                
                return {
                    'followup_questions': response_text,
                    'cost': total_cost,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success'
                }
                
        except Exception as e:
            return {
                'followup_questions': '',
                'cost': 0.0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def process_gap_analysis(self, previous_qa: Dict[str, str], 
                                 current_question: str,
                                 reference_documents: List[str]) -> Dict[str, Any]:
        """전체 갭 분석 프로세스를 관리하는 함수"""
        
        # 1. 갭 분석
        gap_result = await self.analyze_knowledge_gap(previous_qa, current_question, reference_documents)
        
        if gap_result['status'] != 'success':
            return gap_result
        
        # 2. 질의문 생성
        questions_result = await self.generate_followup_questions(
            gap_result['gap_analysis'], reference_documents
        )
        
        return {
            'gap_analysis': gap_result,
            'followup_questions': questions_result,
            'total_cost': gap_result['cost'] + questions_result['cost'],
            'session_id': self.session_id
        }

async def test_knowledge_gap_analyzer():
    """시스템 테스트 함수"""
    print("=== Knowledge Gap Analyzer 테스트 시작 ===\n")
    
    # 테스트 데이터 준비
    previous_qa = {
        'user_question': 'Claude Code의 핵심 특징은 무엇인가요?',
        'model_response': '''Claude Code의 핵심 특징들을 정리해보면 이런 거야:

## 주요 핵심 특징

**1. 멀티-클로딩 (Multi-Clauding)**
- 개발자들이 동시에 6개의 Claude 세션을 실행하는 패턴이 일반화됨
- 각 세션을 다른 목적으로 특화: 질문 전용, 코드 편집 전용 등으로 역할 분담

**2. CLAUDE.md 파일 중심의 커스터마이징**
- 코드 아키텍처, 주의사항, 모범 사례를 기록하는 핵심 파일
- 여기에 투자하면 출력 품질이 극적으로 향상됨'''
    }
    
    current_question = "멀티-클로딩을 실제로 어떻게 활용하는지 구체적인 사례가 알고 싶어"
    
    reference_documents = [
        "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref1.md",
        "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref2.md"
    ]
    
    analyzer = KnowledgeGapAnalyzer()
    
    try:
        print(f"🔍 이전 질문: {previous_qa['user_question']}")
        print(f"🤔 현재 질문: {current_question}")
        print(f"📚 참고 문서: {len(reference_documents)}개")
        print(f"🆔 세션 ID: {analyzer.session_id}")
        print("="*70)
        
        # 갭 분석 실행
        result = await analyzer.process_gap_analysis(previous_qa, current_question, reference_documents)
        
        print("📋 갭 분석 결과:")
        print(result['gap_analysis']['gap_analysis'])
        print("\n" + "="*50 + "\n")
        
        print("❓ 생성된 보완 질의문:")
        print(result['followup_questions']['followup_questions'])
        print("\n" + "="*50 + "\n")
        
        print(f"💰 총 비용: ${result['total_cost']:.4f}")
        print(f"⏰ 완료 시간: {datetime.now().isoformat()}")
        
        # 결과 저장
        results_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/gap_analysis_{analyzer.session_id}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📁 결과 저장: {os.path.basename(results_file)}")
        
    except CLINotFoundError:
        print("❌ Claude CLI가 설치되지 않았습니다.")
        print("설치 명령어: npm install -g @anthropic-ai/claude-code")
    except ProcessError as e:
        print(f"❌ 프로세스 실행 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_knowledge_gap_analyzer())