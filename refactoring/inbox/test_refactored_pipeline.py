# 생성 시간: Mon Sep  3 17:23:45 KST 2025
# 핵심 내용: 리팩터링된 파이프라인 테스트 스크립트 (selected_chapters 테스트 모드)
# 상세 내용:
#   - test_basic_pipeline (라인 19-38): 기본 파이프라인 테스트 
#   - test_selected_chapters (라인 40-60): 선택된 장만 테스트
#   - main (라인 62-85): 메인 실행 함수
# 상태: active

import asyncio
import sys
from pathlib import Path

# 현재 디렉토리를 sys.path에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 리팩터링된 파이프라인 임포트
from src.core.pipeline_orchestrator import BookPipelineOrchestrator

# 테스트용 PDF 경로 (실제 파일로 변경 필요)
TEST_PDF_PATH = "/home/nadle/projects/Knowledge_Sherpa/v2/sources/dop.pdf"

async def test_basic_pipeline():
    """기본 파이프라인 테스트 (테스트 모드 비활성화)"""
    print("=== 기본 파이프라인 테스트 시작 ===")
    
    # 설정 디렉토리 지정
    config_dir = current_dir / "config"
    
    try:
        # 파이프라인 인스턴스 생성 (테스트 모드 비활성화)
        pipeline = BookPipelineOrchestrator(
            config_dir=str(config_dir),
            test_mode=False,
            selected_chapters=None
        )
        
        # 실행
        result = await pipeline.execute(TEST_PDF_PATH)
        
        print(f"결과: {'성공' if result.is_success else '실패'}")
        if not result.is_success:
            print(f"오류: {result.error}")
        else:
            print(f"완료된 단계: {result.completed_stages}/{result.total_stages}")
            
        return result
        
    except Exception as e:
        print(f"❌ 기본 파이프라인 테스트 실패: {e}")
        return None

async def test_selected_chapters():
    """선택된 장만 테스트"""
    print("=== 선택된 장 테스트 시작 ===")
    
    config_dir = current_dir / "config"
    
    try:
        # 파이프라인 인스턴스 생성 (1, 3장만 테스트)
        pipeline = BookPipelineOrchestrator(
            config_dir=str(config_dir),
            test_mode=True,
            selected_chapters=[1, 3]  # 1장과 3장만 처리
        )
        
        # 실행
        result = await pipeline.execute(TEST_PDF_PATH)
        
        print(f"결과: {'성공' if result.is_success else '실패'}")
        if not result.is_success:
            print(f"오류: {result.error}")
        else:
            print(f"완료된 단계: {result.completed_stages}/{result.total_stages}")
            
        return result
        
    except Exception as e:
        print(f"❌ 선택된 장 테스트 실패: {e}")
        return None

async def main():
    """메인 실행 함수"""
    print("🚀 리팩터링된 파이프라인 테스트 시작")
    
    # PDF 파일 존재 확인
    if not Path(TEST_PDF_PATH).exists():
        print(f"❌ 테스트 PDF 파일을 찾을 수 없습니다: {TEST_PDF_PATH}")
        print("TEST_PDF_PATH 변수를 실제 PDF 파일 경로로 변경해주세요.")
        return
    
    print(f"📖 테스트 대상: {TEST_PDF_PATH}")
    
    # 테스트 실행
    try:
        # 1. 선택된 장만 테스트 (더 안전)
        print("\n" + "="*50)
        selected_result = await test_selected_chapters()
        
        if selected_result and selected_result.is_success:
            print("✅ 선택된 장 테스트 성공!")
        else:
            print("❌ 선택된 장 테스트 실패")
            
        # 2. 필요시 기본 파이프라인 테스트 (주석 해제)
        # print("\n" + "="*50)
        # basic_result = await test_basic_pipeline()
        
        print("\n🎉 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())