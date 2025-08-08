# 생성 시간: 2025-08-08 16:16:25 KST  
# 핵심 내용: Chapter 1 테스트용 Claude SDK 텍스트 경계 추가 스크립트 - 소규모 배치 처리
# 상세 내용:
#   - main() 함수 (라인 9-32): 메인 실행 로직, 테스트 데이터로 Claude SDK 검증
#   - test_claude_boundaries() 함수 (라인 34-71): Chapter 1 데이터로 경계 텍스트 추가 테스트
#   - process_small_batch() 함수 (라인 73-115): 3-5개씩 소규모 배치 처리
#   - create_simple_prompt() 함수 (라인 117-142): 간소화된 Claude 프롬프트 생성
#   - parse_simple_response() 함수 (라인 144-172): Claude 응답 파싱 및 검증
# 상태: 활성
# 주소: test_claude_boundaries
# 참조: create_test_data (테스트 데이터), claude_sdk_test (SDK 사용법)

import json
import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """Chapter 1 테스트 데이터로 Claude SDK 검증"""
    
    print("🧪 Chapter 1 Claude SDK 텍스트 경계 테스트 시작...")
    
    # 테스트 파일 경로
    test_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/test_data'
    leaf_nodes_file = os.path.join(test_dir, 'chapter1_leaf_nodes.json')
    text_file = os.path.join(test_dir, 'chapter1_text.md')
    output_file = os.path.join(test_dir, 'chapter1_with_boundaries.json')
    
    # 파일 존재 확인
    if not os.path.exists(leaf_nodes_file):
        print(f"❌ 리프 노드 파일 없음: {leaf_nodes_file}")
        return
    
    if not os.path.exists(text_file):
        print(f"❌ 텍스트 파일 없음: {text_file}")
        return
    
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 테스트 실행
    asyncio.run(test_claude_boundaries(leaf_nodes_file, text_file, output_file))

async def test_claude_boundaries(leaf_nodes_file, text_file, output_file):
    """Chapter 1 데이터로 경계 텍스트 추가 테스트"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    print(f"🌿 리프 노드: {len(leaf_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    # 출력 토큰 제한을 고려한 작은 배치 (2개씩)
    batch_size = 2
    batches = [leaf_nodes[i:i + batch_size] for i in range(0, len(leaf_nodes), batch_size)]
    
    print(f"📦 배치 개수: {len(batches)}개 (배치당 {batch_size}개씩)")
    
    # 각 배치 처리
    processed_nodes = []
    
    for i, batch in enumerate(batches, 1):
        print(f"\n🔄 배치 {i}/{len(batches)} 처리 중... ({len(batch)}개 노드)")
        
        try:
            batch_result = await process_small_batch(batch, text_content, i)
            
            if batch_result:
                processed_nodes.extend(batch_result)
                print(f"   ✅ 배치 {i} 성공: {len(batch_result)}개 처리")
            else:
                print(f"   ❌ 배치 {i} 실패: 원본 데이터 유지")
                processed_nodes.extend(batch)
                
        except Exception as e:
            print(f"   💥 배치 {i} 오류: {e}")
            processed_nodes.extend(batch)
        
        # 배치 간 지연 시간 (연속 요청 문제 방지)
        if i < len(batches):  # 마지막 배치가 아닌 경우
            print(f"   ⏳ 10초 대기 중...")
            await asyncio.sleep(10)
    
    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_nodes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 테스트 완료! 결과: {output_file}")

async def process_small_batch(batch, text_content, batch_num):
    """3-5개씩 소규모 배치 처리"""
    
    try:
        # 간소화된 프롬프트 생성
        prompt = create_simple_prompt(batch, text_content)
        
        print(f"   🤖 Claude 요청 중... (배치 {batch_num})")
        
        # Claude SDK 호출 (max_tokens 파라미터 제거)
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="텍스트에서 각 제목의 시작과 끝 부분을 찾아 JSON으로 반환하세요."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        if not responses:
            print(f"   ⚠️  응답 없음")
            return None
        
        # 응답 파싱
        full_response = "\n".join(responses)
        print(f"   📥 응답 길이: {len(full_response)} 문자")
        print(f"   📝 응답 미리보기: {full_response[:100]}...")
        
        # 간단한 파싱
        result = parse_simple_response(full_response, batch)
        
        return result
        
    except Exception as e:
        print(f"   ❌ Claude 처리 오류: {e}")
        return None

def create_simple_prompt(batch, text_content):
    """간소화된 Claude 프롬프트 생성"""
    
    titles_list = ""
    for node in batch:
        titles_list += f"- ID {node['id']}: \"{node['title']}\"\n"
    
    # 텍스트 길이 제한 (처음 20,000자만)
    limited_text = text_content[:20000]
    if len(text_content) > 20000:
        limited_text += "\n\n[... 텍스트 계속됨 ...]"
    
    prompt = f"""다음 텍스트에서 각 제목의 간략한 시작/끝 텍스트를 찾아주세요.

**텍스트:**
```
{limited_text}
```

**찾을 제목들:**
{titles_list}

**중요 요구사항:**
- start_text: 해당 제목이 나타나는 줄 (5-15자 정도의 짧은 텍스트)
- end_text: 다음 제목이나 섹션이 시작되는 줄 (5-15자 정도의 짧은 텍스트)
- 긴 문단이 아닌 제목/헤더만 반환

**JSON 형식:**
```json
[
  {{
    "id": 1,
    "title": "제목",
    "level": 1,
    "start_text": "Part 1",
    "end_text": "1 Introduction"
  }}
]
```"""
    
    return prompt

def parse_simple_response(response_text, original_batch):
    """Claude 응답 파싱 및 검증"""
    
    try:
        import re
        
        # JSON 블록 찾기
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        json_matches = re.findall(json_pattern, response_text)
        
        if json_matches:
            json_text = json_matches[0].strip()
            parsed_data = json.loads(json_text)
            
            print(f"   ✅ JSON 파싱 성공: {len(parsed_data)}개")
            
            # 간단한 검증
            if len(parsed_data) == len(original_batch):
                return parsed_data
            else:
                print(f"   ⚠️  노드 개수 불일치: 기대 {len(original_batch)}, 실제 {len(parsed_data)}")
                return original_batch
        else:
            print(f"   ⚠️  JSON 블록을 찾을 수 없음")
            return original_batch
            
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON 파싱 실패: {e}")
        return original_batch
    
    except Exception as e:
        print(f"   ❌ 파싱 오류: {e}")
        return original_batch

if __name__ == "__main__":
    main()