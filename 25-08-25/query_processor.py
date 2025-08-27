# 목차
# 생성 시간: Mon Aug 25 12:30:05 KST 2025
# 핵심 내용: Claude Code 세션 ID 기반 질의문 처리 및 개별 문서 응답 생성 시스템
# 상세 내용:
#   - SessionManager 클래스 (27-98): 세션 ID 캐시 관리 및 훅 로그 추출
#   - QueryProcessor 클래스 (100-236): 메인 클래스로 질의 처리 담당
#   - process_query() (130-200): 전체 질의 처리 프로세스 실행
#   - main() (238-258): CLI 실행 함수
# 상태: active
# 주소: query_processor
# 참조: get_session_id.py의 훅 로그 추출, document_query_processor.py의 individual_answers, understanding_gap_analyzer.py의 분석 로직

import asyncio
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

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

class SessionManager:
    """세션 ID 캐시 관리 및 훅 로그 추출"""
    
    def __init__(self, current_dir: str):
        self.current_dir = current_dir
        self.session_cache_file = os.path.join(current_dir, ".session_cache.json")
    
    def get_session_from_logs(self) -> Optional[str]:
        """훅 로그에서 최신 세션 ID 추출"""
        try:
            result = subprocess.run(['tail', '-20', '/tmp/claude_hook_debug.log'], 
                                  capture_output=True, text=True, timeout=5)
            
            # session_id 패턴 찾기 (최신 것부터)
            matches = re.findall(r'"session_id":"([^"]+)"', result.stdout)
            return matches[-1] if matches else None
        except Exception as e:
            print(f"훅 로그에서 세션 ID 추출 실패: {e}")
            return None
    
    def save_session_cache(self, session_id: str, query_number: int = 1) -> bool:
        """세션 ID 캐시 파일 저장"""
        try:
            cache_data = {
                'session_id': session_id,
                'cached_at': datetime.now().isoformat(),
                'session_prefix': session_id.split('-')[0] if '-' in session_id else session_id[:8],
                'query_number': query_number
            }
            
            with open(self.session_cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"세션 캐시 저장 실패: {e}")
            return False
    
    def load_session_cache(self) -> Optional[Dict[str, Any]]:
        """캐시에서 세션 정보 로드"""
        try:
            if not os.path.exists(self.session_cache_file):
                return None
                
            with open(self.session_cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                return cache_data
        except Exception as e:
            print(f"세션 캐시 로드 실패: {e}")
            return None
    
    def get_or_create_session_info(self) -> Dict[str, Any]:
        """훅 로그 우선으로 세션 정보 확인 및 관리"""
        # 1. 훅 로그에서 현재 세션 ID 추출
        print("훅 로그에서 현재 세션 ID 확인 중...")
        current_session_id = self.get_session_from_logs()
        
        if not current_session_id:
            # 훅 로그에서 세션 ID를 찾을 수 없는 경우 기본값 사용
            default_session = datetime.now().strftime('%H%M%S')
            print(f"훅 로그에서 세션 ID 추출 실패, 기본값 사용: {default_session}")
            self.save_session_cache(default_session, 1)
            return {
                'session_id': default_session,
                'session_prefix': default_session,
                'query_number': 1
            }
        
        # 2. 캐시된 세션 정보와 비교
        cached_info = self.load_session_cache()
        cached_session_id = cached_info.get('session_id') if cached_info else None
        
        if cached_session_id == current_session_id:
            # 같은 세션: 쿼리 번호 증가
            query_number = cached_info.get('query_number', 0) + 1
            print(f"기존 세션 계속: {current_session_id}, 쿼리 번호: {query_number}")
            self.save_session_cache(current_session_id, query_number)
            return {
                'session_id': current_session_id,
                'session_prefix': cached_info.get('session_prefix', current_session_id.split('-')[0]),
                'query_number': query_number
            }
        else:
            # 새로운 세션: 쿼리 번호 1로 초기화
            session_prefix = current_session_id.split('-')[0] if '-' in current_session_id else current_session_id[:8]
            print(f"새로운 세션 감지: {current_session_id} (이전: {cached_session_id})")
            self.save_session_cache(current_session_id, 1)
            return {
                'session_id': current_session_id,
                'session_prefix': session_prefix,
                'query_number': 1
            }

class QueryProcessor:
    """Claude Code 세션 ID 기반 질의문 처리 및 개별 문서 응답 생성 시스템"""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.chat_logs_dir = os.path.join(self.current_dir, "chat-logs")
        
        # 기존 클래스 인스턴스 생성
        self.session_manager = SessionManager(self.current_dir)
        self.doc_processor = DocumentQueryProcessor(self.current_dir)
        self.gap_analyzer = UnderstandingGapAnalyzer()
    
    def _read_folder_files(self, folder_path: str) -> List[Dict[str, str]]:
        """폴더 내 모든 파일을 읽어서 리스트로 반환"""
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"폴더가 존재하지 않습니다: {folder_path}")
        
        files_data = []
        
        # 모든 파일 검색 (숨김 파일 제외)
        for file_path in folder.glob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    # 텍스트 파일만 읽기 시도
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        files_data.append({
                            'path': str(file_path),
                            'name': file_path.name,
                            'content': content
                        })
                except UnicodeDecodeError:
                    # UTF-8 실패시 CP949 시도
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
    
    def _create_session_folder(self, session_prefix: str, query_number: int) -> str:
        """세션 폴더 생성: session_{session_prefix}_{hhmm} 형식"""
        try:
            current_time = datetime.now().strftime('%H%M')
            folder_name = f"session_{session_prefix}_{current_time}"
            folder_path = os.path.join(self.current_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            return folder_path
        except Exception as e:
            print(f"폴더 생성 실패: {e}")
            return self.current_dir
    
    def _save_individual_result(self, result_data: Dict[str, Any], folder_path: str, query_number: int, doc_filename: str) -> str:
        """개별 응답 결과 저장: individual_{query_number}_{참조문서파일명}_answer.json"""
        try:
            # 파일 확장자 제거하고 안전한 파일명으로 변환
            safe_doc_name = Path(doc_filename).stem.replace(' ', '_')
            filename = f"individual_{query_number}_{safe_doc_name}_answer.json"
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            return file_path
        except Exception as e:
            print(f"개별 결과 저장 실패: {e}")
            return ""
    
    def _find_existing_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """chat-logs에서 기존 세션 파일 검색"""
        try:
            if not os.path.exists(self.chat_logs_dir):
                return None
            
            # session_id의 첫 번째 부분 (- 앞부분) 추출
            session_prefix = session_id.split('-')[0]
            session_file = f"session_{session_prefix}.json"
            session_path = os.path.join(self.chat_logs_dir, session_file)
            
            if os.path.exists(session_path):
                with open(session_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            print(f"기존 세션 검색 실패: {e}")
            return None
    
    async def _process_understanding_gap_analysis(self, session_id: str, query_number: int, current_query: str, 
                                                 files_data: List[Dict[str, str]], session_folder: str) -> str:
        """사용자 이해도 부족 분석 및 추가 정보 생성"""
        try:
            # 기존 세션 확인
            existing_session = self._find_existing_session(session_id)
            if not existing_session:
                print("기존 세션이 없어 이해도 분석을 건너뜁니다.")
                return ""
            
            print("기존 세션 발견, 이해도 분석 진행...")
            
            # 가장 최근 질의/응답 추출
            if not ('conversations' in existing_session and existing_session['conversations']):
                print("기존 대화 내용이 없어 이해도 분석을 건너뜁니다.")
                return ""
            
            # 직전 대화 가져오기 (null 값이어도 포함)
            conversations = existing_session['conversations']
            if len(conversations) < 2:  # 최소 2개 대화 필요 (이전 + 현재)
                print("대화가 부족하여 이해도 분석을 건너뜁니다.")
                return ""
            
            last_conversation = conversations[-2]  # 현재 질문 직전 대화
            previous_query = last_conversation.get('query', '')
            previous_answer = last_conversation.get('answer', '') or "답변 없음"
            
            print(f"이해도 분석 진행: 직전 쿼리 #{last_conversation.get('query_number', 'N/A')}")
            
            import time
            start_time = time.time()
            
            # 1. 이해도 부족 분석 질의 생성
            gap_result = await self.gap_analyzer.analyze_understanding_gap(
                previous_query, previous_answer, current_query
            )
            
            if not gap_result.get('success', False):
                print(f"이해도 분석 실패: {gap_result.get('error', '')}")
                return ""
            
            understanding_gap = gap_result.get('analysis', '')
            generated_query = gap_result.get('generated_query', '')
            is_related = gap_result.get('is_related', False)
            
            # 2. 관련성이 있을 때만 참고문헌 기반 답변 생성
            answer_result = {'success': True, 'answer': '해당 사항 없음'}
            if is_related and generated_query and generated_query != '해당 사항 없음':
                combined_content = "\n\n=== 문서 구분선 ===\n\n".join([f['content'] for f in files_data])
                answer_result = await self.gap_analyzer.generate_supplementary_answer(
                    generated_query, combined_content
                )
            
            elapsed_time = round(time.time() - start_time, 2)
            
            # 3. 새로운 필드 구조로 데이터 구성
            extra_info_data = {
                'previous_query': previous_query,
                'previous_model_response': previous_answer,
                'current_query': current_query,
                'is_related': is_related,
                'understanding_gap': understanding_gap,
                'generated_query': generated_query,
                'supplementary_answer': answer_result.get('answer', '') if answer_result.get('success', False) else '',
                'elapsed_time': elapsed_time,
                'timestamp': datetime.now().isoformat(),
                'document_paths': [f['path'] for f in files_data],
                'success': answer_result.get('success', False)
            }
            
            if not answer_result.get('success', False):
                extra_info_data['error'] = answer_result.get('error', '')
            
            # 4. extra_info_{query_number} 형식으로 저장
            filename = f"extra_info_{query_number}.json"
            file_path = os.path.join(session_folder, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(extra_info_data, f, ensure_ascii=False, indent=2)
            
            print(f"이해도 분석 완료: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"이해도 분석 처리 실패: {e}")
            return ""

    async def process_query(self, query: str, folder_path: str) -> Dict[str, Any]:
        """전체 질의 처리 프로세스 실행"""
        try:
            # 1. 세션 정보 생성
            session_info = self.session_manager.get_or_create_session_info()
            session_id = session_info['session_id']
            session_prefix = session_info['session_prefix']
            query_number = session_info['query_number']
            
            print(f"세션 ID: {session_id}")
            print(f"세션 접두어: {session_prefix}")
            print(f"쿼리 번호: {query_number}")
            
            # 2. 폴더 내 파일 읽기
            print(f"폴더 읽기: {folder_path}")
            files_data = self._read_folder_files(folder_path)
            print(f"파일 개수: {len(files_data)}")
            
            # 3. 세션 폴더 생성
            session_folder = self._create_session_folder(session_prefix, query_number)
            print(f"세션 폴더: {session_folder}")
            
            # 4. 개별 응답 생성 (기존 DocumentQueryProcessor 활용)
            print("개별 응답 생성 중...")
            prompt = "다음 참고 문서를 바탕으로 질의에 대해 간결하고 정확하게 답변해주세요."
            document_list = [f['content'] for f in files_data]
            document_paths = [f['path'] for f in files_data]
            
            individual_results = await self.doc_processor.individual_answers(
                prompt, query, document_list, document_paths
            )
            
            # 5. 개별 결과를 새로운 형식으로 저장
            saved_files = []
            for i, (result, file_data) in enumerate(zip(individual_results, files_data)):
                # 결과 데이터 재구성 - 요청된 필드 구조로 변경 (has_relevant_content 포함)
                reformatted_result = {
                    'query_number': query_number,
                    'query': query,
                    'model_response': result.get('answer', ''),
                    'has_relevant_content': result.get('has_relevant_content', None),
                    'elapsed_time': result.get('elapsed_time', 0),
                    'timestamp': result.get('timestamp', ''),
                    'document_path': file_data['path'],
                    'success': result.get('success', False)
                }
                
                if not result.get('success', False):
                    reformatted_result['error'] = result.get('error', '')
                
                saved_file = self._save_individual_result(reformatted_result, session_folder, query_number, file_data['name'])
                saved_files.append(saved_file)
                reformatted_result['saved_file'] = saved_file
            
            # 6. 이해도 분석 작업 (독립적으로 실행)
            extra_info_file = await self._process_understanding_gap_analysis(
                session_id, query_number, query, files_data, session_folder
            )
            
            # 7. 최종 결과 반환
            return {
                'session_id': session_id,
                'session_prefix': session_prefix,
                'query_number': query_number,
                'query': query,
                'folder_path': folder_path,
                'files_processed': len(files_data),
                'session_folder': session_folder,
                'individual_results': individual_results,
                'saved_files': saved_files,
                'extra_info_file': extra_info_file,
                'has_existing_session': bool(extra_info_file),
                'success': True
            }
            
        except Exception as e:
            # 예외 발생시에도 가능한 경우 세션 정보를 포함
            try:
                session_info = self.session_manager.get_or_create_session_info()
                error_result = {
                    'success': False,
                    'error': str(e),
                    'query': query,
                    'folder_path': folder_path,
                    'session_id': session_info['session_id'],
                    'session_prefix': session_info['session_prefix'],
                    'query_number': session_info['query_number']
                }
            except Exception as session_error:
                # 세션 정보도 가져올 수 없는 경우 - query_number 없이 반환하고 명확한 오류 기록
                error_result = {
                    'success': False,
                    'error': f"주요 오류: {str(e)} | 세션 정보 오류: {str(session_error)} | query_number를 확정할 수 없음",
                    'query': query,
                    'folder_path': folder_path,
                    'session_error': True
                }
            
            return error_result

def main():
    """CLI 실행 함수"""
    import sys
    
    if len(sys.argv) < 3:
        print("사용법: python query_processor.py '<질의문>' <폴더_경로>")
        print("예시: python query_processor.py '이 문서의 핵심 내용이 뭐야?' ./references")
        return
    
    query = sys.argv[1]
    folder_path = sys.argv[2]
    
    async def run():
        processor = QueryProcessor()
        result = await processor.process_query(query, folder_path)
        
        if result['success']:
            print(f"\n=== 처리 완료 ===")
            print(f"세션 접두어: {result['session_prefix']}")
            print(f"쿼리 번호: {result['query_number']}")
            print(f"처리된 파일: {result['files_processed']}개")
            print(f"세션 폴더: {result['session_folder']}")
            if result['extra_info_file']:
                print(f"추가 정보 파일: {result['extra_info_file']}")
        else:
            print(f"\n=== 처리 실패 ===")
            print(f"오류: {result['error']}")
            if 'query_number' in result:
                print(f"쿼리 번호: {result['query_number']}")
            if result.get('session_error'):
                print("⚠️ 세션 정보를 확정할 수 없어 쿼리 번호가 누락됨")
    
    asyncio.run(run())

if __name__ == "__main__":
    main()