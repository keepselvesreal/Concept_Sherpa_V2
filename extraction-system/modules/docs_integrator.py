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
    """노드 문서 통합 - 리팩토링 전 방식 적용 (개별 노드 문서에 content.md 내용 통합)"""
    try:
        if not os.path.exists(video_folder):
            return {"success": False, "error": f"비디오 폴더가 존재하지 않습니다: {video_folder}"}
        
        print("🔗 노드 문서 통합 시작")
        print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
        
        # 1. 메타데이터 로드
        metadata_file = os.path.join(video_folder, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"✅ 메타데이터 로드 완료: {len(metadata)}개 필드")
        
        # 2. content.md 파일 로드
        content_file = os.path.join(video_folder, "content.md")
        content = None
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            print(f"📖 내용 로드 완료: {len(content)} 문자")
        else:
            print("ℹ️ content.md 파일이 없음")
        
        # 3. 노드 정보 문서 파일 찾기 (*_info.md)
        info_files = []
        for file in os.listdir(video_folder):
            if file.endswith('_info.md'):
                info_files.append(os.path.join(video_folder, file))
        
        if not info_files:
            return {"success": False, "error": "노드 정보 문서를 찾을 수 없습니다 (*_info.md)"}
        
        print(f"📁 발견된 노드 정보 문서: {len(info_files)}개")
        
        # 4. 각 파일별 통합 처리
        processed_count = 0
        for info_file in info_files:
            print(f"📄 처리 중: {os.path.basename(info_file)}")
            success = True
            
            # 메타데이터 통합
            if metadata and integrate_metadata_to_node(info_file, metadata):
                print(f"   ✅ 메타데이터 통합 완료")
            elif metadata:
                print(f"   ⚠️ 메타데이터 통합 실패")
                success = False
            
            # 내용 통합 (level 0 파일만)
            if '_lev0_' in os.path.basename(info_file) and content:
                if integrate_content_to_node(info_file, content):
                    print(f"   ✅ 내용 통합 완료")
                else:
                    print(f"   ⚠️ 내용 통합 실패")
                    success = False
            elif '_lev0_' in os.path.basename(info_file):
                print(f"   ℹ️ 내용 파일이 없음")
            else:
                print(f"   ℹ️ level 0이 아니므로 내용 통합 건너뜀")
            
            if success:
                processed_count += 1
        
        print("=" * 50)
        print("🎉 노드 문서 통합 완료")
        print(f"📂 처리된 파일: {processed_count}개")
        
        return {
            "success": True,
            "updated_file": f"{processed_count}개 노드 문서",
            "integrated_sections": ["metadata", "content"]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def integrate_metadata_to_node(info_file: str, metadata: Dict) -> bool:
    """메타데이터를 노드 정보 문서의 속성 섹션에 통합 (process_status만 false로 변경)"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # process_status: true -> false로 변경
        updated_content = re.sub(
            r'process_status: true', 
            'process_status: false', 
            content
        )
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"❌ 메타데이터 통합 실패: {e}")
        return False


def integrate_content_to_node(info_file: str, content: str) -> bool:
    """내용을 노드 정보 문서의 내용 섹션에 통합"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 내용 섹션 찾기 및 교체 (# 내용 --- 부터 # 구성 --- 까지)
        pattern = r'(# 내용\n---\n)(.*?)(# 구성\n---)'
        
        # 제목 추가 (파일명에서 추출)
        filename = os.path.basename(info_file)
        title_match = re.search(r'_lev\d+_(.+?)_info\.md', filename)
        title = title_match.group(1).replace('_', ' ') if title_match else "Content"
        
        new_content_section = f"# {title}\n\n{content}\n\n"
        
        replacement = rf'\1{new_content_section}\3'
        updated_content = re.sub(pattern, replacement, doc_content, flags=re.DOTALL)
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"❌ 내용 통합 실패: {e}")
        return False