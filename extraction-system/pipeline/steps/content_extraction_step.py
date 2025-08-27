# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 노드 정보 추출 단계 (subprocess 제거, 비동기 통일)
# 상세 내용:
#   - NodeContentExtractionStep (라인 13-37): 7단계 노드 정보 추출 클래스
#   - execute() (라인 17-37): 비동기 실행 메서드, subprocess 대신 직접 함수 호출
# 상태: active
# 주소: pipeline/steps/content_extraction_step
# 참조: modules/content_extractor.py 직접 호출

from typing import Dict, Any
from .base import PipelineStep
from ..models import StepResult
from modules.content_extractor import extract_enhanced_node_content


class NodeContentExtractionStep(PipelineStep):
    """7단계: 노드 정보 추출 (개선됨)"""
    
    def __init__(self):
        super().__init__("노드 정보 추출")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """비동기 실행 (subprocess 제거)"""
        self._log_step_start()
        
        try:
            folder_path = context.get("folder_path")
            if not folder_path:
                return StepResult.error_result("폴더 경로가 없습니다")
            
            # subprocess 대신 직접 함수 호출 (비동기화)
            result = await self._run_sync_function(extract_enhanced_node_content, folder_path)
            
            if result["success"]:
                self._log_step_success()
                return StepResult.success_result({
                    "extraction_output_file": result["output_file"],
                    "extraction_insights_file": result["insights_file"],
                    "extraction_processed_count": result["processed_count"],
                    "extraction_insights_count": result["insights_count"]
                })
            else:
                self._log_step_error(result["error"])
                return StepResult.error_result(result["error"])
        
        except Exception as e:
            error_msg = f"노드 정보 추출 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)