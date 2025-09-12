# 생성 시간: Tue Sep 10 15:45:23 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 메서드별 정상 동작 테스트
# 상세 내용:
#   - TestIntegratedNodeGenerationStage (라인 15-120): 메인 테스트 클래스
#   - test_generate_node_documents (라인 20-35): 노드 문서 생성 메서드 테스트
#   - test_generate_content_documents_with_api (라인 37-52): AI API 포함 콘텐츠 문서 생성 테스트
#   - test_generate_content_documents_without_api (라인 54-69): AI API 제외 콘텐츠 문서 생성 테스트
#   - test_integrate_documents (라인 71-86): 문서 통합 메서드 테스트
#   - test_process_full_pipeline_with_api (라인 88-103): 전체 파이프라인 API 포함 테스트
#   - test_process_full_pipeline_without_api (라인 105-120): 전체 파이프라인 API 제외 테스트
# 상태: active
# 참조: integrated_node_generation_stage_v4.py (테스트 대상)

import pytest
import asyncio
import json
from pathlib import Path

# 픽스처 임포트
pytest_plugins = ["tests.fixtures.integrated_node_generation_fixtures"]

class TestIntegratedNodeGenerationStage:
    """IntegratedNodeGenerationStage 각 메서드별 정상 동작 테스트"""
    
    def pytest_generate_tests(self, metafunc):
        """동적 매개변수화: integrate_documents_result.json의 selected_chapters 개수만큼 테스트 생성"""
        if "chapter_index" in metafunc.fixturenames:
            # integrate_documents_result.json에서 selected_chapters 정보 확인
            data_file = Path("tests/data/integrated_node_generation/integrate_documents_result.json")
            if data_file.exists():
                try:
                    with open(data_file, 'r', encoding='utf-8') as f:
                        test_data = json.load(f)
                    # 새로운 구조: {"selected_chapters": [...], "documents": [...]}
                    if 'selected_chapters' in test_data:
                        selected_chapters = test_data['selected_chapters']
                        chapter_indices = list(range(len(selected_chapters)))
                        print(f"🔍 동적 매개변수화: {len(selected_chapters)}개 챕터 감지됨")
                    else:
                        chapter_indices = [0]  # 기본값
                except Exception as e:
                    print(f"⚠️ integrate_documents_result.json 로드 실패: {e}")
                    chapter_indices = [0]  # 기본값
            else:
                print("⚠️ integrate_documents_result.json이 없습니다. 기본값 사용")
                chapter_indices = [0]  # 기본값
            
            metafunc.parametrize("chapter_index", chapter_indices)
    
    @pytest.mark.asyncio
    async def test_generate_node_documents(self, integrated_stage, selected_chapters_data, expected_node_documents, chapter_index):
        """
        ✅ generate_node_documents 메서드 테스트 (AI API 호출 없음)
        """
        # 챕터 인덱스 범위 체크
        if chapter_index >= len(selected_chapters_data):
            pytest.skip(f"챕터 인덱스 {chapter_index}는 존재하지 않음 (총 {len(selected_chapters_data)}개)")
            
        chapter_data = selected_chapters_data[chapter_index]  # 동적으로 선택
        print(f"📝 테스트 챕터 [{chapter_index}]: {chapter_data.get('chapter_title', 'Unknown')}")
        
        # 실제 메서드 실행
        result = await integrated_stage.generate_node_documents(chapter_data)
        
        # 기본 검증
        assert isinstance(result, list), "결과는 리스트여야 함"
        assert len(result) > 0, "노드 문서가 생성되어야 함"
        
        # 결과 구조 검증
        for doc in result:
            assert 'file_name' in doc, "file_name 필드가 있어야 함"
            assert 'content' in doc, "content 필드가 있어야 함"
            assert isinstance(doc['file_name'], str), "file_name은 문자열이어야 함"
            assert isinstance(doc['content'], str), "content는 문자열이어야 함"
        
        print(f"✅ 노드 문서 생성 완료: {len(result)}개")
    
    # @pytest.mark.api_test
    @pytest.mark.asyncio
    async def test_generate_content_documents_with_api(self, integrated_stage, selected_chapters_data, expected_content_documents, chapter_index):
        """
        🤖 generate_content_documents 메서드 테스트 (실제 AI API 호출)
        """
        # 챕터 인덱스 범위 체크
        if chapter_index >= len(selected_chapters_data):
            pytest.skip(f"챕터 인덱스 {chapter_index}는 존재하지 않음 (총 {len(selected_chapters_data)}개)")
            
        chapter_data = selected_chapters_data[chapter_index]  # 동적으로 선택
        print(f"🤖 AI API 테스트 - 챕터 [{chapter_index}]: {chapter_data.get('chapter_title', 'Unknown')}")
        
        # 실제 AI API 호출하여 메서드 실행
        result = await integrated_stage.generate_content_documents(chapter_data)
        
        # 기본 검증 
        assert isinstance(result, list), "결과는 리스트여야 함"
        # AI API 결과는 가변적이므로 구조만 검증
        
        for doc in result:
            assert 'file_name' in doc, "file_name 필드가 있어야 함"
            assert 'content' in doc, "content 필드가 있어야 함"
            
        print(f"✅ 콘텐츠 문서 생성 완료 (API): {len(result)}개")
    
    # @pytest.mark.unit_test  
    @pytest.mark.asyncio
    async def test_generate_content_documents_without_api(self, integrated_stage_with_mock, selected_chapters_data, expected_content_documents, chapter_index):
        """
        🔧 generate_content_documents 메서드 테스트 (AI API Mock 사용)
        """
        # 챕터 인덱스 범위 체크
        if chapter_index >= len(selected_chapters_data):
            pytest.skip(f"챕터 인덱스 {chapter_index}는 존재하지 않음 (총 {len(selected_chapters_data)}개)")
            
        chapter_data = selected_chapters_data[chapter_index]  # 동적으로 선택
        print(f"🔧 Mock 테스트 - 챕터 [{chapter_index}]: {chapter_data.get('chapter_title', 'Unknown')}")
        
        # Mock된 AI 서비스로 메서드 실행
        result = await integrated_stage_with_mock.generate_content_documents(chapter_data)
        
        # Mock 테스트: 기본 구조만 검증 (개수는 Mock 설정에 따라 달라짐)
        assert isinstance(result, list), "결과는 리스트여야 함"
        assert len(result) > 0, "최소 1개의 결과가 있어야 함"
        
        # 결과 구조 검증
        for doc in result:
            assert 'file_name' in doc, "file_name 필드가 있어야 함"
            assert 'content' in doc, "content 필드가 있어야 함"
        
        print(f"✅ 콘텐츠 문서 생성 완료 (Mock): {len(result)}개")
    
    @pytest.mark.asyncio
    async def test_integrate_documents(self, integrated_stage, selected_chapters_data, 
                                     expected_node_documents, expected_content_documents, 
                                     expected_integrate_documents, chapter_index):
        """
        🔗 integrate_documents 메서드 테스트 (AI API 호출 없음)
        """
        # 챕터 인덱스 범위 체크
        if chapter_index >= len(selected_chapters_data):
            pytest.skip(f"챕터 인덱스 {chapter_index}는 존재하지 않음 (총 {len(selected_chapters_data)}개)")
            
        chapter_data = selected_chapters_data[chapter_index]  # 동적으로 선택
        print(f"🔗 문서 통합 테스트 - 챕터 [{chapter_index}]: {chapter_data.get('chapter_title', 'Unknown')}")
        
        # 실제 메서드 실행
        result = await integrated_stage.integrate_documents(
            chapter_data, 
            expected_node_documents, 
            expected_content_documents
        )
        
        # 기본 검증
        assert isinstance(result, list), "결과는 리스트여야 함"
        assert len(result) > 0, "통합 문서가 생성되어야 함"
        
        # 결과 구조 검증
        for doc in result:
            assert 'file_name' in doc, "file_name 필드가 있어야 함"
            assert 'content' in doc, "content 필드가 있어야 함"
            assert '/unified_info_docs/' in doc['file_name'], "정규화된장이름/unified_info_docs/ 구조여야 함"
            
        print(f"✅ 문서 통합 완료: {len(result)}개")
    
    # @pytest.mark.integration_api
    @pytest.mark.asyncio
    async def test_process_full_pipeline_with_api(self, integrated_stage, selected_chapters_data):
        """
        🚀 process 메서드 전체 파이프라인 테스트 (실제 AI API 호출)
        """
        print(f"🚀 전체 파이프라인 테스트 (API 포함)")
        
        # selected_chapters_data를 process 메서드 입력 형식으로 변환
        input_data = {
            "data": {
                "chapters_analysis": {
                    "chapters_info": selected_chapters_data
                }
            }
        }
        
        # 전체 프로세스 실행
        result = await integrated_stage.process(input_data)
        
        # 성공 검증
        assert result['success'] is True, f"처리 실패: {result.get('error')}"
        assert result['error'] is None, "에러가 없어야 함"
        
        # 3단계 결과 검증
        assert 'stage_1_results' in result, "1단계 결과가 있어야 함"
        assert 'stage_2_results' in result, "2단계 결과가 있어야 함"  
        assert 'stage_3_results' in result, "3단계 결과가 있어야 함"
        
        print(f"✅ 전체 파이프라인 완료 (API)")
    
    # @pytest.mark.integration_unit
    @pytest.mark.asyncio
    async def test_process_full_pipeline_without_api(self, integrated_stage_with_mock, selected_chapters_data):
        """
        🔧 process 메서드 전체 파이프라인 테스트 (AI API Mock 사용)
        """
        print(f"🔧 전체 파이프라인 테스트 (Mock)")
        
        # selected_chapters_data를 process 메서드 입력 형식으로 변환
        input_data = {
            "data": {
                "chapters_analysis": {
                    "chapters_info": selected_chapters_data
                }
            }
        }
        
        # Mock된 AI 서비스로 전체 프로세스 실행
        result = await integrated_stage_with_mock.process(input_data)
        
        # 성공 검증 
        assert result['success'] is True, f"처리 실패: {result.get('error')}"
        assert result['error'] is None, "에러가 없어야 함"
        
        # 3단계 결과 검증
        assert 'stage_1_results' in result, "1단계 결과가 있어야 함"
        assert 'stage_2_results' in result, "2단계 결과가 있어야 함"
        assert 'stage_3_results' in result, "3단계 결과가 있어야 함"
        
        print(f"✅ 전체 파이프라인 완료 (Mock)")