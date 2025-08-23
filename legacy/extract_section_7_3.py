#!/usr/bin/env python3
"""
7.3 Schema flexibility and strictness 섹션 추출 스크립트
"""

def extract_section_7_3(file_path):
    """7.3 섹션만 정확히 추출"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 시작과 종료 마커 정의
    start_marker = "7.3 Schema flexibility and strictness"
    end_marker = "7.4 Schema composition"
    
    # 시작 위치 찾기
    start_pos = content.find(start_marker)
    if start_pos == -1:
        return None, "시작 마커를 찾을 수 없습니다"
    
    # 종료 위치 찾기 
    end_pos = content.find(end_marker, start_pos)
    if end_pos == -1:
        return None, "종료 마커를 찾을 수 없습니다"
    
    # 섹션 추출 (종료 마커 직전까지)
    section_text = content[start_pos:end_pos].strip()
    
    return section_text, "추출 성공"

def main():
    file_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    
    section_text, message = extract_section_7_3(file_path)
    
    if section_text:
        # 추출된 텍스트를 파일로 저장
        output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/section_7_3_extracted.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(section_text)
        
        print(f"✅ {message}")
        print(f"📁 저장 위치: {output_path}")
        print(f"📊 추출된 텍스트 길이: {len(section_text)} 문자")
        print("\n" + "="*50)
        print("추출된 섹션 미리보기:")
        print("="*50)
        print(section_text[:500] + "...")
    else:
        print(f"❌ 오류: {message}")

if __name__ == "__main__":
    main()