# -*- coding: utf-8 -*-
"""
생성 시간: 2025-08-09 17:08:05
핵심 내용: Chapter 7 Basic data validation의 리프 노드들의 텍스트 경계 추출 도구
상세 내용:
    - extract_chapter7_boundaries(): Chapter 7 리프 노드들의 시작/종료 문자 추출
    - save_boundaries_to_json(): 추출된 경계 정보를 JSON 파일로 저장
상태: 활성
주소: chapter7_leaf_nodes_with_boundaries
참조: part2_scalability_leaf_nodes.json의 Chapter 7 리프 노드들 기반
"""

import json

def extract_chapter7_boundaries():
    """Chapter 7의 리프 노드들에 시작/종료 문자 추가"""
    
    # 원본 JSON 데이터에서 Chapter 7 관련 리프 노드들만 추출
    chapter7_nodes = [
        {
            "id": 66,
            "title": "7 Introduction",
            "level": 2,
            "start_text": "Basic data validation",
            "end_text": "fourth principle"
        },
        {
            "id": 67,
            "title": "7.1 Data validation in DOP",
            "level": 2,
            "start_text": "7.1 Data validation",
            "end_text": "code base is bigger"
        },
        {
            "id": 68,
            "title": "7.2 JSON Schema in a nutshell",
            "level": 2,
            "start_text": "7.2 JSON Schema",
            "end_text": "search book request"
        },
        {
            "id": 69,
            "title": "7.3 Schema flexibility and strictness",
            "level": 2,
            "start_text": "7.3 Schema flexibility",
            "end_text": "in what you accept"
        },
        {
            "id": 70,
            "title": "7.4 Schema composition",
            "level": 2,
            "start_text": "7.4 Schema composition",
            "end_text": "what went wrong"
        },
        {
            "id": 71,
            "title": "7.5 Details about data validation failures",
            "level": 2,
            "start_text": "7.5 Details about",
            "end_text": "exactly what he needs"
        },
        {
            "id": 72,
            "title": "Summary",
            "level": 2,
            "start_text": "Summary",
            "end_text": "covered in chapter 12"
        }
    ]
    
    return chapter7_nodes

def save_boundaries_to_json(nodes, output_file):
    """추출된 경계 정보를 JSON 파일로 저장"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)
    
    print(f"Chapter 7 리프 노드 경계 정보가 {output_file}에 저장되었습니다.")
    print(f"총 {len(nodes)}개의 리프 노드 경계가 추출되었습니다.")

if __name__ == "__main__":
    # Chapter 7 리프 노드 경계 추출
    chapter7_nodes = extract_chapter7_boundaries()
    
    # JSON 파일로 저장
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_boundaries.json"
    save_boundaries_to_json(chapter7_nodes, output_file)
    
    # 결과 확인
    for node in chapter7_nodes:
        print(f"ID {node['id']}: {node['title']}")
        print(f"  시작: '{node['start_text']}'")
        print(f"  종료: '{node['end_text']}'")
        print()