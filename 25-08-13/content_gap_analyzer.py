#!/usr/bin/env python3

"""
생성 시간: 2025년 8월 13일 17:52:18 KST
핵심 내용: 상위-하위 노드 간 내용 존재 여부를 확인하여 has_content 필드를 추가하는 스크립트
상세 내용:
- load_nodes (라인 30-45): JSON 노드 파일 로드
- identify_parent_child_gaps (라인 50-75): 상위-하위 노드 간격 식별
- check_content_exists (라인 80-130): Claude SDK를 통한 내용 존재 확인
- analyze_content_gaps (라인 135-170): 모든 간격에 대한 내용 분석
- save_updated_nodes (라인 175-190): has_content 필드가 추가된 노드 저장
- main (라인 195-230): 메인 실행 함수 및 CLI 인터페이스
상태: 스크립트 작성 완료
주소: content_gap_analyzer
참조: 노드 구조와 원문을 기반으로 한 내용 간격 분석
"""

import anyio
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from claude_code_sdk import query, ClaudeCodeOptions

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

def identify_parent_child_gaps(nodes: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """상위-하위 노드 간격을 식별합니다."""
    
    # 노드를 ID 순서대로 정렬
    sorted_nodes = sorted(nodes, key=lambda x: x.get('id', 0))
    
    gaps = []
    
    for i in range(len(sorted_nodes) - 1):
        current_node = sorted_nodes[i]
        next_node = sorted_nodes[i + 1]
        
        current_level = current_node.get('level', 0)
        next_level = next_node.get('level', 0)
        
        # 상위 노드 - 하위 노드인 경우 (현재 레벨 < 다음 레벨)
        if current_level < next_level:
            gaps.append((current_node, next_node))
    
    return gaps

def basic_content_check(source_text: str, parent_title: str, child_title: str) -> Optional[bool]:
    """
    기본적인 텍스트 분석으로 내용 존재 여부를 확인합니다.
    
    Returns:
        True: 확실히 내용 있음
        False: 확실히 내용 없음  
        None: 판단 불가 (AI 분석 필요)
    """
    lines = source_text.split('\n')
    
    # 상위 섹션과 하위 섹션의 위치 찾기
    parent_idx = None
    child_idx = None
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if parent_title in line_stripped and (line_stripped.startswith('#') or line_stripped.startswith('##')):
            parent_idx = i
        elif child_title in line_stripped and (line_stripped.startswith('#') or line_stripped.startswith('##')):
            child_idx = i
            break
    
    # 섹션을 찾지 못한 경우
    if parent_idx is None or child_idx is None:
        return None
    
    # 상위 섹션 다음 줄부터 하위 섹션 이전 줄까지 확인
    content_lines = lines[parent_idx + 1:child_idx]
    
    # 빈 줄과 공백만 있는지 확인
    has_meaningful_content = False
    for line in content_lines:
        stripped = line.strip()
        if stripped:  # 비어있지 않은 줄이 있으면
            has_meaningful_content = True
            break
    
    return has_meaningful_content

async def check_content_exists(source_text: str, parent_node: Dict[str, Any], child_node: Dict[str, Any]) -> Dict[str, Any]:
    """
    상위-하위 노드 사이에 내용이 존재하는지 확인합니다.
    먼저 기본 검증을 수행하고, 판단이 어려운 경우만 Claude SDK를 사용합니다.
    
    Args:
        source_text: 원본 텍스트
        parent_node: 상위 노드
        child_node: 하위 노드
        
    Returns:
        Dict with analysis result
    """
    try:
        parent_title = parent_node.get('title', '')
        child_title = child_node.get('title', '')
        parent_level = parent_node.get('level', 0)
        child_level = child_node.get('level', 0)
        
        # 1. 기본 검증 먼저 수행
        basic_result = basic_content_check(source_text, parent_title, child_title)
        
        if basic_result is not None:
            # 기본 검증으로 판단 가능한 경우
            method = "기본 텍스트 분석"
            analysis = f"기본 검증: {'내용 있음' if basic_result else '빈 줄/공백만 있음'}"
            
            return {
                "parent_node": parent_node,
                "child_node": child_node,
                "has_content": basic_result,
                "analysis": analysis,
                "method": method,
                "status": "success"
            }
        
        # 2. 기본 검증으로 판단이 어려운 경우만 AI 분석 수행
        prompt = f"""다음 문서에서 "{parent_title}" 섹션과 "{child_title}" 섹션 사이에 의미있는 내용이 존재하는지 분석해주세요.

【분석 대상】
- 상위 섹션: "{parent_title}" (레벨 {parent_level})
- 하위 섹션: "{child_title}" (레벨 {child_level})

【중요】
- 빈 줄이나 공백만 있는 경우: 내용 없음
- 섹션 헤더만 있고 바로 하위 섹션이 시작되는 경우: 내용 없음  
- 도입부 문장이나 개요 설명이 있는 경우: 내용 있음

【응답 형식】
반드시 "YES" 또는 "NO"로만 답변하세요.
- YES: 의미있는 내용이 존재
- NO: 내용 없음 (빈 줄/공백만 있음)

【원본 문서】
{source_text}"""

        # Claude 호출
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="문서 구조 분석 전문가. 섹션 간 내용 존재 여부를 정확히 판단하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        # 응답 추출
        response = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            response += block.text
                else:
                    response += str(message.content)
        
        response = response.strip()
        
        # 응답 분석 (YES/NO 형식)
        response_upper = response.upper().strip()
        has_content = False
        method = "AI 분석"
        
        if response_upper.startswith("YES"):
            has_content = True
        elif response_upper.startswith("NO"):
            has_content = False
        else:
            # 응답 형식이 맞지 않는 경우 재시도
            print(f"⚠️  응답 형식 오류, 재시도: {parent_title} -> {child_title} (응답: {response[:50]}...)")
            
            # 더 명확한 프롬프트로 재시도
            retry_prompt = f""""{parent_title}" 섹션과 "{child_title}" 섹션 사이에 내용이 있습니까?

반드시 "YES" 또는 "NO"로만 답변하세요.

문서:
{source_text[:2000]}..."""
            
            try:
                retry_messages = []
                async for message in query(
                    prompt=retry_prompt,
                    options=ClaudeCodeOptions(
                        max_turns=1,
                        system_prompt="YES 또는 NO로만 답변하세요.",
                        allowed_tools=[]
                    )
                ):
                    retry_messages.append(message)
                
                # 재시도 응답 추출
                retry_response = ""
                for message in retry_messages:
                    if hasattr(message, 'content'):
                        if isinstance(message.content, list):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    retry_response += block.text
                        else:
                            retry_response += str(message.content)
                
                retry_response_upper = retry_response.upper().strip()
                
                if retry_response_upper.startswith("YES"):
                    has_content = True
                    method = "AI 분석 (재시도 성공)"
                elif retry_response_upper.startswith("NO"):
                    has_content = False
                    method = "AI 분석 (재시도 성공)"
                else:
                    # 재시도도 실패한 경우 보수적으로 내용 없음으로 판단
                    has_content = False
                    method = "AI 분석 (재시도 실패, 기본값 적용)"
                    print(f"⚠️  재시도도 실패: {retry_response[:50]}...")
                    
            except Exception as retry_e:
                # 재시도 중 오류 발생시 보수적으로 내용 없음으로 판단
                has_content = False
                method = f"AI 분석 (재시도 오류: {str(retry_e)[:30]}...)"
                print(f"⚠️  재시도 오류: {retry_e}")
        
        return {
            "parent_node": parent_node,
            "child_node": child_node,
            "has_content": has_content,
            "analysis": response,
            "method": method,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "parent_node": parent_node,
            "child_node": child_node,
            "has_content": False,
            "analysis": f"분석 오류: {str(e)}",
            "status": "error"
        }

async def analyze_content_gaps(source_file: str, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    모든 상위-하위 노드 간격에 대해 내용 존재 여부를 분석합니다.
    
    Args:
        source_file: 원본 파일 경로
        nodes: 노드 리스트
        
    Returns:
        분석 결과 딕셔너리
    """
    print(f"📖 원본 파일 읽는 중: {source_file}")
    
    # 원본 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    
    # 상위-하위 노드 간격 식별
    gaps = identify_parent_child_gaps(nodes)
    print(f"🔍 식별된 상위-하위 노드 간격: {len(gaps)}개")
    
    if not gaps:
        print("📋 상위-하위 노드 간격이 없습니다.")
        return {
            "total_gaps": 0,
            "analyzed": 0,
            "content_exists": 0,
            "no_content": 0,
            "results": []
        }
    
    # 간격 정보 출력
    for i, (parent, child) in enumerate(gaps, 1):
        print(f"   {i}. {parent['title']} (L{parent['level']}) → {child['title']} (L{child['level']})")
    
    print(f"\n🚀 내용 존재 분석 시작...")
    start_time = time.time()
    
    # 모든 간격을 순차적으로 분석 (API 제한 고려)
    results = []
    for i, (parent, child) in enumerate(gaps, 1):
        print(f"🔄 분석 중 ({i}/{len(gaps)}): {parent['title']} → {child['title']}")
        
        result = await check_content_exists(source_text, parent, child)
        results.append(result)
        
        # API 제한을 고려한 딜레이
        if i < len(gaps):
            await asyncio.sleep(1)
    
    elapsed = time.time() - start_time
    
    # 결과 정리
    successful = [r for r in results if r.get("status") == "success"]
    content_exists = [r for r in successful if r.get("has_content") == True]
    no_content = [r for r in successful if r.get("has_content") == False]
    
    print(f"✅ 분석 완료 ({elapsed:.1f}초)")
    print(f"   - 총 간격: {len(gaps)}개")
    print(f"   - 내용 존재: {len(content_exists)}개")
    print(f"   - 내용 없음: {len(no_content)}개")
    
    return {
        "total_gaps": len(gaps),
        "analyzed": len(successful),
        "content_exists": len(content_exists),
        "no_content": len(no_content),
        "elapsed_time": elapsed,
        "results": results
    }

def save_updated_nodes(nodes: List[Dict[str, Any]], analysis_results: Dict[str, Any], output_file: str) -> None:
    """has_content 필드가 추가된 노드를 저장합니다."""
    
    # 결과에서 has_content 정보 추출
    content_map = {}
    for result in analysis_results.get("results", []):
        if result.get("status") == "success":
            parent_id = result["parent_node"].get("id")
            content_map[parent_id] = result.get("has_content", False)
    
    # 노드에 has_content 필드 추가
    updated_nodes = []
    for node in nodes:
        updated_node = node.copy()
        node_id = node.get("id")
        
        if node_id in content_map:
            updated_node["has_content"] = content_map[node_id]
            print(f"📝 {node['title']}: has_content = {content_map[node_id]}")
        
        updated_nodes.append(updated_node)
    
    # 파일 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
        
        print(f"💾 업데이트된 노드 저장: {output_file}")
        
    except Exception as e:
        print(f"❌ 파일 저장 오류: {e}")

async def main():
    """메인 실행 함수"""
    if len(sys.argv) < 3:
        print("사용법: python content_gap_analyzer.py <원문파일> <노드파일> [출력파일]")
        print("예시: python content_gap_analyzer.py source.md script_node_structure.json updated_nodes.json")
        return
    
    source_file = sys.argv[1]
    nodes_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else f"{Path(nodes_file).stem}_with_content.json"
    
    print("🔍 상위-하위 노드 간 내용 존재 분석기")
    print("=" * 60)
    print(f"📄 원본 파일: {source_file}")
    print(f"📋 노드 파일: {nodes_file}")
    print(f"📁 출력 파일: {output_file}")
    
    # 파일 존재 확인
    for file_path in [source_file, nodes_file]:
        if not Path(file_path).exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return
    
    # 노드 로드
    nodes = load_nodes(nodes_file)
    if not nodes:
        print("❌ 노드 데이터를 로드할 수 없습니다.")
        return
    
    print(f"\n📊 노드 정보:")
    print(f"   - 총 노드 수: {len(nodes)}개")
    
    print("\n" + "=" * 60)
    
    try:
        # 내용 간격 분석
        analysis_results = await analyze_content_gaps(source_file, nodes)
        
        if analysis_results["total_gaps"] > 0:
            # 업데이트된 노드 저장
            save_updated_nodes(nodes, analysis_results, output_file)
            
            print(f"\n📊 최종 결과:")
            print(f"   - 분석된 간격: {analysis_results['analyzed']}개")
            print(f"   - 내용 존재: {analysis_results['content_exists']}개")
            print(f"   - 내용 없음: {analysis_results['no_content']}개")
            print(f"   - 소요 시간: {analysis_results['elapsed_time']:.1f}초")
        
        print(f"\n✨ 작업 완료!")
        
    except Exception as e:
        print(f"❌ 전체 작업 실패: {e}")

if __name__ == "__main__":
    anyio.run(main)