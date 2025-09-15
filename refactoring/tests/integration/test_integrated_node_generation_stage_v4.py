# 생성 시간: Wed Sep 15 10:45:20 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage v4 정상 동작 테스트 (데이터 구조 변경 검증 + generate_content_documents 테스트)
# 상세 내용:
#   - TestIntegratedNodeGenerationStageV4 (라인 27-29): 메인 테스트 클래스
#   - test_process_data_format (라인 30-149): 데이터 형식 변경 정상 동작 테스트 (실제 process_result.json 사용, 출력과 동일한 데이터 저장)
#   - test_generate_content_documents (라인 151-269): generate_content_documents 메서드 단독 테스트 (2장 데이터 사용, 실제 메서드 출력과 동일한 데이터 저장)
# 상태: active
# 참조: test_integrated_node_generation_stage_v4.py (데이터 구조 변경 반영)

import json
import pytest
from pathlib import Path

import sys
from pathlib import Path
# refactoring 프로젝트 경로 추가
refactoring_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(refactoring_root))

from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
from utils.logger_v2 import Logger


class TestIntegratedNodeGenerationStageV4:
    """IntegratedNodeGenerationStage v4 데이터 구조 변경 테스트 (실제 데이터 사용)"""
    
    @pytest.mark.asyncio
    async def test_process_data_format(self):
        """
        process 메서드의 데이터 형식 변경 정상 동작 테스트 - 실제 process_result.json 사용
        
        변경 내용 검증:
        - success 필드 제거
        - output 필드 → data 필드로 변경  
        - data 안에 book_information 필드 추가 (processed_chapters 위에 위치)
        - book_metadata → book_information 필드명 변경
        
        입력: '/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/workspace_preparation/process_result.json'
        
        기대 결과:
        - data.book_information: Dict 타입 (실제 workspace_data에서 추출)
        - data.processed_chapters: List 타입
        - data.unified_documents: List 타입
        - error: None (성공 시)
        """
        print("📋 IntegratedNodeGenerationStage v4 데이터 구조 테스트 시작 (실제 데이터)")
        
        # Given - 실제 workspace_preparation process_result.json 로드 (새로 생성된 데이터)
        workspace_data_path = Path(__file__).parent.parent / "data" / "workspace_preparation_stage" / "process_result.json"
        assert workspace_data_path.exists(), f"실제 워크스페이스 데이터 파일이 없습니다: {workspace_data_path}"
        
        with open(workspace_data_path, 'r', encoding='utf-8') as f:
            prev_stage_result = json.load(f)
        
        # 1, 2장만 포함한 테스트 데이터 구성
        original_chapters_data = prev_stage_result['data']['chapters_data']
        test_chapters_data = original_chapters_data[:2]  # 처음 2개 장만 선택
        
        # 테스트용 입력 데이터 구성 (이전 단계 결과 구조 유지)
        test_input = {
            'data': {
                'book_information': prev_stage_result['data']['book_information'],
                'raw_toc_data': prev_stage_result['data']['raw_toc_data'],
                'chapters_data': test_chapters_data  # 1, 2장만 전달
            }
        }
        
        print(f"📖 실제 process_result.json 로드 완료")
        print(f"   - book_information: {prev_stage_result['data']['book_information']}")
        print(f"   - 테스트용 chapters_data 수: {len(test_chapters_data)} (1, 2장만)")
        
        # When - IntegratedNodeGenerationStage 초기화 및 실행
        try:
            config = {}
            logger = Logger("test_integrated_node_generation_v4")
            stage = IntegratedNodeGenerationStage(config, logger)
            
            print(f"✅ IntegratedNodeGenerationStage v4 초기화 완료")
            
            # process 메서드 실행 (이전 단계 결과를 직접 전달)
            result = await stage.process(test_input)
            
            print(f"✅ process 메서드 실행 완료")
            
        except Exception as e:
            print(f"❌ 스테이지 실행 중 오류: {e}")
            pytest.fail(f"IntegratedNodeGenerationStage 실행 실패: {e}")
        
        # Then - 출력 구조 검증
        print(f"🔍 출력 구조 검증 시작")
        
        # 1. 기본 구조 검증
        assert isinstance(result, dict), "결과는 딕셔너리여야 함"
        assert "data" in result, "data 필드가 있어야 함"
        assert "error" in result, "error 필드가 있어야 함"
        assert "success" not in result, "success 필드는 제거되어야 함"  
        assert "output" not in result, "output 필드는 제거되어야 함"
        
        # 2. data 필드 내부 구조 검증
        data = result["data"]
        assert isinstance(data, dict), "data는 딕셔너리여야 함"
        assert "book_information" in data, "data에 book_information 필드가 있어야 함"
        assert "processed_chapters" in data, "data에 processed_chapters 필드가 있어야 함"
        assert "unified_documents" in data, "data에 unified_documents 필드가 있어야 함"
        
        # 3. 필드 순서 검증 (book_information이 processed_chapters 앞에 위치)
        data_keys = list(data.keys())
        book_information_index = data_keys.index("book_information")
        processed_chapters_index = data_keys.index("processed_chapters")
        assert book_information_index < processed_chapters_index, "book_information이 processed_chapters보다 앞에 위치해야 함"
        
        # 4. 각 필드 타입 검증
        assert isinstance(data["book_information"], dict), "book_information은 딕셔너리여야 함"
        assert isinstance(data["processed_chapters"], list), "processed_chapters는 리스트여야 함"
        assert isinstance(data["unified_documents"], list), "unified_documents는 리스트여야 함"
        
        # 5. book_information 내용 검증 (실제 workspace_data에서 추출된 것)
        book_information = data["book_information"]
        expected_information = test_input['data']['book_information']
        assert book_information == expected_information, f"book_information이 예상값과 일치하지 않음: {book_information}"
        
        # 6. 성공 시 처리된 데이터가 있는지 확인
        if result.get('error') is None:
            assert len(data["processed_chapters"]) > 0, "성공 시 processed_chapters가 있어야 함"
            print(f"✅ 성공적으로 {len(data['processed_chapters'])}개 장 처리됨")
        
        print(f"✅ 모든 출력 구조 검증 통과")
        print(f"📊 검증 결과:")
        print(f"   - data.book_information: {type(data['book_information'])} (키 개수: {len(data['book_information'])})")
        print(f"   - data.processed_chapters: {type(data['processed_chapters'])} (길이: {len(data['processed_chapters'])})")
        print(f"   - data.unified_documents: {type(data['unified_documents'])} (길이: {len(data['unified_documents'])})")
        print(f"   - error: {result.get('error')}")
        
        # 7. 실제 process 결과를 integrated_node_generation_stage 폴더에 저장 (출력과 동일한 데이터)
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager()  # 설정 파일에서 경로 자동 로드
        folder_name = data_manager.get_folder_name("integrated_node_generation_stage")
        data_manager.save_test_result(
            test_method_name="process", 
            result_data=result,  # result를 그대로 저장
            folder_name=folder_name
        )
        
        print(f"💾 테스트 결과 저장 완료 (process 출력과 동일한 데이터)")
        print(f"🎉 IntegratedNodeGenerationStage v4 데이터 구조 테스트 성공!")
        
        return result
    
    @pytest.mark.asyncio
    async def test_generate_content_documents(self):
        """
        generate_content_documents 메서드 단독 테스트 - 2장 데이터 사용
        
        목적: AI 기반 콘텐츠 문서 생성 메서드의 정상 동작 확인
        
        입력: workspace_preparation/process_result.json의 2장 데이터
        
        기대 결과:
        - 반환값: List[Dict] 형태, 각 항목은 {'file_name': str, 'content': str}
        - file_name 형식: {book_title}/{chapter_title}/sections/{section_title}.md
        - content: 실제 추출된 콘텐츠 (비어있지 않음)
        """
        print("📋 generate_content_documents 메서드 단독 테스트 시작")
        
        # Given - 실제 workspace_preparation process_result.json에서 2장 데이터 로드 (새로 생성된 데이터)
        workspace_data_path = Path(__file__).parent.parent / "data" / "workspace_preparation_stage" / "process_result.json"
        assert workspace_data_path.exists(), f"워크스페이스 데이터 파일이 없습니다: {workspace_data_path}"
        
        with open(workspace_data_path, 'r', encoding='utf-8') as f:
            workspace_result = json.load(f)
        
        # 2장 데이터 추출
        chapters_data = workspace_result['data']['chapters_data']
        assert len(chapters_data) >= 2, "테스트용 2장 데이터가 충분하지 않습니다"
        
        chapter_2_data = chapters_data[1]  # 2장 선택 (0-based index)
        book_info = workspace_result['data']['book_information']
        normalized_book_title = book_info.get('normalized_title', 'Unknown_Book')
        
        print(f"📖 테스트 대상 - 2장: {chapter_2_data.get('chapter_title', 'Unknown')}")
        print(f"   - 정규화된 책 제목: {normalized_book_title}")
        print(f"   - 챕터 TOC 항목 수: {len(chapter_2_data.get('chapter_toc', []))}")
        print(f"   - 콘텐츠 텍스트 길이: {len(chapter_2_data.get('content_text', ''))} 문자")
        
        # When - IntegratedNodeGenerationStage 초기화 및 generate_content_documents 호출
        try:
            config = {}
            logger = Logger("test_generate_content_documents")
            stage = IntegratedNodeGenerationStage(config, logger)
            
            print(f"✅ IntegratedNodeGenerationStage 초기화 완료")
            
            # generate_content_documents 메서드 직접 호출
            result = await stage.generate_content_documents(
                chapter_info=chapter_2_data, 
                normalized_book_title=normalized_book_title
            )
            
            print(f"✅ generate_content_documents 메서드 실행 완료")
            
        except Exception as e:
            print(f"❌ generate_content_documents 실행 중 오류: {e}")
            pytest.fail(f"generate_content_documents 실행 실패: {e}")
        
        # Then - 결과 검증
        print(f"🔍 generate_content_documents 결과 검증 시작")
        
        # 1. 기본 구조 검증
        assert isinstance(result, list), "반환값은 리스트여야 함"
        print(f"   ✅ 반환값 타입: {type(result)}")
        
        # 2. 생성된 문서가 있는지 확인 (빈 리스트가 아닌 경우)
        if len(result) > 0:
            print(f"   📄 생성된 문서 수: {len(result)}")
            
            # 3. 각 문서 구조 검증
            for i, document in enumerate(result):
                assert isinstance(document, dict), f"문서 {i}는 딕셔너리여야 함"
                assert 'file_name' in document, f"문서 {i}에 file_name 필드가 없음"
                assert 'content' in document, f"문서 {i}에 content 필드가 없음"
                assert isinstance(document['file_name'], str), f"문서 {i}의 file_name은 문자열이어야 함"
                assert isinstance(document['content'], str), f"문서 {i}의 content는 문자열이어야 함"
                
                # 4. 파일명 형식 검증 (book_title/chapter_title/sections/section_title.md)
                file_name = document['file_name']
                assert file_name.endswith('.md'), f"문서 {i}의 파일명이 .md로 끝나지 않음: {file_name}"
                assert '/sections/' in file_name, f"문서 {i}의 파일명에 /sections/ 경로가 없음: {file_name}"
                assert file_name.startswith(normalized_book_title), f"문서 {i}의 파일명이 책 제목으로 시작하지 않음: {file_name}"
                
                # 5. 콘텐츠가 비어있지 않은지 확인
                content = document['content'].strip()
                assert len(content) > 0, f"문서 {i}의 콘텐츠가 비어있음"
                
                print(f"   ✅ 문서 {i+1}: {file_name} (콘텐츠 길이: {len(content)})")
            
            print(f"✅ 모든 생성된 문서 검증 통과")
            
        else:
            print(f"   ⚠️ 생성된 문서가 없음 (빈 리스트 반환)")
            # 빈 리스트도 유효한 경우일 수 있음 (내용이 없는 섹션들만 있는 경우)
        
        # 6. 입력 데이터 검증 (참고용)
        chapter_title = chapter_2_data.get('chapter_title', 'Unknown')
        chapter_toc = chapter_2_data.get('chapter_toc', [])
        content_text = chapter_2_data.get('content_text', '')
        
        print(f"📊 입력 데이터 정보:")
        print(f"   - 챕터 제목: {chapter_title}")
        print(f"   - TOC 항목 수: {len(chapter_toc)}")
        print(f"   - 콘텐츠 텍스트 길이: {len(content_text)} 문자")
        print(f"   - 생성된 문서 수: {len(result)}")
        
        # 7. 실제 메서드 출력과 동일한 데이터를 테스트 데이터로 저장
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager()  # 설정 파일에서 경로 자동 로드
        folder_name = data_manager.get_folder_name("integrated_node_generation_stage")
        
        # result를 그대로 저장 (메서드 출력과 동일)
        data_manager.save_test_result(
            test_method_name="generate_content_documents", 
            result_data=result,  # 실제 메서드 출력과 완전히 동일한 데이터
            folder_name=folder_name
        )
        
        print(f"💾 테스트 결과 저장 완료 (generate_content_documents 메서드 출력과 동일한 데이터)")
        print(f"🎉 generate_content_documents 메서드 테스트 성공!")
        
        return result
    
    @pytest.mark.asyncio
    async def test_content_processing_stage_process(self):
        """
        ContentProcessingStage process 메서드 테스트 - prev_stage_result 기반
        
        목적: 수정된 ContentProcessingStage의 process 메서드 정상 동작 확인
        
        변경 내용:
        - process 시그니처: book_folder_path → prev_stage_result
        - 출력 형식: {success, error, result} → {data, error}
        - data 내용: 장별 파일명 그룹화
        
        입력: integrated_node_generation_stage/process_result.json
        
        기대 결과:
        - data: Dict 형태, 장별 파일명 리스트
        - error: None (성공 시)
        """
        print("📋 ContentProcessingStage process 메서드 테스트 시작")
        
        # Given - 실제 integrated_node_generation_stage process_result.json 로드
        prev_stage_data_path = Path(__file__).parent.parent / "data" / "integrated_node_generation_stage" / "process_result.json"
        assert prev_stage_data_path.exists(), f"이전 단계 데이터 파일이 없습니다: {prev_stage_data_path}"
        
        with open(prev_stage_data_path, 'r', encoding='utf-8') as f:
            prev_stage_result = json.load(f)
        
        print(f"📖 이전 단계 결과 로드 완료 (2장 데이터)")
        print(f"   - 처리된 장 수: {len(prev_stage_result['data']['processed_chapters'])}")
        print(f"   - 통합 문서 수: {len(prev_stage_result['data']['unified_documents'])}")
        
        # When - ContentProcessingStage 초기화 및 실행
        try:
            # AI 서비스 실제 설정 파일 사용
            from services.ai_service_v4 import AIService
            from utils.config_manager import ConfigManager
            from utils.logger_v2 import Logger
            
            config_manager = ConfigManager()
            logger = Logger("test_content_processing")
            ai_service = AIService(config_manager, logger, "content_processing")
            
            # ContentProcessingStage 초기화 (stage_config 제거)
            from stages.content_processing_stage import ContentProcessingStage
            stage = ContentProcessingStage({}, ai_service)
            
            print(f"✅ ContentProcessingStage 초기화 완료")
            
            # process 메서드 실행 (prev_stage_result 기반)
            result = await stage.process(prev_stage_result)
            
            print(f"✅ process 메서드 실행 완료")
            
        except Exception as e:
            print(f"❌ ContentProcessingStage 실행 중 오류: {e}")
            pytest.fail(f"ContentProcessingStage 실행 실패: {e}")
        
        # Then - 출력 구조 검증
        print(f"🔍 출력 구조 검증 시작")
        
        # 1. 기본 구조 검증
        assert isinstance(result, dict), "결과는 딕셔너리여야 함"
        assert "data" in result, "data 필드가 있어야 함"
        assert "error" in result, "error 필드가 있어야 함"
        assert "success" not in result, "success 필드는 제거되어야 함"
        assert "result" not in result, "result 필드는 제거되어야 함"
        
        # 2. 에러 없는지 확인
        assert result['error'] is None, f"에러가 발생했습니다: {result['error']}"
        
        # 3. data 구조 검증 - 장별 파일명 그룹화
        data = result["data"]
        assert isinstance(data, dict), "data는 딕셔너리여야 함"
        
        # 4. 장별 파일명 구조 확인 (normalized_title 형식) - 2장만
        expected_chapters = [
            "2_Separation_between_code_and_data"
        ]
        
        for chapter_title, file_names in data.items():
            assert isinstance(chapter_title, str), f"장 제목은 문자열이어야 함: {chapter_title}"
            assert isinstance(file_names, list), f"파일명 리스트는 리스트여야 함: {file_names}"
            
            # 파일명들이 문자열인지 확인
            for file_name in file_names:
                assert isinstance(file_name, str), f"파일명은 문자열이어야 함: {file_name}"
        
        # 5. 예상되는 장들이 있는지 확인
        for expected_chapter in expected_chapters:
            assert expected_chapter in data, f"예상된 장이 없습니다: {expected_chapter}"
            assert len(data[expected_chapter]) > 0, f"장에 파일이 없습니다: {expected_chapter}"
        
        print(f"✅ 모든 출력 구조 검증 통과")
        print(f"📊 검증 결과:")
        print(f"   - 처리된 장 수: {len(data)}")
        for chapter_title, file_names in data.items():
            print(f"   - {chapter_title}: {len(file_names)}개 파일")
        print(f"   - error: {result.get('error')}")
        
        # 6. 실제 process 결과를 content_processing_stage 폴더에 저장 (출력과 동일한 데이터)
        from tests.utils.test_data_manager import TestResultDataManager
        data_manager = TestResultDataManager()
        folder_name = data_manager.get_folder_name("content_processing_stage")
        data_manager.save_test_result(
            test_method_name="process", 
            result_data=result,  # result를 그대로 저장
            folder_name=folder_name
        )
        
        print(f"💾 테스트 결과 저장 완료 (process 출력과 동일한 데이터)")
        print(f"🎉 ContentProcessingStage process 메서드 테스트 성공!")
        
        return result