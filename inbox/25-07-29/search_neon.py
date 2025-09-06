#!/usr/bin/env python3
"""
Neon DB 검색 전용 스크립트
사용자 질의에 대한 관련 자료만 조회하여 반환 (답변 생성 X)
Claude Code 세션에서 도구로 사용
"""

import os
import sys
import json
from pathlib import Path

# 상위 디렉토리의 모듈들을 import하기 위한 경로 추가
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

try:
    from embedding_service_v2 import get_embedding_service
    from neon_vector_db import NeonVectorDB
except ImportError as e:
    print(f"❌ 필요한 모듈을 가져올 수 없습니다: {e}")
    print("상위 디렉토리에 embedding_service_v2.py, neon_vector_db.py가 있는지 확인하세요.")
    sys.exit(1)

import logging

# 로깅 레벨을 WARNING으로 설정하여 불필요한 로그 숨김
logging.getLogger().setLevel(logging.WARNING)

def search_neon_db(query: str, max_results: int = 3) -> dict:
    """
    Neon DB에서 질의와 관련된 자료만 검색하여 반환
    
    Args:
        query: 검색 질의
        max_results: 최대 결과 수
        
    Returns:
        검색 결과 딕셔너리
    """
    try:
        # 시스템 초기화
        embedding_service = get_embedding_service()
        neon_db = NeonVectorDB()
        
        # 질의를 임베딩으로 변환
        query_embedding = embedding_service.create_embedding(query)
        
        # 핵심 내용 검색
        core_results = neon_db.search_core_content(query_embedding, max_results)
        
        # 상세 내용 검색
        detailed_results = neon_db.search_detailed_content(query_embedding, max_results)
        
        # 상세 내용에 원문 추가
        for result in detailed_results:
            if result['core_ref']:
                original = neon_db.get_core_content_by_id(result['core_ref'])
                if original:
                    result['original_content'] = original['document']
        
        # 리소스 정리
        neon_db.close()
        
        return {
            'success': True,
            'core_results': core_results,
            'detailed_results': detailed_results,
            'total_results': len(core_results) + len(detailed_results)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'core_results': [],
            'detailed_results': [],
            'total_results': 0
        }

def format_search_results_for_claude(query: str, search_results: dict) -> str:
    """
    검색 결과를 Claude Code가 활용할 수 있는 형태로 포매팅
    답변 생성은 하지 않고, 자료만 정리하여 제공
    
    Args:
        query: 사용자 질문
        search_results: Neon DB 검색 결과
        
    Returns:
        Claude에게 제공할 자료 정보
    """
    if not search_results['success'] or search_results['total_results'] == 0:
        return f"🤔 '{query}'와 관련된 자료를 데이터베이스에서 찾을 수 없습니다.\n\n일반적인 지식을 바탕으로 답변해주세요."
    
    output_parts = []
    
    output_parts.append(f"📚 **사용자 질의**: '{query}'\n")
    output_parts.append(f"🔍 **데이터베이스 검색 결과**: {search_results['total_results']}개 관련 자료 발견\n")
    output_parts.append("다음 자료들을 참고하여 사용자 질문에 답변해주세요:\n\n")
    
    core_results = search_results['core_results']
    detailed_results = search_results['detailed_results']
    
    # 핵심 내용 자료
    if core_results:
        output_parts.append("## 📖 주요 참고 자료\n")
        
        for i, result in enumerate(core_results, 1):
            confidence = max(0, (1 - result['distance']) * 100)
            output_parts.append(f"### 자료 {i} (관련도: {confidence:.1f}%)\n")
            
            # 문서 내용 파싱
            doc = result['document']
            if doc.startswith('{'):  # JSON 형태 (상위 섹션)
                try:
                    doc_obj = json.loads(doc)
                    output_parts.append(f"**제목**: {doc_obj.get('title', 'N/A')}\n")
                    output_parts.append(f"**내용 요약**: {doc_obj.get('content_summary', 'N/A')}\n")
                    if doc_obj.get('composed_of'):
                        output_parts.append(f"**하위 구성**: {', '.join(doc_obj['composed_of'])}\n")
                except:
                    output_parts.append(f"**내용**: {doc[:500]}...\n")
            else:  # 일반 텍스트 (하위 섹션)
                # 제목 추출
                title_lines = [line for line in doc.split('\n') if line.startswith('# ')]
                if title_lines:
                    title = title_lines[0].replace('# ', '').strip()
                    output_parts.append(f"**제목**: {title}\n")
                
                # 페이지 정보 추출
                page_lines = [line for line in doc.split('\n') if '페이지 범위' in line]
                if page_lines:
                    page_info = page_lines[0].split('**페이지 범위:**')[1].strip() if '**페이지 범위:**' in page_lines[0] else 'N/A'
                    output_parts.append(f"**페이지**: {page_info}\n")
                
                # 내용 추출 (더 많이 표시)
                content_lines = [line.strip() for line in doc.split('\n') 
                               if line.strip() and not line.startswith('#') 
                               and not line.startswith('**')]
                content_text = '\n'.join(content_lines[:10])  # 첫 10줄
                if content_text:
                    output_parts.append(f"**내용**:\n{content_text}\n")
            
            output_parts.append("---\n")
    
    # 상세 분석 자료 (간략하게)
    if detailed_results:
        output_parts.append("## 🔬 추가 참고 자료\n")
        best_detailed = detailed_results[0]  # 가장 관련성 높은 것만
        confidence = max(0, (1 - best_detailed['distance']) * 100)
        output_parts.append(f"관련 상세 분석 자료 (관련도: {confidence:.1f}%): {best_detailed['id']}\n")
        if best_detailed.get('original_content'):
            original = best_detailed['original_content']
            if original.startswith('{'):
                try:
                    doc_obj = json.loads(original)
                    output_parts.append(f"참조 섹션: {doc_obj.get('title', 'N/A')}\n")
                except:
                    pass
        output_parts.append("\n")
    
    # 마무리 안내
    output_parts.append("---\n")
    output_parts.append("💡 **참고**: 위 자료들을 바탕으로 사용자의 질문에 대해 정확하고 도움이 되는 답변을 제공해주세요.\n")
    output_parts.append(f"🗄️ **출처**: Neon PostgreSQL 지식 데이터베이스")
    
    return "".join(output_parts)

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python3 search_neon.py \"검색할 질의\" [최대결과수]")
        print("예시: python3 search_neon.py \"OOP의 문제점은 무엇인가?\"")
        sys.exit(1)
    
    # 첫 번째 인자를 질의로 사용
    query = sys.argv[1]
    
    # 선택적으로 최대 결과 수 지정 (기본값: 3)
    max_results = 3
    if len(sys.argv) > 2:
        try:
            max_results = int(sys.argv[2])
        except ValueError:
            print("❌ 최대 결과 수는 숫자여야 합니다.")
            sys.exit(1)
    
    # DB 검색 실행
    search_results = search_neon_db(query, max_results)
    
    # Claude Code를 위한 자료 포매팅 및 출력
    formatted_output = format_search_results_for_claude(query, search_results)
    print(formatted_output)

if __name__ == "__main__":
    main()