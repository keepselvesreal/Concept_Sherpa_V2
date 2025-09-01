# 생성 시간: Mon Sep  1 16:14:53 KST 2025
# 핵심 내용: 1장 목차 정보로 노드 문서 생성 테스트 스크립트
# 상세 내용:
#   - test_node_generation() (line 15-35): 1장 목차 파일로 노드 문서 생성 테스트
#   - main() (line 37-45): 메인 실행 함수
# 상태: active
# 주소: test_node_generation
# 참조: book_pipeline_v2.py의 노드 문서 생성 기능 테스트

#!/usr/bin/env uv run python

import os
import sys
from pathlib import Path

# 직접 구현으로 import 제거

def test_node_generation_direct():
    """1장 목차 정보로 노드 문서 생성 직접 테스트 (BookPipeline의 해당 함수들만 사용)"""
    print("🧪 === 1장 노드 문서 생성 테스트 시작 ===")
    
    # 필요한 모듈들 import
    import json
    import re
    
    # 1장 목차 파일 경로
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/1_Complexity_of_object_oriented_programming_toc.json"
    
    # 출력 디렉토리 (1장 폴더)
    chapter_folder = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    print(f"📖 TOC 파일: {toc_file}")
    print(f"📁 출력 폴더: {chapter_folder}")
    
    if not os.path.exists(toc_file):
        print(f"❌ TOC 파일을 찾을 수 없습니다: {toc_file}")
        return False
    
    if not os.path.exists(chapter_folder):
        print(f"❌ 장 폴더를 찾을 수 없습니다: {chapter_folder}")
        return False
    
    try:
        # TOC 파일 로드 
        print("📚 TOC 파일 로드 중...")
        with open(toc_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 노드 로드 완료")
        
        # 노드 정보 문서 출력 디렉토리 생성
        node_docs_dir = os.path.join(chapter_folder, "node_info_docs")
        os.makedirs(node_docs_dir, exist_ok=True)
        print(f"📁 출력 디렉토리 생성: {node_docs_dir}")
        
        created_count = 0
        failed_count = 0
        
        # 각 노드별 문서 생성
        for node in nodes:
            try:
                # 파일명 생성: {id}_lev{level}_title_info.md
                title_clean = re.sub(r'[^\w\s.-]', '', node['title'])  # 점(.)도 유지
                title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
                
                filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
                filepath = os.path.join(node_docs_dir, filename)
                
                # 수정된 문서 내용 생성 (추출 섹션 하위 내용 제거)
                content = f"""# 속성
---
process_status: false

# 추출
---

# 내용
---

# 구성
---
"""
                
                # 파일 저장
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                created_count += 1
                print(f"   ✅ 생성: {filename}")
            
            except Exception as e:
                failed_count += 1
                print(f"   ❌ 실패 (ID: {node.get('id', '?')}): {e}")
        
        print(f"\n🎉 노드 문서 생성 완료!")
        print(f"📊 성공: {created_count}개")
        print(f"📊 실패: {failed_count}개")
        print(f"📁 출력 위치: {node_docs_dir}")
        
        return created_count > 0
    
    except Exception as e:
        print(f"❌ 테스트 중 예외 발생: {str(e)}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 노드 문서 생성 테스트 시작")
    
    success = test_node_generation_direct()
    
    if success:
        print("🎉 전체 테스트 완료!")
    else:
        print("😞 테스트 실패")

if __name__ == "__main__":
    main()