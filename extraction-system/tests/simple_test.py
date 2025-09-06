# 생성 시간: Tue Sep  2 15:08:00 KST 2025
# 핵심 내용: 파이프라인 단계별 간단한 직접 테스트 (실제 모듈 사용)
# 상세 내용:
#   - test_stage_1 (라인 25-45): 1단계 노드 정보 문서 생성 테스트
#   - test_stage_2 (라인 47-70): 2단계 콘텐츠 노드 분석 테스트  
#   - test_stage_3 (라인 72-95): 3단계 문서 통합 테스트
# 상태: active
# 주소: simple_test
# 참조: -

import os
import sys
import asyncio
from pathlib import Path

# 경로 추가
# 파이프라인 경로 제거 후 필요한 것만 추가
pipeline_path = '/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline'
if pipeline_path in sys.path:
    sys.path.remove(pipeline_path)

sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30')  # 노드 문서 생성
sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31')  # 콘텐츠 노드 분석
sys.path.insert(0, '/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')  # 문서 통합 (마지막에 추가)

def test_stage_1_node_generation():
    """1단계: 노드 정보 문서 생성 테스트 (함수 기반)"""
    print("🔄 1단계: 노드 정보 문서 생성 테스트")
    
    # 실제 함수 임포트 (25-08-30 폴더에서)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "node_document_generator", 
        "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30/node_document_generator.py"
    )
    node_gen_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(node_gen_module)
    
    generate_node_documents = node_gen_module.generate_node_documents
    load_nodes = node_gen_module.load_nodes
    
    # 1장 테스트 데이터 사용
    chapter_dir = Path("tests/fixtures/chapter_1")
    toc_file = chapter_dir / "1_Complexity_of_object_oriented_programming_toc.json"
    
    try:
        # JSON 로드
        nodes = load_nodes(str(toc_file))
        print(f"✓ 노드 로드 완료: {len(nodes)}개")
        
        # 출력 디렉토리 생성
        output_dir = chapter_dir / "node_info_docs"
        output_dir.mkdir(exist_ok=True)
        
        # 문서 생성
        generate_node_documents(nodes, str(output_dir))
        
        # 결과 확인
        generated_files = list(output_dir.glob("*.md"))
        print(f"✅ 1단계 성공: {len(generated_files)}개 문서 생성")
        return True
        
    except Exception as e:
        print(f"❌ 1단계 실패: {str(e)}")
        return False

def test_stage_2_content_analysis():
    """2단계: 콘텐츠 노드 분석 테스트"""
    print("🔄 2단계: 콘텐츠 노드 분석 테스트")
    
    try:
        # ContentNodeAnalyzer 임포트 시도
        from content_node_analyzer_v2 import ContentNodeAnalyzer
        
        # 1장 테스트 데이터
        chapter_dir = Path("tests/fixtures/chapter_1") 
        toc_file = chapter_dir / "1_Complexity_of_object_oriented_programming_toc.json"
        content_file = chapter_dir / "1_Complexity_of_object_oriented_programming_content.md"
        
        # 설정 파일 경로
        config_path = "tests/test_extraction_config.yaml"
        
        # 분석기 초기화
        analyzer = ContentNodeAnalyzer(config_path=config_path)
        
        # 분석 실행 (비동기)
        result = asyncio.run(analyzer.analyze_chapter_toc(str(toc_file), str(content_file)))
        
        if result.get('success', False):
            extracted_count = len(result.get('extracted_files', []))
            print(f"✅ 2단계 성공: {extracted_count}개 파일 추출")
            return True
        else:
            print(f"❌ 2단계 실패: {result.get('error', '알 수 없는 오류')}")
            return False
            
    except Exception as e:
        print(f"❌ 2단계 예외: {str(e)}")
        return False

def test_stage_3_document_integration():
    """3단계: 문서 통합 테스트"""
    print("🔄 3단계: 문서 통합 테스트")
    
    try:
        # DocumentIntegrator 임포트
        from document_integrator import DocumentIntegrator
        
        # 1장 디렉토리
        chapter_dir = Path("tests/fixtures/chapter_1")
        
        # 통합기 초기화
        integrator = DocumentIntegrator()
        
        # 통합 실행
        result = integrator.integrate_documents_for_chapter(str(chapter_dir))
        
        if result.get('success', False):
            integrated_count = result.get('integrated_count', 0)
            print(f"✅ 3단계 성공: {integrated_count}개 문서 통합")
            return True
        else:
            print(f"❌ 3단계 실패: {result.get('error', '알 수 없는 오류')}")
            return False
            
    except Exception as e:
        print(f"❌ 3단계 예외: {str(e)}")
        return False

def main():
    """메인 테스트 실행"""
    print("🧪 파이프라인 단계별 간단 테스트 시작\n")
    
    results = []
    
    # 1단계 테스트
    results.append(("1단계 노드 생성", test_stage_1_node_generation()))
    
    # 2단계 테스트
    results.append(("2단계 콘텐츠 분석", test_stage_2_content_analysis()))
    
    # 3단계 테스트
    results.append(("3단계 문서 통합", test_stage_3_document_integration()))
    
    # 결과 요약
    print(f"\n📊 테스트 결과 요약:")
    for stage, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"  {stage}: {status}")
    
    success_count = sum(1 for _, success in results if success)
    print(f"\n🎯 총 {success_count}/{len(results)} 단계 성공")

if __name__ == "__main__":
    main()