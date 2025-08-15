#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:05 KST
핵심 내용: 7장 Basic data validation의 리프 노드 텍스트를 추출하여 개별 파일로 저장
상세 내용:
    - load_simple_leaf_nodes() (line 19-25): 간소화된 리프 노드 JSON 로드
    - filter_chapter7_nodes() (line 27-34): 7장에 해당하는 리프 노드 필터링
    - extract_text_from_main_file() (line 36-82): 메인 텍스트 파일에서 해당 섹션 텍스트 추출
    - save_individual_files() (line 84-104): 각 리프 노드를 개별 파일로 저장
    - main() (line 106-126): 전체 프로세스 실행
상태: active
주소: extract_chapter7_leaf_texts
참조: part2_scalability_leaf_simple.json, extracted_texts/Level01_7 Basic data validation.md
"""

import json
import os
import re
from pathlib import Path

def load_simple_leaf_nodes(file_path):
    """간소화된 리프 노드 JSON 로드"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_chapter7_nodes(nodes):
    """7장에 해당하는 리프 노드들만 필터링"""
    chapter7_nodes = []
    for node in nodes:
        title = node['title']
        # 7장 관련 노드들: "7 Introduction", "7.1", "7.2", "7.3", "7.4", "7.5", "Summary" (7장의)
        if (title.startswith('7 ') or title.startswith('7.')) or \
           (title == 'Summary' and node['level'] == 2 and node['id'] == 72):
            chapter7_nodes.append(node)
    return chapter7_nodes

def extract_text_from_main_file(main_file_path, section_title):
    """메인 텍스트 파일에서 특정 섹션의 텍스트 추출"""
    with open(main_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 섹션 제목을 정규화하여 매칭
    normalized_title = section_title.replace('.', r'\.')
    
    # 다양한 패턴으로 섹션 시작 찾기
    patterns = [
        rf"^(=== 페이지 \d+ ===.*?){re.escape(section_title)}",
        rf"^{re.escape(section_title)}$",
        rf"^\d+\.\d+\s+{re.escape(section_title.replace('7.', '').replace('7 ', '').strip())}$",
    ]
    
    start_pos = -1
    end_pos = -1
    
    # 패턴 매칭으로 시작 위치 찾기
    for pattern in patterns:
        matches = list(re.finditer(pattern, content, re.MULTILINE | re.DOTALL))
        if matches:
            start_pos = matches[0].start()
            break
    
    if start_pos == -1:
        # 직접 텍스트 검색
        if section_title in content:
            start_pos = content.find(section_title)
        else:
            return f"섹션 '{section_title}'를 찾을 수 없습니다."
    
    # 다음 섹션 시작 위치 찾기 (페이지 구분이나 다음 섹션 제목)
    next_section_patterns = [
        r"^=== 페이지 \d+ ===.*?^\d+\.\d+\s+",
        r"^=== 페이지 \d+ ===.*?^Summary$",
        r"^=== 페이지 \d+ ===.*?^8\s+",
    ]
    
    # 현재 섹션 이후의 내용에서 다음 섹션 찾기
    remaining_content = content[start_pos + len(section_title):]
    
    for pattern in next_section_patterns:
        match = re.search(pattern, remaining_content, re.MULTILINE | re.DOTALL)
        if match:
            end_pos = start_pos + len(section_title) + match.start()
            break
    
    if end_pos == -1:
        # 파일 끝까지
        section_text = content[start_pos:]
    else:
        section_text = content[start_pos:end_pos]
    
    return section_text.strip()

def save_individual_files(chapter7_nodes, main_file_path, output_dir):
    """각 리프 노드를 개별 파일로 저장"""
    os.makedirs(output_dir, exist_ok=True)
    
    for node in chapter7_nodes:
        node_id = node['id']
        title = node['title']
        level = node['level']
        
        # 파일명 생성 (안전한 파일명으로 변환)
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        filename = f"{node_id:03d}_{safe_title}.md"
        file_path = os.path.join(output_dir, filename)
        
        # 텍스트 추출
        section_text = extract_text_from_main_file(main_file_path, title)
        
        # 파일 내용 생성
        content = f"# {title}\n\n"
        content += f"**ID:** {node_id}\n"
        content += f"**Level:** {level}\n\n"
        content += "---\n\n"
        content += section_text
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"저장: {filename}")

def main():
    # 파일 경로 설정
    simple_nodes_file = 'part2_scalability_leaf_simple.json'
    main_text_file = 'extracted_texts/Level01_7 Basic data validation.md'
    output_dir = 'chapter7_leaf_texts'
    
    # 리프 노드 로드
    leaf_nodes = load_simple_leaf_nodes(simple_nodes_file)
    
    # 7장 노드 필터링
    chapter7_nodes = filter_chapter7_nodes(leaf_nodes)
    
    print(f"7장 리프 노드 {len(chapter7_nodes)}개를 찾았습니다:")
    for node in chapter7_nodes:
        print(f"- ID {node['id']}: {node['title']} (Level {node['level']})")
    
    # 개별 파일로 저장
    save_individual_files(chapter7_nodes, main_text_file, output_dir)
    
    print(f"\n모든 파일이 {output_dir}/ 폴더에 저장되었습니다.")

if __name__ == '__main__':
    main()