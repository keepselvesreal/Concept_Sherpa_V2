#!/usr/bin/env python3
"""
Content extraction script for TOC-organized folder structure
Extracts PDF content for each leaf node and creates markdown files
"""

import pdfplumber
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import json
from dataclasses import dataclass
import pickle

@dataclass
class LeafNodeContent:
    """Represents content for a leaf node"""
    title: str
    folder_path: Path
    page_range: Optional[Tuple[int, int]]
    content: str = ""
    extraction_status: str = "pending"  # pending, extracted, failed

class ContentExtractor:
    def __init__(self, pdf_path: str, organized_dir: str = "Data-Oriented_Programming_Organized"):
        self.pdf_path = pdf_path
        self.organized_dir = Path(organized_dir)
        self.leaf_nodes = []
        self.content_mappings = self._load_content_mappings()
        
    def _load_content_mappings(self) -> Dict[str, Tuple[int, int]]:
        """Load detailed content mappings for chapters and sections"""
        return {
            # Part 1 - Flexibility
            "1_complexity": (31, 53),
            "2_separation": (54, 70), 
            "3_basic_data": (71, 98),
            "4_state_management": (99, 118),
            "5_concurrency": (119, 137),
            "6_unit_tests": (138, 168),
            
            # Part 2 - Scalability  
            "7_data_validation": (169, 190),
            "8_advanced_concurrency": (191, 202),
            "9_persistent_structures": (203, 224),
            "10_database": (225, 247),
            "11_web_services": (248, 274),
            
            # Part 3 - Maintainability
            "12_advanced_validation": (275, 299),
            "13_polymorphism": (300, 322),
            "14_advanced_manipulation": (323, 338),
            "15_debugging": (339, 380),
            
            # Appendices
            "appendix_a": (381, 410),
            "appendix_b": (411, 430),
            "appendix_c": (431, 450),
            "appendix_d": (451, 460)
        }
    
    def discover_leaf_nodes(self) -> None:
        """Discover all leaf nodes by scanning the organized folder structure"""
        print("Leaf node 폴더 구조 스캔 중...")
        
        leaf_count = 0
        for part_dir in self.organized_dir.iterdir():
            if not part_dir.is_dir() or part_dir.name.startswith('.'):
                continue
                
            print(f"  스캔 중: {part_dir.name}")
            
            for item in part_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if this is a leaf node (no .folder_metadata.json indicates leaf)
                    metadata_file = item / ".folder_metadata.json"
                    if not metadata_file.exists():
                        # This is a leaf node folder
                        leaf_node = LeafNodeContent(
                            title=self._folder_name_to_title(item.name),
                            folder_path=item,
                            page_range=self._estimate_page_range(item.name, part_dir.name)
                        )
                        self.leaf_nodes.append(leaf_node)
                        leaf_count += 1
                        print(f"    ✓ Leaf node: {item.name}")
                    else:
                        print(f"    ⊢ Internal node: {item.name} (has metadata)")
        
        print(f"✅ {leaf_count}개 leaf node 발견")
    
    def _folder_name_to_title(self, folder_name: str) -> str:
        """Convert folder name back to readable title"""
        # Replace underscores with spaces and clean up
        title = folder_name.replace('_', ' ')
        # Fix common patterns
        title = re.sub(r'\bDOP\b', 'DOP', title)
        title = re.sub(r'\bOOP\b', 'OOP', title)
        title = re.sub(r'\bUML\b', 'UML', title)
        title = re.sub(r'\bJSON\b', 'JSON', title)
        return title.title()
    
    def _estimate_page_range(self, folder_name: str, part_name: str) -> Optional[Tuple[int, int]]:
        """Estimate page range for a leaf node based on folder and part names"""
        folder_lower = folder_name.lower()
        
        # Try to match with known content mappings
        for key, (start, end) in self.content_mappings.items():
            if any(keyword in folder_lower for keyword in key.split('_')):
                # For chapter-level matches, estimate subsection ranges
                if 'chapter' not in key and 'appendix' not in key:
                    # This is a section within a chapter
                    return self._estimate_section_range(folder_lower, start, end)
                else:
                    # This is a full chapter or appendix
                    return (start, end)
        
        # Fallback estimation based on part and numbering
        return self._fallback_page_estimation(folder_lower, part_name)
    
    def _estimate_section_range(self, folder_name: str, chapter_start: int, chapter_end: int) -> Tuple[int, int]:
        """Estimate page range for sections within a chapter"""
        chapter_pages = chapter_end - chapter_start + 1
        
        # Simple estimation based on section numbering
        if re.search(r'^1\.1', folder_name):
            # First major section, typically 30-40% of chapter
            section_pages = max(3, int(chapter_pages * 0.35))
            return (chapter_start, chapter_start + section_pages - 1)
        elif re.search(r'^1\.2', folder_name):
            # Second major section
            section_start = chapter_start + int(chapter_pages * 0.35)
            section_pages = max(3, int(chapter_pages * 0.4))
            return (section_start, min(chapter_end, section_start + section_pages - 1))
        elif 'summary' in folder_name:
            # Summary is typically at the end, 1-2 pages
            return (chapter_end - 1, chapter_end)
        else:
            # Generic subsection estimation
            return (chapter_start + 2, chapter_start + 5)
    
    def _fallback_page_estimation(self, folder_name: str, part_name: str) -> Optional[Tuple[int, int]]:
        """Fallback page estimation for unmatched items"""
        # Simple heuristic based on part
        if "part_1" in part_name.lower():
            base_start = 31
            base_end = 168
        elif "part_2" in part_name.lower():
            base_start = 169
            base_end = 274
        elif "part_3" in part_name.lower():
            base_start = 275
            base_end = 380
        elif "appendices" in part_name.lower():
            base_start = 381
            base_end = 460
        else:
            return None
        
        # Return a small range in the appropriate part
        return (base_start, base_start + 3)
    
    def extract_all_content(self) -> None:
        """Extract PDF content for all leaf nodes"""
        print(f"PDF 콘텐츠 추출 시작: {len(self.leaf_nodes)}개 leaf node")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"총 PDF 페이지: {total_pages}")
            
            extracted_count = 0
            failed_count = 0
            
            for i, leaf_node in enumerate(self.leaf_nodes, 1):
                print(f"  [{i}/{len(self.leaf_nodes)}] {leaf_node.title}")
                
                if not leaf_node.page_range:
                    print(f"    ⚠️  페이지 범위 없음, 건너뛰기")
                    leaf_node.extraction_status = "failed"
                    failed_count += 1
                    continue
                
                try:
                    content = self._extract_page_range(pdf, leaf_node.page_range, total_pages)
                    if content.strip():
                        leaf_node.content = content
                        leaf_node.extraction_status = "extracted"
                        self._save_leaf_content(leaf_node)
                        extracted_count += 1
                        print(f"    ✅ 추출 완료 ({leaf_node.page_range[0]}-{leaf_node.page_range[1]}페이지)")
                    else:
                        leaf_node.extraction_status = "failed"
                        failed_count += 1
                        print(f"    ❌ 빈 콘텐츠")
                        
                except Exception as e:
                    leaf_node.extraction_status = "failed"
                    failed_count += 1
                    print(f"    ❌ 추출 실패: {e}")
            
            print(f"\n📊 추출 완료: ✅ {extracted_count}개 성공, ❌ {failed_count}개 실패")
            self._create_extraction_report(extracted_count, failed_count)
    
    def _extract_page_range(self, pdf, page_range: Tuple[int, int], total_pages: int) -> str:
        """Extract text from specific page range"""
        start_page, end_page = page_range
        start_page = max(1, start_page) - 1  # Convert to 0-based
        end_page = min(total_pages, end_page) - 1
        
        content = ""
        for page_num in range(start_page, end_page + 1):
            if page_num >= total_pages:
                break
                
            page = pdf.pages[page_num]
            page_text = page.extract_text() or ""
            
            if page_text.strip():
                content += f"=== PAGE {page_num + 1} ===\n{page_text}\n\n"
        
        return content.strip()
    
    def _save_leaf_content(self, leaf_node: LeafNodeContent) -> None:
        """Save extracted content to markdown file"""
        # Create the directory if it doesn't exist
        leaf_node.folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create content markdown file
        content_file = leaf_node.folder_path / "content.md"
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(f"# {leaf_node.title}\n\n")
            f.write(f"**페이지 범위:** {leaf_node.page_range[0]}-{leaf_node.page_range[1]}\n\n")
            f.write(f"**추출 상태:** {leaf_node.extraction_status}\n\n")
            f.write("---\n\n")
            f.write(leaf_node.content)
        
        # Create metadata file
        metadata = {
            "title": leaf_node.title,
            "page_range": f"{leaf_node.page_range[0]}-{leaf_node.page_range[1]}",
            "extraction_status": leaf_node.extraction_status,
            "content_length": len(leaf_node.content),
            "content_file": "content.md"
        }
        
        metadata_file = leaf_node.folder_path / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _create_extraction_report(self, extracted: int, failed: int) -> None:
        """Create extraction summary report"""
        report = {
            "extraction_summary": {
                "total_leaf_nodes": len(self.leaf_nodes),
                "extracted_successfully": extracted,
                "extraction_failed": failed,
                "success_rate": f"{extracted}/{len(self.leaf_nodes)} ({100*extracted//len(self.leaf_nodes) if self.leaf_nodes else 0}%)"
            },
            "leaf_nodes_detail": []
        }
        
        # Add details for each leaf node
        for node in self.leaf_nodes:
            report["leaf_nodes_detail"].append({
                "title": node.title,
                "folder_path": str(node.folder_path.relative_to(self.organized_dir)),
                "page_range": f"{node.page_range[0]}-{node.page_range[1]}" if node.page_range else "Unknown",
                "status": node.extraction_status,
                "content_length": len(node.content) if node.content else 0
            })
        
        # Save JSON report
        report_file = self.organized_dir / "extraction_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save readable markdown report
        markdown_report = self.organized_dir / "extraction_report.md"
        with open(markdown_report, 'w', encoding='utf-8') as f:
            f.write("# Content Extraction Report\n\n")
            f.write(f"**Total Leaf Nodes:** {len(self.leaf_nodes)}\n")
            f.write(f"**Successfully Extracted:** {extracted}\n") 
            f.write(f"**Failed Extractions:** {failed}\n")
            f.write(f"**Success Rate:** {100*extracted//len(self.leaf_nodes) if self.leaf_nodes else 0}%\n\n")
            
            f.write("## Extraction Details\n\n")
            for node in self.leaf_nodes:
                status_emoji = "✅" if node.extraction_status == "extracted" else "❌"
                f.write(f"- {status_emoji} **{node.title}**\n")
                f.write(f"  - Path: `{node.folder_path.relative_to(self.organized_dir)}`\n")
                f.write(f"  - Pages: {node.page_range[0]}-{node.page_range[1]}\n" if node.page_range else "  - Pages: Unknown\n")
                f.write(f"  - Content Length: {len(node.content)} characters\n\n")
        
        print(f"📄 추출 보고서 생성: {report_file}")
        print(f"📄 추출 보고서 (읽기용): {markdown_report}")

def main():
    """메인 실행 함수"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    organized_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_Organized"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
        
    if not Path(organized_dir).exists():
        print(f"❌ 조직화된 폴더를 찾을 수 없습니다: {organized_dir}")
        print("먼저 toc_folder_organizer.py를 실행하세요.")
        return
    
    print("🚀 TOC 기반 콘텐츠 추출 시작")
    print(f"📖 PDF: {pdf_path}")
    print(f"📁 조직화 폴더: {organized_dir}")
    
    extractor = ContentExtractor(pdf_path, organized_dir)
    
    try:
        # Step 1: Discover leaf nodes
        extractor.discover_leaf_nodes()
        
        # Step 2: Extract all content
        extractor.extract_all_content()
        
        print("\n✅ 모든 콘텐츠 추출 완료!")
        
    except Exception as e:
        print(f"\n❌ 콘텐츠 추출 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()