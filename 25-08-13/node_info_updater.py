#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 21:30:15 KST
핵심 내용: 노드 정보 문서의 내용 섹션에 실제 노드 데이터를 추가하는 스크립트
상세 내용:
- load_nodes (라인 25-40): JSON 파일에서 노드 데이터 로드
- find_info_files (라인 45-60): 디렉토리에서 *_info.md 파일 검색
- find_corresponding_content_file (라인 65-85): info 파일에 대응하는 내용 파일 검색
- generate_header_from_title (라인 90-105): 제목을 헤더로 변환 (레벨 고려)
- update_info_file_content (라인 110-170): info 파일의 내용 섹션 업데이트
- process_all_info_files (라인 175-215): 모든 info 파일 처리
- main (라인 220-250): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: node_info_updater
참조: info 파일과 content 파일 간의 매핑 및 내용 삽입
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

def load_nodes(nodes_file: str) -> List[Dict[str, Any]]:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # headers 키가 있는 경우 추출
        if isinstance(nodes, dict) and 'headers' in nodes:
            nodes = nodes['headers']
            
        return nodes
    except Exception as e:
        print(f"노드 파일 로드 오류: {e}")
        return []

def find_info_files(directory: str) -> List[str]:
    """디렉토리에서 *_info.md 패턴의 파일들을 찾습니다."""
    info_files = []
    for file in os.listdir(directory):
        if file.endswith('_info.md'):
            info_files.append(os.path.join(directory, file))
    return sorted(info_files)

def find_corresponding_content_file(info_file: str, directory: str) -> Optional[str]:
    """info 파일에 대응하는 내용 파일을 찾습니다.
    
    예: 1_When_Experience_Becomes_a_Handicap_info.md
    -> 1_When_Experience_Becomes_a_Handicap.md
    """
    # info 파일명에서 _info.md 제거
    base_name = os.path.basename(info_file)
    if base_name.endswith('_info.md'):
        content_name = base_name[:-8] + '.md'  # _info.md -> .md
        content_path = os.path.join(directory, content_name)
        
        if os.path.exists(content_path):
            return content_path
    
    return None

def generate_header_from_title(title: str, level: int) -> str:
    """제목을 레벨에 맞는 마크다운 헤더로 변환합니다.
    
    level 1 -> ### (level + 2개의 #)
    level 0 -> ## (level + 2개의 #)
    """
    header_level = level + 2
    headers = '#' * header_level
    return f"{headers} {title}"

def update_info_file_content(info_file: str, nodes: List[Dict[str, Any]], directory: str) -> bool:
    """info 파일의 내용 섹션을 업데이트합니다."""
    
    try:
        # info 파일 읽기
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 파일명에서 노드 정보 추출 (level_title_info.md)
        base_name = os.path.basename(info_file)
        if not base_name.endswith('_info.md'):
            print(f"⚠️  올바르지 않은 파일명 형식: {base_name}")
            return False
        
        # level_title 부분 추출
        name_without_info = base_name[:-8]  # _info.md 제거
        
        # 레벨과 제목 분리
        parts = name_without_info.split('_', 1)
        if len(parts) < 2:
            print(f"⚠️  레벨 정보를 찾을 수 없음: {base_name}")
            return False
        
        level_str, title_part = parts
        try:
            level = int(level_str)
        except ValueError:
            print(f"⚠️  레벨을 숫자로 변환 불가: {level_str}")
            return False
        
        # 언더스코어를 공백으로 변환하여 제목 복원
        title = title_part.replace('_', ' ')
        
        # 노드에서 정확한 제목 찾기
        node_title = None
        for node in nodes:
            if node.get('level') == level and node.get('title'):
                # 제목이 유사한지 확인 (공백/언더스코어 차이 무시)
                node_title_normalized = node['title'].replace(' ', '_').replace('-', '_')
                if title_part.lower() == node_title_normalized.lower():
                    node_title = node['title']
                    break
        
        if not node_title:
            node_title = title
        
        # 대응하는 내용 파일 찾기
        content_file = find_corresponding_content_file(info_file, directory)
        
        # 내용 섹션 찾기 및 업데이트
        lines = content.split('\n')
        content_section_start = -1
        
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_section_start = i
                break
        
        if content_section_start == -1:
            print(f"⚠️  '# 내용' 섹션을 찾을 수 없음: {base_name}")
            return False
        
        # 내용 섹션 업데이트
        if content_file and os.path.exists(content_file):
            # 내용 파일이 있는 경우
            with open(content_file, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
            
            # 내용 섹션 바로 다음에 파일 내용 삽입
            new_lines = lines[:content_section_start + 1] + [file_content]
            print(f"✅ 내용 파일 삽입: {os.path.basename(content_file)} → {base_name}")
        else:
            # 내용 파일이 없는 경우, 제목을 헤더로 삽입
            header = generate_header_from_title(node_title, level)
            new_lines = lines[:content_section_start + 1] + [header]
            print(f"✅ 제목 헤더 삽입: {header} → {base_name}")
        
        # 구성 섹션이 있으면 그 부분은 유지
        config_section_start = -1
        for i, line in enumerate(lines):
            if line.strip() == '# 구성':
                config_section_start = i
                break
        
        if config_section_start != -1:
            new_lines.extend([''] + lines[config_section_start:])
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"❌ {os.path.basename(info_file)} 처리 오류: {e}")
        return False

def process_all_info_files(nodes: List[Dict[str, Any]], directory: str) -> None:
    """디렉토리의 모든 info 파일을 처리합니다."""
    
    info_files = find_info_files(directory)
    
    if not info_files:
        print("📋 처리할 *_info.md 파일이 없습니다.")
        return
    
    print(f"🔍 발견된 info 파일: {len(info_files)}개")
    for info_file in info_files:
        print(f"   - {os.path.basename(info_file)}")
    
    print(f"\n🚀 info 파일 내용 업데이트 시작...")
    
    success_count = 0
    for info_file in info_files:
        if update_info_file_content(info_file, nodes, directory):
            success_count += 1
    
    print(f"\n✅ 처리 완료: {success_count}/{len(info_files)}개 성공")

def main():
    """메인 실행 함수"""
    if len(sys.argv) < 3:
        print("사용법: python node_info_updater.py <노드파일> <디렉토리>")
        print("예시: python node_info_updater.py posts_nodes.json ./post/")
        print()
        print("기능: 노드 정보 문서(*_info.md)의 내용 섹션에 실제 노드 데이터를 추가")
        return
    
    nodes_file = sys.argv[1]
    directory = sys.argv[2]
    
    print("📄 노드 정보 문서 업데이터")
    print("=" * 50)
    print(f"📋 노드 파일: {nodes_file}")
    print(f"📁 디렉토리: {directory}")
    
    # 파일 존재 확인
    if not os.path.exists(nodes_file):
        print(f"❌ 노드 파일을 찾을 수 없습니다: {nodes_file}")
        return
    
    if not os.path.isdir(directory):
        print(f"❌ 디렉토리를 찾을 수 없습니다: {directory}")
        return
    
    # 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("❌ 노드 데이터를 로드할 수 없습니다.")
        return
    
    print(f"📊 로드된 노드: {len(nodes)}개")
    print("\n" + "=" * 50)
    
    # 모든 info 파일 처리
    process_all_info_files(nodes, directory)
    
    print(f"\n✨ 작업 완료!")

if __name__ == "__main__":
    main()