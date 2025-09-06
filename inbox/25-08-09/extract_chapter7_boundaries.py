#!/usr/bin/env python3
"""
7장 리프 노드 텍스트 경계 추출기

이 스크립트는 7장의 리프 노드들에 대해 시작/종료 마커를 추출하여
나중에 정확한 섹션 추출이 가능하도록 합니다.

사용법:
    python extract_chapter7_boundaries.py
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


class Chapter7BoundaryExtractor:
    """7장 리프 노드 경계 추출기"""
    
    def __init__(self, marker_length: int = 80):
        """
        초기화
        
        Args:
            marker_length: 시작/종료 마커 텍스트 길이
        """
        self.marker_length = marker_length
        
    def load_files(self, leaf_nodes_path: str, chapter_text_path: str) -> Tuple[List[Dict], str]:
        """파일들을 로드합니다."""
        print("📂 파일 로드 중...")
        
        # 리프 노드 JSON 로드
        with open(leaf_nodes_path, 'r', encoding='utf-8') as f:
            leaf_nodes = json.load(f)
        
        # 7장 텍스트 로드
        with open(chapter_text_path, 'r', encoding='utf-8') as f:
            chapter_text = f.read()
        
        print(f"✅ 리프 노드: {len(leaf_nodes)}개")
        print(f"✅ 7장 텍스트: {len(chapter_text):,}자")
        
        return leaf_nodes, chapter_text
    
    def filter_chapter7_nodes(self, leaf_nodes: List[Dict]) -> List[Dict]:
        """7장 관련 노드만 필터링합니다."""
        print("\n🔍 7장 관련 노드 필터링...")
        
        chapter7_nodes = []
        
        for node in leaf_nodes:
            title = node.get('title', '')
            
            # 7장 관련 노드 조건
            is_chapter7 = (
                title.startswith('7 ') or 
                title.startswith('7.') or
                (title == 'Part 2 Introduction' and node.get('id') == 64) or
                (title == 'Summary' and node.get('id') == 72)
            )
            
            if is_chapter7:
                chapter7_nodes.append(node)
                print(f"  ✓ {title} (id: {node.get('id')})")
        
        print(f"\n📊 7장 관련 노드: {len(chapter7_nodes)}개")
        return chapter7_nodes
    
    def normalize_text(self, text: str) -> str:
        """텍스트 정규화 (공백, 개행 처리)"""
        # 연속된 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        # 앞뒤 공백 제거
        return text.strip()
    
    def find_section_boundaries(self, chapter_text: str, section_title: str) -> Tuple[int, int]:
        """섹션의 시작과 끝 위치를 찾습니다."""
        
        # 다양한 제목 패턴 시도
        title_patterns = [
            f"# {section_title}",
            f"## {section_title}",
            f"### {section_title}",
            section_title,
            # 페이지 구분 후 제목이 나오는 패턴
            rf"===.*?===\s*{re.escape(section_title)}",
        ]
        
        start_pos = -1
        for pattern in title_patterns:
            match = re.search(pattern, chapter_text, re.IGNORECASE | re.MULTILINE)
            if match:
                start_pos = match.start()
                break
        
        if start_pos == -1:
            # 단순 문자열 검색으로 폴백
            start_pos = chapter_text.find(section_title)
            if start_pos == -1:
                print(f"⚠️  섹션을 찾을 수 없습니다: {section_title}")
                return 0, len(chapter_text)
        
        # 다음 섹션의 시작점을 현재 섹션의 끝점으로 설정
        next_section_patterns = [
            r'\n# ',
            r'\n## ',
            r'\n### ',
            r'=== 페이지 \d+ ===.*?\n[#]',
            r'\n7\.',  # 7.1, 7.2 등
            r'\n8 ',   # 8장 시작
            r'\nSummary\n'
        ]
        
        end_pos = len(chapter_text)
        for pattern in next_section_patterns:
            match = re.search(pattern, chapter_text[start_pos + len(section_title):])
            if match:
                candidate_end = start_pos + len(section_title) + match.start()
                end_pos = min(end_pos, candidate_end)
        
        return start_pos, end_pos
    
    def extract_boundary_markers(self, chapter_text: str, start_pos: int, end_pos: int) -> Tuple[str, str]:
        """시작과 끝 마커를 추출합니다."""
        
        # 시작 마커 추출
        start_text = chapter_text[start_pos:start_pos + self.marker_length]
        start_marker = self.normalize_text(start_text)
        
        # 끝 마커 추출
        end_start = max(end_pos - self.marker_length, start_pos)
        end_text = chapter_text[end_start:end_pos]
        end_marker = self.normalize_text(end_text)
        
        return start_marker, end_marker
    
    def process_chapter7_nodes(self, chapter_text: str, chapter7_nodes: List[Dict]) -> List[Dict]:
        """7장 노드들을 처리합니다."""
        print("\n🔄 7장 노드 경계 추출 중...")
        
        processed_nodes = []
        
        for node in chapter7_nodes:
            title = node.get('title', '')
            node_id = node.get('id')
            
            print(f"\n  처리 중: {title} (id: {node_id})")
            
            # 섹션 경계 찾기
            start_pos, end_pos = self.find_section_boundaries(chapter_text, title)
            
            if start_pos >= 0 and end_pos > start_pos:
                # 경계 마커 추출
                start_marker, end_marker = self.extract_boundary_markers(
                    chapter_text, start_pos, end_pos
                )
                
                # 노드 업데이트
                updated_node = node.copy()
                updated_node['start_text'] = start_marker
                updated_node['end_text'] = end_marker
                updated_node['section_start_pos'] = start_pos
                updated_node['section_end_pos'] = end_pos
                updated_node['section_length'] = end_pos - start_pos
                
                print(f"    ✅ 위치: {start_pos:,} - {end_pos:,} ({end_pos - start_pos:,}자)")
                print(f"    ✅ 시작 마커: {len(start_marker)}자")
                print(f"    ✅ 종료 마커: {len(end_marker)}자")
                
                processed_nodes.append(updated_node)
                
            else:
                print(f"    ❌ 섹션 경계를 찾을 수 없습니다")
                # 원본 노드 그대로 추가
                processed_nodes.append(node)
        
        return processed_nodes
    
    def validate_boundaries(self, chapter_text: str, processed_nodes: List[Dict]) -> bool:
        """추출된 경계의 정확성을 검증합니다."""
        print("\n🔍 경계 마커 검증 중...")
        
        validation_passed = True
        
        for node in processed_nodes:
            title = node.get('title', '')
            start_text = node.get('start_text', '')
            end_text = node.get('end_text', '')
            
            if not start_text or not end_text:
                continue
                
            # 시작 마커가 텍스트에서 찾아지는지 확인
            start_found = chapter_text.find(start_text) >= 0
            end_found = chapter_text.find(end_text) >= 0
            
            print(f"  {title}:")
            print(f"    시작 마커: {'✅' if start_found else '❌'}")
            print(f"    종료 마커: {'✅' if end_found else '❌'}")
            
            if not start_found or not end_found:
                validation_passed = False
        
        return validation_passed
    
    def save_results(self, processed_nodes: List[Dict], output_path: str):
        """결과를 JSON 파일로 저장합니다."""
        print(f"\n💾 결과 저장 중: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_nodes, f, ensure_ascii=False, indent=2)
        
        print("✅ 저장 완료!")
    
    def print_summary(self, processed_nodes: List[Dict]):
        """처리 결과 요약을 출력합니다."""
        print("\n📊 처리 결과 요약:")
        print("=" * 50)
        
        total_nodes = len(processed_nodes)
        nodes_with_boundaries = len([n for n in processed_nodes if n.get('start_text')])
        
        print(f"전체 노드 수: {total_nodes}")
        print(f"경계 추출 완료: {nodes_with_boundaries}")
        print(f"성공률: {nodes_with_boundaries/total_nodes*100:.1f}%")
        
        print("\n📋 처리된 노드들:")
        for node in processed_nodes:
            title = node.get('title', '')
            has_boundaries = bool(node.get('start_text'))
            status = "✅" if has_boundaries else "❌"
            section_length = node.get('section_length', 0)
            
            print(f"  {status} {title} ({section_length:,}자)")


def main():
    """메인 실행 함수"""
    print("🚀 7장 리프 노드 경계 추출기 시작")
    print("=" * 50)
    
    # 파일 경로
    leaf_nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part2_scalability_leaf_nodes.json"
    chapter_text_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_with_boundaries.json"
    
    # 추출기 초기화
    extractor = Chapter7BoundaryExtractor(marker_length=80)
    
    try:
        # 1. 파일 로드
        leaf_nodes, chapter_text = extractor.load_files(leaf_nodes_path, chapter_text_path)
        
        # 2. 7장 관련 노드 필터링
        chapter7_nodes = extractor.filter_chapter7_nodes(leaf_nodes)
        
        # 3. 경계 마커 추출
        processed_nodes = extractor.process_chapter7_nodes(chapter_text, chapter7_nodes)
        
        # 4. 검증
        validation_passed = extractor.validate_boundaries(chapter_text, processed_nodes)
        
        # 5. 결과 저장
        extractor.save_results(processed_nodes, output_path)
        
        # 6. 요약 출력
        extractor.print_summary(processed_nodes)
        
        if validation_passed:
            print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
        else:
            print("\n⚠️  일부 경계 마커에 문제가 있습니다. 결과를 확인해주세요.")
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)