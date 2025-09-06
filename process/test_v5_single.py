#!/usr/bin/env python3
# 생성 시간: 2025-01-02 15:40:00 KST
# 핵심 내용: process 디렉토리에서 V5 엔진 직접 테스트
# 상세 내용:
#   - main (10-80): 25번 노드 V5 처리 테스트 (process 디렉토리 내에서 실행)
# 상태: active
# 참조: 없음

import asyncio
import logging
import sys
import os
from pathlib import Path
import yaml

# 현재 디렉토리를 Python path에 추가
sys.path.append('.')

async def test_v5_single_node():
    """25번 노드 V5 처리 테스트"""
    from modules.engines_v5 import ExtractionEngineV5
    from modules.ai_providers import AIProviderFactory
    from modules.managers import NodeDocumentManager
    from modules.core import NodeInfo
    
    # 설정 파일 로드
    config_path = "../test_config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 로깅 설정
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # AI 팩토리 초기화 (프로바이더 자동 설정)
    ai_factory = AIProviderFactory(config, logger)
    
    # V5 엔진 초기화
    extraction_engine = ExtractionEngineV5(ai_factory, logger)
    
    # 추가 매니저들 초기화
    from modules.managers import DebugManager
    from modules.ai_providers import UpdateLogger
    
    debug_dir = Path(config['debug_dir'])
    debug_manager = DebugManager(debug_dir, logger)
    update_logger = UpdateLogger()
    
    # 노드 문서 매니저 초기화
    node_docs_dir = Path(config['node_docs_dir'])
    nodes_json_path = Path(config['nodes_json_path'])
    doc_manager = NodeDocumentManager(
        node_docs_dir, ai_factory, debug_manager, 
        update_logger, logger, nodes_json_path
    )
    
    # 테스트할 노드 정보 생성 (58번 파일 - 6.1장)
    test_node = NodeInfo(
        id=58,
        title="6.1_The_simplicity_of_data_oriented_test_cases", 
        level=2,
        parent_id=57,  # 6_Unit_tests
        children_ids=[],
        has_content=True
    )
    
    print(f"🚀 V5 엔진 테스트 시작: {test_node.title}")
    
    try:
        # 노드의 통합 콘텐츠 가져오기
        content = await doc_manager.get_combined_content(test_node)
        print(f"📄 콘텐츠 길이: {len(content)} 문자")
        
        # V5 추출 실행
        print("🔍 V5 추출 실행...")
        result = await extraction_engine.extract_all_info(
            content, 
            test_node.title, 
            test_node, 
            doc_manager, 
            update_logger=None
        )
        
        if result.success:
            print(f"✅ V5 추출 성공: {test_node.title}")
            print(f"📊 API 호출 횟수: {extraction_engine.get_api_calls_count()}")
            print("📝 결과를 확인해보세요:")
            print(f"   파일: {node_docs_dir}/25_lev3_1.2.4_Complex_class_hierarchies_info.md")
        else:
            print(f"❌ V5 추출 실패: {test_node.title}")
            if result.error:
                print(f"오류: {result.error}")
        
        return result.success
        
    except Exception as e:
        logger.error(f"❌ 테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 현재 작업 디렉토리 변경
    os.chdir('/home/nadle/projects/Knowledge_Sherpa/v2/process')
    
    # 비동기 실행
    result = asyncio.run(test_v5_single_node())
    print(f"\n🎯 최종 결과: {'성공' if result else '실패'}")