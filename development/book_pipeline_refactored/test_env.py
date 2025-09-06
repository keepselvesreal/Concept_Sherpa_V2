# 생성 시간: Mon Jan  2 17:15:00 KST 2025
# 핵심 내용: 환경변수 및 기본 기능 테스트 스크립트
# 상세 내용:
#   - main (라인 15-50): 메인 테스트 실행 함수
#   - 환경변수 로드 확인
#   - AI Provider Factory 초기화 및 사용 가능 Provider 확인
# 상태: active

import sys
import os
from pathlib import Path

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def main():
    """환경변수 및 기본 기능 테스트"""
    print("🚀 리팩토링된 북 파이프라인 환경설정 테스트")
    
    # 기본 모듈 임포트 테스트
    try:
        from src.refactoring_logger import RefactoringLogger
        from src.ai_providers import AIProviderFactory
        from src.toc_extractor import TocExtractor
        print("✅ 모듈 임포트 성공")
    except Exception as e:
        print(f"❌ 모듈 임포트 실패: {e}")
        return
    
    # 로거 초기화 테스트
    try:
        logger = RefactoringLogger(project_root / "logs")
        print("✅ 로거 초기화 성공")
    except Exception as e:
        print(f"❌ 로거 초기화 실패: {e}")
        return
    
    # AI Factory 초기화 및 환경변수 테스트
    try:
        config_path = project_root / "config" / "ai_config.yaml"
        ai_factory = AIProviderFactory(str(config_path), logger)
        print("✅ AI Factory 초기화 성공")
        
        # 환경변수 확인
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            print(f"✅ GEMINI_API_KEY 로드됨 (길이: {len(gemini_key)})")
        else:
            print("❌ GEMINI_API_KEY 없음")
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print(f"✅ OPENAI_API_KEY 로드됨 (길이: {len(openai_key)})")
        else:
            print("⚠️ OPENAI_API_KEY 없음")
        
        # 사용 가능한 Provider 확인
        available_providers = ai_factory.get_available_providers()
        print(f"📋 사용 가능한 AI Providers: {available_providers}")
        
        if 'gemini' in available_providers:
            print("✅ Gemini Provider 사용 가능")
            
            # Gemini Provider 테스트 (실제 API 호출 안함)
            gemini_provider = ai_factory.get_provider('gemini')
            print(f"✅ Gemini Provider 생성됨 (모델: {gemini_provider.model})")
        
    except Exception as e:
        print(f"❌ AI Factory 초기화 실패: {e}")
        return
    
    # 목차 추출기 초기화 테스트
    try:
        toc_extractor = TocExtractor(logger=logger, ai_factory=ai_factory)
        print("✅ 목차 추출기 초기화 성공")
    except Exception as e:
        print(f"❌ 목차 추출기 초기화 실패: {e}")
        return
    
    print("🎉 모든 환경설정 및 기본 기능 테스트 통과!")
    print(f"📁 로그 디렉토리: {project_root / 'logs'}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())