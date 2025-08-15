#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 19:05:45 KST
핵심 내용: fallback 로직이 추가된 섹션 간 텍스트 추출기 (Claude SDK 기반)
상세 내용:
- load_nodes (라인 35-50): 간소화된 JSON 노드 파일 로드
- find_next_section_title (라인 55-80): 다음 섹션 제목 찾기
- extract_section_between (라인 85-200): fallback 로직을 포함한 섹션 간 텍스트 추출
- process_single_node (라인 205-255): 단일 노드 처리 및 파일 저장
- process_all_nodes (라인 260-315): 모든 노드 병렬 처리
- main (라인 320-365): 메인 실행 함수 및 자원 관리
상태: fallback 로직 추가 완료
주소: node_section_extractor_v2_with_fallback
참조: 재시도 및 검증 로직 강화
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
MAX_CONCURRENT_TASKS = 3  # 최대 병렬 작업 수 (섹션 간 텍스트 추출용으로 낮춤)
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
    """간소화된 JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        print(f"📊 로드된 노드 수: {len(nodes)}개")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 오류: {e}")
        return []

def find_next_section_title(nodes: List[Dict[str, Any]], current_id: int) -> Optional[str]:
    """현재 노드 다음의 섹션 제목을 찾습니다."""
    current_index = None
    
    # 현재 노드의 인덱스 찾기
    for i, node in enumerate(nodes):
        if node.get('id') == current_id:
            current_index = i
            break
    
    if current_index is None or current_index >= len(nodes) - 1:
        return None
    
    # 다음 노드의 제목 반환
    next_node = nodes[current_index + 1]
    return next_node.get('title')

async def extract_section_between(source_text: str, current_title: str, next_title: Optional[str], node_id: int, retry_count: int = 0) -> Dict[str, Any]:
    """
    Claude SDK를 사용하여 두 섹션 사이의 텍스트만 추출합니다.
    
    Args:
        source_text: 원본 텍스트
        current_title: 현재 섹션 제목
        next_title: 다음 섹션 제목 (None이면 문서 끝까지)
        node_id: 노드 ID
        retry_count: 재시도 횟수
    
    Returns:
        추출 결과 딕셔너리
    """
    global semaphore, active_tasks
    
    # 세마포어를 사용하여 동시 실행 작업 수 제한
    async with semaphore:
        current_task = asyncio.current_task()
        active_tasks.add(current_task)
        
        try:
            # 경계 설정 지시사항
            if next_title:
                boundary_instruction = f'"{current_title}" 섹션 헤더 바로 다음부터 "{next_title}" 섹션 헤더 바로 전까지의 텍스트만 추출해주세요.'
                extraction_scope = f'"{current_title}" 섹션과 "{next_title}" 사이'
            else:
                boundary_instruction = f'"{current_title}" 섹션 헤더 바로 다음부터 문서 끝까지의 텍스트를 추출해주세요.'
                extraction_scope = f'"{current_title}" → 문서 끝'
            
            # 재시도별 프롬프트 강화
            retry_emphasis = ""
            if retry_count > 0:
                retry_emphasis = f"""
【재시도 {retry_count+1}회차】 이전 추출이 실패했습니다. 더 신중하게 접근해주세요:
- 섹션 제목을 정확히 찾아주세요 (대소문자, 구두점 주의)
- 섹션 헤더는 제외하고 그 다음 줄부터 추출해주세요
- 원본 텍스트 구조를 그대로 유지해주세요
- 빈 줄이나 공백도 원본 그대로 보존해주세요"""
            
            prompt = f"""다음 문서에서 특정 섹션 헤더 사이의 텍스트만 정확히 추출해주세요.

【추출 대상】
- 목표: {extraction_scope}
- {boundary_instruction}

{retry_emphasis}

【추출 규칙】
1. 섹션 제목이 정확히 일치하는 부분을 찾아주세요
2. 섹션 헤더 자체는 제외하고, 그 바로 다음 줄부터의 내용만 추출
3. 하위 섹션 헤더들과 그 내용은 포함
4. 다음 동일 레벨 섹션 헤더가 나오면 그 직전까지만
5. 원본 마크다운 형식을 그대로 유지
6. 빈 줄이나 공백도 원본 그대로 보존
7. 추가 설명이나 주석 없이 해당 텍스트만 반환

【예시】
만약 "## Introduction" 다음에 "## Next Section"이 있다면:
- "## Introduction" 라인은 제외
- 그 다음 줄부터 "## Next Section" 직전 줄까지만 추출

【추출할 텍스트】
{current_title} 섹션과 {next_title if next_title else '문서 끝'} 사이의 내용

【원본 문서】
{source_text}"""

            # Claude 호출
            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="문서 섹션 분석 전문가. 지정된 섹션 경계 사이의 텍스트만 정확히 추출하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            # 응답 추출
            extracted_content = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                extracted_content += block.text
                    else:
                        extracted_content += str(message.content)
            
            extracted_content = extracted_content.strip()
            
            # 추출 결과 검증 및 fallback
            if not extracted_content or len(extracted_content) < 20 or "섹션을 찾을 수 없습니다" in extracted_content or "Looking for section" in extracted_content:
                if retry_count < 2:  # 최대 3회까지 시도
                    print(f"⚠️  {current_title}: 추출 실패 (길이: {len(extracted_content)}), {retry_count+2}차 재시도...")
                    await asyncio.sleep(1)  # 잠깐 대기
                    return await extract_section_between(source_text, current_title, next_title, node_id, retry_count + 1)
                else:
                    return {
                        "node_id": node_id,
                        "current_title": current_title,
                        "next_title": next_title,
                        "content": "",
                        "content_length": 0,
                        "status": "failed_after_retry",
                        "error": f"3회 시도 후에도 추출 실패: 내용 길이 {len(extracted_content)}"
                    }
            
            return {
                "node_id": node_id,
                "current_title": current_title,
                "next_title": next_title,
                "content": extracted_content,
                "content_length": len(extracted_content),
                "status": "success"
            }
            
        except Exception as e:
            if retry_count < 2:
                print(f"⚠️  {current_title}: 예외 발생 ({e}), {retry_count+2}차 재시도...")
                await asyncio.sleep(1)
                return await extract_section_between(source_text, current_title, next_title, node_id, retry_count + 1)
            else:
                return {
                    "node_id": node_id,
                    "current_title": current_title,
                    "next_title": next_title,
                    "content": "",
                    "content_length": 0,
                    "status": "error",
                    "error": str(e)
                }
        finally:
            # 작업 완료 시 active_tasks에서 제거
            if current_task in active_tasks:
                active_tasks.remove(current_task)

async def process_single_node(node: Dict[str, Any], nodes: List[Dict[str, Any]], 
                              source_text: str, output_dir: Path) -> Dict[str, Any]:
    """
    단일 노드를 처리하여 섹션 간 텍스트를 추출하고 파일로 저장합니다.
    """
    node_id = node.get('id')
    title = node.get('title', 'Unknown')
    
    # 다음 섹션 제목 찾기
    next_title = find_next_section_title(nodes, node_id)
    
    # Claude SDK로 섹션 간 텍스트 추출
    result = await extract_section_between(source_text, title, next_title, node_id)
    
    if result["status"] == "success":
        # 파일명 생성 (제목을 파일명으로 사용)
        safe_filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_filename = safe_filename.replace(' ', '_')
        filename = f"{safe_filename}.md"
        
        # 파일 경로
        file_path = output_dir / filename
        
        try:
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                if result["content"]:
                    f.write(result["content"])
                else:
                    f.write("*섹션 간 내용이 비어있습니다.*")
            
            text_length = result["content_length"]
            
            print(f"✅ 저장: {filename} ({text_length:,}자)")
            
            return {
                "id": node_id,
                "title": title,
                "filename": filename,
                "text_length": text_length,
                "status": "success",
                "has_content": bool(result["content"])
            }
            
        except Exception as e:
            return {
                "id": node_id,
                "title": title,
                "filename": f"{safe_filename}.md",
                "text_length": 0,
                "status": "error",
                "error": f"파일 저장 실패: {e}"
            }
    else:
        print(f"❌ 실패: {title} - {result.get('error', '알 수 없는 오류')}")
        return {
            "id": node_id,
            "title": title,
            "filename": "",
            "text_length": 0,
            "status": result["status"],
            "error": result.get("error", "추출 실패")
        }

async def process_all_nodes(nodes: List[Dict[str, Any]], source_file: str, output_dir: str) -> Dict[str, Any]:
    """모든 노드를 병렬로 처리합니다."""
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 원본 파일 읽는 중: {source_file}")
    
    # 원본 텍스트 로드
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_text = f.read()
    except Exception as e:
        print(f"❌ 원본 파일 로드 실패: {e}")
        return {"status": "error", "error": str(e)}
    
    print(f"🚀 섹션 간 텍스트 추출 시작 ({len(nodes)}개 노드)")
    start_time = time.time()
    
    # 모든 노드를 병렬로 처리
    tasks = []
    for node in nodes:
        task = asyncio.create_task(
            process_single_node(node, nodes, source_text, output_path),
            name=f"extract_node_{node.get('id', 'unknown')}"
        )
        tasks.append(task)
    
    # 모든 작업 완료 대기
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed = time.time() - start_time
    
    # 결과 처리
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            node = nodes[i]
            processed_results.append({
                "id": node.get('id'),
                "title": node.get('title', 'Unknown'),
                "status": "error",
                "error": str(result)
            })
        else:
            processed_results.append(result)
    
    # 결과 집계
    successful = [r for r in processed_results if r.get("status") == "success"]
    with_content = [r for r in successful if r.get("has_content", False)]
    empty_content = [r for r in successful if not r.get("has_content", False)]
    failed_retry = [r for r in processed_results if r.get("status") == "failed_after_retry"]
    failed = [r for r in processed_results if r.get("status") == "error"]
    
    print(f"\n✅ 처리 완료 ({elapsed:.1f}초)")
    print(f"   - 총 노드: {len(nodes)}개")
    print(f"   - 성공: {len(successful)}개")
    print(f"   - 내용 있음: {len(with_content)}개")
    print(f"   - 비어있음: {len(empty_content)}개")
    print(f"   - 재시도 후 실패: {len(failed_retry)}개")
    print(f"   - 오류: {len(failed)}개")
    
    if failed_retry or failed:
        print(f"\n❌ 실패한 노드:")
        for fail in failed_retry + failed:
            print(f"   - {fail.get('title', 'Unknown')}: {fail.get('error', 'Unknown error')}")
    
    return {
        "total_nodes": len(nodes),
        "successful": len(successful),
        "with_content": len(with_content),
        "empty_content": len(empty_content),
        "failed_retry": len(failed_retry),
        "failed": len(failed),
        "elapsed_time": elapsed,
        "results": processed_results
    }

async def main():
    """메인 실행 함수"""
    global semaphore
    
    if len(sys.argv) < 3:
        print("사용법: python node_section_extractor_v2.py <노드파일> <원문파일> [출력디렉토리]")
        print("예시: python node_section_extractor_v2.py minimal_nodes.json source.md sections_v2/")
        print()
        print("기능: fallback 로직을 포함한 Claude SDK 기반 섹션 간 텍스트 추출")
        return
    
    # 시그널 핸들러 등록 및 자원 정리 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup_resources)
    
    # 세마포어 초기화
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    
    nodes_file = sys.argv[1]
    source_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "extracted_sections_v2_fallback"
    
    print("📄 섹션 간 텍스트 추출기 v2 (Claude SDK + Fallback)")
    print("=" * 60)
    print(f"📋 노드 파일: {nodes_file}")
    print(f"📖 원문 파일: {source_file}")
    print(f"📁 출력 디렉토리: {output_dir}")
    print(f"🔧 최대 동시 작업: {MAX_CONCURRENT_TASKS}개")
    print(f"🔄 재시도 횟수: 최대 3회")
    
    # 파일 존재 확인
    for file_path in [nodes_file, source_file]:
        if not Path(file_path).exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return
    
    # 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("❌ 노드 데이터를 로드할 수 없습니다.")
        return
    
    print("\n" + "=" * 60)
    
    try:
        # 모든 노드 처리
        results = await process_all_nodes(nodes, source_file, output_dir)
        
        total_failed = results.get("failed_retry", 0) + results.get("failed", 0)
        if total_failed == 0:
            print(f"\n✨ 모든 작업 완료! 결과가 '{output_dir}' 디렉토리에 저장되었습니다.")
        else:
            print(f"\n⚠️  일부 작업 실패: {total_failed}개 노드 처리 실패")
    
    except Exception as e:
        print(f"\n❌ 전체 작업 실패: {e}")
    
    finally:
        cleanup_resources()

if __name__ == "__main__":
    anyio.run(main)