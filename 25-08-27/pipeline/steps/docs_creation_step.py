# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 노드 문서 생성 단계 (subprocess 제거, 비동기 통일)
# 상세 내용:
#   - NodeDocsCreationStep (라인 13-35): 5단계 노드 문서 생성 클래스
#   - execute() (라인 17-35): 비동기 실행 메서드, subprocess 대신 직접 함수 호출
# 상태: active
# 주소: pipeline/steps/docs_creation_step
# 참조: modules/node_docs_creator.py 직접 호출

from typing import Dict, Any
from .base import PipelineStep
from ..models import StepResult
from ...modules.node_docs_creator import create_node_info_docs


class NodeDocsCreationStep(PipelineStep):
    """5단계: 노드 정보 문서 생성 (개선됨)"""
    
    def __init__(self):
        super().__init__("노드 정보 문서 생성")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """비동기 실행 (subprocess 제거)"""
        self._log_step_start()
        
        try:
            folder_path = context.get("folder_path")
            if not folder_path:
                return StepResult.error_result("폴더 경로가 없습니다")
            
            # subprocess 대신 직접 함수 호출 (비동기화)
            result = await self._run_sync_function(create_node_info_docs, folder_path)
            
            if result["success"]:
                self._log_step_success()
                return StepResult.success_result({
                    "docs_output_dir": result["output_dir"],
                    "docs_created_files": result["created_files"],
                    "docs_node_count": result["node_count"]
                })
            else:
                self._log_step_error(result["error"])
                return StepResult.error_result(result["error"])
        
        except Exception as e:
            error_msg = f"노드 문서 생성 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)