#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 11:45:12
핵심 내용: MD 추출 JSON에서 노드 정보 문서 파일들을 생성하는 스크립트
상세 내용: 
    - load_nodes() (line 20): 기본 노드 JSON 파일 로드
    - enhance_nodes() (line 35): 기본 노드를 확장 노드로 변환 (부모-자식 관계 계산)
    - create_user_metadata_template() (line 80): 사용자 메타데이터 템플릿 생성
    - sanitize_title() (line 105): 파일명용 제목 정리
    - create_info_file() (line 115): 개별 노드 정보 파일 생성
    - main() (line 150): 메인 실행 함수
상태: active
참조: create_node_info_files.py, user_metadata_creator.py
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_nodes(nodes_json_path: str) -> List[Dict[str, Any]]:
    """기본 노드 JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(nodes_json_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 노드 로드 완료")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 실패: {e}")
        return []


def enhance_nodes(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """기본 노드를 확장 노드로 변환 (부모-자식 관계 계산)"""
    enhanced_nodes = []
    
    for i, node in enumerate(nodes):
        node_id = node.get('id', i)
        level = node.get('level', 0)
        title = node.get('title', 'Untitled')
        
        # 부모 노드 찾기 (현재 노드보다 앞에 있는 노드 중 level이 하나 작은 노드)
        parent_id = None
        if level > 0:
            for j in range(i - 1, -1, -1):
                prev_node = nodes[j]
                if prev_node.get('level', 0) == level - 1:
                    parent_id = prev_node.get('id', j)
                    break
        
        enhanced_node = {
            'id': node_id,
            'level': level,
            'title': title,
            'parent_id': parent_id,
            'children_ids': [],
            'has_content': level == 0  # level 0만 내용이 있다고 가정
        }
        enhanced_nodes.append(enhanced_node)
    
    # 자식 노드 ID 계산
    for node in enhanced_nodes:
        node_id = node['id']
        children = [n['id'] for n in enhanced_nodes if n.get('parent_id') == node_id]
        node['children_ids'] = children
    
    print(f"✅ {len(enhanced_nodes)}개 확장 노드 생성 완료")
    return enhanced_nodes





def sanitize_title(title: str) -> str:
    """파일명에 사용할 수 있도록 제목을 정리합니다."""
    # 특수문자 제거
    safe_title = re.sub(r'[^\w\s\-\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\uAC00-\uD7AF]', '', title)
    # 공백과 하이픈을 언더스코어로 변환
    safe_title = re.sub(r'[-\s]+', '_', safe_title)
    # 양끝 언더스코어 제거
    safe_title = safe_title.strip('_')
    # 너무 긴 경우 자르기
    if len(safe_title) > 50:
        safe_title = safe_title[:50].rstrip('_')
    return safe_title


def create_info_file(node: Dict[str, Any], nodes: List[Dict[str, Any]], output_dir: str) -> bool:
    """개별 노드의 정보 파일을 생성합니다."""
    try:
        node_id = node.get('id', 0)
        level = node.get('level', 0)
        title = node.get('title', 'Untitled')
        parent_id = node.get('parent_id')
        children_ids = node.get('children_ids', [])
        has_content = node.get('has_content', False)
        
        # 파일명 생성: {id:02d}_lev{level}_{title}_info.md
        safe_title = sanitize_title(title)
        filename = f"{node_id:02d}_lev{level}_{safe_title}_info.md"
        
        # 자식 노드 파일명 생성 (구성 섹션용)
        child_filenames = []
        for child_id in children_ids:
            child_node = next((n for n in nodes if n.get('id') == child_id), None)
            if child_node:
                child_level = child_node.get('level', 0)
                child_title = child_node.get('title', 'Untitled')
                child_safe_title = sanitize_title(child_title)
                child_filename = f"{child_id:02d}_lev{child_level}_{child_safe_title}_info.md"
                child_filenames.append(child_filename)
        
        # 구성 섹션 내용
        composition_content = "\n".join(child_filenames) if child_filenames else ""
        
        # 파일 내용 생성
        content = f"""# 속성
---
process_status: false

# 추출
---


# 내용
---


# 구성
---
{composition_content}"""
        
        # 파일 저장
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        content_status = "[내용있음]" if has_content else "[내용없음]"
        print(f"   📄 생성: {filename} {content_status}")
        return True
        
    except Exception as e:
        print(f"❌ 노드 ID {node.get('id', 'N/A')} 파일 생성 실패: {e}")
        return False


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python create_node_info_docs.py <nodes_json>")
        print("Example: python create_node_info_docs.py nodes.json")
        sys.exit(1)
    
    nodes_json_path = sys.argv[1]
    
    # 파일 존재 확인
    if not os.path.exists(nodes_json_path):
        print(f"❌ 노드 JSON 파일이 존재하지 않습니다: {nodes_json_path}")
        sys.exit(1)
    
    print("🚀 노드 정보 문서 생성 시작")
    print("=" * 50)
    
    # 1. 노드 데이터 로드 및 확장
    nodes = load_nodes(nodes_json_path)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        sys.exit(1)
    
    enhanced_nodes = enhance_nodes(nodes)
    
    # 2. 출력 디렉토리 생성
    output_dir = Path("node_info_docs")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 출력 디렉토리: {output_dir.absolute()}")
    
    # 3. 각 노드별 정보 파일 생성
    print("📄 정보 파일 생성 중...")
    created_count = 0
    
    for node in enhanced_nodes:
        if create_info_file(node, enhanced_nodes, str(output_dir)):
            created_count += 1
    
    print(f"\n✅ 완료: {created_count}개 정보 파일 생성")
    print(f"📊 has_content=true 노드: {len([n for n in enhanced_nodes if n.get('has_content')])}개")
    print(f"📂 파일 위치: {output_dir.absolute()}")


if __name__ == "__main__":
    main()