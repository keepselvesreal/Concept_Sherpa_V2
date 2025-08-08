# 목차
# - 생성 시간: 2025-08-07 12:33:15 KST
# - 핵심 내용: Chapter 1 전체 텍스트를 Claude에게 전달하여 필요한 Introduction 목차들을 분석하는 테스트 도구
# - 상세 내용:
#     - analyze_chapter1_introductions(1-40): Chapter 1 전체를 분석해서 Introduction 필요 부분을 찾는 함수
#     - main(42-65): Chapter 1 파일을 로드하고 분석 실행하는 함수
# - 상태: 활성
# - 주소: chapter1_toc_analyzer
# - 참조: chapter1_extracted.md

import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

async def analyze_chapter1_introductions(chapter1_content: str):
    """Chapter 1 전체 내용을 분석하여 필요한 Introduction 목차들을 찾기"""
    
    prompt = f"""다음은 Data-Oriented Programming 책의 Chapter 1 전체 내용입니다:

{chapter1_content}

**엄격한 기준에 따라 Introduction 필요 여부를 판단하세요:**

**규칙 1: Chapter-Section 간격 확인**
- Chapter 1 제목과 첫 번째 Section(1.1) 사이에 텍스트 내용이 존재하면 → "1.0 Introduction" 필요
- 내용이 없고 바로 Section이 시작하면 → "1.0 Introduction" 불필요

**규칙 2: Section-Subsection 간격 확인** 
- Section 1.1과 첫 번째 Subsection(1.1.1) 사이에 텍스트 내용이 존재하면 → "1.1.0 Introduction" 필요
- Section 1.2와 첫 번째 Subsection(1.2.1) 사이에 텍스트 내용이 존재하면 → "1.2.0 Introduction" 필요
- 내용이 없고 바로 Subsection이 시작하면 → 해당 Introduction 불필요

**출력 형식:**
오직 위 규칙에 따라 내용이 실제로 존재하는 경우만 다음 형식으로 나열하세요:
- 1.0 Introduction (페이지 X-Y)  [Chapter 1과 Section 1.1 사이 내용 존재]
- 1.1.0 Introduction (페이지 X-Y) [Section 1.1과 Subsection 1.1.1 사이 내용 존재]
- 1.2.0 Introduction (페이지 X-Y) [Section 1.2와 Subsection 1.2.1 사이 내용 존재]

**중요:** 개인적 판단이나 해석은 금지하며, 오직 텍스트 내용의 실제 존재 여부만으로 판단하세요."""

    try:
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="주어진 엄격한 규칙에만 따라 텍스트 내용 존재 여부를 확인하는 분석가입니다. 개인적 판단이나 해석은 하지 않고 오직 명시된 기준만 적용합니다."
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
        print(f"❌ Chapter 1 분석 실패: {e}")
        return ""

async def main():
    print("🚀 Chapter 1 목차 분석 테스트...")
    
    # Chapter 1 파일 로드
    chapter1_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/chapter1_extracted.md"
    
    try:
        with open(chapter1_file, 'r', encoding='utf-8') as f:
            chapter1_content = f.read()
            
        print(f"📚 Chapter 1 로드: {len(chapter1_content):,} 문자")
        
        # Claude 분석 실행
        print("\n🔍 Claude로 Chapter 1 Introduction 분석 중...")
        analysis_result = await analyze_chapter1_introductions(chapter1_content)
        
        if analysis_result:
            print(f"\n📋 Claude 분석 결과:")
            print("=" * 60)
            print(analysis_result)
            print("=" * 60)
            print(f"\n✅ 분석 완료! ({len(analysis_result):,} 문자)")
        else:
            print("\n❌ 분석 결과를 받지 못했습니다.")
            
    except Exception as e:
        print(f"❌ Chapter 1 파일 로드 실패: {e}")

if __name__ == "__main__":
    asyncio.run(main())