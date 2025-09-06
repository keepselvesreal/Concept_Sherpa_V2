# 생성 시간: 2025-08-08 16:29:23 KST
# 핵심 내용: Claude SDK로 전체 텍스트와 모든 리프 노드를 한 번에 처리하여 start_text, end_text 추가
# 상세 내용:
#   - main() 함수 (라인 9-32): 메인 실행 로직, 단일 Claude 요청으로 모든 노드 처리
#   - process_all_nodes_at_once() 함수 (라인 34-66): 전체 노드를 한 번에 Claude에게 요청
#   - create_comprehensive_prompt() 함수 (라인 68-96): 전체 텍스트와 모든 리프 노드를 포함한 프롬프트 생성
#   - parse_comprehensive_response() 함수 (라인 98-132): Claude 응답에서 JSON 파싱 및 검증
# 상태: 활성
# 주소: simple_claude_boundaries
# 참조: test_data (Chapter 1 테스트 데이터)

import json
import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """Chapter 1 테스트 데이터로 단일 Claude 요청 테스트"""
    
    print("🧪 Claude SDK 단일 요청 테스트 시작...")
    
    # 테스트 파일 경로
    test_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/test_data'
    leaf_nodes_file = os.path.join(test_dir, 'chapter1_leaf_nodes.json')
    text_file = os.path.join(test_dir, 'chapter1_text.md')
    output_file = os.path.join(test_dir, 'chapter1_single_request.json')
    
    # 파일 존재 확인
    if not os.path.exists(leaf_nodes_file) or not os.path.exists(text_file):
        print(f"❌ 테스트 파일이 없습니다.")
        return
    
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 처리 실행
    asyncio.run(process_all_nodes_at_once(leaf_nodes_file, text_file, output_file))

async def process_all_nodes_at_once(leaf_nodes_file, text_file, output_file):
    """전체 노드를 한 번에 Claude에게 요청"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    print(f"🌿 리프 노드: {len(leaf_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    try:
        # 포괄적 프롬프트 생성
        prompt = create_comprehensive_prompt(leaf_nodes, text_content)
        
        print(f"🤖 Claude에게 전체 요청 중... ({len(leaf_nodes)}개 노드)")
        
        # Claude SDK 호출
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="전체 텍스트를 분석하여 각 리프 노드의 start_text와 end_text를 정확히 찾아 JSON으로 반환하세요."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        if responses:
            full_response = "\\n".join(responses)
            print(f"📥 Claude 응답 길이: {len(full_response)} 문자")
            print(f"📝 Claude 응답 내용: {full_response}")
            
            # 응답 파싱
            result = parse_comprehensive_response(full_response, leaf_nodes)
            
            # 결과 저장
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 완료! 결과: {output_file}")
        else:
            print("❌ Claude 응답 없음")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

def create_comprehensive_prompt(leaf_nodes, text_content):
    """전체 텍스트와 모든 리프 노드를 포함한 프롬프트 생성"""
    
    # 노드 목록 생성
    nodes_list = ""
    for node in leaf_nodes:
        nodes_list += f"{node['id']}. \"{node['title']}\" (level {node['level']})\\n"
    
    prompt = f"""다음 텍스트에서 리프 노드들의 간단한 시작/끝 텍스트를 찾아 JSON으로 반환해주세요.

텍스트 (처음 15,000자):
{text_content[:15000]}

리프 노드들:
{nodes_list}

JSON으로 반환:
```json
[{{"id":1,"title":"Part 1 Introduction","level":1,"start_text":"Part 1","end_text":"Complexity of object-"}}]
```"""
    
    return prompt

def parse_comprehensive_response(response_text, original_nodes):
    """Claude 응답에서 JSON 파싱 및 검증"""
    
    try:
        import re
        
        # JSON 블록 찾기
        json_pattern = r'```json\\s*([\\s\\S]*?)\\s*```'
        json_matches = re.findall(json_pattern, response_text)
        
        if json_matches:
            json_text = json_matches[0].strip()
            parsed_data = json.loads(json_text)
            
            print(f"✅ JSON 파싱 성공: {len(parsed_data)}개 노드")
            
            # 노드 수 검증
            if len(parsed_data) == len(original_nodes):
                print(f"✅ 노드 수 일치: {len(parsed_data)}개")
                return parsed_data
            else:
                print(f"⚠️  노드 수 불일치: 기대 {len(original_nodes)}, 실제 {len(parsed_data)}")
                # 부족한 노드는 원본으로 채움
                result = parsed_data[:]
                for i in range(len(parsed_data), len(original_nodes)):
                    result.append(original_nodes[i])
                return result
        else:
            print("❌ JSON 블록을 찾을 수 없음")
            return original_nodes
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return original_nodes
        
    except Exception as e:
        print(f"❌ 파싱 오류: {e}")
        return original_nodes

if __name__ == "__main__":
    main()