#!/usr/bin/env python3
"""
생성 시간: 2025년 8월 9일 12:46 KST
핵심 내용: Chapter 7 Basic Data Validation 리프 노드 텍스트 추출 스크립트
상세 내용:
    - extract_chapter7_text(): PDF에서 7장 텍스트 추출하는 메인 함수
    - find_text_between(): 시작/종료 문자열 사이의 텍스트 추출 함수  
    - clean_extracted_text(): 추출된 텍스트 정리 및 정규화 함수
    - save_extracted_texts(): 추출된 텍스트들을 개별 파일로 저장하는 함수
    - main(): 스크립트 실행 메인 함수
상태: 작성 완료
주소: chapter7_text_extractor
참조: chapter7_leaf_nodes_with_boundaries.json 사용
"""

import json
import re
import os
import sys
from pathlib import Path

# PyPDF2 import
try:
    import PyPDF2
except ImportError:
    print("PyPDF2를 설치해주세요: pip install PyPDF2")
    sys.exit(1)

def load_leaf_nodes(json_path):
    """경계 문자열이 포함된 리프 노드 데이터 로드"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 주석 제거 (/* ... */ 형태)
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            return json.loads(content)
    except Exception as e:
        print(f"JSON 파일 로드 실패 {json_path}: {e}")
        return []

def extract_pdf_text(pdf_path):
    """PDF 전체 텍스트 추출"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            full_text = ""
            
            # 페이지 169-190 (7장 범위)를 중심으로 추출
            start_page = 168  # 0-based index
            end_page = 195    # 여유분 포함
            
            for page_num in range(start_page, min(end_page, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += text + "\n"
                
            return full_text
            
    except Exception as e:
        print(f"PDF 텍스트 추출 실패 {pdf_path}: {e}")
        return ""

def find_text_between(full_text, start_text, end_text, node_title=""):
    """시작 문자열과 종료 문자열 사이의 텍스트 추출"""
    try:
        # 텍스트 정규화
        full_text = re.sub(r'\s+', ' ', full_text)
        start_text = re.sub(r'\s+', ' ', start_text.strip())
        end_text = re.sub(r'\s+', ' ', end_text.strip())
        
        # 시작 문자열 찾기
        start_pattern = re.escape(start_text).replace(r'\ ', r'\s+')
        start_match = re.search(start_pattern, full_text, re.IGNORECASE)
        
        if not start_match:
            print(f"⚠️  '{node_title}' 시작 문자열 찾을 수 없음: '{start_text}'")
            return ""
            
        start_pos = start_match.start()
        
        # 종료 문자열 찾기 (시작 위치 이후에서)
        end_pattern = re.escape(end_text).replace(r'\ ', r'\s+')
        end_match = re.search(end_pattern, full_text[start_pos:], re.IGNORECASE)
        
        if not end_match:
            print(f"⚠️  '{node_title}' 종료 문자열 찾을 수 없음: '{end_text}'")
            # 다음 섹션 시작까지 추출 시도
            next_section_patterns = [
                r'\d+\.\d+\s+[A-Z]',  # 7.1, 7.2 등
                r'Summary\s*\n',
                r'Chapter\s+\d+'
            ]
            
            for pattern in next_section_patterns:
                next_match = re.search(pattern, full_text[start_pos + 100:], re.IGNORECASE)
                if next_match:
                    end_pos = start_pos + 100 + next_match.start()
                    extracted_text = full_text[start_pos:end_pos]
                    return clean_extracted_text(extracted_text)
            
            # 최대 5000자까지만 추출
            extracted_text = full_text[start_pos:start_pos + 5000]
            return clean_extracted_text(extracted_text)
        
        end_pos = start_pos + end_match.end()
        extracted_text = full_text[start_pos:end_pos]
        
        return clean_extracted_text(extracted_text)
        
    except Exception as e:
        print(f"텍스트 추출 오류 '{node_title}': {e}")
        return ""

def clean_extracted_text(text):
    """추출된 텍스트 정리 및 정규화"""
    if not text:
        return ""
    
    # 기본 정리
    text = text.strip()
    
    # 페이지 번호 제거
    text = re.sub(r'=== 페이지 \d+ ===', '', text)
    text = re.sub(r'\n\d+\s+(CHAPTER|Summary)', r'\n\1', text)
    
    # 연속된 공백 정리
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # 줄바꿈 정리
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def save_extracted_texts(extracted_data, output_dir):
    """추출된 텍스트들을 개별 파일로 저장"""
    os.makedirs(output_dir, exist_ok=True)
    
    for item in extracted_data:
        if item.get('extracted_text'):
            # 파일명 생성
            safe_title = re.sub(r'[^\w\s-]', '', item['title'])
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{item['id']:03d}_{safe_title}.md"
            filepath = os.path.join(output_dir, filename)
            
            # 파일 내용 구성
            content = f"# {item['title']}\n\n"
            content += f"**ID:** {item['id']}\n"
            content += f"**Level:** {item['level']}\n\n"
            content += "---\n\n"
            content += item['extracted_text']
            
            # 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 저장: {filename} ({len(item['extracted_text'])} chars)")

def extract_chapter7_text():
    """Chapter 7 리프 노드 텍스트 추출 메인 함수"""
    # 파일 경로 설정
    current_dir = Path(__file__).parent
    json_path = current_dir / "chapter7_leaf_nodes_with_boundaries.json"
    pdf_path = current_dir / ".." / "2022_Data-Oriented Programming_Manning.pdf"
    output_dir = current_dir / "chapter7_extracted_texts"
    
    print("📚 Chapter 7 텍스트 추출 시작...")
    
    # 1. 리프 노드 데이터 로드
    leaf_nodes = load_leaf_nodes(json_path)
    if not leaf_nodes:
        print("❌ 리프 노드 데이터 로드 실패")
        return
        
    print(f"📋 {len(leaf_nodes)}개 리프 노드 로드 완료")
    
    # 2. PDF 텍스트 추출
    print("📖 PDF 텍스트 추출 중...")
    full_text = extract_pdf_text(pdf_path)
    if not full_text:
        print("❌ PDF 텍스트 추출 실패")
        return
        
    print(f"✅ PDF 텍스트 추출 완료 ({len(full_text)} chars)")
    
    # 3. 각 리프 노드별 텍스트 추출
    extracted_data = []
    
    for node in leaf_nodes:
        print(f"\n🔍 처리 중: {node['title']}")
        
        extracted_text = find_text_between(
            full_text, 
            node['start_text'], 
            node['end_text'],
            node['title']
        )
        
        if extracted_text:
            word_count = len(extracted_text.split())
            char_count = len(extracted_text)
            print(f"✅ 추출 성공: {word_count} words, {char_count} chars")
            status = "success"
        else:
            word_count = 0
            char_count = 0
            print(f"❌ 추출 실패")
            status = "failed"
        
        extracted_data.append({
            'id': node['id'],
            'title': node['title'],
            'level': node['level'],
            'start_text': node['start_text'],
            'end_text': node['end_text'],
            'extracted_text': extracted_text,
            'word_count': word_count,
            'char_count': char_count,
            'extraction_status': status
        })
    
    # 4. 결과 저장
    print(f"\n💾 결과 저장 중...")
    
    # JSON 결과 저장
    result_file = current_dir / "chapter7_extracted_results.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
    
    # 개별 텍스트 파일 저장
    save_extracted_texts(extracted_data, output_dir)
    
    # 5. 결과 요약
    successful = sum(1 for item in extracted_data if item['extraction_status'] == 'success')
    total_words = sum(item['word_count'] for item in extracted_data)
    total_chars = sum(item['char_count'] for item in extracted_data)
    
    print(f"\n📊 추출 완료 요약:")
    print(f"   성공: {successful}/{len(extracted_data)} 노드")
    print(f"   총 단어수: {total_words:,}")
    print(f"   총 문자수: {total_chars:,}")
    print(f"   결과 파일: {result_file}")
    print(f"   텍스트 디렉토리: {output_dir}")

def main():
    """메인 실행 함수"""
    try:
        extract_chapter7_text()
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()