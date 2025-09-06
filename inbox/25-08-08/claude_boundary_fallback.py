# 생성 시간: 2025-08-08 16:50:25 KST
# 핵심 내용: Claude SDK 경계 생성 + 빈 문자열 fallback 처리
# 상세 내용:
#   - main() 함수 (라인 9-35): 메인 실행 로직, 빈 경계 검증 및 fallback 처리
#   - generate_boundaries_with_fallback() 함수 (라인 37-85): 경계 생성 + fallback 처리
#   - check_empty_boundaries() 함수 (라인 87-105): 빈 경계 문자열 검사
#   - process_empty_boundaries() 함수 (라인 107-145): 빈 경계에 대한 fallback 요청
#   - create_fallback_prompt() 함수 (라인 147-170): fallback 프롬프트 생성
# 상태: 활성
# 주소: claude_boundary_fallback
# 참조: claude_boundary_generator (기본 생성기)

import json
import asyncio
import os
import sys
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """Claude SDK 경계 생성 + fallback 처리"""
    
    if len(sys.argv) != 4:
        print("사용법: python claude_boundary_fallback.py <리프노드파일> <텍스트파일> <출력파일>")
        print("예시: python claude_boundary_fallback.py chapter1_leaf_nodes.json chapter1_text.md output.json")
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
    
    print(f"🔍 Claude SDK 경계 생성 + Fallback 시작...")
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 처리 실행
    asyncio.run(generate_boundaries_with_fallback(leaf_nodes_file, text_file, output_file))

async def generate_boundaries_with_fallback(leaf_nodes_file, text_file, output_file):
    """경계 생성 + fallback 처리"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    print(f"🌿 리프 노드: {len(leaf_nodes)}개")
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    
    try:
        # 1단계: 기본 경계 생성
        from claude_boundary_generator import create_boundary_prompt, parse_claude_response
        
        prompt = create_boundary_prompt(leaf_nodes, text_content)
        
        print(f"🤖 1단계: Claude에게 기본 경계 생성 요청...")
        
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
            result = parse_claude_response(full_response, leaf_nodes)
            
            if result:
                # 2단계: 빈 경계 검사
                empty_nodes = check_empty_boundaries(result)
                
                if empty_nodes:
                    print(f"⚠️  빈 경계 발견: {len(empty_nodes)}개 노드")
                    
                    # 3단계: fallback 처리
                    fixed_nodes = await process_empty_boundaries(empty_nodes, text_content)
                    
                    # 결과 통합
                    for fixed_node in fixed_nodes:
                        for i, node in enumerate(result):
                            if node['id'] == fixed_node['id']:
                                result[i] = fixed_node
                                break
                
                # 결과 저장
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 경계 생성 + Fallback 완료! 결과: {output_file}")
                print(f"📊 최종 처리된 노드: {len(result)}개")
            else:
                print("❌ 기본 경계 생성 실패")
        else:
            print("❌ Claude 응답 없음")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

def check_empty_boundaries(nodes):
    """빈 경계 문자열 검사"""
    
    empty_nodes = []
    
    for node in nodes:
        if not node.get('start_text', '').strip() or not node.get('end_text', '').strip():
            empty_nodes.append(node)
            print(f"   🔍 빈 경계 발견: ID {node['id']} - \"{node['title']}\"")
            print(f"      start_text: \"{node.get('start_text', '')}\"")
            print(f"      end_text: \"{node.get('end_text', '')}\"")
    
    return empty_nodes

async def process_empty_boundaries(empty_nodes, text_content):
    """빈 경계에 대한 fallback 요청"""
    
    print(f"🔧 Fallback 처리 시작: {len(empty_nodes)}개 노드")
    
    fixed_nodes = []
    
    # 작은 배치로 나누어 처리 (3개씩)
    batch_size = 3
    batches = [empty_nodes[i:i + batch_size] for i in range(0, len(empty_nodes), batch_size)]
    
    for i, batch in enumerate(batches, 1):
        print(f"\n🔄 Fallback 배치 {i}/{len(batches)} 처리 중... ({len(batch)}개 노드)")
        
        try:
            # fallback 프롬프트 생성
            fallback_prompt = create_fallback_prompt(batch, text_content)
            
            options = ClaudeCodeOptions(
                max_turns=1,
                system_prompt="간단한 제목만 JSON으로 반환하세요."
            )
            
            responses = []
            async for message in query(prompt=fallback_prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            responses.append(block.text)
            
            if responses:
                full_response = "\n".join(responses)
                from claude_boundary_generator import parse_claude_response
                batch_result = parse_claude_response(full_response, batch)
                
                if batch_result:
                    fixed_nodes.extend(batch_result)
                    print(f"   ✅ 배치 {i} 성공: {len(batch_result)}개 수정")
                else:
                    print(f"   ⚠️  배치 {i} 파싱 실패, 원본 유지")
                    fixed_nodes.extend(batch)
            else:
                print(f"   ⚠️  배치 {i} 응답 없음, 원본 유지")
                fixed_nodes.extend(batch)
            
            # 배치 간 지연
            if i < len(batches):
                print(f"   ⏳ 5초 대기...")
                await asyncio.sleep(5)
                
        except Exception as e:
            print(f"   ❌ 배치 {i} 오류: {e}, 원본 유지")
            fixed_nodes.extend(batch)
    
    return fixed_nodes

def create_fallback_prompt(nodes, text_content):
    """fallback 프롬프트 생성"""
    
    # 노드 정보
    nodes_info = ""
    for node in nodes:
        nodes_info += f"ID {node['id']}: \"{node['title']}\"\n"
    
    # 텍스트 제한 (8,000자)
    limited_text = text_content[:8000]
    if len(text_content) > 8000:
        limited_text += "\n\n[... 계속됨 ...]"
    
    prompt = f"""텍스트:
{limited_text}

다음 노드들의 간단한 경계만 찾기:
{nodes_info}

간단한 제목/키워드만 추출:
[{{"id":1,"title":"제목","level":1,"start_text":"간단한시작","end_text":"간단한끝"}}]"""
    
    return prompt

if __name__ == "__main__":
    main()