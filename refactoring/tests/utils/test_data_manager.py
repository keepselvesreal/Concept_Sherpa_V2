# 생성 시간: Fri Sep 12 12:17:48 KST 2025
# 핵심 내용: 테스트 결과 데이터 저장/불러오기 매니저 (메타데이터 없는 순수 출력 결과 저장)
# 상세 내용:
#   - TestResultDataManager (라인 14-60): 메인 데이터 매니저 클래스
#   - save_test_result (라인 23-35): 테스트 결과를 JSON 파일로 저장
#   - load_test_result (라인 37-50): JSON 파일에서 테스트 결과 불러오기
#   - has_test_result (라인 52-56): 테스트 결과 파일 존재 여부 확인
#   - get_result_file_path (라인 58-60): 결과 파일 경로 생성 헬퍼 메서드
# 상태: active

import json
from pathlib import Path
from typing import Any, Optional

class TestResultDataManager:
    """테스트 결과 데이터 저장/불러오기 매니저 (메타데이터 없는 순수 출력 결과 저장)"""
    
    def __init__(self, base_path: str):
        """
        데이터 매니저 초기화
        
        Args:
            base_path: 테스트 결과를 저장할 기본 경로
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_test_result(self, test_method_name: str, result_data: Any) -> None:
        """
        테스트 결과를 JSON 파일로 저장 (순수 출력 결과만)
        
        Args:
            test_method_name: 테스트 메서드 이름 (예: "test_generate_node_documents")
            result_data: 저장할 테스트 결과 데이터 (메서드의 실제 출력 결과)
        """
        try:
            file_path = self.get_result_file_path(test_method_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
                
            print(f"✅ 테스트 결과 저장 완료: {file_path}")
            
        except Exception as e:
            print(f"❌ 테스트 결과 저장 실패 ({test_method_name}): {str(e)}")
            raise
    
    def load_test_result(self, test_method_name: str) -> Optional[Any]:
        """
        저장된 테스트 결과를 JSON 파일에서 불러오기
        
        Args:
            test_method_name: 테스트 메서드 이름
            
        Returns:
            저장된 테스트 결과 데이터 (파일이 없으면 None)
        """
        try:
            file_path = self.get_result_file_path(test_method_name)
            
            if not file_path.exists():
                print(f"⚠️ 테스트 결과 파일이 존재하지 않음: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                result_data = json.load(f)
                
            print(f"✅ 테스트 결과 로드 완료: {file_path}")
            return result_data
            
        except Exception as e:
            print(f"❌ 테스트 결과 로드 실패 ({test_method_name}): {str(e)}")
            raise
    
    def has_test_result(self, test_method_name: str) -> bool:
        """
        테스트 결과 파일 존재 여부 확인
        
        Args:
            test_method_name: 테스트 메서드 이름
            
        Returns:
            파일 존재 여부
        """
        file_path = self.get_result_file_path(test_method_name)
        return file_path.exists()
    
    def get_result_file_path(self, test_method_name: str) -> Path:
        """테스트 결과 파일 경로 생성"""
        return self.base_path / f"{test_method_name}_result.json"