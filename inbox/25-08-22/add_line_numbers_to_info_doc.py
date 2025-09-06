#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 17:07:00 KST
핵심 내용: 노드 정보 문서의 추출 섹션과 내용 섹션에 IDE 라인 번호 정보 추가
상세 내용: 
    - main() (라인 18-50): 메인 실행 함수, 명령행 인수 처리
    - add_line_numbers_to_sections() (라인 53-95): 추출 및 내용 섹션에 라인 번호 추가
    - remove_existing_line_info() (라인 98-125): 기존 라인 정보 제거
상태: active
주소: add_line_numbers_to_info_doc
참조: sync_line_numbers.py
"""

import re
import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python add_line_numbers_to_info_doc.py <info_md_file>")
        print("Example: python add_line_numbers_to_info_doc.py 00_lev0_Example_info.md")
        sys.exit(1)
    
    md_file_path = Path(sys.argv[1])
    
    if not md_file_path.exists():
        print(f"❌ 파일이 존재하지 않습니다: {md_file_path}")
        sys.exit(1)
    
    print("🔍 노드 정보 문서 라인 번호 동기화 시작")
    print("=" * 50)
    print(f"📁 대상 파일: {md_file_path}")
    
    # 1단계: 기존 라인 정보 제거
    cleaned_count = remove_existing_line_info(str(md_file_path))
    if cleaned_count > 0:
        print(f"✅ 기존 라인 정보 제거 완료: {cleaned_count}개")
    
    # 2단계: 새 라인 번호 추가
    updated_count = add_line_numbers_to_sections(str(md_file_path))
    if updated_count > 0:
        print(f"✅ 라인 번호 동기화 완료: {updated_count}개 라인")
        print(f"📍 IDE에서 보이는 라인 번호와 일치")
    else:
        print("ℹ️ 라인 번호를 추가할 내용이 없음")
    
    print(f"✅ 처리 완료: {md_file_path}")


def add_line_numbers_to_sections(file_path: str) -> int:
    """추출 섹션과 내용 섹션에 라인 번호 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        updated_lines = []
        updated_count = 0
        in_extraction_section = False
        in_content_section = False
        
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            # 섹션 시작/끝 확인
            if stripped == "# 추출":
                in_extraction_section = True
                in_content_section = False
            elif stripped == "# 내용":
                in_extraction_section = False
                in_content_section = True
            elif stripped == "# 구성":
                in_extraction_section = False
                in_content_section = False
            elif stripped.startswith("# ") and stripped not in ["# 추출", "# 내용", "# 구성", "# 속성"]:
                # 다른 섹션이면 모두 종료
                in_extraction_section = False
                in_content_section = False
            
            # 추출 섹션이나 내용 섹션에서 내용이 있는 라인에 라인 번호 추가
            if (in_extraction_section or in_content_section) and stripped:
                # 섹션 제목, 구분선(---), 빈 줄 제외
                if (not stripped.startswith("#") and 
                    stripped != "---" and 
                    not stripped.startswith("Line ")):  # 이미 라인 번호가 있는 경우 제외
                    
                    # 타임스탬프 패턴 확인 ([MM:SS])
                    if re.search(r'^\[\d{2}:\d{2}\]', stripped):
                        updated_line = f"Line {line_num}: {line}"
                        updated_lines.append(updated_line)
                        updated_count += 1
                        print(f"   타임스탬프 라인 {line_num}: {stripped[:50]}...")
                    else:
                        # 일반 텍스트 라인도 라인 번호 추가
                        if len(stripped) > 10:  # 의미있는 내용만
                            updated_line = f"Line {line_num}: {line}"
                            updated_lines.append(updated_line)
                            updated_count += 1
                            print(f"   텍스트 라인 {line_num}: {stripped[:50]}...")
                        else:
                            updated_lines.append(line)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # 파일에 다시 저장
        if updated_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
        
        return updated_count
        
    except Exception as e:
        print(f"❌ 라인 번호 추가 중 오류: {e}")
        return 0


def remove_existing_line_info(file_path: str) -> int:
    """기존 "Line X:" 정보 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # "Line X: " 패턴을 제거 (다양한 패턴 대응)
        patterns = [
            r'^Line \d+: ',  # 라인 시작 부분의 Line X: 제거
        ]
        
        cleaned_content = content
        total_count = 0
        
        for pattern in patterns:
            cleaned_content, count = re.subn(
                pattern,
                '',
                cleaned_content,
                flags=re.MULTILINE
            )
            total_count += count
        
        if total_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
        
        return total_count
        
    except Exception as e:
        print(f"❌ 기존 라인 정보 제거 중 오류: {e}")
        return 0


if __name__ == "__main__":
    main()