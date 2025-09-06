# 목차
# - 생성 시간: 2025-08-07 12:25:30 KST
# - 핵심 내용: Part 텍스트를 분석하여 필요한 Introduction 목차들을 문자열 리스트로 반환하는 간단한 테스트 도구
# - 상세 내용:
#     - analyze_part_for_introductions(1-35): Part 텍스트를 분석해서 Introduction 목차 리스트 반환
#     - test_with_part1(37-55): Part 1으로 테스트 실행
#     - main(57-65): 메인 실행 함수
# - 상태: 활성
# - 주소: simple_toc_analyzer
# - 참조: extracted_parts/Part_01_Part_1_Flexibility.md

import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

async def analyze_part_for_introductions(part_content: str):
    """Part 텍스트를 분석하여 필요한 Introduction 목차들을 문자열 리스트로 반환"""
    
    prompt = f"""다음은 책의 한 Part 전체 내용입니다:

{part_content}

이 내용을 분석해서 상위 구성요소와 하위 구성요소 사이에 내용이 있어서 Introduction이 필요한 곳들을 찾아주세요.

**규칙:**
- Part와 Chapter 사이에 내용이 있으면: "0 Introduction"
- Chapter와 Section 사이에 내용이 있으면: "X.0 Introduction"  
- Section과 Subsection 사이에 내용이 있으면: "X.Y.0 Introduction"

**결과:** 필요한 Introduction 목차들을 다음 형식으로 반환해주세요:
- 0 Introduction (페이지 29-30)
- 1.0 Introduction (페이지 31)
- 1.1.0 Introduction (페이지 32)

각 줄마다 하나씩, 목차 문자열만 반환해주세요."""

    try:
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="책 구조를 분석하여 필요한 Introduction 섹션을 찾는 전문가입니다."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        full_response = "\n".join(responses) if responses else ""
        
        # 응답에서 Introduction 라인들 추출
        introduction_lines = []
        for line in full_response.split('\n'):
            line = line.strip()
            if 'Introduction' in line and ('0 ' in line or '.0 ' in line):
                # '- ' 같은 prefix 제거
                if line.startswith('- '):
                    line = line[2:]
                introduction_lines.append(line)
        
        return introduction_lines
        
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
        return []

async def test_with_part1():
    """Part 1으로 테스트"""
    
    # Part 1 파일 로드
    part1_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_01_Part_1_Flexibility.md"
    
    try:
        with open(part1_path, 'r', encoding='utf-8') as f:
            full_content = f.read()
            
        # 처음 10,000자만 사용 (테스트용)
        part1_content = full_content[:10000]
        
        print(f"📚 Part 1 로드: {len(full_content):,} 문자 (테스트용: {len(part1_content):,} 문자)")
        
        # Claude 분석 실행
        print("🔍 Claude로 Introduction 분석 중...")
        introductions = await analyze_part_for_introductions(part1_content)
        
        # 결과 출력
        print(f"\n✅ 발견된 Introduction 목차들 ({len(introductions)}개):")
        for i, intro in enumerate(introductions, 1):
            print(f"  {i}. {intro}")
        
        return introductions
        
    except Exception as e:
        print(f"❌ Part 1 로드 실패: {e}")
        return []

async def main():
    print("🚀 간단한 목차 Introduction 분석 테스트...")
    
    introductions = await test_with_part1()
    
    if introductions:
        print(f"\n🎉 테스트 성공! {len(introductions)}개 Introduction 발견")
    else:
        print("\n❌ 테스트 실패 또는 Introduction 없음")

if __name__ == "__main__":
    asyncio.run(main())