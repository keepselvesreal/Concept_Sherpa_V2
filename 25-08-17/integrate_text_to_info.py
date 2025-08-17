# 생성 시간: 2025-08-17 22:25:45 KST
# 핵심 내용: 섹션 텍스트 또는 전체 텍스트를 정보 파일의 '# 내용' 섹션에 통합하고 메타데이터를 삽입하는 스크립트
# 상세 내용:
#   - load_info_files 함수 (라인 23-29): 정보 파일들을 로드
#   - find_section_file 함수 (라인 32-41): 대응하는 섹션 파일 찾기
#   - load_metadata 함수 (라인 44-52): 메타데이터 JSON 파일 로드
#   - integrate_metadata 함수 (라인 55-84): 메타데이터를 속성 섹션에 삽입
#   - integrate_section_text 함수 (라인 87-140): 섹션 텍스트를 정보 파일에 통합
#   - update_process_status 함수 (라인 143-163): process_status를 true로 업데이트
#   - integrate_full_text_to_level_zero 함수 (라인 166-255): level 0 노드에 전체 텍스트 삽입
#   - main 함수 (라인 258-332): 메인 실행 함수 (--full-text 옵션 추가)
# 상태: 활성
# 주소: integrate_text_to_info/level_zero_full_text_v2
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
    # info_file: "01_lev1_title_info.md" -> section_file: "01_lev1_title.md"
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
        print(f"⚠️ 메타데이터 로드 실패: {e}")
        return None


def integrate_metadata(info_file: str, metadata: Dict) -> bool:
    """메타데이터를 속성 섹션에 삽입 (process_status 밑에, 기존 메타데이터 제거 후 새로 추가)"""
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
            print("❌ process_status 라인을 찾을 수 없음")
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
        print(f"❌ 메타데이터 통합 실패: {e}")
        return False


def extract_node_info_from_filename(info_file: str) -> tuple:
    """정보 파일명에서 노드 정보 추출 (level, title)"""
    filename = os.path.basename(info_file)
    # 예: "01_lev1_current_limitations_and_problems_in_ai_coding_info.md"
    parts = filename.replace('_info.md', '').split('_')
    
    if len(parts) >= 2 and parts[1].startswith('lev'):
        level = int(parts[1][3:])  # "lev1" -> 1
        title_parts = parts[2:]  # ["current", "limitations", "and", ...]
        title = ' '.join(word.capitalize() for word in title_parts)
        return level, title
    
    return 0, "Unknown Title"


def add_title_to_content_section(info_file: str) -> bool:
    """섹션 파일이 없을 때 노드 제목을 level에 맞는 헤더로 추가"""
    try:
        level, title = extract_node_info_from_filename(info_file)
        
        # level에 맞는 헤더 생성
        header_prefix = '#' * (level + 1)  # level 0 -> #, level 1 -> ##
        title_content = f"{header_prefix} {title}"
        
        # 정보 파일 읽기
        with open(info_file, 'r', encoding='utf-8') as f:
            info_content = f.read()
        
        # '# 내용' 섹션 찾기
        lines = info_content.split('\n')
        content_start = -1
        content_end = len(lines)
        
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_start = i
                break
        
        if content_start == -1:
            print(f"❌ '# 내용' 섹션을 찾을 수 없음: {os.path.basename(info_file)}")
            return False
        
        # 다음 섹션 시작 찾기
        for i in range(content_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                content_end = i
                break
        
        # 내용 추가 (구분선 다음에)
        insert_pos = content_start + 1
        if insert_pos < len(lines) and lines[insert_pos].strip() == '---':
            insert_pos += 1
        
        new_lines = (
            lines[:insert_pos] +
            [title_content] +
            [''] +
            lines[content_end:]
        )
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"❌ 제목 추가 실패: {e}")
        return False


def integrate_section_text(info_file: str, section_file: str) -> bool:
    """섹션 텍스트를 정보 파일의 '# 내용' 섹션에 통합"""
    try:
        # 섹션 텍스트 읽기
        with open(section_file, 'r', encoding='utf-8') as f:
            section_content = f.read().strip()
        
        # 정보 파일 읽기
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
            print(f"❌ '# 내용' 섹션을 찾을 수 없음: {os.path.basename(info_file)}")
            return False
        
        # 다음 섹션 시작 찾기
        for i in range(content_start + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                content_end = i
                break
        
        # 내용 삽입 (구분선 다음에)
        # '# 내용' 다음 라인이 '---'인지 확인
        insert_pos = content_start + 1
        if insert_pos < len(lines) and lines[insert_pos].strip() == '---':
            insert_pos += 1
        
        new_lines = (
            lines[:insert_pos] +
            [section_content] +
            [''] +
            lines[content_end:]
        )
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"❌ 텍스트 통합 실패: {e}")
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
        print(f"❌ process_status 업데이트 실패: {e}")
        return False


def integrate_full_text_to_level_zero(info_dir: str, full_text: str, metadata_file: str = None) -> bool:
    """level 0 노드 정보 문서의 내용 섹션에 전체 텍스트를 삽입하는 함수"""
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
            
            # 2. 전체 텍스트를 내용 섹션에 삽입
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
                [full_text] +
                [''] +
                lines[content_end:]
            )
            
            # 파일 저장
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            # 3. level 0 노드의 경우 구성 섹션 비우기
            # 구성 섹션 찾기 및 비우기
            with open(info_file, 'r', encoding='utf-8') as f:
                updated_content = f.read()
            
            updated_lines = updated_content.split('\n')
            composition_start = -1
            composition_end = len(updated_lines)
            
            # '# 구성' 섹션 찾기
            for i, line in enumerate(updated_lines):
                if line.strip() == '# 구성':
                    composition_start = i
                    break
            
            if composition_start != -1:
                # 다음 섹션 시작 찾기 (만약 있다면)
                for i in range(composition_start + 1, len(updated_lines)):
                    if updated_lines[i].strip().startswith('# ') and updated_lines[i].strip() != '# 구성':
                        composition_end = i
                        break
                
                # 구성 섹션을 구분선만 남기고 비우기
                composition_insert_pos = composition_start + 1
                if composition_insert_pos < len(updated_lines) and updated_lines[composition_insert_pos].strip() == '---':
                    composition_insert_pos += 1
                
                new_composition_lines = (
                    updated_lines[:composition_insert_pos] +
                    [''] +
                    updated_lines[composition_end:]
                )
                
                # 파일 재저장
                with open(info_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_composition_lines))
            
            # 4. 작업 완료 (process_status는 수동으로 관리)
            print(f"   ✅ 전체 텍스트 통합 및 구성 섹션 비우기 완료 (process_status는 false 유지)")
            integrated_count += 1
                
        except Exception as e:
            print(f"   ❌ 처리 실패: {e}")
            continue
    
    print(f"\n✅ Level 0 노드 전체 텍스트 통합 완료: {integrated_count}개 파일")
    return integrated_count > 0


def update_level_zero_with_content(info_dir: str, full_text_file: str, metadata_file: str = None) -> bool:
    """사용자 메타데이터와 원문으로 level 0 노드 문서를 업데이트하는 함수"""
    print("🚀 Level 0 노드 문서 업데이트 시작")
    print("=" * 50)
    
    # 원문 파일 확인
    if not os.path.exists(full_text_file):
        print(f"❌ 원문 파일을 찾을 수 없음: {full_text_file}")
        return False
    
    # 메타데이터 로드
    metadata = None
    if metadata_file and os.path.exists(metadata_file):
        metadata = load_metadata(metadata_file)
        print(f"📋 메타데이터 로드 완료: {metadata_file}")
    else:
        print(f"⚠️ 메타데이터 파일을 찾을 수 없음: {metadata_file}")
    
    # 원문 로드
    with open(full_text_file, 'r', encoding='utf-8') as f:
        full_text_content = f.read().strip()
    print(f"📖 원문 로드 완료: {full_text_file}")
    
    # level 0 정보 파일 찾기
    level_zero_files = []
    for file in os.listdir(info_dir):
        if file.endswith('_info.md') and '_lev0_' in file:
            level_zero_files.append(os.path.join(info_dir, file))
    
    if not level_zero_files:
        print("❌ Level 0 정보 파일을 찾을 수 없습니다.")
        return False
    
    print(f"🔍 Level 0 정보 파일 발견: {len(level_zero_files)}개")
    
    updated_count = 0
    
    for info_file in level_zero_files:
        print(f"\n📄 업데이트 중: {os.path.basename(info_file)}")
        
        try:
            # 1. 메타데이터 통합 (있는 경우)
            if metadata:
                if integrate_metadata(info_file, metadata):
                    print(f"   ✅ 메타데이터 통합 완료")
                else:
                    print(f"   ⚠️ 메타데이터 통합 실패")
            
            # 2. 원문을 내용 섹션에 삽입
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
                continue
            
            # 다음 섹션 시작 찾기
            for i in range(content_start + 1, len(lines)):
                if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                    content_end = i
                    break
            
            # 내용 삽입
            insert_pos = content_start + 1
            if insert_pos < len(lines) and lines[insert_pos].strip() == '---':
                insert_pos += 1
            
            new_lines = (
                lines[:insert_pos] +
                [full_text_content] +
                [''] +
                lines[content_end:]
            )
            
            # 파일 저장
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            # 3. level 0의 경우 구성 섹션 비우기
            with open(info_file, 'r', encoding='utf-8') as f:
                updated_content = f.read()
            
            updated_lines = updated_content.split('\n')
            composition_start = -1
            composition_end = len(updated_lines)
            
            # '# 구성' 섹션 찾기
            for i, line in enumerate(updated_lines):
                if line.strip() == '# 구성':
                    composition_start = i
                    break
            
            if composition_start != -1:
                # 다음 섹션 시작 찾기 (만약 있다면)
                for i in range(composition_start + 1, len(updated_lines)):
                    if updated_lines[i].strip().startswith('# ') and updated_lines[i].strip() != '# 구성':
                        composition_end = i
                        break
                
                # 구성 섹션을 구분선만 남기고 비우기
                composition_insert_pos = composition_start + 1
                if composition_insert_pos < len(updated_lines) and updated_lines[composition_insert_pos].strip() == '---':
                    composition_insert_pos += 1
                
                new_composition_lines = (
                    updated_lines[:composition_insert_pos] +
                    [''] +
                    updated_lines[composition_end:]
                )
                
                # 파일 재저장
                with open(info_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_composition_lines))
            
            print(f"   ✅ 원문 통합 및 구성 섹션 비우기 완료 (process_status는 false 유지)")
            updated_count += 1
                
        except Exception as e:
            print(f"   ❌ 업데이트 실패: {e}")
            continue
    
    print(f"\n✅ Level 0 노드 문서 업데이트 완료: {updated_count}개 파일")
    print(f"📝 process_status는 false로 유지됩니다 (정보 추출 작업 시 true로 변경)")
    return updated_count > 0


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
    
    # level 0 노드 업데이트 모드
    if args.level_zero_update:
        if not args.full_text:
            print("❌ --level-zero-update 사용 시 --full-text 옵션이 필요합니다.")
            return
        
        metadata_file = args.metadata or os.path.join(args.info_dir, 'user_input_metadata.json')
        update_level_zero_with_content(args.info_dir, args.full_text, metadata_file)
        return
    
    # 전체 텍스트를 level 0 노드에 삽입하는 경우 (기존 방식)
    if args.full_text:
        if not os.path.exists(args.full_text):
            print(f"❌ 전체 텍스트 파일을 찾을 수 없음: {args.full_text}")
            return
        
        with open(args.full_text, 'r', encoding='utf-8') as f:
            full_text_content = f.read().strip()
        
        integrate_full_text_to_level_zero(args.info_dir, full_text_content, args.metadata)
        return
    
    # 기존 섹션별 처리
    if not args.sections_dir:
        print("❌ sections_dir 또는 --full-text 중 하나는 필수입니다.")
        return
    
    print("🚀 섹션 텍스트를 정보 파일에 통합 시작")
    print("=" * 50)
    
    # 메타데이터 로드
    metadata = None
    if args.metadata and os.path.exists(args.metadata):
        metadata = load_metadata(args.metadata)
        print(f"📋 메타데이터 로드 완료: {args.metadata}")
    elif args.metadata:
        print(f"⚠️ 메타데이터 파일을 찾을 수 없음: {args.metadata}")
    
    # 정보 파일들 로드
    info_files = load_info_files(args.info_dir)
    print(f"📁 발견된 정보 파일: {len(info_files)}개")
    
    integrated_count = 0
    
    for info_file in info_files:
        print(f"\n📄 처리 중: {os.path.basename(info_file)}")
        
        # 1. 메타데이터 통합 (있는 경우)
        if metadata:
            if integrate_metadata(info_file, metadata):
                print(f"   ✅ 메타데이터 통합 완료")
            else:
                print(f"   ⚠️ 메타데이터 통합 실패")
        
        # 2. 대응하는 섹션 파일 찾기
        section_file = find_section_file(info_file, args.sections_dir)
        
        if section_file:
            # 3a. 섹션 파일이 있는 경우: 섹션 텍스트 통합
            if integrate_section_text(info_file, section_file):
                print(f"   ✅ 섹션 텍스트 통합 완료: {os.path.basename(section_file)}")
                
                # 4. process_status 업데이트
                if update_process_status(info_file):
                    print(f"   ✅ process_status 업데이트 완료")
                    integrated_count += 1
        else:
            # 3b. 섹션 파일이 없는 경우: 노드 제목 추가
            if add_title_to_content_section(info_file):
                print(f"   ✅ 노드 제목 추가 완료")
                # process_status는 업데이트하지 않음 (내용만 있고 추출은 아직)
            else:
                print(f"   ⚠️ 노드 제목 추가 실패")
    
    print(f"\n✅ 통합 완료: {integrated_count}개 파일")


if __name__ == "__main__":
    main()