# 생성 시간: 2025-08-08 16:35:12 KST
# 핵심 내용: 최소한의 Claude SDK 테스트 - 2개 노드만 처리
# 상세 내용:
#   - main() 함수 (라인 9-32): 메인 실행 로직, 최소 2개 노드만 테스트
#   - process_minimal_nodes() 함수 (라인 34-66): 2개 노드만으로 간단한 테스트
#   - create_minimal_prompt() 함수 (라인 68-85): 최소한의 프롬프트 생성
# 상태: 활성
# 주소: minimal_claude_test
# 참조: test_data (Chapter 1 테스트 데이터)

import json
import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """최소 2개 노드로 Claude SDK 테스트"""
    
    print("🧪 최소한의 Claude SDK 테스트 시작...")
    
    # 테스트 파일 경로
    test_dir = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/test_data'
    leaf_nodes_file = os.path.join(test_dir, 'chapter1_leaf_nodes.json')
    text_file = os.path.join(test_dir, 'chapter1_text.md')
    output_file = os.path.join(test_dir, 'minimal_test_result.json')
    
    # 파일 존재 확인
    if not os.path.exists(leaf_nodes_file) or not os.path.exists(text_file):
        print(f"❌ 테스트 파일이 없습니다.")
        return
    
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 처리 실행
    asyncio.run(process_minimal_nodes(leaf_nodes_file, text_file, output_file))

async def process_minimal_nodes(leaf_nodes_file, text_file, output_file):
    """2개 노드만으로 간단한 테스트"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    # 처음 2개 노드만 사용
    minimal_nodes = leaf_nodes[:2]
    
    print(f"🌿 테스트 노드: {len(minimal_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    try:
        # 최소한 프롬프트 생성
        prompt = create_minimal_prompt(minimal_nodes, text_content[:5000])
        
        print(f"🤖 Claude에게 최소 요청 중... ({len(minimal_nodes)}개 노드)")
        
        # Claude SDK 호출
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="간단한 텍스트 경계를 찾아 JSON으로 반환하세요."
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
            print(f"📝 Claude 응답 내용: {full_response}")
            
            # 결과 저장 (원본 형태로)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(minimal_nodes, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 완료! 결과: {output_file}")
        else:
            print("❌ Claude 응답 없음")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

def create_minimal_prompt(nodes, text_content):
    """최소한의 프롬프트 생성"""
    
    prompt = f"""다음 텍스트에서 2개 제목의 시작 부분만 찾아주세요.

텍스트:
{text_content}

찾을 제목:
1. "{nodes[0]['title']}"
2. "{nodes[1]['title']}"

각 제목이 나타나는 텍스트의 시작 부분 5-10글자만 알려주세요."""
    
    return prompt

if __name__ == "__main__":
    main()