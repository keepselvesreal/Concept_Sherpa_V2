# 생성 시간: Mon Sep  1 16:50:25 KST 2025
# 핵심 내용: 1장 디렉토리 기반 DocumentIntegrator 동작 점검 테스트
# 상세 내용:
#   - test_document_integration() (line 15-50): 1장 디렉토리로 문서 통합 테스트
#   - main() (line 52-60): 메인 실행 함수
# 상태: active
# 주소: test_document_integration
# 참조: document_integrator.py 모듈 테스트

#!/usr/bin/env uv run python

import os
import sys
from pathlib import Path

# pipeline 모듈 경로 추가
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')
from document_integrator import DocumentIntegrator

def test_document_integration():
    """1장 디렉토리로 DocumentIntegrator 동작 점검 테스트"""
    print("🧪 === DocumentIntegrator 동작 점검 테스트 시작 ===")
    
    # 1장 디렉토리 경로
    chapter_folder = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    print(f"📁 테스트 대상 폴더: {chapter_folder}")
    
    if not os.path.exists(chapter_folder):
        print(f"❌ 장 폴더를 찾을 수 없습니다: {chapter_folder}")
        return False
    
    try:
        # DocumentIntegrator 인스턴스 생성
        integrator = DocumentIntegrator()
        
        # 문서 통합 실행
        print("🔗 문서 통합 실행 중...")
        result = integrator.integrate_documents_for_chapter(chapter_folder)
        
        if result.get('success', False):
            print(f"✅ 테스트 성공!")
            print(f"📊 통합된 문서 수: {result.get('integrated_count', 0)}")
            print(f"📊 전체 노드 수: {result.get('total_nodes', 0)}")
            print(f"📄 사용된 TOC 파일: {os.path.basename(result.get('toc_file_used', ''))}")
            print(f"📁 처리된 폴더: {result.get('chapter_folder', '')}")
            
            # 통합된 파일 중 하나 확인해보기
            node_docs_dir = os.path.join(chapter_folder, "node_info_docs")
            if os.path.exists(node_docs_dir):
                sample_files = [f for f in os.listdir(node_docs_dir) if f.endswith('_info.md')][:3]
                if sample_files:
                    print(f"📋 통합된 샘플 파일들:")
                    for sample_file in sample_files:
                        print(f"   - {sample_file}")
            
            return True
        else:
            print(f"❌ 테스트 실패: {result.get('error', '알 수 없는 오류')}")
            return False
    
    except Exception as e:
        print(f"❌ 테스트 중 예외 발생: {str(e)}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 DocumentIntegrator 동작 점검 테스트 시작")
    
    success = test_document_integration()
    
    if success:
        print("🎉 전체 테스트 완료!")
    else:
        print("😞 테스트 실패")

if __name__ == "__main__":
    main()