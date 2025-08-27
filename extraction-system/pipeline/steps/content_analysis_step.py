# 생성 시간: 2025-08-27 15:20 KST
# 핵심 내용: 콘텐츠 분석 단계 - 통합된 노드 문서들의 추출 섹션 생성
# 상세 내용:
#   - ContentAnalysisStep (라인 18-90): 통합된 노드 문서들을 분석하는 파이프라인 단계
#   - execute() (라인 22-70): 각 노드 문서의 내용 섹션을 분석해서 추출 섹션 업데이트
#   - _extract_content_section() (라인 72-88): 노드 문서에서 내용 섹션 추출
#   - _update_extraction_section() (라인 90-108): 추출 섹션을 파일에 업데이트
# 상태: active
# 주소: pipeline/steps/content_analysis_step
# 참조: modules/content_analyzer.py 모듈 사용 (리팩토링 전 방식 적용)

import os
import re
from typing import Dict, Any
from .base import PipelineStep
from ..models import StepResult
from modules.content_analyzer import analyze_content_with_claude


class ContentAnalysisStep(PipelineStep):
    """콘텐츠 분석 단계 - 통합된 노드 문서들의 추출 섹션 생성"""
    
    def __init__(self):
        super().__init__("콘텐츠 분석 (통합된 노드 문서 분석)")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """콘텐츠 분석 실행 - 통합된 노드 문서들을 분석"""
        self._log_step_start()
        
        try:
            # 비디오 폴더 경로에서 통합된 노드 문서들 찾기
            video_folder_path = context.get("video_folder_path")
            if not video_folder_path or not os.path.exists(video_folder_path):
                return StepResult.error_result("비디오 폴더를 찾을 수 없습니다")
            
            print(f"📁 비디오 폴더: {video_folder_path}")
            
            # *_info.md 파일들 찾기
            info_files = []
            for file in os.listdir(video_folder_path):
                if file.endswith('_info.md'):
                    info_files.append(os.path.join(video_folder_path, file))
            
            if not info_files:
                return StepResult.error_result("노드 정보 문서를 찾을 수 없습니다 (*_info.md)")
            
            print(f"📄 발견된 노드 문서: {len(info_files)}개")
            
            # 각 노드 문서의 "내용" 섹션을 분석하여 "추출" 섹션 업데이트
            processed_count = 0
            for info_file in info_files:
                print(f"📄 분석 중: {os.path.basename(info_file)}")
                
                # 파일에서 "내용" 섹션 추출
                content_section = self._extract_content_section(info_file)
                if not content_section:
                    print(f"⚠️ {os.path.basename(info_file)}: 내용 섹션이 비어있음")
                    continue
                
                # Claude SDK로 내용 분석 (직접 async 함수 호출)
                analysis_result = await analyze_content_with_claude(content_section)
                
                if analysis_result.get("success"):
                    # 추출 섹션을 파일에 업데이트
                    self._update_extraction_section(info_file, analysis_result.get("extraction_section", ""))
                    # process_status를 true로 변경 (추출 완료)
                    self._update_process_status(info_file, True)
                    print(f"✅ {os.path.basename(info_file)}: 추출 섹션 업데이트 완료")
                    processed_count += 1
                else:
                    print(f"❌ {os.path.basename(info_file)}: 분석 실패")
            
            self._log_step_success()
            return StepResult.success_result({
                "processed_files": processed_count,
                "total_files": len(info_files)
            })
            
        except Exception as e:
            error_msg = f"콘텐츠 분석 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult.error_result(error_msg)
    
    def _extract_content_section(self, info_file: str) -> str:
        """노드 문서에서 내용 섹션 추출"""
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 내용 섹션 찾기 (# 내용 --- 부터 # 구성 --- 까지)
            pattern = r'# 내용\n---\n(.*?)# 구성\n---'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                section_content = match.group(1).strip()
                if section_content and len(section_content) > 10:
                    return section_content
            
            return ""
            
        except Exception as e:
            print(f"❌ 내용 섹션 추출 실패: {e}")
            return ""
    
    def _update_extraction_section(self, info_file: str, extraction_section: str):
        """추출 섹션을 파일에 업데이트"""
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 찾기 및 교체
            pattern = r'(# 추출\n---\n)(.*?)(# 내용\n---)'
            replacement = rf'\1{extraction_section}\n\n\3'
            updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
        except Exception as e:
            print(f"❌ 추출 섹션 업데이트 실패: {e}")
    
    def _update_process_status(self, info_file: str, status: bool):
        """process_status를 업데이트"""
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # process_status 변경
            status_value = "true" if status else "false"
            updated_content = re.sub(
                r'process_status: (true|false)', 
                f'process_status: {status_value}', 
                content
            )
            
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
        except Exception as e:
            print(f"❌ process_status 업데이트 실패: {e}")