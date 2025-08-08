# 목차
# - 생성 시간: 2025-08-07 12:30:15 KST
# - 핵심 내용: Part 1에서 Chapter 1 부분만 추출하여 별도 파일로 저장하는 도구
# - 상세 내용:
#     - extract_chapter1_content(1-45): Part 1에서 페이지 31-53 부분을 추출하는 함수
#     - save_chapter1_file(47-65): Chapter 1 내용을 별도 파일로 저장하는 함수
#     - main(67-80): 전체 프로세스 실행 함수
# - 상태: 활성
# - 주소: extract_chapter1
# - 참조: Part_01_Part_1_Flexibility.md, core_toc_with_page_ranges.json

import os
import re
from datetime import datetime

def extract_chapter1_content(part1_file_path: str):
    """Part 1에서 Chapter 1 부분만 추출"""
    
    try:
        with open(part1_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Part 1 로드: {len(content):,} 문자")
        
        # Chapter 1 시작 지점 찾기 (페이지 31)
        chapter1_start = None
        chapter2_start = None
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # "## 페이지 31" 패턴 찾기
            if '## 페이지 31' in line:
                chapter1_start = i
                print(f"📍 Chapter 1 시작 발견: 라인 {i}")
                
            # "## 페이지 54" 패턴 찾기 (Chapter 2 시작)
            elif '## 페이지 54' in line:
                chapter2_start = i
                print(f"📍 Chapter 2 시작 발견: 라인 {i}")
                break
        
        if chapter1_start is None:
            print("❌ Chapter 1 시작점을 찾을 수 없습니다.")
            return None
            
        # Chapter 1 내용 추출
        if chapter2_start:
            chapter1_lines = lines[chapter1_start:chapter2_start]
        else:
            # Chapter 2를 못 찾으면 끝까지
            chapter1_lines = lines[chapter1_start:]
        
        chapter1_content = '\n'.join(chapter1_lines)
        
        print(f"✅ Chapter 1 추출 완료: {len(chapter1_content):,} 문자")
        print(f"📄 페이지 범위: 31-53 (예상)")
        
        return chapter1_content
        
    except Exception as e:
        print(f"❌ 추출 실패: {e}")
        return None

def save_chapter1_file(chapter1_content: str, output_path: str):
    """Chapter 1 내용을 별도 파일로 저장"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')
    
    file_content = f"""# 목차
# - 생성 시간: {timestamp}
# - 핵심 내용: Part 1에서 추출한 Chapter 1 전체 내용 (페이지 31-53)
# - 상세 내용: Claude 목차 분석 테스트용 Chapter 1 독립 파일
# - 상태: 활성
# - 주소: chapter1_extracted
# - 참조: Part_01_Part_1_Flexibility.md

# Chapter 1: Complexity of object-oriented programming

{chapter1_content}
"""
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        print(f"✅ Chapter 1 파일 저장: {output_path}")
        print(f"📊 파일 크기: {len(file_content):,} 문자")
        
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")

def main():
    print("🚀 Chapter 1 추출 작업 시작...")
    
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07"
    part1_file = os.path.join(base_dir, "extracted_parts", "Part_01_Part_1_Flexibility.md")
    output_file = os.path.join(base_dir, "chapter1_extracted.md")
    
    # Chapter 1 추출
    chapter1_content = extract_chapter1_content(part1_file)
    
    if chapter1_content:
        # 파일 저장
        save_chapter1_file(chapter1_content, output_file)
        print(f"\n🎉 Chapter 1 추출 완료!")
        print(f"📁 출력 파일: {output_file}")
    else:
        print("\n❌ Chapter 1 추출 실패")

if __name__ == "__main__":
    main()