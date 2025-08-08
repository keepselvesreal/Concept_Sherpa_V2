# 목차
# - 생성 시간: 2025-08-07 12:15:30 KST
# - 핵심 내용: 검증된 Claude Code SDK를 사용하여 목차에 Introduction 섹션을 추가하는 최종 버전
# - 상세 내용:
#     - analyze_part_gaps(1-40): Part별로 내용 갭을 분석하는 함수
#     - enhance_toc_with_claude(42-80): Claude SDK로 목차를 분석하고 강화하는 함수
#     - main(82-95): 메인 실행 함수
# - 상태: 활성
# - 주소: final_toc_enhancer
# - 참조: PDF_목차.md, extracted_parts/

import asyncio
import os
from datetime import datetime
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def load_file_content(file_path: str) -> str:
    """파일 내용 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 로드 실패 {file_path}: {e}")
        return ""

async def analyze_part_gaps():
    """Part별 갭 분석"""
    
    # 파일 로드
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07"
    toc_content = load_file_content(os.path.join(base_dir, "PDF_목차.md"))
    part1_content = load_file_content(os.path.join(base_dir, "extracted_parts", "Part_01_Part_1_Flexibility.md"))
    
    if not toc_content or not part1_content:
        print("필요한 파일을 로드할 수 없습니다.")
        return None
    
    # Part 1 시작 부분 추출 (매우 짧게)
    part1_start = part1_content[:1000]  # 처음 1000자만
    toc_sample = toc_content[:1500]  # 목차도 1500자만
    
    # 분석 프롬프트 (매우 간단)
    prompt = f"""목차에 Introduction 추가 분석:

목차:
{toc_sample}

Part 1 내용:
{part1_start}

Part 1(29페이지)과 Chapter 1(31페이지) 사이에 내용이 있으므로 "0 Introduction (29-30페이지)" 추가 필요.

이런 식으로 다른 곳도 분석해서 업데이트된 목차 제공해주세요."""

    print(f"📏 프롬프트 길이: {len(prompt):,} 문자")
    
    try:
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="책 목차 구조 분석 전문가"
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        return "\n".join(responses) if responses else None
        
    except Exception as e:
        print(f"Claude 분석 실패: {e}")
        return None

def save_results(analysis_result: str, base_dir: str):
    """분석 결과 저장"""
    if not analysis_result:
        return
        
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')
    
    # v2 목차 파일 저장
    v2_content = f"""# 목차
# - 생성 시간: {timestamp}
# - 핵심 내용: Claude SDK로 분석하여 Introduction 섹션이 추가된 강화된 목차
# - 상세 내용: 상하위 구성요소 사이의 내용을 분석하여 자동 생성된 Introduction 항목들
# - 상태: 활성
# - 주소: PDF_목차_v2
# - 참조: PDF_목차.md

{analysis_result}
"""
    
    v2_path = os.path.join(base_dir, "PDF_목차_v2.md")
    with open(v2_path, 'w', encoding='utf-8') as f:
        f.write(v2_content)
    
    # 분석 리포트 저장
    report_content = f"""# Claude 목차 분석 리포트

**분석 시간**: {timestamp}
**분석 도구**: Claude Code SDK

## 분석 결과

{analysis_result}

---
*이 리포트는 Claude Code SDK로 자동 생성되었습니다.*
"""
    
    report_path = os.path.join(base_dir, "introduction_analysis_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 결과 저장 완료:")
    print(f"📁 강화된 목차: {v2_path}")
    print(f"📊 분석 리포트: {report_path}")

async def main():
    print("🚀 Claude Code SDK 목차 Enhancement (최종 버전)")
    
    print("\n🔍 Part 갭 분석 중...")
    result = await analyze_part_gaps()
    
    if result:
        print(f"\n✅ 분석 완료: {len(result):,} 문자")
        print("\n📋 Claude 분석 결과:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # 결과 저장
        base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07"
        save_results(result, base_dir)
        
        print(f"\n🎉 목차 Enhancement 완료!")
    else:
        print("\n❌ 분석 실패")

if __name__ == "__main__":
    asyncio.run(main())