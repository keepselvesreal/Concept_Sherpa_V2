# 생성 시간: Tue Sep  2 11:29:03 KST 2025
# 핵심 내용: 선별된 장(1,6,9장)에 대한 파이프라인 동작 점검용 테스트 스크립트
# 상세 내용:
#   - test_selected_chapters_pipeline (라인 95-190): 메인 테스트 함수
#   - filter_selected_chapters (라인 45-93): 선별 장 필터링 함수
#   - main (라인 192-223): 스크립트 실행 진입점
#   - SelectedChaptersPipeline (라인 25-43): 선별 장 처리용 파이프라인 래퍼 클래스
# 상태: active
# 주소: test_selected_chapters
# 참조: book_pipeline_v3.py

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 기존 파이프라인 임포트
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')
from book_pipeline_v3 import BookPipeline, PipelineResult

# 추가 모듈 임포트
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29')
from extract_chapters_v5 import normalize_title

class SelectedChaptersPipeline:
    """선별된 장만 처리하는 파이프라인 래퍼"""
    
    def __init__(self, selected_chapter_numbers: List[int]):
        self.selected_chapter_numbers = selected_chapter_numbers
        self.pipeline = BookPipeline(test_mode=False, max_chapters=None)  # 일반 모드로 생성
        
    def get_selected_chapters_info(self) -> str:
        """선별된 장 정보 반환"""
        return f"선별된 장: {', '.join(map(str, self.selected_chapter_numbers))}장"
    
    async def execute_selected_chapters(self, pdf_path: str) -> Dict[str, Any]:
        """선별된 장만 처리하는 파이프라인 실행"""
        print(f"🎯 {self.get_selected_chapters_info()} 처리 시작")
        
        # 1단계: 전체 워크스페이스 준비 (모든 장 폴더 생성)
        workspace_data = await self.pipeline.prepare_chapter_workspace(pdf_path)
        if not workspace_data.get('success', False):
            return {'success': False, 'error': workspace_data.get('error')}
        
        # 선별된 장만 필터링
        filtered_workspace = filter_selected_chapters(workspace_data, self.selected_chapter_numbers)
        
        # 2-4단계: 선별된 장만 처리
        integration_data = await self.pipeline.integrate_chapter_information_sequentially(filtered_workspace, pdf_path)
        node_processing_data = await self.pipeline.process_node_documents(integration_data)
        enhanced_toc_data = await self.pipeline.generate_enhanced_toc(node_processing_data)
        
        return {
            'success': True,
            'workspace_info': filtered_workspace,
            'integration_info': integration_data,
            'node_processing_info': node_processing_data,
            'enhanced_toc_info': enhanced_toc_data,
            'selected_chapters': self.selected_chapter_numbers
        }

def filter_selected_chapters(workspace_data: Dict[str, Any], selected_chapter_numbers: List[int]) -> Dict[str, Any]:
    """워크스페이스 데이터에서 선별된 장만 필터링"""
    
    print(f"🔍 선별 필터링: {selected_chapter_numbers}장만 추출")
    
    original_folders = workspace_data.get('created_folders', [])
    if not original_folders:
        print("⚠️ 생성된 장 폴더가 없습니다")
        return workspace_data
    
    print(f"📂 전체 생성된 장: {len(original_folders)}개")
    
    # 선별된 장만 필터링
    selected_folders = []
    for folder_info in original_folders:
        chapter_number = folder_info.get('chapter_number')
        if chapter_number in selected_chapter_numbers:
            selected_folders.append(folder_info)
            print(f"  ✅ 장 {chapter_number}: {folder_info.get('chapter_title', '')} - 선택됨")
        else:
            print(f"  ⏭️ 장 {chapter_number}: {folder_info.get('chapter_title', '')} - 건너뜀")
    
    print(f"🎯 최종 선별된 장: {len(selected_folders)}개")
    
    # 선별된 장 목록 상세 출력
    for i, folder in enumerate(selected_folders, 1):
        chapter_number = folder.get('chapter_number')
        chapter_title = folder.get('chapter_title', '')
        folder_path = folder.get('folder_path', '')
        
        print(f"  {i}. 장 {chapter_number}: {chapter_title}")
        print(f"     📁 경로: {folder_path}")
        print(f"     📄 목차파일: {folder.get('toc_file', 'N/A')}")
        print(f"     📊 페이지: {folder.get('page_range', 'N/A')}")
        print(f"     🔢 항목수: {folder.get('items_count', 0)}")
        print()
    
    # 필터링된 워크스페이스 데이터 반환
    filtered_data = workspace_data.copy()
    filtered_data['created_folders'] = selected_folders
    filtered_data['total_chapters'] = len(selected_folders)
    filtered_data['original_total_chapters'] = len(original_folders)
    filtered_data['selected_chapter_numbers'] = selected_chapter_numbers
    filtered_data['filtering_applied'] = True
    
    return filtered_data

async def test_selected_chapters_pipeline():
    """선별된 장(1,6,9장) 파이프라인 테스트"""
    
    print("🚀 선별된 장 파이프라인 테스트 시작")
    print("=" * 60)
    
    # 테스트 설정
    selected_chapters = [1, 6, 9]  # 테스트할 장 번호들
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/inbox/Data_Oriented_Programming.pdf"
    
    print(f"📚 PDF 파일: {os.path.basename(pdf_path)}")
    print(f"🎯 선별 장: {', '.join(map(str, selected_chapters))}장")
    print(f"⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # PDF 파일 존재 확인
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    try:
        # 선별된 장 파이프라인 생성 및 실행
        pipeline = SelectedChaptersPipeline(selected_chapters)
        
        print(f"🔧 {pipeline.get_selected_chapters_info()} 파이프라인 초기화 완료")
        print()
        
        # 파이프라인 실행
        start_time = datetime.now()
        result = await pipeline.execute_selected_chapters(pdf_path)
        end_time = datetime.now()
        duration = end_time - start_time
        
        print()
        print("=" * 60)
        print("🏁 테스트 완료!")
        print(f"⏱️ 소요 시간: {duration}")
        
        if result.get('success', False):
            print("✅ 테스트 성공!")
            
            # 결과 상세 분석
            workspace_info = result.get('workspace_info', {})
            integration_info = result.get('integration_info', {})
            node_processing_info = result.get('node_processing_info', {})
            enhanced_toc_info = result.get('enhanced_toc_info', {})
            
            print("\n📊 처리 결과 요약:")
            print(f"  📚 책 제목: {workspace_info.get('book_title', 'N/A')}")
            print(f"  🎯 선별 장수: {len(selected_chapters)}장")
            print(f"  📂 전체 생성된 장: {workspace_info.get('original_total_chapters', 0)}장")
            print(f"  ✅ 통합 처리 완료: {integration_info.get('processed_chapters', 0)}장")
            print(f"  📋 노드 문서 처리: {node_processing_info.get('processed_chapters', 0)}장")
            print(f"  📄 Enhanced TOC 생성: {enhanced_toc_info.get('generated_count', 0)}개")
            
            # 성공률 계산
            target_count = len(selected_chapters)
            success_count = integration_info.get('processed_chapters', 0)
            success_rate = (success_count / target_count * 100) if target_count > 0 else 0
            
            print(f"  📈 성공률: {success_count}/{target_count} ({success_rate:.1f}%)")
            
            # 로그 디렉토리 정보
            logs_dir = workspace_info.get('book_title')
            if logs_dir:
                normalized_title = normalize_title(logs_dir)
                logs_path = f"/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs/{normalized_title}"
                print(f"  📋 로그 디렉토리: {logs_path}")
                
                # update_history 폴더 확인
                update_history_path = f"{logs_path}/update_history"
                if os.path.exists(update_history_path):
                    print(f"  📁 update_history: {update_history_path} ✅")
                else:
                    print(f"  📁 update_history: 아직 생성되지 않음 (노드 처리 후 생성됨)")
            
            # 생성된 폴더 상세 정보
            print("\n📁 생성된 장별 폴더:")
            created_folders = workspace_info.get('created_folders', [])
            for folder in created_folders:
                chapter_num = folder.get('chapter_number')
                chapter_title = folder.get('chapter_title', '')
                folder_path = folder.get('folder_path', '')
                print(f"  장 {chapter_num}: {chapter_title}")
                print(f"    📁 {folder_path}")
                
        else:
            print("❌ 테스트 실패!")
            error = result.get('error', '알 수 없는 오류')
            print(f"🚨 오류: {error}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ 테스트 실행 중 예외 발생: {str(e)}")
        print(f"⏰ 실패 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """메인 실행 함수"""
    print("🔍 선별된 장(1,6,9장) 파이프라인 동작 점검")
    print("=" * 60)
    print("📋 목적: 전체 장 처리 없이 특정 장만 선별하여 파이프라인 동작 검증")
    print("⚠️ 주의: 이 스크립트는 기존 파이프라인 코드를 수정하지 않음")
    print("🎯 대상: Data_Oriented_Programming.pdf의 1, 6, 9장")
    print()
    
    try:
        # 비동기 함수 실행
        asyncio.run(test_selected_chapters_pipeline())
        
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"\n💥 실행 중 치명적 오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()