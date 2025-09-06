# 생성 시간: Wed Sep  4 12:08:15 KST 2025
# 핵심 내용: 선택된 장들의 실제 노드 문서 생성 및 결과 확인 테스트
# 상세 내용:
#   - TestSelectedChaptersNodeGeneration (라인 26-200): 선택된 장들의 노드 문서 생성 테스트 클래스
#   - test_generate_nodes_for_selected_chapters (라인 40-120): 1,6,9장의 노드 문서 생성 테스트
#   - save_generated_nodes (라인 122-180): 생성된 노드 문서들을 파일로 저장
#   - display_node_summary (라인 182-200): 생성된 노드들의 요약 정보 출력
# 상태: active
# 참조: test_integrated_node_with_specific_chapters.py

import pytest
import asyncio
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# 서비스와 설정 클래스들 임포트
from services.node_document_service import NodeDocumentService
from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory

class TestSelectedChaptersNodeGeneration:
    """
    테스트 유형: Social Unit Test
    선택된 장들(1, 6, 9장)의 실제 노드 문서 생성 및 결과 확인 테스트
    
    요구사항:
    - 워크스페이스에서 생성된 실제 TOC 데이터 사용
    - 1, 6, 9장의 노드 문서를 실제로 생성
    - 생성된 결과를 파일로 저장하여 사용자가 확인 가능하게 함
    
    입력: 워크스페이스의 실제 장별 TOC 파일들
    출력: 선택된 장들의 노드 문서 파일들 + 요약 정보
    """
    
    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.config_manager = ConfigManager()
        self.logger_factory = LoggerFactory(self.config_manager)
        self.test_logger = self.logger_factory.create_book_logger("selected_chapters_test", "./logs")
        
        # NodeDocumentService 초기화
        self.node_document_service = NodeDocumentService(self.config_manager, self.test_logger)
        
        # 기본 설정
        self.target_chapters = [1, 6, 9]
        self.workspace_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output/Data_Oriented_Programming"
        self.result_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/results/selected_chapters_nodes"
        
    @pytest.mark.anyio
    async def test_generate_nodes_for_selected_chapters(self):
        """
        선택된 장들의 실제 TOC 데이터를 사용하여 노드 문서 생성 테스트
        """
        print(f"\n🚀 선택된 장들의 노드 문서 생성 테스트 시작")
        print(f"   🎯 대상 장: {self.target_chapters}")
        print(f"   📁 워크스페이스: {self.workspace_path}")
        
        # 결과 저장 디렉토리 생성
        os.makedirs(self.result_dir, exist_ok=True)
        print(f"   💾 결과 저장 경로: {self.result_dir}")
        
        chapter_results = []
        
        for chapter_num in self.target_chapters:
            print(f"\n📖 장 {chapter_num} 노드 문서 생성 중...")
            
            # 1. 장 폴더 찾기
            chapter_folder = None
            for folder in os.listdir(self.workspace_path):
                if folder.startswith(f"{chapter_num}_") and os.path.isdir(os.path.join(self.workspace_path, folder)):
                    chapter_folder = folder
                    break
            
            if not chapter_folder:
                print(f"   ❌ 장 {chapter_num} 폴더를 찾을 수 없습니다.")
                continue
                
            print(f"   📂 장 폴더: {chapter_folder}")
            
            # 2. TOC 파일 읽기
            toc_file = os.path.join(self.workspace_path, chapter_folder, f"{chapter_folder}_toc.json")
            if not os.path.exists(toc_file):
                print(f"   ❌ TOC 파일을 찾을 수 없습니다: {toc_file}")
                continue
            
            with open(toc_file, 'r', encoding='utf-8') as f:
                chapter_toc = json.load(f)
            
            print(f"   📋 TOC 항목 수: {len(chapter_toc)}")
            
            # 3. NodeDocumentService를 사용하여 노드 문서 생성
            try:
                # generate_documents_for_chapter 메서드 사용
                chapter_output_dir = os.path.join(self.result_dir, f"chapter_{chapter_num:02d}")
                os.makedirs(chapter_output_dir, exist_ok=True)
                
                generation_result = self.node_document_service.generate_documents_for_chapter(
                    chapter_folder=chapter_output_dir,
                    toc_file=toc_file
                )
                
                if generation_result.success:
                    generated_files = generation_result.created_files
                    print(f"   ✅ 노드 문서 생성 완료: {generation_result.created_count}개 파일")
                    
                    chapter_results.append({
                        'chapter_number': chapter_num,
                        'chapter_folder': chapter_folder,
                        'toc_items_count': len(chapter_toc),
                        'generated_files_count': generation_result.created_count,
                        'generated_files': generated_files,
                        'success': True
                    })
                    
                    # 생성된 파일들 나열
                    for file_path in generated_files[:3]:  # 처음 3개만 출력
                        print(f"     📄 {os.path.basename(file_path)}")
                    if len(generated_files) > 3:
                        print(f"     ... 외 {len(generated_files)-3}개 파일")
                        
                else:
                    print(f"   ❌ 노드 문서 생성 실패: {generation_result.error}")
                    chapter_results.append({
                        'chapter_number': chapter_num,
                        'chapter_folder': chapter_folder,
                        'success': False,
                        'error': str(generation_result.error)
                    })
            
            except Exception as e:
                print(f"   ❌ 노드 문서 생성 중 오류: {str(e)}")
                chapter_results.append({
                    'chapter_number': chapter_num,
                    'chapter_folder': chapter_folder,
                    'success': False,
                    'error': str(e)
                })
        
        # 4. 결과 요약 저장 및 출력
        await self.save_generation_summary(chapter_results)
        self.display_generation_summary(chapter_results)
        
        return chapter_results
    
    async def save_generation_summary(self, chapter_results: List[Dict]):
        """생성 결과 요약을 JSON 파일로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = os.path.join(self.result_dir, f"node_generation_summary_{timestamp}.json")
        
        summary_data = {
            'test_timestamp': timestamp,
            'target_chapters': self.target_chapters,
            'workspace_path': self.workspace_path,
            'result_directory': self.result_dir,
            'chapters_processed': len(chapter_results),
            'chapters_success': len([r for r in chapter_results if r.get('success', False)]),
            'total_generated_files': sum(r.get('generated_files_count', 0) for r in chapter_results if r.get('success', False)),
            'chapter_results': chapter_results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 결과 요약 저장 완료: {summary_file}")
    
    def display_generation_summary(self, chapter_results: List[Dict]):
        """생성 결과 요약 정보 출력"""
        print(f"\n🎉 선택된 장들의 노드 문서 생성 완료!")
        print(f"   📊 처리된 장: {len(chapter_results)}/{len(self.target_chapters)}")
        
        success_count = len([r for r in chapter_results if r.get('success', False)])
        print(f"   ✅ 성공한 장: {success_count}")
        
        total_files = sum(r.get('generated_files_count', 0) for r in chapter_results if r.get('success', False))
        print(f"   📄 총 생성 파일: {total_files}개")
        
        print(f"\n📋 장별 상세 결과:")
        for result in chapter_results:
            status = "✅" if result.get('success', False) else "❌"
            chapter_num = result['chapter_number']
            if result.get('success', False):
                file_count = result.get('generated_files_count', 0)
                print(f"   {status} 장 {chapter_num}: {file_count}개 노드 문서 생성")
            else:
                error = result.get('error', '알 수 없는 오류')
                print(f"   {status} 장 {chapter_num}: 실패 - {error}")