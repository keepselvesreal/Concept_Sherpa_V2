#!/usr/bin/env python3
"""
# 생성 시간: 2025-08-10 23:45:00 KST
# 핵심 내용: Claude Code SDK로 7.3 섹션 추출
# 상세 내용: 
#   - extract_section_7_3 (line 15): 간단한 프롬프트로 7.3 섹션 추출
#   - main (line 50): 실행 함수
# 상태: active
# 주소: extract_7_3_claude_sdk
# 참조: 없음
"""

import anyio
from claude_code_sdk import query, ClaudeCodeOptions
from pathlib import Path
import time

async def extract_section_7_3(source_file: str) -> str:
    """Claude SDK로 7.3 섹션 추출"""
    
    # 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 간단한 프롬프트
    prompt = f"""다음 문서에서 "7.3 Schema flexibility and strictness" 섹션만 찾아서 그 내용을 완전히 추출해주세요.

섹션은 "7.3 Schema flexibility and strictness"로 시작해서 다음 섹션 "7.4 Schema composition" 직전까지입니다.

원본 텍스트 그대로 반환하세요. 추가 설명은 필요 없습니다.

{text}"""

    # Claude 호출
    messages = []
    async for message in query(
        prompt=prompt,
        options=ClaudeCodeOptions(
            max_turns=1,
            system_prompt="텍스트 추출 전문가. 요청된 섹션만 정확히 추출하여 반환하세요.",
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
    
    return response.strip()

async def main():
    """메인 함수"""
    print("🚀 Claude SDK로 7.3 섹션 추출")
    
    source_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    output_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/section_7_3_extracted.md"
    
    try:
        start_time = time.time()
        print("📖 추출 중...")
        
        content = await extract_section_7_3(source_file)
        
        if content:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            elapsed = time.time() - start_time
            print(f"✅ 완료! ({elapsed:.1f}초)")
            print(f"📄 길이: {len(content):,}자")
            print(f"💾 저장: {output_file}")
            
            # 미리보기
            preview = content[:300].replace('\n', ' ')
            print(f"📋 미리보기: {preview}...")
        else:
            print("❌ 추출 실패")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    anyio.run(main)