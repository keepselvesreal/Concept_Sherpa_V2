# 목차
# 생성 시간: 2025-08-26 20:45:30 KST
# 핵심 내용: 통합 질의응답 처리 오케스트레이터 v2 - 통합 로깅 및 출력 분리 적용
# 상세 내용:
#   - UnifiedProcessor 클래스 (33-310): 메인 통합 처리 시스템 및 통합 로깅
#   - ResultCollector 클래스 (313-340): 결과 수집 및 통합
#   - setup_logging() 함수 (343-373): 파일 전용 로깅 시스템 (콘솔 핸들러 제거)
#   - main() 함수 (376-429): CLI 인터페이스
# 상태: active
# 주소: unified_processor_v2
# 참조: unified_processor.py (통합 로깅 및 출력 분리 적용)

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
    """통합 질의응답 처리 시스템 v2 - 통합 로깅 및 출력 분리"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self.script_dir = Path(__file__).parent
        
        # 통합 로깅 설정 (파일 전용)
        self.logger = setup_logging(self.config)
        
        # 컴포넌트 초기화
        self.session_cache_manager = SessionCacheManager(self.script_dir, self.logger)
        self.session_manager = SessionManager(self.script_dir, self.config, self.logger)
        self.result_collector = ResultCollector(self.config, self.logger)
        self.output_formatter = OutputFormatter(self.config, self.logger)
        
        # 각 프로세서 초기화 - 기존 방식 유지 (자체 로깅)
        self.session_processor = SessionQueryProcessor(
            config_path=str(self.script_dir / "config.yaml")
        )
        self.individual_processor = IndividualDocumentProcessor(
            config_path=str(self.script_dir / "config.yaml")
        )
        
        self.logger.info("UnifiedProcessor v2 초기화 완료 - 통합 로깅 적용")
    
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
            
            # ===== 4단계: 개별 문서 분석 결과 표시 =====
            await self._display_individual_document_results(all_results, query)
            
            # ===== 5단계: 보충 분석 결과 표시 (질의 번호 >= 2일 때) =====
            if query_number >= 2:
                await self._display_supplementary_results(all_results, query_number)
            
            # ===== 6단계: 통합 결과 출력 (상세 결과 섹션 제거) =====
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
    
    async def _display_individual_document_results(self, all_results: Dict[str, Any], query: str):
        """개별 문서 분석 결과 표시 - 관련성이 있는 문서들의 응답"""
        individual_result = all_results.get('individual_document_processor')
        
        if not individual_result or not individual_result.get('success', False):
            self.logger.info("개별 문서 분석 결과 없음 또는 실패")
            return
        
        # 관련성이 있는 응답만 필터링
        relevant_responses = individual_result.get('relevant_responses', [])
        
        if not relevant_responses:
            self.output_formatter.display_message("\n📭 관련성이 있는 응답이 없습니다.", style="yellow")
            return
        
        # 관련성이 있는 문서들의 응답 표시
        self.output_formatter.console.print("\n" + "═" * 80, style="bold yellow")
        self.output_formatter.console.print("🎯 관련성이 있는 문서들의 응답", style="bold yellow")
        self.output_formatter.console.print("═" * 80, style="bold yellow")
        
        # 질의 내용 표시
        from rich.panel import Panel
        query_panel = Panel(
            query,
            title="🔍 질의 내용",
            title_align="left",
            border_style="bold blue"
        )
        self.output_formatter.console.print(query_panel)
        self.output_formatter.console.print()
        
        # 각 관련 문서의 응답 출력
        for i, resp in enumerate(relevant_responses):
            # 문서명 표시
            doc_name = resp.get('document_name', 'Unknown')
            elapsed_time = resp.get('elapsed_time', 0.0)
            self.output_formatter.console.print(f"📄 {doc_name} ({elapsed_time:.1f}초)", style="dim white")
            self.output_formatter.console.print()
            
            # 응답 내용 표시
            from rich.markdown import Markdown
            response_panel = Panel(
                Markdown(resp.get('response', '')),
                title="💬 응답 내용",
                title_align="left",
                border_style="bold green",
                padding=(1, 2)
            )
            self.output_formatter.console.print(response_panel)
            
            # 마지막이 아니면 구분선
            if i < len(relevant_responses) - 1:
                self.output_formatter.console.print("─" * 80, style="dim")
                self.output_formatter.console.print()
        
        # 관련성 응답 메시지
        self.output_formatter.console.print(f"\n✨ 관련성 있는 응답은 {len(relevant_responses)}개입니다.", style="bold green")
        self.logger.info(f"개별 문서 분석 결과 표시 완료 - {len(relevant_responses)}개 응답")
    
    async def _display_supplementary_results(self, all_results: Dict[str, Any], query_number: int):
        """보충 분석 결과 표시 - description, generated_query, has_relevant_content, response만"""
        supplementary_result = all_results.get('supplementary_context_analyzer')
        
        if not supplementary_result or not supplementary_result.get('success', False):
            self.logger.info("보충 분석 결과 없음 또는 실패")
            return
        
        # JSON 구조에 맞게 outputs.supplementary_response 접근
        outputs = supplementary_result.get('outputs', {})
        relevance_analysis = outputs.get('relevance_analysis', {})
        supplementary_response = outputs.get('supplementary_response', {})
        
        if not relevance_analysis.get('is_relevant', False):
            self.logger.info("보충 분석: 이전 대화와 연관성 없음")
            return
        
        # 보충 분석 결과 표시
        self.output_formatter.display_header("🔍 이해 보충 분석", style="bold cyan")
        
        # 기본 정보 표시
        info_dict = {
            "📋 분석 설명": relevance_analysis.get('description', '설명 없음')[:150] + "..." if len(relevance_analysis.get('description', '')) > 150 else relevance_analysis.get('description', '설명 없음'),
            "🎯 생성된 질의": relevance_analysis.get('generated_query', '질의 없음'),
            "🔗 연관성": "✅ 있음" if relevance_analysis.get('is_relevant', False) else "❌ 없음"
        }
        self.output_formatter.display_info_panel(info_dict, "📊 보충 분석 정보")
        
        # 보충 응답이 있으면 표시
        if 'response' in supplementary_response and supplementary_response['response']:
            self.output_formatter.display_response_panel(
                supplementary_response['response'],
                "💬 이해 보충 응답"
            )
        
        self.logger.info("보충 분석 결과 표시 완료")
    
    async def _display_integrated_results(self, results: Dict[str, Any]):
        """통합 결과 출력 - 상세 결과 섹션 제거"""
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
        
        # 📄 상세 결과 섹션 제거됨 - 사용자 출력과 로깅 완전 분리
        self.logger.info("통합 결과 출력 완료 - 상세 결과 섹션 제거")


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
    """파일 전용 통합 로깅 시스템 설정 - 콘솔 핸들러 제거"""
    log_config = config.get('logging', {})
    log_dir = Path(log_config.get('file_path', './logs/unified_processor.log')).parent
    log_dir.mkdir(exist_ok=True)
    
    # 통합 시스템 루트 로거 설정
    logger = logging.getLogger('unified_system')
    logger.setLevel(getattr(logging, log_config.get('level', 'INFO')))
    
    # 기존 핸들러 제거 (중복 방지)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러만 추가 (콘솔 핸들러 제거)
    file_handler = logging.FileHandler(log_config.get('file_path', './logs/unified_processor_v2.log'))
    file_handler.setLevel(logging.DEBUG)
    
    # 포맷터
    formatter = logging.Formatter(
        log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    # 로거 전파 방지 (중복 방지)
    logger.propagate = False
    
    return logger


async def main():
    """CLI 인터페이스 메인 함수"""
    parser = argparse.ArgumentParser(
        description="통합 질의응답 처리 시스템 v2 - 통합 로깅 및 출력 분리",
        epilog="""
사용 예시:
  첫 번째 질의: python unified_processor_v2.py "데이터 지향 프로그래밍의 특징은?"
  자동 재개:   python unified_processor_v2.py "더 자세한 예시를 들어줘"
  새 세션:     python unified_processor_v2.py "새로운 주제로 시작" --new-session
  수동 재개:   python unified_processor_v2.py "질문" --session-id abc123-def456
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('query', help='처리할 질의문')
    parser.add_argument('--session-id', help='재개할 세션 ID (수동 지정)')
    parser.add_argument('--new-session', action='store_true', help='강제로 새 세션 시작')
    parser.add_argument('--config', default='./config.yaml', help='설정 파일 경로')
    
    args = parser.parse_args()
    
    try:
        # UnifiedProcessor v2 초기화 및 실행
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
