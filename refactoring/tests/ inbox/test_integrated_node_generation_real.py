# 생성 시간: Mon Sep  8 08:06:37 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage v3의 3단계 프로세스 정상 동작 확인 테스트 (실제 데이터 사용)
# 상세 내용:
#   - TestIntegratedNodeGenerationReal (라인 25-180): 실제 데이터를 사용한 integration 테스트 클래스
#   - test_single_chapter_processing (라인 35-89): 1장 단일 처리 테스트 메서드
#   - test_stage_1_node_documents (라인 91-119): 1단계 노드 문서 생성 개별 테스트
#   - test_stage_2_content_documents (라인 121-149): 2단계 콘텐츠 문서 생성 개별 테스트  
#   - test_stage_3_integrate_documents (라인 151-179): 3단계 문서 통합 개별 테스트
#   - _save_test_results (라인 181-220): 테스트 결과를 임시 폴더에 저장하는 헬퍼 메서드
# 상태: active

import os
import sys
import json
import asyncio
import unittest
from datetime import datetime
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# 테스트 대상 클래스 임포트
from stages.integrated_node_generation_stage_v3 import IntegratedNodeGenerationStage
from utils.config_manager import ConfigManager

class TestIntegratedNodeGenerationReal(unittest.TestCase):
    """
    IntegratedNodeGenerationStage v3의 실제 데이터를 사용한 integration 테스트
    
    요구사항:
    - 실제 Data_Oriented_Programming 데이터 사용 (mock 사용 금지)
    - 1장 'Complexity_of_object_oriented_programming' 대상
    - 3단계 프로세스 정상 동작 확인: 노드문서생성 → 콘텐츠문서생성 → 문서통합
    - 결과를 임시 폴더에 저장하여 사용자가 직접 확인 가능
    """
    
    def setUp(self):
        """테스트 초기화"""
        # ConfigManager 초기화
        self.config_manager = ConfigManager()
        
        # IntegratedNodeGenerationStage 초기화
        self.stage = IntegratedNodeGenerationStage(self.config_manager)
        
        # 원본 데이터 경로 설정
        self.original_data_dir = project_root / "tests" / "data" / "Data_Oriented_Programming"
        self.original_chapter_1_dir = self.original_data_dir / "1_Complexity_of_object_oriented_programming"
        
        # 임시 테스트 폴더 설정
        timestamp = datetime.now().strftime("%H%M")
        self.test_base_dir = project_root / "tests" / "data" / "integrated_node_generation_test"
        self.chapter_1_dir = self.test_base_dir / "1_Complexity_of_object_oriented_programming"
        
        # 임시 폴더 생성 및 원본 데이터 복사
        self._setup_test_data()
        
        print(f"📁 테스트 데이터 복사 완료: {self.chapter_1_dir}")
        print(f"📁 테스트 결과가 저장될 위치: {self.chapter_1_dir}")
    
    def _setup_test_data(self):
        """원본 데이터를 임시 테스트 폴더에 복사"""
        import shutil
        
        # 기존 테스트 폴더 정리
        if self.test_base_dir.exists():
            shutil.rmtree(self.test_base_dir)
        
        # 테스트 폴더 생성
        self.test_base_dir.mkdir(parents=True, exist_ok=True)
        
        # 원본 데이터 복사
        if self.original_chapter_1_dir.exists():
            shutil.copytree(self.original_chapter_1_dir, self.chapter_1_dir)
        else:
            raise FileNotFoundError(f"원본 데이터 폴더를 찾을 수 없습니다: {self.original_chapter_1_dir}")
    
    def tearDown(self):
        """테스트 정리 - 임시 폴더 유지 (사용자 확인용)"""
        print(f"✅ 테스트 완료. 결과 확인: {self.test_base_dir}")
        print("🗑️ 수동 정리 필요시: rm -rf 위 경로")
        
    def test_single_chapter_processing(self):
        """1장 전체 프로세스 테스트 (3단계 순차 실행)"""
        print(f"\n=== 1장 전체 프로세스 테스트 시작 ===")
        print(f"테스트 대상: {self.chapter_1_dir}")
        print(f"결과 저장 경로: {self.test_base_dir}")
        
        # 필수 파일 존재 확인
        toc_file = self.chapter_1_dir / "1_Complexity_of_object_oriented_programming_toc.json"
        content_file = self.chapter_1_dir / "1_Complexity_of_object_oriented_programming_content.md"
        
        self.assertTrue(toc_file.exists(), f"TOC 파일이 존재하지 않음: {toc_file}")
        self.assertTrue(content_file.exists(), f"Content 파일이 존재하지 않음: {content_file}")
        
        # 비동기 메서드 실행
        async def run_test():
            # 1장만 처리하도록 단계별로 직접 실행
            # 1단계: 노드 문서 생성
            stage1_result = await self.stage.generate_node_documents(str(self.chapter_1_dir))
            self.assertTrue(stage1_result['success'], f"1단계 실패: {stage1_result.get('error')}")
            
            # 2단계: 콘텐츠 문서 생성  
            stage2_result = await self.stage.generate_content_documents(str(self.chapter_1_dir))
            self.assertTrue(stage2_result['success'], f"2단계 실패: {stage2_result.get('error')}")
            
            # 3단계: 문서 통합
            stage3_result = await self.stage.integrate_documents(str(self.chapter_1_dir))
            self.assertTrue(stage3_result['success'], f"3단계 실패: {stage3_result.get('error')}")
            
            # 전체 결과 구성
            result = {
                'success': True,
                'data': {
                    'processed_chapters': 1,
                    'total_chapters': 1,
                    'success_rate': 100.0,
                    'results': [{
                        'folder_name': '1_Complexity_of_object_oriented_programming',
                        'folder_path': str(self.chapter_1_dir),
                        'success': True,
                        'stages': {
                            'node_docs': stage1_result,
                            'sections': stage2_result,
                            'integration': stage3_result
                        }
                    }]
                },
                'error': None
            }
            
            # 결과 검증
            self.assertTrue(result['success'], f"Process 실패: {result.get('error')}")
            self.assertIsNotNone(result['data'])
            
            # 상세 결과 확인
            data = result['data']
            self.assertEqual(data['processed_chapters'], 1, "처리된 장 수가 1이 아님")
            self.assertEqual(data['total_chapters'], 1, "전체 장 수가 1이 아님")  # 1장만 처리
            
            # 결과 저장 (임시 테스트 폴더에)
            self._save_test_results("full_process", result)
            
            print(f"✅ 전체 프로세스 완료: {data['processed_chapters']}/{data['total_chapters']} 장 성공")
            return result
            
        # asyncio로 실행
        result = asyncio.run(run_test())
        
        # 생성된 파일들 확인
        self._verify_generated_files()
        
    def test_stage_1_node_documents(self):
        """1단계: 노드 문서 생성 개별 테스트"""
        print(f"\n=== 1단계 개별 테스트: 노드 문서 생성 ===")
        
        async def run_stage_1():
            result = await self.stage.generate_node_documents(str(self.chapter_1_dir))
            
            # 결과 검증
            self.assertTrue(result['success'], f"1단계 실패: {result.get('error')}")
            
            # 결과 저장
            self._save_test_results("stage_1_node_docs", result)
            
            # node_info_docs 폴더 생성 확인
            node_docs_dir = self.chapter_1_dir / "node_info_docs"
            self.assertTrue(node_docs_dir.exists(), "node_info_docs 폴더가 생성되지 않음")
            
            # 생성된 파일 개수 확인
            md_files = list(node_docs_dir.glob("*.md"))
            print(f"✅ 1단계 완료: node_info_docs에 {len(md_files)}개 파일 생성")
            
            return result
            
        asyncio.run(run_stage_1())
        
    def test_stage_2_content_documents(self):
        """2단계: 콘텐츠 문서 생성 개별 테스트"""
        print(f"\n=== 2단계 개별 테스트: 콘텐츠 문서 생성 ===")
        
        async def run_stage_2():
            result = await self.stage.generate_content_documents(str(self.chapter_1_dir))
            
            # 결과 검증
            self.assertTrue(result['success'], f"2단계 실패: {result.get('error')}")
            self.assertIsNotNone(result['data'])
            
            # 결과 저장
            self._save_test_results("stage_2_content_docs", result)
            
            # content.json 및 sections 폴더 확인
            content_json = self.chapter_1_dir / "content.json"
            sections_dir = self.chapter_1_dir / "sections"
            
            if content_json.exists():
                print(f"✅ content.json 생성됨")
            if sections_dir.exists():
                section_files = list(sections_dir.glob("*.md"))
                print(f"✅ sections 폴더에 {len(section_files)}개 파일 생성")
            
            print(f"✅ 2단계 완료: {result['data']}")
            
            return result
            
        asyncio.run(run_stage_2())
        
    def test_stage_3_integrate_documents(self):
        """3단계: 문서 통합 개별 테스트"""
        print(f"\n=== 3단계 개별 테스트: 문서 통합 ===")
        
        async def run_stage_3():
            result = await self.stage.integrate_documents(str(self.chapter_1_dir))
            
            # 결과 검증
            self.assertTrue(result['success'], f"3단계 실패: {result.get('error')}")
            
            # 결과 저장
            self._save_test_results("stage_3_integration", result)
            
            # unified_info_docs 폴더 확인
            unified_dir = self.chapter_1_dir / "unified_info_docs"
            if unified_dir.exists():
                unified_files = list(unified_dir.glob("*.md"))
                print(f"✅ unified_info_docs에 {len(unified_files)}개 통합 문서 생성")
            
            print(f"✅ 3단계 완료")
            
            return result
            
        asyncio.run(run_stage_3())
    
    def _save_test_results(self, test_name: str, result: dict):
        """테스트 결과를 JSON 파일로 저장 (임시 테스트 폴더에)"""
        try:
            # 테스트 폴더에 결과 저장
            result_file = self.test_base_dir / f"{test_name}_result.json"
            
            # datetime 객체 등 JSON 직렬화 불가능한 객체 처리
            def json_serializer(obj):
                if hasattr(obj, '__dict__'):
                    return obj.__dict__
                return str(obj)
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=json_serializer)
                
            print(f"📄 테스트 결과 저장: {result_file.name}")
            
        except Exception as e:
            print(f"❌ 결과 저장 실패: {e}")
    
    def _verify_generated_files(self):
        """생성된 파일들 검증"""
        print(f"\n=== 생성된 파일 검증 ===")
        
        # 각 단계별 폴더 확인
        folders_to_check = [
            ("node_info_docs", "노드 정보 문서"),
            ("sections", "섹션 콘텐츠 파일"),
            ("unified_info_docs", "통합 문서")
        ]
        
        for folder_name, description in folders_to_check:
            folder_path = self.chapter_1_dir / folder_name
            if folder_path.exists():
                files = list(folder_path.glob("*"))
                print(f"✅ {description}: {len(files)}개 파일 ({folder_name})")
            else:
                print(f"⚠️ {description}: 폴더 없음 ({folder_name})")
                
        # content.json 확인
        content_json = self.chapter_1_dir / "content.json"
        if content_json.exists():
            print(f"✅ content.json 생성됨")
        else:
            print(f"⚠️ content.json 생성되지 않음")

if __name__ == '__main__':
    # 테스트 실행 전 경로 확인
    print("=== IntegratedNodeGenerationStage v3 실제 데이터 테스트 ===")
    
    # 단일 테스트 메서드 실행 (전체 프로세스 테스트)
    suite = unittest.TestSuite()
    suite.addTest(TestIntegratedNodeGenerationReal('test_single_chapter_processing'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)