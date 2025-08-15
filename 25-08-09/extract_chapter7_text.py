#!/usr/bin/env python3
"""
Chapter 7 Text Extraction Script
텍스트 경계 정보를 바탕으로 7장의 각 리프 노드 텍스트를 추출합니다.
"""

import json
import os

def load_json_file(file_path):
    """JSON 파일을 로드합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_text_file(file_path):
    """텍스트 파일을 로드합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_between(content, start_text, end_text, section_title):
    """시작 문자열과 종료 문자열 사이의 텍스트를 추출합니다."""
    print(f"\n=== {section_title} 추출 중 ===")
    print(f"시작 문자열: '{start_text}'")
    print(f"종료 문자열: '{end_text}'")
    
    start_idx = content.find(start_text)
    if start_idx == -1:
        print(f"❌ 시작 문자열 '{start_text}'를 찾을 수 없습니다.")
        return None
        
    print(f"✓ 시작 위치: {start_idx}")
    
    # 시작 위치부터 종료 문자열 검색
    end_idx = content.find(end_text, start_idx)
    if end_idx == -1:
        print(f"❌ 종료 문자열 '{end_text}'를 찾을 수 없습니다.")
        return None
        
    print(f"✓ 종료 위치: {end_idx}")
    
    # 종료 문자열 포함하여 추출
    extracted_text = content[start_idx:end_idx + len(end_text)]
    print(f"✓ 추출된 텍스트 길이: {len(extracted_text)} 문자")
    
    return extracted_text

def main():
    # 파일 경로 설정
    boundaries_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_leaf_nodes_with_boundaries.json"
    source_text_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_leaf_nodes/"
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 로드
    print("📁 파일 로드 중...")
    boundaries = load_json_file(boundaries_file)
    source_content = load_text_file(source_text_file)
    
    print(f"✓ 경계 정보: {len(boundaries)}개 리프 노드")
    print(f"✓ 원본 텍스트 길이: {len(source_content)} 문자")
    
    extracted_texts = {}
    
    # 각 리프 노드 텍스트 추출
    for node in boundaries:
        node_id = node['id']
        title = node['title']
        start_text = node['start_text']
        end_text = node['end_text']
        
        # 텍스트 추출
        extracted = extract_text_between(source_content, start_text, end_text, title)
        
        if extracted:
            # 파일로 저장
            safe_title = title.replace('/', '_').replace(' ', '_')
            output_file = f"{output_dir}node_{node_id}_{safe_title}.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"=== {title} (ID: {node_id}) ===\n\n")
                f.write(extracted)
            
            extracted_texts[node_id] = {
                'title': title,
                'text': extracted,
                'length': len(extracted),
                'file': output_file
            }
            
            print(f"💾 저장됨: {output_file}")
            
        else:
            print(f"❌ {title} 추출 실패")
    
    # 추출 결과 요약
    print(f"\n📊 추출 결과 요약:")
    print(f"총 {len(boundaries)}개 노드 중 {len(extracted_texts)}개 성공적으로 추출")
    
    # 결과를 JSON으로도 저장
    summary_file = f"{output_dir}extraction_summary.json"
    summary_data = {
        'total_nodes': len(boundaries),
        'extracted_nodes': len(extracted_texts),
        'extraction_results': extracted_texts
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"📋 추출 요약 저장: {summary_file}")
    
    return extracted_texts

if __name__ == "__main__":
    extracted_texts = main()