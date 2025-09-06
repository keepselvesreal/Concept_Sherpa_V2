# 생성 시간: Thu Sep  5 11:50:00 KST 2025
# 핵심 내용: extract_content_nodes 메서드 1장 실제 데이터 테스트
# 상세 내용:
#   - TestExtractContentNodesChapter1 (라인 20-80): 1장 데이터 기반 테스트 클래스
#   - test_extract_content_nodes_chapter_1 (라인 30-80): 1장 데이터 테스트
#   - MockConfigManager (라인 12-25): 테스트용 설정 관리자
# 상태: active

import os
import json
import pytest
import asyncio

# 테스트 대상 클래스
from src.stages.integrated_node_generation_stage_v2 import IntegratedNodeGenerationStage

class MockConfigManager:
    def __init__(self, config_dir):
        self.config_dir = config_dir
    
    def get_config(self, section, key=None):
        # AI 설정 반환 (기본값)
        if section == "default_ai":
            return {
                "provider": "gemini",
                "model": "gemini-2.0-flash-lite",
                "temperature": 0.1,
                "max_tokens": 8192,
                "api_key": None
            }
        return {}

class TestExtractContentNodesChapter1:
    """extract_content_nodes 메서드 1장 실제 데이터 테스트"""
    
    @pytest.fixture
    def setup_stage(self):
        """테스트 환경 설정"""
        config_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/config"
        config_manager = MockConfigManager(config_dir)
        stage = IntegratedNodeGenerationStage(config_manager)
        return stage
    
    @pytest.mark.asyncio
    async def test_extract_content_nodes_chapter_1(self, setup_stage):
        """1장 실제 데이터로 extract_content_nodes 테스트"""
        stage = setup_stage
        
        # 1장 실제 데이터 경로
        chapter_1_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
        
        # 필수 파일 존재 확인
        toc_file = os.path.join(chapter_1_path, "1_Complexity_of_object_oriented_programming_toc.json")
        content_file = os.path.join(chapter_1_path, "1_Complexity_of_object_oriented_programming_content.md")
        
        assert os.path.exists(toc_file), f"TOC 파일이 존재하지 않음: {toc_file}"
        assert os.path.exists(content_file), f"Content 파일이 존재하지 않음: {content_file}"
        
        # extract_content_nodes 실행
        result = await stage.extract_content_nodes(chapter_1_path)
        
        # 기본 결과 검증
        assert result['success'] is True, f"extract_content_nodes 실패: {result.get('error', '')}"
        assert result['error'] is None
        
        # content.json 파일 생성 확인
        content_json_file = os.path.join(chapter_1_path, "content.json")
        assert os.path.exists(content_json_file), f"content.json 파일이 생성되지 않음: {content_json_file}"
        
        # content.json 내용 확인
        with open(content_json_file, 'r', encoding='utf-8') as f:
            content_nodes = json.load(f)
        
        assert isinstance(content_nodes, list), "content.json은 배열이어야 함"
        assert len(content_nodes) > 0, "content.json에 노드가 없음"
        
        # has_content 필드 확인
        has_content_count = 0
        for node in content_nodes:
            assert 'has_content' in node, f"노드에 has_content 필드 없음: {node.get('title', '?')}"
            assert isinstance(node['has_content'], bool), f"has_content는 boolean이어야 함: {node.get('title', '?')}"
            
            if node['has_content']:
                has_content_count += 1
        
        print(f"1장 테스트 완료: {len(content_nodes)}개 노드 중 {has_content_count}개 내용 포함")
        
        # 원본 TOC 구조 유지 확인
        with open(toc_file, 'r', encoding='utf-8') as f:
            original_toc = json.load(f)
        
        assert len(content_nodes) == len(original_toc), "content.json과 원본 TOC 노드 수가 다름"
        
        # 필수 필드들이 유지되는지 확인
        for i, (original, content) in enumerate(zip(original_toc, content_nodes)):
            assert content['id'] == original['id'], f"노드 {i}: id 불일치"
            assert content['title'] == original['title'], f"노드 {i}: title 불일치"
            assert content['level'] == original['level'], f"노드 {i}: level 불일치"

if __name__ == "__main__":
    # 비동기 테스트 실행
    async def run_test():
        config_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/config"
        config_manager = MockConfigManager(config_dir)
        stage = IntegratedNodeGenerationStage(config_manager)
        
        print("=== extract_content_nodes 1장 테스트 시작 ===")
        
        try:
            chapter_1_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
            result = await stage.extract_content_nodes(chapter_1_path)
            print(f"1장 결과: {result}")
        except Exception as e:
            print(f"1장 테스트 실패: {e}")
    
    # 비동기 실행
    asyncio.run(run_test())