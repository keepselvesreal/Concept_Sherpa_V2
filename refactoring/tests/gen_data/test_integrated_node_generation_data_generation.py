# 생성 시간: Tue Sep 10 15:52:47 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 실제 데이터 생성 및 픽스처 자동 생성 테스트
# 상세 내용:
#   - TestIntegratedNodeGenerationDataGeneration (라인 20-180): 실제 데이터 생성 → 픽스처 자동 생성 클래스
#   - test_generate_all_method_data (라인 25-120): 각 메서드 실행하여 결과 저장 및 픽스처 생성
#   - _load_workspace_data (라인 122-140): workspace_result.json 로드 및 선택 챕터 필터링
#   - _save_test_data (라인 142-165): 테스트 데이터 JSON 저장
#   - _generate_fixtures (라인 167-180): 픽스처 파일 자동 생성
# 상태: active
# 참조: test_workspace_preparation_data_generation.py (참조 패턴), integrated_node_generation_stage_v4.py (테스트 대상)

import pytest
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# 기존 공통 픽스처들
pytest_plugins = ["tests.fixtures.workspace_preparation_fixtures"]

class TestIntegratedNodeGenerationDataGeneration:
    """IntegratedNodeGenerationStage 실제 데이터 생성 → 픽스처 자동 생성"""
    
    @pytest.mark.asyncio
    async def test_generate_node_documents_data(self, config_manager, test_logger, selected_chapters=[1, 2]):
        """
        📝 generate_node_documents 데이터만 생성
        
        Args:
            selected_chapters: 처리할 챕터 번호 리스트 (1-based)
        """
        print(f"📝 generate_node_documents 데이터 생성 시작")
        print(f"📊 선택 챕터: {selected_chapters}")
        
        # 1. workspace_result 로드 및 선택 챕터 필터링
        workspace_data, selected_chapters_data = self._load_workspace_data(selected_chapters)
        print(f"📖 로드된 총 챕터: {len(workspace_data.get('chapters_analysis', {}).get('chapters_info', []))}개")
        print(f"🎯 선택된 챕터: {len(selected_chapters_data)}개")
        
        # 2. IntegratedNodeGenerationStage 초기화
        from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
        stage = IntegratedNodeGenerationStage(config_manager, None)
        stage.logger = test_logger
        
        # 3. generate_node_documents 실행
        node_results = []
        for chapter_data in selected_chapters_data:
            chapter_title = chapter_data.get('chapter_title', 'Unknown')
            print(f"  📖 처리 중: {chapter_title}")
            
            try:
                chapter_node_results = await stage.generate_node_documents(chapter_data)
                node_results.extend(chapter_node_results)
                print(f"  ✅ 완료: {len(chapter_node_results)}개 노드 문서")
            except Exception as e:
                print(f"  ❌ 오류: {str(e)}")
                raise
        
        self._save_test_data("generate_node_documents_result", node_results, selected_chapters_data)
        print(f"💾 노드 문서 결과 저장: {len(node_results)}개")

    @pytest.mark.asyncio
    async def test_generate_content_documents_data(self, config_manager, test_logger, selected_chapters=[1, 2]):
        """
        🤖 generate_content_documents 데이터만 생성 (AI API 호출)
        
        Args:
            selected_chapters: 처리할 챕터 번호 리스트 (1-based)
        """
        print(f"🤖 generate_content_documents 데이터 생성 시작")
        print(f"📊 선택 챕터: {selected_chapters}")
        
        # 1. workspace_result 로드 및 선택 챕터 필터링
        workspace_data, selected_chapters_data = self._load_workspace_data(selected_chapters)
        print(f"🎯 선택된 챕터: {len(selected_chapters_data)}개")
        
        # 2. IntegratedNodeGenerationStage 초기화
        from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
        stage = IntegratedNodeGenerationStage(config_manager, None)
        stage.logger = test_logger
        
        # 3. generate_content_documents 실행
        content_results = []
        for chapter_data in selected_chapters_data:
            chapter_title = chapter_data.get('chapter_title', 'Unknown')
            print(f"  📖 처리 중: {chapter_title}")
            
            try:
                chapter_content_results = await stage.generate_content_documents(chapter_data)
                content_results.extend(chapter_content_results)
                print(f"  ✅ 완료: {len(chapter_content_results)}개 콘텐츠 문서")
            except Exception as e:
                print(f"  ❌ AI API 오류: {str(e)}")
                print(f"  ⚠️ 빈 결과로 계속 진행")
        
        self._save_test_data("generate_content_documents_result", content_results, selected_chapters_data)
        print(f"💾 콘텐츠 문서 결과 저장: {len(content_results)}개")

    @pytest.mark.asyncio
    async def test_integrate_documents_data(self, config_manager, test_logger, selected_chapters=[1, 2]):
        """
        🔗 integrate_documents 데이터만 생성 (AI API 없음)
        
        Args:
            selected_chapters: 처리할 챕터 번호 리스트 (1-based)
        """
        print(f"🔗 integrate_documents 데이터 생성 시작")
        print(f"📊 선택 챕터: {selected_chapters}")
        
        # 1. workspace_result 로드 및 선택 챕터 필터링
        workspace_data, selected_chapters_data = self._load_workspace_data(selected_chapters)
        print(f"🎯 선택된 챕터: {len(selected_chapters_data)}개")
        
        # 2. IntegratedNodeGenerationStage 초기화
        from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
        stage = IntegratedNodeGenerationStage(config_manager, None)
        stage.logger = test_logger
        
        # 3. 기존 데이터 로드 (node_results, content_results 필요)
        from pathlib import Path
        import json
        
        # node_documents_result 로드 (새로운 구조)
        node_data_path = Path("tests/data/integrated_node_generation/generate_node_documents_result.json")
        if node_data_path.exists():
            with open(node_data_path, 'r', encoding='utf-8') as f:
                node_data = json.load(f)
            node_results = node_data["documents"]  # 새로운 구조에서 documents 필드 사용
            print(f"📝 기존 node_results 로드: {len(node_results)}개")
        else:
            print("⚠️ node_results 파일이 없습니다. test_generate_node_documents_data를 먼저 실행하세요.")
            node_results = []
        
        # content_documents_result 로드 (새로운 구조)
        content_data_path = Path("tests/data/integrated_node_generation/generate_content_documents_result.json")
        if content_data_path.exists():
            with open(content_data_path, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            content_results = content_data["documents"]  # 새로운 구조에서 documents 필드 사용
            print(f"🤖 기존 content_results 로드: {len(content_results)}개")
        else:
            print("⚠️ content_results 파일이 없습니다. test_generate_content_documents_data를 먼저 실행하세요.")
            content_results = []
        
        # 4. integrate_documents 실행
        integrate_results = []
        for i, chapter_data in enumerate(selected_chapters_data):
            chapter_title = chapter_data.get('chapter_title', 'Unknown')
            print(f"  📖 통합 처리 중: {chapter_title}")
            
            try:
                chapter_integrate_results = await stage.integrate_documents(
                    chapter_data, 
                    node_results,     # 전체 노드 결과 사용
                    content_results   # 전체 콘텐츠 결과 사용
                )
                integrate_results.extend(chapter_integrate_results)
                print(f"  ✅ 완료: {len(chapter_integrate_results)}개 통합 문서")
            except Exception as e:
                print(f"  ❌ 오류: {str(e)}")
                raise
        
        self._save_test_data("integrate_documents_result", integrate_results, selected_chapters_data)
        print(f"💾 통합 문서 결과 저장: {len(integrate_results)}개")

    @pytest.mark.asyncio
    async def test_process_data(self, config_manager, test_logger, selected_chapters=[1, 2]):
        """
        🚀 process 메서드 완전 실행 데이터 생성 (전체 파이프라인)
        
        Args:
            selected_chapters: 처리할 챕터 번호 리스트 (1-based)
        """
        print(f"🚀 process 메서드 완전 실행 데이터 생성 시작")
        print(f"📊 선택 챕터: {selected_chapters}")
        
        # 1. workspace_result 로드 및 선택 챕터 필터링
        workspace_data, selected_chapters_data = self._load_workspace_data(selected_chapters)
        print(f"🎯 선택된 챕터: {len(selected_chapters_data)}개")
        
        # 2. IntegratedNodeGenerationStage 초기화
        from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
        stage = IntegratedNodeGenerationStage(config_manager, None)
        stage.logger = test_logger
        
        # 3. process 메서드 실행 (전체 파이프라인)
        input_data = {
            'data': {
                'chapters_analysis': {
                    'chapters_info': selected_chapters_data
                }
            }
        }
        
        try:
            process_result = await stage.process(input_data)
            print(f"✅ process 메서드 실행 완료")
            print(f"   - 성공 여부: {process_result['success']}")
            if process_result['success']:
                data = process_result['data']
                print(f"   - 처리된 챕터: {len(data['processed_chapters'])}개")
                print(f"   - 통합 문서: {len(data['unified_documents'])}개")
                
                # 처리된 챕터 정보 출력
                for i, chapter in enumerate(data['processed_chapters'], 1):
                    print(f"     {i}. {chapter['chapter_title']} → {chapter['normalized_title']}")
            else:
                print(f"   - 오류: {process_result['error']}")
                
        except Exception as e:
            print(f"❌ process 메서드 실행 오류: {str(e)}")
            raise
        
        # 4. 결과 저장
        self._save_test_data("process_result", process_result, selected_chapters_data)
        print(f"💾 process 결과 저장 완료")
        
    def _load_workspace_data(self, selected_chapters: List[int]) -> tuple:
        """
        workspace_result.json 로드 및 선택 챕터 필터링
        
        Args:
            selected_chapters: 1-based 챕터 번호 리스트
            
        Returns:
            tuple: (전체_workspace_data, 선택된_챕터들)
        """
        # workspace_result.json 로드
        workspace_path = Path("tests/data/workspace_preparation/workspace_result.json")
        if not workspace_path.exists():
            raise FileNotFoundError(f"workspace_result.json이 없습니다: {workspace_path}")
            
        with open(workspace_path, 'r', encoding='utf-8') as f:
            workspace_result = json.load(f)
            
        workspace_data = workspace_result['data']
        all_chapters = workspace_data.get('chapters_data', [])  # ✅ chapters_data 사용! (실제 데이터)
        
        # 선택된 챕터 필터링 (1-based → 0-based 변환)
        selected_chapters_data = []
        for chapter_num in selected_chapters:
            if 1 <= chapter_num <= len(all_chapters):
                # ✅ 실제 chapters_data 사용 (이미 완전한 데이터 구조)
                selected_chapters_data.append(all_chapters[chapter_num - 1])
            else:
                raise ValueError(f"❌ 챕터 {chapter_num}이 존재하지 않습니다. 총 {len(all_chapters)}개 챕터")
        
        return workspace_data, selected_chapters_data
    
    def _save_test_data(self, name: str, data: Any, selected_chapters_data: List[Dict] = None, format: str = "json"):
        """
        테스트 데이터 저장 - integrated_node_generation 폴더에
        
        Args:
            name: 파일명 (확장자 제외)
            data: 저장할 데이터 (문서 결과)
            selected_chapters_data: 선택된 장들의 정보
            format: 저장 형식 ('json')
        """
        data_dir = Path("tests/data/integrated_node_generation")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 선택된 장 정보 생성 (chapter_title + normalized_title)
        selected_chapters = []
        if selected_chapters_data:
            from utils.text_utils import normalize_title
            for chapter in selected_chapters_data:
                chapter_title = chapter.get('chapter_title', 'Unknown Chapter')
                selected_chapters.append({
                    "chapter_title": chapter_title,
                    "normalized_title": normalize_title(chapter_title)
                })
        
        # 최종 저장 데이터 구조
        save_data = {
            "selected_chapters": selected_chapters,
            "documents": data
        }
        
        if format == "json":
            file_path = data_dir / f"{name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"지원하지 않는 형식입니다: {format}")
        
        print(f"💾 저장: {file_path}")
    
    def _generate_fixtures(self, workspace_data: Dict, selected_chapters_data: List[Dict], 
                          node_results: List, content_results: List, integrate_results: List):
        """
        픽스처 파일 자동 생성 - 선택된 챕터 데이터 동적 반영
        """
        fixtures_dir = Path("tests/fixtures")
        fixtures_dir.mkdir(parents=True, exist_ok=True)
        
        # 선택된 챕터 정보
        chapter_nums = [i+1 for i in range(len(selected_chapters_data))]  # 1-based indexing
        chapter_titles = [ch.get('chapter_title', 'Unknown') for ch in selected_chapters_data]
        
        fixture_content = f'''# 생성 시간: Auto-generated from test_integrated_node_generation_data_generation.py
# 핵심 내용: IntegratedNodeGenerationStage 전용 픽스처 정의 (동적 생성)
# 선택된 챕터: {chapter_nums} ({', '.join(chapter_titles)})
# 상세 내용:
#   - integrated_stage (라인 16-26): IntegratedNodeGenerationStage 인스턴스 생성
#   - integrated_stage_with_mock (라인 28-41): Mock AI 서비스가 적용된 Stage 인스턴스
#   - selected_chapters_data (라인 43-51): 선택된 챕터들의 테스트 데이터 (동적)
#   - expected_node_documents (라인 53-61): generate_node_documents 예상 결과
#   - expected_content_documents (라인 63-71): generate_content_documents 예상 결과  
#   - expected_integrate_documents (라인 73-81): integrate_documents 예상 결과
# 상태: active
# 참조: 자동 생성됨

import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def integrated_stage(config_manager, test_logger):
    """IntegratedNodeGenerationStage 인스턴스 생성"""
    from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
    
    stage = IntegratedNodeGenerationStage(config_manager, None)
    stage.logger = test_logger
    return stage

@pytest.fixture  
def integrated_stage_with_mock(config_manager, test_logger):
    """Mock AI 서비스가 적용된 IntegratedNodeGenerationStage"""
    from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
    
    stage = IntegratedNodeGenerationStage(config_manager, None)
    stage.logger = test_logger
    
    # ContentDocumentService Mock 설정
    mock_service = AsyncMock()
    mock_service.detect_section_content.return_value = [
        {{"id": 1, "title": "Mock Section", "has_content": True}}
    ]
    mock_service.extract_section_content.return_value = "Mock extracted content"
    stage.content_document_service = mock_service
    
    return stage

@pytest.fixture
def selected_chapters_data():
    """선택된 챕터들의 테스트 데이터 (챕터 {chapter_nums}: {', '.join(chapter_titles)})"""
    return {json.dumps(selected_chapters_data, ensure_ascii=False, indent=4)}

@pytest.fixture
def expected_node_documents():
    """generate_node_documents 예상 결과 (총 {len(node_results)}개)"""
    return {json.dumps(node_results, ensure_ascii=False, indent=4)}

@pytest.fixture
def expected_content_documents():
    """generate_content_documents 예상 결과 (총 {len(content_results)}개)"""
    return {json.dumps(content_results, ensure_ascii=False, indent=4)}

@pytest.fixture
def expected_integrate_documents():
    """integrate_documents 예상 결과 (총 {len(integrate_results)}개)"""
    return {json.dumps(integrate_results, ensure_ascii=False, indent=4)}
'''
        
        fixture_file = fixtures_dir / "integrated_node_generation_fixtures.py"
        with open(fixture_file, 'w', encoding='utf-8') as f:
            f.write(fixture_content)
            
        print(f"🎭 픽스처 파일 생성: {fixture_file}")
        print(f"   📊 선택 챕터: {chapter_nums} ({', '.join(chapter_titles)})")
        print(f"   📝 데이터 개수: 노드({len(node_results)}), 콘텐츠({len(content_results)}), 통합({len(integrate_results)})")