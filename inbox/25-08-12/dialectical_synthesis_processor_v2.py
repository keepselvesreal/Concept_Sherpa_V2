"""
생성 시간: 2025-08-12 15:12:00 KST
핵심 내용: 정반합 방법론 V2 - 공통 모듈과 핵심 변화 과정 보고서 시스템
상세 내용:
    - DialecticalSynthesisProcessor 클래스 (라인 25-): 정반합 3단계 처리 관리 (개선됨)
    - ContentAnalyzer 통합 (라인 35): 4가지 정보 추출 공통 모듈 활용
    - ProcessLogger 통합 (라인 38): 구조화된 로깅 시스템 활용
    - gather_and_analyze_stage() (라인 90-): 통합분석 단계 - 자식들 결합하여 전체 대상 4가지 정보 추출
    - improve_individual_stage() (라인 142-): 개별개선 단계 - 전체 정보로 각 자식 노드들의 정보 업데이트
    - final_integration_stage() (라인 256-): 최종통합 단계 - 업데이트된 자식들을 반영하여 전체 정보 재업데이트
    - generate_change_reports() (라인 361-): 상위/하위 문서의 모든 변화 과정 보고서 생성
상태: 활성
주소: dialectical_synthesis_processor_v2
참조: dialectical_synthesis_processor.py (기존 버전), content_analysis_module.py, logging_system.py
"""

import asyncio
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from node_structure_analyzer import Node
from content_analysis_module import ContentAnalyzer
from logging_system import ProcessLogger


class DialecticalSynthesisProcessor:
    """정반합 방법론을 적용한 노드 처리 클래스 V2 - 핵심 변화 과정 보고서 중심"""
    
    MAX_CONCURRENT_TASKS = 3  # 동시 실행 작업 수 제한
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 공통 모듈 초기화
        self.logger = ProcessLogger("dialectical_synthesis", self.output_dir)
        self.content_analyzer = ContentAnalyzer(self.logger.logger)
        
        # 병렬 처리를 위한 세마포어
        self.semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_TASKS)
        
        # 변화 과정 추적 데이터
        self.change_tracking = {
            "upper_node_changes": {},  # 상위 노드의 모든 변화 과정
            "child_node_changes": {}   # 각 하위 노드의 모든 변화 과정
        }
    
    def create_node_file(self, node: Node, node_type: str) -> Path:
        """노드 파일 생성"""
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        if node_type == "root":
            node_file_path = self.output_dir / f"root_{safe_title}.md"
            header_level = "#"
        else:
            node_file_path = self.output_dir / f"internal_level_{node.level}_{safe_title}.md"
            header_level = "#" * node.level
        
        # 자식 노드들의 파일명 수집
        child_files = []
        for child in node.children:
            if child.is_leaf():
                safe_child_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                child_file = f"leaf_{safe_child_title}_info_filled.md"
                child_files.append(child_file)
            else:
                child_files.extend(self._collect_leaf_files_from_internal(child))
        
        content = f"{header_level} {node.title}\n\n"
        for child_file in child_files:
            content += f"{child_file}\n"
        
        with open(node_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return node_file_path
    
    def _collect_leaf_files_from_internal(self, internal_node: Node) -> List[str]:
        """내부 노드로부터 모든 리프 노드 파일명 수집 (재귀)"""
        leaf_files = []
        for child in internal_node.children:
            if child.is_leaf():
                safe_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                leaf_files.append(f"leaf_{safe_title}_info_filled.md")
            else:
                leaf_files.extend(self._collect_leaf_files_from_internal(child))
        return leaf_files

    async def gather_and_analyze_stage(self, node: Node) -> Dict[str, str]:
        """통합분석 단계 (정): 자식들 결합하여 전체 대상 4가지 정보 추출"""
        stage_start = time.time()
        self.logger.log_operation(f"통합분석시작_{node.title}", "시작")
        
        # 1. 노드 파일 생성
        node_type = "root" if node.is_root() else "internal"
        node_file = self.create_node_file(node, node_type)
        
        # 2. 노드 정보 파일 생성
        info_file = self.create_node_info_file(node, node_type)
        
        # 3. 자식들 내용 결합
        combined_content = self.combine_children_content(node)
        
        # 4. 공통 모듈을 사용한 4가지 분석
        thesis_info = await self.content_analyzer.analyze_content(
            content=combined_content,
            title=node.title,
            context_type="combined"
        )
        
        # 5. 결과를 정보 파일에 업데이트
        success_count = 0
        for section_name, content in thesis_info.items():
            if content and not content.startswith("분석 실패") and len(content.strip()) > 0:
                if self.update_section(info_file, section_name, content):
                    success_count += 1
        
        # 6. 정보 파일을 _filled로 변경
        filled_file = self.rename_to_filled(info_file, node_type, node)
        
        # 7. 상위 노드 변화 과정 기록 - 통합분석단계
        self.change_tracking["upper_node_changes"][node.title] = {
            "파일명": filled_file.name if filled_file else None,
            "통합분석_최초생성": {
                "핵심 내용": thesis_info.get("핵심 내용", ""),
                "상세 핵심 내용": thesis_info.get("상세 핵심 내용", ""),
                "주요 화제": thesis_info.get("주요 화제", ""),
                "부차 화제": thesis_info.get("부차 화제", "")
            },
            "통합분석_시간": time.time() - stage_start,
            "통합분석_성공": success_count == 4
        }
        
        stage_duration = time.time() - stage_start
        self.logger.log_operation(f"통합분석완료_{node.title}", "성공", 
                                {"성공섹션": f"{success_count}/4", 
                                 "소요시간": f"{stage_duration:.2f}초"}, stage_duration)
        
        return thesis_info

    async def improve_individual_stage(self, node: Node, gathered_info: Dict[str, str]) -> List[Node]:
        """개별개선 단계 (반): 전체 정보로 각 자식 노드들의 핵심/상세 내용만 업데이트"""
        stage_start_time = time.time()
        self.logger.log_operation(f"개별개선시작_{node.title}", "시작")
        
        updated_children = []
        leaf_children = [child for child in node.children if child.is_leaf()]
        
        # 병렬 처리를 위한 작업 리스트 생성
        parallel_tasks = []
        
        for child in leaf_children:
            task_name = f"자식노드_{child.title}_개선"
            parallel_tasks.append(
                self.parallel_task_with_logging(
                    self._process_child_node_v2, 
                    child, gathered_info,
                    task_name=task_name
                )
            )
        
        # 병렬 처리 실행
        if parallel_tasks:
            results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
            
            # 결과 처리
            for i, result in enumerate(results):
                child = leaf_children[i]
                if isinstance(result, Exception):
                    self.logger.log_error(f"자식노드처리_{child.title}", result)
                elif result:
                    updated_children.append(child)
        
        # 내부 노드 처리 (순차적으로)
        for child in node.children:
            if not child.is_leaf():
                updated_children.append(child)
        
        stage_duration = time.time() - stage_start_time
        self.logger.log_operation(f"개별개선완료_{node.title}", "성공", 
                                {"처리자식노드": f"{len(updated_children)}개",
                                 "소요시간": f"{stage_duration:.2f}초"}, stage_duration)
        
        return updated_children

    async def _process_child_node_v2(self, child: Node, gathered_info: Dict[str, str]) -> bool:
        """개별 자식 노드 처리 V2 - 변화 과정 추적"""
        try:
            # 리프 노드 정보 파일 경로
            safe_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
            child_info_file = self.output_dir / f"leaf_{safe_title}_info_filled.md"
            
            if not child_info_file.exists():
                return False
                
            # 기존 내용 읽기 (변화 전)
            with open(child_info_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 기존 4가지 정보 추출
            original_sections = self._extract_all_sections(original_content)
            
            # 기존 주요/부차 화제 보존
            original_main_topics, original_sub_topics = self.preserve_original_topics(child_info_file)
            
            # 개선용 컨텍스트 생성
            enhancement_content = f"""기존 정보:
{original_content}

전체 정보 (보완용):
핵심 내용: {gathered_info.get('핵심 내용', '')}
상세 핵심 내용: {gathered_info.get('상세 핵심 내용', '')}
주요 화제: {gathered_info.get('주요 화제', '')}
부차 화제: {gathered_info.get('부차 화제', '')}"""
            
            # 핵심 내용과 상세 내용만 개선
            enhanced_info = await self.content_analyzer.analyze_content(
                content=enhancement_content,
                title=child.title,
                context_type="enhancement"
            )
            
            # 결과 업데이트 (핵심 내용, 상세 핵심 내용만)
            updated_sections = {}
            for section_name in ["핵심 내용", "상세 핵심 내용"]:
                if section_name in enhanced_info and enhanced_info[section_name]:
                    content = enhanced_info[section_name]
                    if not content.startswith("분석 실패") and len(content.strip()) > 0:
                        if self.update_section(child_info_file, section_name, content):
                            updated_sections[section_name] = content
            
            # 기존 화제들 복원
            if original_main_topics:
                self.update_section(child_info_file, "주요 화제", original_main_topics)
                updated_sections["주요 화제"] = original_main_topics
            if original_sub_topics:
                self.update_section(child_info_file, "부차 화제", original_sub_topics)
                updated_sections["부차 화제"] = original_sub_topics
            
            # 변화 과정 기록
            self.change_tracking["child_node_changes"][child.title] = {
                "파일명": child_info_file.name,
                "개별개선_변화전": original_sections,
                "개별개선_변화후": updated_sections,
                "변화된섹션": [k for k in updated_sections.keys() if k in ["핵심 내용", "상세 핵심 내용"]],
                "보존된섹션": ["주요 화제", "부차 화제"] if (original_main_topics or original_sub_topics) else []
            }
            
            return len(updated_sections) > 0
            
        except Exception as e:
            self.logger.log_error(f"자식처리_{child.title}", e)
            return False

    async def final_integration_stage(self, node: Node, updated_children: List[Node], original_info: Dict[str, str]) -> bool:
        """최종통합 단계 (합): 업데이트된 자식들을 반영하여 전체 정보 재업데이트"""
        stage_start_time = time.time()
        self.logger.log_operation(f"최종통합시작_{node.title}", "시작")
        
        # 1. 업데이트된 자식들의 내용을 다시 결합
        updated_combined_content = self.combine_children_content(node)
        
        # 2. 합성 컨텍스트 생성
        synthesis_content = f"""업데이트된 구성 요소들:
{updated_combined_content}

기존 상위 정보:
핵심 내용: {original_info.get('핵심 내용', '')}
상세 핵심 내용: {original_info.get('상세 핵심 내용', '')}
주요 화제: {original_info.get('주요 화제', '')}
부차 화제: {original_info.get('부차 화제', '')}"""
        
        # 3. 공통 모듈을 사용한 최종 통합 분석
        synthesis_result = await self.content_analyzer.analyze_content(
            content=synthesis_content,
            title=node.title,
            context_type="synthesis"
        )
        
        # 4. _filled 파일 경로 확인 및 업데이트
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        node_type = "root" if node.is_root() else "internal"
        
        if node_type == "root":
            filled_file = self.output_dir / f"root_{safe_title}_info_filled.md"
        else:
            filled_file = self.output_dir / f"internal_level_{node.level}_{safe_title}_info_filled.md"
        
        if not filled_file.exists():
            return False
        
        # 5. 개선된 내용들을 파일에 업데이트
        success_count = 0
        final_sections = {}
        
        for section_name, content in synthesis_result.items():
            if content and not content.startswith("분석 실패") and len(content.strip()) > 0:
                if self.update_section(filled_file, section_name, content):
                    success_count += 1
                    final_sections[section_name] = content
        
        # 6. 상위 노드 변화 과정 기록 - 최종통합단계
        if node.title in self.change_tracking["upper_node_changes"]:
            self.change_tracking["upper_node_changes"][node.title]["최종통합_최종업데이트"] = final_sections
            self.change_tracking["upper_node_changes"][node.title]["최종통합_시간"] = time.time() - stage_start_time
            self.change_tracking["upper_node_changes"][node.title]["최종통합_성공"] = success_count >= 2
        
        stage_duration = time.time() - stage_start_time
        success = success_count >= 2
        
        self.logger.log_operation(f"최종통합완료_{node.title}", "성공" if success else "부분실패",
                                {"성공섹션": f"{success_count}/4",
                                 "소요시간": f"{stage_duration:.2f}초"}, stage_duration)
        
        return success

    async def parallel_task_with_logging(self, task_func, *args, task_name: str):
        """병렬 처리를 위한 작업 래퍼"""
        async with self.semaphore:
            return await task_func(*args)

    async def process_node_with_dialectical_synthesis(self, node: Node) -> bool:
        """정반합 방법론으로 단일 노드 처리 - 변화 과정 보고서 생성"""
        process_info = {
            "대상노드": node.title,
            "노드타입": node.get_node_type(),
            "자식노드수": len(node.children)
        }
        
        self.logger.log_process_start(process_info)
        start_time = time.time()
        
        try:
            # 1. 통합분석 단계
            gathered_info = await self.gather_and_analyze_stage(node)
            
            # 2. 개별개선 단계  
            updated_children = await self.improve_individual_stage(node, gathered_info)
            
            # 3. 최종통합 단계
            success = await self.final_integration_stage(node, updated_children, gathered_info)
            
            # 4. 변화 과정 보고서 생성
            await self.generate_change_reports(node)
            
            elapsed_time = time.time() - start_time
            summary = {
                "결과": "성공" if success else "실패",
                "소요시간": f"{elapsed_time:.2f}초",
                "변화과정보고서": "생성완료"
            }
            
            self.logger.log_process_end(success, summary)
            return success
            
        except Exception as e:
            self.logger.log_error(f"정반합처리_{node.title}", e)
            return False

    async def generate_change_reports(self, node: Node):
        """핵심 변화 과정 보고서 생성 - 상위 노드 및 하위 노드별"""
        try:
            # 1. 상위 노드 변화 과정 보고서
            upper_report = await self.create_upper_node_change_report(node)
            
            # 2. 하위 노드 변화 과정 보고서
            child_report = await self.create_child_nodes_change_report(node)
            
            self.logger.log_operation("변화과정보고서생성", "성공", {
                "상위노드보고서": upper_report.name,
                "하위노드보고서": child_report.name
            })
            
        except Exception as e:
            self.logger.log_error("변화과정보고서생성", e)

    async def create_upper_node_change_report(self, node: Node) -> Path:
        """상위 노드의 모든 변화 과정 보고서 생성"""
        report_path = self.output_dir / f"upper_node_changes_{node.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        if node.title not in self.change_tracking["upper_node_changes"]:
            # 빈 보고서 생성
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"# 상위 노드 변화 과정 보고서: {node.title}\n\n변화 과정 데이터 없음\n")
            return report_path
        
        change_data = self.change_tracking["upper_node_changes"][node.title]
        
        report_content = f"""# 상위 노드 변화 과정 보고서: {node.title}

## 개요
- **노드명**: {node.title}
- **파일명**: {change_data.get("파일명", "알 수 없음")}
- **보고서 생성**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 통합분석 단계 - 전체 대상 최초 추출 결과

### 핵심 내용
```
{change_data.get("통합분석_최초생성", {}).get("핵심 내용", "추출 실패")}
```

### 상세 핵심 내용
```
{change_data.get("통합분석_최초생성", {}).get("상세 핵심 내용", "추출 실패")}
```

### 주요 화제
```
{change_data.get("통합분석_최초생성", {}).get("주요 화제", "추출 실패")}
```

### 부차 화제
```
{change_data.get("통합분석_최초생성", {}).get("부차 화제", "추출 실패")}
```

## 최종통합 단계 - 최종 업데이트 결과

"""
        
        final_update = change_data.get("최종통합_최종업데이트", {})
        
        for section_name in ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]:
            content = final_update.get(section_name, "업데이트 실패")
            report_content += f"### {section_name}\n```\n{content}\n```\n\n"
        
        report_content += f"""## 변화 요약

- **통합분석 성공**: {'✅' if change_data.get("통합분석_성공", False) else '❌'}
- **통합분석 소요시간**: {change_data.get("통합분석_시간", 0):.2f}초
- **최종통합 성공**: {'✅' if change_data.get("최종통합_성공", False) else '❌'}
- **최종통합 소요시간**: {change_data.get("최종통합_시간", 0):.2f}초

---
*보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path

    async def create_child_nodes_change_report(self, node: Node) -> Path:
        """각 하위 노드의 모든 변화 과정 보고서 생성"""
        report_path = self.output_dir / f"child_nodes_changes_{node.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_content = f"""# 하위 노드들 변화 과정 보고서: {node.title}

## 개요
- **상위 노드**: {node.title}
- **처리 대상**: {len(self.change_tracking["child_node_changes"])}개 하위 노드
- **보고서 생성**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if not self.change_tracking["child_node_changes"]:
            report_content += "변화 과정 데이터가 없습니다.\n"
        else:
            for child_name, change_data in self.change_tracking["child_node_changes"].items():
                report_content += f"""## 하위 노드: {child_name}

### 파일 정보
- **파일명**: {change_data.get("파일명", "알 수 없음")}
- **변화된 섹션**: {", ".join(change_data.get("변화된섹션", []))}
- **보존된 섹션**: {", ".join(change_data.get("보존된섹션", []))}

### 변화 전 내용

"""
                
                before_data = change_data.get("개별개선_변화전", {})
                for section_name in ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]:
                    content = before_data.get(section_name, "내용 없음")
                    report_content += f"#### {section_name}\n```\n{content}\n```\n\n"
                
                report_content += "### 변화 후 내용\n\n"
                
                after_data = change_data.get("개별개선_변화후", {})
                for section_name in ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]:
                    content = after_data.get(section_name, "내용 없음")
                    
                    # 변화된 섹션인지 표시
                    if section_name in change_data.get("변화된섹션", []):
                        marker = " 🔄 **업데이트됨**"
                    elif section_name in change_data.get("보존된섹션", []):
                        marker = " 🔒 **보존됨**"
                    else:
                        marker = ""
                    
                    report_content += f"#### {section_name}{marker}\n```\n{content}\n```\n\n"
                
                report_content += "---\n\n"
        
        report_content += f"""## 전체 요약

- **총 처리 노드**: {len(self.change_tracking["child_node_changes"])}개
- **변화된 노드**: {sum(1 for data in self.change_tracking["child_node_changes"].values() if data.get("변화된섹션"))}개
- **보존 정책**: 주요/부차 화제는 기존 내용 유지, 핵심/상세 내용만 개선

---
*보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path

    # 유틸리티 메서드들
    def _extract_all_sections(self, content: str) -> Dict[str, str]:
        """파일에서 모든 섹션 내용 추출"""
        sections = {}
        section_names = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        
        for section_name in section_names:
            sections[section_name] = self._extract_section_content(content, section_name)
        
        return sections
    
    def _extract_section_content(self, content: str, section: str) -> str:
        """특정 섹션의 내용만 추출"""
        header_pattern = f"## {section}"
        header_start = content.find(header_pattern)
        
        if header_start == -1:
            return ""
        
        content_start = header_start + len(header_pattern)
        next_header_start = content.find("\n## ", content_start)
        
        if next_header_start == -1:
            section_content = content[content_start:].strip()
        else:
            section_content = content[content_start:next_header_start].strip()
        
        return section_content

    def create_node_info_file(self, node: Node, node_type: str) -> Path:
        """노드 정보 파일 생성"""
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        if node_type == "root":
            info_file_path = self.output_dir / f"root_{safe_title}_info.md"
        else:
            info_file_path = self.output_dir / f"internal_level_{node.level}_{safe_title}_info.md"
        
        template = """# 추가 정보

## 핵심 내용

## 상세 핵심 내용

## 주요 화제

## 부차 화제
"""
        
        with open(info_file_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        return info_file_path
    
    def combine_children_content(self, node: Node) -> str:
        """자식 노드들의 내용을 하나로 결합"""
        combined_content = f"# {node.title} 모든 구성 요소의 내용 결합\n\n"
        
        for child in node.children:
            if child.is_leaf():
                safe_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                leaf_file = self.output_dir / f"leaf_{safe_title}_info_filled.md"
                
                if leaf_file.exists():
                    with open(leaf_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    combined_content += f"## ========== {child.title} ==========\n\n"
                    combined_content += content + "\n\n"
                    combined_content += "=" * 100 + "\n\n"
            else:
                internal_content = self._collect_internal_content(child)
                combined_content += f"## ========== {child.title} (내부 노드) ==========\n\n"
                combined_content += internal_content + "\n\n"
                combined_content += "=" * 100 + "\n\n"
        
        return combined_content
    
    def _collect_internal_content(self, internal_node: Node) -> str:
        """내부 노드의 모든 리프 자식들 내용 수집"""
        content = ""
        for child in internal_node.children:
            if child.is_leaf():
                safe_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                leaf_file = self.output_dir / f"leaf_{safe_title}_info_filled.md"
                
                if leaf_file.exists():
                    with open(leaf_file, 'r', encoding='utf-8') as f:
                        leaf_content = f.read()
                    content += f"### {child.title}\n{leaf_content}\n\n"
            else:
                content += self._collect_internal_content(child)
        return content

    def update_section(self, file_path: Path, header: str, content: str) -> bool:
        """파일의 특정 헤더 섹션에 내용 업데이트"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            header_pattern = f"## {header}"
            header_start = text.find(header_pattern)
            
            if header_start == -1:
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
        except:
            return False

    def preserve_original_topics(self, file_path: Path) -> tuple:
        """기존 주요 화제와 부차 화제를 추출하여 보존"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            main_topics = self._extract_section_content(content, "주요 화제")
            sub_topics = self._extract_section_content(content, "부차 화제")
            
            return main_topics, sub_topics
        except:
            return "", ""
        
    def rename_to_filled(self, info_file_path: Path, node_type: str, node: Node) -> Path:
        """정보 파일명을 _filled 접미사로 변경"""
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        if node_type == "root":
            filled_path = self.output_dir / f"root_{safe_title}_info_filled.md"
        else:
            filled_path = self.output_dir / f"internal_level_{node.level}_{safe_title}_info_filled.md"
        
        if info_file_path.exists():
            info_file_path.rename(filled_path)
            return filled_path
        return info_file_path


async def main():
    """테스트 실행"""
    from node_structure_analyzer import NodeStructureAnalyzer
    
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12"
    
    print("=" * 60)
    print("정반합 방법론 시스템 V2 - 핵심 변화 과정 보고서")
    print("=" * 60)
    
    # 노드 구조 분석
    analyzer = NodeStructureAnalyzer(json_path, "")
    if not analyzer.load_json_structure():
        return
    
    # 루트 노드 찾기
    root_nodes = [node for node in analyzer.nodes.values() if node.is_root()]
    if not root_nodes:
        print("❌ 루트 노드를 찾을 수 없습니다")
        return
    
    root_node = root_nodes[0]
    print(f"🎯 처리 대상: {root_node.title}")
    
    # 정반합 프로세서 생성 및 실행
    processor = DialecticalSynthesisProcessor(output_dir)
    success = await processor.process_node_with_dialectical_synthesis(root_node)
    
    print(f"\n🎯 최종 결과: {'성공' if success else '실패'}")
    print("📊 생성된 변화 과정 보고서:")
    
    # 생성된 보고서 파일 확인
    output_path = Path(output_dir)
    change_reports = list(output_path.glob("*changes*.md"))
    
    for report_file in change_reports:
        print(f"  - {report_file.name}")


if __name__ == "__main__":
    asyncio.run(main())