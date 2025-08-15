"""
생성 시간: 2025-08-14 14:29:39 KST (수정: 2025-08-14 19:25:10 KST)
핵심 내용: 정반합 방법론 V6 - DataLoader 경로 수정 및 로깅 시스템 V2 적용
상세 내용:
    - DataLoader 클래스 (라인 26-): 목적별 분리 (추출/업데이트 전용), node_docs_dir 기반
    - DataProcessor 클래스 (라인 179-): 3단계 처리 로직 분리
    - DataSaver 클래스 (라인 344-): 결과 저장 및 status 관리
    - DialecticalSynthesisProcessor 클래스 (라인 482-): 올바른 노드 파일 경로 설정
    - 핵심 수정: DataLoader가 node_docs_dir를 base_dir로 사용하여 실제 노드 파일 접근
    - 로깅 시스템 V2 적용으로 테스트 전용 확장 로깅 지원
    - main() 함수 매개변수명 변경: output_dir → node_docs_dir
상태: 활성
주소: dialectical_synthesis_processor_v6/fixed
참조: dialectical_synthesis_processor_v5.py, logging_system_v2.py
"""

import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any

from node_grouper import NodeGrouper
from content_analysis_module import ContentAnalyzer
from logging_system_v2 import ProcessLogger


class DataLoader:
    """목적별로 분리된 노드 정보 로딩 클래스"""
    
    def __init__(self, base_dir: Path, logger: ProcessLogger):
        self.base_dir = base_dir
        self.logger = logger
    
    def load_for_extraction(self, node_data: Dict[str, Any]) -> str:
        """추출 전용: 내용 섹션 + 구성 파일들의 내용 섹션 결합"""
        try:
            node_title = node_data.get("title", "")
            
            # 노드 정보 파일 경로
            node_file_path = self._get_node_file_path(node_data)
            if not node_file_path.exists():
                self.logger.log_error(f"노드파일없음_{node_title}", f"파일 없음: {node_file_path}")
                return ""
            
            # 1. 현재 노드의 내용 섹션 추출
            current_content = self._extract_section_from_file(node_file_path, "내용")
            
            # 2. 구성 파일들의 내용 섹션 수집
            composition_files = self._get_composition_files(node_file_path)
            composition_contents = []
            
            for file_name in composition_files:
                comp_file_path = self.base_dir / file_name
                if comp_file_path.exists():
                    comp_content = self._extract_section_from_file(comp_file_path, "내용")
                    if comp_content.strip():
                        composition_contents.append(f"=== {file_name} 내용 ===\n{comp_content}")
            
            # 3. 통합 텍스트 생성
            combined_content = ""
            
            # 현재 노드 내용이 있으면 추가
            if current_content.strip():
                combined_content += f"# {node_title} - 현재 노드 내용\n{current_content}\n\n"
            
            # 구성 파일들 내용 추가
            if composition_contents:
                combined_content += f"# {node_title} - 구성 요소들 내용\n\n"
                combined_content += "\n\n".join(composition_contents)
            
            # 둘 다 없으면 빈 문자열
            if not combined_content.strip():
                self.logger.log_operation(f"추출데이터로딩_{node_title}", "경고", 
                                        {"타입": "내용없음", "현재내용": len(current_content), 
                                         "구성파일수": len(composition_files)})
                return ""
            
            self.logger.log_operation(f"추출데이터로딩_{node_title}", "성공", 
                                    {"타입": "내용+구성결합", "현재내용": len(current_content),
                                     "구성파일수": len(composition_files), "총텍스트길이": len(combined_content)})
            return combined_content
            
        except Exception as e:
            self.logger.log_error(f"추출데이터로딩_{node_data.get('title', '')}", e)
            return ""
    
    def load_for_update(self, node_data: Dict[str, Any]) -> str:
        """업데이트 전용: 내용 + 자식들의 추출 섹션 결합"""
        try:
            node_title = node_data.get("title", "")
            
            # 노드 정보 파일 경로
            node_file_path = self._get_node_file_path(node_data)
            if not node_file_path.exists():
                self.logger.log_error(f"노드파일없음_{node_title}", f"파일 없음: {node_file_path}")
                return ""
            
            # 1. 현재 노드의 내용 섹션
            current_content = self._extract_section_from_file(node_file_path, "내용")
            
            # 2. 자식 노드들의 추출 섹션 수집
            composition_extractions = self.load_composition_extractions(node_data)
            
            # 3. 결합
            combined_text = self._combine_for_update(current_content, composition_extractions, node_title)
            
            self.logger.log_operation(f"업데이트데이터로딩_{node_title}", "성공", 
                                    {"타입": "내용+자식추출", "자식수": len(composition_extractions), 
                                     "텍스트길이": len(combined_text)})
            return combined_text
            
        except Exception as e:
            self.logger.log_error(f"업데이트데이터로딩_{node_data.get('title', '')}", e)
            return ""
    
    def load_composition_extractions(self, node_data: Dict[str, Any]) -> List[str]:
        """구성 파일들의 추출 섹션만 수집"""
        try:
            node_file_path = self._get_node_file_path(node_data)
            composition_files = self._get_composition_files(node_file_path)
            
            extractions = []
            for file_name in composition_files:
                file_path = self.base_dir / file_name
                if file_path.exists():
                    extraction = self._extract_section_from_file(file_path, "추출")
                    if extraction:
                        extractions.append(f"=== {file_name} ===\n{extraction}")
            
            return extractions
            
        except Exception as e:
            self.logger.log_error(f"구성추출로딩_{node_data.get('title', '')}", e)
            return []
    
    def get_composition_files(self, node_data: Dict[str, Any]) -> List[str]:
        """구성 섹션에서 파일 목록 추출"""
        try:
            node_file_path = self._get_node_file_path(node_data)
            return self._get_composition_files(node_file_path)
        except Exception:
            return []
    
    def _get_node_file_path(self, node_data: Dict[str, Any]) -> Path:
        """노드 정보 파일 경로 생성 - 실제 파일명 규칙에 맞춤"""
        node_id = node_data.get("id", 0)
        level = node_data.get("level", 0)
        title = node_data.get("title", "")
        # 실제 파일명: 소문자, 공백은 언더스코어, 하이픈 유지
        safe_title = title.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
        safe_title = safe_title.replace("-", "_")  # 하이픈도 언더스코어로 변경
        return self.base_dir / f"{node_id:02d}_lev{level}_{safe_title}_info.md"
    
    def _extract_section_from_file(self, file_path: Path, section_name: str) -> str:
        """파일에서 특정 섹션 내용 추출 - 하위 헤더 포함"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            header_pattern = f"# {section_name}"
            header_start = content.find(header_pattern)
            
            if header_start == -1:
                return ""
            
            content_start = header_start + len(header_pattern)
            
            # 다음 메인 섹션 헤더를 찾기 (같은 레벨의 헤더만)
            # 줄 시작에서 시작하는 "# " 패턴을 찾아야 함
            lines = content[content_start:].split('\n')
            section_lines = []
            
            for line in lines:
                # 줄 시작에서 "# "로 시작하는 것은 메인 섹션 헤더
                if line.strip().startswith('# ') and not line.strip().startswith('##'):
                    break
                section_lines.append(line)
            
            section_content = '\n'.join(section_lines).strip()
            return section_content
            
        except Exception as e:
            self.logger.log_error(f"섹션추출_{file_path.name}", e)
            return ""
    
    def _get_composition_files(self, node_file_path: Path) -> List[str]:
        """구성 섹션에서 파일 목록 추출"""
        try:
            composition_content = self._extract_section_from_file(node_file_path, "구성")
            if not composition_content:
                return []
            
            files = []
            for line in composition_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and line.endswith('.md'):
                    files.append(line)
            
            return files
            
        except Exception:
            return []
    
    def _combine_for_update(self, current_content: str, composition_extractions: List[str], node_title: str) -> str:
        """업데이트용 데이터 결합"""
        combined = f"# {node_title} - 업데이트용 통합\n\n"
        
        if current_content:
            combined += f"## 현재 노드 내용\n{current_content}\n\n"
        
        if composition_extractions:
            combined += "## 자식 노드들 추출 정보\n\n"
            for extraction in composition_extractions:
                combined += f"{extraction}\n\n"
        
        return combined


class DataProcessor:
    """3단계 처리 로직을 분리한 데이터 가공 클래스"""
    
    def __init__(self, content_analyzer: ContentAnalyzer, logger: ProcessLogger):
        self.content_analyzer = content_analyzer
        self.logger = logger
        # 병렬처리 제한: 최대 2개 동시 실행으로 안정성 확보
        self.semaphore = asyncio.Semaphore(2)
        self._active_tasks = set()  # 활성 태스크 추적
    
    async def process_content_extraction(self, content: str, node_title: str) -> Dict[str, str]:
        """순수 추출 작업: 4가지 정보 추출 (리프/부모 공통) - 자원 관리 포함"""
        async with self.semaphore:  # 세마포어로 동시 실행 제한
            process_start = time.time()
            task_id = f"extract_{node_title}_{id(asyncio.current_task())}"
            
            try:
                # 활성 태스크 등록
                self._active_tasks.add(task_id)
                self.logger.log_operation(f"내용추출시작_{node_title}", "시작", 
                                        {"활성태스크수": len(self._active_tasks)})
                
                result = await self.content_analyzer.analyze_content(
                    content=content,
                    title=node_title,
                    context_type="combined"
                )
                
                extracted_data = {}
                section_names = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
                
                for section_name in section_names:
                    content_result = result.get(section_name, "")
                    if content_result and not content_result.startswith("분석 실패") and len(content_result.strip()) > 0:
                        extracted_data[section_name] = content_result
                    else:
                        extracted_data[section_name] = "추출 실패"
                
                process_time = time.time() - process_start
                success_count = len([v for v in extracted_data.values() if v != "추출 실패"])
                
                self.logger.log_operation(f"내용추출완료_{node_title}", "완료", 
                                        {"처리시간": f"{process_time:.2f}초", "성공섹션": f"{success_count}/4"})
                
                return extracted_data
                
            except Exception as e:
                self.logger.log_error(f"내용추출_{node_title}", e)
                return {
                    "핵심 내용": "추출 실패",
                    "상세 핵심 내용": "추출 실패", 
                    "주요 화제": "추출 실패",
                    "부차 화제": "추출 실패"
                }
            finally:
                # 자원 정리: 태스크 제거
                self._active_tasks.discard(task_id)
                remaining_tasks = len(self._active_tasks)
                if remaining_tasks > 0:
                    self.logger.log_operation(f"자원정리_{node_title}", "완료", 
                                            {"남은태스크수": remaining_tasks})
    
    async def update_composition_nodes(self, reference_info: Dict[str, str], 
                                     composition_files: List[str], 
                                     base_dir: Path) -> Dict[str, Dict[str, str]]:
        """자식 노드들 업데이트 (부모 추출 정보 기반)"""
        update_results = {}
        
        for file_name in composition_files:
            file_path = base_dir / file_name
            if file_path.exists():
                updated_data = await self._update_single_composition_node(file_path, reference_info)
                update_results[file_name] = updated_data
            else:
                update_results[file_name] = {}
        
        return update_results
    
    async def process_synthesis_update(self, combined_content: str, 
                                     updated_children: Dict[str, Dict[str, str]], 
                                     original_info: Dict[str, str],
                                     node_title: str) -> Dict[str, str]:
        """최종 통합 업데이트 (업데이트된 자식 정보 반영)"""
        try:
            # 업데이트된 자식 노드들의 내용을 결합
            updated_combined_content = self._combine_updated_composition_content(updated_children)
            
            # 통합 분석용 컨텍스트 생성
            synthesis_content = f"""업데이트된 자식 요소들:
{updated_combined_content}

현재 노드 내용과 기존 추출 정보:
{combined_content}

기존 상위 정보:
핵심 내용: {original_info.get('핵심 내용', '')}
상세 핵심 내용: {original_info.get('상세 핵심 내용', '')}
주요 화제: {original_info.get('주요 화제', '')}
부차 화제: {original_info.get('부차 화제', '')}"""
            
            # 최종 통합 분석
            updated_info = await self.content_analyzer.analyze_content(
                content=synthesis_content,
                title=node_title,
                context_type="synthesis"
            )
            
            self.logger.log_operation(f"통합업데이트_{node_title}", "완료")
            return updated_info
            
        except Exception as e:
            self.logger.log_error(f"통합업데이트_{node_title}", e)
            return {}
    
    async def _update_single_composition_node(self, file_path: Path, reference_info: Dict[str, str]) -> Dict[str, str]:
        """단일 자식 노드 갱신"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            current_extraction = self._extract_section_content(original_content, "추출")
            
            enhancement_content = f"""기존 정보:
{current_extraction}

전체 정보 (보완용):
핵심 내용: {reference_info.get('핵심 내용', '')}
상세 핵심 내용: {reference_info.get('상세 핵심 내용', '')}
주요 화제: {reference_info.get('주요 화제', '')}
부차 화제: {reference_info.get('부차 화제', '')}"""
            
            updated_info = await self.content_analyzer.analyze_content(
                content=enhancement_content,
                title=file_path.stem,
                context_type="enhancement"
            )
            
            self.logger.log_operation(f"자식노드갱신_{file_path.name}", "완료")
            return updated_info
            
        except Exception as e:
            self.logger.log_error(f"자식노드갱신_{file_path.name}", e)
            return {}
    
    def _extract_section_content(self, content: str, section: str) -> str:
        """특정 섹션의 내용만 추출"""
        header_pattern = f"# {section}"
        header_start = content.find(header_pattern)
        
        if header_start == -1:
            return ""
        
        content_start = header_start + len(header_pattern)
        next_header_start = content.find("\n# ", content_start)
        
        if next_header_start == -1:
            section_content = content[content_start:].strip()
        else:
            section_content = content[content_start:next_header_start].strip()
        
        return section_content
    
    def _combine_updated_composition_content(self, updated_composition_data: Dict[str, Dict[str, str]]) -> str:
        """업데이트된 자식 요소들의 내용 결합"""
        combined = ""
        
        for file_name, data in updated_composition_data.items():
            if data:
                combined += f"## ========== {file_name} ==========\n\n"
                
                for section_name in ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]:
                    content = data.get(section_name, "")
                    if content and content != "추출 실패":
                        combined += f"### {section_name}\n{content}\n\n"
                
                combined += "=" * 100 + "\n\n"
        
        return combined


class DataSaver:
    """결과 저장 및 status 관리 클래스"""
    
    def __init__(self, base_dir: Path, logger: ProcessLogger):
        self.base_dir = base_dir
        self.logger = logger
    
    def save_to_extraction_section(self, file_path: Path, data: Dict[str, str]) -> bool:
        """추출 영역에 결과 저장"""
        try:
            if not file_path.exists():
                self._create_basic_node_file(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extraction_start = content.find("# 추출")
            if extraction_start == -1:
                content += "\n\n# 추출\n\n"
                extraction_start = content.find("# 추출")
            
            extraction_content = self._build_extraction_content(data)
            
            next_section_start = content.find("\n# ", extraction_start + 4)
            
            if next_section_start == -1:
                new_content = content[:extraction_start] + f"# 추출\n\n{extraction_content}\n"
            else:
                new_content = content[:extraction_start] + f"# 추출\n\n{extraction_content}\n" + content[next_section_start:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            success_sections = len([v for v in data.values() if v and v != "추출 실패"])
            self.logger.log_operation(f"저장완료_{file_path.name}", "성공", {"성공섹션": success_sections})
            return True
            
        except Exception as e:
            self.logger.log_error(f"저장실패_{file_path.name}", e)
            return False
    
    def update_node_status(self, file_path: Path, status: bool) -> bool:
        """노드 정보 파일의 process_status 필드 업데이트"""
        try:
            if not file_path.exists():
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 속성 섹션에서 process_status 찾기/업데이트
            status_pattern = "process_status:"
            status_start = content.find(status_pattern)
            
            if status_start == -1:
                # process_status가 없으면 속성 섹션에 추가
                attr_start = content.find("# 속성")
                if attr_start != -1:
                    attr_end = content.find("\n# ", attr_start + 4)
                    if attr_end == -1:
                        # 속성이 마지막 섹션
                        new_content = content + f"\nprocess_status: {str(status).lower()}\n"
                    else:
                        # 속성 섹션 끝에 추가
                        new_content = content[:attr_end] + f"\nprocess_status: {str(status).lower()}\n" + content[attr_end:]
                else:
                    # 속성 섹션이 없으면 파일 시작에 추가
                    new_content = f"# 속성\nprocess_status: {str(status).lower()}\n\n{content}"
            else:
                # 기존 process_status 값 업데이트
                line_end = content.find('\n', status_start)
                if line_end == -1:
                    line_end = len(content)
                
                new_content = content[:status_start] + f"process_status: {str(status).lower()}" + content[line_end:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.log_operation(f"상태업데이트_{file_path.name}", "성공", {"status": str(status).lower()})
            return True
            
        except Exception as e:
            self.logger.log_error(f"상태업데이트_{file_path.name}", e)
            return False
    
    def check_node_status(self, file_path: Path) -> bool:
        """노드의 process_status 확인"""
        try:
            if not file_path.exists():
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            status_pattern = "process_status:"
            status_start = content.find(status_pattern)
            
            if status_start == -1:
                return False
            
            line_end = content.find('\n', status_start)
            if line_end == -1:
                line_end = len(content)
            
            status_line = content[status_start:line_end]
            return "true" in status_line.lower()
            
        except Exception:
            return False
    
    def _create_basic_node_file(self, file_path: Path):
        """기본 노드 정보 파일 구조 생성"""
        template = """# 속성
process_status: false

# 추출

# 내용

# 구성
"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
    
    def _build_extraction_content(self, data: Dict[str, str]) -> str:
        """추출 섹션 내용 구성"""
        content = ""
        
        section_order = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        
        for section_name in section_order:
            if section_name in data and data[section_name] and data[section_name] != "추출 실패":
                content += f"## {section_name}\n{data[section_name]}\n\n"
        
        return content.strip()


class DialecticalSynthesisProcessor:
    """정반합 방법론 메인 처리 클래스 V6 - 의존성 기반 레벨별 처리"""
    
    def __init__(self, node_docs_dir: str):
        self.node_docs_dir = Path(node_docs_dir)  # 실제 노드 파일들이 있는 디렉토리
        self.node_docs_dir.mkdir(exist_ok=True)
        
        # 로그 출력용 디렉토리 (node_docs_dir의 부모 디렉토리)
        self.output_dir = self.node_docs_dir.parent
        
        # 공통 모듈 초기화
        self.logger = ProcessLogger("dialectical_synthesis_v6", self.output_dir)
        self.content_analyzer = ContentAnalyzer(self.logger.logger)
        
        # 전담 클래스들 초기화 - DataLoader는 실제 노드 파일 디렉토리 사용
        self.data_loader = DataLoader(self.node_docs_dir, self.logger)
        self.data_processor = DataProcessor(self.content_analyzer, self.logger)
        self.data_saver = DataSaver(self.node_docs_dir, self.logger)
        self.node_grouper = NodeGrouper(self.logger)
        
        # 처리 결과 추적
        self.processing_results = {}
    
    async def process_nodes_from_json(self, json_path: str) -> Dict[str, Any]:
        """JSON 파일에서 노드를 로드하여 의존성 기반 배치 처리"""
        # JSON 로드
        if not self.node_grouper.load_nodes_from_json(json_path):
            self.logger.log_error("JSON로드", f"실패: {json_path}")
            return {}
        
        return await self.process_nodes_with_dependencies(self.node_grouper.nodes_data)
    
    async def process_nodes_with_dependencies(self, nodes_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """의존성 기반 노드 처리 - 레벨별 순차, 레벨 내 의존성 고려"""
        batch_start = time.time()
        self.logger.log_operation("의존성처리시작", "시작", {"총노드수": len(nodes_data)})
        
        # 1. 레벨별 노드 분류 (리프/부모 분리)
        level_categories = self.categorize_nodes_by_level(nodes_data)
        
        # 2. 높은 레벨(하위)부터 순차 처리
        total_results = {}
        for level in sorted(level_categories.keys(), reverse=True):
            category = level_categories[level]
            
            self.logger.log_operation(f"레벨{level}처리시작", "시작", 
                                    {"리프노드": len(category["leaf_nodes"]), 
                                     "부모노드": len(category["parent_nodes"])})
            
            # 레벨별 처리
            level_success = await self.process_level_with_dependencies(level, category)
            
            if not level_success:
                self.logger.log_error(f"레벨{level}처리", "실패 - 상위 레벨 처리 중단")
                break
            
            # 결과 수집
            total_results.update(self.collect_level_results(category))
        
        batch_time = time.time() - batch_start
        success_count = sum(1 for r in total_results.values() if r)
        
        self.logger.log_operation("의존성처리완료", "완료", 
                                {"처리시간": f"{batch_time:.2f}초", 
                                 "성공노드": f"{success_count}/{len(total_results)}"})
        
        return total_results
    
    def categorize_nodes_by_level(self, nodes_data: List[Dict[str, Any]]) -> Dict[int, Dict[str, List[Dict[str, Any]]]]:
        """레벨별로 노드를 리프/부모로 분류"""
        level_categories = {}
        
        for node in nodes_data:
            level = node.get("level", 0)
            if level not in level_categories:
                level_categories[level] = {"leaf_nodes": [], "parent_nodes": []}
            
            children_ids = node.get("children_ids", [])
            if children_ids and len(children_ids) > 0:
                level_categories[level]["parent_nodes"].append(node)
            else:
                level_categories[level]["leaf_nodes"].append(node)
        
        return level_categories
    
    async def process_level_with_dependencies(self, level: int, category: Dict[str, List[Dict[str, Any]]]) -> bool:
        """레벨 내 의존성 기반 처리"""
        
        # 1단계: 모든 리프 노드 처리 (병렬 가능)
        if category["leaf_nodes"]:
            leaf_results = await self.process_all_leaf_nodes(category["leaf_nodes"])
            
            # 리프 노드 완료 검증
            if not self.verify_nodes_completion(category["leaf_nodes"]):
                self.logger.log_error(f"레벨{level}_리프노드", "완료 검증 실패")
                return False
        
        # 2단계: 부모 노드들 처리 (이제 자식들의 추출 섹션 존재)
        if category["parent_nodes"]:
            parent_results = await self.process_all_parent_nodes(category["parent_nodes"])
            
            # 부모 노드 완료 검증
            if not self.verify_nodes_completion(category["parent_nodes"]):
                self.logger.log_error(f"레벨{level}_부모노드", "완료 검증 실패")
                return False
        
        self.logger.log_operation(f"레벨{level}처리완료", "성공")
        return True
    
    async def process_all_leaf_nodes(self, leaf_nodes: List[Dict[str, Any]]) -> Dict[str, bool]:
        """모든 리프 노드 처리 (제한된 병렬) - 자원 관리 강화"""
        results = {}
        total_nodes = len(leaf_nodes)
        
        self.logger.log_operation("리프노드병렬처리시작", "시작", 
                                {"총노드수": total_nodes, "최대동시실행": 2})
        
        # 배치별 처리 (최대 2개씩)
        batch_size = 2
        for i in range(0, total_nodes, batch_size):
            batch = leaf_nodes[i:i + batch_size]
            batch_start = time.time()
            
            # 배치 내 병렬 처리
            tasks = []
            for node_data in batch:
                task = self.process_leaf_node_pipeline(node_data)
                tasks.append(task)
            
            try:
                # 배치 실행 및 결과 수집
                task_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for j, result in enumerate(task_results):
                    node_title = batch[j].get("title", "")
                    if isinstance(result, Exception):
                        self.logger.log_error(f"리프노드병렬_{node_title}", result)
                        results[node_title] = False
                    else:
                        results[node_title] = result
                
                batch_time = time.time() - batch_start
                batch_num = (i // batch_size) + 1
                self.logger.log_operation(f"배치{batch_num}완료", "완료", 
                                        {"소요시간": f"{batch_time:.2f}초", "노드수": len(batch)})
                
                # 배치 간 잠시 대기 (메모리 정리)
                if i + batch_size < total_nodes:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                self.logger.log_error(f"배치{(i // batch_size) + 1}처리", e)
                # 배치 실패 시 해당 노드들 실패 처리
                for node_data in batch:
                    results[node_data.get("title", "")] = False
        
        success_count = sum(1 for success in results.values() if success)
        self.logger.log_operation("리프노드병렬처리완료", "완료", 
                                {"성공": f"{success_count}/{total_nodes}"})
        
        return results
    
    async def process_all_parent_nodes(self, parent_nodes: List[Dict[str, Any]]) -> Dict[str, bool]:
        """모든 부모 노드 처리 (순차 - 자식 의존성 때문)"""
        results = {}
        
        for node_data in parent_nodes:
            node_title = node_data.get("title", "")
            result = await self.process_parent_node_pipeline(node_data)
            results[node_title] = result
        
        return results
    
    async def process_leaf_node_pipeline(self, node_data: Dict[str, Any]) -> bool:
        """리프 노드 파이프라인: 추출 → 저장 → status 업데이트"""
        node_start = time.time()
        node_title = node_data.get("title", "")
        
        self.logger.log_operation(f"리프파이프라인시작_{node_title}", "시작")
        
        try:
            # 1. 추출 작업 (내용 섹션만)
            extraction_data = self.data_loader.load_for_extraction(node_data)
            if not extraction_data:
                return False
            
            extracted_info = await self.data_processor.process_content_extraction(extraction_data, node_title)
            
            # 2. 저장
            node_file_path = self.data_loader._get_node_file_path(node_data)
            save_success = self.data_saver.save_to_extraction_section(node_file_path, extracted_info)
            
            # 3. status 업데이트
            if save_success:
                status_success = self.data_saver.update_node_status(node_file_path, True)
                
                node_time = time.time() - node_start
                self.logger.log_operation(f"리프파이프라인완료_{node_title}", 
                                        "성공" if status_success else "저장성공_상태실패", 
                                        {"처리시간": f"{node_time:.2f}초"})
                return status_success
            
            return False
            
        except Exception as e:
            self.logger.log_error(f"리프파이프라인오류_{node_title}", e)
            return False
    
    async def process_parent_node_pipeline(self, node_data: Dict[str, Any]) -> bool:
        """부모 노드 3단계 파이프라인"""
        node_start = time.time()
        node_title = node_data.get("title", "")
        
        self.logger.log_operation(f"부모파이프라인시작_{node_title}", "시작")
        
        try:
            # 1단계: 부모 노드 추출 (내용 섹션만) - 비어있어도 진행
            extraction_data = self.data_loader.load_for_extraction(node_data)
            
            if extraction_data.strip():
                # 내용이 있으면 추출 수행
                parent_extracted = await self.data_processor.process_content_extraction(extraction_data, node_title)
            else:
                # 내용이 없으면 빈 추출 정보로 진행 (자식 노드 종합용 부모 노드)
                self.logger.log_operation(f"부모노드빈내용_{node_title}", "진행", 
                                        {"자식노드종합": "예정"})
                parent_extracted = {
                    "핵심 내용": "",
                    "상세 핵심 내용": "",
                    "주요 화제": "",
                    "부차 화제": ""
                }
            
            # 2단계: 자식 노드들 업데이트 (부모 추출 정보 기반)
            composition_files = self.data_loader.get_composition_files(node_data)
            updated_children = await self.data_processor.update_composition_nodes(
                parent_extracted, composition_files, self.node_docs_dir
            )
            
            # 자식 노드들 저장
            children_save_success = await self.save_updated_children(updated_children)
            
            # 3단계: 부모 노드 최종 업데이트 (업데이트된 자식 정보 반영)
            update_data = self.data_loader.load_for_update(node_data)
            final_extracted = await self.data_processor.process_synthesis_update(
                update_data, updated_children, parent_extracted, node_title
            )
            
            # 4. 부모 노드 저장 및 status 업데이트
            node_file_path = self.data_loader._get_node_file_path(node_data)
            save_success = self.data_saver.save_to_extraction_section(node_file_path, final_extracted)
            
            if save_success:
                status_success = self.data_saver.update_node_status(node_file_path, True)
                
                node_time = time.time() - node_start
                self.logger.log_operation(f"부모파이프라인완료_{node_title}", 
                                        "성공" if status_success else "저장성공_상태실패", 
                                        {"처리시간": f"{node_time:.2f}초", 
                                         "자식저장": "성공" if children_save_success else "실패"})
                return status_success
            
            return False
            
        except Exception as e:
            self.logger.log_error(f"부모파이프라인오류_{node_title}", e)
            return False
    
    async def save_updated_children(self, updated_children: Dict[str, Dict[str, str]]) -> bool:
        """업데이트된 자식 노드들 저장"""
        success_count = 0
        
        for file_name, comp_data in updated_children.items():
            if comp_data:
                comp_file_path = self.node_docs_dir / file_name
                if self.data_saver.save_to_extraction_section(comp_file_path, comp_data):
                    success_count += 1
        
        return success_count == len([data for data in updated_children.values() if data])
    
    def verify_nodes_completion(self, nodes: List[Dict[str, Any]]) -> bool:
        """노드들의 완료 상태 검증 (process_status가 true인지 확인)"""
        for node_data in nodes:
            node_file_path = self.data_loader._get_node_file_path(node_data)
            if not self.data_saver.check_node_status(node_file_path):
                node_title = node_data.get("title", "")
                self.logger.log_error(f"노드완료검증_{node_title}", "status가 true가 아님")
                return False
        
        return True
    
    def collect_level_results(self, category: Dict[str, List[Dict[str, Any]]]) -> Dict[str, bool]:
        """레벨별 결과 수집"""
        results = {}
        
        for node_data in category["leaf_nodes"] + category["parent_nodes"]:
            node_title = node_data.get("title", "")
            node_file_path = self.data_loader._get_node_file_path(node_data)
            results[node_title] = self.data_saver.check_node_status(node_file_path)
        
        return results


async def main():
    """테스트 실행"""
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/nodes.json"
    node_docs_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/node_docs"
    
    print("=" * 60)
    print("정반합 방법론 시스템 V6 - 의존성 기반 처리 및 모듈화된 DataLoader")
    print("=" * 60)
    
    # 정반합 프로세서 생성 및 실행 - 노드 파일이 있는 디렉토리 전달
    processor = DialecticalSynthesisProcessor(node_docs_dir)
    results = await processor.process_nodes_from_json(json_path)
    
    print(f"\n🎯 최종 결과:")
    success_count = sum(1 for success in results.values() if success)
    print(f"  - 성공: {success_count}/{len(results)}")
    print(f"  - 실패: {len(results) - success_count}/{len(results)}")
    
    if results:
        print(f"\n📋 처리된 노드들:")
        for node_title, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {node_title}")


if __name__ == "__main__":
    asyncio.run(main())