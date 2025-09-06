# 구현 파일명: pipeline_orchestrator_v2.py, 테스트 유형: integration
# 생성 시간: Fri Sep  5 12:23:19 KST 2025
# 핵심 내용: BookPipelineOrchestrator v2 통합 테스트 (실제 PDF 데이터 사용)
# 상세 내용:
#   - PipelineOrchestratorV2Tester (라인 20-250): v2 오케스트레이터 테스트 클래스
#   - setup_environment (라인 30-60): 테스트 환경 설정 (실제 PDF 파일 확인)
#   - test_full_pipeline_single_chapter (라인 62-140): 단일 장 전체 파이프라인 테스트
#   - test_selected_chapters_mode (라인 142-200): 선택된 장 모드 테스트
#   - test_error_scenarios (라인 202-250): 오류 시나리오 테스트
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

# 필요한 모듈들 직접 임포트
sys.path.append(str(src_path / "core"))
sys.path.append(str(src_path / "utils"))
sys.path.append(str(src_path / "stages"))

from core.pipeline_orchestrator_v2 import BookPipelineOrchestrator
from utils.config_manager import ConfigManager

class PipelineOrchestratorV2Tester:
    """
    BookPipelineOrchestrator v2 통합 테스트 클래스
    실제 PDF 파일을 사용하여 전체 파이프라인의 동작을 검증한다.
    """
    
    def __init__(self):
        self.test_pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/books/Data-Oriented_Programming.pdf"
        self.output_base_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output")
        self.config_dir = project_root / "config"
        self.orchestrator = None
        
        # 테스트 시나리오별 설정
        self.test_scenarios = {
            'single_chapter': {'chapters': [1], 'name': '단일 장 테스트'},
            'multiple_chapters': {'chapters': [1, 2], 'name': '다중 장 테스트'},
            'full_mode': {'chapters': None, 'name': '전체 모드 테스트'}
        }
    
    def setup_environment(self) -> bool:
        """
        테스트 환경 설정 및 검증
        실제 PDF 파일과 설정 디렉토리 존재 여부를 확인한다.
        """
        print("🔧 테스트 환경 설정 중...")
        
        # PDF 파일 존재 확인
        if not Path(self.test_pdf_path).exists():
            print(f"❌ 테스트 PDF 파일을 찾을 수 없음: {self.test_pdf_path}")
            return False
        print(f"✅ 테스트 PDF 파일 확인: {Path(self.test_pdf_path).name}")
        
        # 설정 디렉토리 확인
        if not self.config_dir.exists():
            print(f"❌ 설정 디렉토리를 찾을 수 없음: {self.config_dir}")
            return False
        print(f"✅ 설정 디렉토리 확인: {self.config_dir}")
        
        # 출력 디렉토리 준비
        self.output_base_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ 출력 디렉토리 준비: {self.output_base_path}")
        
        return True
    
    async def test_full_pipeline_single_chapter(self) -> bool:
        """
        단일 장 전체 파이프라인 테스트
        장 1만 선택하여 전체 파이프라인의 동작을 검증한다.
        """
        print(f"\n📊 === 단일 장 전체 파이프라인 테스트 ===")
        
        try:
            # 테스트 모드로 오케스트레이터 생성
            self.orchestrator = BookPipelineOrchestrator(
                config_dir=str(self.config_dir),
                test_mode=True,
                selected_chapters=[1]  # 장 1만 테스트
            )
            print(f"✅ 오케스트레이터 v2 초기화 성공 (테스트 모드: 장 1)")
            
            # 파이프라인 실행
            print(f"🚀 파이프라인 실행 시작...")
            start_time = datetime.now()
            
            result = await self.orchestrator.execute(self.test_pdf_path)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # 결과 검증
            if not result.is_success:
                print(f"❌ 파이프라인 실행 실패: {result.error}")
                return False
            
            print(f"✅ 파이프라인 실행 성공!")
            print(f"   - 실행 시간: {execution_time:.2f}초")
            print(f"   - 완료 단계: {result.completed_stages}/{result.total_stages}")
            print(f"   - 진행률: {result.progress_percent}%")
            print(f"   - 파이프라인 버전: {result.data.get('pipeline_version', 'unknown')}")
            
            # 결과 데이터 검증
            workspace_info = result.data.get('workspace_info', {})
            if workspace_info:
                print(f"📚 처리된 책: {workspace_info.get('book_title', 'unknown')}")
                print(f"📁 출력 경로: {workspace_info.get('output_directory', 'unknown')}")
                
                # 실제로 생성된 파일들 확인
                output_dir = Path(workspace_info.get('output_directory', ''))
                if output_dir.exists():
                    created_files = list(output_dir.rglob("*"))
                    folders = [f for f in created_files if f.is_dir()]
                    files = [f for f in created_files if f.is_file()]
                    print(f"📂 생성된 폴더: {len(folders)}개")
                    print(f"📄 생성된 파일: {len(files)}개")
                    
                    # 주요 파일 확인
                    key_files = ['toc.json']
                    for key_file in key_files:
                        key_file_path = output_dir / key_file
                        status = "✅" if key_file_path.exists() else "❌"
                        print(f"   {status} {key_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 단일 장 테스트 실행 중 예외: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_selected_chapters_mode(self) -> bool:
        """
        선택된 장 모드 테스트
        여러 장을 선택하여 테스트 모드의 동작을 검증한다.
        """
        print(f"\n📊 === 선택된 장 모드 테스트 ===")
        
        selected_chapters = [1, 2]  # 장 1, 2 선택
        
        try:
            # 다중 장 선택 모드로 오케스트레이터 생성
            self.orchestrator = BookPipelineOrchestrator(
                config_dir=str(self.config_dir),
                test_mode=True,
                selected_chapters=selected_chapters
            )
            print(f"✅ 오케스트레이터 v2 초기화 성공 (테스트 모드: 장 {selected_chapters})")
            
            # 파이프라인 실행
            print(f"🚀 다중 장 파이프라인 실행 시작...")
            start_time = datetime.now()
            
            result = await self.orchestrator.execute(self.test_pdf_path)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # 결과 검증
            if not result.is_success:
                print(f"❌ 다중 장 파이프라인 실행 실패: {result.error}")
                return False
            
            print(f"✅ 다중 장 파이프라인 실행 성공!")
            print(f"   - 실행 시간: {execution_time:.2f}초")
            print(f"   - 대상 장: {selected_chapters}")
            print(f"   - 완료 단계: {result.completed_stages}/{result.total_stages}")
            
            # 테스트 모드 설정 확인
            test_config = result.data.get('test_mode', {})
            if test_config.get('enabled'):
                actual_selected = test_config.get('selected_chapters', [])
                if actual_selected == selected_chapters:
                    print(f"✅ 테스트 모드 설정 검증 성공: {actual_selected}")
                else:
                    print(f"❌ 테스트 모드 설정 불일치: 예상 {selected_chapters}, 실제 {actual_selected}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ 선택된 장 모드 테스트 실행 중 예외: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_error_scenarios(self) -> bool:
        """
        오류 시나리오 테스트
        잘못된 입력이나 파일 부재 시의 오류 처리를 검증한다.
        """
        print(f"\n📊 === 오류 시나리오 테스트 ===")
        
        test_cases = [
            {
                'name': '존재하지 않는 PDF 파일',
                'pdf_path': '/nonexistent/file.pdf',
                'expect_error': True
            },
            {
                'name': '빈 PDF 경로',
                'pdf_path': '',
                'expect_error': True
            },
            {
                'name': 'None PDF 경로',
                'pdf_path': None,
                'expect_error': True
            }
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']} 테스트")
            
            try:
                # 일반 모드로 오케스트레이터 생성
                orchestrator = BookPipelineOrchestrator(config_dir=str(self.config_dir))
                
                # 파이프라인 실행
                result = await orchestrator.execute(test_case['pdf_path'])
                
                # 결과 검증
                if test_case['expect_error']:
                    if not result.is_success:
                        print(f"✅ 예상된 오류 발생: {result.error}")
                        success_count += 1
                    else:
                        print(f"❌ 오류가 발생해야 하는데 성공함")
                else:
                    if result.is_success:
                        print(f"✅ 성공")
                        success_count += 1
                    else:
                        print(f"❌ 실패: {result.error}")
                
            except Exception as e:
                if test_case['expect_error']:
                    print(f"✅ 예상된 예외 발생: {str(e)}")
                    success_count += 1
                else:
                    print(f"❌ 예상치 못한 예외: {str(e)}")
        
        total_tests = len(test_cases)
        success_rate = (success_count / total_tests) * 100
        
        print(f"\n--- 오류 시나리오 테스트 결과 ---")
        print(f"총 {success_count}/{total_tests}개 테스트 통과")
        print(f"통과율: {success_rate:.1f}%")
        
        return success_count == total_tests

async def run_all_tests():
    """전체 테스트 실행"""
    print("BookPipelineOrchestrator v2 통합 테스트")
    print("=" * 70)
    print(f"테스트 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = PipelineOrchestratorV2Tester()
    
    # 환경 설정
    if not tester.setup_environment():
        print("💥 환경 설정 실패로 테스트 중단")
        return False
    
    # 테스트 실행
    test_results = []
    
    # 1. 단일 장 전체 파이프라인 테스트
    print(f"\n{'='*50}")
    result1 = await tester.test_full_pipeline_single_chapter()
    test_results.append(('단일 장 파이프라인', result1))
    
    # 2. 선택된 장 모드 테스트
    print(f"\n{'='*50}")
    result2 = await tester.test_selected_chapters_mode()
    test_results.append(('선택된 장 모드', result2))
    
    # 3. 오류 시나리오 테스트
    print(f"\n{'='*50}")
    result3 = await tester.test_error_scenarios()
    test_results.append(('오류 시나리오', result3))
    
    # 전체 결과 요약
    print(f"\n{'='*70}")
    print("📊 전체 테스트 결과 요약")
    print(f"{'='*70}")
    
    success_count = 0
    total_count = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ 통과" if success else "❌ 실패"
        print(f"{test_name:20} : {status}")
        if success:
            success_count += 1
    
    success_rate = (success_count / total_count) * 100
    print(f"\n총 통과: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_count == total_count:
        print("🎉 모든 테스트 통과!")
        return True
    else:
        print("⚠️ 일부 테스트 실패")
        return False

def main():
    """메인 실행 함수"""
    try:
        success = asyncio.run(run_all_tests())
        
        if success:
            print("\n🎉 전체 테스트 성공!")
        else:
            print("\n💥 일부 테스트 실패!")
        
        return success
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 예외: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)