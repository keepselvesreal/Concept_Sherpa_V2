#!/usr/bin/env python3
"""
섹션 텍스트 추출기 - Claude Code SDK 공식 방법 사용

원문에서 각 title로 시작되는 섹션의 시작, 종료 문자열을 추출하고
해당 섹션의 전체 텍스트를 정확히 추출하는 스크립트

Claude Code SDK 공식 문서: https://docs.anthropic.com/ko/docs/claude-code/sdk#python
"""

import anyio
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from claude_code_sdk import query, ClaudeCodeOptions, Message

class SectionExtractor:
    """Claude Code SDK를 사용한 섹션 추출기"""
    
    def __init__(self):
        """초기화"""
        pass
    
    async def load_files(self, text_file: str, json_file: str) -> tuple[str, List[Dict]]:
        """파일 로드"""
        try:
            # 원문 텍스트 로드
            with open(text_file, 'r', encoding='utf-8') as f:
                source_text = f.read()
            print(f"✓ 원문 로드 완료: {len(source_text):,}자")
            
            # 섹션 JSON 로드
            with open(json_file, 'r', encoding='utf-8') as f:
                sections = json.load(f)
            print(f"✓ 섹션 정보 로드 완료: {len(sections)}개")
            
            return source_text, sections
            
        except Exception as e:
            print(f"❌ 파일 로드 실패: {e}")
            raise
    
    async def extract_section_boundaries(self, source_text: str, section_title: str, next_title: Optional[str] = None) -> Dict[str, str]:
        """
        Claude Code SDK를 사용해 섹션의 시작과 끝 텍스트 추출
        """
        # 문서 샘플링 (너무 큰 경우)
        source_sample = source_text
        if len(source_text) > 30000:
            target_pos = source_text.find(section_title)
            if target_pos != -1:
                start_sample = max(0, target_pos - 5000)
                end_sample = min(len(source_text), target_pos + 25000)
                source_sample = source_text[start_sample:end_sample]
            else:
                source_sample = source_text[:30000]
        
        # 다음 섹션 정보
        next_section_info = f"다음 섹션은 '{next_title}'입니다." if next_title else "이것은 문서의 마지막 섹션입니다."
        
        # 프롬프트 생성
        prompt = f"""다음 텍스트에서 "{section_title}" 섹션의 정확한 시작과 끝 부분을 찾아주세요.

{next_section_info}

작업 단계:
1. "{section_title}" 제목이 나타나는 위치를 찾으세요
2. 섹션 제목부터 시작해서 30자를 추출하여 start_text로 만드세요
3. 현재 섹션이 끝나는 지점을 찾으세요 (다음 섹션 시작 직전 또는 문서 끝)
4. 섹션의 마지막 부분에서 30자를 추출하여 end_text로 만드세요

중요: 
- start_text는 섹션 제목을 포함해야 합니다
- end_text는 현재 섹션의 마지막 부분이어야 합니다 (다음 섹션 포함 X)
- 각각 정확히 30자여야 합니다

JSON 형식으로만 응답하세요:
{{
  "title": "{section_title}",
  "start_text": "정확히 30자",
  "end_text": "정확히 30자"
}}

텍스트:
{source_sample}"""

        try:
            messages: List[Message] = []
            
            print(f"🧠 Claude SDK로 '{section_title}' 경계 추출 중...")
            
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="텍스트 분석 전문가로서 정확한 섹션 경계를 추출하세요. JSON 형식으로만 응답하세요.",
                    allowed_tools=[]  # 텍스트 분석만 사용
                )
            ):
                messages.append(message)
            
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
            
            # 응답 내용 디버깅
            print(f"📄 Claude 응답 길이: {len(response_text)}")
            print(f"📄 Claude 응답 시작: {response_text[:500]}...")
            
            # JSON 추출 및 파싱 (더 유연하게)
            json_match = re.search(r'\{.*?"title".*?\}', response_text, re.DOTALL)
            if not json_match:
                # 더 넓은 패턴으로 시도
                json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
            
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    
                    # 30자 길이 조정
                    if 'start_text' in result and len(result['start_text']) > 30:
                        result['start_text'] = result['start_text'][:30]
                    if 'end_text' in result and len(result['end_text']) > 30:
                        result['end_text'] = result['end_text'][:30]
                    
                    return result
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 디코딩 실패: {e}")
                    print(f"   추출된 JSON: {json_match.group()[:200]}...")
            
            print(f"❌ JSON 파싱 실패")
            print(f"   응답 전체: {response_text}")
            return {"title": section_title, "start_text": "", "end_text": ""}
                
        except Exception as e:
            print(f"❌ 경계 추출 실패 '{section_title}': {e}")
            return {"title": section_title, "start_text": "", "end_text": ""}
    
    def extract_section_content(self, full_text: str, start_text: str, end_text: str) -> str:
        """
        시작과 끝 텍스트를 사용해 섹션 전체 내용 추출
        """
        if not start_text or not end_text:
            return ""
        
        # 시작 위치 찾기
        start_idx = full_text.find(start_text)
        if start_idx == -1:
            # 부분 매칭 시도
            start_words = start_text.split()[:3]
            partial_start = ' '.join(start_words)
            start_idx = full_text.find(partial_start)
            if start_idx == -1:
                return ""
        
        # 끝 위치 찾기 (시작 위치 이후)
        end_idx = full_text.find(end_text, start_idx)
        if end_idx == -1:
            # 부분 매칭 시도
            end_words = end_text.split()[-3:]
            partial_end = ' '.join(end_words)
            end_idx = full_text.find(partial_end, start_idx)
            if end_idx == -1:
                return ""
            end_idx += len(partial_end)
        else:
            end_idx += len(end_text)
        
        return full_text[start_idx:end_idx].strip()
    
    async def process_all_sections(self, text_file: str, json_file: str, output_dir: str):
        """
        모든 섹션 처리 및 추출
        """
        print("🚀 Claude Code SDK 섹션 추출기 시작")
        print("=" * 50)
        
        # 파일 로드
        source_text, sections = await self.load_files(text_file, json_file)
        
        # 출력 디렉토리 생성
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = []
        successful_extractions = 0
        
        for i, section in enumerate(sections):
            # 첫 번째 섹션만 테스트
            if i > 0:
                break
                
            title = section['title']
            next_title = sections[i + 1]['title'] if i + 1 < len(sections) else None
            
            print(f"\n📖 처리 중: {title}")
            if next_title:
                print(f"   📍 다음 섹션: {next_title}")
            
            # 경계 추출
            start_time = time.time()
            boundaries = await self.extract_section_boundaries(source_text, title, next_title)
            elapsed = time.time() - start_time
            
            # 섹션 내용 추출
            section_content = ""
            if boundaries['start_text'] and boundaries['end_text']:
                section_content = self.extract_section_content(
                    source_text, 
                    boundaries['start_text'], 
                    boundaries['end_text']
                )
                
                if section_content:
                    successful_extractions += 1
                    print(f"   ✅ 성공 ({len(section_content):,}자, {elapsed:.2f}초)")
                else:
                    print(f"   ❌ 내용 추출 실패 ({elapsed:.2f}초)")
            else:
                print(f"   ❌ 경계 추출 실패 ({elapsed:.2f}초)")
            
            # 결과 저장
            result = {
                "id": section['id'],
                "title": title,
                "level": section['level'],
                "start_text": boundaries['start_text'],
                "end_text": boundaries['end_text'],
                "content": section_content,
                "content_length": len(section_content),
                "extraction_time": elapsed
            }
            results.append(result)
            
            # 개별 섹션 파일 저장 (성공한 경우만)
            if section_content:
                safe_title = re.sub(r'[^\w\s-]', '', title).strip()
                safe_title = re.sub(r'[-\s]+', '_', safe_title)
                section_file = output_path / f"section_{section['id']:03d}_{safe_title}.md"
                
                with open(section_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"**ID:** {section['id']}\n")
                    f.write(f"**Level:** {section['level']}\n")
                    f.write(f"**Length:** {len(section_content):,} characters\n")
                    f.write(f"**Extraction Time:** {elapsed:.2f} seconds\n\n")
                    f.write("---\n\n")
                    f.write(section_content)
        
        # 전체 결과 저장
        results_file = output_path / "extraction_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # 업데이트된 섹션 정보 저장 (경계 포함)
        for i, result in enumerate(results):
            sections[i]['start_text'] = result['start_text']
            sections[i]['end_text'] = result['end_text']
        
        updated_sections_file = output_path / "updated_sections.json"
        with open(updated_sections_file, 'w', encoding='utf-8') as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)
        
        # 요약 보고서
        total_time = sum(r['extraction_time'] for r in results)
        success_rate = (successful_extractions / len(results)) * 100
        
        print(f"\n{'=' * 50}")
        print(f"📊 추출 완료 요약:")
        print(f"   총 섹션: {len(results)}개")
        print(f"   성공: {successful_extractions}개 ({success_rate:.1f}%)")
        print(f"   실패: {len(results) - successful_extractions}개")
        print(f"   총 소요시간: {total_time:.2f}초")
        print(f"   평균 처리시간: {total_time/len(results):.2f}초/섹션")
        print(f"\n📁 결과 파일:")
        print(f"   전체 결과: {results_file}")
        print(f"   업데이트된 섹션: {updated_sections_file}")
        print(f"   개별 섹션들: {output_path}/section_*.md")

async def main():
    """메인 실행 함수"""
    # 파일 경로 설정
    text_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    json_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/extracted_sections"
    
    # 추출기 실행
    extractor = SectionExtractor()
    await extractor.process_all_sections(text_file, json_file, output_dir)

if __name__ == "__main__":
    anyio.run(main)