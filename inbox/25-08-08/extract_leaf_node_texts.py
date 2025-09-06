# 생성 시간: 2025-08-08 12:21:04 KST
# 핵심 내용: start_text와 end_text 정보를 활용해 전체 텍스트에서 각 리프 노드의 텍스트를 추출하여 개별 파일로 저장
# 상세 내용:
#   - main() 함수 (라인 9-43): 메인 실행 로직, 파일 읽기 및 텍스트 추출 조율
#   - extract_node_text() 함수 (라인 45-75): start_text와 end_text 사이의 텍스트 추출
#   - save_node_text() 함수 (라인 77-94): 추출된 텍스트를 개별 파일로 저장
#   - create_output_directory() 함수 (라인 96-103): 출력 디렉토리 생성
# 상태: 활성
# 주소: extract_leaf_node_texts
# 참조: leaf_nodes_with_text_boundaries (리프 노드 경계 정보)

import json
import os

def main():
    # 파일 경로 설정
    boundaries_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/leaf_nodes_with_text_boundaries.json'
    source_text_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md'
    output_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/extracted_leaf_texts'
    
    try:
        # 출력 디렉토리 생성
        create_output_directory(output_dir)
        
        # 리프 노드 경계 정보 읽기
        with open(boundaries_file, 'r', encoding='utf-8') as f:
            leaf_nodes = json.load(f)
        
        # 전체 텍스트 읽기
        with open(source_text_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        print(f"전체 텍스트 길이: {len(full_text)} 문자")
        
        # id 15까지의 리프 노드만 필터링
        target_nodes = [node for node in leaf_nodes if node['id'] <= 15]
        
        print(f"처리할 리프 노드 개수: {len(target_nodes)}개")
        
        # 각 리프 노드별 텍스트 추출 및 저장
        extracted_count = 0
        for node in target_nodes:
            extracted_text = extract_node_text(full_text, node)
            if extracted_text:
                save_node_text(node, extracted_text, output_dir)
                extracted_count += 1
                print(f"✅ ID {node['id']:2d}: {node['title'][:50]}... ({len(extracted_text)} 문자)")
            else:
                print(f"❌ ID {node['id']:2d}: {node['title'][:50]}... (텍스트 추출 실패)")
        
        print(f"\n총 {extracted_count}개 리프 노드의 텍스트가 추출되어 {output_dir}에 저장되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

def extract_node_text(full_text, node):
    """start_text와 end_text 사이의 텍스트 추출"""
    start_text = node['start_text']
    end_text = node['end_text']
    
    try:
        # start_text 위치 찾기
        start_pos = full_text.find(start_text)
        if start_pos == -1:
            print(f"   ⚠️  start_text를 찾을 수 없음: {start_text[:30]}...")
            return None
        
        # end_text 위치 찾기 (start_pos 이후에서)
        end_pos = full_text.find(end_text, start_pos + len(start_text))
        if end_pos == -1:
            # end_text를 찾을 수 없으면 다음 섹션 헤더나 파일 끝까지
            print(f"   ⚠️  end_text를 찾을 수 없음: {end_text[:30]}...")
            # 다음 번호 섹션이나 Summary를 찾기
            next_section_patterns = ['\n1.', '\n2.', '\nSummary', '\nCHAPTER']
            for pattern in next_section_patterns:
                temp_end = full_text.find(pattern, start_pos + len(start_text))
                if temp_end != -1:
                    end_pos = temp_end
                    break
            if end_pos == -1:
                end_pos = len(full_text)
        
        # 텍스트 추출
        extracted_text = full_text[start_pos:end_pos].strip()
        return extracted_text
        
    except Exception as e:
        print(f"   ❌ 텍스트 추출 중 오류: {e}")
        return None

def save_node_text(node, text, output_dir):
    """추출된 텍스트를 개별 파일로 저장"""
    try:
        # 파일명 생성 (안전한 파일명으로 변환)
        safe_title = node['title'].replace('/', '_').replace(':', '_').replace('?', '').replace('<', '').replace('>', '').replace('|', '_').replace('*', '_').replace('"', '_')
        filename = f"{node['id']:03d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        # 목차와 함께 저장
        content = f"""# 생성 시간: 2025-08-08 12:21:04 KST
# 핵심 내용: {node['title']} 섹션의 추출된 텍스트
# 상세 내용:
#   - 리프 노드 ID: {node['id']}
#   - 제목: {node['title']}
#   - 레벨: {node['level']}
#   - 텍스트 길이: {len(text)} 문자
# 상태: 활성
# 주소: extracted_leaf_text/{node['id']:03d}
# 참조: leaf_nodes_with_text_boundaries (경계 정보)

{text}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ 파일 저장 중 오류: {e}")

def create_output_directory(output_dir):
    """출력 디렉토리 생성"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"출력 디렉토리 생성/확인: {output_dir}")
    except Exception as e:
        print(f"디렉토리 생성 실패: {e}")
        raise

if __name__ == "__main__":
    main()