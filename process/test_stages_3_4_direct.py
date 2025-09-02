# 생성 시간: 2025-09-01 21:35:00 KST  
# 핵심 내용: process 폴더에서 3단계, 4단계 독립 테스트 스크립트
# 상세 내용:
#   - test_stage_3_only (라인 25-80): 3단계 노드 정보 문서 처리만 테스트
#   - test_stage_4_only (라인 82-120): 4단계 enhanced_chapter_toc.md 생성만 테스트  
#   - main (라인 122-150): 메인 실행 함수
# 상태: active
# 주소: test_stages_3_4_direct
# 참조: unified_node_processor_v4.py, chapter_toc_generator.py

import asyncio
import os
import sys
import logging
import yaml
import tempfile
from pathlib import Path

# 필요한 모듈 임포트
from unified_node_processor_v4 import UnifiedNodeProcessor
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/components')
from chapter_toc_generator import combine_extracts

async def test_stage_3_only():
    """3단계: 노드 정보 문서 처리만 테스트"""
    print("🧪 === 3단계 독립 테스트: 노드 정보 문서 처리 ===")
    
    # 테스트 대상 폴더
    chapter_folder = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    # unified_node_processor_v4에 맞는 config 생성 (flat 구조)
    config = {
        'ai_provider': 'gemini',
        'processing_mode': 'v3',
        'nodes_json_path': f"{chapter_folder}/1_Complexity_of_object_oriented_programming_toc.json",
        'node_docs_dir': f"{chapter_folder}/node_info_docs",
        'debug_dir': "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs",
        
        # 병렬 처리 설정
        'parallel': {
            'max_concurrent': 3
        },
        
        # 로깅 설정
        'logging': {
            'level': 'INFO',
            'save_logs': True
        },
        
        # AI 모델 설정
        'models': {
            'claude': "claude-3-sonnet-20240229",
            'gemini': "gemini-2.5-flash",  # 요청한 모델
            'openai': "gpt-4"
        },
        
        # 프로바이더별 상세 설정
        'providers': {
            'gemini': {
                'model': 'gemini-2.5-flash',
                'temperature': 0.7
            },
            'claude': {
                'model': 'claude-3-sonnet'
            },
            'openai': {
                'model': 'gpt-4',
                'temperature': 0.7
            }
        }
    }
    
    # 로그 디렉토리 생성
    os.makedirs("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs", exist_ok=True)
    
    # 임시 config 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as temp_config:
        yaml.dump(config, temp_config, default_flow_style=False, indent=2, allow_unicode=True)
        temp_config_path = temp_config.name
    
    try:
        print(f"🔧 임시 config 파일: {temp_config_path}")
        print(f"🎯 대상 폴더: {chapter_folder}")
        print(f"🤖 AI 모델: {config['ai_provider']} (gemini-2.5-flash)")
        
        # UnifiedNodeProcessor 초기화
        print("🚀 UnifiedNodeProcessor 초기화 중...")
        processor = UnifiedNodeProcessor(temp_config_path)
        
        # 노드 처리 실행
        print("⚡ 노드 처리 실행 중...")
        result = await processor.process_all_nodes()
        
        # 결과 출력
        if result.get('success'):
            print("✅ 3단계 성공!")
            print(f"📊 처리된 노드: {result.get('processed_nodes')}")
            print(f"⏱️ 소요 시간: {result.get('duration')}")
            
            # 에러가 있다면 표시
            if result.get('errors'):
                print("⚠️ 경고/오류:")
                for error in result.get('errors', [])[:3]:  # 처음 3개만 표시
                    print(f"  - {error}")
            
            return True
        else:
            print(f"❌ 3단계 실패!")
            print(f"📊 실패 노드: {result.get('failed_nodes')}")
            if result.get('errors'):
                print("오류 목록:")
                for error in result.get('errors', [])[:5]:  # 처음 5개만 표시
                    print(f"  - {error}")
            return False
            
    except Exception as e:
        print(f"❌ 3단계 테스트 중 예외: {e}")
        return False
    finally:
        # 임시 파일 정리
        if os.path.exists(temp_config_path):
            os.unlink(temp_config_path)

def test_stage_4_only():
    """4단계: enhanced_chapter_toc.md 생성만 테스트"""
    print("\n🧪 === 4단계 독립 테스트: enhanced_chapter_toc.md 생성 ===")
    
    # 노드 정보 문서 폴더
    node_docs_folder = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/node_info_docs"
    
    try:
        # 폴더 존재 확인
        if not os.path.exists(node_docs_folder):
            print(f"❌ 노드 정보 문서 폴더를 찾을 수 없음: {node_docs_folder}")
            return False
        
        print(f"🎯 대상 폴더: {node_docs_folder}")
        
        # combine_extracts 함수 사용
        print("🔗 추출 섹션 결합 중...")
        combined_content = combine_extracts(node_docs_folder)
        
        if not combined_content.strip():
            print("⚠️ 추출할 내용이 없습니다")
            return False
        
        # enhanced_chapter_toc.md 파일 저장
        output_filename = "enhanced_1_Complexity_of_object_oriented_programming_toc.md"
        output_path = os.path.join(node_docs_folder, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(combined_content)
        
        print("✅ 4단계 성공!")
        print(f"📄 생성된 파일: {output_path}")
        print(f"📏 파일 크기: {len(combined_content)} bytes")
        print(f"📝 내용 미리보기:")
        print("=" * 50)
        print(combined_content[:300] + "..." if len(combined_content) > 300 else combined_content)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 4단계 테스트 중 오류: {e}")
        return False

async def main():
    """메인 테스트 실행 함수"""
    print("🧪🚀 3단계, 4단계 독립 테스트 시작!")
    print("🎯 대상: Data_Oriented_Programming/1_Complexity_of_object_oriented_programming")
    print("🤖 AI 모델: gemini-2.5-flash")
    print()
    
    # 3단계 테스트
    stage3_success = await test_stage_3_only()
    
    # 4단계 테스트 (3단계 성공 여부와 관계없이 실행)
    stage4_success = test_stage_4_only()
    
    # 최종 결과
    print(f"\n🎉 테스트 결과:")
    print(f"  3단계 (노드 문서 처리): {'✅ 성공' if stage3_success else '❌ 실패'}")
    print(f"  4단계 (Enhanced TOC): {'✅ 성공' if stage4_success else '❌ 실패'}")
    
    if stage3_success and stage4_success:
        print("\n🎉🎉 모든 단계 테스트 성공! 🎉🎉")
    elif stage3_success or stage4_success:
        print("\n⚠️ 일부 단계만 성공")
    else:
        print("\n❌ 모든 단계 실패")

if __name__ == "__main__":
    asyncio.run(main())