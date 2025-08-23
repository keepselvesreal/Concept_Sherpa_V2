#!/usr/bin/env python3
"""
TOC-based folder organization and content extraction script
Creates folder structure based on TOC hierarchy and extracts content for leaf nodes
Excludes Front Matter and Index sections as requested
"""

import pdfplumber
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import json
from dataclasses import dataclass

@dataclass
class TOCNode:
    """Represents a node in the TOC hierarchy"""
    id: str
    title: str
    level: int
    is_leaf: bool
    children: List['TOCNode']
    parent: Optional['TOCNode'] = None
    page_range: Optional[Tuple[int, int]] = None

class TOCFolderOrganizer:
    def __init__(self, toc_file: str, pdf_path: str, output_dir: str = "Data-Oriented_Programming_Organized"):
        self.toc_file = Path(toc_file)
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.toc_tree = None
        self.leaf_nodes = []
        self.internal_nodes = []
        
    def parse_toc_structure(self) -> None:
        """Parse TOC file and build hierarchical structure"""
        print("TOC 구조 파싱 중...")
        
        with open(self.toc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        nodes_stack = []  # Stack to track hierarchy
        root = None
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # Skip Front Matter and Index sections
            if self._should_skip_section(line):
                continue
                
            # Determine hierarchy level and extract info
            level = self._get_hierarchy_level(line)
            if level == -1:
                continue
                
            title, is_leaf = self._extract_title_and_type(line)
            if not title:
                continue
                
            # Debug first few nodes and root finding (optional)
            # if len(self.leaf_nodes) + len(self.internal_nodes) < 10 or level == 0:
            #     print(f"Processing: '{line.strip()[:50]}' -> Level {level}, Title: '{title}', Leaf: {is_leaf}")
                
            # Create node
            node_id = self._generate_node_id(title, level)
            node = TOCNode(
                id=node_id,
                title=title,
                level=level,
                is_leaf=is_leaf,
                children=[]
            )
            
            # Handle hierarchy
            if level == 0:  # Root node
                root = node
                nodes_stack = [node]
            else:
                # Find parent at appropriate level
                while len(nodes_stack) > level:
                    nodes_stack.pop()
                
                if nodes_stack:
                    parent = nodes_stack[-1]
                    node.parent = parent
                    parent.children.append(node)
                
                nodes_stack.append(node)
            
            # Categorize nodes
            if is_leaf:
                self.leaf_nodes.append(node)
            else:
                self.internal_nodes.append(node)
        
        self.toc_tree = root
        print(f"TOC 파싱 완료: {len(self.internal_nodes)}개 internal nodes, {len(self.leaf_nodes)}개 leaf nodes")
        
        # Debug: print tree structure
        if root:
            print("Root found:", root.title)
            print(f"Root has {len(root.children)} children")
        else:
            print("❌ Root node not created!")
    
    def _should_skip_section(self, line: str) -> bool:
        """Check if section should be skipped (Front Matter or Index)"""
        skip_patterns = [
            r'^\s*##\s+front\s+matter',  # Front Matter section header
            r'^\s*-\s*brief\s+contents\s*$',
            r'^\s*-\s*contents\s*$',  # Only standalone "contents", not "Table of Contents"
            r'^\s*-\s*forewords\s*$',
            r'^\s*-\s*preface\s*$',
            r'^\s*-\s*acknowledgments\s*$',
            r'^\s*-\s*about\s+this\s+book\s*$',
            r'^\s*-\s*about\s+the\s+author\s*$',
            r'^\s*-\s*about\s+the\s+cover',
            r'^\s*-\s*dramatis\s+personae\s*$',
            r'^\s*##\s+index\s*(\(|$)',  # Index section header
            r'^\s*-\s*[A-Z]\s*$',  # Single letter index entries
        ]
        
        line_lower = line.lower().strip()
        for pattern in skip_patterns:
            if re.search(pattern, line_lower):
                return True
        return False
    
    def _get_hierarchy_level(self, line: str) -> int:
        """Determine hierarchy level from line formatting"""
        # Count leading hash symbols for markdown headers
        hash_match = re.match(r'^(#+)\s', line)
        if hash_match:
            hash_count = len(hash_match.group(1))
            return hash_count - 1  # Convert to 0-based (# = 0, ## = 1, ### = 2)
            
        # Count leading dashes/spaces for list items
        dash_match = re.match(r'^(\s*)-\s+', line)
        if dash_match:
            spaces = len(dash_match.group(1))
            # Each 2-space indent increases level
            # Base level for single dash is 2 (under ##)
            indent_level = spaces // 2
            return 2 + indent_level  # Start from level 2 for first-level bullets
            
        return -1  # Invalid line
    
    def _extract_title_and_type(self, line: str) -> Tuple[str, bool]:
        """Extract title and determine if it's a leaf node"""
        # Remove markdown formatting
        clean_line = re.sub(r'^#+\s*', '', line)  # Remove hash headers
        clean_line = re.sub(r'^-\s*', '', clean_line)  # Remove dash bullets
        clean_line = clean_line.strip()
        
        # Check for explicit node type annotations
        is_leaf = False
        if '(leaf node)' in clean_line:
            is_leaf = True
            clean_line = re.sub(r'\s*\(leaf node\)', '', clean_line)
        elif '(internal node)' in clean_line:
            is_leaf = False
            clean_line = re.sub(r'\s*\(internal node\)', '', clean_line)
        elif '(root node)' in clean_line:
            is_leaf = False
            clean_line = re.sub(r'\s*\(root node\)', '', clean_line)
        else:
            # For items without explicit annotation, determine heuristically
            # Usually bullets with subsections are internal nodes
            # Final level items without further nesting are leaf nodes
            is_leaf = self._guess_leaf_status(line)
        
        # Clean up title - remove any remaining parenthetical notes
        clean_line = re.sub(r'\s*\([^)]*\)', '', clean_line)  # Remove any parenthetical
        clean_line = clean_line.strip()
        
        return clean_line, is_leaf
    
    def _guess_leaf_status(self, line: str) -> bool:
        """Heuristically determine if a line represents a leaf node"""
        # Items that are typically leaf nodes:
        # - Numbered subsections (1.1.1, 1.2.3, etc.)
        # - Summary sections
        # - Introduction sections
        # - Simple topic items
        
        clean_line = line.strip().lower()
        
        # Remove markdown formatting for analysis
        clean_line = re.sub(r'^#+\s*', '', clean_line)  # Remove hash headers
        clean_line = re.sub(r'^-\s*', '', clean_line)  # Remove dash bullets
        
        # Leaf node indicators
        leaf_indicators = [
            r'^\d+\.\d+\.\d+',  # Three-level numbering (1.1.1)
            r'summary\s*$',     # Summary sections
            r'introduction.*\(사용자 추가\)',  # User-added introductions
            r'conclusion\s*$',  # Conclusion sections
        ]
        
        for pattern in leaf_indicators:
            if re.search(pattern, clean_line):
                return True
        
        # Default to internal node for safety (can be overridden by explicit annotation)
        return False
    
    def _generate_node_id(self, title: str, level: int) -> str:
        """Generate unique node ID from title"""
        # Clean title for filesystem
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'\s+', '_', clean_title.strip())
        clean_title = clean_title[:50]  # Limit length
        
        # Add level prefix for uniqueness
        level_prefixes = ['Root', 'Part', 'Chapter', 'Section', 'Subsection']
        prefix = level_prefixes[min(level, len(level_prefixes) - 1)]
        
        return f"{prefix}_{clean_title}"
    
    def create_folder_structure(self) -> None:
        """Create folder structure for all internal nodes"""
        print("폴더 구조 생성 중...")
        
        if not self.toc_tree:
            print("❌ TOC 구조가 파싱되지 않았습니다.")
            return
        
        # Create base output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Recursively create folders for internal nodes
        self._create_folders_recursive(self.toc_tree, self.output_dir)
        
        print(f"✅ 폴더 구조 생성 완료: {len(self.internal_nodes)}개 폴더")
    
    def _create_folders_recursive(self, node: TOCNode, current_path: Path) -> None:
        """Recursively create folders for internal nodes"""
        if not node.is_leaf and node.level > 0:  # Skip root, create folders for internal nodes
            # Create folder for this internal node
            folder_name = self._sanitize_folder_name(node.title)
            folder_path = current_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # Create metadata file for the folder
            self._create_folder_metadata(node, folder_path)
            
            # Recursively process children
            for child in node.children:
                if child.is_leaf:
                    # Leaf nodes will have files created later
                    continue
                else:
                    self._create_folders_recursive(child, folder_path)
        else:
            # For root node, process children in base directory
            for child in node.children:
                if not child.is_leaf:
                    self._create_folders_recursive(child, current_path)
    
    def _sanitize_folder_name(self, title: str) -> str:
        """Convert title to filesystem-safe folder name"""
        # Remove problematic characters
        clean_name = re.sub(r'[<>:"/\\|?*]', '', title)
        # Replace spaces and special chars with underscores
        clean_name = re.sub(r'[\s—-]+', '_', clean_name)
        # Remove multiple underscores
        clean_name = re.sub(r'_+', '_', clean_name)
        # Strip leading/trailing underscores
        clean_name = clean_name.strip('_')
        # Limit length
        clean_name = clean_name[:80]
        
        return clean_name or "Unnamed"
    
    def _create_folder_metadata(self, node: TOCNode, folder_path: Path) -> None:
        """Create metadata file for internal node folder"""
        metadata = {
            "node_id": node.id,
            "title": node.title,
            "level": node.level,
            "is_internal_node": True,
            "children_count": len(node.children),
            "leaf_children": [child.title for child in node.children if child.is_leaf],
            "internal_children": [child.title for child in node.children if not child.is_leaf]
        }
        
        with open(folder_path / ".folder_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def identify_leaf_content_ranges(self) -> None:
        """Identify page ranges for leaf node content extraction"""
        print("Leaf node 콘텐츠 범위 식별 중...")
        
        # Use existing part-based extractor page mappings as reference
        page_mappings = self._get_page_mappings()
        
        for leaf_node in self.leaf_nodes:
            # Try to match leaf node to content sections
            page_range = self._find_page_range_for_leaf(leaf_node, page_mappings)
            leaf_node.page_range = page_range
        
        print(f"✅ {len([n for n in self.leaf_nodes if n.page_range])}개 leaf node의 페이지 범위 식별")
    
    def _get_page_mappings(self) -> Dict[str, Tuple[int, int]]:
        """Get approximate page mappings based on existing part-based extractor"""
        return {
            # Part 1 - Flexibility
            "chapter_1": (31, 53),
            "chapter_2": (54, 70), 
            "chapter_3": (71, 98),
            "chapter_4": (99, 118),
            "chapter_5": (119, 137),
            "chapter_6": (138, 168),
            
            # Part 2 - Scalability  
            "chapter_7": (169, 190),
            "chapter_8": (191, 202),
            "chapter_9": (203, 224),
            "chapter_10": (225, 247),
            "chapter_11": (248, 274),
            
            # Part 3 - Maintainability
            "chapter_12": (275, 299),
            "chapter_13": (300, 322),
            "chapter_14": (323, 338),
            "chapter_15": (339, 380),
            
            # Appendices (estimated)
            "appendix_a": (381, 400),
            "appendix_b": (401, 420),
            "appendix_c": (421, 440),
            "appendix_d": (441, 450)
        }
    
    def _find_page_range_for_leaf(self, leaf_node: TOCNode, page_mappings: Dict[str, Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """Find page range for a specific leaf node"""
        title_lower = leaf_node.title.lower()
        
        # Match chapter/appendix level content
        for key, (start, end) in page_mappings.items():
            if any(keyword in title_lower for keyword in key.split('_')):
                # For chapter-level matches, estimate subsection ranges
                if 'chapter' in key:
                    return self._estimate_subsection_range(leaf_node, start, end)
                else:
                    return (start, end)
        
        return None
    
    def _estimate_subsection_range(self, leaf_node: TOCNode, chapter_start: int, chapter_end: int) -> Tuple[int, int]:
        """Estimate page range for subsections within a chapter"""
        # Simple estimation - divide chapter equally among subsections
        # In reality, this would need more sophisticated logic
        chapter_pages = chapter_end - chapter_start + 1
        
        # Find sibling leaf nodes to determine subdivision
        if leaf_node.parent:
            leaf_siblings = [child for child in leaf_node.parent.children if child.is_leaf]
            if leaf_siblings:
                pages_per_section = max(1, chapter_pages // len(leaf_siblings))
                section_index = leaf_siblings.index(leaf_node)
                
                section_start = chapter_start + (section_index * pages_per_section)
                section_end = min(chapter_end, section_start + pages_per_section - 1)
                
                return (section_start, section_end)
        
        # Fallback - return full chapter range
        return (chapter_start, chapter_end)

def main():
    """메인 실행 함수"""
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types.md"
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    if not Path(toc_file).exists():
        print(f"❌ TOC 파일을 찾을 수 없습니다: {toc_file}")
        return
        
    if not Path(pdf_path).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print("🚀 TOC 기반 폴더 조직화 시작")
    print(f"📄 TOC 파일: {toc_file}")
    print(f"📖 PDF 파일: {pdf_path}")
    
    organizer = TOCFolderOrganizer(toc_file, pdf_path)
    
    try:
        # Step 1: Parse TOC structure
        organizer.parse_toc_structure()
        
        # Step 2: Create folder structure
        organizer.create_folder_structure()
        
        # Step 3: Identify content ranges
        organizer.identify_leaf_content_ranges()
        
        print("\n✅ 1단계 완료: 폴더 구조 생성 및 콘텐츠 범위 식별")
        print("다음 단계: PDF 콘텐츠 추출 (별도 스크립트)")
        
    except Exception as e:
        print(f"\n❌ 처리 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()