#!/usr/bin/env python3
"""
생성 시간: 2025-08-08 09:15 KST
핵심 내용: TOC 구조에 Introduction 갭 노드를 삽입하여 새로운 구조화된 JSON 생성
상세 내용:
    - TocGapNodeInserter 클래스 (1-200행): TOC 노드 분석 및 갭 노드 삽입 기능
    - extract_numbering() (30-50행): 타이틀에서 넘버링 체계 추출 알고리즘
    - create_introduction_node() (60-80행): Introduction 노드 생성 로직
    - detect_and_insert_gaps() (100-150행): 갭 탐지 및 노드 삽입 메인 로직
    - main() (180-200행): 메인 실행 함수
상태: 
주소: toc_gap_node_inserter
참조: gap_section_extractor.py
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class TocNode:
    """TOC 노드 정보를 저장하는 데이터클래스"""
    title: str
    level: int
    start_page: int
    end_page: int
    page_count: int
    is_added_node: bool = False

class TocGapNodeInserter:
    """TOC 구조에서 레벨 갭을 탐지하고 Introduction 노드를 삽입하는 클래스"""
    
    def __init__(self, json_path: str, output_path: str):
        self.json_path = Path(json_path)
        self.output_path = Path(output_path)
        self.original_nodes = []
        self.enhanced_nodes = []
        
        # 원본 JSON 데이터 로드
        self._load_original_data()
    
    def _load_original_data(self) -> None:
        """원본 JSON 파일에서 TOC 노드 데이터를 로드"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            
            for node_data in nodes_data:
                node = TocNode(
                    title=node_data.get('title', ''),
                    level=node_data.get('level', 0),
                    start_page=node_data.get('start_page', 0),
                    end_page=node_data.get('end_page', 0),
                    page_count=node_data.get('page_count', 0),
                    is_added_node=False  # 원본 노드는 모두 False
                )
                self.original_nodes.append(node)
            
            print(f"✅ 원본 TOC 데이터 로드 완료: {len(self.original_nodes)}개 노드")
            
        except Exception as e:
            raise Exception(f"원본 JSON 파일 로드 실패: {e}")
    
    def extract_numbering(self, title: str) -> Optional[str]:
        """타이틀에서 넘버링 체계를 추출 (일반적인 숫자/문자 넘버링만)"""
        # 패턴: 숫자로 시작하거나 대문자로 시작하는 넘버링
        patterns = [
            r'^(\d+(?:\.\d+)*)',          # 1, 1.1, 1.1.1 형태
            r'^([A-Z](?:\.\d+)*)',        # A, A.1, A.1.1 형태
        ]
        
        for pattern in patterns:
            match = re.match(pattern, title.strip())
            if match:
                return match.group(1)
        
        return None
    
    def create_introduction_node(self, current_node: TocNode, next_node: TocNode) -> Optional[TocNode]:
        """현재 노드의 조직화 체계를 기반으로 Introduction 노드 생성"""
        current_title = current_node.title
        
        # 현재 노드의 조직화 체계를 추출
        if current_title.startswith("Part"):
            # "Part 1—Flexibility" → "Part 1 Introduction"
            part_match = re.match(r'^(Part\s+\d+)', current_title)
            if part_match:
                intro_title = f"{part_match.group(1)} Introduction"
            else:
                return None
        elif current_title.startswith("Appendix"):
            # "Appendix A—Principles..." → "Appendix A Introduction"
            appendix_match = re.match(r'^(Appendix\s+[A-Z])', current_title)
            if appendix_match:
                intro_title = f"{appendix_match.group(1)} Introduction"
            else:
                return None
        else:
            # 일반적인 넘버링 체계 추출
            current_numbering = self.extract_numbering(current_title)
            if not current_numbering:
                return None
            intro_title = f"{current_numbering} Introduction"
        
        # 페이지 범위 계산
        if current_node.end_page > next_node.start_page:
            # 상위 범주 케이스 (Part → Chapter)
            gap_start = current_node.start_page
            gap_end = next_node.start_page
        else:
            # 일반 케이스 (Chapter → Section)
            gap_start = current_node.end_page
            gap_end = next_node.start_page
        
        # 페이지 범위는 관대하게 처리 (타이틀 기반 필터링에 의존)
        # 레벨 차이가 있으면 무조건 Introduction 노드 생성
        if gap_start <= 0:
            gap_start = 1  # 최소 1페이지로 설정
        
        if gap_end <= gap_start:
            gap_end = gap_start + 1  # 최소 1페이지 범위 보장
        
        gap_page_count = gap_end - gap_start + 1
        
        intro_node = TocNode(
            title=intro_title,
            level=next_node.level,  # 다음 노드와 같은 레벨
            start_page=gap_start,
            end_page=gap_end,
            page_count=gap_page_count,
            is_added_node=True
        )
        
        return intro_node
    
    def detect_and_insert_gaps(self) -> List[TocNode]:
        """레벨 갭을 탐지하고 Introduction 노드를 삽입하여 새로운 TOC 구조 생성"""
        print("🔍 레벨 갭 탐지 및 Introduction 노드 삽입 중...")
        
        enhanced_nodes = []
        inserted_count = 0
        
        for i in range(len(self.original_nodes)):
            current_node = self.original_nodes[i]
            
            # 현재 노드를 결과에 추가
            enhanced_nodes.append(current_node)
            
            # 다음 노드가 있는지 확인
            if i + 1 < len(self.original_nodes):
                next_node = self.original_nodes[i + 1]
                
                # 레벨 갭이 있는지 확인 (current_level < next_level)
                if current_node.level < next_node.level:
                    # Introduction 노드 생성
                    intro_node = self.create_introduction_node(current_node, next_node)
                    
                    if intro_node:
                        enhanced_nodes.append(intro_node)
                        inserted_count += 1
                        
                        print(f"  📄 Introduction 노드 삽입:")
                        print(f"     이전: {current_node.title} (Level {current_node.level})")
                        print(f"     삽입: {intro_node.title} (Level {intro_node.level})")
                        print(f"     다음: {next_node.title} (Level {next_node.level})")
                        print(f"     페이지: {intro_node.start_page}-{intro_node.end_page}")
        
        self.enhanced_nodes = enhanced_nodes
        print(f"✅ 총 {inserted_count}개 Introduction 노드 삽입 완료")
        print(f"📊 전체 노드 수: {len(self.original_nodes)} → {len(self.enhanced_nodes)}")
        
        return enhanced_nodes
    
    def save_enhanced_toc(self) -> None:
        """향상된 TOC 구조를 JSON 파일로 저장"""
        if not self.enhanced_nodes:
            print("⚠️ 저장할 향상된 TOC 데이터가 없습니다.")
            return
        
        try:
            # JSON 형태로 변환
            json_data = []
            for node in self.enhanced_nodes:
                node_dict = {
                    "title": node.title,
                    "level": node.level,
                    "start_page": node.start_page,
                    "end_page": node.end_page,
                    "page_count": node.page_count,
                    "is_added_node": node.is_added_node
                }
                
                json_data.append(node_dict)
            
            # 파일 저장
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 향상된 TOC 파일 저장 완료: {self.output_path}")
            
            # 통계 정보 출력
            self._print_statistics()
            
            # 추가된 노드만 따로 저장
            self._save_added_nodes_only()
            
        except Exception as e:
            print(f"❌ TOC 파일 저장 실패: {e}")
    
    def _save_added_nodes_only(self) -> None:
        """추가된 노드만 따로 JSON 파일로 저장"""
        try:
            # 추가된 노드만 필터링
            added_nodes = [node for node in self.enhanced_nodes if node.is_added_node]
            
            if not added_nodes:
                print("⚠️ 추가된 노드가 없습니다.")
                return
            
            # JSON 형태로 변환
            json_data = []
            for node in added_nodes:
                node_dict = {
                    "title": node.title,
                    "level": node.level,
                    "start_page": node.start_page,
                    "end_page": node.end_page,
                    "page_count": node.page_count,
                    "is_added_node": node.is_added_node
                }
                json_data.append(node_dict)
            
            # 추가된 노드만 저장하는 파일 경로
            added_nodes_path = self.output_path.parent / f"{self.output_path.stem}_added_nodes_only.json"
            
            # 파일 저장
            with open(added_nodes_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"📋 추가된 노드만 저장: {added_nodes_path} ({len(added_nodes)}개)")
            
        except Exception as e:
            print(f"❌ 추가된 노드 파일 저장 실패: {e}")
    
    def _print_statistics(self) -> None:
        """삽입 결과 통계 출력"""
        original_count = len(self.original_nodes)
        enhanced_count = len(self.enhanced_nodes)
        introduction_count = enhanced_count - original_count
        
        print(f"\n📊 TOC 구조 향상 통계:")
        print(f"   원본 노드 수: {original_count}")
        print(f"   향상된 노드 수: {enhanced_count}")
        print(f"   삽입된 Introduction 노드: {introduction_count}")
        
        # 레벨별 통계
        level_stats = {}
        intro_level_stats = {}
        
        for node in self.enhanced_nodes:
            level_key = f"Level {node.level}"
            level_stats[level_key] = level_stats.get(level_key, 0) + 1
            
            if node.is_added_node:
                intro_level_stats[level_key] = intro_level_stats.get(level_key, 0) + 1
        
        print(f"\n📈 레벨별 노드 분포:")
        for level, count in sorted(level_stats.items()):
            intro_count = intro_level_stats.get(level, 0)
            print(f"   {level}: {count}개 (Introduction: {intro_count}개)")

def main():
    """메인 실행 함수"""
    # 파일 경로 설정
    input_json = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/core_toc_with_page_ranges.json"
    output_json = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/core_toc_with_page_ranges_v2.json"
    
    # 입력 파일 존재 확인
    if not Path(input_json).exists():
        print(f"❌ 입력 JSON 파일을 찾을 수 없습니다: {input_json}")
        return
    
    print("🚀 TOC 구조 향상 작업 시작")
    print(f"📊 입력 파일: {input_json}")
    print(f"💾 출력 파일: {output_json}")
    
    try:
        # TOC 갭 노드 삽입기 생성
        inserter = TocGapNodeInserter(input_json, output_json)
        
        # 갭 탐지 및 Introduction 노드 삽입
        enhanced_nodes = inserter.detect_and_insert_gaps()
        
        if enhanced_nodes:
            # 향상된 TOC 구조 저장
            inserter.save_enhanced_toc()
            print("\n✅ TOC 구조 향상 작업 완료!")
        else:
            print("⚠️ 삽입할 Introduction 노드가 없습니다.")
        
    except Exception as e:
        print(f"\n❌ TOC 구조 향상 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()