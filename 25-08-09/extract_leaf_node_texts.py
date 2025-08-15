#!/usr/bin/env python3
"""
# 목차
- 생성 시간: 2025-08-09 11:09:47 KST
- 핵심 내용: Part 2 Scalability의 각 리프 노드 텍스트를 경계 정보를 사용해 추출하여 개별 마크다운 파일로 저장
- 상세 내용:
    - extract_text_between_boundaries(full_text, start_text, end_text): 시작과 끝 텍스트 사이의 내용을 추출하는 함수
    - sanitize_filename(title): 파일명으로 사용할 수 없는 문자를 제거하는 함수
    - main(): JSON 파일을 읽고 각 리프 노드의 텍스트를 추출하여 저장하는 메인 함수
- 상태: 활성
- 주소: extract_leaf_node_texts
- 참조: part2_scalability_leaf_nodes_with_boundaries.json, Part_02_Part_2_Scalability.md
"""

import json
import os
import re
from pathlib import Path

def extract_text_between_boundaries(full_text, start_text, end_text):
    """
    전체 텍스트에서 시작 텍스트와 끝 텍스트 사이의 내용을 추출합니다.
    
    Args:
        full_text (str): 전체 텍스트
        start_text (str): 시작 경계 텍스트
        end_text (str): 끝 경계 텍스트
    
    Returns:
        str: 추출된 텍스트 또는 None (찾을 수 없는 경우)
    """
    try:
        # 시작 텍스트 찾기
        start_index = full_text.find(start_text)
        if start_index == -1:
            print(f"시작 텍스트를 찾을 수 없습니다: {start_text[:50]}...")
            return None
        
        # 끝 텍스트 찾기 (시작 위치 이후에서)
        end_index = full_text.find(end_text, start_index + len(start_text))
        if end_index == -1:
            print(f"끝 텍스트를 찾을 수 없습니다: {end_text[:50]}...")
            return None
        
        # 시작 텍스트부터 끝 텍스트 + 끝 텍스트 길이까지 추출
        extracted_text = full_text[start_index:end_index + len(end_text)]
        return extracted_text.strip()
        
    except Exception as e:
        print(f"텍스트 추출 중 오류 발생: {e}")
        return None

def sanitize_filename(title):
    """
    파일명으로 사용할 수 없는 문자를 제거하고 안전한 파일명을 만듭니다.
    """
    # 특수문자 제거 및 공백을 언더스코어로 변경
    safe_name = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_name = re.sub(r'\s+', '_', safe_name)
    safe_name = safe_name.replace('.', '_')
    return safe_name

def main():
    """
    메인 함수: JSON 파일을 읽고 각 리프 노드의 텍스트를 추출하여 저장합니다.
    """
    # 파일 경로 설정
    base_dir = Path(__file__).parent
    boundaries_file = base_dir / "part2_scalability_leaf_nodes_with_boundaries.json"
    source_text_file = base_dir.parent / "25-08-07" / "extracted_parts" / "Part_02_Part_2_Scalability.md"
    output_dir = base_dir / "part2_extracted_texts"
    
    # 출력 디렉토리 생성
    output_dir.mkdir(exist_ok=True)
    
    try:
        # JSON 파일 읽기
        print("경계 정보 JSON 파일을 읽는 중...")
        with open(boundaries_file, 'r', encoding='utf-8') as f:
            leaf_nodes = json.load(f)
        
        # 소스 텍스트 파일 읽기
        print("원본 텍스트 파일을 읽는 중...")
        with open(source_text_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        print(f"총 {len(leaf_nodes)}개의 리프 노드를 처리합니다.")
        
        # 각 리프 노드에 대해 텍스트 추출
        successful_extractions = 0
        failed_extractions = 0
        
        for i, node in enumerate(leaf_nodes, 1):
            node_id = node['id']
            title = node['title']
            start_text = node['start_text']
            end_text = node['end_text']
            
            print(f"\n[{i}/{len(leaf_nodes)}] 처리 중: {title} (ID: {node_id})")
            
            # 텍스트 추출
            extracted_text = extract_text_between_boundaries(full_text, start_text, end_text)
            
            if extracted_text:
                # 파일명 생성
                safe_filename = sanitize_filename(f"{node_id:03d}_{title}")
                output_file = output_dir / f"{safe_filename}.md"
                
                # 마크다운 파일로 저장
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"**ID**: {node_id}  \n")
                    f.write(f"**Level**: {node.get('level', 'N/A')}  \n")
                    f.write(f"**추출 시간**: 2025-08-09 11:09:47 KST\n\n")
                    f.write("---\n\n")
                    f.write(extracted_text)
                
                print(f"✓ 성공: {output_file}")
                successful_extractions += 1
            else:
                print(f"✗ 실패: {title} (ID: {node_id})")
                failed_extractions += 1
        
        # 결과 요약
        print(f"\n=== 추출 완료 ===")
        print(f"성공: {successful_extractions}개")
        print(f"실패: {failed_extractions}개")
        print(f"출력 디렉토리: {output_dir}")
        
        # 추출 보고서 생성
        report_file = output_dir / "extraction_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Part 2 Scalability 텍스트 추출 보고서\n\n")
            f.write(f"**추출 시간**: 2025-08-09 11:09:47 KST  \n")
            f.write(f"**총 노드 수**: {len(leaf_nodes)}개  \n")
            f.write(f"**성공**: {successful_extractions}개  \n")
            f.write(f"**실패**: {failed_extractions}개  \n\n")
            
            if failed_extractions > 0:
                f.write("## 실패한 노드들\n\n")
                for node in leaf_nodes:
                    extracted_text = extract_text_between_boundaries(full_text, node['start_text'], node['end_text'])
                    if not extracted_text:
                        f.write(f"- **{node['title']}** (ID: {node['id']})\n")
            
            f.write("\n## 성공적으로 추출된 파일들\n\n")
            for node in leaf_nodes:
                extracted_text = extract_text_between_boundaries(full_text, node['start_text'], node['end_text'])
                if extracted_text:
                    safe_filename = sanitize_filename(f"{node['id']:03d}_{node['title']}")
                    f.write(f"- `{safe_filename}.md` - {node['title']}\n")
        
        print(f"추출 보고서 생성: {report_file}")
        
    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")

if __name__ == "__main__":
    main()