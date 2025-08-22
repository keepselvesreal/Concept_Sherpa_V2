#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 14:38:15
핵심 내용: 노드 정보 문서에 메타정보와 내용을 통합하는 스크립트
상세 내용: 
    - main() (line 20): 메인 실행 함수, 명령행 인수 처리
    - integrate_metadata() (line 50): 메타데이터를 속성 섹션에 통합
    - integrate_content() (line 90): 내용을 내용 섹션에 통합
    - update_process_status() (line 130): process_status를 true로 업데이트
상태: active
참조: integrate_node_documents.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python integrate_node_documents_v2.py <extraction_folder>")
        print("Example: python integrate_node_documents_v2.py ./YouTube_250822")
        sys.exit(1)
    
    extraction_folder = sys.argv[1]
    
    # 폴더 존재 확인
    if not os.path.exists(extraction_folder):
        print(f"❌ 추출 폴더가 존재하지 않습니다: {extraction_folder}")
        sys.exit(1)
    
    # 노드 정보 문서는 extraction 폴더에 직접 있음
    node_info_docs_dir = extraction_folder
    
    print("🚀 노드 정보 문서 통합 시작")
    print("=" * 50)
    print(f"📁 처리 폴더: {os.path.abspath(extraction_folder)}")
    
    # 메타데이터 파일 찾기
    metadata_file = os.path.join(extraction_folder, "metadata.json")
    metadata = None
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✅ 메타데이터 로드 완료: {len(metadata)}개 필드")
    
    # 내용 파일 찾기 (*_content.md)
    content_files = []
    for file in os.listdir(extraction_folder):
        if file.endswith('_content.md'):
            content_files.append(os.path.join(extraction_folder, file))
    
    content = None
    if content_files:
        with open(content_files[0], 'r', encoding='utf-8') as f:
            content = f.read().strip()
        print(f"📖 내용 로드 완료: {len(content)} 문자")
    
    # 노드 정보 문서 파일 찾기
    info_files = []
    for file in os.listdir(node_info_docs_dir):
        if file.endswith('_info.md'):
            info_files.append(os.path.join(node_info_docs_dir, file))
    
    if not info_files:
        print("❌ 노드 정보 문서 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print(f"📁 발견된 노드 정보 문서: {len(info_files)}개")
    
    # 각 노드 정보 문서에 대해 통합 처리
    processed_count = 0
    for info_file in sorted(info_files):
        print(f"\n📄 처리 중: {os.path.basename(info_file)}")
        
        success = True
        
        # 1. 메타데이터 통합
        if metadata and integrate_metadata(info_file, metadata):
            print(f"   ✅ 메타데이터 통합 완료")
        elif metadata:
            print(f"   ⚠️ 메타데이터 통합 실패")
            success = False
        
        # 2. 내용 통합 (level 0 파일만)
        if '_lev0_' in os.path.basename(info_file) and content:
            if integrate_content(info_file, content):
                print(f"   ✅ 내용 통합 완료")
            else:
                print(f"   ⚠️ 내용 통합 실패")
                success = False
        elif '_lev0_' in os.path.basename(info_file):
            print(f"   ℹ️ 내용 파일이 없음")
        else:
            print(f"   ℹ️ level 0이 아니므로 내용 통합 건너뜀")
        
        # 3. process_status는 false로 유지 (나중에 다른 단계에서 처리)
        if success:
            print(f"   ✅ 노드 문서 통합 완료 (process_status: false 유지)")
            processed_count += 1
    
    print(f"\n✅ 최종 노드 문서 통합 완료: {processed_count}개 파일 처리됨")
    print(f"📂 결과 위치: {os.path.abspath(extraction_folder)}")


def integrate_metadata(info_file: str, metadata: Dict) -> bool:
    """메타데이터를 속성 섹션에 통합 (process_status 밑에 추가)"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # process_status 라인과 다음 섹션 찾기
        process_status_idx = -1
        next_section_idx = len(lines)
        
        for i, line in enumerate(lines):
            if line.startswith('process_status:'):
                process_status_idx = i
            elif process_status_idx != -1 and line.strip().startswith('# '):
                next_section_idx = i
                break
        
        if process_status_idx == -1:
            print(f"   ❌ process_status 라인을 찾을 수 없음")
            return False
        
        # 새로운 메타데이터 라인 생성
        metadata_lines = []
        for key, value in metadata.items():
            if not key.startswith('_'):  # _로 시작하는 내부 필드는 제외
                metadata_lines.append(f"{key}: {value}")
        
        # process_status 다음부터 다음 섹션 전까지 기존 메타데이터 제거하고 새로 추가
        new_lines = (
            lines[:process_status_idx+1] +  # process_status 라인까지
            metadata_lines +                # 새 메타데이터
            [''] +                          # 빈 줄
            lines[next_section_idx:]        # 다음 섹션부터
        )
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"   ❌ 메타데이터 통합 실패: {e}")
        return False


def integrate_content(info_file: str, content: str) -> bool:
    """내용을 내용 섹션에 통합 (노드 title 포함)"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            info_content = f.read()
        
        lines = info_content.split('\n')
        content_start = -1
        content_end = len(lines)
        
        # '# 내용' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_start = i
                break
        
        if content_start == -1:
            print(f"   ❌ '# 내용' 섹션을 찾을 수 없음")
            return False
        
        # 노드 title 추출 (파일명에서)
        import os
        filename = os.path.basename(info_file)
        # 파일명 형식: 00_lev0_Building_and_prototyping_with_Claude_Code_info.md
        parts = filename.replace('_info.md', '').split('_', 2)
        if len(parts) >= 3:
            title_part = parts[2].replace('_', ' ')
        else:
            title_part = "Content"
        
        # 다음 섹션 시작 찾기
        for i in range(content_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                content_end = i
                break
        
        # 내용 삽입 (구분선 다음에 title과 함께)
        insert_pos = content_start + 1
        if insert_pos < len(lines) and lines[insert_pos].strip() == '---':
            insert_pos += 1
        
        new_lines = (
            lines[:insert_pos] +
            [f"# {title_part}"] +
            [''] +
            [content] +
            [''] +
            lines[content_end:]
        )
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"   ❌ 내용 통합 실패: {e}")
        return False


# update_process_status 함수는 제거됨 - process_status는 false로 유지


if __name__ == "__main__":
    main()