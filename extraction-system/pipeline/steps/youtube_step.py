# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: YouTube 스크립트 추출 단계 (기존 youtube_extractor 연동)
# 상세 내용:
#   - YouTubeExtractionStep (라인 13-40): 2단계 YouTube 스크립트 추출 클래스
#   - execute() (라인 17-40): 기존 youtube_extractor와 연동
# 상태: active
# 주소: pipeline/steps/youtube_step
# 참조: youtube_extractor.py 연동

from typing import Dict, Any
from .base import PipelineStep
from ..models import StepResult
from youtube_extractor import process_youtube_url


class YouTubeExtractionStep(PipelineStep):
    """2단계: YouTube 스크립트 추출"""
    
    def __init__(self):
        super().__init__("YouTube 스크립트 추출")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """YouTube 스크립트 추출"""
        self._log_step_start()
        
        try:
            url = context.get("url")
            folder_path = context.get("folder_path")
            metadata = context.get("metadata", {})
            
            if not url or not folder_path:
                return StepResult.error_result("URL 또는 폴더 경로가 없습니다")
            
            # 기존 youtube_extractor 함수 호출 (비동기화)
            result = await self._run_sync_function(process_youtube_url, url, ".", folder_path, metadata)
            
            if result["success"]:
                self._log_step_success()
                
                # 실제 metadata.json 경로 업데이트 (비디오 ID 폴더 안에 생성됨)
                script_file_path = result["file_info"]["full_path"]
                from pathlib import Path
                video_folder = Path(script_file_path).parent
                actual_json_path = video_folder / "metadata.json"
                
                print(f"🔍 업데이트된 metadata.json 경로: {actual_json_path}")
                
                return StepResult.success_result({
                    "script_file_path": script_file_path,
                    "video_info": result["video_info"],
                    "json_path": str(actual_json_path),  # 올바른 경로로 업데이트
                    "video_folder_path": str(video_folder)  # 비디오 폴더 경로 추가
                })
            else:
                self._log_step_error(result.get("message", "Unknown error"))
                return StepResult.error_result(result.get("message", "YouTube 추출 실패"))
        
        except Exception as e:
            error_msg = f"YouTube 스크립트 추출 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)