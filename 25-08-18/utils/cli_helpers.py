"""
생성 시간: 2025-08-18 11:10:12
핵심 내용: CLI 인터페이스를 위한 유틸리티 헬퍼 함수들
상세 내용:
    - CLIHelpers 클래스 (라인 20-120): CLI 출력 및 포맷팅 유틸리티
    - print_dict 메서드 (라인 30-45): 딕셔너리 예쁘게 출력
    - print_table_schema 메서드 (라인 47-70): 테이블 스키마 출력
    - print_query_results 메서드 (라인 72-95): 쿼리 결과 테이블 형태 출력
    - confirm_action 메서드 (라인 97-110): 사용자 확인 입력
    - format_file_size 메서드 (라인 112-120): 파일 크기 포맷팅
상태: 
주소: cli_helpers
참조: 
"""

from typing import List, Dict, Any, Optional
import json
from tabulate import tabulate

class CLIHelpers:
    """
    CLI 인터페이스를 위한 헬퍼 함수들
    """
    
    @staticmethod
    def print_dict(data: Dict[str, Any], indent: int = 0) -> None:
        """
        딕셔너리를 예쁘게 출력
        
        Args:
            data: 출력할 딕셔너리
            indent: 들여쓰기 레벨
        """
        indent_str = "  " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{indent_str}{key}:")
                CLIHelpers.print_dict(value, indent + 1)
            elif isinstance(value, list):
                print(f"{indent_str}{key}:")
                for item in value:
                    print(f"{indent_str}  - {item}")
            else:
                print(f"{indent_str}{key}: {value}")
    
    @staticmethod
    def print_table_schema(schema: List[Dict[str, Any]]) -> None:
        """
        테이블 스키마를 테이블 형태로 출력
        
        Args:
            schema: 컬럼 정보 리스트
        """
        if not schema:
            print("스키마 정보가 없습니다.")
            return
        
        headers = ["컬럼명", "타입", "NULL 허용", "기본값", "최대길이"]
        rows = []
        
        for col in schema:
            row = [
                col.get('column_name', ''),
                col.get('data_type', ''),
                "YES" if col.get('is_nullable', False) else "NO",
                col.get('default_value', '') or '',
                str(col.get('max_length', '')) if col.get('max_length') else ''
            ]
            rows.append(row)
        
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def print_query_results(results: List[Dict[str, Any]], max_rows: int = 50) -> None:
        """
        쿼리 결과를 테이블 형태로 출력
        
        Args:
            results: 쿼리 결과 리스트
            max_rows: 최대 출력 행 수
        """
        if not results:
            print("결과가 없습니다.")
            return
        
        # 헤더 추출
        headers = list(results[0].keys())
        
        # 데이터 행 생성 (최대 행 수 제한)
        rows = []
        for i, row in enumerate(results[:max_rows]):
            formatted_row = []
            for header in headers:
                value = row.get(header, '')
                # 긴 텍스트는 줄임표로 처리
                if isinstance(value, str) and len(value) > 50:
                    value = value[:47] + "..."
                formatted_row.append(value)
            rows.append(formatted_row)
        
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # 더 많은 결과가 있는 경우 안내
        if len(results) > max_rows:
            print(f"\n... ({len(results) - max_rows}개 더 많은 결과가 있습니다)")
    
    @staticmethod
    def confirm_action(message: str, default: bool = False) -> bool:
        """
        사용자에게 확인을 요청
        
        Args:
            message: 확인 메시지
            default: 기본값 (Enter 입력 시)
            
        Returns:
            사용자 확인 결과
        """
        suffix = " [Y/n]" if default else " [y/N]"
        try:
            response = input(f"{message}{suffix}: ").strip().lower()
            
            if not response:
                return default
            
            return response in ['y', 'yes', '예', 'ㅇ']
        except (KeyboardInterrupt, EOFError):
            return False
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        파일 크기를 읽기 쉬운 형태로 포맷팅
        
        Args:
            size_bytes: 바이트 단위 크기
            
        Returns:
            포맷된 크기 문자열
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    @staticmethod
    def print_separator(char: str = "-", length: int = 50) -> None:
        """
        구분선 출력
        
        Args:
            char: 구분선 문자
            length: 구분선 길이
        """
        print(char * length)
    
    @staticmethod
    def print_success(message: str) -> None:
        """성공 메시지 출력"""
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message: str) -> None:
        """에러 메시지 출력"""
        print(f"❌ {message}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        """경고 메시지 출력"""
        print(f"⚠️  {message}")
    
    @staticmethod
    def print_info(message: str) -> None:
        """정보 메시지 출력"""
        print(f"ℹ️  {message}")