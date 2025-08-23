"""
# 목차
- 생성 시간: 2025년 8월 23일 12:40:37 KST
- 핵심 내용: Claude SDK를 사용한 다중 에이전트 동시 실행 및 응답 수집 시스템
- 상세 내용:
    - MultiAgentClaudeClient 클래스 (라인 21-86): 여러 Claude 에이전트를 관리하고 동시 실행하는 메인 클래스
    - get_response_with_metadata 함수 (라인 26-41): 개별 에이전트의 응답을 메타데이터와 함께 수집하는 비동기 함수
    - run_agents_concurrently 함수 (라인 43-70): 여러 에이전트를 동시에 실행하고 결과를 수집하는 함수
    - main 함수 (라인 72-86): 테스트 시나리오를 실행하는 메인 함수
    - test_multi_agent_system 함수 (라인 88-142): 실제 테스트를 수행하는 함수
    - 에러 핸들링 (라인 115-125): CLI 설치 오류 및 프로세스 오류 처리
    - 결과 출력 (라인 126-142): 각 에이전트의 응답과 메타데이터를 구조화하여 출력
- 상태: 활성
- 주소: multi_agent_claude_tester
- 참조: 제공된 예시 코드 기반으로 작성
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

class MultiAgentClaudeClient:
    """여러 Claude 에이전트를 관리하고 동시 실행하는 클래스"""
    
    def __init__(self):
        self.results = {}
        
    async def get_response_with_metadata(self, client: ClaudeSDKClient, prompt: str, agent_name: str) -> Dict[str, Any]:
        """개별 에이전트의 응답을 메타데이터와 함께 수집"""
        try:
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
                'agent_name': agent_name,
                'text': ''.join(text_parts),
                'cost': total_cost,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'agent_name': agent_name,
                'text': '',
                'cost': 0.0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def run_agents_concurrently(self, agent_configs: List[Dict[str, str]]) -> Dict[str, Any]:
        """여러 에이전트를 동시에 실행하고 결과를 수집"""
        clients = []
        tasks = []
        
        try:
            # 각 에이전트에 대해 클라이언트 생성 및 태스크 준비
            for config in agent_configs:
                client = ClaudeSDKClient()
                clients.append(client)
                
                # 컨텍스트 매니저 진입
                await client.__aenter__()
                
                task = self.get_response_with_metadata(
                    client, 
                    config['prompt'], 
                    config['name']
                )
                tasks.append(task)
            
            # 모든 태스크를 동시에 실행
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                'results': results,
                'total_agents': len(agent_configs),
                'execution_time': datetime.now().isoformat()
            }
            
        finally:
            # 모든 클라이언트 정리
            for client in clients:
                try:
                    await client.__aexit__(None, None, None)
                except:
                    pass
    
    async def main(self):
        """메인 실행 함수"""
        agent_configs = [
            {
                'name': 'code_reviewer',
                'prompt': 'Python 코드의 일반적인 품질 체크포인트를 3가지만 알려주세요'
            },
            {
                'name': 'test_writer', 
                'prompt': 'Python 함수를 테스트할 때 고려해야 할 핵심 사항 3가지를 알려주세요'
            },
            {
                'name': 'documentation_writer',
                'prompt': 'API 문서 작성 시 꼭 포함해야 할 요소 3가지를 알려주세요'
            }
        ]
        
        return await self.run_agents_concurrently(agent_configs)

async def test_multi_agent_system():
    """다중 에이전트 시스템 테스트 함수"""
    print("=== Claude SDK 다중 에이전트 테스트 시작 ===\n")
    
    client = MultiAgentClaudeClient()
    
    try:
        # 1. 단일 에이전트 테스트
        print("1. 단일 에이전트 테스트...")
        async with ClaudeSDKClient() as single_client:
            result = await client.get_response_with_metadata(
                single_client, 
                "안녕하세요! 간단한 인사말을 해주세요.",
                "greeting_agent"
            )
            print(f"단일 에이전트 결과: {result['status']}")
            print(f"응답 길이: {len(result['text'])} 문자\n")
        
        # 2. 다중 에이전트 동시 실행 테스트
        print("2. 다중 에이전트 동시 실행 테스트...")
        results = await client.main()
        
        # 결과 처리 및 출력
        print(f"총 {results['total_agents']}개 에이전트 실행 완료")
        print(f"실행 시간: {results['execution_time']}\n")
        
        for i, result in enumerate(results['results']):
            if isinstance(result, Exception):
                print(f"에이전트 {i+1} 실행 중 오류: {result}")
                continue
                
            print(f"=== {result['agent_name']} 결과 ===")
            print(f"상태: {result['status']}")
            print(f"타임스탬프: {result['timestamp']}")
            
            if result['status'] == 'success':
                print(f"응답 길이: {len(result['text'])} 문자")
                print(f"비용: ${result['cost']:.4f}")
                print(f"응답 내용 (처음 200자): {result['text'][:200]}...")
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
        results_file = f"/home/nadle/projects/Concept_Sherpa_V2/25-08-23/multi_agent_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"결과가 {results_file}에 저장되었습니다.")
    except Exception as e:
        print(f"결과 저장 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_multi_agent_system())