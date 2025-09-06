# 생성 시간: 2025-08-09 15:45:00 KST
# 핵심 내용: 병렬 처리 방식으로 리프 노드 경계 추출 - 15자 이내 시작/종료 문자열
# 상세 내용:
#   - main() 함수 (라인 11-45): 메인 실행 로직 및 파라미터 처리
#   - extract_chapter7_nodes() 함수 (라인 47-65): 7장 관련 노드만 필터링
#   - process_parallel_boundaries() 함수 (라인 67-120): 병렬 처리 로직
#   - extract_node_context() 함수 (라인 122-145): 각 노드 주변 컨텍스트 추출
#   - create_boundary_prompt() 함수 (라인 147-170): Claude 요청 프롬프트 생성
#   - parse_boundary_response() 함수 (라인 172-205): Claude 응답 파싱
# 상태: 활성
# 주소: parallel_boundary_extractor
# 참조: simple_claude_boundary, part2_scalability_leaf_nodes.json

import json
import asyncio
import os
import sys
import re
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

def main():
    """병렬 처리 방식 경계 추출 실험"""
    
    if len(sys.argv) != 4:
        print("사용법: python parallel_boundary_extractor.py <리프노드파일> <텍스트파일> <출력파일>")
        print("예시: python parallel_boundary_extractor.py part2_scalability_leaf_nodes.json Level01_7_Basic_data_validation.md chapter7_boundaries.json")
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
    
    print(f"🚀 병렬 경계 추출 시작...")
    print(f"📄 리프 노드: {leaf_nodes_file}")
    print(f"📖 텍스트: {text_file}")
    print(f"💾 출력: {output_file}")
    
    # 비동기 처리 실행
    asyncio.run(process_parallel_boundaries(leaf_nodes_file, text_file, output_file))

def extract_chapter7_nodes(leaf_nodes):
    """7장 관련 노드만 필터링"""
    
    chapter7_nodes = []
    in_chapter7 = False
    
    for node in leaf_nodes:
        title = node.get("title", "")
        
        # 7장 시작 감지
        if title.startswith("7 ") or title.startswith("7."):
            in_chapter7 = True
            chapter7_nodes.append(node)
        # 8장 시작 시 종료
        elif title.startswith("8 ") or title.startswith("8."):
            break
        # 7장 내부 노드들
        elif in_chapter7:
            chapter7_nodes.append(node)
    
    print(f"🔍 7장 노드 필터링: 전체 {len(leaf_nodes)}개 → 7장 {len(chapter7_nodes)}개")
    return chapter7_nodes

async def process_parallel_boundaries(leaf_nodes_file, text_file, output_file):
    """병렬 처리로 경계 추출"""
    
    # 데이터 로드
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        all_nodes = json.load(f)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    # 7장 노드만 추출
    chapter7_nodes = extract_chapter7_nodes(all_nodes)
    
    if len(chapter7_nodes) < 2:
        print("❌ 7장 노드가 충분하지 않음")
        return
    
    print(f"📏 텍스트 길이: {len(text_content):,} 문자")
    print(f"🌿 처리할 노드: {len(chapter7_nodes)}개")
    
    # 중간 노드들 (첫째, 마지막 제외)
    middle_nodes = chapter7_nodes[1:-1]  
    results = []
    
    try:
        # 중간 노드들 병렬 처리
        print(f"⚡ 병렬 처리 시작: {len(middle_nodes)}개 노드")
        
        for i, node in enumerate(middle_nodes):
            print(f"🔄 처리 중: {node['title']}")
            
            # 컨텍스트 추출
            context = extract_node_context(text_content, node["title"])
            
            if context:
                # Claude 요청
                boundary_data = await request_boundary_from_claude(node, context)
                
                if boundary_data:
                    # 원본 인덱스 계산 (전체 배열에서의 위치)
                    original_index = i + 1  # 중간 노드이므로 +1
                    
                    results.append({
                        "original_index": original_index,
                        "node": node,
                        "boundaries": boundary_data
                    })
                    
                    print(f"✅ 완료: {node['title']} → start: '{boundary_data.get('start_text', '')}', end: '{boundary_data.get('end_text', '')}'")
                else:
                    print(f"❌ 실패: {node['title']}")
            else:
                print(f"⚠️ 컨텍스트 없음: {node['title']}")
        
        # 결과 적용 (병렬 처리 결과를 순차적으로 적용)
        updated_nodes = chapter7_nodes.copy()
        
        for result in results:
            idx = result["original_index"]
            boundaries = result["boundaries"]
            
            # 현재 노드에 시작점 적용
            updated_nodes[idx]["start_text"] = boundaries.get("start_text", "")
            
            # 이전 노드에 종료점 적용
            if idx > 0:
                updated_nodes[idx - 1]["end_text"] = boundaries.get("start_text", "")
        
        # 첫째와 마지막 노드 처리
        handle_first_and_last_nodes(updated_nodes, text_content)
        
        # 결과 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_nodes, f, ensure_ascii=False, indent=2)
        
        print(f"🎉 병렬 경계 추출 완료! 결과: {output_file}")
        print(f"📊 처리된 노드: {len(updated_nodes)}개")
        
    except Exception as e:
        print(f"❌ 오류: {e}")

def extract_node_context(text_content, node_title, context_size=800):
    """각 노드 제목 주변 컨텍스트 추출"""
    
    # 제목 패턴 생성 (유연한 매칭)
    title_clean = node_title.replace(".", r"\.").replace(" ", r"\s+")
    pattern = rf"{re.escape(title_clean)}"
    
    match = re.search(pattern, text_content, re.IGNORECASE)
    
    if match:
        start_pos = max(0, match.start() - context_size // 2)
        end_pos = min(len(text_content), match.end() + context_size // 2)
        
        context = text_content[start_pos:end_pos]
        print(f"🎯 컨텍스트 추출: {node_title} → {len(context)}자")
        return context
    else:
        print(f"⚠️ 제목 못 찾음: {node_title}")
        return None

async def request_boundary_from_claude(node, context):
    """Claude에게 경계 추출 요청"""
    
    prompt = create_boundary_prompt(node, context)
    
    try:
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="정확한 JSON만 반환하세요. 추가 설명은 불필요합니다."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
        
        if responses:
            full_response = "\n".join(responses)
            return parse_boundary_response(full_response)
        
    except Exception as e:
        print(f"❌ Claude 요청 오류: {e}")
    
    return None

def create_boundary_prompt(node, context):
    """Claude 요청 프롬프트 생성"""
    
    prompt = f"""다음 텍스트에서 섹션 "{node['title']}"의 정확한 경계를 찾아주세요.

텍스트:
{context}

요구사항:
1. start_text: 이 섹션이 시작되는 고유한 문자열 (정확히 15자 이내)
2. end_text: 이 섹션이 끝나고 다음 섹션이 시작되는 지점의 고유한 문자열 (정확히 15자 이내)

응답 형식 (JSON만):
{{
    "start_text": "섹션 시작 문자열",
    "end_text": "다음 섹션 시작 문자열"
}}"""
    
    return prompt

def parse_boundary_response(response_text):
    """Claude 응답 파싱"""
    
    try:
        # JSON 블록 찾기
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        json_matches = re.findall(json_pattern, response_text)
        
        json_text = ""
        if json_matches:
            json_text = json_matches[0].strip()
        else:
            # JSON 객체 직접 찾기
            json_pattern2 = r'\{[^{}]*"start_text"[^{}]*"end_text"[^{}]*\}'
            json_matches2 = re.findall(json_pattern2, response_text)
            if json_matches2:
                json_text = json_matches2[0].strip()
        
        if json_text:
            parsed_data = json.loads(json_text)
            
            # 15자 제한 검증
            start_text = parsed_data.get("start_text", "")
            end_text = parsed_data.get("end_text", "")
            
            if len(start_text) > 15:
                start_text = start_text[:15]
            if len(end_text) > 15:
                end_text = end_text[:15]
            
            return {
                "start_text": start_text,
                "end_text": end_text
            }
        
        print(f"⚠️ JSON 파싱 실패")
        return None
        
    except Exception as e:
        print(f"❌ 응답 파싱 오류: {e}")
        return None

def handle_first_and_last_nodes(nodes, text_content):
    """첫째와 마지막 노드 특별 처리"""
    
    if len(nodes) < 2:
        return
    
    # 첫째 노드: 시작점만 설정 (문서 시작부터)
    first_node = nodes[0]
    first_title = first_node["title"]
    
    # 첫째 노드 제목 찾기
    title_pattern = re.escape(first_title.replace(".", r"\."))
    match = re.search(title_pattern, text_content, re.IGNORECASE)
    
    if match:
        start_pos = max(0, match.start() - 10)
        start_text = text_content[start_pos:start_pos + 15].strip()
        nodes[0]["start_text"] = start_text[:15]
    
    # 마지막 노드: 종료점만 설정 (문서 끝까지)
    last_node = nodes[-1]
    
    # Summary나 마지막 섹션 끝을 찾기
    summary_pattern = r'Summary|정리|요약'
    matches = list(re.finditer(summary_pattern, text_content, re.IGNORECASE))
    
    if matches:
        last_match = matches[-1]
        end_pos = min(len(text_content), last_match.end() + 50)
        end_text = text_content[end_pos-15:end_pos].strip()
        nodes[-1]["end_text"] = end_text[-15:] if len(end_text) > 15 else end_text

if __name__ == "__main__":
    main()