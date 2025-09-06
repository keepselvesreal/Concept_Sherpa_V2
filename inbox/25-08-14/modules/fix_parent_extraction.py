#!/usr/bin/env python3
"""
부모 노드 추출 섹션 복원 스크립트
"""

import asyncio
import json
from pathlib import Path
from parent_node_processor import ParentNodeProcessor

async def fix_parent_extraction():
    """부모 노드 추출 섹션만 복원"""
    print("=" * 50)
    print("부모 노드 추출 섹션 복원")
    print("=" * 50)
    
    # 설정
    node_docs_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/node_docs_v2"
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/nodes.json"
    
    # JSON 로드
    with open(json_path, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    # 부모 노드 찾기 (레벨 0)
    parent_node = None
    for node in nodes:
        if node.get("level") == 0:
            parent_node = node
            break
    
    if not parent_node:
        print("❌ 부모 노드를 찾을 수 없습니다")
        return
    
    print(f"🎯 부모 노드: {parent_node['title']}")
    
    # 처리기 초기화
    processor = ParentNodeProcessor(node_docs_dir)
    
    # 부모 노드 추출만 실행
    print("📋 부모 노드 추출 시작...")
    try:
        result = await processor.process_parent_extraction(parent_node)
        if result:
            print("✅ 부모 노드 추출 완료!")
        else:
            print("❌ 부모 노드 추출 실패!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(fix_parent_extraction())