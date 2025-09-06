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

from .core import NodeInfo, ExtractionResult, UpdateLogEntry
from .ai_providers import AIProviderFactory


class UpdateLogger:
    """업데이트 로그 관리 - 개별 프롬프트 파일 저장 방식"""
    def __init__(self, debug_dir: Path):
        # update_history 서브디렉토리 생성
        self.log_dir = debug_dir / "update_history"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.UpdateLogger")
    
    def _sanitize_filename(self, filename: str) -> str:
        """파일명에서 특수문자 제거"""
        import re
        # 파일명에 사용할 수 없는 문자들을 언더스코어로 대체
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 연속된 언더스코어 제거 및 공백을 언더스코어로 변경
        safe_name = re.sub(r'_+', '_', safe_name.replace(' ', '_'))
        # 최대 50자로 제한
        return safe_name[:50]
    
    def _format_simple_extraction_log(self, system_prompt: str, prompt: str, result: str) -> str:
        """간단한 추출 로그 형식 생성 - 프롬프트와 결과만"""
        return f"""[SYSTEM_PROMPT]
{system_prompt}

[PROMPT]
{prompt}

[추출 결과]
{result}"""
    
    def _format_simple_update_log(self, system_prompt: str, prompt: str, update_content: str) -> str:
        """간단한 업데이트 로그 형식 생성 - 프롬프트와 결과만"""
        return f"""[SYSTEM_PROMPT]
{system_prompt}

[PROMPT]
{prompt}

[업데이트 결과]
{update_content}"""
    
    async def log_extraction_with_prompt(self, node_title: str, info_type: str,
                                        prompt: str, system_prompt: str, 
                                        extraction_result: str):
        """추출 작업 시 프롬프트와 결과 저장"""
        try:
            # 시간 형식: HHMM
            time_stamp = datetime.now().strftime('%H%M')
            
            # 파일명 생성: extraction_{정보유형}_{title}_{HHMM}.txt
            safe_title = self._sanitize_filename(node_title)
            filename = f"extraction_{info_type}_{safe_title}_{time_stamp}.txt"
            log_file = self.log_dir / filename
            
            # 로그 내용 구성
            log_content = self._format_simple_extraction_log(
                system_prompt, prompt, extraction_result
            )
            
            # 파일 저장
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.logger.info(f"📝 정보 유형별 추출 히스토리 저장: {filename}")
            return str(log_file)
            
        except Exception as e:
            self.logger.error(f"❌ 정보 유형별 추출 히스토리 저장 실패: {e}")
            return None
    
    async def log_update_with_prompt(self, node_title: str, info_type: str,
                                    prompt: str, system_prompt: str, 
                                    update_content: str,
                                    operation_type: str = "update"):
        """업데이트 작업 시 프롬프트와 결과 저장"""
        try:
            # 시간 형식: HHMM
            time_stamp = datetime.now().strftime('%H%M')
            
            # 파일명 생성: update_{정보유형}_{title}_{HHMM}.txt
            safe_title = self._sanitize_filename(node_title)
            filename = f"update_{info_type}_{safe_title}_{time_stamp}.txt"
            log_file = self.log_dir / filename
            
            # 로그 내용 구성
            log_content = self._format_simple_update_log(
                system_prompt, prompt, update_content
            )
            
            # 파일 저장
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.logger.info(f"📝 업데이트 히스토리 저장: {filename}")
            return str(log_file)
            
        except Exception as e:
            self.logger.error(f"❌ 업데이트 히스토리 저장 실패: {e}")
            return None
    
    # 기존 JSON 방식 메서드들은 더 이상 사용하지 않음
    def add_entry(self, entry):
        """더 이상 사용하지 않음 - 개별 파일 저장 방식으로 변경"""
        pass
    
    def save_logs(self):
        """더 이상 사용하지 않음 - 개별 파일 저장 방식으로 변경"""
        pass


class NodeDocumentManager:
    """노드 문서 관리자 - 재귀적 구성 노드 처리 포함"""
    
    def __init__(self, node_docs_dir: Path, ai_factory: AIProviderFactory,
                 debug_manager: 'DebugManager', update_logger: UpdateLogger,
                 logger: logging.Logger, nodes_json_path: Optional[Path] = None):
        self.node_docs_dir = node_docs_dir
        self.nodes_json_path = nodes_json_path
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
            # 설정된 nodes_json_path 우선 사용, 없으면 기본 경로에서 찾기
            nodes_json_path = None
            if self.nodes_json_path and self.nodes_json_path.exists():
                nodes_json_path = self.nodes_json_path
            else:
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
            has_content_nodes = []  # has_content가 True인 노드들 추적
            missing_documents = []  # 누락된 문서들 추적
            
            for node_data in nodes_data:
                # 문서 경로 설정
                document_path = None
                if node_data.get('has_content', False):
                    # 실제 파일명 형식: {id:02d}_lev{level}_{title}_info.md (공백과 하이픈을 언더스코어로 치환)
                    title_safe = node_data['title'].replace(' ', '_').replace('-', '').replace(':', '').replace('?', '')
                    doc_filename = f"{node_data['id']:02d}_lev{node_data['level']}_{title_safe}_info.md"
                    document_path = str(self.node_docs_dir / doc_filename)
                    has_content_nodes.append((node_data['id'], node_data['title'], doc_filename))
                    
                    # 문서 파일 존재 여부 확인
                    if not Path(document_path).exists():
                        missing_documents.append(doc_filename)
                
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
            
            # 처리할 노드 문서가 없으면 명확한 오류 발생
            if has_content_nodes and missing_documents:
                error_msg = f"❌ 처리할 노드 문서 {len(missing_documents)}개가 누락되었습니다!"
                error_msg += f"\n📁 노드 문서 디렉토리: {self.node_docs_dir}"
                error_msg += f"\n📋 전체 has_content 노드: {len(has_content_nodes)}개"
                error_msg += f"\n❌ 누락된 문서: {missing_documents[:5]}"  # 처음 5개만 표시
                if len(missing_documents) > 5:
                    error_msg += f" ... (총 {len(missing_documents)}개)"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            if has_content_nodes and not missing_documents:
                self.logger.info(f"✅ 모든 노드 문서 확인 완료: {len(has_content_nodes)}개 문서")
            
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
        """추출 섹션 업데이트 - 개별 정보 타입별로 업데이트"""
        try:
            print(f"🐛 update_extraction_section 호출: {node.title}")
            print(f"🐛 추출 결과:")
            print(f"  - core_content: {bool(result.core_content)} ({len(result.core_content) if result.core_content else 0} 문자)")
            print(f"  - detailed_core_content: {bool(result.detailed_core_content)} ({len(result.detailed_core_content) if result.detailed_core_content else 0} 문자)")
            print(f"  - detailed_content: {bool(result.detailed_content)} ({len(result.detailed_content) if result.detailed_content else 0} 문자)")
            print(f"  - main_topics: {bool(result.main_topics)} ({len(result.main_topics) if result.main_topics else 0} 문자)")
            print(f"  - sub_topics: {bool(result.sub_topics)} ({len(result.sub_topics) if result.sub_topics else 0} 문자)")
            
            # 각 정보 타입별로 개별 업데이트
            if result.core_content:
                print(f"🐛 핵심 내용 업데이트 호출")
                try:
                    await self.update_node_section(node, "핵심 내용", result.core_content, update_logger)
                    print(f"🐛 핵심 내용 업데이트 완료")
                except Exception as e:
                    print(f"🐛 핵심 내용 업데이트 실패: {e}")
            else:
                print(f"🐛 핵심 내용 건너뜀 - 값: {repr(result.core_content)}")
                
            if result.detailed_core_content:
                await self.update_node_section(node, "상세 핵심 내용", result.detailed_core_content, update_logger)
                
            if result.detailed_content:
                await self.update_node_section(node, "상세 정보", result.detailed_content, update_logger)
                
            if result.main_topics:
                await self.update_node_section(node, "주요 화제", result.main_topics, update_logger)
                
            if result.sub_topics:
                await self.update_node_section(node, "부차 화제", result.sub_topics, update_logger)
                
            print(f"🐛 update_extraction_section 완료: {node.title}")
        except Exception as e:
            self.logger.error(f"추출 섹션 업데이트 실패: {node.title} - {e}")
            raise
    
    async def update_node_section(self, node: NodeInfo, section_name: str, new_content: str,
                                update_logger: UpdateLogger = None):
        """특정 정보 타입 섹션만 업데이트"""
        try:
            if not node.document_path:
                return
                
            doc_path = Path(node.document_path)
            if not doc_path.exists():
                return
            
            print(f"🐛 update_node_section 호출: {node.title} - {section_name}")
            print(f"🐛 새 내용 길이: {len(new_content)} 문자")
            print(f"🐛 새 내용 미리보기: {new_content[:100]}...")
            
            # 파일 읽기
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"🐛 원본 파일 내용 라인 수: {len(content.splitlines())}")
            print(f"🐛 원본 파일에서 '# 추출' 포함 여부: {'# 추출' in content}")
            
            # 해당 섹션 찾기 (예: ## 핵심 내용)
            section_header = f"## {section_name}"
            section_start = content.find(section_header)
            
            if section_start == -1:
                print(f"🐛 섹션을 찾을 수 없음: {section_name}")
                return
            
            print(f"🐛 섹션 시작 위치: {section_start}")
            
            # 섹션 헤더 라인의 끝 찾기 (헤더 다음 줄부터 내용 시작)
            header_end = content.find('\n', section_start)
            if header_end == -1:
                header_end = len(content)
            content_start = header_end + 1
            
            print(f"🐛 헤더 끝 위치: {header_end}, 내용 시작 위치: {content_start}")
            
            # content[:content_start] 분석
            prefix_content = content[:content_start]
            print(f"🐛 content[:content_start] 길이: {len(prefix_content)} 문자")
            print(f"🐛 content[:content_start]에 '# 추출' 포함: {'# 추출' in prefix_content}")
            print(f"🐛 content[:content_start] 마지막 50자:")
            print(repr(prefix_content[-50:]))
            
            # 다음 섹션 시작점 찾기 (## 또는 # 헤더)
            lines = content[content_start:].split('\n')
            next_section_start = -1
            
            for i, line in enumerate(lines):
                stripped_line = line.strip()
                if stripped_line.startswith('## ') or stripped_line.startswith('# '):
                    next_section_start = content_start + sum(len(l) + 1 for l in lines[:i])
                    break
            
            
            # 기존 내용 추출 (섹션 헤더는 제외하고 내용만)
            if next_section_start == -1:
                old_content = content[content_start:].strip()
                # 파일 끝까지이므로 헤더 유지 + 빈 줄 + 새 내용
                new_full_content = content[:content_start] + '\n' + new_content.strip() + '\n'
                print(f"🐛 파일 끝 섹션 처리: next_section_start == -1")
            else:
                old_content = content[content_start:next_section_start].strip()
                # 중간 섹션이므로 헤더 유지 + 빈 줄 + 새 내용 + 빈 줄 + 다음 섹션
                new_full_content = content[:content_start] + '\n' + new_content.strip() + '\n\n' + content[next_section_start:]
                print(f"🐛 중간 섹션 처리: next_section_start = {next_section_start}")
            
            print(f"🐛 new_full_content 길이: {len(new_full_content)} 문자")
            print(f"🐛 new_full_content에 '# 추출' 포함: {'# 추출' in new_full_content}")
            print(f"🐛 new_full_content 처음 200자:")
            print(repr(new_full_content[:200]))
            
            
            # UpdateLogger 사용 안함 - 개별 파일 저장 방식으로 변경됨
            
            # 파일 저장
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(new_full_content)
                
            # 파일 저장 후 검증
            with open(doc_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            
            print(f"🐛 파일 저장 후 검증:")
            print(f"🐛 저장된 파일 길이: {len(saved_content)} 문자")
            print(f"🐛 저장된 파일에 '# 추출' 포함: {'# 추출' in saved_content}")
            print(f"🐛 저장된 파일 처음 200자:")
            print(repr(saved_content[:200]))
                
            print(f"🐛 섹션 업데이트 완료: {section_name}")
            
        except Exception as e:
            self.logger.error(f"노드 섹션 업데이트 실패: {node.title} - {section_name} - {e}")
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
            
            # 기존 추출 섹션 내용 추출 (디버그 로그용)
            if next_section == -1:
                old_extraction_content = content[extraction_start:].strip()
            else:
                old_extraction_content = content[extraction_start:next_section].strip()
            
            clean_extraction = extraction_content.strip()
            
            if next_section == -1:
                new_content = content[:extraction_start] + clean_extraction + "\n"
            else:
                new_content = content[:extraction_start] + clean_extraction + "\n" + content[next_section:]
            
            # UpdateLogger 사용 안함 - 개별 파일 저장 방식으로 변경됨
            
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
            
            print(f"🐛 update_process_status 호출: {node.title}")
            print(f"🐛 원본 파일에 '# 추출' 포함: {'# 추출' in content}")
            
            # YAML 메타데이터 섹션 업데이트
            if content.startswith('# 속성\n---\n'):
                # "# 추출" 헤더의 위치를 먼저 찾기
                extraction_header_pos = content.find('\n# 추출\n')
                if extraction_header_pos != -1:
                    print(f"🐛 '# 추출' 헤더 위치: {extraction_header_pos}")
                    
                    # YAML 메타데이터는 "# 추출" 이전까지
                    yaml_start_len = len('# 속성\n---\n')
                    yaml_content = content[yaml_start_len:extraction_header_pos]
                    
                    try:
                        metadata = yaml.safe_load(yaml_content.strip()) or {}
                        metadata['process_status'] = status
                        
                        updated_yaml = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
                        
                        # "# 추출" 헤더부터의 모든 내용을 보존
                        remaining_content = content[extraction_header_pos:]
                        print(f"🐛 보존될 부분에 '# 추출' 포함: {'# 추출' in remaining_content}")
                        print(f"🐛 보존될 부분 처음 100자:")
                        print(repr(remaining_content[:100]))
                        
                        # 새 내용 구성: YAML 헤더 + 업데이트된 메타데이터 + "# 추출"부터의 모든 내용
                        new_content = f"# 속성\n---\n{updated_yaml}{remaining_content}"
                        
                        print(f"🐛 재구성된 내용에 '# 추출' 포함: {'# 추출' in new_content}")
                        
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