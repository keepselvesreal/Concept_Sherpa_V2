# 생성 시간: Thu Sep  4 11:43:27 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 특정 장별 테스트 (1, 6, 9장 등 원하는 장만 선택, ResultLogger로 결과 저장)
# 상세 내용:
#   - TestSpecificChapters (라인 XX-XX): 특정 장 선택 테스트 클래스
#   - test_specific_chapters_integration (라인 XX-XX): 지정된 장들만 통합 노드 생성 테스트
#   - save_integrated_node_documents (라인 XX-XX): 생성된 통합 노드 문서들을 ResultLogger로 저장
#   - filter_chapters_by_numbers (라인 XX-XX): 특정 장 번호로 필터링하는 헬퍼 메서드
# 상태: active

import pytest
import asyncio
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List

# 필요한 모듈 임포트  
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from stages.integrated_node_generation_stage import IntegratedNodeGenerationStage
from stages.workspace_preparation import WorkspacePreparationStage
from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory

class TestSpecificChapters:
    """특정 장들만 선택하여 IntegratedNodeGenerationStage 테스트"""
    
    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.config_manager = ConfigManager()
        self.logger_factory = LoggerFactory(self.config_manager)
        
        # ResultLogger 생성 (통합 노드 문서 저장용)
        self.result_logger = self.logger_factory.create_result_logger("integrated_node_test")
        
    def filter_chapters_by_numbers(self, created_folders: List[Dict], target_chapters: List[int]) -> List[Dict]:
        """
        특정 장 번호들로 폴더 리스트 필터링
        
        Args:
            created_folders: 워크스페이스에서 생성된 전체 장 폴더 리스트
            target_chapters: 처리하고 싶은 장 번호들 (예: [1, 6, 9])
            
        Returns:
            필터링된 장 폴더 리스트
        """
        filtered_folders = []
        
        for folder_info in created_folders:
            chapter_number = folder_info.get('chapter_number', 0)
            if chapter_number in target_chapters:
                filtered_folders.append(folder_info)
                print(f"✅ 장 {chapter_number} 선택됨: {folder_info.get('chapter_title', '')}")
            else:
                print(f"⏭️  장 {chapter_number} 건너뜀")
                
        return filtered_folders
    
    def save_integrated_node_documents(self, stage_results: Dict[str, Any], workspace_result: Dict[str, Any]):
        """
        생성된 통합 노드 문서들을 ResultLogger로 저장
        
        Args:
            stage_results: IntegratedNodeGenerationStage.process() 결과
            workspace_result: 워크스페이스 준비 결과
        """
        print(f"\n📁 통합 노드 문서 결과 저장 시작...")
        
        # 1. 전체 결과 요약 저장
        summary_data = {
            'test_summary': {
                'success': stage_results.get('success', False),
                'processed_chapters': stage_results.get('processed_chapters', 0),
                'total_chapters': stage_results.get('total_chapters', 0),
                'success_rate': stage_results.get('success_rate', 0)
            },
            'workspace_info': {
                'book_title': workspace_result.get('book_info', {}).get('title', 'Unknown'),
                'output_dir': workspace_result.get('output_dir', ''),
                'total_created_folders': len(workspace_result.get('created_folders', []))
            },
            'processing_results': stage_results.get('node_processing_results', [])
        }
        
        summary_file = self.result_logger.save_result("integration_summary", summary_data, "json")
        print(f"   📄 요약 파일: {summary_file}")
        
        # 2. 각 장별 상세 결과 저장
        node_processing_results = stage_results.get('node_processing_results', [])
        
        for chapter_result in node_processing_results:
            if not chapter_result.get('success', False):
                continue
                
            chapter_num = chapter_result.get('chapter_number', 0)
            chapter_title = chapter_result.get('chapter_title', 'Unknown')
            
            # 장별 상세 데이터
            chapter_data = {
                'chapter_info': {
                    'number': chapter_num,
                    'title': chapter_title
                },
                'processing_stages': {
                    'node_documents': chapter_result.get('node_docs', {}),
                    'content_nodes': chapter_result.get('content_nodes', {}),
                    'integration': chapter_result.get('integration', {})
                },
                'file_locations': self._get_chapter_file_locations(chapter_num, workspace_result)
            }
            
            # 장별 파일 저장
            chapter_file = self.result_logger.save_result(
                f"chapter_{chapter_num:02d}_integration_result", 
                chapter_data, 
                "json"
            )
            print(f"   📄 장 {chapter_num} 상세 결과: {chapter_file}")
            
            # 마크다운 리포트도 생성
            md_content = self._create_chapter_markdown_report(chapter_data)
            md_file = self.result_logger.save_result(
                f"chapter_{chapter_num:02d}_report",
                md_content,
                "md"
            )
            print(f"   📄 장 {chapter_num} 마크다운 리포트: {md_file}")
        
        print(f"✅ 통합 노드 문서 결과 저장 완료!")
    
    def _get_chapter_file_locations(self, chapter_number: int, workspace_result: Dict[str, Any]) -> Dict[str, Any]:
        """장별 생성된 파일들의 위치 정보 수집"""
        created_folders = workspace_result.get('created_folders', [])
        
        for folder_info in created_folders:
            if folder_info.get('chapter_number') == chapter_number:
                folder_path = folder_info.get('path', '')
                toc_file = folder_info.get('toc_file', '')
                
                file_locations = {
                    'chapter_folder': folder_path,
                    'toc_file': toc_file,
                    'existing_files': []
                }
                
                # 폴더 내 실제 파일들 확인
                if os.path.exists(folder_path):
                    try:
                        for item in os.listdir(folder_path):
                            item_path = os.path.join(folder_path, item)
                            if os.path.isfile(item_path):
                                file_locations['existing_files'].append({
                                    'name': item,
                                    'path': item_path,
                                    'size': os.path.getsize(item_path)
                                })
                            elif os.path.isdir(item_path):
                                # 서브디렉터리도 확인 (node_info_docs 등)
                                subdir_files = []
                                try:
                                    for subitem in os.listdir(item_path):
                                        subitem_path = os.path.join(item_path, subitem)
                                        if os.path.isfile(subitem_path):
                                            subdir_files.append({
                                                'name': subitem,
                                                'path': subitem_path,
                                                'size': os.path.getsize(subitem_path)
                                            })
                                    file_locations[f'subdir_{item}'] = subdir_files
                                except Exception as e:
                                    file_locations[f'subdir_{item}_error'] = str(e)
                    except Exception as e:
                        file_locations['folder_read_error'] = str(e)
                
                return file_locations
        
        return {'error': f'장 {chapter_number} 정보를 찾을 수 없음'}
    
    def _create_chapter_markdown_report(self, chapter_data: Dict[str, Any]) -> str:
        """장별 마크다운 리포트 생성"""
        chapter_info = chapter_data.get('chapter_info', {})
        chapter_num = chapter_info.get('number', 0)
        chapter_title = chapter_info.get('title', 'Unknown')
        
        md_content = f"""# 장 {chapter_num} 통합 노드 문서 생성 결과

## 📖 장 정보
- **번호**: {chapter_num}
- **제목**: {chapter_title}

## 🔄 처리 단계별 결과

### 1단계: 노드 정보 문서 생성
```json
{json.dumps(chapter_data.get('processing_stages', {}).get('node_documents', {}), ensure_ascii=False, indent=2)}
```

### 2단계: 콘텐츠 노드 추출
```json
{json.dumps(chapter_data.get('processing_stages', {}).get('content_nodes', {}), ensure_ascii=False, indent=2)}
```

### 3단계: 문서 통합
```json
{json.dumps(chapter_data.get('processing_stages', {}).get('integration', {}), ensure_ascii=False, indent=2)}
```

## 📁 생성된 파일 위치
```json
{json.dumps(chapter_data.get('file_locations', {}), ensure_ascii=False, indent=2)}
```

---
생성 시간: {asyncio.get_event_loop().time()}
"""
        return md_content
    
    @pytest.mark.anyio
    async def test_specific_chapters_integration(self, real_pdf_path: str):
        """
        특정 장들만 선택하여 통합 노드 생성 테스트
        
        Args:
            real_pdf_path: 실제 PDF 파일 경로 (픽스처에서 제공)
        """
        target_chapters = [1, 6, 9]  # 기본 대상 장들
        print(f"\n🚀 특정 장별 통합 노드 생성 테스트 시작")
        print(f"   📖 PDF: {real_pdf_path}")
        print(f"   🎯 대상 장: {target_chapters}")
        
        # 1. 워크스페이스 준비
        print(f"\n1️⃣ 워크스페이스 준비 중...")
        workspace_stage = WorkspacePreparationStage(self.config_manager, self.logger_factory)
        
        workspace_result = await workspace_stage.process({
            'pdf_path': real_pdf_path,
            'output_dir': './test_output'
        })
        
        if not workspace_result.get('success', False):
            raise Exception(f"워크스페이스 준비 실패: {workspace_result.get('error', '')}")
        
        print(f"✅ 워크스페이스 준비 완료!")
        print(f"   📁 생성된 전체 장: {len(workspace_result.get('created_folders', []))}")
        
        # 2. 특정 장들만 필터링
        print(f"\n2️⃣ 특정 장 선택 중...")
        all_folders = workspace_result.get('created_folders', [])
        selected_folders = self.filter_chapters_by_numbers(all_folders, target_chapters)
        
        if not selected_folders:
            raise Exception(f"선택된 장이 없습니다. 대상: {target_chapters}")
        
        print(f"✅ {len(selected_folders)}개 장 선택됨!")
        
        # 3. 선택된 장들로 integration_results 구성
        integration_results = []
        for folder_info in selected_folders:
            integration_results.append({
                'chapter_number': folder_info.get('chapter_number'),
                'chapter_title': folder_info.get('chapter_title', ''),
                'success': True,
                'folder_path': folder_info.get('path', ''),
                'toc_file': folder_info.get('toc_file', '')
            })
        
        # 4. IntegratedNodeGenerationStage 실행
        print(f"\n3️⃣ 통합 노드 생성 단계 실행 중...")
        stage = IntegratedNodeGenerationStage(self.config_manager, self.logger_factory)
        
        input_data = {
            'integration_results': integration_results,
            'book_info': workspace_result.get('book_info', {}),
            'output_dir': workspace_result.get('output_dir', '')
        }
        
        stage_results = await stage.process(input_data)
        
        # 5. 결과 저장
        print(f"\n4️⃣ 결과 저장 중...")
        self.save_integrated_node_documents(stage_results, workspace_result)
        
        # 6. 최종 결과 출력
        print(f"\n🎉 특정 장별 통합 노드 생성 테스트 완료!")
        print(f"   ✅ 성공 여부: {stage_results.get('success', False)}")
        print(f"   📊 처리된 장: {stage_results.get('processed_chapters', 0)}/{len(target_chapters)}")
        print(f"   📈 성공률: {stage_results.get('success_rate', 0):.1f}%")
        
        return stage_results

# 실행 예시
if __name__ == "__main__":
    async def main():
        tester = TestSpecificChapters()
        
        # 실제 PDF 파일 경로 (여기에 실제 경로 입력)
        pdf_path = "/path/to/your/test.pdf"  # 실제 PDF 경로로 수정 필요
        
        # 1, 6, 9장만 테스트
        target_chapters = [1, 6, 9]
        
        try:
            results = await tester.test_specific_chapters_integration(pdf_path, target_chapters)
            print(f"\n최종 결과: {results}")
        except Exception as e:
            print(f"❌ 테스트 실패: {e}")
    
    # 실행
    asyncio.run(main())