#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 14:10:25
핵심 내용: MD 파일의 타임스탬프 라인을 IDE 실제 라인 번호와 동기화하는 스크립트
상세 내용: 
    - main() (line 15): 메인 실행 함수, 명령행 인수 처리
    - remove_existing_line_info() (line 35): 기존 "Line X:" 정보 제거
    - update_line_numbers() (line 55): 실제 IDE 라인 번호로 업데이트
    - validate_timestamp_lines() (line 85): 타임스탬프 라인 유효성 검증
상태: active
참조: test_line_update.py
"""

import re
import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python sync_line_numbers.py <markdown_file>")
        print("Example: python sync_line_numbers.py transcript_structured.md")
        sys.exit(1)
    
    md_file_path = Path(sys.argv[1])
    
    if not md_file_path.exists():
        print(f"❌ 파일이 존재하지 않습니다: {md_file_path}")
        sys.exit(1)
    
    print("🔍 MD 파일 라인 번호 동기화 시작")
    print("=" * 50)
    print(f"📁 대상 파일: {md_file_path}")
    
    # 1단계: 기존 라인 정보 제거
    cleaned_count = remove_existing_line_info(str(md_file_path))
    if cleaned_count > 0:
        print(f"✅ 기존 라인 정보 제거 완료: {cleaned_count}개")
    
    # 2단계: 새 라인 번호로 업데이트
    updated_count = update_line_numbers(str(md_file_path))
    if updated_count > 0:
        print(f"✅ 라인 번호 동기화 완료: {updated_count}개 타임스탬프 라인")
        print(f"📍 IDE에서 보이는 라인 번호와 일치")
    else:
        print("ℹ️ 타임스탬프 라인이 없거나 이미 동기화됨")


def remove_existing_line_info(file_path: str) -> int:
    """기존 "Line X:" 정보 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # "Line X: [MM:SS]" 패턴을 "[MM:SS]"로 변경
        cleaned_content, count = re.subn(
            r'^Line \d+: (\[\d{2}:\d{2}\])',
            r'\1',
            content,
            flags=re.MULTILINE
        )
        
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
        
        return count
        
    except Exception as e:
        print(f"❌ 기존 라인 정보 제거 중 오류: {e}")
        return 0


def update_line_numbers(file_path: str) -> int:
    """실제 IDE 라인 번호로 업데이트"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        updated_lines = []
        updated_count = 0
        
        for line_num, line in enumerate(lines, start=1):
            # 타임스탬프로 시작하는 라인 ([MM:SS])을 찾기
            if re.search(r'^\[\d{2}:\d{2}\]', line.strip()):
                updated_line = f"Line {line_num}: {line}"
                updated_lines.append(updated_line)
                updated_count += 1
                print(f"   동기화: Line {line_num} - {line.strip()[:50]}...")
            else:
                updated_lines.append(line)
        
        # 파일에 다시 저장
        if updated_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
        
        return updated_count
        
    except Exception as e:
        print(f"❌ 라인 번호 업데이트 중 오류: {e}")
        return 0


def validate_timestamp_lines(file_path: str) -> dict:
    """타임스탬프 라인 유효성 검증 및 통계"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        stats = {
            'total_lines': len(lines),
            'timestamp_lines': 0,
            'synced_lines': 0,
            'unsynced_lines': 0
        }
        
        for line_num, line in enumerate(lines, start=1):
            stripped_line = line.strip()
            
            # 타임스탬프 라인 확인
            if re.search(r'\[\d{2}:\d{2}\]', stripped_line):
                stats['timestamp_lines'] += 1
                
                # 동기화된 라인인지 확인
                if stripped_line.startswith(f'Line {line_num}:'):
                    stats['synced_lines'] += 1
                else:
                    stats['unsynced_lines'] += 1
        
        return stats
        
    except Exception as e:
        print(f"❌ 유효성 검증 중 오류: {e}")
        return {}


if __name__ == "__main__":
    main()