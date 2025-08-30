# 생성 시간: 2025-08-30 16:58:49 KST
# 핵심 내용: 통합 노드 처리 시스템의 관리자 클래스들 - 문서, 디버그, 로깅 관리
# 상세 내용:
#   - UpdateLogger (20-45): 업데이트 로그 관리자
#   - NodeDocumentManager (47-200): 노드 문서 관리자 - 재귀적 구성 노드 처리
#   - DebugManager (202-220): 디버깅 정보 관리자
# 상태: active
# 주소: managers
# 참조: unified_node_processor_v3.py

import json
import logging
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from core import NodeInfo, ExtractionResult, UpdateLogEntry
from ai_providers import AIProviderFactory


class UpdateLogger:
    """업데이트 로그 관리"""
    def __init__(self, debug_dir: Path):
        self.debug_dir = debug_dir
        self.log_entries: List[UpdateLogEntry] = []
    
    def add_entry(self, entry: UpdateLogEntry):
        """로그 엔트리 추가"""
        self.log_entries.append(entry)
    
    def save_logs(self):
        """로그를 파일로 저장"""
        if not self.log_entries:
            return
        
        log_file = self.debug_dir / f"update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = []
        for entry in self.log_entries:
            log_data.append({
                'timestamp': entry.timestamp,
                'node_title': entry.node_title,
                'section_type': entry.section_type,
                'before_length': len(entry.before_content),
                'after_length': len(entry.after_content),
                'ai_model': entry.ai_model,
                'prompt_tokens': entry.prompt_tokens,
                'response_tokens': entry.response_tokens
            })
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)


class NodeDocumentManager:
    """노드 문서 관리자 - 재귀적 구성 노드 처리 포함"""
    
    def __init__(self, node_docs_dir: Path, ai_factory: AIProviderFactory,
                 debug_manager: 'DebugManager', update_logger: UpdateLogger,
                 logger: logging.Logger):
        self.node_docs_dir = node_docs_dir
        self.ai_factory = ai_factory
        self.debug_manager = debug_manager
        self.update_logger = update_logger
        self.logger = logger
        self._nodes_cache: Optional[List[NodeInfo]] = None
        self._nodes_dict_cache: Optional[Dict[int, NodeInfo]] = None
    
    async def load_nodes_info(self) -> List[NodeInfo]:
        """노드 정보 로드 (JSON 파일에서)"""
        if self._nodes_cache is not None:
            return self._nodes_cache
        
        try:
            # nodes.json 또는 nodes_updated.json 파일 찾기
            nodes_json_path = None
            for filename in ['nodes_updated.json', 'nodes.json']:
                potential_path = self.node_docs_dir.parent / filename
                if potential_path.exists():
                    nodes_json_path = potential_path
                    break
            
            if not nodes_json_path:
                raise FileNotFoundError("nodes.json 또는 nodes_updated.json 파일을 찾을 수 없습니다")
            
            with open(nodes_json_path, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            
            nodes = []
            for node_data in nodes_data:
                # 문서 경로 설정
                document_path = None
                if node_data.get('has_content', False):
                    doc_filename = f"{node_data['id']}_{node_data['title']}_info.md"
                    document_path = str(self.node_docs_dir / doc_filename)
                
                # process_status 읽기
                process_status = False
                if document_path and Path(document_path).exists():
                    process_status = await self._read_process_status(document_path)
                
                node = NodeInfo(
                    id=node_data['id'],
                    title=node_data['title'],
                    level=node_data['level'],
                    parent_id=node_data.get('parent_id'),
                    children_ids=node_data.get('children_ids', []),
                    has_content=node_data.get('has_content', False),
                    document_path=document_path,
                    process_status=process_status
                )
                nodes.append(node)
            
            self._nodes_cache = nodes
            self._nodes_dict_cache = {node.id: node for node in nodes}
            return nodes
            
        except Exception as e:
            self.logger.error(f"노드 정보 로드 실패: {e}")
            return []
    
    async def _read_process_status(self, document_path: str) -> bool:
        """문서에서 process_status 읽기"""
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML 메타데이터 섹션 찾기
            if content.startswith('# 속성\n---\n'):
                yaml_end = content.find('\n---\n', len('# 속성\n---\n'))
                if yaml_end != -1:
                    yaml_content = content[len('# 속성\n---\n'):yaml_end]
                    try:
                        metadata = yaml.safe_load(yaml_content)
                        return metadata.get('process_status', False)
                    except yaml.YAMLError:
                        pass
            
            return False
            
        except Exception as e:
            self.logger.warning(f"process_status 읽기 실패: {document_path} - {e}")
            return False
    
    async def get_combined_content(self, node: NodeInfo, visited: Optional[Set[int]] = None) -> str:
        """노드의 결합된 내용 반환 (재귀적 처리 포함)"""
        if visited is None:
            visited = set()
        
        # 순환 참조 방지
        if node.id in visited:
            self.logger.warning(f"⚠️ 순환 참조 감지: {node.title} (ID: {node.id})")
            return ""
        
        visited.add(node.id)
        
        try:
            # 현재 노드의 내용 섹션 읽기
            current_content = await self._read_content_section(node)
            
            # 자식 노드가 없으면 현재 내용만 반환
            if not node.children_ids:
                visited.remove(node.id)  # 백트래킹
                return current_content
            
            # 노드 딕셔너리 캐시 확보
            if self._nodes_dict_cache is None:
                await self.load_nodes_info()
            
            # 자식 노드들의 내용을 재귀적으로 결합
            combined = current_content
            for i, child_id in enumerate(node.children_ids, 1):
                child_node = self._nodes_dict_cache.get(child_id)
                if child_node is None:
                    self.logger.warning(f"⚠️ 자식 노드 {child_id}를 찾을 수 없음: {node.title}")
                    continue
                
                # 재귀적으로 자식 노드의 결합된 내용 가져오기
                child_combined_content = await self.get_combined_content(child_node, visited.copy())
                
                if child_combined_content:
                    combined += f"\n\n=== 구성 노드 {i} ({child_node.title}) ===\n{child_combined_content}"
            
            visited.remove(node.id)  # 백트래킹
            return combined
            
        except Exception as e:
            self.logger.error(f"결합 내용 생성 실패: {node.title} - {e}")
            if node.id in visited:
                visited.remove(node.id)  # 백트래킹
            return ""
    
    async def _read_content_section(self, node: NodeInfo) -> str:
        """노드 문서의 내용 섹션 읽기"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                return ""
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # "# 내용" 섹션 추출
            content_start = content.find('\n# 내용\n---\n')
            if content_start == -1:
                return ""
            
            content_start += len('\n# 내용\n---\n')
            
            # 다음 섹션(구성) 시작점 찾기
            next_section = content.find('\n# 구성\n---', content_start)
            if next_section == -1:
                return content[content_start:].strip()
            else:
                return content[content_start:next_section].strip()
                
        except Exception as e:
            self.logger.error(f"내용 섹션 읽기 실패: {node.title} - {e}")
            return ""
    
    async def update_extraction_section(self, node: NodeInfo, result: ExtractionResult,
                                       update_logger: UpdateLogger = None):
        """추출 섹션 업데이트"""
        try:
            extraction_content = self._format_extraction_section(result)
            await self.save_extraction_section(node, extraction_content, update_logger)
        except Exception as e:
            self.logger.error(f"추출 섹션 업데이트 실패: {node.title} - {e}")
            raise
    
    def _format_extraction_section(self, result: ExtractionResult) -> str:
        """추출 결과를 섹션 형식으로 포맷팅"""
        sections = []
        
        if result.core_content:
            sections.append(f"## 핵심 내용\n{result.core_content}")
        
        if result.detailed_core_content:
            sections.append(f"## 상세 핵심 내용\n{result.detailed_core_content}")
        
        if result.detailed_content:
            sections.append(f"## 상세 정보\n{result.detailed_content}")
        
        if result.main_topics:
            sections.append(f"## 주요 화제\n{result.main_topics}")
        
        if result.sub_topics:
            sections.append(f"## 부차 화제\n{result.sub_topics}")
        
        return "\n\n".join(sections)
    
    async def save_extraction_section(self, node: NodeInfo, extraction_content: str, 
                                     update_logger: UpdateLogger = None):
        """추출 섹션 저장"""
        try:
            if not node.document_path:
                return
            
            doc_path = Path(node.document_path)
            if not doc_path.exists():
                return
            
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 교체
            extraction_start = content.find('\n# 추출\n---\n')
            if extraction_start == -1:
                return
            
            extraction_start += len('\n# 추출\n---\n')
            next_section = content.find('\n# 내용\n---', extraction_start)
            
            clean_extraction = extraction_content.strip()
            
            if next_section == -1:
                new_content = content[:extraction_start] + clean_extraction + "\n"
            else:
                new_content = content[:extraction_start] + clean_extraction + "\n" + content[next_section:]
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"✅ 추출 섹션 저장 완료: {node.title}")
            
        except Exception as e:
            self.logger.error(f"추출 섹션 저장 실패: {node.title} - {e}")
            raise
    
    async def update_process_status(self, node: NodeInfo, status: bool):
        """노드의 process_status 업데이트"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                return
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML 메타데이터 섹션 업데이트
            if content.startswith('# 속성\n---\n'):
                yaml_end = content.find('\n---\n', len('# 속성\n---\n'))
                if yaml_end != -1:
                    yaml_content = content[len('# 속성\n---\n'):yaml_end]
                    try:
                        metadata = yaml.safe_load(yaml_content) or {}
                        metadata['process_status'] = status
                        
                        updated_yaml = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
                        end_marker_len = len('\n---\n')
                        new_content = f"# 속성\n---\n{updated_yaml}---\n{content[yaml_end + end_marker_len:]}"
                        
                        with open(node.document_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        # 캐시 업데이트
                        node.process_status = status
                        
                        self.logger.info(f"✅ process_status 업데이트: {node.title} -> {status}")
                        
                    except yaml.YAMLError as e:
                        self.logger.error(f"YAML 파싱 오류: {node.title} - {e}")
            
        except Exception as e:
            self.logger.error(f"process_status 업데이트 실패: {node.title} - {e}")
    
    async def load_node_document_content(self, node: NodeInfo) -> str:
        """노드 문서의 전체 내용 로드"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                self.logger.warning(f"문서 파일 없음: {node.title}")
                return ""
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"문서 로드 실패: {node.title} - {e}")
            return ""
    
    def parse_extraction_section(self, content: str) -> Dict[str, str]:
        """문서에서 추출 섹션 파싱"""
        sections = {}
        
        # # 추출 섹션 찾기
        extraction_start = content.find('# 추출\n---\n')
        if extraction_start == -1:
            return sections
        
        # # 내용 섹션 시작점 찾기
        content_start = content.find('# 내용\n---', extraction_start)
        if content_start == -1:
            extraction_content = content[extraction_start + len('# 추출\n---\n'):]
        else:
            extraction_content = content[extraction_start + len('# 추출\n---\n'):content_start]
        
        # 추출 섹션 내용 파싱
        current_section = None
        current_content = []
        
        for line in extraction_content.split('\n'):
            line = line.strip()
            if line.startswith('## 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'core_content'
                current_content = []
            elif line.startswith('## 상세 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_core_content'
                current_content = []
            elif line.startswith('## 상세 정보'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_content'
                current_content = []
            elif line.startswith('## 주요 화제'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'main_topics'
                current_content = []
            elif line.startswith('## 부차 화제'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'sub_topics'
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # 마지막 섹션 처리
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    async def update_node_section(self, node: NodeInfo, section_type: str, new_content: str,
                                 update_logger: UpdateLogger = None):
        """노드 문서의 특정 섹션 업데이트"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                self.logger.warning(f"문서 파일 없음: {node.title}")
                return
            
            # 현재 문서 내용 로드
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 파싱
            sections = self.parse_extraction_section(content)
            
            # 해당 섹션 업데이트
            sections[section_type] = new_content
            
            # 업데이트된 추출 섹션 재구성
            section_names = {
                'core_content': '## 핵심 내용',
                'detailed_core_content': '## 상세 핵심 내용',
                'detailed_content': '## 상세 정보',
                'main_topics': '## 주요 화제',
                'sub_topics': '## 부차 화제'
            }
            
            updated_sections = []
            for key in ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']:
                if key in sections and sections[key]:
                    updated_sections.append(f"{section_names[key]}\n{sections[key]}")
            
            new_extraction_content = '\n\n'.join(updated_sections)
            
            # 문서에서 추출 섹션 교체
            extraction_start = content.find('# 추출\n---\n')
            content_start = content.find('# 내용\n---', extraction_start)
            
            if extraction_start != -1 and content_start != -1:
                new_content_full = (
                    content[:extraction_start + len('# 추출\n---\n')] + 
                    '\n' + new_extraction_content + '\n\n' +
                    content[content_start:]
                )
                
                # 파일 저장
                with open(node.document_path, 'w', encoding='utf-8') as f:
                    f.write(new_content_full)
                
                self.logger.info(f"✅ {section_type} 섹션 업데이트: {node.title}")
            else:
                self.logger.warning(f"추출 섹션을 찾을 수 없음: {node.title}")
                
        except Exception as e:
            self.logger.error(f"섹션 업데이트 실패: {node.title} - {e}")


class DebugManager:
    """디버깅 관리자"""
    
    def __init__(self, debug_dir: Path, logger: logging.Logger):
        self.debug_dir = debug_dir
        self.logger = logger
        
        # 디버그 디렉토리 생성
        self.debug_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_debug_info(self, filename: str, content: str):
        """디버그 정보 저장"""
        try:
            debug_file = self.debug_dir / filename
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.debug(f"디버그 파일 저장: {filename}")
        except Exception as e:
            self.logger.error(f"디버그 파일 저장 실패: {filename} - {e}")