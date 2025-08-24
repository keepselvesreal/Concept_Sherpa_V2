"""
# 목차
- 생성 시간: 2025년 8월 24일 20:30:50 KST
- 핵심 내용: 참고 문서들에 대한 질의 처리를 위한 collective와 individual 답변 생성 시스템
- 상세 내용:
    - DocumentQueryProcessor 클래스 (라인 28-138): 메인 클래스로 공통 질의 처리 로직을 담당
    - _execute_query 함수 (라인 34-67): Claude SDK를 통한 단일 질의 실행 로직  
    - _save_result 함수 (라인 69-88): 결과를 타임스탬프 기반 JSON 파일로 저장
    - collective_answer 함수 (라인 90-112): 모든 참고문서를 결합하여 단일 답변 생성
    - individual_answers 함수 (라인 114-138): 각 참고문서에 대해 병렬로 개별 답변 생성
    - main 함수 (라인 140-168): 테스트 실행을 위한 메인 함수
- 상태: active
- 주소: document_query_processor
- 참조: conversation_module.py의 Claude SDK 패턴과 multi_agent_claude_tester_haiku3_final.py의 병렬 처리 패턴 결합
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

class DocumentQueryProcessor:
    """참고 문서들에 대한 질의 처리를 담당하는 메인 클래스"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.work_dir = "/home/nadle/projects/Concept_Sherpa_V2/25-08-24"
        self.query_count = 0
    
    async def _execute_query(self, prompt: str, query: str, document_content: str) -> Dict[str, Any]:
        """Claude SDK를 통한 단일 질의 실행 로직"""
        start_time = time.time()
        
        try:
            # 프롬프트와 문서를 결합
            enhanced_prompt = f"""{prompt}

참고 문서:
{document_content}

질의: {query}"""

            async with ClaudeSDKClient() as client:
                await client.query(enhanced_prompt)
                text_parts = []
                
                async for msg in client.receive_response():
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                text_parts.append(block.text)
                
                elapsed_time = time.time() - start_time
                
                return {
                    'success': True,
                    'response': ''.join(text_parts),
                    'elapsed_time': round(elapsed_time, 2),
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': round(elapsed_time, 2),
                'timestamp': datetime.now().isoformat()
            }
    
    def _save_collective_result(self, query_data: Dict[str, Any], document_paths: List[str]) -> str:
        """세션별 collective 답변을 누적하여 저장"""
        try:
            filename = f"{self.work_dir}/collective_answer_{self.session_id}.json"
            
            # 기존 세션 파일 확인
            session_data = {
                'session_id': self.session_id,
                'document_paths': document_paths,
                'queries': []
            }
            
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    session_data['queries'] = existing_data.get('queries', [])
                    # document_paths는 첫 번째 호출에서 설정되고 이후 유지
                    if 'document_paths' in existing_data:
                        session_data['document_paths'] = existing_data['document_paths']
            
            # 새 질의 데이터 추가
            session_data['queries'].append(query_data)
            session_data['total_queries'] = len(session_data['queries'])
            
            # 파일 저장
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            return filename
        except Exception as e:
            print(f"세션 저장 실패: {e}")
            return ""
    
    def _save_individual_result(self, result_data: Dict[str, Any], index: int) -> str:
        """개별 답변을 타임스탬프 기반으로 저장"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.work_dir}/individual_{index:02d}_answer_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            return filename
        except Exception as e:
            print(f"개별 결과 저장 실패: {e}")
            return ""
    
    async def collective_answer(self, prompt: str, query: str, document_list: List[str], document_paths: List[str] = None) -> Dict[str, Any]:
        """모든 참고문서를 결합하여 단일 답변 생성"""
        self.query_count += 1
        
        # 모든 문서를 하나로 결합
        combined_content = "\n\n=== 문서 구분선 ===\n\n".join(document_list)
        
        # 단일 질의 실행
        result = await self._execute_query(prompt, query, combined_content)
        
        # 문서 경로 처리
        doc_paths = document_paths or [f"document_{i}" for i in range(len(document_list))]
        
        # 세션별 질의 데이터 구성 (document_paths 제외)
        query_data = {
            'query_id': self.query_count,
            'query_content': query,
            'answer': result['response'] if result['success'] else '',
            'elapsed_time': result['elapsed_time'],
            'timestamp': result['timestamp'],
            'success': result['success']
        }
        
        if not result['success']:
            query_data['error'] = result['error']
        
        # 세션 파일에 누적 저장
        saved_file = self._save_collective_result(query_data, doc_paths)
        
        # 반환용 데이터 구성
        return_data = {
            'session_id': self.session_id,
            'query_id': self.query_count,
            'query': query,
            'document_count': len(document_list),
            'processing_type': 'collective',
            'model_response': result['response'] if result['success'] else '',
            'elapsed_time': result['elapsed_time'],
            'timestamp': result['timestamp'],
            'document_paths': doc_paths,
            'success': result['success'],
            'saved_file': saved_file
        }
        
        if not result['success']:
            return_data['error'] = result['error']
        
        return return_data
    
    async def individual_answers(self, prompt: str, query: str, document_list: List[str], document_paths: List[str] = None) -> List[Dict[str, Any]]:
        """각 참고문서에 대해 병렬로 개별 답변 생성"""
        self.query_count += 1
        
        # 문서 경로 처리
        doc_paths = document_paths or [f"document_{i}" for i in range(len(document_list))]
        
        # 각 문서에 대한 태스크 생성
        tasks = []
        for i, doc_content in enumerate(document_list):
            task = self._execute_query(prompt, query, doc_content)
            tasks.append((i, task))
        
        # 병렬 실행
        results = []
        task_results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # 결과 처리 및 개별 저장
        for i, task_result in enumerate(task_results):
            if isinstance(task_result, Exception):
                result_data = {
                    'session_id': self.session_id,
                    'query_id': self.query_count,
                    'current_query': query,
                    'answer': '',
                    'elapsed_time': 0.0,
                    'timestamp': datetime.now().isoformat(),
                    'document_path': doc_paths[i] if i < len(doc_paths) else f"document_{i}",
                    'success': False,
                    'error': str(task_result)
                }
            else:
                result_data = {
                    'session_id': self.session_id,
                    'query_id': self.query_count,
                    'current_query': query,
                    'answer': task_result['response'] if task_result['success'] else '',
                    'elapsed_time': task_result['elapsed_time'],
                    'timestamp': task_result['timestamp'],
                    'document_path': doc_paths[i] if i < len(doc_paths) else f"document_{i}",
                    'success': task_result['success']
                }
                
                if not task_result['success']:
                    result_data['error'] = task_result['error']
            
            # 개별 파일로 저장
            saved_file = self._save_individual_result(result_data, i)
            result_data['saved_file'] = saved_file
            
            results.append(result_data)
        
        return results

async def main():
    """테스트 실행을 위한 메인 함수"""
    processor = DocumentQueryProcessor()
    
    # 테스트 데이터
    test_prompt = "다음 참고 문서를 바탕으로 질의에 대해 간결하고 정확하게 답변해주세요."
    test_query = "이 문서의 핵심 내용을 3줄로 요약해주세요."
    test_documents = [
        "첫 번째 문서: 파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다.",
        "두 번째 문서: 자바스크립트는 웹 개발에 필수적인 언어입니다.",
        "세 번째 문서: 데이터 분석에는 R과 파이썬이 널리 사용됩니다."
    ]
    
    print("=== 문서 질의 처리기 테스트 시작 ===\n")
    
    try:
        # 1. Collective 답변 테스트
        print("1. Collective 답변 생성 중...")
        collective_result = await processor.collective_answer(test_prompt, test_query, test_documents)
        print(f"Collective 결과: {collective_result['success']}")
        print(f"처리 시간: {collective_result['elapsed_time']}초")
        print(f"저장된 파일: {collective_result['saved_file']}\n")
        
        # 2. Individual 답변 테스트
        print("2. Individual 답변들 생성 중...")
        individual_results = await processor.individual_answers(test_prompt, test_query, test_documents)
        print(f"Individual 결과: {len(individual_results)}개 답변")
        for result in individual_results:
            print(f"  문서 {result['document_index']}: {result['success']}, {result['elapsed_time']}초")
        
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())