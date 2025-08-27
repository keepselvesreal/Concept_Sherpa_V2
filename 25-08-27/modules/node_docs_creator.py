# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: subprocess 제거된 노드 문서 생성 모듈
# 상세 내용:
#   - create_node_info_docs() (라인 15-70): 메인 노드 문서 생성 함수
#   - load_nodes() (라인 72-88): nodes.json 파일 로드 함수
#   - sanitize_title() (라인 90-102): 파일명용 제목 정리 함수
#   - create_info_file() (라인 104-137): 개별 노드 정보 파일 생성 함수
# 상태: active
# 주소: modules/node_docs_creator
# 참조: create_node_info_docs_fixed.py → 함수화

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


def create_node_info_docs(video_folder: str) -> Dict[str, Any]:
    """노드 정보 문서 생성 (subprocess 제거된 버전)"""
    try:
        # 폴더 존재 확인
        if not os.path.exists(video_folder):
            return {"success": False, "error": f"비디오 폴더가 존재하지 않습니다: {video_folder}"}
        
        print("🚀 노드 정보 문서 생성 시작")
        print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
        
        # 1. 노드 데이터 로드
        nodes = load_nodes(video_folder)
        if not nodes:
            return {"success": False, "error": "노드 데이터가 없습니다"}
        
        # 2. 메타데이터 로드 (기본값 설정)
        metadata_file = os.path.join(video_folder, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # 3. 출력 디렉토리 생성
        output_dir = os.path.join(video_folder, "node_info_docs")
        os.makedirs(output_dir, exist_ok=True)
        
        # 4. 각 노드별 정보 파일 생성
        created_files = []
        for i, node in enumerate(nodes):
            info_filename = create_info_file(node, i, output_dir, metadata)
            if info_filename:
                created_files.append(info_filename)
                print(f"✅ {info_filename} 생성됨")
            else:
                print(f"⚠️ 노드 {i} 정보 파일 생성 실패")
        
        print("=" * 50)
        print(f"🎉 완료: {len(created_files)}개 파일 생성")
        print(f"📂 출력 디렉토리: {output_dir}")
        
        return {
            "success": True,
            "output_dir": output_dir,
            "created_files": created_files,
            "node_count": len(created_files)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_nodes(video_folder: str) -> Optional[List[Dict[str, Any]]]:
    """nodes.json 파일 직접 로드"""
    nodes_file = os.path.join(video_folder, "nodes.json")
    
    if not os.path.exists(nodes_file):
        print(f"❌ nodes.json 파일이 없습니다: {nodes_file}")
        return None
    
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"📄 노드 파일 로드 완료: {len(nodes)}개 노드")
        return nodes
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        return None
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return None


def sanitize_title(title: str) -> str:
    """파일명용 제목 정리"""
    if not title:
        return "untitled"
    
    # 특수문자 제거 및 공백을 언더스코어로 변환
    sanitized = re.sub(r'[^\w\s-]', '', title)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.strip('_')


def create_info_file(node: Dict[str, Any], node_index: int, output_dir: str, metadata: Dict[str, Any]) -> Optional[str]:
    """개별 노드 정보 파일 생성"""
    try:
        title = node.get('title', f'노드_{node_index}')
        content = node.get('content', '')
        node_type = node.get('type', 'unknown')
        
        # 파일명 생성
        safe_title = sanitize_title(title)
        filename = f"{node_index:03d}_{safe_title}_{node_type}_info.md"
        filepath = os.path.join(output_dir, filename)
        
        # 정보 파일 내용 생성
        info_content = f"""# {title}

## 기본 정보
- **노드 인덱스**: {node_index}
- **제목**: {title}
- **타입**: {node_type}
- **생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 내용
{content}

## 메타정보
- **비디오 제목**: {metadata.get('title', 'N/A')}
- **언어**: {metadata.get('language', 'N/A')}
- **처리 날짜**: {metadata.get('processed_date', 'N/A')}
"""
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        return filename
        
    except Exception as e:
        print(f"❌ 노드 {node_index} 정보 파일 생성 오류: {e}")
        return None