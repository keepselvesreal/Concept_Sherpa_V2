"""
생성 시간: 2025-08-14 21:25:00 KST
핵심 내용: 자식 노드 처리 로직 디버깅 - process_single_child_node 시뮬레이션
상세 내용:
    - 실제 parent_node_processor의 process_single_child_node 로직 재현
    - DataLoader.load_for_extraction vs _extract_section_from_file 차이 분석
    - 자식 노드 처리가 스킵되는 정확한 원인 파악
상태: 디버깅용
주소: debug_child_processing
참조: parent_node_processor.py
"""

from pathlib import Path
import sys
import os
import json

# 상위 디렉토리에서 모듈 임포트 가능하게 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.parent_node_processor import DataLoader, ParentNodeProcessor
from modules.logging_system_v2 import ProcessLogger

async def debug_child_processing():
    """자식 노드 처리 로직 디버깅"""
    
    print("=" * 60)
    print("자식 노드 처리 로직 디버깅")
    print("=" * 60)
    
    # 테스트 설정
    node_docs_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/node_docs"
    test_file = Path(node_docs_dir) / "01_lev1_introduction_and_overview_info.md"
    
    print(f"테스트 파일: {test_file}")
    
    if not test_file.exists():
        print(f"❌ 파일이 존재하지 않습니다: {test_file}")
        return
    
    # 1. DataLoader 초기화
    logger = ProcessLogger("debug_child", Path("/tmp"))
    data_loader = DataLoader(Path(node_docs_dir), logger)
    
    # 2. process_single_child_node와 동일한 로직 실행
    print("\n1️⃣ process_single_child_node 로직 시뮬레이션:")
    print("-" * 50)
    
    try:
        # 자식 노드의 내용 섹션 로드 (실제 코드와 동일)
        content = data_loader._extract_section_from_file(test_file, "내용")
        
        print(f"추출된 내용 길이: {len(content)}")
        print(f"content.strip() 결과: {len(content.strip())}")
        print(f"not content.strip(): {not content.strip()}")
        
        if not content.strip():
            print("❌ 빈 내용으로 판단됨 - 여기서 스킵됨!")
            return
        else:
            print("✅ 내용이 있음 - 추출 작업 진행해야 함")
            print(f"내용 미리보기 (첫 200자): {content[:200]}")
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return
    
    # 3. 노드 데이터와 load_for_extraction 비교 테스트
    print("\n2️⃣ load_for_extraction vs 직접 추출 비교:")
    print("-" * 50)
    
    # nodes.json에서 해당 노드 정보 로드
    nodes_file = Path(node_docs_dir).parent / "nodes.json"
    with open(nodes_file, 'r', encoding='utf-8') as f:
        nodes_data = json.load(f)
    
    # 해당 노드 찾기 (id=1인 노드)
    target_node = None
    for node in nodes_data:
        if node['id'] == 1:  # introduction_and_overview
            target_node = node
            break
    
    if target_node:
        print(f"타겟 노드: {target_node['title']}")
        
        # load_for_extraction 결과
        extraction_data = data_loader.load_for_extraction(target_node)
        print(f"load_for_extraction 결과 길이: {len(extraction_data)}")
        print(f"load_for_extraction 결과 (첫 200자): {extraction_data[:200]}")
        
        if not extraction_data.strip():
            print("❌ load_for_extraction에서 빈 결과!")
        else:
            print("✅ load_for_extraction에서 정상 결과")
    else:
        print("❌ 타겟 노드를 찾을 수 없습니다")
    
    # 4. ParentNodeProcessor 초기화해서 실제 테스트
    print("\n3️⃣ 실제 ParentNodeProcessor로 테스트:")
    print("-" * 50)
    
    processor = ParentNodeProcessor(node_docs_dir)
    
    # process_single_child_node 직접 호출 (async)
    try:
        result = await processor.process_single_child_node(test_file)
        print(f"process_single_child_node 결과: {result}")
    except Exception as e:
        print(f"❌ process_single_child_node 오류: {e}")

async def main():
    await debug_child_processing()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())