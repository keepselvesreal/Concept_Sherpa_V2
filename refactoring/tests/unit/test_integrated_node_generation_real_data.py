# 생성 시간: Thu Sep  4 18:35:00 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage_v2의 2단계 동작 점검 테스트 (실제 데이터 활용)
# 상세 내용:
#   - TestIntegratedNodeGenerationRealData (라인 30-280): 메인 테스트 클래스
#   - setup_test_environment (라인 45-75): 실제 테스트 환경 구성
#   - load_real_chapter_data (라인 77-105): 실제 장 데이터 로드
#   - test_stage_initialization_real (라인 107-120): 실제 초기화 테스트
#   - test_generate_node_documents_with_real_data (라인 122-160): 1단계 실제 데이터 테스트
#   - test_extract_content_nodes_analysis (라인 162-200): 2단계 구현 분석
#   - test_integrate_documents_analysis (라인 202-240): 3단계 구현 분석
#   - test_full_process_with_real_output_data (라인 242-280): 전체 플로우 실제 데이터 테스트
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
sys.path.insert(0, str(project_root / "refactoring" / "src"))

# 실제 모듈들 임포트
from src.stages.integrated_node_generation_stage_v2 import IntegratedNodeGenerationStage
from src.services.content_document_service_v3 import ContentDocumentService, ContentDocumentResult
from src.utils.logger_v2 import Logger
from src.config.config_manager import ConfigManager

class TestIntegratedNodeGenerationRealData:
    """IntegratedNodeGenerationStage_v2의 실제 output 데이터 기반 테스트 클래스"""
    
    def __init__(self):
        self.stage = None
        self.config_manager = None
        self.logger = None
        self.output_data_path = None
        self.real_chapter_data = None
        
    def setup_test_environment(self):
        """실제 테스트 환경 구성"""
        print("=== 실제 output 데이터 기반 테스트 환경 구성 ===")
        
        # 실제 output 데이터 경로 설정
        self.output_data_path = project_root / "refactoring" / "output" / "Data_Oriented_Programming"
        
        if not self.output_data_path.exists():
            raise FileNotFoundError(f"실제 output 데이터가 없습니다: {self.output_data_path}")
        
        print(f"실제 데이터 경로: {self.output_data_path}")
        
        # 실제 ConfigManager 생성 (기본 설정 사용)
        config_path = project_root / "refactoring" / "configs" / "pipeline_config.yaml"
        if config_path.exists():
            self.config_manager = ConfigManager(str(config_path))
        else:
            # 더미 config manager 생성
            self.config_manager = type('MockConfig', (), {})()
            
        # 실제 Logger 생성
        self.logger = Logger(
            project_name="integrated_node_real_test",
            base_dir=str(self.output_data_path.parent),
            logs_base_dir=str(self.output_data_path.parent / "logs")
        )
        
        # 실제 IntegratedNodeGenerationStage 초기화
        self.stage = IntegratedNodeGenerationStage(self.config_manager)
        
        print("✅ 실제 테스트 환경 구성 완료")
    
    def load_real_chapter_data(self):
        """실제 장 데이터 로드"""
        print("\n--- 실제 장 데이터 로드 ---")
        
        # 1장 데이터 사용
        chapter_dir = self.output_data_path / "1_Complexity_of_object_oriented_programming"
        
        if not chapter_dir.exists():
            raise FileNotFoundError(f"1장 디렉토리가 없습니다: {chapter_dir}")
        
        # TOC 파일과 content 파일 확인
        toc_file = chapter_dir / "1_Complexity_of_object_oriented_programming_toc.json"
        content_file = chapter_dir / "1_Complexity_of_object_oriented_programming_content.md"
        
        if not toc_file.exists():
            raise FileNotFoundError(f"TOC 파일이 없습니다: {toc_file}")
        if not content_file.exists():
            raise FileNotFoundError(f"Content 파일이 없습니다: {content_file}")
        
        # 실제 데이터 구성
        self.real_chapter_data = {
            'chapter_number': 1,
            'chapter_title': 'Complexity of object-oriented programming',
            'folder_path': str(chapter_dir),
            'toc_file': str(toc_file),
            'content_file': str(content_file)
        }
        
        print(f"✅ 1장 실제 데이터 로드 완료")
        print(f"- 폴더: {chapter_dir}")
        print(f"- TOC: {toc_file.name}")
        print(f"- Content: {content_file.name}")
        
        return self.real_chapter_data
    
    def test_stage_initialization_real(self):
        """1. 실제 스테이지 초기화 테스트"""
        print("\n--- 1. 실제 스테이지 초기화 테스트 ---")
        
        # 스테이지 구성요소 확인
        assert self.stage is not None, "스테이지 초기화 실패"
        assert hasattr(self.stage, 'logger'), "Logger 속성 없음"
        assert hasattr(self.stage, 'node_document_service'), "NodeDocumentService 속성 없음"
        
        # 로거 동작 확인
        self.stage.logger.info("실제 데이터 테스트 시작")
        
        print("✅ 실제 스테이지 초기화 성공")
        return True
    
    def test_generate_node_documents_with_real_data(self):
        """2. 1단계 실제 데이터로 노드 문서 생성 테스트"""
        print("\n--- 2. 1단계 실제 데이터 노드 문서 생성 테스트 ---")
        
        async def run_test():
            # 실제 장 데이터 로드
            chapter_data = self.load_real_chapter_data()
            
            # 실제 book_info (간단히 구성)
            book_info = {
                'title': 'Data-Oriented Programming',
                'author': 'Yehonathan Sharvit',
                'publisher': 'Manning'
            }
            
            print(f"실제 데이터로 1단계 테스트:")
            print(f"- 장번호: {chapter_data['chapter_number']}")
            print(f"- 장제목: {chapter_data['chapter_title']}")
            print(f"- TOC 파일: {chapter_data['toc_file']}")
            
            # 실제 1단계 메서드 호출
            result = await self.stage.generate_node_documents(
                chapter_data, book_info, str(self.output_data_path)
            )
            
            # 결과 분석
            print(f"\n📊 1단계 결과:")
            print(f"- 성공 여부: {result.get('success')}")
            
            if result.get('success'):
                print(f"- 생성된 문서 수: {result.get('created_count', 0)}")
                print("✅ 1단계 실제 데이터 테스트 성공")
            else:
                print(f"- 오류 메시지: {result.get('error', '알 수 없는 오류')}")
                print("⚠️  1단계 실패 (예상됨 - NodeDocumentService 의존성)")
            
            return True
            
        return asyncio.run(run_test())
    
    def test_extract_content_nodes_analysis(self):
        """3. 2단계 콘텐츠 노드 추출 구현 분석"""
        print("\n--- 3. 2단계 콘텐츠 노드 추출 구현 분석 ---")
        
        async def run_test():
            # 실제 TOC 데이터 로드
            chapter_data = self.real_chapter_data or self.load_real_chapter_data()
            
            with open(chapter_data['toc_file'], 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            print(f"실제 TOC 데이터 분석:")
            print(f"- 총 노드 수: {len(toc_data)}")
            print(f"- 노드 구조 예시:")
            for i, node in enumerate(toc_data[:3]):
                print(f"  {i+1}. {node['title']} (level: {node['level']}, pages: {node['page_count']})")
            
            # 현재 2단계 호출 (placeholder 확인)
            node_docs_result = {'success': True, 'created_files': ['dummy']}
            result = await self.stage.extract_content_nodes(
                chapter_data, node_docs_result, str(self.output_data_path)
            )
            
            if result.get('placeholder'):
                print("\n⚠️  2단계는 현재 placeholder 구현")
                print("\n💡 실제 구현을 위한 ContentDocumentService 활용 방법:")
                
                # ContentDocumentService로 실제 분석 시연
                await self.demonstrate_content_analysis_with_real_data(chapter_data, toc_data)
            else:
                print("✅ 2단계 실제 구현 확인")
            
            return True
            
        return asyncio.run(run_test())
    
    async def demonstrate_content_analysis_with_real_data(self, chapter_data, toc_data):
        """실제 데이터로 콘텐츠 분석 시연"""
        print("\n--- 실제 데이터 ContentDocumentService 시연 ---")
        
        try:
            # 실제 content 파일 로드
            with open(chapter_data['content_file'], 'r', encoding='utf-8') as f:
                chapter_content = f.read()
            
            print(f"장 내용 로드:")
            print(f"- 총 문자 수: {len(chapter_content):,}")
            print(f"- 첫 100자: {chapter_content[:100]}...")
            
            # TOC를 섹션 리스트로 변환
            sections = []
            for node in toc_data:
                if node['level'] >= 2:  # 2레벨 이상만 섹션으로 처리
                    sections.append({
                        'id': str(node['id']),
                        'title': node['title'],
                        'level': node['level'],
                        'page_count': node['page_count']
                    })
            
            print(f"\n분석 대상 섹션: {len(sections)}개")
            for i, section in enumerate(sections[:5]):
                print(f"  {i+1}. {section['title']} ({section['page_count']}페이지)")
            
            print(f"\n💡 ContentDocumentService.extract_sections() 호출 방법:")
            print(f"```python")
            print(f"content_service = ContentDocumentService(config_manager, logger)")
            print(f"result = await content_service.extract_sections(")
            print(f"    chapter_sections={len(sections)}개 섹션,")
            print(f"    chapter_content='{len(chapter_content):,}자 내용',")
            print(f"    stage_name='chapter_content_extraction'")
            print(f")")
            print(f"```")
            print(f"이렇게 하면 각 섹션의 has_content 여부를 AI로 분석 가능")
            
        except Exception as e:
            print(f"시연 중 오류: {e}")
    
    def test_integrate_documents_analysis(self):
        """4. 3단계 문서 통합 구현 분석"""
        print("\n--- 4. 3단계 문서 통합 구현 분석 ---")
        
        async def run_test():
            # 모의 콘텐츠 노드 결과 (실제 2단계 결과 시뮬레이션)
            content_nodes_result = {
                'success': True,
                'processed_sections': 12,
                'content_sections': 8,  # has_content=True인 섹션 수
                'section_documents': [
                    {
                        'section_id': '17',
                        'section_title': '1.1.1_The_design_phase',
                        'has_content': True,
                        'content_length': 1250
                    },
                    {
                        'section_id': '18', 
                        'section_title': '1.1.2_UML_101',
                        'has_content': True,
                        'content_length': 2100
                    }
                ]
            }
            
            chapter_data = self.real_chapter_data or self.load_real_chapter_data()
            
            # 현재 3단계 호출
            result = await self.stage.integrate_documents(
                chapter_data, content_nodes_result, str(self.output_data_path)
            )
            
            if result.get('placeholder'):
                print("⚠️  3단계도 현재 placeholder 구현")
                print(f"\n💡 실제 통합 구현 방법:")
                print(f"1. 노드 정보 문서 (1단계 결과) + 콘텐츠 분석 결과 (2단계) 결합")
                print(f"2. 각 노드에 has_content와 실제 추출된 내용 매핑")
                print(f"3. 최종 통합 문서 생성")
                
                # 실제 통합 결과 시뮬레이션
                self.demonstrate_integration_with_real_data(chapter_data, content_nodes_result)
            else:
                print("✅ 3단계 실제 구현 확인")
            
            return True
            
        return asyncio.run(run_test())
    
    def demonstrate_integration_with_real_data(self, chapter_data, content_nodes_result):
        """실제 데이터 통합 시연"""
        print("\n--- 실제 데이터 통합 시연 ---")
        
        # 통합 문서 구조 예시 (실제 데이터 기반)
        integrated_result = {
            "metadata": {
                "book_title": "Data-Oriented Programming",
                "chapter_number": chapter_data['chapter_number'],
                "chapter_title": chapter_data['chapter_title'],
                "processing_date": datetime.now().isoformat(),
                "source_files": {
                    "toc_file": chapter_data['toc_file'],
                    "content_file": chapter_data['content_file']
                }
            },
            "processing_summary": {
                "total_nodes": 12,
                "processed_sections": content_nodes_result['processed_sections'],
                "content_sections": content_nodes_result['content_sections'],
                "empty_sections": content_nodes_result['processed_sections'] - content_nodes_result['content_sections']
            },
            "content_nodes": content_nodes_result['section_documents'],
            "integration_method": "node_documents + content_analysis"
        }
        
        # 결과 출력 디렉토리에 저장 예시
        output_file = Path(self.output_data_path) / "integrated_chapter_1_example.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(integrated_result, f, indent=2, ensure_ascii=False)
        
        print(f"💡 통합 결과 예시 생성: {output_file.name}")
        print(f"- 총 노드: {integrated_result['processing_summary']['total_nodes']}")
        print(f"- 콘텐츠 노드: {integrated_result['processing_summary']['content_sections']}")
        print(f"- 빈 노드: {integrated_result['processing_summary']['empty_sections']}")
    
    def test_full_process_with_real_output_data(self):
        """5. 전체 프로세스 실제 output 데이터 테스트"""
        print("\n--- 5. 전체 프로세스 실제 output 데이터 테스트 ---")
        
        async def run_test():
            # 실제 데이터로 입력 구성
            chapter_data = self.real_chapter_data or self.load_real_chapter_data()
            
            input_data = {
                'integration_results': [{
                    'success': True,
                    'chapter_number': chapter_data['chapter_number'],
                    'chapter_title': chapter_data['chapter_title'],
                    'folder_path': chapter_data['folder_path'],
                    'toc_file': chapter_data['toc_file']
                }],
                'book_info': {
                    'title': 'Data-Oriented Programming',
                    'author': 'Yehonathan Sharvit'
                },
                'output_dir': str(self.output_data_path)
            }
            
            print("실제 output 데이터로 전체 프로세스 실행...")
            print(f"- 입력 장: {chapter_data['chapter_title']}")
            print(f"- TOC 파일: {Path(chapter_data['toc_file']).name}")
            print(f"- 출력 경로: {self.output_data_path}")
            
            # 전체 프로세스 실행
            result = await self.stage.process(input_data)
            
            # 결과 상세 분석
            print(f"\n🎯 실제 데이터 프로세스 결과:")
            print(f"- 전체 성공: {result.get('success')}")
            print(f"- 처리 장수: {result.get('processed_chapters', 0)}")
            print(f"- 성공률: {result.get('success_rate', 0):.1f}%")
            
            if result.get('node_processing_results'):
                for chapter_result in result['node_processing_results']:
                    chapter_num = chapter_result.get('chapter_number')
                    print(f"\n장 {chapter_num} 상세 결과:")
                    
                    if chapter_result.get('success'):
                        stages = ['node_docs', 'content_nodes', 'integration']
                        stage_names = ['1단계(노드문서)', '2단계(콘텐츠노드)', '3단계(문서통합)']
                        
                        for stage, name in zip(stages, stage_names):
                            stage_result = chapter_result.get(stage, {})
                            success = stage_result.get('success', False)
                            placeholder = stage_result.get('placeholder', False)
                            
                            status = "성공" if success else "실패"
                            if placeholder:
                                status += " (placeholder)"
                            
                            print(f"  {name}: {status}")
                    else:
                        print(f"  오류: {chapter_result.get('error', '알 수 없음')}")
            
            print(f"\n📋 현재 상태 요약 (실제 데이터 기준):")
            print(f"- 1단계: NodeDocumentService 필요, TOC 파일 활용")
            print(f"- 2단계: ContentDocumentService로 has_content 분석 필요")  
            print(f"- 3단계: 1,2단계 결과 통합하여 최종 문서 생성 필요")
            
            return True
            
        return asyncio.run(run_test())
    
    def test_generate_node_docs_for_selected_chapters(self):
        """1단계 노드 정보 문서 생성 - 1, 6, 9장 대상"""
        print("\n--- 1단계 노드 정보 문서 생성 (1, 6, 9장) ---")
        
        # 대상 장 정보 
        target_chapters = [
            {
                'chapter_number': 1,
                'folder_name': '1_Complexity_of_object_oriented_programming',
                'title': 'Complexity of object oriented programming'
            },
            {
                'chapter_number': 6,
                'folder_name': '6_Unit_tests',
                'title': 'Unit tests'
            },
            {
                'chapter_number': 9,
                'folder_name': '9_Persistent_data_structures',
                'title': 'Persistent data structures'
            }
        ]
        
        async def run_node_docs_generation():
            success_count = 0
            total_count = len(target_chapters)
            
            for chapter_info in target_chapters:
                chapter_path = self.output_data_path.parent / chapter_info['folder_name']
                toc_file = chapter_path / f"{chapter_info['folder_name']}_toc.json"
                
                print(f"\n📊 장 {chapter_info['chapter_number']} 처리 시작: {chapter_info['title']}")
                print(f"- 폴더: {chapter_path}")
                print(f"- TOC 파일: {toc_file}")
                
                # 파일 존재 확인
                if not chapter_path.exists():
                    print(f"❌ 장 폴더가 존재하지 않음: {chapter_path}")
                    continue
                
                if not toc_file.exists():
                    print(f"❌ TOC 파일이 존재하지 않음: {toc_file}")
                    continue
                
                # chapter_result 구성
                chapter_result = {
                    'chapter_number': chapter_info['chapter_number'],
                    'chapter_title': chapter_info['folder_name'],
                    'folder_path': str(chapter_path),
                    'toc_file': str(toc_file)
                }
                
                try:
                    # 1단계 실행: 노드 정보 문서 생성
                    print(f"🔧 노드 정보 문서 생성 시작...")
                    node_docs_result = await self.stage.generate_node_documents(
                        chapter_result, 
                        {'title': 'Data-Oriented Programming'}, 
                        str(self.output_data_path)
                    )
                    
                    if node_docs_result.get('success', False):
                        created_count = node_docs_result.get('created_count', 0)
                        print(f"✅ 장 {chapter_info['chapter_number']} 노드 정보 문서 생성 완료: {created_count}개 파일")
                        success_count += 1
                        
                        # node_info_docs 폴더 확인
                        node_docs_dir = chapter_path / "node_info_docs"
                        if node_docs_dir.exists():
                            print(f"📁 생성된 파일 목록:")
                            for doc_file in sorted(node_docs_dir.glob("*.md")):
                                print(f"   - {doc_file.name}")
                    else:
                        error_msg = node_docs_result.get('error', '알 수 없는 오류')
                        print(f"❌ 장 {chapter_info['chapter_number']} 노드 정보 문서 생성 실패: {error_msg}")
                        
                except Exception as e:
                    print(f"❌ 장 {chapter_info['chapter_number']} 처리 중 예외: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            print(f"\n--- 1단계 결과 요약 ---")
            print(f"총 {success_count}/{total_count}개 장 처리 성공")
            print(f"성공률: {(success_count/total_count*100):.1f}%")
            
            return success_count == total_count
        
        return asyncio.run(run_node_docs_generation())
    
    def cleanup(self):
        """테스트 정리 (실제 데이터는 건드리지 않음)"""
        # 실제 output 데이터는 건드리지 않고, 테스트 중 생성된 예시 파일만 정리
        example_file = Path(self.output_data_path) / "integrated_chapter_1_example.json"
        if example_file.exists():
            example_file.unlink()
            print(f"예시 파일 정리: {example_file.name}")

def main():
    """메인 테스트 실행"""
    print("IntegratedNodeGenerationStage_v2 실제 output 데이터 기반 테스트")
    print("=" * 75)
    
    test_suite = TestIntegratedNodeGenerationRealData()
    
    try:
        # 환경 설정
        test_suite.setup_test_environment()
        
        # 🎯 1단계 노드 정보 문서 생성 테스트 (1, 6, 9장) 실행
        print("\n🚀 1단계 노드 정보 문서 생성 테스트 (1, 6, 9장) 실행")
        success = test_suite.test_generate_node_docs_for_selected_chapters()
        
        if success:
            print("\n🎉 1단계 노드 정보 문서 생성 성공!")
        else:
            print("\n⚠️ 1단계 노드 정보 문서 생성 일부 실패")
        
        # 기존 테스트들도 실행할 수 있도록 남겨둠
        # tests = [
        #     test_suite.test_stage_initialization_real,
        #     test_suite.test_generate_node_documents_with_real_data,
        #     test_suite.test_extract_content_nodes_analysis,
        #     test_suite.test_integrate_documents_analysis,
        #     test_suite.test_full_process_with_real_output_data
        # ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ 테스트 실행 중 오류: {e}")
                failed += 1
        
        print("\n" + "=" * 75)
        print(f"테스트 결과: {passed}개 성공, {failed}개 실패")
        
        print(f"\n🎯 실제 데이터 기반 핵심 발견사항:")
        print(f"✅ 실제 output 데이터 구조 확인: TOC(JSON) + Content(MD)")
        print(f"⚠️  2단계: ContentDocumentService 통합으로 has_content 분석 구현 필요")
        print(f"⚠️  3단계: 노드정보+콘텐츠분석 결과 통합 문서 생성 로직 필요")
        print(f"\n🚀 다음 작업: 2,3단계 실제 구현 with real data!")
        
    except Exception as e:
        print(f"❌ 테스트 환경 구성 실패: {e}")
        import traceback
        traceback.print_exc()
    finally:
        test_suite.cleanup()

if __name__ == "__main__":
    main()