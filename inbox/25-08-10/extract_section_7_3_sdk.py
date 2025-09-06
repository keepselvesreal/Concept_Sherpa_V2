#!/usr/bin/env python3
"""
# 생성 시간: 2025-08-10 23:43:00 KST
# 핵심 내용: 7.3 Schema flexibility and strictness 섹션만 추출하는 전용 스크립트
# 상세 내용: 
#   - SectionExtractor (line 19): Claude Code SDK를 이용한 섹션 추출 클래스
#   - extract_section_7_3 (line 45): 7.3 섹션 전용 추출 메서드
#   - main (line 160): 메인 실행 함수, 파일 경로와 출력 설정
# 상태: active
# 주소: extract_section_7_3_sdk
# 참조: section_extractor_sdk.py 기반으로 7.3 섹션 전용으로 특화
"""

import anyio
import json
import re
import time
from pathlib import Path
from typing import Dict, Optional
from claude_code_sdk import query, ClaudeCodeOptions, Message

class SectionExtractor:
    """Claude Code SDK를 사용한 7.3 섹션 전용 추출기"""
    
    def __init__(self):
        """초기화"""
        pass
    
    async def extract_section_7_3(self, source_file: str, output_dir: str = None) -> Dict:
        """
        7.3 Schema flexibility and strictness 섹션을 Claude Code SDK로 추출
        
        Args:
            source_file: 원본 마크다운 파일 경로
            output_dir: 출력 디렉토리 (None이면 현재 폴더)
        
        Returns:
            추출 결과 딕셔너리
        """
        print("🚀 7.3 섹션 추출기 시작 (Claude Code SDK)")
        print("=" * 60)
        
        # 원본 파일 로드
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_text = f.read()
            print(f"✓ 원본 파일 로드: {len(source_text):,}자")
        except Exception as e:
            print(f"❌ 파일 로드 실패: {e}")
            return {"success": False, "error": str(e)}
        
        # 7.3 섹션 추출을 위한 프롬프트
        prompt = f"""다음 문서에서 "7.3 Schema flexibility and strictness" 섹션을 정확히 추출해주세요.

작업 요구사항:
1. "7.3 Schema flexibility and strictness" 제목으로 시작하는 부분을 찾으세요
2. 해당 섹션의 전체 내용을 추출하세요 (제목 포함)
3. 다음 섹션("7.4 Schema composition")이 시작되기 직전까지 포함하세요
4. 원본 텍스트의 형식과 구조를 그대로 유지하세요

응답 형식:
{{
  "title": "7.3 Schema flexibility and strictness",
  "content": "전체 섹션 내용",
  "start_position": 시작위치숫자,
  "end_position": 끝위치숫자,
  "word_count": 단어수
}}

원본 문서:
{source_text}"""

        try:
            messages = []
            
            print(f"🧠 Claude SDK로 7.3 섹션 추출 중...")
            start_time = time.time()
            
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="""당신은 정확한 텍스트 추출 전문가입니다. 
지정된 섹션을 정확히 찾아서 완전한 내용을 추출하세요. 
JSON 형식으로만 응답하고, content 필드에는 원본 형식을 그대로 유지하세요.""",
                    allowed_tools=[]  # 텍스트 분석만 사용
                )
            ):
                messages.append(message)
            
            elapsed = time.time() - start_time
            
            # 응답 텍스트 추출
            response_text = ""
            for message in messages:
                if hasattr(message, 'content'):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                response_text += block.text
                    elif hasattr(message.content, 'text'):
                        response_text += message.content.text
                    else:
                        response_text += str(message.content)
                elif hasattr(message, 'text'):
                    response_text += message.text
            
            print(f"✓ Claude 응답 수신: {len(response_text):,}자 ({elapsed:.2f}초)")
            
            # JSON 추출 및 파싱
            json_match = re.search(r'\{.*?"title".*?\}', response_text, re.DOTALL)
            if not json_match:
                # 더 넓은 패턴 시도
                json_match = re.search(r'\{[\s\S]*\}', response_text, re.DOTALL)
            
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    
                    # 결과 검증
                    if 'content' in result and result['content']:
                        content = result['content']
                        word_count = len(content.split())
                        
                        print(f"✅ 섹션 추출 성공:")
                        print(f"   제목: {result.get('title', '7.3 Schema flexibility and strictness')}")
                        print(f"   내용 길이: {len(content):,}자")
                        print(f"   단어 수: {word_count:,}개")
                        print(f"   처리 시간: {elapsed:.2f}초")
                        
                        # 파일 저장
                        if output_dir:
                            output_path = Path(output_dir)
                            output_path.mkdir(exist_ok=True)
                        else:
                            output_path = Path(".")
                        
                        # 7.3 섹션 파일 저장
                        section_file = output_path / "section_7_3_schema_flexibility_strictness.md"
                        with open(section_file, 'w', encoding='utf-8') as f:
                            f.write(f"# 7.3 Schema flexibility and strictness\n\n")
                            f.write(f"**추출 시간:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"**소스:** {source_file}\n")
                            f.write(f"**길이:** {len(content):,}자\n")
                            f.write(f"**단어수:** {word_count:,}개\n")
                            f.write(f"**처리시간:** {elapsed:.2f}초\n\n")
                            f.write("---\n\n")
                            f.write(content)
                        
                        print(f"💾 파일 저장 완료: {section_file}")
                        
                        return {
                            "success": True,
                            "title": result.get('title', '7.3 Schema flexibility and strictness'),
                            "content": content,
                            "file_path": str(section_file),
                            "word_count": word_count,
                            "processing_time": elapsed,
                            "extraction_timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    else:
                        print(f"❌ 내용이 비어있음")
                        return {"success": False, "error": "추출된 내용이 비어있음"}
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 파싱 실패: {e}")
                    print(f"   JSON 내용: {json_match.group()[:500]}...")
                    return {"success": False, "error": f"JSON 파싱 실패: {e}"}
            else:
                print(f"❌ JSON 형식을 찾을 수 없음")
                print(f"   응답 내용: {response_text[:1000]}...")
                return {"success": False, "error": "JSON 형식 응답을 찾을 수 없음"}
                
        except Exception as e:
            print(f"❌ 섹션 추출 실패: {e}")
            return {"success": False, "error": str(e)}

async def main():
    """메인 실행 함수"""
    # 파일 경로 설정
    source_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10"
    
    print(f"📂 입력 파일: {source_file}")
    print(f"📂 출력 디렉토리: {output_dir}")
    
    # 추출기 실행
    extractor = SectionExtractor()
    result = await extractor.extract_section_7_3(source_file, output_dir)
    
    # 최종 결과 출력
    print(f"\n{'=' * 60}")
    if result.get("success"):
        print(f"🎉 7.3 섹션 추출 완료!")
        print(f"📄 제목: {result['title']}")
        print(f"💾 파일: {result['file_path']}")
        print(f"📏 길이: {result['word_count']:,}단어")
        print(f"⏱️ 시간: {result['processing_time']:.2f}초")
    else:
        print(f"❌ 추출 실패: {result.get('error', '알 수 없는 오류')}")

if __name__ == "__main__":
    anyio.run(main)