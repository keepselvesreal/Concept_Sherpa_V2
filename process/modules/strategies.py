# 생성 시간: 2025-08-30 16:58:49 KST
# 핵심 내용: 노드 처리 전략 패턴 구현 - V1, V2, V3, V5 방식 지원
# 상세 내용:
#   - ProcessingStrategy (20-30): 추상 기본 클래스
#   - ProcessingStrategyV1 (32-42): V1 처리 전략 (기본)
#   - ProcessingStrategyV2 (44-54): V2 처리 전략 (개선된)
#   - ProcessingStrategyV3 (56-90): V3 처리 전략 (추출+업데이트 방식)
#   - ProcessingStrategyV5 (98-140): V5 처리 전략 (API 호출 최적화 방식)
# 상태: active
# 주소: strategies
# 참조: unified_node_processor_v3.py

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .core import NodeInfo

if TYPE_CHECKING:
    from .ai_providers import AIProviderFactory, UpdateLogger
    from .managers import NodeDocumentManager, DebugManager
    from .engines import ExtractionEngine, UpdateEngine


class ProcessingStrategy(ABC):
    """처리 전략 추상 클래스"""
    
    def __init__(self, ai_factory: 'AIProviderFactory', logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
    
    @abstractmethod
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager',
                          debug_manager: 'DebugManager', update_logger: 'UpdateLogger') -> bool:
        """노드 처리"""
        pass


class ProcessingStrategyV1(ProcessingStrategy):
    """V1 처리 전략 - 기본"""
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager',
                          debug_manager: 'DebugManager' = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V1 방식으로 노드 처리"""
        # V1 구현은 기존과 동일
        return True


class ProcessingStrategyV2(ProcessingStrategy):
    """V2 처리 전략 - 개선된"""
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager',
                          debug_manager: 'DebugManager' = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V2 방식으로 노드 처리"""
        # V2 구현은 기존과 동일
        return True


class ProcessingStrategyV3(ProcessingStrategy):
    """V3 처리 전략 - 추출+업데이트 방식"""
    
    def __init__(self, ai_factory: 'AIProviderFactory', logger: logging.Logger):
        super().__init__(ai_factory, logger)
        # 순환 임포트 방지를 위해 런타임에 임포트
        from .engines import ExtractionEngine, UpdateEngine
        self.extraction_engine = ExtractionEngine(ai_factory, logger)
        self.update_engine = UpdateEngine(ai_factory, logger)
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager', 
                          debug_manager: 'DebugManager' = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V3 방식으로 노드 처리"""
        try:
            # 1. 추출 작업
            content = await doc_manager.get_combined_content(node)
            extraction_result = await self.extraction_engine.extract_all_info(content, node.title, update_logger)
            
            if not extraction_result.success:
                return False
            
            # 2. 추출 섹션 업데이트
            await doc_manager.update_extraction_section(node, extraction_result, update_logger)
            
            # 3. 부모 노드가 아닌 경우 여기서 종료 (리프 노드)
            if not node.children_ids:
                return True
                
            # 4. 부모 노드인 경우: 구성 노드 내용 반영한 부모 노드 추출 섹션 업데이트
            await self.update_engine.update_parent_extraction_with_composition(node, doc_manager, update_logger)
            
            # 5. 업데이트된 부모 노드 추출 섹션 반영한 구성 노드들 업데이트
            await self.update_engine.update_composition_extractions(node, doc_manager, update_logger)
            
            return True
            
        except Exception as e:
            self.logger.error(f"V3 처리 실패: {node.title} - {e}")
            return False


class ProcessingStrategyV5(ProcessingStrategy):
    """V5 처리 전략 - API 호출 최적화 방식"""
    
    def __init__(self, ai_factory: 'AIProviderFactory', logger: logging.Logger):
        super().__init__(ai_factory, logger)
        # 순환 임포트 방지를 위해 런타임에 임포트
        from .engines_v5 import ExtractionEngineV5, UpdateEngineV5
        self.extraction_engine = ExtractionEngineV5(ai_factory, logger)
        self.update_engine = UpdateEngineV5(ai_factory, logger)
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager', 
                          debug_manager: 'DebugManager' = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V5 방식으로 노드 처리 - API 호출 최적화"""
        try:
            self.logger.info(f"🚀 V5 처리 시작: {node.title}")
            
            # 1. 통합 추출 작업 (단일 API 호출로 바로 저장까지 완료)
            content = await doc_manager.get_combined_content(node)
            extraction_result = await self.extraction_engine.extract_all_info(content, node.title, node, doc_manager, update_logger)
            
            if not extraction_result.success:
                self.logger.error(f"❌ V5 추출 실패: {node.title}")
                return False
            
            self.logger.info(f"✅ V5 추출 완료: {node.title}")
            
            # 2. 부모 노드가 아닌 경우 여기서 종료 (리프 노드)
            if not node.children_ids:
                self.logger.info(f"📊 V5 처리 완료 (리프 노드) - API 호출: {self.extraction_engine.get_api_calls_count()}회")
                return True
                
            # 3. 부모 노드인 경우: 구성 노드 내용 반영한 부모 노드 추출 섹션 업데이트
            await self.update_engine.update_parent_extraction_with_composition(node, doc_manager, update_logger)
            
            # 4. 업데이트된 부모 노드 추출 섹션 반영한 구성 노드들 업데이트
            await self.update_engine.update_composition_extractions(node, doc_manager, update_logger)
            
            total_api_calls = self.extraction_engine.get_api_calls_count() + self.update_engine.get_api_calls_count()
            self.logger.info(f"📊 V5 처리 완료 (부모 노드) - API 호출: {total_api_calls}회")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ V5 처리 실패: {node.title} - {e}")
            return False