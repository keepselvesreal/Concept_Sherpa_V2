# 생성 시간: 2025-09-01 15:05:20 KST
# 핵심 내용: 정확한 참조 로직 기반 콘텐츠 노드 분석 테스트
# 상세 내용:
#   - test_single_chapter (라인 15-65): 개별 장 TOC 분석 테스트 (참조 로직 정확 적용)
#   - main (라인 67-85): 메인 실행 함수
# 상태: active

import os
import sys
import asyncio
from pathlib import Path

# 파이프라인 모듈 임포트
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system')
from pipeline.content_node_analyzer import ContentNodeAnalyzer

async def test_single_chapter():
    """개별 장의 콘텐츠 노드 분석 및 파일 추출 테스트 (참조 로직 정확 적용)"""
    
    # 테스트할 장 정보
    chapter_toc_path = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/1_Complexity_of_object_oriented_programming_toc.json"
    content_nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/content_nodes.json"
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    print("🧪 === 콘텐츠 노드 분석 및 추출 테스트 시작 (참조 로직 정확 적용) ===")
    print(f"📄 TOC 파일: {chapter_toc_path}")
    print(f"📄 Content nodes: {content_nodes_path}")
    print(f"📖 PDF 파일: {pdf_path}")
    
    # 파일 존재 확인
    if not os.path.exists(chapter_toc_path):
        print(f"❌ TOC 파일이 없습니다: {chapter_toc_path}")
        return False
        
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일이 없습니다: {pdf_path}")
        return False
    
    try:
        # ContentNodeAnalyzer 초기화 (로깅 포함)
        analyzer = ContentNodeAnalyzer(config_path="extraction_config.yaml")
        
        # 1단계: 콘텐츠 노드가 없으면 분석부터
        if not os.path.exists(content_nodes_path):
            print("\\n1️⃣ 콘텐츠 노드 분석 실행 중... (content_node_extractor_v3.py 로직)")
            result = await analyzer.analyze_chapter_toc(chapter_toc_path, pdf_path)
            
            if not result.get('success', False):
                print(f"❌ 분석 실패: {result.get('error', 'Unknown error')}")
                return False
            
            print(f"✅ 분석 성공!")
            print(f"📊 전체 항목: {result.get('total_items', 0)}개")
            print(f"📝 콘텐츠 노드: {result.get('content_nodes_count', 0)}개")
        
        # 2단계: 실제 콘텐츠 파일 추출
        print("\\n2️⃣ 콘텐츠 파일 추출 실행 중... (content_extractor.py 로직)")
        extraction_result = await analyzer.extract_content_nodes_to_files(content_nodes_path, pdf_path)
        
        if extraction_result.get('success', False):
            print(f"✅ 콘텐츠 추출 성공!")
            print(f"📊 전체 노드: {extraction_result.get('total_nodes', 0)}개")
            print(f"📄 추출된 파일: {extraction_result.get('successful_extractions', 0)}개")
            return True
        else:
            print(f"❌ 콘텐츠 추출 실패: {extraction_result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 테스트 실행 오류: {str(e)}")
        return False

async def main():
    """메인 실행 함수"""
    print("🚀 콘텐츠 노드 분석 테스트 실행 (참조 로직 정확 적용)")
    
    success = await test_single_chapter()
    
    if success:
        print("\\n🎉 테스트 완료!")
        print("\\n📁 로그 확인:")
        print("   tail -f /home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs/content_analysis.log")
    else:
        print("\\n💥 테스트 실패!")
        print("\\n📁 로그 확인:")
        print("   tail -f /home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs/content_analysis.log")
        sys.exit(1)

if __name__ == "__main__":
    # 환경변수 로드
    try:
        from dotenv import load_dotenv
        load_dotenv("/home/nadle/projects/Knowledge_Sherpa/v2/.env")
        print("✅ 환경변수 로드 완료")
    except ImportError:
        print("⚠️ python-dotenv가 설치되지 않음")
    
    asyncio.run(main())