#!/usr/bin/env python3
"""
TOC 노드 구조 기반 올바른 중첩 조직화 폴더 및 파일 생성 스크립트
- node 구조 우선: node0/node1/node2/node3/node4
- 동일 섹션 조직화: Part별, Chapter별 조직화를 적절한 node 레벨에 적용
- 올바른 중첩: Part1/node3/ch1/ 형태로 구성
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class TOCNestedStructureCreator:
    def __init__(self, toc_file_path: str, base_output_dir: str):
        self.toc_file_path = toc_file_path
        self.base_output_dir = Path(base_output_dir)
        self.toc_structure = []
        self.leaf_nodes = set()
        
        # 각 항목의 Part/Chapter 매핑
        self.part_mapping = {}
        self.chapter_mapping = {}
        self.appendix_mapping = {}
        
    def parse_toc_file(self):
        """TOC 파일을 파싱하여 노드 구조 분석"""
        print("TOC 파일 파싱 중...")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_part = None
        current_appendix = None
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # 노드 정보 추출
            node_match = re.search(r'\(node(\d+)\)$', line)
            if node_match:
                node_level = int(node_match.group(1))
                content = line[:node_match.start()].strip()
                
                # 들여쓰기 레벨 계산
                indent_level = 0
                original_line = lines[line_num - 1]
                for char in original_line:
                    if char == ' ':
                        indent_level += 1
                    elif char == '\t':
                        indent_level += 4
                    else:
                        break
                        
                # '- ' 제거 및 헤더 처리
                if content.startswith('- '):
                    content = content[2:]
                elif content.startswith('#'):
                    # 헤더에서 # 제거
                    content = re.sub(r'^#+\s*', '', content)
                
                # Part/Chapter/Appendix 매핑
                part = self.get_part(content, node_level)
                chapter = self.get_chapter(content, node_level)
                appendix = self.get_appendix(content, node_level)
                
                # 현재 Part/Appendix 추적
                if node_level == 1 and "Part" in content:
                    current_part = part
                elif node_level == 1 and "Appendix" in content:
                    current_appendix = appendix
                
                self.toc_structure.append({
                    'line_num': line_num,
                    'content': content,
                    'node_level': node_level,
                    'indent_level': indent_level,
                    'part': current_part if node_level > 1 and current_part else part,
                    'chapter': chapter,
                    'appendix': current_appendix if node_level > 1 and current_appendix else appendix,
                    'original_line': original_line.strip()
                })
        
        print(f"총 {len(self.toc_structure)}개 항목 파싱 완료")
        return self.toc_structure
    
    def get_part(self, content: str, node_level: int) -> Optional[str]:
        """Part 결정"""
        if node_level == 1 and "Part" in content:
            if "Part1" in content or "Flexibility" in content:
                return "Part1"
            elif "Part2" in content or "Scalability" in content:
                return "Part2"
            elif "Part3" in content or "Maintainability" in content:
                return "Part3"
        return None
    
    def get_chapter(self, content: str, node_level: int) -> Optional[str]:
        """Chapter 결정"""
        if node_level >= 3:  # node3부터 Chapter별 조직화
            # Chapter 번호 추출 (1.0, 2.1 등의 형태)
            chapter_match = re.match(r'^(\d+)\.', content)
            if chapter_match:
                return f"ch{chapter_match.group(1)}"
        return None
    
    def get_appendix(self, content: str, node_level: int) -> Optional[str]:
        """Appendix 결정"""
        if node_level == 1 and "Appendix" in content:
            if "Appendix A" in content:
                return "AppendixA"
            elif "Appendix B" in content:
                return "AppendixB"
            elif "Appendix C" in content:
                return "AppendixC"
            elif "Appendix D" in content:
                return "AppendixD"
        elif node_level >= 2:
            if content.startswith('A.'):
                return "AppendixA"
            elif content.startswith('B.'):
                return "AppendixB"
            elif content.startswith('C.'):
                return "AppendixC"
        return None
    
    def get_appendix_section(self, content: str) -> Optional[str]:
        """Appendix 섹션 결정"""
        if content.startswith('A.1'):
            return "A1-Section"
        elif content.startswith('A.2'):
            return "A2-Section"
        elif content.startswith('A.3'):
            return "A3-Section"
        elif content.startswith('A.4'):
            return "A4-Section"
        elif content.startswith('B.1'):
            return "B1-Section"
        elif content.startswith('B.2'):
            return "B2-Section"
        elif content.startswith('B.3'):
            return "B3-Section"
        elif content.startswith('B.4'):
            return "B4-Section"
        elif content.startswith('C.1'):
            return "C1-Section"
        elif content.startswith('C.2'):
            return "C2-Section"
        elif content.startswith('C.3'):
            return "C3-Section"
        return None
    
    def identify_leaf_nodes(self):
        """Leaf 노드 식별 (하위 노드가 없는 최종 노드들)"""
        print("Leaf 노드 식별 중...")
        
        # 각 항목의 다음 항목과 비교하여 leaf 노드 식별
        for i, item in enumerate(self.toc_structure):
            is_leaf = True
            current_level = item['node_level']
            
            # 다음 항목들을 확인하여 더 깊은 레벨이 있는지 체크
            for j in range(i + 1, len(self.toc_structure)):
                next_item = self.toc_structure[j]
                next_level = next_item['node_level']
                
                if next_level > current_level:
                    is_leaf = False
                    break
                elif next_level <= current_level:
                    break
                    
            if is_leaf:
                self.leaf_nodes.add(i)
        
        print(f"총 {len(self.leaf_nodes)}개 Leaf 노드 식별됨")
        return self.leaf_nodes
    
    def sanitize_filename(self, filename: str) -> str:
        """파일명에서 특수문자 제거 및 정규화"""
        # 특수문자를 안전한 문자로 변경
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'[#]', '', filename)  # # 제거
        filename = filename.replace('?', '')
        filename = filename.replace(':', '')
        filename = filename.replace('—', '-')  # em dash를 일반 dash로
        filename = filename.strip()
        
        # 길이 제한 (200자)
        if len(filename) > 200:
            filename = filename[:200]
            
        return filename
    
    def create_folder_structure(self):
        """기본 노드 폴더 구조 생성"""
        print("기본 폴더 구조 생성 중...")
        
        # 기본 node 폴더들 생성
        for i in range(5):  # node0 ~ node4
            node_path = self.base_output_dir
            for j in range(i + 1):
                node_path = node_path / f"node{j}"
                node_path.mkdir(parents=True, exist_ok=True)
        
        print("기본 노드 폴더 구조 생성 완료")
    
    def create_section_folders(self):
        """섹션별 폴더 생성 (Part, Appendix, Chapter)"""
        print("섹션별 폴더 생성 중...")
        
        # Part 폴더들 (node2 레벨)
        node2_path = self.base_output_dir / "node0" / "node1" / "node2"
        part_folders = ["Part1", "Part2", "Part3", "AppendixA", "AppendixB", "AppendixC"]
        
        for part in part_folders:
            part_path = node2_path / part
            part_path.mkdir(parents=True, exist_ok=True)
            print(f"  생성: {part}")
        
        # Chapter 폴더들 (각 Part의 node3 레벨)
        chapters = set()
        appendix_sections = set()
        
        for item in self.toc_structure:
            if item['chapter'] and item['node_level'] >= 3:
                chapters.add(item['chapter'])
            
            appendix_section = self.get_appendix_section(item['content'])
            if appendix_section and item['node_level'] >= 3:
                appendix_sections.add(appendix_section)
        
        # Part별 Chapter 폴더 생성 (해당 Part에 속하는 Chapter만)
        part_chapters = {
            "Part1": set(),
            "Part2": set(), 
            "Part3": set()
        }
        
        # 각 Part에 속하는 Chapter 분류
        for item in self.toc_structure:
            if item['part'] and item['chapter'] and item['node_level'] >= 3:
                part_chapters[item['part']].add(item['chapter'])
        
        for part in ["Part1", "Part2", "Part3"]:
            if part_chapters[part]:  # 해당 Part에 Chapter가 있는 경우만
                part_node3_path = node2_path / part / "node3"
                part_node3_path.mkdir(parents=True, exist_ok=True)
                
                for chapter in sorted(part_chapters[part]):
                    chapter_path = part_node3_path / chapter
                    chapter_path.mkdir(parents=True, exist_ok=True)
                    
                    # node4 폴더도 미리 생성
                    node4_path = chapter_path / "node4"
                    node4_path.mkdir(parents=True, exist_ok=True)
                    print(f"  생성: {part}/node3/{chapter}")
        
        # Appendix 섹션 폴더 생성
        for appendix in ["AppendixA", "AppendixB", "AppendixC"]:
            appendix_node3_path = node2_path / appendix / "node3"
            appendix_node3_path.mkdir(parents=True, exist_ok=True)
            
            for section in sorted(appendix_sections):
                if section.startswith(appendix[8]):  # A, B, C 매칭
                    section_path = appendix_node3_path / section
                    section_path.mkdir(parents=True, exist_ok=True)
                    print(f"  생성: {appendix}/node3/{section}")
        
        print("섹션별 폴더 생성 완료")
    
    def create_markdown_files(self):
        """각 노드 레벨에 .md 파일 생성"""
        print("마크다운 파일 생성 중...")
        
        file_count = 0
        
        for i, item in enumerate(self.toc_structure):
            content = item['content']
            node_level = item['node_level']
            is_leaf = i in self.leaf_nodes
            part = item['part']
            chapter = item['chapter']
            appendix = item['appendix']
            
            # 파일명 결정
            filename = self.sanitize_filename(content)
            if is_leaf:
                filename += " [CONTENT]"
            filename += ".md"
            
            # 파일 경로 결정
            file_path = self.get_file_path(item)
            
            # 파일 내용 생성
            file_content = f"# {content}\n\n"
            
            if is_leaf:
                file_content += "## 내용\n\n"
                file_content += "[여기에 원자료에서 추출한 내용이 포함될 예정]\n\n"
                file_content += f"**노드 레벨**: node{node_level}  \n"
                file_content += f"**파일 타입**: 내용 포함 (Leaf 노드)  \n"
            else:
                file_content += f"**노드 레벨**: node{node_level}  \n"
                file_content += f"**파일 타입**: 구조 노드  \n"
            
            if part:
                file_content += f"**Part**: {part}  \n"
            if chapter:
                file_content += f"**Chapter**: {chapter}  \n"
            if appendix:
                file_content += f"**Appendix**: {appendix}  \n"
            
            # 파일 생성
            full_file_path = file_path / filename
            full_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            file_count += 1
            
            if file_count % 50 == 0:
                print(f"  {file_count}개 파일 생성 중...")
        
        print(f"총 {file_count}개 마크다운 파일 생성 완료")
    
    def get_file_path(self, item):
        """항목에 따른 올바른 파일 경로 결정"""
        node_level = item['node_level']
        part = item['part']
        chapter = item['chapter']
        appendix = item['appendix']
        content = item['content']
        
        # 기본 경로 (node0, node1용)
        if node_level <= 1:
            base_path = self.base_output_dir
            for i in range(node_level + 1):
                base_path = base_path / f"node{i}"
            return base_path
        
        # node2 레벨: Part/Appendix 폴더 안에
        elif node_level == 2:
            base_path = self.base_output_dir / "node0" / "node1" / "node2"
            if part:
                return base_path / part
            elif appendix:
                return base_path / appendix
            else:
                return base_path
        
        # node3 레벨: Chapter/Appendix Section 폴더 안에
        elif node_level == 3:
            base_path = self.base_output_dir / "node0" / "node1" / "node2"
            if part and chapter:
                return base_path / part / "node3" / chapter
            elif appendix:
                appendix_section = self.get_appendix_section(content)
                if appendix_section:
                    return base_path / appendix / "node3" / appendix_section
                else:
                    # Appendix의 일반적인 node3 파일들 (A.0, Conclusion, Summary 등)
                    return base_path / appendix
            else:
                # Part/Appendix 없는 일반적인 node3 파일들
                base_path = self.base_output_dir
                for i in range(node_level + 1):
                    base_path = base_path / f"node{i}"
                return base_path
        
        # node4 레벨: Chapter의 node4 폴더 안에
        elif node_level == 4:
            base_path = self.base_output_dir / "node0" / "node1" / "node2"
            if part and chapter:
                return base_path / part / "node3" / chapter / "node4"
            elif appendix:
                # node4가 어느 appendix section에 속하는지 판단하기 위해
                # 앞선 항목들을 역추적해서 찾아야 함
                # 우선 간단하게 기본 node4 경로로 처리
                base_path = self.base_output_dir
                for i in range(node_level + 1):
                    base_path = base_path / f"node{i}"
                return base_path
            else:
                base_path = self.base_output_dir
                for i in range(node_level + 1):
                    base_path = base_path / f"node{i}"
                return base_path
        
        # 기타 (예외 상황)
        else:
            base_path = self.base_output_dir
            for i in range(node_level + 1):
                base_path = base_path / f"node{i}"
            return base_path
    
    def create_summary_report(self):
        """생성 결과 요약 보고서"""
        report_path = self.base_output_dir / "nested_structure_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# TOC 중첩 조직화 구조 생성 결과 보고서\n\n")
            f.write(f"## 기본 정보\n")
            f.write(f"- **생성 일시**: {Path().absolute()}\n")
            f.write(f"- **TOC 소스**: {self.toc_file_path}\n")
            f.write(f"- **출력 디렉터리**: {self.base_output_dir}\n\n")
            
            f.write(f"## 생성 통계\n")
            f.write(f"- **총 TOC 항목 수**: {len(self.toc_structure)}\n")
            f.write(f"- **Leaf 노드 수**: {len(self.leaf_nodes)}\n")
            f.write(f"- **구조 노드 수**: {len(self.toc_structure) - len(self.leaf_nodes)}\n\n")
            
            # 노드 레벨별 통계
            f.write("## 노드 레벨별 분포\n")
            level_counts = {}
            for item in self.toc_structure:
                level = item['node_level']
                level_counts[level] = level_counts.get(level, 0) + 1
            
            for level in sorted(level_counts.keys()):
                f.write(f"- **node{level}**: {level_counts[level]}개\n")
            
            f.write("\n## 중첩 조직화 구조\n")
            f.write("```\n")
            f.write("node0/\n")
            f.write("├── Data-Oriented Programming.md\n")
            f.write("└── node1/\n")
            f.write("    ├── Part1-Flexibility.md\n")
            f.write("    └── node2/\n")
            f.write("        ├── Part1/\n")
            f.write("        │   ├── [Part1 node2 파일들...]\n")
            f.write("        │   └── node3/\n")
            f.write("        │       ├── ch1/\n")
            f.write("        │       │   ├── [Chapter1 node3 파일들...]\n")
            f.write("        │       │   └── node4/\n")
            f.write("        │       │       └── [Chapter1 node4 파일들...]\n")
            f.write("        │       └── [기타 Chapter 폴더들...]\n")
            f.write("        └── [기타 Part/Appendix 폴더들...]\n")
            f.write("```\n")
        
        print(f"보고서 생성 완료: {report_path}")
    
    def run(self):
        """전체 프로세스 실행"""
        print("=== TOC 중첩 조직화 구조 생성 시작 ===")
        
        # 1. TOC 파일 파싱
        self.parse_toc_file()
        
        # 2. Leaf 노드 식별
        self.identify_leaf_nodes()
        
        # 3. 기본 폴더 구조 생성
        self.create_folder_structure()
        
        # 4. 섹션별 폴더 생성
        self.create_section_folders()
        
        # 5. 마크다운 파일 생성
        self.create_markdown_files()
        
        # 6. 보고서 생성
        self.create_summary_report()
        
        print("=== TOC 중첩 조직화 구조 생성 완료 ===")

if __name__ == "__main__":
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v3.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    creator = TOCNestedStructureCreator(toc_file, output_dir)
    creator.run()