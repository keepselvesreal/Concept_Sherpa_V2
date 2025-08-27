# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 파이프라인 데이터 모델 및 에러 처리 단순화
# 상세 내용:
#   - PipelineStatus (라인 14-18): 파이프라인 상태 열거형
#   - PipelineResult (라인 20-35): 단순화된 결과 데이터 클래스
#   - PipelineError (라인 37-45): 파이프라인 전용 예외 클래스
# 상태: active
# 주소: pipeline/models
# 참조: 복잡한 부분 성공 타입 제거, 단순한 성공/실패 구조

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from enum import Enum


class PipelineStatus(Enum):
    """파이프라인 실행 상태"""
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class PipelineResult:
    """단순화된 파이프라인 결과"""
    status: PipelineStatus
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    step_completed: int = 0
    total_steps: int = 7
    
    @property
    def progress_percent(self) -> float:
        """진행률 계산"""
        if self.total_steps == 0:
            return 100.0
        return (self.step_completed / self.total_steps) * 100
    
    @property
    def is_success(self) -> bool:
        """성공 여부"""
        return self.status == PipelineStatus.SUCCESS


class PipelineError(Exception):
    """파이프라인 전용 예외 클래스"""
    
    def __init__(self, message: str, step_name: str, step_index: int):
        self.message = message
        self.step_name = step_name
        self.step_index = step_index
        super().__init__(f"[{step_name}] {message}")


@dataclass
class StepResult:
    """개별 단계 결과"""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    @classmethod
    def success_result(cls, data: Dict[str, Any] = None) -> 'StepResult':
        """성공 결과 생성"""
        return cls(success=True, data=data or {})
    
    @classmethod
    def error_result(cls, error: str) -> 'StepResult':
        """실패 결과 생성"""
        return cls(success=False, error=error)