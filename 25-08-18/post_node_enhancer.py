# 생성 시간: 2025-08-18 17:25:00 KST
# 핵심 내용: 포스트 전용 노드 JSON에 부모-자식 관계 및 has_content 필드를 추가하는 모듈
# 상세 내용:
#   - PostNodeEnhancer 클래스 (라인 21-170): 포스트 노드 정보 확장 기능
#   - build_hierarchy 메서드 (라인 31-75): 부모-자식 관계 구축
#   - analyze_content_for_all_nodes 메서드 (라인 77-105): 모든 노드 직접 콘텐츠 분석
#   - extract_node_content 메서드 (라인 107-140): 개별 노드 콘텐츠 추출
#   - enhance_nodes 메서드 (라인 142-160): 전체 노드 확장 처리
#   - save_enhanced_json 메서드 (라인 162-170): 확장된 노드 JSON 저장
#   - main 함수 (라인 172-210): CLI 인터페이스
# 상태: 활성
# 주소: post_node_enhancer
# 참조: node_enhancer (부모-자식 관계 로직)

import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional


class PostNodeEnhancer:
    def __init__(self):
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+)', re.MULTILINE)

    def build_hierarchy(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """레벨 기반으로 부모-자식 관계를 구축"""
        print("🔗 부모-자식 관계 구축 중...")
        
        # 각 노드에 관계 필드 초기화
        for node in nodes:
            node['parent_id'] = None
            node['children_ids'] = []
        
        # 부모-자식 관계 구축
        for i, current_node in enumerate(nodes):
            current_level = current_node.get('level', 0)
            
            # 현재 노드의 부모 찾기 (더 낮은 레벨의 가장 가까운 이전 노드)
            for j in range(i-1, -1, -1):
                potential_parent = nodes[j]
                parent_level = potential_parent.get('level', 0)
                
                if parent_level < current_level:
                    # 부모 발견
                    current_node['parent_id'] = potential_parent['id']
                    potential_parent['children_ids'].append(current_node['id'])
                    break
        
        # 계층 구조 통계 출력
        root_nodes = [n for n in nodes if n['parent_id'] is None]
        leaf_nodes = [n for n in nodes if len(n['children_ids']) == 0]
        intermediate_nodes = [n for n in nodes if n['parent_id'] is not None and len(n['children_ids']) > 0]
        
        print(f"   ✅ 루트 노드: {len(root_nodes)}개")
        print(f"   ✅ 중간 노드: {len(intermediate_nodes)}개")
        print(f"   ✅ 리프 노드: {len(leaf_nodes)}개")
        
        return nodes

    def analyze_content_for_all_nodes(self, nodes: List[Dict[str, Any]], markdown_content: str) -> List[Dict[str, Any]]:
        """모든 노드에 대해 직접 콘텐츠 존재 여부를 분석"""
        print("📝 모든 노드의 has_content 필드 직접 분석 중...")
        
        content_count = 0
        
        for i, node in enumerate(nodes):
            # 각 노드의 실제 콘텐츠 추출
            node_content = self.extract_node_content(node, nodes, i, markdown_content)
            
            # 콘텐츠 존재 여부 판단
            if node_content and node_content.strip():
                # 실제 의미있는 콘텐츠가 있는지 확인 (빈 줄, 공백만 있는 경우 제외)
                cleaned_content = re.sub(r'\s+', ' ', node_content.strip())
                if len(cleaned_content) > 0:
                    node['has_content'] = True
                    content_count += 1
                else:
                    node['has_content'] = False
            else:
                node['has_content'] = False
        
        print(f"   ✅ has_content=True 노드: {content_count}개")
        print(f"   ✅ has_content=False 노드: {len(nodes) - content_count}개")
        
        return nodes

    def extract_node_content(self, current_node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                           current_index: int, markdown_content: str) -> Optional[str]:
        """개별 노드의 실제 콘텐츠를 추출"""
        try:
            # 현재 노드의 헤더 패턴 생성
            current_level = current_node.get('level', 0)
            current_title = current_node.get('title', '')
            current_header_pattern = '#' * (current_level + 1) + r'\s+' + re.escape(current_title)
            
            # 현재 헤더 위치 찾기
            current_match = re.search(current_header_pattern, markdown_content)
            if not current_match:
                return None
            
            start_pos = current_match.end()
            
            # 다음 헤더 위치 찾기 (현재 레벨 이하의 다음 헤더)
            end_pos = len(markdown_content)  # 기본값: 문서 끝
            
            for j in range(current_index + 1, len(all_nodes)):
                next_node = all_nodes[j]
                next_level = next_node.get('level', 0)
                next_title = next_node.get('title', '')
                
                # 현재 레벨 이하의 헤더를 찾으면 콘텐츠 끝
                if next_level <= current_level:
                    next_header_pattern = '#' * (next_level + 1) + r'\s+' + re.escape(next_title)
                    next_match = re.search(next_header_pattern, markdown_content[start_pos:])
                    if next_match:
                        end_pos = start_pos + next_match.start()
                        break
            
            # 콘텐츠 추출
            if start_pos < end_pos:
                content = markdown_content[start_pos:end_pos]
                return content.strip()
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ 노드 {current_node.get('id', 'N/A')} 콘텐츠 추출 중 오류: {e}")
            return None

    def enhance_nodes(self, nodes: List[Dict[str, Any]], markdown_content: str) -> List[Dict[str, Any]]:
        """노드 정보에 부모-자식 관계와 has_content 필드 추가"""
        print(f"🚀 포스트 노드 정보 확장 시작: {len(nodes)}개 노드")
        
        # 1. 부모-자식 관계 구축
        nodes = self.build_hierarchy(nodes)
        
        # 2. 모든 노드에 대해 직접 콘텐츠 분석
        if markdown_content:
            nodes = self.analyze_content_for_all_nodes(nodes, markdown_content)
        else:
            print("⚠️ 마크다운 내용이 제공되지 않아 has_content 필드를 False로 설정")
            for node in nodes:
                node['has_content'] = False
        
        print("✅ 포스트 노드 정보 확장 완료")
        return nodes

    def save_enhanced_json(self, nodes: List[Dict[str, Any]], output_path: str):
        """확장된 노드 리스트를 JSON 파일로 저장"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        print(f"✅ 확장된 포스트 노드 JSON 저장 완료: {output_path}")
        print(f"📊 총 {len(nodes)}개 노드 (부모-자식 관계 및 직접 분석된 has_content 포함)")


def main():
    parser = argparse.ArgumentParser(description='포스트용 노드 JSON에 부모-자식 관계 및 has_content 필드 추가')
    parser.add_argument('input_json', help='입력 노드 JSON 파일 경로')
    parser.add_argument('markdown_file', help='마크다운 파일 경로 (has_content 직접 분석용)')
    parser.add_argument('-o', '--output', help='출력 JSON 파일 경로')
    
    args = parser.parse_args()
    
    # 출력 파일 경로 설정
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input_json)
        output_path = input_path.parent / f"{input_path.stem}_enhanced.json"
    
    enhancer = PostNodeEnhancer()
    
    try:
        # 입력 JSON 로드
        print(f"📥 노드 JSON 로드: {args.input_json}")
        with open(args.input_json, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # 마크다운 내용 로드 (필수)
        print(f"📄 마크다운 파일 로드: {args.markdown_file}")
        with open(args.markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 노드 확장
        enhanced_nodes = enhancer.enhance_nodes(nodes, markdown_content)
        
        # 결과 미리보기
        print(f"\n📋 확장된 노드 미리보기:")
        for node in enhanced_nodes[:3]:  # 처음 3개만 출력
            parent_info = f" (부모: {node['parent_id']})" if node['parent_id'] is not None else " (루트)"
            children_info = f" 자식: {len(node['children_ids'])}개" if node['children_ids'] else ""
            content_info = " [내용있음]" if node['has_content'] else " [내용없음]"
            print(f"  - ID {node['id']} (level {node['level']}): {node['title']}{parent_info}{children_info}{content_info}")
        
        if len(enhanced_nodes) > 3:
            print(f"  ... 및 {len(enhanced_nodes) - 3}개 추가 노드")
        
        # 확장된 JSON 저장
        enhancer.save_enhanced_json(enhanced_nodes, output_path)
        
    except FileNotFoundError as e:
        print(f"❌ 파일을 찾을 수 없습니다: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()