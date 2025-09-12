# 생성 시간: Tue Sep  9 22:39:27 KST 2025
# 핵심 내용: WorkspacePreparationStage 출력 데이터 스키마 정의
# 상세 내용:
#   - WorkspacePreparationOutput (라인 12-66): 워크스페이스 준비 단계 출력 스키마 클래스
#   - validate 클래스 메서드 (라인 19-66): 출력 데이터 검증 메서드
# 상태: active

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

@dataclass
class WorkspacePreparationOutput:
    """워크스페이스 준비 단계 출력 스키마"""
    schema_version: str = "1.0"
    success: bool = False
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    @classmethod
    def validate(cls, result: Dict[str, Any]) -> bool:
        """
        출력 데이터 스키마 검증
        
        Args:
            result: 검증할 결과 딕셔너리
            
        Returns:
            bool: 검증 성공 여부
        """
        # 필수 필드 체크
        required_fields = ['success', 'data', 'error']
        if not all(field in result for field in required_fields):
            return False
        
        # success가 True인 경우 data 필드 검증
        if result['success']:
            if not result['data']:
                return False
                
            data = result['data']
            required_data_fields = ['book_metadata', 'chapters_data']
            if not all(field in data for field in required_data_fields):
                return False
            
            # book_metadata 구조 검증
            book_metadata = data['book_metadata']
            required_metadata_fields = ['title', 'normalized_title', 'total_chapters']
            if not all(field in book_metadata for field in required_metadata_fields):
                return False
                
            # chapters_data 구조 검증
            if not isinstance(data['chapters_data'], list):
                return False
                
            for chapter in data['chapters_data']:
                # 🟢 수정: 'toc_structure' → 'chapter_toc'로 변경
                chapter_required_fields = ['chapter_title', 'chapter_toc', 'content_text', 'metadata']
                if not all(field in chapter for field in chapter_required_fields):
                    return False
                
                # metadata 구조 검증
                metadata = chapter['metadata']
                metadata_required_fields = ['start_page', 'end_page']
                if not all(field in metadata for field in metadata_required_fields):
                    return False
        
        # success가 False인 경우 error 필드 검증
        elif not result['success']:
            if not result.get('error'):
                return False
        
        return True