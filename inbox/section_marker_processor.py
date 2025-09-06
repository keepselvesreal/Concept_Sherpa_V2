#!/usr/bin/env python3
"""
OpenAI 문서 스타일 섹션 마커 프로세서
OpenAI 문서 형식을 기반으로 JSON 구조화된 데이터에 섹션 시작/종료 마커를 추가합니다.
"""
import json
import re
from pathlib import Path

def extract_content_from_md(md_file_path):
    """마크다운 파일에서 구조화된 콘텐츠를 추출합니다."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 페이지 마커로 섹션 추출
    sections = {}
    page_pattern = r'=== 페이지 (\d+) ===\n(.*?)(?==== 페이지 \d+ ===|$)'
    pages = re.findall(page_pattern, content, re.DOTALL)
    
    current_section = None
    current_content = []
    
    for page_num, page_content in pages:
        lines = page_content.strip().split('\n')
        for line in lines:
            # 메인 섹션 헤더 확인 (7.1, 7.2 등의 번호)
            if re.match(r'^\d+\.\d+\s+', line):
                # 이전 섹션 저장
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                # 새 섹션 시작
                current_section = line.strip()
                current_content = [line]
            elif current_section:
                current_content.append(line)
    
    # 마지막 섹션 저장
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def create_section_markers(title, content):
    """콘텐츠에 대한 OpenAI 스타일 섹션 마커를 생성합니다."""
    # 일관된 형식을 위해 제목 정리
    clean_title = title.replace('_', ' ').strip()
    
    # OpenAI 문서와 유사한 섹션 마커 생성
    start_marker = f"## {clean_title}\n"
    end_marker = f"\n---\n"
    
    # 적절한 구조로 콘텐츠 형식화
    formatted_content = f"{start_marker}{content}{end_marker}"
    
    return {
        "start_marker": start_marker,
        "end_marker": end_marker,
        "formatted_content": formatted_content
    }

def process_json_with_markers(json_file_path, md_file_path, output_file_path):
    """MD 콘텐츠를 기반으로 섹션 마커를 추가하여 JSON 파일을 처리합니다."""
    
    # 기존 JSON 구조 로드
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # 마크다운에서 콘텐츠 추출
    md_sections = extract_content_from_md(md_file_path)
    
    # JSON의 각 항목 처리
    enhanced_data = []
    
    for item in json_data:
        enhanced_item = item.copy()
        title = item.get('title', '')
        
        # 마크다운 콘텐츠와 제목 매칭 시도
        matching_content = None
        for section_key, section_content in md_sections.items():
            # 단순 매칭 - 더 정교하게 만들 수 있음
            if title.replace('_', ' ').lower() in section_key.lower():
                matching_content = section_content
                break
        
        if matching_content:
            # 섹션 마커 생성
            markers = create_section_markers(title, matching_content)
            
            # 항목에 마커 추가
            enhanced_item['start_text'] = markers['start_marker']
            enhanced_item['end_text'] = markers['end_marker']
            enhanced_item['content'] = matching_content
            enhanced_item['formatted_section'] = markers['formatted_content']
        else:
            # 매칭되는 콘텐츠가 없는 항목에 기본 마커 추가
            default_markers = create_section_markers(title, f"{title}에 대한 콘텐츠")
            enhanced_item['start_text'] = default_markers['start_marker']
            enhanced_item['end_text'] = default_markers['end_marker']
            enhanced_item['content'] = f"{title}에 대한 콘텐츠"
            enhanced_item['formatted_section'] = default_markers['formatted_content']
        
        enhanced_data.append(enhanced_item)
    
    # 향상된 데이터 저장
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"향상된 JSON이 다음 위치에 저장되었습니다: {output_file_path}")
    return enhanced_data

def main():
    """파일을 처리하는 메인 함수입니다."""
    base_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2")
    
    # 입력 파일들
    json_file = base_dir / "25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    md_file = base_dir / "25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    
    # 출력 파일
    output_dir = base_dir / "25-08-10"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "enhanced_chapter07_with_markers.json"
    
    # 파일 처리
    try:
        enhanced_data = process_json_with_markers(json_file, md_file, output_file)
        
        print(f"{len(enhanced_data)}개 섹션을 성공적으로 처리했습니다")
        print(f"출력이 다음 위치에 저장되었습니다: {output_file}")
        
        # 향상된 데이터 샘플 표시
        if enhanced_data:
            print("\n향상된 섹션 샘플:")
            print("=" * 50)
            sample = enhanced_data[0]
            print(f"제목: {sample.get('title')}")
            print(f"시작 마커: {repr(sample.get('start_text'))}")
            print(f"종료 마커: {repr(sample.get('end_text'))}")
            if 'formatted_section' in sample:
                print(f"형식화된 섹션 미리보기: {sample['formatted_section'][:200]}...")
    
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    main()