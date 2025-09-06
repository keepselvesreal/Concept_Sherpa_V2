# 생성 시간: 2025-08-08 16:03:48 KST
# 핵심 내용: Claude SDK를 사용해 파트별 리프 노드 JSON에 start_text, end_text 정보를 배치 처리로 추가
# 상세 내용:
#   - main() 함수 (라인 10-49): 인자 처리 및 메인 실행 로직
#   - process_part_boundaries() 함수 (라인 51-97): 파트 단위 리프 노드 경계 처리
#   - process_batch_with_claude() 함수 (라인 99-149): Claude SDK로 10개씩 배치 처리
#   - create_batch_prompt() 함수 (라인 151-177): Claude에게 전달할 프롬프트 생성
#   - parse_claude_response() 함수 (라인 179-206): Claude 응답을 파싱하여 JSON 추출
# 상태: 활성
# 주소: add_text_boundaries_with_claude
# 참조: claude_sdk_test (Claude SDK 사용법)

import json
import argparse
import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    # 명령행 인자 처리
    parser = argparse.ArgumentParser(description='Claude SDK로 리프 노드에 start_text, end_text 추가')
    parser.add_argument('--part-text', required=True, help='파트 텍스트 파일 경로 (예: Part_01_Part_1_Flexibility.md)')
    parser.add_argument('--leaf-nodes', required=True, help='리프 노드 JSON 파일 경로 (예: part1_leaf_nodes.json)')
    parser.add_argument('--output', required=True, help='출력 JSON 파일 경로')
    
    args = parser.parse_args()
    
    # 파일 존재 여부 확인
    if not os.path.exists(args.part_text):
        print(f"❌ 파트 텍스트 파일을 찾을 수 없습니다: {args.part_text}")
        return
    
    if not os.path.exists(args.leaf_nodes):
        print(f"❌ 리프 노드 JSON 파일을 찾을 수 없습니다: {args.leaf_nodes}")
        return
    
    print(f"🚀 Claude SDK로 텍스트 경계 추가 시작...")
    print(f"   📄 파트 텍스트: {args.part_text}")
    print(f"   🌿 리프 노드: {args.leaf_nodes}")
    print(f"   📝 출력 파일: {args.output}")
    
    try:
        # 비동기 처리 실행
        asyncio.run(process_part_boundaries(args.part_text, args.leaf_nodes, args.output))
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

async def process_part_boundaries(part_text_file, leaf_nodes_file, output_file):
    """파트 단위 리프 노드 경계 처리"""
    
    # 파트 텍스트 읽기
    with open(part_text_file, 'r', encoding='utf-8') as f:
        part_text = f.read()
    
    print(f"📖 파트 텍스트 길이: {len(part_text):,} 문자")
    
    # 리프 노드 JSON 읽기
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    print(f"🌿 리프 노드 개수: {len(leaf_nodes)}개")
    
    # 10개씩 배치로 나누기
    batch_size = 10
    batches = [leaf_nodes[i:i + batch_size] for i in range(0, len(leaf_nodes), batch_size)]
    
    print(f"📦 배치 개수: {len(batches)}개 (배치당 최대 {batch_size}개)")
    
    # 각 배치 처리
    processed_nodes = []
    
    for i, batch in enumerate(batches, 1):
        print(f"\n🔄 배치 {i}/{len(batches)} 처리 중... ({len(batch)}개 노드)")
        
        try:
            # Claude SDK로 배치 처리
            batch_result = await process_batch_with_claude(batch, part_text, i)
            
            if batch_result:
                processed_nodes.extend(batch_result)
                print(f"   ✅ 배치 {i} 완료: {len(batch_result)}개 노드 처리됨")
            else:
                print(f"   ❌ 배치 {i} 실패: Claude 응답 파싱 실패")
                # 실패한 경우 원본 데이터 유지
                processed_nodes.extend(batch)
        
        except Exception as e:
            print(f"   ❌ 배치 {i} 오류: {e}")
            # 오류 발생 시 원본 데이터 유지
            processed_nodes.extend(batch)
    
    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_nodes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 처리 완료! {len(processed_nodes)}개 노드가 {output_file}에 저장되었습니다.")

async def process_batch_with_claude(batch, part_text, batch_num):
    """Claude SDK로 10개씩 배치 처리"""
    
    try:
        # Claude 프롬프트 생성
        prompt = create_batch_prompt(batch, part_text)
        
        print(f"   🤖 Claude에게 배치 {batch_num} 요청 중...")
        
        # Claude SDK 옵션 설정
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="당신은 텍스트 분석 전문가입니다. 주어진 텍스트에서 각 리프 노드의 정확한 시작과 끝 텍스트를 찾아 JSON 형식으로 반환해주세요."
        )
        
        # Claude SDK 호출
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        if not responses:
            print(f"   ⚠️  Claude로부터 응답을 받지 못했습니다.")
            return None
        
        # 응답 파싱
        full_response = "\\n".join(responses)
        print(f"   📥 Claude 응답 길이: {len(full_response)} 문자")
        
        # JSON 파싱
        parsed_result = parse_claude_response(full_response, batch)
        
        return parsed_result
        
    except Exception as e:
        print(f"   ❌ Claude 처리 중 오류: {e}")
        return None

def create_batch_prompt(batch, part_text):
    """Claude에게 전달할 프롬프트 생성"""
    
    titles_list = ""
    for i, node in enumerate(batch, 1):
        titles_list += f"{i}. ID {node['id']}: \"{node['title']}\"\n"
    
    prompt = f"""다음 텍스트에서 각 리프 노드의 start_text와 end_text를 찾아주세요.

**전체 텍스트:**
```
{part_text[:50000]}  
```
{"... (텍스트가 잘림)" if len(part_text) > 50000 else ""}

**분석할 리프 노드들:**
{titles_list}

**요구사항:**
1. 각 리프 노드 제목이 텍스트에서 나타나는 정확한 위치를 찾으세요
2. start_text: 해당 섹션이 시작되는 부분의 텍스트 (10-30자 정도)
3. end_text: 해당 섹션이 끝나는 부분의 텍스트 (다음 섹션 시작 전까지, 10-30자 정도)

**JSON 형식으로 응답:**
```json
[
  {{
    "id": 1,
    "title": "원제목",
    "level": 1,
    "start_text": "찾은 시작 텍스트",
    "end_text": "찾은 끝 텍스트"
  }}
]
```"""
    
    return prompt

def parse_claude_response(response_text, original_batch):
    """Claude 응답을 파싱하여 JSON 추출"""
    
    try:
        # JSON 코드 블록 찾기
        import re
        json_pattern = r'```json\\s*([\\s\\S]*?)\\s*```'
        json_matches = re.findall(json_pattern, response_text)
        
        if json_matches:
            json_text = json_matches[0].strip()
            parsed_data = json.loads(json_text)
            
            print(f"   ✅ JSON 파싱 성공: {len(parsed_data)}개 노드")
            return parsed_data
        else:
            # JSON 코드 블록이 없으면 전체 응답에서 JSON 찾기
            json_pattern = r'\\[\\s*\\{[\\s\\S]*?\\}\\s*\\]'
            json_matches = re.findall(json_pattern, response_text)
            
            if json_matches:
                parsed_data = json.loads(json_matches[0])
                print(f"   ✅ JSON 파싱 성공 (대안): {len(parsed_data)}개 노드")
                return parsed_data
            else:
                print(f"   ⚠️  JSON을 찾을 수 없습니다. 원본 데이터 유지")
                return original_batch
                
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON 파싱 오류: {e}")
        return original_batch
    
    except Exception as e:
        print(f"   ❌ 응답 파싱 오류: {e}")
        return original_batch

if __name__ == "__main__":
    main()