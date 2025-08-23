"""
# 목차
- 생성 시간: 2025년 8월 23일 15:47:21 KST
- 핵심 내용: 저장된 질의문 JSON 파일을 읽어서 각 질문에 대해 참고 문서 기반으로 답변을 생성하고 파일로 저장하는 시스템
- 상세 내용:
    - QuestionAnsweringProcessor 클래스 (라인 31-181): 질의문 JSON 파일 처리 및 답변 생성을 담당하는 메인 클래스
    - load_questions_from_file 함수 (라인 36-51): JSON 파일에서 질의문 데이터를 로드하는 함수
    - answer_single_question 함수 (라인 53-117): 개별 질문에 대해 Claude로부터 답변을 받는 비동기 함수
    - save_answer_to_file 함수 (라인 119-132): 각 답변을 개별 JSON 파일로 저장하는 함수
    - process_questions_realtime 함수 (라인 134-181): 질문들을 실시간 병렬 처리하는 함수
    - test_question_answering_processor 함수 (라인 183-231): 시스템 테스트 함수
    - 질문 답변 로직 (라인 76-117): 참고 문서를 바탕으로 구체적 답변 생성
    - 실시간 개별 저장 (라인 160-178): 각 답변이 완료되는 즉시 개별 파일 저장
- 상태: active
- 참조: document_based_qa_system_v4.py의 병렬 처리 구조를 활용하여 질의문 전용 처리기로 설계
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

class QuestionAnsweringProcessor:
    """질의문 JSON 파일 처리 및 답변 생성을 담당하는 메인 클래스"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.results = []
        
    def load_questions_from_file(self, questions_file: str) -> Dict[str, Any]:
        """JSON 파일에서 질의문 데이터를 로드하는 함수"""
        try:
            if not os.path.exists(questions_file):
                return {'status': 'error', 'error': f'파일을 찾을 수 없습니다: {questions_file}'}
            
            with open(questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def answer_single_question(self, client: ClaudeSDKClient, question_data: Dict[str, Any], 
                                   reference_documents: List[str], question_index: int) -> Dict[str, Any]:
        """개별 질문에 대해 Claude로부터 답변을 받는 비동기 함수"""
        
        # 참고 문서 내용 로드
        doc_contents = []
        for doc_path in reference_documents:
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    doc_name = os.path.basename(doc_path)
                    doc_contents.append(f"=== {doc_name} ===\n{f.read()}")
        
        reference_text = "\n\n".join(doc_contents)
        
        # 답변 생성 프롬프트
        prompt = f"""태수야, 다음 질문에 대해 참고 문서를 바탕으로 구체적이고 실용적인 답변을 해줘:

**질문:** {question_data.get('question', '')}

**질문 카테고리:** {question_data.get('category', '')}

**갭 설명:** {question_data.get('gap_description', '')}

**참고 문서:**
{reference_text}

참고 문서에서 관련 정보를 찾아서 구체적이고 실용적인 답변을 제공해줘. 
답변에는 해당 정보가 문서의 어느 부분에서 나왔는지 출처를 명시해주고,
가능하다면 구체적인 예시나 활용 방법도 포함해줘."""
        
        try:
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
            
            return {
                'question_index': question_index,
                'original_question': question_data,
                'answer': ''.join(text_parts),
                'reference_documents': reference_documents,
                'metadata': {
                    'cost': total_cost,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success'
                }
            }
            
        except Exception as e:
            return {
                'question_index': question_index,
                'original_question': question_data,
                'answer': '',
                'reference_documents': reference_documents,
                'metadata': {
                    'cost': 0.0,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e)
                }
            }
    
    def save_answer_to_file(self, answer_data: Dict[str, Any]) -> str:
        """각 답변을 개별 JSON 파일로 저장하는 함수"""
        question_index = answer_data.get('question_index', 0)
        filename = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/answer_{self.session_id}_q{question_index:02d}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(answer_data, f, ensure_ascii=False, indent=2)
            return filename
        except Exception as e:
            print(f"답변 파일 저장 실패 (질문 {question_index}): {e}")
            return ""
    
    async def process_questions_realtime(self, questions_file: str) -> Dict[str, Any]:
        """질문들을 실시간 병렬 처리하는 함수"""
        
        # 질의문 파일 로드
        load_result = self.load_questions_from_file(questions_file)
        if load_result['status'] != 'success':
            return load_result
        
        questions_data = load_result['data']
        reference_documents = questions_data.get('reference_documents', [])
        
        # 질의문 리스트 추출 (JSON에서 파싱)
        questions_text = questions_data.get('questions_data', {}).get('followup_questions', '')
        
        try:
            # JSON 문자열에서 질문 리스트 추출
            import re
            json_match = re.search(r'\{.*\}', questions_text, re.DOTALL)
            if json_match:
                questions_json = json.loads(json_match.group())
                questions_list = questions_json.get('followup_questions', [])
            else:
                return {'status': 'error', 'error': '질의문 JSON 파싱 실패'}
        except Exception as e:
            return {'status': 'error', 'error': f'질의문 파싱 오류: {e}'}
        
        print(f"📄 {len(questions_list)}개 질문 처리 시작...")
        print("💫 각 답변이 완료되는 즉시 개별 파일로 저장됩니다.\n")
        
        clients = []
        tasks = []
        completed_results = []
        
        try:
            # 각 질문에 대해 클라이언트 생성 및 태스크 준비
            for i, question_data in enumerate(questions_list):
                client = ClaudeSDKClient()
                clients.append(client)
                
                await client.__aenter__()
                
                task = self.answer_single_question(client, question_data, reference_documents, i)
                tasks.append(task)
            
            # 완료되는 대로 실시간 처리
            for completed_task in asyncio.as_completed(tasks):
                result = await completed_task
                
                if isinstance(result, Exception):
                    print(f"❌ 처리 중 오류: {result}")
                    continue
                
                # 즉시 개별 파일 저장
                saved_file = self.save_answer_to_file(result)
                
                # 즉시 출력
                print(f"✅ 완료: 질문 {result['question_index'] + 1}")
                print(f"   카테고리: {result['original_question'].get('category', 'N/A')}")
                print(f"   상태: {result['metadata']['status']}")
                
                if result['metadata']['status'] == 'success':
                    print(f"   답변 길이: {len(result['answer'])} 문자")
                    print(f"   비용: ${result['metadata']['cost']:.4f}")
                    if saved_file:
                        print(f"   📁 저장: {os.path.basename(saved_file)}")
                else:
                    print(f"   ❌ 오류: {result['metadata'].get('error', '알 수 없는 오류')}")
                
                print("-" * 50)
                completed_results.append(result)
                self.results.append(result)
            
            return {
                'status': 'success',
                'results': completed_results,
                'total_questions': len(questions_list),
                'session_id': self.session_id,
                'execution_time': datetime.now().isoformat()
            }
            
        finally:
            # 모든 클라이언트 정리
            for client in clients:
                try:
                    await client.__aexit__(None, None, None)
                except:
                    pass

async def test_question_answering_processor():
    """시스템 테스트 함수"""
    print("=== Question Answering Processor 테스트 시작 ===\n")
    
    # 가장 최근 질의문 파일 찾기
    base_path = "/home/nadle/projects/Concept_Sherpa_V2/25-08-23"
    questions_files = [f for f in os.listdir(base_path) if f.startswith("followup_questions_") and f.endswith(".json")]
    
    if not questions_files:
        print("❌ 질의문 파일이 없습니다. knowledge_gap_analyzer_v2.py를 먼저 실행해주세요.")
        return
    
    # 가장 최근 파일 선택
    questions_files.sort(reverse=True)
    latest_questions_file = os.path.join(base_path, questions_files[0])
    
    processor = QuestionAnsweringProcessor()
    
    try:
        print(f"📁 질의문 파일: {questions_files[0]}")
        print(f"🆔 세션 ID: {processor.session_id}")
        print("="*70)
        
        # 질의문 처리 실행
        result = await processor.process_questions_realtime(latest_questions_file)
        
        if result['status'] == 'success':
            print(f"🎉 총 {result['total_questions']}개 질문 처리 완료!")
            print(f"⏰ 실행 시간: {result['execution_time']}")
            
            # 전체 비용 계산
            total_cost = sum(r['metadata']['cost'] for r in result['results'] if r['metadata']['status'] == 'success')
            print(f"💰 총 비용: ${total_cost:.4f}")
            
            successful_answers = [r for r in result['results'] if r['metadata']['status'] == 'success']
            print(f"✅ 성공: {len(successful_answers)}개")
            
            failed_answers = [r for r in result['results'] if r['metadata']['status'] == 'error']
            if failed_answers:
                print(f"❌ 실패: {len(failed_answers)}개")
        else:
            print(f"❌ 처리 실패: {result.get('error', '알 수 없는 오류')}")
        
        # 전체 결과 요약 저장
        summary_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/qa_processing_summary_{processor.session_id}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📋 처리 요약 저장: {os.path.basename(summary_file)}")
        
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
    asyncio.run(test_question_answering_processor())