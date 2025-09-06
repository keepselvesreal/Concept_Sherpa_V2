#!/usr/bin/env python3
"""
생성 시간: 2025-08-11 21:05:42 KST
핵심 내용: 노드 파일 생성기 - JSON 구조에서 root/internal 노드에 대응하는 마크다운 파일 생성
상세 내용:
    - get_leaf_descendants (20-45행): 노드의 모든 리프 후손들을 찾는 재귀 함수
    - create_node_file (47-90행): 개별 노드 파일 생성 함수
    - create_all_node_files (92-145행): 모든 root/internal 노드 파일들 생성
    - main (147-170행): CLI 실행 로직
상태: active
주소: create_node_files
참조: section_splitter (구조 참고)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any


def get_leaf_descendants(node_id: int, sections: Dict[int, Dict]) -> List[str]:
    """
    주어진 노드의 모든 리프 후손들을 찾아 파일명 리스트로 반환
    
    Args:
        node_id: 대상 노드 ID
        sections: 전체 섹션 데이터 (id를 키로 한 딕셔너리)
    
    Returns:
        리프 노드들의 파일명 리스트
    """
    leaf_files = []
    node = sections[node_id]
    
    # 리프 노드인 경우 파일명 추가
    if not node['children_ids']:
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', node['title'])
        safe_filename = re.sub(r'\s+', '_', safe_filename)
        filename = f"leaf_{safe_filename}.md"
        leaf_files.append(filename)
    else:
        # internal 노드인 경우 자식들을 재귀 탐색
        for child_id in node['children_ids']:
            child_leafs = get_leaf_descendants(child_id, sections)
            leaf_files.extend(child_leafs)
    
    return leaf_files


def create_node_file(node: Dict[str, Any], sections: Dict[int, Dict], output_dir: Path) -> str:
    """
    개별 노드 파일 생성
    
    Args:
        node: 노드 정보
        sections: 전체 섹션 데이터
        output_dir: 출력 디렉토리
    
    Returns:
        생성된 파일명
    """
    node_id = node['id']
    title = node['title']
    level = node['level']
    
    # 파일명 생성
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', title)
    safe_filename = re.sub(r'\s+', '_', safe_filename)
    
    if level == 0:  # root 노드
        filename = f"root_{safe_filename}.md"
    else:  # internal 노드
        filename = f"internal_level{level}_{safe_filename}.md"
    
    # 헤더 생성 (레벨에 맞는 마크다운 헤더)
    header = "#" * (level + 1) + f" {title}"
    
    # 리프 후손들 찾기
    leaf_files = get_leaf_descendants(node_id, sections)
    
    # 파일 내용 생성
    content_lines = [header, ""]
    content_lines.extend(leaf_files)
    content = "\n".join(content_lines)
    
    # 파일 저장
    filepath = output_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def create_all_node_files(sections_json: str, output_dir: str) -> Dict[str, Any]:
    """
    모든 root/internal 노드 파일들 생성
    
    Args:
        sections_json: 섹션 구조 JSON 파일 경로
        output_dir: 출력 디렉토리 경로
    
    Returns:
        작업 결과 요약
    """
    # JSON 파일 읽기
    with open(sections_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sections_list = data['sections']
    
    # ID를 키로 한 딕셔너리 생성
    sections = {section['id']: section for section in sections_list}
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # root와 internal 노드들 찾기
    root_nodes = [s for s in sections_list if s['level'] == 0]
    internal_nodes = [s for s in sections_list if s['children_ids'] and s['level'] > 0]
    
    results = []
    successful = 0
    failed = 0
    
    # root 노드 처리
    for node in root_nodes:
        try:
            filename = create_node_file(node, sections, output_path)
            leaf_count = len(get_leaf_descendants(node['id'], sections))
            
            results.append({
                'node_type': 'root',
                'title': node['title'],
                'filename': filename,
                'leaf_count': leaf_count,
                'status': 'success'
            })
            successful += 1
            print(f"✅ {filename} (리프 {leaf_count}개)")
            
        except Exception as e:
            results.append({
                'node_type': 'root',
                'title': node['title'],
                'filename': None,
                'status': 'error',
                'error': str(e)
            })
            failed += 1
            print(f"❌ {node['title']}: {e}")
    
    # internal 노드 처리
    for node in internal_nodes:
        try:
            filename = create_node_file(node, sections, output_path)
            leaf_count = len(get_leaf_descendants(node['id'], sections))
            
            results.append({
                'node_type': 'internal',
                'title': node['title'],
                'level': node['level'],
                'filename': filename,
                'leaf_count': leaf_count,
                'status': 'success'
            })
            successful += 1
            print(f"✅ {filename} (리프 {leaf_count}개)")
            
        except Exception as e:
            results.append({
                'node_type': 'internal',
                'title': node['title'],
                'level': node['level'],
                'filename': None,
                'status': 'error',
                'error': str(e)
            })
            failed += 1
            print(f"❌ {node['title']}: {e}")
    
    return {
        'total_nodes': len(root_nodes) + len(internal_nodes),
        'root_nodes': len(root_nodes),
        'internal_nodes': len(internal_nodes),
        'successful': successful,
        'failed': failed,
        'results': results
    }


def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JSON 구조에서 root/internal 노드 파일들 생성')
    parser.add_argument('sections_json', help='섹션 구조 JSON 파일 경로')
    parser.add_argument('output_dir', help='출력 디렉토리 경로')
    
    args = parser.parse_args()
    
    if not Path(args.sections_json).exists():
        print(f"❌ JSON 파일을 찾을 수 없습니다: {args.sections_json}")
        return
    
    print("🎯 노드 파일 생성기")
    print("=" * 50)
    print(f"📋 구조: {args.sections_json}")
    print(f"📂 출력: {args.output_dir}")
    print()
    
    try:
        summary = create_all_node_files(args.sections_json, args.output_dir)
        
        print(f"\n📊 작업 완료:")
        print(f"   - 총 노드: {summary['total_nodes']}개")
        print(f"   - Root: {summary['root_nodes']}개")
        print(f"   - Internal: {summary['internal_nodes']}개")
        print(f"   - 성공: {summary['successful']}개")
        print(f"   - 실패: {summary['failed']}개")
        
        # 실패한 노드들 상세 정보
        failed_results = [r for r in summary['results'] if r['status'] != 'success']
        if failed_results:
            print(f"\n⚠️  실패한 노드들:")
            for result in failed_results:
                print(f"   - {result['title']}: {result.get('error', '알 수 없는 오류')}")
        
        print(f"\n✨ 노드 파일들이 '{args.output_dir}'에 저장되었습니다!")
        
    except Exception as e:
        print(f"❌ 작업 실패: {e}")


if __name__ == "__main__":
    main()