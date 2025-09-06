#!/usr/bin/env python3
"""
생성 시간: 2025-08-08 08:29 KST
핵심 내용: 노드 레벨 차이를 기반으로 PDF에서 섹션 간 gap 콘텐츠를 추출하는 스크립트
상세 내용:
    - GapSectionExtractor 클래스 (1-250행): 메인 추출 클래스, JSON 분석 및 PDF 처리 기능
    - detect_level_gaps() (60-90행): 노드 간 레벨 차이 탐지 알고리즘
    - extract_gap_content() (120-150행): PDF에서 특정 페이지 범위 텍스트 추출
    - save_gap_section() (180-200행): 추출된 데이터를 마크다운으로 저장
    - main() (220-250행): 메인 실행 함수, CLI 인터페이스 제공
상태: 
주소: gap_section_extractor
참조: 
"""

import json
import pdfplumber
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class NodeGap:
    """노드 간 gap 정보를 저장하는 데이터클래스"""
    current_node: Dict
    next_node: Dict
    gap_start_page: int
    gap_end_page: int
    gap_description: str

class GapSectionExtractor:
    """노드 레벨 차이를 기반으로 PDF에서 gap 섹션을 추출하는 클래스"""
    
    def __init__(self, json_path: str, pdf_path: str, output_dir: str):
        self.json_path = Path(json_path)
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.nodes = []
        self.gaps = []
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(exist_ok=True)
        
        # JSON 데이터 로드
        self._load_json_data()
    
    def _load_json_data(self) -> None:
        """JSON 파일에서 노드 데이터를 로드"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.nodes = json.load(f)
            print(f"✅ JSON 데이터 로드 완료: {len(self.nodes)}개 노드")
        except Exception as e:
            raise Exception(f"JSON 파일 로드 실패: {e}")
    
    def detect_level_gaps(self) -> List[NodeGap]:
        """노드 간 레벨 차이가 있는 gap을 탐지"""
        print("🔍 노드 레벨 gap 탐지 중...")
        gaps = []
        
        for i in range(len(self.nodes) - 1):
            current_node = self.nodes[i]
            next_node = self.nodes[i + 1]
            
            current_level = current_node.get('level', 0)
            next_level = next_node.get('level', 0)
            
            # 현재 노드의 레벨이 다음 노드보다 작은 경우 (고차원 → 저차원으로 변화)
            if current_level < next_level:
                # gap 페이지 범위 계산
                current_end_page = current_node.get('end_page', 0)
                next_start_page = next_node.get('start_page', 0)
                
                # 페이지 범위 계산 - 모든 레벨 변화 허용
                gap_start = current_end_page
                gap_end = next_start_page
                
                # 페이지 범위가 유효한지 확인
                if gap_start > 0:
                    gap_description = f"Level {current_level} → Level {next_level}"
                    
                    gap = NodeGap(
                        current_node=current_node,
                        next_node=next_node,
                        gap_start_page=gap_start,
                        gap_end_page=gap_end,
                        gap_description=gap_description
                    )
                    gaps.append(gap)
                    
                    print(f"  📄 Gap 발견: {current_node['title']} → {next_node['title']}")
                    print(f"     레벨: {current_level} → {next_level}, 페이지: {gap_start}-{gap_end}")
        
        self.gaps = gaps
        print(f"✅ 총 {len(gaps)}개 gap 발견")
        return gaps
    
    def _normalize_title_for_search(self, title: str) -> str:
        """타이틀을 검색용으로 정규화"""
        # 특수문자, 숫자, 공백 등을 제거하여 핵심 키워드만 추출
        normalized = re.sub(r'[^\w\s]', ' ', title)  # 특수문자를 공백으로
        normalized = re.sub(r'\s+', ' ', normalized).strip()  # 다중 공백을 단일 공백으로
        return normalized.lower()
    
    def _extract_content_between_titles(self, page_text: str, current_title: str, next_title: str) -> str:
        """페이지에서 두 타이틀 사이의 콘텐츠만 추출"""
        lines = page_text.split('\n')
        
        # 타이틀 정규화
        current_normalized = self._normalize_title_for_search(current_title)
        next_normalized = self._normalize_title_for_search(next_title)
        
        start_idx = -1
        end_idx = len(lines)
        
        # 현재 타이틀 이후 시작점 찾기
        for i, line in enumerate(lines):
            line_normalized = self._normalize_title_for_search(line)
            if current_normalized in line_normalized or line_normalized in current_normalized:
                start_idx = i + 1  # 타이틀 다음 줄부터
                break
        
        # 다음 타이틀 이전 끝점 찾기
        for i, line in enumerate(lines[start_idx:], start_idx):
            line_normalized = self._normalize_title_for_search(line)
            if next_normalized in line_normalized or line_normalized in next_normalized:
                end_idx = i
                break
        
        # 추출된 콘텐츠 반환
        if start_idx >= 0 and start_idx < end_idx:
            extracted_lines = lines[start_idx:end_idx]
            return '\n'.join(extracted_lines).strip()
        
        return ""
    
    def extract_gap_content(self, gap: NodeGap) -> str:
        """특정 gap의 페이지 범위에서 두 타이틀 사이의 PDF 콘텐츠만 추출"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                total_pages = len(pdf.pages)
                
                # 페이지 범위 유효성 검사
                start_page = max(1, gap.gap_start_page) - 1  # 0-based 인덱스로 변환
                end_page = min(total_pages, gap.gap_end_page) - 1
                
                current_title = gap.current_node.get('title', '')
                next_title = gap.next_node.get('title', '')
                
                content = ""
                for page_num in range(start_page, end_page + 1):
                    if page_num >= total_pages:
                        break
                    
                    page = pdf.pages[page_num]
                    page_text = page.extract_text() or ""
                    
                    if page_text.strip():
                        # 타이틀 기반으로 정확한 내용만 추출
                        extracted_text = self._extract_content_between_titles(
                            page_text, current_title, next_title
                        )
                        
                        if extracted_text:
                            content += f"=== PAGE {page_num + 1} ===\n{extracted_text}\n\n"
                        else:
                            # 타이틀 매칭이 실패하면 전체 페이지 포함 (fallback)
                            content += f"=== PAGE {page_num + 1} ===\n{page_text}\n\n"
                
                return content.strip()
                
        except Exception as e:
            print(f"❌ 콘텐츠 추출 실패: {e}")
            return ""
    
    def save_gap_section(self, gap: NodeGap, content: str) -> None:
        """추출된 gap 콘텐츠를 파일로 저장"""
        if not content.strip():
            print(f"⚠️ 빈 콘텐츠, 저장 건너뛰기: {gap.gap_description}")
            return
        
        # 파일명 생성
        current_level = gap.current_node.get('level', 0)
        next_level = gap.next_node.get('level', 0)
        filename = f"gap_{current_level}_to_{next_level}_p{gap.gap_start_page}-{gap.gap_end_page}.md"
        
        # 파일 저장
        filepath = self.output_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 저장 완료: {filename} ({len(content)} 문자)")
            
        except Exception as e:
            print(f"❌ 파일 저장 실패 {filename}: {e}")
    
    def extract_all_gaps(self) -> None:
        """모든 gap의 콘텐츠를 추출하고 저장"""
        if not self.gaps:
            print("⚠️ 탐지된 gap이 없습니다.")
            return
        
        print(f"🚀 {len(self.gaps)}개 gap 콘텐츠 추출 시작...")
        
        extracted_count = 0
        failed_count = 0
        
        for i, gap in enumerate(self.gaps, 1):
            print(f"\n[{i}/{len(self.gaps)}] {gap.gap_description}")
            print(f"  페이지 {gap.gap_start_page}-{gap.gap_end_page} 추출 중...")
            
            content = self.extract_gap_content(gap)
            
            if content.strip():
                self.save_gap_section(gap, content)
                extracted_count += 1
            else:
                print(f"❌ 빈 콘텐츠")
                failed_count += 1
        
        print(f"\n📊 추출 완료: ✅ {extracted_count}개 성공, ❌ {failed_count}개 실패")
        self._create_summary_report(extracted_count, failed_count)
    
    def create_gap_list_only(self) -> None:
        """Gap 목록만 생성하여 검증용 파일로 저장 (PDF 추출 없음)"""
        if not self.gaps:
            print("⚠️ 탐지된 gap이 없습니다.")
            return
        
        print(f"📋 {len(self.gaps)}개 gap 목록 생성 중...")
        
        # 검증용 gap 목록 파일 생성
        gap_list_file = self.output_dir / "gap_list_only.md"
        
        try:
            with open(gap_list_file, 'w', encoding='utf-8') as f:
                f.write("# Gap Detection List\n\n")
                f.write(f"**총 탐지된 Gap 수:** {len(self.gaps)}\n\n")
                f.write("## 탐지된 Gap 목록\n\n")
                
                for i, gap in enumerate(self.gaps, 1):
                    f.write(f"### {i}. **Level {gap.current_node.get('level', 0)} → Level {gap.next_node.get('level', 0)}**\n")
                    f.write(f"- **이전 노드**: {gap.current_node.get('title', '')}\n")
                    f.write(f"  - 페이지 범위: {gap.current_node.get('start_page', 0)}-{gap.current_node.get('end_page', 0)}\n")
                    f.write(f"- **다음 노드**: {gap.next_node.get('title', '')}\n")
                    f.write(f"  - 페이지 범위: {gap.next_node.get('start_page', 0)}-{gap.next_node.get('end_page', 0)}\n")
                    f.write(f"- **Gap 페이지**: {gap.gap_start_page}-{gap.gap_end_page}\n")
                    f.write(f"- **Gap 설명**: {gap.gap_description}\n\n")
                
                # 레벨별 통계
                f.write("## 레벨별 Gap 통계\n\n")
                level_stats = {}
                for gap in self.gaps:
                    level_key = f"Level {gap.current_node.get('level', 0)} → Level {gap.next_node.get('level', 0)}"
                    level_stats[level_key] = level_stats.get(level_key, 0) + 1
                
                for level_transition, count in sorted(level_stats.items()):
                    f.write(f"- **{level_transition}**: {count}개\n")
            
            print(f"📄 Gap 목록 파일 생성: {gap_list_file}")
            
        except Exception as e:
            print(f"❌ Gap 목록 파일 생성 실패: {e}")
    
    def _create_summary_report(self, extracted: int, failed: int) -> None:
        """추출 결과 요약 보고서 생성"""
        report_file = self.output_dir / "gap_extraction_report.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Gap Section Extraction Report\n\n")
                f.write(f"**총 Gap 수:** {len(self.gaps)}\n")
                f.write(f"**추출 성공:** {extracted}\n")
                f.write(f"**추출 실패:** {failed}\n\n")
                
                f.write("## Gap 상세 정보\n\n")
                for gap in self.gaps:
                    f.write(f"- **{gap.gap_description}**\n")
                    f.write(f"  - 이전: {gap.current_node['title']}\n")
                    f.write(f"  - 다음: {gap.next_node['title']}\n")
                    f.write(f"  - 페이지: {gap.gap_start_page}-{gap.gap_end_page}\n\n")
            
            print(f"📄 요약 보고서 생성: {report_file}")
            
        except Exception as e:
            print(f"❌ 보고서 생성 실패: {e}")

def main():
    """메인 실행 함수"""
    # 기본 경로 설정
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges.json"
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/extracted_gaps"
    
    # 파일 존재 확인
    if not Path(json_path).exists():
        print(f"❌ JSON 파일을 찾을 수 없습니다: {json_path}")
        return
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print("🚀 노드 레벨 gap 섹션 추출 시작")
    print(f"📊 JSON: {json_path}")
    print(f"📖 PDF: {pdf_path}")
    print(f"📁 출력: {output_dir}")
    
    try:
        # Gap 추출기 생성
        extractor = GapSectionExtractor(json_path, pdf_path, output_dir)
        
        # Gap 탐지
        gaps = extractor.detect_level_gaps()
        
        if gaps:
            # Gap 목록만 생성 (검증용)
            extractor.create_gap_list_only()
            print("\n✅ Gap 목록 생성 완료!")
        else:
            print("⚠️ 탐지할 gap이 없습니다.")
        
    except Exception as e:
        print(f"\n❌ 추출 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()