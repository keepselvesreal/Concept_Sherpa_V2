"""
생성 시간: 2025-08-07 현재 시각  
핵심 내용: TOC 구조에 상위-하위 구성 단위 사이의 Introduction 노드를 추가하는 수정된 처리기

상세 내용:
    - load_toc_data(1-15): 기존 TOC JSON 파일을 로드하는 함수
    - identify_introduction_positions(17-120): 상위-하위 구성 단위 관계를 정확히 분석하고 Introduction 노드 생성
    - insert_introduction_nodes(122-140): TOC 리스트에 Introduction 노드들을 삽입
    - save_modified_toc(142-155): 수정된 TOC를 새 파일로 저장
    - main(157-170): 메인 실행 함수

상태: active
주소: toc_introduction_processor_v2
참조: toc_introduction_processor
"""

import json
import re
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
        current_title = current_node.get('title', '')
        next_title = next_node.get('title', '')
        
        # 상위 구성 단위 → 하위 구성 단위 관계인지 확인 (정확히 1레벨 차이)
        if next_level == current_level + 1:
            current_start = current_node.get('start_page')
            next_start = next_node.get('start_page')
            
            # 페이지 간격 확인
            has_gap = current_start and next_start and current_start < next_start
            needs_confirmation = current_start == next_start
            
            # Introduction 노드 제목 생성
            intro_title = ""
            
            if current_level == 0:  # Part → Chapter
                # Part 제목에서 번호 추출
                if "Part 1" in current_title:
                    intro_title = "1.0 Introduction (사용자 추가)"
                elif "Part 2" in current_title:
                    intro_title = "7.0 Introduction (사용자 추가)"  # Chapter 7부터 시작
                elif "Part 3" in current_title:
                    intro_title = "12.0 Introduction (사용자 추가)"  # Chapter 12부터 시작
                elif "Appendix A" in current_title:
                    intro_title = "A.0 Introduction (사용자 추가)"
                elif "Appendix B" in current_title:
                    intro_title = "B.0 Introduction (사용자 추가)"
                elif "Appendix C" in current_title:
                    intro_title = "C.0 Introduction (사용자 추가)"
                elif "Appendix D" in current_title:
                    intro_title = "D.0 Introduction (사용자 추가)"
                else:
                    # 기타 level 0 구성 단위
                    continue
                    
            elif current_level == 1:  # Chapter → Section
                # Chapter 제목에서 번호 추출
                chapter_match = re.match(r'^(\d+(?:\.\d+)*|[A-D](?:\.\d+)*)', current_title)
                if chapter_match:
                    chapter_num = chapter_match.group(1)
                    intro_title = f"{chapter_num}.0.0 Introduction (사용자 추가)"
                else:
                    continue
                    
            elif current_level == 2:  # Section → Subsection
                # Section 제목에서 번호 추출
                section_match = re.match(r'^(\d+\.\d+(?:\.\d+)*)', current_title)
                if section_match:
                    section_num = section_match.group(1)
                    intro_title = f"{section_num}.0 Introduction (사용자 추가)"
                else:
                    continue
            else:
                continue
            
            # 확인 필요 표시 추가
            if needs_confirmation:
                intro_title += " - 확인 필요함"
            
            # 설명 생성
            desc = f"{current_title}와 {next_title} 사이에 존재하는 내용을 담은 부분"
            
            intro_node = {
                'title': intro_title,
                'level': next_level,
                'desc': desc
            }
            
            # 삽입 위치와 노드 정보를 저장 (i+1 위치에 삽입)
            introduction_positions.append((i + 1, intro_node))
            print(f"추가될 노드: {intro_title} (위치: {i+1}, level: {next_level})")
    
    return introduction_positions

def insert_introduction_nodes(toc_data: List[Dict[str, Any]], 
                            introduction_positions: List[Tuple[int, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """TOC 리스트에 Introduction 노드들을 적절한 위치에 삽입"""
    # 역순으로 정렬하여 인덱스가 변경되지 않도록 함
    introduction_positions.sort(key=lambda x: x[0], reverse=True)
    
    modified_toc = toc_data.copy()
    
    for position, intro_node in introduction_positions:
        # 조정된 위치에 삽입
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