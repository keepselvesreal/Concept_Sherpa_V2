# 생성 시간: 2025-08-09 16:15:09
# 핵심 내용: TDD로 개발하는 리프 노드 텍스트 추출기의 테스트 케이스들
# 상세 내용:
#   - test_load_leaf_nodes_from_json (라인 15): JSON 파일에서 리프 노드 데이터 로드 테스트
#   - test_extract_section_text_from_markdown (라인 25): 마크다운에서 특정 섹션 텍스트 추출 테스트
#   - test_sanitize_filename (라인 35): 파일명 정리 테스트 
#   - test_save_text_to_file (라인 41): 텍스트를 개별 파일로 저장 테스트
#   - test_process_all_leaf_nodes (라인 51): 전체 리프 노드 처리 통합 테스트
# 상태: 활성
# 주소: test_leaf_text_extractor
# 참조: 

import json
import os
import tempfile
from leaf_text_extractor import LeafTextExtractor

def test_load_leaf_nodes_from_json():
    """JSON 파일에서 리프 노드 데이터를 정확히 로드하는지 테스트"""
    extractor = LeafTextExtractor()
    
    # 테스트 데이터 생성
    test_data = [{"id": 67, "title": "7.1 Data validation in DOP", "level": 2}]
    
    nodes = extractor.load_leaf_nodes_from_data(test_data)
    assert len(nodes) == 1
    assert nodes[0]["id"] == 67
    assert nodes[0]["title"] == "7.1 Data validation in DOP"

def test_extract_section_text_from_markdown():
    """마크다운 파일에서 특정 섹션의 텍스트를 추출하는지 테스트"""
    extractor = LeafTextExtractor()
    
    # 테스트용 마크다운 콘텐츠
    markdown_content = """# 7.1 Data validation in DOP
    
Some content for section 7.1

# 7.2 Another section

Different content"""
    
    result = extractor.extract_section_text(markdown_content, "7.1 Data validation in DOP")
    assert "Some content for section 7.1" in result
    assert "Different content" not in result

def test_sanitize_filename():
    """파일명에서 특수문자를 제거하여 안전한 파일명을 생성하는지 테스트"""
    extractor = LeafTextExtractor()
    
    result = extractor.sanitize_filename("7.1 Data validation in DOP")
    assert result == "71_Data_validation_in_DOP"
    assert "/" not in result
    assert ":" not in result

def test_save_text_to_file():
    """텍스트를 파일로 저장하는 기능 테스트"""
    extractor = LeafTextExtractor()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_text = "This is test content"
        filename = "test_file.md"
        
        extractor.save_text_to_file(test_text, temp_dir, filename)
        
        file_path = os.path.join(temp_dir, filename)
        assert os.path.exists(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert test_text in saved_content

def test_process_all_leaf_nodes():
    """전체 리프 노드 처리 워크플로우 테스트"""
    extractor = LeafTextExtractor()
    
    # 이 테스트는 실제 파일들이 존재할 때 실행
    # 현재는 구조만 검증
    assert hasattr(extractor, 'process_all_leaf_nodes')

if __name__ == "__main__":
    print("테스트 실행 중...")
    
    try:
        test_load_leaf_nodes_from_json()
        print("✅ test_load_leaf_nodes_from_json 통과")
    except Exception as e:
        print(f"❌ test_load_leaf_nodes_from_json 실패: {e}")
    
    try:
        test_extract_section_text_from_markdown()
        print("✅ test_extract_section_text_from_markdown 통과")
    except Exception as e:
        print(f"❌ test_extract_section_text_from_markdown 실패: {e}")
    
    try:
        test_sanitize_filename()
        print("✅ test_sanitize_filename 통과")
    except Exception as e:
        print(f"❌ test_sanitize_filename 실패: {e}")
        
    try:
        test_save_text_to_file()
        print("✅ test_save_text_to_file 통과")
    except Exception as e:
        print(f"❌ test_save_text_to_file 실패: {e}")
        
    try:
        test_process_all_leaf_nodes()
        print("✅ test_process_all_leaf_nodes 통과")
    except Exception as e:
        print(f"❌ test_process_all_leaf_nodes 실패: {e}")
        
    print("테스트 완료!")