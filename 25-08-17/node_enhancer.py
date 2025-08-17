# 생성 시간: 2025-08-17 17:38:23 KST
# 핵심 내용: 노드 JSON에 부모-자식 관계 및 has_content 필드를 추가하는 모듈
# 상세 내용:
#   - NodeEnhancer 클래스 (라인 20-120): 노드 정보 확장 기능
#   - build_hierarchy 메서드 (라인 30-65): 부모-자식 관계 구축
#   - determine_has_content 메서드 (라인 67-85): has_content 필드 판단
#   - enhance_nodes 메서드 (라인 87-110): 전체 노드 확장 처리
#   - save_enhanced_json 메서드 (라인 112-120): 확장된 노드 JSON 저장
#   - main 함수 (라인 122-140): CLI 인터페이스
# 상태: 활성
# 주소: node_enhancer
# 참조: comprehensive_node_processor_v3 (부모-자식 관계 및 has_content 로직)

import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any


class NodeEnhancer:
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
        
        # 통계 출력
        root_nodes = [n for n in nodes if n['parent_id'] is None]
        leaf_nodes = [n for n in nodes if len(n['children_ids']) == 0]
        
        print(f"   ✅ 루트 노드: {len(root_nodes)}개")
        print(f"   ✅ 리프 노드: {len(leaf_nodes)}개")
        
        return nodes
    
    def determine_has_content(self, nodes: List[Dict[str, Any]], markdown_content: str = None) -> List[Dict[str, Any]]:
        """상위-하위 노드 사이에 내용이 존재하는지 판단"""
        print("📝 has_content 필드 판단 중...")
        
        content_count = 0
        
        for i, node in enumerate(nodes):
            # 기본값을 False로 설정
            node['has_content'] = False
            
            # 컨텐츠를 가질 수 있는 경우만 True로 설정
            
            # 1. 리프 노드는 항상 content 존재
            if len(node.get('children_ids', [])) == 0:
                node['has_content'] = True
                content_count += 1
            else:
                # 2. 비-리프 노드: 다음 노드가 더 깊은 레벨이면서 실제 텍스트가 존재하는 경우
                current_level = node.get('level', 0)
                
                # 다음 노드 확인
                if i + 1 < len(nodes):
                    next_node = nodes[i + 1]
                    next_level = next_node.get('level', 0)
                    
                    # 다음 노드가 더 깊은 레벨이면 실제 텍스트 존재 여부 확인
                    if next_level > current_level and markdown_content:
                        # 실제 마크다운에서 현재 노드와 다음 노드 사이에 텍스트가 있는지 확인
                        has_actual_content = self._check_content_between_nodes(node, next_node, markdown_content)
                        if has_actual_content:
                            node['has_content'] = True
                            content_count += 1
        
        print(f"   ✅ has_content=True 노드: {content_count}개")
        
        return nodes
    
    def _check_content_between_nodes(self, current_node: Dict[str, Any], next_node: Dict[str, Any], markdown_content: str) -> bool:
        """현재 노드와 다음 노드 사이에 실제 텍스트 내용이 있는지 확인"""
        try:
            # 현재 노드와 다음 노드의 헤더 생성
            current_header = '#' * (current_node['level'] + 1) + ' ' + current_node['title']
            next_header = '#' * (next_node['level'] + 1) + ' ' + next_node['title']
            
            # 현재 헤더 위치 찾기
            current_match = re.search(re.escape(current_header), markdown_content)
            if not current_match:
                return False
            
            # 다음 헤더 위치 찾기
            next_match = re.search(re.escape(next_header), markdown_content)
            if not next_match:
                return True  # 다음 헤더가 없으면 끝까지 내용이 있다고 가정
            
            # 두 헤더 사이의 텍스트 추출
            start_pos = current_match.end()
            end_pos = next_match.start()
            
            if start_pos >= end_pos:
                return False
            
            between_text = markdown_content[start_pos:end_pos].strip()
            
            # 빈 줄만 있거나 내용이 없으면 False, 실제 내용이 있으면 True
            return len(between_text) > 0 and not re.match(r'^\s*$', between_text)
            
        except Exception as e:
            print(f"   ⚠️ 텍스트 확인 중 오류 (노드 {current_node.get('id', 'N/A')}): {e}")
            return False
    
    def enhance_nodes(self, nodes: List[Dict[str, Any]], markdown_content: str = None) -> List[Dict[str, Any]]:
        """노드 정보에 부모-자식 관계와 has_content 필드 추가"""
        print(f"🚀 노드 정보 확장 시작: {len(nodes)}개 노드")
        
        # 1. 부모-자식 관계 구축
        nodes = self.build_hierarchy(nodes)
        
        # 2. has_content 필드 판단 (마크다운 내용 포함)
        nodes = self.determine_has_content(nodes, markdown_content)
        
        print("✅ 노드 정보 확장 완료")
        return nodes
    
    def save_enhanced_json(self, nodes: List[Dict[str, Any]], output_path: str):
        """확장된 노드 리스트를 JSON 파일로 저장"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        print(f"✅ 확장된 노드 JSON 저장 완료: {output_path}")
        print(f"📊 총 {len(nodes)}개 노드 (부모-자식 관계 및 has_content 포함)")


def main():
    parser = argparse.ArgumentParser(description='노드 JSON에 부모-자식 관계 및 has_content 필드 추가')
    parser.add_argument('input_json', help='입력 노드 JSON 파일 경로')
    parser.add_argument('-m', '--markdown', help='마크다운 파일 경로 (has_content 판단용)')
    parser.add_argument('-o', '--output', help='출력 JSON 파일 경로')
    
    args = parser.parse_args()
    
    # 출력 파일 경로 설정
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input_json)
        output_path = input_path.parent / f"{input_path.stem}_enhanced.json"
    
    enhancer = NodeEnhancer()
    
    try:
        # 입력 JSON 로드
        print(f"📥 노드 JSON 로드: {args.input_json}")
        with open(args.input_json, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # 마크다운 내용 로드 (선택사항)
        markdown_content = None
        if args.markdown:
            print(f"📄 마크다운 파일 로드: {args.markdown}")
            with open(args.markdown, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        
        # 노드 확장
        enhanced_nodes = enhancer.enhance_nodes(nodes, markdown_content)
        
        # 결과 미리보기
        print(f"\n📋 확장된 노드 미리보기:")
        for node in enhanced_nodes[:5]:  # 처음 5개만 출력
            parent_info = f" (부모: {node['parent_id']})" if node['parent_id'] is not None else " (루트)"
            children_info = f" 자식: {len(node['children_ids'])}개" if node['children_ids'] else ""
            content_info = " [내용있음]" if node['has_content'] else " [내용없음]"
            print(f"  - ID {node['id']} (level {node['level']}): {node['title']}{parent_info}{children_info}{content_info}")
        
        if len(enhanced_nodes) > 5:
            print(f"  ... 및 {len(enhanced_nodes) - 5}개 추가 노드")
        
        # 확장된 JSON 저장
        enhancer.save_enhanced_json(enhanced_nodes, output_path)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()