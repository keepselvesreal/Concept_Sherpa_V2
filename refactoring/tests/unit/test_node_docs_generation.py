# 생성 시간: Thu Sep  4 18:58:00 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 1단계(노드 정보 문서 생성) 전용 테스트
# 상세 내용:
#   - NodeDocsGenerationTester (라인 25-180): 1단계 전용 테스트 클래스
#   - setup_stage (라인 35-50): Stage 초기화
#   - test_single_chapter (라인 52-120): 단일 장 테스트
#   - test_selected_chapters (라인 122-180): 선택된 장들 테스트
# 상태: active

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# 프로젝트 경로 추가
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

# 직접 경로에서 모듈들 임포트
sys.path.append(str(src_path / "stages"))
sys.path.append(str(src_path / "config"))
sys.path.append(str(src_path / "utils"))
sys.path.append(str(src_path / "services"))

# 필요한 모듈들 임포트
from integrated_node_generation_stage_v2 import IntegratedNodeGenerationStage

# Mock ConfigManager 클래스
class MockConfigManager:
    def __init__(self):
        self.config = {}

class NodeDocsGenerationTester:
    """1단계 노드 정보 문서 생성 전용 테스트"""
    
    def __init__(self):
        self.output_base_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output/Data_Oriented_Programming")
        self.stage = None
        
        # 테스트 대상 장 목록 (장번호, 폴더명, 제목)
        self.target_chapters = [
            (1, '1_Complexity_of_object_oriented_programming', 'Complexity of object oriented programming'),
            (6, '6_Unit_tests', 'Unit tests'),
            (9, '9_Persistent_data_structures', 'Persistent data structures')
        ]
    
    def setup_stage(self):
        """Stage 초기화"""
        try:
            config_manager = MockConfigManager()
            self.stage = IntegratedNodeGenerationStage(config_manager)
            print("✅ IntegratedNodeGenerationStage 초기화 성공")
            return True
        except Exception as e:
            print(f"❌ Stage 초기화 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_single_chapter(self, chapter_number, folder_name, title):
        """단일 장 1단계 테스트"""
        print(f"\n📊 장 {chapter_number} 처리 시작: {title}")
        
        # 파일 경로 구성
        chapter_path = self.output_base_path / folder_name
        toc_file = chapter_path / f"{folder_name}_toc.json"
        
        print(f"- 폴더: {chapter_path}")
        print(f"- TOC 파일: {toc_file}")
        
        # 파일 존재 확인
        if not chapter_path.exists():
            print(f"❌ 장 폴더가 존재하지 않음: {chapter_path}")
            return False
        
        if not toc_file.exists():
            print(f"❌ TOC 파일이 존재하지 않음: {toc_file}")
            return False
        
        # chapter_result 구성
        chapter_result = {
            'chapter_number': chapter_number,
            'chapter_title': folder_name,
            'folder_path': str(chapter_path),
            'toc_file': str(toc_file)
        }
        
        try:
            # 1단계 실행: 노드 정보 문서 생성
            print(f"🔧 노드 정보 문서 생성 시작...")
            node_docs_result = await self.stage.generate_node_documents(
                chapter_result, 
                {'title': 'Data-Oriented Programming'}, 
                str(self.output_base_path)
            )
            
            if node_docs_result.get('success', False):
                created_count = node_docs_result.get('created_count', 0)
                print(f"✅ 장 {chapter_number} 노드 정보 문서 생성 완료: {created_count}개 파일")
                
                # 생성된 파일들 확인
                node_docs_dir = chapter_path / "node_info_docs"
                if node_docs_dir.exists():
                    print(f"📁 생성된 파일 목록:")
                    doc_files = sorted(node_docs_dir.glob("*.md"))
                    for i, doc_file in enumerate(doc_files[:5], 1):  # 처음 5개만 표시
                        print(f"   {i}. {doc_file.name}")
                    if len(doc_files) > 5:
                        print(f"   ... 총 {len(doc_files)}개 파일")
                else:
                    print(f"⚠️ node_info_docs 폴더가 생성되지 않음")
                
                return True
            else:
                error_msg = node_docs_result.get('error', '알 수 없는 오류')
                print(f"❌ 장 {chapter_number} 노드 정보 문서 생성 실패: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ 장 {chapter_number} 처리 중 예외: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_selected_chapters(self):
        """선택된 장들 1단계 테스트"""
        print("=== 1단계 노드 정보 문서 생성 테스트 ===")
        print(f"대상 장: {[ch[0] for ch in self.target_chapters]}")
        print(f"출력 경로: {self.output_base_path}")
        
        success_count = 0
        total_count = len(self.target_chapters)
        
        for chapter_number, folder_name, title in self.target_chapters:
            success = await self.test_single_chapter(chapter_number, folder_name, title)
            if success:
                success_count += 1
        
        # 결과 요약
        print(f"\n--- 1단계 테스트 결과 요약 ---")
        print(f"총 {success_count}/{total_count}개 장 처리 성공")
        print(f"성공률: {(success_count/total_count*100):.1f}%")
        
        if success_count == total_count:
            print("🎉 모든 장 노드 정보 문서 생성 성공!")
            return True
        else:
            print("⚠️ 일부 장에서 실패 발생")
            return False

def main():
    """메인 실행"""
    print("IntegratedNodeGenerationStage 1단계(노드 정보 문서 생성) 테스트")
    print("=" * 70)
    
    tester = NodeDocsGenerationTester()
    
    # Stage 초기화
    if not tester.setup_stage():
        print("💥 Stage 초기화 실패로 테스트 중단")
        return False
    
    # 비동기 테스트 실행
    try:
        success = asyncio.run(tester.test_selected_chapters())
        
        if success:
            print("\n🎉 전체 테스트 성공!")
        else:
            print("\n💥 테스트 일부 실패!")
        
        return success
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 예외: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)