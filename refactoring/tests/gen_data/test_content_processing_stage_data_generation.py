# 생성 시간: Thu Sep 11 15:09:19 KST 2025
# 핵심 내용: ContentProcessingStage 각 메서드별 실행 결과 데이터 생성 및 저장
# 상세 내용:
#   - TestContentProcessingStageDataGeneration (라인 20-50): 데이터 생성 메인 클래스
#   - test_generate_load_and_sort_data (라인 25-60): load_and_sort_documents 실행 및 결과 저장
#   - _save_data (라인 62-80): 결과 데이터 저장 유틸리티 메서드
# 상태: active

import asyncio
import json
import pytest
from pathlib import Path
from typing import Dict, Any, List

import sys
from pathlib import Path
# refactoring 프로젝트 경로 추가
refactoring_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(refactoring_root))

from stages.content_processing_stage import ContentProcessingStage
from utils.logger_v2 import Logger


def load_test_document_for_generation(chapter_idx: int = 0, node_type: str = "leaf", node_idx: int = 0) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    데이터 생성용 문서 로더 (선택 정보와 함께 반환)
    
    Args:
        chapter_idx: 장 인덱스 (0부터 시작)
        node_type: 노드 타입 ("leaf" 또는 "non_leaf")
        node_idx: 노드 인덱스 (0부터 시작, -1이면 모든 노드 반환)
    
    Returns:
        tuple: (선택된 문서 데이터 또는 문서 리스트, 선택 정보)
    """
    data_path = Path(__file__).parent.parent / "data" / "content_processing" / "load_and_sort_result.json"
    assert data_path.exists(), f"테스트 데이터 파일이 없습니다: {data_path}"
    
    with open(data_path, 'r', encoding='utf-8') as f:
        load_and_sort_data = json.load(f)
    
    # 데이터 구조: result.output.chapters[].leaf_nodes[] 또는 non_leaf_nodes[]
    chapters = load_and_sort_data.get('result', {}).get('output', {}).get('chapters', [])
    assert chapters and len(chapters) > chapter_idx, f"{chapter_idx + 1}장 데이터가 없습니다 (총 {len(chapters)}장)"
    
    target_chapter = chapters[chapter_idx]
    
    if node_type == "leaf":
        nodes = target_chapter.get('leaf_nodes', [])
        node_type_desc = "리프 노드"
    elif node_type == "non_leaf":
        nodes = target_chapter.get('non_leaf_nodes', [])
        node_type_desc = "비리프 노드"
    else:
        raise ValueError(f"지원하지 않는 노드 타입: {node_type}. 'leaf' 또는 'non_leaf'를 사용하세요.")
    
    assert nodes, f"{chapter_idx + 1}장에 {node_type_desc} 데이터가 없습니다"
    
    # 선택 정보 생성
    selection_info = {
        "chapter_idx": chapter_idx,
        "node_type": node_type,
        "node_idx": node_idx
    }
    
    if node_idx == -1:
        # 모든 노드 반환
        print(f"📚 {chapter_idx + 1}장 {node_type_desc} 전체 로드: {len(nodes)}개")
        return nodes, selection_info
    else:
        # 특정 노드 반환
        assert len(nodes) > node_idx, f"{chapter_idx + 1}장 {node_type_desc}에서 {node_idx + 1}번째 데이터가 없습니다 (총 {len(nodes)}개)"
        selected_node = nodes[node_idx]
        print(f"📄 {chapter_idx + 1}장 {node_type_desc} {node_idx + 1}번째 데이터 로드: {selected_node.get('title', 'Unknown')}")
        return selected_node, selection_info


class TestContentProcessingStageDataGeneration:
    """ContentProcessingStage 각 메서드별 실행 결과 데이터 생성"""
    
    @pytest.mark.asyncio
    async def test_generate_load_and_sort_data(self):
        """
        load_and_sort_documents 메서드 실행하여 결과 데이터 생성 및 저장
        
        입력: process_result.json의 documents.data 필드
        출력: load_and_sort_result.json (장별 그룹화된 문서 데이터)
        """
        print("📋 load_and_sort_documents 데이터 생성 시작")
        
        # Given - 입력 데이터 로드
        input_data_path = Path(__file__).parent.parent / "data" / "integrated_node_generation" / "process_result.json"
        assert input_data_path.exists(), f"입력 데이터 파일이 없습니다: {input_data_path}"
        
        with open(input_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # documents.data 필드 추출
        documents_result = raw_data.get('documents', {})
        input_data = documents_result.get('data', {})
        assert input_data, "입력 데이터가 비어있습니다"
        
        print(f"📖 입력 데이터 로드 완료: {input_data_path}")
        
        # ContentProcessingStage 초기화
        config = {}
        logger = Logger("content_processing_data_generation")
        stage = ContentProcessingStage(config, logger)
        
        # When - load_and_sort_documents 실행
        result = await stage.load_and_sort_documents(input_data)
        
        # Then - 결과 검증 및 저장
        assert isinstance(result, dict), "결과는 딕셔너리여야 함"
        assert "output" in result, "output 필드가 있어야 함"
        assert "error" in result, "error 필드가 있어야 함"
        assert result["error"] is None, "성공 시 error는 None이어야 함"
        
        chapters = result["output"]["chapters"]
        assert isinstance(chapters, list), "chapters는 리스트여야 함"
        assert len(chapters) > 0, "결과가 비어있으면 안됨"
        
        print(f"✅ load_and_sort_documents 실행 완료: {len(chapters)}개 장")
        
        # 결과 데이터 저장
        result_data = {
            "method": "load_and_sort_documents",
            "input_source": str(input_data_path),
            "generation_time": "Thu Sep 11 15:09:19 KST 2025",
            "result": result
        }
        
        self._save_data("load_and_sort_result", result_data)
        print(f"💾 데이터 저장 완료")
    
    @pytest.mark.asyncio
    @pytest.mark.expensive  # AI 호출 비용
    async def test_generate_extract_section_data(self):
        """
        generate_extract_section 메서드 실행하여 결과 데이터 생성 및 저장
        
        입력: load_and_sort_result.json에서 선택한 문서
        출력: extract_section_result.json (AI 추출 결과 데이터)
        
        사용 예시:
        - 1장 리프 노드 첫 번째: load_test_document_for_generation(0, "leaf", 0)
        - 1장 비리프 노드 첫 번째: load_test_document_for_generation(0, "non_leaf", 0)
        - 2장 리프 노드 두 번째: load_test_document_for_generation(1, "leaf", 1)
        """
        print("🤖 generate_extract_section 데이터 생성 시작")
        
        # Given - 1장 리프 노드 첫 번째 문서 로드
        sample_document, data_selection = load_test_document_for_generation(chapter_idx=0, node_type="leaf", node_idx=0)
        
        # ContentProcessingStage 초기화 (AI 서비스 포함)
        config = {}
        logger = Logger("content_processing_data_generation")
        
        # AI 서비스 직접 임포트 및 초기화 
        from services.ai_service_v4 import AIService
        ai_service = AIService(config, logger, "content_processing")
        stage = ContentProcessingStage(config, ai_service)
        
        # When - generate_extract_section 실행
        extraction_result = await stage.generate_extract_section(sample_document)
        
        # Then - 결과 검증 및 저장
        assert isinstance(extraction_result, dict), "결과는 딕셔너리여야 함"
        print(f"✅ generate_extract_section 실행 완료: {len(extraction_result)}개 섹션")
        
        # 결과 데이터 저장
        input_data_path = Path(__file__).parent.parent / "data" / "content_processing" / "load_and_sort_result.json"
        result_data = {
            "method": "generate_extract_section",
            "input_source": str(input_data_path),
            "data_selection": data_selection,
            "sample_document": {
                "title": sample_document.get('title', ''),
                "level": sample_document.get('level', 0),
                "content_preview": sample_document.get('content_section', '')[:200] + "..."
            },
            "generation_time": self._get_current_time(),
            "ai_calls_count": stage.api_calls_counter,
            "result": extraction_result
        }
        
        self._save_data("extract_section_result", result_data)
        print(f"💾 AI 추출 결과 저장 완료 ({stage.api_calls_counter}회 호출)")
    
    def _get_current_time(self) -> str:
        """현재 시간 문자열 반환"""
        from datetime import datetime
        
        now = datetime.now()
        return now.strftime("%a %b %d %H:%M:%S KST %Y")
    
    def _save_data(self, filename: str, data: Dict[str, Any], format: str = "json"):
        """
        결과 데이터 저장 유틸리티
        
        Args:
            filename: 파일명 (확장자 제외)
            data: 저장할 데이터
            format: 저장 형식 (기본값: json)
        """
        # 저장 디렉토리 생성
        output_dir = Path(__file__).parent.parent / "data" / "content_processing"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            file_path = output_dir / f"{filename}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"지원하지 않는 형식: {format}")
        
        print(f"💾 저장 완료: {file_path}")
        return file_path