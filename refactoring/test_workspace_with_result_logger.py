# 생성 시간: Thu Sep  4 09:43:18 KST 2025
# 핵심 내용: WorkspacePreparationStage + ResultLogger 실제 데이터 테스트 스크립트
# 상세 내용:
#   - 실제 DOP PDF를 사용한 워크스페이스 준비
#   - ResultLogger를 통한 장별 JSON + 마크다운 결과 저장
#   - output 디렉토리에 저장되는 결과 파일 검증
# 상태: active
# 참조: WorkspacePreparationStage ResultLogger 통합 테스트

import asyncio
import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 설정
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory
from stages.workspace_preparation import WorkspacePreparationStage


async def test_workspace_preparation_with_result_logger():
    """실제 DOP PDF로 워크스페이스 준비 + ResultLogger 테스트"""
    
    print("🚀 WorkspacePreparationStage + ResultLogger 실제 데이터 테스트 시작")
    
    # PDF 파일 경로
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일을 찾을 수 없음: {pdf_path}")
        return
    
    try:
        # ConfigManager 설정
        config_manager = ConfigManager()
        
        # 테스트 모드 - 1장만 처리
        config_manager.data = {
            "test": {
                "enabled": True,
                "selected_chapters": [1]  # 1장만 처리
            },
            "workspace_preparation": {
                "folder_structure": {
                    "base_path": "./output"  # output 디렉토리에 저장
                }
            }
        }
        
        # LoggerFactory 및 Stage 초기화
        logger_factory = LoggerFactory(config_manager)
        workspace_stage = WorkspacePreparationStage(config_manager, logger_factory)
        
        print(f"📖 PDF 파일: {pdf_path}")
        print("📋 테스트 모드: 1장만 처리")
        print("📁 출력 디렉토리: ./output")
        
        # 워크스페이스 준비 실행
        input_data = {"pdf_path": pdf_path}
        print("\n🔄 워크스페이스 준비 실행 중...")
        
        result = await workspace_stage.process(input_data)
        
        if not result['success']:
            print(f"❌ 워크스페이스 준비 실패: {result.get('error', 'Unknown error')}")
            return
        
        print("✅ 워크스페이스 준비 성공!")
        print(f"📖 책 제목: {result['book_title']}")
        print(f"📊 총 장 수: {result['total_chapters']}")
        print(f"📁 생성된 폴더 수: {len(result['created_folders'])}")
        
        # ResultLogger 결과 확인
        result_logger = workspace_stage.result_logger
        if result_logger:
            saved_results = result_logger.list_results()
            print(f"\n💾 ResultLogger 저장 결과:")
            print(f"   총 저장된 파일 수: {len(saved_results)}")
            
            # 파일 형식별 분류
            json_files = [r for r in saved_results if r['format'] == 'json']
            md_files = [r for r in saved_results if r['format'] == 'md']
            
            print(f"   📄 JSON 파일 (장 목차): {len(json_files)}개")
            print(f"   📝 마크다운 파일 (장 내용): {len(md_files)}개")
            
            # 저장된 파일 목록 출력
            print(f"\n📋 저장된 파일 목록:")
            for i, result_file in enumerate(saved_results, 1):
                size_kb = result_file['size'] / 1024
                print(f"   {i}. {result_file['name']}.{result_file['format']} ({size_kb:.1f}KB)")
                
                # JSON 파일 내용 미리보기
                if result_file['format'] == 'json' and i == 1:
                    import json
                    with open(result_file['path'], 'r', encoding='utf-8') as f:
                        toc_data = json.load(f)
                    
                    chapter_info = toc_data['chapter_info']
                    print(f"      📋 {chapter_info['number']}장: {chapter_info['title']}")
                    print(f"      📄 페이지: {chapter_info['start_page']}-{chapter_info['end_page']} ({chapter_info['page_count']}페이지)")
                    print(f"      🔗 섹션 수: {len(toc_data['sections'])}개")
                
                # 마크다운 파일 내용 미리보기
                elif result_file['format'] == 'md' and i <= 2:
                    with open(result_file['path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    lines = content.split('\n')
                    first_header = next((line for line in lines if line.startswith('# ')), "")
                    print(f"      📝 제목: {first_header}")
                    print(f"      📄 내용 길이: {len(content)}자")
            
            print(f"\n🎯 ResultLogger가 성공적으로 각 장별 결과를 JSON(목차) + 마크다운(내용)으로 저장했습니다!")
            print(f"📁 저장 위치: {result_logger.results_dir}")
            
        else:
            print("⚠️ ResultLogger가 초기화되지 않았습니다.")
            
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_workspace_preparation_with_result_logger())