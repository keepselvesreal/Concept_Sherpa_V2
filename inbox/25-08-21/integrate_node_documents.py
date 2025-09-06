#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 13:20:15
핵심 내용: 순수 내용과 사용자 확인 데이터를 기존 노드 정보 문서에 통합하는 스크립트
상세 내용: 
    - main() (line 20): 메인 실행 함수, 명령행 인수 처리
    - load_metadata() (line 45): 사용자 확인 데이터 JSON 파일 로드
    - integrate_metadata() (line 55): 메타데이터를 속성 섹션에 통합
    - integrate_content() (line 95): 순수 내용을 내용 섹션에 통합
    - clear_composition_section() (line 135): 구성 섹션 비우기 (level 0용)
    - update_process_status() (line 165): process_status true로 업데이트
상태: active
참조: integrate_text_to_info.py
"""

import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 4:
        print("Usage: python finalize_knowledge_document.py <node_info_docs_dir> <content_only_md> <user_verification_json>")
        print("Example: python finalize_knowledge_document.py node_info_docs content_only.md user_verification.json")
        sys.exit(1)
    
    node_info_docs_dir = sys.argv[1]
    content_only_md = sys.argv[2] 
    user_verification_json = sys.argv[3]
    
    # 파일 및 디렉토리 존재 확인
    if not os.path.exists(node_info_docs_dir):
        print(f"❌ 노드 정보 문서 디렉토리가 존재하지 않습니다: {node_info_docs_dir}")
        sys.exit(1)
    
    if not os.path.exists(content_only_md):
        print(f"❌ 순수 내용 파일이 존재하지 않습니다: {content_only_md}")
        sys.exit(1)
        
    if not os.path.exists(user_verification_json):
        print(f"❌ 사용자 확인 데이터 파일이 존재하지 않습니다: {user_verification_json}")
        sys.exit(1)
    
    print("🚀 최종 지식 문서 통합 시작")
    print("=" * 50)
    
    # 데이터 로드
    metadata = load_metadata(user_verification_json)
    if not metadata:
        sys.exit(1)
    
    with open(content_only_md, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    print(f"📖 순수 내용 로드 완료: {len(content)} 문자")
    
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
        if integrate_metadata(info_file, metadata):
            print(f"   ✅ 메타데이터 통합 완료")
        else:
            print(f"   ⚠️ 메타데이터 통합 실패")
            success = False
        
        # 2. 순수 내용 통합 (level 0 파일만)
        if '_lev0_' in os.path.basename(info_file):
            if integrate_content(info_file, content):
                print(f"   ✅ 순수 내용 통합 완료")
                
                # 3. 구성 섹션 비우기 (level 0용)
                if clear_composition_section(info_file):
                    print(f"   ✅ 구성 섹션 정리 완료")
                else:
                    print(f"   ⚠️ 구성 섹션 정리 실패")
            else:
                print(f"   ⚠️ 순수 내용 통합 실패")
                success = False
        else:
            print(f"   ℹ️ level 0이 아니므로 내용 통합 건너뜀")
        
        # 4. process_status 업데이트
        if success and update_process_status(info_file):
            print(f"   ✅ process_status 업데이트 완료")
            processed_count += 1
        elif success:
            print(f"   ⚠️ process_status 업데이트 실패")
    
    print(f"\n✅ 최종 지식 문서 통합 완료: {processed_count}개 파일 처리됨")
    print(f"📂 결과 위치: {os.path.abspath(node_info_docs_dir)}")


def load_metadata(metadata_file: str) -> Optional[Dict]:
    """사용자 확인 데이터 JSON 파일 로드"""
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"📋 사용자 확인 데이터 로드 완료: {len(metadata)}개 필드")
        return metadata
    except Exception as e:
        print(f"❌ 사용자 확인 데이터 로드 실패: {e}")
        return None


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
            if not key.startswith('_'):  # _instructions는 제외
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
    """순수 내용을 내용 섹션에 통합"""
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
        
        # 다음 섹션 시작 찾기
        for i in range(content_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                content_end = i
                break
        
        # 내용 삽입 (구분선 다음에)
        insert_pos = content_start + 1
        if insert_pos < len(lines) and lines[insert_pos].strip() == '---':
            insert_pos += 1
        
        new_lines = (
            lines[:insert_pos] +
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


def clear_composition_section(info_file: str) -> bool:
    """구성 섹션 비우기 (level 0 노드용)"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        composition_start = -1
        composition_end = len(lines)
        
        # '# 구성' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 구성':
                composition_start = i
                break
        
        if composition_start == -1:
            print(f"   ℹ️ '# 구성' 섹션을 찾을 수 없음")
            return True  # 구성 섹션이 없어도 정상
        
        # 다음 섹션 시작 찾기 (있다면)
        for i in range(composition_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 구성':
                composition_end = i
                break
        
        # 구성 섹션을 구분선만 남기고 비우기
        insert_pos = composition_start + 1
        if insert_pos < len(lines) and lines[insert_pos].strip() == '---':
            insert_pos += 1
        
        new_lines = (
            lines[:insert_pos] +
            [''] +
            lines[composition_end:]
        )
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"   ❌ 구성 섹션 정리 실패: {e}")
        return False


def update_process_status(info_file: str) -> bool:
    """process_status를 true로 업데이트"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # process_status 업데이트
        updated_content = re.sub(
            r'process_status:\s*false',
            'process_status: true',
            content
        )
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
        
    except Exception as e:
        print(f"   ❌ process_status 업데이트 실패: {e}")
        return False


if __name__ == "__main__":
    main()