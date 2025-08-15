#!/usr/bin/env python3
"""
# claude_boundary_finder_v2.py

## 생성 시간: 2025-08-10 16:05:10 KST

## 핵심 내용: 7.2 JSON Schema 섹션의 정확한 시작/종료 문자열 추출 (폴백 포함)

## 상세 내용:
- BoundaryFinderV2 (라인 27-158): 경계 문자열 추출 메인 클래스 (Claude SDK + 폴백)
- load_files (라인 36-66): 원문과 리프노드 파일 로드
- find_section_boundaries (라인 68-118): 텍스트 분석으로 섹션 경계 찾기
- extract_unique_boundaries (라인 120-158): 고유한 시작/종료 문자열 추출
- main (라인 161-198): 메인 실행 함수

## 상태: 활성

## 주소: claude_boundary_finder_v2

## 참조: claude_boundary_finder
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class BoundaryFinderV2:
    """텍스트 분석 기반 리프노드 경계 추출기"""
    
    def __init__(self):
        """초기화"""
        self.debug = True
    
    def load_files(self, source_path: str, nodes_path: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        원문과 리프노드 파일을 로드합니다.
        
        Args:
            source_path: 원문 파일 경로
            nodes_path: 리프노드 파일 경로
            
        Returns:
            tuple: (원문 텍스트, 리프노드 리스트)
        """
        # 원문 로드
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                source_text = f.read()
            print(f"✓ 원문 로드 완료: {len(source_text):,}자")
        except Exception as e:
            print(f"❌ 원문 로드 실패: {e}")
            return "", []
        
        # 리프노드 로드
        try:
            with open(nodes_path, 'r', encoding='utf-8') as f:
                leaf_nodes = json.load(f)
            print(f"✓ 리프노드 로드 완료: {len(leaf_nodes)}개")
        except Exception as e:
            print(f"❌ 리프노드 로드 실패: {e}")
            return source_text, []
        
        return source_text, leaf_nodes
    
    def find_section_boundaries(self, source_text: str, target_title: str, next_title: Optional[str] = None) -> Tuple[int, int]:
        """
        텍스트 분석으로 섹션의 시작과 끝 위치를 찾습니다.
        
        Args:
            source_text: 전체 원문 텍스트
            target_title: 타겟 섹션 제목
            next_title: 다음 섹션 제목
            
        Returns:
            tuple: (시작 위치, 종료 위치)
        """
        # 1. 타겟 섹션 시작 위치 찾기
        # "7.2 JSON Schema in a nutshell" 단독으로 나타나는 위치 찾기
        lines = source_text.split('\n')
        start_line = -1
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            # 섹션 제목이 단독으로 나타나는 라인 찾기
            if stripped_line == target_title:
                start_line = i
                print(f"✓ 섹션 시작 라인 발견: {i+1} - '{stripped_line}'")
                break
        
        if start_line == -1:
            print(f"❌ 섹션 시작을 찾을 수 없습니다: {target_title}")
            return -1, -1
        
        # 2. 다음 섹션 시작 위치 찾기 (종료점)
        end_line = len(lines)  # 기본값: 문서 끝
        
        if next_title:
            for i in range(start_line + 1, len(lines)):
                stripped_line = lines[i].strip()
                if stripped_line == next_title:
                    end_line = i
                    print(f"✓ 다음 섹션 발견: {i+1} - '{stripped_line}'")
                    break
        
        # 3. 문자 위치로 변환
        start_pos = sum(len(lines[i]) + 1 for i in range(start_line))  # +1 for newline
        end_pos = sum(len(lines[i]) + 1 for i in range(end_line)) - 1  # -1 to exclude next section
        
        print(f"✓ 섹션 범위: 라인 {start_line+1} ~ {end_line} (문자 위치 {start_pos} ~ {end_pos})")
        
        return start_pos, end_pos
    
    def extract_unique_boundaries(self, source_text: str, start_pos: int, end_pos: int) -> Tuple[Optional[str], Optional[str]]:
        """
        섹션에서 고유한 시작/종료 문자열을 추출합니다.
        
        Args:
            source_text: 전체 원문 텍스트
            start_pos: 섹션 시작 위치
            end_pos: 섹션 종료 위치
            
        Returns:
            tuple: (시작 경계 문자열, 종료 경계 문자열)
        """
        section_text = source_text[start_pos:end_pos]
        
        # 시작 경계: 섹션 제목 + 첫 번째 문장
        start_lines = section_text.split('\n')[:3]  # 처음 3줄
        start_boundary = '\n'.join([line for line in start_lines if line.strip()])[:60]
        
        # 종료 경계: 섹션의 마지막 의미 있는 내용
        end_lines = section_text.strip().split('\n')
        meaningful_end_lines = []
        
        # 뒤에서부터 의미 있는 라인 수집 (빈 라인, 페이지 마커 제외)
        for line in reversed(end_lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('===') and not stripped.isdigit():
                meaningful_end_lines.append(line)
                if len(meaningful_end_lines) >= 2:
                    break
        
        if meaningful_end_lines:
            end_boundary = '\n'.join(reversed(meaningful_end_lines))[-60:]
        else:
            end_boundary = section_text.strip()[-60:]
        
        print(f"✓ 시작 경계 (길이 {len(start_boundary)}): '{start_boundary[:40]}...'")
        print(f"✓ 종료 경계 (길이 {len(end_boundary)}): '...{end_boundary[-40:]}'")
        
        return start_boundary.strip(), end_boundary.strip()


def main():
    """메인 실행 함수"""
    print("🚀 7.2 JSON Schema 섹션 경계 추출기 시작")
    print("=" * 50)
    
    # 파일 경로
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    target_title = "7.2 JSON Schema in a nutshell"
    next_title = "7.3 Schema flexibility and strictness"
    
    try:
        # 경계 추출기 생성
        finder = BoundaryFinderV2()
        
        # 파일 로드
        source_text, leaf_nodes = finder.load_files(source_path, nodes_path)
        if not source_text or not leaf_nodes:
            return 1
        
        # 섹션 경계 찾기
        print(f"\n🔍 '{target_title}' 섹션 경계 분석 중...")
        start_pos, end_pos = finder.find_section_boundaries(source_text, target_title, next_title)
        
        if start_pos == -1 or end_pos == -1:
            return 1
        
        # 고유한 경계 문자열 추출
        print(f"\n📝 고유 경계 문자열 추출 중...")
        start_boundary, end_boundary = finder.extract_unique_boundaries(source_text, start_pos, end_pos)
        
        # 결과 출력
        print(f"\n🎉 경계 추출 완료!")
        print(f"📏 추출될 섹션 길이: {end_pos - start_pos:,}자")
        print(f"\n📍 시작 경계:")
        print(f"'{start_boundary}'")
        print(f"\n📍 종료 경계:")
        print(f"'{end_boundary}'")
        
        # 검증
        if start_boundary in source_text and end_boundary in source_text:
            print(f"\n✅ 경계 검증 완료!")
        else:
            print(f"\n⚠️ 경계 검증 실패 - 원문에서 찾을 수 없습니다")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())