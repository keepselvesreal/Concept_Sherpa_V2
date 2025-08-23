#!/usr/bin/env python3
"""
결과 검증 및 완성도 확인
"""

import json
from pathlib import Path

def verify_saved_content():
    json_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extracted_content.json"
    base_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    # JSON 로드
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 저장된 파일 매핑
    file_mappings = {
        "6.2.1 The tree of function calls": f"{base_path}/node0/node1/node2/Part1/node3/ch6/node4/6.2.1 The tree of function calls [CONTENT].md",
        "6.2.2 Unit tests for functions down the tree": f"{base_path}/node0/node1/node2/Part1/node3/ch6/node4/6.2.2 Unit tests for functions down the tree [CONTENT].md",
        "6.2.3 Unit tests for nodes in the tree": f"{base_path}/node0/node1/node2/Part1/node3/ch6/node4/6.2.3 Unit tests for nodes in the tree [CONTENT].md",
        "1.1.1 The design phase": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.1 The design phase [CONTENT].md",
        "1.1.2 UML 101": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.2 UML 101 [CONTENT].md",
        "1.1.3 Explaining each piece of the class diagram": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.3 Explaining each piece of the class diagram [CONTENT].md",
        "1.1.4 The implementation phase": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.1.4 The implementation phase [CONTENT].md",
        "1.2.1 Many relations between classes": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.1 Many relations between classes [CONTENT].md",
        "1.2.2 Unpredictable code behavior": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.2 Unpredictable code behavior [CONTENT].md",
        "1.2.3 Not trivial data serialization": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.3 Not trivial data serialization [CONTENT].md",
        "1.2.4 Complex class hierarchies": f"{base_path}/node0/node1/node2/Part1/node3/ch1/node4/1.2.4 Complex class hierarchies [CONTENT].md",
        "Summary": f"{base_path}/node0/node1/node2/Part3/Summary [CONTENT].md",
        "Introduction": f"{base_path}/node0/node1/node2/Part3/A.0 Introduction (사용자 추가) [CONTENT].md"
    }
    
    print("=== 저장된 내용 검증 ===")
    
    sections = data["sections"]
    verified_count = 0
    total_characters = 0
    
    for section_title, file_path in file_mappings.items():
        file_path_obj = Path(file_path)
        
        if file_path_obj.exists():
            file_size = file_path_obj.stat().st_size
            original_length = sections[section_title]["length"]
            
            # 파일 내용 읽기
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # 검증
            has_title = section_title in file_content
            has_content = "추출된 내용" in file_content
            has_metadata = "추출 완료" in file_content
            
            status = "✅" if (has_title and has_content and has_metadata) else "⚠️"
            
            print(f"{status} {section_title}")
            print(f"    파일 크기: {file_size} 바이트")
            print(f"    원본 길이: {original_length} 문자")
            print(f"    구성 요소: 제목({has_title}), 내용({has_content}), 메타데이터({has_metadata})")
            
            if has_title and has_content and has_metadata:
                verified_count += 1
                total_characters += original_length
            
            print()
        else:
            print(f"❌ 파일 없음: {section_title}")
            print(f"    경로: {file_path}")
            print()
    
    print(f"=== 검증 결과 요약 ===")
    print(f"총 섹션: {len(file_mappings)}")
    print(f"검증 성공: {verified_count}")
    print(f"총 추출 문자 수: {total_characters:,}")
    print(f"완성도: {verified_count/len(file_mappings)*100:.1f}%")
    
    # 추가 통계
    if verified_count > 0:
        avg_length = total_characters // verified_count
        print(f"평균 섹션 길이: {avg_length} 문자")
    
    # 샘플 파일 내용 미리보기
    print(f"\n=== 샘플 파일 내용 미리보기 ===")
    sample_file = file_mappings["6.2.1 The tree of function calls"]
    if Path(sample_file).exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        preview = content[:300] + "..." if len(content) > 300 else content
        print(f"[6.2.1 The tree of function calls]")
        print(preview)
    
    return verified_count == len(file_mappings)

if __name__ == "__main__":
    success = verify_saved_content()
    if success:
        print(f"\n🎉 모든 검증이 성공적으로 완료되었습니다!")
    else:
        print(f"\n⚠️ 일부 검증에 실패했습니다. 위의 내용을 확인하세요.")