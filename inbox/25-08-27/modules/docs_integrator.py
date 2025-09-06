# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: subprocess 제거된 노드 문서 통합 모듈
# 상세 내용:
#   - integrate_node_documents() (라인 14-65): 메인 문서 통합 함수
#   - integrate_metadata() (라인 67-88): 메타데이터 속성 섹션 통합
#   - integrate_content() (라인 90-115): 내용 섹션 통합 함수
# 상태: active
# 주소: modules/docs_integrator
# 참조: integrate_node_documents_fixed.py → 함수화

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional


def integrate_node_documents(video_folder: str) -> Dict[str, Any]:
    """노드 문서 통합 (subprocess 제거된 버전)"""
    try:
        if not os.path.exists(video_folder):
            return {"success": False, "error": f"비디오 폴더가 존재하지 않습니다: {video_folder}"}
        
        print("🔗 노드 문서 통합 시작")
        print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
        
        # 1. content.md 파일 확인
        content_file = os.path.join(video_folder, "content.md")
        if not os.path.exists(content_file):
            return {"success": False, "error": f"content.md 파일이 없습니다: {content_file}"}
        
        # 2. 기존 content.md 읽기
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 3. 메타데이터 로드
        metadata_file = os.path.join(video_folder, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # 4. 메타데이터 섹션 통합
        integrated_content = integrate_metadata(content, metadata)
        
        # 5. 노드 정보 문서들 통합
        docs_dir = os.path.join(video_folder, "node_info_docs")
        if os.path.exists(docs_dir):
            integrated_content = integrate_content(integrated_content, docs_dir)
        
        # 6. 통합된 내용을 content.md에 저장
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(integrated_content)
        
        print("=" * 50)
        print("🎉 노드 문서 통합 완료")
        print(f"📄 업데이트된 파일: {content_file}")
        
        return {
            "success": True,
            "updated_file": content_file,
            "integrated_sections": ["metadata", "node_docs"]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def integrate_metadata(content: str, metadata: Dict[str, Any]) -> str:
    """메타데이터 속성 섹션 통합"""
    try:
        # 메타데이터 섹션 생성
        metadata_section = """
## 📊 비디오 메타정보

- **제목**: {title}
- **언어**: {language}  
- **소스**: {source_url}
- **처리 날짜**: {processed_date}
- **구조 유형**: {structure_type}
- **처리 방식**: {content_processing}

---

""".format(
            title=metadata.get('title', 'N/A'),
            language=metadata.get('language', 'N/A'),
            source_url=metadata.get('source_url', 'N/A'),
            processed_date=metadata.get('processed_date', 'N/A'),
            structure_type=metadata.get('structure_type', 'N/A'),
            content_processing=metadata.get('content_processing', 'N/A')
        )
        
        # 기존 내용에 메타데이터 섹션 추가
        return metadata_section + content
        
    except Exception as e:
        print(f"⚠️ 메타데이터 통합 중 오류: {e}")
        return content


def integrate_content(content: str, docs_dir: str) -> str:
    """노드 정보 문서들을 내용에 통합"""
    try:
        # node_info_docs 디렉토리의 모든 .md 파일 찾기
        docs_path = Path(docs_dir)
        info_files = list(docs_path.glob("*_info.md"))
        
        if not info_files:
            print("⚠️ 통합할 노드 정보 문서가 없습니다")
            return content
        
        # 파일명으로 정렬
        info_files.sort(key=lambda x: x.name)
        
        # 노드 정보 섹션 생성
        nodes_section = "\n\n## 🌐 노드 상세 정보\n\n"
        
        for info_file in info_files:
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                nodes_section += f"### {info_file.name}\n\n"
                nodes_section += file_content + "\n\n---\n\n"
                
            except Exception as e:
                print(f"⚠️ 파일 {info_file.name} 읽기 실패: {e}")
        
        # 기존 내용에 노드 섹션 추가
        return content + nodes_section
        
    except Exception as e:
        print(f"⚠️ 노드 문서 통합 중 오류: {e}")
        return content