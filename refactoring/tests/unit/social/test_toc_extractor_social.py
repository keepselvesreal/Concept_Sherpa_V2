# 생성 시간: Thu Sep  4 08:17:51 KST 2025
# 핵심 내용: toc_extractor 함수들의 Social Unit 테스트 (실제 데이터 기반)
# 상세 내용:
#   - TestTocExtractorSocial (라인 20-155): toc_extractor 함수들의 social unit 테스트 클래스
#   - test_extract_toc_with_pymupdf_real_data (라인 25-45): 실제 PDF에서 목차 추출 테스트
#   - test_process_toc_items_real_data (라인 47-73): 추출된 실제 데이터로 부모-자식 관계 설정 테스트  
#   - test_calculate_page_ranges_real_data (라인 75-105): 실제 데이터로 페이지 범위 계산 테스트
#   - test_full_workflow_real_data (라인 107-155): 전체 워크플로우 통합 테스트 (extract → process → calculate)
# 상태: active
# 주소: tests/unit/social/test_toc_extractor_social
# 참조: N/A

import pytest
import sys
import os
from pathlib import Path

# 기존 toc_extractor 모듈 임포트를 위한 경로 설정
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/inbox/25-08-30')
from toc_extractor import extract_toc_with_pymupdf, process_toc_items, calculate_page_ranges

@pytest.mark.social_unit
class TestTocExtractorSocial:
    """
    toc_extractor 함수들의 Social Unit 테스트
    - 실제 PDF 파일 사용
    - 함수들 간의 협력 테스트 (내부 의존성 포함)
    - 기존 로직의 정상 동작 확인
    """
    
    def test_extract_toc_with_pymupdf_real_data(self, real_pdf_path):
        """
        요구사항: PyMuPDF를 사용하여 실제 PDF에서 목차 구조 추출
        입력: 실제 PDF 파일 경로 (str)
        출력: 목차 항목 리스트 (List[Dict]) - id, title, level, page, parent_id, children_ids 포함
        """
        # When: 실제 PDF에서 목차 추출
        toc_items = extract_toc_with_pymupdf(real_pdf_path)
        
        # Then: 추출 결과 검증
        assert isinstance(toc_items, list), "목차 항목은 리스트여야 함"
        assert len(toc_items) > 0, "실제 PDF에서 목차 항목이 추출되어야 함"
        
        # 첫 번째 항목 구조 검증
        first_item = toc_items[0]
        required_fields = ['id', 'title', 'level', 'page', 'parent_id', 'children_ids']
        for field in required_fields:
            assert field in first_item, f"목차 항목에 {field} 필드가 있어야 함"
        
        # 데이터 타입 검증
        assert isinstance(first_item['id'], int), "id는 정수여야 함"
        assert isinstance(first_item['title'], str), "title은 문자열이어야 함"
        assert isinstance(first_item['level'], int), "level은 정수여야 함"
        assert isinstance(first_item['page'], int), "page는 정수여야 함"
        assert isinstance(first_item['children_ids'], list), "children_ids는 리스트여야 함"
        
        # 실제 데이터 저장 (다음 테스트에서 사용)
        self.extracted_toc_data = toc_items

    def test_process_toc_items_real_data(self, real_pdf_path):
        """
        요구사항: 추출된 목차 항목들의 부모-자식 관계 설정 및 계층 구조 생성
        입력: 추출된 목차 항목 리스트 (List[Dict])
        출력: 부모-자식 관계가 설정된 목차 항목 리스트 (List[Dict])
        """
        # Given: 실제 PDF에서 추출한 목차 데이터
        raw_toc_items = extract_toc_with_pymupdf(real_pdf_path)
        assert len(raw_toc_items) > 0, "전제조건: 목차 항목이 있어야 함"
        
        # When: 부모-자식 관계 처리
        processed_items = process_toc_items(raw_toc_items)
        
        # Then: 처리 결과 검증
        assert isinstance(processed_items, list), "처리된 항목은 리스트여야 함"
        assert len(processed_items) == len(raw_toc_items), "항목 수는 동일해야 함"
        
        # 부모-자식 관계 검증
        for item in processed_items:
            if item['parent_id'] is not None:
                # 부모 항목이 존재하는지 확인
                parent_found = any(p['id'] == item['parent_id'] for p in processed_items)
                assert parent_found, f"항목 {item['id']}의 부모 {item['parent_id']}가 존재해야 함"
                
                # 부모의 children_ids에 포함되는지 확인
                parent_item = next(p for p in processed_items if p['id'] == item['parent_id'])
                assert item['id'] in parent_item['children_ids'], "부모의 자식 목록에 포함되어야 함"
        
        # 실제 처리된 데이터 저장
        self.processed_toc_data = processed_items

    def test_calculate_page_ranges_real_data(self, real_pdf_path):
        """
        요구사항: 목차 항목들의 페이지 범위 계산 (start_page, end_page, page_count)
        입력: 부모-자식 관계가 설정된 목차 항목 리스트 (List[Dict])
        출력: 페이지 범위가 계산된 목차 항목 리스트 (List[Dict])
        """
        # Given: 실제 PDF에서 추출하고 처리한 목차 데이터
        raw_toc_items = extract_toc_with_pymupdf(real_pdf_path)
        processed_items = process_toc_items(raw_toc_items)
        assert len(processed_items) > 0, "전제조건: 처리된 목차 항목이 있어야 함"
        
        # When: 페이지 범위 계산
        complete_items = calculate_page_ranges(processed_items)
        
        # Then: 계산 결과 검증
        assert isinstance(complete_items, list), "완성된 항목은 리스트여야 함"
        assert len(complete_items) == len(processed_items), "항목 수는 동일해야 함"
        
        # 페이지 범위 필드 검증
        for item in complete_items:
            assert 'start_page' in item, "start_page 필드가 있어야 함"
            assert 'end_page' in item, "end_page 필드가 있어야 함"
            assert 'page_count' in item, "page_count 필드가 있어야 함"
            
            # 페이지 범위 논리 검증
            assert item['start_page'] <= item['end_page'], "시작 페이지는 끝 페이지보다 작거나 같아야 함"
            assert item['page_count'] == item['end_page'] - item['start_page'] + 1, "페이지 수 계산이 정확해야 함"
            assert item['page_count'] >= 1, "페이지 수는 최소 1이어야 함"
        
        # 실제 완성된 데이터 저장
        self.complete_toc_data = complete_items

    def test_full_workflow_real_data(self, real_pdf_path):
        """
        요구사항: 전체 목차 추출 워크플로우 통합 테스트 (extract → process → calculate)
        입력: 실제 PDF 파일 경로 (str)
        출력: 완전한 목차 구조 데이터 (List[Dict]) - 모든 필드와 관계 포함
        """
        # When: 전체 워크플로우 실행
        # Step 1: 목차 추출
        raw_toc_items = extract_toc_with_pymupdf(real_pdf_path)
        
        # Step 2: 부모-자식 관계 처리
        processed_items = process_toc_items(raw_toc_items)
        
        # Step 3: 페이지 범위 계산
        complete_items = calculate_page_ranges(processed_items)
        
        # Then: 전체 워크플로우 결과 검증
        assert len(complete_items) > 0, "최종 결과에 항목이 있어야 함"
        
        # 완전한 목차 항목 구조 검증
        complete_fields = ['id', 'title', 'level', 'page', 'parent_id', 'children_ids', 
                          'start_page', 'end_page', 'page_count']
        
        for item in complete_items:
            for field in complete_fields:
                assert field in item, f"완전한 목차 항목에 {field} 필드가 있어야 함"
        
        # 계층 구조 일관성 검증
        root_items = [item for item in complete_items if item['parent_id'] is None]
        assert len(root_items) > 0, "최상위 항목이 존재해야 함"
        
        # 레벨별 분포 검증
        level_counts = {}
        for item in complete_items:
            level = item['level']
            level_counts[level] = level_counts.get(level, 0) + 1
        
        assert len(level_counts) > 1, "여러 레벨의 계층 구조가 있어야 함"
        assert 0 in level_counts, "레벨 0 (최상위) 항목이 있어야 함"
        
        # 실제 완성된 전체 데이터를 클래스 변수로 저장 (다른 테스트에서 사용 가능)
        TestTocExtractorSocial.real_toc_data = complete_items
        
        # 기본 통계 정보 출력 (디버깅용)
        print(f"\n📊 실제 목차 추출 결과:")
        print(f"  - 총 항목 수: {len(complete_items)}")
        print(f"  - 계층 레벨: {len(level_counts)}단계")
        print(f"  - 최상위 항목: {len(root_items)}개")
        print(f"  - 레벨별 분포: {dict(sorted(level_counts.items()))}")