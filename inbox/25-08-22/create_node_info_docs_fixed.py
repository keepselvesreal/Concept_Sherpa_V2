#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 16:53:00 KST
핵심 내용: 유튜브 ID별 폴더 구조에 맞게 수정된 노드 정보 문서 생성 스크립트
상세 내용: 
    - main() (라인 22-76): 메인 실행 함수, 폴더 구조 적응형 처리
    - load_nodes() (라인 79-95): nodes.json 파일 직접 로드 (패턴 매칭 제거)
    - sanitize_title() (라인 98-110): 파일명용 제목 정리 함수
    - create_info_file() (라인 113-146): 개별 노드 정보 파일 생성 함수
상태: active
주소: create_node_info_docs/fixed
참조: create_node_info_docs_v2
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python create_node_info_docs_fixed.py <video_folder>")
        print("Example: python create_node_info_docs_fixed.py ./YouTube_250822/VtmBevBcDzI")
        sys.exit(1)
    
    video_folder = sys.argv[1]
    
    # 폴더 존재 확인
    if not os.path.exists(video_folder):
        print(f"❌ 비디오 폴더가 존재하지 않습니다: {video_folder}")
        sys.exit(1)
    
    print("🚀 노드 정보 문서 생성 시작")
    print("=" * 50)
    print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
    
    # 1. 노드 데이터 로드
    nodes = load_nodes(video_folder)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        sys.exit(1)
    
    # 2. 메타데이터 로드 (기본값 설정)
    metadata_file = os.path.join(video_folder, "metadata.json")
    metadata = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✅ 메타데이터 로드: {len(metadata)}개 필드")
    else:
        print("ℹ️ 메타데이터 파일이 없어 기본값 사용")
        metadata = {
            "source": "youtube",
            "source_type": "youtube", 
            "source_language": "english",
            "structure_type": "standalone",
            "content_processing": "unified"
        }
    
    # 3. 출력 디렉토리는 video_folder 자체
    output_dir = Path(video_folder)
    print(f"📁 출력 디렉토리: {output_dir.absolute()}")
    
    # 4. 각 노드별 정보 파일 생성
    print("📄 정보 파일 생성 중...")
    created_files = []
    
    for node in nodes:
        info_filename = create_info_file(output_dir, node, metadata)
        if info_filename:
            created_files.append(info_filename)
            print(f"   📄 생성: {info_filename}")
    
    print(f"\n✅ 완료: {len(created_files)}개 정보 파일 생성")
    print(f"📂 파일 위치: {output_dir.absolute()}")
    

def load_nodes(video_folder: str) -> List[Dict[str, Any]]:
    """비디오 폴더에서 nodes.json 파일 직접 로드"""
    nodes_file = os.path.join(video_folder, "nodes.json")
    
    if not os.path.exists(nodes_file):
        print(f"❌ nodes.json 파일을 찾을 수 없습니다: {nodes_file}")
        return []
    
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 노드 로드 완료: {os.path.basename(nodes_file)}")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 실패: {e}")
        return []


def sanitize_title(title: str, max_length: int = 50) -> str:
    """파일명으로 사용할 수 있도록 제목을 정리"""
    # 특수문자 제거 및 공백을 언더스코어로 변경
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    
    # 길이 제한
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')
    
    return sanitized


def create_info_file(output_dir: Path, node: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    """개별 노드의 정보 파일 생성"""
    try:
        # 파일명 생성
        level = str(node.get('level', 0)).zfill(2)
        title = sanitize_title(node.get('title', 'Untitled'))
        filename = f"{level}_lev{node.get('level', 0)}_{title}_info.md"
        
        # 파일 경로
        file_path = output_dir / filename
        
        # 파일 내용 생성
        current_time = datetime.now().isoformat()
        
        content = f"""# 속성
---
process_status: false
created_at: {current_time}

# 추출
---


# 내용
---


# 구성
---

"""
        
        # 파일 작성
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
        
    except Exception as e:
        print(f"❌ 정보 파일 생성 실패: {e}")
        return None


if __name__ == "__main__":
    main()