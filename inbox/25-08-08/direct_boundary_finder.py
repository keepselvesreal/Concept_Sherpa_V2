# 생성 시간: 2025-08-08 16:38:45 KST
# 핵심 내용: 직접 텍스트 분석으로 리프 노드 경계 텍스트 찾기 - Claude SDK 출력 토큰 제한 우회
# 상세 내용:
#   - main() 함수 (라인 9-32): 메인 실행 로직, Chapter 1 데이터로 직접 경계 분석
#   - analyze_text_boundaries() 함수 (라인 34-78): 텍스트 직접 분석으로 경계 찾기
#   - find_text_boundaries() 함수 (라인 80-120): 각 리프 노드의 시작/끝 텍스트 추출
#   - get_next_title_text() 함수 (라인 122-140): 다음 제목 텍스트 찾기
# 상태: 활성
# 주소: direct_boundary_finder
# 참조: test_data (Chapter 1 테스트 데이터)

import json
import re
import os

def main():
    """Chapter 1 데이터로 직접 텍스트 경계 분석"""
    
    print("🔍 직접 텍스트 경계 분석 시작...")
    
    # 테스트 파일 경로
    test_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/test_data'
    leaf_nodes_file = os.path.join(test_dir, 'chapter1_leaf_nodes.json')
    text_file = os.path.join(test_dir, 'chapter1_text.md')
    output_file = os.path.join(test_dir, 'chapter1_direct_boundaries.json')
    
    # 파일 존재 확인
    if not os.path.exists(leaf_nodes_file) or not os.path.exists(text_file):
        print(f"❌ 테스트 파일이 없습니다.")
        return
    
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 직접 분석 실행
    analyze_text_boundaries(leaf_nodes_file, text_file, output_file)

def analyze_text_boundaries(leaf_nodes_file, text_file, output_file):
    """텍스트 직접 분석으로 경계 찾기"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    print(f"🌿 리프 노드: {len(leaf_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    # 각 리프 노드의 경계 텍스트 찾기
    processed_nodes = []
    
    for i, node in enumerate(leaf_nodes):
        print(f"\n🔍 노드 {i+1}/{len(leaf_nodes)} 분석: ID {node['id']} - \"{node['title']}\"")
        
        # 경계 텍스트 찾기
        start_text, end_text = find_text_boundaries(node, leaf_nodes, text_content, i)
        
        # 결과 노드 생성
        result_node = {
            'id': node['id'],
            'title': node['title'],
            'level': node['level'],
            'start_text': start_text,
            'end_text': end_text
        }
        
        processed_nodes.append(result_node)
        print(f"   ✅ start_text: \"{start_text}\"")
        print(f"   ✅ end_text: \"{end_text}\"")
    
    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_nodes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 직접 분석 완료! 결과: {output_file}")

def find_text_boundaries(node, all_nodes, text_content, node_index):
    """각 리프 노드의 시작/끝 텍스트 추출"""
    
    title = node['title']
    
    # 제목 정규화 (특수문자 처리)
    title_patterns = [
        title,
        title.replace('—', '-'),
        title.replace('–', '-'),
        title.replace('"', '"').replace('"', '"'),
        title.replace(''', "'").replace(''', "'")
    ]
    
    start_text = ""
    end_text = ""
    
    # 1. 시작 텍스트 찾기
    for pattern in title_patterns:
        if pattern in text_content:
            # 제목 위치 찾기
            title_pos = text_content.find(pattern)
            if title_pos != -1:
                # 제목 앞뒤 텍스트 추출 (15자 정도)
                start_pos = max(0, title_pos - 5)
                start_text = text_content[start_pos:title_pos + min(15, len(pattern))].strip()
                
                # 줄바꿈 제거
                start_text = start_text.replace('\n', ' ').replace('\r', '').strip()
                
                # 너무 긴 경우 자르기
                if len(start_text) > 20:
                    start_text = start_text[:20] + "..."
                
                break
    
    # 2. 끝 텍스트 찾기 (다음 노드의 제목 또는 적절한 구분점)
    if node_index < len(all_nodes) - 1:
        next_node = all_nodes[node_index + 1]
        end_text = get_next_title_text(next_node['title'], text_content)
    else:
        # 마지막 노드인 경우
        if "Summary" in title or "요약" in title:
            end_text = "Summary"
        else:
            # 적절한 종료 지점 찾기
            common_endings = ["Summary", "Conclusion", "## 페이지", "Part ", "Chapter"]
            for ending in common_endings:
                if ending in text_content:
                    end_text = ending
                    break
            
            if not end_text:
                end_text = "End of section"
    
    return start_text, end_text

def get_next_title_text(next_title, text_content):
    """다음 제목 텍스트 찾기"""
    
    # 다음 제목의 시작 부분 찾기
    next_patterns = [
        next_title,
        next_title.replace('—', '-'),
        next_title.replace('–', '-')
    ]
    
    for pattern in next_patterns:
        if pattern in text_content:
            # 제목의 첫 10-15자 반환
            short_title = pattern[:15] if len(pattern) > 15 else pattern
            return short_title.strip()
    
    # 찾지 못한 경우 원본 제목의 일부 반환
    return next_title[:10] + "..." if len(next_title) > 10 else next_title

if __name__ == "__main__":
    main()