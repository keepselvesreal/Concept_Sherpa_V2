# 생성 시간: 2025-09-01 15:42:25 KST
# 핵심 내용: 수정된 북 파이프라인 테스트 스크립트
# 상세 내용:
#   - test_book_pipeline (라인 15-30): 1장 테스트 모드로 파이프라인 실행
# 상태: active

import asyncio
import sys
import os

# 경로 설정
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')

from book_pipeline_v3 import BookPipeline

async def test_book_pipeline(pdf_path: str):
    """북 파이프라인 테스트 실행"""
    print("📚 북 파이프라인 테스트 시작...")
    print(f"📄 PDF 경로: {pdf_path}")
    print("🧪 테스트 모드: 1장만 처리")
    print("-" * 60)
    
    try:
        # 테스트 모드로 파이프라인 실행
        pipeline = BookPipeline(test_mode=True)
        result = await pipeline.execute(pdf_path)
        
        print("\n" + "=" * 60)
        print("📊 실행 결과:")
        print(f"✅ 성공: {result.get('success', False)}")
        print(f"📊 처리된 장: {result.get('chapters_processed', 0)}개")
        if 'error' in result:
            print(f"❌ 오류: {result['error']}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 테스트 실행 오류: {str(e)}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # PDF 경로
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    # 테스트 실행
    asyncio.run(test_book_pipeline(pdf_path))