# 생성 시간: Thu Sep  4 23:02:00 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 2단계(콘텐츠 노드 추출) 전용 테스트
# 상세 내용:
#   - ContentExtractionTester (라인 25-200): 2단계 전용 테스트 클래스
#   - setup_stage (라인 35-50): Stage 초기화
#   - test_single_chapter_stage2 (라인 52-140): 단일 장 2단계 테스트
#   - test_selected_chapters_stage2 (라인 142-200): 선택된 장들 2단계 테스트
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
from config_manager import ConfigManager

class ContentExtractionTester:
    """2단계 콘텐츠 노드 추출 전용 테스트"""
    
    def __init__(self):
        self.output_base_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output/Data_Oriented_Programming")
        self.stage = None
        
        # 테스트 대상 장 목록 (1장만)
        self.target_chapters = [
            (1, '1_Complexity_of_object_oriented_programming', 'Complexity of object oriented programming')
        ]
    
    def setup_stage(self):
        """Stage 초기화"""
        try:
            # 실제 ConfigManager 사용
            config_manager = ConfigManager()
            self.stage = IntegratedNodeGenerationStage(config_manager)
            print("✅ IntegratedNodeGenerationStage 초기화 성공")
            return True
        except Exception as e:
            print(f"❌ Stage 초기화 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_single_chapter_stage2(self, chapter_number, folder_name, title):
        """단일 장 2단계(콘텐츠 노드 추출) 테스트"""
        print(f"\n📊 장 {chapter_number} 2단계 처리 시작: {title}")
        
        # 파일 경로 구성
        chapter_path = self.output_base_path / folder_name
        toc_file = chapter_path / f"{folder_name}_toc.json"
        content_file = chapter_path / f"{folder_name}_content.md"
        node_docs_dir = chapter_path / "node_info_docs"
        
        print(f"- 폴더: {chapter_path}")
        print(f"- TOC 파일: {toc_file}")
        print(f"- 콘텐츠 파일: {content_file}")
        print(f"- 노드 문서 폴더: {node_docs_dir}")
        
        # 파일 존재 확인
        if not chapter_path.exists():
            print(f"❌ 장 폴더가 존재하지 않음: {chapter_path}")
            return False
        
        if not toc_file.exists():
            print(f"❌ TOC 파일이 존재하지 않음: {toc_file}")
            return False
            
        if not content_file.exists():
            print(f"❌ 콘텐츠 파일이 존재하지 않음: {content_file}")
            return False
            
        if not node_docs_dir.exists():
            print(f"❌ 1단계 노드 문서 폴더가 존재하지 않음: {node_docs_dir}")
            return False
        
        # 1단계 결과 구성 (가상의 성공 결과)
        node_docs_result = {
            'success': True,
            'created_count': len(list(node_docs_dir.glob("*.md"))),
            'node_docs_dir': str(node_docs_dir)
        }
        
        # chapter_result 구성
        chapter_result = {
            'chapter_number': chapter_number,
            'chapter_title': folder_name,
            'folder_path': str(chapter_path),
            'toc_file': str(toc_file),
            'content_file': str(content_file)
        }
        
        try:
            # 2단계 실행: 콘텐츠 노드 추출
            print(f"🔧 콘텐츠 노드 추출 시작...")
            content_nodes_result = await self.stage.extract_content_nodes(
                chapter_result, 
                node_docs_result,
                str(self.output_base_path)
            )
            
            if content_nodes_result.get('success', False):
                processed_sections = content_nodes_result.get('processed_sections', 0)
                content_sections = content_nodes_result.get('content_sections', 0)
                empty_sections = processed_sections - content_sections
                
                print(f"✅ 장 {chapter_number} 콘텐츠 노드 추출 완료")
                print(f"   - 처리된 섹션: {processed_sections}개")
                print(f"   - 콘텐츠 있는 섹션: {content_sections}개") 
                print(f"   - 빈 섹션: {empty_sections}개")
                
                # 추출된 문서들 확인
                extracted_documents = content_nodes_result.get('extracted_documents', [])
                if extracted_documents:
                    print(f"📄 추출된 문서 예시:")
                    for i, doc in enumerate(extracted_documents[:3], 1):  # 처음 3개만 표시
                        doc_title = doc.get('title', 'Unknown')[:50]
                        has_content = doc.get('has_content', False)
                        status = "✓" if has_content else "○"
                        print(f"   {i}. {status} {doc_title}")
                    if len(extracted_documents) > 3:
                        print(f"   ... 총 {len(extracted_documents)}개 문서")
                
                return True
            else:
                error_msg = content_nodes_result.get('error', '알 수 없는 오류')
                print(f"❌ 장 {chapter_number} 콘텐츠 노드 추출 실패: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ 장 {chapter_number} 2단계 처리 중 예외: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_selected_chapters_stage2(self):
        """선택된 장들 2단계 테스트"""
        print("=== 2단계 콘텐츠 노드 추출 테스트 ===")
        print(f"대상 장: {[ch[0] for ch in self.target_chapters]}")
        print(f"출력 경로: {self.output_base_path}")
        print("※ 1단계에서 생성된 노드 정보 문서 활용")
        
        success_count = 0
        total_count = len(self.target_chapters)
        results = []
        
        for chapter_number, folder_name, title in self.target_chapters:
            success = await self.test_single_chapter_stage2(chapter_number, folder_name, title)
            results.append({
                'chapter_number': chapter_number,
                'title': title,
                'success': success
            })
            if success:
                success_count += 1
        
        # 결과 요약
        print(f"\n--- 2단계 테스트 결과 요약 ---")
        print(f"총 {success_count}/{total_count}개 장 처리 성공")
        print(f"성공률: {(success_count/total_count*100):.1f}%")
        
        # 장별 상세 결과
        print(f"\n📋 장별 결과:")
        for result in results:
            status = "✅ 성공" if result['success'] else "❌ 실패"
            print(f"  장 {result['chapter_number']}: {status}")
        
        if success_count == total_count:
            print("🎉 모든 장 콘텐츠 노드 추출 성공!")
            return True
        else:
            print("⚠️ 일부 장에서 실패 발생")
            return False

def main():
    """메인 실행"""
    print("IntegratedNodeGenerationStage 2단계(콘텐츠 노드 추출) 테스트")
    print("=" * 70)
    
    tester = ContentExtractionTester()
    
    # Stage 초기화
    if not tester.setup_stage():
        print("💥 Stage 초기화 실패로 테스트 중단")
        return False
    
    # 비동기 테스트 실행
    try:
        success = asyncio.run(tester.test_selected_chapters_stage2())
        
        if success:
            print("\n🎉 전체 2단계 테스트 성공!")
        else:
            print("\n💥 2단계 테스트 일부 실패!")
        
        return success
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 예외: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)