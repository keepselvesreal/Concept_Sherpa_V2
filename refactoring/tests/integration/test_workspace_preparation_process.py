# 생성 시간: Wed Jan 15 22:10:23 KST 2025
# 핵심 내용: workspace_preparation process 메서드 정상 동작 테스트
# 상세 내용:
#   - test_workspace_preparation_process (라인 18-55): workspace_preparation.process 정상 동작 테스트
#   - 테스트 대상 PDF: 2022_Data-Oriented Programming_Manning.pdf
#   - 테스트 결과 저장: workspace_preparation/process_result.json
# 상태: active

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from stages.workspace_preparation_v3 import WorkspacePreparationStage
from utils.config_manager import ConfigManager

# tests/utils에서 test_data_manager 임포트
test_utils_path = Path(__file__).parent.parent / "utils"
sys.path.append(str(test_utils_path))
from test_data_manager import TestResultDataManager

async def test_workspace_preparation_process():
    """workspace_preparation.process 메서드 정상 동작 테스트"""
    
    print("🧪 workspace_preparation process 테스트 시작")
    
    # 설정 관리자 초기화
    config_dir = Path(__file__).parent.parent.parent / "config"
    config_manager = ConfigManager(str(config_dir))
    
    # workspace_preparation 스테이지 초기화
    workspace_stage = WorkspacePreparationStage(config_manager, None)
    
    # 테스트 입력 데이터
    test_pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    
    # PDF 파일 존재 확인
    if not Path(test_pdf_path).exists():
        raise FileNotFoundError(f"테스트 PDF 파일이 없습니다: {test_pdf_path}")
    
    stage_input = {
        'data': {
            'pdf_path': test_pdf_path
        },
        'error': None
    }
    
    try:
        print(f"📖 PDF 처리 시작: {Path(test_pdf_path).name}")
        
        # process 메서드 실행
        result = await workspace_stage.process(stage_input)
        
        print(f"✅ process 메서드 실행 완료")
        print(f"📊 결과 구조: {list(result.keys()) if isinstance(result, dict) else type(result)}")
        
        # 결과 검증
        if isinstance(result, dict) and 'data' in result:
            data = result['data']
            if data and isinstance(data, dict):
                print(f"📚 책 정보: {data.get('book_information', {}).get('title', 'Unknown')}")
                print(f"📄 처리된 장 수: {len(data.get('chapters_data', []))}")
        
        # 테스트 결과 저장
        test_data_manager = TestResultDataManager()
        test_data_manager.save_test_result("process", result, "workspace_preparation")
        
        print("🎉 workspace_preparation process 테스트 성공!")
        return True
        
    except Exception as e:
        print(f"❌ workspace_preparation process 테스트 실패: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_workspace_preparation_process())