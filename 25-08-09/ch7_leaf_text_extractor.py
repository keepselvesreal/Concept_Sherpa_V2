# 
# 생성 시간: 2025-08-09 14:20 (한국 시간)
# 핵심 내용: 7장 Basic data validation 리프 노드 텍스트 추출기
# 상세 내용:
#   - load_boundaries_data (line 15-20): JSON에서 경계 정보 로드
#   - load_original_text (line 22-27): 원문 텍스트 파일 로드
#   - extract_section_text (line 29-45): 시작/종료 문자로 섹션 텍스트 추출
#   - extract_all_leaf_texts (line 47-65): 모든 리프 노드 텍스트 추출
#   - save_extracted_texts (line 67-75): 추출된 텍스트를 개별 파일로 저장
#   - main (line 77-90): 전체 추출 프로세스 실행
# 상태: active
# 주소: ch7_leaf_text_extractor
# 참조: 

import json
import os
from pathlib import Path

def load_boundaries_data(json_file_path):
    """JSON 파일에서 경계 정보 로드"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_original_text(text_file_path):
    """원문 텍스트 파일 로드"""
    with open(text_file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_section_text(original_text, start_text, end_text, section_title):
    """시작과 종료 문자 사이의 텍스트 추출"""
    try:
        start_idx = original_text.find(start_text)
        if start_idx == -1:
            print(f"Warning: '{start_text}' not found for section '{section_title}'")
            return ""
        
        end_idx = original_text.find(end_text, start_idx + len(start_text))
        if end_idx == -1:
            print(f"Warning: '{end_text}' not found for section '{section_title}'")
            return original_text[start_idx:]
        
        extracted_text = original_text[start_idx:end_idx].strip()
        return extracted_text
    except Exception as e:
        print(f"Error extracting text for '{section_title}': {e}")
        return ""

def extract_all_leaf_texts(boundaries_data, original_text):
    """모든 리프 노드 텍스트 추출"""
    extracted_texts = {}
    
    for node in boundaries_data:
        node_id = node['id']
        title = node['title']
        start_text = node['start_text']
        end_text = node['end_text']
        
        print(f"Extracting: {title} (ID: {node_id})")
        
        section_text = extract_section_text(original_text, start_text, end_text, title)
        extracted_texts[node_id] = {
            'title': title,
            'text': section_text,
            'start_text': start_text,
            'end_text': end_text
        }
    
    return extracted_texts

def save_extracted_texts(extracted_texts, output_dir):
    """추출된 텍스트를 개별 파일로 저장"""
    os.makedirs(output_dir, exist_ok=True)
    
    for node_id, data in extracted_texts.items():
        # 파일명에서 특수문자 제거
        safe_title = data['title'].replace('/', '_').replace(':', '_').replace('.', '_')
        filename = f"{node_id:03d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {data['title']}\n\n")
            f.write(data['text'])
        
        print(f"Saved: {filename}")

def main():
    # 파일 경로 설정
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09"
    boundaries_file = os.path.join(base_dir, "ch7_leaf_nodes_with_boundaries.json")
    original_text_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    output_dir = os.path.join(base_dir, "ch7_leaf_texts")
    
    # 텍스트 추출 실행
    boundaries_data = load_boundaries_data(boundaries_file)
    original_text = load_original_text(original_text_file)
    
    extracted_texts = extract_all_leaf_texts(boundaries_data, original_text)
    save_extracted_texts(extracted_texts, output_dir)
    
    print(f"\n추출 완료: {len(extracted_texts)}개 리프 노드 텍스트 추출됨")
    print(f"출력 디렉토리: {output_dir}")

if __name__ == "__main__":
    main()