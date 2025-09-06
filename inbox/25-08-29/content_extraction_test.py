# 생성 시간: 2025-08-29 09:40:03 KST
# 핵심 내용: unified_node_processor.py V3 방식에서 get_combined_content() 메서드로 전달되는 content 내용 확인
# 상세 내용:
#   - test_content_extraction 함수 (18-35라인): chapter7_02 파일로 content 추출 테스트
#   - main 함수 (37-45라인): 테스트 실행 및 결과 저장
# 상태: active
# 주소: content_extraction_test
# 참조: unified_node_processor.py의 get_combined_content 메서드

import asyncio
import yaml
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# unified_node_processor.py에서 필요한 클래스들 임포트
import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28')
from unified_node_processor import NodeDocumentManager, NodeInfo

async def test_content_extraction():
    """chapter7_02_7.2_JSON_Schema_in_a_nutshell.md 파일로 content 추출 테스트"""
    
    # 기본 설정
    config = {
        'nodes_json_path': '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/nodes_updated.json',
        'node_docs_dir': '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs'
    }
    
    # NodeDocumentManager 초기화
    doc_manager = NodeDocumentManager(config, logger)
    
    # 테스트용 노드 생성 (부모 노드로 변경 - 자식 노드들의 내용도 포함)
    test_node = NodeInfo(
        id=0, 
        title="7_Basic_data_validation",
        level=1,
        parent_id=None,
        children_ids=[1, 2, 3, 4, 5, 6],  # 모든 자식 노드 ID들
        has_content=True,
        document_path="/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs/00_lev1_7_Basic_data_validation_info.md"
    )
    
    # get_combined_content 메서드로 content 추출
    content = await doc_manager.get_combined_content(test_node)
    
    return content

async def main():
    """메인 함수"""
    try:
        content = await test_content_extraction()
        
        # 결과를 파일로 저장
        output_file = Path('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29/unified_processor_extracted_content.txt')
        output_file.write_text(content, encoding='utf-8')
        
        logger.info(f"✅ Content 추출 완료: {len(content)} 글자")
        logger.info(f"💾 결과 저장: {output_file}")
        
        print(f"수정된 unified_node_processor.py로 추출된 content 길이: {len(content)} 글자")
        print(f"결과 파일: {output_file}")
        print(f"\n=== Unified Processor Content 미리보기 (처음 500자) ===")
        print(content[:500] + "..." if len(content) > 500 else content)
        
        # 내가 수동으로 만든 결과와 비교
        manual_result_path = Path('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29/corrected_combined_content.txt')
        if manual_result_path.exists():
            manual_content = manual_result_path.read_text(encoding='utf-8')
            print(f"\n📊 비교 결과:")
            print(f"   수동 생성: {len(manual_content)} 글자")
            print(f"   Unified Processor: {len(content)} 글자")
            print(f"   차이: {abs(len(manual_content) - len(content))} 글자")
            print(f"   일치 여부: {'✅ 일치' if len(manual_content) == len(content) else '❌ 불일치'}")
        
    except Exception as e:
        logger.error(f"❌ 테스트 실패: {e}")

if __name__ == "__main__":
    asyncio.run(main())