# 생성 시간: 2025-09-01 21:30:00 KST  
# 핵심 내용: book_pipeline_v3.py의 3단계, 4단계만 독립 테스트하는 스크립트
# 상세 내용:
#   - test_stage_3_node_processing (라인 20-60): 3단계 노드 정보 문서 처리 테스트
#   - test_stage_4_enhanced_toc (라인 62-90): 4단계 enhanced_chapter_toc.md 생성 테스트  
#   - main (라인 92-130): 메인 실행 함수
# 상태: active
# 주소: test_stages_3_4
# 참조: book_pipeline_v3.py의 process_node_documents, generate_enhanced_toc 메서드

import asyncio
import os
import sys
import logging
from pathlib import Path

# 필요한 모듈 경로 추가
sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')
sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31')
sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/process')  # unified_node_processor_v4
sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/components')  # chapter_toc_generator

# book_pipeline_v3에서 BookPipeline 클래스 임포트
from book_pipeline_v3 import BookPipeline
from extract_chapters_v5 import normalize_title

async def test_stage_3_node_processing():
    """3단계: 노드 정보 문서 처리 테스트"""
    print("🧪 === 3단계 테스트: 노드 정보 문서 처리 ===")
    
    # BookPipeline 인스턴스 생성 (테스트 모드)
    pipeline = BookPipeline(test_mode=True, max_chapters=1)
    
    # 테스트용 데이터 준비
    chapter_folder = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    # 필요한 속성 설정
    pipeline.output_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system")  
    pipeline.normalized_book_title = "Data_Oriented_Programming"
    pipeline.logs_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs/Data_Oriented_Programming")
    pipeline.logs_dir.mkdir(parents=True, exist_ok=True)
    
    # 로그 시스템 설정
    pipeline.setup_logging_system("Data_Oriented_Programming")
    
    # 가짜 integration_data 생성 (2단계 완료 결과 시뮬레이션)
    integration_data = {
        'success': True,
        'integration_results': [
            {
                'chapter_number': 1,
                'chapter_title': '1_Complexity_of_object_oriented_programming',
                'success': True,
                'steps_completed': ['노드 정보 문서 생성', '콘텐츠 노드/내용 문서 생성', '문서 통합']
            }
        ]
    }
    
    try:
        # 3단계 실행
        print("🚀 3단계 process_node_documents 실행 중...")
        result = await pipeline.process_node_documents(integration_data)
        
        if result.get('success'):
            print(f"✅ 3단계 성공!")
            print(f"📊 처리된 장: {result.get('processed_chapters')}")
            print(f"📋 처리 결과: {result.get('node_processing_results')}")
            return result
        else:
            print(f"❌ 3단계 실패: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ 3단계 테스트 중 오류: {e}")
        return None

async def test_stage_4_enhanced_toc(node_processing_data):
    """4단계: enhanced_chapter_toc.md 생성 테스트"""
    print("\n🧪 === 4단계 테스트: enhanced_chapter_toc.md 생성 ===")
    
    if not node_processing_data:
        print("❌ 3단계 결과가 없어서 4단계 테스트 불가")
        return None
    
    # BookPipeline 인스턴스 생성 (테스트 모드)
    pipeline = BookPipeline(test_mode=True, max_chapters=1)
    
    # 필요한 속성 설정 (3단계와 동일)
    pipeline.output_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system")  
    pipeline.normalized_book_title = "Data_Oriented_Programming"
    pipeline.logs_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs/Data_Oriented_Programming")
    
    # 로그 시스템 설정
    pipeline.setup_logging_system("Data_Oriented_Programming")
    
    try:
        # 4단계 실행
        print("🚀 4단계 generate_enhanced_toc 실행 중...")
        result = await pipeline.generate_enhanced_toc(node_processing_data)
        
        if result.get('success'):
            print(f"✅ 4단계 성공!")
            print(f"📄 생성된 파일: {result.get('generated_count')}")
            print(f"📋 생성 결과:")
            for file_info in result.get('generated_files', []):
                print(f"  - {file_info['file_path']} ({file_info['file_size']} bytes)")
            return result
        else:
            print(f"❌ 4단계 실패: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ 4단계 테스트 중 오류: {e}")
        return None

async def main():
    """메인 테스트 실행 함수"""
    print("🧪🚀 3단계, 4단계 독립 테스트 시작!")
    print("🎯 대상: Data_Oriented_Programming/1_Complexity_of_object_oriented_programming")
    print("🤖 AI 모델: gemini-2.5-flash (extraction_config.yaml 설정)")
    print()
    
    # 3단계 테스트
    node_result = await test_stage_3_node_processing()
    
    if node_result:
        # 4단계 테스트 
        toc_result = await test_stage_4_enhanced_toc(node_result)
        
        if toc_result:
            print("\n🎉🎉 3단계, 4단계 테스트 모두 성공! 🎉🎉")
            print("✅ 노드 정보 문서 추출/업데이트 완료")
            print("✅ enhanced_chapter_toc.md 생성 완료")
        else:
            print("\n⚠️ 3단계 성공, 4단계 실패")
    else:
        print("\n❌ 3단계 실패로 테스트 중단")

if __name__ == "__main__":
    asyncio.run(main())