#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 17:16:14 KST
핵심 내용: 노드 구조를 기반으로 원문에서 섹션별 텍스트를 추출하여 마크다운 파일로 저장하는 스크립트
상세 내용:
- load_nodes (라인 30-45): JSON 노드 파일 로드
- load_toc_structure (라인 50-65): 목차 구조 로드
- extract_single_section (라인 70-150): Claude SDK를 이용한 단일 섹션 추출
- find_section_boundaries (라인 155-175): 섹션 경계 찾기
- extract_all_sections (라인 180-220): 모든 노드에 대한 섹션 병렬 추출
- save_extracted_content (라인 225-250): 추출된 내용을 파일로 저장
- main (라인 255-290): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: node_section_extractor
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/parallel_section_extractor.py
"""

import anyio
import asyncio
import json
import sys
import time
import signal
import atexit
from pathlib import Path
from typing import List, Dict, Any, Optional
from claude_code_sdk import query, ClaudeCodeOptions

# 전역 자원 관리
MAX_CONCURRENT_TASKS = 5  # 최대 병렬 작업 수
active_tasks = set()  # 현재 실행 중인 작업들
semaphore = None  # 세마포어 (main에서 초기화)

def cleanup_resources():
    """자원 정리 함수"""
    global active_tasks
    print("\n🧹 자원 정리 중...")
    
    # 남은 작업들 취소
    for task in list(active_tasks):
        if not task.done():
            task.cancel()
    
    active_tasks.clear()
    print("✅ 자원 정리 완료")

def signal_handler(signum, frame):
    """시그널 핸들러 - Ctrl+C 등 중단 신호 처리"""
    print(f"\n🛑 중단 신호 감지 (시그널 {signum})")
    cleanup_resources()
    sys.exit(0)

def load_nodes(nodes_file: str) -> List[Dict[str, Any]]:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # headers 키가 있는 경우 추출
        if isinstance(nodes, dict) and 'headers' in nodes:
            nodes = nodes['headers']
            
        return nodes
    except Exception as e:
        print(f"노드 파일 로드 오류: {e}")
        return []

def load_toc_structure(toc_file: str) -> str:
    """목차 파일을 로드하여 구조 정보를 반환합니다."""
    try:
        with open(toc_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"목차 파일 로드 오류: {e}")
        return ""

async def extract_single_section(source_text: str, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], toc_structure: str, retry_count: int = 0) -> Dict[str, Any]:
    """
    단일 노드 섹션을 Claude SDK로 추출
    
    Args:
        source_text: 원본 텍스트
        node: 추출할 노드 정보
        all_nodes: 전체 노드 리스트
        toc_structure: 목차 구조 정보
        retry_count: 재시도 횟수
    
    Returns:
        Dict with node info, content, status
    """
    global semaphore, active_tasks
    
    # 세마포어를 사용하여 동시 실행 작업 수 제한
    async with semaphore:
        current_task = asyncio.current_task()
        active_tasks.add(current_task)
        
        try:
            section_title = node.get('title', '')
            node_id = node.get('id', '')
            node_level = node.get('level', 0)
            
            # 다음 같은 레벨 또는 상위 레벨 섹션 찾기
            next_section = find_section_boundaries(node, all_nodes)
            
            # 경계 설정
            if next_section:
                boundary_instruction = f'섹션은 "{section_title}" 부분부터 "{next_section}" 직전까지입니다.'
            else:
                boundary_instruction = f'섹션은 "{section_title}" 부분부터 문서의 끝 또는 다음 상위 섹션까지입니다.'
            
            # 재시도별 프롬프트 강화
            retry_emphasis = ""
            if retry_count > 0:
                retry_emphasis = f"""
【재시도 {retry_count+1}회차】 이전 추출이 실패했습니다. 더 신중하게 접근해주세요:
- 섹션 제목을 정확히 찾아주세요 (대소문자, 구두점 주의)
- 해당 섹션의 모든 내용을 누락 없이 포함해주세요
- 원본 텍스트 구조를 그대로 유지해주세요"""

            prompt = f"""다음 문서에서 "{section_title}" 섹션만 찾아서 그 내용을 완전히 추출해주세요.

【문서 전체 구조】
{toc_structure}

【추출 대상】
- 목표 섹션: "{section_title}" (ID: {node_id}, Level: {node_level})
- {boundary_instruction}

{retry_emphasis}

【추출 규칙】
1. 섹션 제목이 정확히 일치하는 부분을 찾아주세요
2. 해당 섹션의 모든 내용을 누락 없이 포함해주세요
3. 하위 섹션들도 모두 포함해주세요
4. 코드 예제, 목록, 표 등 모든 요소를 포함해주세요
5. 원본 형태 그대로 반환하세요 (추가 설명이나 주석 금지)

【원본 문서】
{source_text}"""

            # Claude 호출
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="기술문서 섹션 추출 전문가. 요청된 섹션의 모든 내용을 정확히 추출하여 원본 형태로 반환하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            # 응답 추출
            content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                content += block.text
                    else:
                        content += str(message.content)
            
            content = content.strip()
            
            # 추출 결과 검증
            if not content or len(content) < 50:
                if retry_count < 2:  # 최대 3회까지 시도
                    print(f"⚠️  {section_title}: 추출 실패, {retry_count+2}차 재시도...")
                    await asyncio.sleep(1)
                    return await extract_single_section(source_text, node, all_nodes, toc_structure, retry_count + 1)
                else:
                    return {
                        "node_id": node_id,
                        "section_title": section_title,
                        "content": "",
                        "status": "failed_after_retry",
                        "error": f"3회 시도 후에도 추출 실패: 내용 길이 {len(content)}",
                        "length": 0
                    }
            
            return {
                "node_id": node_id,
                "section_title": section_title,
                "content": content,
                "status": "success",
                "length": len(content)
            }
            
        except Exception as e:
            if retry_count < 2:
                print(f"⚠️  {section_title}: 예외 발생, {retry_count+2}차 재시도... ({e})")
                await asyncio.sleep(1)
                return await extract_single_section(source_text, node, all_nodes, toc_structure, retry_count + 1)
            else:
                return {
                    "node_id": node.get('id', ''),
                    "section_title": node.get('title', ''),
                    "content": "",
                    "status": "error",
                    "error": str(e),
                    "length": 0
                }
        finally:
            # 작업 완료 후 active_tasks에서 제거
            if current_task in active_tasks:
                active_tasks.remove(current_task)

def find_section_boundaries(current_node: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> Optional[str]:
    """현재 노드 이후에 오는 같은 레벨 또는 상위 레벨 섹션을 찾습니다."""
    current_id = current_node.get('id')
    current_level = current_node.get('level', 0)
    
    # ID 순으로 정렬된 노드에서 다음 섹션 찾기
    sorted_nodes = sorted(all_nodes, key=lambda x: x.get('id', 0))
    
    for i, node in enumerate(sorted_nodes):
        if node.get('id') == current_id and i < len(sorted_nodes) - 1:
            # 현재 노드 다음부터 검색
            for next_node in sorted_nodes[i+1:]:
                next_level = next_node.get('level', 0)
                # 같은 레벨 또는 상위 레벨인 경우
                if next_level <= current_level:
                    return next_node.get('title')
            break
    
    return None

async def extract_all_sections(source_file: str, nodes: List[Dict[str, Any]], toc_structure: str, output_dir: str) -> Dict[str, Any]:
    """
    모든 노드 섹션을 병렬로 추출
    
    Args:
        source_file: 원본 파일 경로
        nodes: 노드 데이터 리스트
        toc_structure: 목차 구조
        output_dir: 출력 디렉토리
    
    Returns:
        Dict with extraction summary
    """
    print(f"📖 원본 파일 읽는 중: {source_file}")
    
    # 원본 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    
    print(f"🎯 추출할 섹션 수: {len(nodes)}")
    
    # 병렬 추출 실행
    start_time = time.time()
    print("🚀 병렬 추출 시작...")
    
    # 모든 섹션을 병렬로 추출
    tasks = [
        extract_single_section(source_text, node, nodes, toc_structure) 
        for node in nodes
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed = time.time() - start_time
    
    # 결과 정리
    successful = [r for r in results if isinstance(r, dict) and r.get("status") == "success"]
    failed = [r for r in results if isinstance(r, dict) and r.get("status") in ["failed_after_retry", "error"]]
    exceptions = [r for r in results if isinstance(r, Exception)]
    
    print(f"✅ 병렬 추출 완료 ({elapsed:.1f}초)")
    print(f"   - 성공: {len(successful)}개")
    print(f"   - 실패: {len(failed)}개") 
    print(f"   - 예외: {len(exceptions)}개")
    
    # 개별 파일로 저장
    save_extracted_content(successful, output_dir)
    
    return {
        "total_sections": len(nodes),
        "successful": len(successful),
        "failed": len(failed),
        "exceptions": len(exceptions),
        "elapsed_time": elapsed,
        "results": results
    }

def save_extracted_content(successful_results: List[Dict[str, Any]], output_dir: str) -> None:
    """추출된 내용을 개별 파일로 저장합니다."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for result in successful_results:
        if result["content"]:
            # 파일명 생성 (node_id와 제목 기반)
            node_id = result["node_id"]
            title = result["section_title"]
            
            # 파일명 안전하게 변환
            safe_title = title.replace("/", "_").replace(":", "_").replace(" ", "_")
            safe_title = safe_title.replace("-", "_").replace("?", "").replace("!", "")
            
            filename = f"section_{node_id:02d}_{safe_title}.md"
            filepath = output_path / filename
            
            # 파일 내용 구성 (헤더 정보 포함)
            file_content = f"""# {title}

<!-- 추출 정보
노드 ID: {node_id}
제목: {title}
추출 길이: {result['length']:,}자
추출 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}
-->

{result['content']}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            print(f"💾 저장: {filename} ({result['length']:,}자)")

async def main():
    """메인 실행 함수"""
    global semaphore
    
    if len(sys.argv) < 4:
        print("사용법: python node_section_extractor.py <원문파일> <노드파일> <목차파일> [출력디렉토리]")
        print("예시: python node_section_extractor.py source.md script_node_structure.json table_of_contents.md ./extracted_sections")
        return
    
    # 자원 관리 설정
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 프로그램 종료 시 자동 정리
    atexit.register(cleanup_resources)
    
    source_file = sys.argv[1]
    nodes_file = sys.argv[2] 
    toc_file = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else "./extracted_sections"
    
    print("🎯 노드 기반 섹션 추출기 - Claude SDK")
    print("=" * 60)
    print(f"📄 원본 파일: {source_file}")
    print(f"📋 노드 파일: {nodes_file}")
    print(f"📑 목차 파일: {toc_file}")
    print(f"📂 출력 디렉토리: {output_dir}")
    
    # 파일 존재 확인
    for file_path in [source_file, nodes_file, toc_file]:
        if not Path(file_path).exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return
    
    # 노드와 목차 로드
    nodes = load_nodes(nodes_file)
    toc_structure = load_toc_structure(toc_file)
    
    if not nodes:
        print("❌ 노드 데이터를 로드할 수 없습니다.")
        return
    
    print(f"\n📊 노드 정보:")
    print(f"   - 총 노드 수: {len(nodes)}개")
    
    # 레벨별 통계
    level_counts = {}
    for node in nodes:
        level = node.get('level', 0)
        level_counts[level] = level_counts.get(level, 0) + 1
    
    for level in sorted(level_counts.keys()):
        print(f"   - Level {level}: {level_counts[level]}개")
    
    print("\n" + "=" * 60)
    
    try:
        # 섹션 추출 실행
        summary = await extract_all_sections(source_file, nodes, toc_structure, output_dir)
        
        print(f"\n📊 최종 결과:")
        print(f"   - 총 섹션: {summary['total_sections']}개")
        print(f"   - 성공: {summary['successful']}개")
        print(f"   - 실패: {summary['failed']}개")
        print(f"   - 소요 시간: {summary['elapsed_time']:.1f}초")
        
        # 실패한 섹션 상세 정보
        failed_results = [r for r in summary['results'] 
                         if isinstance(r, dict) and r.get("status") in ["failed_after_retry", "error"]]
        if failed_results:
            print(f"\n❌ 실패한 섹션들:")
            for result in failed_results:
                print(f"   - {result['section_title']}: {result.get('error', '알 수 없는 오류')}")
        
        print(f"\n✨ 작업 완료!")
        
    except Exception as e:
        print(f"❌ 전체 작업 실패: {e}")
    finally:
        # 작업 완료 후 자원 정리
        cleanup_resources()
        print(f"⚙️  최대 동시 작업 수: {MAX_CONCURRENT_TASKS}")

if __name__ == "__main__":
    anyio.run(main)