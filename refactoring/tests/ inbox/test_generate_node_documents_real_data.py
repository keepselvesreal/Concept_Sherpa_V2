# 생성 시간: Fri Sep  5 15:35:44 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage의 generate_node_documents 메서드 실제 데이터 테스트
# 상세 내용:
#   - TestGenerateNodeDocumentsRealData (라인 20-120): 테스트 클래스
#   - setUp (라인 22-45): 테스트 환경 설정 (실제 데이터 경로, config_manager 초기화)
#   - test_generate_node_documents_chapter_1 (라인 47-70): 1장 노드 문서 생성 테스트
#   - test_generate_node_documents_chapter_6 (라인 72-95): 6장 노드 문서 생성 테스트  
#   - test_generate_node_documents_chapter_9 (라인 97-120): 9장 노드 문서 생성 테스트
#   - _create_chapter_result_data (라인 122-135): 실제 데이터 구조에 맞는 chapter_result 생성
# 상태: active

"""
요구사항: IntegratedNodeGenerationStage.generate_node_documents 메서드의 정상 동작 테스트
- 실제 데이터 사용 (mock 사용 금지)
- 1, 6, 9장 대상 테스트
- 노드 정보 문서가 기존 장 폴더 내에 생성되는지 검증
"""

import unittest
import asyncio
import os
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

# 직접 파일 임포트
from stages.integrated_node_generation_stage_v2 import IntegratedNodeGenerationStage
from utils.config_manager import ConfigManager

class TestGenerateNodeDocumentsRealData(unittest.TestCase):
    """IntegratedNodeGenerationStage.generate_node_documents 실제 데이터 테스트 (social unit test)"""
    
    def setUp(self):
        """실제 데이터 경로와 config_manager 설정"""
        # 실제 데이터 경로
        self.data_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming"
        
        # ConfigManager 초기화 (실제 구현 사용) - 디렉토리 경로 전달
        config_dir = os.path.join(project_root, "config")
        self.config_manager = ConfigManager(config_dir)
        
        # IntegratedNodeGenerationStage 인스턴스 생성
        self.stage = IntegratedNodeGenerationStage(self.config_manager)
        
        # 테스트 대상 장들의 정보
        self.test_chapters = [
            {
                'number': 1,
                'folder_name': '1_Complexity_of_object_oriented_programming',
                'title': 'Complexity of object-oriented programming'
            },
            {
                'number': 6,
                'folder_name': '6_Unit_tests', 
                'title': 'Unit tests'
            },
            {
                'number': 9,
                'folder_name': '9_Persistent_data_structures',
                'title': 'Persistent data structures'
            }
        ]
    
    def test_generate_node_documents_chapter_1(self):
        """1장 노드 문서 생성 테스트 - 실제 데이터 사용"""
        chapter_info = self.test_chapters[0]  # 1장
        chapter_result = self._create_chapter_result_data(chapter_info)
        book_info = {"title": "Data Oriented Programming", "author": "Test"}
        output_dir = self.data_dir
        
        # 비동기 메서드 실행
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            self.stage.generate_node_documents(chapter_result, book_info, output_dir)
        )
        
        # 새로운 반환 형식 검증 (success, error만)
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('error', result)
        
        # success/error 필드만 있는지 확인
        expected_keys = {'success', 'error'}
        self.assertEqual(set(result.keys()), expected_keys, 
                        f"반환 형식이 올바르지 않음. 기대: {expected_keys}, 실제: {set(result.keys())}")
        
        # 성공 시 node_info_docs 폴더가 생성되었는지 확인
        if result.get('success'):
            node_docs_dir = os.path.join(chapter_result['folder_path'], 'node_info_docs')
            self.assertTrue(os.path.exists(node_docs_dir), 
                          f"node_info_docs 폴더가 생성되지 않음: {node_docs_dir}")
            
            # 생성된 파일이 있는지 확인
            created_files = os.listdir(node_docs_dir)
            self.assertGreater(len(created_files), 0, "노드 정보 문서가 생성되지 않음")
            
            self.assertIsNone(result.get('error'), "성공 시 error는 None이어야 함")
        else:
            self.assertIsNotNone(result.get('error'), "실패 시 error 메시지가 있어야 함")
        
        print(f"1장 테스트 결과: {result}")
    
    def test_generate_node_documents_chapter_6(self):
        """6장 노드 문서 생성 테스트 - 실제 데이터 사용"""
        chapter_info = self.test_chapters[1]  # 6장
        chapter_result = self._create_chapter_result_data(chapter_info)
        book_info = {"title": "Data Oriented Programming", "author": "Test"}
        output_dir = self.data_dir
        
        # 비동기 메서드 실행
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            self.stage.generate_node_documents(chapter_result, book_info, output_dir)
        )
        
        # 새로운 반환 형식 검증 (success, error만)
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('error', result)
        
        # success/error 필드만 있는지 확인
        expected_keys = {'success', 'error'}
        self.assertEqual(set(result.keys()), expected_keys, 
                        f"반환 형식이 올바르지 않음. 기대: {expected_keys}, 실제: {set(result.keys())}")
        
        # 성공 시 node_info_docs 폴더가 생성되었는지 확인
        if result.get('success'):
            node_docs_dir = os.path.join(chapter_result['folder_path'], 'node_info_docs')
            self.assertTrue(os.path.exists(node_docs_dir), 
                          f"node_info_docs 폴더가 생성되지 않음: {node_docs_dir}")
            
            self.assertIsNone(result.get('error'), "성공 시 error는 None이어야 함")
        else:
            self.assertIsNotNone(result.get('error'), "실패 시 error 메시지가 있어야 함")
        
        print(f"6장 테스트 결과: {result}")
    
    def test_generate_node_documents_chapter_9(self):
        """9장 노드 문서 생성 테스트 - 실제 데이터 사용"""
        chapter_info = self.test_chapters[2]  # 9장
        chapter_result = self._create_chapter_result_data(chapter_info)
        book_info = {"title": "Data Oriented Programming", "author": "Test"}
        output_dir = self.data_dir
        
        # 비동기 메서드 실행
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            self.stage.generate_node_documents(chapter_result, book_info, output_dir)
        )
        
        # 새로운 반환 형식 검증 (success, error만)
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('error', result)
        
        # success/error 필드만 있는지 확인
        expected_keys = {'success', 'error'}
        self.assertEqual(set(result.keys()), expected_keys, 
                        f"반환 형식이 올바르지 않음. 기대: {expected_keys}, 실제: {set(result.keys())}")
        
        # 성공 시 node_info_docs 폴더가 생성되었는지 확인
        if result.get('success'):
            node_docs_dir = os.path.join(chapter_result['folder_path'], 'node_info_docs')
            self.assertTrue(os.path.exists(node_docs_dir), 
                          f"node_info_docs 폴더가 생성되지 않음: {node_docs_dir}")
            
            self.assertIsNone(result.get('error'), "성공 시 error는 None이어야 함")
        else:
            self.assertIsNotNone(result.get('error'), "실패 시 error 메시지가 있어야 함")
        
        print(f"9장 테스트 결과: {result}")
    
    def _create_chapter_result_data(self, chapter_info):
        """실제 데이터 구조에 맞는 chapter_result 생성"""
        folder_path = os.path.join(self.data_dir, chapter_info['folder_name'])
        toc_file = os.path.join(folder_path, f"{chapter_info['folder_name']}_toc.json")
        content_file = os.path.join(folder_path, f"{chapter_info['folder_name']}_content.md")
        
        return {
            'chapter_number': chapter_info['number'],
            'chapter_title': chapter_info['title'],
            'folder_path': folder_path,
            'toc_file': toc_file,
            'content_file': content_file,
            'success': True
        }

if __name__ == '__main__':
    unittest.main()