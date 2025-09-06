# 생성 시간: 2025-08-08 16:55:30 KST
# 핵심 내용: 수동 작업 방식 모방 - 간단한 Claude SDK 경계 생성
# 상세 내용:
#   - main() 함수 (라인 9-35): 메인 실행 로직, 파라미터로 파일 경로 받기
#   - generate_simple_boundaries() 함수 (라인 37-75): 간단한 Claude 요청
#   - create_simple_prompt() 함수 (라인 77-95): 간단한 사용자 프롬프트
#   - parse_simple_response() 함수 (라인 97-130): 간단한 응답 파싱
# 상태: 활성
# 주소: simple_claude_boundary
# 참조: test_data (Chapter 1 테스트 데이터)

import json
import asyncio
import os
import sys
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """간단한 수동 작업 방식 모방"""
    
    if len(sys.argv) != 4:
        print("사용법: python simple_claude_boundary.py <리프노드파일> <텍스트파일> <출력파일>")
        print("예시: python simple_claude_boundary.py chapter1_leaf_nodes.json chapter1_text.md output.json")
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
    
    print(f"🔍 간단한 Claude SDK 경계 생성 시작...")
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 처리 실행
    asyncio.run(generate_simple_boundaries(leaf_nodes_file, text_file, output_file))

async def generate_simple_boundaries(leaf_nodes_file, text_file, output_file):
    """간단한 Claude 요청"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    print(f"🌿 리프 노드: {len(leaf_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    try:
        # 간단한 프롬프트 생성
        prompt = create_simple_prompt(leaf_nodes, text_content)
        
        print(f"🤖 Claude에게 경계 생성 요청...")
        
        # 매우 간단한 시스템 프롬프트
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="JSON만 반환. 설명 금지."
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
            
            # 간단한 응답 파싱
            result = parse_simple_response(full_response, leaf_nodes)
            
            if result:
                # 결과 저장
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 간단한 경계 생성 완료! 결과: {output_file}")
                print(f"📊 처리된 노드: {len(result)}개")
            else:
                print("❌ 응답 파싱 실패")
        else:
            print("❌ Claude 응답 없음")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

def create_simple_prompt(leaf_nodes, text_content):
    """간단한 사용자 프롬프트"""
    
    # 텍스트 제한 (15,000자)
    limited_text = text_content[:15000]
    if len(text_content) > 15000:
        limited_text += "\n[... 계속됨 ...]"
    
    # 리프 노드 목록
    nodes_list = json.dumps(leaf_nodes, ensure_ascii=False, indent=2)
    
    # 실제 텍스트 참조 프롬프트
    prompt = f"""텍스트:
{limited_text}

JSON:
{nodes_list}

텍스트에서 실제 각 제목의 간단한 시작/끝 부분을 찾아 start_text, end_text에 추가."""
    
    return prompt

def parse_simple_response(response_text, original_nodes):
    """간단한 응답 파싱"""
    
    try:
        import re
        
        print(f"📝 응답 내용 샘플: {response_text[:300]}...")
        
        # JSON 배열 찾기
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        json_matches = re.findall(json_pattern, response_text)
        
        json_text = ""
        if json_matches:
            json_text = json_matches[0].strip()
        else:
            # JSON 블록이 없으면 전체 응답에서 배열 찾기
            array_pattern = r'\[[\s\S]*?\]'
            array_matches = re.findall(array_pattern, response_text)
            if array_matches:
                # 가장 큰 배열 선택
                json_text = max(array_matches, key=len).strip()
        
        if json_text:
            parsed_data = json.loads(json_text)
            
            if isinstance(parsed_data, list) and len(parsed_data) > 0:
                print(f"✅ JSON 파싱 성공: {len(parsed_data)}개 노드")
                return parsed_data
            else:
                print(f"❌ 잘못된 JSON 구조")
                return None
        else:
            print(f"❌ JSON을 찾을 수 없음")
            return None
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return None
        
    except Exception as e:
        print(f"❌ 파싱 오류: {e}")
        return None

if __name__ == "__main__":
    main()