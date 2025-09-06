#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 14:34:11
핵심 내용: 노드 JSON에서 기본 노드 정보 문서 생성 (최소 속성)
상세 내용: 
    - main() (line 18): 메인 실행 함수, 명령행 인수 처리
    - load_nodes() (line 43): 노드 JSON 파일 로드
    - sanitize_title() (line 58): 파일명용 제목 정리
    - create_info_file() (line 73): 개별 노드 정보 파일 생성
상태: active
참조: create_node_info_docs.py
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python create_node_info_docs_v2.py <extraction_folder>")
        print("Example: python create_node_info_docs_v2.py ./YouTube_250822")
        sys.exit(1)
    
    extraction_folder = sys.argv[1]
    
    # 폴더 존재 확인
    if not os.path.exists(extraction_folder):
        print(f"❌ 추출 폴더가 존재하지 않습니다: {extraction_folder}")
        sys.exit(1)
    
    print("🚀 노드 정보 문서 생성 시작")
    print("=" * 50)
    print(f"📁 처리 폴더: {os.path.abspath(extraction_folder)}")
    
    # 1. 노드 데이터 로드
    nodes = load_nodes(extraction_folder)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        sys.exit(1)
    
    # 2. 출력 디렉토리 생성 (extraction 폴더에 직접 생성)
    output_dir = Path(extraction_folder)
    print(f"📁 출력 디렉토리: {output_dir.absolute()}")
    
    # 3. 각 노드별 정보 파일 생성
    print("📄 정보 파일 생성 중...")
    created_count = 0
    
    for node in nodes:
        if create_info_file(node, str(output_dir)):
            created_count += 1
    
    print(f"\n✅ 완료: {created_count}개 정보 파일 생성")
    print(f"📂 파일 위치: {output_dir.absolute()}")


def load_nodes(extraction_folder: str) -> List[Dict[str, Any]]:
    """노드 JSON 파일을 로드합니다."""
    # nodes.json 파일 찾기
    nodes_files = []
    for file in os.listdir(extraction_folder):
        if file.endswith('_nodes.json'):
            nodes_files.append(os.path.join(extraction_folder, file))
    
    if not nodes_files:
        print("❌ 노드 JSON 파일을 찾을 수 없습니다 (*_nodes.json)")
        return []
    
    nodes_file = nodes_files[0]  # 첫 번째 파일 사용
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 노드 로드 완료: {os.path.basename(nodes_file)}")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 실패: {e}")
        return []


def sanitize_title(title: str) -> str:
    """파일명에 사용할 수 있도록 제목을 정리합니다."""
    # 특수문자 제거 (한글, 영문, 숫자, 하이픈, 언더스코어만 허용)
    safe_title = re.sub(r'[^\w\s\-\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\uAC00-\uD7AF]', '', title)
    # 공백과 하이픈을 언더스코어로 변환
    safe_title = re.sub(r'[-\s]+', '_', safe_title)
    # 양끝 언더스코어 제거
    safe_title = safe_title.strip('_')
    # 너무 긴 경우 자르기
    if len(safe_title) > 50:
        safe_title = safe_title[:50].rstrip('_')
    return safe_title


def create_info_file(node: Dict[str, Any], output_dir: str) -> bool:
    """개별 노드의 정보 파일을 생성합니다."""
    try:
        node_id = node.get('id', 0)
        level = node.get('level', 0)
        title = node.get('title', 'Untitled')
        
        # 파일명 생성: {id:02d}_lev{level}_{title}_info.md
        safe_title = sanitize_title(title)
        filename = f"{node_id:02d}_lev{level}_{safe_title}_info.md"
        
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

"""
        
        # 파일 저장
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   📄 생성: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ 노드 ID {node.get('id', 'N/A')} 파일 생성 실패: {e}")
        return False


if __name__ == "__main__":
    main()