"""
생성 시간: 2025-08-18 13:15:42
핵심 내용: 검색 결과를 파일로 저장하는 스크립트
상세 내용:
    - main 함수 (라인 20-50): 검색 실행 및 결과 저장
    - save_results_to_files 함수 (라인 52-85): 개별 문서 파일 저장
    - 환경변수 로드 및 검색 엔진 초기화
상태: 
주소: save_search_results
참조: test_search_engine, document_search_engine
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from document_search_engine import DocumentSearchEngine

async def main():
    """검색 실행 및 결과 파일 저장"""
    # 환경변수 로드
    load_dotenv()
    
    # 검색 엔진 초기화
    search_engine = DocumentSearchEngine()
    await search_engine.initialize()
    
    # 테스트 질의 실행
    query = "ai 코딩의 문제점 해결 도구들에 대해 알고 싶어"
    print(f"🔍 검색 질의: {query}")
    
    results = await search_engine.search(query)
    print(f"📊 검색 결과: {len(results)}개 문서")
    
    # 결과 저장
    if results:
        await save_results_to_files(results)
        print(f"✅ {len(results)}개 문서가 파일로 저장되었습니다.")
    else:
        print("❌ 저장할 결과가 없습니다.")
    
    # 리소스 정리
    await search_engine.close()

async def save_results_to_files(results):
    """검색 결과를 개별 파일로 저장"""
    # 결과 저장 디렉토리 생성
    output_dir = Path("search_results")
    output_dir.mkdir(exist_ok=True)
    
    for i, doc in enumerate(results, 1):
        # 파일명 생성 (안전한 파일명으로 변환)
        safe_title = "".join(c for c in doc.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"{i:02d}_{safe_title}.md"
        
        file_path = output_dir / filename
        
        # 문서 내용 저장 (반환 결과 그대로)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc.formatted_content)
        
        print(f"💾 저장됨: {file_path}")

if __name__ == "__main__":
    asyncio.run(main())