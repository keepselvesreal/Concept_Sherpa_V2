"""
생성 시간: 2025-08-09 16:30:00 KST
핵심 내용: TOC JSON에서 리프 노드들을 level별, chapter별로 그룹화하여 JSON 파일로 저장하는 시스템
상세 내용:
    - TOCAnalyzer (라인 10-80): JSON 목차 데이터 분석 및 리프 노드 식별 기능
    - LeafNodeGrouper (라인 82-150): 리프 노드들을 level별, chapter별로 그룹화하는 기능
    - JSONFileManager (라인 152-200): 그룹화된 데이터를 JSON 파일로 저장하는 관리 기능
    - main 함수 (라인 202-250): 전체 프로세스 실행 및 결과 출력
상태: 초기 구현 완료
주소: leaf_node_organizer
참조: enhanced_toc_with_relationships.json 파일 구조 기반으로 구현
"""

import json
import os
from typing import List, Dict, Any, Set
from collections import defaultdict


class TOCAnalyzer:
    """TOC JSON 데이터를 분석하여 리프 노드들을 식별하는 클래스"""
    
    def __init__(self, toc_file_path: str):
        self.toc_file_path = toc_file_path
        self.toc_data = self.load_toc_data()
        self.node_dict = self.create_node_dict()
    
    def load_toc_data(self) -> List[Dict[str, Any]]:
        """목차 JSON 파일을 로드"""
        try:
            with open(self.toc_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"TOC 데이터 로드 성공: {len(data)}개 노드")
                return data
        except Exception as e:
            print(f"TOC 파일 로드 오류: {e}")
            return []
    
    def create_node_dict(self) -> Dict[int, Dict[str, Any]]:
        """노드 ID를 키로 하는 딕셔너리 생성"""
        node_dict = {}
        for node in self.toc_data:
            node_dict[node['id']] = node
        return node_dict
    
    def is_leaf_node(self, node: Dict[str, Any]) -> bool:
        """리프 노드인지 확인 (자식이 없는 노드)"""
        children_ids = node.get('children_ids', [])
        return len(children_ids) == 0
    
    def get_leaf_nodes(self) -> List[Dict[str, Any]]:
        """모든 리프 노드들을 반환"""
        leaf_nodes = []
        for node in self.toc_data:
            if self.is_leaf_node(node):
                # 페이지 수가 0보다 큰 리프 노드만 포함
                if node.get('page_count', 0) > 0:
                    leaf_nodes.append(node)
        
        print(f"리프 노드 {len(leaf_nodes)}개 발견")
        return leaf_nodes
    
    def get_parent_chain(self, node_id: int) -> List[Dict[str, Any]]:
        """노드의 부모 체인을 반환 (root까지)"""
        chain = []
        current_id = node_id
        
        while current_id is not None:
            if current_id in self.node_dict:
                current_node = self.node_dict[current_id]
                chain.append(current_node)
                current_id = current_node.get('parent_id')
            else:
                break
        
        # root부터 현재 노드까지 순서로 뒤집기
        chain.reverse()
        return chain
    
    def print_leaf_nodes_summary(self):
        """리프 노드 요약 출력"""
        leaf_nodes = self.get_leaf_nodes()
        level_counts = defaultdict(int)
        
        for node in leaf_nodes:
            level_counts[node['level']] += 1
        
        print("\n=== 리프 노드 레벨별 요약 ===")
        for level in sorted(level_counts.keys()):
            print(f"Level {level}: {level_counts[level]}개")


class LeafNodeGrouper:
    """리프 노드들을 level별, chapter별로 그룹화하는 클래스"""
    
    def __init__(self, analyzer: TOCAnalyzer):
        self.analyzer = analyzer
        self.leaf_nodes = analyzer.get_leaf_nodes()
    
    def group_by_level(self) -> Dict[int, List[Dict[str, Any]]]:
        """레벨별로 리프 노드들을 그룹화"""
        level_groups = defaultdict(list)
        
        for node in self.leaf_nodes:
            level = node['level']
            level_groups[level].append(node)
        
        return dict(level_groups)
    
    def group_by_level_and_chapter(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """레벨별, 챕터별로 리프 노드들을 그룹화"""
        result = defaultdict(lambda: defaultdict(list))
        
        for node in self.leaf_nodes:
            level = node['level']
            
            # 부모 체인에서 챕터 찾기 (level 0 또는 1)
            parent_chain = self.analyzer.get_parent_chain(node['id'])
            chapter_info = self.find_chapter_info(parent_chain, level)
            
            level_key = f"level_{level:02d}"
            chapter_key = chapter_info['key']
            
            # 추가 메타데이터 포함
            enriched_node = {
                **node,
                'chapter_info': chapter_info,
                'parent_chain': [{'id': p['id'], 'title': p['title'], 'level': p['level']} 
                                for p in parent_chain]
            }
            
            result[level_key][chapter_key].append(enriched_node)
        
        return dict(result)
    
    def find_chapter_info(self, parent_chain: List[Dict[str, Any]], current_level: int) -> Dict[str, Any]:
        """부모 체인에서 적절한 챕터 정보를 찾기"""
        # Level 0 또는 1인 가장 가까운 부모를 찾기
        for i in range(len(parent_chain) - 1, -1, -1):
            parent = parent_chain[i]
            if parent['level'] in [0, 1]:
                return {
                    'id': parent['id'],
                    'title': parent['title'],
                    'level': parent['level'],
                    'key': f"chapter_{parent['id']:03d}_{self.sanitize_title(parent['title'])}"
                }
        
        # 적절한 챕터를 찾지 못한 경우
        return {
            'id': -1,
            'title': 'Unknown',
            'level': -1,
            'key': 'chapter_unknown'
        }
    
    def sanitize_title(self, title: str) -> str:
        """제목을 파일명으로 사용가능하도록 정리"""
        invalid_chars = '<>:"/\\|?*#'
        for char in invalid_chars:
            title = title.replace(char, '_')
        return title.strip()[:50]  # 길이 제한
    
    def print_grouping_summary(self):
        """그룹화 결과 요약 출력"""
        grouped = self.group_by_level_and_chapter()
        
        print("\n=== 그룹화 결과 요약 ===")
        for level_key in sorted(grouped.keys()):
            level_data = grouped[level_key]
            total_nodes = sum(len(nodes) for nodes in level_data.values())
            print(f"\n{level_key.upper()}: {total_nodes}개 리프 노드, {len(level_data)}개 챕터")
            
            for chapter_key in sorted(level_data.keys()):
                nodes = level_data[chapter_key]
                if nodes:  # 빈 리스트가 아닌 경우만
                    chapter_title = nodes[0]['chapter_info']['title'][:50]
                    print(f"  - {chapter_key}: {len(nodes)}개 노드 ({chapter_title}...)")


class JSONFileManager:
    """JSON 파일 저장 및 관리를 담당하는 클래스"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.create_output_directory()
    
    def create_output_directory(self):
        """출력 디렉토리 생성"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"출력 디렉토리 생성: {self.output_dir}")
    
    def save_level_groups(self, level_groups: Dict[int, List[Dict[str, Any]]]):
        """레벨별 그룹을 개별 JSON 파일로 저장"""
        for level, nodes in level_groups.items():
            filename = f"level_{level:02d}_leaf_nodes.json"
            filepath = os.path.join(self.output_dir, filename)
            
            data = {
                'level': level,
                'node_count': len(nodes),
                'created_at': '2025-08-09',
                'nodes': nodes
            }
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"레벨 {level} 저장 완료: {filename} ({len(nodes)}개 노드)")
            except Exception as e:
                print(f"레벨 {level} 저장 오류: {e}")
    
    def save_level_chapter_groups(self, grouped_data: Dict[str, Dict[str, List[Dict[str, Any]]]]):
        """레벨별, 챕터별 그룹을 JSON 파일로 저장"""
        for level_key, level_data in grouped_data.items():
            for chapter_key, nodes in level_data.items():
                if not nodes:  # 빈 리스트 스킵
                    continue
                
                filename = f"{level_key}_{chapter_key}_leaf_nodes.json"
                filepath = os.path.join(self.output_dir, filename)
                
                chapter_info = nodes[0]['chapter_info'] if nodes else {}
                data = {
                    'level_key': level_key,
                    'chapter_key': chapter_key,
                    'chapter_info': chapter_info,
                    'node_count': len(nodes),
                    'created_at': '2025-08-09',
                    'nodes': nodes
                }
                
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    chapter_title = chapter_info.get('title', 'Unknown')[:30]
                    print(f"저장 완료: {filename} ({len(nodes)}개 노드, {chapter_title}...)")
                except Exception as e:
                    print(f"저장 오류 ({filename}): {e}")


def main():
    """메인 실행 함수"""
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/leaf_nodes_by_level_chapter"
    
    try:
        print("=== 리프 노드 조직화 시작 ===")
        
        # TOC 분석기 초기화
        analyzer = TOCAnalyzer(toc_file)
        analyzer.print_leaf_nodes_summary()
        
        # 리프 노드 그룹화
        grouper = LeafNodeGrouper(analyzer)
        grouper.print_grouping_summary()
        
        # JSON 파일 관리자 초기화
        file_manager = JSONFileManager(output_dir)
        
        # 레벨별 그룹 저장
        print(f"\n=== 레벨별 JSON 파일 저장 ===")
        level_groups = grouper.group_by_level()
        file_manager.save_level_groups(level_groups)
        
        # 레벨별, 챕터별 그룹 저장
        print(f"\n=== 레벨별, 챕터별 JSON 파일 저장 ===")
        level_chapter_groups = grouper.group_by_level_and_chapter()
        file_manager.save_level_chapter_groups(level_chapter_groups)
        
        print(f"\n=== 작업 완료 ===")
        print(f"모든 파일이 {output_dir}에 저장되었습니다.")
        
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")


if __name__ == "__main__":
    main()