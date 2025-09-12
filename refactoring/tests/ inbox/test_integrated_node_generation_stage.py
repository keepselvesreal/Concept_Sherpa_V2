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
    

    
    @pytest.mark.asyncio
    async def test_generate_node_documents(self, integrated_stage, selected_chapters_data, normalized_book_title):
        """
        ✅ generate_node_documents 메서드 테스트 (AI API 호출 없음)
        """
        all_results = []
        
        # 선택된 모든 챕터에 대해 노드 문서 생성
        for chapter_data in selected_chapters_data:
            print(f"📝 노드 문서 생성 중: {chapter_data.get('chapter_title', 'Unknown')}")
            
            # 각 챕터의 노드 문서 생성
            chapter_result = await integrated_stage.generate_node_documents(chapter_data, normalized_book_title)
            
            # 기본 검증
            assert isinstance(chapter_result, list), "결과는 리스트여야 함"
            assert len(chapter_result) > 0, "노드 문서가 생성되어야 함"
            
            # 결과를 전체 리스트에 추가
            all_results.extend(chapter_result)
        
        # 전체 결과 구조 검증
        for doc in all_results:
            assert 'file_name' in doc, "file_name 필드가 있어야 함"
            assert 'content' in doc, "content 필드가 있어야 함"
            assert isinstance(doc['file_name'], str), "file_name은 문자열이어야 함"
            assert isinstance(doc['content'], str), "content는 문자열이어야 함"
        
        # 결과 저장 (모든 챕터의 결과를 하나의 파일에)
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager("tests/data/integrated_node_generation_stage")
        data_manager.save_test_result("generate_node_documents", all_results)
        
        print(f"✅ 노드 문서 생성 완료: 총 {len(all_results)}개 ({len(selected_chapters_data)}개 챕터)")
    
    # @pytest.mark.api_test
    @pytest.mark.asyncio
    async def test_generate_content_documents_with_api(self, integrated_stage, selected_chapters_data, normalized_book_title):
        """
        🤖 generate_content_documents 메서드 테스트 (실제 AI API 호출)
        """
        all_results = []
        
        # 선택된 모든 챕터에 대해 콘텐츠 문서 생성
        for chapter_data in selected_chapters_data:
            print(f"🤖 콘텐츠 문서 생성 중 (API): {chapter_data.get('chapter_title', 'Unknown')}")
            
            # 각 챕터의 콘텐츠 문서 생성 (실제 AI API 호출)
            chapter_result = await integrated_stage.generate_content_documents(chapter_data, normalized_book_title)
            
            # 기본 검증
            assert isinstance(chapter_result, list), "결과는 리스트여야 함"
            # AI API 결과는 가변적이므로 구조만 검증
            
            for doc in chapter_result:
                assert 'file_name' in doc, "file_name 필드가 있어야 함"
                assert 'content' in doc, "content 필드가 있어야 함"
            
            # 결과를 전체 리스트에 추가
            all_results.extend(chapter_result)
        
        # 결과 저장 (모든 챕터의 결과를 하나의 파일에)
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager("tests/data/integrated_node_generation_stage")
        data_manager.save_test_result("generate_content_documents", all_results)
            
        print(f"✅ 콘텐츠 문서 생성 완료 (API): 총 {len(all_results)}개 ({len(selected_chapters_data)}개 챕터)")
    
    # @pytest.mark.unit_test  
    @pytest.mark.asyncio
    async def test_generate_content_documents_without_api(self, integrated_stage_with_mock, selected_chapters_data, normalized_book_title):
        """
        🔧 generate_content_documents 메서드 테스트 (AI API Mock 사용)
        """
        all_results = []
        
        # 선택된 모든 챕터에 대해 콘텐츠 문서 생성 (Mock)
        for chapter_data in selected_chapters_data:
            print(f"🔧 콘텐츠 문서 생성 중 (Mock): {chapter_data.get('chapter_title', 'Unknown')}")
            
            # Mock된 AI 서비스로 메서드 실행 (정규화된 책 제목 전달)
            chapter_result = await integrated_stage_with_mock.generate_content_documents(chapter_data, normalized_book_title)
            
            # Mock 테스트: 기본 구조만 검증 (개수는 Mock 설정에 따라 달라짐)
            assert isinstance(chapter_result, list), "결과는 리스트여야 함"
            assert len(chapter_result) > 0, "최소 1개의 결과가 있어야 함"
            
            # 결과 구조 검증
            for doc in chapter_result:
                assert 'file_name' in doc, "file_name 필드가 있어야 함"
                assert 'content' in doc, "content 필드가 있어야 함"
            
            # 결과를 전체 리스트에 추가
            all_results.extend(chapter_result)
        
        print(f"✅ 콘텐츠 문서 생성 완료 (Mock): 총 {len(all_results)}개 ({len(selected_chapters_data)}개 챕터)")
    
    @pytest.mark.asyncio
    async def test_integrate_documents(self, integrated_stage, selected_chapters_data, normalized_book_title):
        """
        🔗 integrate_documents 메서드 테스트 (AI API 호출 없음)
        """
        all_results = []
        
        # 선택된 모든 챕터에 대해 문서 통합
        for chapter_data in selected_chapters_data:
            print(f"🔗 문서 통합 중: {chapter_data.get('chapter_title', 'Unknown')}")
            
            # 노드 문서와 콘텐츠 문서 먼저 생성
            node_documents = await integrated_stage.generate_node_documents(chapter_data, normalized_book_title)
            content_documents = await integrated_stage.generate_content_documents(chapter_data, normalized_book_title)
            
            # 실제 메서드 실행 (정규화된 책 제목 전달)
            chapter_result = await integrated_stage.integrate_documents(
                chapter_data, 
                node_documents, 
                content_documents,
                normalized_book_title
            )
            
            # 기본 검증
            assert isinstance(chapter_result, list), "결과는 리스트여야 함"
            assert len(chapter_result) > 0, "통합 문서가 생성되어야 함"
            
            # 결과 구조 검증
            for doc in chapter_result:
                assert 'file_name' in doc, "file_name 필드가 있어야 함"
                assert 'content' in doc, "content 필드가 있어야 함"
                assert '/unified_info_docs/' in doc['file_name'], "정규화된장이름/unified_info_docs/ 구조여야 함"
            
            # 결과를 전체 리스트에 추가
            all_results.extend(chapter_result)
        
        # 결과 저장 (모든 챕터의 결과를 하나의 파일에)
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager("tests/data/integrated_node_generation_stage")
        data_manager.save_test_result("integrate_documents", all_results)
            
        print(f"✅ 문서 통합 완료: 총 {len(all_results)}개 ({len(selected_chapters_data)}개 챕터)")
    
    # @pytest.mark.integration_api
    @pytest.mark.asyncio
    async def test_process_full_pipeline_with_api(self, integrated_stage, selected_chapters_data, normalized_book_title):
        """
        🚀 process 메서드 전체 파이프라인 테스트 (실제 AI API 호출)
        """
        print(f"🚀 전체 파이프라인 테스트 (API 포함) - {len(selected_chapters_data)}개 챕터")
        
        # 선택된 챕터들을 process 메서드 입력 형식으로 변환
        input_data = {
            "data": {
                "book_metadata": {
                    "normalized_title": normalized_book_title
                },
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
        
        # 데이터 구조 검증
        assert 'data' in result, "data 필드가 있어야 함"
        assert 'processed_chapters' in result['data'], "processed_chapters가 있어야 함"
        assert 'unified_documents' in result['data'], "unified_documents가 있어야 함"
        
        # 결과 저장 (process.json으로 저장)
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager("tests/data/integrated_node_generation_stage")
        data_manager.save_test_result("process", result)
        
        print(f"✅ 전체 파이프라인 완료 (API)")
    
    # @pytest.mark.integration_unit
    @pytest.mark.asyncio
    async def test_process_full_pipeline_without_api(self, integrated_stage_with_mock, selected_chapters_data, normalized_book_title):
        """
        🔧 process 메서드 전체 파이프라인 테스트 (AI API Mock 사용)
        """
        print(f"🔧 전체 파이프라인 테스트 (Mock) - {len(selected_chapters_data)}개 챕터")
        
        # 선택된 챕터들을 process 메서드 입력 형식으로 변환
        input_data = {
            "data": {
                "book_metadata": {
                    "normalized_title": normalized_book_title
                },
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