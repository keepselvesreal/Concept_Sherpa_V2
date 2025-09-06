# 생성 시간: Mon Jan  2 17:20:00 KST 2025
# 핵심 내용: 실제 PDF 파일을 사용한 목차 추출 및 AI 장 식별 테스트
# 상세 내용:
#   - main (라인 15-60): 메인 테스트 실행 함수
#   - PDF 목차 추출 테스트
#   - AI 기반 장 식별 테스트
# 상태: active

import sys
import os
import json
from pathlib import Path

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def main():
    """실제 PDF로 목차 추출 및 AI 장 식별 테스트"""
    print("📖 실제 PDF 파일 테스트 시작")
    
    # PDF 파일 경로
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    
    # PDF 파일 존재 확인
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print(f"✅ PDF 파일 확인: {os.path.basename(pdf_path)}")
    
    # 모듈 임포트
    try:
        from src.refactoring_logger import RefactoringLogger
        from src.ai_providers import AIProviderFactory
        from src.toc_extractor import TocExtractor
        print("✅ 모듈 임포트 성공")
    except Exception as e:
        print(f"❌ 모듈 임포트 실패: {e}")
        return
    
    # 로거 및 AI Factory 초기화
    try:
        logger = RefactoringLogger(project_root / "logs")
        config_path = project_root / "config" / "ai_config.yaml"
        ai_factory = AIProviderFactory(str(config_path), logger)
        toc_extractor = TocExtractor(logger=logger, ai_factory=ai_factory)
        print("✅ 컴포넌트 초기화 성공")
    except Exception as e:
        print(f"❌ 컴포넌트 초기화 실패: {e}")
        return
    
    # 1단계: PDF 목차 추출
    print("\n🔍 1단계: PDF 목차 추출 중...")
    try:
        toc_result = toc_extractor.extract_toc(pdf_path)
        
        if toc_result.success:
            toc_count = len(toc_result.toc_data.get("toc_structure", []))
            print(f"✅ 목차 추출 성공: {toc_count}개 항목")
            
            # 목차 몇 개 샘플 출력
            toc_structure = toc_result.toc_data.get("toc_structure", [])
            print("📋 목차 샘플 (처음 5개):")
            for i, item in enumerate(toc_structure[:5]):
                print(f"  {i+1}. {item.get('title', 'N/A')} (페이지: {item.get('page', 'N/A')}, 레벨: {item.get('level', 'N/A')})")
            
        else:
            print(f"❌ 목차 추출 실패: {toc_result.error}")
            return
            
    except Exception as e:
        print(f"❌ 목차 추출 중 예외: {e}")
        return
    
    # 2단계: AI 기반 장 식별
    print("\n🤖 2단계: AI 기반 장 식별 중...")
    try:
        chapter_result = await toc_extractor.analyze_chapters_with_ai(toc_result.toc_data)
        
        if chapter_result.success:
            chapters_count = len(chapter_result.chapters_info)
            print(f"✅ 장 식별 성공: {chapters_count}개 장")
            
            # 식별된 장들 출력
            print("📚 식별된 장들:")
            for i, chapter in enumerate(chapter_result.chapters_info):
                title = chapter.get('title', 'N/A')
                start_page = chapter.get('start_page', 'N/A')
                end_page = chapter.get('end_page', 'N/A')
                print(f"  {i+1}. {title} (페이지: {start_page}-{end_page})")
            
        else:
            print(f"❌ 장 식별 실패: {chapter_result.error}")
            return
            
    except Exception as e:
        print(f"❌ 장 식별 중 예외: {e}")
        return
    
    print("\n🎉 모든 테스트 완료!")
    print(f"📁 로그 확인: {project_root / 'logs'}")
    
    # 로그 파일 확인
    log_files = list((project_root / "logs").rglob("*.log"))
    if log_files:
        print("📋 생성된 로그 파일들:")
        for log_file in log_files:
            print(f"  - {log_file.relative_to(project_root)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())