"""
생성 시간: 2025-08-18 11:09:02
핵심 내용: 데이터베이스 작업을 위한 추상 인터페이스 정의
상세 내용:
    - DatabaseInterface 추상 클래스 (라인 22-120): 모든 DB 어댑터가 구현해야 할 인터페이스
    - 연결 관리 메서드: connect, close, test_connection
    - 테이블 관리 메서드: list_tables, get_table_schema, create_table, drop_table
    - 스키마 관리 메서드: add_column, modify_column, drop_column
    - 데이터 관리 메서드: insert_data, query_data, update_data, delete_data
    - 백업/복원 메서드: backup_table, restore_table
상태: 
주소: database_interface
참조: 
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union

class DatabaseInterface(ABC):
    """
    데이터베이스 작업을 위한 추상 인터페이스
    모든 데이터베이스 어댑터는 이 인터페이스를 구현해야 함
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        데이터베이스 어댑터 초기화
        
        Args:
            config: 데이터베이스 연결 설정
        """
        self.config = config
        self.connection = None
    
    @abstractmethod
    def connect(self) -> bool:
        """
        데이터베이스에 연결
        
        Returns:
            연결 성공 여부
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """데이터베이스 연결 종료"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        연결 상태 테스트
        
        Returns:
            연결이 유효한지 여부
        """
        pass
    
    # 테이블 관리 메서드
    @abstractmethod
    def list_tables(self) -> List[str]:
        """
        데이터베이스의 모든 테이블 목록 반환
        
        Returns:
            테이블명 리스트
        """
        pass
    
    @abstractmethod
    def get_table_schema(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        테이블의 스키마 정보 반환
        
        Args:
            table_name: 테이블명
            
        Returns:
            컬럼 정보 리스트 (컬럼명, 타입, NULL 허용 여부, 기본값 등)
        """
        pass
    
    @abstractmethod
    def create_table(self, table_name: str, columns: List[Dict[str, Any]]) -> bool:
        """
        새 테이블 생성
        
        Args:
            table_name: 테이블명
            columns: 컬럼 정의 리스트
            
        Returns:
            생성 성공 여부
        """
        pass
    
    @abstractmethod
    def drop_table(self, table_name: str) -> bool:
        """
        테이블 삭제
        
        Args:
            table_name: 테이블명
            
        Returns:
            삭제 성공 여부
        """
        pass
    
    # 스키마 관리 메서드
    @abstractmethod
    def add_column(self, table_name: str, column_name: str, 
                   column_type: str, default_value: Optional[str] = None) -> bool:
        """
        테이블에 컬럼 추가
        
        Args:
            table_name: 테이블명
            column_name: 컬럼명
            column_type: 컬럼 타입
            default_value: 기본값
            
        Returns:
            추가 성공 여부
        """
        pass
    
    @abstractmethod
    def modify_column(self, table_name: str, column_name: str, 
                      new_type: str) -> bool:
        """
        컬럼 타입 수정
        
        Args:
            table_name: 테이블명
            column_name: 컬럼명
            new_type: 새로운 컬럼 타입
            
        Returns:
            수정 성공 여부
        """
        pass
    
    @abstractmethod
    def drop_column(self, table_name: str, column_name: str) -> bool:
        """
        컬럼 삭제
        
        Args:
            table_name: 테이블명
            column_name: 컬럼명
            
        Returns:
            삭제 성공 여부
        """
        pass
    
    # 데이터 관리 메서드
    @abstractmethod
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        데이터 삽입
        
        Args:
            table_name: 테이블명
            data: 삽입할 데이터 (컬럼명: 값)
            
        Returns:
            삽입 성공 여부
        """
        pass
    
    @abstractmethod
    def query_data(self, table_name: str, 
                   columns: Optional[List[str]] = None,
                   where_clause: Optional[str] = None,
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        데이터 조회
        
        Args:
            table_name: 테이블명
            columns: 조회할 컬럼 리스트 (None이면 모든 컬럼)
            where_clause: WHERE 조건
            limit: 최대 결과 수
            
        Returns:
            조회 결과 리스트
        """
        pass
    
    @abstractmethod
    def update_data(self, table_name: str, set_clause: Dict[str, Any],
                    where_clause: str) -> int:
        """
        데이터 수정
        
        Args:
            table_name: 테이블명
            set_clause: 수정할 값들 (컬럼명: 새값)
            where_clause: WHERE 조건
            
        Returns:
            수정된 행 수
        """
        pass
    
    @abstractmethod
    def delete_data(self, table_name: str, where_clause: str) -> int:
        """
        데이터 삭제
        
        Args:
            table_name: 테이블명
            where_clause: WHERE 조건
            
        Returns:
            삭제된 행 수
        """
        pass
    
    # 백업/복원 메서드
    @abstractmethod
    def backup_table(self, table_name: str, backup_path: str) -> bool:
        """
        테이블 백업
        
        Args:
            table_name: 테이블명
            backup_path: 백업 파일 경로
            
        Returns:
            백업 성공 여부
        """
        pass
    
    @abstractmethod
    def restore_table(self, table_name: str, backup_path: str) -> bool:
        """
        테이블 복원
        
        Args:
            table_name: 테이블명
            backup_path: 백업 파일 경로
            
        Returns:
            복원 성공 여부
        """
        pass
    
    # 유틸리티 메서드
    def get_database_info(self) -> Dict[str, Any]:
        """
        데이터베이스 정보 반환
        
        Returns:
            데이터베이스 정보 딕셔너리
        """
        return {
            'adapter_type': self.__class__.__name__,
            'connection_config': {k: v for k, v in self.config.items() 
                                if k not in ['password', 'url']},  # 보안 정보 제외
            'connected': self.test_connection() if hasattr(self, 'test_connection') else False
        }