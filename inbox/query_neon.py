#!/usr/bin/env python3
"""
Neon DB 질의 스크립트
첫 번째 인자로 질의를 받아서 Neon PostgreSQL에서 검색하고 출처와 함께 결과 반환
"""

import sys
import json
from embedding_service_v2 import get_embedding_service
from neon_vector_db import NeonVectorDB
import logging

# 로깅 레벨을 WARNING으로 설정하여 불필요한 로그 숨김
logging.getLogger().setLevel(logging.WARNING)

def query_neon_db(query: str, max_results: int = 3) -> str:
    """
    Neon DB에서 질의 검색 및 결과 반환
    
    Args:
        query: 검색 질의
        max_results: 최대 결과 수
        
    Returns:
        포매팅된 검색 결과
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
        
        # 결과 포매팅
        output = format_search_results(query, core_results, detailed_results)
        
        # 리소스 정리
        neon_db.close()
        
        return output
        
    except Exception as e:
        return f"❌ 검색 중 오류 발생: {str(e)}"

def format_search_results(query: str, core_results: list, detailed_results: list) -> str:
    """검색 결과 포매팅"""
    
    if not core_results and not detailed_results:
        return f"🤔 '{query}'에 대한 관련 정보를 찾을 수 없습니다."
    
    output = f"## 🔍 질의: '{query}'\n\n"
    
    # 핵심 내용 결과
    if core_results:
        output += "### 📚 핵심 내용\n\n"
        
        for i, result in enumerate(core_results, 1):
            confidence = max(0, (1 - result['distance']) * 100)
            
            output += f"**{i}. {result['id']}** (신뢰도: {confidence:.1f}%)\n"
            
            # 문서 내용 파싱
            doc = result['document']
            if doc.startswith('{'):  # JSON 형태 (상위 섹션)
                try:
                    doc_obj = json.loads(doc)
                    output += f"- **제목**: {doc_obj.get('title', 'N/A')}\n"
                    output += f"- **요약**: {doc_obj.get('content_summary', 'N/A')}\n"
                    if doc_obj.get('composed_of'):
                        output += f"- **하위 구성**: {', '.join(doc_obj['composed_of'])}\n"
                except:
                    output += f"- **내용**: {doc[:200]}...\n"
            else:  # 일반 텍스트 (하위 섹션)
                # 제목 추출
                title_lines = [line for line in doc.split('\n') if line.startswith('# ')]
                if title_lines:
                    title = title_lines[0].replace('# ', '').strip()
                    output += f"- **제목**: {title}\n"
                
                # 페이지 정보 추출
                page_lines = [line for line in doc.split('\n') if '페이지 범위' in line]
                if page_lines:
                    page_info = page_lines[0].split('**페이지 범위:**')[1].strip() if '**페이지 범위:**' in page_lines[0] else 'N/A'
                    output += f"- **페이지**: {page_info}\n"
                
                # 첫 번째 내용 단락 추출
                content_lines = [line.strip() for line in doc.split('\n') 
                               if line.strip() and not line.startswith('#') 
                               and not line.startswith('**') and len(line.strip()) > 20]
                if content_lines:
                    first_content = content_lines[0][:150]
                    output += f"- **내용**: {first_content}...\n"
            
            output += f"- **출처**: Neon DB - core_content 테이블\n\n"
    
    # 상세 내용 결과
    if detailed_results:
        output += "### 🔬 상세 분석\n\n"
        
        for i, result in enumerate(detailed_results, 1):
            confidence = max(0, (1 - result['distance']) * 100)
            
            output += f"**{i}. {result['id']}** (신뢰도: {confidence:.1f}%)\n"
            output += f"- **원문 참조**: {result['core_ref']}\n"
            
            # 참조된 원문 정보 표시
            if result.get('original_content'):
                original = result['original_content']
                if original.startswith('{'):
                    try:
                        doc_obj = json.loads(original)
                        output += f"- **참조 섹션**: {doc_obj.get('title', 'N/A')}\n"
                    except:
                        pass
                else:
                    title_lines = [line for line in original.split('\n') if line.startswith('# ')]
                    if title_lines:
                        title = title_lines[0].replace('# ', '').strip()
                        output += f"- **참조 섹션**: {title}\n"
            
            output += f"- **출처**: Neon DB - detailed_content 테이블\n\n"
    
    # 검색 통계
    total_results = len(core_results) + len(detailed_results)
    output += f"---\n"
    output += f"📊 **검색 통계**: {total_results}개 결과 (핵심: {len(core_results)}, 상세: {len(detailed_results)})\n"
    output += f"🗄️ **데이터베이스**: Neon PostgreSQL + pgvector\n"
    
    return output

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python query_neon.py \"검색할 질의\"")
        print("예시: python query_neon.py \"OOP의 문제점은 무엇인가?\"")
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
    
    # 질의 실행 및 결과 출력
    result = query_neon_db(query, max_results)
    print(result)

if __name__ == "__main__":
    main()