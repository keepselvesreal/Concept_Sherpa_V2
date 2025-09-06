#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 19:15:30 KST
핵심 내용: 간소화된 프롬프트를 사용하는 섹션 간 텍스트 추출기 v3 (상위 3개 노드 테스트용)
상세 내용:
- load_nodes (라인 35-50): 간소화된 JSON 노드 파일 로드 (상위 3개만)
- find_next_section_title (라인 55-80): 다음 섹션 제목 찾기
- extract_section_between (라인 85-170): 간소화된 프롬프트로 섹션 간 텍스트 추출
- process_single_node (라인 175-225): 단일 노드 처리 및 파일 저장
- process_all_nodes (라인 230-285): 모든 노드 병렬 처리
- main (라인 290-335): 메인 실행 함수 및 자원 관리
상태: v3 버전 - 간소화된 프롬프트 + 상위 3개 노드 테스트
주소: node_section_extractor_v3
참조: parallel_section_extractor.py의 간소화된 프롬프트 적용
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
MAX_CONCURRENT_TASKS = 3
active_tasks = set()
semaphore = None

def cleanup_resources():
    """자원 정리 함수"""
    global active_tasks
    print("\n🧹 자원 정리 중...")
    
    for task in list(active_tasks):
        if not task.done():
            task.cancel()
    
    active_tasks.clear()
    print("✅ 자원 정리 완료")

def signal_handler(signum, frame):
    """시그널 핸들러"""
    print(f"\n🛑 중단 신호 감지 (시그널 {signum})")
    cleanup_resources()
    sys.exit(0)

def load_nodes(nodes_file: str, limit: int = None) -> List[Dict[str, Any]]:
    """간소화된 JSON 파일에서 노드 데이터를 로드합니다 (상위 N개만)."""
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        # limit이 지정된 경우만 제한
        if limit is not None:
            limited_nodes = nodes[:limit]
            print(f"📊 로드된 노드 수: {len(limited_nodes)}개 (전체 {len(nodes)}개 중 상위 {limit}개)")
            return limited_nodes
        else:
            print(f"📊 로드된 노드 수: {len(nodes)}개 (전체)")
            return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 오류: {e}")
        return []

def find_next_section_title(nodes: List[Dict[str, Any]], current_id: int) -> Optional[str]:
    """현재 노드 다음의 섹션 제목을 찾습니다."""
    current_index = None
    
    for i, node in enumerate(nodes):
        if node.get('id') == current_id:
            current_index = i
            break
    
    if current_index is None or current_index >= len(nodes) - 1:
        return None
    
    next_node = nodes[current_index + 1]
    return next_node.get('title')

async def extract_section_between(source_text: str, current_title: str, next_title: Optional[str], node_id: int, retry_count: int = 0) -> Dict[str, Any]:
    """
    간소화된 프롬프트로 두 섹션 사이의 텍스트를 추출합니다.
    
    Args:
        source_text: 원본 텍스트
        current_title: 현재 섹션 제목
        next_title: 다음 섹션 제목
        node_id: 노드 ID
        retry_count: 재시도 횟수
    """
    global semaphore, active_tasks
    
    async with semaphore:
        current_task = asyncio.current_task()
        active_tasks.add(current_task)
        
        try:
            # 경계 설정
            if next_title:
                boundary_instruction = f'섹션은 "{current_title}" 부분부터 "{next_title}" 직전까지입니다.'
            else:
                boundary_instruction = f'섹션은 "{current_title}" 부분부터 문서의 끝까지입니다.'
            
            # 재시도별 프롬프트 강화
            retry_emphasis = ""
            if retry_count > 0:
                retry_emphasis = f"""
【재시도 {retry_count+1}회차】 이전 추출이 실패했습니다. 더 신중하게 접근해주세요:
- 섹션 제목을 정확히 찾아주세요
- 해당 섹션의 모든 내용을 누락 없이 포함해주세요
- 원본 텍스트 구조를 그대로 유지해주세요"""
            
            # 간소화된 프롬프트 (parallel_section_extractor.py 스타일)
            prompt = f"""다음 문서에서 "{current_title}" 섹션만 찾아서 그 내용을 완전히 추출해주세요.

【추출 대상】
- 목표 섹션: "{current_title}"
- {boundary_instruction}

{retry_emphasis}

【추출 규칙】
1. 섹션 제목이 정확히 일치하는 부분을 찾아주세요
2. 해당 섹션의 모든 내용을 누락 없이 포함해주세요  
3. 코드 예제, 대화, TIP 등 모든 요소를 포함해주세요
4. 원본 형태 그대로 반환하세요 (추가 설명 금지)

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
            if not extracted_content or len(extracted_content) < 50 or "Looking for section" in extracted_content:
                if retry_count < 2:  # 최대 3회까지 시도
                    print(f"⚠️  {current_title}: 추출 실패 (길이: {len(extracted_content)}), {retry_count+2}차 재시도...")
                    await asyncio.sleep(1)
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
            if current_task in active_tasks:
                active_tasks.remove(current_task)

async def process_single_node(node: Dict[str, Any], nodes: List[Dict[str, Any]], 
                              source_text: str, output_dir: Path) -> Dict[str, Any]:
    """단일 노드를 처리하여 섹션 간 텍스트를 추출하고 파일로 저장합니다."""
    node_id = node.get('id')
    title = node.get('title', 'Unknown')
    
    # 다음 섹션 제목 찾기
    next_title = find_next_section_title(nodes, node_id)
    
    # Claude SDK로 섹션 간 텍스트 추출
    result = await extract_section_between(source_text, title, next_title, node_id)
    
    if result["status"] == "success":
        # 파일명 생성 (level_title.md 형식)
        level = node.get('level')
        if level is None:
            raise ValueError(f"노드 ID {node_id}에 level 정보가 없습니다: {title}")
        
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"{level}_{safe_title}.md"
        
        file_path = output_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
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
                "filename": filename,
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
        print("사용법: python node_section_extractor_v3.py <노드파일> <원문파일> [출력디렉토리]")
        print("예시: python node_section_extractor_v3.py minimal_nodes.json source.md sections_v3/")
        print()
        print("기능: 간소화된 프롬프트로 상위 3개 노드의 섹션 간 텍스트 추출 (테스트용)")
        return
    
    # 시그널 핸들러 등록 및 자원 정리 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup_resources)
    
    # 세마포어 초기화
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    
    nodes_file = sys.argv[1]
    source_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "extracted_sections_v3"
    
    print("📄 섹션 간 텍스트 추출기 v3 (간소화된 프롬프트)")
    print("=" * 70)
    print(f"📋 노드 파일: {nodes_file}")
    print(f"📖 원문 파일: {source_file}")
    print(f"📁 출력 디렉토리: {output_dir}")
    print(f"🔧 최대 동시 작업: {MAX_CONCURRENT_TASKS}개")
    
    # 파일 존재 확인
    for file_path in [nodes_file, source_file]:
        if not Path(file_path).exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return
    
    # 노드 로드 (전체)
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("❌ 노드 데이터를 로드할 수 없습니다.")
        return
    
    print("\n" + "=" * 70)
    
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