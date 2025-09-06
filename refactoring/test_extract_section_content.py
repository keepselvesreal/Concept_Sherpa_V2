# 생성 시간: Sat Sep  6 11:37:33 KST 2025
# 핵심 내용: extract_section_content 실제 동작 검증 테스트
# 상세 내용:
#   - test_extract_section_content (라인 15-80): 메인 테스트 함수
#   - load_test_data (라인 82-95): 테스트 데이터 로드 함수
#   - create_sample_content_sections (라인 97-110): 샘플 content_sections 생성
# 상태: active

import asyncio
import json
import sys
import os
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 실제 모듈들 import (mock 사용 안함)
from src.services.content_document_service_v4 import ContentDocumentService
from src.utils.config_manager import ConfigManager
import logging

async def test_extract_section_content_with_provider(provider_name="gemini"):
    """특정 AI 제공자로 extract_section_content 테스트"""
    print(f"🚀 **extract_section_content 테스트 시작 ({provider_name})**\n")
    
    try:
        # 테스트 데이터 로드
        chapter_content, content_sections = load_test_data()
        
        # 🔍 **입력 데이터 확인**
        print(f"📥 **테스트 입력 확인**:")
        print(f"   - 장 내용 길이: {len(chapter_content)} 문자")
        print(f"   - has_content=True 섹션 수: {len(content_sections)}개")
        print(f"   - 첫 3개 섹션: {[s['title'] for s in content_sections[:3]]}")
        print()
        
        # 실제 ConfigManager와 Logger 사용
        config_manager = ConfigManager()
        
        # 간단한 로거 설정
        logger = logging.getLogger("test_extract_section_content")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        # 특정 제공자로 설정 임시 변경
        original_config = config_manager.ai_config.copy()
        if provider_name == "claude":
            config_manager.ai_config["stage_specific_ai"]["information_integration"]["extract_section_content"] = {
                "provider": "claude",
                "model": "claude-3-5-sonnet-20241022", 
                "temperature": 0.1,
                "max_tokens": 8192
            }
        elif provider_name == "openai":
            config_manager.ai_config["stage_specific_ai"]["information_integration"]["extract_section_content"] = {
                "provider": "openai",
                "model": "gpt-4-turbo-preview",
                "temperature": 0.1
            }
        # gemini는 기본 설정 그대로 사용
        
        # ContentDocumentService 초기화
        service = ContentDocumentService(config_manager, logger)
        print("✅ **ContentDocumentService 초기화 완료**\n")
        
        # extract_section_content 실행 (처음 3개 섹션만 테스트)
        print(f"🔄 **extract_section_content 실행 중 ({provider_name})**")
        extracted_sections = await service.extract_section_content(
            content_sections=content_sections[:3],  # 처음 3개 섹션만 (빠른 테스트)
            chapter_content=chapter_content,
            stage_name="test_extraction"
        )
        
        # 🔍 **결과 확인**
        print(f"\n📊 **추출 결과 확인**:")
        print(f"   - 추출된 섹션 수: {len(extracted_sections)}개")
        
        for i, section in enumerate(extracted_sections, 1):
            print(f"\n📄 **섹션 {i}**: {section['section_title']}")
            print(f"   - 섹션 ID: {section['section_id']}")
            print(f"   - 내용 길이: {section['content_length']} 문자")
            print(f"   - 첫 100자: {section['extracted_content'][:100]}...")
        
        # sections 폴더에 저장 테스트 - 제공자별 폴더에 저장
        base_test_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
        test_output_dir = os.path.join(base_test_dir, f"sections_{provider_name}")
        os.makedirs(test_output_dir, exist_ok=True)
        
        print(f"\n💾 **파일 저장 테스트**: {test_output_dir}")
        service._save_section_files(extracted_sections, test_output_dir)
        
        # 저장된 파일들 확인
        sections_dir = os.path.join(test_output_dir, "sections")
        if os.path.exists(sections_dir):
            saved_files = os.listdir(sections_dir)
            print(f"✅ **저장된 파일**: {len(saved_files)}개")
            for filename in saved_files:
                file_path = os.path.join(sections_dir, filename)
                file_size = os.path.getsize(file_path)
                print(f"   - {filename} ({file_size} bytes)")
        
        print(f"\n🎉 **테스트 성공 완료!**")
        return True
        
    except Exception as e:
        print(f"\n❌ **테스트 실패**: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def load_test_data():
    """테스트 데이터 로드"""
    test_data_dir = Path(__file__).parent / "tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    # 장 내용 로드
    content_file = test_data_dir / "1_Complexity_of_object_oriented_programming_content.md"
    with open(content_file, 'r', encoding='utf-8') as f:
        chapter_content = f.read()
    
    # content.json 로드 (has_content=True만 필터링)
    content_json_file = test_data_dir / "content.json"
    with open(content_json_file, 'r', encoding='utf-8') as f:
        all_sections = json.load(f)
    
    content_sections = [s for s in all_sections if s.get('has_content', False)]
    
    return chapter_content, content_sections

async def test_all_providers():
    """모든 AI 제공자 테스트"""
    providers = ["gemini", "claude", "openai"]
    results = {}
    
    print("🌟 **모든 AI 제공자 테스트 시작**\n")
    
    for provider in providers:
        try:
            print(f"{'='*50}")
            result = await test_extract_section_content_with_provider(provider)
            results[provider] = "성공" if result else "실패"
            print(f"{'='*50}\n")
        except Exception as e:
            results[provider] = f"실패: {str(e)}"
            print(f"❌ **{provider} 테스트 실패**: {str(e)}")
            print(f"{'='*50}\n")
    
    # 전체 결과 요약
    print("📋 **전체 테스트 결과 요약**:")
    for provider, result in results.items():
        status = "✅" if result == "성공" else "❌"
        print(f"   {status} {provider}: {result}")
    
    success_count = sum(1 for result in results.values() if result == "성공")
    total_count = len(providers)
    
    print(f"\n🎯 **최종 결과**: {success_count}/{total_count} 제공자 성공")
    
    return success_count > 0

if __name__ == "__main__":
    # 모든 제공자 테스트 실행
    success = asyncio.run(test_all_providers())
    
    if success:
        print("\n🎉 **전체 테스트 완료**")
        exit(0)
    else:
        print("\n💥 **전체 테스트 실패**")
        exit(1)