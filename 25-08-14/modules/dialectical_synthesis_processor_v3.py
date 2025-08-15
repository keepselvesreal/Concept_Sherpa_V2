"""
생성 시간: 2025-08-13 15:18:03 KST
핵심 내용: 정반합 방법론 V3 - 재구조화된 데이터 처리 파이프라인
상세 내용:
    - DataLoader 클래스 (라인 35-): 노드 정보 파일 로딩 및 텍스트 추출 전담
    - DataProcessor 클래스 (라인 180-): 데이터 가공 및 갱신 작업 분리 (기존 Claude SDK 프롬프트 사용)
    - DataSaver 클래스 (라인 320-): 결과 저장 전담
    - NodeGrouper 클래스 (라인 380-): 노드 그룹화 및 정렬 로직
    - DialecticalSynthesisProcessor 클래스 (라인 450-): 메인 처리 로직 조직화
    - 파일명 형식: level_node title_info.md (node 접두사 제거)
상태: 활성
주소: dialectical_synthesis_processor_v3
참조: dialectical_synthesis_processor_v2.py (이전 버전)
"""

import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any

from node_structure_analyzer import Node
from content_analysis_module import ContentAnalyzer
from logging_system import ProcessLogger


class DataLoader:
    """노드 정보 파일 로딩 및 텍스트 추출 전담 클래스"""
    
    def __init__(self, base_dir: Path, logger: ProcessLogger):
        self.base_dir = base_dir
        self.logger = logger
    
    def load_node_content_data(self, node: Node) -> str:
        """gather_and_analyze_stage용: 내용 영역 데이터 로딩"""
        try:
            # 1. 노드 정보 파일 경로
            node_file_path = self._get_node_file_path(node)
            if not node_file_path.exists():
                self.logger.log_error(f"노드파일없음_{node.title}", f"파일 없음: {node_file_path}")
                return ""
            
            # 2. 현재 파일의 내용 영역 추출
            current_content = self._extract_section_from_file(node_file_path, "내용")
            
            # 3. 구성 영역에서 파일 목록 가져오기
            composition_files = self._get_composition_files(node_file_path)
            
            # 4. 구성 파일들의 내용 영역 추출하여 결합
            composition_content = []
            for file_name in composition_files:
                file_path = self.base_dir / file_name
                if file_path.exists():
                    content = self._extract_section_from_file(file_path, "내용")
                    if content:
                        composition_content.append(f"=== {file_name} ===\n{content}")
            
            # 5. 전체 결합
            combined_text = self._combine_content_data(current_content, composition_content, node.title)
            
            self.logger.log_operation(f"내용데이터로딩_{node.title}", "성공", 
                                    {"구성파일수": len(composition_files), "텍스트길이": len(combined_text)})
            return combined_text
            
        except Exception as e:
            self.logger.log_error(f"내용데이터로딩_{node.title}", e)
            return ""
    
    def load_node_extraction_data(self, node: Node) -> str:
        """improve_individual_stage용: 추출 영역 데이터 로딩"""
        try:
            # 1. 노드 정보 파일 경로
            node_file_path = self._get_node_file_path(node)
            if not node_file_path.exists():
                return ""
            
            # 2. 현재 파일의 추출 영역 추출
            current_extraction = self._extract_section_from_file(node_file_path, "추출")
            
            # 3. 구성 파일들의 추출 영역도 수집
            composition_files = self._get_composition_files(node_file_path)
            composition_extractions = []
            
            for file_name in composition_files:
                file_path = self.base_dir / file_name
                if file_path.exists():
                    extraction = self._extract_section_from_file(file_path, "추출")
                    if extraction:
                        composition_extractions.append(f"=== {file_name} ===\n{extraction}")
            
            # 4. 전체 결합
            combined_extraction = self._combine_extraction_data(current_extraction, composition_extractions, node.title)
            
            self.logger.log_operation(f"추출데이터로딩_{node.title}", "성공", 
                                    {"구성파일수": len(composition_files), "텍스트길이": len(combined_extraction)})
            return combined_extraction
            
        except Exception as e:
            self.logger.log_error(f"추출데이터로딩_{node.title}", e)
            return ""
    
    def _get_node_file_path(self, node: Node) -> Path:
        """노드 정보 파일 경로 생성 - level_node title_info.md 형식 (node 접두사 제거)"""
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        return self.base_dir / f"{node.level}_{safe_title}_info.md"
    
    def _extract_section_from_file(self, file_path: Path, section_name: str) -> str:
        """파일에서 특정 섹션 내용 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 섹션 헤더 찾기 (# 섹션명)
            header_pattern = f"# {section_name}"
            header_start = content.find(header_pattern)
            
            if header_start == -1:
                return ""
            
            # 섹션 내용 추출
            content_start = header_start + len(header_pattern)
            next_header_start = content.find("\n# ", content_start)
            
            if next_header_start == -1:
                section_content = content[content_start:].strip()
            else:
                section_content = content[content_start:next_header_start].strip()
            
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
            
            # 파일명 라인들 추출
            files = []
            for line in composition_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and line.endswith('.md'):
                    files.append(line)
            
            return files
            
        except Exception:
            return []
    
    def _combine_content_data(self, current_content: str, composition_content: List[str], node_title: str) -> str:
        """내용 영역 데이터 결합"""
        combined = f"# {node_title} - 내용 영역 통합\n\n"
        
        if current_content:
            combined += f"## 현재 노드 내용\n{current_content}\n\n"
        
        if composition_content:
            combined += "## 구성 요소들 내용\n\n"
            for content in composition_content:
                combined += f"{content}\n\n"
        
        return combined
    
    def _combine_extraction_data(self, current_extraction: str, composition_extractions: List[str], node_title: str) -> str:
        """추출 영역 데이터 결합"""
        combined = f"# {node_title} - 추출 영역 통합\n\n"
        
        if current_extraction:
            combined += f"## 현재 노드 추출\n{current_extraction}\n\n"
        
        if composition_extractions:
            combined += "## 구성 요소들 추출\n\n"
            for extraction in composition_extractions:
                combined += f"{extraction}\n\n"
        
        return combined


class DataProcessor:
    """데이터 가공 및 갱신 작업 전담 클래스 - 기존 Claude SDK 프롬프트 사용"""
    
    def __init__(self, content_analyzer: ContentAnalyzer, logger: ProcessLogger):
        self.content_analyzer = content_analyzer
        self.logger = logger
        self.semaphore = asyncio.Semaphore(3)  # 동시 처리 제한
    
    async def process_content_extraction(self, combined_content: str, node_title: str) -> Dict[str, str]:
        """
        데이터 가공: 핵심, 상세 핵심, 주요 화제, 부차 화제 병렬 추출
        기존 Claude SDK 프롬프트를 사용하여 내용 영역과 구성 영역이 결합된 정보를 대상으로 진행
        """
        process_start = time.time()
        self.logger.log_operation(f"내용추출시작_{node_title}", "시작")
        
        # 기존 프롬프트를 사용한 분석 (analyze_content의 기본 동작 활용)
        try:
            # ContentAnalyzer의 기존 프롬프트를 사용 - combined 타입으로 분석
            result = await self.content_analyzer.analyze_content(
                content=combined_content,
                title=node_title,
                context_type="combined"  # 기존 v2에서 사용하던 타입
            )
            
            # 결과 검증 및 정리
            extracted_data = {}
            section_names = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
            
            for section_name in section_names:
                content = result.get(section_name, "")
                if content and not content.startswith("분석 실패") and len(content.strip()) > 0:
                    extracted_data[section_name] = content
                else:
                    extracted_data[section_name] = "추출 실패"
            
            process_time = time.time() - process_start
            success_count = len([v for v in extracted_data.values() if v != "추출 실패"])
            
            self.logger.log_operation(f"내용추출완료_{node_title}", "완료", 
                                    {"처리시간": f"{process_time:.2f}초", "성공섹션": f"{success_count}/4"})
            
            return extracted_data
            
        except Exception as e:
            self.logger.log_error(f"내용추출_{node_title}", e)
            # 실패 시 빈 결과 반환
            return {
                "핵심 내용": "추출 실패",
                "상세 핵심 내용": "추출 실패", 
                "주요 화제": "추출 실패",
                "부차 화제": "추출 실패"
            }
    
    async def update_composition_nodes(self, reference_info: Dict[str, str], 
                                     composition_files: List[str], 
                                     base_dir: Path) -> Dict[str, Dict[str, str]]:
        """
        구성 노드 정보 파일 갱신 - 기존 Claude SDK 프롬프트 사용
        기준: 전체 대상으로 추출한 정보(reference_info)
        참고: 구성 노드의 추출 영역 정보
        """
        update_results = {}
        
        for file_name in composition_files:
            file_path = base_dir / file_name
            if file_path.exists():
                updated_data = await self._update_single_composition_node(file_path, reference_info)
                update_results[file_name] = updated_data
            else:
                update_results[file_name] = {}
        
        return update_results
    
    async def _update_single_composition_node(self, file_path: Path, reference_info: Dict[str, str]) -> Dict[str, str]:
        """단일 구성 노드 갱신 - 기존 Claude SDK 프롬프트 사용"""
        try:
            # 기존 추출 영역 내용 읽기 (기준 정보)
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 기존 추출 영역에서 현재 정보 추출
            current_extraction = self._extract_section_content(original_content, "추출")
            
            # 갱신 컨텍스트 생성 (기존 v2에서 사용하던 형식)
            enhancement_content = f"""기존 정보:
{current_extraction}

전체 정보 (보완용):
핵심 내용: {reference_info.get('핵심 내용', '')}
상세 핵심 내용: {reference_info.get('상세 핵심 내용', '')}
주요 화제: {reference_info.get('주요 화제', '')}
부차 화제: {reference_info.get('부차 화제', '')}"""
            
            # 기존 프롬프트를 사용한 갱신 (enhancement 타입 사용)
            updated_info = await self.content_analyzer.analyze_content(
                content=enhancement_content,
                title=file_path.stem,
                context_type="enhancement"  # 기존 v2에서 사용하던 타입
            )
            
            self.logger.log_operation(f"구성노드갱신_{file_path.name}", "완료")
            return updated_info
            
        except Exception as e:
            self.logger.log_error(f"구성노드갱신_{file_path.name}", e)
            return {}
    
    async def update_current_node(self, current_file_path: Path, 
                                updated_composition_data: Dict[str, Dict[str, str]], 
                                original_info: Dict[str, str]) -> Dict[str, str]:
        """
        현재 노드 정보 파일 갱신 - 기존 Claude SDK 프롬프트 사용
        기준: 전체 대상으로 추출한 정보(original_info) 
        참고: 업데이트된 각 구성 노드 추출 영역 정보(updated_composition_data)
        """
        try:
            # 업데이트된 구성 노드들의 내용을 다시 결합 (기존 v2 방식)
            updated_combined_content = self._combine_updated_composition_content(updated_composition_data)
            
            # 기존 v2에서 사용하던 synthesis_content 형식으로 구성
            synthesis_content = f"""업데이트된 구성 요소들:
{updated_combined_content}

기존 상위 정보:
핵심 내용: {original_info.get('핵심 내용', '')}
상세 핵심 내용: {original_info.get('상세 핵심 내용', '')}
주요 화제: {original_info.get('주요 화제', '')}
부차 화제: {original_info.get('부차 화제', '')}"""
            
            # 기존 프롬프트를 사용한 최종 통합 분석 (synthesis 타입 사용)
            updated_info = await self.content_analyzer.analyze_content(
                content=synthesis_content,
                title=current_file_path.stem,
                context_type="synthesis"  # 기존 v2에서 사용하던 타입
            )
            
            self.logger.log_operation(f"현재노드갱신_{current_file_path.name}", "완료")
            return updated_info
            
        except Exception as e:
            self.logger.log_error(f"현재노드갱신_{current_file_path.name}", e)
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
        """업데이트된 구성 요소들의 내용 결합 (기존 v2 방식)"""
        combined = ""
        
        for file_name, data in updated_composition_data.items():
            if data:  # 빈 딕셔너리가 아닌 경우만
                combined += f"## ========== {file_name} ==========\n\n"
                
                # 4가지 섹션 순서대로 추가
                for section_name in ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]:
                    content = data.get(section_name, "")
                    if content and content != "추출 실패":
                        combined += f"### {section_name}\n{content}\n\n"
                
                combined += "=" * 100 + "\n\n"
        
        return combined


class DataSaver:
    """결과 저장 전담 클래스"""
    
    def __init__(self, base_dir: Path, logger: ProcessLogger):
        self.base_dir = base_dir
        self.logger = logger
    
    def save_to_extraction_section(self, file_path: Path, data: Dict[str, str]) -> bool:
        """추출 영역에 결과 저장"""
        try:
            # 기존 파일 읽기
            if not file_path.exists():
                # 파일이 없으면 기본 구조 생성
                self._create_basic_node_file(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 찾기 또는 생성
            extraction_start = content.find("# 추출")
            if extraction_start == -1:
                # 추출 섹션이 없으면 추가
                content += "\n\n# 추출\n\n"
                extraction_start = content.find("# 추출")
            
            # 추출 섹션 내용 구성
            extraction_content = self._build_extraction_content(data)
            
            # 추출 섹션 이후 내용 찾기
            next_section_start = content.find("\n# ", extraction_start + 4)
            
            if next_section_start == -1:
                # 추출이 마지막 섹션
                new_content = content[:extraction_start] + f"# 추출\n\n{extraction_content}\n"
            else:
                # 추출 이후에 다른 섹션이 있음
                new_content = content[:extraction_start] + f"# 추출\n\n{extraction_content}\n" + content[next_section_start:]
            
            # 파일에 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            success_sections = len([v for v in data.values() if v and v != "추출 실패"])
            self.logger.log_operation(f"저장완료_{file_path.name}", "성공", {"성공섹션": success_sections})
            return True
            
        except Exception as e:
            self.logger.log_error(f"저장실패_{file_path.name}", e)
            return False
    
    def _create_basic_node_file(self, file_path: Path):
        """기본 노드 정보 파일 구조 생성"""
        template = """# 속성
process_status: pending

# 추출

# 내용

# 구성
"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
    
    def _build_extraction_content(self, data: Dict[str, str]) -> str:
        """추출 섹션 내용 구성"""
        content = ""
        
        # 섹션 순서 정의
        section_order = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        
        for section_name in section_order:
            if section_name in data and data[section_name] and data[section_name] != "추출 실패":
                content += f"## {section_name}\n{data[section_name]}\n\n"
        
        return content.strip()


class NodeGrouper:
    """노드 그룹화 및 정렬 로직 전담 클래스"""
    
    def __init__(self, logger: ProcessLogger):
        self.logger = logger
    
    def group_and_sort_nodes(self, nodes: List[Node]) -> Dict[int, List[Node]]:
        """같은 수준의 부모 노드끼리 그룹화, 하위 수준(높은 level)이 앞에 위치하게 정렬"""
        try:
            # 1. 부모 노드들만 필터링 (자식이 있는 노드)
            parent_nodes = [node for node in nodes if node.children]
            
            # 2. 레벨별로 그룹화
            level_groups = {}
            for node in parent_nodes:
                level = node.level
                if level not in level_groups:
                    level_groups[level] = []
                level_groups[level].append(node)
            
            # 3. 각 레벨 내에서 제목별 정렬
            for level in level_groups:
                level_groups[level].sort(key=lambda x: x.title)
            
            # 4. 레벨별로 정렬 (높은 레벨이 앞에 - 하위 수준 노드가 먼저)
            sorted_groups = dict(sorted(level_groups.items(), key=lambda x: x[0], reverse=True))
            
            self.logger.log_operation("노드그룹화", "완료", 
                                    {"레벨수": len(sorted_groups), 
                                     "총부모노드수": sum(len(nodes) for nodes in sorted_groups.values())})
            
            return sorted_groups
            
        except Exception as e:
            self.logger.log_error("노드그룹화", e)
            return {}
    
    def get_processing_order(self, grouped_nodes: Dict[int, List[Node]]) -> List[Node]:
        """처리 순서에 따른 노드 리스트 반환 - 높은 레벨(하위 수준)부터"""
        processing_order = []
        
        # 높은 레벨부터 처리 (하위 수준 노드가 먼저)
        for level in sorted(grouped_nodes.keys(), reverse=True):
            processing_order.extend(grouped_nodes[level])
        
        return processing_order


class DialecticalSynthesisProcessor:
    """정반합 방법론 메인 처리 클래스 V3 - 재구조화된 파이프라인"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 공통 모듈 초기화
        self.logger = ProcessLogger("dialectical_synthesis_v3", self.output_dir)
        self.content_analyzer = ContentAnalyzer(self.logger.logger)
        
        # 전담 클래스들 초기화
        self.data_loader = DataLoader(self.output_dir, self.logger)
        self.data_processor = DataProcessor(self.content_analyzer, self.logger)
        self.data_saver = DataSaver(self.output_dir, self.logger)
        self.node_grouper = NodeGrouper(self.logger)
        
        # 처리 결과 추적
        self.processing_results = {}
    
    async def process_nodes_batch(self, nodes: List[Node]) -> Dict[str, Any]:
        """노드 배치 처리 - 그룹화 및 정렬된 순서로"""
        batch_start = time.time()
        self.logger.log_operation("배치처리시작", "시작", {"총노드수": len(nodes)})
        
        # 1. 노드 그룹화 및 정렬
        grouped_nodes = self.node_grouper.group_and_sort_nodes(nodes)
        processing_order = self.node_grouper.get_processing_order(grouped_nodes)
        
        self.logger.log_operation("처리순서결정", "완료", 
                                {"그룹수": len(grouped_nodes), "처리대상": len(processing_order)})
        
        # 2. 순차적으로 각 노드 처리
        results = {}
        for i, node in enumerate(processing_order):
            self.logger.log_operation(f"노드처리진행", "진행중", 
                                    {"현재": f"{i+1}/{len(processing_order)}", "노드": node.title})
            result = await self.process_single_node_pipeline(node)
            results[node.title] = result
        
        batch_time = time.time() - batch_start
        success_count = sum(1 for r in results.values() if r)
        
        self.logger.log_operation("배치처리완료", "완료", 
                                {"처리시간": f"{batch_time:.2f}초", 
                                 "성공노드": f"{success_count}/{len(results)}"})
        
        return results
    
    async def process_single_node_pipeline(self, node: Node) -> bool:
        """단일 노드 처리 파이프라인 - 데이터 준비/처리/저장 단계별 분리"""
        node_start = time.time()
        self.logger.log_operation(f"파이프라인시작_{node.title}", "시작", 
                                {"레벨": node.level, "자식수": len(node.children)})
        
        try:
            # 1. 데이터 준비 단계 (불러오기)
            success = await self._data_preparation_stage(node)
            if not success:
                self.logger.log_operation(f"파이프라인실패_{node.title}", "실패", {"단계": "데이터준비"})
                return False
            
            # 2. 데이터 처리 단계 (가공 및 갱신)
            success = await self._data_processing_stage(node)
            if not success:
                self.logger.log_operation(f"파이프라인실패_{node.title}", "실패", {"단계": "데이터처리"})
                return False
            
            # 3. 데이터 저장 단계
            success = await self._data_storage_stage(node)
            
            node_time = time.time() - node_start
            self.logger.log_operation(f"파이프라인완료_{node.title}", 
                                    "성공" if success else "실패", 
                                    {"처리시간": f"{node_time:.2f}초"})
            
            return success
            
        except Exception as e:
            self.logger.log_error(f"파이프라인오류_{node.title}", e)
            return False
    
    async def _data_preparation_stage(self, node: Node) -> bool:
        """데이터 준비 단계 - 불러오기"""
        try:
            # gather_and_analyze_stage용 내용 영역 데이터 로딩
            content_data = self.data_loader.load_node_content_data(node)
            if not content_data:
                self.logger.log_error(f"데이터준비_{node.title}", "내용 영역 데이터 로딩 실패")
                return False
            
            # improve_individual_stage용 추출 영역 데이터 로딩
            extraction_data = self.data_loader.load_node_extraction_data(node)
            
            # 처리 결과에 저장
            self.processing_results[node.title] = {
                "content_data": content_data,
                "extraction_data": extraction_data,
                "stage": "준비완료"
            }
            
            self.logger.log_operation(f"데이터준비_{node.title}", "성공")
            return True
            
        except Exception as e:
            self.logger.log_error(f"데이터준비_{node.title}", e)
            return False
    
    async def _data_processing_stage(self, node: Node) -> bool:
        """데이터 처리 단계 - 가공 및 갱신 (기존 Claude SDK 프롬프트 사용)"""
        try:
            node_data = self.processing_results.get(node.title, {})
            content_data = node_data.get("content_data", "")
            
            if not content_data:
                return False
            
            # 데이터 가공: 기존 Claude SDK 프롬프트 기반 4가지 정보 추출
            extracted_info = await self.data_processor.process_content_extraction(content_data, node.title)
            
            # 구성 파일 목록 가져오기
            node_file_path = self.data_loader._get_node_file_path(node)
            composition_files = self.data_loader._get_composition_files(node_file_path)
            
            # 데이터 갱신: 구성 노드들 업데이트 (기존 프롬프트 사용)
            updated_composition_data = {}
            if composition_files:
                updated_composition_data = await self.data_processor.update_composition_nodes(
                    extracted_info, composition_files, self.output_dir
                )
                
                # 현재 노드 업데이트 (기존 프롬프트 사용)
                if node_file_path.exists():
                    current_updated = await self.data_processor.update_current_node(
                        node_file_path, updated_composition_data, extracted_info
                    )
                    # 현재 노드 갱신 결과를 extracted_info에 반영
                    if current_updated:
                        extracted_info.update(current_updated)
            
            # 결과 저장
            self.processing_results[node.title].update({
                "extracted_info": extracted_info,
                "updated_composition_data": updated_composition_data,
                "stage": "처리완료"
            })
            
            self.logger.log_operation(f"데이터처리_{node.title}", "성공", 
                                    {"구성파일수": len(composition_files)})
            return True
            
        except Exception as e:
            self.logger.log_error(f"데이터처리_{node.title}", e)
            return False
    
    async def _data_storage_stage(self, node: Node) -> bool:
        """데이터 저장 단계"""
        try:
            node_data = self.processing_results.get(node.title, {})
            extracted_info = node_data.get("extracted_info", {})
            updated_composition_data = node_data.get("updated_composition_data", {})
            
            if not extracted_info:
                return False
            
            # 1. 현재 노드 파일의 추출 영역에 저장
            node_file_path = self.data_loader._get_node_file_path(node)
            success = self.data_saver.save_to_extraction_section(node_file_path, extracted_info)
            
            # 2. 구성 노드들의 추출 영역에도 저장
            composition_save_count = 0
            for file_name, comp_data in updated_composition_data.items():
                if comp_data:  # 업데이트된 데이터가 있는 경우만
                    comp_file_path = self.output_dir / file_name
                    if self.data_saver.save_to_extraction_section(comp_file_path, comp_data):
                        composition_save_count += 1
            
            if success:
                self.processing_results[node.title]["stage"] = "저장완료"
            
            self.logger.log_operation(f"데이터저장_{node.title}", "성공" if success else "실패", 
                                    {"현재노드": "성공" if success else "실패", 
                                     "구성노드": f"{composition_save_count}/{len(updated_composition_data)}"})
            
            return success
            
        except Exception as e:
            self.logger.log_error(f"데이터저장_{node.title}", e)
            return False


async def main():
    """테스트 실행"""
    from node_structure_analyzer import NodeStructureAnalyzer
    
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-13"
    
    print("=" * 60)
    print("정반합 방법론 시스템 V3 - 재구조화된 파이프라인")
    print("=" * 60)
    
    # 노드 구조 분석
    analyzer = NodeStructureAnalyzer(json_path, "")
    if not analyzer.load_json_structure():
        print("❌ JSON 구조 로딩 실패")
        return
    
    # 부모 노드들만 수집 (자식이 있는 노드)
    all_nodes = list(analyzer.nodes.values())
    parent_nodes = [node for node in all_nodes if node.children]
    
    print(f"🎯 총 노드 수: {len(all_nodes)}")
    print(f"🎯 부모 노드 수: {len(parent_nodes)}")
    
    # 정반합 프로세서 생성 및 실행
    processor = DialecticalSynthesisProcessor(output_dir)
    results = await processor.process_nodes_batch(parent_nodes)
    
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