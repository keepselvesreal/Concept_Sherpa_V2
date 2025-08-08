#!/usr/bin/env python3
"""
TOC 정교화 스크립트

목적: 
1. 마크다운 목차 파일과 PDF 원본을 분석하여 서로 다른 구성 단위 간에 내용이 있는지 확인
2. 내용이 존재하는 경우 X.0 Introduction (사용자 추가) 형태로 항목을 삽입하여 계층 구조 정교화

특징:
- 같은 레벨 간(1.1.1 ↔ 1.1.2)은 확인하지 않음 (당연히 내용 존재)
- 서로 다른 레벨 간(1.1 ↔ 1.1.1)만 분석하여 중간 내용 존재 시 Introduction 항목 추가
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
import pdfplumber


class TOCItem:
    """목차 항목을 나타내는 클래스"""
    
    def __init__(self, level: int, number: str, title: str, raw_line: str, line_index: int):
        self.level = level  # 들여쓰기 레벨 (0, 1, 2, ...)
        self.number = number  # 섹션 번호 (1, 1.1, 1.1.1, A.1 등)
        self.title = title  # 제목
        self.raw_line = raw_line  # 원본 라인
        self.line_index = line_index  # 원본 파일에서의 라인 번호
        # 문자+숫자 형태도 처리 (A.1, B.2.1 등)
        self.number_parts = self._parse_number_parts(number)
    
    def _parse_number_parts(self, number: str) -> List:
        """번호를 파싱하여 비교 가능한 형태로 변환"""
        parts = []
        for part in number.split('.'):
            if part.isdigit():
                parts.append(('num', int(part)))
            elif len(part) > 0:
                parts.append(('str', part))
        return parts
    
    def __repr__(self):
        return f"TOCItem(level={self.level}, number='{self.number}', title='{self.title}')"
    
    def is_parent_of(self, other: 'TOCItem') -> bool:
        """다른 항목의 부모인지 확인"""
        if len(self.number_parts) >= len(other.number_parts):
            return False
        
        # 부모의 번호가 자식 번호의 접두사인지 확인
        return self.number_parts == other.number_parts[:len(self.number_parts)]
    
    def is_direct_parent_of(self, other: 'TOCItem') -> bool:
        """다른 항목의 직접 부모인지 확인 (바로 한 단계 위) - Part-Chapter 관계 포함"""
        
        # 특별 케이스: Part와 Chapter 관계 처리
        # Part 1 → Chapter 1, Part 2 → Chapter 7 등
        if (len(self.number_parts) == 1 and self.title and 
            ('flexibility' in self.title.lower() or 'scalability' in self.title.lower() or 'maintainability' in self.title.lower())):
            # Part 제목으로 판단
            if len(other.number_parts) == 1 and other.number_parts[0][0] == 'num':
                # Part 1 → Chapter 1-6, Part 2 → Chapter 7-11, Part 3 → Chapter 12-15
                part_num = self.number_parts[0][1]
                chapter_num = other.number_parts[0][1]
                
                if part_num == 1 and 1 <= chapter_num <= 6:
                    return True
                elif part_num == 2 and 7 <= chapter_num <= 11:
                    return True  
                elif part_num == 3 and 12 <= chapter_num <= 15:
                    return True
        
        # 일반적인 부모-자식 관계
        if len(other.number_parts) != len(self.number_parts) + 1:
            return False
        
        # 부모의 모든 파트가 자식의 접두사와 일치하는지 확인
        for i, parent_part in enumerate(self.number_parts):
            if i >= len(other.number_parts) or parent_part != other.number_parts[i]:
                return False
        
        return True
    
    def get_level_depth(self) -> int:
        """번호 깊이 반환 (1=1레벨, 1.1=2레벨, 1.1.1=3레벨)"""
        return len(self.number_parts)


class TOCNormalizer:
    """TOC 정교화 클래스"""
    
    def __init__(self):
        self.toc_items: List[TOCItem] = []
        self.pdf_text: str = ""
        self.pdf_pages: List[str] = []
        
    def parse_toc_markdown(self, toc_file_path: str) -> None:
        """향상된 마크다운 TOC 파일 파싱 - 모든 형태의 섹션 번호 지원"""  
        print(f"TOC 파일 파싱 중: {toc_file_path}")
        
        with open(toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self.toc_items = []
        
        for line_idx, line in enumerate(lines):
            line = line.rstrip()
            if not line:
                continue
            
            # 들여쓰기 레벨 계산
            indent_match = re.match(r'^(\s*)', line)
            if indent_match:
                indent = len(indent_match.group(1).replace('\t', '    '))
                if '- ' in line:
                    level = (indent + line.find('- ') + 2) // 2
                else:
                    level = indent // 2
            else:
                level = 0
            
            # 확장된 패턴들 - Appendix, Part, Chapter 모두 지원
            patterns = [
                # 기본 숫자 패턴
                r'^#+\s*(\d+(?:\.\d+)*)\s+(.+)$',                    # ### 1 Title
                r'^\s*-\s*(\d+(?:\.\d+)*)\s+(.+)$',                 # - 1.1 Title
                r'^\s*(\d+(?:\.\d+)*)\s+(.+)$',                     # 1.1 Title
                
                # Appendix 패턴 (A.1, B.2.1 등)
                r'^\s*-\s*([A-Z]\.\d+(?:\.\d+)*)\s+(.+)$',          # - A.1 Title
                r'^\s*([A-Z]\.\d+(?:\.\d+)*)\s+(.+)$',              # A.1 Title
                r'^#+\s*([A-Z]\.\d+(?:\.\d+)*)\s+(.+)$',            # ### A.1 Title
                
                # Part 패턴 
                r'^#+\s*Part\s+(\d+)\s*[—\-]\s*(.+)$',              # ## Part 1—Flexibility  
                r'^\s*-\s*Part\s+(\d+)\s*[—\-]\s*(.+)$',            # - Part 1—Flexibility
                
                # Chapter 패턴
                r'^#+\s*(Chapter\s+\d+)\s*[:\-]\s*(.+)$',           # ### Chapter 1: Title
            ]
            
            match_found = False
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    number = match.group(1)
                    title = match.group(2).strip()
                    
                    # Part는 번호 그대로 사용, Chapter는 번호만 추출
                    if 'part' in line.lower() and '—' in line:
                        # Part는 특별 처리하지 않음 - 이미 번호만 추출됨
                        pass
                    elif number.lower().startswith('chapter'):
                        number = re.search(r'(\d+)', number).group(1)
                    
                    toc_item = TOCItem(level, number, title, line, line_idx)
                    self.toc_items.append(toc_item)
                    match_found = True
                    break
            
            # 파싱 실패한 라인 출력 (번호가 포함된 경우만)
            if not match_found and re.search(r'[A-Z]?\d+', line) and not line.startswith('#'):
                print(f"Warning: 파싱 실패 라인 {line_idx + 1}: {line}")
        
        print(f"파싱된 TOC 항목 수: {len(self.toc_items)}")
        
        # 레벨별 통계
        level_counts = {}
        for item in self.toc_items:
            depth = item.get_level_depth()
            level_counts[depth] = level_counts.get(depth, 0) + 1
        
        print("레벨별 항목 수:")
        for depth in sorted(level_counts.keys()):
            print(f"  레벨 {depth}: {level_counts[depth]}개")
    
    def extract_pdf_content(self, pdf_file_path: str) -> None:
        """PDF에서 텍스트 내용 추출"""
        print(f"PDF 파일에서 텍스트 추출 중: {pdf_file_path}")
        
        try:
            with pdfplumber.open(pdf_file_path) as pdf:
                self.pdf_pages = []
                full_text = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        self.pdf_pages.append(page_text)
                        full_text.append(page_text)
                    else:
                        self.pdf_pages.append("")
                
                self.pdf_text = '\n'.join(full_text)
                print(f"추출된 페이지 수: {len(self.pdf_pages)}")
                print(f"총 텍스트 길이: {len(self.pdf_text):,} 문자")
                
        except Exception as e:
            print(f"PDF 추출 오류: {e}")
            raise
    
    def find_section_in_pdf(self, section_number: str, title: str) -> Optional[Tuple[int, int]]:
        """향상된 PDF 섹션 찾기 - 실제 책 내용에서 섹션 위치 탐지"""
        patterns = []
        
        # Part 섹션 특별 처리 (실제 책 내용에서)
        if section_number.isdigit() and title and any(keyword in title.lower() for keyword in ['flexibility', 'scalability', 'maintainability']):
            patterns.extend([
                rf'PART\s+{re.escape(section_number)}\s+{re.escape(title)}',
                rf'PART\s+{re.escape(section_number)}\s+{re.escape(title.title())}',
                rf'\d+\s+PART\s+{re.escape(section_number)}\s+{re.escape(title)}',
                rf'\d+\s+PART\s+{re.escape(section_number)}\s+{re.escape(title.title())}',
            ])
        
        # Chapter 섹션 특별 처리 (실제 책 내용에서) 
        elif section_number.isdigit() and title and not any(keyword in title.lower() for keyword in ['flexibility', 'scalability', 'maintainability']):
            # Chapter 패턴들 - 띄어쓰기나 연결된 텍스트 처리
            title_escaped = re.escape(title.replace(' ', '').replace('-', ''))  # 공백과 하이픈 제거
            title_partial = re.escape(title.split()[0] if title else '')  # 첫 단어만
            patterns.extend([
                rf'\d+\s+CHAPTER\s+{re.escape(section_number)}\s+{re.escape(title)}',
                rf'CHAPTER\s+{re.escape(section_number)}\s+{re.escape(title)}', 
                rf'\d+\s+CHAPTER\s+{re.escape(section_number)}\s+.*{title_partial}',  # 첫 단어 매칭
                rf'\d+\s+CHAPTER\s+{re.escape(section_number)}\s+.*{title_escaped}',  # 연결된 텍스트 매칭
            ])
            # Chapter는 백업 패턴 사용하지 않음 - 특정 패턴만 사용
            
        # 일반 섹션 처리 (. 포함된 경우)
        elif '.' in section_number:
            # 점이 포함된 경우 (1.1, 1.2.1, A.1 등)
            if title:
                title_clean = re.escape(title.strip())
                patterns.extend([
                    rf'{re.escape(section_number)}\.?\s+{title_clean}',
                    rf'^{re.escape(section_number)}\s+{title_clean}',
                ])
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'{re.escape(section_number)}\.?\s+[A-Z]',
            ])
        elif re.match(r'^[A-Z]\.\d+', section_number):
            # Appendix 형태 (A.1, B.2 등)
            if title:
                title_clean = re.escape(title.strip())
                patterns.extend([
                    rf'^{re.escape(section_number)}\s+{title_clean}',
                    rf'{re.escape(section_number)}\.?\s+{title_clean}',
                ])
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'{re.escape(section_number)}\.?\s+[A-Z]',
            ])
        
        # 각 페이지에서 검색 - TOC 페이지들 제외 (페이지 25 이후부터 검색)
        for page_num, page_text in enumerate(self.pdf_pages):
            if not page_text or page_num < 25:  # TOC 페이지들 제외
                continue
                
            lines = page_text.split('\n')
            for line_idx, line in enumerate(lines):
                line = line.strip()
                
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        return (page_num, line_idx)
        
        return None
    
    def check_content_between_levels(self, parent_item: TOCItem, child_item: TOCItem) -> bool:
        """서로 다른 레벨의 두 섹션 사이에 실질적인 내용이 있는지 확인"""
        
        # 부모-자식 관계가 아닌 경우 확인하지 않음
        if not parent_item.is_direct_parent_of(child_item):
            return False
        
        # Part-Chapter 관계는 같은 레벨 깊이여도 확인 (특별 케이스)
        is_part_chapter = (
            parent_item.get_level_depth() == child_item.get_level_depth() and
            parent_item.get_level_depth() == 1 and  # 둘 다 단일 숫자
            any(keyword in parent_item.title.lower() for keyword in ['flexibility', 'scalability', 'maintainability']) and
            any(keyword in child_item.title.lower() for keyword in ['complexity', 'separation', 'basic', 'state', 'concurrency', 'unit', 'validation', 'advanced', 'persistent', 'database', 'web', 'polymorphism', 'manipulation', 'debugging'])
        )
        
        # 일반적인 같은 레벨인 경우 확인하지 않음 (예: 1.1.1과 1.1.2)
        if parent_item.get_level_depth() == child_item.get_level_depth() and not is_part_chapter:
            return False
        
        print(f"내용 확인: {parent_item.number} '{parent_item.title}' → {child_item.number} '{child_item.title}'")
        
        # PDF에서 두 섹션의 위치 찾기
        parent_pos = self.find_section_in_pdf(parent_item.number, parent_item.title)
        child_pos = self.find_section_in_pdf(child_item.number, child_item.title)
        
        if parent_pos is None:
            print(f"  부모 섹션을 PDF에서 찾을 수 없음: {parent_item.number}")
            return False
            
        if child_pos is None:
            print(f"  자식 섹션을 PDF에서 찾을 수 없음: {child_item.number}")
            return False
        
        parent_page, parent_line = parent_pos
        child_page, child_line = child_pos
        
        print(f"  부모 위치: 페이지 {parent_page + 1}, 라인 {parent_line + 1}")
        print(f"  자식 위치: 페이지 {child_page + 1}, 라인 {child_line + 1}")
        
        # 자식이 부모보다 앞에 있으면 안됨
        if child_page < parent_page or (child_page == parent_page and child_line <= parent_line):
            print(f"  자식 섹션이 부모보다 앞에 위치함")
            return False
        
        # 중간 내용 확인
        content_lines = []
        
        if parent_page == child_page:
            # 같은 페이지 내에서 확인
            page_lines = self.pdf_pages[parent_page].split('\n')
            content_lines = page_lines[parent_line + 1:child_line]
        else:
            # 여러 페이지에 걸쳐 확인
            # 부모 섹션 이후 부분
            parent_page_lines = self.pdf_pages[parent_page].split('\n')
            content_lines.extend(parent_page_lines[parent_line + 1:])
            
            # 중간 페이지들 전체
            for page_idx in range(parent_page + 1, child_page):
                if page_idx < len(self.pdf_pages):
                    content_lines.extend(self.pdf_pages[page_idx].split('\n'))
            
            # 자식 섹션 이전 부분
            if child_page < len(self.pdf_pages):
                child_page_lines = self.pdf_pages[child_page].split('\n')
                content_lines.extend(child_page_lines[:child_line])
        
        # 실질적인 내용이 있는지 확인 (더 정확한 기준)
        meaningful_lines = 0
        for line in content_lines:
            line = line.strip()
            # 빈 줄, 페이지 번호, 짧은 라인 제외
            if line and not re.match(r'^\d+$', line) and len(line) > 15:
                # 다른 섹션 헤딩이 아닌지 확인 (Appendix 포함)
                if not re.match(r'^(\d+(\.\d+)*|[A-Z]\.\d+(\.\d+)*)\s+', line):
                    meaningful_lines += 1
                    if meaningful_lines >= 2:  # 2줄 이상의 의미 있는 내용이 있으면 true
                        print(f"  → 중간 내용 존재함 (의미있는 라인 {meaningful_lines}개)")
                        return True
        
        print(f"  → 중간 내용 없음 (의미있는 라인 {meaningful_lines}개)")
        return False
    
    def find_intro_insertions(self) -> List[Tuple[TOCItem, TOCItem]]:
        """Introduction을 삽입해야 할 위치들을 찾음 - 모든 자식에 대해 확인"""
        print("Introduction 삽입 위치 분석 중...")
        insertions = []
        
        for i, item in enumerate(self.toc_items):
            # 이 항목의 직접 자식들 찾기
            direct_children = []
            for other_item in self.toc_items:
                if item.is_direct_parent_of(other_item):
                    direct_children.append(other_item)
            
            if direct_children:
                # 번호 순으로 정렬
                direct_children.sort(key=lambda x: (len(x.number_parts), x.number_parts))
                
                # 모든 직접 자식과의 사이에 내용이 있는지 확인
                for child in direct_children:
                    if self.check_content_between_levels(item, child):
                        insertions.append((item, child))
                        break  # 하나라도 내용이 있으면 Introduction 필요
        
        return insertions
    
    def generate_intro_line(self, parent_item: TOCItem, child_item: TOCItem) -> str:
        """Introduction 라인 생성"""
        
        # Part-Chapter 관계인지 확인
        is_part_chapter = (
            parent_item.get_level_depth() == child_item.get_level_depth() and
            parent_item.get_level_depth() == 1 and
            any(keyword in parent_item.title.lower() for keyword in ['flexibility', 'scalability', 'maintainability']) and
            any(keyword in child_item.title.lower() for keyword in ['complexity', 'separation', 'basic', 'state', 'concurrency', 'unit', 'validation', 'advanced', 'persistent', 'database', 'web', 'polymorphism', 'manipulation', 'debugging'])
        )
        
        # Part-Chapter 사이는 Chapter와 동일한 레벨(###)로 생성, Part 번호 포함
        if is_part_chapter:
            return f"### Part {parent_item.number} Introduction (사용자 추가)"
        
        # 일반적인 경우: 자식과 동일한 레벨의 들여쓰기 사용
        child_line = child_item.raw_line
        
        # 자식 라인의 들여쓰기 패턴을 그대로 사용
        indent_match = re.match(r'^(\s*-?\s*)', child_line)
        if indent_match:
            prefix = indent_match.group(1)
        else:
            prefix = ""
        
        # 번호에 .0을 추가
        intro_number = f"{parent_item.number}.0"
        return f"{prefix}{intro_number} Introduction (사용자 추가)"
    
    def generate_normalized_toc(self) -> str:
        """정교화된 TOC 생성"""
        print("정교화된 TOC 생성 중...")
        
        intro_insertions = self.find_intro_insertions()
        
        print(f"Introduction 삽입이 필요한 위치 {len(intro_insertions)}개 발견:")
        for parent, child in intro_insertions:
            print(f"  - {parent.number} '{parent.title}' → {child.number} '{child.title}' 사이")
        
        # 삽입할 위치들을 기록 (자식 항목을 키로 사용)
        insertions_dict = {}
        for parent, child in intro_insertions:
            insertions_dict[child.line_index] = (parent, child)
        
        # 원본 파일을 다시 읽어서 라인별로 처리
        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()
        
        result_lines = []
        
        for line_idx, line in enumerate(original_lines):
            # 현재 라인 이전에 Introduction을 삽입해야 하는지 확인
            if line_idx in insertions_dict:
                parent, child = insertions_dict[line_idx]
                intro_line = self.generate_intro_line(parent, child)
                result_lines.append(intro_line + '\n')
            
            # 현재 라인 추가
            result_lines.append(line)
        
        return ''.join(result_lines)
    
    def normalize_toc(self, toc_file_path: str, pdf_file_path: str, output_file_path: str) -> None:
        """전체 정교화 프로세스 실행"""
        self.toc_file_path = toc_file_path
        
        # 1단계: TOC 마크다운 파싱
        self.parse_toc_markdown(toc_file_path)
        
        # 2단계: PDF 내용 추출
        self.extract_pdf_content(pdf_file_path)
        
        # 3단계: 정교화된 TOC 생성
        normalized_toc = self.generate_normalized_toc()
        
        # 4단계: 결과 저장
        print(f"결과 파일 저장 중: {output_file_path}")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(normalized_toc)
        
        print("TOC 정교화 완료!")


def main():
    parser = argparse.ArgumentParser(description='TOC 정교화 도구 - PDF 분석 기반')
    parser.add_argument('--toc', required=True, help='TOC 마크다운 파일 경로')
    parser.add_argument('--pdf', required=True, help='PDF 원본 파일 경로')
    parser.add_argument('--output', required=True, help='출력 파일 경로')
    
    args = parser.parse_args()
    
    # 파일 존재 여부 확인
    if not Path(args.toc).exists():
        print(f"오류: TOC 파일을 찾을 수 없습니다: {args.toc}")
        return 1
    
    if not Path(args.pdf).exists():
        print(f"오류: PDF 파일을 찾을 수 없습니다: {args.pdf}")
        return 1
    
    # 출력 디렉토리 생성
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 정교화 실행
    try:
        normalizer = TOCNormalizer()
        normalizer.normalize_toc(args.toc, args.pdf, args.output)
        return 0
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())