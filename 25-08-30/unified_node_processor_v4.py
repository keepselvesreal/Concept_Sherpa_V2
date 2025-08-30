# 생성 시간: 2025-08-30 17:15:00 KST
# 핵심 내용: 통합 노드 정보 문서의 추출 섹션 자동 생성/업데이트 시스템 - 완전 모듈화 버전
# 상세 내용:
#   - UnifiedNodeProcessor 클래스 (40-180): 메인 처리 시스템 및 작업 조율
#   - 완전 모듈화된 구조: modules 패키지에서 모든 컴포넌트들을 import
# 상태: active
# 주소: unified_node_processor_v4
# 참조: unified_node_processor_v3.py (모듈화 이전 버전)

import asyncio
import json
import logging
import os
import yaml
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set

# 모듈화된 컴포넌트들 import
from modules import (
    ProcessingMode, AIProvider, NodeInfo, ExtractionResult, ProcessingStatus, UpdateLogEntry,
    AIProviderFactory, UpdateLogger,
    ProcessingStrategy, ProcessingStrategyV1, ProcessingStrategyV2, ProcessingStrategyV3,
    NodeDocumentManager, DebugManager,
    ExtractionEngine, UpdateEngine,
    NodeTraverser, ProgressTracker
)


class UnifiedNodeProcessor:
    """통합 노드 처리 시스템"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logger()
        
        # 컴포넌트 초기화
        self.ai_factory = AIProviderFactory(self.config, self.logger)
        self.doc_manager = NodeDocumentManager(self.config, self.logger)
        self.traverser = NodeTraverser(self.logger)
        self.tracker = ProgressTracker(self.logger)
        self.debug_manager = DebugManager(Path(self.config['debug_dir']), self.logger)
        
        # 처리 전략 초기화
        self.strategy = self._create_strategy()
        
        self.logger.info(f"✅ UnifiedNodeProcessor 초기화 완료")
        self.logger.info(f"🔧 처리 모드: {self.config.get('processing_mode', 'v3')}")
        self.logger.info(f"🤖 AI 프로바이더: {self.config.get('ai_provider', 'gemini')}")
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로딩"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # 기본 설정 적용
            defaults = {
                'debug_dir': './25-08-30',
                'processing_mode': 'v3',
                'ai_provider': 'gemini'
            }
            for key, value in defaults.items():
                if key not in config:
                    config[key] = value
                    
            return config
        except Exception as e:
            print(f"❌ 설정 파일 로딩 실패: {e}")
            raise
    
    def _setup_logger(self) -> logging.Logger:
        """로거 설정"""
        logger = logging.getLogger('unified_node_processor')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _create_strategy(self) -> ProcessingStrategy:
        """처리 전략 생성"""
        mode = ProcessingMode(self.config.get('processing_mode', 'v3'))
        
        if mode == ProcessingMode.V1:
            return ProcessingStrategyV1(self.ai_factory, self.logger)
        elif mode == ProcessingMode.V2:
            return ProcessingStrategyV2(self.ai_factory, self.logger)
        elif mode == ProcessingMode.V3:
            return ProcessingStrategyV3(self.ai_factory, self.logger)
        else:
            raise ValueError(f"지원되지 않는 처리 모드: {mode}")
    
    async def process_all_nodes(self) -> Dict[str, Any]:
        """모든 노드 처리"""
        self.logger.info("🚀 노드 처리 시작")
        self.tracker.start_processing()
        
        try:
            # 1. 노드 정보 로딩
            nodes = await self.doc_manager.load_nodes_info()
            self.logger.info(f"📋 로딩된 노드 수: {len(nodes)}")
            
            # 2. 처리할 노드들 필터링 (process_status가 False인 노드들만)
            nodes_to_process = [node for node in nodes if not node.process_status]
            self.logger.info(f"🎯 처리 대상 노드 수: {len(nodes_to_process)}")
            
            if not nodes_to_process:
                self.logger.info("✅ 처리할 노드가 없습니다.")
                return {
                    'success': True,
                    'total_nodes': 0,
                    'processed_nodes': 0,
                    'failed_nodes': 0,
                    'duration': "0:00:00",
                    'errors': []
                }
            
            # 3. 노드 순회 순서 결정 (bottom-up)
            processing_order = self.traverser.get_processing_order(nodes_to_process)
            self.tracker.set_total_nodes(len(nodes_to_process))
            
            self.logger.info("📊 처리 순서:")
            total_nodes_in_order = 0
            for level_idx, level_nodes in enumerate(processing_order):
                self.logger.info(f"  레벨 {level_idx + 1}: {len(level_nodes)}개 노드")
                total_nodes_in_order += len(level_nodes)
            
            # 4. 레벨별로 순차 처리
            update_logger = UpdateLogger(Path(self.config['debug_dir']))
            
            for level_idx, level_nodes in enumerate(processing_order):
                self.logger.info(f"🔄 레벨 {level_idx + 1} 처리 시작 ({len(level_nodes)}개 노드)")
                
                for node in level_nodes:
                    self.logger.info(f"🎯 노드 처리 시작: {node.title}")
                    self.tracker.set_current_node(node.title)
                    
                    try:
                        # 전략 패턴을 사용한 노드 처리
                        success = await self.strategy.process_node(
                            node, self.doc_manager, self.debug_manager, update_logger
                        )
                        
                        if success:
                            # process_status를 True로 변경
                            await self.doc_manager.update_process_status(node, True)
                            self.tracker.mark_completed(node.title)
                            self.logger.info(f"✅ 노드 처리 완료: {node.title}")
                        else:
                            self.tracker.mark_failed(node.title, "처리 실패")
                            self.logger.error(f"❌ 노드 처리 실패: {node.title}")
                        
                    except Exception as e:
                        error_msg = str(e)
                        self.tracker.mark_failed(node.title, error_msg)
                        self.logger.error(f"❌ 노드 처리 중 오류: {node.title} - {error_msg}")
            
            # 5. 로그 저장
            update_logger.save_logs()
            
        except Exception as e:
            self.logger.error(f"❌ 전체 처리 중 오류 발생: {e}")
            self.tracker.add_error(f"시스템 오류: {e}")
        
        return self.tracker.get_final_result()


# CLI 인터페이스
async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='통합 노드 정보 문서 처리 시스템 v4')
    parser.add_argument('--config', default='./config.yaml', help='설정 파일 경로')
    parser.add_argument('--ai-provider', choices=['gemini', 'claude', 'openai'], 
                       help='AI 프로바이더 선택')
    parser.add_argument('--processing-mode', choices=['v1', 'v2', 'v3'], default='v3',
                       help='처리 방식 선택')
    parser.add_argument('--debug-dir', default='./25-08-30',
                       help='디버깅 폴더 경로')
    
    args = parser.parse_args()
    
    # 설정 오버라이드
    config_path = args.config
    overrides = {}
    if args.ai_provider:
        overrides['ai_provider'] = args.ai_provider
    if args.processing_mode:
        overrides['processing_mode'] = args.processing_mode
    if args.debug_dir:
        overrides['debug_dir'] = args.debug_dir
    
    try:
        processor = UnifiedNodeProcessor(config_path)
        
        # 설정 오버라이드 적용
        for key, value in overrides.items():
            processor.config[key] = value
        
        print(f"🚀 통합 노드 처리 시작 (v4)")
        print(f"📋 AI 프로바이더: {processor.config.get('ai_provider', 'gemini')}")
        print(f"📋 처리 방식: {processor.config.get('processing_mode', 'v3')}")
        print(f"📁 디버깅 폴더: {processor.config.get('debug_dir', './25-08-30')}")
        
        result = await processor.process_all_nodes()
        
        if result['success']:
            print(f"\n✅ 전체 처리 완료!")
            print(f"📊 처리된 노드: {result['processed_nodes']}/{result['total_nodes']}")
            print(f"⏱️ 소요 시간: {result['duration']}")
        else:
            print(f"\n❌ 처리 실패!")
            print(f"📊 실패한 노드: {result['failed_nodes']}/{result['total_nodes']}")
            if result['errors']:
                print("오류 목록:")
                for error in result['errors']:
                    print(f"  - {error}")
    
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))