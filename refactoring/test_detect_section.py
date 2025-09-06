# 생성 시간: Sat Sep  6 13:58:15 KST 2025
# 핵심 내용: detect_section_content 실제 데이터 테스트 실행기
# 상세 내용:
#   - test_detect_section_content (라인 31-74): 실제 파일을 사용한 detect_section_content 테스트
#   - main (라인 76-80): 테스트 실행 메인 함수
# 상태: active

import asyncio
import json
from pathlib import Path
import sys
import os

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.content_document_service_v4 import ContentDocumentService
from src.utils.logger_v2 import Logger
from src.utils.config_manager import ConfigManager

async def test_detect_section_content():
    """실제 파일로 detect_section_content 테스트"""
    
    # 입력 파일 경로
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/1_Complexity_of_object_oriented_programming_toc.json"
    content_file = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/1_Complexity_of_object_oriented_programming_content.md"
    
    # 출력 디렉토리 (테스트 데이터 디렉토리로 변경)
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    print("🚀 detect_section_content 테스트 시작")
    print(f"📁 TOC 파일: {toc_file}")
    print(f"📄 Content 파일: {content_file}")
    print(f"🎯 출력 디렉토리: {output_dir}")
    
    try:
        # 서비스 초기화
        logger = Logger(project_name="detect_section_test")
        config_manager = ConfigManager("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/config/ai_config.yaml")
        service = ContentDocumentService(config_manager=config_manager, logger=logger)
        
        # TOC 데이터 로드
        with open(toc_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        print(f"✅ TOC 데이터 로드 완료: {len(toc_data)}개 노드")
        
        # Content 데이터 로드
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = f.read()
        print(f"✅ Content 데이터 로드 완료: {len(content_data)}자")
        
        # 출력 디렉토리 생성
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        print(f"📁 출력 디렉토리 생성: {output_dir}")
        
        # detect_section_content 실행
        print("\n🔍 detect_section_content 실행 중...")
        result = await service.detect_section_content(
            chapter_sections=toc_data,
            chapter_content=content_data,
            stage_name="detect_section_content"
        )
        
        print(f"\n✅ detect_section_content 완료!")
        print(f"📊 결과: 총 {len(result)}개 섹션")
        
        # has_content 필드 확인
        has_content_count = sum(1 for node in result if node.get('has_content', False))
        print(f"   - has_content=true 노드: {has_content_count}개")
        print(f"   - has_content=false 노드: {len(result) - has_content_count}개")
        
        # content.json 파일 저장
        content_json_path = Path(output_dir) / "content.json"
        with open(content_json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 content.json 저장 완료:")
        print(f"   - 경로: {content_json_path}")
        print(f"   - 파일 크기: {content_json_path.stat().st_size}바이트")
        
        # 샘플 노드 출력
        if result:
            print(f"\n📋 샘플 노드:")
            sample_node = result[0]
            for key, value in sample_node.items():
                if key == 'children_ids' and isinstance(value, list) and len(value) > 3:
                    print(f"   - {key}: [처음 3개만] {value[:3]}...")
                else:
                    print(f"   - {key}: {value}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_detect_section_content())