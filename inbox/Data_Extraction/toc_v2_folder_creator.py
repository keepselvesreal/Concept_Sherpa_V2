#!/usr/bin/env python3
"""
TOC v2 기반 폴더 구조 생성기
- Root node 이름을 최상위 폴더로 사용
- Leaf node를 제외한 모든 node를 레벨에 맞게 계층적 폴더로 생성
- Front Matter와 Index 섹션 제외
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import json
from dataclasses import dataclass

@dataclass
class TOCNodeV2:
    """TOC v2 노드 표현"""
    title: str
    level: int
    node_type: str  # node0, node1, node2, node3, node4
    is_leaf: bool
    children: List['TOCNodeV2']
    parent: Optional['TOCNodeV2'] = None
    folder_path: Optional[Path] = None

class TOCFolderCreatorV2:
    def __init__(self, toc_file: str, output_base_dir: str = "/home/nadle/projects/Knowledge_Sherpa/v2/Data_Extraction"):
        self.toc_file = Path(toc_file)
        self.output_base_dir = Path(output_base_dir)
        self.root_node = None
        self.all_nodes = []
        self.leaf_nodes = []
        self.internal_nodes = []
        
    def parse_toc_v2(self) -> None:
        """TOC v2 파일을 파싱하여 노드 트리 구성"""
        print("TOC v2 파일 파싱 중...")
        
        with open(self.toc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        node_stack = []  # 계층 추적을 위한 스택
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # Front Matter와 Index 섹션 스킵
            if self._should_skip_section(line):
                continue
                
            # 노드 정보 추출
            node_info = self._parse_line(line)
            if not node_info:
                continue
                
            title, node_type, level = node_info
            
            # 노드 생성
            node = TOCNodeV2(
                title=title,
                level=level,
                node_type=node_type,
                is_leaf=self._is_leaf_node(node_type),
                children=[]
            )
            
            # Root node 설정
            if level == 0:  # node0
                self.root_node = node
                node_stack = [node]
            else:
                # 올바른 부모 찾기
                while len(node_stack) > level:
                    node_stack.pop()
                
                if node_stack:
                    parent = node_stack[-1]
                    node.parent = parent
                    parent.children.append(node)
                
                node_stack.append(node)
            
            # 노드 분류
            self.all_nodes.append(node)
            if node.is_leaf:
                self.leaf_nodes.append(node)
            else:
                self.internal_nodes.append(node)
        
        print(f"파싱 완료: 전체 {len(self.all_nodes)}개 노드 ({len(self.internal_nodes)}개 internal, {len(self.leaf_nodes)}개 leaf)")
        
    def _should_skip_section(self, line: str) -> bool:
        """Front Matter와 Index 섹션 스킵 여부 결정"""
        line_lower = line.lower().strip()
        
        skip_patterns = [
            r'^\s*##\s+front\s+matter\s*$',
            r'^\s*-\s*data-oriented\s+programming\s*$',
            r'^\s*-\s*brief\s+contents\s*$',
            r'^\s*-\s*contents\s*$',
            r'^\s*-\s*forewords\s*$',
            r'^\s*-\s*preface\s*$',
            r'^\s*-\s*acknowledgments\s*$',
            r'^\s*-\s*about\s+this\s+book\s*$',
            r'^\s*-\s*who\s+should\s+read',
            r'^\s*-\s*how\s+this\s+book',
            r'^\s*-\s*about\s+the\s+code\s*$',
            r'^\s*-\s*livebook\s+discussion',
            r'^\s*-\s*about\s+the\s+author\s*$',
            r'^\s*-\s*about\s+the\s+cover',
            r'^\s*-\s*dramatis\s+personae\s*$',
            r'^\s*##\s+index\s*(\(|$)',
            r'^\s*-\s*[A-Z]\s*(\(|$)',  # Index 단일 문자 항목
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, line_lower):
                return True
        return False
    
    def _parse_line(self, line: str) -> Optional[Tuple[str, str, int]]:
        """라인에서 제목, 노드타입, 레벨 추출"""
        # node 타입 추출 (node0, node1, node2, node3, node4)
        node_match = re.search(r'\(node(\d+)\)', line)
        if not node_match:
            return None
            
        node_level = int(node_match.group(1))
        node_type = f"node{node_level}"
        
        # 제목 추출 (node 표기와 마크다운 기호 제거)
        title = line
        title = re.sub(r'\s*\(node\d+\)\s*', '', title)  # node 표기 제거
        title = re.sub(r'^#+\s*', '', title)  # 마크다운 헤더 제거
        title = re.sub(r'^-\s*', '', title)   # 불릿 포인트 제거
        title = title.strip()
        
        if not title:
            return None
            
        return title, node_type, node_level
    
    def _is_leaf_node(self, node_type: str) -> bool:
        """현재는 모든 node4가 leaf node라고 가정"""
        return node_type == "node4"
    
    def create_folder_structure(self) -> None:
        """계층적 폴더 구조 생성"""
        print("폴더 구조 생성 중...")
        
        if not self.root_node:
            print("❌ Root node가 없습니다.")
            return
            
        # Root 폴더 생성 (root node 이름 사용)
        root_folder_name = self._sanitize_folder_name(self.root_node.title)
        root_path = self.output_base_dir / root_folder_name
        root_path.mkdir(parents=True, exist_ok=True)
        self.root_node.folder_path = root_path
        
        print(f"Root 폴더 생성: {root_path}")
        
        # 재귀적으로 internal node 폴더들 생성
        folder_count = self._create_folders_recursive(self.root_node, root_path)
        
        print(f"✅ 폴더 구조 생성 완료: {folder_count}개 폴더")
        
        # 구조 요약 생성
        self._create_structure_summary()
    
    def _create_folders_recursive(self, node: TOCNodeV2, parent_path: Path) -> int:
        """재귀적으로 폴더 생성"""
        folder_count = 0
        
        for child in node.children:
            if not child.is_leaf:  # Internal node만 폴더로 생성
                folder_name = self._sanitize_folder_name(child.title)
                child_path = parent_path / folder_name
                child_path.mkdir(exist_ok=True)
                child.folder_path = child_path
                
                # 폴더 메타데이터 생성
                self._create_folder_metadata(child, child_path)
                
                folder_count += 1
                
                # 재귀적으로 하위 폴더들 생성
                folder_count += self._create_folders_recursive(child, child_path)
        
        return folder_count
    
    def _sanitize_folder_name(self, title: str) -> str:
        """폴더 이름으로 사용 가능하도록 제목 정리"""
        # 문제가 되는 문자들 제거/변환
        clean_name = re.sub(r'[<>:"/\\|?*]', '', title)
        clean_name = re.sub(r'[—–-]+', '_', clean_name)  # 다양한 대시를 언더스코어로
        clean_name = re.sub(r'\s+', '_', clean_name)      # 공백을 언더스코어로
        clean_name = re.sub(r'[^\w\s_-]', '', clean_name) # 특수문자 제거
        clean_name = re.sub(r'_+', '_', clean_name)       # 중복 언더스코어 제거
        clean_name = clean_name.strip('_')                # 앞뒤 언더스코어 제거
        
        # 길이 제한
        if len(clean_name) > 80:
            clean_name = clean_name[:80].rstrip('_')
            
        return clean_name or "Unnamed"
    
    def _create_folder_metadata(self, node: TOCNodeV2, folder_path: Path) -> None:
        """폴더 메타데이터 파일 생성"""
        metadata = {
            "title": node.title,
            "node_type": node.node_type,
            "level": node.level,
            "is_leaf": node.is_leaf,
            "children_count": len(node.children),
            "leaf_children": [child.title for child in node.children if child.is_leaf],
            "internal_children": [child.title for child in node.children if not child.is_leaf],
            "parent": node.parent.title if node.parent else None
        }
        
        metadata_file = folder_path / ".folder_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _create_structure_summary(self) -> None:
        """폴더 구조 요약 보고서 생성"""
        summary = {
            "root_folder": self.root_node.title if self.root_node else "Unknown",
            "total_nodes": len(self.all_nodes),
            "internal_nodes": len(self.internal_nodes),
            "leaf_nodes": len(self.leaf_nodes),
            "folder_structure": self._generate_folder_tree()
        }
        
        # JSON 요약
        summary_file = self.output_base_dir / "folder_structure_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # 읽기 쉬운 텍스트 요약
        text_summary_file = self.output_base_dir / "folder_structure_summary.md"
        with open(text_summary_file, 'w', encoding='utf-8') as f:
            f.write("# 폴더 구조 요약\n\n")
            f.write(f"**Root 폴더:** {self.root_node.title}\n")
            f.write(f"**전체 노드 수:** {len(self.all_nodes)}\n")
            f.write(f"**Internal 노드 (폴더):** {len(self.internal_nodes)}\n")
            f.write(f"**Leaf 노드 (파일 대상):** {len(self.leaf_nodes)}\n\n")
            
            f.write("## 폴더 구조\n\n")
            f.write("```\n")
            f.write(self._generate_folder_tree_text(self.root_node, ""))
            f.write("```\n\n")
            
            f.write("## Leaf 노드 목록 (콘텐츠 추출 대상)\n\n")
            for leaf in self.leaf_nodes:
                parent_path = self._get_node_path(leaf.parent) if leaf.parent else ""
                f.write(f"- **{leaf.title}** ({leaf.node_type})\n")
                f.write(f"  - 경로: `{parent_path}`\n\n")
        
        print(f"📊 구조 요약 생성: {summary_file}")
        print(f"📄 구조 요약 (읽기용): {text_summary_file}")
    
    def _generate_folder_tree(self) -> dict:
        """폴더 트리 구조를 딕셔너리로 생성"""
        if not self.root_node:
            return {}
            
        return self._node_to_dict(self.root_node)
    
    def _node_to_dict(self, node: TOCNodeV2) -> dict:
        """노드를 딕셔너리 형태로 변환"""
        result = {
            "title": node.title,
            "type": node.node_type,
            "is_leaf": node.is_leaf
        }
        
        if not node.is_leaf and node.children:
            result["children"] = [self._node_to_dict(child) for child in node.children]
            
        return result
    
    def _generate_folder_tree_text(self, node: TOCNodeV2, indent: str) -> str:
        """텍스트 형태의 폴더 트리 생성"""
        result = ""
        
        if node.level == 0:
            result += f"{indent}{self._sanitize_folder_name(node.title)}/\n"
            child_indent = indent + "├── "
        else:
            if not node.is_leaf:
                result += f"{indent}{self._sanitize_folder_name(node.title)}/\n"
                child_indent = indent.replace("├──", "│  ").replace("└──", "   ") + "├── "
            else:
                result += f"{indent}📄 {node.title} ({node.node_type})\n"
                return result
        
        for i, child in enumerate(node.children):
            if i == len(node.children) - 1:
                child_prefix = child_indent.replace("├──", "└──")
            else:
                child_prefix = child_indent
            result += self._generate_folder_tree_text(child, child_prefix)
        
        return result
    
    def _get_node_path(self, node: TOCNodeV2) -> str:
        """노드의 전체 경로 생성"""
        if not node:
            return ""
            
        parts = []
        current = node
        while current and current.level > 0:
            if not current.is_leaf:
                parts.append(self._sanitize_folder_name(current.title))
            current = current.parent
        
        parts.reverse()
        return "/".join(parts)

def main():
    """메인 실행 함수"""
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v2.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/Data_Extraction"
    
    if not Path(toc_file).exists():
        print(f"❌ TOC 파일을 찾을 수 없습니다: {toc_file}")
        return
        
    print("🚀 TOC v2 기반 폴더 구조 생성 시작")
    print(f"📄 TOC 파일: {toc_file}")
    print(f"📁 출력 디렉토리: {output_dir}")
    
    creator = TOCFolderCreatorV2(toc_file, output_dir)
    
    try:
        # Step 1: TOC 파싱
        creator.parse_toc_v2()
        
        # Step 2: 폴더 구조 생성
        creator.create_folder_structure()
        
        print("\n✅ 폴더 구조 생성 완료!")
        print(f"Root 폴더: {creator.root_node.folder_path}")
        print(f"Internal 노드 폴더: {len(creator.internal_nodes)}개")
        print(f"Leaf 노드 (콘텐츠 추출 대상): {len(creator.leaf_nodes)}개")
        
    except Exception as e:
        print(f"\n❌ 폴더 구조 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()