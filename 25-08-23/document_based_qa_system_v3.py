"""
# 목차
- 생성 시간: 2025년 8월 23일 15:26:07 KST  
- 핵심 내용: Claude SDK를 사용해 여러 참고 문서에 대해 병렬로 질문 답변을 생성하며, 각 답변이 완료되는 즉시 개별 파일로 저장하는 시스템 (사용자 질문 포함)
- 상세 내용:
    - DocumentBasedQASystemV3 클래스 (라인 31-178): 사용자 질문을 개별 저장 파일에 포함하는 문서 기반 질의응답 시스템
    - get_response_for_document 함수 (라인 36-89): 개별 문서에 대해 Claude로부터 답변을 받고 질문 정보를 포함하는 비동기 함수
    - save_individual_result 함수 (라인 91-103): 각 답변을 사용자 질문과 함께 개별 JSON 파일로 즉시 저장하는 함수
    - process_documents_realtime 함수 (라인 105-163): asyncio.as_completed를 사용한 실시간 처리 함수
    - main 함수 (라인 165-178): 새로운 실시간 처리 방식을 사용하는 메인 함수
    - test_document_qa_system_v3 함수 (라인 180-243): 질문 포함 실시간 개별 저장 테스트 함수
    - 질문 정보 포함 저장 (라인 82-89): 각 개별 결과에 사용자 질문 정보 추가
    - 실시간 출력 (라인 146-161): 각 문서 답변이 완료되는 즉시 출력 및 개별 파일 저장
- 상태: active
- 참조: document_based_qa_system_v2.py를 기반으로 사용자 질문 포함 저장 기능 추가
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

class DocumentBasedQASystemV3:
    """사용자 질문을 개별 저장 파일에 포함하는 문서 기반 질의응답 시스템"""
    
    def __init__(self):
        self.results = []
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    async def get_response_for_document(self, client: ClaudeSDKClient, question: str, 
                                      document_path: str, document_name: str) -> Dict[str, Any]:
        """개별 문서에 대해 Claude로부터 답변을 받고 질문 정보를 포함하는 비동기 함수"""
        try:
            # 파일 읽기
            if not os.path.exists(document_path):
                return {
                    'question': question,  # 질문 정보 추가
                    'document_name': document_name,
                    'document_path': document_path,
                    'answer': '',
                    'cost': 0.0,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error',
                    'error': f'파일을 찾을 수 없습니다: {document_path}'
                }
            
            with open(document_path, 'r', encoding='utf-8') as f:
                document_content = f.read()
            
            # 프롬프트 생성
            prompt = f"""질문: {question}

참고 문서 (파일: {document_name}):
{document_content}

위 참고 문서를 바탕으로 질문에 답변해주세요. 
답변에 해당 내용이 문서의 어느 부분에 있는지 명시해주세요."""
            
            # Claude에게 질문
            await client.query(prompt)
            text_parts = []
            total_cost = 0.0
            
            async for msg in client.receive_response():
                if hasattr(msg, 'content'):
                    for block in msg.content:
                        if hasattr(block, 'text'):
                            text_parts.append(block.text)
                
                # 결과 메시지에서 비용 정보 추출
                if type(msg).__name__ == "ResultMessage":
                    total_cost = getattr(msg, 'total_cost_usd', 0.0)
            
            return {
                'question': question,  # 질문 정보 추가
                'document_name': document_name,
                'document_path': document_path,
                'answer': ''.join(text_parts),
                'cost': total_cost,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'question': question,  # 질문 정보 추가
                'document_name': document_name,
                'document_path': document_path,
                'answer': '',
                'cost': 0.0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def save_individual_result(self, result: Dict[str, Any]) -> str:
        """각 답변을 사용자 질문과 함께 개별 JSON 파일로 즉시 저장"""
        # 파일명에서 확장자 제거
        doc_name_clean = os.path.splitext(result['document_name'])[0]
        filename = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/qa_result_{self.session_id}_{doc_name_clean}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return filename
        except Exception as e:
            print(f"개별 결과 저장 실패 ({result['document_name']}): {e}")
            return ""
    
    async def process_documents_realtime(self, question: str, 
                                       document_paths: List[str]) -> Dict[str, Any]:
        """asyncio.as_completed를 사용한 실시간 처리 함수"""
        clients = []
        tasks = []
        completed_results = []
        
        try:
            print(f"📄 {len(document_paths)}개 문서 처리 시작...")
            print("💫 각 답변이 완료되는 즉시 개별 파일로 저장됩니다.")
            print(f"❓ 질문: {question}\n")
            
            # 각 문서에 대해 클라이언트 생성 및 태스크 준비
            for document_path in document_paths:
                client = ClaudeSDKClient()
                clients.append(client)
                
                # 컨텍스트 매니저 진입
                await client.__aenter__()
                
                # 문서 이름 추출 (파일명만)
                document_name = os.path.basename(document_path)
                
                task = self.get_response_for_document(
                    client, 
                    question, 
                    document_path,
                    document_name
                )
                tasks.append(task)
            
            # 완료되는 대로 실시간 처리
            for completed_task in asyncio.as_completed(tasks):
                result = await completed_task
                
                if isinstance(result, Exception):
                    print(f"❌ 처리 중 오류: {result}")
                    continue
                
                # 즉시 개별 파일 저장
                saved_file = self.save_individual_result(result)
                
                # 즉시 출력
                print(f"✅ 완료: {result['document_name']}")
                print(f"   상태: {result['status']}")
                print(f"   시간: {result['timestamp']}")
                
                if result['status'] == 'success':
                    print(f"   답변 길이: {len(result['answer'])} 문자")
                    print(f"   비용: ${result['cost']:.4f}")
                    if saved_file:
                        print(f"   📁 저장: {os.path.basename(saved_file)}")
                else:
                    print(f"   ❌ 오류: {result.get('error', '알 수 없는 오류')}")
                
                print("-" * 50)
                completed_results.append(result)
                self.results.append(result)
            
            return {
                'question': question,
                'results': completed_results,
                'total_documents': len(document_paths),
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
    
    async def main(self, question: str, document_paths: List[str]):
        """실시간 처리 방식을 사용하는 메인 함수"""
        return await self.process_documents_realtime(question, document_paths)

async def test_document_qa_system_v3():
    """질문 포함 실시간 개별 저장 문서 기반 질의응답 시스템 테스트 함수"""
    print("=== Claude SDK 문서 기반 QA 시스템 V3 (질문 포함 실시간 저장) 테스트 시작 ===\n")
    
    # 테스트 질문
    question = "Claude Code의 핵심 특징은 무엇인가요?"
    
    # 테스트 문서 경로들
    document_paths = [
        "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref1.md",
        "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref2.md"
    ]
    
    qa_system = DocumentBasedQASystemV3()
    
    try:
        print(f"🤔 질문: {question}")
        print(f"📚 참고 문서 수: {len(document_paths)}")
        print(f"🆔 세션 ID: {qa_system.session_id}")
        print("="*70)
        
        # 문서 기반 QA 실행 (실시간 처리)
        results = await qa_system.main(question, document_paths)
        
        # 최종 요약 출력
        print(f"🎉 총 {results['total_documents']}개 문서 처리 완료!")
        print(f"⏰ 실행 시간: {results['execution_time']}")
        
        # 전체 비용 계산
        total_cost = sum(r['cost'] for r in results['results'] if r['status'] == 'success')
        print(f"💰 총 비용: ${total_cost:.4f}")
        
        successful_docs = [r for r in results['results'] if r['status'] == 'success']
        print(f"✅ 성공: {len(successful_docs)}개")
        
        failed_docs = [r for r in results['results'] if r['status'] == 'error']
        if failed_docs:
            print(f"❌ 실패: {len(failed_docs)}개")
        
        print()
        
    except CLINotFoundError:
        print("❌ Claude CLI가 설치되지 않았습니다.")
        print("설치 명령어: npm install -g @anthropic-ai/claude-code")
    except ProcessError as e:
        print(f"❌ 프로세스 실행 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()

    # 최종 요약 정보를 별도 파일로 저장
    try:
        summary_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/qa_summary_{qa_system.session_id}.json"
        summary_data = {
            'session_info': {
                'session_id': qa_system.session_id,
                'question': question,
                'total_documents': len(document_paths),
                'execution_time': results['execution_time'] if 'results' in locals() else datetime.now().isoformat()
            },
            'document_paths': document_paths,
            'processing_summary': {
                'successful': len([r for r in qa_system.results if r['status'] == 'success']),
                'failed': len([r for r in qa_system.results if r['status'] == 'error']),
                'total_cost': sum(r['cost'] for r in qa_system.results if r['status'] == 'success')
            }
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"📋 요약 정보가 {os.path.basename(summary_file)}에 저장되었습니다.")
    except Exception as e:
        print(f"요약 저장 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_document_qa_system_v3())