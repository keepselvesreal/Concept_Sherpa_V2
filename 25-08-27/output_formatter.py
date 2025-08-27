# 목차
# 생성 시간: 2025-08-26 15:26:50 KST
# 핵심 내용: CLI 출력 처리 공통 모듈 - Rich Console 기반 통합 UI/UX
# 상세 내용:
#   - OutputFormatter 클래스 (23-183): Rich Console 기반 출력 포맷터
#   - display_query_result() 함수 (185-232): 질의 결과 출력
#   - display_individual_results() 함수 (234-283): 개별 문서 결과 출력
#   - display_supplementary_results() 함수 (285-325): 보충 분석 결과 출력
#   - display_error() 함수 (327-338): 에러 메시지 출력
#   - display_progress() 함수 (340-348): 진행 상황 표시
# 상태: active
# 주소: output_formatter
# 참조: session_query_processor.py (OutputManager), individual_document_processor.py (출력 부분)

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text


class OutputFormatter:
    """Rich Console 기반 공통 출력 포맷터"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.output_config = config.get('output', {})
        self.console = Console()
        
        # 출력 활성화 여부 확인
        self.enable_console = self.output_config.get('enable_console', True)
        self.enable_progress = self.output_config.get('enable_progress', True)
    
    def display_header(self, title: str, subtitle: str = "", style: str = "bold green"):
        """헤더 출력"""
        if not self.enable_console:
            return
        
        self.console.print("\n" + "="*80, style=style)
        self.console.print(title, style=style)
        if subtitle:
            self.console.print(subtitle, style="dim")
        self.console.print("="*80, style=style)
    
    def display_query_panel(self, query: str, title: str = "🔍 질의 내용"):
        """질의 내용 패널 출력"""
        if not self.enable_console:
            return
        
        query_panel = Panel(
            query,
            title=title,
            title_align="left",
            border_style="blue"
        )
        self.console.print(query_panel)
    
    def display_info_panel(self, info_dict: Dict[str, Any], title: str = "📊 처리 정보"):
        """정보 패널 출력"""
        if not self.enable_console:
            return
        
        info_lines = []
        for key, value in info_dict.items():
            info_lines.append(f"{key}: {value}")
        
        info_text = "\n".join(info_lines)
        info_panel = Panel(
            info_text,
            title=title,
            title_align="left",
            border_style="yellow"
        )
        self.console.print(info_panel)
    
    def display_response_panel(self, response: str, title: str = "💬 응답 내용"):
        """응답 내용 패널 출력"""
        if not self.enable_console:
            return
        
        response_panel = Panel(
            Markdown(response),
            title=title,
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(response_panel)
    
    def display_table(self, data: List[Dict[str, Any]], columns: List[str], title: str = "결과 테이블"):
        """테이블 형태로 데이터 출력"""
        if not self.enable_console or not data:
            return
        
        table = Table(title=title)
        
        # 컬럼 추가
        for col in columns:
            table.add_column(col, justify="left")
        
        # 데이터 추가
        for item in data:
            row = [str(item.get(col, "")) for col in columns]
            table.add_row(*row)
        
        self.console.print(table)
    
    def display_separator(self, style: str = "dim"):
        """구분선 출력"""
        if self.enable_console:
            self.console.print("─" * 80, style=style)
    
    def display_message(self, message: str, style: str = "white"):
        """일반 메시지 출력"""
        if self.enable_console:
            self.console.print(message, style=style)
    
    def display_success(self, message: str):
        """성공 메시지 출력"""
        if self.enable_console:
            self.console.print(f"✅ {message}", style="bold green")
    
    def display_warning(self, message: str):
        """경고 메시지 출력"""
        if self.enable_console:
            self.console.print(f"⚠️ {message}", style="bold yellow")
    
    def display_error(self, message: str):
        """에러 메시지 출력"""
        if self.enable_console:
            self.console.print(f"❌ {message}", style="bold red")
    
    def display_info(self, message: str):
        """정보 메시지 출력"""
        if self.enable_console:
            self.console.print(f"ℹ️ {message}", style="cyan")
    
    def display_progress_message(self, message: str):
        """진행 상황 메시지 출력"""
        if self.enable_console and self.enable_progress:
            self.console.print(message, style="yellow")
    
    def create_progress_context(self):
        """Progress 컨텍스트 매니저 반환"""
        if self.enable_console and self.enable_progress:
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            )
        else:
            # 비활성화된 경우 더미 컨텍스트 반환
            class DummyProgress:
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def add_task(self, *args, **kwargs):
                    return 1
                def update(self, *args, **kwargs):
                    pass
            return DummyProgress()


def display_query_result(query: str, response_result: Dict[str, Any], session_id: str, 
                        document_count: int = 0, save_path: str = "", 
                        is_first_query: bool = True, config: Dict[str, Any] = None):
    """질의 결과 출력 (첫 번째 질의 및 재개 질의 공통)"""
    if config is None:
        config = {}
    
    formatter = OutputFormatter(config)
    
    # 헤더 출력
    title = "🎯 첫 번째 질의 처리 완료" if is_first_query else "🔄 세션 재개 질의 처리 완료"
    formatter.display_header(title)
    
    # 질의 내용 표시
    formatter.display_query_panel(query)
    
    # 처리 정보 구성
    info_dict = {
        "🆔 세션 ID": session_id,
        "💾 저장 위치": save_path,
        "⏱️ 처리 시간": f"{response_result.get('elapsed_time', 0.0):.2f}초"
    }
    
    if is_first_query and document_count > 0:
        info_dict["📂 참조 문서 수"] = f"{document_count}개"
    
    formatter.display_info_panel(info_dict)
    
    # 응답 내용 표시
    response_content = response_result.get('response', '응답 없음')
    formatter.display_response_panel(response_content)
    
    # 재개 명령어 안내 (첫 번째 질의인 경우)
    if is_first_query:
        formatter.display_success("세션이 생성되었습니다. 다음 명령어로 대화를 이어가세요:")
        formatter.display_message(f"python session_query_processor.py \"다음 질문\" --session-id {session_id}", style="cyan")


def display_individual_results(query: str, results: List[Dict[str, Any]], config: Dict[str, Any] = None):
    """개별 문서 처리 결과 출력"""
    if config is None:
        config = {}
    
    formatter = OutputFormatter(config)
    
    # 관련성이 있는 결과만 필터링
    relevant_results = [r for r in results if r.get('has_relevant_content', False) and r.get('success', False)]
    
    if not relevant_results:
        formatter.display_warning("관련성이 있는 응답이 없습니다.")
        return
    
    # 헤더 출력
    formatter.display_header("🎯 관련성이 있는 문서들의 응답", style="bold yellow")
    
    # 질의 내용 표시
    formatter.display_query_panel(query)
    formatter.console.print()
    
    # 각 관련 문서의 응답 출력
    for i, result in enumerate(relevant_results):
        # 문서명을 작게 표시 (덜 강조)
        doc_name_without_ext = Path(result['document_name']).stem
        elapsed_time = result.get('elapsed_time', 0.0)
        formatter.display_message(f"📄 {result['document_name']} ({elapsed_time:.1f}초)", style="dim white")
        formatter.console.print()
        
        # 응답 내용을 강조된 패널로 표시
        formatter.display_response_panel(result['model_response'])
        
        # 마지막이 아니면 구분선 표시
        if i < len(relevant_results) - 1:
            formatter.display_separator()
            formatter.console.print()
    
    formatter.display_success(f"관련성 있는 응답 {len(relevant_results)}개를 표시했습니다.")


def display_supplementary_results(analysis_result: Dict[str, Any], config: Dict[str, Any] = None):
    """보충 분석 결과 출력"""
    if config is None:
        config = {}
    
    formatter = OutputFormatter(config)
    
    formatter.display_header("🔍 보충 분석 결과", style="bold cyan")
    
    # 연관성 분석 결과
    relevance = analysis_result.get('outputs', {}).get('relevance_analysis', {})
    is_relevant = relevance.get('is_relevant', False)
    description = relevance.get('description', '분석 결과 없음')
    
    relevance_info = {
        "🔗 연관성": "있음" if is_relevant else "없음",
        "📝 분석 내용": description
    }
    formatter.display_info_panel(relevance_info, "🔍 연관성 분석")
    
    # 보충 응답이 있는 경우 표시
    supplementary = analysis_result.get('outputs', {}).get('supplementary_response')
    if supplementary and is_relevant:
        formatter.console.print()
        formatter.display_query_panel(supplementary['query'], "💡 보충 질의")
        formatter.display_response_panel(supplementary['response'], "💬 보충 응답")
        
        supp_info = {
            "⏱️ 처리 시간": f"{supplementary.get('elapsed_time', 0.0):.2f}초",
            "📄 참조 문서": f"{len(supplementary.get('document_paths', []))}개"
        }
        formatter.display_info_panel(supp_info, "📊 보충 응답 정보")


def display_error(error_message: str, config: Dict[str, Any] = None):
    """에러 메시지 통합 출력"""
    if config is None:
        config = {}
    
    formatter = OutputFormatter(config)
    formatter.display_error(error_message)


def display_progress(message: str, config: Dict[str, Any] = None):
    """진행 상황 표시"""
    if config is None:
        config = {}
    
    formatter = OutputFormatter(config)
    formatter.display_progress_message(message)