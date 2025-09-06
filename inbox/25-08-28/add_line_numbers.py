#!/usr/bin/env python3
"""
생성 시간: 2025-08-28 09:40:25
핵심 내용: MD 파일의 모든 라인에 IDE와 동일한 라인 번호를 추가하는 스크립트
상세 내용: 
    - main() (line 19): 메인 실행 함수, 명령행 인수 처리
    - add_line_numbers() (line 40): 각 라인에 "Line X: " 형식으로 라인 번호 추가
    - validate_output() (line 67): 출력 파일 유효성 검증
상태: active
주소: add_line_numbers
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-21/sync_line_numbers.py
"""

import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("Usage: python add_line_numbers.py <markdown_file>")
        print("Example: python add_line_numbers.py DOP.md")
        sys.exit(1)
    
    input_file_path = Path(sys.argv[1])
    
    if not input_file_path.exists():
        print(f"❌ 파일이 존재하지 않습니다: {input_file_path}")
        sys.exit(1)
    
    # 출력 파일명 생성 (원본파일명_with_lines.md)
    output_file_path = input_file_path.parent / f"{input_file_path.stem}_with_lines.md"
    
    print("🔍 MD 파일 라인 번호 추가 시작")
    print("=" * 50)
    print(f"📁 입력 파일: {input_file_path}")
    print(f"📁 출력 파일: {output_file_path}")
    
    # 라인 번호 추가
    total_lines = add_line_numbers(str(input_file_path), str(output_file_path))
    
    if total_lines > 0:
        print(f"✅ 라인 번호 추가 완료: {total_lines}개 라인")
        print(f"📍 IDE 라인 번호와 동일한 형식으로 생성됨")
        
        # 출력 파일 검증
        if validate_output(str(output_file_path)):
            print(f"✅ 출력 파일 검증 완료")
    else:
        print("❌ 라인 번호 추가 실패")


def add_line_numbers(input_path: str, output_path: str) -> int:
    """각 라인에 "Line X: " 형식으로 라인 번호 추가"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        numbered_lines = []
        
        for line_num, line in enumerate(lines, start=1):
            # 각 라인 앞에 "Line X: " 추가
            # 개행 문자 처리: 기존 라인의 개행 문자 유지
            if line.endswith('\n'):
                numbered_line = f"Line {line_num}: {line}"
            else:
                numbered_line = f"Line {line_num}: {line}\n"
            
            numbered_lines.append(numbered_line)
            
            # 진행 상황 표시 (10줄마다)
            if line_num % 10 == 0 or line_num == len(lines):
                print(f"   처리 중... {line_num}/{len(lines)} 라인")
        
        # 새 파일에 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(numbered_lines)
        
        return len(lines)
        
    except Exception as e:
        print(f"❌ 라인 번호 추가 중 오류: {e}")
        return 0


def validate_output(output_path: str) -> bool:
    """출력 파일 유효성 검증"""
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 모든 라인이 "Line X: "로 시작하는지 확인
        for line_num, line in enumerate(lines, start=1):
            expected_prefix = f"Line {line_num}: "
            if not line.startswith(expected_prefix):
                print(f"❌ 검증 실패: Line {line_num}이 올바른 형식이 아님")
                return False
        
        print(f"📊 검증 결과: {len(lines)}개 라인 모두 올바른 형식")
        return True
        
    except Exception as e:
        print(f"❌ 출력 파일 검증 중 오류: {e}")
        return False


if __name__ == "__main__":
    main()