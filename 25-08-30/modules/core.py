# 생성 시간: 2025-08-30 16:58:49 KST
# 핵심 내용: 통합 노드 처리 시스템의 핵심 데이터 클래스들과 열거형 정의
# 상세 내용:
#   - ProcessingMode (10-15): 처리 모드 열거형 (V1, V2, V3)
#   - AIProvider (17-22): AI 프로바이더 열거형 (GEMINI, CLAUDE, OPENAI)
#   - NodeInfo (24-35): 노드 정보 데이터 클래스
#   - ExtractionResult (37-48): 추출 결과 데이터 클래스
#   - ProcessingStatus (50-56): 처리 상태 데이터 클래스
#   - UpdateLogEntry (58-68): 업데이트 로그 엔트리 데이터 클래스
# 상태: active
# 주소: core
# 참조: unified_node_processor_v3.py

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ProcessingMode(Enum):
    """처리 모드"""
    V1 = "v1"
    V2 = "v2" 
    V3 = "v3"  # 추출→업데이트 방식
    V5 = "v5"  # API 호출 최적화 방식


class AIProvider(Enum):
    """AI 프로바이더"""
    GEMINI = "gemini"
    CLAUDE = "claude"
    OPENAI = "openai"


@dataclass
class NodeInfo:
    """노드 정보"""
    id: int
    title: str
    level: int
    parent_id: Optional[int]
    children_ids: List[int]
    has_content: bool
    document_path: Optional[str] = None
    process_status: bool = False


@dataclass
class ExtractionResult:
    """추출 결과"""
    core_content: str = ""
    detailed_core_content: str = ""
    detailed_content: str = ""  # 새로 추가된 정보 타입
    main_topics: str = ""
    sub_topics: str = ""
    success: bool = False
    error: Optional[str] = None


@dataclass
class ProcessingStatus:
    """처리 상태"""
    total_nodes: int = 0
    processed_nodes: int = 0
    failed_nodes: int = 0


@dataclass
class UpdateLogEntry:
    """업데이트 로그 엔트리"""
    timestamp: str
    node_title: str
    section_type: str
    before_content: str
    after_content: str
    ai_model: str
    prompt_tokens: int
    response_tokens: int