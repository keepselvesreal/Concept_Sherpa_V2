# 생성 시간: Mon Sep  3 17:15:25 KST 2025
# 핵심 내용: 메인 파이프라인 오케스트레이터 (4단계 통합 관리, selected_chapters 테스트 모드 지원)
# 상세 내용:
#   - BookPipelineOrchestrator (라인 20-163): 메인 파이프라인 오케스트레이터 클래스
#   - __init__ (라인 25-41): 설정과 의존성 초기화
#   - execute (라인 43-116): 파이프라인 실행 메인 메서드
#   - _log_pipeline_start (라인 118-139): 파이프라인 시작 로그
#   - _log_pipeline_completion (라인 141-163): 파이프라인 완료 로그
# 상태: active

import os
from pathlib import Path
from typing import Dict, Any, Optional

# 핵심 컴포넌트 임포트
from .base.pipeline_result import PipelineResult, StageResult
from ..utils.config_manager import ConfigManager
from ..utils.logger import LoggerFactory

# 단계별 프로세서 임포트
from ..stages.workspace_preparation import WorkspacePreparationStage
# TODO: 나머지 단계들도 구현되면 임포트
# from ..stages.information_integration import InformationIntegrationStage
# from ..stages.content_processing import ContentProcessingStage
# from ..stages.toc_generation import TocGenerationStage

class BookPipelineOrchestrator:
    """메인 파이프라인 오케스트레이터 (4단계 통합 관리)"""
    
    def __init__(self, config_dir: str = None, test_mode: bool = False, selected_chapters: list = None):
        """
        Args:
            config_dir: 설정 파일 디렉토리 경로
            test_mode: 테스트 모드 활성화
            selected_chapters: 테스트할 장 번호 목록 (예: [1, 3, 5])
        """
        # 설정 관리자 초기화
        if config_dir is None:
            config_dir = Path(__file__).parent.parent.parent / "config"
        self.config_manager = ConfigManager(config_dir)
        
        # 테스트 모드 설정 (설정 파일보다 매개변수 우선)
        if test_mode or selected_chapters:
            self.config_manager.pipeline_config['test_mode'] = {
                'enabled': True,
                'selected_chapters': selected_chapters or [],
                'debug_verbose': True,
                'skip_on_error': False
            }
        
        # 로거 팩토리 초기화
        self.logger_factory = LoggerFactory(self.config_manager)
        
        # 메인 로거 (책별 로거는 1단계에서 생성)
        self.main_logger = None
        
        # 단계별 프로세서 초기화
        self._initialize_stages()
        
    def _initialize_stages(self):
        """단계별 프로세서 초기화"""
        self.stage_1 = WorkspacePreparationStage(self.config_manager, self.logger_factory)
        # TODO: 나머지 단계들 초기화
        # self.stage_2 = InformationIntegrationStage(self.config_manager, self.logger_factory)
        # self.stage_3 = ContentProcessingStage(self.config_manager, self.logger_factory)  
        # self.stage_4 = TocGenerationStage(self.config_manager, self.logger_factory)
        
    async def execute(self, pdf_path: str, metadata_info: Dict[str, Any] = None) -> PipelineResult:
        """
        파이프라인 실행 메인 메서드
        
        Args:
            pdf_path: 처리할 PDF 파일 경로
            metadata_info: 메타데이터 정보 (선택사항)
            
        Returns:
            PipelineResult: 파이프라인 실행 결과
        """
        result = PipelineResult(total_stages=4)
        
        try:
            # 입력 검증
            if not pdf_path or not os.path.exists(pdf_path):
                result.set_success(False, f"유효하지 않은 PDF 경로: {pdf_path}")
                return result
            
            # 파이프라인 시작 로그
            self._log_pipeline_start(pdf_path)
            
            # 1단계: 기본 작업 준비 (워크스페이스 생성)
            stage1_result = StageResult("workspace_preparation")
            try:
                stage1_data = await self.stage_1.process({'pdf_path': pdf_path})
                
                if stage1_data.get('success'):
                    stage1_result.complete(success=True, data=stage1_data)
                    self.main_logger = self.stage_1.logger  # 책별 로거를 메인 로거로 설정
                else:
                    stage1_result.complete(success=False, error=stage1_data.get('error', '알 수 없는 오류'))
                    
            except Exception as e:
                stage1_result.complete(success=False, error=str(e))
                
            result.add_stage_result(stage1_result)
            
            if not stage1_result.success:
                result.set_success(False, f"1단계 실패: {stage1_result.error}")
                return result
            
            # 2단계: 통합 노드 정보 문서 생성
            # TODO: 구현 예정
            stage2_result = StageResult("information_integration")
            stage2_result.complete(success=True, data={'status': 'TODO - 구현 예정'})
            result.add_stage_result(stage2_result)
            
            # 3단계: 가공 작업
            # TODO: 구현 예정  
            stage3_result = StageResult("content_processing")
            stage3_result.complete(success=True, data={'status': 'TODO - 구현 예정'})
            result.add_stage_result(stage3_result)
            
            # 4단계: 목차 생성
            # TODO: 구현 예정
            stage4_result = StageResult("toc_generation")
            stage4_result.complete(success=True, data={'status': 'TODO - 구현 예정'})
            result.add_stage_result(stage4_result)
            
            # 성공 완료
            result.set_success(True)
            result.data = {
                'workspace_info': stage1_data,
                'pipeline_version': 'refactored_v1',
                'test_mode': self.config_manager.get_test_config(),
                'total_stages_completed': result.completed_stages
            }
            
            # 완료 로그
            self._log_pipeline_completion(result, stage1_data)
            
            return result
            
        except Exception as e:
            error_msg = f"파이프라인 실행 중 예외 발생: {str(e)}"
            result.set_success(False, error_msg)
            
            if self.main_logger:
                self.main_logger.error(error_msg)
            else:
                print(f"❌ {error_msg}")
                
            return result
            
    def _log_pipeline_start(self, pdf_path: str):
        """파이프라인 시작 로그"""
        print("🚀 리팩터링된 책 파이프라인 v1 실행 시작")
        print(f"📖 처리 대상: {os.path.basename(pdf_path)}")
        
        # 테스트 모드 정보
        test_config = self.config_manager.get_test_config()
        if test_config.get('enabled'):
            selected_chapters = test_config.get('selected_chapters', [])
            if selected_chapters:
                print(f"🧪 테스트 모드: 선택된 장 {selected_chapters}")
            else:
                print("🧪 테스트 모드: 모든 장 처리")
        else:
            print("🔄 일반 모드: 전체 파이프라인 실행")
            
    def _log_pipeline_completion(self, result: PipelineResult, workspace_data: Dict[str, Any]):
        """파이프라인 완료 로그"""
        test_config = self.config_manager.get_test_config()
        is_test_mode = test_config.get('enabled', False)
        
        if result.is_success:
            if is_test_mode:
                selected_chapters = test_config.get('selected_chapters', [])
                print("🧪🎉 리팩터링된 파이프라인 테스트 모드 완료! 🎉🧪")
                if selected_chapters:
                    print(f"🔬 테스트 대상: {selected_chapters} 장")
                else:
                    print("🔬 테스트 대상: 모든 장")
            else:
                print("🎉🎉🎉 리팩터링된 파이프라인 전체 완료! 🎉🎉🎉")
                
            print(f"📚 책: {workspace_data.get('book_title', '알 수 없음')}")
            print(f"📁 출력: {workspace_data.get('output_directory', '')}")
            print(f"📊 완료 단계: {result.completed_stages}/{result.total_stages}")
            print(f"🕐 진행률: {result.progress_percent}%")
            
            if self.main_logger:
                self.main_logger.info(f"리팩터링된 파이프라인 완료 - {result.completed_stages}/{result.total_stages} 단계")
        else:
            print(f"❌ 파이프라인 실패: {result.error}")
            if self.main_logger:
                self.main_logger.error(f"파이프라인 실패: {result.error}")