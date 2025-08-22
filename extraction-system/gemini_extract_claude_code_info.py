#!/usr/bin/env python3
"""
생성 시간: 2025-08-22 16:30:15
핵심 내용: Gemini API를 사용해서 Claude Code 노드 정보 문서에서 주요 정보 추출
상세 내용: 
    - extract_content_section() (line 35): 노드 정보 문서에서 '# 내용' 섹션 추출
    - GeminiProvider (line 60): Gemini 2.0 Flash 모델 API 구현체  
    - extract_claude_code_info() (line 120): Claude Code 관련 5가지 정보 추출
    - save_extracted_info() (line 200): 추출 결과를 마크다운 파일로 저장
    - main() (line 240): 메인 실행 함수
상태: active
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-21/gemini_extract_content.py
"""

import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Gemini API imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai 패키지가 설치되지 않았습니다.")
    print("설치 명령어: pip install google-generativeai")


def extract_content_section(info_file: str) -> str:
    """노드 정보 문서에서 '# 내용' 섹션 추출"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        content_start = -1
        content_end = len(lines)
        
        # '# 내용' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_start = i + 1
                break
        
        # 다음 구조 섹션 찾기 (# 구성, # 속성 등)
        structure_sections = ['# 구성', '# 속성', '# 추출']
        for i in range(content_start, len(lines)):
            line = lines[i].strip()
            if any(line.startswith(section) for section in structure_sections):
                content_end = i
                break
        
        if content_start == -1:
            return ""
        
        # 구분선(---)까지 스킵
        while content_start < content_end and lines[content_start].strip() == '---':
            content_start += 1
        
        # 실제 텍스트가 있는지 확인
        section_content = '\n'.join(lines[content_start:content_end])
        has_actual_text = any(line.strip() and not line.strip() == '---' for line in lines[content_start:content_end])
        
        if not has_actual_text:
            return ""
        
        return section_content.strip()
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""


class GeminiProvider:
    """Gemini 2.0 Flash API 구현체"""
    
    def __init__(self, api_key: Optional[str] = None):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai 패키지가 필요합니다")
        
        # API 키 설정 (환경 변수 또는 직접 전달)
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # 환경 변수에서 API 키 가져오기
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY 환경 변수를 설정하거나 api_key 파라미터를 제공해주세요")
            genai.configure(api_key=api_key)
        
        # Gemini 2.5 Flash 모델 설정
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        print("✅ Gemini 2.5 Flash 모델 초기화 완료")
    
    async def generate_content(self, prompt: str, system_instruction: str = "") -> str:
        """
        Gemini를 사용한 내용 생성
        
        Args:
            prompt: 사용자 프롬프트
            system_instruction: 시스템 지시사항
            
        Returns:
            생성된 텍스트
        """
        try:
            # 시스템 지시사항이 있으면 프롬프트 앞에 추가
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
            
            # 비동기 생성 (실제로는 동기 호출이지만 asyncio와 호환되도록 처리)
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.model.generate_content(full_prompt)
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return "❌ Gemini API에서 응답을 생성하지 못했습니다"
                
        except Exception as e:
            print(f"❌ Gemini API 호출 실패: {e}")
            return f"❌ Gemini API 오류: {str(e)}"


async def extract_claude_code_info(content: str, title: str, provider: GeminiProvider) -> Dict[str, str]:
    """
    Gemini를 사용해 Claude Code 관련 문서에서 5가지 정보 추출
    
    Args:
        content: 추출할 문서 내용
        title: 문서 제목
        provider: Gemini 제공자
        
    Returns:
        추출된 정보 딕셔너리
    """
    print(f"🚀 Gemini 2.5 Flash로 Claude Code 정보 추출 시작: {title}")
    
    results = {}
    
    # 1. 핵심 내용 추출
    print("1️⃣ 핵심 내용 추출 중...")
    core_prompt = f"""다음은 Claude Code에 관한 "{title}" 내용입니다:

{content}

이 Claude Code 관련 내용에서 가장 핵심적인 내용을 2-3문장으로 간결하게 한국어로 요약해주세요.
Claude Code의 어떤 특징, 기능, 사용법이 가장 중요한지 명확하게 설명해주세요.

응답 형식: 바로 요약 내용만 작성하고, 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_instruction = "당신은 개발 도구 및 AI 코딩 도구 분석 전문가입니다. Claude Code의 핵심 기능과 가치를 간결하고 명확하게 추출하세요."
    
    results["핵심 내용"] = await provider.generate_content(core_prompt, system_instruction)
    
    # 2. 상세 핵심 내용 추출
    print("2️⃣ 상세 핵심 내용 추출 중...")
    detailed_core_prompt = f"""앞서 추출한 핵심 내용: "{results['핵심 내용']}"

원본 내용: "{title}" - Claude Code 관련 내용
{content}

핵심 내용에서 언급된 Claude Code의 주요 특징들을 더 자세하게 설명해주세요. 
개발 워크플로우에서의 활용 방법, 주요 기능들, 그리고 개발자들이 얻는 이점을 포함하여 300-500단어로 한국어로 작성해주세요.

응답 형식: 바로 상세 설명만 작성하고, 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_instruction = "Claude Code의 기능과 개발자 경험을 상세히 설명하는 전문가입니다."
    
    results["상세 핵심 내용"] = await provider.generate_content(detailed_core_prompt, system_instruction)
    
    # 3. 상세 내용 추출
    print("3️⃣ 상세 내용 추출 중...")
    detailed_prompt = f"""다음은 Claude Code에 관한 "{title}" 내용입니다:

{content}

이 내용에서 Claude Code의 중요한 세부사항들을 상세하게 한국어로 추출해주세요.
기술적 구현 방법, 구체적 사용 예시, 개발팀의 접근 방식, 사용자 패턴, SDK 활용법 등을 포함해서 충분히 자세하게 설명해주세요.

응답 형식: 바로 상세 내용만 작성하고, 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_instruction = "Claude Code의 기술적 세부사항과 실제 사용 사례를 체계적으로 분석하고 설명하는 전문가입니다."
    
    results["상세 내용"] = await provider.generate_content(detailed_prompt, system_instruction)
    
    # 4. 주요 화제 추출
    print("4️⃣ 주요 화제 추출 중...")
    main_topics_prompt = f"""다음은 Claude Code에 관한 "{title}" 내용입니다:

{content}

이 내용에서 다루어지는 Claude Code 관련 주요 화제나 주제를 3-5개 추출해주세요.
각 항목은 반드시 "- " 문자로 시작하는 목록 형태로 작성하고, 한국어로 작성해주세요.

형식 예시:
- 개발팀 문화와 프로세스: 설명
- 제품 아키텍처와 기능 개발: 설명
- 사용자 성장과 채택 패턴: 설명

응답에 추가 내용 없이 바로 목록만 작성하세요."""
    
    system_instruction = "Claude Code 관련 주요 주제를 명확하게 식별하고 목록으로 정리하는 전문가입니다."
    
    results["주요 화제"] = await provider.generate_content(main_topics_prompt, system_instruction)
    
    # 5. 부차 화제 추출
    print("5️⃣ 부차 화제 추출 중...")
    sub_topics_prompt = f"""다음은 Claude Code에 관한 "{title}" 내용입니다:

{content}

주요 테마를 보완하는 Claude Code의 부차적 주제, 세부 기능, 또는 지원 세부사항을 3-5개 추출해주세요.
각 항목은 반드시 "- " 문자로 시작하는 목록 형태로 작성하고, 한국어로 작성해주세요.

형식 예시:
- 멀티 클로드 세션 활용법: 설명
- CLAUDE.md 파일 최적화: 설명  
- 커스텀 슬래시 명령어: 설명

응답에 추가 내용 없이 바로 목록만 작성하세요."""
    
    system_instruction = "Claude Code의 부차적 주제와 고급 기능을 식별하고 목록으로 정리하는 전문가입니다."
    
    results["부차 화제"] = await provider.generate_content(sub_topics_prompt, system_instruction)
    
    print("✅ 모든 정보 추출 완료")
    return results


def save_extracted_info(extracted_data: Dict[str, str], source_file: str, output_dir: str = None) -> str:
    """
    추출된 정보를 파일로 저장
    
    Args:
        extracted_data: 추출된 정보 딕셔너리
        source_file: 원본 파일 경로
        output_dir: 출력 디렉토리 (없으면 현재 날짜 디렉토리 생성)
        
    Returns:
        생성된 파일 경로
    """
    # 출력 디렉토리 설정
    if not output_dir:
        current_date = datetime.now().strftime("%y-%m-%d")
        output_dir = f"/home/nadle/projects/Knowledge_Sherpa/v2/{current_date}/gemini_extracted"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 파일명 생성 (2.5 Flash 버전임을 명시)
    source_name = Path(source_file).stem
    output_file = os.path.join(output_dir, f"{source_name}_gemini25_extracted.md")
    
    # 파일 내용 구성
    content = f"""# {source_name} - Gemini 추출 결과

**원본 파일:** {source_file}  
**추출 시간:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**모델:** Gemini 2.5 Flash  

---

## 핵심 내용
{extracted_data.get('핵심 내용', '추출 실패')}

## 상세 핵심 내용  
{extracted_data.get('상세 핵심 내용', '추출 실패')}

## 상세 내용
{extracted_data.get('상세 내용', '추출 실패')}

## 주요 화제
{extracted_data.get('주요 화제', '추출 실패')}

## 부차 화제
{extracted_data.get('부차 화제', '추출 실패')}

---

*Generated by Gemini 2.5 Flash*
"""
    
    # 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file


async def main():
    """메인 실행 함수"""
    # 입력 파일 경로
    info_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/YouTube_250822/00_lev0_Building_and_prototyping_with_Claude_Code_info.md"
    
    print("🎯 Claude Code 정보 추출 시작")
    print("=" * 50)
    print(f"📄 입력 파일: {info_file}")
    
    # 파일 존재 확인
    if not os.path.exists(info_file):
        print(f"❌ 파일을 찾을 수 없습니다: {info_file}")
        return
    
    # 내용 섹션 추출
    content = extract_content_section(info_file)
    if not content:
        print("❌ 내용 섹션이 비어있거나 추출할 수 없습니다.")
        return
    
    # 제목 추출
    title = Path(info_file).stem.replace('_info', '')
    
    print(f"📝 제목: {title}")
    print(f"📊 내용 길이: {len(content):,} 문자")
    
    try:
        # .env에서 API 키 로드
        from dotenv import load_dotenv
        env_path = "/home/nadle/projects/Knowledge_Sherpa/v2/.env"
        load_dotenv(env_path)
        
        # Gemini 제공자 초기화
        provider = GeminiProvider()
        
        # 정보 추출
        extracted_data = await extract_claude_code_info(content, title, provider)
        
        # 결과 저장
        output_file = save_extracted_info(extracted_data, info_file)
        
        print(f"\n✅ 추출 결과가 저장되었습니다: {output_file}")
        
        # 결과 요약 출력
        print("\n📊 추출 결과 요약:")
        for key, value in extracted_data.items():
            status = "✅" if not value.startswith("❌") else "❌"
            preview = value[:100].replace('\n', ' ') + "..." if len(value) > 100 else value
            print(f"  {status} {key}: {preview}")
            
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(main())