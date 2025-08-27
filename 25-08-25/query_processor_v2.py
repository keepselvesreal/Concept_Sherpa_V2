# 생성 시간: 2025-08-25 20:23:02 KST
# 핵심 내용: AI 판단 기반 참조 문서 관련성 평가 및 조건부 응답 생성 시스템 (기존 query_processor.py 확장)
# 상세 내용:
#   - RelevanceJudge 클래스 (27-85): AI 기반 문서-질의 관련성 판단 전담 클래스
#   - QueryProcessor 클래스 (87-158): 기존 기능 + 관련성 판단 통합
#   - _judge_relevance 메서드 (135-158): AI 기반 관련성 판단 핵심 로직
#   - _generate_conditional_response 메서드 (160-190): 조건부 응답 생성
#   - RELEVANCE_JUDGMENT_PROMPT (267-284): 단계별 관련성 판단 프롬프트
#   - DOCUMENT_BASED_PROMPT (286-294): 문서 기반 응답 프롬프트  
#   - KNOWLEDGE_BASED_PROMPT (296-304): 사전 지식 기반 응답 프롬프트
# 상태: active
# 주소: query_processor_v2
# 참조: query_processor (기존 파일)

import asyncio
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# 기존 모듈 임포트
from document_query_processor import DocumentQueryProcessor
from understanding_gap_analyzer import UnderstandingGapAnalyzer
from get_session_id import get_session_from_logs

try:
    from claude_code_sdk import ClaudeSDKClient, CLINotFoundError, ProcessError
except ImportError as e:
    print(f"claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    exit(1)

@dataclass
class RelevanceResult:
    """관련성 판단 결과"""
    has_relevant_content: bool
    reasoning: str
    confidence: float = 0.0

class RelevanceJudge:
    """AI 기반 문서-질의 관련성 판단 전담 클래스"""
    
    def __init__(self):
        # 실제 AI 모델 클라이언트 초기화 (여기서는 Claude SDK 사용)
        try:
            self.ai_client = ClaudeSDKClient()
        except Exception as e:
            print(f"AI 클라이언트 초기화 실패: {e}")
            self.ai_client = None
    
    async def judge_relevance(self, query: str, reference_documents: List[str]) -> RelevanceResult:
        """
        AI를 사용해 질의와 참조 문서 간 관련성 판단
        
        Args:
            query: 사용자 질의
            reference_documents: 참조 문서 목록
            
        Returns:
            RelevanceResult: 관련성 판단 결과
        """
        if not self.ai_client:
            # AI 클라이언트가 없으면 보수적으로 False 반환
            return RelevanceResult(
                has_relevant_content=False,
                reasoning="AI 클라이언트 초기화 실패로 관련성 판단 불가",
                confidence=0.0
            )
        
        try:
            # 문서들을 하나의 텍스트로 결합
            documents_text = "\n\n".join([
                f"=== 문서 {i+1} ===\n{doc}" 
                for i, doc in enumerate(reference_documents)
            ])
            
            # 관련성 판단 프롬프트 구성
            prompt = RELEVANCE_JUDGMENT_PROMPT.format(
                query=query,
                documents=documents_text
            )
            
            # AI에게 관련성 판단 요청
            response = await self.ai_client.generate_async(prompt)
            
            # JSON 응답 파싱
            try:
                result = json.loads(response)
                return RelevanceResult(
                    has_relevant_content=result.get("has_relevant_content", False),
                    reasoning=result.get("reasoning", "판단 근거 없음"),
                    confidence=result.get("confidence", 0.0)
                )
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 텍스트에서 true/false 추출 시도
                has_relevant = "true" in response.lower()
                return RelevanceResult(
                    has_relevant_content=has_relevant,
                    reasoning=f"JSON 파싱 실패, 텍스트 기반 판단: {response[:100]}...",
                    confidence=0.5 if has_relevant else 0.3
                )
                
        except Exception as e:
            print(f"관련성 판단 중 오류: {e}")
            # 에러 발생 시 보수적으로 False 반환
            return RelevanceResult(
                has_relevant_content=False,
                reasoning=f"관련성 판단 중 오류 발생: {str(e)}",
                confidence=0.0
            )

class QueryProcessor:
    """AI 관련성 판단 기능이 추가된 질의 처리 시스템"""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.chat_logs_dir = os.path.join(self.current_dir, "chat-logs")
        
        # 기존 클래스 인스턴스 생성
        from query_processor import SessionManager  # 기존 SessionManager 재사용
        self.session_manager = SessionManager(self.current_dir)
        self.doc_processor = DocumentQueryProcessor(self.current_dir)
        self.gap_analyzer = UnderstandingGapAnalyzer()
        
        # 새로운 관련성 판단기 추가
        self.relevance_judge = RelevanceJudge()
        
        # AI 클라이언트 (응답 생성용)
        try:
            self.ai_client = ClaudeSDKClient()
        except Exception as e:
            print(f"AI 클라이언트 초기화 실패: {e}")
            self.ai_client = None
    
    def _read_folder_files(self, folder_path: str) -> List[Dict[str, str]]:
        """폴더 내 모든 파일을 읽어서 리스트로 반환 (기존 로직 재사용)"""
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"폴더가 존재하지 않습니다: {folder_path}")
        
        files_data = []
        
        for file_path in folder.glob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        files_data.append({
                            'path': str(file_path),
                            'name': file_path.name,
                            'content': content
                        })
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='cp949') as f:
                            content = f.read()
                            files_data.append({
                                'path': str(file_path),
                                'name': file_path.name,
                                'content': content
                            })
                    except Exception:
                        print(f"텍스트 파일이 아닙니다, 건너뛰기: {file_path.name}")
                        continue
                except Exception as e:
                    print(f"파일 읽기 실패: {file_path.name}, {e}")
                    continue
        
        return files_data
    
    async def _judge_relevance(self, query: str, documents: List[str]) -> RelevanceResult:
        """
        AI를 사용해 질의와 참조 문서 간 관련성 판단
        
        Args:
            query: 사용자 질의
            documents: 참조 문서 내용 목록
            
        Returns:
            RelevanceResult: 관련성 판단 결과
        """
        print("🤖 AI 관련성 판단 중...")
        result = await self.relevance_judge.judge_relevance(query, documents)
        print(f"📊 관련성 판단 결과: {result.has_relevant_content} (신뢰도: {result.confidence:.2f})")
        print(f"💭 판단 근거: {result.reasoning}")
        return result
    
    async def _generate_conditional_response(self, query: str, documents: List[str], 
                                           has_relevant_content: bool) -> str:
        """
        관련성 판단 결과에 따른 조건부 응답 생성
        
        Args:
            query: 사용자 질의
            documents: 참조 문서 목록
            has_relevant_content: 관련성 판단 결과
            
        Returns:
            str: 생성된 응답
        """
        if not self.ai_client:
            return "AI 클라이언트가 초기화되지 않아 응답을 생성할 수 없습니다."
        
        try:
            if has_relevant_content:
                # 참조 문서 기반 응답
                print("📄 참조 문서 기반 응답 생성 중...")
                documents_text = "\n\n".join([
                    f"=== 참조문서 {i+1} ===\n{doc}" 
                    for i, doc in enumerate(documents)
                ])
                prompt = DOCUMENT_BASED_PROMPT.format(
                    query=query,
                    documents=documents_text
                )
            else:
                # 사전 지식 기반 응답
                print("🧠 사전 지식 기반 응답 생성 중...")
                prompt = KNOWLEDGE_BASED_PROMPT.format(query=query)
            
            response = await self.ai_client.generate_async(prompt)
            return response
            
        except Exception as e:
            return f"응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    async def process_single_query_with_relevance(self, query: str, 
                                                reference_documents: List[str]) -> Dict[str, Any]:
        """
        단일 질의에 대한 관련성 판단 + 조건부 응답 생성
        
        Args:
            query: 사용자 질의
            reference_documents: 참조 문서 내용 목록
            
        Returns:
            Dict: 처리 결과 (model_response, has_relevant_content 포함)
        """
        start_time = datetime.now()
        
        try:
            # 1단계: 관련성 판단
            relevance_result = await self._judge_relevance(query, reference_documents)
            
            # 2단계: 조건부 응답 생성
            model_response = await self._generate_conditional_response(
                query, reference_documents, relevance_result.has_relevant_content
            )
            
            elapsed_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'query': query,
                'model_response': model_response,
                'has_relevant_content': relevance_result.has_relevant_content,
                'relevance_reasoning': relevance_result.reasoning,
                'relevance_confidence': relevance_result.confidence,
                'elapsed_time': elapsed_time,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            elapsed_time = (datetime.now() - start_time).total_seconds()
            return {
                'query': query,
                'model_response': f"처리 중 오류가 발생했습니다: {str(e)}",
                'has_relevant_content': False,
                'relevance_reasoning': f"오류로 인한 판단 불가: {str(e)}",
                'relevance_confidence': 0.0,
                'elapsed_time': elapsed_time,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            }
    
    async def process_query_enhanced(self, query: str, folder_path: str) -> Dict[str, Any]:
        """
        관련성 판단 기능이 추가된 전체 질의 처리 프로세스
        (기존 process_query 메서드의 확장 버전)
        
        Args:
            query: 사용자 질의
            folder_path: 참조 문서가 있는 폴더 경로
            
        Returns:
            Dict: 처리 결과 (각 문서별로 관련성 판단 + 조건부 응답 포함)
        """
        try:
            print(f"🚀 관련성 판단 기능이 포함된 질의 처리 시작")
            print(f"📝 질의: {query}")
            print(f"📂 폴더: {folder_path}")
            
            # 1. 폴더 내 파일 읽기
            files_data = self._read_folder_files(folder_path)
            print(f"📚 읽은 파일 수: {len(files_data)}")
            
            # 2. 각 문서별로 관련성 판단 + 조건부 응답 생성
            enhanced_results = []
            for i, file_data in enumerate(files_data):
                print(f"\n=== 문서 {i+1}/{len(files_data)}: {file_data['name']} ===")
                
                result = await self.process_single_query_with_relevance(
                    query, [file_data['content']]
                )
                
                # 문서 정보 추가
                result['document_name'] = file_data['name']
                result['document_path'] = file_data['path']
                
                enhanced_results.append(result)
                
                # 결과 요약 출력
                status = "✅" if result['has_relevant_content'] else "❌"
                print(f"{status} 관련성: {result['has_relevant_content']}")
                print(f"⏱️ 처리 시간: {result['elapsed_time']:.2f}초")
            
            # 3. 전체 결과 요약
            relevant_count = sum(1 for r in enhanced_results if r['has_relevant_content'])
            
            return {
                'query': query,
                'folder_path': folder_path,
                'total_documents': len(files_data),
                'relevant_documents': relevant_count,
                'irrelevant_documents': len(files_data) - relevant_count,
                'enhanced_results': enhanced_results,
                'processing_timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            return {
                'query': query,
                'folder_path': folder_path,
                'error': str(e),
                'processing_timestamp': datetime.now().isoformat(),
                'success': False
            }

# 프롬프트 템플릿들
RELEVANCE_JUDGMENT_PROMPT = """
다음 사용자 질의와 참조 문서들을 분석하여 관련성을 판단해주세요.

사용자 질의: {query}

참조 문서들:
{documents}

작업 단계:
1. 사용자 질의의 핵심 키워드와 의도를 파악하세요
2. 각 참조 문서에서 질의와 관련된 내용이 있는지 확인하세요  
3. 관련 내용이 하나라도 있으면 true, 전혀 없으면 false로 판단하세요
4. 판단 근거를 명확히 제시하세요
5. 신뢰도를 0.0~1.0 사이로 평가하세요

JSON 형식으로만 응답하세요:
{{"has_relevant_content": true 또는 false, "reasoning": "판단 근거", "confidence": 0.0~1.0}}
"""

DOCUMENT_BASED_PROMPT = """
다음 참조 문서의 내용을 바탕으로 사용자 질의에 답변해주세요.

사용자 질의: {query}

{documents}

참조 문서의 내용만을 근거로 정확하고 구체적으로 답변해주세요.
문서에서 직접 언급되지 않은 내용은 추가하지 마세요.
"""

KNOWLEDGE_BASED_PROMPT = """
다음 질의에 대해 당신의 사전 지식을 바탕으로 답변해주세요.

사용자 질의: {query}

일반적인 지식과 경험을 바탕으로 도움이 되는 답변을 제공해주세요.
참조할 문서가 없으므로 당신이 학습한 내용을 기반으로 답변하세요.
"""

# CLI 실행 함수
async def main():
    """개선된 CLI 실행 함수"""
    import sys
    
    if len(sys.argv) < 3:
        print("사용법: python query_processor_v2.py '<질의문>' <폴더_경로>")
        print("예시: python query_processor_v2.py '이 문서의 핵심 내용이 뭐야?' ./references")
        return
    
    query = sys.argv[1]
    folder_path = sys.argv[2]
    
    processor = QueryProcessor()
    result = await processor.process_query_enhanced(query, folder_path)
    
    if result['success']:
        print(f"\n=== 🎯 처리 완료 ===")
        print(f"📊 총 문서: {result['total_documents']}개")
        print(f"✅ 관련 문서: {result['relevant_documents']}개") 
        print(f"❌ 무관 문서: {result['irrelevant_documents']}개")
        print(f"⏱️ 처리 시각: {result['processing_timestamp']}")
        
        print(f"\n=== 📋 개별 결과 요약 ===")
        for i, res in enumerate(result['enhanced_results']):
            status = "✅ 관련" if res['has_relevant_content'] else "❌ 무관"
            print(f"{i+1}. {res['document_name']}: {status}")
    else:
        print(f"\n=== ❌ 처리 실패 ===")
        print(f"오류: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())