#!/usr/bin/env python3
"""
Content Analyzer - TDD RED 단계
PDF 전체 분석을 통해 모든 서로 다른 레벨 간 내용 존재 여부를 병렬로 확인하여
필요한 모든 Introduction 항목을 식별하는 스크립트

이 결과는 "테스트 케이스"로 사용되어 toc_normalizer.py가 모든 항목을 
올바르게 탐지할 때까지 개선하는데 활용됩니다.
"""

import argparse
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import pdfplumber


class TOCItem:
    """목차 항목을 나타내는 클래스"""
    
    def __init__(self, level: int, number: str, title: str, raw_line: str, line_index: int):
        self.level = level
        self.number = number
        self.title = title
        self.raw_line = raw_line
        self.line_index = line_index
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
    
    def is_direct_parent_of(self, other: 'TOCItem') -> bool:
        """다른 항목의 직접 부모인지 확인"""
        if len(other.number_parts) != len(self.number_parts) + 1:
            return False
        
        # 부모의 모든 파트가 자식의 접두사와 일치하는지 확인
        for i, parent_part in enumerate(self.number_parts):
            if i >= len(other.number_parts) or parent_part != other.number_parts[i]:
                return False
        
        return True
    
    def get_level_depth(self) -> int:
        """번호 깊이 반환"""
        return len(self.number_parts)


class ContentAnalyzer:
    """PDF 내용 분석기 - 병렬 처리 지원"""
    
    def __init__(self):
        self.toc_items: List[TOCItem] = []
        self.pdf_pages: List[str] = []
        
    def parse_comprehensive_toc(self, toc_file_path: str) -> None:
        """포괄적 TOC 파싱 - 모든 형태의 섹션 번호 지원"""
        print(f"포괄적 TOC 파싱 중: {toc_file_path}")
        
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
                r'^#+\s*(Part\s+\d+)\s*[—\-]\s*(.+)$',              # ## Part 1—Flexibility
                r'^\s*-\s*(Part\s+\d+)\s*[—\-]\s*(.+)$',            # - Part 1—Flexibility
                
                # Chapter 패턴
                r'^#+\s*(Chapter\s+\d+)\s*[:\-]\s*(.+)$',           # ### Chapter 1: Title
            ]
            
            match_found = False
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    number = match.group(1)
                    title = match.group(2).strip()
                    
                    # Part와 Chapter 형태는 번호만 추출
                    if number.lower().startswith('part'):
                        number = re.search(r'(\d+)', number).group(1)
                    elif number.lower().startswith('chapter'):
                        number = re.search(r'(\d+)', number).group(1)
                    
                    toc_item = TOCItem(level, number, title, line, line_idx)
                    self.toc_items.append(toc_item)
                    match_found = True
                    break
            
            # 파싱 실패한 라인 출력 (번호가 포함된 경우만)
            if not match_found and re.search(r'[A-Z]?\d+', line) and not line.startswith('#'):
                print(f"Warning: 파싱 실패 라인 {line_idx + 1}: {line}")
        
        print(f"파싱된 총 TOC 항목 수: {len(self.toc_items)}")
        
        # 레벨별 통계
        level_stats = {}
        for item in self.toc_items:
            depth = item.get_level_depth()
            level_stats[depth] = level_stats.get(depth, 0) + 1
        
        print("레벨별 항목 수:")
        for depth in sorted(level_stats.keys()):
            print(f"  레벨 {depth}: {level_stats[depth]}개")
    
    def extract_pdf_content(self, pdf_file_path: str) -> None:
        """PDF 내용 추출"""
        print(f"PDF 내용 추출 중: {pdf_file_path}")
        
        try:
            with pdfplumber.open(pdf_file_path) as pdf:
                self.pdf_pages = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        self.pdf_pages.append(page_text)
                    else:
                        self.pdf_pages.append("")
                
                print(f"추출된 페이지 수: {len(self.pdf_pages)}")
                
        except Exception as e:
            print(f"PDF 추출 오류: {e}")
            raise
    
    def find_section_in_pdf_enhanced(self, section_number: str, title: str) -> Optional[Tuple[int, int]]:
        """향상된 PDF 섹션 찾기"""
        patterns = []
        
        # 제목과 함께 매칭 (우선순위 높음)
        if title:
            title_clean = re.escape(title.strip())
            patterns.extend([
                rf'{re.escape(section_number)}\s+{title_clean}',
                rf'Chapter\s+{re.escape(section_number)}\s*[:\-\s]*{title_clean}',
                rf'{re.escape(section_number)}\.?\s+{title_clean}',
                rf'Part\s+{re.escape(section_number)}\s*[—\-]\s*{title_clean}',
            ])
        
        # 번호만으로 매칭 (백업)
        if '.' not in section_number and section_number.isdigit():
            # 숫자만인 경우 (1, 2, 3...)
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'Chapter\s+{re.escape(section_number)}[^\d]',
                rf'Part\s+{re.escape(section_number)}[^\d]',
            ])
        elif '.' in section_number:
            # 점이 포함된 경우 (1.1, 1.2.1, A.1 등)
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'{re.escape(section_number)}\.?\s+[A-Z]',
            ])
        elif re.match(r'^[A-Z]\.\d+', section_number):
            # Appendix 형태 (A.1, B.2 등)
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'{re.escape(section_number)}\.?\s+[A-Z]',
            ])
        
        # 각 페이지에서 검색
        for page_num, page_text in enumerate(self.pdf_pages):
            if not page_text:
                continue
                
            lines = page_text.split('\n')
            for line_idx, line in enumerate(lines):
                line = line.strip()
                
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        return (page_num, line_idx)
        
        return None
    
    def check_content_between_sections(self, args_tuple: Tuple) -> Dict:
        """단일 섹션 쌍의 내용 존재 여부 확인 (병렬 처리용)"""
        parent_item, child_item, pdf_pages = args_tuple
        
        result = {
            'parent': parent_item.number,
            'parent_title': parent_item.title,
            'child': child_item.number,
            'child_title': child_item.title,
            'has_content': False,
            'content_lines': 0,
            'found_parent': False,
            'found_child': False
        }
        
        # PDF에서 섹션 위치 찾기
        parent_pos = self.find_section_in_pdf_enhanced(parent_item.number, parent_item.title)
        child_pos = self.find_section_in_pdf_enhanced(child_item.number, child_item.title)
        
        if parent_pos is None:
            return result
            
        if child_pos is None:
            return result
        
        result['found_parent'] = True
        result['found_child'] = True
        
        parent_page, parent_line = parent_pos
        child_page, child_line = child_pos
        
        # 자식이 부모보다 앞에 있으면 안됨
        if child_page < parent_page or (child_page == parent_page and child_line <= parent_line):
            return result
        
        # 중간 내용 확인
        content_lines = []
        
        if parent_page == child_page:
            # 같은 페이지
            page_lines = pdf_pages[parent_page].split('\n')
            content_lines = page_lines[parent_line + 1:child_line]
        else:
            # 여러 페이지
            parent_page_lines = pdf_pages[parent_page].split('\n')
            content_lines.extend(parent_page_lines[parent_line + 1:])
            
            for page_idx in range(parent_page + 1, child_page):
                if page_idx < len(pdf_pages):
                    content_lines.extend(pdf_pages[page_idx].split('\n'))
            
            if child_page < len(pdf_pages):
                child_page_lines = pdf_pages[child_page].split('\n')
                content_lines.extend(child_page_lines[:child_line])
        
        # 의미 있는 내용 라인 수 계산
        meaningful_lines = 0
        for line in content_lines:
            line = line.strip()
            # 빈 줄, 페이지 번호, 짧은 라인 제외
            if line and not re.match(r'^\d+$', line) and len(line) > 15:
                # 다른 섹션 헤딩이 아닌지 확인
                if not re.match(r'^(\d+(\.\d+)*|[A-Z]\.\d+(\.\d+)*)\s+', line):
                    meaningful_lines += 1
        
        result['content_lines'] = meaningful_lines
        result['has_content'] = meaningful_lines >= 2  # 2줄 이상의 의미 있는 내용
        
        return result
    
    def analyze_all_content_gaps_parallel(self) -> List[Dict]:
        """모든 레벨 간 내용 존재 여부를 병렬로 분석"""
        print("모든 부모-자식 쌍 생성 중...")
        
        # 모든 직접 부모-자식 쌍 찾기
        parent_child_pairs = []
        for parent in self.toc_items:
            for child in self.toc_items:
                if parent.is_direct_parent_of(child):
                    parent_child_pairs.append((parent, child, self.pdf_pages))
        
        print(f"분석할 부모-자식 쌍 수: {len(parent_child_pairs)}")
        
        if not parent_child_pairs:
            return []
        
        # 병렬 처리로 내용 존재 여부 확인
        results = []
        max_workers = min(cpu_count(), len(parent_child_pairs))
        
        print(f"병렬 처리 시작 (워커 수: {max_workers})")
        
        # 순차 처리로 변경 (PDF 객체 공유 문제 해결)
        for i, pair in enumerate(parent_child_pairs):
            if i % 10 == 0:
                print(f"진행률: {i}/{len(parent_child_pairs)} ({i/len(parent_child_pairs)*100:.1f}%)")
            
            result = self.check_content_between_sections_local(pair)
            results.append(result)
        
        return results
    
    def check_content_between_sections_local(self, args_tuple: Tuple) -> Dict:
        """로컬 버전의 내용 확인 (PDF 객체 공유 문제 해결)"""
        parent_item, child_item, pdf_pages = args_tuple
        
        result = {
            'parent': parent_item.number,
            'parent_title': parent_item.title,
            'child': child_item.number,
            'child_title': child_item.title,
            'has_content': False,
            'content_lines': 0,
            'found_parent': False,
            'found_child': False
        }
        
        # PDF에서 섹션 위치 찾기 (로컬 구현)
        parent_pos = self._find_section_local(parent_item.number, parent_item.title, pdf_pages)
        child_pos = self._find_section_local(child_item.number, child_item.title, pdf_pages)
        
        if parent_pos is None or child_pos is None:
            return result
            
        result['found_parent'] = True
        result['found_child'] = True
        
        parent_page, parent_line = parent_pos
        child_page, child_line = child_pos
        
        # 자식이 부모보다 앞에 있으면 안됨
        if child_page < parent_page or (child_page == parent_page and child_line <= parent_line):
            return result
        
        # 중간 내용 확인
        content_lines = []
        
        if parent_page == child_page:
            page_lines = pdf_pages[parent_page].split('\n')
            content_lines = page_lines[parent_line + 1:child_line]
        else:
            parent_page_lines = pdf_pages[parent_page].split('\n')
            content_lines.extend(parent_page_lines[parent_line + 1:])
            
            for page_idx in range(parent_page + 1, child_page):
                if page_idx < len(pdf_pages):
                    content_lines.extend(pdf_pages[page_idx].split('\n'))
            
            if child_page < len(pdf_pages):
                child_page_lines = pdf_pages[child_page].split('\n')
                content_lines.extend(child_page_lines[:child_line])
        
        # 의미 있는 내용 라인 수 계산
        meaningful_lines = 0
        for line in content_lines:
            line = line.strip()
            if line and not re.match(r'^\d+$', line) and len(line) > 15:
                if not re.match(r'^(\d+(\.\d+)*|[A-Z]\.\d+(\.\d+)*)\s+', line):
                    meaningful_lines += 1
        
        result['content_lines'] = meaningful_lines
        result['has_content'] = meaningful_lines >= 2
        
        return result
    
    def _find_section_local(self, section_number: str, title: str, pdf_pages: List[str]) -> Optional[Tuple[int, int]]:
        """로컬 섹션 찾기"""
        patterns = []
        
        if title:
            title_clean = re.escape(title.strip())
            patterns.extend([
                rf'{re.escape(section_number)}\s+{title_clean}',
                rf'Chapter\s+{re.escape(section_number)}\s*[:\-\s]*{title_clean}',
                rf'{re.escape(section_number)}\.?\s+{title_clean}',
                rf'Part\s+{re.escape(section_number)}\s*[—\-]\s*{title_clean}',
            ])
        
        if '.' not in section_number and section_number.isdigit():
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'Chapter\s+{re.escape(section_number)}[^\d]',
                rf'Part\s+{re.escape(section_number)}[^\d]',
            ])
        elif '.' in section_number:
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'{re.escape(section_number)}\.?\s+[A-Z]',
            ])
        elif re.match(r'^[A-Z]\.\d+', section_number):
            patterns.extend([
                rf'^{re.escape(section_number)}\s+[A-Z]',
                rf'{re.escape(section_number)}\.?\s+[A-Z]',
            ])
        
        for page_num, page_text in enumerate(pdf_pages):
            if not page_text:
                continue
                
            lines = page_text.split('\n')
            for line_idx, line in enumerate(lines):
                line = line.strip()
                
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        return (page_num, line_idx)
        
        return None
    
    def save_expected_introductions(self, results: List[Dict], output_file: str) -> None:
        """예상 Introduction 항목들을 JSON으로 저장"""
        # 내용이 있는 항목들만 필터링
        expected_introductions = []
        
        for result in results:
            if result['has_content'] and result['found_parent'] and result['found_child']:
                expected_introductions.append({
                    'parent_number': result['parent'],
                    'parent_title': result['parent_title'],
                    'child_number': result['child'],
                    'child_title': result['child_title'],
                    'intro_number': f"{result['parent']}.0",
                    'intro_title': "Introduction (사용자 추가)",
                    'content_lines': result['content_lines']
                })
        
        # 번호 순으로 정렬
        expected_introductions.sort(key=lambda x: (
            len(x['parent_number'].split('.')),
            x['parent_number']
        ))
        
        output_data = {
            'analysis_summary': {
                'total_pairs_analyzed': len(results),
                'pairs_with_content': len(expected_introductions),
                'expected_introduction_count': len(expected_introductions)
            },
            'expected_introductions': expected_introductions
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n예상 Introduction 항목 저장 완료: {output_file}")
        print(f"총 분석한 부모-자식 쌍: {len(results)}")
        print(f"내용이 있는 쌍: {len(expected_introductions)}")
        print(f"예상 Introduction 항목 수: {len(expected_introductions)}")
        
        print("\n예상 Introduction 항목들:")
        for intro in expected_introductions:
            print(f"  - {intro['intro_number']} {intro['intro_title']} "
                  f"(between {intro['parent_number']} and {intro['child_number']}, "
                  f"{intro['content_lines']} lines)")
    
    def analyze_complete(self, toc_file_path: str, pdf_file_path: str, output_file: str) -> None:
        """전체 분석 프로세스 실행"""
        print("=== TDD RED 단계: PDF 전체 내용 분석 ===")
        
        # 1. 포괄적 TOC 파싱
        self.parse_comprehensive_toc(toc_file_path)
        
        # 2. PDF 내용 추출
        self.extract_pdf_content(pdf_file_path)
        
        # 3. 병렬 내용 존재 여부 분석
        results = self.analyze_all_content_gaps_parallel()
        
        # 4. 예상 Introduction 항목들 저장
        self.save_expected_introductions(results, output_file)
        
        print("\n=== RED 단계 완료 ===")
        print(f"이제 이 결과를 '테스트 케이스'로 사용하여")
        print(f"toc_normalizer.py가 모든 항목을 올바르게 탐지하도록 개선합니다.")


def main():
    parser = argparse.ArgumentParser(description='Content Analyzer - TDD RED 단계')
    parser.add_argument('--toc', required=True, help='TOC 마크다운 파일 경로')
    parser.add_argument('--pdf', required=True, help='PDF 원본 파일 경로')
    parser.add_argument('--output', required=True, help='예상 결과 JSON 출력 파일 경로')
    
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
    
    # 분석 실행
    try:
        analyzer = ContentAnalyzer()
        analyzer.analyze_complete(args.toc, args.pdf, args.output)
        return 0
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())