#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 09:51:30 KST
핵심 내용: Part 2, Part 3 리프 노드 내용 추출 (Part 1과 동일한 방식)
상세 내용:
  - extract_content_for_part: 파트별 리프 노드 내용 추출
  - 원본 MD 파일에서 직접 텍스트 추출
  - Part 1과 동일한 알고리즘 사용
상태: 활성
주소: extract_parts_23_content
참조: part2_scalability_with_boundaries_fixed.json, part3_maintainability_with_boundaries_fixed.json
"""

import json
import os
import re
from datetime import datetime

def extract_content_for_part(part_num, part_title, boundaries_file):
    """파트별 리프 노드 내용 추출"""
    base_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09'
    
    # 원본 MD 파일 경로 
    md_file_map = {
        2: '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_02_Part_2_Scalability.md',
        3: '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_03_Part_3_Maintainability.md'
    }
    
    md_file = md_file_map[part_num]
    output_dir = os.path.join(base_dir, f'part{part_num}_{part_title.lower()}_leaf_nodes')
    
    # 출력 폴더 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 로드
    with open(boundaries_file, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    def find_text_position(search_text):
        """텍스트의 시작 위치 찾기 (Part 1과 동일한 알고리즘)"""
        if not search_text:
            return -1
        
        # 멀티라인 텍스트의 경우 첫 번째 라인만 사용
        search_first_line = search_text.split('\n')[0].strip()
        
        # 정확한 매치부터 시도
        if search_first_line in md_content:
            return md_content.find(search_first_line)
        
        return -1
    
    def extract_node_content(start_text, end_text):
        """노드 내용 추출 (Part 1과 동일한 알고리즘)"""
        start_pos = find_text_position(start_text)
        if start_pos == -1:
            return f"<!-- 시작 텍스트를 찾을 수 없음: {start_text} -->\n"
        
        # 끝 위치 찾기
        end_pos = len(md_content)
        if end_text:
            end_text_pos = find_text_position(end_text)
            if end_text_pos != -1 and end_text_pos > start_pos:
                end_pos = end_text_pos
        
        # 내용 추출
        content = md_content[start_pos:end_pos].strip()
        return content
    
    # 각 노드 처리
    success_count = 0
    failed_count = 0
    
    print(f"\n🔄 Part {part_num} ({part_title.title()}) 내용 추출 시작...")
    print(f"📂 출력 폴더: {output_dir}")
    print(f"📄 총 {len(nodes)}개 리프 노드 처리")
    
    for node in nodes:
        try:
            # 내용 추출
            content = extract_node_content(node['start_text'], node['end_text'])
            
            # 파일명 생성 (안전한 파일명으로 변환)
            safe_title = re.sub(r'[^\w\s-]', '', node['title'])
            safe_title = re.sub(r'\s+', '_', safe_title.strip())
            filename = f"{node['id']:03d}_{safe_title}.md"
            
            # MD 파일 내용 생성
            md_file_content = f"""# {node['title']}

**ID**: {node['id']}  
**Level**: {node['level']}  
**추출 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')}

---

{content}
"""
            
            # 파일 저장
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_file_content)
            
            print(f"✓ {node['id']:03d}: {node['title']} → {filename}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ {node['id']:03d}: {node['title']} → ERROR: {e}")
            failed_count += 1
    
    print(f"\n✅ Part {part_num} 완료!")
    print(f"   성공: {success_count}개")
    print(f"   실패: {failed_count}개")
    print(f"   📂 저장 위치: {output_dir}")
    
    return output_dir

def main():
    """메인 실행 함수"""
    print("🚀 Part 2, Part 3 리프 노드 내용 추출 시작...")
    
    # 처리할 파트들
    parts = [
        (2, "scalability", "part2_scalability_with_boundaries_fixed.json"),
        (3, "maintainability", "part3_maintainability_with_boundaries_fixed.json")
    ]
    
    for part_num, part_title, boundaries_file in parts:
        try:
            boundaries_path = f'/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/{boundaries_file}'
            extract_content_for_part(part_num, part_title, boundaries_path)
            
        except Exception as e:
            print(f"❌ Part {part_num} 처리 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 모든 파트 리프 노드 내용 추출 완료!")

if __name__ == "__main__":
    main()