#!/usr/bin/env python3
"""
TOC 계층 구조 정규화 스크립트

목적: 계층적 목차 구조에서 서로 다른 계층 간에 내용이 있는 경우
     상위 계층에 "Intro" 접미사를 추가하여 동일한 레벨의 구성 단위로만
     이루어진 깔끔한 계층 구조를 만든다.

예시:
현재: 1 - [중간 내용] - 1.1 - [중간 내용] - 1.1.1
목표: 1 - 1 Intro - 1.1 - 1.1 Intro - 1.1.1
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class TOCItem:
    """목차 항목을 나타내는 클래스"""
    
    def __init__(self, level: int, number: str, title: str, raw_line: str):
        self.level = level  # 들여쓰기 레벨 (0, 1, 2, ...)
        self.number = number  # 섹션 번호 (1, 1.1, 1.1.1, ...)
        self.title = title  # 제목
        self.raw_line = raw_line  # 원본 라인
        self.number_parts = [int(x) for x in number.split('.')]  # [1], [1,1], [1,1,1] 등
    
    def __repr__(self):
        return f"TOCItem(level={self.level}, number='{self.number}', title='{self.title}')"
    
    def is_parent_of(self, other: 'TOCItem') -> bool:
        """다른 항목의 부모인지 확인"""
        if len(self.number_parts) >= len(other.number_parts):
            return False
        
        # 부모의 번호가 자식 번호의 접두사인지 확인
        return self.number_parts == other.number_parts[:len(self.number_parts)]
    
    def is_direct_parent_of(self, other: 'TOCItem') -> bool:
        """다른 항목의 직접 부모인지 확인 (바로 한 단계 위)"""
        return (len(other.number_parts) == len(self.number_parts) + 1 and
                self.number_parts == other.number_parts[:len(self.number_parts)])


class TOCHierarchyNormalizer:
    """TOC 계층 구조 정규화 클래스"""
    
    def __init__(self):
        self.toc_items: List[TOCItem] = []
        self.content_text = ""
    
    def parse_toc_file(self, toc_file_path: str) -> None:
        """TOC 파일을 파싱하여 계층 구조 추출"""
        with open(toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self.toc_items = []
        
        for line in lines:
            line = line.rstrip()
            if not line:
                continue
            
            # 번호가 있는 섹션 라인인지 확인
            # 예: "- 1.1 OOP design: Classic or classical?"
            #     "  - 1.1.1 The design phase"
            #     "### 1 Complexity of object-oriented programming"
            
            # 들여�기 레벨 계산
            indent_match = re.match(r'^(\s*)-?\s*', line)
            if indent_match:
                indent = len(indent_match.group(1).replace('\t', '    '))
                level = indent // 2  # 2칸 들여쓰기당 1레벨
            else:
                level = 0
            
            # 섹션 번호와 제목 추출
            # 패턴들: "### 1 Title", "- 1.1 Title", "  - 1.1.1 Title"
            patterns = [
                r'^#+\s*(\d+(?:\.\d+)*)\s+(.+)$',  # ### 1 Title
                r'^\s*-?\s*(\d+(?:\.\d+)*)\s+(.+)$',  # - 1.1 Title 또는   - 1.1.1 Title
            ]
            
            match_found = False
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    number = match.group(1)
                    title = match.group(2).strip()
                    
                    toc_item = TOCItem(level, number, title, line)
                    self.toc_items.append(toc_item)
                    match_found = True
                    break
            
            if not match_found and ('###' in line or re.search(r'\d+', line)):
                # 디버깅을 위해 매치되지 않은 라인 출력
                print(f"Warning: Could not parse line: {line}")
    
    def load_content_file(self, content_file_path: str) -> None:
        """실제 내용이 담긴 텍스트 파일 로드"""
        with open(content_file_path, 'r', encoding='utf-8') as f:
            self.content_text = f.read()
    
    def find_section_position(self, section_number: str) -> Optional[int]:
        """텍스트에서 특정 섹션의 위치를 찾음"""
        # 섹션 헤딩을 찾는 패턴들
        patterns = []
        
        # 단일 숫자인 경우 (예: "1") - 챕터 헤딩을 찾음
        if '.' not in section_number:
            patterns.extend([
                rf'^#\s*Chapter\s+{re.escape(section_number)}[:\s]',  # "# Chapter 1: Title"
                rf'^{re.escape(section_number)}\s+.+$',  # "1 Title"
                rf'^#.*{re.escape(section_number)}.*$',   # 일반적인 마크다운 헤딩
            ])
        else:
            # 하위 섹션인 경우 (예: "1.1", "1.1.1")
            patterns.extend([
                rf'^{re.escape(section_number)}\s+.+$',  # "1.1 Title"
                rf'^{re.escape(section_number)}\..*$',   # "1.1.1 Title" (점으로 시작하는 하위 섹션도 포함)
            ])
        
        lines = self.content_text.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    return i
        
        return None
    
    def has_content_between_sections(self, parent_item: TOCItem, child_item: TOCItem) -> bool:
        """두 섹션 사이에 내용이 있는지 확인"""
        parent_pos = self.find_section_position(parent_item.number)
        child_pos = self.find_section_position(child_item.number)
        
        if parent_pos is None or child_pos is None:
            return False
        
        if child_pos <= parent_pos:
            return False
        
        lines = self.content_text.split('\n')
        
        # 부모 섹션 다음 라인부터 자식 섹션 이전 라인까지 확인
        for i in range(parent_pos + 1, child_pos):
            line = lines[i].strip()
            if line and not line.startswith('#'):  # 비어있지 않고 헤딩이 아닌 라인
                return True
        
        return False
    
    def find_intro_insertions(self) -> List[Tuple[TOCItem, TOCItem]]:
        """Intro를 삽입해야 할 위치들을 찾음"""
        insertions = []
        
        for i, item in enumerate(self.toc_items):
            # 이 항목의 직접 자식들 찾기
            direct_children = []
            for j, other_item in enumerate(self.toc_items):
                if item.is_direct_parent_of(other_item):
                    direct_children.append(other_item)
            
            if direct_children:
                # 첫 번째 직접 자식과의 사이에 내용이 있는지 확인
                first_child = direct_children[0]
                if self.has_content_between_sections(item, first_child):
                    insertions.append((item, first_child))
        
        return insertions
    
    def generate_normalized_toc(self) -> str:
        """정규화된 TOC 생성"""
        intro_insertions = self.find_intro_insertions()
        
        # 삽입할 위치들을 기록
        insertions_dict = {}
        for parent, child in intro_insertions:
            insertions_dict[child] = parent
        
        result_lines = []
        
        for i, item in enumerate(self.toc_items):
            # 현재 항목 이전에 Intro를 삽입해야 하는지 확인
            if item in insertions_dict:
                parent = insertions_dict[item]
                # Intro 라인 생성
                intro_line = self._generate_intro_line(parent, item.level)
                result_lines.append(intro_line)
            
            # 현재 항목 추가
            result_lines.append(item.raw_line)
        
        return '\n'.join(result_lines)
    
    def _generate_intro_line(self, parent_item: TOCItem, child_level: int) -> str:
        """Intro 라인 생성"""
        # 자식과 같은 레벨의 들여쓰기 사용 (자식의 들여쓰기와 동일)
        indent = '  ' * child_level if child_level > 0 else ''
        prefix = '- '
        
        # 번호에 .0을 추가하고 사용자 추가 표시
        intro_number = f"{parent_item.number}.0"
        return f"{indent}{prefix}{intro_number} Intro (사용자 추가)"
    
    def normalize_toc(self, toc_file_path: str, content_file_path: str, output_file_path: str) -> None:
        """전체 정규화 프로세스 실행"""
        print(f"TOC 파일 파싱 중: {toc_file_path}")
        self.parse_toc_file(toc_file_path)
        print(f"파싱된 TOC 항목 수: {len(self.toc_items)}")
        
        print(f"내용 파일 로딩 중: {content_file_path}")
        self.load_content_file(content_file_path)
        
        print("계층 간 내용 존재 여부 분석 중...")
        intro_insertions = self.find_intro_insertions()
        
        print(f"Intro 삽입이 필요한 위치 {len(intro_insertions)}개 발견:")
        for parent, child in intro_insertions:
            print(f"  - {parent.number} '{parent.title}' → {child.number} '{child.title}' 사이")
        
        print("정규화된 TOC 생성 중...")
        normalized_toc = self.generate_normalized_toc()
        
        print(f"결과 파일 저장 중: {output_file_path}")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(normalized_toc)
        
        print("정규화 완료!")


def main():
    parser = argparse.ArgumentParser(description='TOC 계층 구조 정규화 도구')
    parser.add_argument('--toc', required=True, help='TOC 마크다운 파일 경로')
    parser.add_argument('--content', required=True, help='실제 내용이 담긴 텍스트 파일 경로')
    parser.add_argument('--output', required=True, help='출력 파일 경로')
    
    args = parser.parse_args()
    
    # 파일 존재 여부 확인
    if not Path(args.toc).exists():
        print(f"오류: TOC 파일을 찾을 수 없습니다: {args.toc}")
        return 1
    
    if not Path(args.content).exists():
        print(f"오류: 내용 파일을 찾을 수 없습니다: {args.content}")
        return 1
    
    # 출력 디렉토리 생성
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 정규화 실행
    try:
        normalizer = TOCHierarchyNormalizer()
        normalizer.normalize_toc(args.toc, args.content, args.output)
        return 0
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())