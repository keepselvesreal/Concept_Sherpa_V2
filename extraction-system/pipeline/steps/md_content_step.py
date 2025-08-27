# 생성 시간: 2025-08-27 17:38 KST → 2025-08-27 20:09 KST 수정
# 핵심 내용: MD 파일 콘텐츠 처리 단계 (## Excerpt 이후 콘텐츠만 추출)
# 상세 내용:
#   - MDContentProcessingStep (라인 15-85): MD 파일 ## Excerpt 이후 내용만 추출하여 content.md 생성
#   - execute() (라인 20-65): ## Excerpt 섹션의 --- 이후 부분만 추출
#   - _find_first_header() (라인 67-80): 첫 번째 # 헤더 위치 탐지 (대안용)
#   - _clean_markdown_content() (라인 79-107): ## Excerpt --- 이후 콘텐츠 추출
#   - _find_content_after_excerpt() (라인 109-131): ## Excerpt 섹션의 --- 이후 위치 탐지
# 상태: active
# 주소: pipeline/steps/md_content_step/excerpt_filtered
# 참조: header_cleaner.py → ## Excerpt 필터링으로 개선

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
        """마크다운 내용 정리 (## Excerpt 섹션의 --- 이후 부분만 추출)"""
        lines = md_content.splitlines(keepends=True)
        
        # ## Excerpt 섹션의 --- 이후 위치 찾기
        content_start_index = self._find_content_after_excerpt(lines)
        
        if content_start_index is None:
            print("⚠️ ## Excerpt 섹션 또는 --- 구분선을 찾을 수 없습니다. 첫 번째 헤더부터 사용합니다.")
            # 대안: 첫 번째 헤더 찾기
            header_line_index = self._find_first_header(lines)
            if header_line_index is not None:
                cleaned_lines = lines[header_line_index:]
                removed_lines = header_line_index
                print(f"🎯 첫 번째 헤더 위치: {header_line_index + 1}번째 줄")
            else:
                print("⚠️ 헤더도 찾을 수 없습니다. 파일을 그대로 사용합니다.")
                cleaned_lines = lines
                removed_lines = 0
        else:
            print(f"🎯 ## Excerpt 이후 콘텐츠 시작 위치: {content_start_index + 1}번째 줄")
            # --- 이후부터 끝까지 추출
            cleaned_lines = lines[content_start_index:]
            removed_lines = content_start_index
        
        # 문자열로 결합
        cleaned_content = ''.join(cleaned_lines)
        
        return cleaned_content, removed_lines
    
    def _find_content_after_excerpt(self, lines: List[str]) -> Optional[int]:
        """## Excerpt 섹션의 --- 이후 위치 탐지"""
        excerpt_found = False
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # > ## Excerpt 패턴 찾기
            if not excerpt_found and '## Excerpt' in stripped_line:
                excerpt_found = True
                print(f"🔍 ## Excerpt 섹션 발견: {i + 1}번째 줄")
                continue
            
            # Excerpt 발견 후 첫 번째 --- 찾기
            if excerpt_found and stripped_line == '---':
                print(f"🔍 --- 구분선 발견: {i + 1}번째 줄")
                # --- 다음 줄부터 반환 (빈 줄 건너뛰기)
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():  # 비어있지 않은 첫 번째 줄
                        return j
                return i + 1  # 빈 줄만 있는 경우 --- 바로 다음부터
        
        return None