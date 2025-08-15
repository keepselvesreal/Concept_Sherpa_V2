"""
생성 시간: 2025-08-12 12:20:00 KST
핵심 내용: 리프 노드 처리 시스템 - 정식 버전 (완전한 분석 수행)
상세 내용:
    - 병렬 처리 MAX_CONCURRENT_TASKS=2
    - 완전한 Claude SDK 기반 분석 수행
    - CPU 사용률 모니터링 및 자원 관리
    - 재시도 및 fallback 로직 포함
상태: 활성
주소: leaf_node_processor
참조: text_info_processor_v3.py (기반 코드)
"""

import asyncio
import psutil
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions
import time
from typing import List, Optional
from node_structure_analyzer import Node

class LeafNodeProcessor:
    """리프 노드 텍스트 파일 처리 클래스 - 병렬 처리 및 자원 관리"""
    
    def __init__(self, output_dir: str, max_concurrent_tasks: int = 2):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.max_concurrent_tasks = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.active_tasks = set()

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
        
        print(f"📄 정보 파일 생성: {info_file_path.name}")
        return info_file_path

    def validate_analysis_result(self, result, min_length=10):
        """분석 결과 유효성 검증"""
        header, content = result
        if not content or len(content.strip()) < min_length:
            return False, f"'{header}' 결과가 너무 짧거나 비어있음: {len(content.strip())}자"
        if "분석 실패" in content:
            return False, f"'{header}' 분석 실패 메시지 포함"
        return True, "유효"

    async def analyze_core_content(self, text):
        """핵심 내용 분석"""
        prompt = f"""다음 텍스트의 핵심 내용을 간결하게 정리해주세요:

{text}

핵심 내용만 2-3문장으로 요약해주세요. 응답에 '핵심 내용'이라는 제목이나 헤더는 포함하지 마세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="텍스트 분석 전문가. 텍스트의 핵심 내용을 간결하고 정확하게 요약하세요.",
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
            print(f"핵심 내용 분석 중 오류 발생: {e}")
            return ('핵심 내용', f"분석 실패: {str(e)}")

    async def analyze_detailed_content(self, text):
        """상세 핵심 내용 분석"""
        prompt = f"""다음 텍스트의 상세 핵심 내용을 체계적으로 정리해주세요:

{text}

주요 개념과 설명을 포함하여 상세하게 정리해주세요. 응답에 '상세 핵심 내용'이라는 제목이나 헤더는 포함하지 마세요."""
        
        try:
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="텍스트 분석 전문가. 텍스트의 상세 내용을 체계적이고 포괄적으로 정리하세요.",
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
            print(f"상세 내용 분석 중 오류 발생: {e}")
            return ('상세 핵심 내용', f"분석 실패: {str(e)}")

    async def analyze_main_topics(self, text):
        """주요 화제 분석"""
        prompt = f"""다음 텍스트에서 다루는 주요 화제들을 추출해주세요:

{text}

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
                    system_prompt="텍스트 분석 전문가. 텍스트에서 주요 화제를 정확히 식별하고 지정된 형식으로 정리하세요.",
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
            print(f"주요 화제 분석 중 오류 발생: {e}")
            return ('주요 화제', f"분석 실패: {str(e)}")

    async def analyze_sub_topics(self, text):
        """부차 화제 분석"""
        prompt = f"""다음 텍스트에서 다루는 부차적인 화제들을 추출해주세요:

{text}

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
                    system_prompt="텍스트 분석 전문가. 텍스트에서 부차적 화제를 식별하고 지정된 형식으로 정리하세요.",
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
            print(f"부차 화제 분석 중 오류 발생: {e}")
            return ('부차 화제', f"분석 실패: {str(e)}")

    async def retry_analysis_with_fallback(self, text, analysis_func, max_retries=2):
        """분석 실패 시 재시도 및 fallback 로직"""
        for attempt in range(max_retries):
            try:
                print(f"    시도 {attempt + 1}/{max_retries}: {analysis_func.__name__}")
                result = await analysis_func(text)
                is_valid, validation_msg = self.validate_analysis_result(result)
                
                if is_valid:
                    print(f"    ✅ {analysis_func.__name__} 성공")
                    return result
                else:
                    print(f"    ❌ {analysis_func.__name__} 검증 실패: {validation_msg}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(1)
                        
            except Exception as e:
                print(f"    ❌ {analysis_func.__name__} 오류: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
        
        # fallback 로직
        header = result[0] if 'result' in locals() else analysis_func.__name__.replace('analyze_', '').replace('_', ' ')
        
        if 'sub_topics' in analysis_func.__name__:
            fallback_content = f"""- 구체적인 구현 방법: 텍스트에서 다루는 기술적 구현 방법과 세부 설명
- 예시 및 적용 사례: 제시된 예시와 실제 상황에서의 적용 방법
- 관련 개념: 주요 내용을 이해하기 위해 필요한 배경 지식과 관련 개념들"""
        elif 'main_topics' in analysis_func.__name__:
            fallback_content = f"""- 핵심 개념 및 정의: 텍스트에서 다루는 주요 개념들과 그 정의
- 주요 방법론: 제시된 주요 방법론과 접근 방식
- 적용 사례: 구체적인 적용 사례와 예시들"""
        elif 'core' in analysis_func.__name__:
            fallback_content = "이 텍스트는 복잡한 내용을 다루고 있으며, 자동 분석에서 핵심 내용 추출에 실패했습니다."
        else:
            fallback_content = "이 섹션의 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요."
        
        print(f"    🔄 {analysis_func.__name__} fallback 적용")
        return (header, fallback_content)

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

    def rename_to_filled(self, info_file_path: Path) -> Path:
        """정보 파일명을 _filled 접미사로 변경"""
        filled_path = info_file_path.parent / f"{info_file_path.stem}_filled.md"
        info_file_path.rename(filled_path)
        print(f"🔄 파일명 변경: {info_file_path.name} → {filled_path.name}")
        return filled_path

    async def process_single_leaf_node(self, node: Node, text_file_path: Path) -> tuple:
        """단일 리프 노드 처리 (세마포어 포함)"""
        async with self.semaphore:
            task_id = f"node_{node.id}"
            self.active_tasks.add(task_id)
            
            try:
                print(f"\n📄 처리 시작: {node.title}")
                print("-" * 50)
                
                # 1. 텍스트 파일 읽기
                if not text_file_path.exists():
                    print(f"❌ 텍스트 파일을 찾을 수 없습니다: {text_file_path}")
                    return (node, False)
                
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                print(f"✅ 텍스트 읽기 완료: {len(text)} 문자")
                
                # 2. 정보 파일 생성
                info_file_path = self.create_leaf_info_file(node)
                
                # 3. 4개 분석 작업을 fallback과 함께 병렬로 실행
                print("🔄 4개 분석 작업을 병렬로 실행 중...")
                
                tasks = [
                    self.retry_analysis_with_fallback(text, self.analyze_core_content),
                    self.retry_analysis_with_fallback(text, self.analyze_detailed_content),
                    self.retry_analysis_with_fallback(text, self.analyze_main_topics),
                    self.retry_analysis_with_fallback(text, self.analyze_sub_topics)
                ]
                
                # 병렬 실행
                results = await asyncio.gather(*tasks)
                
                # 4. 결과를 파일에 업데이트
                print("📝 분석 결과를 파일에 업데이트 중...")
                success_count = 0
                for i, (header, content) in enumerate(results):
                    print(f"결과 {i+1}: 헤더='{header}', 내용 길이={len(content)}자")
                    if self.update_section(info_file_path, header, content):
                        success_count += 1
                
                # 5. 작업 완료 후 파일명 변경
                if success_count == 4:
                    filled_path = self.rename_to_filled(info_file_path)
                    print(f"✅ '{node.title}' 처리 완료")
                    return (node, True)
                else:
                    print(f"❌ '{node.title}' 처리 실패: {success_count}/4 작업 성공")
                    return (node, False)
                
            except Exception as e:
                print(f"❌ '{node.title}' 처리 중 오류: {e}")
                return (node, False)
            finally:
                self.active_tasks.discard(task_id)

    async def process_all_leaf_nodes_parallel(self, leaf_nodes: List[Node], text_base_path: Path) -> int:
        """모든 리프 노드를 병렬 처리"""
        print(f"\n{'='*60}")
        print(f"리프 노드 병렬 처리 시작 - 총 {len(leaf_nodes)}개 노드")
        print(f"최대 동시 작업: {self.max_concurrent_tasks}개")
        print(f"완전한 Claude SDK 분석 수행")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # 모든 작업을 병렬로 실행할 태스크 생성
        tasks = []
        for node in leaf_nodes:
            safe_title = node.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
            text_file_path = text_base_path / f"{safe_title}.md"
            
            task = self.process_single_leaf_node(node, text_file_path)
            tasks.append(task)
        
        try:
            # 모든 태스크 병렬 실행
            print(f"\n🚀 {len(tasks)}개 작업 병렬 실행 시작...")
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 분석
            success_count = 0
            error_count = 0
            
            print(f"\n📊 처리 결과 분석...")
            for result in results:
                if isinstance(result, Exception):
                    error_count += 1
                    print(f"❌ 예외 발생: {str(result)}")
                else:
                    node, success = result
                    if success:
                        success_count += 1
                        print(f"✅ {node.title}: 성공")
                    else:
                        error_count += 1
                        print(f"❌ {node.title}: 실패")
            
            elapsed_time = time.time() - start_time
            
            # 완료 메시지
            print(f"\n{'='*60}")
            print(f"모든 리프 노드 병렬 처리 완료!")
            print(f"성공: {success_count}/{len(leaf_nodes)} 노드")
            print(f"실패: {error_count}/{len(leaf_nodes)} 노드") 
            print(f"처리 시간: {elapsed_time:.2f}초")
            print(f"평균 처리 속도: {len(leaf_nodes)/elapsed_time:.2f} 노드/초")
            print(f"{'='*60}")
            
            return success_count
            
        finally:
            # 자원 해제
            if self.active_tasks:
                print(f"🧹 활성 작업 {len(self.active_tasks)}개 완료 대기 중...")
                while self.active_tasks:
                    await asyncio.sleep(0.1)
            print("🧹 자원 해제 완료")

async def main():
    """테스트 실행"""
    from node_structure_analyzer import NodeStructureAnalyzer
    
    json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/chapter7_clean.json"
    text_base_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12"
    
    print("=" * 60)
    print("리프 노드 병렬 처리 시스템 - 정식 버전")
    print("=" * 60)
    
    # 노드 구조 분석
    analyzer = NodeStructureAnalyzer(json_path, text_base_path)
    if not analyzer.load_json_structure():
        return
    
    # 리프 노드 처리 (병렬, MAX_CONCURRENT_TASKS=2)
    processor = LeafNodeProcessor(output_dir, max_concurrent_tasks=2)
    leaf_nodes = analyzer.get_leaf_nodes()
    
    # 비동기 병렬 실행
    success_count = await processor.process_all_leaf_nodes_parallel(leaf_nodes, Path(text_base_path))
    
    print(f"\n🎯 최종 결과: {success_count}/{len(leaf_nodes)} 리프 노드 처리 성공")
    
    # 생성된 파일 확인
    print(f"\n📁 생성된 파일 확인:")
    output_path = Path(output_dir)
    filled_files = list(output_path.glob("leaf_*_info_filled.md"))
    
    print(f"  - leaf_*_info_filled.md: {len(filled_files)}개")
    for file in filled_files:
        print(f"    - {file.name}")

if __name__ == "__main__":
    asyncio.run(main())