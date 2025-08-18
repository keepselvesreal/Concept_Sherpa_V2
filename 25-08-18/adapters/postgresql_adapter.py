"""
생성 시간: 2025-08-18 11:09:25
핵심 내용: PostgreSQL 데이터베이스 어댑터 구현
상세 내용:
    - PostgreSQLAdapter 클래스 (라인 25-380): DatabaseInterface를 구현한 PostgreSQL 어댑터
    - 연결 관리 (라인 40-80): connect, close, test_connection 구현
    - 테이블 관리 (라인 82-165): list_tables, get_table_schema, create_table, drop_table 구현
    - 스키마 관리 (라인 167-245): add_column, modify_column, drop_column 구현
    - 데이터 관리 (라인 247-340): insert_data, query_data, update_data, delete_data 구현
    - 백업/복원 (라인 342-380): backup_table, restore_table 구현
    - 환경변수 및 직접 연결 문자열 지원
상태: 
주소: postgresql_adapter
참조: database_interface
"""

import os
import json
import csv
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

from core.database_interface import DatabaseInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgreSQLAdapter(DatabaseInterface):
    """
    PostgreSQL 데이터베이스 어댑터
    psycopg2를 사용하여 PostgreSQL과 상호작용
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        PostgreSQL 어댑터 초기화
        
        Args:
            config: 데이터베이스 연결 설정
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2가 설치되지 않았습니다. pip install psycopg2-binary")
        
        super().__init__(config)
        self.connection = None
        self._build_connection_string()
        
    def _build_connection_string(self):
        """연결 설정에서 연결 문자열 구성"""
        connection_config = self.config.get('connection', {})
        
        # 직접 URL이 제공된 경우
        if 'url' in connection_config:
            url = connection_config['url']
            # 환경변수 참조인지 확인
            if url.startswith('from_env:'):
                env_var = url.replace('from_env:', '')
                self.connection_string = os.getenv(env_var)
                if not self.connection_string:
                    raise ValueError(f"환경변수 {env_var}가 설정되지 않았습니다.")
            else:
                self.connection_string = url
        else:
            # 개별 설정으로 연결 문자열 구성
            host = self._resolve_env_var(connection_config.get('host', 'localhost'))
            port = self._resolve_env_var(connection_config.get('port', '5432'))
            database = self._resolve_env_var(connection_config.get('database', ''))
            user = self._resolve_env_var(connection_config.get('user', ''))
            password = self._resolve_env_var(connection_config.get('password', ''))
            
            self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    def _resolve_env_var(self, value: str) -> str:
        """환경변수 참조 해석"""
        if isinstance(value, str) and value.startswith('from_env:'):
            env_var = value.replace('from_env:', '')
            return os.getenv(env_var, '')
        return str(value)
    
    def connect(self) -> bool:
        """PostgreSQL 데이터베이스에 연결"""
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.connection.autocommit = True
            logger.info("PostgreSQL 연결 성공")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL 연결 실패: {e}")
            return False
    
    def close(self) -> None:
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("PostgreSQL 연결 종료")
    
    def test_connection(self) -> bool:
        """연결 상태 테스트"""
        if not self.connection:
            return self.connect()
        
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT 1")
                return True
        except Exception:
            return self.connect()
    
    # 테이블 관리 메서드
    def list_tables(self) -> List[str]:
        """모든 테이블 목록 반환"""
        if not self.test_connection():
            return []
        
        try:
            with self.connection.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = [row[0] for row in cur.fetchall()]
                return tables
        except Exception as e:
            logger.error(f"테이블 목록 조회 실패: {e}")
            return []
    
    def get_table_schema(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """테이블 스키마 정보 반환"""
        if not self.test_connection():
            return None
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default,
                        character_maximum_length,
                        numeric_precision,
                        numeric_scale
                    FROM information_schema.columns 
                    WHERE table_name = %s AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """, (table_name,))
                
                columns = []
                for row in cur.fetchall():
                    columns.append({
                        'column_name': row['column_name'],
                        'data_type': row['data_type'],
                        'is_nullable': row['is_nullable'] == 'YES',
                        'default_value': row['column_default'],
                        'max_length': row['character_maximum_length'],
                        'precision': row['numeric_precision'],
                        'scale': row['numeric_scale']
                    })
                
                return columns if columns else None
        except Exception as e:
            logger.error(f"테이블 스키마 조회 실패 ({table_name}): {e}")
            return None
    
    def create_table(self, table_name: str, columns: List[Dict[str, Any]]) -> bool:
        """새 테이블 생성"""
        if not self.test_connection():
            return False
        
        try:
            column_definitions = []
            for col in columns:
                col_def = f"{col['name']} {col['type']}"
                if not col.get('nullable', True):
                    col_def += " NOT NULL"
                if 'default' in col:
                    col_def += f" DEFAULT {col['default']}"
                column_definitions.append(col_def)
            
            create_sql = f"CREATE TABLE {table_name} ({', '.join(column_definitions)});"
            
            with self.connection.cursor() as cur:
                cur.execute(create_sql)
            
            logger.info(f"테이블 생성 완료: {table_name}")
            return True
        except Exception as e:
            logger.error(f"테이블 생성 실패 ({table_name}): {e}")
            return False
    
    def drop_table(self, table_name: str) -> bool:
        """테이블 삭제"""
        if not self.test_connection():
            return False
        
        try:
            with self.connection.cursor() as cur:
                cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            
            logger.info(f"테이블 삭제 완료: {table_name}")
            return True
        except Exception as e:
            logger.error(f"테이블 삭제 실패 ({table_name}): {e}")
            return False
    
    # 스키마 관리 메서드
    def add_column(self, table_name: str, column_name: str, 
                   column_type: str, default_value: Optional[str] = None) -> bool:
        """테이블에 컬럼 추가"""
        if not self.test_connection():
            return False
        
        try:
            alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            if default_value:
                alter_sql += f" DEFAULT {default_value}"
            alter_sql += ";"
            
            with self.connection.cursor() as cur:
                cur.execute(alter_sql)
            
            logger.info(f"컬럼 추가 완료: {table_name}.{column_name}")
            return True
        except Exception as e:
            logger.error(f"컬럼 추가 실패 ({table_name}.{column_name}): {e}")
            return False
    
    def modify_column(self, table_name: str, column_name: str, new_type: str) -> bool:
        """컬럼 타입 수정"""
        if not self.test_connection():
            return False
        
        try:
            alter_sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_type};"
            
            with self.connection.cursor() as cur:
                cur.execute(alter_sql)
            
            logger.info(f"컬럼 수정 완료: {table_name}.{column_name}")
            return True
        except Exception as e:
            logger.error(f"컬럼 수정 실패 ({table_name}.{column_name}): {e}")
            return False
    
    def drop_column(self, table_name: str, column_name: str) -> bool:
        """컬럼 삭제"""
        if not self.test_connection():
            return False
        
        try:
            alter_sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
            
            with self.connection.cursor() as cur:
                cur.execute(alter_sql)
            
            logger.info(f"컬럼 삭제 완료: {table_name}.{column_name}")
            return True
        except Exception as e:
            logger.error(f"컬럼 삭제 실패 ({table_name}.{column_name}): {e}")
            return False
    
    # 데이터 관리 메서드
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> bool:
        """데이터 삽입"""
        if not self.test_connection():
            return False
        
        try:
            columns = list(data.keys())
            values = []
            
            # 값 처리 (JSON 타입 변환)
            for value in data.values():
                if isinstance(value, (dict, list)):
                    values.append(json.dumps(value))
                else:
                    values.append(value)
            
            placeholders = ', '.join(['%s'] * len(values))
            
            # UPSERT 사용 (ON CONFLICT DO UPDATE)
            conflict_column = 'id' if 'id' in columns else columns[0]
            update_clauses = [f"{col} = EXCLUDED.{col}" for col in columns if col != conflict_column]
            
            if update_clauses:
                insert_sql = f"""
                    INSERT INTO {table_name} ({', '.join(columns)}) 
                    VALUES ({placeholders})
                    ON CONFLICT ({conflict_column}) DO UPDATE SET
                    {', '.join(update_clauses)};
                """
            else:
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
            
            with self.connection.cursor() as cur:
                cur.execute(insert_sql, values)
            
            logger.info(f"데이터 삽입 완료: {table_name}")
            return True
        except Exception as e:
            logger.error(f"데이터 삽입 실패 ({table_name}): {e}")
            return False
    
    def query_data(self, table_name: str, 
                   columns: Optional[List[str]] = None,
                   where_clause: Optional[str] = None,
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """데이터 조회"""
        if not self.test_connection():
            return []
        
        try:
            column_str = ', '.join(columns) if columns else '*'
            query_sql = f"SELECT {column_str} FROM {table_name}"
            
            if where_clause:
                query_sql += f" WHERE {where_clause}"
            
            if limit:
                query_sql += f" LIMIT {limit}"
            
            query_sql += ";"
            
            with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query_sql)
                results = [dict(row) for row in cur.fetchall()]
            
            return results
        except Exception as e:
            logger.error(f"데이터 조회 실패 ({table_name}): {e}")
            return []
    
    def update_data(self, table_name: str, set_clause: Dict[str, Any],
                    where_clause: str) -> int:
        """데이터 수정"""
        if not self.test_connection():
            return 0
        
        try:
            set_items = [f"{col} = %s" for col in set_clause.keys()]
            set_str = ', '.join(set_items)
            values = list(set_clause.values())
            
            update_sql = f"UPDATE {table_name} SET {set_str} WHERE {where_clause};"
            
            with self.connection.cursor() as cur:
                cur.execute(update_sql, values)
                affected_rows = cur.rowcount
            
            logger.info(f"데이터 수정 완료: {table_name} ({affected_rows}행)")
            return affected_rows
        except Exception as e:
            logger.error(f"데이터 수정 실패 ({table_name}): {e}")
            return 0
    
    def delete_data(self, table_name: str, where_clause: str) -> int:
        """데이터 삭제"""
        if not self.test_connection():
            return 0
        
        try:
            delete_sql = f"DELETE FROM {table_name} WHERE {where_clause};"
            
            with self.connection.cursor() as cur:
                cur.execute(delete_sql)
                affected_rows = cur.rowcount
            
            logger.info(f"데이터 삭제 완료: {table_name} ({affected_rows}행)")
            return affected_rows
        except Exception as e:
            logger.error(f"데이터 삭제 실패 ({table_name}): {e}")
            return 0
    
    # 백업/복원 메서드
    def backup_table(self, table_name: str, backup_path: str) -> bool:
        """테이블 백업 (CSV 형식)"""
        if not self.test_connection():
            return False
        
        try:
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 데이터 조회
            data = self.query_data(table_name)
            if not data:
                logger.warning(f"백업할 데이터가 없습니다: {table_name}")
                return True
            
            # CSV 파일로 저장
            with open(backup_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"테이블 백업 완료: {table_name} -> {backup_path}")
            return True
        except Exception as e:
            logger.error(f"테이블 백업 실패 ({table_name}): {e}")
            return False
    
    def restore_table(self, table_name: str, backup_path: str) -> bool:
        """테이블 복원 (CSV 형식)"""
        if not self.test_connection():
            return False
        
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                logger.error(f"백업 파일이 존재하지 않습니다: {backup_path}")
                return False
            
            # CSV 파일 읽기
            with open(backup_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
            
            if not data:
                logger.warning(f"복원할 데이터가 없습니다: {backup_path}")
                return True
            
            # 데이터 삽입
            success_count = 0
            for row in data:
                if self.insert_data(table_name, row):
                    success_count += 1
            
            logger.info(f"테이블 복원 완료: {table_name} ({success_count}/{len(data)}행)")
            return success_count == len(data)
        except Exception as e:
            logger.error(f"테이블 복원 실패 ({table_name}): {e}")
            return False