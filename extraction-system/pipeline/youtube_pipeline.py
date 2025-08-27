# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: YouTube 처리 파이프라인 메인 클래스
# 상세 내용:
#   - YouTubePipeline (라인 18-95): 7단계 파이프라인 오케스트레이션 클래스
#   - _setup_steps() (라인 97-115): 단계별 클래스 초기화
#   - get_progress() (라인 117-125): 진행 상황 조회 메서드
#   - _handle_step_failure() (라인 127-135): 실패 처리 메서드
# 상태: active
# 주소: pipeline/youtube_pipeline
# 참조: 단순화된 에러 처리와 비동기 통일 적용

import asyncio
from typing import Dict, Any, List
from .models import PipelineResult, PipelineStatus, PipelineError
from .steps.base import PipelineStep
from .steps.metadata_step import MetadataCreationStep
from .steps.youtube_step import YouTubeExtractionStep
from .steps.transcript_step import TranscriptImprovementStep
from .steps.node_step import NodeGenerationStep
from .steps.docs_creation_step import NodeDocsCreationStep
from .steps.docs_integration_step import NodeDocsIntegrationStep
from .steps.content_extraction_step import NodeContentExtractionStep
from .steps.content_analysis_step import ContentAnalysisStep


class YouTubePipeline:
    """YouTube 처리 7단계 파이프라인"""
    
    def __init__(self):
        self.steps: List[PipelineStep] = []
        self.current_step_index = 0
        self.context: Dict[str, Any] = {}
        self._setup_steps()
    
    async def execute(self, url: str, metadata_info: Dict[str, str]) -> PipelineResult:
        """전체 파이프라인 실행"""
        print("🚀 YouTube 파이프라인 시작")
        print("=" * 60)
        
        # 초기 컨텍스트 설정
        self.context = {
            "url": url,
            "metadata_info": metadata_info
        }
        
        try:
            # 각 단계 순차 실행
            for i, step in enumerate(self.steps):
                self.current_step_index = i + 1
                
                print(f"🔄 {self.current_step_index}/7단계: {step.name}")
                
                # 단계 실행
                step_result = await step.execute(self.context)
                
                if not step_result.success:
                    # 실패 시 즉시 종료 (Fail-Fast)
                    return self._handle_step_failure(step, step_result.error)
                
                # 성공 시 컨텍스트 업데이트
                self.context.update(step_result.data)
                print(f"✅ {step.name} 완료")
                print("-" * 40)
            
            # 전체 성공
            print("🎉 전체 파이프라인 완료!")
            print("=" * 60)
            
            return PipelineResult(
                status=PipelineStatus.SUCCESS,
                data=self.context,
                step_completed=len(self.steps),
                total_steps=len(self.steps)
            )
        
        except Exception as e:
            # 예상치 못한 오류 처리
            error_msg = f"파이프라인 실행 중 예상치 못한 오류: {str(e)}"
            print(f"❌ {error_msg}")
            
            return PipelineResult(
                status=PipelineStatus.FAILED,
                data=self.context,
                error=error_msg,
                step_completed=self.current_step_index - 1,
                total_steps=len(self.steps)
            )
    
    async def execute_single_step(self, step_index: int, context: Dict[str, Any] = None) -> PipelineResult:
        """개별 단계 실행 (테스트/디버깅 용도)"""
        if step_index < 1 or step_index > len(self.steps):
            return PipelineResult(
                status=PipelineStatus.FAILED,
                error=f"잘못된 단계 번호: {step_index} (1-{len(self.steps)} 범위)"
            )
        
        step = self.steps[step_index - 1]
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
    
    def _setup_steps(self):
        """파이프라인 단계 초기화"""
        self.steps = [
            MetadataCreationStep(),           # 1단계: 메타데이터 생성
            YouTubeExtractionStep(),          # 2단계: YouTube 스크립트 추출
            TranscriptImprovementStep(),      # 3단계: 스크립트 개선
            NodeGenerationStep(),             # 4단계: 노드 생성
            NodeDocsCreationStep(),           # 5단계: 노드 문서 생성 (빈 템플릿)
            NodeDocsIntegrationStep(),        # 6단계: 노드 문서 통합 (메타데이터+내용)
            ContentAnalysisStep()             # 7단계: 콘텐츠 분석 (통합된 노드 문서 분석)
            # NodeContentExtractionStep()     # 더 이상 사용하지 않음 (ContentAnalysisStep으로 대체)
        ]
    
    def get_progress(self) -> Dict[str, Any]:
        """현재 진행 상황 조회"""
        return {
            "current_step": self.current_step_index,
            "total_steps": len(self.steps),
            "progress_percent": (self.current_step_index / len(self.steps)) * 100,
            "current_step_name": self.steps[self.current_step_index - 1].name if self.current_step_index > 0 else None,
            "completed_steps": [step.name for step in self.steps[:self.current_step_index - 1]]
        }
    
    def _handle_step_failure(self, step: PipelineStep, error: str) -> PipelineResult:
        """단계 실패 처리 (단순화된 버전)"""
        print(f"❌ {step.name} 실패: {error}")
        print("=" * 60)
        
        return PipelineResult(
            status=PipelineStatus.FAILED,
            data=self.context,
            error=f"{step.name} 실패: {error}",
            step_completed=self.current_step_index - 1,
            total_steps=len(self.steps)
        )