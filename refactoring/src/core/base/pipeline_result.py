# 생성 시간: Mon Sep  3 17:03:35 KST 2025
# 핵심 내용: 파이프라인 실행 결과 관리 클래스들
# 상세 내용:
#   - StageResult (라인 12-35): 단계별 실행 결과 클래스
#   - PipelineResult (라인 37-82): 전체 파이프라인 실행 결과 클래스
#   - add_stage_result (라인 57-66): 단계 결과 추가
#   - update_progress (라인 68-73): 진행률 업데이트
#   - set_success (라인 75-82): 성공 상태 설정
# 상태: active

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class StageResult:
    """단계별 실행 결과"""
    stage_name: str
    success: bool = False
    error: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()
    
    def complete(self, success: bool = True, error: str = None, data: Dict[str, Any] = None):
        """단계 완료 처리"""
        self.end_time = datetime.now()
        self.success = success
        self.error = error
        if data:
            self.data.update(data)
        
        if self.start_time and self.end_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()

class PipelineResult:
    """전체 파이프라인 실행 결과"""
    
    def __init__(self, total_stages: int = 4):
        self.is_success = False
        self.error = None
        self.data = {}
        self.stage_results: List[StageResult] = []
        self.total_stages = total_stages
        self.completed_stages = 0
        self.progress_percent = 0
        self.start_time = datetime.now()
        self.end_time = None
        
    @property  
    def current_stage(self) -> int:
        """현재 진행 중인 단계 번호 (1부터 시작)"""
        return len(self.stage_results) + 1
        
    def add_stage_result(self, stage_result: StageResult):
        """단계 결과 추가"""
        self.stage_results.append(stage_result)
        
        if stage_result.success:
            self.completed_stages += 1
            
        self.update_progress()
        
    def update_progress(self):
        """진행률 업데이트"""
        self.progress_percent = int((self.completed_stages / self.total_stages) * 100)
        
    def set_success(self, success: bool = True, error: str = None):
        """성공 상태 설정"""
        self.is_success = success
        self.error = error
        self.end_time = datetime.now()
        
        if success:
            self.progress_percent = 100
            self.completed_stages = self.total_stages