"""
생성 시간: 2025-08-29 15:42:36 KST
핵심 내용: PyMuPDF를 사용한 완전한 계층 구조 목차 추출 도구
상세 내용:
    - import_libraries (17-24라인): 필요한 라이브러리 임포트
    - extract_toc_with_pymupdf (26-95라인): PyMuPDF로 완전한 목차 구조 추출
    - process_toc_items (97-150라인): 목차 항목 처리 및 정리
    - calculate_page_ranges (152-210라인): 각 노드의 페이지 범위 계산
    - save_complete_toc (212-240라인): 완성된 목차 JSON으로 저장
    - validate_and_report (242-310라인): 결과 검증 및 리포트 생성
    - main (312-350라인): 전체 처리 실행 함수
상태: active
참조: PyMuPDF 라이브러리 활용으로 완전한 목차 추출
"""

import json
import os
import fitz  # PyMuPDF
from datetime import datetime
from typing import List, Dict, Any, Optional

def extract_toc_with_pymupdf(pdf_path: str) -> List[Dict]:
    """PyMuPDF를 사용하여 완전한 목차 구조 추출"""
    toc_items = []
    
    try:
        # PDF 열기
        doc = fitz.open(pdf_path)
        print(f"전체 페이지 수: {doc.page_count}")
        
        # 목차(Table of Contents) 추출
        toc = doc.get_toc(simple=False)  # simple=False로 완전한 정보 가져오기
        print(f"발견된 TOC 항목: {len(toc)}개")
        
        if not toc:
            print("❌ PDF에서 목차 정보를 찾을 수 없습니다.")
            doc.close()
            return []
        
        # TOC 항목 처리
        for i, item in enumerate(toc):
            try:
                # PyMuPDF TOC 형식: [level, title, page, destination_dict]
                if len(item) >= 3:
                    level = item[0] - 1  # PyMuPDF는 1부터 시작하므로 0부터 시작하도록 조정
                    title = item[1].strip()
                    page = item[2]  # PyMuPDF는 이미 1부터 시작하는 페이지 번호
                    
                    # 유효성 검사
                    if title and page > 0:
                        toc_item = {
                            'id': i,
                            'title': title,
                            'level': max(0, level),  # 음수 레벨 방지
                            'page': page,
                            'parent_id': None,  # 나중에 설정
                            'children_ids': []
                        }
                        
                        toc_items.append(toc_item)
                        print(f"Level {level}: {title} (page {page})")
                    
            except Exception as e:
                print(f"TOC 항목 {i} 처리 오류: {e}")
                continue
        
        doc.close()
        
    except Exception as e:
        print(f"PDF 처리 오류: {e}")
        return []
    
    return toc_items

def process_toc_items(toc_items: List[Dict]) -> List[Dict]:
    """목차 항목 처리 및 부모-자식 관계 설정"""
    if not toc_items:
        return []
    
    print(f"\n🔧 목차 항목 처리 및 관계 설정...")
    
    # 레벨별 통계
    level_stats = {}
    for item in toc_items:
        level = item['level']
        level_stats[level] = level_stats.get(level, 0) + 1
    
    print("추출된 레벨별 통계:")
    for level in sorted(level_stats.keys()):
        print(f"  Level {level}: {level_stats[level]}개 항목")
    
    # 부모-자식 관계 설정
    for i, item in enumerate(toc_items):
        current_level = item['level']
        
        # 부모 찾기: 이전 항목들 중 레벨이 정확히 하나 낮은 가장 가까운 항목
        parent_id = None
        for j in range(i - 1, -1, -1):
            if toc_items[j]['level'] == current_level - 1:
                parent_id = toc_items[j]['id']
                break
        
        item['parent_id'] = parent_id
        
        # 부모의 자식 리스트에 추가
        if parent_id is not None:
            toc_items[parent_id]['children_ids'].append(item['id'])
    
    # 계층 구조 검증
    root_items = [item for item in toc_items if item['parent_id'] is None]
    print(f"최상위 항목: {len(root_items)}개")
    
    return toc_items

def calculate_page_ranges(toc_items: List[Dict]) -> List[Dict]:
    """각 노드의 페이지 범위 계산 (개선된 로직)"""
    if not toc_items:
        return []
    
    print(f"\n📊 페이지 범위 계산...")
    enhanced_items = []
    
    for i, item in enumerate(toc_items):
        enhanced_item = item.copy()
        start_page = item['page']
        current_level = item['level']
        
        # 끝 페이지 찾기 로직
        end_page = None
        
        # 다음 항목들 검사
        for j in range(i + 1, len(toc_items)):
            next_item = toc_items[j]
            next_level = next_item['level']
            
            # 같은 레벨이거나 상위 레벨인 경우 → 현재 섹션 종료
            if next_level <= current_level:
                end_page = next_item['page'] - 1
                break
        
        # 적절한 끝 페이지를 찾지 못한 경우 기본값 설정
        if end_page is None:
            # 레벨에 따른 기본 페이지 수
            if current_level == 0:  # Part, Appendix 등
                end_page = start_page + 50
            elif current_level == 1:  # Chapter
                end_page = start_page + 25
            elif current_level == 2:  # Section
                end_page = start_page + 8
            else:  # Subsection
                end_page = start_page + 3
            
            # 마지막 항목인 경우 더 보수적으로
            if i == len(toc_items) - 1:
                end_page = start_page + 2
        
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
                "extraction_method": "PyMuPDF complete TOC extraction with hierarchy",
                "extraction_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S KST'),
                "total_items": len(toc_data),
                "note": "Complete hierarchy extracted using PyMuPDF library"
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
    
    print("\n" + "="*80)
    print("📊 PyMuPDF 기반 완전한 목차 추출 결과 리포트")
    print("="*80)
    
    # 레벨별 통계
    level_stats = {}
    for item in toc_data:
        level = item['level']
        if level not in level_stats:
            level_stats[level] = {'count': 0, 'items': []}
        level_stats[level]['count'] += 1
        level_stats[level]['items'].append(item)
    
    print(f"총 항목 수: {len(toc_data)}")
    print(f"최대 계층 깊이: {max(level_stats.keys()) + 1}")
    print(f"\n계층별 분포:")
    for level in sorted(level_stats.keys()):
        count = level_stats[level]['count']
        percentage = (count / len(toc_data)) * 100
        print(f"  Level {level}: {count}개 ({percentage:.1f}%)")
    
    # 각 레벨별 상세 내용
    print(f"\n📖 계층별 상세 구조 (상위 5개 레벨):")
    for level in sorted(level_stats.keys())[:5]:
        items = level_stats[level]['items'][:8]  # 각 레벨에서 처음 8개
        print(f"\n  🔷 Level {level} - {level_stats[level]['count']}개 항목:")
        
        for item in items:
            indent = "    " + "  " * level
            page_info = f"[{item['start_page']}-{item['end_page']}]"
            children_info = f"({len(item['children_ids'])}개 하위)" if item['children_ids'] else ""
            title_display = item['title'][:70] + "..." if len(item['title']) > 70 else item['title']
            print(f"{indent}• {title_display} {page_info} {children_info}")
        
        if len(level_stats[level]['items']) > 8:
            remaining = len(level_stats[level]['items']) - 8
            print(f"      {' ' * (level * 2)}... 그리고 {remaining}개 더")
    
    # 검증 요약
    total_pages = sum(item['page_count'] for item in toc_data)
    avg_pages = total_pages / len(toc_data) if toc_data else 0
    
    print(f"\n📈 요약 통계:")
    print(f"  • 총 커버 페이지 수: {total_pages}")
    print(f"  • 항목당 평균 페이지: {avg_pages:.1f}")
    print(f"  • 최대 섹션 크기: {max(item['page_count'] for item in toc_data)}페이지")
    print(f"  • 최소 섹션 크기: {min(item['page_count'] for item in toc_data)}페이지")

def main():
    pdf_path = '/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29'
    output_file = os.path.join(output_dir, 'complete_toc_pymupdf.json')
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 PyMuPDF를 사용한 완전한 목차 추출 시작")
    print(f"📖 대상 PDF: {os.path.basename(pdf_path)}")
    
    # 1단계: PyMuPDF로 목차 추출
    print("\n1️⃣ PyMuPDF로 완전한 목차 추출...")
    toc_items = extract_toc_with_pymupdf(pdf_path)
    
    if not toc_items:
        print("❌ 목차 추출 실패")
        return
    
    # 2단계: 목차 항목 처리
    print("\n2️⃣ 목차 항목 처리 및 관계 설정...")
    processed_toc = process_toc_items(toc_items)
    
    # 3단계: 페이지 범위 계산
    print("\n3️⃣ 페이지 범위 계산...")
    complete_toc = calculate_page_ranges(processed_toc)
    
    # 4단계: 결과 저장 및 검증
    print("\n4️⃣ 결과 저장...")
    if save_complete_toc(complete_toc, output_file):
        validate_and_report(complete_toc)
        print(f"\n✅ 모든 작업 완료! 결과: {output_file}")
    else:
        print("❌ 결과 저장 실패")

if __name__ == "__main__":
    main()