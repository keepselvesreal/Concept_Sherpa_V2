# 생성 시간: 2025-09-01 11:17:52 KST
# 핵심 내용: 특정 폴더 내 모든 .md 파일에서 '# 추출' 섹션 밑 내용을 수집하여 하나의 문서로 결합하는 스크립트
# 상세 내용:
#   - extract_title_from_filename (line 15): 파일명에서 title 추출 (숫자+레벨 정보 제거)
#   - find_min_lev_title (line 22): lev 값이 가장 작은 파일의 title 반환  
#   - extract_section_content (line 35): '# 추출' 섹션 밑 내용 추출
#   - combine_extracts (line 61): 모든 파일의 추출 내용을 결합하여 최종 문서 생성
#   - main (line 87): 스크립트 메인 실행 함수
# 상태: active
# 주소: extract_sections
# 참조: 

import os
import re
import sys
from pathlib import Path

def extract_title_from_filename(filename):
    """파일명에서 title 추출 (lev{n} 뒤 모든 내용 포함)"""
    # 예: 21_lev2_1.2_Sources_of_complexity_info.md -> 1.2_Sources_of_complexity
    pattern = r'^\d+_lev\d+_(.+)_info\.md$'
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    return filename.replace('.md', '')

def find_min_lev_title(folder_path):
    """lev 값이 가장 작은 파일의 title 반환"""
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    min_lev = float('inf')
    min_lev_title = None
    
    for filename in md_files:
        lev_match = re.search(r'_lev(\d+)_', filename)
        if lev_match:
            lev_num = int(lev_match.group(1))
            if lev_num < min_lev:
                min_lev = lev_num
                min_lev_title = extract_title_from_filename(filename)
    
    return min_lev_title or "combined"

def extract_section_content(file_path):
    """# 추출 섹션 밑 내용 추출"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # # 추출 섹션 찾기
        extract_pattern = r'# 추출\s*\n(.*?)(?=\n#[^#]|\Z)'
        match = re.search(extract_pattern, content, re.DOTALL)
        
        if match:
            extracted_content = match.group(1).strip()
            # 첫 번째 --- 라인 제거 (있다면)
            if extracted_content.startswith('---'):
                lines = extracted_content.split('\n')
                if lines[0].strip() == '---':
                    extracted_content = '\n'.join(lines[1:]).strip()
            return extracted_content
        return ""
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def combine_extracts(folder_path):
    """모든 파일의 추출 내용을 결합하여 최종 문서 생성"""
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    
    # 파일명의 숫자 순서로 정렬
    def sort_key(filename):
        match = re.match(r'^(\d+)_', filename)
        return int(match.group(1)) if match else float('inf')
    
    md_files.sort(key=sort_key)
    
    combined_content = []
    
    for filename in md_files:
        file_path = os.path.join(folder_path, filename)
        title = extract_title_from_filename(filename)
        extracted_content = extract_section_content(file_path)
        
        if extracted_content:
            combined_content.append(f"# {title}")
            combined_content.append("")
            combined_content.append(extracted_content)
            combined_content.append("")
    
    return '\n'.join(combined_content)

def main():
    """메인 실행 함수"""
    if len(sys.argv) != 2:
        print("사용법: python extract_sections.py <폴더경로>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.exists(folder_path):
        print(f"폴더가 존재하지 않습니다: {folder_path}")
        sys.exit(1)
    
    # lev가 가장 작은 파일의 title로 결과 파일명 생성
    base_title = find_min_lev_title(folder_path)
    output_filename = f"enhanced_{base_title}_toc.md"
    output_path = os.path.join(folder_path, output_filename)
    
    # 내용 결합
    combined_content = combine_extracts(folder_path)
    
    if not combined_content.strip():
        print("추출할 내용이 없습니다.")
        sys.exit(1)
    
    # 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print(f"결과 파일이 생성되었습니다: {output_path}")

if __name__ == "__main__":
    main()