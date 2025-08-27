# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 노드 생성 단계 (기존 node_generator 연동)
# 상세 내용:
#   - NodeGenerationStep (라인 14-45): 4단계 노드 생성 클래스
#   - execute() (라인 18-45): 기존 node_generator와 연동
# 상태: active
# 주소: pipeline/steps/node_step
# 참조: node_generator.py 연동

import json
from typing import Dict, Any
from pathlib import Path
from .base import PipelineStep
from ..models import StepResult
from node_generator import load_metadata, extract_headers_by_type


class NodeGenerationStep(PipelineStep):
    """4단계: 노드 생성"""
    
    def __init__(self):
        super().__init__("노드 생성")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """노드 생성"""
        self._log_step_start()
        
        try:
            json_path = context.get("json_path")
            script_file_path = context.get("script_file_path")
            
            if not json_path or not script_file_path:
                return StepResult.error_result("JSON 경로 또는 스크립트 파일 경로가 없습니다")
            
            # 메타데이터 로드 (비동기화)
            metadata = await self._run_sync_function(load_metadata, Path(json_path))
            if not metadata:
                return StepResult.error_result("메타데이터 로드 실패")
            
            # 스크립트 내용 읽기 및 헤더 추출 (비동기화)
            content = await self._run_sync_function(self._read_script_content, script_file_path)
            nodes = await self._run_sync_function(extract_headers_by_type, content, metadata)
            
            # 노드 파일 저장 (비동기화)
            script_path = Path(script_file_path)
            nodes_file = script_path.parent / "nodes.json"
            await self._run_sync_function(self._save_nodes, nodes_file, nodes)
            
            self._log_step_success()
            return StepResult.success_result({
                "nodes_file": str(nodes_file),
                "node_count": len(nodes)
            })
        
        except Exception as e:
            error_msg = f"노드 생성 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)
    
    def _read_script_content(self, script_file_path: str) -> str:
        """스크립트 내용 읽기 (동기 함수)"""
        with open(script_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _save_nodes(self, nodes_file: Path, nodes: list):
        """노드 파일 저장 (동기 함수)"""
        with open(nodes_file, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)