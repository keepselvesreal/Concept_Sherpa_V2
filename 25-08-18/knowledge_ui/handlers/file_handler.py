"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: 파일 선택 및 처리 핸들러 - 선택된 파일 경로 전달 및 출력
상세 내용:
    - FileHandler: 파일 처리 메인 클래스
    - process_file(file_path): 선택된 파일의 경로를 처리하고 출력
    - _validate_file(file_path): 파일 유효성 검사
    - _get_file_info(file_path): 파일 정보 추출
    - _log_file_processing(file_path, info): 파일 처리 로그 출력
상태: 활성
주소: knowledge_ui/handlers/file_handler
참조: 
"""

import os
import sys
from datetime import datetime


class FileHandler:
    def __init__(self):
        """파일 핸들러 초기화"""
        # 출력 디렉토리 설정
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'processed_files')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 로그 파일 경로
        self.log_file = os.path.join(self.output_dir, 'file_processing_log.txt')
        
    def process_file(self, file_path):
        """
        선택된 파일을 처리합니다. 현재는 경로 출력 및 로그 기록만 수행합니다.
        
        Args:
            file_path (str): 처리할 파일의 경로
            
        Returns:
            dict: 처리 결과 정보
        """
        try:
            # 파일 유효성 검사
            if not self._validate_file(file_path):
                return {
                    'success': False,
                    'error': '파일이 존재하지 않거나 접근할 수 없습니다.'
                }
            
            # 파일 정보 추출
            file_info = self._get_file_info(file_path)
            
            # 콘솔에 파일 경로 출력 (요구사항)
            print("=" * 60)
            print("📁 파일 처리 요청")
            print("=" * 60)
            print(f"선택된 파일 경로: {file_path}")
            print(f"파일명: {file_info['filename']}")
            print(f"파일 크기: {file_info['size_mb']:.2f} MB")
            print(f"파일 확장자: {file_info['extension']}")
            print(f"처리 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # 로그 파일에 기록
            self._log_file_processing(file_path, file_info)
            
            return {
                'success': True,
                'file_path': file_path,
                'message': f'파일 경로가 정상적으로 전달되었습니다: {os.path.basename(file_path)}',
                'file_info': file_info
            }
            
        except Exception as e:
            error_msg = f'파일 처리 중 오류 발생: {str(e)}'
            print(f"❌ {error_msg}")
            
            return {
                'success': False,
                'error': error_msg
            }
    
    def _validate_file(self, file_path):
        """
        파일의 유효성을 검사합니다.
        
        Args:
            file_path (str): 검사할 파일 경로
            
        Returns:
            bool: 파일이 유효한지 여부
        """
        try:
            return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    def _get_file_info(self, file_path):
        """
        파일의 기본 정보를 추출합니다.
        
        Args:
            file_path (str): 파일 경로
            
        Returns:
            dict: 파일 정보
        """
        try:
            stat_info = os.stat(file_path)
            filename = os.path.basename(file_path)
            name, extension = os.path.splitext(filename)
            
            return {
                'filename': filename,
                'name': name,
                'extension': extension.lower() if extension else '',
                'size_bytes': stat_info.st_size,
                'size_mb': stat_info.st_size / (1024 * 1024),
                'modified_time': datetime.fromtimestamp(stat_info.st_mtime),
                'created_time': datetime.fromtimestamp(stat_info.st_ctime)
            }
            
        except Exception as e:
            return {
                'filename': os.path.basename(file_path),
                'error': f'정보 추출 실패: {str(e)}'
            }
    
    def _log_file_processing(self, file_path, file_info):
        """
        파일 처리 내역을 로그 파일에 기록합니다.
        
        Args:
            file_path (str): 처리된 파일 경로
            file_info (dict): 파일 정보
        """
        try:
            log_entry = f"""
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 파일 처리 로그
파일 경로: {file_path}
파일명: {file_info.get('filename', 'Unknown')}
파일 크기: {file_info.get('size_mb', 0):.2f} MB
확장자: {file_info.get('extension', 'Unknown')}
처리 상태: 성공 (경로 전달 완료)
{'=' * 80}
"""
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            print(f"⚠️ 로그 기록 실패: {str(e)}")
    
    def get_processing_history(self):
        """
        파일 처리 히스토리를 반환합니다.
        
        Returns:
            str: 로그 파일 내용 또는 오류 메시지
        """
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return "처리 히스토리가 없습니다."
                
        except Exception as e:
            return f"히스토리 조회 실패: {str(e)}"