"""
생성 시간: 2024-08-11 15:40:00 KST
핵심 내용: Claude SDK를 사용한 TOC 리프 노드 병렬 추출 및 저장
상세 내용:
    - extract_with_claude(): Claude SDK로 TOC 구조 분석 및 리프 노드 추출
    - save_upper_level_nodes(nodes): 장보다 상위 수준 리프 노드 저장
    - save_chapter_nodes(chapter_key, chapter_data): 개별 장 리프 노드 저장
    - 병렬 처리로 모든 저장 작업 동시 실행
상태: 활성
주소: parallel_leaf_extractor
참조: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json
"""

import anyio
import asyncio
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from claude_code_sdk import query, ClaudeCodeOptions

async def save_upper_level_nodes(nodes):
    """장보다 상위 수준의 리프 노드 저장"""
    with open('upper_level_leaf_nodes.json', 'w', encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)
    print(f'장보다 상위 수준 리프 노드 {len(nodes)}개 저장 완료')
    return len(nodes)

async def save_chapter_nodes(chapter_key, chapter_data):
    """개별 장의 리프 노드 저장"""
    with open(f'{chapter_key}_leaf_nodes.json', 'w', encoding='utf-8') as f:
        json.dump(chapter_data, f, ensure_ascii=False, indent=2)
    print(f'{chapter_key}: {len(chapter_data)}개 리프 노드 저장 완료')
    return chapter_key, len(chapter_data)

def fallback_classify_nodes(leaf_nodes, toc_data):
    """Claude 응답 실패 시 로컬 로직으로 리프 노드 분류"""
    print("로컬 분류 로직 실행 중...")
    
    # TOC 딕셔너리 생성 (빠른 검색용)
    toc_dict = {item['id']: item for item in toc_data}
    
    upper_level = []
    chapter_level = {}
    
    for leaf in leaf_nodes:
        # level이 0이거나 1이면서 Part, Appendix, Introduction 등을 포함하는 경우 상위 레벨로 분류
        if (leaf['level'] <= 1 and 
            any(keyword in leaf['title'] for keyword in ['Part', 'Appendix', 'Introduction', 'Conclusion'])):
            upper_level.append(leaf)
        else:
            # 부모를 추적해서 장 찾기
            parent_chapter = find_chapter_parent(leaf, toc_dict)
            if parent_chapter:
                chapter_num = extract_chapter_number(parent_chapter['title'])
                if chapter_num:
                    chapter_key = f"chapter_{chapter_num}"
                    
                    if chapter_key not in chapter_level:
                        chapter_level[chapter_key] = []
                    
                    chapter_level[chapter_key].append(leaf)
                else:
                    # 장 번호를 추출할 수 없는 경우 상위 레벨로 분류
                    upper_level.append(leaf)
            else:
                # 부모 장을 찾지 못한 경우 상위 레벨로 분류
                upper_level.append(leaf)
    
    print(f"로컬 분류 결과: 상위 레벨 {len(upper_level)}개, 장 레벨 {sum(len(nodes) for nodes in chapter_level.values())}개")
    
    return {
        'upper_level_leaf_nodes': upper_level,
        'chapter_level_leaf_nodes': chapter_level
    }

def find_chapter_parent(leaf_node, toc_dict):
    """리프 노드의 부모 중에서 장에 해당하는 노드를 찾기"""
    current_id = leaf_node.get('parent_id')
    
    while current_id is not None:
        current_node = toc_dict.get(current_id)
        if not current_node:
            break
        
        # level=1이면서 숫자로 시작하는 제목이면 장으로 판단
        if (current_node['level'] == 1 and 
            any(current_node['title'].strip().startswith(str(i)) for i in range(1, 20))):
            return current_node
        
        current_id = current_node.get('parent_id')
    
    return None

def extract_chapter_number(title):
    """제목에서 장 번호 추출"""
    import re
    # "1 Complexity..." → "01"
    # "2 Separation..." → "02"
    match = re.match(r'^(\d+)', title.strip())
    if match:
        return match.group(1).zfill(2)
    return None

async def extract_with_claude():
    # TOC 데이터 로드
    toc_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json'
    with open(toc_file, 'r', encoding='utf-8') as f:
        toc_data = json.load(f)
    
    print(f'총 {len(toc_data)}개 TOC 항목 로드됨')
    
    # 먼저 리프 노드만 로컬에서 식별
    leaf_nodes = [item for item in toc_data if not item.get('children_ids') or len(item.get('children_ids', [])) == 0]
    print(f'식별된 리프 노드: {len(leaf_nodes)}개')
    
    # Claude에게 리프 노드 분류만 요청 (데이터 크기 축소)
    prompt = f'''
다음 리프 노드들을 구조에 따라 두 그룹으로 분류해주세요:

리프 노드 데이터: {json.dumps(leaf_nodes, ensure_ascii=False, indent=2)}

분류 기준:
1. 장보다 상위 수준: 더 큰 단위에 해당하는 리프 노드들
2. 장 수준: 각 장에 속하는 리프 노드들

다음 JSON 형식으로 응답해주세요:
{{
  "upper_level_leaf_nodes": [
    {{"id": 노드ID, "title": "제목", "level": 레벨}}
  ],
  "chapter_level_leaf_nodes": {{
    "chapter_01": [
      {{"id": 노드ID, "title": "제목", "level": 레벨}}
    ]
  }}
}}
'''
    
    try:
        print('Claude SDK로 리프 노드 추출 중...')
        
        # Claude 호출
        messages = []
        async for message in query(
            prompt=prompt,
            options=ClaudeCodeOptions(
                max_turns=1,
                system_prompt="JSON 목차 데이터 분석 전문가. 리프 노드를 정확히 식별하고 구조에 따라 분류하여 JSON 형식으로 반환하세요.",
                allowed_tools=[]
            )
        ):
            messages.append(message)
        
        # 응답 추출
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        
        content = content.strip()
        
        print(f"Claude 응답 길이: {len(content)}")
        if len(content) > 0:
            print(f"Claude 응답 내용 (처음 500자): {content[:500]}")
        else:
            print("Claude 응답이 비어있습니다. messages 확인:")
            for i, msg in enumerate(messages):
                print(f"메시지 {i}: {type(msg)} - {hasattr(msg, 'content')}")
                if hasattr(msg, 'content'):
                    print(f"  content type: {type(msg.content)}")
                    print(f"  content: {str(msg.content)[:200]}")
        
        # JSON 추출 및 Fallback 로직
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end != -1:
            json_str = content[start:end]
            print(f"추출된 JSON (처음 200자): {json_str[:200]}")
            
            try:
                result = json.loads(json_str)
                
                # 필수 키 존재 확인
                if 'upper_level_leaf_nodes' not in result or 'chapter_level_leaf_nodes' not in result:
                    raise ValueError("필수 키가 누락된 응답")
                
                print("Claude 응답 파싱 성공")
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON 파싱 실패: {e}")
                print("Fallback: 로컬 로직으로 분류 처리")
                result = fallback_classify_nodes(leaf_nodes, toc_data)
            
        else:
            print("JSON 구조를 찾을 수 없음")
            print("Fallback: 로컬 로직으로 분류 처리")
            result = fallback_classify_nodes(leaf_nodes, toc_data)
        
        # 병렬 처리를 위한 태스크 생성
        tasks = []
        
        # 장보다 상위 수준 노드 저장 태스크
        tasks.append(save_upper_level_nodes(result['upper_level_leaf_nodes']))
        
        # 각 장별 노드 저장 태스크들
        for chapter_key, chapter_data in result['chapter_level_leaf_nodes'].items():
            tasks.append(save_chapter_nodes(chapter_key, chapter_data))
        
        print(f'{len(tasks)}개 저장 작업을 병렬로 실행 중...')
        # 모든 저장 작업 병렬 실행
        results = await asyncio.gather(*tasks)
        
        # 결과 집계
        upper_count = results[0]  # 첫 번째는 상위 수준 카운트
        chapter_results = results[1:]  # 나머지는 장별 결과
        
        # 요약 정보
        summary = {
            'source_file': toc_file,
            'timestamp': '2024-08-11T15:40:00+09:00',
            'total_upper_level': upper_count,
            'total_chapters': len(chapter_results),
            'chapter_details': {chapter: count for chapter, count in chapter_results},
            'total_chapter_nodes': sum(count for _, count in chapter_results)
        }
        
        with open('extraction_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print('요약 정보 저장 완료')
        
        print(f'\\n=== 병렬 처리 완료 ===')
        print(f'장보다 상위 수준: {summary["total_upper_level"]}개')
        print(f'처리된 장 수: {summary["total_chapters"]}개')
        print(f'총 장 수준 노드: {summary["total_chapter_nodes"]}개')
        print(f'저장된 파일들: {len(tasks)}개')
            
    except Exception as e:
        print(f'오류: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    anyio.run(extract_with_claude)