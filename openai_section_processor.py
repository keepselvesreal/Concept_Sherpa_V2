#!/usr/bin/env python3
"""
OpenAI API를 사용하여 섹션 마커를 추가하는 프로세서
원문과 JSON 데이터를 OpenAI 모델에 전달하여 각 섹션의 시작/종료 문자를 추가합니다.
"""
import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def load_text_content(md_file_path):
    """마크다운 파일에서 텍스트 콘텐츠를 로드합니다."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_json_sections(json_file_path):
    """JSON 파일에서 섹션 정보를 로드합니다."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_openai_prompt(text_content, json_sections):
    """OpenAI API에 전달할 프롬프트를 생성합니다."""
    prompt = f"""
다음은 데이터 지향 프로그래밍 책의 7장 "Basic data validation" 내용과 해당 챕터의 섹션 구조입니다.

원문 내용:
```
{text_content}
```

섹션 구조 (JSON):
```json
{json.dumps(json_sections, indent=2, ensure_ascii=False)}
```

작업 요청:
1. 위 원문에서 각 섹션에 해당하는 내용을 정확히 추출해주세요
2. OpenAI 문서 스타일에 맞게 각 섹션의 시작과 종료 마커를 추가해주세요
3. 시작 마커: "## [섹션 제목]\\n"
4. 종료 마커: "\\n---\\n"

응답 형식:
각 섹션에 대해 다음과 같은 JSON 형식으로 응답해주세요:

```json
[
  {{
    "id": 섹션ID,
    "title": "섹션 제목",
    "level": 레벨,
    "start_text": "시작 마커",
    "end_text": "종료 마커",
    "content": "해당 섹션의 실제 내용",
    "formatted_content": "마커가 포함된 완전한 섹션 내용"
  }}
]
```

중요사항:
- 원문에서 각 섹션에 해당하는 내용을 정확히 식별하여 추출해주세요
- 섹션 제목과 내용이 일치하도록 해주세요
- JSON 형식을 정확히 유지해주세요
"""
    return prompt

def process_with_openai(text_content, json_sections, api_key):
    """OpenAI API를 사용하여 섹션을 처리합니다."""
    client = OpenAI(api_key=api_key)
    
    prompt = create_openai_prompt(text_content, json_sections)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 기술 문서 전문가입니다. 주어진 텍스트에서 섹션을 정확히 식별하고 적절한 마커를 추가하여 구조화된 형태로 반환해주세요."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return None

def parse_openai_response(response_content):
    """OpenAI 응답에서 JSON 데이터를 추출합니다."""
    try:
        # JSON 블록 찾기
        start_marker = "```json"
        end_marker = "```"
        
        start_idx = response_content.find(start_marker)
        if start_idx == -1:
            # ```json이 없으면 단순히 JSON 찾기
            start_idx = response_content.find("[")
        else:
            start_idx += len(start_marker)
        
        end_idx = response_content.find(end_marker, start_idx)
        if end_idx == -1:
            # 마커가 없으면 전체 내용에서 마지막 ] 찾기
            end_idx = response_content.rfind("]")
            if end_idx != -1:
                end_idx += 1
            else:
                end_idx = len(response_content)
        
        json_str = response_content[start_idx:end_idx].strip()
        
        # JSON 문자열 정리 (잘린 부분 수정)
        if not json_str.endswith(']') and not json_str.endswith('}'):
            # JSON이 잘린 경우 마지막 완전한 객체까지만 사용
            last_complete = json_str.rfind('}')
            if last_complete != -1:
                # 마지막 완전한 객체 다음에 ] 추가
                json_str = json_str[:last_complete + 1] + '\n]'
        
        print(f"파싱할 JSON 길이: {len(json_str)} 문자")
        print(f"JSON 시작: {json_str[:100]}...")
        print(f"JSON 끝: ...{json_str[-100:]}")
        
        # JSON 파싱
        parsed_data = json.loads(json_str)
        return parsed_data
    
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        print(f"오류 위치 근처: {json_str[max(0, e.pos-50):e.pos+50] if 'e.pos' in locals() else 'N/A'}")
        
        # 백업 방법: 각 섹션을 개별적으로 파싱 시도
        try:
            return parse_partial_response(response_content)
        except:
            return None
    except Exception as e:
        print(f"응답 파싱 중 오류: {e}")
        return None

def parse_partial_response(response_content):
    """부분적으로 파싱된 응답을 복구합니다."""
    print("부분 응답 파싱 시도 중...")
    sections = []
    
    # 각 섹션을 개별적으로 찾아서 파싱
    lines = response_content.split('\n')
    current_section = {}
    in_content = False
    content_lines = []
    
    for line in lines:
        line = line.strip()
        
        if '"id":' in line:
            current_section['id'] = int(line.split(':')[1].strip().rstrip(','))
        elif '"title":' in line:
            title = line.split(':', 1)[1].strip().strip('"').rstrip(',')
            current_section['title'] = title
        elif '"level":' in line:
            current_section['level'] = int(line.split(':')[1].strip().rstrip(','))
        elif '"start_text":' in line:
            start_text = line.split(':', 1)[1].strip().strip('"').rstrip(',')
            current_section['start_text'] = start_text.replace('\\n', '\n')
        elif '"end_text":' in line:
            end_text = line.split(':', 1)[1].strip().strip('"').rstrip(',')
            current_section['end_text'] = end_text.replace('\\n', '\n')
        elif '"content":' in line and not in_content:
            in_content = True
            # content 시작 부분
            content_start = line.split(':', 1)[1].strip()
            if content_start.startswith('"') and content_start.endswith('",'):
                # 한 줄로 완료된 경우
                current_section['content'] = content_start[1:-2]
                in_content = False
            elif content_start.startswith('"'):
                content_lines = [content_start[1:]]
        elif in_content:
            if line.endswith('",') or line.endswith('"'):
                # content 끝
                if line.endswith('",'):
                    content_lines.append(line[:-2])
                else:
                    content_lines.append(line[:-1])
                current_section['content'] = '\n'.join(content_lines)
                content_lines = []
                in_content = False
            else:
                content_lines.append(line)
        elif line == '},' or line == '}':
            # 섹션 완료
            if current_section and 'title' in current_section:
                # formatted_content 생성
                if 'content' in current_section and 'start_text' in current_section and 'end_text' in current_section:
                    current_section['formatted_content'] = f"{current_section['start_text']}{current_section['content']}{current_section['end_text']}"
                sections.append(current_section)
            current_section = {}
    
    return sections if sections else None

def save_enhanced_json(enhanced_data, output_file_path):
    """향상된 데이터를 JSON 파일로 저장합니다."""
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"향상된 JSON이 저장되었습니다: {output_file_path}")

def main():
    """메인 함수"""
    base_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2")
    
    # 입력 파일들
    json_file = base_dir / "25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    md_file = base_dir / "25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    
    # 출력 파일
    output_dir = base_dir / "25-08-10"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "openai_enhanced_chapter07.json"
    
    # OpenAI API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("오류: OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        return
    
    try:
        print("파일 로딩 중...")
        # 파일들 로드
        text_content = load_text_content(md_file)
        json_sections = load_json_sections(json_file)
        
        print(f"원문 길이: {len(text_content)} 문자")
        print(f"JSON 섹션 수: {len(json_sections)}개")
        
        print("OpenAI API 호출 중...")
        # OpenAI로 처리
        response = process_with_openai(text_content, json_sections, api_key)
        
        if response:
            print("OpenAI 응답 파싱 중...")
            # 응답 파싱
            enhanced_data = parse_openai_response(response)
            
            if enhanced_data:
                print("결과 저장 중...")
                # 결과 저장
                save_enhanced_json(enhanced_data, output_file)
                
                print(f"\n✅ 성공적으로 처리 완료!")
                print(f"처리된 섹션 수: {len(enhanced_data)}개")
                print(f"출력 파일: {output_file}")
                
                # 샘플 출력
                if enhanced_data:
                    print(f"\n📋 첫 번째 섹션 샘플:")
                    sample = enhanced_data[0]
                    print(f"제목: {sample.get('title')}")
                    print(f"시작 마커: {repr(sample.get('start_text'))}")
                    print(f"종료 마커: {repr(sample.get('end_text'))}")
                    if sample.get('content'):
                        preview = sample['content'][:200] + "..." if len(sample['content']) > 200 else sample['content']
                        print(f"내용 미리보기: {preview}")
            else:
                print("❌ OpenAI 응답 파싱에 실패했습니다.")
        else:
            print("❌ OpenAI API 호출에 실패했습니다.")
    
    except Exception as e:
        print(f"❌ 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    main()