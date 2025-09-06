# 생성 시간: 2025-08-18 10:25:54 KST
# 핵심 내용: 섹션 텍스트 또는 전체 텍스트를 정보 파일의 '# 내용' 섹션에 통합하고 메타데이터를 삽입하는 스크립트 (제목 중복 방지)
# 상세 내용:
#   - load_info_files 함수 (라인 23-29): 정보 파일들을 로드
#   - find_section_file 함수 (라인 32-41): 대응하는 섹션 파일 찾기
#   - load_metadata 함수 (라인 44-52): 메타데이터 JSON 파일 로드
#   - integrate_metadata 함수 (라인 55-84): 메타데이터를 속성 섹션에 삽입
#   - remove_first_title 함수 (라인 87-105): 첫 번째 제목 라인 제거 (중복 방지)
#   - integrate_full_text_to_level_zero 함수 (라인 108-195): level 0 노드에 전체 텍스트 삽입 (제목 중복 방지)
#   - main 함수 (라인 198-272): 메인 실행 함수 (--full-text 옵션 추가)
# 상태: 활성
# 주소: integrate_text_to_info_v3/title_dedup_fixed
# 참조: integrate_text_to_info (원본 파일)

import os
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional

def load_info_files(info_dir: str) -> List[str]:
    """정보 파일들을 로드"""
    info_files = []
    for file in os.listdir(info_dir):
        if file.endswith('_info.md'):
            info_files.append(os.path.join(info_dir, file))
    return sorted(info_files)

def find_section_file(info_file: str, sections_dir: str) -> Optional[str]:
    """대응하는 섹션 파일 찾기"""
    info_filename = os.path.basename(info_file)
    section_filename = info_filename.replace('_info.md', '.md')
    section_path = os.path.join(sections_dir, section_filename)
    
    if os.path.exists(section_path):
        return section_path
    return None

def load_metadata(metadata_file: str) -> Optional[Dict]:
    """메타데이터 JSON 파일 로드"""
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        print(f"❌ 메타데이터 로드 실패: {e}")
        return None

def integrate_metadata(info_file: str, metadata: Dict) -> bool:
    """메타데이터를 속성 섹션에 삽입"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # '# 속성' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 속성':
                # 다음 라인이 구분선('---')인지 확인
                if i + 1 < len(lines) and lines[i + 1].strip() == '---':
                    # 구분선 다음에 메타데이터 삽입
                    insert_pos = i + 2
                    
                    # 메타데이터 라인들 생성
                    metadata_lines = []
                    for key, value in metadata.items():
                        if not key.startswith('_'):  # _instructions 같은 내부 키 제외
                            metadata_lines.append(f"{key}: {value}")
                    
                    # 기존 메타데이터 제거하고 새로 삽입
                    new_lines = lines[:insert_pos] + metadata_lines + ['']
                    
                    # 다음 섹션 찾기
                    next_section_start = -1
                    for j in range(insert_pos, len(lines)):
                        if lines[j].strip().startswith('# ') and lines[j].strip() != '# 속성':
                            next_section_start = j
                            break
                    
                    if next_section_start != -1:
                        new_lines.extend(lines[next_section_start:])
                    
                    # 파일 저장
                    with open(info_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    
                    return True
        
        return False
        
    except Exception as e:
        print(f"❌ 메타데이터 통합 실패: {e}")
        return False

def remove_first_title(text: str) -> str:
    """텍스트에서 첫 번째 문서 제목 라인만 제거 (중복 방지)"""
    lines = text.strip().split('\n')
    if not lines:
        return text
    
    # 첫 번째 라인이 문서 제목인지 확인 (# 시작하고 그 다음이 ## 또는 빈 라인)
    first_line = lines[0].strip()
    if first_line.startswith('# ') and not first_line.startswith('## '):
        # 두 번째 라인이 빈 라인이고 세 번째 라인이 ## 로 시작하면 문서 제목으로 판단
        if len(lines) >= 3 and lines[1].strip() == '' and lines[2].strip().startswith('## '):
            # 첫 번째 제목 라인과 그 다음 빈 라인 제거
            return '\n'.join(lines[2:])
        # 두 번째 라인이 바로 ## 로 시작하면 문서 제목으로 판단
        elif len(lines) >= 2 and lines[1].strip().startswith('## '):
            # 첫 번째 제목 라인만 제거
            return '\n'.join(lines[1:])
    
    return text

def integrate_full_text_to_level_zero(info_dir: str, full_text: str, metadata_file: str = None) -> bool:
    """level 0 노드 정보 문서의 내용 섹션에 전체 텍스트를 삽입하는 함수 (제목 중복 방지)"""
    print("🚀 Level 0 노드에 전체 텍스트 통합 시작")
    print("=" * 50)
    
    # 메타데이터 로드
    metadata = None
    if metadata_file and os.path.exists(metadata_file):
        metadata = load_metadata(metadata_file)
        print(f"📋 메타데이터 로드 완료: {metadata_file}")
    
    # level 0 정보 파일 찾기 (파일명에 lev0 포함)
    level_zero_files = []
    for file in os.listdir(info_dir):
        if file.endswith('_info.md') and '_lev0_' in file:
            level_zero_files.append(os.path.join(info_dir, file))
    
    if not level_zero_files:
        print("❌ Level 0 정보 파일을 찾을 수 없습니다.")
        return False
    
    print(f"🔍 Level 0 정보 파일 발견: {len(level_zero_files)}개")
    
    integrated_count = 0
    
    for info_file in level_zero_files:
        print(f"\n📄 처리 중: {os.path.basename(info_file)}")
        
        try:
            # 1. 메타데이터 통합 (있는 경우)
            if metadata:
                if integrate_metadata(info_file, metadata):
                    print(f"   ✅ 메타데이터 통합 완료")
                else:
                    print(f"   ⚠️ 메타데이터 통합 실패")
            
            # 2. 전체 텍스트에서 첫 번째 제목 제거 (중복 방지)
            cleaned_text = remove_first_title(full_text)
            
            # 3. 전체 텍스트를 내용 섹션에 삽입
            with open(info_file, 'r', encoding='utf-8') as f:
                info_content = f.read()
            
            # '# 내용' 섹션 찾기 및 교체
            lines = info_content.split('\n')
            content_start = -1
            content_end = len(lines)
            
            # '# 내용' 섹션 시작 찾기
            for i, line in enumerate(lines):
                if line.strip() == '# 내용':
                    content_start = i
                    break
            
            if content_start == -1:
                print(f"   ❌ '# 내용' 섹션을 찾을 수 없음")
                continue
            
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
                [cleaned_text] +
                [''] +
                lines[content_end:]
            )
            
            # 파일 저장
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            # 4. level 0 노드의 경우 구성 섹션 비우기
            with open(info_file, 'r', encoding='utf-8') as f:
                info_content = f.read()
            
            lines = info_content.split('\n')
            
            for i, line in enumerate(lines):
                if line.strip() == '# 구성':
                    # 다음 섹션 시작 찾기
                    next_section_start = len(lines)
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip().startswith('# ') and lines[j].strip() != '# 구성':
                            next_section_start = j
                            break
                    
                    # 구성 섹션을 비우고 구분선만 남기기
                    new_lines = (
                        lines[:i] +
                        ['# 구성', '---', ''] +
                        lines[next_section_start:]
                    )
                    
                    # 파일 저장
                    with open(info_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    break
            
            print(f"   ✅ 전체 텍스트 통합 및 구성 섹션 비우기 완료 (제목 중복 방지, process_status는 false 유지)")
            integrated_count += 1
            
        except Exception as e:
            print(f"   ❌ 처리 실패: {e}")
    
    print(f"\n✅ Level 0 노드 전체 텍스트 통합 완료: {integrated_count}개 파일")
    return integrated_count > 0

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='섹션 텍스트를 정보 파일에 통합하고 메타데이터 삽입')
    parser.add_argument('info_dir', help='정보 파일들이 있는 디렉토리')
    parser.add_argument('sections_dir', nargs='?', help='섹션 파일들이 있는 디렉토리')
    parser.add_argument('-m', '--metadata', help='메타데이터 JSON 파일 경로')
    parser.add_argument('--full-text', help='level 0 노드에 삽입할 전체 텍스트 파일 경로')
    parser.add_argument('--level-zero-update', action='store_true', 
                       help='level 0 노드 업데이트 모드 (메타데이터와 원문 통합)')
    
    args = parser.parse_args()
    
    # --full-text 옵션이 제공된 경우 level 0 전용 처리
    if args.full_text:
        if not os.path.exists(args.full_text):
            print(f"❌ 전체 텍스트 파일을 찾을 수 없음: {args.full_text}")
            return
        
        # 전체 텍스트 로드
        with open(args.full_text, 'r', encoding='utf-8') as f:
            full_text_content = f.read().strip()
        
        integrate_full_text_to_level_zero(args.info_dir, full_text_content, args.metadata)
        return
    
    # 기존 처리는 생략 (level 0 전용 기능만 구현)
    print("❌ --full-text 옵션이 필요합니다.")

if __name__ == "__main__":
    main()