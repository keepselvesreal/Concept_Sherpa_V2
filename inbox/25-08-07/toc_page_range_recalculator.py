#!/usr/bin/env python3
"""
TOC JSON의 페이지 범위를 재계산하는 스크립트
각 노드의 실제 내용 범위 = 해당 노드 title부터 다음 형제 노드 직전까지
"""

import json
import os
from datetime import datetime

def load_toc_json(json_path: str) -> list:
    """JSON 목차 파일 로드"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
            print(f"✅ JSON 목차 로드 완료: {len(toc_data)} 개 항목")
            return toc_data
    except Exception as e:
        print(f"❌ JSON 목차 로드 실패: {e}")
        return []

def find_next_content_start(toc_data: list, current_index: int) -> int:
    """
    현재 노드의 실제 끝 페이지를 찾기 위해 바로 다음에 나오는 모든 노드를 확인
    - 바로 다음 노드(하위 레벨 포함)의 시작 페이지를 반환
    - 이렇게 해야 각 노드가 자신의 title부터 다음 노드 직전까지의 실제 내용만 가짐
    """
    # 바로 다음 노드가 있으면 그 시작 페이지 반환
    if current_index + 1 < len(toc_data):
        return toc_data[current_index + 1]['start_page']
    
    # 마지막 노드인 경우 None 반환
    return None

def recalculate_page_ranges(toc_data: list) -> list:
    """
    각 노드의 실제 페이지 범위를 재계산
    """
    enhanced_toc = []
    
    for i, item in enumerate(toc_data):
        # 기본 항목 복사
        enhanced_item = item.copy()
        
        # 시작 페이지는 기존 그대로
        actual_start = item['start_page']
        
        # 바로 다음 노드의 시작 페이지 찾기
        next_start_page = find_next_content_start(toc_data, i)
        
        # 끝 페이지 계산
        if next_start_page is not None:
            actual_end = next_start_page - 1
        else:
            # 마지막 노드인 경우 기존 end_page 사용
            actual_end = item['end_page']
        
        # 실제 페이지 수 계산
        actual_page_count = actual_end - actual_start + 1
        
        # 새 필드 추가
        enhanced_item['actual_start_page'] = actual_start
        enhanced_item['actual_end_page'] = actual_end
        enhanced_item['actual_page_count'] = actual_page_count
        
        enhanced_toc.append(enhanced_item)
    
    return enhanced_toc

def validate_results(enhanced_data: list):
    """
    결과 검증 및 통계 출력
    """
    print("\n📊 페이지 범위 재계산 결과 검증:")
    
    # 기본 통계
    total_items = len(enhanced_data)
    zero_page_items = []
    negative_page_items = []
    
    for item in enhanced_data:
        if item['actual_page_count'] <= 0:
            if item['actual_page_count'] == 0:
                zero_page_items.append(item)
            else:
                negative_page_items.append(item)
    
    print(f"✅ 총 항목 수: {total_items}")
    print(f"⚠️ 페이지 수가 0인 항목: {len(zero_page_items)}")
    print(f"❌ 페이지 수가 음수인 항목: {len(negative_page_items)}")
    
    # 문제가 있는 항목 출력
    if zero_page_items:
        print("\n🔍 페이지 수가 0인 항목들:")
        for item in zero_page_items:
            print(f"  - ID {item['id']}: {item['title']} (페이지 {item['actual_start_page']}-{item['actual_end_page']})")
    
    if negative_page_items:
        print("\n🚨 페이지 수가 음수인 항목들:")
        for item in negative_page_items:
            print(f"  - ID {item['id']}: {item['title']} (페이지 {item['actual_start_page']}-{item['actual_end_page']})")
    
    # 레벨별 통계
    level_stats = {}
    for item in enhanced_data:
        level = item['level']
        if level not in level_stats:
            level_stats[level] = {
                'count': 0,
                'total_pages': 0,
                'avg_pages': 0
            }
        
        level_stats[level]['count'] += 1
        level_stats[level]['total_pages'] += item['actual_page_count']
    
    print(f"\n📈 레벨별 통계:")
    for level, stats in sorted(level_stats.items()):
        avg_pages = stats['total_pages'] / stats['count'] if stats['count'] > 0 else 0
        print(f"  Level {level}: {stats['count']}개 항목, 평균 {avg_pages:.1f} 페이지")

def save_enhanced_json(enhanced_data: list, output_path: str):
    """업데이트된 JSON을 저장"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 페이지 범위 재계산된 JSON 저장 완료: {output_path}")
        
    except Exception as e:
        print(f"❌ JSON 저장 실패: {e}")

def main():
    """메인 실행 함수"""
    print("🚀 TOC 페이지 범위 재계산 시작...")
    
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07"
    input_json = os.path.join(base_dir, "enhanced_toc_with_relationships.json")
    output_json = os.path.join(base_dir, "toc_with_actual_ranges.json")
    
    # 1. JSON 데이터 로드
    print("\n📚 JSON 데이터 로드 중...")
    toc_data = load_toc_json(input_json)
    
    if not toc_data:
        print("❌ JSON 데이터 로드 실패로 작업 중단")
        return
    
    # 2. 페이지 범위 재계산
    print("\n🔄 페이지 범위 재계산 중...")
    enhanced_data = recalculate_page_ranges(toc_data)
    
    # 3. 결과 검증
    validate_results(enhanced_data)
    
    # 4. 결과 저장
    print("\n💾 결과 저장 중...")
    save_enhanced_json(enhanced_data, output_json)
    
    print(f"\n🎉 작업 완료!")
    print(f"📁 입력 파일: {input_json}")
    print(f"📁 출력 파일: {output_json}")
    
    # 몇 가지 예시 출력
    print(f"\n📋 처음 5개 항목의 페이지 범위 비교:")
    for i, item in enumerate(enhanced_data[:5]):
        original_range = f"{item['start_page']}-{item['end_page']} ({item['page_count']}p)"
        actual_range = f"{item['actual_start_page']}-{item['actual_end_page']} ({item['actual_page_count']}p)"
        print(f"  ID {item['id']}: {item['title'][:50]}...")
        print(f"    원본: {original_range} → 실제: {actual_range}")

if __name__ == "__main__":
    main()