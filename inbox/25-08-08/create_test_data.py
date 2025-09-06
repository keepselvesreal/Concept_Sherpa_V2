# 생성 시간: 2025-08-08 16:16:25 KST
# 핵심 내용: Chapter 1 테스트용 데이터 생성 - 리프 노드(ID 16까지)와 텍스트(Chapter 1까지) 추출
# 상세 내용:
#   - main() 함수 (라인 9-26): 메인 실행 로직, 테스트 데이터 생성 조율
#   - create_chapter1_leaf_nodes() 함수 (라인 28-46): ID 16까지 리프 노드 JSON 생성
#   - create_chapter1_text() 함수 (라인 48-74): Chapter 1까지 텍스트 추출
#   - find_chapter2_start() 함수 (라인 76-87): Chapter 2 시작 위치 찾기
# 상태: 활성
# 주소: create_test_data
# 참조: part1_leaf_nodes, Part_01_Part_1_Flexibility (원본 데이터)

import json
import os

def main():
    """Chapter 1 테스트용 데이터 생성"""
    
    print("🧪 Chapter 1 테스트 데이터 생성 시작...")
    
    # 파일 경로
    part1_leaf_nodes = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/leaf_nodes_by_parts/part1_leaf_nodes.json'
    part1_text = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md'
    test_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/test_data'
    
    # 1. Chapter 1 리프 노드 생성 (ID 16까지)
    create_chapter1_leaf_nodes(part1_leaf_nodes, test_dir)
    
    # 2. Chapter 1 텍스트 생성 (Chapter 2 전까지)
    create_chapter1_text(part1_text, test_dir)
    
    print("✅ Chapter 1 테스트 데이터 생성 완료!")

def create_chapter1_leaf_nodes(part1_leaf_file, test_dir):
    """ID 16까지 리프 노드만 추출하여 테스트용 JSON 생성"""
    
    with open(part1_leaf_file, 'r', encoding='utf-8') as f:
        all_nodes = json.load(f)
    
    # ID 16까지만 필터링 (Chapter 1 Summary까지 포함)
    chapter1_nodes = [node for node in all_nodes if node['id'] <= 16]
    
    # 테스트용 JSON 저장
    output_file = os.path.join(test_dir, 'chapter1_leaf_nodes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chapter1_nodes, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Chapter 1 리프 노드: {len(chapter1_nodes)}개 → {output_file}")
    
    # 노드 목록 출력
    for node in chapter1_nodes:
        print(f"   ID {node['id']:2d}: {node['title']}")

def create_chapter1_text(part1_text_file, test_dir):
    """Part 1 텍스트에서 Chapter 1까지만 추출"""
    
    with open(part1_text_file, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    print(f"📖 전체 텍스트 길이: {len(full_text):,} 문자")
    
    # Chapter 2 시작 위치 찾기
    chapter2_start = find_chapter2_start(full_text)
    
    if chapter2_start > 0:
        # Chapter 2 전까지 텍스트 추출
        chapter1_text = full_text[:chapter2_start].strip()
        print(f"✂️  Chapter 1 텍스트 길이: {len(chapter1_text):,} 문자")
    else:
        # Chapter 2를 찾지 못한 경우 전체 텍스트 사용
        chapter1_text = full_text
        print("⚠️  Chapter 2 시작점을 찾지 못했습니다. 전체 텍스트 사용")
    
    # 테스트용 텍스트 파일 저장
    output_file = os.path.join(test_dir, 'chapter1_text.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(chapter1_text)
    
    print(f"📝 Chapter 1 텍스트 저장: {output_file}")

def find_chapter2_start(text):
    """Chapter 2 시작 위치 찾기"""
    
    # 여러 패턴으로 Chapter 2 시작점 찾기
    patterns = [
        'CHAPTER 2',
        'Chapter 2',
        '2 Separation between code and data',
        '\n2\n',
        '## 2 '
    ]
    
    for pattern in patterns:
        pos = text.find(pattern)
        if pos > 0:
            print(f"🎯 Chapter 2 시작점 발견: '{pattern}' at position {pos}")
            return pos
    
    return -1

if __name__ == "__main__":
    main()