# 생성 시간: 2025-08-27 17:34 KST
# 핵심 내용: MD 파일 source 통합 단계 
# 상세 내용:
#   - MDSourceIntegrationStep (라인 15-70): MD 파일 source 필드를 metadata.json에 통합
#   - execute() (라인 20-55): source_updater.py 로직을 파이프라인에 통합
#   - _extract_source_from_md() (라인 57-75): YAML front matter에서 source 추출
#   - _update_metadata_source() (라인 77-95): metadata.json source 필드 업데이트
# 상태: active
# 주소: pipeline/steps/md_source_step
# 참조: source_updater.py → 파이프라인 단계로 변환

import json
import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pipeline.steps.base import PipelineStep
from pipeline.models import StepResult


class MDSourceIntegrationStep(PipelineStep):
    """MD 파일 source 통합 단계 (2/7)"""
    
    def __init__(self):
        super().__init__("Source 통합")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """source.md의 YAML front matter에서 source를 추출하여 metadata.json에 통합"""
        self._log_step_start()
        
        try:
            # 이전 단계에서 전달된 정보
            folder_path = context.get("folder_path")
            source_file = context.get("source_file")
            metadata_file = context.get("metadata_file")
            
            if not all([folder_path, source_file, metadata_file]):
                return StepResult(success=False, error="필요한 파일 경로 정보가 없습니다")
            
            # source.md에서 source 필드 추출
            source_path = Path(source_file)
            with open(source_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            source_url = self._extract_source_from_md(md_content)
            
            if source_url:
                # metadata.json 업데이트
                await self._update_metadata_source(Path(metadata_file), source_url)
                print(f"🔗 Source 필드 업데이트: {source_url}")
            else:
                print("⚠️ YAML front matter에서 source 필드를 찾을 수 없습니다. source는 빈 문자열로 유지됩니다.")
            
            self._log_step_success()
            
            return StepResult(
                success=True,
                data={
                    "source_url": source_url or "",
                    "source_extracted": source_url is not None
                }
            )
            
        except Exception as e:
            error_msg = f"Source 통합 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult(success=False, error=error_msg)
    
    def _extract_source_from_md(self, md_content: str) -> Optional[str]:
        """마크다운 YAML front matter에서 source 필드 추출"""
        try:
            # YAML front matter 패턴: ---로 시작하고 ---로 끝남
            pattern = r'^---\s*\n(.*?)\n---\s*\n'
            match = re.match(pattern, md_content, re.DOTALL)
            
            if not match:
                return None
            
            yaml_content = match.group(1)
            yaml_data = yaml.safe_load(yaml_content)
            
            if yaml_data and 'source' in yaml_data:
                source_value = yaml_data['source']
                if isinstance(source_value, str) and source_value.strip():
                    return source_value.strip()
            
            return None
            
        except Exception as e:
            print(f"⚠️ YAML 파싱 오류: {str(e)}")
            return None
    
    async def _update_metadata_source(self, metadata_file: Path, source_url: str) -> None:
        """metadata.json의 source 필드 업데이트"""
        try:
            # 기존 metadata.json 로드
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # source 필드 업데이트
            old_source = metadata.get('source', '')
            metadata['source'] = source_url
            
            # 파일 저장
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"📋 이전 source: '{old_source}' → 새로운 source: '{source_url}'")
            
        except Exception as e:
            raise Exception(f"metadata.json 업데이트 중 오류: {str(e)}")