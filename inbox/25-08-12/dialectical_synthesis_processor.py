"""
생성 시간: 2025-08-12 12:35:00 KST
핵심 내용: 정반합 방법론 구현 - 헤겔의 변증법적 정반합을 적용한 노드 처리 시스템
상세 내용:
    - DialecticalSynthesisProcessor 클래스: 정반합 3단계 처리 관리
    - thesis_stage(node): 정(正) - 자식들 결합하여 전체 대상 4가지 정보 추출
    - antithesis_stage(node, thesis_info): 반(反) - 전체 정보로 각 자식 노드들의 4가지 정보 업데이트
    - synthesis_stage(node, updated_children): 합(合) - 업데이트된 자식들을 반영하여 전체 정보 재업데이트
    - 내부/루트 노드에만 적용 (리프 노드 제외)
    - section_info_enhancer.py와 upper_section_enhancer.py 로직 통합
상태: 활성
주소: dialectical_synthesis_processor
참조: section_info_enhancer.py, upper_section_enhancer.py (참조 구현)
"""

import asyncio
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions
import time
import shutil
import logging
from typing import List, Dict, Optional, Tuple
from node_structure_analyzer import Node

class DialecticalSynthesisProcessor:
    """정반합 방법론을 적용한 노드 처리 클래스"""
    
    # 병렬 처리 설정
    MAX_CONCURRENT_TASKS = 3  # 동시 실행 작업 수 제한
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 비교를 위한 백업 디렉토리 생성
        self.backup_dir = self.output_dir / "backup_before_dialectical"
        self.backup_dir.mkdir(exist_ok=True)
        
        # 로깅 설정
        self.setup_logging()
        
        # 시간 추적
        self.timing_log = {}
        
        # 병렬 처리를 위한 세마포어
        self.semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_TASKS)
        
    def setup_logging(self):
        """로깅 시스템 설정"""
        log_file = self.output_dir / "dialectical_synthesis.log"
        
        # 로거 설정
        self.logger = logging.getLogger('DialecticalSynthesis')
        self.logger.setLevel(logging.DEBUG)
        
        # 기존 핸들러 제거
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 포매터
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info("정반합 프로세서 로깅 시스템 초기화 완료")
    
    def log_timing(self, operation: str, start_time: float, end_time: float = None):
        """작업 시간 로깅"""
        if end_time is None:
            end_time = time.time()
        
        duration = end_time - start_time
        self.timing_log[operation] = duration
        
        self.logger.info(f"⏱️ {operation}: {duration:.2f}초")
        print(f"⏱️ {operation}: {duration:.2f}초")
        
        return duration
    
    async def parallel_task_with_logging(self, task_func, *args, task_name: str):
        """병렬 처리를 위한 작업 래퍼 (세마포어 + 로깅)"""
        async with self.semaphore:
            start_time = time.time()
            self.logger.info(f"🔄 {task_name} 시작 (병렬 처리)")
            print(f"🔄 {task_name} 시작")
            
            try:
                result = await task_func(*args)
                
                duration = time.time() - start_time
                self.logger.info(f"✅ {task_name} 완료 ({duration:.2f}초)")
                print(f"✅ {task_name} 완료 ({duration:.2f}초)")
                
                # 결과 내용 로깅 (첫 100자만)
                if isinstance(result, tuple) and len(result) == 2:
                    header, content = result
                    content_preview = content[:100] + "..." if len(content) > 100 else content
                    self.logger.debug(f"📝 {task_name} 결과 미리보기: {header} - {content_preview}")
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                self.logger.error(f"❌ {task_name} 실패 ({duration:.2f}초): {str(e)}")
                print(f"❌ {task_name} 실패: {str(e)}")
                raise
    
    def log_analysis_result(self, function_name: str, result: Tuple[str, str], success: bool = True):
        """분석 결과 상세 로깅"""
        if success and result and len(result) == 2:
            header, content = result
            content_length = len(content) if content else 0
            
            self.logger.info(f"📊 {function_name} 분석 결과:")
            self.logger.info(f"   🏷️ 헤더: {header}")
            self.logger.info(f"   📏 내용 길이: {content_length}자")
            
            # 내용 미리보기 (첫 200자)
            if content:
                preview = content[:200].replace('\n', ' ') + "..." if len(content) > 200 else content.replace('\n', ' ')
                self.logger.info(f"   👀 내용 미리보기: {preview}")
        else:
            self.logger.warning(f"📊 {function_name} 분석 결과가 비어있거나 형식이 잘못됨")
    
    def create_node_file(self, node: Node, node_type: str) -> Path:
        """노드 파일 생성 (internal_title.md 또는 root_title.md)"""
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
                # internal 노드인 경우 그 자식들의 리프 노드들 수집
                child_files.extend(self._collect_leaf_files_from_internal(child))
        
        content = f"{header_level} {node.title}\n\n"
        for child_file in child_files:
            content += f"{child_file}\n"
        
        with open(node_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📄 노드 파일 생성: {node_file_path.name}")
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
        
        print(f"📄 노드 정보 파일 생성: {info_file_path.name}")
        return info_file_path
    
    def combine_children_content(self, node: Node) -> str:
        """자식 노드들의 내용을 하나로 결합"""
        combined_content = f"# {node.title} 모든 구성 요소의 내용 결합\n\n"
        
        for i, child in enumerate(node.children, 1):
            if child.is_leaf():
                # 리프 노드인 경우 해당 텍스트 파일 읽기
                safe_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                leaf_file = self.output_dir / f"leaf_{safe_title}_info_filled.md"
                
                if leaf_file.exists():
                    with open(leaf_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    combined_content += f"## ========== {child.title} ==========\n\n"
                    combined_content += content + "\n\n"
                    combined_content += "=" * 100 + "\n\n"
            else:
                # 내부 노드인 경우 그 자식들의 내용 재귀적으로 수집
                internal_content = self._collect_internal_content(child)
                combined_content += f"## ========== {child.title} (내부 노드) ==========\n\n"
                combined_content += internal_content + "\n\n"
                combined_content += "=" * 100 + "\n\n"
        
        print(f"📋 자식 노드 내용 결합 완료: {len(combined_content)} 문자")
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

    async def analyze_combined_core_content(self, combined_content: str, node_title: str) -> tuple:
        """결합된 내용에서 전체 대상 핵심 내용 분석"""
        prompt = f"""다음은 "{node_title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{combined_content}

이 전체 내용을 바탕으로 "{node_title}"의 핵심 내용을 2-3문장으로 요약해주세요.
각 구성 요소의 핵심을 통합적으로 반영하여 전체적인 관점에서 정리해주세요.

응답에 '핵심 내용'이라는 헤더는 포함하지 마세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {node_title}의 모든 구성 요소를 통합적으로 분석하여 전체적인 핵심 내용을 간결하게 요약하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return ('핵심 내용', content.strip())
            
        except Exception as e:
            print(f"전체 대상 핵심 내용 분석 중 오류 발생: {e}")
            return ('핵심 내용', f"분석 실패: {str(e)}")

    async def analyze_combined_detailed_content(self, combined_content: str, node_title: str) -> tuple:
        """결합된 내용에서 전체 대상 상세 핵심 내용 분석"""
        prompt = f"""다음은 "{node_title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{combined_content}

이 전체 내용을 바탕으로 "{node_title}"의 상세 핵심 내용을 체계적으로 정리해주세요.
각 구성 요소들 간의 관계와 전체적인 흐름을 고려하여 포괄적으로 설명해주세요.

응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {node_title}의 모든 구성 요소를 체계적으로 분석하여 상세한 내용을 포괄적으로 정리하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return ('상세 핵심 내용', content.strip())
            
        except Exception as e:
            print(f"전체 대상 상세 내용 분석 중 오류 발생: {e}")
            return ('상세 핵심 내용', f"분석 실패: {str(e)}")

    async def analyze_combined_main_topics(self, combined_content: str, node_title: str) -> tuple:
        """결합된 내용에서 전체 대상 주요 화제 분석"""
        prompt = f"""다음은 "{node_title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{combined_content}

이 전체 내용을 바탕으로 "{node_title}"에서 다루는 주요 화제들을 추출해주세요.
각 구성 요소에서 나온 주요 화제들을 모두 포함하되, 전체적인 관점에서 통합적으로 정리해주세요.

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {node_title}의 모든 구성 요소에서 주요 화제를 종합적으로 식별하고 통합적 관점에서 정리하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return ('주요 화제', content.strip())
            
        except Exception as e:
            print(f"전체 대상 주요 화제 분석 중 오류 발생: {e}")
            return ('주요 화제', f"분석 실패: {str(e)}")

    async def analyze_combined_sub_topics(self, combined_content: str, node_title: str) -> tuple:
        """결합된 내용에서 전체 대상 부차 화제 분석"""
        prompt = f"""다음은 "{node_title}"을 구성하는 모든 하위 요소들의 내용을 결합한 것입니다:

{combined_content}

이 전체 내용을 바탕으로 "{node_title}"에서 다루는 부차적인 화제들을 추출해주세요.
각 구성 요소에서 나온 부차 화제들을 모두 포함하되, 전체적인 관점에서 통합적으로 정리해주세요.

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. {node_title}의 모든 구성 요소에서 부차 화제를 종합적으로 식별하고 통합적 관점에서 정리하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return ('부차 화제', content.strip())
            
        except Exception as e:
            print(f"전체 대상 부차 화제 분석 중 오류 발생: {e}")
            return ('부차 화제', f"분석 실패: {str(e)}")

    def update_section(self, file_path: Path, header: str, content: str) -> bool:
        """파일의 특정 헤더 섹션에 내용 업데이트"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        header_pattern = f"## {header}"
        header_start = text.find(header_pattern)
        
        if header_start == -1:
            print(f"헤더를 찾을 수 없습니다: {header}")
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

    async def thesis_stage(self, node: Node) -> Dict[str, str]:
        """정(正) 단계: 자식들 결합하여 전체 대상 4가지 정보 추출"""
        stage_start = time.time()
        print(f"\n🔄 정(正) 단계: {node.title}")
        print("=" * 50)
        self.logger.info(f"정(正) 단계 시작: {node.title}")
        
        # 1. 노드 파일 생성
        node_type = "root" if node.is_root() else "internal"
        node_file = self.create_node_file(node, node_type)
        
        # 2. 노드 정보 파일 생성
        info_file = self.create_node_info_file(node, node_type)
        
        # 3. 자식들 내용 결합
        combined_content = self.combine_children_content(node)
        
        # 4. 전체 대상 4가지 분석 병렬 실행 (fallback 포함)
        print("🔄 전체 대상 4가지 분석 병렬 실행 중 (fallback 포함)...")
        
        tasks = [
            self.retry_analysis_with_fallback(self.analyze_combined_core_content, combined_content, node.title),
            self.retry_analysis_with_fallback(self.analyze_combined_detailed_content, combined_content, node.title),
            self.retry_analysis_with_fallback(self.analyze_combined_main_topics, combined_content, node.title),
            self.retry_analysis_with_fallback(self.analyze_combined_sub_topics, combined_content, node.title)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # 5. 결과를 정보 파일에 업데이트
        print("📝 분석 결과를 정보 파일에 업데이트 중...")
        thesis_info = {}
        
        for header, content in results:
            if content and len(content.strip()) > 0:  # 내용이 실제로 있는지 확인
                if self.update_section(info_file, header, content):
                    thesis_info[header] = content
                    print(f"    ✅ {header}: {len(content)}자")
                else:
                    print(f"    ❌ {header}: 업데이트 실패")
            else:
                print(f"    ⚠️ {header}: 분석 결과가 비어있음")
        
        # 6. 정보 파일을 _filled로 변경 (정 단계 완료 표시)
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        if node_type == "root":
            filled_file = self.output_dir / f"root_{safe_title}_info_filled.md"
        else:
            filled_file = self.output_dir / f"internal_level_{node.level}_{safe_title}_info_filled.md"
        
        if info_file.exists():
            info_file.rename(filled_file)
            print(f"🔄 파일명 변경: {info_file.name} → {filled_file.name}")
        
        self.log_timing("정(正)_단계", stage_start)
        print(f"✅ 정(正) 단계 완료: {len(thesis_info)}/4 분석 성공")
        self.logger.info(f"✅ 정(正) 단계 완료: {len(thesis_info)}/4 분석 성공")
        return thesis_info

    async def enhance_leaf_core_content(self, leaf_content: str, thesis_info: Dict[str, str], leaf_title: str) -> str:
        """리프 노드의 핵심 내용을 전체 정보로 개선"""
        comprehensive_info = f"""핵심 내용: {thesis_info.get('핵심 내용', '')}

상세 핵심 내용: {thesis_info.get('상세 핵심 내용', '')}

주요 화제: {thesis_info.get('주요 화제', '')}

부차 화제: {thesis_info.get('부차 화제', '')}"""
        
        prompt = f"""다음은 전체 내용을 대상으로 작성된 추가 정보입니다:

{comprehensive_info}

그리고 다음은 특정 섹션({leaf_title})의 기존 추가 정보입니다:

{leaf_content}

**작업 요청:**
기존 섹션의 핵심 내용을 **주된 내용으로 유지**하면서, 전체 내용을 대상으로 작성된 추가 정보를 **보완적으로 반영**하여 개선해주세요.

**중요한 원칙:**
1. 기존 각 섹션의 핵심 내용이 주가 되어야 함
2. 전체 내용 대상 추가 정보는 보완적으로만 활용
3. 해당 섹션의 고유한 특성과 내용 유지
4. 전체적인 맥락에서 해당 섹션의 위치와 역할 반영
5. 2-3문장으로 간결하게 작성
6. 응답에 '핵심 내용'이라는 헤더는 포함하지 마세요

개선된 핵심 내용만 작성해주세요:"""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. 기존 섹션 내용을 주로 유지하면서 전체 내용 대상 추가 정보를 보완적으로 반영하여 {leaf_title}의 핵심 내용을 개선하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return content.strip()
            
        except Exception as e:
            print(f"리프 노드 핵심 내용 개선 중 오류 발생: {e}")
            return ""

    async def enhance_leaf_detailed_content(self, leaf_content: str, thesis_info: Dict[str, str], leaf_title: str) -> str:
        """리프 노드의 상세 핵심 내용을 전체 정보로 개선"""
        comprehensive_info = f"""핵심 내용: {thesis_info.get('핵심 내용', '')}

상세 핵심 내용: {thesis_info.get('상세 핵심 내용', '')}

주요 화제: {thesis_info.get('주요 화제', '')}

부차 화제: {thesis_info.get('부차 화제', '')}"""
        
        prompt = f"""다음은 전체 내용을 대상으로 작성된 추가 정보입니다:

{comprehensive_info}

그리고 다음은 특정 섹션({leaf_title})의 기존 추가 정보입니다:

{leaf_content}

**작업 요청:**
기존 섹션의 상세 핵심 내용을 **주된 내용으로 유지**하면서, 전체 내용을 대상으로 작성된 추가 정보를 **보완적으로 반영**하여 개선해주세요.

**중요한 원칙:**
1. 기존 각 섹션의 상세 핵심 내용이 주가 되어야 함
2. 전체 내용 대상 추가 정보는 맥락적 보완만 제공
3. 해당 섹션의 고유한 특성과 세부 설명 유지
4. 전체적인 관점에서 해당 섹션이 전체 내에서 어떤 역할을 하는지 반영
5. 체계적이고 포괄적으로 정리
6. 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요
7. 헤더 사용 시 ### 3레벨부터 사용

개선된 상세 핵심 내용만 작성해주세요:"""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. 기존 섹션의 상세 내용을 주로 유지하면서 전체 내용 대상 추가 정보를 보완적으로 반영하여 {leaf_title}의 상세 내용을 개선하세요. 헤더는 ### 레벨부터 사용하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return content.strip()
            
        except Exception as e:
            print(f"리프 노드 상세 내용 개선 중 오류 발생: {e}")
            return ""

    def preserve_original_topics(self, file_path: Path) -> tuple:
        """기존 주요 화제와 부차 화제를 추출하여 보존"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 주요 화제 추출
        main_topics_start = content.find("## 주요 화제")
        sub_topics_start = content.find("## 부차 화제")
        
        main_topics = ""
        sub_topics = ""
        
        if main_topics_start != -1:
            if sub_topics_start != -1:
                main_topics = content[main_topics_start:sub_topics_start].replace("## 주요 화제\n", "").strip()
            else:
                main_topics = content[main_topics_start:].replace("## 주요 화제\n", "").strip()
        
        if sub_topics_start != -1:
            sub_topics = content[sub_topics_start:].replace("## 부차 화제\n", "").strip()
        
        return main_topics, sub_topics
        
    def backup_files_before_dialectical(self, node: Node) -> None:
        """정반합 시작 전 모든 관련 파일들을 백업"""
        print(f"📋 정반합 시작 전 파일 백업: {node.title}")
        
        # 루트 노드 파일 백업
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        if node.is_root():
            root_file = self.output_dir / f"root_{safe_title}_info_filled.md"
            if root_file.exists():
                backup_file = self.backup_dir / f"root_{safe_title}_info_filled_BEFORE.md"
                shutil.copy2(root_file, backup_file)
                print(f"    ✅ 루트 파일 백업: {backup_file.name}")
        
        # 모든 리프 노드 파일들 백업
        for child in node.children:
            if child.is_leaf():
                safe_child_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                child_file = self.output_dir / f"leaf_{safe_child_title}_info_filled.md"
                if child_file.exists():
                    backup_file = self.backup_dir / f"leaf_{safe_child_title}_info_filled_BEFORE.md"
                    shutil.copy2(child_file, backup_file)
                    print(f"    ✅ 리프 파일 백업: {backup_file.name}")
        
        print(f"📋 백업 완료: backup_before_dialectical/ 디렉토리")
    
    def create_comparison_report(self, node: Node) -> Path:
        """정반합 전후 비교 리포트 생성"""
        print(f"📊 정반합 전후 비교 리포트 생성: {node.title}")
        
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        report_file = self.output_dir / f"dialectical_comparison_report_{safe_title}.md"
        
        comparison_content = f"""# 정반합 방법론 적용 전후 비교 리포트

## 개요
- **대상**: {node.title}
- **적용 방법론**: 헤겔의 변증법적 정반합 (正-反-合)
- **처리 시간**: {time.strftime('%Y-%m-%d %H:%M:%S')}

## 정반합 방법론 설명

### 정(正) 단계
자식 노드들의 내용을 결합하여 전체 대상의 4가지 정보(핵심 내용, 상세 핵심 내용, 주요 화제, 부차 화제)를 추출

### 반(反) 단계  
전체 정보를 바탕으로 각 자식 노드들의 핵심 내용과 상세 핵심 내용만 업데이트 (주요/부차 화제는 유지)

### 합(合) 단계
업데이트된 자식들을 반영하여 전체 정보를 재업데이트 (모든 화제에 출처 표시)

---

## 파일별 변경 사항

"""
        
        # 루트 파일 비교
        if node.is_root():
            root_before = self.backup_dir / f"root_{safe_title}_info_filled_BEFORE.md"
            root_after = self.output_dir / f"root_{safe_title}_info_filled.md"
            
            if root_before.exists() and root_after.exists():
                comparison_content += f"### 루트 파일: root_{safe_title}_info_filled.md\n\n"
                comparison_content += self._compare_file_sections(root_before, root_after)
                comparison_content += "\n---\n\n"
        
        # 각 리프 파일 비교
        for child in node.children:
            if child.is_leaf():
                safe_child_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                leaf_before = self.backup_dir / f"leaf_{safe_child_title}_info_filled_BEFORE.md"
                leaf_after = self.output_dir / f"leaf_{safe_child_title}_info_filled.md"
                
                if leaf_before.exists() and leaf_after.exists():
                    comparison_content += f"### 리프 파일: leaf_{safe_child_title}_info_filled.md\n\n"
                    comparison_content += self._compare_file_sections(leaf_before, leaf_after)
                    comparison_content += "\n---\n\n"
        
        comparison_content += f"""## 전체 결과 요약

✅ **정반합 방법론 적용 완료**
- 정(正): 전체 대상 통합 분석
- 반(反): 개별 구성 요소 개선  
- 합(合): 최종 통합 업데이트

📁 **백업 파일 위치**: backup_before_dialectical/
📊 **비교 리포트**: {report_file.name}

---
*생성 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(comparison_content)
        
        print(f"📊 비교 리포트 생성 완료: {report_file.name}")
        return report_file
    
    def _compare_file_sections(self, before_file: Path, after_file: Path) -> str:
        """두 파일의 섹션별 변경사항 비교"""
        try:
            with open(before_file, 'r', encoding='utf-8') as f:
                before_content = f.read()
            with open(after_file, 'r', encoding='utf-8') as f:
                after_content = f.read()
            
            sections = ["핵심 내용", "상세 핵심 내용", "주요 화제", "부차 화제"]
            comparison = ""
            
            for section in sections:
                before_section = self._extract_section_content(before_content, section)
                after_section = self._extract_section_content(after_content, section)
                
                if before_section != after_section:
                    comparison += f"#### {section}\n"
                    if not before_section.strip():
                        comparison += "**변경 전**: (비어있음)\n\n"
                    else:
                        comparison += f"**변경 전**: {before_section[:200]}{'...' if len(before_section) > 200 else ''}\n\n"
                    
                    if not after_section.strip():
                        comparison += "**변경 후**: (비어있음)\n\n"
                    else:
                        comparison += f"**변경 후**: {after_section[:200]}{'...' if len(after_section) > 200 else ''}\n\n"
                    
                    comparison += f"**상태**: ✅ 업데이트됨\n\n"
                else:
                    comparison += f"#### {section}\n**상태**: 🔄 변경 없음\n\n"
            
            return comparison
            
        except Exception as e:
            return f"비교 중 오류 발생: {str(e)}\n\n"
    
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
    
    def validate_analysis_result(self, result: Tuple[str, str], min_length: int = 10) -> Tuple[bool, str]:
        """분석 결과 유효성 검증"""
        if not result or len(result) != 2:
            return False, "분석 결과 형식이 올바르지 않음"
        
        header, content = result
        
        if not header or not content:
            return False, "헤더 또는 내용이 비어있음"
        
        if len(content.strip()) < min_length:
            return False, f"내용이 너무 짧음 (최소 {min_length}자 필요)"
        
        # 오류 메시지 포함 여부 확인
        error_indicators = ["분석 실패", "오류 발생", "에러", "Error", "error"]
        for indicator in error_indicators:
            if indicator in content:
                return False, f"오류 메시지 포함: {indicator}"
        
        return True, "검증 성공"
    
    async def retry_analysis_with_fallback(self, analysis_func, *args, max_retries: int = 2, timeout: int = 20) -> Tuple[str, str]:
        """분석 실패 시 재시도 및 fallback 로직 (최적화된 버전)"""
        func_name = analysis_func.__name__
        start_time = time.time()
        
        self.logger.info(f"분석 시작: {func_name}")
        
        for attempt in range(max_retries):
            try:
                attempt_start = time.time()
                print(f"    시도 {attempt + 1}/{max_retries}: {func_name} (타임아웃: {timeout}초)")
                self.logger.debug(f"시도 {attempt + 1}/{max_retries}: {func_name} (타임아웃: {timeout}초)")
                
                # 타임아웃 설정으로 무한 대기 방지
                result = await asyncio.wait_for(analysis_func(*args), timeout=timeout)
                is_valid, validation_msg = self.validate_analysis_result(result)
                
                attempt_duration = time.time() - attempt_start
                self.logger.debug(f"시도 {attempt + 1} 소요시간: {attempt_duration:.2f}초")
                
                if is_valid:
                    print(f"    ✅ {func_name} 성공")
                    self.logger.info(f"✅ {func_name} 성공 (시도 {attempt + 1})")
                    self.log_timing(f"{func_name}_성공", start_time)
                    return result
                else:
                    print(f"    ❌ {func_name} 검증 실패: {validation_msg}")
                    self.logger.warning(f"❌ {func_name} 검증 실패: {validation_msg}")
                    if attempt < max_retries - 1:
                        print(f"    ⏳ {func_name} 재시도 중...")
                        self.logger.info(f"⏳ {func_name} 재시도 중...")
                        await asyncio.sleep(1)  # 재시도 전 1초 대기로 단축
                        
            except asyncio.TimeoutError:
                attempt_duration = time.time() - attempt_start
                print(f"    ⏱️ {func_name} 타임아웃 ({timeout}초)")
                self.logger.warning(f"⏱️ {func_name} 타임아웃 (시도 {attempt + 1}, {attempt_duration:.2f}초)")
                # 타임아웃 시 즉시 fallback 적용
                break
            except Exception as e:
                attempt_duration = time.time() - attempt_start
                print(f"    ❌ {func_name} 오류: {e}")
                self.logger.error(f"❌ {func_name} 오류 (시도 {attempt + 1}, {attempt_duration:.2f}초): {e}")
                if attempt < max_retries - 1:
                    print(f"    ⏳ {func_name} 재시도 중...")
                    self.logger.info(f"⏳ {func_name} 재시도 중...")
                    await asyncio.sleep(1)
        
        # 모든 재시도 실패 시 fallback
        header = result[0] if 'result' in locals() and result else func_name.replace('analyze_combined_', '').replace('_', ' ')
        
        print(f"    🔄 {func_name} fallback 적용")
        self.logger.warning(f"🔄 {func_name} 모든 재시도 실패, fallback 적용")
        
        fallback_result = self._generate_fallback_content(func_name, header, args)
        self.log_timing(f"{func_name}_fallback", start_time)
        
        return fallback_result
    
    def _generate_fallback_content(self, func_name: str, header: str, args: tuple) -> Tuple[str, str]:
        """함수별 맞춤형 fallback 콘텐츠 생성"""
        
        if 'sub_topics' in func_name:
            fallback_content = """- 구체적인 구현 방법 및 기술적 세부사항: 텍스트에서 다루는 기술적 구현 방법과 세부 설명
- 예시 코드 및 실제 적용 사례: 제시된 코드 예시와 실제 상황에서의 적용 방법
- 관련 개념 및 배경 지식: 주요 내용을 이해하기 위해 필요한 배경 지식과 관련 개념들
- 제한사항 및 주의사항: 사용 시 고려해야 할 제한사항이나 주의해야 할 점들"""
        
        elif 'main_topics' in func_name:
            fallback_content = """- 핵심 개념 및 정의: 텍스트에서 다루는 주요 개념들과 그 정의
- 주요 방법론 및 접근법: 제시된 주요 방법론과 접근 방식
- 실제 적용 사례 및 예시: 구체적인 적용 사례와 예시들"""
        
        elif 'core' in func_name:
            fallback_content = "이 내용은 복잡한 기술적 내용을 다루고 있으며, 자동 분석에서 핵심 내용 추출에 실패했습니다. 수동 검토가 필요합니다."
        
        elif 'detailed' in func_name:
            fallback_content = "이 섹션의 상세 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요."
        
        else:
            fallback_content = "이 섹션의 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요."
        
        return (header, fallback_content)

    async def antithesis_stage(self, node: Node, thesis_info: Dict[str, str]) -> List[Node]:
        """반(反) 단계: 전체 정보로 각 자식 노드들의 핵심 내용, 상세 핵심 내용만 업데이트 (주요/부차 화제 유지)"""
        stage_start_time = time.time()
        print(f"\n🔄 반(反) 단계: {node.title}")
        print("=" * 50)
        self.logger.info(f"반(反) 단계 시작: {node.title} (자식 노드 {len(node.children)}개)")
        
        updated_children = []
        leaf_children = [child for child in node.children if child.is_leaf()]
        
        # 병렬 처리를 위한 작업 리스트 생성
        parallel_tasks = []
        
        for child in leaf_children:
            task_name = f"자식노드_{child.title}_업데이트"
            parallel_tasks.append(
                self.parallel_task_with_logging(
                    self._process_child_node, 
                    child, thesis_info,
                    task_name=task_name
                )
            )
        
        # 병렬 처리 실행
        if parallel_tasks:
            self.logger.info(f"📦 병렬 처리 시작: {len(parallel_tasks)}개 작업 (MAX_CONCURRENT: {self.MAX_CONCURRENT_TASKS})")
            print(f"📦 병렬 처리 시작: {len(parallel_tasks)}개 작업")
            
            results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
            
            # 결과 처리
            for i, result in enumerate(results):
                child = leaf_children[i]
                if isinstance(result, Exception):
                    self.logger.error(f"❌ {child.title} 처리 실패: {str(result)}")
                    print(f"❌ {child.title} 처리 실패: {str(result)}")
                elif result:
                    updated_children.append(child)
                    self.logger.info(f"✅ {child.title} 처리 완료")
        
        # 내부 노드 처리 (순차적으로)
        for child in node.children:
            if not child.is_leaf():
                self.logger.info(f"🔄 내부 노드: {child.title} (추후 구현)")
                print(f"    🔄 내부 노드: {child.title} (추후 구현)")
                updated_children.append(child)
        
        stage_duration = time.time() - stage_start_time
        self.log_timing(f"반(反)_단계", stage_start_time)
        self.logger.info(f"✅ 반(反) 단계 완료: {len(updated_children)}개 자식 노드 처리 ({stage_duration:.2f}초)")
        print(f"✅ 반(反) 단계 완료: {len(updated_children)}개 자식 노드 처리")
        return updated_children
    
    async def _process_child_node(self, child: Node, thesis_info: Dict[str, str]) -> bool:
        """개별 자식 노드 처리 (병렬 실행용)"""
        try:
            self.logger.info(f"📝 자식 노드 처리 시작: {child.title}")
            
            # 리프 노드 정보 파일 경로
            safe_title = child.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
            child_info_file = self.output_dir / f"leaf_{safe_title}_info_filled.md"
            
            if not child_info_file.exists():
                self.logger.warning(f"❌ {child.title} 정보 파일 없음: {child_info_file}")
                return False
                
            # 기존 내용 읽기
            with open(child_info_file, 'r', encoding='utf-8') as f:
                leaf_content = f.read()
            
            # 기존 주요/부차 화제 보존
            original_main_topics, original_sub_topics = self.preserve_original_topics(child_info_file)
            self.logger.debug(f"📋 {child.title} 기존 주요/부차 화제 보존 완료")
            
            # 핵심 내용과 상세 내용을 병렬로 개선 (fallback 포함)
            self.logger.info(f"🔄 {child.title} 핵심 내용 및 상세 핵심 내용 개선 시작")
            
            tasks = [
                self.retry_analysis_with_fallback(self.enhance_leaf_core_content, leaf_content, thesis_info, child.title),
                self.retry_analysis_with_fallback(self.enhance_leaf_detailed_content, leaf_content, thesis_info, child.title)
            ]
            
            enhanced_core, enhanced_detailed = await asyncio.gather(*tasks)
            
            # 결과 로깅
            self.log_analysis_result("enhance_leaf_core_content", enhanced_core)
            self.log_analysis_result("enhance_leaf_detailed_content", enhanced_detailed)
            
            # 개선된 내용 업데이트 (핵심 내용, 상세 핵심 내용만)
            core_updated = False
            detailed_updated = False
            
            if enhanced_core and len(enhanced_core) == 2:
                self.update_section(child_info_file, enhanced_core[0], enhanced_core[1])
                self.logger.info(f"✅ {child.title} 핵심 내용 업데이트 완료")
                core_updated = True
            else:
                self.logger.warning(f"❌ {child.title} 핵심 내용 개선 실패")
            
            if enhanced_detailed and len(enhanced_detailed) == 2:
                self.update_section(child_info_file, enhanced_detailed[0], enhanced_detailed[1])
                self.logger.info(f"✅ {child.title} 상세 핵심 내용 업데이트 완료")
                detailed_updated = True
            else:
                self.logger.warning(f"❌ {child.title} 상세 핵심 내용 개선 실패")
            
            # 기존 화제들 복원 (변경되지 않도록 보장)
            if original_main_topics:
                self.update_section(child_info_file, "주요 화제", original_main_topics)
                self.logger.debug(f"🔄 {child.title} 주요 화제 복원 완료")
            
            if original_sub_topics:
                self.update_section(child_info_file, "부차 화제", original_sub_topics)
                self.logger.debug(f"🔄 {child.title} 부차 화제 복원 완료")
            
            success = core_updated or detailed_updated
            if success:
                self.logger.info(f"✅ {child.title} 전체 업데이트 완료")
            else:
                self.logger.warning(f"⚠️ {child.title} 일부 업데이트 실패")
                
            return success
            
        except Exception as e:
            self.logger.error(f"❌ {child.title} 처리 중 오류: {str(e)}")
            return False

    async def enhance_synthesis_core_content(self, updated_combined_content: str, original_info: Dict[str, str], node_title: str) -> str:
        """합(合) 단계에서 상위 노드의 핵심 내용을 업데이트된 자식들 정보로 개선"""
        original_upper_content = f"""핵심 내용: {original_info.get('핵심 내용', '')}

상세 핵심 내용: {original_info.get('상세 핵심 내용', '')}

주요 화제: {original_info.get('주요 화제', '')}

부차 화제: {original_info.get('부차 화제', '')}"""
        
        prompt = f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{updated_combined_content}

그리고 다음은 기존 상위 섹션({node_title})의 내용입니다:

{original_upper_content}

**작업 요청:**
기존 상위 섹션의 핵심 내용을 **주된 내용으로 유지**하면서, 업데이트된 각 구성 요소의 핵심을 반영하여 **보다 통합적인 관점**으로 개선해주세요.

**중요한 원칙:**
1. 기존 상위 섹션의 핵심 내용이 주가 되어야 함
2. 업데이트된 각 구성 요소의 개선된 정보들을 통합적으로 활용
3. 전체의 구성 요소들을 아우르는 통합적 관점 반영
4. 2-3문장으로 간결하게 작성
5. 응답에 '핵심 내용'이라는 헤더는 포함하지 마세요

개선된 핵심 내용만 작성해주세요:"""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. 기존 상위 섹션 내용을 주로 유지하면서 업데이트된 각 구성 요소의 핵심을 반영하여 {node_title}의 통합적 관점으로 개선하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return content.strip()
            
        except Exception as e:
            print(f"합(合) 단계 핵심 내용 개선 중 오류 발생: {e}")
            return ""

    async def enhance_synthesis_detailed_content(self, updated_combined_content: str, original_info: Dict[str, str], node_title: str) -> str:
        """합(合) 단계에서 상위 노드의 상세 핵심 내용을 업데이트된 자식들 정보로 개선"""
        original_upper_content = f"""핵심 내용: {original_info.get('핵심 내용', '')}

상세 핵심 내용: {original_info.get('상세 핵심 내용', '')}

주요 화제: {original_info.get('주요 화제', '')}

부차 화제: {original_info.get('부차 화제', '')}"""
        
        prompt = f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{updated_combined_content}

그리고 다음은 기존 상위 섹션({node_title})의 내용입니다:

{original_upper_content}

**작업 요청:**
기존 상위 섹션의 상세 핵심 내용을 **주된 내용으로 유지**하면서, 업데이트된 각 구성 요소의 핵심을 반영하여 **보다 통합적인 관점**으로 개선해주세요.

**중요한 원칙:**
1. 기존 상위 섹션의 상세 핵심 내용이 주가 되어야 함
2. 업데이트된 각 구성 요소의 개선된 정보들을 통합적으로 활용
3. 전체의 구조와 흐름을 반영한 포괄적 설명
4. 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요
5. 헤더 사용 시 ### 3레벨부터 사용

개선된 상세 핵심 내용만 작성해주세요:"""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt=f"텍스트 분석 전문가. 기존 상위 섹션의 상세 내용을 주로 유지하면서 업데이트된 각 구성 요소의 핵심을 반영하여 {node_title}의 통합적 관점으로 개선하세요. 헤더는 ### 레벨부터 사용하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return content.strip()
            
        except Exception as e:
            print(f"합(合) 단계 상세 내용 개선 중 오류 발생: {e}")
            return ""

    async def enhance_synthesis_main_topics(self, updated_combined_content: str) -> str:
        """합(合) 단계에서 모든 구성 요소의 주요 화제 + 전체적 관점에서 추가된 주요 화제 (출처 표시)"""
        prompt = f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{updated_combined_content}

**작업 요청:**
각 구성 요소의 주요 화제들을 **모두 포함**하되, 출처를 다음과 같이 표시:
- 대부분은 구체적인 구성 요소명으로 표시 (예: [출처: 7_Introduction])
- 일부 화제는 전체적 관점에서 통합된 것으로 표시 (예: [출처: 전체 관점])

다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 7_Introduction]
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 전체 관점]

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="텍스트 분석 전문가. 각 구성 요소의 주요 화제를 모두 포함하면서 전체적 관점에서 추가 화제를 식별하여 종합적으로 정리하되, 반드시 각 화제의 출처를 표시하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return content.strip()
            
        except Exception as e:
            print(f"합(合) 단계 주요 화제 개선 중 오류 발생: {e}")
            return ""

    async def enhance_synthesis_sub_topics(self, updated_combined_content: str) -> str:
        """합(合) 단계에서 모든 구성 요소의 부차 화제 + 전체적 관점에서 추가된 부차 화제 (출처 표시)"""
        prompt = f"""다음은 업데이트된 모든 구성 요소들의 정보를 결합한 내용입니다:

{updated_combined_content}

**작업 요청:**
각 구성 요소의 부차 화제들을 **모두 포함**하되, 출처를 다음과 같이 표시:
- 대부분은 구체적인 구성 요소명으로 표시 (예: [출처: 7_Introduction])
- 일부 화제는 전체적 관점에서 통합된 것으로 표시 (예: [출처: 전체 관점])

다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 7_Introduction]
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용 [출처: 전체 관점]

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="텍스트 분석 전문가. 각 구성 요소의 부차 화제를 모두 포함하면서 전체적 관점에서 추가 화제를 식별하여 종합적으로 정리하되, 반드시 각 화제의 출처를 표시하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            return content.strip()
            
        except Exception as e:
            print(f"합(合) 단계 부차 화제 개선 중 오류 발생: {e}")
            return ""

    async def synthesis_stage(self, node: Node, updated_children: List[Node], original_info: Dict[str, str]) -> bool:
        """합(合) 단계: 업데이트된 자식들을 반영하여 전체 정보 재업데이트 (주요/부차 화제 포함, 출처 표시)"""
        stage_start_time = time.time()
        print(f"\n🔄 합(合) 단계: {node.title}")
        print("=" * 50)
        self.logger.info(f"합(合) 단계 시작: {node.title}")
        
        # 1. 업데이트된 자식들의 내용을 다시 결합
        self.logger.info(f"📋 업데이트된 자식들 내용 결합 중 ({len(updated_children)}개 자식)")
        updated_combined_content = self.combine_children_content(node)
        content_length = len(updated_combined_content) if updated_combined_content else 0
        self.logger.debug(f"📏 결합된 내용 길이: {content_length}자")
        
        # 2. 기존 정보 + 업데이트된 자식들 정보를 종합한 최종 분석 (4가지 모두, fallback 포함)
        print("🔄 최종 통합 분석 4가지 병렬 실행 중 (fallback 포함)...")
        self.logger.info("🔄 최종 통합 분석 4가지 병렬 실행 시작")
        
        synthesis_start_time = time.time()
        tasks = [
            self.retry_analysis_with_fallback(self.enhance_synthesis_core_content, updated_combined_content, original_info, node.title),
            self.retry_analysis_with_fallback(self.enhance_synthesis_detailed_content, updated_combined_content, original_info, node.title),
            self.retry_analysis_with_fallback(self.enhance_synthesis_main_topics, updated_combined_content),
            self.retry_analysis_with_fallback(self.enhance_synthesis_sub_topics, updated_combined_content)
        ]
        
        enhanced_core, enhanced_detailed, enhanced_main_topics, enhanced_sub_topics = await asyncio.gather(*tasks)
        synthesis_duration = time.time() - synthesis_start_time
        self.logger.info(f"⏱️ 병렬 분석 완료: {synthesis_duration:.2f}초")
        
        # 분석 결과들 로깅
        self.log_analysis_result("enhance_synthesis_core_content", enhanced_core)
        self.log_analysis_result("enhance_synthesis_detailed_content", enhanced_detailed)
        self.log_analysis_result("enhance_synthesis_main_topics", enhanced_main_topics)
        self.log_analysis_result("enhance_synthesis_sub_topics", enhanced_sub_topics)
        
        # 3. _filled 파일 경로 확인 및 업데이트
        safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        node_type = "root" if node.is_root() else "internal"
        
        if node_type == "root":
            filled_file = self.output_dir / f"root_{safe_title}_info_filled.md"
        else:
            filled_file = self.output_dir / f"internal_level_{node.level}_{safe_title}_info_filled.md"
        
        if not filled_file.exists():
            self.logger.error(f"❌ 상위 노드 정보 파일을 찾을 수 없음: {filled_file}")
            print(f"❌ 상위 노드 정보 파일을 찾을 수 없음: {filled_file}")
            return False
        
        # 4. 개선된 내용들을 파일에 업데이트
        print(f"📝 상위 노드 파일 최종 업데이트 중...")
        self.logger.info(f"📝 {filled_file} 최종 업데이트 시작")
        
        success_count = 0
        update_results = {}
        
        if enhanced_core and len(enhanced_core) == 2:
            self.update_section(filled_file, enhanced_core[0], enhanced_core[1])
            success_count += 1
            update_results['핵심_내용'] = True
            self.logger.info(f"✅ 핵심 내용 최종 업데이트 완료")
            print(f"    ✅ 핵심 내용 최종 업데이트 완료")
        else:
            update_results['핵심_내용'] = False
            self.logger.warning(f"❌ 핵심 내용 개선 실패")
            print(f"    ❌ 핵심 내용 개선 실패")
        
        if enhanced_detailed and len(enhanced_detailed) == 2:
            self.update_section(filled_file, enhanced_detailed[0], enhanced_detailed[1])
            success_count += 1
            update_results['상세_내용'] = True
            self.logger.info(f"✅ 상세 핵심 내용 최종 업데이트 완료")
            print(f"    ✅ 상세 핵심 내용 최종 업데이트 완료")
        else:
            update_results['상세_내용'] = False
            self.logger.warning(f"❌ 상세 핵심 내용 개선 실패")
            print(f"    ❌ 상세 핵심 내용 개선 실패")
        
        if enhanced_main_topics and len(enhanced_main_topics) == 2:
            self.update_section(filled_file, enhanced_main_topics[0], enhanced_main_topics[1])
            success_count += 1
            update_results['주요_화제'] = True
            self.logger.info(f"✅ 주요 화제 최종 업데이트 완료 (출처 표시)")
            print(f"    ✅ 주요 화제 최종 업데이트 완료 (출처 표시)")
        else:
            update_results['주요_화제'] = False
            self.logger.warning(f"❌ 주요 화제 개선 실패")
            print(f"    ❌ 주요 화제 개선 실패")
        
        if enhanced_sub_topics and len(enhanced_sub_topics) == 2:
            self.update_section(filled_file, enhanced_sub_topics[0], enhanced_sub_topics[1])
            success_count += 1
            update_results['부차_화제'] = True
            self.logger.info(f"✅ 부차 화제 최종 업데이트 완료 (출처 표시)")
            print(f"    ✅ 부차 화제 최종 업데이트 완료 (출처 표시)")
        else:
            update_results['부차_화제'] = False
            self.logger.warning(f"❌ 부차 화제 개선 실패")
            print(f"    ❌ 부차 화제 개선 실패")
        
        stage_duration = time.time() - stage_start_time
        self.log_timing(f"합(合)_단계", stage_start_time)
        
        success = success_count >= 2  # 최소 절반 이상 성공하면 성공으로 간주
        self.logger.info(f"📊 합(合) 단계 결과: {success_count}/4 섹션 성공 ({stage_duration:.2f}초)")
        self.logger.info(f"📋 업데이트 결과: {update_results}")
        
        print(f"✅ 합(合) 단계 완료: {node.title} - {success_count}/4 섹션 성공")
        return success

    async def process_node_with_dialectical_synthesis(self, node: Node) -> bool:
        """정반합 방법론으로 단일 노드 처리 (비교 기능 포함)"""
        print(f"\n{'='*60}")
        print(f"정반합 처리 시작: {node.title} ({node.get_node_type()})")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            # 0. 백업 (비교를 위해)
            self.backup_files_before_dialectical(node)
            
            # 1. 정(正) 단계
            thesis_info = await self.thesis_stage(node)
            
            # 2. 반(反) 단계  
            updated_children = await self.antithesis_stage(node, thesis_info)
            
            # 3. 합(合) 단계
            success = await self.synthesis_stage(node, updated_children, thesis_info)
            
            # 4. 비교 리포트 생성
            if success:
                comparison_report = self.create_comparison_report(node)
                print(f"📊 비교 리포트: {comparison_report.name}")
            
            elapsed_time = time.time() - start_time
            
            print(f"\n{'='*60}")
            print(f"정반합 처리 완료: {node.title}")
            print(f"처리 시간: {elapsed_time:.2f}초")
            print(f"결과: {'성공' if success else '실패'}")
            if success:
                print(f"백업: backup_before_dialectical/ 디렉토리")
                print(f"비교: dialectical_comparison_report_{node.title.replace(' ', '_')}.md")
            print(f"{'='*60}")
            
            return success
            
        except Exception as e:
            print(f"❌ 정반합 처리 중 오류: {node.title} - {e}")
            return False

async def main():
    """테스트 실행"""
    from node_structure_analyzer import NodeStructureAnalyzer
    
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12"
    
    print("정반합 방법론 시스템 테스트")
    print("=" * 40)
    
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

if __name__ == "__main__":
    asyncio.run(main())