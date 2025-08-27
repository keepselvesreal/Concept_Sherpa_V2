# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 파이프라인 단계 기본 클래스 (비동기 처리 통일)
# 상세 내용:
#   - PipelineStep (라인 13-40): 추상 기본 클래스, 모든 단계가 async/await 사용
#   - AsyncStepMixin (라인 42-55): 비동기 유틸리티 믹스인 클래스
# 상태: active
# 주소: pipeline/steps/base
# 참조: 모든 단계를 async/await으로 통일

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models import StepResult


class PipelineStep(ABC):
    """파이프라인 단계 추상 기본 클래스 (비동기 통일)"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """
        단계 실행 (모든 하위 클래스에서 async로 구현)
        
        Args:
            context: 이전 단계들에서 전달된 컨텍스트 데이터
            
        Returns:
            StepResult: 성공/실패와 함께 다음 단계로 전달할 데이터
        """
        pass
    
    async def _run_sync_function(self, func, *args, **kwargs):
        """
        동기 함수를 비동기로 실행
        blocking 함수를 executor에서 실행하여 비동기화
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    
    def _log_step_start(self):
        """단계 시작 로그"""
        print(f"🔄 {self.name} 시작...")
    
    def _log_step_success(self):
        """단계 성공 로그"""
        print(f"✅ {self.name} 완료")
    
    def _log_step_error(self, error: str):
        """단계 실패 로그"""
        print(f"❌ {self.name} 실패: {error}")


class AsyncStepMixin:
    """비동기 처리 유틸리티 믹스인"""
    
    async def run_with_timeout(self, coro, timeout_seconds: int = 300):
        """타임아웃과 함께 코루틴 실행"""
        try:
            return await asyncio.wait_for(coro, timeout=timeout_seconds)
        except asyncio.TimeoutError:
            raise Exception(f"작업이 {timeout_seconds}초 내에 완료되지 않았습니다")
    
    async def run_parallel(self, *coros):
        """여러 코루틴을 병렬로 실행"""
        return await asyncio.gather(*coros)