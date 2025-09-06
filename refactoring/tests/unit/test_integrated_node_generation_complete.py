# 생성 시간: Thu Sep  4 18:46:00 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage_v2의 완전한 3단계 테스트 (실제 데이터 활용)
# 상세 내용:
#   - TestIntegratedNodeGenerationComplete (라인 30-200): 완전한 3단계 테스트 클래스
#   - test_complete_3_stage_process (라인 40-120): 전체 3단계 프로세스 테스트
#   - verify_stage_results (라인 122-150): 각 단계 결과 검증
#   - print_results_summary (라인 152-200): 결과 요약 출력
# 상태: active

import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

# 프로젝트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# 실제 모듈들 임포트
from src.stages.integrated_node_generation_stage_v2 import IntegratedNodeGenerationStage
from src.config.config_manager import ConfigManager

class TestIntegratedNodeGenerationComplete:
    """완전한 3단계 IntegratedNodeGenerationStage 테스트"""
    
    def __init__(self):
        self.output_data_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/"
        self.config_manager = ConfigManager()
    
    def test_complete_3_stage_process(self):
        """전체 3단계 프로세스 테스트"""
        print("=== IntegratedNodeGenerationStage 완전한 3단계 테스트 ===")
        print(f"테스트 데이터 경로: {self.output_data_path}")
        
        async def run_complete_test():
            # IntegratedNodeGenerationStage 초기화
            stage = IntegratedNodeGenerationStage(self.config_manager)
            
            # 입력 데이터 구성 (실제 chapter 정보)
            input_data = {
                'integration_results': [
                    {
                        'success': True,
                        'chapter_number': 1,
                        'chapter_title': '1_Complexity_of_object_oriented_programming',
                        'folder_path': self.output_data_path,
                        'toc_file': os.path.join(self.output_data_path, "1_Complexity_of_object_oriented_programming_toc.json"),
                        'content_file': os.path.join(self.output_data_path, "1_Complexity_of_object_oriented_programming_content.md")
                    }
                ],
                'book_info': {
                    'title': 'Data-Oriented Programming',
                    'author': 'Yehonathan Sharvit'
                },
                'output_dir': self.output_data_path
            }
            
            print(f"📊 입력 데이터 구성 완료")
            print(f"- 장 개수: {len(input_data['integration_results'])}")
            print(f"- TOC 파일: {os.path.basename(input_data['integration_results'][0]['toc_file'])}")
            print(f"- 콘텐츠 파일: {os.path.basename(input_data['integration_results'][0]['content_file'])}")
            
            # 전체 프로세스 실행
            print(f"\n🚀 전체 3단계 프로세스 시작...")
            try:
                result = await stage.process(input_data)
                
                print(f"\n✅ 전체 프로세스 완료!")
                self.print_results_summary(result)
                
                # 각 단계별 결과 검증
                if result.get('success', False):
                    self.verify_stage_results(result)
                else:
                    print(f"❌ 프로세스 실패: {result.get('error', '알 수 없는 오류')}")
                
                return result
                
            except Exception as e:
                print(f"❌ 프로세스 실행 중 예외: {str(e)}")
                import traceback
                traceback.print_exc()
                return {'success': False, 'error': str(e)}
        
        return asyncio.run(run_complete_test())
    
    def verify_stage_results(self, result):
        """각 단계 결과 검증"""
        print(f"\n--- 단계별 결과 검증 ---")
        
        node_processing_results = result.get('node_processing_results', [])
        if not node_processing_results:
            print(f"❌ 노드 처리 결과가 없음")
            return
        
        chapter_result = node_processing_results[0]
        if not chapter_result.get('success', False):
            print(f"❌ 장 처리 실패: {chapter_result.get('error', '')}")
            return
        
        # 1단계 검증
        node_docs = chapter_result.get('node_docs', {})
        if node_docs.get('success', False):
            print(f"✅ 1단계 (노드 정보 문서 생성): {node_docs.get('created_count', 0)}개 파일")
        else:
            print(f"❌ 1단계 실패: {node_docs.get('error', '')}")
        
        # 2단계 검증  
        content_nodes = chapter_result.get('content_nodes', {})
        if content_nodes.get('success', False):
            print(f"✅ 2단계 (콘텐츠 노드 추출): {content_nodes.get('content_sections', 0)}개 콘텐츠 노드")
        else:
            print(f"❌ 2단계 실패: {content_nodes.get('error', '')}")
        
        # 3단계 검증
        integration = chapter_result.get('integration', {})
        if integration.get('success', False):
            integrated_count = integration.get('integrated_count', 0)
            total_nodes = integration.get('total_nodes', 0)
            print(f"✅ 3단계 (문서 통합): {integrated_count}/{total_nodes}개 문서 통합")
        else:
            print(f"❌ 3단계 실패: {integration.get('error', '')}")
    
    def print_results_summary(self, result):
        """결과 요약 출력"""
        print(f"\n--- 전체 결과 요약 ---")
        print(f"전체 성공 여부: {result.get('success', False)}")
        print(f"처리된 장 수: {result.get('processed_chapters', 0)}")
        print(f"총 장 수: {result.get('total_chapters', 0)}")
        print(f"성공률: {result.get('success_rate', 0):.1f}%")
        
        # 개별 장 결과
        node_processing_results = result.get('node_processing_results', [])
        for i, chapter_result in enumerate(node_processing_results, 1):
            print(f"\n장 {i} ({chapter_result.get('chapter_title', '')}):")
            if chapter_result.get('success', False):
                print(f"  ✅ 성공")
                # 각 단계별 상세 정보
                node_docs = chapter_result.get('node_docs', {})
                content_nodes = chapter_result.get('content_nodes', {})
                integration = chapter_result.get('integration', {})
                
                print(f"  - 1단계: {node_docs.get('created_count', 0)}개 노드 문서")
                print(f"  - 2단계: {content_nodes.get('content_sections', 0)}개 콘텐츠 노드")
                print(f"  - 3단계: {integration.get('integrated_count', 0)}개 통합 문서")
            else:
                print(f"  ❌ 실패: {chapter_result.get('error', '')}")

if __name__ == "__main__":
    tester = TestIntegratedNodeGenerationComplete()
    result = tester.test_complete_3_stage_process()
    
    if result and result.get('success', False):
        print(f"\n🎉 모든 테스트 성공!")
    else:
        print(f"\n💥 테스트 실패!")
        if result:
            print(f"오류: {result.get('error', '알 수 없는 오류')}")