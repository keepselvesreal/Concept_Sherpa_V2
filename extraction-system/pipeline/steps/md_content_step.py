# 생성 시간: 2025-08-27 17:38 KST
# 핵심 내용: MD 파일 콘텐츠 처리 단계
# 상세 내용:
#   - MDContentProcessingStep (라인 15-85): MD 파일 헤더 정리 및 content.md 생성
#   - execute() (라인 20-65): header_cleaner.py 로직을 파이프라인에 통합
#   - _find_first_header() (라인 67-80): 첫 번째 # 헤더 위치 탐지
#   - _clean_markdown_content() (라인 82-105): 마크다운 내용 정리
# 상태: active
# 주소: pipeline/steps/md_content_step
# 참조: header_cleaner.py → 파이프라인 단계로 변환

import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from pipeline.steps.base import PipelineStep
from pipeline.models import StepResult


class MDContentProcessingStep(PipelineStep):
    """MD 파일 콘텐츠 처리 단계 (4/7)"""
    
    def __init__(self):
        super().__init__("콘텐츠 처리")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """첫 번째 # 헤더 이전 내용을 제거하여 content.md 생성"""
        self._log_step_start()
        
        try:
            # 이전 단계에서 전달된 정보
            folder_path = context.get("folder_path")
            md_content = context.get("md_content")
            
            if not all([folder_path, md_content]):
                return StepResult(success=False, error="필요한 정보가 없습니다 (folder_path, md_content)")
            
            # 마크다운 내용 정리
            cleaned_content, removed_lines = self._clean_markdown_content(md_content)
            
            # content.md 저장
            content_file = Path(folder_path) / "content.md"
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"📊 전체 줄 수: {len(md_content.splitlines())}줄")
            print(f"📊 제거된 줄 수: {removed_lines}줄")
            print(f"📊 저장된 줄 수: {len(cleaned_content.splitlines())}줄")
            print(f"💾 정리된 파일 저장: {content_file}")
            
            self._log_step_success()
            
            return StepResult(
                success=True,
                data={
                    "content_file": str(content_file),
                    "original_lines": len(md_content.splitlines()),
                    "removed_lines": removed_lines,
                    "cleaned_lines": len(cleaned_content.splitlines()),
                    "cleaned_content": cleaned_content
                }
            )
            
        except Exception as e:
            error_msg = f"콘텐츠 처리 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult(success=False, error=error_msg)
    
    def _find_first_header(self, lines: List[str]) -> Optional[int]:
        """첫 번째 # 헤더 위치 탐지"""
        header_pattern = re.compile(r'^#+\s+')
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line and header_pattern.match(stripped_line):
                return i
        
        return None
    
    def _clean_markdown_content(self, md_content: str) -> Tuple[str, int]:
        """마크다운 내용 정리 (첫 번째 헤더 이전 내용 제거)"""
        lines = md_content.splitlines(keepends=True)
        
        # 첫 번째 헤더 위치 찾기
        header_line_index = self._find_first_header(lines)
        
        if header_line_index is None:
            print("⚠️ # 헤더를 찾을 수 없습니다. 파일을 그대로 사용합니다.")
            cleaned_lines = lines
            removed_lines = 0
        else:
            print(f"🎯 첫 번째 헤더 위치: {header_line_index + 1}번째 줄")
            # 헤더부터 끝까지 추출
            cleaned_lines = lines[header_line_index:]
            removed_lines = header_line_index
        
        # 문자열로 결합
        cleaned_content = ''.join(cleaned_lines)
        
        return cleaned_content, removed_lines