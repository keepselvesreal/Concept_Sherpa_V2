# 생성 시간: 2025-08-30 17:15:00 KST
# 핵심 내용: 통합 노드 처리 시스템의 유틸리티 클래스들
# 상세 내용:
#   - NodeTraverser (20-50): bottom-up 노드 순회 관리
#   - ProgressTracker (52-100): 진행률 추적 및 오류 관리
#   - DebugManager (102-130): 디버깅용 파일 저장 관리
# 상태: active
# 주소: utils
# 참조: unified_node_processor_v3.py

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from .core import NodeInfo, ProcessingStatus


class NodeTraverser:
    """노드 순회 관리자"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def get_processing_order(self, nodes: List[NodeInfo]) -> List[List[NodeInfo]]:
        """bottom-up 처리 순서 결정"""
        # 레벨별로 노드 그룹핑
        level_groups = {}
        for node in nodes:
            if node.level not in level_groups:
                level_groups[node.level] = []
            level_groups[node.level].append(node)
        
        # 레벨 순서대로 정렬 (높은 레벨부터 - 리프 노드부터)
        sorted_levels = sorted(level_groups.keys(), reverse=True)
        
        processing_order = []
        for level in sorted_levels:
            processing_order.append(level_groups[level])
        
        return processing_order


class ProgressTracker:
    """진행률 추적기"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.start_time = None
        self.status = ProcessingStatus()
        self.current_node = ""
        self.errors = []
    
    def start_processing(self):
        """처리 시작"""
        self.start_time = datetime.now()
        self.status = ProcessingStatus()
    
    def set_total_nodes(self, total: int):
        """전체 노드 수 설정"""
        self.status.total_nodes = total
    
    def set_current_node(self, node_title: str):
        """현재 처리 중인 노드 설정"""
        self.current_node = node_title
    
    def mark_completed(self, node_title: str):
        """노드 완료 처리"""
        self.status.processed_nodes += 1
    
    def mark_failed(self, node_title: str, error: str):
        """노드 실패 처리"""
        self.status.failed_nodes += 1
        self.add_error(f"{node_title}: {error}")
    
    def add_error(self, error: str):
        """오류 추가"""
        self.errors.append(error)
    
    def get_final_result(self) -> Dict[str, Any]:
        """최종 결과 반환"""
        end_time = datetime.now()
        duration = str(end_time - self.start_time) if self.start_time else "Unknown"
        
        return {
            'success': self.status.failed_nodes == 0,
            'total_nodes': self.status.total_nodes,
            'processed_nodes': self.status.processed_nodes,
            'failed_nodes': self.status.failed_nodes,
            'duration': duration,
            'errors': self.errors
        }


class DebugManager:
    """디버깅 관리자"""
    
    def __init__(self, debug_dir: Path, logger: logging.Logger):
        self.debug_dir = debug_dir
        self.logger = logger
        
        # 디버그 디렉토리 생성
        self.debug_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_debug_info(self, filename: str, content: str):
        """디버그 정보 저장"""
        try:
            debug_file = self.debug_dir / filename
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.debug(f"디버그 파일 저장: {filename}")
        except Exception as e:
            self.logger.error(f"디버그 파일 저장 실패: {filename} - {e}")