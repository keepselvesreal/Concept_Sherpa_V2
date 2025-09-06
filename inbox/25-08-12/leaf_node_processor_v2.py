"""
생성 시간: 2025-08-12 15:07:00 KST
핵심 내용: 리프 노드 처리 시스템 V2 - 공통 모듈과 새로운 로깅 시스템을 사용하는 개선된 버전
상세 내용:
    - LeafNodeProcessor 클래스 (라인 30-): 공통 모듈 기반 리프 노드 처리 클래스
    - ContentAnalyzer 통합 (라인 35): 4가지 정보 추출 공통 모듈 활용
    - ProcessLogger 통합 (라인 38): 구조화된 로깅 시스템 활용
    - process_single_leaf_node() (라인 70-): 단일 리프 노드 처리 (개선됨)
    - load_leaf_content() (라인 135-): 리프 파일에서 내용 로드
    - update_section() (라인 155-): 파일 섹션 업데이트
    - process_all_leaf_nodes_parallel() (라인 175-): 병렬 처리 관리자
상태: 활성  
주소: leaf_node_processor_v2
참조: leaf_node_processor.py (기존 버전), content_analysis_module.py, logging_system.py
"""

import asyncio
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from node_structure_analyzer import Node
from content_analysis_module import ContentAnalyzer
from logging_system import ProcessLogger, ReportGenerator


class LeafNodeProcessor:
    """공통 모듈을 사용하는 리프 노드 처리 클래스 V2"""
    
    def __init__(self, output_dir: str, max_concurrent_tasks: int = 2):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.max_concurrent_tasks = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        
        # 공통 모듈 초기화
        self.logger = ProcessLogger("leaf_node_processor", self.output_dir)
        self.content_analyzer = ContentAnalyzer(self.logger.logger)
        self.report_generator = ReportGenerator(self.output_dir)
        
        # 처리 통계
        self.processing_stats = {
            "total_nodes": 0,
            "successful_nodes": 0,
            "failed_nodes": 0,
            "node_results": {}
        }
    
    def create_leaf_info_file(self, node: Node) -> Path:
        """리프 노드 정보 파일 기본 구조 생성"""
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        info_file_path = self.output_dir / f"leaf_{safe_title}_info.md"
        
        template = """# 추가 정보

## 핵심 내용

## 상세 핵심 내용

## 주요 화제

## 부차 화제
"""
        
        with open(info_file_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        self.logger.log_operation(f"정보파일생성_{node.title}", "성공", {"파일경로": str(info_file_path)})
        return info_file_path

    async def process_single_leaf_node(self, node: Node, leaf_content_dir: Path) -> tuple:
        """단일 리프 노드 처리 (공통 모듈 사용)"""
        async with self.semaphore:
            operation_start_time = time.time()
            node_name = node.title
            
            try:
                self.logger.log_operation(f"노드처리시작_{node_name}", "시작")
                
                # 1. 리프 노드 내용 로드
                leaf_content = self.load_leaf_content(node, leaf_content_dir)
                
                if not leaf_content:
                    self.logger.log_operation(f"노드처리_{node_name}", "실패", {"이유": "리프 내용 로드 실패"})
                    return (node, False)
                
                self.logger.log_operation(f"내용로드_{node_name}", "성공", 
                                        {"내용길이": len(leaf_content), "문자수": len(leaf_content)})
                
                # 2. 정보 파일 생성
                info_file_path = self.create_leaf_info_file(node)
                
                # 3. 4가지 정보 추출 (공통 모듈 사용)
                analysis_start_time = time.time()
                self.logger.log_operation(f"4가지분석시작_{node_name}", "시작")
                
                analysis_result = await self.content_analyzer.analyze_content(
                    content=leaf_content,
                    title=node_name,
                    context_type="section"
                )
                
                analysis_duration = time.time() - analysis_start_time
                self.logger.log_operation(f"4가지분석완료_{node_name}", "성공", 
                                        {"소요시간": f"{analysis_duration:.2f}초"}, analysis_duration)
                
                # 4. 결과를 파일에 업데이트
                update_start_time = time.time()
                success_count = 0
                
                for section_name, content in analysis_result.items():
                    if content and not content.startswith("분석 실패") and len(content.strip()) > 0:
                        if self.update_section(info_file_path, section_name, content):
                            success_count += 1
                            self.logger.log_operation(f"섹션업데이트_{node_name}_{section_name}", "성공",
                                                    {"내용길이": len(content)})
                        else:
                            self.logger.log_operation(f"섹션업데이트_{node_name}_{section_name}", "실패")
                    else:
                        self.logger.log_operation(f"섹션업데이트_{node_name}_{section_name}", "실패",
                                                {"이유": "분석 결과 없음 또는 오류"})
                
                update_duration = time.time() - update_start_time
                
                # 5. 작업 완료 후 파일명 변경
                total_duration = time.time() - operation_start_time
                
                if success_count == 4:
                    filled_path = self.rename_to_filled(info_file_path)
                    self.logger.log_operation(f"노드처리완료_{node_name}", "성공", 
                                            {"성공섹션": f"{success_count}/4", 
                                             "최종파일": filled_path.name,
                                             "총소요시간": f"{total_duration:.2f}초"}, total_duration)
                    
                    # 통계 업데이트
                    self.processing_stats["successful_nodes"] += 1
                    self.processing_stats["node_results"][node_name] = {
                        "status": "성공",
                        "success": True,
                        "updated_sections": list(analysis_result.keys()),
                        "duration": total_duration
                    }
                    
                    return (node, True)
                else:
                    self.logger.log_operation(f"노드처리부분실패_{node_name}", "경고", 
                                            {"성공섹션": f"{success_count}/4",
                                             "총소요시간": f"{total_duration:.2f}초"}, total_duration)
                    
                    # 통계 업데이트
                    self.processing_stats["failed_nodes"] += 1
                    self.processing_stats["node_results"][node_name] = {
                        "status": f"부분실패 ({success_count}/4 섹션 성공)",
                        "success": False,
                        "updated_sections": [k for k, v in analysis_result.items() if v and len(v.strip()) > 0],
                        "duration": total_duration
                    }
                    
                    return (node, False)
                
            except Exception as e:
                total_duration = time.time() - operation_start_time
                self.logger.log_error(f"노드처리_{node_name}", e, {"소요시간": f"{total_duration:.2f}초"})
                
                # 통계 업데이트
                self.processing_stats["failed_nodes"] += 1
                self.processing_stats["node_results"][node_name] = {
                    "status": "오류 발생",
                    "success": False,
                    "error": str(e),
                    "duration": total_duration
                }
                
                return (node, False)

    def load_leaf_content(self, node: Node, content_dir: Path) -> Optional[str]:
        """리프 노드의 내용을 로드 (leaf_로 시작하는 파일에서)"""
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        # leaf_로 시작하는 파일들을 찾아서 내용 로드
        possible_files = [
            content_dir / f"leaf_{safe_title}.md",
            content_dir / f"leaf_{safe_title}_info_filled.md"
        ]
        
        for file_path in possible_files:
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.logger.log_operation(f"파일로드_{node.title}", "성공", 
                                            {"파일경로": str(file_path), "내용길이": len(content)})
                    return content
                except Exception as e:
                    self.logger.log_error(f"파일읽기_{node.title}", e, {"파일경로": str(file_path)})
        
        self.logger.log_operation(f"파일로드_{node.title}", "실패", 
                                {"시도한파일들": [str(f) for f in possible_files]})
        return None

    def update_section(self, file_path: Path, header: str, content: str) -> bool:
        """파일의 특정 헤더 섹션에 내용 업데이트"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            header_pattern = f"## {header}"
            header_start = text.find(header_pattern)
            
            if header_start == -1:
                self.logger.log_validation(f"헤더찾기_{header}", False, f"헤더를 찾을 수 없음: {header}")
                return False
            
            content_start = header_start + len(header_pattern)
            next_header_start = text.find("\n## ", content_start)
            
            if next_header_start == -1:
                new_text = text[:content_start] + f"\n{content}\n"
            else:
                new_text = text[:content_start] + f"\n{content}\n" + text[next_header_start:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_text)
            
            return True
            
        except Exception as e:
            self.logger.log_error(f"섹션업데이트_{header}", e)
            return False

    async def process_all_leaf_nodes_parallel(self, leaf_nodes: List[Node], leaf_content_dir: Path) -> int:
        """모든 리프 노드를 병렬 처리 (공통 모듈 및 로깅 사용)"""
        process_info = {
            "총노드수": len(leaf_nodes),
            "최대동시작업": self.max_concurrent_tasks,
            "리프내용디렉토리": str(leaf_content_dir),
            "출력디렉토리": str(self.output_dir)
        }
        
        self.logger.log_process_start(process_info)
        self.processing_stats["total_nodes"] = len(leaf_nodes)
        
        start_time = time.time()
        
        # 모든 작업을 병렬로 실행할 태스크 생성
        tasks = []
        for node in leaf_nodes:
            task = self.process_single_leaf_node(node, leaf_content_dir)
            tasks.append(task)
        
        try:
            self.logger.log_operation("병렬처리시작", "시작", {"작업수": len(tasks)})
            
            # 모든 태스크 병렬 실행
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 분석
            success_count = 0
            error_count = 0
            
            for result in results:
                if isinstance(result, Exception):
                    error_count += 1
                    self.logger.log_error("병렬작업", result)
                else:
                    node, success = result
                    if success:
                        success_count += 1
            
            elapsed_time = time.time() - start_time
            
            # 처리 완료 로깅
            summary = {
                "성공노드": f"{success_count}/{len(leaf_nodes)}",
                "실패노드": f"{len(leaf_nodes) - success_count}/{len(leaf_nodes)}",
                "성공률": f"{(success_count/len(leaf_nodes)*100):.1f}%",
                "총처리시간": f"{elapsed_time:.2f}초",
                "평균처리속도": f"{len(leaf_nodes)/elapsed_time:.2f} 노드/초"
            }
            
            self.logger.log_process_end(success_count > len(leaf_nodes) // 2, summary)
            
            # 보고서 생성
            process_report = self.logger.create_process_report()
            update_report = self.report_generator.generate_update_report(
                "leaf_node_processor", self.processing_stats["node_results"]
            )
            
            self.logger.log_operation("보고서생성", "성공", 
                                    {"프로세스보고서": process_report.name,
                                     "업데이트보고서": update_report.name})
            
            return success_count
            
        except Exception as e:
            self.logger.log_error("병렬처리", e)
            self.logger.log_process_end(False, {"오류": str(e)})
            return 0

    def rename_to_filled(self, info_file_path: Path) -> Path:
        """정보 파일명을 _filled 접미사로 변경"""
        filled_path = info_file_path.parent / f"{info_file_path.stem}_filled.md"
        info_file_path.rename(filled_path)
        return filled_path


async def main():
    """테스트 실행"""
    from node_structure_analyzer import NodeStructureAnalyzer
    
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json"
    leaf_content_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12"  # leaf_ 파일들이 있는 디렉토리
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12"
    
    print("=" * 60)
    print("리프 노드 처리 시스템 V2 - 공통 모듈 버전")
    print("=" * 60)
    
    # 노드 구조 분석
    analyzer = NodeStructureAnalyzer(json_path, "")
    if not analyzer.load_json_structure():
        return
    
    # 리프 노드 처리 (병렬, MAX_CONCURRENT_TASKS=2)
    processor = LeafNodeProcessor(output_dir, max_concurrent_tasks=2)
    leaf_nodes = analyzer.get_leaf_nodes()
    
    print(f"🎯 처리 대상: {len(leaf_nodes)}개 리프 노드")
    print(f"📂 리프 내용 디렉토리: {leaf_content_dir}")
    
    # 비동기 병렬 실행
    success_count = await processor.process_all_leaf_nodes_parallel(leaf_nodes, Path(leaf_content_dir))
    
    print(f"\n🎯 최종 결과: {success_count}/{len(leaf_nodes)} 리프 노드 처리 성공")
    
    # 생성된 파일 확인
    print(f"\n📁 생성된 파일 확인:")
    output_path = Path(output_dir)
    filled_files = list(output_path.glob("leaf_*_info_filled.md"))
    
    print(f"  - leaf_*_info_filled.md: {len(filled_files)}개")
    for file in filled_files[:5]:  # 처음 5개만 표시
        print(f"    - {file.name}")
    if len(filled_files) > 5:
        print(f"    - ... 외 {len(filled_files)-5}개")


if __name__ == "__main__":
    asyncio.run(main())