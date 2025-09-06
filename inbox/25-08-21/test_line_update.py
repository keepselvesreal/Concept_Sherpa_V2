"""
라인 번호 업데이트 테스트 스크립트
"""

import re

def update_actual_line_numbers(file_path: str) -> None:
    """
    구조화된 파일에서 타임스탬프 라인 앞에 "Line X:" 정보를 추가합니다.
    
    Args:
        file_path (str): 구조화된 파일 경로
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        updated_lines = []
        for line_num, line in enumerate(lines, start=1):
            # 타임스탬프로 시작하는 라인 ([MM:SS])을 찾아서 Line 정보 추가
            if re.search(r'^\[\d{2}:\d{2}\]', line.strip()):
                updated_line = f"Line {line_num}: {line}"
                updated_lines.append(updated_line)
                print(f"업데이트: Line {line_num} - {line.strip()[:50]}...")
            else:
                updated_lines.append(line)
        
        # 파일에 다시 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
            
        print("✅ 실제 IDE 라인 번호로 업데이트 완료")
        
    except Exception as e:
        print(f"❌ 라인 번호 업데이트 중 오류: {str(e)}")

if __name__ == "__main__":
    # 기존 구조화된 파일로 테스트
    file_path = "Engineers… Claude Code Output Styles Are Here. Don_mJhsWrEv-Go_structured.md"
    print("🔍 라인 번호 업데이트 테스트 시작...")
    update_actual_line_numbers(file_path)