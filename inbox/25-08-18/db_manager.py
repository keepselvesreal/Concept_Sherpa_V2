"""
생성 시간: 2025-08-18 11:08:36
핵심 내용: 범용 데이터베이스 관리 스크립트 - 메인 CLI 인터페이스
상세 내용:
    - DatabaseManager 클래스 (라인 30-85): 메인 CLI 관리자
    - Command 처리 시스템 (라인 87-200): 명령어별 처리 로직
    - 프로젝트 관리 명령어: projects (list, select, create)
    - 테이블 관리 명령어: tables (list, show, create, drop)
    - 스키마 관리 명령어: schema (add-column, modify-column, drop-column)
    - 데이터 관리 명령어: data (insert, query, update, delete)
상태: 
주소: db_manager
참조: 
"""

import argparse
import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv('/home/nadle/projects/Knowledge_Sherpa/v2/.env')

from core.database_interface import DatabaseInterface
from adapters.postgresql_adapter import PostgreSQLAdapter
from utils.config_loader import ConfigLoader
from utils.cli_helpers import CLIHelpers

class DatabaseManager:
    """
    범용 데이터베이스 관리 시스템의 메인 클래스
    """
    
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.cli_helpers = CLIHelpers()
        self.current_project = None
        self.db_adapter = None
    
    def load_project(self, project_name: str) -> bool:
        """
        프로젝트를 로드하고 DB 어댑터를 초기화
        
        Args:
            project_name: 로드할 프로젝트명
            
        Returns:
            성공 여부
        """
        try:
            project_config = self.config_loader.get_project_config(project_name)
            if not project_config:
                print(f"프로젝트 '{project_name}'을 찾을 수 없습니다.")
                return False
            
            # 어댑터 초기화
            adapter_type = project_config.get('adapter', 'postgresql')
            if adapter_type == 'postgresql':
                self.db_adapter = PostgreSQLAdapter(project_config)
            else:
                print(f"지원되지 않는 어댑터 타입: {adapter_type}")
                return False
            
            self.current_project = project_name
            print(f"프로젝트 '{project_name}' 로드 완료")
            return True
            
        except Exception as e:
            print(f"프로젝트 로드 실패: {e}")
            return False
    
    def run(self, args):
        """
        메인 실행 함수
        
        Args:
            args: argparse로 파싱된 명령행 인수
        """
        try:
            # 프로젝트 관련 명령어는 별도 처리
            if args.command == 'projects':
                self.handle_projects_command(args)
                return
            
            # 다른 명령어들은 프로젝트 로드가 필요
            if not args.project:
                print("프로젝트를 지정해야 합니다. --project 옵션을 사용하세요.")
                return
            
            if not self.load_project(args.project):
                return
            
            # 명령어별 처리
            if args.command == 'tables':
                self.handle_tables_command(args)
            elif args.command == 'schema':
                self.handle_schema_command(args)
            elif args.command == 'data':
                self.handle_data_command(args)
            else:
                print(f"알 수 없는 명령어: {args.command}")
                
        except Exception as e:
            print(f"실행 중 오류 발생: {e}")
        finally:
            if self.db_adapter:
                self.db_adapter.close()

    def handle_projects_command(self, args):
        """프로젝트 관련 명령어 처리"""
        if args.subcommand == 'list':
            projects = self.config_loader.list_projects()
            if projects:
                print("사용 가능한 프로젝트:")
                for project in projects:
                    print(f"  - {project}")
            else:
                print("등록된 프로젝트가 없습니다.")
        
        elif args.subcommand == 'show':
            if not args.name:
                print("프로젝트명을 지정해야 합니다.")
                return
            
            project_config = self.config_loader.get_project_config(args.name)
            if project_config:
                print(f"프로젝트 '{args.name}' 정보:")
                self.cli_helpers.print_dict(project_config)
            else:
                print(f"프로젝트 '{args.name}'을 찾을 수 없습니다.")

    def handle_tables_command(self, args):
        """테이블 관련 명령어 처리"""
        if args.subcommand == 'list':
            tables = self.db_adapter.list_tables()
            if tables:
                print("테이블 목록:")
                for table in tables:
                    print(f"  - {table}")
            else:
                print("테이블이 없습니다.")
        
        elif args.subcommand == 'show':
            if not args.name:
                print("테이블명을 지정해야 합니다.")
                return
            
            schema = self.db_adapter.get_table_schema(args.name)
            if schema:
                print(f"테이블 '{args.name}' 스키마:")
                self.cli_helpers.print_table_schema(schema)
            else:
                print(f"테이블 '{args.name}'을 찾을 수 없습니다.")

    def handle_schema_command(self, args):
        """스키마 관련 명령어 처리"""
        if args.subcommand == 'add-column':
            if not all([args.table, args.column_name, args.column_type]):
                print("테이블명, 컬럼명, 컬럼 타입을 모두 지정해야 합니다.")
                return
            
            success = self.db_adapter.add_column(
                args.table, 
                args.column_name, 
                args.column_type,
                args.default
            )
            if success:
                print(f"컬럼 '{args.column_name}' 추가 완료")
            else:
                print("컬럼 추가 실패")
        
        elif args.subcommand == 'drop-column':
            if not all([args.table, args.column_name]):
                print("테이블명과 컬럼명을 지정해야 합니다.")
                return
            
            success = self.db_adapter.drop_column(args.table, args.column_name)
            if success:
                print(f"컬럼 '{args.column_name}' 삭제 완료")
            else:
                print("컬럼 삭제 실패")

    def handle_data_command(self, args):
        """데이터 관련 명령어 처리"""
        if args.subcommand == 'query':
            if not args.table:
                print("테이블명을 지정해야 합니다.")
                return
            
            results = self.db_adapter.query_data(
                args.table,
                where_clause=args.where,
                limit=args.limit
            )
            
            if results:
                print(f"테이블 '{args.table}' 조회 결과:")
                self.cli_helpers.print_query_results(results)
            else:
                print("조회 결과가 없습니다.")

def create_parser():
    """
    명령행 인수 파서 생성
    
    Returns:
        argparse.ArgumentParser: 설정된 파서
    """
    parser = argparse.ArgumentParser(description='범용 데이터베이스 관리 도구')
    parser.add_argument('--project', '-p', help='사용할 프로젝트명')
    
    subparsers = parser.add_subparsers(dest='command', help='사용 가능한 명령어')
    
    # projects 명령어
    projects_parser = subparsers.add_parser('projects', help='프로젝트 관리')
    projects_subparsers = projects_parser.add_subparsers(dest='subcommand')
    
    projects_subparsers.add_parser('list', help='프로젝트 목록 보기')
    
    show_project_parser = projects_subparsers.add_parser('show', help='프로젝트 정보 보기')
    show_project_parser.add_argument('name', help='프로젝트명')
    
    # tables 명령어
    tables_parser = subparsers.add_parser('tables', help='테이블 관리')
    tables_subparsers = tables_parser.add_subparsers(dest='subcommand')
    
    tables_subparsers.add_parser('list', help='테이블 목록 보기')
    
    show_table_parser = tables_subparsers.add_parser('show', help='테이블 스키마 보기')
    show_table_parser.add_argument('name', help='테이블명')
    
    # schema 명령어
    schema_parser = subparsers.add_parser('schema', help='스키마 관리')
    schema_subparsers = schema_parser.add_subparsers(dest='subcommand')
    
    add_column_parser = schema_subparsers.add_parser('add-column', help='컬럼 추가')
    add_column_parser.add_argument('table', help='테이블명')
    add_column_parser.add_argument('column_name', help='컬럼명')
    add_column_parser.add_argument('column_type', help='컬럼 타입')
    add_column_parser.add_argument('--default', help='기본값')
    
    drop_column_parser = schema_subparsers.add_parser('drop-column', help='컬럼 삭제')
    drop_column_parser.add_argument('table', help='테이블명')
    drop_column_parser.add_argument('column_name', help='컬럼명')
    
    # data 명령어
    data_parser = subparsers.add_parser('data', help='데이터 관리')
    data_subparsers = data_parser.add_subparsers(dest='subcommand')
    
    query_parser = data_subparsers.add_parser('query', help='데이터 조회')
    query_parser.add_argument('table', help='테이블명')
    query_parser.add_argument('--where', help='WHERE 조건')
    query_parser.add_argument('--limit', type=int, default=10, help='최대 결과 수')
    
    return parser

def main():
    """메인 함수"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = DatabaseManager()
    manager.run(args)

if __name__ == "__main__":
    main()