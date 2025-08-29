"""
생성 시간: 2025-08-29 15:42:36 KST
핵심 내용: PDF 북마크에서 올바른 계층 구조를 추출하는 수정된 목차 처리 도구
상세 내용:
    - import_libraries (17-23라인): 필요한 라이브러리 임포트
    - extract_bookmarks_with_levels (25-95라인): 올바른 계층 구조로 북마크 추출
    - build_toc_hierarchy (97-155라인): 목차 계층 구조 및 관계 생성
    - calculate_page_ranges (157-225라인): 각 노드의 페이지 범위 계산
    - save_complete_toc (227-255라인): 완성된 목차 JSON으로 저장
    - validate_and_report (257-305라인): 결과 검증 및 리포트 생성
    - main (307-345라인): 전체 처리 실행 함수
상태: active
참조: 25-08-28/toc_extractor_with_ranges.py 수정본
"""

import json
import os
import re
from datetime import datetime
from PyPDF2 import PdfReader
from typing import List, Dict, Any, Optional

def extract_bookmarks_with_levels(pdf_path: str) -> List[Dict]:
    """북마크의 실제 계층 구조를 올바르게 추출"""
    bookmarks = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            print(f"전체 페이지 수: {len(pdf_reader.pages)}")
            
            def process_outline_recursive(outline_items, current_level=0):
                """재귀적으로 아웃라인 처리하여 올바른 레벨 할당"""
                if not outline_items:
                    return
                    
                for item in outline_items:
                    try:
                        # 제목 처리
                        title = item.title.strip() if hasattr(item, 'title') and item.title else "Unknown"
                        
                        # 페이지 번호 추출
                        page = None
                        if hasattr(item, 'page') and item.page:
                            try:
                                # get_destination_page_number 메서드 사용
                                page = pdf_reader.get_destination_page_number(item) + 1
                            except Exception as e:
                                print(f"페이지 번호 추출 오류 ({title}): {e}")
                                # 대안 방법들
                                try:
                                    if hasattr(item.page, 'idnum'):
                                        for i, pdf_page in enumerate(pdf_reader.pages):
                                            if hasattr(pdf_page, 'idnum') and pdf_page.idnum == item.page.idnum:
                                                page = i + 1
                                                break
                                except:
                                    pass
                        
                        if page:  # 유효한 페이지가 있을 때만 추가
                            current_id = len(bookmarks)
                            
                            bookmark_item = {
                                'id': current_id,
                                'title': title,
                                'level': current_level,  # 현재 레벨 사용
                                'page': page,
                                'parent_id': None,  # 나중에 설정
                                'children_ids': []
                            }
                            
                            bookmarks.append(bookmark_item)
                            print(f"Level {current_level}: {title} (page {page})")
                            
                            # 하위 항목이 있으면 재귀 처리
                            if hasattr(item, 'node') and hasattr(item.node, 'kids') and item.node.kids:
                                child_outline_items = []
                                for child_ref in item.node.kids:
                                    try:
                                        child_obj = pdf_reader._get_object(child_ref)
                                        if hasattr(child_obj, 'title'):
                                            child_outline_items.append(child_obj)
                                    except:
                                        pass
                                
                                if child_outline_items:
                                    process_outline_recursive(child_outline_items, current_level + 1)
                        
                    except Exception as e:
                        print(f"북마크 항목 처리 오류: {e}")
            
            if pdf_reader.outline:
                print("북마크 발견, 계층 구조 추출 중...")
                process_outline_recursive(pdf_reader.outline, 0)
            else:
                print("PDF에 북마크가 없습니다.")
                
    except Exception as e:
        print(f"PDF 북마크 추출 오류: {e}")
    
    return bookmarks

def build_toc_hierarchy(bookmarks: List[Dict]) -> List[Dict]:
    """목차 계층 구조 구성 및 부모-자식 관계 설정"""
    if not bookmarks:
        return []
    
    print(f"\n계층 구조 분석:")
    level_count = {}
    for item in bookmarks:
        level = item['level']
        level_count[level] = level_count.get(level, 0) + 1
        
    for level in sorted(level_count.keys()):
        print(f"  Level {level}: {level_count[level]}개 항목")
    
    # 부모-자식 관계 설정
    for i, item in enumerate(bookmarks):
        current_level = item['level']
        
        # 부모 찾기 (이전 항목들 중에서 레벨이 하나 낮은 가장 가까운 항목)
        parent_id = None
        for j in range(i - 1, -1, -1):
            if bookmarks[j]['level'] == current_level - 1:
                parent_id = bookmarks[j]['id']
                break
        
        item['parent_id'] = parent_id
        
        # 부모의 자식 리스트에 추가
        if parent_id is not None:
            bookmarks[parent_id]['children_ids'].append(item['id'])
    
    print(f"계층 구조 구성 완료: {len(bookmarks)}개 항목")
    return bookmarks

def calculate_page_ranges(toc_items: List[Dict]) -> List[Dict]:
    """각 노드의 페이지 범위 계산 (레벨 기반 로직 개선)"""
    if not toc_items:
        return []
    
    enhanced_items = []
    
    for i, item in enumerate(toc_items):
        enhanced_item = item.copy()
        start_page = item['page']
        current_level = item['level']
        
        # 끝 페이지 찾기 로직 개선
        end_page = None
        
        # 다음 항목들 중에서 적절한 종료점 찾기
        for j in range(i + 1, len(toc_items)):
            next_item = toc_items[j]
            next_level = next_item['level']
            
            # 같은 레벨이거나 상위 레벨인 경우 → 현재 섹션 종료
            if next_level <= current_level:
                end_page = next_item['page'] - 1
                break
            
            # 하위 레벨이지만 너무 큰 차이가 나면 → 다른 큰 섹션으로 판단
            if current_level == 0 and next_level == 0:  # 같은 최상위 레벨
                end_page = next_item['page'] - 1
                break
        
        # 적절한 끝 페이지를 찾지 못한 경우
        if end_page is None:
            if current_level == 0:  # 최상위 레벨
                # 다음 최상위 레벨까지 또는 기본값
                end_page = start_page + 20
            else:
                # 하위 레벨은 보수적으로
                end_page = start_page + 5
            
            # 문서 끝에 가까운 경우 조정
            if i == len(toc_items) - 1:
                end_page = start_page + 2
        
        # 최소 페이지 보장
        if end_page < start_page:
            end_page = start_page
        
        enhanced_item.update({
            'start_page': start_page,
            'end_page': end_page,
            'page_count': end_page - start_page + 1
        })
        
        enhanced_items.append(enhanced_item)
    
    print(f"페이지 범위 계산 완료: {len(enhanced_items)}개 항목")
    return enhanced_items

def save_complete_toc(toc_data: List[Dict], output_path: str) -> bool:
    """완성된 목차를 JSON으로 저장"""
    try:
        complete_data = {
            "extraction_info": {
                "source_pdf": "2022_Data-Oriented Programming_Manning.pdf",
                "extraction_method": "PyPDF2 bookmarks with correct hierarchy levels",
                "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                "total_items": len(toc_data),
                "note": "Fixed level calculation to properly reflect bookmark hierarchy"
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
    
    print("\n" + "="*70)
    print("📊 수정된 목차 추출 결과 검증 리포트")
    print("="*70)
    
    # 레벨별 통계
    level_stats = {}
    for item in toc_data:
        level = item['level']
        if level not in level_stats:
            level_stats[level] = {'count': 0, 'items': []}
        level_stats[level]['count'] += 1
        level_stats[level]['items'].append(item)
    
    print(f"총 항목 수: {len(toc_data)}")
    print(f"레벨 분포:")
    for level in sorted(level_stats.keys()):
        count = level_stats[level]['count']
        print(f"  Level {level}: {count}개 항목")
    
    # 각 레벨별 샘플 표시
    print(f"\n레벨별 샘플:")
    for level in sorted(level_stats.keys())[:4]:  # 처음 4개 레벨만
        items = level_stats[level]['items'][:3]  # 각 레벨에서 처음 3개만
        print(f"  Level {level} 샘플:")
        for item in items:
            indent = "    " + "  " * level
            page_info = f"(p.{item['page']}, {item['page_count']}페이지)"
            print(f"{indent}- {item['title'][:50]}... {page_info}")
        
        if len(level_stats[level]['items']) > 3:
            print(f"    ... 그리고 {len(level_stats[level]['items']) - 3}개 더")
        print()

def main():
    pdf_path = '/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29'
    output_file = os.path.join(output_dir, 'complete_toc_with_fixed_levels.json')
    
    if not os.path.exists(pdf_path):
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 수정된 계층 구조 목차 추출 시작")
    print(f"📖 대상 PDF: {os.path.basename(pdf_path)}")
    
    # 1단계: 북마크 추출 (올바른 계층 구조)
    print("\n1️⃣ 계층 구조를 포함한 북마크 추출 중...")
    bookmarks = extract_bookmarks_with_levels(pdf_path)
    
    if not bookmarks:
        print("❌ 북마크 추출 실패")
        return
    
    # 2단계: 부모-자식 관계 설정
    print("\n2️⃣ 부모-자식 관계 설정 중...")
    structured_toc = build_toc_hierarchy(bookmarks)
    
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