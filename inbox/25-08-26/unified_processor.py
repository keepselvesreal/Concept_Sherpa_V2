# 목차
# 생성 시간: 2025-08-26 15:26:50 KST
# 핵심 내용: 통합 질의응답 처리 오케스트레이터 - 직접 임포트를 통한 병렬 실행 및 결과 통합
# 상세 내용:
#   - UnifiedProcessor 클래스 (33-310): 메인 통합 처리 시스템 및 직접 함수 호출
#   - ResultCollector 클래스 (313-340): 결과 수집 및 통합
#   - setup_logging() 함수 (343-373): 통합 로깅 시스템
#   - main() 함수 (376-429): CLI 인터페이스
# 상태: active
# 주소: unified_processor
# 참조: session_manager.py, output_formatter.py, 각 프로세서 직접 임포트

import argparse
import asyncio
import json
import logging
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple

from session_manager import SessionCacheManager, SessionManager
from output_formatter import OutputFormatter, display_error

# 각 프로세서 직접 임포트
from session_query_processor import SessionQueryProcessor
from individual_document_processor import IndividualDocumentProcessor
from supplementary_context_analyzer import analyze_supplementary_context


class UnifiedProcessor:
    """통합 질의응답 처리 시스템"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self.script_dir = Path(__file__).parent
        
        # 로깅 설정
        self.logger = setup_logging(self.config)
        
        # 컴포넌트 초기화
        self.session_cache_manager = SessionCacheManager(self.script_dir, self.logger)
        self.session_manager = SessionManager(self.script_dir, self.config, self.logger)
        self.result_collector = ResultCollector(self.config, self.logger)
        self.output_formatter = OutputFormatter(self.config, self.logger)
        
        # 각 프로세서 직접 초기화
        self.session_processor = SessionQueryProcessor(config_path=str(self.script_dir / "config.yaml"))
        self.individual_processor = IndividualDocumentProcessor(config_path=str(self.script_dir / "config.yaml"))
        
        self.logger.info("UnifiedProcessor 초기화 완료")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ 설정 파일 파싱 오류: {e}")
            sys.exit(1)
    
    async def process_query(self, query: str, force_new_session: bool = False, 
                           session_id: str = None) -> Dict[str, Any]:
        """통합 질의 처리 메인 함수"""
        try:
            self.logger.info(f"통합 질의 처리 시작: {query[:50]}...")
            
            # ===== 1단계: session_query_processor 실행 (세션 관리 포함) =====
            self.output_formatter.display_progress_message("🤖 세션 및 질의 처리 중...")
            session_result = await self._run_session_processor(
                query, force_new_session, session_id
            )
            
            if not session_result['success']:
                return session_result
            
            # 세션 정보 추출
            current_session_id = session_result['session_id']
            query_number = session_result['query_number']
            
            self.logger.info(f"세션 처리 완료: ID={current_session_id[:20]}..., 질의번호={query_number}")
            
            # ===== 2단계: 나머지 프로세서들 병렬 실행 =====
            self.output_formatter.display_progress_message("⚡ 개별/보충 분석 병렬 처리...")
            other_results = await self._run_parallel_processors(
                query, current_session_id, query_number
            )
            
            # 결과 통합
            all_results = {
                'session_query_processor': session_result,
                **other_results
            }
            
            # ===== 3단계: 결과 수집 및 통합 =====
            self.output_formatter.display_progress_message("📊 결과 통합 중...")
            integrated_results = self.result_collector.integrate_results(
                query, current_session_id, query_number, all_results
            )
            
            # ===== 4단계: 통합 결과 출력 =====
            await self._display_integrated_results(integrated_results)
            
            self.logger.info("통합 질의 처리 완료")
            
            return {
                'success': True,
                'session_id': current_session_id,
                'query_number': query_number,
                'query': query,
                'results': integrated_results
            }
            
        except Exception as e:
            self.logger.error(f"통합 질의 처리 오류: {str(e)}")
            display_error(f"처리 중 오류가 발생했습니다: {str(e)}", self.config)
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _run_session_processor(self, query: str, force_new_session: bool, session_id: str) -> Dict[str, Any]:
        """session_query_processor 실행 (세션 관리 포함)"""
        start_time = time.time()
        try:
            if force_new_session:
                # 새 세션 시작
                result = await self.session_processor.process_first_query(
                    query=query
                )
            elif session_id:
                # 수동 세션 ID로 재개
                cached_session = self.session_cache_manager.load_current_session()
                if cached_session and cached_session.get('session_id'):
                    query_number = cached_session.get('query_number', 1) + 1
                else:
                    query_number = 1
                    
                result = await self.session_processor.process_resume_query(
                    query=query,
                    session_id=session_id,
                    query_number=query_number
                )
            else:
                # 자동 감지: 캐시 확인
                cached_session = self.session_cache_manager.load_current_session()
                if cached_session and cached_session.get('session_id'):
                    # 기존 세션 재개
                    session_id = cached_session['session_id']
                    query_number = cached_session.get('query_number', 1) + 1
                    result = await self.session_processor.process_resume_query(
                        query=query,
                        session_id=session_id,
                        query_number=query_number
                    )
                else:
                    # 새 세션 시작
                    result = await self.session_processor.process_first_query(
                        query=query
                    )
            
            result['elapsed_time'] = time.time() - start_time
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }
    
    async def _run_parallel_processors(self, query: str, session_id: str, query_number: int) -> Dict[str, Any]:
        """나머지 프로세서들 병렬 실행 (individual + supplementary)"""
        functions = []
        
        # 1. individual_document_processor (항상 실행)
        functions.append(
            self._call_individual_processor(query, session_id, query_number)
        )
        
        # 2. supplementary_context_analyzer (질의 번호 >= 2일 때만 실행)
        if query_number >= 2:
            functions.append(
                self._call_supplementary_analyzer(query, session_id, query_number)
            )
            self.logger.info("보충 분석 함수 포함 - 질의 번호 >= 2")
        else:
            self.logger.info("보충 분석 함수 제외 - 첫 번째 질의")
        
        # 병렬 실행
        self.logger.info(f"{len(functions)}개 프로세서 병렬 실행 시작")
        results = await asyncio.gather(*functions, return_exceptions=True)
        
        # 결과 정리
        function_names = ['individual_document_processor']
        if query_number >= 2:
            function_names.append('supplementary_context_analyzer')
        
        function_results = {}
        for name, result in zip(function_names, results):
            if isinstance(result, Exception):
                self.logger.error(f"{name} 실행 오류: {result}")
                function_results[name] = {
                    'success': False,
                    'error': str(result),
                    'elapsed_time': 0.0
                }
            else:
                function_results[name] = result
                status = "성공" if result.get('success', False) else "실패"
                self.logger.info(f"{name} 완료 - {status}")
        
        return function_results
    
    async def _call_individual_processor(self, query: str, session_id: str, query_number: int):
        """IndividualDocumentProcessor.process_individual_documents 호출"""
        start_time = time.time()
        try:
            result = await self.individual_processor.process_individual_documents(
                query=query,
                session_id=session_id,
                query_number=query_number
            )
            result['elapsed_time'] = time.time() - start_time
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }
    
    async def _call_supplementary_analyzer(self, query: str, session_id: str, query_number: int):
        """supplementary_context_analyzer.analyze_supplementary_context 호출"""
        start_time = time.time()
        try:
            result = await analyze_supplementary_context(
                current_query=query,
                session_id=session_id,
                query_number=query_number,
                config_path=str(self.script_dir / "config.yaml"),
                verbose=False
            )
            result['elapsed_time'] = time.time() - start_time
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }
    
    async def _display_integrated_results(self, results: Dict[str, Any]):
        """통합 결과 출력"""
        self.output_formatter.display_header("🎯 통합 처리 결과", style="bold green")
        
        # 기본 정보
        info_dict = {
            "🆔 세션 ID": results['session_id'],
            "🔢 질의 번호": results['query_number'],
            "📝 질의": results['query'][:100] + "..." if len(results['query']) > 100 else results['query']
        }
        self.output_formatter.display_info_panel(info_dict, "📋 기본 정보")
        
        # 각 프로세스 결과 요약
        process_results = results.get('process_results', {})
        
        summary_data = []
        for process_name, result in process_results.items():
            status = "✅ 성공" if result.get('success', False) else "❌ 실패"
            summary_data.append({
                "프로세스": process_name,
                "상태": status,
                "처리 시간": f"{result.get('elapsed_time', 0.0):.2f}초"
            })
        
        if summary_data:
            self.output_formatter.display_table(
                summary_data, 
                ["프로세스", "상태", "처리 시간"], 
                "📊 프로세스 실행 결과"
            )
        
        # 성공한 결과들의 상세 내용 출력
        successful_results = {k: v for k, v in process_results.items() if v.get('success', False)}
        
        if successful_results:
            self.output_formatter.console.print("\n")
            self.output_formatter.display_header("📄 상세 결과", style="bold blue")
            
            for process_name, result in successful_results.items():
                if result.get('response') or result.get('relevant_responses'):
                    self.output_formatter.display_message(f"\n🔹 {process_name} 결과:", style="bold cyan")
                    
                    # 응답 내용이 있으면 표시
                    if result.get('response'):
                        response_text = self._extract_clean_response(result['response'])
                        self.output_formatter.display_response_panel(
                            response_text, 
                            f"💬 {process_name} 응답"
                        )
                    
                    # 관련 응답들이 있으면 표시 (individual_document_processor)
                    if result.get('relevant_responses'):
                        for resp in result['relevant_responses'][:2]:  # 최대 2개만 표시
                            self.output_formatter.display_response_panel(
                                resp.get('response', ''), 
                                f"📄 {resp.get('document_name', 'Unknown')}"
                            )
    
    def _extract_clean_response(self, response_data: str) -> str:
        """JSON 문자열로 중첩된 응답에서 실제 내용 추출"""
        try:
            # JSON 문자열인지 확인하고 파싱
            if isinstance(response_data, str) and response_data.strip().startswith('{'):
                parsed = json.loads(response_data)
                # model_response 필드가 있으면 그것을 사용
                if 'model_response' in parsed:
                    return parsed['model_response']
                # response 필드가 있으면 그것을 사용
                elif 'response' in parsed:
                    return parsed['response']
            
            # JSON이 아니거나 파싱할 수 없으면 원본 반환
            return response_data
            
        except (json.JSONDecodeError, TypeError, KeyError):
            # 파싱 실패 시 원본 반환
            return response_data


class ResultCollector:
    """결과 수집 및 통합 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def integrate_results(self, query: str, session_id: str, query_number: int, 
                         process_results: Dict[str, Any]) -> Dict[str, Any]:
        """프로세스 결과들을 통합"""
        integrated = {
            'query': query,
            'session_id': session_id,
            'query_number': query_number,
            'timestamp': datetime.now().isoformat(),
            'process_results': process_results,
            'summary': self._create_summary(process_results)
        }
        
        self.logger.info("결과 통합 완료")
        return integrated
    
    def _create_summary(self, process_results: Dict[str, Any]) -> Dict[str, Any]:
        """결과 요약 생성"""
        total_processes = len(process_results)
        successful_processes = sum(1 for result in process_results.values() if result.get('success', False))
        total_elapsed = sum(result.get('elapsed_time', 0.0) for result in process_results.values())
        
        return {
            'total_processes': total_processes,
            'successful_processes': successful_processes,
            'failed_processes': total_processes - successful_processes,
            'total_elapsed_time': round(total_elapsed, 2),
            'success_rate': round(successful_processes / total_processes * 100, 1) if total_processes > 0 else 0
        }


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """통합 로깅 시스템 설정"""
    log_config = config.get('logging', {})
    log_dir = Path(log_config.get('file_path', './logs/unified_processor.log')).parent
    log_dir.mkdir(exist_ok=True)
    
    # 기본 로거 설정
    logger = logging.getLogger('unified_processor')
    logger.setLevel(getattr(logging, log_config.get('level', 'INFO')))
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러
    file_handler = logging.FileHandler(log_config.get('file_path', './logs/unified_processor.log'))
    file_handler.setLevel(logging.DEBUG)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포맷터
    formatter = logging.Formatter(
        log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


async def main():
    """CLI 인터페이스 메인 함수"""
    parser = argparse.ArgumentParser(
        description="통합 질의응답 처리 시스템",
        epilog="""
사용 예시:
  첫 번째 질의: python unified_processor.py "데이터 지향 프로그래밍의 특징은?"
  자동 재개:   python unified_processor.py "더 자세한 예시를 들어줘"
  새 세션:     python unified_processor.py "새로운 주제로 시작" --new-session
  수동 재개:   python unified_processor.py "질문" --session-id abc123-def456
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('query', help='처리할 질의문')
    parser.add_argument('--session-id', help='재개할 세션 ID (수동 지정)')
    parser.add_argument('--new-session', action='store_true', help='강제로 새 세션 시작')
    parser.add_argument('--config', default='./config.yaml', help='설정 파일 경로')
    
    args = parser.parse_args()
    
    try:
        # UnifiedProcessor 초기화 및 실행
        processor = UnifiedProcessor(args.config)
        
        result = await processor.process_query(
            query=args.query,
            force_new_session=args.new_session,
            session_id=args.session_id
        )
        
        # 결과에 따른 종료 코드 설정
        sys.exit(0 if result['success'] else 1)
        
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())