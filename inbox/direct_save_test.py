#!/usr/bin/env python3
"""
직접 파일 매핑하여 저장 테스트
"""

import json
from pathlib import Path

def direct_save_test():
    json_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extracted_content.json"
    
    # JSON 로드
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 직접 매핑 (정확한 파일 경로)
    file_mappings = {
        "6.2.1 The tree of function calls": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part1/node3/ch6/node4/6.2.1 The tree of function calls [CONTENT].md",
        "6.2.2 Unit tests for functions down the tree": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part1/node3/ch6/node4/6.2.2 Unit tests for functions down the tree [CONTENT].md",
        "6.2.3 Unit tests for nodes in the tree": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part1/node3/ch6/node4/6.2.3 Unit tests for nodes in the tree [CONTENT].md",
        "1.1.1 The design phase": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part1/node3/ch1/node4/1.1.1 The design phase [CONTENT].md",
        "1.1.2 UML 101": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part1/node3/ch1/node4/1.1.2 UML 101 [CONTENT].md",
        "1.2.1 Many relations between classes": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part1/node3/ch1/node4/1.2.1 Many relations between classes [CONTENT].md",
        "Summary": "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure/node0/node1/node2/Part3/Summary [CONTENT].md"
    }
    
    sections = data["sections"]
    saved_count = 0
    
    print("직접 매핑으로 파일 저장 테스트...")
    
    for section_title, file_path in file_mappings.items():
        if section_title in sections:
            section_data = sections[section_title]
            content = section_data["content"]
            
            try:
                # 파일에 저장
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {section_title}\n\n")
                    f.write("## 추출된 내용\n\n")
                    f.write(content)
                    f.write(f"\n\n---\n\n")
                    f.write(f"**추출 완료**: {section_data['length']} 문자\n")
                    f.write(f"**추출 시간**: {section_data['extracted_at']}\n")
                
                print(f"✅ 저장 성공: {section_title}")
                saved_count += 1
                
            except Exception as e:
                print(f"❌ 저장 실패 {section_title}: {e}")
        else:
            print(f"❌ 섹션 없음: {section_title}")
    
    print(f"\n저장 완료: {len(file_mappings)}개 중 {saved_count}개 성공")

if __name__ == "__main__":
    direct_save_test()