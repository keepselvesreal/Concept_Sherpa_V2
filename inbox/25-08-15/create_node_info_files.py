# 생성 시간: Fri Aug 15 10:57:22 KST 2025
# 핵심 내용: 노드 JSON 파일에서 정보 파일들을 생성하는 간단한 스크립트
# 상세 내용:
#   - load_nodes() (line 21): JSON 파일에서 노드 데이터 로드
#   - sanitize_title() (line 35): 파일명에 사용할 수 있도록 제목 정리
#   - create_info_file() (line 45): 개별 노드의 정보 파일 생성
#   - main() (line 69): 메인 실행 함수
# 상태: 활성
# 주소: create_node_info_files
# 참조: comprehensive_node_processor_v2 (핵심 기능 추출)

#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path

def load_nodes(json_path: str) -> list:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 노드 로드 완료")
        return nodes
    except Exception as e:
        print(f"❌ 파일 로드 실패: {e}")
        return []

def sanitize_title(title: str) -> str:
    """파일명에 사용할 수 있도록 제목을 정리합니다."""
    # 특수문자 제거
    safe_title = re.sub(r'[^\w\s-]', '', title)
    # 공백과 하이픈을 언더스코어로 변환
    safe_title = re.sub(r'[-\s]+', '_', safe_title)
    # 양끝 언더스코어 제거 및 소문자 변환
    return safe_title.strip('_').lower()

def create_info_file(node: dict, output_dir: str) -> bool:
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
process_status: false

# 추출


# 내용


# 구성
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

def main():
    """메인 실행 함수"""
    # 입력 파일 경로
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-15/node.json"
    
    # 출력 디렉토리 (현재 디렉토리)
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-15"
    
    print("🚀 노드 정보 파일 생성 시작")
    print("=" * 50)
    
    # 1. 노드 데이터 로드
    nodes = load_nodes(json_path)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        return
    
    # 2. 각 노드별 정보 파일 생성
    print("📄 정보 파일 생성 중...")
    created_count = 0
    
    for node in nodes:
        if create_info_file(node, output_dir):
            created_count += 1
    
    print(f"\n✅ 완료: {created_count}개 정보 파일 생성")

if __name__ == "__main__":
    main()