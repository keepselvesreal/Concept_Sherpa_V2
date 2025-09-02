# 생성 시간: Mon Jan  2 16:25:00 KST 2025
# 핵심 내용: 리팩토링 전용 경량 로거 - 문제 포착 및 작업 추적 중심
# 상세 내용:
#   - RefactoringLogContext (라인 16-25): 로그 컨텍스트 데이터 클래스
#   - RefactoringLogger (라인 27-140): 리팩토링 전용 로거 메인 클래스
#   - operation_start (라인 45-55): 작업 시작 로깅
#   - operation_success (라인 57-67): 작업 성공 로깅
#   - operation_error (라인 69-86): 작업 실패 로깅 (상세)
#   - unexpected_result (라인 88-100): 예상과 다른 결과 로깅
#   - _sanitize_inputs/_sanitize_outputs (라인 102-140): 입출력 데이터 정리
# 상태: active

from dataclasses import dataclass
from typing import Any, Dict, Optional
import json
from datetime import datetime
from pathlib import Path
import traceback

@dataclass
class RefactoringLogContext:
    """리팩토링 로그 컨텍스트"""
    stage: str          # "workspace_prep", "chapter_integration" 등
    class_name: str     # 실제 클래스명
    method_name: str    # 실제 메서드명
    operation_id: str   # 유니크한 작업 ID (타임스탬프 기반)
    
    def __post_init__(self):
        if not self.operation_id:
            self.operation_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

class RefactoringLogger:
    """리팩토링 전용 경량 로거"""
    
    def __init__(self, base_log_dir: Path):
        self.base_log_dir = Path(base_log_dir)
        self.base_log_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_log_file(self, context: RefactoringLogContext) -> Path:
        """logs/{stage}/{class_name}_{method_name}.log"""
        stage_dir = self.base_log_dir / context.stage
        stage_dir.mkdir(exist_ok=True)
        return stage_dir / f"{context.class_name}_{context.method_name}.log"
    
    def operation_start(self, context: RefactoringLogContext, inputs: Dict[str, Any]):
        """작업 시작 로깅 - 입력값만"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation_id": context.operation_id,
            "event": "START",
            "class": context.class_name,
            "method": context.method_name,
            "inputs": self._sanitize_inputs(inputs)
        }
        self._write_log(context, log_entry)
    
    def operation_success(self, context: RefactoringLogContext, outputs: Dict[str, Any]):
        """작업 성공 로깅 - 출력값만"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation_id": context.operation_id,
            "event": "SUCCESS",
            "class": context.class_name,
            "method": context.method_name,
            "outputs": self._sanitize_outputs(outputs)
        }
        self._write_log(context, log_entry)
    
    def operation_error(self, context: RefactoringLogContext, error: Exception, 
                       inputs: Dict[str, Any] = None):
        """작업 실패 로깅 - 상세한 오류 정보"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation_id": context.operation_id,
            "event": "ERROR",
            "class": context.class_name,
            "method": context.method_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
        }
        
        if inputs:
            log_entry["inputs_at_failure"] = self._sanitize_inputs(inputs)
            
        self._write_log(context, log_entry)
    
    def unexpected_result(self, context: RefactoringLogContext, 
                         expected: Any, actual: Any, description: str):
        """예상과 다른 결과 로깅"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation_id": context.operation_id,
            "event": "UNEXPECTED",
            "class": context.class_name,
            "method": context.method_name,
            "description": description,
            "expected": str(expected),
            "actual": str(actual)
        }
        self._write_log(context, log_entry)
    
    def save_result(self, context: RefactoringLogContext, result: Any, 
                   filename: Optional[str] = None, description: str = "Result saved"):
        """최종 결과를 파일로 저장 (사용자 확인용)"""
        import json
        from datetime import datetime
        
        # 결과 저장 디렉토리
        results_dir = self.base_log_dir / "results"
        results_dir.mkdir(exist_ok=True)
        
        # 파일명 생성
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{context.class_name}_{context.method_name}_{timestamp}.json"
        
        result_file = results_dir / filename
        
        # 결과 저장
        try:
            with open(result_file, 'w', encoding='utf-8') as f:
                if isinstance(result, (dict, list)):
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    # 기타 객체는 문자열로 변환
                    json.dump({"result": str(result), "type": type(result).__name__}, 
                             f, ensure_ascii=False, indent=2)
            
            # 로그 기록
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation_id": context.operation_id,
                "event": "RESULT_SAVED",
                "class": context.class_name,
                "method": context.method_name,
                "description": description,
                "result_file": str(result_file.relative_to(self.base_log_dir.parent)),
                "file_size": result_file.stat().st_size
            }
            
            self._write_log(context, log_entry)
            return str(result_file)
            
        except Exception as e:
            # 저장 실패 시 로그만 기록
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation_id": context.operation_id,
                "event": "RESULT_SAVE_FAILED",
                "class": context.class_name,
                "method": context.method_name,
                "error": str(e),
                "attempted_file": str(result_file)
            }
            self._write_log(context, log_entry)
            return None
    
    def _sanitize_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """입력값 정리 - 파일 경로, 크기 등만"""
        sanitized = {}
        for key, value in inputs.items():
            if isinstance(value, (str, Path)) and ('path' in key.lower() or 'file' in key.lower()):
                sanitized[key] = str(value)
                # 파일 존재 여부도 체크
                if Path(value).exists():
                    sanitized[f"{key}_exists"] = True
                    if Path(value).is_file():
                        sanitized[f"{key}_size"] = Path(value).stat().st_size
                else:
                    sanitized[f"{key}_exists"] = False
            elif isinstance(value, (int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, (list, dict)):
                sanitized[f"{key}_type"] = type(value).__name__
                sanitized[f"{key}_length"] = len(value)
            else:
                sanitized[f"{key}_type"] = type(value).__name__
        return sanitized
    
    def _sanitize_outputs(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """출력값 정리 - 성공/실패, 생성된 파일 등만"""
        sanitized = {}
        for key, value in outputs.items():
            if key in ['success', 'is_success', 'error']:
                sanitized[key] = value
            elif 'count' in key.lower() or 'number' in key.lower():
                sanitized[key] = value
            elif isinstance(value, (list, dict)):
                sanitized[f"{key}_length"] = len(value)
            elif isinstance(value, (str, Path)) and ('path' in key.lower() or 'file' in key.lower()):
                sanitized[key] = str(value)
        return sanitized
    
    def _write_log(self, context: RefactoringLogContext, log_entry: Dict[str, Any]):
        """로그 파일에 JSON 라인 추가"""
        log_file = self._get_log_file(context)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')