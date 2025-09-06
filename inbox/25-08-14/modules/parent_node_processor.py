"""
생성 시간: 2025-08-14 20:11:03 KST
핵심 내용: 부모 노드 전용 처리 모듈 - 자식 노드 우선 처리 및 개선된 업데이트 로직
상세 내용:
    - ParentNodeProcessor 클래스 (라인 30-): 부모 노드 전용 처리 로직
    - DataLoader 클래스 (라인 280-): 부모 노드용 데이터 로딩 전용
    - process_parent_node() (라인 50-): 5단계 부모 노드 처리 파이프라인
    - process_children_first() (라인 95-): process_status=false인 자식 노드 우선 처리
    - update_child_extraction_sections() (라인 135-): 핵심/상세핵심만 업데이트
    - process_parent_extraction() (라인 175-): 부모 노드 추출 작업
    - finalize_parent_extraction() (라인 220-): 부모 노드 최종 업데이트
상태: 활성
주소: parent_node_processor/v3_integrated
참조: content_analysis_module_v3.py
"""

import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from content_analysis_module_v3 import ContentAnalyzer
from logging_system_v2 import ProcessLogger


class ParentNodeProcessor:
    """부모 노드 전용 처리 클래스 - 자식 노드 우선 처리 및 개선된 업데이트 로직"""
    
    def __init__(self, node_docs_dir: str, logger: Optional[ProcessLogger] = None):
        self.node_docs_dir = Path(node_docs_dir)
        self.node_docs_dir.mkdir(exist_ok=True)
        
        # 로깅 시스템 초기화
        if logger is None:
            self.output_dir = self.node_docs_dir.parent
            self.logger = ProcessLogger("parent_node_processor", self.output_dir)
        else:
            self.logger = logger
            
        # 분석 모듈 초기화 (V3 사용)
        self.content_analyzer = ContentAnalyzer(self.logger.logger)
        self.data_loader = DataLoader(self.node_docs_dir, self.logger)
        
        # 세마포어로 동시 처리 제한
        self.semaphore = asyncio.Semaphore(2)
    
    async def process_parent_node(self, node_data: Dict[str, Any]) -> bool:
        """부모 노드 전체 처리 파이프라인 - 5단계"""
        node_start = time.time()
        node_title = node_data.get("title", "")
        
        self.logger.log_operation(f"부모노드처리시작_{node_title}", "시작")
        
        try:
            # 1단계: 자식 노드들 우선 처리 (process_status=false인 것만)
            children_success = await self.process_children_first(node_data)
            if not children_success:
                self.logger.log_error(f"자식노드처리_{node_title}", "자식 노드 처리 실패")
                return False
            
            # 2단계: 부모 노드 추출 작업
            parent_extraction_success = await self.process_parent_extraction(node_data)
            if not parent_extraction_success:
                self.logger.log_error(f"부모추출_{node_title}", "부모 노드 추출 실패")
                return False
            
            # 3단계: 자식 노드 추출 섹션 업데이트
            update_success = await self.update_child_extraction_sections(node_data)
            if not update_success:
                self.logger.log_error(f"자식업데이트_{node_title}", "자식 노드 업데이트 실패")
                return False
            
            # 4단계: 부모 노드 최종 업데이트 (업데이트된 자식 정보 반영)
            final_success = await self.finalize_parent_extraction(node_data)
            if not final_success:
                self.logger.log_error(f"부모최종_{node_title}", "부모 노드 최종 업데이트 실패")
                return False
            
            # 5단계: process_status 업데이트
            status_success = self.update_node_status(node_data, True)
            
            node_time = time.time() - node_start
            self.logger.log_operation(f"부모노드처리완료_{node_title}", 
                                    "성공" if status_success else "처리성공_상태실패", 
                                    {"처리시간": f"{node_time:.2f}초"})
            
            return status_success
            
        except Exception as e:
            self.logger.log_error(f"부모노드처리오류_{node_title}", e)
            return False
    
    async def process_children_first(self, node_data: Dict[str, Any]) -> bool:
        """자식 노드들 우선 처리 - process_status=false인 것만"""
        node_title = node_data.get("title", "")
        composition_files = self.data_loader.get_composition_files(node_data)
        
        if not composition_files:
            self.logger.log_operation(f"자식노드없음_{node_title}", "확인", {"구성파일수": 0})
            return True
        
        # process_status가 false인 자식 노드들 필터링
        unprocessed_children = []
        for file_name in composition_files:
            file_path = self.node_docs_dir / file_name
            if file_path.exists() and not self.check_node_status(file_path):
                unprocessed_children.append(file_name)
        
        if not unprocessed_children:
            self.logger.log_operation(f"자식노드완료됨_{node_title}", "확인", 
                                    {"총자식수": len(composition_files), "미처리": 0})
            return True
        
        self.logger.log_operation(f"자식노드처리시작_{node_title}", "시작", 
                                {"총자식수": len(composition_files), "미처리": len(unprocessed_children)})
        
        # 미처리 자식 노드들 처리
        success_count = 0
        for file_name in unprocessed_children:
            file_path = self.node_docs_dir / file_name
            success = await self.process_single_child_node(file_path)
            if success:
                success_count += 1
        
        all_success = success_count == len(unprocessed_children)
        self.logger.log_operation(f"자식노드처리완료_{node_title}", 
                                "성공" if all_success else "부분성공", 
                                {"성공": f"{success_count}/{len(unprocessed_children)}"})
        
        return all_success
    
    async def update_child_extraction_sections(self, node_data: Dict[str, Any]) -> bool:
        """자식 노드 추출 섹션 업데이트 - 핵심 내용, 상세 핵심 내용만"""
        node_title = node_data.get("title", "")
        composition_files = self.data_loader.get_composition_files(node_data)
        
        if not composition_files:
            return True
        
        # 부모 노드의 추출 정보 로드 (참고 정보)
        parent_file_path = self.data_loader._get_node_file_path(node_data)
        parent_extraction = self.data_loader._extract_section_from_file(parent_file_path, "추출")
        
        if not parent_extraction:
            self.logger.log_error(f"부모추출정보없음_{node_title}", "부모 노드 추출 섹션이 없음")
            return False
        
        success_count = 0
        for file_name in composition_files:
            file_path = self.node_docs_dir / file_name
            if file_path.exists():
                success = await self.update_single_child_extraction(file_path, parent_extraction)
                if success:
                    success_count += 1
        
        all_success = success_count == len(composition_files)
        self.logger.log_operation(f"자식업데이트완료_{node_title}", 
                                "성공" if all_success else "부분성공", 
                                {"성공": f"{success_count}/{len(composition_files)}"})
        
        return all_success
    
    async def process_parent_extraction(self, node_data: Dict[str, Any]) -> bool:
        """부모 노드 추출 작업"""
        node_title = node_data.get("title", "")
        
        # 추출용 데이터 로드
        extraction_data = self.data_loader.load_for_extraction(node_data)
        
        if not extraction_data.strip():
            # 내용이 없으면 오류 상황
            self.logger.log_error(f"부모내용없음_{node_title}", "부모 노드에 내용이 없음 - 정상적이지 않은 상황")
            return False
        
        # 내용이 있으면 추출 수행 (정상 상황)
        extracted_info = await self.content_analyzer.extract_content(extraction_data, node_title)
        
        # 모든 필수 섹션이 있는지 검증
        missing_sections = self.validate_extraction_sections(extracted_info)
        
        if missing_sections:
            self.logger.log_operation(f"누락섹션발견_{node_title}", "재추출", 
                                    {"누락섹션": missing_sections})
            
            # 누락된 섹션만 재추출
            retry_extracted = await self.retry_missing_sections(extraction_data, node_title, missing_sections)
            
            # 기존 결과와 재추출 결과 병합
            extracted_info.update(retry_extracted)
        
        # 추출 섹션에 새로운 헤더 형식으로 저장
        node_file_path = self.data_loader._get_node_file_path(node_data)
        return self.save_extraction_with_new_header(node_file_path, extracted_info)
    
    async def finalize_parent_extraction(self, node_data: Dict[str, Any]) -> bool:
        """부모 노드 최종 업데이트 - 업데이트된 자식 정보 반영"""
        node_title = node_data.get("title", "")
        
        # 부모 노드의 현재 추출 섹션
        parent_file_path = self.data_loader._get_node_file_path(node_data)
        base_extraction = self.data_loader._extract_section_from_file(parent_file_path, "추출")
        
        # 자식 노드들의 추출 섹션들
        composition_files = self.data_loader.get_composition_files(node_data)
        children_extractions = []
        
        for file_name in composition_files:
            file_path = self.node_docs_dir / file_name
            if file_path.exists():
                child_extraction = self.data_loader._extract_section_from_file(file_path, "추출")
                if child_extraction.strip():
                    children_extractions.append(child_extraction)
        
        if not children_extractions:
            self.logger.log_operation(f"최종업데이트스킵_{node_title}", "스킵", {"이유": "자식추출정보없음"})
            return True
        
        # 최종 통합 업데이트
        final_extraction = await self.content_analyzer.update_parent_extraction(
            base_extraction, children_extractions, f"{node_title}_최종통합"
        )
        
        # 빈 결과 검증 - 업데이트 결과가 비어있으면 기존 내용 유지
        if not final_extraction.strip():
            self.logger.log_operation(f"최종업데이트건너뛰기_{node_title}", "건너뛰기", {"이유": "업데이트결과빈내용", "기존내용유지": True})
            return True
        
        # 저장
        return self.save_extraction_text(parent_file_path, final_extraction)
    
    async def process_single_child_node(self, file_path: Path) -> bool:
        """단일 자식 노드 처리 - 추출 작업"""
        file_name = file_path.name
        
        try:
            # 자식 노드의 내용 섹션 로드
            content = self.data_loader._extract_section_from_file(file_path, "내용")
            
            if not content.strip():
                self.logger.log_operation(f"자식빈내용_{file_name}", "스킵", {"이유": "내용없음"})
                # 빈 내용이라도 process_status는 true로 설정
                return self.update_file_status(file_path, True)
            
            # 추출 작업
            title = file_path.stem.replace("_info", "")
            extracted_info = await self.content_analyzer.extract_content(content, title)
            
            # 모든 필수 섹션이 있는지 검증
            missing_sections = self.validate_extraction_sections(extracted_info)
            
            if missing_sections:
                self.logger.log_operation(f"자식누락섹션_{file_name}", "재추출", 
                                        {"누락섹션": missing_sections})
                
                # 누락된 섹션만 재추출
                retry_extracted = await self.retry_missing_sections(content, title, missing_sections)
                
                # 기존 결과와 재추출 결과 병합
                extracted_info.update(retry_extracted)
            
            # 저장
            save_success = self.save_extraction_with_new_header(file_path, extracted_info)
            
            if save_success:
                status_success = self.update_file_status(file_path, True)
                return status_success
            
            return False
            
        except Exception as e:
            self.logger.log_error(f"자식노드처리_{file_name}", e)
            return False
    
    async def update_single_child_extraction(self, file_path: Path, parent_extraction: str) -> bool:
        """단일 자식 노드 추출 섹션 업데이트"""
        file_name = file_path.name
        
        try:
            # 자식 노드의 현재 추출 섹션
            base_extraction = self.data_loader._extract_section_from_file(file_path, "추출")
            
            if not base_extraction.strip():
                self.logger.log_operation(f"자식추출없음_{file_name}", "스킵", {"이유": "추출섹션없음"})
                return True
            
            # 업데이트 수행
            title = file_path.stem.replace("_info", "")
            updated_extraction = await self.content_analyzer.update_child_extraction(
                base_extraction, parent_extraction, title
            )
            
            # 저장
            return self.save_extraction_text(file_path, updated_extraction)
            
        except Exception as e:
            self.logger.log_error(f"자식추출업데이트_{file_name}", e)
            return False
    
    def save_extraction_with_new_header(self, file_path: Path, data: Dict[str, str]) -> bool:
        """새로운 헤더 형식으로 추출 섹션에 저장"""
        try:
            if not file_path.exists():
                self._create_basic_node_file(file_path)
            
            # 추출 섹션 내용 생성
            extraction_content = self.content_analyzer.format_extraction_section(data)
            
            return self.save_extraction_text(file_path, extraction_content)
            
        except Exception as e:
            self.logger.log_error(f"추출저장_{file_path.name}", e)
            return False
    
    def save_extraction_text(self, file_path: Path, extraction_text: str) -> bool:
        """추출 섹션 텍스트를 파일에 저장"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extraction_start = content.find("# 추출")
            if extraction_start == -1:
                content += "\n\n# 추출\n\n"
                extraction_start = content.find("# 추출")
            
            next_section_start = content.find("\n# ", extraction_start + 4)
            
            if next_section_start == -1:
                new_content = content[:extraction_start] + f"# 추출\n\n{extraction_text}\n"
            else:
                new_content = content[:extraction_start] + f"# 추출\n\n{extraction_text}\n" + content[next_section_start:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.log_operation(f"추출저장완료_{file_path.name}", "성공")
            return True
            
        except Exception as e:
            self.logger.log_error(f"추출저장실패_{file_path.name}", e)
            return False
    
    def update_node_status(self, node_data: Dict[str, Any], status: bool) -> bool:
        """노드의 process_status 업데이트"""
        node_file_path = self.data_loader._get_node_file_path(node_data)
        return self.update_file_status(node_file_path, status)
    
    def update_file_status(self, file_path: Path, status: bool) -> bool:
        """파일의 process_status 업데이트"""
        try:
            if not file_path.exists():
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            status_pattern = "process_status:"
            status_start = content.find(status_pattern)
            
            if status_start == -1:
                # process_status가 없으면 속성 섹션에 추가
                attr_start = content.find("# 속성")
                if attr_start != -1:
                    attr_end = content.find("\n# ", attr_start + 4)
                    if attr_end == -1:
                        new_content = content + f"\nprocess_status: {str(status).lower()}\n"
                    else:
                        new_content = content[:attr_end] + f"\nprocess_status: {str(status).lower()}\n" + content[attr_end:]
                else:
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
    
    def validate_extraction_sections(self, extracted_info: Dict[str, str]) -> List[str]:
        """추출된 섹션들이 모두 있는지 검증하고 누락된 섹션 목록 반환"""
        required_sections = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
        missing_sections = []
        
        for section in required_sections:
            if section not in extracted_info or not extracted_info[section].strip():
                missing_sections.append(section)
        
        return missing_sections
    
    async def retry_missing_sections(self, extraction_data: str, title: str, missing_sections: List[str]) -> Dict[str, str]:
        """누락된 섹션들만 재추출"""
        retry_result = {}
        
        for section in missing_sections:
            try:
                if section == "핵심 내용":
                    section_name, content = await self.content_analyzer._extract_core_content(extraction_data, title)
                elif section == "상세 핵심 내용":
                    section_name, content = await self.content_analyzer._extract_detailed_content(extraction_data, title)
                elif section == "주요 화제":
                    section_name, content = await self.content_analyzer._extract_main_topics(extraction_data, title)
                elif section == "부차 화제":
                    section_name, content = await self.content_analyzer._extract_sub_topics(extraction_data, title)
                else:
                    continue
                
                if content and content.strip():
                    retry_result[section] = content.strip()
                    self.logger.log_operation(f"섹션재추출성공_{title}", section, {"길이": f"{len(content)}자"})
                else:
                    self.logger.log_operation(f"섹션재추출실패_{title}", section, {"결과": "빈내용"})
                    
            except Exception as e:
                self.logger.log_error(f"섹션재추출오류_{title}_{section}", e)
        
        return retry_result


class DataLoader:
    """부모 노드 처리용 데이터 로딩 클래스"""
    
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
            
            return combined_content
            
        except Exception as e:
            self.logger.log_error(f"추출데이터로딩_{node_data.get('title', '')}", e)
            return ""
    
    def get_composition_files(self, node_data: Dict[str, Any]) -> List[str]:
        """구성 섹션에서 파일 목록 추출"""
        try:
            node_file_path = self._get_node_file_path(node_data)
            return self._get_composition_files(node_file_path)
        except Exception:
            return []
    
    def _get_node_file_path(self, node_data: Dict[str, Any]) -> Path:
        """노드 정보 파일 경로 생성"""
        node_id = node_data.get("id", 0)
        level = node_data.get("level", 0)
        title = node_data.get("title", "")
        safe_title = title.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
        safe_title = safe_title.replace("-", "_")
        return self.base_dir / f"{node_id:02d}_lev{level}_{safe_title}_info.md"
    
    def _extract_section_from_file(self, file_path: Path, section_name: str) -> str:
        """파일에서 특정 섹션 내용 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            header_pattern = f"# {section_name}"
            header_start = content.find(header_pattern)
            
            if header_start == -1:
                return ""
            
            content_start = header_start + len(header_pattern)
            
            lines = content[content_start:].split('\n')
            section_lines = []
            
            for line in lines:
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


async def test_parent_node_processor():
    """부모 노드 처리기 테스트"""
    import json
    
    # 테스트 설정
    node_docs_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/node_docs_v2"
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/nodes.json"
    
    print("=" * 50)
    print("부모 노드 처리기 테스트")
    print("=" * 50)
    
    # 프로세서 생성
    processor = ParentNodeProcessor(node_docs_dir)
    
    # 테스트용 노드 데이터 로드
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            nodes_data = json.load(f)
        
        # 부모 노드 찾기 (children_ids가 있는 노드)
        parent_nodes = [node for node in nodes_data if node.get("children_ids") and len(node.get("children_ids", [])) > 0]
        
        if not parent_nodes:
            print("❌ 테스트할 부모 노드가 없습니다.")
            return
        
        # 첫 번째 부모 노드로 테스트
        test_node = parent_nodes[0]
        node_title = test_node.get("title", "")
        
        print(f"🎯 테스트 대상 노드: {node_title}")
        print(f"   - 레벨: {test_node.get('level', 0)}")
        print(f"   - 자식 수: {len(test_node.get('children_ids', []))}")
        
        # 처리 실행
        result = await processor.process_parent_node(test_node)
        
        print(f"\n📋 처리 결과:")
        print(f"  {'✅' if result else '❌'} {node_title}: {'성공' if result else '실패'}")
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류: {e}")


if __name__ == "__main__":
    asyncio.run(test_parent_node_processor())