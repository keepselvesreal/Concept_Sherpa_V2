"""
생성 시간: 2025-08-12 15:05:00 KST
핵심 내용: 공통 로깅 시스템 - 구조화된 로깅과 보고서 생성을 위한 통합 시스템
상세 내용:
    - ProcessLogger 클래스 (라인 25-): 프로세스별 전용 로거
    - setup_process_logger() (라인 35-): 프로세스별 로거 설정
    - log_process_start/end() (라인 75-): 프로세스 시작/종료 로깅
    - log_operation() (라인 85-): 개별 작업 로깅
    - create_process_report() (라인 125-): 프로세스 완료 보고서 생성
    - ReportGenerator 클래스 (라인 165-): 다양한 보고서 생성 클래스
    - generate_comparison_report() (라인 175-): 작업 전후 비교 보고서
    - generate_update_report() (라인 215-): 업데이트 과정 보고서
상태: 활성
주소: logging_system
참조: dialectical_synthesis_processor.py (기존 로깅 시스템 참조)
"""

import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ProcessLogger:
    """프로세스별 전용 로거 클래스"""
    
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
            "정보": "ℹ️"
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
        successful_operations = sum(1 for op in self.operation_results.values() if op["status"] == "성공")
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
            status_emoji = "✅" if result["status"] == "성공" else "❌"
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