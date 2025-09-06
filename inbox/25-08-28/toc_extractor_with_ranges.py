"""
생성 시간: 2025-08-28 한국 시간
핵심 내용: PDF 북마크 추출 및 페이지 범위 계산을 통합한 목차 처리 도구
상세 내용:
    - import_libraries (9-15라인): 필요한 라이브러리 임포트
    - extract_bookmarks_correct (17-65라인): PyPDF2의 올바른 메서드로 북마크 추출
    - build_toc_hierarchy (67-120라인): 목차 계층 구조 및 관계 생성
    - calculate_page_ranges (122-165라인): 각 노드의 페이지 범위 계산
    - save_complete_toc (167-190라인): 완성된 목차 JSON으로 저장
    - validate_and_report (192-225라인): 결과 검증 및 리포트 생성
    - main (227-250라인): 전체 처리 실행 함수
상태: active
참조: 25-08-07의 방식 및 로직 적용
"""

import json
import os
import re
from datetime import datetime
from PyPDF2 import PdfReader
from typing import List, Dict, Any, Optional

def extract_bookmarks_correct(pdf_path: str) -> List[Dict]:
    """25-08-07 방식으로 올바른 페이지 번호와 함께 북마크 추출"""
    bookmarks = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            print(f"전체 페이지 수: {len(pdf_reader.pages)}")
            
            def process_outline(outline, level=0, parent_id=None):
                nonlocal bookmarks
                
                if isinstance(outline, list):
                    for item in outline:
                        process_outline(item, level, parent_id)
                else:
                    try:
                        title = outline.title.strip() if outline.title else "Unknown"
                        
                        # 올바른 페이지 번호 추출 방법
                        page = None
                        if hasattr(outline, 'page') and outline.page:
                            try:
                                # get_destination_page_number 메서드 사용
                                page = pdf_reader.get_destination_page_number(outline) + 1
                            except:
                                # 대안 방법들 시도
                                if hasattr(outline.page, 'idnum'):
                                    # 페이지 객체에서 실제 인덱스 찾기
                                    for i, pdf_page in enumerate(pdf_reader.pages):
                                        if hasattr(pdf_page, 'idnum') and pdf_page.idnum == outline.page.idnum:
                                            page = i + 1
                                            break
                        
                        current_id = len(bookmarks)
                        
                        bookmark_item = {
                            'id': current_id,
                            'title': title,
                            'level': level,
                            'page': page,
                            'parent_id': parent_id,
                            'children_ids': []
                        }
                        
                        bookmarks.append(bookmark_item)
                        
                        # 부모에 자식 ID 추가
                        if parent_id is not None:
                            bookmarks[parent_id]['children_ids'].append(current_id)
                        
                        # 하위 항목이 있는지 확인하고 처리
                        if hasattr(outline, 'node') and hasattr(outline.node, 'kids'):
                            for child_ref in outline.node.kids:
                                try:
                                    child = pdf_reader._get_object(child_ref)
                                    if hasattr(child, 'title'):
                                        process_outline(child, level + 1, current_id)
                                except:
                                    pass
                                    
                    except Exception as e:
                        print(f"북마크 항목 처리 오류: {e}")
            
            if pdf_reader.outline:
                print("북마크 발견, 추출 중...")
                process_outline(pdf_reader.outline)
            else:
                print("PDF에 북마크가 없습니다.")
                
    except Exception as e:
        print(f"PDF 북마크 추출 오류: {e}")
    
    return bookmarks

def build_toc_hierarchy(bookmarks: List[Dict]) -> List[Dict]:
    """목차 계층 구조 구성 및 정리"""
    if not bookmarks:
        return []
    
    # 유효한 페이지 번호가 있는 항목만 필터링
    valid_bookmarks = []
    for item in bookmarks:
        if item.get('page') and isinstance(item['page'], int) and item['page'] > 0:
            valid_bookmarks.append(item)
        else:
            print(f"무효한 페이지 번호 제외: {item['title']} (페이지: {item.get('page')})")
    
    # ID 재할당 (필터링으로 인한 빈 공간 제거)
    id_mapping = {}
    for new_id, item in enumerate(valid_bookmarks):
        old_id = item['id']
        id_mapping[old_id] = new_id
        item['id'] = new_id
    
    # parent_id와 children_ids 업데이트
    for item in valid_bookmarks:
        # parent_id 업데이트
        if item['parent_id'] is not None and item['parent_id'] in id_mapping:
            item['parent_id'] = id_mapping[item['parent_id']]
        else:
            item['parent_id'] = None
            
        # children_ids 업데이트
        new_children = []
        for child_id in item['children_ids']:
            if child_id in id_mapping:
                new_children.append(id_mapping[child_id])
        item['children_ids'] = new_children
    
    print(f"계층 구조 구성 완료: {len(valid_bookmarks)}개 유효한 항목")
    return valid_bookmarks

def calculate_page_ranges(toc_items: List[Dict]) -> List[Dict]:
    """각 노드의 페이지 범위 계산"""
    if not toc_items:
        return []
    
    # 페이지 번호로 정렬
    sorted_items = sorted(toc_items, key=lambda x: x['page'])
    
    enhanced_items = []
    
    for i, item in enumerate(sorted_items):
        enhanced_item = item.copy()
        
        start_page = item['page']
        
        # 다음 항목의 시작 페이지 찾기 (같은 레벨 이하의 항목들 중에서)
        end_page = None
        current_level = item['level']
        
        for j in range(i + 1, len(sorted_items)):
            next_item = sorted_items[j]
            next_level = next_item['level']
            
            # 다음 항목이 현재 항목보다 같은 레벨이거나 상위 레벨인 경우
            if next_level <= current_level:
                end_page = next_item['page'] - 1
                break
            # 하위 레벨이지만 큰 레벨 차이가 나는 경우 (다른 섹션으로 판단)
            elif next_level > current_level + 2:
                end_page = next_item['page'] - 1
                break
        
        # 마지막 항목이거나 적절한 끝 페이지를 찾지 못한 경우
        if end_page is None:
            # 기본값으로 다음 큰 섹션 시작 전까지 또는 문서 끝까지
            if i + 1 < len(sorted_items):
                # 다음 레벨 0 항목이 있다면 그 전까지
                for j in range(i + 1, len(sorted_items)):
                    if sorted_items[j]['level'] == 0:
                        end_page = sorted_items[j]['page'] - 1
                        break
                
                if end_page is None:
                    end_page = start_page + 10  # 기본값
            else:
                end_page = start_page + 5  # 마지막 항목의 기본값
        
        # 최소 1페이지는 보장
        if end_page < start_page:
            end_page = start_page
        
        enhanced_item.update({
            'start_page': start_page,
            'end_page': end_page,
            'page_count': end_page - start_page + 1
        })
        
        enhanced_items.append(enhanced_item)
    
    # 원래 순서로 다시 정렬 (ID 순)
    enhanced_items.sort(key=lambda x: x['id'])
    
    print(f"페이지 범위 계산 완료: {len(enhanced_items)}개 항목")
    return enhanced_items

def save_complete_toc(toc_data: List[Dict], output_path: str) -> bool:
    """완성된 목차를 JSON으로 저장"""
    try:
        complete_data = {
            "extraction_info": {
                "source_pdf": "2022_Data-Oriented Programming_Manning.pdf",
                "extraction_method": "PyPDF2 bookmarks with correct page numbers",
                "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                "total_items": len(toc_data)
            },
            "toc_structure": toc_data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, ensure_ascii=False, indent=2)
        
        print(f"완성된 목차 저장: {output_path}")
        return True
        
    except Exception as e:
        print(f"목차 저장 오류: {e}")
        return False

def validate_and_report(toc_data: List[Dict]):
    """결과 검증 및 상세 리포트"""
    if not toc_data:
        print("검증할 데이터가 없습니다.")
        return
    
    print("\n" + "="*60)
    print("📊 목차 추출 결과 검증 리포트")
    print("="*60)
    
    # 기본 통계
    total_items = len(toc_data)
    level_stats = {}
    page_issues = []
    
    for item in toc_data:
        level = item['level']
        if level not in level_stats:
            level_stats[level] = {'count': 0, 'total_pages': 0}
        
        level_stats[level]['count'] += 1
        level_stats[level]['total_pages'] += item.get('page_count', 0)
        
        # 페이지 관련 이슈 체크
        if item.get('page_count', 0) <= 0:
            page_issues.append(item)
    
    print(f"총 항목 수: {total_items}")
    print(f"페이지 범위 이슈: {len(page_issues)}개")
    
    print(f"\n레벨별 통계:")
    for level in sorted(level_stats.keys()):
        stats = level_stats[level]
        avg_pages = stats['total_pages'] / stats['count'] if stats['count'] > 0 else 0
        print(f"  Level {level}: {stats['count']}개 항목, 평균 {avg_pages:.1f}페이지")
    
    # 처음 10개 항목 미리보기
    print(f"\n목차 미리보기 (처음 10개):")
    for i, item in enumerate(toc_data[:10]):
        indent = "  " * item['level']
        page_range = f"({item['start_page']}-{item['end_page']}, {item['page_count']}p)"
        print(f"{i+1:2d}. {indent}{item['title'][:50]}... {page_range}")
    
    if len(toc_data) > 10:
        print(f"    ... 그리고 {len(toc_data) - 10}개 더")

def main():
    pdf_path = '/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28'
    output_file = os.path.join(output_dir, 'complete_toc_with_ranges.json')
    
    if not os.path.exists(pdf_path):
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print("🚀 통합 목차 추출 및 페이지 범위 계산 시작")
    print(f"📖 대상 PDF: {os.path.basename(pdf_path)}")
    
    # 1단계: 북마크 추출 (올바른 페이지 번호)
    print("\n1️⃣ 북마크에서 목차 추출 중...")
    bookmarks = extract_bookmarks_correct(pdf_path)
    print(f"추출된 북마크: {len(bookmarks)}개")
    
    if not bookmarks:
        print("❌ 북마크 추출 실패")
        return
    
    # 2단계: 계층 구조 정리
    print("\n2️⃣ 계층 구조 구성 중...")
    structured_toc = build_toc_hierarchy(bookmarks)
    
    if not structured_toc:
        print("❌ 계층 구조 구성 실패")
        return
    
    # 3단계: 페이지 범위 계산
    print("\n3️⃣ 페이지 범위 계산 중...")
    complete_toc = calculate_page_ranges(structured_toc)
    
    # 4단계: 결과 저장
    print("\n4️⃣ 결과 저장 중...")
    if save_complete_toc(complete_toc, output_file):
        # 5단계: 검증 및 리포트
        validate_and_report(complete_toc)
        print(f"\n✅ 작업 완료! 결과 파일: {output_file}")
    else:
        print("❌ 결과 저장 실패")

if __name__ == "__main__":
    main()