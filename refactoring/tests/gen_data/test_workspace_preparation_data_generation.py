# 생성 시간: Tue Sep  9 22:41:45 KST 2025
# 핵심 내용: WorkspacePreparationStage 실제 데이터 생성 및 픽스처 저장 테스트
# 상세 내용:
#   - TestWorkspacePreparationDataGeneration (라인 15-81): 실제 PDF로 데이터 생성 → 픽스처 저장 클래스
#   - test_generate_workspace_data (라인 18-56): 실제 PDF를 사용한 워크스페이스 데이터 생성 및 저장
#   - _save_test_data (라인 58-81): 테스트 데이터 저장 메서드 (JSON/MD 형식)
# 상태: active

import pytest
import json
import asyncio
from pathlib import Path

# WorkspacePreparation 전용 픽스처 임포트
pytest_plugins = ["tests.fixtures.workspace_preparation_fixtures"]

class TestWorkspacePreparationDataGeneration:
    """실제 PDF로 데이터 생성 → 픽스처 저장"""
    
    @pytest.mark.asyncio
    async def test_generate_workspace_data(self, real_pdf_path, config_manager, test_logger):
        """
        🟢 실제 PDF를 사용한 워크스페이스 데이터 생성 및 저장
        """
        print(f"📖 실제 PDF 경로: {real_pdf_path}")
        
        # WorkspacePreparationStage_v3 실행
        from stages.workspace_preparation_v3 import WorkspacePreparationStage
        stage = WorkspacePreparationStage(config_manager, None)  # logger_factory 대신 None
        stage.logger = test_logger
        
        # 🟢 실제 PDF 처리
        result = await stage.process({"pdf_path": real_pdf_path})
        
        # 기본 검증
        assert result['success'] is True, f"처리 실패: {result.get('error')}"
        assert 'data' in result
        assert result['data'] is not None
        
        data = result['data']
        assert 'book_metadata' in data
        assert 'chapters_data' in data
        assert 'raw_toc_data' in data
        
        # 🟢 픽스처 저장 (전체 결과만 저장)
        print(f"📝 책 제목: {data['book_metadata']['title']}")
        print(f"📊 장 개수: {len(data['chapters_data'])}개")
        
        # 테스트 데이터 디렉토리 생성
        data_dir = Path("tests/data/workspace_preparation")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 🟢 전체 결과만 저장 (개별 데이터는 이 파일에서 조회 가능)
        self._save_test_data("workspace_result", result, "json")
        
        print(f"✅ 테스트 데이터 생성 완료: {len(data['chapters_data'])}개 장")
        
        # 스키마 검증도 함께 수행
        from tests.schemas.stage_schemas import WorkspacePreparationOutput
        assert WorkspacePreparationOutput.validate(result), "스키마 검증 실패"
        print("✅ 스키마 검증 통과")
    
    def _save_test_data(self, name: str, data, format: str = "json"):
        """
        테스트 데이터 저장 - 지정된 형식으로 저장
        
        Args:
            name: 파일명 (확장자 제외)
            data: 저장할 데이터
            format: 저장 형식 ('json' 또는 'md')
        """
        data_dir = Path("tests/data/workspace_preparation")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        if format == "md":
            # Markdown 형식으로 저장
            file_path = data_dir / f"{name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(data))
        elif format == "json":
            # JSON 형식으로 저장
            file_path = data_dir / f"{name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"지원하지 않는 형식입니다: {format}. 'md' 또는 'json'을 사용하세요.")
        
        print(f"💾 저장: {file_path} (형식: {format})")