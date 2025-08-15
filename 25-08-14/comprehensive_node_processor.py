#!/usr/bin/env python3

"""
생성 시간: 2025년 08월 14일 10:13:28 KST
핵심 내용: 노드 정보를 종합적으로 처리하여 완전한 노드 구조 및 문서를 생성하는 통합 스크립트
상세 내용:
- load_input_data (라인 45-80): JSON 노드 정보 또는 마크다운 파일을 입력으로 받아 처리
- extract_headers_from_md (라인 85-120): 마크다운 파일에서 헤더 구조 추출
- build_hierarchy (라인 125-170): 레벨 기반 부모-자식 관계 구축
- determine_has_content (라인 175-200): 상위-하위 노드 사이 내용 존재 여부 판단
- save_nodes_json (라인 205-225): 전체 노드 구조를 nodes.json으로 저장
- filter_and_save_content_nodes (라인 230-265): has_content=true 또는 리프 노드를 content_nodes.json으로 저장
- create_node_documents (라인 270-310): 모든 노드에 대해 level_title_info.md 파일 생성
- process_nodes_comprehensive (라인 315-380): 전체 처리 프로세스 통합 실행
- main (라인 385-420): 메인 실행 함수 및 CLI 인터페이스
상태: 활성
주소: comprehensive_node_processor
참조: header_to_json_converter.py, node_hierarchy_builder.py, content_node_filter_v2.py, node_document_generator.py 기능 통합
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

def load_input_data(input_path: str) -> Tuple[List[Dict[str, Any]], bool]:
    """
    입력 파일을 로드합니다. JSON 노드 파일 또는 마크다운 파일 지원.
    
    Args:
        input_path: 입력 파일 경로
        
    Returns:
        Tuple[노드 리스트, 마크다운 파일 여부]
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")
    
    # 파일 확장자로 타입 판단
    if input_file.suffix.lower() in ['.md', '.txt']:
        # 마크다운 파일
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        nodes = extract_headers_from_md(content)
        return nodes, True
        
    elif input_file.suffix.lower() == '.json':
        # JSON 노드 파일
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # headers 키가 있는 경우 추출
        if isinstance(data, dict) and 'headers' in data:
            nodes = data['headers']
        else:
            nodes = data
            
        return nodes, False
    
    else:
        raise ValueError(f"지원되지 않는 파일 형식: {input_file.suffix}")

def extract_headers_from_md(content: str) -> List[Dict[str, Any]]:
    """
    마크다운 콘텐츠에서 헤더를 추출하여 노드 구조로 변환합니다.
    
    Args:
        content: 마크다운 콘텐츠
        
    Returns:
        노드 리스트
    """
    headers = []
    pattern = r'^(#{1,6})\s+(.+)$'
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        match = re.match(pattern, line)
        
        if match:
            hash_marks = match.group(1)
            title = match.group(2).strip()
            level = len(hash_marks) - 1  # # = 0, ## = 1, ### = 2
            
            node = {
                "id": len(headers),
                "title": title,
                "level": level
            }
            headers.append(node)
    
    print(f"📊 마크다운에서 {len(headers)}개 헤더 추출 완료")
    return headers

def build_hierarchy(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    레벨 기반으로 부모-자식 관계를 구축합니다.
    
    Args:
        nodes: 노드 리스트
        
    Returns:
        계층 관계가 추가된 노드 리스트
    """
    print("🔗 부모-자식 관계 구축 중...")
    
    # 노드를 정렬 (id 순서대로)
    nodes_sorted = sorted(nodes, key=lambda x: x.get('id', 0))
    
    # 각 노드에 관계 필드 초기화
    for node in nodes_sorted:
        node['parent_id'] = None
        node['children_ids'] = []
    
    # 부모-자식 관계 구축
    for i, current_node in enumerate(nodes_sorted):
        current_level = current_node.get('level', 0)
        
        # 현재 노드의 부모 찾기 (더 낮은 레벨의 가장 가까운 이전 노드)
        for j in range(i-1, -1, -1):
            potential_parent = nodes_sorted[j]
            parent_level = potential_parent.get('level', 0)
            
            if parent_level < current_level:
                # 부모 발견
                current_node['parent_id'] = potential_parent['id']
                potential_parent['children_ids'].append(current_node['id'])
                break
    
    # 통계 출력
    root_nodes = [n for n in nodes_sorted if n['parent_id'] is None]
    leaf_nodes = [n for n in nodes_sorted if len(n['children_ids']) == 0]
    
    print(f"   ✅ 루트 노드: {len(root_nodes)}개")
    print(f"   ✅ 리프 노드: {len(leaf_nodes)}개")
    
    return nodes_sorted

def determine_has_content(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    상위-하위 노드 사이에 내용이 존재하는지 판단하여 has_content 필드를 추가합니다.
    
    Args:
        nodes: 노드 리스트
        
    Returns:
        has_content 필드가 추가된 노드 리스트
    """
    print("📝 has_content 필드 판단 중...")
    
    # 현재는 리프 노드와 첫 번째 레벨 노드에 대해 has_content = True로 설정
    # 실제 구현에서는 더 정교한 로직 필요
    content_count = 0
    
    for node in nodes:
        # 리프 노드는 항상 content 존재
        if len(node.get('children_ids', [])) == 0:
            node['has_content'] = True
            content_count += 1
        else:
            # 비-리프 노드는 기본적으로 False, 향후 확장 가능
            node['has_content'] = False
    
    print(f"   ✅ has_content=True 노드: {content_count}개")
    
    return nodes

def save_nodes_json(nodes: List[Dict[str, Any]], output_path: str = "nodes.json") -> bool:
    """
    전체 노드 구조를 JSON 파일로 저장합니다.
    
    Args:
        nodes: 노드 리스트
        output_path: 출력 파일 경로
        
    Returns:
        저장 성공 여부
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        print(f"💾 전체 노드 구조 저장: {output_path} ({len(nodes)}개 노드)")
        return True
    except Exception as e:
        print(f"❌ nodes.json 저장 실패: {e}")
        return False

def filter_and_save_content_nodes(nodes: List[Dict[str, Any]], output_path: str = "content_nodes.json") -> bool:
    """
    has_content=True 또는 리프 노드만 필터링하여 저장합니다.
    
    Args:
        nodes: 노드 리스트
        output_path: 출력 파일 경로
        
    Returns:
        저장 성공 여부
    """
    print("🔍 content 노드 필터링 중...")
    
    filtered_nodes = []
    
    for node in nodes:
        has_content = node.get('has_content', False)
        is_leaf = len(node.get('children_ids', [])) == 0
        
        if has_content or is_leaf:
            filtered_node = {
                "id": node.get('id'),
                "level": node.get('level'),
                "title": node.get('title')
            }
            filtered_nodes.append(filtered_node)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_nodes, f, ensure_ascii=False, indent=2)
        print(f"💾 content 노드 저장: {output_path} ({len(filtered_nodes)}개 노드)")
        return True
    except Exception as e:
        print(f"❌ content_nodes.json 저장 실패: {e}")
        return False

def create_node_documents(nodes: List[Dict[str, Any]], output_dir: str = "node_docs") -> bool:
    """
    모든 노드에 대해 level_title_info.md 파일을 생성합니다.
    
    Args:
        nodes: 노드 리스트
        output_dir: 출력 디렉토리
        
    Returns:
        생성 성공 여부
    """
    print("📄 노드 문서 생성 중...")
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    created_count = 0
    
    for node in nodes:
        try:
            level = node.get('level', 0)
            title = node.get('title', 'Untitled')
            
            # 파일명 생성
            clean_title = re.sub(r'[^\w\s-]', '', title).strip()
            clean_title = re.sub(r'[-\s]+', '_', clean_title)
            filename = f"{level}_{clean_title}_info.md"
            
            # 자식 노드 파일명 생성
            children_filenames = ""
            if node.get('children_ids'):
                for child_id in node['children_ids']:
                    child_node = next((n for n in nodes if n.get('id') == child_id), None)
                    if child_node:
                        child_level = child_node.get('level', 0)
                        child_title = child_node.get('title', 'Untitled')
                        child_clean_title = re.sub(r'[^\w\s-]', '', child_title).strip()
                        child_clean_title = re.sub(r'[-\s]+', '_', child_clean_title)
                        child_filename = f"{child_level}_{child_clean_title}_info.md"
                        children_filenames += f"{child_filename}\n"
            
            # 문서 내용 생성
            content = f"""# 속성
process_status:

# 추출


# 내용


# 구성
{children_filenames}"""
            
            # 파일 저장
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_count += 1
            
        except Exception as e:
            print(f"❌ 노드 ID {node.get('id', 'N/A')} 문서 생성 오류: {e}")
    
    print(f"📄 노드 문서 생성 완료: {output_dir}/ ({created_count}개 파일)")
    return created_count > 0

def process_nodes_comprehensive(input_path: str, output_dir: str = ".") -> bool:
    """
    전체 노드 처리 프로세스를 실행합니다.
    
    Args:
        input_path: 입력 파일 경로 (JSON 노드 파일 또는 마크다운 파일)
        output_dir: 출력 디렉토리
        
    Returns:
        처리 성공 여부
    """
    print("🚀 종합 노드 처리 시작")
    print("=" * 60)
    print(f"📁 입력 파일: {input_path}")
    print(f"📁 출력 디렉토리: {output_dir}")
    print()
    
    try:
        # 1. 입력 데이터 로드
        print("1️⃣ 입력 데이터 로드")
        nodes, is_markdown = load_input_data(input_path)
        if is_markdown:
            print(f"   📝 마크다운 파일에서 {len(nodes)}개 노드 추출")
        else:
            print(f"   📄 JSON 파일에서 {len(nodes)}개 노드 로드")
        
        if not nodes:
            print("❌ 노드 데이터가 없습니다.")
            return False
        
        # 2. 부모-자식 관계 구축
        print("\n2️⃣ 계층 관계 구축")
        nodes = build_hierarchy(nodes)
        
        # 3. has_content 필드 판단
        print("\n3️⃣ 내용 존재 여부 판단")
        nodes = determine_has_content(nodes)
        
        # 4. 전체 노드 구조 저장 (nodes.json)
        print("\n4️⃣ 전체 노드 구조 저장")
        nodes_json_path = os.path.join(output_dir, "nodes.json")
        save_nodes_json(nodes, nodes_json_path)
        
        # 5. content 노드 필터링 저장 (content_nodes.json)
        print("\n5️⃣ 콘텐츠 노드 필터링 저장")
        content_nodes_path = os.path.join(output_dir, "content_nodes.json")
        filter_and_save_content_nodes(nodes, content_nodes_path)
        
        # 6. 노드 문서 생성 (level_title_info.md)
        print("\n6️⃣ 노드 문서 생성")
        docs_dir = os.path.join(output_dir, "node_docs")
        create_node_documents(nodes, docs_dir)
        
        print("\n✨ 종합 노드 처리 완료!")
        print("=" * 60)
        print(f"📊 처리 결과:")
        print(f"   - 전체 노드: {len(nodes)}개")
        print(f"   - 콘텐츠 노드: {len([n for n in nodes if n.get('has_content') or len(n.get('children_ids', [])) == 0])}개")
        print(f"   - 생성된 파일:")
        print(f"     • {nodes_json_path}")
        print(f"     • {content_nodes_path}")
        print(f"     • {docs_dir}/ (각 노드별 info.md 파일)")
        
        return True
        
    except Exception as e:
        print(f"❌ 처리 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='노드 정보를 종합적으로 처리하여 완전한 노드 구조 및 문서를 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python comprehensive_node_processor.py document.md
  python comprehensive_node_processor.py nodes.json -o ./output
  python comprehensive_node_processor.py script_structure.json --output-dir ./processed
        """
    )
    
    parser.add_argument('input_file', help='입력 파일 (JSON 노드 파일 또는 마크다운 파일)')
    parser.add_argument('-o', '--output-dir', default='.', help='출력 디렉토리 (기본값: 현재 디렉토리)')
    parser.add_argument('-v', '--verbose', action='store_true', help='상세 출력')
    
    args = parser.parse_args()
    
    # 처리 실행
    success = process_nodes_comprehensive(args.input_file, args.output_dir)
    
    if success:
        print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
        return 0
    else:
        print("\n💥 작업 실행 중 오류가 발생했습니다.")
        return 1

if __name__ == "__main__":
    exit(main())