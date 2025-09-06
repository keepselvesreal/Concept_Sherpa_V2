#!/usr/bin/env python3
"""
통합 지식 Q&A 스크립트
Neon DB에서 자료 검색 → Claude 답변 생성 → 세션 저장을 한 번에 처리
"""

import os
import sys
import subprocess
from pathlib import Path

# 상위 디렉토리의 모듈들을 import하기 위한 경로 추가
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

try:
    from embedding_service_v2 import get_embedding_service
    from neon_vector_db import NeonVectorDB
    from save_qa_session import save_qa_session
except ImportError as e:
    print(f"❌ 필요한 모듈을 가져올 수 없습니다: {e}")
    print("상위 디렉토리에 embedding_service_v2.py, neon_vector_db.py가 있는지 확인하세요.")
    sys.exit(1)

import logging

# 로깅 레벨을 WARNING으로 설정하여 불필요한 로그 숨김
logging.getLogger().setLevel(logging.WARNING)

def search_neon_db(query: str, max_results: int = 3) -> dict:
    """
    Neon DB에서 질의 검색 및 결과 반환
    
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

def generate_claude_answer(query: str, search_results: dict) -> str:
    """
    검색 결과를 바탕으로 Claude 답변 생성
    
    Args:
        query: 사용자 질문
        search_results: Neon DB 검색 결과
        
    Returns:
        Claude가 생성한 답변
    """
    if not search_results['success'] or search_results['total_results'] == 0:
        return f"'{query}'에 대한 관련 정보를 데이터베이스에서 찾을 수 없습니다."
    
    # 검색 결과를 요약하여 답변 생성
    core_results = search_results['core_results']
    detailed_results = search_results['detailed_results']
    
    answer_parts = []
    
    # 질문에 대한 직접적인 답변 시작
    answer_parts.append(f"'{query}'에 대한 답변을 데이터베이스에서 찾은 자료를 바탕으로 제공드리겠습니다.\n")
    
    # 핵심 내용 기반 답변
    if core_results:
        answer_parts.append("## 📚 주요 내용\n")
        
        for i, result in enumerate(core_results[:2], 1):  # 상위 2개만 사용
            confidence = max(0, (1 - result['distance']) * 100)
            
            # 문서 내용 파싱하여 핵심 정보 추출
            doc = result['document']
            if doc.startswith('{'):  # JSON 형태
                try:
                    import json
                    doc_obj = json.loads(doc)
                    title = doc_obj.get('title', 'N/A')
                    content = doc_obj.get('content_summary', doc_obj.get('content', 'N/A'))
                    answer_parts.append(f"**{i}. {title}** (신뢰도: {confidence:.1f}%)\n")
                    answer_parts.append(f"{content}\n\n")
                except:
                    answer_parts.append(f"**{i}.** {doc[:300]}...\n\n")
            else:  # 일반 텍스트
                # 제목 추출
                title_lines = [line for line in doc.split('\n') if line.startswith('# ')]
                title = title_lines[0].replace('# ', '').strip() if title_lines else f"섹션 {i}"
                
                # 첫 번째 내용 단락 추출
                content_lines = [line.strip() for line in doc.split('\n') 
                               if line.strip() and not line.startswith('#') 
                               and not line.startswith('**') and len(line.strip()) > 20]
                content = content_lines[0] if content_lines else "내용을 찾을 수 없습니다."
                
                answer_parts.append(f"**{i}. {title}** (신뢰도: {confidence:.1f}%)\n")
                answer_parts.append(f"{content[:200]}...\n\n")
    
    # 상세 분석이 있다면 추가
    if detailed_results and len(detailed_results) > 0:
        answer_parts.append("## 🔬 추가 관련 정보\n")
        best_detailed = detailed_results[0]  # 가장 관련성 높은 것만
        confidence = max(0, (1 - best_detailed['distance']) * 100)
        answer_parts.append(f"관련 상세 분석 정보가 있습니다 (신뢰도: {confidence:.1f}%)\n\n")
    
    # 결론 및 출처
    answer_parts.append("---\n")
    answer_parts.append(f"📊 **검색 결과**: {search_results['total_results']}개 관련 자료 발견\n")
    answer_parts.append(f"🗄️ **출처**: Neon PostgreSQL 지식 데이터베이스")
    
    return "".join(answer_parts)

def run_qa_session(query: str, qa_file_path: str = None):
    """
    전체 Q&A 세션 실행: 검색 → 답변 생성 → 저장
    
    Args:
        query: 사용자 질문
        qa_file_path: 저장할 파일 경로
    """
    print(f"🔍 질의 처리 중: '{query}'")
    
    # 1. Neon DB 검색
    print("📚 데이터베이스 검색 중...")
    search_results = search_neon_db(query)
    
    if not search_results['success']:
        print(f"❌ 검색 실패: {search_results['error']}")
        return False
    
    print(f"✅ 검색 완료: {search_results['total_results']}개 결과 발견")
    
    # 2. Claude 답변 생성
    print("🤖 답변 생성 중...")
    answer = generate_claude_answer(query, search_results)
    
    # 3. 답변 출력
    print("\n" + "="*60)
    print("📝 생성된 답변:")
    print("="*60)
    print(answer)
    print("="*60 + "\n")
    
    # 4. 세션 저장
    if qa_file_path is None:
        qa_file_path = os.path.join(current_dir, 'qa_sessions.md')
    
    print("💾 세션 저장 중...")
    save_success = save_qa_session(query, answer, qa_file_path)
    
    if save_success:
        print(f"✅ 전체 Q&A 세션 완료!")
        return True
    else:
        print("❌ 세션 저장 실패")
        return False

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python knowledge_qa.py \"검색할 질의\" [저장파일경로]")
        print("예시: python knowledge_qa.py \"OOP의 문제점은 무엇인가?\"")
        sys.exit(1)
    
    # 첫 번째 인자를 질의로 사용
    query = sys.argv[1]
    
    # 선택적으로 저장 파일 경로 지정
    qa_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Q&A 세션 실행
    success = run_qa_session(query, qa_file_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()