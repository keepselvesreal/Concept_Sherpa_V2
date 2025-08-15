#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:49:54 KST
핵심 내용: JSON 목차 데이터를 Part 단위로 분리하는 스크립트
상세 내용:
  - load_json_data (라인 21-26): JSON 파일 로드 함수
  - get_part_data (라인 28-40): Part별 데이터 추출 함수
  - save_part_file (라인 42-48): Part별 JSON 파일 저장 함수
  - main (라인 50-80): 메인 실행 함수
상태: 활성
주소: split_parts
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json
"""

import json
import os

def load_json_data(file_path):
    """JSON 파일을 로드하여 반환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_part_data(data, part_id):
    """특정 Part ID에 해당하는 모든 데이터를 추출"""
    part_data = []
    
    for item in data:
        # Part 자체이거나 해당 Part의 자식인 경우 추가
        if item['id'] == part_id or is_descendant(data, item, part_id):
            part_data.append(item)
    
    return part_data

def is_descendant(data, item, part_id):
    """해당 아이템이 특정 Part의 후손인지 확인"""
    current_item = item
    while current_item['parent_id'] is not None:
        if current_item['parent_id'] == part_id:
            return True
        # 부모 찾기
        current_item = next((x for x in data if x['id'] == current_item['parent_id']), None)
        if current_item is None:
            break
    return False

def save_part_file(part_data, filename):
    """Part 데이터를 JSON 파일로 저장"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(part_data, f, ensure_ascii=False, indent=2)

def main():
    # 입력 파일 경로
    input_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09'
    
    # JSON 데이터 로드
    data = load_json_data(input_file)
    
    # Part 정의 (level 0인 항목들)
    parts = [
        {'id': 0, 'filename': 'part1_flexibility.json', 'title': 'Part 1—Flexibility'},
        {'id': 63, 'filename': 'part2_scalability.json', 'title': 'Part 2—Scalability'},
        {'id': 112, 'filename': 'part3_maintainability.json', 'title': 'Part 3—Maintainability'},
        {'id': 147, 'filename': 'appendix_a_principles.json', 'title': 'Appendix A—Principles of data-oriented programming'},
        {'id': 174, 'filename': 'appendix_b_generic_access.json', 'title': 'Appendix B—Generic data access in statically-typed languages'},
        {'id': 194, 'filename': 'appendix_c_paradigms.json', 'title': 'Appendix C—Data-oriented programming paradigms'},
        {'id': 216, 'filename': 'appendix_d_lodash.json', 'title': 'Appendix D—Lodash reference'}
    ]
    
    # 각 Part별로 데이터 분리 및 저장
    for part in parts:
        part_data = get_part_data(data, part['id'])
        output_file = os.path.join(output_dir, part['filename'])
        save_part_file(part_data, output_file)
        print(f"✓ {part['title']} → {part['filename']} ({len(part_data)} items)")

if __name__ == "__main__":
    main()