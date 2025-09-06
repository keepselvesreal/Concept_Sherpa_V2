"""
생성 시간: 2025-08-18 12:22:54
핵심 내용: DocumentSearchEngine 테스트 스크립트
상세 내용:
    - test_search_engine 함수 (라인 25-70): 메인 테스트 실행 함수
    - setup_environment 함수 (라인 72-90): 환경 설정 및 로깅 초기화
    - print_search_results 함수 (라인 92-120): 검색 결과 출력 함수
    - 테스트 질의: "ai 코딩의 문제점 해결 도구들에 대해 알고 싶어"
상태: 
주소: test_search_engine
참조: document_search_engine
"""

import asyncio
import logging
import os
import sys
from typing import List

# 프로젝트 루트를 파이썬 패스에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv('/home/nadle/projects/Knowledge_Sherpa/v2/.env')

from document_search_engine import DocumentSearchEngine, ReconstructedDocument

def setup_environment():
    """환경 설정 및 로깅 초기화"""
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('search_engine_test.log')
        ]
    )
    
    # 환경 변수 확인
    required_env_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'NEON_DATABASE_URL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️ 누락된 환경 변수: {', '.join(missing_vars)}")
        print("테스트를 계속 진행하지만 일부 기능이 제한될 수 있습니다.")
    else:
        print("✅ 모든 환경 변수 확인 완료")

async def test_search_engine():
    """
    DocumentSearchEngine 테스트 실행
    질의: "ai 코딩의 문제점 해결 도구들에 대해 알고 싶어"
    """
    logger = logging.getLogger(__name__)
    
    print("🚀 DocumentSearchEngine 테스트 시작")
    print("=" * 60)
    
    # 검색 엔진 초기화
    search_engine = DocumentSearchEngine()
    
    try:
        print("📡 검색 엔진 초기화 중...")
        await search_engine.initialize(project_name="knowledge_sherpa")
        print("✅ 검색 엔진 초기화 완료")
        
        # 시스템 상태 확인
        print("\n🔍 시스템 상태 확인 중...")
        status = await search_engine.get_system_status()
        print(f"  - 데이터베이스 연결: {'✅' if status.get('database_connected') else '❌'}")
        print(f"  - 컴포넌트 초기화: {'✅' if status.get('components_initialized') else '❌'}")
        print(f"  - 데이터베이스 상태: {status.get('database_status', 'unknown')}")
        
        # 테스트 질의 실행
        test_query = "ai 코딩의 문제점 해결 도구들에 대해 알고 싶어"
        print(f"\n🔎 테스트 질의 실행: '{test_query}'")
        print("-" * 60)
        
        # 검색 실행
        results = await search_engine.search(
            query=test_query,
            project_name="knowledge_sherpa",
            max_results=3
        )
        
        # 결과 출력
        print(f"\n📊 검색 결과: {len(results)}개 문서 발견")
        print("=" * 60)
        
        if results:
            print_search_results(results)
        else:
            print("❌ 검색 결과가 없습니다.")
            print("\n🔍 원인 분석:")
            print("  1. 데이터베이스에 해당 내용의 문서가 없을 수 있습니다")
            print("  2. 임계값(similarity_threshold)이 너무 높을 수 있습니다")
            print("  3. 임베딩 테이블에 데이터가 없을 수 있습니다")
        
        # 최종 통계
        final_stats = search_engine.search_stats
        print(f"\n📈 검색 통계:")
        print(f"  - 총 검색 횟수: {final_stats['total_searches']}")
        print(f"  - 평균 검색 시간: {final_stats['avg_search_time']:.2f}초")
        print(f"  - 성공률: {final_stats['success_rate']:.1f}%")
        
    except Exception as e:
        logger.error(f"테스트 실행 오류: {e}")
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        
    finally:
        print("\n🔄 리소스 정리 중...")
        try:
            await search_engine.close()
            print("✅ 리소스 정리 완료")
        except Exception as e:
            print(f"⚠️ 리소스 정리 중 오류: {e}")
        
        print("\n🏁 테스트 완료")

def print_search_results(results: List[ReconstructedDocument]):
    """검색 결과를 보기 좋게 출력"""
    for i, doc in enumerate(results, 1):
        print(f"\n📄 문서 {i}: {doc.title}")
        print(f"   🎯 유사도: {doc.similarity_score:.4f}")
        print(f"   🔍 검색 차원: {doc.search_dimension}")
        print(f"   📝 문서 ID: {doc.document_id}")
        
        # 메타데이터 출력
        metadata = doc.metadata
        print(f"   📂 소스 타입: {metadata.get('source_type', 'unknown')}")
        print(f"   🌐 언어: {metadata.get('document_language', 'unknown')}")
        print(f"   🏗️ 구조 타입: {metadata.get('structure_type', 'unknown')}")
        
        # 문서 내용 미리보기 (처음 200자)
        content_preview = doc.formatted_content.replace('\n', ' ')[:200]
        print(f"   📖 내용 미리보기: {content_preview}...")
        
        print("-" * 40)

async def main():
    """메인 실행 함수"""
    setup_environment()
    await test_search_engine()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n💥 예상치 못한 오류 발생: {e}")
        sys.exit(1)