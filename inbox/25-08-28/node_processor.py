# 생성 시간: Thu Aug 28 16:38:54 KST 2025
# 핵심 내용: 노드 JSON 파일에 ID, 부모-자식 관계, has_content 필드를 추가하고 개별 노드 정보 문서를 생성하는 스크립트
# 상세 내용:
#   - load_nodes() (line 30): JSON 노드 파일 로드
#   - add_node_ids() (line 47): 노드에 순차적 ID 추가
#   - build_parent_child_relationships() (line 61): 레벨 기반 부모-자식 관계 구축
#   - determine_has_content() (line 99): 해당 마크다운 파일에서 실제 본문 내용 존재 여부 확인
#   - save_updated_nodes() (line 138): 업데이트된 노드 JSON 파일 저장
#   - generate_node_documents() (line 152): 개별 노드 정보 문서 생성
#   - create_single_node_document() (line 183): 단일 노드 문서 생성 헬퍼
#   - main() (line 218): 메인 실행 함수
# 상태: active
# 주소: node_processor
# 참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-14 폴더 참고

#!/usr/bin/env uv run python

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

def load_nodes(nodes_file: str) -> List[Dict[str, Any]]:
    """
    노드 JSON 파일을 로드합니다.
    
    Args:
        nodes_file: 노드 JSON 파일 경로
        
    Returns:
        노드 리스트
    """
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"📊 {len(nodes)}개 노드 로드 완료")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 실패: {e}")
        return []

def add_node_ids(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    노드에 순차적 ID를 추가합니다.
    
    Args:
        nodes: 노드 리스트
        
    Returns:
        ID가 추가된 노드 리스트
    """
    print("🔢 노드 ID 추가 중...")
    for i, node in enumerate(nodes):
        node['id'] = i
    print(f"   ✅ {len(nodes)}개 노드에 ID 추가 완료")
    return nodes

def build_parent_child_relationships(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    레벨 기반으로 부모-자식 관계를 구축합니다.
    
    Args:
        nodes: 노드 리스트
        
    Returns:
        부모-자식 관계가 추가된 노드 리스트
    """
    print("👨‍👩‍👧‍👦 부모-자식 관계 구축 중...")
    
    # 모든 노드 초기화
    for node in nodes:
        node['parent_id'] = None
        node['children_ids'] = []
    
    # 부모-자식 관계 구축
    for i, current_node in enumerate(nodes):
        current_level = current_node['level']
        
        # 부모 찾기 - 이전 노드들 중에서 레벨이 하나 낮은 가장 가까운 노드
        for j in range(i - 1, -1, -1):
            if nodes[j]['level'] == current_level - 1:
                parent_id = nodes[j]['id']
                current_node['parent_id'] = parent_id
                nodes[j]['children_ids'].append(current_node['id'])
                break
    
    # 통계
    parent_count = len([n for n in nodes if n['parent_id'] is not None])
    children_count = len([n for n in nodes if len(n['children_ids']) > 0])
    
    print(f"   ✅ 부모 관계: {parent_count}개, 자식 관계: {children_count}개")
    return nodes

def determine_has_content(nodes: List[Dict[str, Any]], process_dir: str) -> List[Dict[str, Any]]:
    """
    해당 마크다운 파일에서 실제 본문 내용 존재 여부를 확인합니다.
    
    Args:
        nodes: 노드 리스트
        process_dir: 마크다운 파일들이 있는 디렉토리
        
    Returns:
        has_content 필드가 추가된 노드 리스트
    """
    print("📝 has_content 필드 판단 중...")
    
    content_count = 0
    
    # 실제 파일명 매핑
    filename_map = {
        0: "chapter7_00_7_Basic_data_validation.md",
        1: "chapter7_01_7.1_Data validation_in_DOP.md", 
        2: "chapter7_02_7.2_JSON_Schema_in_a_nutshell.md",
        3: "chapter7_03_7.3_Schema_flexibility_and_strictness.md",
        4: "chapter7_04_7.4_Schema_composition.md",
        5: "chapter7_05_7.5_Details_about_data_validation_failures.md",
        6: "chapter7_06_Summary.md"
    }
    
    for i, node in enumerate(nodes):
        # 실제 파일명 사용
        filename = filename_map.get(i, f"chapter7_0{i}_unknown.md")
        
        filepath = os.path.join(process_dir, filename)
        
        # 파일이 존재하고 본문 내용이 있는지 확인
        has_content = False
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 헤더 이후 실제 본문 내용이 있는지 확인
                lines = content.split('\n')
                
                # 메타데이터 섹션을 지나서 실제 내용이 있는지 확인
                in_metadata = False
                actual_content_lines = []
                
                for line in lines:
                    line_stripped = line.strip()
                    
                    # 첫 번째 헤더 이후부터 시작
                    if line_stripped.startswith('#'):
                        continue
                        
                    # 메타데이터 섹션 감지 (Level:, 페이지 범위: 등)
                    if line_stripped.startswith('**Level:**') or line_stripped.startswith('**페이지 범위:**'):
                        in_metadata = True
                        continue
                    
                    # --- 라인이 나오면 메타데이터 섹션 종료
                    if line_stripped == '---':
                        in_metadata = False
                        continue
                    
                    # 메타데이터 섹션이 아닌 곳에서 실제 내용 확인
                    if not in_metadata and line_stripped:
                        # 페이지 구분자(=== 페이지 N ===)가 아닌 실제 내용
                        if not line_stripped.startswith('===') and not line_stripped.startswith('**'):
                            actual_content_lines.append(line_stripped)
                
                # 실제 본문이 있으면 has_content = True
                has_content = len(actual_content_lines) > 0
                
                if has_content:
                    print(f"   ✅ {filename}: {len(actual_content_lines)}줄의 본문 내용 발견")
                
            except Exception as e:
                print(f"   ⚠️ 파일 읽기 오류 ({filename}): {e}")
                has_content = False
        else:
            print(f"   ⚠️ 파일 없음: {filename}")
        
        node['has_content'] = has_content
        if has_content:
            content_count += 1
    
    print(f"   ✅ has_content=True 노드: {content_count}개")
    return nodes

def save_updated_nodes(nodes: List[Dict[str, Any]], output_file: str) -> bool:
    """
    업데이트된 노드를 JSON 파일로 저장합니다.
    
    Args:
        nodes: 노드 리스트
        output_file: 출력 파일 경로
        
    Returns:
        저장 성공 여부
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        print(f"💾 업데이트된 노드 파일 저장 완료: {output_file}")
        return True
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")
        return False

def generate_node_documents(nodes: List[Dict[str, Any]], output_dir: str) -> None:
    """
    각 노드에 대한 개별 정보 문서를 생성합니다.
    
    Args:
        nodes: 노드 리스트
        output_dir: 출력 디렉토리
    """
    print("📄 개별 노드 정보 문서 생성 중...")
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    created_count = 0
    for node in nodes:
        if create_single_node_document(node, nodes, output_dir):
            created_count += 1
    
    print(f"   ✅ {created_count}개 노드 문서 생성 완료")

def create_single_node_document(node: Dict[str, Any], all_nodes: List[Dict[str, Any]], output_dir: str) -> bool:
    """
    단일 노드 문서를 생성합니다.
    
    Args:
        node: 대상 노드
        all_nodes: 전체 노드 리스트 (관계 정보 참조용)
        output_dir: 출력 디렉토리
        
    Returns:
        생성 성공 여부
    """
    try:
        # 파일명 생성: {id}_lev{level}_title_info.md
        title_clean = re.sub(r'[^\w\s.-]', '', node['title'])  # 점(.)도 유지
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        
        filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
        filepath = os.path.join(output_dir, filename)
        
        # 부모/자식 정보 수집
        parent_info = None
        if node['parent_id'] is not None:
            parent_node = next((n for n in all_nodes if n['id'] == node['parent_id']), None)
            if parent_node:
                parent_info = f"{parent_node['id']:02d} - {parent_node['title']}"
        
        children_info = []
        for child_id in node['children_ids']:
            child_node = next((n for n in all_nodes if n['id'] == child_id), None)
            if child_node:
                children_info.append(f"{child_node['id']:02d} - {child_node['title']}")
        
        # 문서 내용 생성 (4개 섹션 구조)
        content = f"""# 속성
---
process_status: false

# 추출
---

# 내용
---

# 구성
---
"""
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"   ❌ 노드 문서 생성 실패 (ID: {node.get('id', '?')}): {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 노드 처리 스크립트 시작")
    
    # 경로 설정
    process_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process"
    nodes_file = os.path.join(process_dir, "nodes.json")
    output_nodes_file = os.path.join(process_dir, "nodes_updated.json")
    output_docs_dir = os.path.join(process_dir, "node_docs")
    
    # 1. 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        return
    
    # 2. ID 추가
    nodes = add_node_ids(nodes)
    
    # 3. 부모-자식 관계 구축
    nodes = build_parent_child_relationships(nodes)
    
    # 4. has_content 필드 판단
    nodes = determine_has_content(nodes, process_dir)
    
    # 5. 업데이트된 노드 저장
    if save_updated_nodes(nodes, output_nodes_file):
        print(f"📊 처리 완료 - 업데이트된 파일: {output_nodes_file}")
    
    # 6. 개별 노드 문서 생성
    generate_node_documents(nodes, output_docs_dir)
    
    print("✅ 모든 작업 완료!")

if __name__ == "__main__":
    main()