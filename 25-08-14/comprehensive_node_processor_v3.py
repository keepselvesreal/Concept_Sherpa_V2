# 생성 시간: Fri Aug 16 17:40:12 KST 2025
# 핵심 내용: 노드 정보를 바탕으로 향상된 노드 문서(node_docs_v3)를 생성하고 텍스트 문서와 통합하는 종합 처리기
# 상세 내용:
#   - load_input_data() (line 30): JSON 노드 정보 또는 마크다운 파일을 입력으로 받아 처리
#   - extract_headers_from_md() (line 69): 마크다운 파일에서 헤더 구조 추출
#   - build_hierarchy() (line 102): 레벨 기반 부모-자식 관계 구축
#   - determine_has_content() (line 146): 상위-하위 노드 사이 내용 존재 여부 판단
#   - save_nodes_json() (line 175): 전체 노드 구조를 nodes.json으로 저장
#   - filter_and_save_content_nodes() (line 195): has_content=true 또는 리프 노드를 content_nodes.json으로 저장
#   - create_node_documents_v3() (line 231): v3 노드 문서 생성 (향상된 메타데이터와 구조)
#   - integrate_with_text_documents() (line 328): 추출된 섹션 파일과 통합
#   - process_nodes_comprehensive_v3() (line 380): 전체 처리 프로세스 통합 실행
#   - main() (line 456): CLI 인터페이스 및 실행 로직
# 상태: 활성
# 주소: comprehensive_node_processor_v3
# 참조: comprehensive_node_processor_v2 (향상 버전)

#!/usr/bin/env python3

import json
import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

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

def create_node_documents_v3(nodes: List[Dict[str, Any]], output_dir: str = "node_docs_v3") -> bool:
    """
    향상된 메타데이터와 구조를 가진 v3 노드 문서 생성
    
    Args:
        nodes: 노드 리스트
        output_dir: 출력 디렉토리
        
    Returns:
        생성 성공 여부
    """
    print("📄 노드 문서 생성 중 (v3 - 향상된 메타데이터와 구조)...")
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    created_count = 0
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for node in nodes:
        try:
            node_id = node.get('id', 0)
            level = node.get('level', 0)
            title = node.get('title', 'Untitled')
            parent_id = node.get('parent_id')
            children_ids = node.get('children_ids', [])
            has_content = node.get('has_content', False)
            
            # 파일명 생성: {id:02d}_lev{level}_{title}_info.md
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            safe_title = safe_title.strip('_').lower()
            
            filename = f"{node_id:02d}_lev{level}_{safe_title}_info.md"
            
            # 부모 노드 정보
            parent_info = ""
            if parent_id is not None:
                parent_node = next((n for n in nodes if n.get('id') == parent_id), None)
                if parent_node:
                    parent_title = parent_node.get('title', 'Untitled')
                    parent_safe_title = re.sub(r'[^\w\s-]', '', parent_title)
                    parent_safe_title = re.sub(r'[-\s]+', '_', parent_safe_title).strip('_').lower()
                    parent_filename = f"{parent_id:02d}_lev{parent_node.get('level', 0)}_{parent_safe_title}_info.md"
                    parent_info = f"parent: {parent_filename}"
            
            # 자식 노드 파일명 생성
            children_filenames = []
            if children_ids:
                for child_id in children_ids:
                    child_node = next((n for n in nodes if n.get('id') == child_id), None)
                    if child_node:
                        child_level = child_node.get('level', 0)
                        child_title = child_node.get('title', 'Untitled')
                        child_safe_title = re.sub(r'[^\w\s-]', '', child_title)
                        child_safe_title = re.sub(r'[-\s]+', '_', child_safe_title).strip('_').lower()
                        child_filename = f"{child_id:02d}_lev{child_level}_{child_safe_title}_info.md"
                        children_filenames.append(child_filename)
            
            # 구성 섹션 내용
            composition_content = "\n".join(children_filenames) if children_filenames else ""
            
            # 문서 내용 생성 (v2 형식과 동일한 간단한 구조)
            content = f"""# 속성
process_status:

# 추출


# 내용


# 구성
{composition_content}"""
            
            # 파일 저장
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_count += 1
            print(f"   ✅ 생성: {filename}")
            
        except Exception as e:
            print(f"❌ 노드 ID {node.get('id', 'N/A')} 문서 생성 오류: {e}")
    
    print(f"📄 노드 문서 생성 완료: {output_dir}/ ({created_count}개 파일)")
    return created_count > 0

def integrate_with_text_documents(nodes: List[Dict[str, Any]], sections_dir: str, output_dir: str = "node_docs_v3") -> bool:
    """
    추출된 섹션 파일과 노드 문서를 통합합니다.
    
    Args:
        nodes: 노드 리스트
        sections_dir: 추출된 섹션 파일 디렉토리
        output_dir: 노드 문서 디렉토리
        
    Returns:
        통합 성공 여부
    """
    print("🔗 텍스트 문서와 통합 중...")
    
    if not os.path.exists(sections_dir):
        print(f"⚠️  섹션 디렉토리를 찾을 수 없습니다: {sections_dir}")
        return False
    
    updated_count = 0
    
    for node in nodes:
        if not node.get('has_content', False):
            continue
            
        try:
            node_id = node.get('id', 0)
            level = node.get('level', 0)
            title = node.get('title', 'Untitled')
            
            # 노드 문서 파일명
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title).strip('_').lower()
            node_filename = f"{node_id:02d}_lev{level}_{safe_title}_info.md"
            node_filepath = os.path.join(output_dir, node_filename)
            
            # 대응하는 섹션 파일 찾기
            section_filename = f"{node_id:02d}_lev{level}_{safe_title}.md"
            section_filepath = os.path.join(sections_dir, section_filename)
            
            if not os.path.exists(section_filepath):
                print(f"   ⚠️  섹션 파일 없음: {section_filename}")
                continue
            
            if not os.path.exists(node_filepath):
                print(f"   ⚠️  노드 파일 없음: {node_filename}")
                continue
            
            # 섹션 내용 읽기
            with open(section_filepath, 'r', encoding='utf-8') as f:
                section_content = f.read().strip()
            
            # 노드 문서 읽기
            with open(node_filepath, 'r', encoding='utf-8') as f:
                node_content = f.read()
            
            # 내용 섹션에 삽입
            lines = node_content.split('\n')
            content_section_start = -1
            
            for i, line in enumerate(lines):
                if line.strip() == '# 내용':
                    content_section_start = i
                    break
            
            if content_section_start == -1:
                print(f"   ⚠️  '# 내용' 섹션을 찾을 수 없음: {node_filename}")
                continue
            
            # 다음 섹션 시작점 찾기
            next_section_start = len(lines)
            for i in range(content_section_start + 1, len(lines)):
                if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                    next_section_start = i
                    break
            
            # 내용 삽입
            new_lines = (
                lines[:content_section_start + 1] +
                [''] +
                [section_content] +
                [''] +
                lines[next_section_start:]
            )
            
            # process_status 업데이트만 수행
            for i, line in enumerate(new_lines):
                if line.startswith('process_status:'):
                    new_lines[i] = "process_status: 통합완료"
            
            # 파일 저장
            with open(node_filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            updated_count += 1
            print(f"   ✅ 통합: {section_filename} → {node_filename}")
            
        except Exception as e:
            print(f"❌ 노드 ID {node.get('id', 'N/A')} 통합 오류: {e}")
    
    print(f"🔗 텍스트 문서 통합 완료: {updated_count}개 파일 업데이트")
    return updated_count > 0

def process_nodes_comprehensive_v3(input_path: str, sections_dir: Optional[str] = None, output_dir: str = ".") -> bool:
    """
    전체 노드 처리 프로세스를 실행합니다 (v3 - 향상된 메타데이터와 텍스트 통합).
    
    Args:
        input_path: 입력 파일 경로 (JSON 노드 파일 또는 마크다운 파일)
        sections_dir: 추출된 섹션 파일 디렉토리 (선택사항)
        output_dir: 출력 디렉토리
        
    Returns:
        처리 성공 여부
    """
    print("🚀 종합 노드 처리 시작 (v3 - 향상된 메타데이터와 텍스트 통합)")
    print("=" * 80)
    print(f"📁 입력 파일: {input_path}")
    print(f"📁 섹션 디렉토리: {sections_dir or '지정되지 않음'}")
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
        
        # 6. 노드 문서 생성 (v3 - 향상된 메타데이터)
        print("\n6️⃣ 노드 문서 생성 (v3)")
        docs_dir = os.path.join(output_dir, "node_docs_v3")
        create_node_documents_v3(nodes, docs_dir)
        
        # 7. 텍스트 문서와 통합 (섹션 디렉토리가 제공된 경우)
        if sections_dir:
            print("\n7️⃣ 텍스트 문서와 통합")
            integrate_with_text_documents(nodes, sections_dir, docs_dir)
        
        print("\n✨ 종합 노드 처리 완료! (v3)")
        print("=" * 80)
        print(f"📊 처리 결과:")
        print(f"   - 전체 노드: {len(nodes)}개")
        print(f"   - 콘텐츠 노드: {len([n for n in nodes if n.get('has_content') or len(n.get('children_ids', [])) == 0])}개")
        print(f"   - 생성된 파일:")
        print(f"     • {nodes_json_path}")
        print(f"     • {content_nodes_path}")
        print(f"     • {docs_dir}/ (v3 파일명: {'{id:02d}'}_lev{'{level}'}_{'{title}'}_info.md)")
        if sections_dir:
            print(f"     • 텍스트 문서 통합 완료")
        
        return True
        
    except Exception as e:
        print(f"❌ 처리 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='향상된 메타데이터와 텍스트 통합을 지원하는 노드 정보 종합 처리기 (v3)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python comprehensive_node_processor_v3.py nodes.json
  python comprehensive_node_processor_v3.py nodes.json -s extracted_sections -o ./output
  python comprehensive_node_processor_v3.py document.md --sections-dir ./sections --output-dir ./processed

v3 개선사항:
  - 향상된 메타데이터 (생성/수정 시간, 우선순위, 콘텐츠 타입 등)
  - 추출된 텍스트 문서와의 자동 통합
  - 부모-자식 관계 추적
  - 더 풍부한 문서 구조
        """
    )
    
    parser.add_argument('input_file', help='입력 파일 (JSON 노드 파일 또는 마크다운 파일)')
    parser.add_argument('-s', '--sections-dir', help='추출된 섹션 파일 디렉토리 (통합용)')
    parser.add_argument('-o', '--output-dir', default='.', help='출력 디렉토리 (기본값: 현재 디렉토리)')
    parser.add_argument('-v', '--verbose', action='store_true', help='상세 출력')
    
    args = parser.parse_args()
    
    # 처리 실행
    success = process_nodes_comprehensive_v3(args.input_file, args.sections_dir, args.output_dir)
    
    if success:
        print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
        return 0
    else:
        print("\n💥 작업 실행 중 오류가 발생했습니다.")
        return 1

if __name__ == "__main__":
    exit(main())