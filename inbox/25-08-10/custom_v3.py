import anyio
import json
import re
import time
from claude_code_sdk import query, ClaudeCodeOptions, Message

async def extract_30char_boundaries_v3(source_path: str, nodes_path: str, target_index: int):
    """
    Claude SDK를 사용해 정확한 30자 경계 추출
    
    매개변수:
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
    
    # 문서 샘플링 (더 크게 설정)
    if len(source_text) > 30000:
        target_pos = source_text.find(target_title)
        if target_pos != -1:
            start_sample = max(0, target_pos - 5000)
            end_sample = min(len(source_text), target_pos + 25000)
            source_sample = source_text[start_sample:end_sample]
            print(f"📏 문서 샘플링: {len(source_sample):,}자 (전체 {len(source_text):,}자)")
        else:
            source_sample = source_text[:30000]
            print(f"📏 문서 앞부분 샘플링: {len(source_sample):,}자")
    else:
        source_sample = source_text
    
    # 다음 섹션 정보
    next_section_info = f"다음 섹션은 '{next_title}'입니다." if next_title else "이것은 문서의 마지막 섹션입니다."
    
    # 단계별 30자 경계 추출 요청
    prompt = f"""다음 단계에 따라 "{target_title}" 섹션의 30자 경계를 추출해주세요:

1단계: 섹션 제목 찾기
- 문서에서 "{target_title}" 제목이 나타나는 정확한 위치를 찾으세요

2단계: 섹션 제목 시작부터 30자를 추출하여 START_30 만들기
- "{target_title}" 제목의 첫 번째 글자부터 시작하여 정확히 30자를 추출하세요

3단계: 현재 섹션의 정확한 끝 찾기  
- {next_section_info}
- "{target_title}" 섹션 내용이 끝나고 {"다음 섹션 '" + next_title + "'이 시작되기" if next_title else "문서가 끝나는"} 직전의 위치를 찾으세요

4단계: 현재 섹션의 마지막 30자를 추출하여 END_30 만들기  
- 중요: "{target_title}" 섹션 내용의 마지막 30자만 추출하세요
- {f"다음 섹션 '{next_title}'의 텍스트는 포함하지 마세요" if next_title else "문서 끝까지가 이 섹션의 범위입니다"}
- "{target_title}" 섹션의 맨 마지막 문자부터 정확히 30자를 거슬러 올라가 계산하세요

결과 형식:
START_30: [정확히 30자]
END_30: [정확히 30자]

문서:
{source_sample}"""

    messages: list[Message] = []
    
    print(f"🧠 Claude SDK로 30자 경계 추출 시작...")
    print(f"📏 프롬프트 길이: {len(prompt):,}자")
    
    try:
        message_count = 0
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="당신은 텍스트 분석 전문가입니다. 어떤 도구도 사용하지 마시고, 텍스트 분석만으로 답변하세요. 요청된 형식으로만 답변하세요.",
                allowed_tools=[]
            )
        ):
            message_count += 1
            print(f"📨 메시지 {message_count} 수신 중...")
            messages.append(message)
        print(f"✅ Claude SDK 응답 완료 - 총 {message_count}개 메시지")
    except Exception as e:
        print(f"❌ Claude SDK 호출 실패: {e}")
        return
    
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
            print(f"  내용: {str(message)[:300]}...")
    
    # 정규식으로 30자 경계 추출 (줄바꿈 포함하여 더 유연하게)
    start_match = re.search(r'START_30:\s*["\']?(.{1,35})["\']?', response_text, re.DOTALL)
    end_match = re.search(r'END_30:\s*["\']?(.{1,35})["\']?', response_text, re.DOTALL)
    
    start_30 = start_match.group(1).strip().strip('"\'') if start_match else None
    end_30 = end_match.group(1).strip().strip('"\'') if end_match else None
    
    # 30자 추출 및 검증 로직 (최대 3회 재시도)
    max_retries = 3
    retry_count = 0
    
    # 프롬프트 생성 함수
    def create_prompt(retry_info=None):
        next_section_instruction = ""
        if "마지막 섹션" in next_section_info:
            next_section_instruction = f"""3단계: 현재 섹션의 끝 찾기
- 이것은 문서의 마지막 섹션이므로, "{target_title}" 섹션은 문서 끝까지 확장됩니다
- 예시: 현재 섹션이 "...최종 검증 규칙입니다." 로 끝나고 더 이상 내용이 없는 경계점을 식별

4단계: 현재 섹션의 마지막 30자를 추출하여 END_30 만들기
- "{target_title}" 섹션 내용의 마지막 30자를 찾으세요
- "{target_title}" 섹션의 마지막 문자부터 거슬러 올라가 정확히 30자를 추출하세요"""
        else:
            next_title_clean = next_title if next_title else ""
            next_section_instruction = f"""3단계: 섹션 간의 정확한 경계 찾기
- {next_section_info}
- "{target_title}" 섹션이 끝나고 "{next_title_clean}"이 시작되는 정확한 지점을 찾으세요
- "{target_title}" 섹션에 속하는 마지막 문자를 찾으세요 ("{next_title_clean}" 시작 전)
- 예시: 현재 섹션이 "...검증 완료." 로 끝나고 다음 섹션이 "{next_title_clean}"로 시작하는 경계점을 식별

4단계: 현재 섹션의 마지막 30자를 추출하여 END_30 만들기
- 중요: "{target_title}" 섹션 내용의 마지막 30자만 추출하세요
- "{next_title_clean}" 섹션의 텍스트는 포함하지 마세요
- "{target_title}" 섹션의 맨 마지막 문자부터 정확히 30자를 거슬러 올라가 계산하세요"""

        retry_instruction = ""
        if retry_info:
            retry_instruction = f"\n⚠️ 재시도 요청: {retry_info}\n"

        return f"""다음 단계에 따라 "{target_title}" 섹션의 30자 경계를 추출해주세요:

{next_section_info}
{retry_instruction}
1단계: 섹션 제목 찾기
- 문서에서 "{target_title}" 제목이 나타나는 정확한 위치를 찾으세요

2단계: 섹션 제목 시작부터 30자를 추출하여 START_30 만들기
- "{target_title}" 제목의 첫 번째 글자부터 시작하여 정확히 30자를 추출하세요
- 예시: "7.2 JSON Schema 개요" → "7.2 JSON Schema 개요\n내"

{next_section_instruction}

5단계: 최종 검증
- START_30이 정확히 30자이고 섹션 제목을 포함하는지 확인하세요
- END_30이 정확히 30자이고 현재 섹션의 마지막 부분에서 추출되었는지 확인하세요 (다음 섹션이 아닌)
- 예시: 현재 섹션이 "...내용의 끝."으로 끝나고 다음 섹션이 "다음 섹션 제목"으로 시작한다면,
  END_30은 "...어떤 텍스트 내용의 끝." (현재 섹션의 30자)가 되어야 하고
  "다음 섹션 제목..." (다음 섹션의 텍스트)이 되면 안됩니다

결과 형식 (추출된 정보만):
START_30: [정확히 30자]
END_30: [정확히 30자]

문서:
{source_sample}"""

    # Claude SDK 재요청 함수
    async def retry_extraction(retry_info):
        print(f"🔄 Claude SDK 재요청 시작...")
        retry_prompt = create_prompt(retry_info)
        retry_messages = []
        
        try:
            retry_message_count = 0
            async for message in query(
                prompt=retry_prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="당신은 텍스트 분석 전문가입니다. 어떤 도구도 사용하지 마시고, 텍스트 분석만으로 답변하세요. 요청된 형식으로만 답변하세요.",
                    allowed_tools=[]
                )
            ):
                retry_message_count += 1
                print(f"🔄📨 재시도 메시지 {retry_message_count} 수신...")
                retry_messages.append(message)
            print(f"✅ 재시도 완료 - {retry_message_count}개 메시지")
        except Exception as e:
            print(f"❌ 재시도 실패: {e}")
            return ""
        
        # 재시도 응답 텍스트 추출
        retry_response_text = ""
        for message in retry_messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            retry_response_text += block.text
                elif hasattr(message.content, 'text'):
                    retry_response_text += message.content.text
                else:
                    retry_response_text += str(message.content)
            elif hasattr(message, 'text'):
                retry_response_text += message.text
            else:
                msg_str = str(message)
                if 'text=' in msg_str:
                    text_matches = re.findall(r"text='([^']*)'", msg_str)
                    if not text_matches:
                        text_matches = re.findall(r'text="([^"]*)"', msg_str)
                    for text in text_matches:
                        retry_response_text += text
        
        return retry_response_text

    # Claude SDK 검증 함수
    async def validate_extraction(start_text, end_text):
        print(f"🔍 Claude SDK 검증 시작...")
        validation_prompt = f"""{target_title}" 섹션에 대해 추출된 경계가 올바른지 검증해주세요:

추출된 START_30: "{start_text}"
추출된 END_30: "{end_text}"

{next_section_info}

검증 포인트:
1. START_30이 실제로 "{target_title}" 섹션의 시작 부분인가요?
2. END_30이 실제로 해당 섹션의 끝 부분인가요?
3. 이 두 경계가 "{target_title}" 섹션의 모든 내용을 포함하나요?

간단히 "예" 또는 "아니오"로 답변하세요. 아니오인 경우, 이유를 한 문장으로 설명하세요.

문서:
{source_sample}"""
        
        validation_messages = []
        try:
            validation_message_count = 0
            async for message in query(
                prompt=validation_prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="검증 전문가로서 간결하게 답변하세요.",
                    allowed_tools=[]
                )
            ):
                validation_message_count += 1
                print(f"🔍📨 검증 메시지 {validation_message_count} 수신...")
                validation_messages.append(message)
            print(f"✅ 검증 완료 - {validation_message_count}개 메시지")
        except Exception as e:
            print(f"❌ 검증 실패: {e}")
            return "no - validation failed due to error"
        
        # 검증 응답 텍스트 추출
        validation_response = ""
        for message in validation_messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            validation_response += block.text
                elif hasattr(message.content, 'text'):
                    validation_response += message.content.text
            elif hasattr(message, 'text'):
                validation_response += message.text
        
        return validation_response

    print(f"\n🔄 검증 루프 시작 - 최대 {max_retries}회 시도")
    
    while retry_count < max_retries:
        print(f"\n--- 루프 반복 {retry_count + 1}/{max_retries} ---")
        print(f"현재 상태: START_30={len(start_30) if start_30 else 'None'}자, END_30={len(end_30) if end_30 else 'None'}자")
        
        # 30자 길이 검증 (None 값 처리)
        start_needs_retry = (start_30 is None) or (start_30 and len(start_30) != 30)
        end_needs_retry = (end_30 is None) or (end_30 and len(end_30) != 30)
        
        print(f"길이 검증: START_30 재시도={start_needs_retry}, END_30 재시도={end_needs_retry}")
        
        # 길이가 잘못된 경우 재시도
        if start_needs_retry or end_needs_retry:
            retry_count += 1
            print(f"   🔄 길이 재시도 {retry_count}/{max_retries}")
            
            retry_info_parts = []
            if start_needs_retry:
                if start_30 is None:
                    retry_info_parts.append(f"START_30이 추출되지 않았습니다. 정확히 30자를 추출해주세요.")
                else:
                    retry_info_parts.append(f"START_30이 {len(start_30)}자입니다 ('{start_30}'). 정확히 30자를 다시 추출해주세요.")
            if end_needs_retry:
                if end_30 is None:
                    retry_info_parts.append(f"END_30이 추출되지 않았습니다. 정확히 30자를 추출해주세요.")
                else:
                    retry_info_parts.append(f"END_30이 {len(end_30)}자입니다 ('{end_30}'). 정확히 30자를 다시 추출해주세요.")
            
            retry_info = " ".join(retry_info_parts)
            print(f"   📡 Claude SDK 재요청 중... ({retry_info})")
            
            start_time = time.time()
            retry_response = await retry_extraction(retry_info)
            elapsed = time.time() - start_time
            print(f"   ⏱️ 재요청 소요시간: {elapsed:.2f}초")
            
            # 재시도 결과 추출
            retry_start_match = re.search(r'START_30:\s*["\']?(.{1,35})["\']?', retry_response, re.DOTALL)
            retry_end_match = re.search(r'END_30:\s*["\']?(.{1,35})["\']?', retry_response, re.DOTALL)
            
            if retry_start_match and start_needs_retry:
                new_start_30 = retry_start_match.group(1).strip().strip('"\'')
                if len(new_start_30) >= 30:
                    start_30 = new_start_30[:30]
                    
            if retry_end_match and end_needs_retry:
                new_end_30 = retry_end_match.group(1).strip().strip('"\'')
                if len(new_end_30) >= 30:
                    end_30 = new_end_30[:30]
            
            continue
        
        # 길이가 올바른 경우 내용 검증 수행
        if start_30 and end_30 and len(start_30) == 30 and len(end_30) == 30:
            print(f"   ✓ 길이 검증 통과 - Claude SDK로 내용 검증 중...")
            
            start_time = time.time()
            validation_result = await validate_extraction(start_30, end_30)
            elapsed = time.time() - start_time
            print(f"   ⏱️ 검증 소요시간: {elapsed:.2f}초")
            print(f"   🔍 검증 결과: {validation_result}")
            
            # 검증 결과 분석
            if "yes" in validation_result.lower():
                print(f"   ✅ 내용 검증 통과!")
                break
            else:
                retry_count += 1
                print(f"   🔄 내용 재시도 {retry_count}/{max_retries}")
                
                retry_info = f"이전 추출 결과가 올바르지 않았습니다: {validation_result}. 더 정확한 30자 경계를 다시 추출해주세요."
                print(f"   📡 Claude SDK 재요청 중... (내용 검증 실패)")
                
                retry_response = await retry_extraction(retry_info)
                
                # 재시도 결과 추출
                retry_start_match = re.search(r'START_30:\s*["\']?(.{1,35})["\']?', retry_response, re.DOTALL)
                retry_end_match = re.search(r'END_30:\s*["\']?(.{1,35})["\']?', retry_response, re.DOTALL)
                
                if retry_start_match:
                    new_start_30 = retry_start_match.group(1).strip().strip('"\'')
                    if len(new_start_30) >= 30:
                        start_30 = new_start_30[:30]
                        
                if retry_end_match:
                    new_end_30 = retry_end_match.group(1).strip().strip('"\'')
                    if len(new_end_30) >= 30:
                        end_30 = new_end_30[:30]
        else:
            break
    
    # 최종 결과 처리
    if start_30 and end_30 and len(start_30) == 30 and len(end_30) == 30:
        print(f"✅ 30자 경계 추출 및 검증 성공!")
        print(f"   📍 시작 30자: '{start_30}'")
        print(f"   📍 종료 30자: '{end_30}'")
        
        # 원문에서 검증
        start_pos = source_text.find(start_30)
        end_pos = source_text.find(end_30)
        
        if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
            section_length = end_pos - start_pos + len(end_30)
            print(f"✅ 원문 검증 성공! 추출될 섹션 길이: {section_length:,}자")
            print(f"   📍 시작 위치: {start_pos:,}, 종료 위치: {end_pos:,}")
            
            # 추출된 섹션 전체 확인
            extracted_section = source_text[start_pos:end_pos + len(end_30)]
            
            print(f"\n📋 추출된 경계 상세 정보:")
            print(f"=" * 60)
            print(f"🎯 섹션: {target_title}")
            print(f"📏 전체 길이: {len(extracted_section):,}자")
            print(f"")
            print(f"🔹 시작 경계 (30자): '{start_30}'")
            print(f"   분석: 제목 + 직후 내용")
            print(f"   원문 위치: {start_pos:,}")
            print(f"")
            print(f"🔹 종료 경계 (30자): '{end_30}'")
            print(f"   분석: 마지막 내용 + 다음 섹션 시작")
            print(f"   원문 위치: {end_pos:,}")
            print(f"")
            print(f"📖 추출된 섹션 시작 (100자):")
            print(f"'{extracted_section[:100]}...'")
            print(f"")
            print(f"📖 추출된 섹션 끝 (100자):")
            print(f"'...{extracted_section[-100:]}'")
            print(f"=" * 60)
            
            # 리프노드 업데이트
            leaf_nodes[target_index]['start_text'] = start_30
            leaf_nodes[target_index]['end_text'] = end_30
            
            # 업데이트된 리프노드 저장
            output_path = nodes_path.replace('.json', '_v3_30char_boundaries.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(leaf_nodes, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 업데이트된 리프노드 저장: {output_path}")
            
        else:
            print(f"❌ 원문 검증 실패:")
            print(f"   시작 위치: {start_pos} (찾았음: {start_pos != -1})")
            print(f"   종료 위치: {end_pos} (찾았음: {end_pos != -1})")
            if start_pos != -1 and end_pos != -1:
                print(f"   위치 순서: {'올바름' if start_pos < end_pos else '잘못됨'}")
            
    else:
        print(f"❌ 30자 경계 추출 최종 실패")
        print(f"   시작 30자: '{start_30}' (길이: {len(start_30) if start_30 else 0})")
        print(f"   종료 30자: '{end_30}' (길이: {len(end_30) if end_30 else 0})")
        if retry_count >= max_retries:
            print(f"   최대 재시도 횟수 ({max_retries}회) 초과")

async def main():
    """메인 실행 함수"""
    print("🚀 Claude SDK 정확한 30자 경계 추출 (v3 - 재시도+검증)")
    print("=" * 65)
    
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
    
    # 테스트
    target_index = 2  # 7.2 JSON Schema 개요
    
    print(f"\n{'='*25} 테스트 시작 {'='*25}")
    await extract_30char_boundaries_v3(source_path, nodes_path, target_index)

anyio.run(main)