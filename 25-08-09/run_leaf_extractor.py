# 생성 시간: 2025-08-09 16:15:09
# 핵심 내용: 리프 노드 텍스트 추출 실행 스크립트
# 상세 내용:
#   - 실제 데이터 파일들을 사용하여 리프 노드 텍스트 추출 실행
#   - JSON 파일과 마크다운 파일 경로 설정 및 출력 디렉터리 생성
# 상태: 활성
# 주소: run_leaf_extractor
# 참조: leaf_text_extractor.py

from leaf_text_extractor import LeafTextExtractor
import os

def main():
    # 파일 경로 설정
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part2_scalability_leaf_nodes.json"
    markdown_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_leaf_texts"
    
    # 파일 존재 확인
    if not os.path.exists(json_path):
        print(f"❌ JSON 파일이 존재하지 않습니다: {json_path}")
        return
    
    if not os.path.exists(markdown_path):
        print(f"❌ 마크다운 파일이 존재하지 않습니다: {markdown_path}")
        return
    
    print("🚀 리프 노드 텍스트 추출 시작...")
    print(f"JSON 파일: {json_path}")
    print(f"마크다운 파일: {markdown_path}")
    print(f"출력 디렉터리: {output_dir}")
    print("-" * 60)
    
    # 추출기 실행
    extractor = LeafTextExtractor()
    extractor.process_all_leaf_nodes(json_path, markdown_path, output_dir)
    
    print("-" * 60)
    print("✅ 추출 완료!")

if __name__ == "__main__":
    main()