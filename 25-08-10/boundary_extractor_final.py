#!/usr/bin/env python3
"""
# boundary_extractor_final.py

## 생성 시간: 2025-08-10 16:35:10 KST

## 핵심 내용: 최종 동적 리프노드 경계 추출기 (Claude SDK + 텍스트 분석)

## 상세 내용:
- FinalBoundaryExtractor (라인 26-175): 하이브리드 경계 추출 메인 클래스
- load_files (라인 35-65): 원문과 리프노드 파일 로드
- extract_boundaries_hybrid (라인 67-142): Claude SDK + 텍스트 분석 하이브리드 방식
- find_precise_boundaries (라인 144-175): 정확한 텍스트 경계 추출
- main (라인 178-218): 메인 실행 함수

## 상태: 활성

## 주소: boundary_extractor_final

## 참조: dynamic_boundary_extractor
"""

import json
import asyncio
import re
from typing import Dict, List, Any, Optional, Tuple


class FinalBoundaryExtractor:
    """Claude SDK + 텍스트 분석을 결합한 최종 경계 추출기"""
    
    def __init__(self, debug: bool = True):
        """
        초기화
        
        Args:
            debug: 디버그 모드 활성화
        """
        self.debug = debug
    
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
    
    async def extract_boundaries_hybrid(self, source_text: str, target_node: Dict[str, Any], next_node: Optional[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        """
        하이브리드 방식으로 경계를 추출합니다 (텍스트 분석 우선, Claude SDK 보조).
        
        Args:
            source_text: 전체 원문 텍스트
            target_node: 타겟 노드
            next_node: 다음 노드 (종료점 판단용)
            
        Returns:
            tuple: (시작 경계 문자열, 종료 경계 문자열)
        """
        target_title = target_node.get('title', '')
        next_title = next_node.get('title', '') if next_node else None
        
        print(f"🔍 '{target_title}' 섹션 경계 분석 중...")
        if next_title:
            print(f"   다음 섹션: '{next_title}'")
        
        # 1단계: 텍스트 분석으로 섹션 위치 찾기
        lines = source_text.split('\n')
        
        # 타겟 섹션 시작 라인 찾기
        start_line = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == target_title:
                start_line = i
                print(f"   📍 시작 라인 발견: {i+1}")
                break
        
        if start_line == -1:
            print(f"   ❌ 시작 라인을 찾을 수 없습니다")
            return None, None
        
        # 다음 섹션 시작 라인 찾기 (종료점)
        end_line = len(lines)
        if next_title:
            for i in range(start_line + 1, len(lines)):
                stripped = lines[i].strip()
                if stripped == next_title:
                    end_line = i
                    print(f"   📍 종료 라인 발견: {i+1}")
                    break
        
        # 2단계: 정확한 경계 문자열 추출
        return self.find_precise_boundaries(source_text, lines, start_line, end_line)
    
    def find_precise_boundaries(self, source_text: str, lines: List[str], start_line: int, end_line: int) -> Tuple[str, str]:
        """
        정확한 경계 문자열을 추출합니다.
        
        Args:
            source_text: 전체 원문
            lines: 라인별로 분리된 텍스트
            start_line: 시작 라인 번호
            end_line: 종료 라인 번호
            
        Returns:
            tuple: (시작 경계 문자열, 종료 경계 문자열)
        """
        # 시작 경계: 섹션 제목 + 다음 2-3줄의 의미있는 내용
        start_boundary_lines = [lines[start_line]]  # 섹션 제목
        
        # 다음 의미있는 라인들 추가 (빈 라인, 페이지 마커 제외)
        for i in range(start_line + 1, min(start_line + 5, len(lines))):
            line = lines[i].strip()
            if line and not line.startswith('===') and not line.isdigit():
                start_boundary_lines.append(lines[i])
                if len(start_boundary_lines) >= 3:  # 제목 + 2줄 충분
                    break
        
        start_boundary = '\n'.join(start_boundary_lines)
        
        # 종료 경계: 마지막 의미있는 내용
        end_boundary_lines = []
        
        # 끝에서부터 역순으로 의미있는 라인 수집
        for i in range(end_line - 1, max(end_line - 10, start_line), -1):
            line = lines[i].strip()
            if line and not line.startswith('===') and not line.isdigit():
                end_boundary_lines.append(lines[i])
                if len(end_boundary_lines) >= 2:
                    break
        
        if end_boundary_lines:
            end_boundary = '\n'.join(reversed(end_boundary_lines))
        else:
            end_boundary = lines[end_line - 1] if end_line > start_line else lines[start_line]
        
        # 길이 제한 (너무 길면 잘라내기)
        if len(start_boundary) > 100:
            start_boundary = start_boundary[:100]
        if len(end_boundary) > 100:
            end_boundary = end_boundary[-100:]
        
        print(f"   ✓ 시작 경계 생성: '{start_boundary[:40]}...'")
        print(f"   ✓ 종료 경계 생성: '...{end_boundary[-40:]}'")
        
        return start_boundary.strip(), end_boundary.strip()


async def main():
    """메인 실행 함수"""
    print("🚀 최종 동적 리프노드 경계 추출기 (3번째 노드 테스트)")
    print("=" * 60)
    
    # 파일 경로
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    
    try:
        # 추출기 생성
        extractor = FinalBoundaryExtractor()
        
        # 파일 로드
        source_text, leaf_nodes = extractor.load_files(source_path, nodes_path)
        if not source_text or not leaf_nodes:
            return 1
        
        # 3번째 리프노드 선택
        target_index = 2
        target_node = leaf_nodes[target_index]
        next_node = leaf_nodes[target_index + 1] if target_index + 1 < len(leaf_nodes) else None
        
        print(f"\n🎯 테스트 대상: {target_node.get('title', 'Unknown')} (ID: {target_node.get('id', 'Unknown')})")
        
        # 경계 추출
        start_boundary, end_boundary = await extractor.extract_boundaries_hybrid(
            source_text, target_node, next_node
        )
        
        if not start_boundary or not end_boundary:
            return 1
        
        # 검증
        start_pos = source_text.find(start_boundary)
        end_pos = source_text.find(end_boundary)
        
        if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
            section_length = end_pos - start_pos + len(end_boundary)
            print(f"\n✅ 경계 추출 및 검증 성공!")
            print(f"📏 섹션 길이: {section_length:,}자")
            print(f"\n📝 최종 경계:")
            print(f"시작: '{start_boundary}'")
            print(f"종료: '{end_boundary}'")
        else:
            print(f"\n❌ 경계 검증 실패")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)