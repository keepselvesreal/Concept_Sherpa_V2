"""
# 목차
- 생성 시간: 2025년 8월 23일 13:29:14 KST
- 핵심 내용: Claude SDK를 사용해 여러 참고 문서에 대해 병렬로 질문 답변을 생성하는 시스템
- 상세 내용:
    - DocumentBasedQASystem 클래스 (라인 31-142): 문서 기반 질의응답 시스템의 메인 클래스
    - get_response_for_document 함수 (라인 36-80): 개별 문서에 대해 Claude로부터 답변을 받는 비동기 함수
    - process_documents_concurrently 함수 (라인 82-124): 여러 문서를 병렬 처리하는 함수
    - main 함수 (라인 126-142): 테스트 실행을 위한 메인 함수
    - test_document_qa_system 함수 (라인 144-193): 실제 테스트를 수행하는 함수
    - 에러 핸들링 (라인 158-165): CLI 설치 오류 및 프로세스 오류 처리
    - 결과 출력 (라인 173-193): 각 문서별 답변과 메타데이터를 구조화하여 출력
- 상태: active
- 참조: multi_agent_claude_tester.py를 기반으로 문서 기반 QA 시스템으로 수정
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

class DocumentBasedQASystem:
    """여러 참고 문서에 대해 병렬로 질문 답변을 생성하는 시스템"""
    
    def __init__(self):
        self.results = {}
        
    async def get_response_for_document(self, client: ClaudeSDKClient, question: str, 
                                      document_path: str, document_name: str) -> Dict[str, Any]:
        """개별 문서에 대해 Claude로부터 답변을 받는 비동기 함수"""
        try:
            # 파일 읽기
            if not os.path.exists(document_path):
                return {
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
                'document_name': document_name,
                'document_path': document_path,
                'answer': ''.join(text_parts),
                'cost': total_cost,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'document_name': document_name,
                'document_path': document_path,
                'answer': '',
                'cost': 0.0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def process_documents_concurrently(self, question: str, 
                                           document_paths: List[str]) -> Dict[str, Any]:
        """여러 문서를 병렬 처리하는 함수"""
        clients = []
        tasks = []
        
        try:
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
            
            # 모든 태스크를 동시에 실행
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                'question': question,
                'results': results,
                'total_documents': len(document_paths),
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
        """메인 실행 함수"""
        return await self.process_documents_concurrently(question, document_paths)

async def test_document_qa_system():
    """문서 기반 질의응답 시스템 테스트 함수"""
    print("=== Claude SDK 문서 기반 QA 시스템 테스트 시작 ===\n")
    
    # 테스트 질문
    question = "Claude Code의 핵심 특징은 무엇인가요?"
    
    # 테스트 문서 경로들
    document_paths = [
        "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref1.md",
        "/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref2.md"
    ]
    
    qa_system = DocumentBasedQASystem()
    
    try:
        print(f"질문: {question}")
        print(f"참고 문서 수: {len(document_paths)}")
        print("="*50)
        
        # 문서 기반 QA 실행
        results = await qa_system.main(question, document_paths)
        
        # 결과 출력
        print(f"총 {results['total_documents']}개 문서 처리 완료")
        print(f"실행 시간: {results['execution_time']}\n")
        
        for i, result in enumerate(results['results']):
            if isinstance(result, Exception):
                print(f"문서 {i+1} 처리 중 오류: {result}")
                continue
                
            print(f"=== 문서: {result['document_name']} ===")
            print(f"상태: {result['status']}")
            print(f"타임스탬프: {result['timestamp']}")
            
            if result['status'] == 'success':
                print(f"답변 길이: {len(result['answer'])} 문자")
                print(f"비용: ${result['cost']:.4f}")
                print(f"답변:\n{result['answer']}")
            else:
                print(f"오류: {result.get('error', '알 수 없는 오류')}")
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

    # 결과를 JSON 파일로 저장
    try:
        results_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/qa_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"결과가 {results_file}에 저장되었습니다.")
    except Exception as e:
        print(f"결과 저장 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_document_qa_system())