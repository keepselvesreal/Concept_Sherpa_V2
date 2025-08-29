"""
생성 시간: 2025-08-29 15:42:36 KST
핵심 내용: PDF 내용 분석을 통한 계층 구조 추론 목차 추출 도구
상세 내용:
    - import_libraries (17-24라인): 필요한 라이브러리 임포트
    - extract_bookmarks_basic (26-80라인): 기본 북마크 추출
    - infer_hierarchy_from_titles (82-160라인): 제목 패턴 분석으로 계층 구조 추론
    - build_complete_hierarchy (162-220라인): 완전한 계층 구조 구성
    - calculate_page_ranges (222-285라인): 각 노드의 페이지 범위 계산
    - save_complete_toc (287-315라인): 완성된 목차 JSON으로 저장
    - validate_and_report (317-375라인): 결과 검증 및 리포트 생성
    - main (377-415라인): 전체 처리 실행 함수
상태: active
참조: 25-08-28 원본에서 내용 기반 계층 추론 로직 추가
"""

import json
import os
import re
from datetime import datetime
from PyPDF2 import PdfReader
from typing import List, Dict, Any, Optional

def extract_bookmarks_basic(pdf_path: str) -> List[Dict]:
    """기본 북마크 추출 (계층 정보 없이)"""
    bookmarks = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            print(f"전체 페이지 수: {len(pdf_reader.pages)}")
            
            def collect_outline_items(outline_items):
                """모든 아웃라인 항목을 평면적으로 수집"""
                items = []
                if not outline_items:
                    return items
                
                for item in outline_items:
                    try:
                        title = item.title.strip() if hasattr(item, 'title') and item.title else "Unknown"
                        page = None
                        
                        if hasattr(item, 'page') and item.page:
                            try:
                                page = pdf_reader.get_destination_page_number(item) + 1
                            except:
                                try:
                                    if hasattr(item.page, 'idnum'):
                                        for i, pdf_page in enumerate(pdf_reader.pages):
                                            if hasattr(pdf_page, 'idnum') and pdf_page.idnum == item.page.idnum:
                                                page = i + 1
                                                break
                                except:
                                    pass
                        
                        if page and title:
                            items.append({
                                'title': title,
                                'page': page
                            })
                            
                        # 하위 항목도 수집
                        if hasattr(item, 'node') and hasattr(item.node, 'kids'):
                            for child_ref in item.node.kids:
                                try:
                                    child_obj = pdf_reader._get_object(child_ref)
                                    if hasattr(child_obj, 'title'):
                                        items.extend(collect_outline_items([child_obj]))
                                except:
                                    pass
                                    
                    except Exception as e:
                        print(f"북마크 항목 처리 오류: {e}")
                
                return items
            
            if pdf_reader.outline:
                print("북마크 발견, 수집 중...")
                raw_items = collect_outline_items(pdf_reader.outline)
                
                # ID 할당하고 정렬
                for i, item in enumerate(sorted(raw_items, key=lambda x: x['page'])):
                    bookmarks.append({
                        'id': i,
                        'title': item['title'],
                        'page': item['page'],
                        'level': 0,  # 기본값, 나중에 추론
                        'parent_id': None,
                        'children_ids': []
                    })
            else:
                print("PDF에 북마크가 없습니다.")
                
    except Exception as e:
        print(f"PDF 북마크 추출 오류: {e}")
    
    return bookmarks

def infer_hierarchy_from_titles(bookmarks: List[Dict]) -> List[Dict]:
    """제목 패턴 분석을 통한 계층 구조 추론"""
    if not bookmarks:
        return []
    
    print("\n🔍 제목 패턴 분석을 통한 계층 구조 추론...")
    
    for item in bookmarks:
        title = item['title']
        level = 0
        
        # 패턴 1: 장/절 번호 패턴
        # "1 Complexity of object-oriented programming" → Level 1
        # "1.1 OOP design: Classic or classical?" → Level 2  
        # "1.1.1 The design phase" → Level 3
        chapter_match = re.match(r'^(\d+(?:\.\d+)*)', title)
        if chapter_match:
            number_part = chapter_match.group(1)
            dots_count = number_part.count('.')
            level = dots_count + 1
        
        # 패턴 2: Part 패턴
        elif re.match(r'^Part\s+\d+', title, re.IGNORECASE):
            level = 0  # 최상위
        
        # 패턴 3: Appendix 패턴
        elif re.match(r'^Appendix\s+[A-Z]', title, re.IGNORECASE):
            level = 0  # 최상위
        
        # 패턴 4: 서문, 목차 등
        elif title.lower() in ['forewords', 'preface', 'acknowledgments', 'about this book', 
                              'about the author', 'about the cover illustration', 'dramatis personae',
                              'brief contents', 'contents', 'index']:
            level = 0  # 최상위
        
        # 패턴 5: Summary 패턴
        elif title.lower() == 'summary':
            level = 1  # 장 내의 요약
        
        # 패턴 6: 기타 섹션 제목들
        elif re.match(r'^[A-Z]\.', title):  # "A.1", "B.2" 등
            parts = title.split('.')
            if len(parts) >= 2:
                level = len(parts) - 1
            else:
                level = 1
        
        # 패턴 7: 들여쓰기 기반 추론 (제목 길이와 내용으로)
        if level == 0 and not re.match(r'^(Part|Appendix)', title, re.IGNORECASE):
            # 짧은 제목이고 일반적인 단어들 → 상위 레벨 가능성
            if len(title.split()) <= 3 and not any(word in title.lower() for word in ['the', 'and', 'with', 'for']):
                level = 1
            else:
                # 긴 제목 → 하위 레벨 가능성
                level = 2
        
        item['level'] = level
        print(f"Level {level}: {title}")
    
    return bookmarks

def build_complete_hierarchy(bookmarks: List[Dict]) -> List[Dict]:
    """완전한 부모-자식 관계 구성"""
    if not bookmarks:
        return []
    
    print(f"\n👥 부모-자식 관계 구성...")
    
    # 레벨별 통계
    level_stats = {}
    for item in bookmarks:
        level = item['level']
        level_stats[level] = level_stats.get(level, 0) + 1
    
    print("레벨별 항목 수:")
    for level in sorted(level_stats.keys()):
        print(f"  Level {level}: {level_stats[level]}개")
    
    # 부모-자식 관계 설정
    for i, item in enumerate(bookmarks):
        current_level = item['level']
        
        # 부모 찾기: 이전 항목들 중 레벨이 정확히 하나 낮은 가장 가까운 항목
        parent_id = None
        for j in range(i - 1, -1, -1):
            if bookmarks[j]['level'] == current_level - 1:
                parent_id = bookmarks[j]['id']
                break
        
        item['parent_id'] = parent_id
        
        # 부모의 자식 리스트에 추가
        if parent_id is not None:
            bookmarks[parent_id]['children_ids'].append(item['id'])
    
    return bookmarks

def calculate_page_ranges(toc_items: List[Dict]) -> List[Dict]:
    """각 노드의 페이지 범위 계산 (계층 구조 고려)"""
    if not toc_items:
        return []
    
    enhanced_items = []
    
    for i, item in enumerate(toc_items):
        enhanced_item = item.copy()
        start_page = item['page']
        current_level = item['level']
        
        # 끝 페이지 찾기
        end_page = None
        
        # 다음 항목들을 검사하여 적절한 종료점 찾기
        for j in range(i + 1, len(toc_items)):
            next_item = toc_items[j]
            next_level = next_item['level']
            
            # 같은 레벨이거나 상위 레벨인 경우 → 현재 섹션 종료
            if next_level <= current_level:
                end_page = next_item['page'] - 1
                break
        
        # 끝 페이지를 찾지 못한 경우 기본값 설정
        if end_page is None:
            if current_level == 0:  # 최상위 레벨
                end_page = start_page + 30  # 넉넉하게
            elif current_level == 1:  # 챕터 레벨
                end_page = start_page + 15
            else:  # 하위 섹션
                end_page = start_page + 5
            
            # 마지막 항목인 경우 더 보수적으로
            if i == len(toc_items) - 1:
                end_page = start_page + 3
        
        # 최소 1페이지 보장
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
                "extraction_method": "Title pattern analysis with hierarchy inference",
                "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                "total_items": len(toc_data),
                "note": "Hierarchy levels inferred from title patterns (chapter numbers, sections, etc.)"
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
    print("📊 내용 기반 계층 구조 추론 결과 리포트")
    print("="*70)
    
    # 레벨별 통계 및 샘플
    level_stats = {}
    for item in toc_data:
        level = item['level']
        if level not in level_stats:
            level_stats[level] = {'count': 0, 'items': []}
        level_stats[level]['count'] += 1
        level_stats[level]['items'].append(item)
    
    print(f"총 항목 수: {len(toc_data)}")
    print(f"계층 분포:")
    for level in sorted(level_stats.keys()):
        count = level_stats[level]['count']
        percentage = (count / len(toc_data)) * 100
        print(f"  Level {level}: {count}개 ({percentage:.1f}%)")
    
    # 계층별 상세 샘플
    print(f"\n📋 계층별 상세 구조:")
    for level in sorted(level_stats.keys())[:5]:  # 처음 5개 레벨
        items = level_stats[level]['items'][:5]  # 각 레벨에서 처음 5개
        print(f"\n  📂 Level {level} ({level_stats[level]['count']}개 항목):")
        for item in items:
            indent = "    " + "  " * level
            page_info = f"[p.{item['start_page']}-{item['end_page']}]"
            children = f"({len(item['children_ids'])}개 하위)" if item['children_ids'] else ""
            print(f"{indent}• {item['title'][:60]}... {page_info} {children}")
        
        if len(level_stats[level]['items']) > 5:
            remaining = len(level_stats[level]['items']) - 5
            print(f"      ... 그리고 {remaining}개 더")
    
    # 부모-자식 관계 검증
    hierarchy_issues = []
    for item in toc_data:
        if item['parent_id'] is not None:
            parent = next((x for x in toc_data if x['id'] == item['parent_id']), None)
            if not parent:
                hierarchy_issues.append(f"항목 {item['id']}의 부모 {item['parent_id']}를 찾을 수 없음")
    
    if hierarchy_issues:
        print(f"\n⚠️  계층 구조 이슈 ({len(hierarchy_issues)}개):")
        for issue in hierarchy_issues[:5]:
            print(f"    - {issue}")
    else:
        print(f"\n✅ 계층 구조 검증 완료 - 문제없음")

def main():
    pdf_path = '/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29'
    output_file = os.path.join(output_dir, 'complete_toc_content_based.json')
    
    if not os.path.exists(pdf_path):
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 내용 기반 계층 구조 추론 목차 추출 시작")
    print(f"📖 대상 PDF: {os.path.basename(pdf_path)}")
    
    # 1단계: 기본 북마크 추출
    print("\n1️⃣ 기본 북마크 추출 중...")
    bookmarks = extract_bookmarks_basic(pdf_path)
    
    if not bookmarks:
        print("❌ 북마크 추출 실패")
        return
    
    # 2단계: 제목 패턴으로 계층 구조 추론
    print("\n2️⃣ 제목 패턴 분석으로 계층 추론...")
    inferred_bookmarks = infer_hierarchy_from_titles(bookmarks)
    
    # 3단계: 완전한 계층 구조 구성
    print("\n3️⃣ 완전한 계층 구조 구성...")
    structured_toc = build_complete_hierarchy(inferred_bookmarks)
    
    # 4단계: 페이지 범위 계산
    print("\n4️⃣ 페이지 범위 계산...")
    complete_toc = calculate_page_ranges(structured_toc)
    
    # 5단계: 결과 저장
    print("\n5️⃣ 결과 저장...")
    if save_complete_toc(complete_toc, output_file):
        validate_and_report(complete_toc)
        print(f"\n✅ 작업 완료! 결과 파일: {output_file}")
    else:
        print("❌ 결과 저장 실패")

if __name__ == "__main__":
    main()