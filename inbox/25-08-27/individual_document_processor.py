# 생성 시간: 2025-08-26 12:37:31 KST
# 핵심 내용: 참조 문서별 개별 답변 생성 시스템 - 기존 세션 캐시 활용
# 상세 내용:
#   - IndividualDocumentProcessor 클래스 (43-186): 메인 처리 시스템
#   - SessionCacheLoader 클래스 (188-248): 세션 캐시 읽기 전용 로더
#   - DocumentProcessor 클래스 (250-316): 개별 문서 처리
#   - ParallelProcessor 클래스 (318-383): 병렬 처리 관리
#   - main() 함수 (385-420): CLI 인터페이스
# 상태: active
# 주소: individual_document_processor
# 참조: session_query_processor.py, query_processor_v2.py

import asyncio
import json
import logging
import os
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from common_utils import find_session_folder

try:
    from claude_code_sdk import ClaudeCodeOptions, query as claude_query
except ImportError as e:
    print(f"❌ claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    sys.exit(1)

# Rich 라이브러리 임포트 (화면 출력용)
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

@dataclass
class DocumentResult:
    """개별 문서 처리 결과"""
    document_name: str
    document_path: str
    query: str
    model_response: str
    has_relevant_content: bool
    elapsed_time: float
    timestamp: str
    success: bool
    error: Optional[str] = None

class IndividualDocumentProcessor:
    """참조 문서별 개별 답변 생성 시스템"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self.script_dir = Path(__file__).parent
        
        # 컴포넌트 초기화
        self.cache_loader = SessionCacheLoader(self.script_dir)
        self.doc_processor = DocumentProcessor(self.config)
        self.parallel_processor = ParallelProcessor(self.config)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}")
            # 기본 설정 사용
            return {
                'references': {
                    'folder_path': './references',
                    'supported_extensions': ['.md', '.txt'],
                    'exclude_patterns': ['.*']
                }
            }
        except yaml.YAMLError as e:
            print(f"❌ 설정 파일 파싱 오류: {e}")
            sys.exit(1)
    
    async def process_individual_documents(self, query: str, session_id: str = None, query_number: int = None) -> Dict[str, Any]:
        """개별 문서별 답변 생성 메인 프로세스"""
        try:
            print(f"🚀 개별 문서 처리 시작")
            print(f"📝 질의: {query}")
            
            # 매개변수로만 처리 (세션 관리는 앞단에서 완료됨)
            if not session_id:
                raise ValueError("session_id가 필수 매개변수입니다. 통합 프로세서에서 세션 관리가 먼저 이루어져야 합니다.")
            if query_number is None:
                raise ValueError("query_number가 필수 매개변수입니다. 통합 프로세서에서 세션 관리가 먼저 이루어져야 합니다.")
            
            current_session_id = session_id
            current_query_number = query_number
            print(f"📋 매개변수 사용: 세션 ID={session_id[:20]}..., 질의 번호={query_number}")
            
            # 2. 세션 폴더 찾기
            session_folder = find_session_folder(current_session_id, self.config, __file__)
            if not session_folder:
                raise ValueError(f"세션 폴더를 찾을 수 없습니다: {current_session_id}")
            
            print(f"📁 세션 폴더: {session_folder.name}")
            
            # 3. 참조 문서 수집
            documents = await self._collect_reference_documents()
            if not documents:
                raise ValueError("참조 문서를 찾을 수 없습니다.")
            
            print(f"📚 참조 문서 수: {len(documents)}개")
            
            # 4. 병렬 처리로 각 문서별 답변 생성
            print(f"⚡ 병렬 처리 시작...")
            results = await self.parallel_processor.process_documents_parallel(
                query, documents, current_query_number
            )
            
            # 5. 결과를 세션 폴더에 저장
            save_results = await self._save_results_to_session_folder(
                session_folder, results, current_query_number
            )
            
            # 6. 결과 요약
            successful_count = sum(1 for r in results if r.success)
            relevant_count = sum(1 for r in results if r.has_relevant_content)
            
            print(f"\n✅ 처리 완료!")
            print(f"📊 총 문서: {len(results)}개")
            print(f"✅ 성공: {successful_count}개")
            print(f"📄 관련 문서: {relevant_count}개")
            print(f"💾 저장 위치: {session_folder}")
            
            # 7. has_relevant_content가 true인 문서의 응답은 unified_processor에서 통합 표시
            # await self._display_relevant_responses(query, results)  # 비활성화
            
            return {
                'success': True,
                'session_id': current_session_id,
                'query_number': current_query_number,
                'session_folder': str(session_folder),
                'total_documents': len(results),
                'successful_documents': successful_count,
                'relevant_documents': relevant_count,
                'results': [
                    {
                        'document_name': r.document_name,
                        'success': r.success,
                        'has_relevant_content': r.has_relevant_content,
                        'elapsed_time': r.elapsed_time
                    } for r in results
                ],
                'save_results': save_results
            }
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _collect_reference_documents(self) -> List[Dict[str, str]]:
        """참조 문서 수집"""
        ref_config = self.config.get('references', {})
        folder_path = Path(ref_config.get('folder_path', './references'))
        
        if not folder_path.is_absolute():
            folder_path = self.script_dir / folder_path
        
        if not folder_path.exists():
            raise FileNotFoundError(f"참조 폴더가 존재하지 않습니다: {folder_path}")
        
        documents = []
        supported_extensions = ref_config.get('supported_extensions', ['.md', '.txt'])
        exclude_patterns = ref_config.get('exclude_patterns', ['.*'])
        
        for file_path in folder_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if file_path.suffix not in supported_extensions:
                continue
            
            if any(file_path.match(pattern) for pattern in exclude_patterns):
                continue
            
            try:
                content = await self._read_file_content(file_path)
                documents.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'content': content
                })
            except Exception as e:
                print(f"⚠️ 파일 읽기 실패: {file_path.name} - {e}")
                continue
        
        return documents
    
    async def _read_file_content(self, file_path: Path) -> str:
        """파일 내용 읽기 (다중 인코딩 지원)"""
        encodings = ['utf-8', 'cp949', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        raise UnicodeDecodeError(f"지원하지 않는 인코딩: {file_path}")
    
    async def _save_results_to_session_folder(self, session_folder: Path, 
                                           results: List[DocumentResult], 
                                           query_number: int) -> List[str]:
        """결과를 세션 폴더에 저장"""
        save_results = []
        
        for result in results:
            # 파일명에서 확장자 제거
            doc_name_without_ext = Path(result.document_name).stem
            filename = f"individual_{query_number}_{doc_name_without_ext}_answer.json"
            file_path = session_folder / filename
            
            save_data = {
                'query_number': query_number,
                'query': result.query,
                'model_response': result.model_response,
                'has_relevant_content': result.has_relevant_content,
                'elapsed_time': result.elapsed_time,
                'timestamp': result.timestamp,
                'document_path': result.document_path,
                'success': result.success
            }
            
            if result.error:
                save_data['error'] = result.error
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                save_results.append(str(file_path))
                print(f"💾 저장: {filename}")
            except Exception as e:
                print(f"❌ 저장 실패: {filename} - {e}")
        
        return save_results
    
    async def _display_relevant_responses(self, query: str, results: List[DocumentResult]):
        """has_relevant_content가 true인 문서들의 응답을 화면에 출력"""
        relevant_results = [r for r in results if r.has_relevant_content and r.success]
        
        if not relevant_results:
            console.print("\n📭 관련성이 있는 응답이 없습니다.", style="yellow")
            return
        
        # 질의 내용 표시
        console.print("\n" + "═" * 80, style="bold yellow")
        console.print("🎯 관련성이 있는 문서들의 응답", style="bold yellow")
        console.print("═" * 80, style="bold yellow")
        
        query_panel = Panel(
            query,
            title="🔍 질의 내용",
            title_align="left",
            border_style="bold blue"
        )
        console.print(query_panel)
        console.print()
        
        # 각 관련 문서의 응답 출력
        for i, result in enumerate(relevant_results):
            # 문서명을 작게 표시 (덜 강조)
            doc_name_without_ext = Path(result.document_name).stem
            console.print(f"📄 {result.document_name} ({result.elapsed_time:.1f}초)", style="dim white")
            console.print()
            
            # 응답 내용을 강조된 패널로 표시
            response_panel = Panel(
                Markdown(result.model_response),
                title="💬 응답 내용",
                title_align="left",
                border_style="bold green",
                padding=(1, 2)
            )
            console.print(response_panel)
            
            # 마지막이 아니면 구분선 표시
            if i < len(relevant_results) - 1:
                console.print("─" * 80, style="dim")
                console.print()
        
        console.print(f"\n✨ 관련성 있는 응답은 {len(relevant_results)}개입니다.", style="bold green")

class SessionCacheLoader:
    """세션 캐시 읽기 전용 로더"""
    
    def __init__(self, script_dir: Path):
        self.script_dir = script_dir
        self.cache_file = script_dir / '.session_cache.json'
    
    def load_session_cache(self) -> Optional[Dict[str, Any]]:
        """세션 캐시 파일 읽기 (읽기 전용)"""
        try:
            if not self.cache_file.exists():
                print("❌ 세션 캐시 파일이 없습니다.")
                return None
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            print(f"✅ 세션 캐시 로드 완료")
            return cache_data
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ 세션 캐시 로드 오류: {e}")
            return None
        except Exception as e:
            print(f"❌ 예상치 못한 캐시 로드 오류: {e}")
            return None
    

class DocumentProcessor:
    """개별 문서 처리 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def process_single_document(self, query: str, document: Dict[str, str]) -> DocumentResult:
        """단일 문서에 대한 답변 생성"""
        start_time = time.time()
        
        try:
            # 관련성 판단 포함 프롬프트
            prompt = f"""다음 사용자 질의와 참조 문서를 분석하여 답변해주세요.

사용자 질의: {query}

참조 문서: {document['name']}
{document['content']}

작업:
1. 먼저 참조 문서에 질의와 관련된 내용이 있는지 판단하세요
2. 관련 내용이 있으면 문서를 바탕으로 정확하고 구체적으로 답변하세요
3. 관련 내용이 없으면 "관련 내용 없음"으로 답변하세요

**중요 - 출처 표시 규칙:**
- 참조한 내용의 출처를 반드시 [라인번호] 형식으로 표시하세요
- 단일 라인: [5] 
- 연속 구간: [10-15]
- 여러 구간: [5], [12-15], [20]
- 답변 내용에서 참조한 모든 내용에 출처를 명시하세요

응답 형식은 다음 JSON 구조로 작성해주세요:
{{
    "has_relevant_content": true 또는 false,
    "model_response": "실제 답변 내용 (출처 표시 포함)"
}}"""

            # Claude SDK로 질의 처리
            responses = []
            
            async for message in claude_query(prompt=prompt):
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                    elif hasattr(content, 'text'):
                        responses.append(content.text)
                    else:
                        responses.append(str(content))
            
            elapsed_time = time.time() - start_time
            raw_response = '\n'.join(responses) if responses else ''
            
            # JSON 응답 파싱
            try:
                import re
                json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{[^{}]*"has_relevant_content"[^{}]*\})', 
                                     raw_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1) or json_match.group(2)
                    parsed_response = json.loads(json_str)
                    
                    return DocumentResult(
                        document_name=document['name'],
                        document_path=document['path'],
                        query=query,
                        model_response=parsed_response.get('model_response', raw_response),
                        has_relevant_content=parsed_response.get('has_relevant_content', False),
                        elapsed_time=elapsed_time,
                        timestamp=datetime.now().isoformat(),
                        success=True
                    )
                else:
                    # JSON 파싱 실패 시 키워드 추출
                    has_relevant = 'true' in raw_response.lower() and 'has_relevant_content' in raw_response.lower()
                    return DocumentResult(
                        document_name=document['name'],
                        document_path=document['path'],
                        query=query,
                        model_response=raw_response,
                        has_relevant_content=has_relevant,
                        elapsed_time=elapsed_time,
                        timestamp=datetime.now().isoformat(),
                        success=True
                    )
                    
            except (json.JSONDecodeError, AttributeError):
                return DocumentResult(
                    document_name=document['name'],
                    document_path=document['path'],
                    query=query,
                    model_response=raw_response,
                    has_relevant_content=False,
                    elapsed_time=elapsed_time,
                    timestamp=datetime.now().isoformat(),
                    success=True
                )
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            return DocumentResult(
                document_name=document['name'],
                document_path=document['path'],
                query=query,
                model_response=f'문서 처리 중 오류가 발생했습니다: {str(e)}',
                has_relevant_content=False,
                elapsed_time=elapsed_time,
                timestamp=datetime.now().isoformat(),
                success=False,
                error=str(e)
            )

class ParallelProcessor:
    """병렬 처리 관리 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.doc_processor = DocumentProcessor(config)
        self.max_concurrent = config.get('parallel', {}).get('max_concurrent', 5)
    
    async def process_documents_parallel(self, query: str, documents: List[Dict[str, str]], 
                                       query_number: int) -> List[DocumentResult]:
        """문서들을 병렬로 처리"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_with_semaphore(doc: Dict[str, str]) -> DocumentResult:
            async with semaphore:
                print(f"🔄 처리 중: {doc['name']}")
                result = await self.doc_processor.process_single_document(query, doc)
                status = "✅" if result.success else "❌"
                relevance = "관련" if result.has_relevant_content else "무관"
                print(f"{status} 완료: {doc['name']} ({relevance}, {result.elapsed_time:.1f}초)")
                return result
        
        # 병렬 실행
        tasks = [process_with_semaphore(doc) for doc in documents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 예외 처리
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                doc = documents[i]
                processed_results.append(DocumentResult(
                    document_name=doc['name'],
                    document_path=doc['path'],
                    query=query,
                    model_response=f'병렬 처리 중 오류: {str(result)}',
                    has_relevant_content=False,
                    elapsed_time=0.0,
                    timestamp=datetime.now().isoformat(),
                    success=False,
                    error=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results

async def main():
    """CLI 인터페이스"""
    import argparse
    
    parser = argparse.ArgumentParser(description='개별 문서별 답변 생성 시스템')
    parser.add_argument('query', help='처리할 질의문')
    parser.add_argument('--config', default='./config.yaml', help='설정 파일 경로')
    parser.add_argument('--query-number', type=int, help='질의 번호 (통합 프로세서에서 전달)')
    
    args = parser.parse_args()
    
    query = args.query
    config_path = args.config
    manual_query_number = args.query_number
    
    try:
        processor = IndividualDocumentProcessor(config_path)
        result = await processor.process_individual_documents(
            query, 
            session_id=None,  # CLI에서는 None, 캐시에서 읽음
            query_number=manual_query_number
        )
        
        if result['success']:
            print(f"\n🎉 전체 처리 완료!")
        else:
            print(f"\n💥 처리 실패: {result['error']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())