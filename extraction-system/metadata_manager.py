# 생성 시간: 2025-08-22 09:30 KST
# 핵심 내용: YouTube URL 메타정보 JSON 파일 생성 및 관리 모듈
# 상세 내용:
#   - create_metadata_json(line 15): 메타정보 JSON 파일 생성 및 폴더 생성
#   - get_existing_folder(line 45): 기존 생성된 폴더 확인
#   - _generate_folder_name(line 58): 날짜 기반 폴더명 생성
# 상태: active

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional


def create_metadata_json(metadata_info: Dict[str, str], youtube_url: str) -> Dict[str, Any]:
    """
    메타정보 JSON 파일을 생성하고 YouTube 날짜 폴더를 생성합니다.
    (개별 비디오 폴더의 metadata.json은 나중에 youtube_extractor에서 생성)
    
    Args:
        metadata_info: UI에서 수집한 메타정보 딕셔너리
        youtube_url: YouTube URL
        
    Returns:
        생성 결과 정보 딕셔너리
    """
    try:
        # 날짜별 폴더 생성 (YouTube_250822 같은 형식)
        folder_name = _generate_folder_name()
        folder_path = os.path.join(".", folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # 메타정보 JSON 구조 생성
        metadata = {
            "source": youtube_url,
            "source_type": metadata_info.get("source_type", "youtube"),
            "source_language": metadata_info.get("source_language", "korean"),
            "structure_type": metadata_info.get("structure_type", "standalone"),
            "content_processing": metadata_info.get("content_processing", "unified"),
            "created_at": datetime.now().isoformat()
        }
        
        # 임시 JSON 파일 경로 (실제로는 개별 비디오 폴더에 저장될 예정)
        json_filename = "metadata.json"
        json_path = os.path.join(folder_path, json_filename)
        
        return {
            "success": True,
            "folder_path": folder_path,
            "json_path": json_path,
            "metadata": metadata
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "folder_path": None,
            "json_path": None
        }


def get_existing_folder() -> Optional[str]:
    """
    오늘 날짜로 생성된 기존 YouTube 폴더가 있는지 확인합니다.
    
    Returns:
        존재하는 폴더 경로 또는 None
    """
    folder_name = _generate_folder_name()
    folder_path = os.path.join(".", folder_name)
    
    if os.path.exists(folder_path):
        return folder_path
    return None


def _generate_folder_name() -> str:
    """
    현재 날짜 기반으로 YouTube 폴더명을 생성합니다.
    
    Returns:
        YouTube_yymmdd 형식의 폴더명
    """
    current_date = datetime.now().strftime("%y%m%d")
    return f"YouTube_{current_date}"