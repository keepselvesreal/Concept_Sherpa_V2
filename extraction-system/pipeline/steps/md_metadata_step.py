# 생성 시간: 2025-08-27 17:32 KST
# 핵심 내용: MD 파일 메타데이터 생성 단계
# 상세 내용:
#   - MDMetadataCreationStep (라인 20-80): MD 파일 메타데이터 생성 클래스
#   - execute() (라인 25-65): 메타데이터 생성 및 폴더 구조 생성
#   - _create_metadata() (라인 67-85): metadata.json 생성 로직
#   - _create_folder_structure() (라인 87-105): 폴더 구조 생성 로직
# 상태: active
# 주소: pipeline/steps/md_metadata_step
# 참조: 신규 생성 (MD 파이프라인 전용)

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from pipeline.steps.base import PipelineStep
from pipeline.models import StepResult
from title_extractor import generate_post_folder_name, check_folder_exists


class MDMetadataCreationStep(PipelineStep):
    """MD 파일 메타데이터 생성 단계 (1/7)"""
    
    def __init__(self):
        super().__init__("메타데이터 생성")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """메타데이터 생성 및 폴더 구조 생성"""
        self._log_step_start()
        
        try:
            # 필요한 정보 추출
            md_file_path = context.get("md_file_path")
            metadata_info = context.get("metadata_info", {})
            
            if not md_file_path:
                return StepResult(success=False, error="MD 파일 경로가 제공되지 않았습니다")
            
            # MD 파일 내용 읽기
            md_path = Path(md_file_path)
            if not md_path.exists():
                return StepResult(success=False, error=f"MD 파일을 찾을 수 없습니다: {md_file_path}")
            
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 폴더명 생성
            base_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system")
            folder_path, title = generate_post_folder_name(md_content)
            
            if not folder_path:
                return StepResult(success=False, error="MD 파일에서 제목을 찾을 수 없습니다. 첫 번째 # 헤더가 필요합니다.")
            
            # 중복 폴더 확인
            full_folder_path = base_path / folder_path
            if full_folder_path.exists():
                return StepResult(success=False, error=f"동일한 폴더가 이미 존재합니다: {folder_path}")
            
            # 폴더 생성
            full_folder_path.mkdir(parents=True, exist_ok=False)
            print(f"📁 폴더 생성: {full_folder_path}")
            
            # 메타데이터 생성 (safe_folder_name 추출)
            from title_extractor import create_safe_folder_name
            safe_folder_name = create_safe_folder_name(title)
            metadata = self._create_metadata(metadata_info, title, safe_folder_name)
            
            # metadata.json 저장
            metadata_file = full_folder_path / "metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"💾 메타데이터 저장: {metadata_file}")
            
            # MD 파일을 폴더로 복사 (source.md로)
            source_file = full_folder_path / "source.md"
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"📄 원본 파일 복사: {source_file}")
            
            self._log_step_success()
            
            return StepResult(
                success=True,
                data={
                    "folder_path": str(full_folder_path),
                    "metadata_file": str(metadata_file),
                    "source_file": str(source_file),
                    "title": title,
                    "md_content": md_content
                }
            )
            
        except Exception as e:
            error_msg = f"메타데이터 생성 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult(success=False, error=error_msg)
    
    def _create_metadata(self, metadata_info: Dict[str, Any], title: str, safe_folder_name: str) -> Dict[str, Any]:
        """metadata.json 생성"""
        return {
            "source": "",  # 빈 문자열로 초기화 (다음 단계에서 채워짐)
            "source_type": metadata_info.get("source_type", "markdown"),
            "source_language": metadata_info.get("source_language", "korean"),
            "structure_type": metadata_info.get("structure_type", "standalone"),
            "content_processing": metadata_info.get("content_processing", "unified"),
            "title": title,
            "folder_name": safe_folder_name,  # 40글자 이하 안전한 폴더명
            "created_at": datetime.now().isoformat()
        }