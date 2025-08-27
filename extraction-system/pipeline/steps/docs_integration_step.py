# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 노드 문서 통합 단계 (subprocess 제거, 비동기 통일)
# 상세 내용:
#   - NodeDocsIntegrationStep (라인 13-35): 6단계 노드 문서 통합 클래스
#   - execute() (라인 17-35): 비동기 실행 메서드, subprocess 대신 직접 함수 호출
# 상태: active
# 주소: pipeline/steps/docs_integration_step
# 참조: modules/docs_integrator.py 직접 호출

from typing import Dict, Any
from .base import PipelineStep
from ..models import StepResult
from modules.docs_integrator import integrate_node_documents


class NodeDocsIntegrationStep(PipelineStep):
    """6단계: 노드 문서 통합 (개선됨)"""
    
    def __init__(self):
        super().__init__("노드 문서 통합")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """비동기 실행 (subprocess 제거)"""
        self._log_step_start()
        
        try:
            folder_path = context.get("folder_path")
            if not folder_path:
                return StepResult.error_result("폴더 경로가 없습니다")
            
            # subprocess 대신 직접 함수 호출 (비동기화)
            result = await self._run_sync_function(integrate_node_documents, folder_path)
            
            if result["success"]:
                self._log_step_success()
                return StepResult.success_result({
                    "integration_updated_file": result["updated_file"],
                    "integration_sections": result["integrated_sections"]
                })
            else:
                self._log_step_error(result["error"])
                return StepResult.error_result(result["error"])
        
        except Exception as e:
            error_msg = f"노드 문서 통합 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)