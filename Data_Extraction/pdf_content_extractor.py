#!/usr/bin/env python3
"""
PDF 콘텐츠 추출기 - Leaf node용
생성된 폴더 구조에서 leaf node들을 찾아 PDF에서 해당 콘텐츠를 추출하여 파일 생성
"""

import pdfplumber
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import json
from dataclasses import dataclass

@dataclass
class LeafNodeInfo:
    """Leaf node 정보"""
    title: str
    folder_path: Path
    parent_path: str
    page_range: Optional[Tuple[int, int]] = None
    content: str = ""
    extraction_status: str = "pending"

class PDFContentExtractor:
    def __init__(self, pdf_path: str, base_dir: str = "/home/nadle/projects/Knowledge_Sherpa/v2/Data_Extraction/Data_Oriented_Programming", toc_file: str = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v2.md"):
        self.pdf_path = pdf_path
        self.base_dir = Path(base_dir)
        self.toc_file = Path(toc_file)
        self.leaf_nodes = []
        self.content_mappings = self._get_content_mappings()
        
    def _get_content_mappings(self) -> Dict[str, Tuple[int, int]]:
        """PDF 페이지 범위 매핑 정보"""
        return {
            # Part 1 - Flexibility (31-168)
            "complexity": (31, 53),
            "separation": (54, 70),
            "basic_data": (71, 98),
            "state_management": (99, 118),
            "concurrency": (119, 137),
            "unit_tests": (138, 168),
            
            # Part 2 - Scalability (169-274)
            "data_validation": (169, 190),
            "advanced_concurrency": (191, 202),
            "persistent": (203, 224),
            "database": (225, 247),
            "web_services": (248, 274),
            
            # Part 3 - Maintainability (275-380)
            "advanced_validation": (275, 299),
            "polymorphism": (300, 322),
            "advanced_manipulation": (323, 338),
            "debugging": (339, 380),
            
            # Appendices (381-460)
            "appendix_a": (381, 410),
            "appendix_b": (411, 430),
            "appendix_c": (431, 450),
            "appendix_d": (451, 460)
        }
    
    def discover_leaf_nodes(self) -> None:
        """폴더 구조를 스캔하여 leaf node들 발견"""
        print("Leaf node 폴더 스캔 중...")
        
        if not self.base_dir.exists():
            print(f"❌ 기본 디렉토리가 존재하지 않습니다: {self.base_dir}")
            return
            
        leaf_count = 0
        for root, dirs, files in os.walk(self.base_dir):
            current_path = Path(root)
            
            # metadata 파일이 있는지 확인
            metadata_file = current_path / ".folder_metadata.json"
            if metadata_file.exists():
                # metadata 파일을 읽어서 leaf node인지 확인
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # is_leaf가 True인 폴더를 찾음
                    if metadata.get('is_leaf', False):
                        relative_path = current_path.relative_to(self.base_dir)
                        parent_path = str(relative_path.parent) if relative_path.parent != Path('.') else ""
                        
                        leaf_node = LeafNodeInfo(
                            title=metadata.get('title', current_path.name.replace('_', ' ')),
                            folder_path=current_path,
                            parent_path=parent_path
                        )
                        
                        # 페이지 범위 추정
                        leaf_node.page_range = self._estimate_page_range(leaf_node)
                        
                        self.leaf_nodes.append(leaf_node)
                        leaf_count += 1
                        
                        if leaf_count <= 10:  # 처음 10개만 로그 출력
                            print(f"  ✓ {leaf_node.title} -> {leaf_node.page_range}")
                            
                except Exception as e:
                    print(f"  ⚠️ metadata 파일 읽기 오류 {metadata_file}: {e}")
        
        print(f"✅ 총 {leaf_count}개 leaf node 발견")
    
    def _estimate_page_range(self, leaf_node: LeafNodeInfo) -> Optional[Tuple[int, int]]:
        """Leaf node의 페이지 범위 추정"""
        title_lower = leaf_node.title.lower()
        parent_lower = leaf_node.parent_path.lower()
        
        # 1. 챕터/섹션 키워드로 매핑
        for key, (start, end) in self.content_mappings.items():
            if any(keyword in title_lower or keyword in parent_lower 
                   for keyword in key.split('_')):
                return self._refine_page_range(leaf_node, start, end)
        
        # 2. 부모 경로 기반 추정
        if "part_1" in parent_lower:
            return self._estimate_by_part(leaf_node, 31, 168)
        elif "part_2" in parent_lower:
            return self._estimate_by_part(leaf_node, 169, 274)
        elif "part_3" in parent_lower:
            return self._estimate_by_part(leaf_node, 275, 380)
        elif "appendices" in parent_lower:
            return self._estimate_by_appendix(leaf_node, 381, 460)
        
        # 3. 기본 추정값
        return (50, 55)  # 기본 5페이지
    
    def _refine_page_range(self, leaf_node: LeafNodeInfo, chapter_start: int, chapter_end: int) -> Tuple[int, int]:
        """챕터 내에서 세부 섹션의 페이지 범위 추정"""
        title_lower = leaf_node.title.lower()
        chapter_pages = chapter_end - chapter_start + 1
        
        # Introduction 섹션
        if "introduction" in title_lower or "사용자_추가" in leaf_node.title:
            return (chapter_start, chapter_start + 2)
        
        # Summary 섹션
        elif "summary" in title_lower:
            return (chapter_end - 1, chapter_end)
        
        # 번호가 있는 섹션들 (1.1, 1.2, 2.1 등)
        elif re.search(r'\d+\.\d+', title_lower):
            section_match = re.search(r'(\d+)\.(\d+)', title_lower)
            if section_match:
                section_num = int(section_match.group(2))
                # 섹션 번호에 따라 페이지 범위 추정
                section_pages = max(3, chapter_pages // 6)  # 챕터를 대략 6개 섹션으로 나눔
                section_start = chapter_start + (section_num - 1) * section_pages + 2
                section_end = min(chapter_end - 1, section_start + section_pages - 1)
                return (section_start, section_end)
        
        # 일반 섹션
        else:
            section_pages = max(3, chapter_pages // 4)
            return (chapter_start + 2, chapter_start + 2 + section_pages - 1)
    
    def _estimate_by_part(self, leaf_node: LeafNodeInfo, part_start: int, part_end: int) -> Tuple[int, int]:
        """Part 범위 내에서 추정"""
        # 기본적으로 3-5페이지 할당
        pages = 4
        start_page = part_start + hash(leaf_node.title) % (part_end - part_start - pages)
        return (start_page, start_page + pages - 1)
    
    def _estimate_by_appendix(self, leaf_node: LeafNodeInfo, app_start: int, app_end: int) -> Tuple[int, int]:
        """Appendix 범위 내에서 추정"""
        title_lower = leaf_node.title.lower()
        
        if "appendix_a" in leaf_node.parent_path.lower():
            return self._refine_page_range(leaf_node, 381, 410)
        elif "appendix_b" in leaf_node.parent_path.lower():
            return self._refine_page_range(leaf_node, 411, 430)
        elif "appendix_c" in leaf_node.parent_path.lower():
            return self._refine_page_range(leaf_node, 431, 450)
        elif "appendix_d" in leaf_node.parent_path.lower():
            return (451, 460)
        
        return (app_start, app_start + 3)
    
    def extract_all_content(self) -> None:
        """모든 leaf node의 콘텐츠 추출"""
        if not self.leaf_nodes:
            print("❌ Leaf node가 없습니다. 먼저 discover_leaf_nodes()를 실행하세요.")
            return
            
        print(f"PDF 콘텐츠 추출 시작: {len(self.leaf_nodes)}개 leaf node")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"PDF 총 페이지: {total_pages}")
            
            success_count = 0
            failed_count = 0
            
            for i, leaf_node in enumerate(self.leaf_nodes, 1):
                print(f"[{i}/{len(self.leaf_nodes)}] {leaf_node.title}", end=" ")
                
                if not leaf_node.page_range:
                    print("❌ 페이지 범위 없음")
                    leaf_node.extraction_status = "failed"
                    failed_count += 1
                    continue
                
                try:
                    content = self._extract_content(pdf, leaf_node.page_range, total_pages)
                    if content.strip():
                        leaf_node.content = content
                        leaf_node.extraction_status = "success"
                        self._save_content_file(leaf_node)
                        success_count += 1
                        print(f"✅ ({leaf_node.page_range[0]}-{leaf_node.page_range[1]})")
                    else:
                        leaf_node.extraction_status = "empty"
                        failed_count += 1
                        print("❌ 빈 콘텐츠")
                        
                except Exception as e:
                    leaf_node.extraction_status = "error"
                    failed_count += 1
                    print(f"❌ 오류: {str(e)[:50]}")
            
            print(f"\n📊 추출 결과: ✅ {success_count}개 성공, ❌ {failed_count}개 실패")
            self._create_extraction_report(success_count, failed_count)
    
    def _extract_content(self, pdf, page_range: Tuple[int, int], total_pages: int) -> str:
        """지정된 페이지 범위에서 텍스트 추출"""
        start_page, end_page = page_range
        start_page = max(1, start_page) - 1  # 0-based 인덱스로 변환
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
    
    def _save_content_file(self, leaf_node: LeafNodeInfo) -> None:
        """Leaf node 콘텐츠를 파일로 저장"""
        # 폴더가 존재하지 않으면 생성
        leaf_node.folder_path.mkdir(parents=True, exist_ok=True)
        
        # content.md 파일 생성
        content_file = leaf_node.folder_path / "content.md"
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(f"# {leaf_node.title}\n\n")
            f.write(f"**경로:** {leaf_node.parent_path}\n")
            f.write(f"**페이지 범위:** {leaf_node.page_range[0]}-{leaf_node.page_range[1]}\n")
            f.write(f"**추출 상태:** {leaf_node.extraction_status}\n")
            f.write(f"**콘텐츠 길이:** {len(leaf_node.content)} 문자\n\n")
            f.write("---\n\n")
            f.write(leaf_node.content)
        
        # metadata.json 파일 생성
        metadata = {
            "title": leaf_node.title,
            "parent_path": leaf_node.parent_path,
            "page_range": f"{leaf_node.page_range[0]}-{leaf_node.page_range[1]}" if leaf_node.page_range else "Unknown",
            "extraction_status": leaf_node.extraction_status,
            "content_length": len(leaf_node.content),
            "content_file": "content.md"
        }
        
        metadata_file = leaf_node.folder_path / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _create_extraction_report(self, success: int, failed: int) -> None:
        """추출 결과 보고서 생성"""
        report_data = {
            "extraction_summary": {
                "total_leaf_nodes": len(self.leaf_nodes),
                "successful_extractions": success,
                "failed_extractions": failed,
                "success_rate": f"{success}/{len(self.leaf_nodes)} ({100*success//len(self.leaf_nodes) if self.leaf_nodes else 0}%)"
            },
            "leaf_nodes": []
        }
        
        # 각 leaf node 정보 추가
        for node in self.leaf_nodes:
            report_data["leaf_nodes"].append({
                "title": node.title,
                "parent_path": node.parent_path,
                "page_range": f"{node.page_range[0]}-{node.page_range[1]}" if node.page_range else "Unknown",
                "status": node.extraction_status,
                "content_length": len(node.content)
            })
        
        # JSON 보고서 저장
        report_file = self.base_dir.parent / "extraction_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # 텍스트 보고서 저장
        text_report_file = self.base_dir.parent / "extraction_report.md"
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write("# PDF 콘텐츠 추출 보고서\n\n")
            f.write(f"**추출 일시:** 2025-08-06\n")
            f.write(f"**총 Leaf Node 수:** {len(self.leaf_nodes)}\n")
            f.write(f"**성공적 추출:** {success}개\n")
            f.write(f"**실패한 추출:** {failed}개\n")
            f.write(f"**성공률:** {100*success//len(self.leaf_nodes) if self.leaf_nodes else 0}%\n\n")
            
            f.write("## 상세 결과\n\n")
            for node in self.leaf_nodes:
                status_emoji = "✅" if node.extraction_status == "success" else "❌"
                f.write(f"- {status_emoji} **{node.title}**\n")
                f.write(f"  - 경로: `{node.parent_path}`\n")
                f.write(f"  - 페이지: {node.page_range[0]}-{node.page_range[1]}\n" if node.page_range else "  - 페이지: Unknown\n")
                f.write(f"  - 상태: {node.extraction_status}\n")
                f.write(f"  - 콘텐츠 길이: {len(node.content)} 문자\n\n")
        
        print(f"📄 추출 보고서 생성: {text_report_file}")

def main():
    """메인 실행 함수"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/Data_Extraction/Data_Oriented_Programming"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
        
    if not Path(base_dir).exists():
        print(f"❌ 기본 디렉토리를 찾을 수 없습니다: {base_dir}")
        print("먼저 toc_v2_folder_creator.py를 실행하세요.")
        return
    
    print("🚀 PDF 콘텐츠 추출 시작")
    print(f"📖 PDF: {pdf_path}")
    print(f"📁 기본 디렉토리: {base_dir}")
    
    extractor = PDFContentExtractor(pdf_path, base_dir)
    
    try:
        # Step 1: Leaf node 발견
        extractor.discover_leaf_nodes()
        
        # Step 2: 콘텐츠 추출
        extractor.extract_all_content()
        
        print("\n✅ PDF 콘텐츠 추출 완료!")
        
    except Exception as e:
        print(f"\n❌ 추출 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()