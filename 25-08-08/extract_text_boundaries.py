# 생성 시간: 2025-08-08 12:13:10 KST
# 핵심 내용: 리프 노드에 실제 텍스트 경계(start_text, end_text)를 추가하여 새로운 JSON 파일 생성
# 상세 내용:
#   - main() 함수 (라인 9-37): 메인 실행 로직, 파일 읽기 및 텍스트 경계 분석
#   - analyze_text_boundaries() 함수 (라인 39-145): 전체 텍스트에서 각 리프 노드의 경계 텍스트 추출
#   - find_text_boundary() 함수 (라인 147-174): 특정 제목의 실제 텍스트 위치 찾기
#   - normalize_for_search() 함수 (라인 176-181): 검색을 위한 텍스트 정규화
# 상태: 활성
# 주소: extract_text_boundaries
# 참조: leaf_nodes_only (리프 노드 JSON 파일)

import json
import re

def main():
    # 파일 경로 설정
    leaf_nodes_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/leaf_nodes_only.json'
    text_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md'
    output_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/leaf_nodes_with_text_boundaries.json'
    
    try:
        # 리프 노드 JSON 파일 읽기
        with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
            leaf_nodes = json.load(f)
        
        # 전체 텍스트 파일 읽기
        with open(text_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        print(f"리프 노드 개수: {len(leaf_nodes)}")
        print(f"전체 텍스트 길이: {len(full_text)} 문자")
        
        # 텍스트 경계 분석 및 추가
        nodes_with_boundaries = analyze_text_boundaries(leaf_nodes, full_text)
        
        # 결과를 새로운 JSON 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(nodes_with_boundaries, f, ensure_ascii=False, indent=2)
        
        print(f"텍스트 경계가 추가된 리프 노드가 {output_file}에 저장되었습니다.")
        
        # 처음 5개 노드의 경계 정보 출력
        print("\\n처음 5개 노드의 텍스트 경계:")
        for i, node in enumerate(nodes_with_boundaries[:5]):
            print(f"{i+1}. ID: {node['id']}, Title: {node['title']}")
            print(f"   Start: {node['start_text'][:100]}...")
            print(f"   End: {node['end_text'][:100]}...")
            
    except Exception as e:
        print(f"오류 발생: {e}")

def analyze_text_boundaries(leaf_nodes, full_text):
    """전체 텍스트에서 각 리프 노드의 start_text와 end_text 추출"""
    nodes_with_boundaries = []
    
    # Part 1 관련 리프 노드만 처리 (Part_01_Part_1_Flexibility.md는 Part 1만 포함)
    part1_nodes = [node for node in leaf_nodes if 
                   node['title'].startswith('Part 1') or 
                   node['title'].startswith('1') or
                   (node['title'] == 'Summary' and node['id'] <= 62)]
    
    print(f"Part 1 관련 리프 노드: {len(part1_nodes)}개")
    
    for i, node in enumerate(part1_nodes):
        new_node = {
            'id': node['id'],
            'title': node['title'],
            'level': node['level']
        }
        
        title = node['title']
        
        # start_text 찾기
        start_text = find_text_boundary(full_text, title, is_start=True)
        
        # end_text 찾기 (다음 노드의 제목)
        if i < len(part1_nodes) - 1:
            next_title = part1_nodes[i + 1]['title']
            end_text = find_text_boundary(full_text, next_title, is_start=True)
        else:
            # 마지막 노드의 경우 적절한 끝 지점 찾기
            if title == 'Summary':
                # Summary 다음에 오는 섹션 찾기
                end_patterns = ['Summary', '## 페이지', 'CHAPTER', 'Part 2']
                end_text = None
                for pattern in end_patterns:
                    end_text = find_text_boundary(full_text, pattern, is_start=True, after_title=title)
                    if end_text:
                        break
                if not end_text:
                    end_text = "END_OF_DOCUMENT"
            else:
                end_text = find_text_boundary(full_text, "Summary", is_start=True, after_title=title)
                if not end_text:
                    end_text = "END_OF_SECTION"
        
        new_node['start_text'] = start_text if start_text else f"NOT_FOUND_{title}"
        new_node['end_text'] = end_text if end_text else f"NOT_FOUND_END_{title}"
        
        nodes_with_boundaries.append(new_node)
    
    # Part 1이 아닌 나머지 노드들도 기본 정보만으로 추가
    other_nodes = [node for node in leaf_nodes if not (
        node['title'].startswith('Part 1') or 
        node['title'].startswith('1') or
        (node['title'] == 'Summary' and node['id'] <= 62)
    )]
    
    for node in other_nodes:
        new_node = {
            'id': node['id'],
            'title': node['title'],
            'level': node['level'],
            'start_text': f"TITLE_START_{node['title']}",
            'end_text': f"TITLE_END_{node['title']}"
        }
        nodes_with_boundaries.append(new_node)
    
    # ID 순으로 정렬
    nodes_with_boundaries.sort(key=lambda x: x['id'])
    
    return nodes_with_boundaries

def find_text_boundary(text, title, is_start=True, after_title=None):
    """텍스트에서 특정 제목의 경계 텍스트를 찾기"""
    
    # 제목 정규화 및 패턴 생성
    patterns = []
    
    if title == "Part 1 Introduction":
        patterns = [r"Part 1\\nFlexibility", r"Part 1"]
    elif title.startswith("Part 1"):
        patterns = [r"Part 1"]
    elif re.match(r'^\\d+\\s+Introduction$', title):  # "1 Introduction", "2 Introduction" 등
        chapter_num = title.split()[0]
        patterns = [f"^{chapter_num}\\s", f"CHAPTER {chapter_num}", f"^{chapter_num}$"]
    elif re.match(r'^\\d+\\.\\d+\\s+Introduction$', title):  # "1.1 Introduction" 등
        section_num = title.split()[0]
        patterns = [f"^{section_num}\\s"]
    elif re.match(r'^\\d+\\.\\d+\\.\\d+', title):  # "1.1.1 The design phase" 등
        patterns = [re.escape(title), title.replace(' ', '\\s+')]
    elif title == "Summary":
        if after_title:
            # after_title 이후의 첫 번째 Summary 찾기
            after_pos = text.find(after_title)
            if after_pos != -1:
                remaining_text = text[after_pos + len(after_title):]
                summary_pos = remaining_text.find("Summary")
                if summary_pos != -1:
                    return "Summary"
        patterns = [r"^Summary$", r"Summary"]
    else:
        patterns = [re.escape(title), title.replace(' ', '\\s+')]
    
    # 패턴으로 검색
    for pattern in patterns:
        matches = list(re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE))
        if matches:
            match = matches[0]  # 첫 번째 매치 사용
            if is_start:
                # 해당 라인의 시작부터 반환
                line_start = text.rfind('\\n', 0, match.start()) + 1
                line_end = text.find('\\n', match.end())
                if line_end == -1:
                    line_end = len(text)
                return text[line_start:line_end].strip()
            else:
                return text[match.start():match.end()]
    
    return None

def normalize_for_search(text):
    """검색을 위한 텍스트 정규화"""
    return re.sub(r'\\s+', ' ', text.strip())

if __name__ == "__main__":
    main()