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
                return StepResult.success_result({
                    "script_file_path": result["file_info"]["full_path"],
                    "video_info": result["video_info"]
                })
            else:
                self._log_step_error(result.get("message", "Unknown error"))
                return StepResult.error_result(result.get("message", "YouTube 추출 실패"))
        
        except Exception as e:
            error_msg = f"YouTube 스크립트 추출 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)