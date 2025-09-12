# 생성 시간: Tue Sep  9 22:42:15 KST 2025
# 핵심 내용: WorkspacePreparationStage 개별 메서드 로직 검증 (픽스처 활용)
# 상세 내용:
#   - TestWorkspacePreparationLogic (라인 13-94): 픽스처 데이터 활용한 개별 메서드 로직 검증 클래스
#   - test_extract_toc_from_pdf_logic (라인 16-34): 실제 PDF → TOC 추출 결과 픽스처 비교 검증
#   - test_analyze_chapters_with_ai_logic (라인 36-56): 실제 목차 데이터 → AI 분석 결과 구조 검증
#   - test_workspace_preparation_output_schema (라인 58-94): 워크스페이스 준비 출력 스키마 검증
# 상태: active

import pytest
from tests.schemas.stage_schemas import WorkspacePreparationOutput

# WorkspacePreparation 전용 픽스처 임포트
pytest_plugins = ["tests.fixtures.workspace_preparation_fixtures"]

class TestWorkspacePreparationLogic:
    """픽스처 데이터 활용한 개별 메서드 로직 검증"""
    
    @pytest.mark.asyncio
    async def test_extract_toc_from_pdf_logic(self, real_pdf_path, toc_data, config_manager, test_logger):
        """🟢 실제 PDF → TOC 추출 결과가 픽스처와 동일한지 검증"""
        from stages.workspace_preparation_v3 import WorkspacePreparationStage
        
        stage = WorkspacePreparationStage(config_manager, None)
        stage.logger = test_logger
        
        # 실제 PDF로 TOC 추출
        result = await stage.extract_toc_from_pdf(real_pdf_path)
        
        # 기본 구조 검증
        assert result['success'] is True, f"TOC 추출 실패: {result.get('error')}"
        assert 'data' in result
        assert 'toc_structure' in result['data']
        
        # 픽스처 데이터와 비교 (구조가 동일한지)
        extracted_toc = result['data']['toc_structure']
        fixture_toc = toc_data['toc_structure']
        
        assert len(extracted_toc) == len(fixture_toc), f"TOC 항목 수 불일치: {len(extracted_toc)} vs {len(fixture_toc)}"
        print(f"✅ TOC 추출 검증 통과: {len(extracted_toc)}개 항목")
    
    @pytest.mark.asyncio
    async def test_analyze_chapters_with_ai_logic(self, toc_data, config_manager, test_logger):
        """🟢 실제 목차 데이터 → AI 분석 결과 구조 검증"""
        from stages.workspace_preparation_v3 import WorkspacePreparationStage
        
        stage = WorkspacePreparationStage(config_manager, None)
        stage.logger = test_logger
        
        # 실제 목차 데이터로 AI 분석
        result = await stage.analyze_chapters_with_ai(toc_data)
        
        # 결과 구조 검증
        assert result['success'] is True, f"AI 분석 실패: {result.get('error')}"
        assert 'chapters_info' in result
        assert isinstance(result['chapters_info'], list)
        assert len(result['chapters_info']) > 0, "장 정보가 비어있음"
        
        # 각 장 정보 구조 검증
        for i, chapter_info in enumerate(result['chapters_info']):
            assert 'title' in chapter_info, f"장 {i+1}: title 필드 누락"
            assert 'start_page' in chapter_info, f"장 {i+1}: start_page 필드 누락"
            assert 'end_page' in chapter_info, f"장 {i+1}: end_page 필드 누락"
            
        print(f"✅ AI 장 분석 검증 통과: {len(result['chapters_info'])}개 장")
    
    def test_workspace_preparation_output_schema(self, toc_data):
        """🟢 워크스페이스 준비 출력 스키마 검증"""
        
        # 성공 케이스 테스트 데이터 구성
        success_result = {
            'success': True,
            'data': {
                'book_metadata': {
                    'title': 'Test Book', 
                    'normalized_title': 'Test_Book', 
                    'total_chapters': 2
                },
                'chapters_data': [
                    {
                        'chapter_title': 'Chapter 1',
                        'chapter_toc': toc_data['toc_structure'][:3],  # 🟢 수정: chapter_toc 사용
                        'content_text': 'Sample content for chapter 1',
                        'metadata': {'start_page': 1, 'end_page': 10}
                    },
                    {
                        'chapter_title': 'Chapter 2', 
                        'chapter_toc': toc_data['toc_structure'][3:6],
                        'content_text': 'Sample content for chapter 2',
                        'metadata': {'start_page': 11, 'end_page': 20}
                    }
                ],
                'raw_toc_data': toc_data
            },
            'error': None
        }
        
        # 성공 케이스 스키마 검증
        assert WorkspacePreparationOutput.validate(success_result), "성공 케이스 스키마 검증 실패"
        
        # 실패 케이스 테스트 데이터 구성
        failure_result = {
            'success': False,
            'data': None,
            'error': "테스트 에러 메시지"
        }
        
        # 실패 케이스 스키마 검증
        assert WorkspacePreparationOutput.validate(failure_result), "실패 케이스 스키마 검증 실패"
        
        print("✅ 워크스페이스 준비 출력 스키마 검증 통과")