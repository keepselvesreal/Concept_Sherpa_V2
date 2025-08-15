import anyio
import json
import re
from claude_code_sdk import query, ClaudeCodeOptions, Message

async def extract_15char_boundaries_v2(source_path: str, nodes_path: str, target_index: int):
    """
    Claude SDK를 사용해 더 정확한 15자 경계 추출 및 리프노드 업데이트
    - 시작: 섹션 제목 + 뒤의 구체 문자 5글자 포함
    - 종료: 다음 섹션 제목 전의 구체 문자 5글자 포함
    
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
    
    # 다음 노드 정보 (종료 경계용)
    next_node = leaf_nodes[target_index + 1] if target_index + 1 < len(leaf_nodes) else None
    next_title = next_node.get('title', '') if next_node else None
    
    print(f"\n🎯 대상 노드: '{target_title}'")
    if next_title:
        print(f"📍 다음 노드: '{next_title}'")
    
    # 문서 샘플링 (너무 길면)
    if len(source_text) > 25000:
        target_pos = source_text.find(target_title)
        if target_pos != -1:
            start_sample = max(0, target_pos - 3000)
            end_sample = min(len(source_text), target_pos + 20000)
            source_sample = source_text[start_sample:end_sample]
            print(f"📏 문서 샘플링: {len(source_sample):,}자 (전체 {len(source_text):,}자)")
        else:
            source_sample = source_text[:25000]
            print(f"📏 문서 앞부분 샘플링: {len(source_sample):,}자")
    else:
        source_sample = source_text
    
    # 다음 섹션 정보 구성
    next_section_info = f"다음 섹션은 '{next_title}'입니다." if next_title else "문서의 마지막 섹션입니다."
    
    # Claude에게 일반화된 15자 경계 추출 요청
    prompt = f"""문서에서 "{target_title}" 섹션의 정확한 15자 경계를 찾으세요.

{next_section_info}

중요: 제목만이 아니라 구체적인 내용도 포함해야 합니다!

요구사항:
1. START_15: "{target_title}" 섹션 제목 + 그 직후 나오는 구체적인 내용 5글자를 포함하여 총 15자
   예: "7.2 JSON Schema in a nutshell" + "Theo " = "7.2 JSON SchemTheo "
2. END_15: 해당 섹션 마지막 구체적인 내용 5글자 + 다음 섹션 제목 시작 부분을 포함하여 총 15자  
   예: "...false" + "7.3 Schema" = "false7.3 Schema"
3. 페이지 헤더나 목차가 아닌 실제 섹션 내용에서 추출
4. 이 경계들 사이의 텍스트가 해당 섹션의 모든 내용만 포함해야 함

설명 없이 반드시 다음 형식으로만 응답:
START_15: [정확히 15자]
END_15: [정확히 15자]

예시:
START_15: 7.2 JSON SchemTheo 
END_15: false7.3 Schema

문서:
{source_sample}"""

    messages: list[Message] = []
    
    print(f"🧠 Claude SDK로 개선된 15자 경계 추출 중...")
    
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
        
        # 원문에서 검증 (정확한 매칭 및 유사 매칭)
        start_pos = source_text.find(start_15)
        end_pos = source_text.find(end_15)
        
        # 시작 경계가 정확히 매칭되지 않으면 공백 제거 후 재시도
        if start_pos == -1:
            start_15_clean = start_15.strip()
            start_pos = source_text.find(start_15_clean)
            if start_pos != -1:
                start_15 = start_15_clean  # 정확한 매칭으로 업데이트
                print(f"   🔧 시작 경계 공백 제거 후 매칭: '{start_15}'")
        
        if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
            section_length = end_pos - start_pos + len(end_15)
            print(f"✅ 경계 검증 성공! 추출될 섹션 길이: {section_length:,}자")
            print(f"   📍 시작 위치: {start_pos:,}, 종료 위치: {end_pos:,}")
            
            # 추출된 섹션 전체 확인
            extracted_section = source_text[start_pos:end_pos + len(end_15)]
            
            print(f"\n📋 추출된 경계 상세 정보:")
            print(f"=" * 60)
            print(f"🎯 섹션: {target_title}")
            print(f"📏 전체 길이: {len(extracted_section):,}자")
            print(f"")
            print(f"🔹 시작 경계 (15자): '{start_15}'")
            print(f"   원문 위치: {start_pos:,}")
            print(f"   시작 부분 컨텍스트 (앞뒤 30자):")
            context_start = max(0, start_pos - 30)
            context_text = source_text[context_start:start_pos + 45]
            print(f"   '{context_text}'")
            print(f"")
            print(f"🔹 종료 경계 (15자): '{end_15}'")
            print(f"   원문 위치: {end_pos:,}")
            print(f"   종료 부분 컨텍스트 (앞뒤 30자):")
            context_end_start = max(0, end_pos - 30)
            context_end_text = source_text[context_end_start:end_pos + len(end_15) + 30]
            print(f"   '{context_end_text}'")
            print(f"")
            print(f"📖 추출된 섹션 시작 (200자):")
            print(f"'{extracted_section[:200]}...'")
            print(f"")
            print(f"📖 추출된 섹션 끝 (200자):")
            print(f"'...{extracted_section[-200:]}'")
            print(f"=" * 60)
            
            # 리프노드 업데이트
            leaf_nodes[target_index]['start_text'] = start_15
            leaf_nodes[target_index]['end_text'] = end_15
            
            # 업데이트된 리프노드 저장
            output_path = nodes_path.replace('.json', '_v2_boundaries.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(leaf_nodes, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 업데이트된 리프노드 저장: {output_path}")
            
        else:
            print(f"❌ 경계 검증 실패:")
            print(f"   시작 위치: {start_pos} (찾았음: {start_pos != -1})")
            print(f"   종료 위치: {end_pos} (찾았음: {end_pos != -1})")
            print(f"   위치 순서: {'올바름' if start_pos < end_pos else '잘못됨'}")
            
    else:
        print(f"❌ 15자 경계 추출 실패")
        print(f"   시작 15자: {start_15}")
        print(f"   종료 15자: {end_15}")

async def main():
    """메인 실행 함수 - 일반화된 테스트"""
    print("🚀 Claude SDK 일반화된 15자 경계 추출 (v2)")
    print("=" * 55)
    
    # 파일 경로 설정
    source_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    nodes_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json"
    
    # 리프노드 미리보기
    try:
        with open(nodes_path, 'r', encoding='utf-8') as f:
            leaf_nodes = json.load(f)
        
        print(f"\n📋 사용 가능한 리프노드:")
        for i, node in enumerate(leaf_nodes):
            print(f"  {i}: {node.get('title', 'Unknown')}")
    except Exception as e:
        print(f"❌ 리프노드 미리보기 실패: {e}")
        return
    
    # 다양한 노드 테스트 (일반화 검증)
    test_indices = [2]  # 현재는 7.2 섹션만, 나중에 [0, 1, 2, 3] 등으로 확장 가능
    
    for target_index in test_indices:
        print(f"\n{'='*20} 인덱스 {target_index} 테스트 {'='*20}")
        await extract_15char_boundaries_v2(source_path, nodes_path, target_index)

anyio.run(main)