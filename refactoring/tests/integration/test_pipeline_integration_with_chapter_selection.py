# test_pipeline_integration_with_chapter_selection.py
# 생성 시간: Mon Sep  8 16:38:46 KST 2025
# 핵심 내용: 3단계 파이프라인 통합 테스트 (장 선택 기능 포함)
# 상세 내용:
#   - TestPipelineIntegrationWithChapterSelection (라인 18-200): 메인 테스트 클래스
#   - setUp (라인 29-55): 테스트 환경 설정 및 ConfigManager 초기화
#   - test_full_pipeline_with_selected_chapters (라인 57-120): 전체 파이프라인 테스트
#   - test_workspace_preparation_stage (라인 122-140): 1단계 워크스페이스 준비 테스트
#   - test_integrated_node_generation_stage (라인 142-160): 2단계 통합 노드 생성 테스트
#   - test_content_processing_stage (라인 162-180): 3단계 콘텐츠 처리 테스트
#   - _setup_test_config_manager (라인 182-210): 테스트용 ConfigManager 설정
# 상태: active

import os
import sys
import json
import asyncio
import unittest
from pathlib import Path
from datetime import datetime

# 프로젝트 경로 추가
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from utils.config_manager import ConfigManager
from utils.logger_v2 import Logger
from stages.workspace_preparation_v2 import WorkspacePreparationStage
from stages.integrated_node_generation_stage_v3 import IntegratedNodeGenerationStage
from stages.content_processing_stage import ContentProcessingStage
from services.ai_service_v4 import AIService

class TestPipelineIntegrationWithChapterSelection(unittest.TestCase):
    """3단계 파이프라인 통합 테스트 (장 선택 기능 포함)
    
    요구사항:
    - PDF에서 목차 추출 후 선택된 장만 필터링 (WorkspacePreparationStage.create_chapter_folders에서 처리)
    - 실제 객체 사용 (mock 객체 금지)
    - 각 단계 결과 저장 후 경로 전달로 독립성 보장
    - 최종 결과: workspace가 생성한 실제 책 폴더 경로 사용
    """
    
    def setUp(self):
        """테스트 환경 설정"""
        # 입력 데이터 설정
        self.pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
        self.selected_chapters = [1, 2]  # 테스트할 장 번호
        
        # 테스트 결과 저장 경로 (WorkspacePreparationStage가 실제로 사용할 경로)
        self.test_output_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data")
        self.test_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 테스트용 ConfigManager 설정 (장 선택 기능 포함)
        self.config_manager = self._setup_test_config_manager()
        
        # LoggerFactory 초기화 (간단한 팩토리 클래스)
        class LoggerFactory:
            def create_logger(self, name):
                return Logger(name)
        self.logger_factory = LoggerFactory()
        
        # 각 단계별 결과 저장용 변수
        self.stage1_result = None
        self.stage2_result = None  
        self.stage3_result = None
        
        print(f"\n🧪 테스트 설정 완료")
        print(f"📄 PDF 경로: {self.pdf_path}")
        print(f"🎯 선택된 장: {self.selected_chapters}")
        print(f"📁 테스트 출력 디렉토리: {self.test_output_dir}")
        
    def test_full_pipeline_with_selected_chapters(self):
        """전체 파이프라인 테스트 (선택된 장만 처리)"""
        print(f"\n🚀 전체 파이프라인 테스트 시작")
        
        # 1단계: 워크스페이스 준비 (장 선택 적용)
        print(f"\n1️⃣ 워크스페이스 준비 단계 시작...")
        stage1_result = asyncio.run(self._run_workspace_preparation())
        
        self.assertTrue(stage1_result['success'], f"1단계 실패: {stage1_result.get('error')}")
        self.stage1_result = stage1_result
        
        # 1단계 결과에서 실제 생성된 책 폴더 경로 추출
        actual_book_dir = Path(stage1_result['output_directory'])
        self.assertTrue(actual_book_dir.exists(), f"책 폴더가 생성되지 않음: {actual_book_dir}")
        
        created_folders = stage1_result['created_folders']
        print(f"✅ 1단계 완료: {len(created_folders)}개 장 폴더 생성")
        print(f"📁 실제 생성된 책 폴더: {actual_book_dir}")
        
        # 선택된 장만 생성되었는지 확인
        self.assertEqual(len(created_folders), len(self.selected_chapters), 
                        f"선택된 장 개수 불일치: 예상 {len(self.selected_chapters)}개, 실제 {len(created_folders)}개")
        
        for folder_info in created_folders:
            folder_path = Path(folder_info['folder_path'])
            self.assertTrue(folder_path.exists(), f"장 폴더가 없음: {folder_path}")
            print(f"   📂 생성된 장 폴더: {folder_path.name}")
            
        # 2단계: 통합 노드 생성 (실제 생성된 책 폴더 경로 사용)
        print(f"\n2️⃣ 통합 노드 생성 단계 시작...")
        stage2_result = asyncio.run(self._run_integrated_node_generation(str(actual_book_dir)))
        
        self.assertTrue(stage2_result['success'], f"2단계 실패: {stage2_result.get('error')}")
        self.stage2_result = stage2_result
        
        print(f"✅ 2단계 완료: {stage2_result['data']['processed_chapters']}개 장 처리")
        
        # 3단계: 콘텐츠 처리 (각 생성된 장 폴더에 대해)
        print(f"\n3️⃣ 콘텐츠 처리 단계 시작...")
        stage3_results = []
        
        for folder_info in created_folders:
            chapter_folder = folder_info['folder_path']
            print(f"📁 장 폴더 처리: {Path(chapter_folder).name}")
            
            stage3_result = asyncio.run(self._run_content_processing(chapter_folder))
            stage3_results.append(stage3_result)
            
            self.assertTrue(stage3_result['success'], f"3단계 실패: {stage3_result.get('error')}")
        
        self.stage3_result = stage3_results
        print(f"✅ 3단계 완료: {len(stage3_results)}개 장 콘텐츠 처리")
        
        # 최종 결과 검증
        self._verify_final_results(actual_book_dir, created_folders)
        
        print(f"\n🎉 전체 파이프라인 테스트 성공!")
        print(f"📊 최종 결과:")
        print(f"   - 처리된 장: {len(created_folders)}개")
        print(f"   - 선택된 장: {self.selected_chapters}")
        print(f"   - 총 노드: {stage2_result['data'].get('processed_chapters', 0)}개")
        print(f"   - 최종 출력 경로: {actual_book_dir}")

    def test_workspace_preparation_stage(self):
        """1단계 워크스페이스 준비 단계 개별 테스트"""
        print(f"\n🧪 1단계 워크스페이스 준비 단계 테스트 (장 선택: {self.selected_chapters})")
        
        result = asyncio.run(self._run_workspace_preparation())
        
        self.assertTrue(result['success'], f"워크스페이스 준비 실패: {result.get('error')}")
        self.assertIn('normalized_book_title', result)
        self.assertIn('created_folders', result)
        
        # 선택된 장 개수와 실제 생성된 폴더 개수 일치 확인
        self.assertEqual(len(result['created_folders']), len(self.selected_chapters), 
                        f"장 필터링 실패: 선택 {len(self.selected_chapters)}개, 생성 {len(result['created_folders'])}개")
        
        print(f"✅ 1단계 테스트 통과: {result['normalized_book_title']} - {len(result['created_folders'])}개 장 생성")

    def test_integrated_node_generation_stage(self):
        """2단계 통합 노드 생성 단계 개별 테스트"""
        print(f"\n🧪 2단계 통합 노드 생성 단계 테스트")
        
        # 1단계 먼저 실행
        stage1_result = asyncio.run(self._run_workspace_preparation())
        self.assertTrue(stage1_result['success'])
        
        # 2단계 실행 (실제 생성된 책 폴더 경로 사용)
        book_dir = stage1_result['output_directory']
        result = asyncio.run(self._run_integrated_node_generation(book_dir))
        
        self.assertTrue(result['success'], f"통합 노드 생성 실패: {result.get('error')}")
        self.assertIn('data', result)
        self.assertIn('processed_chapters', result['data'])
        
        print(f"✅ 2단계 테스트 통과: {result['data']['processed_chapters']}개 장 처리")

    def test_content_processing_stage(self):
        """3단계 콘텐츠 처리 단계 개별 테스트"""
        print(f"\n🧪 3단계 콘텐츠 처리 단계 테스트")
        
        # 1, 2단계 먼저 실행
        stage1_result = asyncio.run(self._run_workspace_preparation())
        self.assertTrue(stage1_result['success'])
        
        book_dir = stage1_result['output_directory']
        stage2_result = asyncio.run(self._run_integrated_node_generation(book_dir))
        self.assertTrue(stage2_result['success'])
        
        # 3단계 실행 (첫 번째 생성된 장 폴더만)
        if stage1_result['created_folders']:
            first_folder = stage1_result['created_folders'][0]
            result = asyncio.run(self._run_content_processing(first_folder['folder_path']))
            
            self.assertTrue(result['success'], f"콘텐츠 처리 실패: {result.get('error')}")
            print(f"✅ 3단계 테스트 통과: {result.get('processed_count', 0)}개 문서 처리")
        else:
            self.fail("테스트할 장 폴더가 생성되지 않음")

    async def _run_workspace_preparation(self):
        """1단계: 워크스페이스 준비 실행"""
        stage = WorkspacePreparationStage(self.config_manager, self.logger_factory)
        
        input_data = {
            'pdf_path': self.pdf_path
        }
        
        return await stage.process(input_data)
    
    async def _run_integrated_node_generation(self, book_directory: str):
        """2단계: 통합 노드 생성 실행"""
        stage = IntegratedNodeGenerationStage(self.config_manager, self.logger_factory)
        
        input_data = {
            'book_directory': book_directory
        }
        
        return await stage.process(input_data)
    
    async def _run_content_processing(self, chapter_folder: str):
        """3단계: 콘텐츠 처리 실행"""
        # ContentProcessingStage는 config와 ai_service를 별도로 받음
        # Logger를 제대로 생성해서 전달
        logger = Logger("content_processing_test")
        ai_service = AIService(self.config_manager, logger, "content_processing")
        
        config = {
            'processing_mode': 'unified_type_processing',
            'max_parallel': 4
        }
        
        stage = ContentProcessingStage(config, ai_service)
        
        return await stage.process(chapter_folder)
    
    def _setup_test_config_manager(self):
        """테스트용 ConfigManager 설정 (장 선택 기능 포함)"""
        # 테스트용 설정 생성 (메모리에서)
        test_pipeline_config = {
            'test_mode': {
                'enabled': True,  # 🔥 테스트 모드 활성화
                'selected_chapters': self.selected_chapters,  # 🎯 선택된 장
                'debug_verbose': True,
                'skip_on_error': False
            },
            'workspace_preparation': {
                'folder_structure': {
                    'base_path': str(self.test_output_dir)  # 📁 테스트 출력 경로
                }
            },
            'global': {
                'logs_base_dir': str(self.test_output_dir / "logs")
            }
        }
        
        # ConfigManager 인스턴스 생성 후 설정 주입
        config_manager = ConfigManager()
        config_manager.pipeline_config = test_pipeline_config
        
        return config_manager
    
    def _verify_final_results(self, actual_book_dir: Path, created_folders: list):
        """최종 결과 검증"""
        print(f"\n🔍 최종 결과 검증 시작...")
        
        # 각 선택된 장 폴더가 올바르게 생성되었는지 확인
        for folder_info in created_folders:
            chapter_folder = Path(folder_info['folder_path'])
            
            # 기본 파일들 확인 (WorkspacePreparationStage 결과)
            content_files = list(chapter_folder.glob("*_content.md"))
            toc_files = list(chapter_folder.glob("*_toc.json"))
            
            self.assertTrue(len(content_files) > 0, f"content 파일 없음: {chapter_folder}")
            self.assertTrue(len(toc_files) > 0, f"toc 파일 없음: {chapter_folder}")
            
            print(f"   ✅ 기본 파일 확인: {chapter_folder.name}")
            
            # 2단계 결과 확인 (IntegratedNodeGenerationStage 결과)
            node_docs_dir = chapter_folder / "node_info_docs"
            sections_dir = chapter_folder / "sections"
            unified_docs_dir = chapter_folder / "unified_info_docs"
            
            if self.stage2_result and self.stage2_result['success']:
                self.assertTrue(node_docs_dir.exists(), f"node_info_docs 폴더 없음: {chapter_folder}")
                self.assertTrue(unified_docs_dir.exists(), f"unified_info_docs 폴더 없음: {chapter_folder}")
                print(f"   ✅ 2단계 결과 확인: {chapter_folder.name}")
            
            # 3단계 결과 확인 (ContentProcessingStage 결과)
            if self.stage3_result:
                # unified_info_docs 내 파일들이 process_status: true로 업데이트되었는지 확인
                unified_files = list(unified_docs_dir.glob("*_info.md"))
                if unified_files:
                    # 첫 번째 파일 샘플 확인
                    sample_file = unified_files[0]
                    with open(sample_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'process_status: true' in content or '## 핵심 내용' in content:
                            print(f"   ✅ 3단계 결과 확인: {chapter_folder.name}")
                        else:
                            print(f"   ⚠️ 3단계 처리 미완료: {chapter_folder.name}")
        
        print(f"✅ 최종 결과 검증 완료")


if __name__ == '__main__':
    # 특정 장 번호로 테스트 실행 가능
    unittest.main(verbosity=2)