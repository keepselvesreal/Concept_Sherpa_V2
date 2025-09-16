# 생성 시간: Fri Sep  5 12:23:19 KST 2025
# 핵심 내용: 메인 파이프라인 오케스트레이터 v2 (최신 AI providers, logger_v2, workspace_preparation_v2 반영)
# 상세 내용:
#   - BookPipelineOrchestrator (라인 20-195): 메인 파이프라인 오케스트레이터 클래스
#   - __init__ (라인 25-65): 설정과 의존성 초기화 (최신 구조 반영)
#   - execute (라인 67-145): 파이프라인 실행 메인 메서드 (v2 stage 사용)
#   - _log_pipeline_start (라인 147-168): 파이프라인 시작 로그
#   - _log_pipeline_completion (라인 170-195): 파이프라인 완료 로그
# 상태: active
# 참조: pipeline_orchestrator.py (최신 구조 및 서비스 반영)

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 최신 컴포넌트 임포트 (절대 경로로 수정)
sys.path.append(str(Path(__file__).parent.parent))
from core.base.pipeline_result import PipelineResult, StageResult
from utils.config_manager import ConfigManager
from utils.logger_v2 import Logger

# 최신 단계별 프로세서 임포트
from stages.workspace_preparation_v3 import WorkspacePreparationStage
from stages.integrated_node_generation_stage_v4 import IntegratedNodeGenerationStage
# TODO: 나머지 단계들도 구현되면 임포트
# from ..stages.content_processing_v2 import ContentProcessingStage
# from ..stages.toc_generation_v2 import TocGenerationStage

class BookPipelineOrchestrator:
    """메인 파이프라인 오케스트레이터 v2 (최신 구조 반영)"""
    
    def __init__(self, config_dir: str = None):
        """
        Args:
            config_dir: 설정 파일 디렉토리 경로
        """
        # 설정 관리자 초기화
        if config_dir is None:
            config_dir = Path(__file__).parent.parent.parent / "config"
        self.config_manager = ConfigManager(config_dir)
        
        # 통합 파이프라인 로거 생성
        self.main_logger = Logger(
            project_name="book_pipeline_v2",
            logs_base_dir="./logs"
        )
        
        # 단계별 프로세서 초기화
        self._initialize_stages()
        
    def _initialize_stages(self):
        """단계별 프로세서 초기화 (통합 로거 사용)"""
        # 1단계: 기본 작업 준비 (워크스페이스 생성)
        self.workspace_preparation_stage = WorkspacePreparationStage(
            self.config_manager,
            logger_factory=None  # 통합 로거 사용 예정
        )
        
        # 2단계: 통합 노드 정보 문서 생성
        self.integrated_node_generation_stage = IntegratedNodeGenerationStage(
            self.config_manager,
            logger_factory=None  # 통합 로거 사용 예정
        )
        
        # TODO: 나머지 단계들 초기화
        # self.content_processing_stage = ContentProcessingStage(self.config_manager, None)  
        # self.toc_generation_stage = TocGenerationStage(self.config_manager, None)
        
    async def execute(self, pdf_path: str) -> PipelineResult:
        """
        파이프라인 실행 메인 메서드
        
        Args:
            pdf_path: 처리할 PDF 파일 경로
            
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
            
            # 1단계: 기본 작업 준비 (워크스페이스 생성) - v2 사용
            try:
                stage1_output = await self.workspace_preparation_stage.process({'data': {'pdf_path': pdf_path}, 'error': None})
            except Exception as e:
                stage1_output = {'data': {}, 'error': str(e)}
            
            if not self._handle_stage_result(stage1_output, "workspace_preparation_stage", 1, result):
                return result
            
            # 2단계: 통합 노드 정보 문서 생성 (v4)
            try:
                stage2_output = await self.integrated_node_generation_stage.process(stage1_output)
            except Exception as e:
                stage2_output = {'data': {}, 'error': str(e)}
            
            if not self._handle_stage_result(stage2_output, "integrated_node_generation_stage", 2, result):
                return result
            
            # 3단계: 가공 작업 (v2)
            # TODO: 구현 예정  
            stage3_result = StageResult("content_processing_stage")
            stage3_result.complete(error=None, data={'status': 'TODO - v2 구현 예정'})
            result.add_stage_result(stage3_result)
            
            # 4단계: 목차 생성 (v2)
            # TODO: 구현 예정
            stage4_result = StageResult("toc_generation_stage")
            stage4_result.complete(error=None, data={'status': 'TODO - v2 구현 예정'})
            result.add_stage_result(stage4_result)
            
            # 성공 완료
            result.set_success(True)
            
            # 완료 로그
            self._log_pipeline_completion(result, stage1_output)
            
            return result
            
        except Exception as e:
            error_msg = f"파이프라인 v2 실행 중 예외 발생: {str(e)}"
            result.set_success(False, error_msg)
            
            if self.main_logger:
                self.main_logger.error(error_msg)
            else:
                print(f"❌ {error_msg}")
                
            return result
    
    def _handle_stage_result(self, stage_output: Dict[str, Any], stage_name: str, 
                           step_number: int, result: PipelineResult) -> bool:
        """
        스테이지 결과 처리 및 StageResult 생성
        
        Args:
            stage_output: 스테이지 실행 결과
            stage_name: 스테이지명
            step_number: 단계 번호
            result: PipelineResult 객체
        
        Returns:
            bool: 성공 여부 (False면 파이프라인 중단해야 함)
        """
        stage_result = StageResult(stage_name)
        
        if stage_output.get('error') is None:
            stage_result.complete(error=None, data=stage_output.get('data', {}))
        else:
            stage_result.complete(error=stage_output.get('error', '알 수 없는 오류'))
        
        result.add_stage_result(stage_result)
        
        if stage_result.error is not None:
            result.set_success(False, f"{step_number}단계 실패: {stage_result.error}")
            return False
        
        return True
            
    def _log_pipeline_start(self, pdf_path: str):
        """파이프라인 시작 로그"""
        print("🚀 리팩터링된 책 파이프라인 v2 실행 시작")
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
                print("🧪🎉 리팩터링된 파이프라인 v2 테스트 모드 완료! 🎉🧪")
                if selected_chapters:
                    print(f"🔬 테스트 대상: {selected_chapters} 장")
                else:
                    print("🔬 테스트 대상: 모든 장")
            else:
                print("🎉🎉🎉 리팩터링된 파이프라인 v2 전체 완료! 🎉🎉🎉")
                
            print(f"📚 책: {workspace_data.get('book_title', '알 수 없음')}")
            print(f"📁 출력: {workspace_data.get('output_directory', '')}")
            print(f"📊 완료 단계: {result.completed_stages}/{result.total_stages}")
            print(f"🕐 진행률: {result.progress_percent}%")
            
            if self.main_logger:
                self.main_logger.info(f"리팩터링된 파이프라인 v2 완료 - {result.completed_stages}/{result.total_stages} 단계")
        else:
            print(f"❌ 파이프라인 v2 실패: {result.error}")
            if self.main_logger:
                self.main_logger.error(f"파이프라인 v2 실패: {result.error}")