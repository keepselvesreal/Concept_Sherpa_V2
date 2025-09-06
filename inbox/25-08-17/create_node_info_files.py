# 생성 시간: 2025-08-17 22:21:30 KST
# 핵심 내용: 확장된 노드 JSON 파일에서 정보 파일들을 생성하는 스크립트 (level 0 필터링 기능 추가)
# 상세 내용:
#   - load_enhanced_nodes 함수 (라인 21-30): 확장된 노드 JSON 파일 로드
#   - sanitize_title 함수 (라인 33-40): 파일명에 사용할 수 있도록 제목 정리
#   - create_info_file 함수 (라인 44-100): 개별 노드의 정보 파일 생성 (부모-자식 정보 포함)
#   - create_level_zero_only_info_file 함수 (라인 104-142): 오직 level 0 노드만 필터링하여 정보 파일 생성
#   - main 함수 (라인 145-188): CLI 인터페이스 및 실행 로직 (--level-zero-only 옵션 추가)
# 상태: 활성
# 주소: create_node_info_files/level_zero_filtered_v2
# 참조: create_node_info_files (원본 파일)

import json
import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any
from user_metadata_creator import create_user_input_template


def load_enhanced_nodes(json_path: str) -> List[Dict[Any, Any]]:
    """확장된 노드 JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 확장 노드 로드 완료")
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



def create_info_file(node: Dict[str, Any], nodes: List[Dict[str, Any]], output_dir: str) -> bool:
    """개별 노드의 정보 파일을 생성합니다 (부모-자식 정보 포함)."""
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


def create_level_zero_template_only(json_path: str, output_dir: str = 'level_zero_info_file') -> int:
    """level 0 노드 템플릿만 생성하는 함수 (구성 섹션 비움)"""
    print("🚀 Level 0 노드 템플릿 생성 시작 (메타데이터 입력 대기용)")
    print("=" * 50)
    
    # 1. 확장된 노드 데이터 로드
    nodes = load_enhanced_nodes(json_path)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        return 0
    
    # 2. level 0 노드만 필터링
    level_zero_nodes = [node for node in nodes if node.get('level') == 0]
    print(f"🔍 Level 0 노드 발견: {len(level_zero_nodes)}개")
    
    if not level_zero_nodes:
        print("❌ Level 0 노드가 없습니다.")
        return 0
    
    # 3. 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 출력 디렉토리: {output_path.absolute()}")
    
    # 4. 사용자 입력 템플릿 파일 생성
    create_user_input_template(str(output_path))
    
    # 5. level 0 노드 템플릿 생성 (구성 섹션 비움)
    print("📄 Level 0 템플릿 생성 중...")
    created_count = 0
    
    for node in level_zero_nodes:
        try:
            node_id = node.get('id', 0)
            level = node.get('level', 0)
            title = node.get('title', 'Untitled')
            
            # 파일명 생성
            safe_title = sanitize_title(title)
            filename = f"{node_id:02d}_lev{level}_{safe_title}_info.md"
            
            # 템플릿 내용 생성 (구성 섹션 비움)
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
            
            print(f"   📄 템플릿 생성: {filename}")
            created_count += 1
            
        except Exception as e:
            print(f"❌ 노드 ID {node.get('id', 'N/A')} 템플릿 생성 실패: {e}")
            continue
    
    print(f"\n✅ Level 0 템플릿 생성 완료: {created_count}개")
    print(f"📝 다음 단계: {output_path}/user_input_metadata.json 파일을 수정하세요")
    print(f"📂 파일 위치: {output_path.absolute()}")
    
    return created_count


def create_level_zero_only_info_file(json_path: str, output_dir: str = 'level_zero_info_file') -> int:
    """오직 level 0 노드의 정보 문서 파일만 생성하는 함수 (하위 호환성)"""
    return create_level_zero_template_only(json_path, output_dir)


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='확장된 노드 JSON에서 정보 파일들을 생성')
    parser.add_argument('enhanced_nodes_json', help='확장된 노드 JSON 파일 경로')
    parser.add_argument('-o', '--output-dir', default='node_info_files',
                      help='출력 디렉토리 (기본값: node_info_files)')
    parser.add_argument('--level-zero-only', action='store_true',
                      help='level 0 노드만 생성')
    
    args = parser.parse_args()
    
    # level 0 노드만 생성하는 경우 (템플릿만)
    if args.level_zero_only:
        create_level_zero_only_info_file(args.enhanced_nodes_json, args.output_dir)
        return
    
    print("🚀 노드 정보 파일 생성 시작")
    print("=" * 50)
    
    # 1. 확장된 노드 데이터 로드
    nodes = load_enhanced_nodes(args.enhanced_nodes_json)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        return
    
    # 2. 출력 디렉토리 생성
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 출력 디렉토리: {output_dir.absolute()}")
    
    # 3. 사용자 입력 템플릿 파일 생성
    create_user_input_template(str(output_dir))
    
    # 4. 각 노드별 정보 파일 생성
    print("📄 정보 파일 생성 중...")
    created_count = 0
    
    for node in nodes:
        if create_info_file(node, nodes, str(output_dir)):
            created_count += 1
    
    print(f"\n✅ 완료: {created_count}개 정보 파일 생성")
    print(f"📊 has_content=true 노드: {len([n for n in nodes if n.get('has_content')])}개")
    print(f"📂 파일 위치: {output_dir.absolute()}")


if __name__ == "__main__":
    main()