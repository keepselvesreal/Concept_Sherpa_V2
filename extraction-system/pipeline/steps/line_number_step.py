# 생성 시간: 2025-08-28 10:50 KST
# 핵심 내용: MD 파일에 라인 번호를 추가하는 파이프라인 스텝
# 상세 내용:
#   - LineNumberStep 클래스 (22-95): 메인 라인 번호 추가 처리
#   - execute() 메서드 (24-56): 파이프라인 실행 로직
#   - _add_line_numbers() 메서드 (58-95): 실제 라인 번호 추가 로직
# 상태: active
# 주소: pipeline/steps/line_number_step
# 참조: add_line_numbers.py 로직을 파이프라인 스텝으로 통합

import asyncio
from pathlib import Path
from typing import Dict, Any

from .base import PipelineStep
from ..models import StepResult


class LineNumberStep(PipelineStep):
    """MD 파일에 라인 번호를 추가하는 파이프라인 스텝"""
    
    def __init__(self):
        super().__init__("라인 번호 추가")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """라인 번호 추가 실행"""
        self._log_step_start()
        
        try:
            # 컨텍스트에서 필요한 정보 추출 (6단계에서 integration_updated_file로 저장되고 7단계에서 보존된 최종 *_info.md 파일)
            info_md_path = context.get("integration_updated_file")
            if not info_md_path:
                error_msg = "integration_updated_file이 컨텍스트에 없습니다 (6단계 NodeDocsIntegrationStep에서 생성되고 7단계에서 보존된 최종 *_info.md 파일)"
                self._log_step_error(error_msg)
                return StepResult(success=False, error=error_msg)
            
            info_md_file = Path(info_md_path)
            if not info_md_file.exists():
                error_msg = f"최종 정보 파일이 존재하지 않습니다: {info_md_path}"
                self._log_step_error(error_msg)
                return StepResult(success=False, error=error_msg)
            
            # 라인 번호가 추가된 파일 경로 생성
            output_file_path = info_md_file.parent / f"{info_md_file.stem}_with_lines.md"
            
            print(f"📁 입력 파일: {info_md_file}")
            print(f"📁 출력 파일: {output_file_path}")
            
            # 라인 번호 추가 (비동기로 실행)
            total_lines = await self._run_sync_function(
                self._add_line_numbers, str(info_md_file), str(output_file_path)
            )
            
            if total_lines > 0:
                print(f"✅ 라인 번호 추가 완료: {total_lines}개 라인")
                print(f"📍 IDE 라인 번호와 동일한 형식으로 생성됨")
                
                self._log_step_success()
                return StepResult(
                    success=True,
                    data={
                        "info_md_with_lines_path": str(output_file_path),
                        "original_info_md_path": str(info_md_file),
                        "total_lines": total_lines,
                        "line_number_format": "Line X: 형식"
                    }
                )
            else:
                error_msg = "라인 번호 추가 실패"
                self._log_step_error(error_msg)
                return StepResult(success=False, error=error_msg)
        
        except Exception as e:
            error_msg = f"라인 번호 추가 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult(success=False, error=error_msg)
    
    def _add_line_numbers(self, input_path: str, output_path: str) -> int:
        """각 라인에 "Line X: " 형식으로 라인 번호 추가 (add_line_numbers.py 로직)"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            numbered_lines = []
            
            for line_num, line in enumerate(lines, start=1):
                # 각 라인 앞에 "Line X: " 추가
                # 개행 문자 처리: 기존 라인의 개행 문자 유지
                if line.endswith('\n'):
                    numbered_line = f"Line {line_num}: {line}"
                else:
                    numbered_line = f"Line {line_num}: {line}\n"
                
                numbered_lines.append(numbered_line)
                
                # 진행 상황 표시 (20줄마다)
                if line_num % 20 == 0 or line_num == len(lines):
                    print(f"   처리 중... {line_num}/{len(lines)} 라인")
            
            # 새 파일에 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(numbered_lines)
            
            return len(lines)
            
        except Exception as e:
            print(f"❌ 라인 번호 추가 중 오류: {e}")
            return 0
    
    def _validate_output(self, output_path: str) -> bool:
        """출력 파일 유효성 검증"""
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 모든 라인이 "Line X: "로 시작하는지 확인
            for line_num, line in enumerate(lines, start=1):
                expected_prefix = f"Line {line_num}: "
                if not line.startswith(expected_prefix):
                    print(f"❌ 검증 실패: Line {line_num}이 올바른 형식이 아님")
                    return False
            
            print(f"📊 검증 결과: {len(lines)}개 라인 모두 올바른 형식")
            return True
            
        except Exception as e:
            print(f"❌ 출력 파일 검증 중 오류: {e}")
            return False