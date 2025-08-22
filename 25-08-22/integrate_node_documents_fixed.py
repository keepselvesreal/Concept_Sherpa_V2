#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 16:55:00 KST
핵심 내용: 유튜브 ID별 폴더 구조에 맞게 수정된 노드 문서 통합 스크립트
상세 내용: 
    - main() (라인 22-88): 메인 실행 함수, content.md 직접 로드
    - integrate_metadata() (라인 91-112): 메타데이터 속성 섹션 통합
    - integrate_content() (라인 115-140): 내용 섹션 통합 함수
상태: active
주소: integrate_node_documents/fixed
참조: integrate_node_documents_v2
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python integrate_node_documents_fixed.py <video_folder>")
        print("Example: python integrate_node_documents_fixed.py ./YouTube_250822/VtmBevBcDzI")
        sys.exit(1)
    
    video_folder = sys.argv[1]
    
    # 폴더 존재 확인
    if not os.path.exists(video_folder):
        print(f"❌ 비디오 폴더가 존재하지 않습니다: {video_folder}")
        sys.exit(1)
    
    print("🚀 노드 정보 문서 통합 시작")
    print("=" * 50)
    print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
    
    # 1. 메타데이터 로드
    metadata = None
    metadata_file = os.path.join(video_folder, "metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✅ 메타데이터 로드 완료: {len(metadata)}개 필드")
    
    # 2. content.md 파일 직접 로드
    content = None
    content_file = os.path.join(video_folder, "content.md")
    if os.path.exists(content_file):
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        print(f"📖 내용 로드 완료: {len(content)} 문자")
    else:
        print("ℹ️ content.md 파일이 없음")
    
    # 3. 노드 정보 문서 파일 찾기
    info_files = []
    for file in os.listdir(video_folder):
        if file.endswith('_info.md'):
            info_files.append(os.path.join(video_folder, file))
    
    if not info_files:
        print("❌ 노드 정보 문서를 찾을 수 없습니다 (*_info.md)")
        sys.exit(1)
    
    print(f"📁 발견된 노드 정보 문서: {len(info_files)}개")
    
    # 4. 각 파일별 통합 처리
    processed_count = 0
    for info_file in info_files:
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
    print(f"📂 결과 위치: {os.path.abspath(video_folder)}")


def integrate_metadata(info_file: str, metadata: Dict) -> bool:
    """메타데이터를 노드 정보 문서의 속성 섹션에 통합"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 속성 섹션 업데이트
        lines = content.split('\n')
        in_properties = False
        new_lines = []
        
        for line in lines:
            if line.strip() == '# 속성':
                new_lines.append(line)
                in_properties = True
            elif line.strip() == '---' and in_properties:
                new_lines.append(line)
                # 메타데이터 추가
                for key, value in metadata.items():
                    if key not in ['created_at']:  # created_at은 기존 값 유지
                        new_lines.append(f"{key}: {value}")
                in_properties = False
            elif not in_properties:
                new_lines.append(line)
            # in_properties일 때는 기존 속성 라인들을 건너뜀 (메타데이터로 대체)
            elif line.startswith('process_status:') or line.startswith('created_at:'):
                new_lines.append(line)  # 이 두 필드는 유지
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
    except Exception as e:
        print(f"❌ 메타데이터 통합 실패: {e}")
        return False


def integrate_content(info_file: str, content: str) -> bool:
    """내용을 노드 정보 문서의 내용 섹션에 통합"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # 내용 섹션 찾기 및 교체
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


if __name__ == "__main__":
    main()