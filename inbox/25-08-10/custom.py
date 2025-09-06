import anyio
import json
import re
from claude_code_sdk import query, ClaudeCodeOptions, Message

async def extract_15char_boundaries(source_path: str, nodes_path: str, target_index: int):
    """
    Claude SDK를 사용해 15자 경계 추출 및 리프노드 업데이트
    
    Args:
        source_path: 원문 파일 경로
        nodes_path: 리프노드 파일 경로  
        target_index: 대상 노드 인덱스
    """
    # 원문 로드
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_text = f.read()
        print(f"✓ 원문 로드 완료: {len(source_text):,}자")
    except Exception as e:
        print(f"❌ 원문 로드 실패: {e}")
        return
    
    # 리프노드 로드
    try:
        with open(nodes_path, 'r', encoding='utf-8') as f:
            leaf_nodes = json.load(f)
        print(f"✓ 리프노드 로드 완료: {len(leaf_nodes)}개")
    except Exception as e:
        print(f"❌ 리프노드 로드 실패: {e}")
        return
    
    # 타겟 노드 확인
    if target_index >= len(leaf_nodes):
        print(f"❌ 인덱스 {target_index}의 노드가 존재하지 않습니다")
        return
    
    target_node = leaf_nodes[target_index]
    target_title = target_node.get('title', '')
    
    print(f"\n🎯 대상 노드: '{target_title}'")
    
    # 문서 샘플링 (너무 길면)
    if len(source_text) > 20000:
        target_pos = source_text.find(target_title)
        if target_pos != -1:
            start_sample = max(0, target_pos - 3000)
            end_sample = min(len(source_text), target_pos + 12000)
            source_sample = source_text[start_sample:end_sample]
        else:
            source_sample = source_text[:20000]
    else:
        source_sample = source_text
    
    # Claude에게 15자 경계 추출 요청
    prompt = f"""문서에서 "{target_title}" 섹션만 정확히 추출할 수 있는 고유한 경계 문자열 15자씩 찾으세요.

중요: 이 경계로 나중에 원문에서 해당 섹션만 정확히 잘라낼 것입니다.

요구사항:
1. START_15: "{target_title}" 제목이 나타나는 라인에서 15자 (제목 전체 포함하되 고유하게)
2. END_15: 해당 섹션이 끝나고 다음 섹션 제목이 시작되기 직전 부분에서 15자 (다음 섹션과 명확히 구분)
3. 원문에서 START_15와 END_15 사이를 추출하면 해당 섹션의 내용만 나와야 함

반드시 다음 형식으로만 응답:
START_15: [정확히 15자]
END_15: [정확히 15자]

문서:
{source_sample}"""

    messages: list[Message] = []
    
    print(f"🧠 Claude SDK로 15자 경계 추출 중...")
    
    async for message in query(
        prompt=prompt,
        options=ClaudeCodeOptions(
            max_turns=1,
            system_prompt="텍스트 분석만으로 응답하세요. 도구를 사용하지 마세요. 요청된 형식으로만 답변하세요.",
            allowed_tools=[]
        )
    ):
        messages.append(message)
    
    # 응답에서 텍스트 추출
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
        else:
            # AssistantMessage나 다른 타입 처리
            msg_str = str(message)
            if 'text=' in msg_str:
                text_matches = re.findall(r"text='([^']*)'", msg_str)
                if not text_matches:
                    text_matches = re.findall(r'text="([^"]*)"', msg_str)
                for text in text_matches:
                    response_text += text
    
    print(f"📄 Claude 응답 길이: {len(response_text)}")
    print(f"📄 Claude 응답: {response_text}")
    if not response_text.strip():
        print("📝 메시지 디버그:")
        for i, message in enumerate(messages):
            print(f"  메시지 {i}: {type(message).__name__}")
            print(f"  내용: {str(message)[:500]}...")
    
    # 정규식으로 15자 경계 추출
    start_match = re.search(r'START_15:\s*(.{15})', response_text)
    end_match = re.search(r'END_15:\s*(.{15})', response_text)
    
    start_15 = start_match.group(1) if start_match else None
    end_15 = end_match.group(1) if end_match else None
    
    if start_15 and end_15:
        print(f"✓ 15자 경계 추출 성공!")
        print(f"   📍 시작 15자: '{start_15}'")
        print(f"   📍 종료 15자: '{end_15}'")
        
        # 리프노드 업데이트
        leaf_nodes[target_index]['start_text'] = start_15
        leaf_nodes[target_index]['end_text'] = end_15
        
        # 업데이트된 리프노드 저장
        output_path = nodes_path.replace('.json', '_with_boundaries.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(leaf_nodes, f, ensure_ascii=False, indent=2)
        print(f"✅ 업데이트된 리프노드 저장: {output_path}")
        
    else:
        print(f"❌ 15자 경계 추출 실패")

async def main():
    """메인 실행 함수"""
    print("🚀 Claude SDK 15자 경계 추출 및 리프노드 업데이트")
    print("=" * 55)
    
    # 파일 경로 설정
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    
    # 3번째 노드 (인덱스 2) 테스트
    target_index = 2
    
    await extract_15char_boundaries(source_path, nodes_path, target_index)

anyio.run(main)