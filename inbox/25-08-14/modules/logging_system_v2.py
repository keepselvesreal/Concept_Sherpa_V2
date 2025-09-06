"""
생성 시간: 2025-08-14 14:48:59 KST
핵심 내용: 강화된 로깅 시스템 V2 - 단계별 테스트 및 의존성 추적 지원
상세 내용:
    - ProcessLogger 클래스 (라인 25-): 기본 로깅 기능 유지
    - TestLogger 클래스 (라인 350-): 테스트 전용 확장 로거
    - log_test_stage() (라인 370-): 테스트 단계별 세분화 로깅
    - log_dependency_check() (라인 390-): 의존성 검증 로깅  
    - log_level_status() (라인 410-): 레벨별 진행 상황 로깅
    - log_status_change() (라인 430-): 노드 상태 변화 추적
    - log_assertion() (라인 450-): 테스트 단언 로깅
    - log_file_state() (라인 470-): 파일 상태 로깅
    - create_test_report() (라인 490-): 테스트 결과 상세 보고서
상태: 활성
주소: logging_system_v2
참조: logging_system.py (원본 버전)
"""

import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ProcessLogger:
    """프로세스별 전용 로거 클래스 - 기본 기능"""
    
    def __init__(self, process_name: str, output_dir: Path):
        self.process_name = process_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.logger = self.setup_process_logger()
        self.process_start_time = None
        self.operation_times = {}
        self.operation_results = {}
        
    def setup_process_logger(self) -> logging.Logger:
        """프로세스별 로거 설정"""
        log_file = self.output_dir / f"{self.process_name}.log"
        
        # 로거 생성
        logger = logging.getLogger(f'{self.process_name}_{id(self)}')
        logger.setLevel(logging.DEBUG)
        
        # 기존 핸들러 제거
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 포매터
        formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logger.info(f"=== {self.process_name} 로깅 시스템 초기화 완료 ===")
        return logger
    
    def log_process_start(self, process_info: Dict[str, Any]):
        """프로세스 시작 로깅"""
        self.process_start_time = time.time()
        self.logger.info(f"🚀 {self.process_name} 프로세스 시작")
        for key, value in process_info.items():
            self.logger.info(f"   📋 {key}: {value}")
    
    def log_process_end(self, success: bool, summary: Dict[str, Any] = None):
        """프로세스 종료 로깅"""
        if self.process_start_time:
            duration = time.time() - self.process_start_time
            self.logger.info(f"⏱️ 전체 프로세스 소요 시간: {duration:.2f}초")
        
        status = "성공" if success else "실패"
        self.logger.info(f"🏁 {self.process_name} 프로세스 완료: {status}")
        
        if summary:
            for key, value in summary.items():
                self.logger.info(f"   📊 {key}: {value}")
    
    def log_operation(self, operation_name: str, status: str, details: Dict[str, Any] = None, 
                     duration: float = None):
        """개별 작업 로깅"""
        timestamp = time.time()
        
        # 상태별 이모지
        status_emoji = {
            "시작": "🔄",
            "성공": "✅", 
            "실패": "❌",
            "경고": "⚠️",
            "정보": "ℹ️",
            "진행중": "🔄",
            "완료": "✅"
        }
        
        emoji = status_emoji.get(status, "📋")
        log_message = f"{emoji} {operation_name}: {status}"
        
        if duration:
            log_message += f" ({duration:.2f}초)"
        
        self.logger.info(log_message)
        
        # 세부사항 로깅
        if details:
            for key, value in details.items():
                self.logger.debug(f"   - {key}: {value}")
        
        # 작업 결과 저장
        self.operation_results[operation_name] = {
            "status": status,
            "timestamp": timestamp,
            "duration": duration,
            "details": details or {}
        }
    
    def log_validation(self, validation_name: str, result: bool, message: str = ""):
        """검증 결과 로깅"""
        status = "성공" if result else "실패"
        emoji = "✅" if result else "❌"
        
        log_message = f"{emoji} 검증_{validation_name}: {status}"
        if message:
            log_message += f" - {message}"
        
        self.logger.info(log_message)
    
    def log_error(self, error_context: str, error: Exception, details: Dict[str, Any] = None):
        """오류 로깅"""
        self.logger.error(f"❌ {error_context}: {str(error)}")
        if details:
            for key, value in details.items():
                self.logger.error(f"   - {key}: {value}")
    
    def create_process_report(self) -> Path:
        """프로세스 완료 보고서 생성"""
        report_path = self.output_dir / f"{self.process_name}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # 통계 계산
        total_operations = len(self.operation_results)
        successful_operations = sum(1 for op in self.operation_results.values() if op["status"] in ["성공", "완료"])
        failed_operations = total_operations - successful_operations
        
        # 보고서 내용 생성
        report_content = f"""# {self.process_name} 처리 보고서

## 개요
- **프로세스명**: {self.process_name}
- **실행 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **전체 소요 시간**: {time.time() - self.process_start_time:.2f}초 (시작 시점부터)

## 처리 결과
- **전체 작업 수**: {total_operations}
- **성공 작업**: {successful_operations}
- **실패 작업**: {failed_operations}
- **성공률**: {(successful_operations/total_operations*100):.1f}% (전체 작업 기준)

## 작업별 상세 결과

"""
        
        # 작업별 결과 추가
        for operation_name, result in self.operation_results.items():
            status_emoji = "✅" if result["status"] in ["성공", "완료"] else "❌"
            duration_text = f" ({result['duration']:.2f}초)" if result['duration'] else ""
            
            report_content += f"### {status_emoji} {operation_name}\n"
            report_content += f"- **상태**: {result['status']}\n"
            report_content += f"- **실행 시간**: {datetime.fromtimestamp(result['timestamp']).strftime('%H:%M:%S')}\n"
            
            if result['duration']:
                report_content += f"- **소요 시간**: {result['duration']:.2f}초\n"
            
            if result['details']:
                report_content += "- **세부사항**:\n"
                for key, value in result['details'].items():
                    report_content += f"  - {key}: {value}\n"
            
            report_content += "\n"
        
        report_content += f"""---
*보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 보고서 파일 생성
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"📊 프로세스 보고서 생성 완료: {report_path.name}")
        return report_path


class TestLogger(ProcessLogger):
    """테스트 전용 확장 로거 - 단계별 추적 및 의존성 검증"""
    
    def __init__(self, test_name: str, output_dir: Path):
        super().__init__(f"test_{test_name}", output_dir)
        self.test_stages = {}  # 테스트 단계별 결과
        self.dependency_checks = {}  # 의존성 검증 결과
        self.level_statuses = {}  # 레벨별 상태
        self.status_changes = {}  # 상태 변화 추적
        self.assertions = {}  # 테스트 단언 결과
        self.file_states = {}  # 파일 상태 추적
        
    def log_test_stage(self, stage_name: str, target: str, status: str, details: Dict[str, Any] = None):
        """테스트 단계별 세분화 로깅"""
        timestamp = time.time()
        
        # 단계별 이모지
        stage_emoji = {
            "시작": "🔄",
            "성공": "✅",
            "실패": "❌",
            "건너뜀": "⏭️",
            "진행중": "🔄"
        }
        
        emoji = stage_emoji.get(status, "📋")
        log_message = f"{emoji} [테스트단계] {stage_name} - {target}: {status}"
        
        self.logger.info(log_message)
        
        # 세부사항 로깅
        if details:
            for key, value in details.items():
                self.logger.debug(f"   🔍 {key}: {value}")
        
        # 테스트 단계 결과 저장
        stage_key = f"{stage_name}_{target}"
        self.test_stages[stage_key] = {
            "stage": stage_name,
            "target": target,
            "status": status,
            "timestamp": timestamp,
            "details": details or {}
        }
    
    def log_dependency_check(self, parent: str, children: List[str], all_completed: bool, 
                           completed_children: List[str] = None):
        """의존성 검증 로깅"""
        timestamp = time.time()
        completed_children = completed_children or []
        
        status_emoji = "✅" if all_completed else "❌"
        completion_rate = f"{len(completed_children)}/{len(children)}"
        
        log_message = f"{status_emoji} [의존성검증] {parent}: {completion_rate} 자식 완료"
        self.logger.info(log_message)
        
        # 자식별 상태 로깅
        for child in children:
            child_status = "✅" if child in completed_children else "⏳"
            self.logger.debug(f"   {child_status} 자식노드: {child}")
        
        # 의존성 검증 결과 저장
        self.dependency_checks[parent] = {
            "parent": parent,
            "children": children,
            "completed_children": completed_children,
            "all_completed": all_completed,
            "completion_rate": completion_rate,
            "timestamp": timestamp
        }
    
    def log_level_status(self, level: int, stats: Dict[str, int], all_completed: bool = False):
        """레벨별 진행 상황 로깅"""
        timestamp = time.time()
        
        total_nodes = stats.get("total", 0)
        completed_nodes = stats.get("completed", 0)
        leaf_nodes = stats.get("leaf_nodes", 0)
        parent_nodes = stats.get("parent_nodes", 0)
        
        completion_rate = f"{completed_nodes}/{total_nodes}" if total_nodes > 0 else "0/0"
        status_emoji = "✅" if all_completed else "🔄"
        
        log_message = f"{status_emoji} [레벨상태] 레벨{level}: {completion_rate} 완료"
        self.logger.info(log_message)
        self.logger.debug(f"   📊 리프노드: {leaf_nodes}개, 부모노드: {parent_nodes}개")
        
        # 레벨 상태 저장
        self.level_statuses[level] = {
            "level": level,
            "stats": stats,
            "completion_rate": completion_rate,
            "all_completed": all_completed,
            "timestamp": timestamp
        }
    
    def log_status_change(self, node: str, before: str, after: str, file_path: str = ""):
        """노드 상태 변화 추적"""
        timestamp = time.time()
        
        change_emoji = "🔄" if before != after else "ℹ️"
        log_message = f"{change_emoji} [상태변화] {node}: {before} → {after}"
        
        if file_path:
            log_message += f" (파일: {Path(file_path).name})"
        
        self.logger.info(log_message)
        
        # 상태 변화 저장
        change_key = f"{node}_{timestamp}"
        self.status_changes[change_key] = {
            "node": node,
            "before": before,
            "after": after,
            "file_path": file_path,
            "timestamp": timestamp,
            "changed": before != after
        }
    
    def log_assertion(self, test_name: str, expected: Any, actual: Any, passed: bool, 
                     message: str = ""):
        """테스트 단언 로깅"""
        timestamp = time.time()
        
        status_emoji = "✅" if passed else "❌"
        log_message = f"{status_emoji} [단언] {test_name}: {'통과' if passed else '실패'}"
        
        if message:
            log_message += f" - {message}"
        
        self.logger.info(log_message)
        self.logger.debug(f"   🎯 예상값: {expected}")
        self.logger.debug(f"   📝 실제값: {actual}")
        
        # 단언 결과 저장
        self.assertions[test_name] = {
            "test_name": test_name,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "message": message,
            "timestamp": timestamp
        }
    
    def log_file_state(self, file_path: Path, section: str, content_length: int, 
                      status: str = "확인"):
        """파일 상태 로깅"""
        timestamp = time.time()
        
        file_name = file_path.name if isinstance(file_path, Path) else Path(file_path).name
        log_message = f"📄 [파일상태] {file_name}/{section}: {content_length}자 ({status})"
        
        self.logger.debug(log_message)
        
        # 파일 상태 저장
        state_key = f"{file_name}_{section}"
        self.file_states[state_key] = {
            "file_path": str(file_path),
            "file_name": file_name,
            "section": section,
            "content_length": content_length,
            "status": status,
            "timestamp": timestamp
        }
    
    def log_test_summary(self, test_category: str, success: int, failed: int, 
                        duration: float = None):
        """테스트 카테고리별 요약 로깅"""
        total = success + failed
        success_rate = (success / total * 100) if total > 0 else 0
        
        summary_emoji = "✅" if failed == 0 else "⚠️" if success > failed else "❌"
        log_message = f"{summary_emoji} [테스트요약] {test_category}: {success}/{total} 성공 ({success_rate:.1f}%)"
        
        if duration:
            log_message += f" (소요: {duration:.2f}초)"
        
        self.logger.info(log_message)
    
    def create_test_report(self) -> Path:
        """테스트 결과 상세 보고서 생성"""
        report_path = self.output_dir / f"{self.process_name}_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # 통계 계산
        total_stages = len(self.test_stages)
        successful_stages = sum(1 for stage in self.test_stages.values() if stage["status"] in ["성공", "완료"])
        
        total_assertions = len(self.assertions)
        passed_assertions = sum(1 for assertion in self.assertions.values() if assertion["passed"])
        
        # 성공률 계산
        stage_success_rate = (successful_stages/total_stages*100) if total_stages > 0 else 0.0
        assertion_success_rate = (passed_assertions/total_assertions*100) if total_assertions > 0 else 0.0
        
        # 보고서 내용 생성
        report_content = f"""# {self.process_name} 테스트 상세 보고서

## 📊 테스트 개요
- **테스트명**: {self.process_name}
- **실행 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **전체 소요 시간**: {time.time() - self.process_start_time:.2f}초

## 📈 테스트 결과 요약
- **테스트 단계**: {successful_stages}/{total_stages} 성공 ({stage_success_rate:.1f}%)
- **단언 검사**: {passed_assertions}/{total_assertions} 통과 ({assertion_success_rate:.1f}%)
- **의존성 검증**: {len(self.dependency_checks)}건
- **레벨 상태 추적**: {len(self.level_statuses)}개 레벨
- **상태 변화 추적**: {len(self.status_changes)}건

## 🧪 테스트 단계별 결과

"""
        
        # 테스트 단계 결과
        for stage_key, stage_info in self.test_stages.items():
            status_emoji = "✅" if stage_info["status"] in ["성공", "완료"] else "❌"
            
            report_content += f"### {status_emoji} {stage_info['stage']} - {stage_info['target']}\n"
            report_content += f"- **상태**: {stage_info['status']}\n"
            report_content += f"- **시간**: {datetime.fromtimestamp(stage_info['timestamp']).strftime('%H:%M:%S')}\n"
            
            if stage_info['details']:
                report_content += "- **세부사항**:\n"
                for key, value in stage_info['details'].items():
                    report_content += f"  - {key}: {value}\n"
            
            report_content += "\n"
        
        # 의존성 검증 결과
        if self.dependency_checks:
            report_content += "## 🔗 의존성 검증 결과\n\n"
            
            for parent, dep_info in self.dependency_checks.items():
                status_emoji = "✅" if dep_info["all_completed"] else "❌"
                
                report_content += f"### {status_emoji} {parent}\n"
                report_content += f"- **완료율**: {dep_info['completion_rate']}\n"
                report_content += f"- **전체 완료**: {'예' if dep_info['all_completed'] else '아니오'}\n"
                report_content += "- **자식 노드들**:\n"
                
                for child in dep_info['children']:
                    child_emoji = "✅" if child in dep_info['completed_children'] else "❌"
                    report_content += f"  - {child_emoji} {child}\n"
                
                report_content += "\n"
        
        # 레벨 상태 추적
        if self.level_statuses:
            report_content += "## 📊 레벨별 상태 추적\n\n"
            
            for level, level_info in sorted(self.level_statuses.items()):
                status_emoji = "✅" if level_info["all_completed"] else "🔄"
                
                report_content += f"### {status_emoji} 레벨 {level}\n"
                report_content += f"- **완료율**: {level_info['completion_rate']}\n"
                
                stats = level_info['stats']
                report_content += f"- **리프 노드**: {stats.get('leaf_nodes', 0)}개\n"
                report_content += f"- **부모 노드**: {stats.get('parent_nodes', 0)}개\n"
                report_content += f"- **전체 완료**: {'예' if level_info['all_completed'] else '아니오'}\n\n"
        
        # 단언 검사 결과
        if self.assertions:
            report_content += "## ✅ 단언 검사 결과\n\n"
            
            for test_name, assertion_info in self.assertions.items():
                status_emoji = "✅" if assertion_info["passed"] else "❌"
                
                report_content += f"### {status_emoji} {test_name}\n"
                report_content += f"- **결과**: {'통과' if assertion_info['passed'] else '실패'}\n"
                report_content += f"- **예상값**: {assertion_info['expected']}\n"
                report_content += f"- **실제값**: {assertion_info['actual']}\n"
                
                if assertion_info['message']:
                    report_content += f"- **메시지**: {assertion_info['message']}\n"
                
                report_content += "\n"
        
        # 상태 변화 추적
        if self.status_changes:
            report_content += "## 🔄 상태 변화 추적\n\n"
            
            for change_key, change_info in self.status_changes.items():
                change_emoji = "🔄" if change_info["changed"] else "ℹ️"
                
                report_content += f"### {change_emoji} {change_info['node']}\n"
                report_content += f"- **변화**: {change_info['before']} → {change_info['after']}\n"
                report_content += f"- **시간**: {datetime.fromtimestamp(change_info['timestamp']).strftime('%H:%M:%S')}\n"
                
                if change_info['file_path']:
                    report_content += f"- **파일**: {Path(change_info['file_path']).name}\n"
                
                report_content += "\n"
        
        report_content += f"""---
*테스트 보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 보고서 파일 생성
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"📊 테스트 보고서 생성 완료: {report_path.name}")
        return report_path


class ReportGenerator:
    """다양한 보고서 생성을 위한 클래스"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_comparison_report(self, process_name: str, before_after_data: Dict[str, Dict[str, str]]) -> Path:
        """작업 전후 비교 보고서 생성"""
        report_path = self.output_dir / f"{process_name}_comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_content = f"""# {process_name} 작업 전후 비교 보고서

## 개요
- **프로세스**: {process_name}
- **비교 실행 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **비교 대상**: {len(before_after_data)}개 항목

## 항목별 변경사항

"""
        
        for item_name, comparison_data in before_after_data.items():
            report_content += f"### {item_name}\n\n"
            
            before_content = comparison_data.get('before', '(비어있음)')
            after_content = comparison_data.get('after', '(비어있음)')
            
            if before_content != after_content:
                report_content += "**변경 전:**\n"
                report_content += f"```\n{before_content[:200]}{'...' if len(before_content) > 200 else ''}\n```\n\n"
                
                report_content += "**변경 후:**\n"
                report_content += f"```\n{after_content[:200]}{'...' if len(after_content) > 200 else ''}\n```\n\n"
                
                report_content += "**상태**: ✅ 업데이트됨\n\n"
            else:
                report_content += "**상태**: 🔄 변경 없음\n\n"
            
            report_content += "---\n\n"
        
        report_content += f"""## 요약

📊 **전체 결과**:
- 변경된 항목: {sum(1 for data in before_after_data.values() if data.get('before') != data.get('after'))}개
- 변경 없는 항목: {sum(1 for data in before_after_data.values() if data.get('before') == data.get('after'))}개

---
*보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path
    
    def generate_update_report(self, process_name: str, node_updates: Dict[str, Dict[str, Any]]) -> Path:
        """노드별 업데이트 과정 보고서 생성"""
        report_path = self.output_dir / f"{process_name}_update_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_content = f"""# {process_name} 업데이트 과정 보고서

## 개요
- **프로세스**: {process_name}
- **업데이트 실행 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **업데이트 대상**: {len(node_updates)}개 노드

## 노드별 업데이트 결과

"""
        
        success_count = 0
        for node_name, update_info in node_updates.items():
            status = update_info.get('status', '알 수 없음')
            success = update_info.get('success', False)
            
            if success:
                success_count += 1
                
            status_emoji = "✅" if success else "❌"
            
            report_content += f"### {status_emoji} {node_name}\n\n"
            report_content += f"- **상태**: {status}\n"
            
            if 'updated_sections' in update_info:
                sections = update_info['updated_sections']
                report_content += f"- **업데이트된 섹션**: {len(sections)}개\n"
                for section in sections:
                    report_content += f"  - {section}\n"
            
            if 'duration' in update_info:
                report_content += f"- **소요 시간**: {update_info['duration']:.2f}초\n"
                
            if 'error' in update_info:
                report_content += f"- **오류**: {update_info['error']}\n"
            
            report_content += "\n---\n\n"
        
        # 요약 추가
        report_content += f"""## 업데이트 요약

📊 **전체 결과**:
- 성공한 노드: {success_count}/{len(node_updates)}개 ({(success_count/len(node_updates)*100):.1f}%)
- 실패한 노드: {len(node_updates) - success_count}/{len(node_updates)}개

---
*보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path