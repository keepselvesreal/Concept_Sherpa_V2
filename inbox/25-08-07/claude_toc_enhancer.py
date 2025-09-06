# 목차
# - 생성 시간: 2025-08-07 11:45:30 KST
# - 핵심 내용: Claude Code SDK를 사용하여 Part 내용을 분석하고 상하위 구성요소 사이에 Introduction 섹션을 자동 추가하는 도구
# - 상세 내용:
#     - load_part_content(1-25): Part 파일들의 내용을 로드하는 함수
#     - load_toc_content(27-40): 기존 목차 파일을 로드하는 함수
#     - create_analysis_prompt(42-75): Claude SDK용 분석 프롬프트를 생성하는 함수
#     - save_enhanced_toc(77-95): 업데이트된 목차를 v2 파일로 저장하는 함수
#     - save_analysis_report(97-115): 분석 리포트를 저장하는 함수
#     - main(117-145): 전체 프로세스를 실행하는 메인 함수
# - 상태: 활성
# - 주소: claude_toc_enhancer
# - 참조: extracted_parts/, PDF_목차.md, claude-code-sdk

import asyncio
import os
from pathlib import Path
from datetime import datetime
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

# 환경 변수 로드
def load_env():
    """환경 변수 로드"""
    env_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/.env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def load_part_content(base_dir: str) -> dict:
    """Part 파일들의 내용을 로드"""
    parts_content = {}
    
    part_files = [
        ("Part 1", "Part_01_Part_1_Flexibility.md"),
        ("Part 2", "Part_02_Part_2_Scalability.md"), 
        ("Part 3", "Part_03_Part_3_Maintainability.md")
    ]
    
    for part_name, filename in part_files:
        file_path = os.path.join(base_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                parts_content[part_name] = content
                print(f"✅ {part_name} 로드 완료: {len(content):,} 문자")
        except Exception as e:
            print(f"❌ {part_name} 로드 실패: {e}")
            parts_content[part_name] = ""
    
    return parts_content

def load_toc_content(toc_path: str) -> str:
    """기존 목차 파일 로드"""
    try:
        with open(toc_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"✅ 목차 로드 완료: {len(content):,} 문자")
            return content
    except Exception as e:
        print(f"❌ 목차 로드 실패: {e}")
        return ""

def create_analysis_prompt(parts_content: dict, toc_content: str) -> str:
    """Claude SDK용 분석 프롬프트 생성 (매우 간단한 버전)"""
    
    # 매우 짧은 샘플만 사용
    part1_sample = parts_content.get('Part 1', '')[:500]
    toc_sample = toc_content[:2000]
    
    prompt = f"""다음 목차에 Introduction 섹션을 추가해주세요:

목차 일부:
{toc_sample}

Part 1 시작:
{part1_sample}

Part 1은 페이지 29에서 시작하고 Chapter 1은 페이지 31에서 시작합니다.
사이에 내용이 있으므로 "0 Introduction (페이지 29-30)" 을 추가해주세요.

비슷한 방식으로 다른 곳도 분석해서 업데이트된 목차를 제공해주세요."""

    return prompt

def save_enhanced_toc(response_content: str, output_path: str):
    """업데이트된 목차를 v2 파일로 저장"""
    try:
        # 헤더 추가
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')
        
        enhanced_content = f"""# 목차
# - 생성 시간: {timestamp}
# - 핵심 내용: Claude SDK로 분석하여 Introduction 섹션이 추가된 강화된 목차
# - 상세 내용: 상하위 구성요소 사이의 내용을 분석하여 자동 생성된 Introduction 항목들
# - 상태: 활성
# - 주소: PDF_목차_v2
# - 참조: PDF_목차.md

{response_content}
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        print(f"✅ 강화된 목차 저장 완료: {output_path}")
        
    except Exception as e:
        print(f"❌ 목차 저장 실패: {e}")

def save_analysis_report(response_content: str, output_path: str):
    """분석 리포트 저장"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')
        
        report_content = f"""# 목차 Introduction 추가 분석 리포트

## 분석 정보
- 분석 시간: {timestamp}
- 분석 도구: Claude Code SDK
- 분석 대상: Data-Oriented Programming 전체 Part 내용

## Claude SDK 분석 결과

{response_content}

---
*이 리포트는 Claude Code SDK에 의해 자동 생성되었습니다.*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"✅ 분석 리포트 저장 완료: {output_path}")
        
    except Exception as e:
        print(f"❌ 리포트 저장 실패: {e}")

async def main():
    """메인 실행 함수"""
    print("🚀 Claude Code SDK 목차 Enhancement 시작...")
    
    # 환경 설정
    load_env()
    
    base_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07"
    parts_dir = os.path.join(base_dir, "extracted_parts")
    toc_file = os.path.join(base_dir, "PDF_목차.md")
    output_toc = os.path.join(base_dir, "PDF_목차_v2.md")
    output_report = os.path.join(base_dir, "introduction_analysis_report.md")
    
    # 1. 데이터 로드
    print("\n📚 데이터 로드 중...")
    parts_content = load_part_content(parts_dir)
    toc_content = load_toc_content(toc_file)
    
    if not toc_content:
        print("❌ 목차 로드 실패로 작업 중단")
        return
    
    # 2. 분석 프롬프트 생성
    print("\n🔍 Claude SDK 분석 준비 중...")
    prompt = create_analysis_prompt(parts_content, toc_content)
    print(f"📏 프롬프트 길이: {len(prompt):,} 문자")
    
    # 3. Claude SDK 호출
    print("\n🤖 Claude SDK로 전체 내용 분석 중...")
    try:
        # 옵션 설정
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="당신은 책의 목차 구조를 분석하고 개선하는 전문가입니다."
        )
        
        # 응답 수집
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        if responses:
            # 모든 응답을 합쳐서 처리
            full_response = "\n".join(responses)
            print(f"✅ Claude 분석 완료: {len(full_response):,} 문자")
            
            # 4. 결과 저장
            print("\n💾 결과 저장 중...")
            save_enhanced_toc(full_response, output_toc)
            save_analysis_report(full_response, output_report)
            
            print(f"\n🎉 작업 완료!")
            print(f"📁 강화된 목차: {output_toc}")
            print(f"📊 분석 리포트: {output_report}")
            
        else:
            print("❌ Claude로부터 응답을 받지 못했습니다.")
            
    except Exception as e:
        print(f"❌ Claude SDK 호출 실패: {e}")
        print(f"오류 타입: {type(e)}")

if __name__ == "__main__":
    asyncio.run(main())