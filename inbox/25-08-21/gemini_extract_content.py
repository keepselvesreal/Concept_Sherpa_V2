#!/usr/bin/env python3
"""
생성 시간: 2025-08-21 21:15:32
핵심 내용: Gemini 2.0 Flash-lite 모델을 사용해 문서에서 핵심 정보, 상세 핵심 정보, 상세 정보, 주요 화제, 부차 화제를 추출하는 스크립트
상세 내용: 
    - GeminiProvider (line 30): Gemini 2.0 Flash-lite API 구현체
    - extract_content_with_gemini() (line 80): Gemini를 사용한 내용 추출
    - extract_all_information() (line 120): 5가지 정보를 순차적으로 추출
    - save_extracted_info() (line 200): 추출된 정보를 파일로 저장
    - main() (line 240): 메인 실행 함수
상태: active
참조: extract_enhanced_node_content.py
"""

import os
import asyncio
import argparse
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


class GeminiProvider:
    """Gemini 2.0 Flash-lite API 구현체"""
    
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
        
        # Gemini 2.0 Flash-lite 모델 설정
        self.model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
        print("✅ Gemini 2.0 Flash-lite 모델 초기화 완료")
    
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


async def extract_content_with_gemini(content: str, title: str, provider: GeminiProvider) -> Dict[str, str]:
    """
    Gemini를 사용해 문서에서 5가지 정보 추출
    
    Args:
        content: 추출할 문서 내용
        title: 문서 제목
        provider: Gemini 제공자
        
    Returns:
        추출된 정보 딕셔너리
    """
    print(f"🚀 Gemini 2.0 Flash-lite로 정보 추출 시작: {title}")
    
    results = {}
    
    # 1. 핵심 정보 추출
    print("1️⃣ 핵심 정보 추출 중...")
    core_prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 가장 핵심적인 내용을 2-3문장으로 간결하게 한국어로 요약해주세요.
무엇이 가장 중요한 개념이고 핵심 메시지인지 명확하게 설명해주세요.

응답 형식: 바로 요약 내용만 작성하고, 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_instruction = "당신은 기술 문서 분석 전문가입니다. 복잡한 내용에서 핵심을 간결하고 명확하게 추출하세요."
    
    results["핵심 정보"] = await provider.generate_content(core_prompt, system_instruction)
    
    # 2. 상세 핵심 정보 추출
    print("2️⃣ 상세 핵심 정보 추출 중...")
    detailed_core_prompt = f"""앞서 추출한 핵심 정보: "{results['핵심 정보']}"

원본 내용: "{title}"
{content}

핵심 정보에서 언급된 요점들을 더 자세하게 설명해주세요. 
중요한 세부사항과 배경 정보를 포함하여 300-500단어로 한국어로 작성해주세요.

응답 형식: 바로 상세 설명만 작성하고, 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_instruction = "핵심 내용을 보완하는 상세한 설명을 제공하는 전문가입니다."
    
    results["상세 핵심 정보"] = await provider.generate_content(detailed_core_prompt, system_instruction)
    
    # 3. 상세 정보 추출
    print("3️⃣ 상세 정보 추출 중...")
    detailed_prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 중요한 세부사항들을 상세하게 한국어로 추출해주세요.
기술적 내용, 구체적 예시, 구현 방법, 장단점 등을 포함해서 충분히 자세하게 설명해주세요.

응답 형식: 바로 상세 내용만 작성하고, 헤더나 마크다운 형식은 사용하지 마세요."""
    
    system_instruction = "기술 문서의 상세 내용을 체계적으로 분석하고 설명하는 전문가입니다."
    
    results["상세 정보"] = await provider.generate_content(detailed_prompt, system_instruction)
    
    # 4. 주요 화제 추출
    print("4️⃣ 주요 화제 추출 중...")
    main_topics_prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 다루어지는 주요 화제나 주제를 3-5개 추출해주세요.
각 항목은 반드시 "- " 문자로 시작하는 목록 형태로 작성하고, 한국어로 작성해주세요.

형식 예시:
- 주제1: 설명
- 주제2: 설명
- 주제3: 설명

응답에 추가 내용 없이 바로 목록만 작성하세요."""
    
    system_instruction = "주요 주제를 명확하게 식별하고 목록으로 정리하는 전문가입니다."
    
    results["주요 화제"] = await provider.generate_content(main_topics_prompt, system_instruction)
    
    # 5. 부차 화제 추출
    print("5️⃣ 부차 화제 추출 중...")
    sub_topics_prompt = f"""다음은 "{title}"의 내용입니다:

{content}

주요 테마를 보완하는 부차적 주제, 세부 주제, 또는 지원 세부사항을 3-5개 추출해주세요.
각 항목은 반드시 "- " 문자로 시작하는 목록 형태로 작성하고, 한국어로 작성해주세요.

형식 예시:
- 부차주제1: 설명  
- 부차주제2: 설명
- 부차주제3: 설명

응답에 추가 내용 없이 바로 목록만 작성하세요."""
    
    system_instruction = "부차적 주제와 세부사항을 식별하고 목록으로 정리하는 전문가입니다."
    
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
    
    # 파일명 생성
    source_name = Path(source_file).stem
    output_file = os.path.join(output_dir, f"{source_name}_gemini_extracted.md")
    
    # 파일 내용 구성
    content = f"""# {source_name} - Gemini 추출 결과

**원본 파일:** {source_file}  
**추출 시간:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**모델:** Gemini 2.0 Flash-lite  

---

## 핵심 정보
{extracted_data.get('핵심 정보', '추출 실패')}

## 상세 핵심 정보  
{extracted_data.get('상세 핵심 정보', '추출 실패')}

## 상세 정보
{extracted_data.get('상세 정보', '추출 실패')}

## 주요 화제
{extracted_data.get('주요 화제', '추출 실패')}

## 부차 화제
{extracted_data.get('부차 화제', '추출 실패')}

---

*Generated by Gemini 2.0 Flash-lite*
"""
    
    # 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file


async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='Gemini 2.0 Flash-lite를 사용한 문서 정보 추출')
    parser.add_argument('input_file', help='처리할 문서 파일 경로')
    parser.add_argument('--api-key', help='Gemini API 키 (환경 변수 GEMINI_API_KEY 사용 가능)')
    parser.add_argument('--output-dir', help='출력 디렉토리 (기본값: 현재 날짜 디렉토리)')
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not os.path.exists(args.input_file):
        print(f"❌ 파일을 찾을 수 없습니다: {args.input_file}")
        return
    
    # 파일 내용 읽기
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
        return
    
    # 제목 추출
    title = Path(args.input_file).stem
    
    print(f"📄 파일: {args.input_file}")
    print(f"📝 제목: {title}")
    print(f"📊 내용 길이: {len(content):,} 문자")
    
    try:
        # Gemini 제공자 초기화
        provider = GeminiProvider(api_key=args.api_key)
        
        # 정보 추출
        extracted_data = await extract_content_with_gemini(content, title, provider)
        
        # 결과 저장
        output_file = save_extracted_info(extracted_data, args.input_file, args.output_dir)
        
        print(f"✅ 추출 결과가 저장되었습니다: {output_file}")
        
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