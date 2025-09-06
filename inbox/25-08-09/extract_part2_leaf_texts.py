# extract_part2_leaf_texts.py
# 생성 시간: 2025-08-09 11:24:21
# 핵심 내용: Part 2 Scalability 리프 노드의 텍스트를 정확히 추출하여 개별 파일로 저장
# 상세 내용:
#   - load_boundaries() (라인 18-25): 경계 정보가 포함된 JSON 파일 로드
#   - load_source_text() (라인 27-33): 원본 Part 2 텍스트 파일 로드  
#   - extract_text_between_boundaries() (라인 35-67): 시작/종료 문자열 사이의 텍스트 추출
#   - clean_extracted_text() (라인 69-80): 추출된 텍스트 정리 및 포맷팅
#   - save_leaf_text() (라인 82-96): 리프 노드 텍스트를 개별 파일로 저장
#   - main() (라인 98-124): 메인 실행 함수
# 상태: 활성
# 주소: extract_part2_leaf_texts
# 참조: part2_scalability_leaf_nodes_with_boundaries.json, Part_02_Part_2_Scalability.md

import json
import os
from pathlib import Path
import re

def load_boundaries(json_path):
    """경계 정보가 포함된 JSON 파일을 로드합니다."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_source_text(text_path):
    """원본 Part 2 텍스트 파일을 로드합니다."""
    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_between_boundaries(source_text, start_text, end_text):
    """시작과 종료 문자열 사이의 텍스트를 추출합니다."""
    try:
        # 시작 지점 찾기
        start_index = source_text.find(start_text)
        if start_index == -1:
            print(f"Warning: 시작 텍스트를 찾을 수 없습니다: '{start_text[:20]}...'")
            return None
        
        # 시작 지점부터 검색 시작
        search_start = start_index
        
        # 종료 지점 찾기 (시작 지점 이후에서)
        end_index = source_text.find(end_text, search_start)
        if end_index == -1:
            # 종료 텍스트를 찾을 수 없으면 파일 끝까지
            print(f"Warning: 종료 텍스트를 찾을 수 없습니다: '{end_text[:20]}...'")
            print("파일 끝까지 추출합니다.")
            extracted_text = source_text[start_index:]
        else:
            # 시작 지점부터 종료 지점까지 추출
            extracted_text = source_text[start_index:end_index]
        
        return extracted_text.strip()
        
    except Exception as e:
        print(f"텍스트 추출 중 오류 발생: {e}")
        return None

def clean_extracted_text(text):
    """추출된 텍스트를 정리하고 포맷팅합니다."""
    if not text:
        return ""
    
    # 여러 줄바꿈을 2개로 제한
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 앞뒤 공백 제거
    text = text.strip()
    
    return text

def save_leaf_text(node_id, title, text, output_dir):
    """리프 노드 텍스트를 개별 파일로 저장합니다."""
    if not text:
        print(f"Warning: 노드 {node_id}의 텍스트가 비어있습니다.")
        return
    
    # 파일명 생성 (안전한 파일명으로 변환)
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    safe_title = re.sub(r'[-\s]+', '_', safe_title)
    filename = f"{node_id:03d}_{safe_title}.md"
    
    filepath = Path(output_dir) / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"저장 완료: {filename} ({len(text)} 문자)")

def main():
    # 파일 경로 설정
    boundaries_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part2_scalability_leaf_nodes_with_boundaries.json"
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_02_Part_2_Scalability.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part2_extracted_leaf_texts"
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 로드
    print("경계 정보 및 원본 텍스트 로드 중...")
    leaf_nodes = load_boundaries(boundaries_path)
    source_text = load_source_text(source_path)
    
    # 각 리프 노드의 텍스트 추출
    print(f"\n총 {len(leaf_nodes)}개의 리프 노드 텍스트를 추출합니다...\n")
    
    for i, node in enumerate(leaf_nodes, 1):
        node_id = node['id']
        title = node['title']
        start_text = node['start_text']
        end_text = node['end_text']
        
        print(f"[{i}/{len(leaf_nodes)}] 처리 중: {title}")
        
        # 텍스트 추출
        extracted_text = extract_text_between_boundaries(source_text, start_text, end_text)
        
        if extracted_text:
            # 텍스트 정리
            cleaned_text = clean_extracted_text(extracted_text)
            
            # 파일 저장
            save_leaf_text(node_id, title, cleaned_text, output_dir)
        else:
            print(f"Error: 노드 {node_id}의 텍스트 추출 실패")
        
        print()
    
    print(f"모든 리프 노드 텍스트가 {output_dir}에 저장되었습니다.")

if __name__ == "__main__":
    main()