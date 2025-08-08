# 생성 시간: 2025-08-08 16:42:15 KST
# 핵심 내용: Claude SDK로 리프 노드 경계 정보 자동 생성 - 수동 작업 자동화
# 상세 내용:
#   - main() 함수 (라인 9-35): 메인 실행 로직, 파라미터로 파일 경로 받기
#   - generate_boundaries_with_claude() 함수 (라인 37-80): Claude SDK로 경계 정보 생성
#   - create_boundary_prompt() 함수 (라인 82-105): 경계 추가 요청 프롬프트 생성
#   - parse_claude_response() 함수 (라인 107-140): Claude 응답에서 JSON 추출
# 상태: 활성
# 주소: claude_boundary_generator
# 참조: test_data (Chapter 1 테스트 데이터)

import json
import asyncio
import os
import sys
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """Claude SDK로 리프 노드 경계 정보 자동 생성"""
    
    if len(sys.argv) != 4:
        print("사용법: python claude_boundary_generator.py <리프노드파일> <텍스트파일> <출력파일>")
        print("예시: python claude_boundary_generator.py chapter1_leaf_nodes.json chapter1_text.md output.json")
        return
    
    leaf_nodes_file = sys.argv[1]
    text_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # 파일 존재 확인
    if not os.path.exists(leaf_nodes_file):
        print(f"❌ 리프 노드 파일 없음: {leaf_nodes_file}")
        return
    
    if not os.path.exists(text_file):
        print(f"❌ 텍스트 파일 없음: {text_file}")
        return
    
    print(f"🔍 Claude SDK 경계 생성 시작...")
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 처리 실행
    asyncio.run(generate_boundaries_with_claude(leaf_nodes_file, text_file, output_file))

async def generate_boundaries_with_claude(leaf_nodes_file, text_file, output_file):
    """Claude SDK로 경계 정보 생성"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    print(f"🌿 리프 노드: {len(leaf_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    try:
        # 경계 추가 프롬프트 생성
        prompt = create_boundary_prompt(leaf_nodes, text_content)
        
        print(f"🤖 Claude에게 경계 생성 요청 중...")
        
        # Claude SDK 호출
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="JSON만 반환하세요. 설명하지 마세요."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        if responses:
            full_response = "\n".join(responses)
            print(f"📥 Claude 응답 길이: {len(full_response)} 문자")
            
            # JSON 응답 파싱
            result = parse_claude_response(full_response, leaf_nodes)
            
            if result:
                # 결과 저장
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 경계 생성 완료! 결과: {output_file}")
                print(f"📊 처리된 노드: {len(result)}개")
            else:
                print("❌ Claude 응답 파싱 실패")
        else:
            print("❌ Claude 응답 없음")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

def create_boundary_prompt(leaf_nodes, text_content):
    """경계 추가 요청 프롬프트 생성"""
    
    # 노드 목록 생성
    nodes_info = ""
    for node in leaf_nodes:
        nodes_info += f"ID {node['id']}: \"{node['title']}\" (level {node['level']})\n"
    
    # 텍스트 길이 제한 (처음 10,000자)
    limited_text = text_content[:10000]
    if len(text_content) > 10000:
        limited_text += "\n\n[... 텍스트 계속됨 ...]"
    
    prompt = f"""텍스트:
{limited_text}

리프 노드들:
{nodes_info}

각 노드의 간단한 제목만 start_text, end_text로 추출. 긴 문단 금지.
JSON만 반환:
[{{"id":1,"title":"Part 1 Introduction","level":1,"start_text":"Part 1","end_text":"Complexity of object-"}}]"""
    
    return prompt

def parse_claude_response(response_text, original_nodes):
    """Claude 응답에서 JSON 추출"""
    
    try:
        import re
        
        # 직접 JSON 배열 찾기 (```json 블록이 없을 수도 있음)
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        json_matches = re.findall(json_pattern, response_text)
        
        json_text = ""
        if json_matches:
            json_text = json_matches[0].strip()
        else:
            # JSON 블록이 없으면 전체 응답에서 JSON 배열 찾기
            array_pattern = r'\[[\s\S]*?\]'
            array_matches = re.findall(array_pattern, response_text)
            if array_matches:
                json_text = array_matches[0].strip()
            else:
                json_text = response_text.strip()
        
        if json_text:
            parsed_data = json.loads(json_text)
            
            print(f"✅ JSON 파싱 성공: {len(parsed_data)}개 노드")
            
            # 기본 검증
            if isinstance(parsed_data, list) and len(parsed_data) > 0:
                # 필수 필드 확인
                sample_node = parsed_data[0]
                required_fields = ['id', 'title', 'level', 'start_text', 'end_text']
                
                if all(field in sample_node for field in required_fields):
                    print(f"✅ JSON 구조 검증 성공")
                    return parsed_data
                else:
                    print(f"❌ 필수 필드 누락")
                    return None
            else:
                print(f"❌ 잘못된 JSON 구조")
                return None
        else:
            print(f"❌ JSON을 찾을 수 없음")
            print(f"📝 응답 내용: {response_text[:200]}...")
            return None
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패: {e}")
        print(f"📝 응답 내용: {response_text[:200]}...")
        return None
        
    except Exception as e:
        print(f"❌ 파싱 오류: {e}")
        return None

if __name__ == "__main__":
    main()