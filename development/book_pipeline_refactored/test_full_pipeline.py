#!/usr/bin/env python3
# 생성 시간: 2025년 09월 02일 17시 15분
# 핵심 내용: 전체 북 파이프라인 테스트 스크립트 - 목차 추출부터 장별 폴더 생성까지 완전한 플로우 테스트
# 상세 내용:
#   - 환경 설정 및 임포트 (라인 10-20): 시스템 패스 추가 및 필요한 모듈 임포트
#   - test_full_pipeline (라인 22-55): 전체 파이프라인 테스트 함수
#   - 메인 실행부 (라인 57-70): 스크립트 실행 및 결과 출력
# 상태: active
# 참조: 새로 생성된 파일

import sys
import os
from pathlib import Path

# 프로젝트 경로 설정
project_root = Path(__file__).parent
sys.path.append(str(project_root / 'src'))

from toc_extractor import TocExtractor
from refactoring_logger import RefactoringLogger
from ai_providers import AIProviderFactory

def test_full_pipeline():
    """전체 파이프라인 테스트"""
    
    # 테스트 설정
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    log_dir = project_root / "logs"
    extraction_base = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system"
    
    print("🚀 북 파이프라인 전체 테스트 시작")
    print("=" * 60)
    print(f"📄 PDF: {Path(pdf_path).name}")
    print(f"📁 추출 경로: {extraction_base}")
    print("=" * 60)
    
    try:
        # 컴포넌트 초기화
        logger = RefactoringLogger(log_dir)
        
        # config 파일 경로 설정 (없으면 기본값 사용)
        config_path = project_root / "config" / "ai_providers.yaml"
        if not config_path.exists():
            # 기본 설정으로 생성
            config_path.parent.mkdir(parents=True, exist_ok=True)
            default_config = {
                'default_provider': 'gemini',
                'providers': {
                    'gemini': {
                        'model': 'gemini-2.0-flash-lite',
                        'api_key_env': 'GEMINI_API_KEY'
                    }
                }
            }
            import yaml
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f)
        
        ai_factory = AIProviderFactory(config_path, logger=logger)
        
        toc_extractor = TocExtractor(logger=logger, ai_factory=ai_factory)
        
        # 전체 파이프라인 실행
        result = toc_extractor.organize_chapters(pdf_path, extraction_base)
        
        # 결과 출력
        if result["success"]:
            print("\n🎉 파이프라인 성공!")
            print(f"📚 책 디렉토리: {result['book_info']['book_directory']}")
            print(f"📖 생성된 장 수: {result['book_info']['total_chapters']}")
            
            print("\n📊 단계별 결과:")
            stages = result["pipeline_stages"]
            print(f"  1. 목차 추출: {stages['toc_extraction']['total_toc_items']}개 항목")
            print(f"  2. 장 식별: {stages['chapter_identification']['total_chapters']}개 장")
            print(f"  3. 폴더 생성: {stages['chapter_organization']['created_chapters']}개 장 폴더")
            
            return True
        else:
            print(f"\n❌ 파이프라인 실패: {result.get('error', '알 수 없는 오류')}")
            return False
            
    except Exception as e:
        print(f"\n💥 예외 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📖 Book Pipeline Refactored - 전체 테스트")
    print("=" * 60)
    
    success = test_full_pipeline()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 테스트 성공!")
    else:
        print("❌ 테스트 실패!")
    print("=" * 60)