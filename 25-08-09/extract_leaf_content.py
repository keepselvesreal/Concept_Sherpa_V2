#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:49:54 KST
핵심 내용: 텍스트 경계를 기반으로 각 리프 노드의 내용을 추출하여 개별 MD 파일로 저장
상세 내용:
  - load_json_data (라인 22-26): JSON 파일 로드
  - read_md_file (라인 28-32): MD 파일 읽기
  - find_text_position (라인 34-47): 텍스트 위치 찾기
  - extract_node_content (라인 49-75): 노드 내용 추출
  - create_output_folder (라인 77-82): 출력 폴더 생성
  - save_node_as_md (라인 84-99): MD 파일로 저장
  - process_leaf_nodes (라인 101-130): 전체 처리
상태: 활성
주소: extract_leaf_content
참조: part1_flexibility_with_boundaries.json, Part_01_Part_1_Flexibility.md
"""

import json
import os
import re
from datetime import datetime

def load_json_data(file_path):
    """JSON 파일을 로드하여 반환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_md_file(file_path):
    """MD 파일을 읽어 텍스트 반환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def find_text_position(md_content, search_text):
    """MD 내용에서 특정 텍스트의 위치를 찾기"""
    lines = md_content.split('\n')
    
    # 검색 텍스트를 줄바꿈으로 분리
    search_lines = search_text.split('\n')
    search_first_line = search_lines[0].strip()
    
    for i, line in enumerate(lines):
        if search_first_line in line.strip():
            return i
    
    return -1

def extract_node_content(md_content, start_text, end_text):
    """시작과 끝 텍스트 사이의 내용을 추출"""
    lines = md_content.split('\n')
    
    # 시작 위치 찾기
    start_pos = find_text_position(md_content, start_text)
    if start_pos == -1:
        return f"<!-- 시작 텍스트를 찾을 수 없음: {start_text} -->\n"
    
    # 끝 위치 찾기
    end_pos = len(lines)  # 기본값: 파일 끝
    if end_text:
        end_pos = find_text_position(md_content, end_text)
        if end_pos == -1:
            end_pos = len(lines)
    
    # 내용 추출
    if start_pos < end_pos:
        content_lines = lines[start_pos:end_pos]
        return '\n'.join(content_lines)
    else:
        return f"<!-- 내용 추출 실패: start_pos={start_pos}, end_pos={end_pos} -->\n"

def create_output_folder(base_dir, folder_name):
    """출력 폴더 생성"""
    output_dir = os.path.join(base_dir, folder_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def save_node_as_md(node, content, output_dir):
    """노드를 MD 파일로 저장"""
    # 파일명 생성 (특수문자 제거)
    safe_title = re.sub(r'[^\w\s-]', '', node['title'])
    safe_title = re.sub(r'\s+', '_', safe_title.strip())
    filename = f"{node['id']:03d}_{safe_title}.md"
    
    # MD 파일 내용 생성
    md_content = f"""# {node['title']}

**ID**: {node['id']}  
**Level**: {node['level']}  
**추출 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')}

---

{content}
"""
    
    # 파일 저장
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filename

def process_leaf_nodes():
    """리프 노드들을 처리하여 개별 MD 파일로 저장"""
    base_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09'
    
    # 입력 파일들
    boundaries_file = os.path.join(base_dir, 'part1_flexibility_with_boundaries.json')
    md_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md'
    
    # 출력 폴더 생성
    output_dir = create_output_folder(base_dir, 'part1_leaf_nodes')
    
    # 데이터 로드
    nodes = load_json_data(boundaries_file)
    md_content = read_md_file(md_file)
    
    print(f"Processing {len(nodes)} leaf nodes...")
    print(f"Output directory: {output_dir}")
    
    success_count = 0
    for node in nodes:
        try:
            # 내용 추출
            content = extract_node_content(md_content, node['start_text'], node['end_text'])
            
            # MD 파일로 저장
            filename = save_node_as_md(node, content, output_dir)
            
            print(f"✓ {node['id']:03d}: {node['title']} → {filename}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ {node['id']:03d}: {node['title']} → ERROR: {e}")
    
    print(f"\n완료: {success_count}/{len(nodes)} 파일이 성공적으로 생성됨")
    print(f"저장 위치: {output_dir}")

if __name__ == "__main__":
    process_leaf_nodes()