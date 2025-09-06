#!/usr/bin/env python3
"""
TOC JSON에 parent-children 관계 추가하는 간단한 스크립트
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

def build_parent_children_relationships(toc_data: list) -> list:
    """parent-children 관계를 구축하여 새로운 JSON 구조 생성"""
    enhanced_toc = []
    
    for i, item in enumerate(toc_data):
        # 기본 항목 복사
        enhanced_item = item.copy()
        
        # parent 찾기 (현재 level보다 1 작은 level을 가진 가장 가까운 이전 항목)
        parent_id = None
        current_level = item['level']
        
        if current_level > 0:  # level 0은 최상위이므로 parent가 없음
            for j in range(i - 1, -1, -1):
                if toc_data[j]['level'] == current_level - 1:
                    parent_id = j  # 인덱스를 parent_id로 사용
                    break
        
        # children 찾기 (현재 level보다 1 큰 level을 가진 직계 하위 항목들)
        children_ids = []
        
        for j in range(i + 1, len(toc_data)):
            next_item = toc_data[j]
            next_level = next_item['level']
            
            # 같은 레벨이거나 상위 레벨을 만나면 중단
            if next_level <= current_level:
                break
            
            # 바로 다음 레벨(직계 자식)인 경우에만 추가
            if next_level == current_level + 1:
                children_ids.append(j)  # 인덱스를 child_id로 사용
        
        # parent와 children 정보 추가
        enhanced_item['id'] = i  # 고유 ID 추가
        enhanced_item['parent_id'] = parent_id
        enhanced_item['children_ids'] = children_ids
        
        enhanced_toc.append(enhanced_item)
    
    return enhanced_toc

def save_enhanced_json(enhanced_data: list, output_path: str):
    """업데이트된 JSON을 저장"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 강화된 JSON 저장 완료: {output_path}")
        print(f"📊 총 {len(enhanced_data)} 개 항목 처리")
        
        # 통계 정보 출력
        level_counts = {}
        parent_counts = 0
        children_counts = 0
        
        for item in enhanced_data:
            level = item['level']
            level_counts[level] = level_counts.get(level, 0) + 1
            
            if item['parent_id'] is not None:
                parent_counts += 1
            
            if item['children_ids']:
                children_counts += 1
        
        print(f"📈 레벨별 항목 수: {level_counts}")
        print(f"👨‍👩‍👧‍👦 parent가 있는 항목: {parent_counts}")
        print(f"👶 children이 있는 항목: {children_counts}")
        
    except Exception as e:
        print(f"❌ JSON 저장 실패: {e}")

def main():
    """메인 실행 함수"""
    print("🚀 TOC Parent-Children 관계 추가 시작...")
    
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07"
    input_json = os.path.join(base_dir, "core_toc_with_page_ranges.json")
    output_json = os.path.join(base_dir, "enhanced_toc_with_relationships.json")
    
    # 1. JSON 데이터 로드
    print("\n📚 JSON 데이터 로드 중...")
    toc_data = load_toc_json(input_json)
    
    if not toc_data:
        print("❌ JSON 데이터 로드 실패로 작업 중단")
        return
    
    # 2. parent-children 관계 구축
    print("\n🔗 parent-children 관계 구축 중...")
    enhanced_data = build_parent_children_relationships(toc_data)
    
    # 3. 결과 저장
    print("\n💾 결과 저장 중...")
    save_enhanced_json(enhanced_data, output_json)
    
    print(f"\n🎉 작업 완료!")
    print(f"📁 입력 파일: {input_json}")
    print(f"📁 출력 파일: {output_json}")

if __name__ == "__main__":
    main()