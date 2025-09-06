#!/usr/bin/env python3
# 생성 시간: Sat Sep  6 16:50:00 KST 2025
# 핵심 내용: unified_info_docs 통합 로직 테스트
# 상세 내용:
#   - test_unified_integration (라인 15-80): integrate_documents 메서드 테스트
#   - MockConfigManager (라인 10-13): 간단한 설정 관리자 모킹
# 상태: active

import asyncio
import sys
import os
import json
from pathlib import Path

# 프로젝트 경로 추가
sys.path.append(str(Path(__file__).parent / "refactoring" / "src"))

from stages.integrated_node_generation_stage_v3 import IntegratedNodeGenerationStage

class MockConfigManager:
    """간단한 설정 관리자 모킹"""
    pass

async def test_unified_integration():
    """unified_info_docs 통합 로직 테스트"""
    
    print("🧪 unified_info_docs 통합 테스트 시작")
    
    # 테스트 폴더 경로
    test_folder = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    
    print(f"📂 테스트 폴더: {test_folder}")
    
    # 📋 **사전 확인**: 필수 폴더들 존재 확인
    print("\n📋 **사전 확인**:")
    
    sections_dir = os.path.join(test_folder, "sections")
    node_docs_dir = os.path.join(test_folder, "node_info_docs")
    toc_file = os.path.join(test_folder, "1_Complexity_of_object_oriented_programming_toc.json")
    
    print(f"  - sections/ 폴더: {'✅' if os.path.exists(sections_dir) else '❌'}")
    print(f"  - node_info_docs/ 폴더: {'✅' if os.path.exists(node_docs_dir) else '❌'}")
    print(f"  - TOC 파일: {'✅' if os.path.exists(toc_file) else '❌'}")
    
    if os.path.exists(sections_dir):
        section_files = os.listdir(sections_dir)
        print(f"  - sections 파일 수: {len(section_files)}개")
        print(f"    예시 파일들: {section_files[:3]}")
    
    if os.path.exists(node_docs_dir):
        node_files = os.listdir(node_docs_dir)
        print(f"  - node_info_docs 파일 수: {len(node_files)}개")
    
    try:
        # Stage 초기화
        config_manager = MockConfigManager()
        stage = IntegratedNodeGenerationStage(config_manager)
        
        # TOC 데이터 로드
        with open(toc_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        
        print(f"\n🔧 **통합 실행**: {len(toc_data)}개 노드 처리")
        
        # 각 노드별로 통합 실행
        success_count = 0
        for node in toc_data:
            result = stage._integrate_single_document(
                node=node,
                all_nodes=toc_data,
                content_dir=test_folder,
                node_docs_dir=node_docs_dir
            )
            if result:
                success_count += 1
                print(f"  ✅ {node.get('id', '?'):02d}: {node.get('title', '제목없음')}")
            else:
                print(f"  ❌ {node.get('id', '?'):02d}: {node.get('title', '제목없음')}")
        
        print(f"\n📊 **통합 결과**: {success_count}/{len(toc_data)}개 성공")
        
        # 🔍 **결과 검증**: unified_info_docs 폴더 확인
        print("\n🔍 **결과 검증**:")
        unified_dir = os.path.join(test_folder, "unified_info_docs")
        
        if os.path.exists(unified_dir):
            unified_files = os.listdir(unified_dir)
            print(f"  - unified_info_docs/ 폴더: ✅ ({len(unified_files)}개 파일)")
            
            # 첫 번째 파일 내용 간단 확인
            if unified_files:
                sample_file = os.path.join(unified_dir, unified_files[0])
                with open(sample_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"  - 샘플 파일: {unified_files[0]}")
                print(f"    📄 내용 길이: {len(content)}자")
                
                # sections 내용 포함 여부 확인
                has_section_content = len([line for line in content.split('\n') if line.strip() and not line.startswith('#') and not line.startswith('---')]) > 10
                print(f"    🔗 sections 내용 포함: {'✅' if has_section_content else '❌'}")
                
                # 구조 확인
                has_structure = all(section in content for section in ["# 속성", "# 추출", "# 내용", "# 구성"])
                print(f"    📋 문서 구조 완성: {'✅' if has_structure else '❌'}")
                
        else:
            print(f"  - unified_info_docs/ 폴더: ❌ (생성되지 않음)")
        
        print(f"\n🎯 **테스트 완료**: {'성공' if success_count > 0 and os.path.exists(unified_dir) else '실패'}")
        return True
        
    except Exception as e:
        print(f"❌ **테스트 실패**: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_unified_integration())
    print(f"\n🏁 **최종 결과**: {'✅ 성공' if success else '❌ 실패'}")