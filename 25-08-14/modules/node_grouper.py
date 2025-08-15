"""
생성 시간: 2025-08-14 11:35:00 KST
핵심 내용: 독립적인 노드 그룹화 및 정렬 시스템 - JSON 딕셔너리 직접 처리
상세 내용:
    - NodeGrouper 클래스 (라인 18-): JSON 노드 데이터 직접 처리
    - load_nodes_from_json() (라인 26-): JSON 파일에서 노드 데이터 로드
    - group_and_sort_nodes() (라인 43-): 부모 노드 그룹화 및 레벨별 정렬  
    - get_processing_order() (라인 70-): 하위→상위 처리 순서 생성
    - filter_parent_nodes() (라인 77-): 자식이 있는 노드만 필터링
    - Node 클래스 의존성 완전 제거
상태: 활성
주소: node_grouper
참조: dialectical_synthesis_processor_v3.py (NodeGrouper 클래스 분리)
"""

import json
from pathlib import Path
from typing import List, Dict, Any


class NodeGrouper:
    """노드 그룹화 및 정렬 로직 전담 클래스 - JSON 딕셔너리 직접 처리"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.nodes_data = []
    
    def load_nodes_from_json(self, json_path: str) -> bool:
        """JSON 파일에서 노드 데이터 로드"""
        try:
            json_file = Path(json_path)
            if not json_file.exists():
                if self.logger:
                    self.logger.log_error("JSON로드", f"파일 없음: {json_path}")
                return False
            
            with open(json_file, 'r', encoding='utf-8') as f:
                self.nodes_data = json.load(f)
            
            if self.logger:
                self.logger.log_operation("JSON로드", "성공", {"노드수": len(self.nodes_data)})
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_error("JSON로드", e)
            return False
    
    def group_and_sort_nodes(self, nodes_data: List[Dict[str, Any]] = None) -> Dict[int, List[Dict[str, Any]]]:
        """부모 노드들을 레벨별로 그룹화, 하위 수준(높은 level)이 앞에 위치하게 정렬"""
        try:
            # 노드 데이터 결정
            target_nodes = nodes_data if nodes_data is not None else self.nodes_data
            
            # 1. 부모 노드들만 필터링 (자식이 있는 노드)
            parent_nodes = self.filter_parent_nodes(target_nodes)
            
            # 2. 레벨별로 그룹화
            level_groups = {}
            for node in parent_nodes:
                level = node.get("level", 0)
                if level not in level_groups:
                    level_groups[level] = []
                level_groups[level].append(node)
            
            # 3. 각 레벨 내에서 제목별 정렬
            for level in level_groups:
                level_groups[level].sort(key=lambda x: x.get("title", ""))
            
            # 4. 레벨별로 정렬 (높은 레벨이 앞에 - 하위 수준 노드가 먼저)
            sorted_groups = dict(sorted(level_groups.items(), key=lambda x: x[0], reverse=True))
            
            if self.logger:
                self.logger.log_operation("노드그룹화", "완료", 
                                        {"레벨수": len(sorted_groups), 
                                         "총부모노드수": sum(len(nodes) for nodes in sorted_groups.values())})
            
            return sorted_groups
            
        except Exception as e:
            if self.logger:
                self.logger.log_error("노드그룹화", e)
            return {}
    
    def get_processing_order(self, grouped_nodes: Dict[int, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """처리 순서에 따른 노드 리스트 반환 - 높은 레벨(하위 수준)부터"""
        processing_order = []
        
        # 높은 레벨부터 처리 (하위 수준 노드가 먼저)
        for level in sorted(grouped_nodes.keys(), reverse=True):
            processing_order.extend(grouped_nodes[level])
        
        return processing_order
    
    def filter_parent_nodes(self, nodes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """자식이 있는 노드만 필터링"""
        parent_nodes = []
        for node in nodes_data:
            children_ids = node.get("children_ids", [])
            if children_ids and len(children_ids) > 0:
                parent_nodes.append(node)
        return parent_nodes
    
    def print_grouped_structure(self, grouped_nodes: Dict[int, List[Dict[str, Any]]]):
        """그룹화된 구조를 시각적으로 출력"""
        print("\n📋 그룹화된 노드 구조:")
        print("=" * 60)
        
        for level in sorted(grouped_nodes.keys(), reverse=True):
            nodes = grouped_nodes[level]
            print(f"레벨 {level} ({len(nodes)}개 노드):")
            for node in nodes:
                title = node.get("title", "제목없음")
                node_id = node.get("id", -1)
                children_count = len(node.get("children_ids", []))
                print(f"  - [{node_id:02d}] {title} (자식: {children_count}개)")
        
        print("=" * 60)


def main():
    """테스트 실행"""
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/nodes.json"
    
    grouper = NodeGrouper()
    
    print("노드 그룹화 시스템 테스트")
    print("=" * 50)
    
    # 1. JSON 로드
    if not grouper.load_nodes_from_json(json_path):
        print("❌ JSON 로드 실패")
        return
    
    # 2. 그룹화 및 정렬
    grouped_nodes = grouper.group_and_sort_nodes()
    
    # 3. 구조 출력
    grouper.print_grouped_structure(grouped_nodes)
    
    # 4. 처리 순서 출력
    processing_order = grouper.get_processing_order(grouped_nodes)
    print(f"\n🎯 처리 순서 ({len(processing_order)}개 노드):")
    for i, node in enumerate(processing_order):
        title = node.get("title", "제목없음")
        level = node.get("level", 0)
        print(f"  {i+1:02d}. [레벨{level}] {title}")


if __name__ == "__main__":
    main()