#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 20:54:00 KST
핵심 내용: 마크다운 파일의 헤더를 분석하여 JSON 노드 구조를 생성하는 범용 스크립트
상세 내용:
- extract_headers (라인 35-65): 마크다운 헤더 패턴 매칭 및 추출
- create_node_structure (라인 70-95): 헤더 정보를 JSON 노드로 변환
- save_json (라인 100-120): JSON 파일 저장 및 형식화
- main (라인 125-175): 메인 실행 함수, 파일 처리 및 결과 출력
상태: 활성
주소: header_to_json_converter
참조: node_section_extractor_v3.py의 노드 구조 호환성 고려
"""

import re
import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

def extract_headers(text: str) -> List[Tuple[str, int]]:
    """
    마크다운 텍스트에서 헤더를 추출합니다.
    
    Args:
        text: 마크다운 텍스트
        
    Returns:
        List of (title, level) tuples
        - title: 헤더 제목 (# 제외)
        - level: 헤더 레벨 (# 개수 - 1, 즉 # = 0, ## = 1, ### = 2)
    """
    headers = []
    
    # 마크다운 헤더 패턴: 줄 시작에 1-6개의 # + 공백 + 제목
    pattern = r'^(#{1,6})\s+(.+)$'
    
    lines = text.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        match = re.match(pattern, line)
        
        if match:
            hash_marks = match.group(1)
            title = match.group(2).strip()
            
            # 레벨 계산 (# 개수 - 1)
            level = len(hash_marks) - 1
            
            headers.append((title, level))
            print(f"📍 발견: {hash_marks} {title} (레벨 {level})")
    
    return headers

def create_node_structure(headers: List[Tuple[str, int]]) -> List[Dict[str, Any]]:
    """
    헤더 리스트를 JSON 노드 구조로 변환합니다.
    
    Args:
        headers: (title, level) 튜플 리스트
        
    Returns:
        노드 딕셔너리 리스트
    """
    nodes = []
    
    for idx, (title, level) in enumerate(headers):
        node = {
            "id": idx,
            "title": title,
            "level": level
        }
        nodes.append(node)
    
    return nodes

def save_json(nodes: List[Dict[str, Any]], output_path: str, indent: int = 2) -> bool:
    """
    노드 구조를 JSON 파일로 저장합니다.
    
    Args:
        nodes: 노드 딕셔너리 리스트
        output_path: 출력 파일 경로
        indent: JSON 들여쓰기
        
    Returns:
        성공 여부
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        print(f"❌ JSON 저장 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='마크다운 파일의 헤더를 JSON 노드 구조로 변환',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python header_to_json_converter.py medium/posts.txt
  python header_to_json_converter.py medium/posts.txt -o nodes.json
  python header_to_json_converter.py medium/posts.txt --indent 4
        """
    )
    
    parser.add_argument('input_file', help='입력 마크다운 파일')
    parser.add_argument('-o', '--output', help='출력 JSON 파일 (기본값: 입력파일명_nodes.json)')
    parser.add_argument('--indent', type=int, default=2, help='JSON 들여쓰기 (기본값: 2)')
    parser.add_argument('-v', '--verbose', action='store_true', help='상세 출력')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    # 입력 파일 존재 확인
    if not input_path.exists():
        print(f"❌ 입력 파일을 찾을 수 없습니다: {input_path}")
        return 1
    
    # 출력 파일 경로 설정
    if args.output:
        output_path = args.output
    else:
        output_path = input_path.stem + "_nodes.json"
    
    print("🔍 마크다운 헤더 → JSON 노드 변환기")
    print("=" * 50)
    print(f"📖 입력 파일: {input_path}")
    print(f"💾 출력 파일: {output_path}")
    print(f"🎯 들여쓰기: {args.indent}칸")
    
    # 파일 읽기
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
        return 1
    
    print(f"\n📊 파일 크기: {len(content):,}자")
    
    # 헤더 추출
    print("\n🔍 헤더 추출 중...")
    headers = extract_headers(content)
    
    if not headers:
        print("❌ 헤더를 찾을 수 없습니다.")
        return 1
    
    print(f"\n✅ 총 {len(headers)}개 헤더 발견")
    
    # 레벨별 통계
    if args.verbose:
        level_counts = {}
        for _, level in headers:
            level_counts[level] = level_counts.get(level, 0) + 1
        
        print("\n📈 레벨별 분포:")
        for level in sorted(level_counts.keys()):
            hash_display = "#" * (level + 1)
            print(f"   레벨 {level} ({hash_display}): {level_counts[level]}개")
    
    # JSON 노드 구조 생성
    print("\n🔄 JSON 노드 구조 생성 중...")
    nodes = create_node_structure(headers)
    
    # JSON 저장
    print(f"\n💾 JSON 파일 저장: {output_path}")
    if save_json(nodes, output_path, args.indent):
        print(f"✅ 성공! {len(nodes)}개 노드가 저장되었습니다.")
        
        # 샘플 출력
        if args.verbose and nodes:
            print(f"\n📝 첫 번째 노드 예시:")
            print(json.dumps(nodes[0], ensure_ascii=False, indent=2))
        
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())