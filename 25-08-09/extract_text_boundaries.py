#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:49:54 KST
핵심 내용: MD 파일에서 리프 노드의 시작/종료 텍스트를 추출하여 JSON 업데이트
상세 내용:
  - read_md_file (라인 21-25): MD 파일 읽기
  - find_text_boundaries (라인 27-80): 텍스트 경계 찾기
  - extract_boundary_text (라인 82-92): 경계 텍스트 추출
  - update_leaf_nodes (라인 94-118): 리프 노드 업데이트
  - process_part1 (라인 120-135): Part 1 처리
상태: 활성
주소: extract_text_boundaries
참조: Part_01_Part_1_Flexibility.md, part1_flexibility_leaf_nodes.json
"""

import json
import re
import os

def read_md_file(file_path):
    """MD 파일을 읽어 텍스트 반환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def find_text_boundaries(md_content, title):
    """제목을 기반으로 시작/종료 텍스트 경계 찾기"""
    lines = md_content.split('\n')
    
    # 제목 패턴들 시도
    title_patterns = [
        title,  # 원본 제목
        title.replace('—', '-'),  # em dash를 hyphen으로
        title.replace('–', '-'),  # en dash를 hyphen으로
        re.escape(title),  # 특수문자 이스케이프
    ]
    
    start_line = None
    end_line = None
    
    # 제목 위치 찾기
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            continue
            
        # 다양한 제목 패턴 매칭
        for pattern in title_patterns:
            if pattern in line_clean:
                start_line = i
                break
        
        if start_line is not None:
            break
    
    if start_line is None:
        # 제목을 찾지 못한 경우, 숫자로 시작하는 패턴 찾기
        title_num = re.match(r'^(\d+(?:\.\d+)*)', title.strip())
        if title_num:
            num_pattern = title_num.group(1)
            for i, line in enumerate(lines):
                if line.strip().startswith(num_pattern):
                    start_line = i
                    break
    
    if start_line is None:
        return "", ""
    
    # 다음 섹션 제목 찾기 (종료점)
    for i in range(start_line + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
            
        # 다음 섹션 제목 패턴 (숫자로 시작하거나 ## 헤더)
        if (re.match(r'^\d+(?:\.\d+)*\s+', line) or 
            line.startswith('##') or 
            line.startswith('# ') or
            line in ['Summary', 'Moving forward', 'Farewell', 'Delivering on time', 'Conclusion']):
            end_line = i
            break
    
    # 텍스트 추출
    start_text = extract_boundary_text(lines, start_line, forward=True)
    if end_line:
        end_text = extract_boundary_text(lines, end_line, forward=False)
    else:
        end_text = ""
    
    return start_text, end_text

def extract_boundary_text(lines, line_idx, forward=True, max_chars=100):
    """지정된 라인 주변에서 경계 텍스트 추출"""
    if forward:
        # 다음 몇 줄에서 의미있는 텍스트 찾기
        for i in range(line_idx, min(line_idx + 5, len(lines))):
            line = lines[i].strip()
            if line and not line.startswith('#') and len(line) > 10:
                return line[:max_chars]
    else:
        # 이전 몇 줄에서 의미있는 텍스트 찾기
        for i in range(line_idx - 1, max(line_idx - 5, 0), -1):
            line = lines[i].strip()
            if line and not line.startswith('#') and len(line) > 10:
                return line[:max_chars]
    
    return lines[line_idx].strip()[:max_chars] if line_idx < len(lines) else ""

def update_leaf_nodes(leaf_nodes_file, md_file, output_file):
    """리프 노드의 텍스트 경계를 업데이트"""
    # JSON 파일 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    # MD 파일 읽기
    md_content = read_md_file(md_file)
    
    # 각 리프 노드의 텍스트 경계 찾기
    updated_nodes = []
    for node in leaf_nodes:
        title = node['title']
        start_text, end_text = find_text_boundaries(md_content, title)
        
        updated_node = node.copy()
        updated_node['start_text'] = start_text
        updated_node['end_text'] = end_text
        updated_nodes.append(updated_node)
        
        print(f"✓ {title} → start: '{start_text[:30]}...' end: '{end_text[:30]}...'")
    
    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
    
    return len(updated_nodes)

def process_part1():
    """Part 1 처리"""
    base_dir = '/home/nadle/projects/Knowledge_Sherpa/v2'
    
    leaf_nodes_file = f'{base_dir}/25-08-09/part1_flexibility_leaf_nodes.json'
    md_file = f'{base_dir}/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md'
    output_file = f'{base_dir}/25-08-09/part1_flexibility_with_boundaries.json'
    
    print("Processing Part 1 - Flexibility...")
    count = update_leaf_nodes(leaf_nodes_file, md_file, output_file)
    print(f"✅ Part 1 완료: {count}개 노드 업데이트 → {output_file}")

if __name__ == "__main__":
    process_part1()