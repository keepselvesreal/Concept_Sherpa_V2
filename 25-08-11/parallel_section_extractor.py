#!/usr/bin/env python3
"""
생성 시간: 2025-08-11 09:33:12 KST
핵심 내용: 병렬 섹션 추출기 - Claude SDK 기반으로 원문에서 여러 섹션을 병렬로 추출
상세 내용:
    - extract_single_section (20-80행): 단일 섹션을 Claude SDK로 추출하는 함수
    - extract_sections_parallel (82-120행): 여러 섹션을 병렬로 추출하는 메인 함수
    - create_sample_sections_json (122-140행): 예시용 JSON 데이터 생성 함수
    - main (142-200행): 실행 및 테스트 함수
상태: 활성
주소: parallel_section_extractor
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/extract_7_3_claude_sdk.py
"""

import anyio
import asyncio
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from claude_code_sdk import query, ClaudeCodeOptions

async def extract_single_section(source_text: str, section_title: str, section_list: List[str], retry_count: int = 0) -> Dict[str, Any]:
    """
    단일 섹션을 Claude SDK로 추출
    
    Args:
        source_text: 원본 텍스트
        section_title: 추출할 섹션 제목
        section_list: 전체 섹션 목록 (다음 섹션 찾기용)
        retry_count: 재시도 횟수
    
    Returns:
        Dict with section_title, content, status
    """
    try:
        # 다음 섹션 찾기 (섹션 경계 확정용)
        current_idx = next((i for i, title in enumerate(section_list) if title == section_title), -1)
        next_section = section_list[current_idx + 1] if current_idx != -1 and current_idx < len(section_list) - 1 else None
        
        # 목차 맥락 생성
        toc_context = "\n".join([f"{i+1}. {title}" for i, title in enumerate(section_list)])
        
        # Introduction 섹션 처리 안내
        introduction_note = ""
        if "Introduction" in section_title:
            introduction_note = """
【중요】 이 섹션은 "Introduction"이지만 실제 문서에는 이 제목이 명시되어 있지 않을 수 있습니다.
대신 장(Chapter) 제목 바로 다음에 오는 도입부 내용이나 첫 번째 하위 섹션 이전의 모든 내용을 찾아주세요."""
        
        # 경계 설정
        if next_section:
            boundary_instruction = f'섹션은 "{section_title}" 부분부터 "{next_section}" 직전까지입니다.'
        else:
            boundary_instruction = f'섹션은 "{section_title}" 부분부터 문서의 끝까지입니다.'
        
        # 재시도별 프롬프트 강화
        retry_emphasis = ""
        if retry_count > 0:
            retry_emphasis = f"""
【재시도 {retry_count+1}회차】 이전 추출이 실패했습니다. 더 신중하게 접근해주세요:
- 섹션 제목을 정확히 찾아주세요
- 해당 섹션의 모든 내용을 누락 없이 포함해주세요
- 원본 텍스트 구조를 그대로 유지해주세요"""
        
        prompt = f"""다음 문서에서 "{section_title}" 섹션만 찾아서 그 내용을 완전히 추출해주세요.

【문서 전체 구조】
{toc_context}

【추출 대상】
- 목표 섹션: "{section_title}"
- {boundary_instruction}

{introduction_note}

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
        
        # 추출 결과 검증 및 fallback
        if not content or len(content) < 50 or "Looking for section" in content:
            if retry_count < 2:  # 최대 3회까지 시도
                print(f"⚠️  {section_title}: 추출 실패, {retry_count+2}차 재시도...")
                await asyncio.sleep(1)  # 잠깐 대기
                return await extract_single_section(source_text, section_title, section_list, retry_count + 1)
            else:
                return {
                    "section_title": section_title,
                    "content": "",
                    "status": "failed_after_retry",
                    "error": f"3회 시도 후에도 추출 실패: 내용 길이 {len(content)}",
                    "length": 0
                }
        
        return {
            "section_title": section_title,
            "content": content,
            "status": "success",
            "length": len(content)
        }
        
    except Exception as e:
        if retry_count < 2:
            print(f"⚠️  {section_title}: 예외 발생, {retry_count+2}차 재시도... ({e})")
            await asyncio.sleep(1)
            return await extract_single_section(source_text, section_title, section_list, retry_count + 1)
        else:
            return {
                "section_title": section_title,
                "content": "",
                "status": "error",
                "error": str(e),
                "length": 0
            }

async def extract_sections_parallel(source_file: str, sections_data: List[Dict[str, Any]], output_dir: str = None) -> Dict[str, Any]:
    """
    여러 섹션을 병렬로 추출
    
    Args:
        source_file: 원본 파일 경로
        sections_data: 섹션 데이터 (title 필드 포함)
        output_dir: 출력 디렉토리 (None이면 개별 파일 저장 안 함)
    
    Returns:
        Dict with results summary
    """
    print(f"📖 원본 파일 읽는 중: {source_file}")
    
    # 원본 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    
    # 섹션 제목 리스트 생성
    section_titles = [item["title"] for item in sections_data]
    print(f"🎯 추출할 섹션 수: {len(section_titles)}")
    
    # 병렬 추출 실행
    start_time = time.time()
    print("🚀 병렬 추출 시작...")
    
    # 모든 섹션을 병렬로 추출
    tasks = [
        extract_single_section(source_text, title, section_titles) 
        for title in section_titles
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed = time.time() - start_time
    
    # 결과 정리
    successful = [r for r in results if isinstance(r, dict) and r.get("status") == "success"]
    failed = [r for r in results if isinstance(r, dict) and r.get("status") == "error"]
    exceptions = [r for r in results if isinstance(r, Exception)]
    
    print(f"✅ 병렬 추출 완료 ({elapsed:.1f}초)")
    print(f"   - 성공: {len(successful)}개")
    print(f"   - 실패: {len(failed)}개")
    print(f"   - 예외: {len(exceptions)}개")
    
    # 개별 파일로 저장 (output_dir 지정된 경우)
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for result in successful:
            if result["content"]:
                # 파일명 안전하게 변환
                safe_title = result["section_title"].replace("/", "_").replace(":", "_").replace(" ", "_")
                filename = f"{safe_title}.md"
                filepath = output_path / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(result["content"])
                
                print(f"💾 저장: {filename} ({result['length']:,}자)")
    
    return {
        "total_sections": len(section_titles),
        "successful": len(successful),
        "failed": len(failed),
        "exceptions": len(exceptions),
        "elapsed_time": elapsed,
        "results": results
    }

def create_sample_sections_json() -> List[Dict[str, Any]]:
    """7장 섹션들을 위한 샘플 JSON 데이터 생성"""
    return [
        {"title": "7 Introduction"},
        {"title": "7.1 Data validation in DOP"},
        {"title": "7.2 JSON Schema in a nutshell"},
        {"title": "7.3 Schema flexibility and strictness"},
        {"title": "7.4 Schema composition"},
        {"title": "7.5 Details about data validation failures"},
        {"title": "Summary"}
    ]

async def main():
    """메인 실행 함수"""
    print("🎯 병렬 섹션 추출기 - Claude SDK")
    print("=" * 50)
    
    # 예시 데이터 설정
    source_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    sections_data = create_sample_sections_json()
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-11/extracted_sections"
    
    # 소스 파일 존재 확인
    if not Path(source_file).exists():
        print(f"❌ 원본 파일을 찾을 수 없습니다: {source_file}")
        return
    
    print(f"📁 원본: {Path(source_file).name}")
    print(f"📂 출력: {output_dir}")
    print(f"📄 섹션 데이터:")
    for i, section in enumerate(sections_data, 1):
        print(f"   {i}. {section['title']}")
    
    print("\n" + "=" * 50)
    
    try:
        # 병렬 추출 실행
        summary = await extract_sections_parallel(source_file, sections_data, output_dir)
        
        print(f"\n📊 최종 결과:")
        print(f"   - 총 섹션: {summary['total_sections']}개")
        print(f"   - 성공: {summary['successful']}개")
        print(f"   - 실패: {summary['failed']}개")
        print(f"   - 소요 시간: {summary['elapsed_time']:.1f}초")
        
        # 실패한 섹션이 있으면 상세 정보 출력
        failed_results = [r for r in summary['results'] if isinstance(r, dict) and r.get("status") == "error"]
        if failed_results:
            print(f"\n❌ 실패한 섹션들:")
            for result in failed_results:
                print(f"   - {result['section_title']}: {result.get('error', '알 수 없는 오류')}")
        
        print(f"\n✨ 작업 완료!")
        
    except Exception as e:
        print(f"❌ 전체 작업 실패: {e}")

if __name__ == "__main__":
    anyio.run(main)