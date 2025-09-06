#!/usr/bin/env python3
"""
모든 추출된 내용을 해당 TOC_Structure 파일들에 저장
"""

import json
from pathlib import Path

def save_all_content():
    json_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extracted_content.json"
    base_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    # JSON 로드
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 완전한 매핑 (모든 13개 섹션)
    file_mappings = {
        # 6.2 섹션들
        "6.2.1 The tree of function calls": f"{base_path}/node0/node1/node2/Part1/node3/ch6/node4/6.2.1 The tree of function calls [CONTENT].md",
        "6.2.2 Unit tests for functions down the tree": f"{base_path}/node0/node1/node2/Part1/node3/ch6/node4/6.2.2 Unit tests for functions down the tree [CONTENT].md",
        "6.2.3 Unit tests for nodes in the tree": f"{base_path}/node0/node1/node2/Part1/node3/ch6/node4/6.2.3 Unit tests for nodes in the tree [CONTENT].md",
        
        # 1.1 섹션들
        "1.1.1 The design phase": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.1 The design phase [CONTENT].md",
        "1.1.2 UML 101": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.2 UML 101 [CONTENT].md",
        "1.1.3 Explaining each piece of the class diagram": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.3 Explaining each piece of the class diagram [CONTENT].md",
        "1.1.4 The implementation phase": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.4 The implementation phase [CONTENT].md",
        
        # 1.2 섹션들
        "1.2.1 Many relations between classes": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.1 Many relations between classes [CONTENT].md",
        "1.2.2 Unpredictable code behavior": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.2 Unpredictable code behavior [CONTENT].md",
        "1.2.3 Not trivial data serialization": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.3 Not trivial data serialization [CONTENT].md",
        "1.2.4 Complex class hierarchies": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.4 Complex class hierarchies [CONTENT].md",
        
        # 기타 섹션들 (첫 번째 매칭되는 Summary와 Introduction 사용)
        "Summary": f"{base_path}/node0/node1/node2/Part3/Summary [CONTENT].md",
        "Introduction": f"{base_path}/node0/node1/node2/Part3/A.0 Introduction (사용자 추가) [CONTENT].md"
    }
    
    sections = data["sections"]
    saved_count = 0
    failed_sections = []
    
    print(f"총 {len(sections)}개 섹션을 저장 중...")
    
    for section_title, file_path in file_mappings.items():
        if section_title in sections:
            section_data = sections[section_title]
            content = section_data["content"]
            
            try:
                # 파일 경로가 존재하는지 확인
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    print(f"⚠️  파일이 존재하지 않음: {file_path_obj.name}")
                    failed_sections.append(section_title)
                    continue
                
                # 파일에 저장
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {section_title}\n\n")
                    f.write("## 추출된 내용\n\n")
                    f.write(content)
                    f.write(f"\n\n---\n\n")
                    f.write(f"**추출 완료**: {section_data['length']} 문자\n")
                    f.write(f"**추출 시간**: {section_data['extracted_at']}\n")
                    f.write(f"**파일 경로**: {file_path_obj.name}\n")
                
                print(f"✅ 저장 성공: {section_title} ({section_data['length']} 문자)")
                saved_count += 1
                
            except Exception as e:
                print(f"❌ 저장 실패 {section_title}: {e}")
                failed_sections.append(section_title)
        else:
            print(f"❌ 섹션 데이터 없음: {section_title}")
            failed_sections.append(section_title)
    
    print(f"\n=== 저장 완료 ===")
    print(f"총 섹션: {len(file_mappings)}")
    print(f"저장 성공: {saved_count}")
    print(f"실패: {len(failed_sections)}")
    
    if failed_sections:
        print(f"\n실패한 섹션들:")
        for section in failed_sections:
            print(f"  - {section}")
    
    # 저장된 파일들 확인
    print(f"\n저장된 파일 샘플:")
    sample_files = list(file_mappings.values())[:3]
    for file_path in sample_files:
        if Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            print(f"  - {Path(file_path).name}: {file_size} 바이트")

if __name__ == "__main__":
    save_all_content()