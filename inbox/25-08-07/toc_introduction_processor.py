"""
생성 시간: 2025-08-07 현재 시각
핵심 내용: TOC 구조에 상위-하위 구성 단위 사이의 Introduction 노드를 추가하는 처리기

상세 내용:
    - load_toc_data(1-15): 기존 TOC JSON 파일을 로드하는 함수
    - identify_introduction_positions(17-85): 상위-하위 구성 단위 관계를 분석하고 Introduction 노드가 필요한 위치를 식별하는 함수
    - create_introduction_node(87-105): Introduction 노드 객체를 생성하는 함수
    - insert_introduction_nodes(107-130): TOC 리스트에 Introduction 노드들을 적절한 위치에 삽입하는 함수
    - save_modified_toc(132-145): 수정된 TOC를 새 파일로 저장하는 함수
    - main(147-160): 메인 실행 함수

상태: active
주소: toc_introduction_processor
참조: 
"""

import json
from typing import List, Dict, Any, Tuple

def load_toc_data(file_path: str) -> List[Dict[str, Any]]:
    """기존 TOC JSON 파일을 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"JSON 파싱 오류: {file_path}")
        return []

def identify_introduction_positions(toc_data: List[Dict[str, Any]]) -> List[Tuple[int, Dict[str, Any]]]:
    """상위-하위 구성 단위 관계를 분석하고 Introduction 노드가 필요한 위치를 식별"""
    introduction_positions = []
    
    for i in range(len(toc_data) - 1):
        current_node = toc_data[i]
        next_node = toc_data[i + 1]
        
        current_level = current_node.get('level', 0)
        next_level = next_node.get('level', 0)
        
        # 상위 구성 단위 → 하위 구성 단위 관계인지 확인
        if next_level == current_level + 1:
            current_start = current_node.get('start_page')
            current_end = current_node.get('end_page')
            next_start = next_node.get('start_page')
            
            # 페이지 간격이 있는지 확인
            has_gap = current_start and next_start and current_start < next_start
            needs_confirmation = current_start == next_start
            
            # Introduction 노드 정보 생성
            if current_level == 0:  # Part → Chapter
                intro_title = f"{next_node.get('title', '').split()[0].replace('—', '.0')} Introduction (사용자 추가)"
                if needs_confirmation:
                    intro_title += " - 확인 필요함"
            elif current_level == 1:  # Chapter → Section  
                chapter_num = current_node.get('title', '').split()[0]
                intro_title = f"{chapter_num}.0.0 Introduction (사용자 추가)"
                if needs_confirmation:
                    intro_title += " - 확인 필요함"
            elif current_level == 2:  # Section → Subsection
                section_num = current_node.get('title', '').split()[0]
                intro_title = f"{section_num}.0 Introduction (사용자 추가)"
                if needs_confirmation:
                    intro_title += " - 확인 필요함"
            else:
                continue
            
            # 설명 생성
            current_title = current_node.get('title', '')
            next_title = next_node.get('title', '')
            desc = f"{current_title}와 {next_title} 사이에 존재하는 내용을 담은 부분"
            
            intro_node = {
                'title': intro_title,
                'level': next_level,
                'desc': desc
            }
            
            # 삽입 위치와 노드 정보를 저장 (i+1 위치에 삽입)
            introduction_positions.append((i + 1, intro_node))
    
    return introduction_positions

def create_introduction_node(title: str, level: int, desc: str) -> Dict[str, Any]:
    """Introduction 노드 객체를 생성"""
    return {
        'title': title,
        'level': level,
        'desc': desc
    }

def insert_introduction_nodes(toc_data: List[Dict[str, Any]], 
                            introduction_positions: List[Tuple[int, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """TOC 리스트에 Introduction 노드들을 적절한 위치에 삽입"""
    # 역순으로 정렬하여 인덱스가 변경되지 않도록 함
    introduction_positions.sort(key=lambda x: x[0], reverse=True)
    
    modified_toc = toc_data.copy()
    
    for position, intro_node in introduction_positions:
        # 조정된 위치에 삽입 (역순 처리로 인한 인덱스 보정)
        adjusted_position = min(position, len(modified_toc))
        modified_toc.insert(adjusted_position, intro_node)
    
    return modified_toc

def save_modified_toc(modified_toc: List[Dict[str, Any]], output_path: str) -> None:
    """수정된 TOC를 새 파일로 저장"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(modified_toc, f, ensure_ascii=False, indent=2)
        print(f"수정된 TOC가 저장되었습니다: {output_path}")
        print(f"총 노드 수: {len(modified_toc)}")
    except Exception as e:
        print(f"파일 저장 오류: {e}")

def main():
    """메인 실행 함수"""
    input_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/toc_with_page_ranges.json"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/toc_with_page_ranges_v2.json"
    
    # 1. 기존 TOC 데이터 로드
    toc_data = load_toc_data(input_file)
    if not toc_data:
        return
    
    # 2. Introduction 노드 위치 식별
    introduction_positions = identify_introduction_positions(toc_data)
    
    # 3. Introduction 노드 삽입
    modified_toc = insert_introduction_nodes(toc_data, introduction_positions)
    
    # 4. 수정된 TOC 저장
    save_modified_toc(modified_toc, output_file)
    
    print(f"추가된 Introduction 노드 수: {len(introduction_positions)}")

if __name__ == "__main__":
    main()