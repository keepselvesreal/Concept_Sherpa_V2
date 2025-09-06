# 생성 시간: 2025-08-29 09:40:03 KST
# 핵심 내용: 부모 노드와 자식 노드들의 결합된 content 내용 확인
# 상세 내용:
#   - 부모 노드의 "# 내용" 섹션 읽기
#   - 자식 노드들의 "# 내용" 섹션 읽기 
#   - 결합된 content 생성 및 저장
# 상태: active
# 주소: simple_content_test
# 참조: unified_node_processor.py의 get_combined_content 메서드

from pathlib import Path

def read_content_section(file_path):
    """노드 문서의 내용 섹션 읽기"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # "# 내용" 섹션 추출
        content_start = content.find('\n# 내용\n---\n')
        if content_start == -1:
            return ""
        
        content_start += len('\n# 내용\n---\n')
        
        # 다음 섹션(구성) 시작점 찾기
        next_section = content.find('\n# 구성\n---', content_start)
        if next_section == -1:
            return content[content_start:].strip()
        else:
            return content[content_start:next_section].strip()
            
    except Exception as e:
        print(f"내용 섹션 읽기 실패: {file_path} - {e}")
        return ""

def main():
    """부모 노드와 자식 노드들의 결합된 content 생성"""
    
    # 부모 노드 경로
    parent_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/00_lev1_7_Basic_data_validation_info.md"
    
    # 자식 노드 경로들 (올바른 순서로 모든 구성 요소 포함)
    child_paths = [
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/01_lev2_7.1_Data_validation_in_DOP_info.md",
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/02_lev2_7.2_JSON_Schema_in_a_nutshell_info.md",
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/03_lev2_7.3_Schema_flexibility_and_strictness_info.md",
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/04_lev2_7.4_Schema_composition_info.md",
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/05_lev2_7.5_Details_about_data_validation_failures_info.md",
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-28/process/node_docs_backup/06_lev2_Summary_info.md"
    ]
    
    # 부모 노드 내용 읽기
    parent_content = read_content_section(parent_path)
    print(f"부모 노드 내용 길이: {len(parent_content)} 글자")
    
    # 결합된 내용 시작 (부모 노드 내용)
    combined_content = parent_content
    
    # 자식 노드들의 내용 추가
    for i, child_path in enumerate(child_paths, 1):
        child_content = read_content_section(child_path)
        if child_content:
            combined_content += f"\n\n=== 구성 노드 {i} ===\n{child_content}"
            print(f"자식 노드 {i} 내용 길이: {len(child_content)} 글자")
    
    # 결과 저장
    output_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29/complete_combined_content_result.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print(f"\n전체 결합된 content 길이: {len(combined_content)} 글자")
    print(f"결과 저장: {output_path}")
    print(f"총 구성 요소: 부모 노드 1개 + 자식 노드 {len(child_paths)}개")
    
    # 미리보기
    print(f"\n=== Combined Content 미리보기 (처음 800자) ===")
    print(combined_content[:800] + "..." if len(combined_content) > 800 else combined_content)

if __name__ == "__main__":
    main()