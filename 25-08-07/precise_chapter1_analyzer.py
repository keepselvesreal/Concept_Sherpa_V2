# 목차
# - 생성 시간: 2025-08-07 13:45:30 KST
# - 핵심 내용: Chapter 1의 정확한 구조 분석 및 Introduction 필요 부분 판단
# - 상세 내용: 페이지별 구조 분석으로 Introduction 필요 여부를 정밀 판단
# - 상태: 활성
# - 주소: precise_chapter1_analyzer
# - 참조: chapter1_extracted.md, core_toc_with_page_ranges.json

import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

async def analyze_chapter1_structure(chapter1_content: str):
    """Chapter 1 구조를 정확히 분석하여 Introduction 필요 부분 판단"""
    
    prompt = f"""다음은 Chapter 1 전체 내용입니다. 정확한 구조 분석을 수행하세요:

{chapter1_content}

**목차 정보 (core_toc_with_page_ranges.json 기준):**
- Chapter 1: 페이지 31-53
- Section 1.1: 페이지 32-40  
- Subsection 1.1.1: 페이지 32-33
- Section 1.2: 페이지 41-51
- Subsection 1.2.1: 페이지 42-43

**엄격한 분석 규칙:**

1. **Chapter 1과 Section 1.1 사이 (페이지 31 ~ Section 1.1 시작 전)**
   - 텍스트 내용이 있으면 → "1.0 Introduction" 필요

2. **Section 1.1과 Subsection 1.1.1 사이 (Section 1.1 시작 ~ Subsection 1.1.1 시작 전)**
   - 텍스트 내용이 있으면 → "1.1.0 Introduction" 필요

3. **Section 1.2와 Subsection 1.2.1 사이 (Section 1.2 시작 ~ Subsection 1.2.1 시작 전)**
   - 텍스트 내용이 있으면 → "1.2.0 Introduction" 필요

**페이지 표시를 기준으로 구조를 정확히 파악하고, 오직 실제 텍스트 내용 존재 여부만으로 판단하세요.**

**출력 형식:**
실제로 내용이 존재하는 경우만 나열:
- 1.0 Introduction (페이지 31-32)
- 1.1.0 Introduction (페이지 32)  
- 1.2.0 Introduction (페이지 41-42)

각각에 대해 어떤 내용이 있는지 간단히 설명하세요."""

    try:
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="페이지 구조를 정확히 분석하여 텍스트 내용의 실제 존재 여부만을 판단하는 정밀 분석가입니다."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        full_response = "\n".join(responses) if responses else ""
        return full_response
        
    except Exception as e:
        print(f"❌ 정밀 분석 실패: {e}")
        return ""

async def main():
    print("🚀 Chapter 1 정밀 구조 분석...")
    
    # Chapter 1 파일 로드
    chapter1_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/chapter1_extracted.md"
    
    try:
        with open(chapter1_file, 'r', encoding='utf-8') as f:
            chapter1_content = f.read()
            
        print(f"📚 Chapter 1 로드: {len(chapter1_content):,} 문자")
        
        # Claude 정밀 분석 실행
        print("\n🔍 Claude로 정밀 구조 분석 중...")
        analysis_result = await analyze_chapter1_structure(chapter1_content)
        
        if analysis_result:
            print(f"\n📋 정밀 분석 결과:")
            print("=" * 70)
            print(analysis_result)
            print("=" * 70)
            print(f"\n✅ 정밀 분석 완료! ({len(analysis_result):,} 문자)")
        else:
            print("\n❌ 분석 결과를 받지 못했습니다.")
            
    except Exception as e:
        print(f"❌ Chapter 1 파일 로드 실패: {e}")

if __name__ == "__main__":
    asyncio.run(main())