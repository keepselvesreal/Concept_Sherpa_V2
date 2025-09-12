# 구현 파일명: pipeline_orchestrator_v2.py, 테스트 유형: integration
# 생성 시간: Fri Sep  5 12:23:19 KST 2025
# 핵심 내용: BookPipelineOrchestrator v2 1단계 단순 테스트 (워크스페이스 준비만 검증)
# 상세 내용:
#   - SimplePipelineV2Tester (라인 20-120): 1단계 전용 단순 테스트 클래스
#   - test_stage1_workspace_preparation (라인 40-80): 워크스페이스 준비 단계만 테스트
#   - verify_stage1_results (라인 82-120): 1단계 결과 검증
# 상태: active

import sys
import asyncio
from pathlib import Path

# 프로젝트 경로를 직접 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# 직접 경로 추가로 import
sys.path.append(str(project_root / "src" / "core"))
sys.path.append(str(project_root / "src" / "utils"))

# 모듈 import
from pipeline_orchestrator_v2 import BookPipelineOrchestrator

class SimplePipelineV2Tester:
    """
    1단계 워크스페이스 준비만 검증하는 단순 테스트
    """
    
    def __init__(self):
        # 실제 테스트용 PDF 파일 경로
        self.test_pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
        self.config_dir = project_root / "config"
        
    def check_test_environment(self) -> bool:
        """테스트 환경 확인"""
        print("🔧 테스트 환경 확인 중...")
        
        # PDF 파일 확인
        if not Path(self.test_pdf_path).exists():
            print(f"❌ 테스트 PDF 파일 없음: {self.test_pdf_path}")
            print("ℹ️ 테스트용 PDF 파일을 확인해주세요.")
            return False
        
        print(f"✅ 테스트 PDF: {Path(self.test_pdf_path).name}")
        return True
        
    async def test_stage1_workspace_preparation(self) -> bool:
        """1단계 워크스페이스 준비 테스트"""
        print(f"\n📊 === 1단계 워크스페이스 준비 테스트 ===")
        
        try:
            # 테스트 모드로 오케스트레이터 생성 (1장만)
            print("🔧 오케스트레이터 v2 초기화...")
            orchestrator = BookPipelineOrchestrator(
                config_dir=str(self.config_dir),
                test_mode=True,
                selected_chapters=[1]  # 1장만 테스트
            )
            print("✅ 오케스트레이터 초기화 완료")
            
            # 파이프라인 실행
            print("🚀 1단계 파이프라인 실행 시작...")
            result = await orchestrator.execute(self.test_pdf_path)
            
            # 기본 결과 확인
            if not result:
                print("❌ 결과 객체가 None")
                return False
                
            print(f"📊 파이프라인 실행 완료")
            print(f"   - 성공 여부: {result.is_success}")
            print(f"   - 완료 단계: {result.completed_stages}")
            print(f"   - 전체 단계: {result.total_stages}")
            
            if not result.is_success:
                print(f"❌ 파이프라인 실행 실패: {result.error}")
                return False
                
            # 1단계 결과 검증
            return self.verify_stage1_results(result)
            
        except Exception as e:
            print(f"❌ 테스트 실행 중 예외: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_stage1_results(self, result) -> bool:
        """1단계 결과 검증"""
        print(f"\n🔍 1단계 결과 검증 중...")
        
        try:
            # 기본 정보 확인
            if result.completed_stages < 1:
                print("❌ 1단계가 완료되지 않음")
                return False
                
            # 결과 데이터 확인
            result_data = result.data
            if not result_data:
                print("❌ 결과 데이터가 없음")
                return False
                
            workspace_info = result_data.get('workspace_info', {})
            if not workspace_info:
                print("❌ 워크스페이스 정보가 없음")
                return False
                
            print("✅ 기본 결과 구조 검증 완료")
            
            # 워크스페이스 정보 출력
            book_title = workspace_info.get('book_title', 'Unknown')
            output_dir = workspace_info.get('output_directory', 'Unknown')
            total_chapters = workspace_info.get('total_chapters', 0)
            
            print(f"📚 책 제목: {book_title}")
            print(f"📁 출력 디렉토리: {output_dir}")
            print(f"📖 총 장 수: {total_chapters}")
            
            # 출력 디렉토리 실제 존재 확인
            if output_dir and output_dir != 'Unknown':
                output_path = Path(output_dir)
                if output_path.exists():
                    print(f"✅ 출력 디렉토리 생성됨: {output_path}")
                    
                    # toc.json 파일 확인
                    toc_file = output_path / "toc.json"
                    if toc_file.exists():
                        print(f"✅ TOC 파일 생성됨: {toc_file}")
                    else:
                        print(f"⚠️ TOC 파일 미생성: {toc_file}")
                else:
                    print(f"⚠️ 출력 디렉토리가 실제로 존재하지 않음: {output_path}")
            
            print("✅ 1단계 워크스페이스 준비 검증 완료")
            return True
            
        except Exception as e:
            print(f"❌ 결과 검증 중 오류: {str(e)}")
            return False

async def run_simple_test():
    """단순 테스트 실행"""
    print("BookPipelineOrchestrator v2 - 1단계 단순 테스트")
    print("=" * 60)
    
    tester = SimplePipelineV2Tester()
    
    # 환경 확인
    if not tester.check_test_environment():
        print("💥 테스트 환경 확인 실패")
        return False
    
    # 1단계 테스트 실행
    success = await tester.test_stage1_workspace_preparation()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 1단계 워크스페이스 준비 테스트 성공!")
    else:
        print("💥 1단계 테스트 실패!")
    
    return success

def main():
    """메인 실행"""
    try:
        success = asyncio.run(run_simple_test())
        return success
    except Exception as e:
        print(f"❌ 메인 실행 중 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n테스트 결과: {'성공' if success else '실패'}")
    exit(0 if success else 1)