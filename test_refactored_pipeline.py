# 생성 시간: Mon Sep  1 16:30:15 KST 2025
# 핵심 내용: 리팩토링된 NodeDocumentGenerator를 사용한 노드 문서 생성 테스트
# 상세 내용:
#   - test_refactored_node_generation() (line 15-50): 리팩토링된 모듈 테스트
#   - main() (line 52-60): 메인 실행 함수
# 상태: active
# 주소: test_refactored_pipeline
# 참조: node_document_generator.py 모듈 테스트

#!/usr/bin/env uv run python

import os
import sys
from pathlib import Path

# pipeline 모듈 경로 추가
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')
from node_document_generator import NodeDocumentGenerator

def test_refactored_node_generation():
    """리팩토링된 NodeDocumentGenerator를 사용한 노드 문서 생성 테스트"""
    print("🧪 === 리팩토링된 노드 문서 생성 테스트 시작 ===")
    
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
        # NodeDocumentGenerator 인스턴스 생성
        generator = NodeDocumentGenerator()
        
        # 노드 문서 생성 실행
        print("📋 노드 문서 생성 중...")
        result = generator.generate_documents_for_chapter(chapter_folder, toc_file)
        
        if result.success:
            print(f"✅ 테스트 성공!")
            print(f"📊 생성된 문서 수: {result.created_count}")
            print(f"📊 실패 문서 수: {result.failed_count}")
            print(f"📊 전체 노드 수: {result.total_nodes}")
            print(f"📁 출력 디렉토리: {result.output_dir}")
            print(f"📄 생성된 파일들:")
            for created_file in result.created_files:
                print(f"   - {os.path.basename(created_file)}")
            return True
        else:
            print(f"❌ 테스트 실패: {result.error}")
            return False
    
    except Exception as e:
        print(f"❌ 테스트 중 예외 발생: {str(e)}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 리팩토링된 파이프라인 테스트 시작")
    
    success = test_refactored_node_generation()
    
    if success:
        print("🎉 전체 테스트 완료!")
    else:
        print("😞 테스트 실패")

if __name__ == "__main__":
    main()