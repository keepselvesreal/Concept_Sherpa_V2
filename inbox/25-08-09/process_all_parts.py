#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:49:54 KST
핵심 내용: Part 2, Part 3의 텍스트 경계 추출 및 리프 노드 MD 파일 생성
상세 내용:
  - create_boundaries_for_part (라인 21-110): 파트별 텍스트 경계 생성
  - extract_part_content (라인 112-170): 파트별 리프 노드 내용 추출
  - process_part (라인 172-190): 전체 파트 처리
  - main (라인 192-225): 메인 실행 함수
상태: 활성
주소: process_all_parts
참조: Part 2, Part 3 MD 및 JSON 파일들
"""

import json
import os
import re
from datetime import datetime

def create_boundaries_for_part(part_num, part_title):
    """파트별 텍스트 경계 생성"""
    base_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09'
    
    # 파일 경로
    leaf_file = f'part{part_num}_{part_title.lower()}_leaf_nodes.json'
    md_file = f'/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_0{part_num}_Part_{part_num}_{part_title.title()}.md'
    output_file = f'part{part_num}_{part_title.lower()}_with_boundaries.json'
    
    # JSON 로드
    with open(os.path.join(base_dir, leaf_file), 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    # MD 파일 읽기
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 섹션 제목들 추출 (숫자로 시작하는 제목들)
    lines = md_content.split('\n')
    section_titles = []
    
    for line in lines:
        line = line.strip()
        # 주요 섹션 제목 패턴 매칭
        if (re.match(r'^\d+(?:\.\d+)* ', line) or 
            line.startswith('Part ') or
            line in ['Summary', 'Moving forward', 'Farewell', 'Delivering on time', 'Conclusion']):
            section_titles.append(line)
    
    print(f"Part {part_num} - 발견된 섹션 제목들:")
    for title in section_titles[:10]:  # 처음 10개만 출력
        print(f"  - {title}")
    if len(section_titles) > 10:
        print(f"  ... 총 {len(section_titles)}개 섹션")
    
    # 각 리프 노드에 대해 경계 설정
    updated_nodes = []
    
    for i, node in enumerate(leaf_nodes):
        title = node['title']
        
        # 시작 텍스트 찾기
        start_text = ""
        end_text = ""
        
        if "Introduction" in title and "Part" in title:
            start_text = f"Part {part_num}"
            # 다음 주요 섹션 찾기
            next_major = None
            for sect in section_titles:
                if re.match(r'^\d+ ', sect):
                    next_major = sect
                    break
            end_text = next_major if next_major else ""
            
        elif title.endswith("Introduction") and not "Part" in title:
            # 챕터 Introduction
            chapter_num = title.split()[0]
            start_text = next((s for s in section_titles if s.startswith(chapter_num + " ")), title)
            # 다음 섹션 찾기
            chapter_prefix = chapter_num + "."
            end_text = next((s for s in section_titles if s.startswith(chapter_prefix)), "")
            
        elif re.match(r'^\d+(\.\d+)* ', title):
            # 번호가 있는 섹션
            start_text = title
            # 다음 섹션 찾기
            current_idx = -1
            for j, sect in enumerate(section_titles):
                if title in sect or sect in title:
                    current_idx = j
                    break
            
            if current_idx >= 0 and current_idx < len(section_titles) - 1:
                end_text = section_titles[current_idx + 1]
            else:
                end_text = ""
                
        elif title == "Summary":
            start_text = "Summary"
            # 다음 주요 섹션 찾기
            next_chapter = None
            for sect in section_titles:
                if re.match(r'^\d+ ', sect) and not sect.startswith(str(part_num)):
                    next_chapter = sect
                    break
            end_text = next_chapter if next_chapter else ""
            
        else:
            # 기타 섹션
            start_text = title
            end_text = ""
        
        updated_node = node.copy()
        updated_node['start_text'] = start_text
        updated_node['end_text'] = end_text
        updated_nodes.append(updated_node)
    
    # 결과 저장
    output_path = os.path.join(base_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Part {part_num} 텍스트 경계 생성 완료: {output_file}")
    return output_path

def extract_part_content(part_num, part_title, boundaries_file):
    """파트별 리프 노드 내용 추출"""
    base_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09'
    
    # 파일 경로
    md_file = f'/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_0{part_num}_Part_{part_num}_{part_title.title()}.md'
    output_dir = os.path.join(base_dir, f'part{part_num}_{part_title.lower()}_leaf_nodes')
    
    # 출력 폴더 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 로드
    with open(boundaries_file, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    lines = md_content.split('\n')
    
    def find_text_position(search_text):
        """텍스트 위치 찾기"""
        if not search_text:
            return -1
        
        search_first_line = search_text.split('\n')[0].strip()
        for i, line in enumerate(lines):
            if search_first_line in line.strip():
                return i
        return -1
    
    def extract_node_content(start_text, end_text):
        """노드 내용 추출"""
        start_pos = find_text_position(start_text)
        if start_pos == -1:
            return f"<!-- 시작 텍스트를 찾을 수 없음: {start_text} -->\n"
        
        end_pos = len(lines)
        if end_text:
            end_pos = find_text_position(end_text)
            if end_pos == -1:
                end_pos = len(lines)
        
        if start_pos < end_pos:
            content_lines = lines[start_pos:end_pos]
            return '\n'.join(content_lines)
        else:
            return f"<!-- 내용 추출 실패: start_pos={start_pos}, end_pos={end_pos} -->\n"
    
    # 각 노드 처리
    success_count = 0
    for node in nodes:
        try:
            # 내용 추출
            content = extract_node_content(node['start_text'], node['end_text'])
            
            # 파일명 생성
            safe_title = re.sub(r'[^\w\s-]', '', node['title'])
            safe_title = re.sub(r'\s+', '_', safe_title.strip())
            filename = f"{node['id']:03d}_{safe_title}.md"
            
            # MD 파일 내용 생성
            md_content = f"""# {node['title']}

**ID**: {node['id']}  
**Level**: {node['level']}  
**추출 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')}

---

{content}
"""
            
            # 파일 저장
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"✓ {node['id']:03d}: {node['title']} → {filename}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ {node['id']:03d}: {node['title']} → ERROR: {e}")
    
    print(f"Part {part_num} 완료: {success_count}/{len(nodes)} 파일 생성")
    return output_dir

def process_part(part_num, part_title):
    """단일 파트 전체 처리"""
    print(f"\n🔄 Part {part_num} - {part_title.title()} 처리 시작...")
    
    # 1. 텍스트 경계 생성
    boundaries_file = create_boundaries_for_part(part_num, part_title)
    
    # 2. 리프 노드 내용 추출
    output_dir = extract_part_content(part_num, part_title, boundaries_file)
    
    print(f"✅ Part {part_num} 완료! 📂 {output_dir}")

def main():
    """메인 실행 함수"""
    print("🚀 Part 2, Part 3 처리 시작...")
    
    parts = [
        (2, "scalability"),
        (3, "maintainability")
    ]
    
    for part_num, part_title in parts:
        try:
            process_part(part_num, part_title)
        except Exception as e:
            print(f"❌ Part {part_num} 처리 중 오류 발생: {e}")
    
    print("\n🎉 모든 파트 처리 완료!")

if __name__ == "__main__":
    main()