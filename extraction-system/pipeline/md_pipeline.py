# 생성 시간: 2025-08-27 17:30 KST  
# 핵심 내용: 마크다운 파일 처리 파이프라인 메인 클래스
# 상세 내용:
#   - MDPipeline (라인 15-150): 4단계 MD 파이프라인 + 유튜브 5단계부터 연결
#   - _setup_md_steps() (라인 152-170): MD 전용 4단계 초기화  
#   - _setup_youtube_steps() (라인 172-185): 유튜브 5-7단계 초기화
#   - execute() (라인 30-95): 전체 파이프라인 실행 메서드
# 상태: active
# 주소: pipeline/md_pipeline
# 참조: pipeline/youtube_pipeline → MD 파일 전용으로 적용

import asyncio
from typing import Dict, Any, List
from pathlib import Path
from pipeline.models import PipelineResult, PipelineStatus, PipelineError
from pipeline.steps.base import PipelineStep
from pipeline.steps.docs_creation_step import NodeDocsCreationStep
from pipeline.steps.docs_integration_step import NodeDocsIntegrationStep
from pipeline.steps.content_analysis_step import ContentAnalysisStep
from pipeline.steps.line_number_step import LineNumberStep


class MDPipeline:
    """마크다운 파일 처리 파이프라인 (4단계 MD + 4단계 공통)"""
    
    def __init__(self):
        self.md_steps: List[PipelineStep] = []
        self.youtube_steps: List[PipelineStep] = []
        self.current_step_index = 0
        self.context: Dict[str, Any] = {}
        self._setup_md_steps()
        self._setup_youtube_steps()
    
    async def execute(self, md_file_path: str, metadata_info: Dict[str, str]) -> PipelineResult:
        """전체 MD 파이프라인 실행 (4단계 MD + 4단계 공통)"""
        print("🚀 마크다운 파이프라인 시작")
        print("=" * 60)
        
        # 초기 컨텍스트 설정
        self.context = {
            "md_file_path": md_file_path,
            "metadata_info": metadata_info
        }
        
        try:
            # 1-4단계: MD 전용 처리
            print("📝 1-4단계: 마크다운 전용 처리")
            for i, step in enumerate(self.md_steps):
                self.current_step_index = i + 1
                
                print(f"🔄 {self.current_step_index}/8단계: {step.name}")
                
                step_result = await step.execute(self.context)
                
                if not step_result.success:
                    return self._handle_step_failure(step, step_result.error)
                
                self.context.update(step_result.data)
                print(f"✅ {step.name} 완료")
                print("-" * 40)
            
            # 5-8단계: 유튜브 파이프라인 공통 단계 재사용 + 라인 번호 추가
            print("🔗 5-8단계: 공통 처리 단계 + 라인 번호 추가")
            for i, step in enumerate(self.youtube_steps):
                self.current_step_index = len(self.md_steps) + i + 1
                
                print(f"🔄 {self.current_step_index}/8단계: {step.name}")
                
                step_result = await step.execute(self.context)
                
                if not step_result.success:
                    return self._handle_step_failure(step, step_result.error)
                
                self.context.update(step_result.data)
                print(f"✅ {step.name} 완료")
                print("-" * 40)
            
            # 전체 성공
            print("🎉 전체 MD 파이프라인 완료!")
            print("=" * 60)
            
            return PipelineResult(
                status=PipelineStatus.SUCCESS,
                data=self.context,
                step_completed=len(self.md_steps) + len(self.youtube_steps),
                total_steps=len(self.md_steps) + len(self.youtube_steps)
            )
        
        except Exception as e:
            error_msg = f"MD 파이프라인 실행 중 예상치 못한 오류: {str(e)}"
            print(f"❌ {error_msg}")
            
            return PipelineResult(
                status=PipelineStatus.FAILED,
                data=self.context,
                error=error_msg,
                step_completed=self.current_step_index - 1,
                total_steps=len(self.md_steps) + len(self.youtube_steps)
            )
    
    async def execute_single_step(self, step_index: int, context: Dict[str, Any] = None) -> PipelineResult:
        """개별 단계 실행 (테스트/디버깅 용도)"""
        total_steps = len(self.md_steps) + len(self.youtube_steps)
        
        if step_index < 1 or step_index > total_steps:
            return PipelineResult(
                status=PipelineStatus.FAILED,
                error=f"잘못된 단계 번호: {step_index} (1-{total_steps} 범위)"
            )
        
        # MD 단계인지 유튜브 단계인지 결정
        if step_index <= len(self.md_steps):
            step = self.md_steps[step_index - 1]
        else:
            step = self.youtube_steps[step_index - len(self.md_steps) - 1]
        
        use_context = context or self.context
        
        try:
            print(f"🔍 단일 단계 실행: {step_index}단계 - {step.name}")
            step_result = await step.execute(use_context)
            
            if step_result.success:
                return PipelineResult(
                    status=PipelineStatus.SUCCESS,
                    data=step_result.data,
                    step_completed=1,
                    total_steps=1
                )
            else:
                return PipelineResult(
                    status=PipelineStatus.FAILED,
                    error=step_result.error,
                    step_completed=0,
                    total_steps=1
                )
        
        except Exception as e:
            return PipelineResult(
                status=PipelineStatus.FAILED,
                error=f"{step.name} 실행 오류: {str(e)}",
                step_completed=0,
                total_steps=1
            )
    
    def _setup_md_steps(self):
        """MD 전용 파이프라인 단계 초기화 (1-4단계)"""
        from pipeline.steps.md_metadata_step import MDMetadataCreationStep
        from pipeline.steps.md_source_step import MDSourceIntegrationStep
        from pipeline.steps.md_node_step import MDNodeGenerationStep
        from pipeline.steps.md_content_step import MDContentProcessingStep
        
        self.md_steps = [
            MDMetadataCreationStep(),        # 1단계: 메타데이터 생성 (UI 정보 + 빈 source)
            MDSourceIntegrationStep(),       # 2단계: source 통합 (source_updater.py)
            MDNodeGenerationStep(),          # 3단계: 노드 생성 (node_generator.py)
            MDContentProcessingStep()        # 4단계: 콘텐츠 처리 (header_cleaner.py → content.md)
        ]
    
    def _setup_youtube_steps(self):
        """유튜브 파이프라인 공통 단계 초기화 (5-8단계)"""
        self.youtube_steps = [
            NodeDocsCreationStep(),          # 5단계: 노드 문서 생성 (빈 템플릿)
            NodeDocsIntegrationStep(),       # 6단계: 노드 문서 통합 (메타데이터+내용)
            ContentAnalysisStep(),           # 7단계: 콘텐츠 분석 (통합된 노드 문서 분석)
            LineNumberStep()                 # 8단계: 라인 번호 추가 (content.md에 Line X: 형식 추가)
        ]
    
    def get_progress(self) -> Dict[str, Any]:
        """현재 진행 상황 조회"""
        total_steps = len(self.md_steps) + len(self.youtube_steps)
        all_steps = self.md_steps + self.youtube_steps
        
        return {
            "current_step": self.current_step_index,
            "total_steps": total_steps,
            "progress_percent": (self.current_step_index / total_steps) * 100,
            "current_step_name": all_steps[self.current_step_index - 1].name if self.current_step_index > 0 else None,
            "completed_steps": [step.name for step in all_steps[:self.current_step_index - 1]]
        }
    
    def _handle_step_failure(self, step: PipelineStep, error: str) -> PipelineResult:
        """단계 실패 처리"""
        print(f"❌ {step.name} 실패: {error}")
        print("=" * 60)
        
        return PipelineResult(
            status=PipelineStatus.FAILED,
            data=self.context,
            error=f"{step.name} 실패: {error}",
            step_completed=self.current_step_index - 1,
            total_steps=len(self.md_steps) + len(self.youtube_steps)
        )