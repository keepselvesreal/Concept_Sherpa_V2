#!/usr/bin/env python3
"""
생성 시간: 2025-08-09 12:32:44 KST
핵심 내용: Chapter 7 리프 노드 텍스트 추출기
상세 내용:
    - load_leaf_nodes(): chapter7_leaf_nodes_with_boundaries.json 로드
    - load_source_text(): Level01_7 Basic data validation.md 읽기
    - extract_leaf_text(): 시작/종료 문자열 기반 텍스트 추출
    - save_extracted_text(): 추출된 텍스트를 개별 마크다운 파일로 저장
    - main(): 전체 추출 프로세스 실행 및 결과 보고서 생성
상태: 활성
주소: chapter7_leaf_text_extractor
참조: chapter7_leaf_nodes_with_boundaries.json, Level01_7 Basic data validation.md
"""

import json
import os
from pathlib import Path

def load_leaf_nodes(json_path):
    """리프 노드 경계 정보 로드"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_source_text(md_path):
    """원본 마크다운 텍스트 로드"""
    with open(md_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_leaf_text(content, start_text, end_text):
    """시작/종료 문자열 기반 텍스트 추출"""
    if not start_text or not end_text:
        return None
    
    start_pos = content.find(start_text)
    if start_pos == -1:
        print(f"❌ 시작 텍스트를 찾을 수 없음: {start_text[:50]}...")
        return None
    
    end_pos = content.find(end_text, start_pos + len(start_text))
    if end_pos == -1:
        print(f"❌ 종료 텍스트를 찾을 수 없음: {end_text[:50]}...")
        return None
    
    return content[start_pos:end_pos].strip()

def save_extracted_text(node, text, output_dir):
    """추출된 텍스트를 파일로 저장"""
    # 안전한 파일명 생성
    safe_title = node['title'].replace('/', '_').replace('\\', '_').replace(':', '_').replace('.', '_')
    filename = f"{node['id']:03d}_{safe_title}.md"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {node['title']}\n\n")
        f.write(f"**ID:** {node['id']}\n")
        f.write(f"**Level:** {node['level']}\n\n")
        f.write("---\n\n")
        f.write(text)
    
    return filepath

def main():
    # 경로 설정
    base_dir = Path('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09')
    json_path = base_dir / 'chapter7_leaf_nodes_with_boundaries.json'
    md_path = base_dir / 'extracted_texts' / 'Level01_7 Basic data validation.md'
    output_dir = base_dir / 'chapter7_leaf_texts'
    
    # 출력 디렉토리 생성
    output_dir.mkdir(exist_ok=True)
    
    print("📖 Chapter 7 리프 노드 텍스트 추출 시작")
    print(f"📄 리프 노드 정보: {json_path.name}")
    print(f"📄 원본 텍스트: {md_path.name}")
    print(f"📁 출력 디렉토리: {output_dir}")
    
    # 파일 로드
    leaf_nodes = load_leaf_nodes(json_path)
    content = load_source_text(md_path)
    
    print(f"🔍 총 {len(leaf_nodes)}개 리프 노드 처리")
    
    extraction_results = []
    
    for i, node in enumerate(leaf_nodes, 1):
        print(f"\n[{i}/{len(leaf_nodes)}] {node['title']} (ID: {node['id']})")
        
        extracted_text = extract_leaf_text(content, node['start_text'], node['end_text'])
        
        if extracted_text:
            filepath = save_extracted_text(node, extracted_text, output_dir)
            extraction_results.append({
                'id': node['id'],
                'title': node['title'],
                'filepath': str(filepath),
                'text_length': len(extracted_text),
                'status': 'success'
            })
            print(f"✅ 추출 완료: {len(extracted_text):,} 문자 → {filepath.name}")
        else:
            extraction_results.append({
                'id': node['id'],
                'title': node['title'],
                'filepath': None,
                'text_length': 0,
                'status': 'failed'
            })
            print(f"❌ 추출 실패")
    
    # 결과 보고서 생성
    successful = len([r for r in extraction_results if r['status'] == 'success'])
    failed = len([r for r in extraction_results if r['status'] == 'failed'])
    
    report_data = {
        'extraction_summary': {
            'total_nodes': len(leaf_nodes),
            'successful_extractions': successful,
            'failed_extractions': failed,
            'success_rate': f"{successful/len(leaf_nodes)*100:.1f}%"
        },
        'results': extraction_results
    }
    
    report_path = output_dir / 'extraction_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 추출 완료!")
    print(f"✅ 성공: {successful}/{len(leaf_nodes)} ({successful/len(leaf_nodes)*100:.1f}%)")
    print(f"❌ 실패: {failed}/{len(leaf_nodes)}")
    print(f"📊 결과 보고서: {report_path}")
    print(f"📁 추출된 파일들: {output_dir}")

if __name__ == "__main__":
    main()