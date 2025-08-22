"""
생성 시간: 2025-08-22 12:26:14 KST
핵심 내용: 메타데이터 JSON과 MD 파일을 받아서 노드 정보 JSON 파일을 생성하는 스크립트
상세 내용:
    - main(): 메인 실행 함수, 명령행 인수 처리 및 전체 플로우 제어 (20-60)
    - load_metadata(metadata_file): JSON 메타데이터 파일 로드 (62-75)
    - extract_headers_by_type(content, metadata): 메타데이터 조건에 따른 헤더 추출 (77-110)
    - extract_all_headers(content): 모든 헤더 추출 (112-135)
    - extract_first_header_only(content): 첫 번째 헤더만 추출 (137-155)
    - clean_title(title): 헤더 텍스트 정제 (157-166)
상태: active
참조: extract_md_data.py
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 3:
        print("Usage: python node_generator.py <metadata.json> <markdown_file.md>")
        print("Example: python node_generator.py metadata.json 250822_001_DAQJvGjlgVM.md")
        sys.exit(1)
    
    metadata_file = Path(sys.argv[1])
    md_file = Path(sys.argv[2])
    
    # 파일 존재 확인
    if not metadata_file.exists():
        print(f"❌ 메타데이터 파일을 찾을 수 없습니다: {metadata_file}")
        sys.exit(1)
        
    if not md_file.exists():
        print(f"❌ 마크다운 파일을 찾을 수 없습니다: {md_file}")
        sys.exit(1)
    
    print(f"📁 메타데이터 파일: {metadata_file}")
    print(f"📁 마크다운 파일: {md_file}")
    
    # 메타데이터 로드
    metadata = load_metadata(metadata_file)
    if not metadata:
        sys.exit(1)
    
    # MD 파일 읽기
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 마크다운 파일 읽기 오류: {str(e)}")
        sys.exit(1)
    
    # 헤더 추출
    nodes = extract_headers_by_type(content, metadata)
    
    # 출력 파일명 생성 (날짜 정보 제거)
    base_name = md_file.stem
    
    # 날짜 정보 제거 (250822_001_DAQJvGjlgVM -> 001_DAQJvGjlgVM)
    if '_' in base_name:
        parts = base_name.split('_', 2)  # ['250822', '001', 'DAQJvGjlgVM']
        if len(parts) >= 3:
            clean_name = f"{parts[1]}_{parts[2]}"  # 001_DAQJvGjlgVM
        else:
            clean_name = base_name
    else:
        clean_name = base_name
    
    nodes_file = md_file.parent / f"{clean_name}_nodes.json"
    
    # JSON 파일로 저장
    try:
        with open(nodes_file, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 노드 추출 완료: {len(nodes)}개 헤더")
        print(f"✅ 노드 파일 저장: {nodes_file}")
        
    except Exception as e:
        print(f"❌ 파일 저장 오류: {str(e)}")
        sys.exit(1)


def load_metadata(metadata_file: Path) -> Dict[str, Any]:
    """JSON 메타데이터 파일 로드"""
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✅ 메타데이터 로드 완료")
        return metadata
    except Exception as e:
        print(f"❌ 메타데이터 파일 로드 오류: {str(e)}")
        return {}


def extract_headers_by_type(content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """메타데이터 조건에 따른 헤더 추출"""
    structure_type = metadata.get("structure_type", "")
    content_processing = metadata.get("content_processing", "")
    
    print(f"📋 구조 타입: {structure_type}")
    print(f"📋 콘텐츠 처리: {content_processing}")
    
    # standalone + unified 조건 확인
    if structure_type == "standalone" and content_processing == "unified":
        print("🎯 조건 만족: standalone + unified -> 첫 번째 헤더만 추출")
        return extract_first_header_only(content)
    else:
        print("🎯 기본 조건: 모든 헤더 추출")
        return extract_all_headers(content)


def extract_all_headers(content: str) -> List[Dict[str, Any]]:
    """모든 헤더 추출"""
    nodes = []
    node_id = 0
    
    lines = content.split('\n')
    
    for line in lines:
        if line.strip().startswith('#'):
            # 헤더 레벨과 텍스트 추출
            match = re.match(r'^(#+)\s*(.+)', line.strip())
            if match:
                header_level = len(match.group(1))  # # 개수
                header_text = match.group(2).strip()
                cleaned_title = clean_title(header_text)
                
                node = {
                    "id": node_id,
                    "level": header_level - 1,  # 헤더 레벨 - 1
                    "title": cleaned_title
                }
                nodes.append(node)
                node_id += 1
    
    return nodes


def extract_first_header_only(content: str) -> List[Dict[str, Any]]:
    """첫 번째 헤더만 추출 (standalone + unified 조건)"""
    lines = content.split('\n')
    
    for line in lines:
        if line.strip().startswith('#'):
            # 헤더 레벨과 텍스트 추출
            match = re.match(r'^(#+)\s*(.+)', line.strip())
            if match:
                header_level = len(match.group(1))  # # 개수
                header_text = match.group(2).strip()
                cleaned_title = clean_title(header_text)
                
                node = {
                    "id": 0,
                    "level": header_level - 1,  # 헤더 레벨 - 1
                    "title": cleaned_title
                }
                return [node]  # 첫 번째 헤더만 반환
    
    return []  # 헤더가 없는 경우


def clean_title(title: str) -> str:
    """헤더 텍스트 정제"""
    # 맨 앞의 숫자와 점/공백 제거 (예: "1. Title" -> "Title")
    cleaned = re.sub(r'^\d+\.?\s*', '', title)
    cleaned = cleaned.strip()
    return cleaned


if __name__ == "__main__":
    main()