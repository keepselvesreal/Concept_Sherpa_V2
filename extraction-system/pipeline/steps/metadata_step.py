# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 메타데이터 생성 단계 (기존 metadata_manager 연동)
# 상세 내용:
#   - MetadataCreationStep (라인 13-35): 1단계 메타데이터 생성 클래스
#   - execute() (라인 17-35): 기존 metadata_manager와 연동
# 상태: active
# 주소: pipeline/steps/metadata_step
# 참조: metadata_manager.py 연동

from typing import Dict, Any
from .base import PipelineStep
from ..models import StepResult
from metadata_manager import create_metadata_json


class MetadataCreationStep(PipelineStep):
    """1단계: 메타데이터 생성"""
    
    def __init__(self):
        super().__init__("메타데이터 생성")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """메타데이터 JSON 생성"""
        self._log_step_start()
        
        try:
            url = context.get("url")
            metadata_info = context.get("metadata_info", {})
            
            if not url:
                return StepResult.error_result("URL이 없습니다")
            
            # 기존 metadata_manager 함수 호출 (비동기화)
            result = await self._run_sync_function(create_metadata_json, metadata_info, url)
            
            if result["success"]:
                self._log_step_success()
                return StepResult.success_result({
                    "folder_path": result["folder_path"],
                    "json_path": result["json_path"],
                    "metadata": result["metadata"]
                })
            else:
                self._log_step_error(result["error"])
                return StepResult.error_result(result["error"])
        
        except Exception as e:
            error_msg = f"메타데이터 생성 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)