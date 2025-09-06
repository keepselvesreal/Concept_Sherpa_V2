# 생성 시간: Thu Sep  4 09:41:15 KST 2025
# 핵심 내용: WorkspacePreparationStage와 ResultLogger 통합 테스트 (실제 PDF 사용)
# 상세 내용:
#   - TestWorkspacePreparationWithResultLogger (라인 17-70): 실제 PDF를 사용한 통합 테스트 클래스
#   - test_dop_book_workspace_preparation_with_result_logging (라인 22-70): DOP 책으로 실제 워크스페이스 준비 및 결과 저장 테스트
# 상태: active
# 참조: WorkspacePreparationStage에 ResultLogger 통합 완료 후 실제 데이터 검증

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime

# 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory
from stages.workspace_preparation import WorkspacePreparationStage

@pytest.mark.integration
@pytest.mark.slow
class TestWorkspacePreparationWithResultLogger:
    """
    WorkspacePreparationStage와 ResultLogger 통합 테스트
    - 실제 PDF를 사용해서 워크스페이스 준비 및 결과 저장 검증
    - 각 장별로 JSON(목차) + 마크다운(내용) 저장 확인
    """
    
    async def test_dop_book_workspace_preparation_with_result_logging(self, temp_directory):
        """
        요구사항: DOP 책 PDF로 실제 워크스페이스 준비 및 ResultLogger 검증
        - 실제 PDF 목차 추출 및 AI 장 분석
        - 각 장별 폴더 생성과 동시에 ResultLogger로 결과 저장
        - output 디렉토리에 JSON + 마크다운 파일 저장 확인
        """
        # Given: 실제 DOP PDF 파일과 WorkspacePreparationStage
        pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
        
        # PDF 파일 존재 확인
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF 파일을 찾을 수 없음: {pdf_path}")
        
        config_manager = ConfigManager()
        
        # 테스트 모드 활성화 (선택된 장만 처리)
        config_manager.data = {
            "test": {
                "enabled": True,
                "selected_chapters": [1, 2]  # 1장, 2장만 처리
            },
            "workspace_preparation": {
                "folder_structure": {
                    "base_path": temp_directory
                }
            }
        }
        
        logger_factory = LoggerFactory(config_manager)
        workspace_stage = WorkspacePreparationStage(config_manager, logger_factory)
        
        # When: 워크스페이스 준비 실행
        input_data = {"pdf_path": pdf_path}
        result = await workspace_stage.process(input_data)
        
        # Then: 워크스페이스 준비 성공 검증
        assert result['success'], f"워크스페이스 준비 실패: {result.get('error', 'Unknown error')}"
        assert 'book_title' in result, "책 제목이 결과에 포함되어야 함"
        assert 'total_chapters' in result, "총 장 수가 결과에 포함되어야 함"
        assert 'created_folders' in result, "생성된 폴더 정보가 포함되어야 함"
        
        print(f"📖 책 제목: {result['book_title']}")
        print(f"📊 총 장 수: {result['total_chapters']}")
        print(f"📁 생성된 폴더 수: {len(result['created_folders'])}")
        
        # ResultLogger 결과 파일 확인
        result_logger = workspace_stage.result_logger
        assert result_logger is not None, "ResultLogger가 초기화되어야 함"
        
        saved_results = result_logger.list_results()
        print(f"💾 저장된 결과 파일 수: {len(saved_results)}")
        
        # JSON과 마크다운 파일이 저장되었는지 확인
        json_files = [r for r in saved_results if r['format'] == 'json']
        md_files = [r for r in saved_results if r['format'] == 'md']
        
        print(f"📄 JSON 파일 수: {len(json_files)}")
        print(f"📝 마크다운 파일 수: {len(md_files)}")
        
        # 최소 1개 이상의 장이 처리되어야 함
        assert len(json_files) >= 1, "최소 1개 장의 JSON 목차 파일이 저장되어야 함"
        
        # 첫 번째 JSON 파일 내용 검증
        if json_files:
            first_json = json_files[0]
            json_path = Path(first_json['path'])
            assert json_path.exists(), f"JSON 파일이 존재해야 함: {json_path}"
            
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            # JSON 구조 검증
            assert 'chapter_info' in toc_data, "장 정보가 포함되어야 함"
            assert 'sections' in toc_data, "섹션 정보가 포함되어야 함"
            assert 'extraction_metadata' in toc_data, "추출 메타데이터가 포함되어야 함"
            
            chapter_info = toc_data['chapter_info']
            assert 'number' in chapter_info, "장 번호가 포함되어야 함"
            assert 'title' in chapter_info, "장 제목이 포함되어야 함"
            assert 'start_page' in chapter_info, "시작 페이지가 포함되어야 함"
            assert 'end_page' in chapter_info, "끝 페이지가 포함되어야 함"
            
            print(f"📋 첫 번째 장: {chapter_info['number']}장 - {chapter_info['title']}")
            print(f"📄 페이지 범위: {chapter_info['start_page']}-{chapter_info['end_page']}")
            print(f"🔗 섹션 수: {len(toc_data['sections'])}")
        
        # 첫 번째 마크다운 파일 내용 검증 (있는 경우)
        if md_files:
            first_md = md_files[0]
            md_path = Path(first_md['path'])
            assert md_path.exists(), f"마크다운 파일이 존재해야 함: {md_path}"
            
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 마크다운 구조 검증
            assert "# " in md_content, "마크다운 헤더가 포함되어야 함"
            assert "**추출 정보:**" in md_content, "추출 정보가 포함되어야 함"
            assert "페이지 범위:" in md_content, "페이지 범위 정보가 포함되어야 함"
            assert "WorkspacePreparationStage pipeline" in md_content, "파이프라인 정보가 포함되어야 함"
            
            print(f"📝 첫 번째 마크다운 파일 크기: {len(md_content)} 문자")
        
        # 실제 저장된 파일들 목록 출력
        print("\n💾 저장된 결과 파일들:")
        for result_file in saved_results[:5]:  # 처음 5개만 출력
            print(f"  - {result_file['name']}.{result_file['format']} ({result_file['size']} bytes)")