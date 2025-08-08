#!/usr/bin/env python3
"""
TOC 노드 구조 기반 폴더 및 파일 생성 스크립트
- 기본 node0/node1/node2/node3/node4 구조 유지
- node2에서 Chapter별 추가 조직화 (Chapter01-15, AppendixA-D, Part-Introduction)
- Leaf 노드에 [CONTENT] 표시 및 내용 추출
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class TOCNodeStructureCreator:
    def __init__(self, toc_file_path: str, base_output_dir: str):
        self.toc_file_path = toc_file_path
        self.base_output_dir = Path(base_output_dir)
        self.toc_structure = []
        self.leaf_nodes = set()
        
    def parse_toc_file(self):
        """TOC 파일을 파싱하여 노드 구조 분석"""
        print("TOC 파일 파싱 중...")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
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
                
                self.toc_structure.append({
                    'line_num': line_num,
                    'content': content,
                    'node_level': node_level,
                    'indent_level': indent_level,
                    'original_line': original_line.strip()
                })
        
        print(f"총 {len(self.toc_structure)}개 항목 파싱 완료")
        
        # 디버깅: node1 항목들 확인
        node1_items = [item for item in self.toc_structure if item['node_level'] == 1]
        print(f"node1 항목 수: {len(node1_items)}")
        for item in node1_items:
            print(f"  - {item['content']}")
        
        return self.toc_structure
    
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
    
    def get_chapter_folder(self, content: str, node_level: int) -> Optional[str]:
        """Chapter별 폴더명 결정"""
        if node_level != 2:  # node2 레벨에서만 Chapter 폴더 생성
            return None
            
        print(f"  Chapter 폴더 확인: '{content}'")
            
        # Chapter 패턴 매칭
        if re.match(r'^\d+\s+', content):  # "1 Title" -> "Chapter01"
            chapter_num = re.match(r'^(\d+)', content).group(1)
            folder_name = f"Chapter{chapter_num.zfill(2)}"
            print(f"    -> Chapter 폴더: {folder_name}")
            return folder_name
            
        elif "Part" in content and "Introduction" in content:  # "Part1 Introduction" -> "Part1-Introduction"
            if re.match(r'^Part\d+\s+Introduction', content):
                folder_name = content.replace(' ', '-')
                print(f"    -> Part Introduction 폴더: {folder_name}")
                return folder_name
                
        elif content.startswith('A.'):  # "A.0 Introduction" -> "AppendixA"
            folder_name = "AppendixA"
            print(f"    -> Appendix A 폴더: {folder_name}")
            return folder_name
            
        elif content.startswith('B.'):  # "B.0 Introduction" -> "AppendixB"
            folder_name = "AppendixB"
            print(f"    -> Appendix B 폴더: {folder_name}")
            return folder_name
            
        elif content.startswith('C.'):  # "C.0 Introduction" -> "AppendixC"
            folder_name = "AppendixC"
            print(f"    -> Appendix C 폴더: {folder_name}")
            return folder_name
            
        elif "Conclusion" in content:  # Appendix A의 Conclusion
            folder_name = "AppendixA"
            print(f"    -> Appendix A 폴더 (Conclusion): {folder_name}")
            return folder_name
            
        elif "Summary" in content:  # Appendix B, C의 Summary
            # Summary의 위치에 따라 결정... 우선 AppendixB로
            folder_name = "AppendixB" 
            print(f"    -> Appendix B 폴더 (Summary): {folder_name}")
            return folder_name
            
        print(f"    -> Chapter 폴더 없음")
        return None
    
    def create_folder_structure(self):
        """기본 노드 폴더 구조 생성"""
        print("폴더 구조 생성 중...")
        
        # 기본 node 폴더들 생성
        for i in range(5):  # node0 ~ node4
            node_path = self.base_output_dir
            for j in range(i + 1):
                node_path = node_path / f"node{j}"
                node_path.mkdir(parents=True, exist_ok=True)
        
        print("기본 노드 폴더 구조 생성 완료")
    
    def create_chapter_folders(self):
        """node2 레벨에서 Chapter별 폴더 생성"""
        print("Chapter별 폴더 생성 중...")
        
        chapter_folders = set()
        
        # node2 레벨의 항목들에서 Chapter 폴더 필요한 것들 식별
        for item in self.toc_structure:
            if item['node_level'] == 2:
                chapter_folder = self.get_chapter_folder(item['content'], 2)
                if chapter_folder:
                    chapter_folders.add(chapter_folder)
        
        # Chapter 폴더 생성
        node2_path = self.base_output_dir / "node0" / "node1" / "node2"
        for folder in chapter_folders:
            folder_path = node2_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  생성: {folder}")
        
        print(f"총 {len(chapter_folders)}개 Chapter 폴더 생성 완료")
        return chapter_folders
    
    def create_markdown_files(self):
        """각 노드 레벨에 .md 파일 생성"""
        print("마크다운 파일 생성 중...")
        
        file_count = 0
        
        for i, item in enumerate(self.toc_structure):
            content = item['content']
            node_level = item['node_level']
            is_leaf = i in self.leaf_nodes
            
            # 파일명 결정
            filename = self.sanitize_filename(content)
            if is_leaf:
                filename += " [CONTENT]"
            filename += ".md"
            
            # 파일 경로 결정
            file_path = self.base_output_dir
            
            # 기본 노드 경로
            for j in range(node_level + 1):
                file_path = file_path / f"node{j}"
            
            # Chapter 폴더가 필요한 경우
            if node_level == 2:
                chapter_folder = self.get_chapter_folder(content, node_level)
                if chapter_folder:
                    file_path = file_path.parent / chapter_folder / f"node{node_level}"
                    file_path.mkdir(parents=True, exist_ok=True)
            
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
            
            # 파일 생성
            full_file_path = file_path / filename
            with open(full_file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            file_count += 1
            
            if file_count % 50 == 0:
                print(f"  {file_count}개 파일 생성 중...")
        
        print(f"총 {file_count}개 마크다운 파일 생성 완료")
    
    def create_summary_report(self):
        """생성 결과 요약 보고서"""
        report_path = self.base_output_dir / "folder_structure_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# TOC 노드 구조 생성 결과 보고서\n\n")
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
            
            f.write("\n## 폴더 구조\n")
            f.write("```\n")
            f.write("node0/\n")
            f.write("├── Data-Oriented Programming.md\n")
            f.write("└── node1/\n")
            f.write("    ├── Part1—Flexibility.md\n")
            f.write("    ├── Part2—Scalability.md\n")
            f.write("    ├── Part3—Maintainability.md\n")
            f.write("    ├── Appendix A—....md\n")
            f.write("    └── node2/\n")
            f.write("        ├── Chapter01/\n")
            f.write("        ├── Chapter02/\n")
            f.write("        ├── AppendixA/\n")
            f.write("        └── [기타 Chapter 폴더들...]\n")
            f.write("```\n")
        
        print(f"보고서 생성 완료: {report_path}")
    
    def run(self):
        """전체 프로세스 실행"""
        print("=== TOC 노드 구조 생성 시작 ===")
        
        # 1. TOC 파일 파싱
        self.parse_toc_file()
        
        # 2. Leaf 노드 식별
        self.identify_leaf_nodes()
        
        # 3. 기본 폴더 구조 생성
        self.create_folder_structure()
        
        # 4. Chapter 폴더 생성
        self.create_chapter_folders()
        
        # 5. 마크다운 파일 생성
        self.create_markdown_files()
        
        # 6. 보고서 생성
        self.create_summary_report()
        
        print("=== TOC 노드 구조 생성 완료 ===")

if __name__ == "__main__":
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/normalized_toc_with_node_types_v3.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    creator = TOCNodeStructureCreator(toc_file, output_dir)
    creator.run()