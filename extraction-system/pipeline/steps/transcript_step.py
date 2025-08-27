# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 스크립트 개선 단계 (기존 transcript_improver 연동)
# 상세 내용:
#   - TranscriptImprovementStep (라인 13-45): 3단계 스크립트 개선 클래스
#   - execute() (라인 17-45): 기존 transcript_improver와 연동
# 상태: active
# 주소: pipeline/steps/transcript_step
# 참조: transcript_improver.py 연동

from typing import Dict, Any
from pathlib import Path
from .base import PipelineStep
from ..models import StepResult
from transcript_improver import improve_transcript_with_claude, extract_transcript_content, extract_first_last_sentences


class TranscriptImprovementStep(PipelineStep):
    """3단계: 스크립트 개선"""
    
    def __init__(self):
        super().__init__("스크립트 개선")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """스크립트 개선"""
        self._log_step_start()
        
        try:
            script_file_path = context.get("script_file_path")
            if not script_file_path:
                return StepResult.error_result("스크립트 파일 경로가 없습니다")
            
            # 스크립트 내용 추출 (비동기화)
            transcript_content = await self._run_sync_function(extract_transcript_content, script_file_path)
            if not transcript_content:
                return StepResult.error_result("스크립트 내용 추출 실패")
            
            # 첫/마지막 문장 추출 (비동기화)
            first_words, last_words = await self._run_sync_function(extract_first_last_sentences, transcript_content)
            
            # Claude로 스크립트 개선 (이미 async 함수)
            improved_content = await improve_transcript_with_claude(transcript_content, first_words, last_words)
            if not improved_content:
                return StepResult.error_result("스크립트 개선 실패")
            
            # 개선된 내용 저장 (비동기화)
            script_path = Path(script_file_path)
            content_file = script_path.parent / "content.md"
            
            await self._run_sync_function(self._save_content, content_file, improved_content)
            
            self._log_step_success()
            return StepResult.success_result({
                "content_file": str(content_file)
            })
        
        except Exception as e:
            error_msg = f"스크립트 개선 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)
    
    def _save_content(self, content_file: Path, improved_content: str):
        """개선된 내용 저장 (동기 함수)"""
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(improved_content)