"""
생성 시간: 2025-08-12 11:54:04 KST
핵심 내용: JSON 구조 파싱 및 노드 관계 분석 시스템 - 일반화된 트리 구조 처리
상세 내용:
    - load_json_structure(json_path): JSON 파일 로드 및 구조 검증
    - Node 클래스: 노드 정보와 관계를 캡슐화
    - build_node_tree(json_data): JSON 데이터를 Node 트리로 변환
    - get_leaf_nodes(): 리프 노드 목록 반환
    - get_nodes_by_level(): 레벨별 노드 분류
    - get_processing_order(): 하위→상위 처리 순서 생성
    - map_node_to_text_file(node, text_base_path): 노드를 텍스트 파일 경로로 매핑
    - validate_text_files_exist(): 모든 리프 노드의 텍스트 파일 존재 확인
상태: 활성
주소: node_structure_analyzer
참조: chapter7_modified.json (테스트 데이터)
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class Node:
    """노드 정보와 관계를 캡슐화하는 클래스"""
    
    def __init__(self, node_data: dict):
        self.title = node_data.get("title", "")
        self.level = node_data.get("level", 0)
        self.id = node_data.get("id", -1)
        self.parent_id = node_data.get("parent_id")
        self.children_ids = node_data.get("children_ids", [])
        self.is_added_node = node_data.get("is_added_node", False)
        
        # 관계 객체들 (나중에 설정됨)
        self.parent = None
        self.children = []
    
    def is_leaf(self) -> bool:
        """리프 노드인지 확인"""
        return len(self.children_ids) == 0
    
    def is_root(self) -> bool:
        """루트 노드인지 확인"""
        return self.parent_id is None
    
    def is_internal(self) -> bool:
        """내부 노드인지 확인 (리프도 루트도 아닌 경우)"""
        return not self.is_leaf() and not self.is_root()
    
    def get_node_type(self) -> str:
        """노드 타입 반환"""
        if self.is_leaf():
            return "leaf"
        elif self.is_root():
            return "root"
        else:
            return "internal"
    
    def __str__(self):
        return f"Node(id={self.id}, title='{self.title}', level={self.level}, type={self.get_node_type()})"

class NodeStructureAnalyzer:
    """JSON 구조를 분석하고 노드 관계를 관리하는 클래스"""
    
    def __init__(self, json_path: str, text_base_path: str):
        self.json_path = Path(json_path)
        self.text_base_path = Path(text_base_path)
        self.nodes = {}  # id -> Node 매핑
        self.root_nodes = []
        
    def load_json_structure(self) -> bool:
        """JSON 파일 로드 및 구조 검증"""
        try:
            if not self.json_path.exists():
                print(f"❌ JSON 파일을 찾을 수 없습니다: {self.json_path}")
                return False
            
            with open(self.json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            if not isinstance(json_data, list):
                print(f"❌ JSON 데이터가 리스트 형태가 아닙니다")
                return False
            
            print(f"✅ JSON 구조 로드 성공: {len(json_data)}개 노드")
            
            # 노드 트리 구축
            return self.build_node_tree(json_data)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 오류: {e}")
            return False
        except Exception as e:
            print(f"❌ JSON 로드 중 오류: {e}")
            return False
    
    def build_node_tree(self, json_data: List[dict]) -> bool:
        """JSON 데이터를 Node 트리로 변환"""
        try:
            # 1. 모든 노드 객체 생성
            for node_data in json_data:
                node = Node(node_data)
                self.nodes[node.id] = node
            
            print(f"📋 노드 객체 생성 완료: {len(self.nodes)}개")
            
            # 2. 부모-자식 관계 설정
            for node in self.nodes.values():
                # 부모 설정
                if node.parent_id is not None:
                    if node.parent_id in self.nodes:
                        node.parent = self.nodes[node.parent_id]
                    else:
                        print(f"⚠️ 부모 노드를 찾을 수 없음: parent_id={node.parent_id}, node_id={node.id}")
                
                # 자식 설정
                for child_id in node.children_ids:
                    if child_id in self.nodes:
                        node.children.append(self.nodes[child_id])
                    else:
                        print(f"⚠️ 자식 노드를 찾을 수 없음: child_id={child_id}, node_id={node.id}")
            
            # 3. 루트 노드 식별
            self.root_nodes = [node for node in self.nodes.values() if node.is_root()]
            print(f"🌳 루트 노드 {len(self.root_nodes)}개 식별")
            
            # 4. 구조 검증
            return self.validate_tree_structure()
            
        except Exception as e:
            print(f"❌ 노드 트리 구축 중 오류: {e}")
            return False
    
    def validate_tree_structure(self) -> bool:
        """트리 구조 유효성 검증"""
        issues = []
        
        # 루트 노드 검증
        if not self.root_nodes:
            issues.append("루트 노드가 없습니다")
        
        # 각 노드 검증
        for node in self.nodes.values():
            # 부모-자식 일관성 검증
            if node.parent:
                if node not in node.parent.children:
                    issues.append(f"부모-자식 관계 불일치: node_id={node.id}")
            
            # 자식 노드들의 부모 검증
            for child in node.children:
                if child.parent != node:
                    issues.append(f"자식-부모 관계 불일치: child_id={child.id}, parent_id={node.id}")
        
        if issues:
            print("❌ 트리 구조 검증 실패:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        print("✅ 트리 구조 검증 성공")
        return True
    
    def get_leaf_nodes(self) -> List[Node]:
        """리프 노드 목록 반환"""
        return [node for node in self.nodes.values() if node.is_leaf()]
    
    def get_nodes_by_level(self) -> Dict[int, List[Node]]:
        """레벨별 노드 분류"""
        levels = {}
        for node in self.nodes.values():
            if node.level not in levels:
                levels[node.level] = []
            levels[node.level].append(node)
        return levels
    
    def get_processing_order(self) -> List[List[Node]]:
        """하위→상위 처리 순서 생성 (레벨별)"""
        levels = self.get_nodes_by_level()
        # 레벨이 높은 것부터 (리프 노드부터) 처리
        sorted_levels = sorted(levels.keys(), reverse=True)
        
        processing_order = []
        for level in sorted_levels:
            processing_order.append(levels[level])
        
        return processing_order
    
    def map_node_to_text_file(self, node: Node) -> Optional[Path]:
        """노드를 텍스트 파일 경로로 매핑"""
        if not node.is_leaf():
            return None  # 리프 노드만 기존 텍스트 파일과 매핑
        
        # 제목을 파일명으로 변환 (특수문자 처리)
        title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        text_file = self.text_base_path / f"{title}.md"
        
        return text_file if text_file.exists() else None
    
    def validate_text_files_exist(self) -> bool:
        """모든 리프 노드의 텍스트 파일 존재 확인"""
        leaf_nodes = self.get_leaf_nodes()
        missing_files = []
        existing_files = []
        
        print(f"📁 리프 노드 텍스트 파일 존재 확인 중... ({len(leaf_nodes)}개)")
        
        for node in leaf_nodes:
            text_file = self.map_node_to_text_file(node)
            if text_file and text_file.exists():
                existing_files.append((node, text_file))
                print(f"  ✅ {node.title} → {text_file.name}")
            else:
                missing_files.append(node)
                print(f"  ❌ {node.title} → 파일 없음")
        
        if missing_files:
            print(f"\n❌ 텍스트 파일이 없는 리프 노드 {len(missing_files)}개:")
            for node in missing_files:
                print(f"  - {node.title}")
            return False
        
        print(f"\n✅ 모든 리프 노드 텍스트 파일 존재 확인 완료 ({len(existing_files)}개)")
        return True
    
    def print_tree_structure(self):
        """트리 구조를 시각적으로 출력"""
        print("\n🌳 노드 트리 구조:")
        print("=" * 60)
        
        def print_node(node: Node, indent: int = 0):
            prefix = "  " * indent
            node_type = node.get_node_type()
            print(f"{prefix}├─ [{node_type}] {node.title} (id: {node.id}, level: {node.level})")
            
            for child in node.children:
                print_node(child, indent + 1)
        
        for root in self.root_nodes:
            print_node(root)
        
        print("=" * 60)
    
    def print_processing_order(self):
        """처리 순서를 출력"""
        processing_order = self.get_processing_order()
        
        print("\n📋 처리 순서 (하위→상위):")
        print("=" * 60)
        
        for i, level_nodes in enumerate(processing_order):
            level = level_nodes[0].level if level_nodes else 0
            print(f"레벨 {level} ({len(level_nodes)}개 노드):")
            for node in level_nodes:
                node_type = node.get_node_type()
                print(f"  - [{node_type}] {node.title}")
        
        print("=" * 60)

def main():
    """테스트 실행"""
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json"
    text_base_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections"
    
    analyzer = NodeStructureAnalyzer(json_path, text_base_path)
    
    print("JSON 구조 분석 시스템 테스트")
    print("=" * 50)
    
    # 1. JSON 구조 로드
    if not analyzer.load_json_structure():
        return
    
    # 2. 트리 구조 출력
    analyzer.print_tree_structure()
    
    # 3. 처리 순서 출력
    analyzer.print_processing_order()
    
    # 4. 텍스트 파일 존재 확인
    analyzer.validate_text_files_exist()

if __name__ == "__main__":
    main()