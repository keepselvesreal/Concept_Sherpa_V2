# 생성 시간: Wed Jan 15 22:15:23 KST 2025
# 핵심 내용: pipeline_orchestrator execute 메서드 정상 동작 테스트
# 상세 내용:
#   - test_pipeline_orchestrator_execute (라인 25-60): pipeline_orchestrator.execute 정상 동작 테스트
#   - 테스트 대상 PDF: 2022_Data-Oriented Programming_Manning.pdf
#   - 테스트 결과 저장: pipeline_orchestrator/execute_result.json
# 상태: active

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from core.pipeline_orchestrator_v2 import BookPipelineOrchestrator

# tests/utils에서 test_data_manager 임포트
test_utils_path = Path(__file__).parent.parent / "utils"
sys.path.append(str(test_utils_path))
from test_data_manager import TestResultDataManager

async def test_pipeline_orchestrator_execute():
    """pipeline_orchestrator.execute 메서드 정상 동작 테스트"""
    
    print("🧪 pipeline_orchestrator execute 테스트 시작")
    
    # 파이프라인 오케스트레이터 초기화
    config_dir = Path(__file__).parent.parent.parent / "config"
    orchestrator = BookPipelineOrchestrator(str(config_dir))
    
    # 테스트 PDF 경로
    test_pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    
    # PDF 파일 존재 확인
    if not Path(test_pdf_path).exists():
        raise FileNotFoundError(f"테스트 PDF 파일이 없습니다: {test_pdf_path}")
    
    try:
        print(f"📖 파이프라인 실행 시작: {Path(test_pdf_path).name}")
        
        # execute 메서드 실행
        result = await orchestrator.execute(test_pdf_path)
        
        print(f"✅ execute 메서드 실행 완료")
        print(f"📊 결과 성공 여부: {result.is_success}")
        print(f"📊 완료된 단계: {result.completed_stages}/{result.total_stages}")
        print(f"📊 진행률: {result.progress_percent}%")
        
        # 결과 검증
        if result.stage_results:
            print(f"📊 단계별 결과: {[sr.stage_name for sr in result.stage_results]}")
            
        # 테스트 결과 저장
        test_data_manager = TestResultDataManager()
        test_data_manager.save_test_result("execute", result.to_dict(), "pipeline_orchestrator")
        
        print("🎉 pipeline_orchestrator execute 테스트 성공!")
        return True
        
    except Exception as e:
        print(f"❌ pipeline_orchestrator execute 테스트 실패: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_pipeline_orchestrator_execute())