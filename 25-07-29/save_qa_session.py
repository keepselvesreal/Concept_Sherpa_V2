#!/usr/bin/env python3
"""
Q&A 세션 기록 저장 스크립트
사용자 질문과 Claude Code의 답변을 지정된 형식으로 파일에 저장
"""

import os
import sys
import subprocess
from datetime import datetime

def get_korean_time():
    """date 명령어를 사용하여 한국 시간 반환"""
    try:
        # TZ=Asia/Seoul로 한국 시간 가져오기
        result = subprocess.run(
            ['date', '+%Y-%m-%d %H:%M:%S'],
            env={**os.environ, 'TZ': 'Asia/Seoul'},
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        # 폴백: Python datetime 사용
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_next_session_number(qa_file_path):
    """다음 세션 번호 계산"""
    if not os.path.exists(qa_file_path):
        return 1
    
    try:
        with open(qa_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 세션 번호 찾기 (세션1, 세션2, ... 형태)
        import re
        session_matches = re.findall(r'세션(\d+)', content)
        if session_matches:
            last_session = max(int(num) for num in session_matches)
            return last_session + 1
        else:
            return 1
    except Exception:
        return 1

def save_qa_session(question, answer, qa_file_path='qa_sessions.md'):
    """
    Q&A 세션을 파일에 저장
    
    Args:
        question: 사용자 질문
        answer: Claude Code의 답변
        qa_file_path: 저장할 파일 경로
    """
    try:
        # 다음 세션 번호 계산
        session_num = get_next_session_number(qa_file_path)
        
        # 한국 시간 가져오기
        korean_time = get_korean_time()
        
        # 새로운 세션 내용 생성
        new_session = f"""세션{session_num}(시작 시간: {korean_time})
질문: {question}
답변: {answer}

"""
        
        # 파일에 추가 또는 생성
        with open(qa_file_path, 'a', encoding='utf-8') as f:
            f.write(new_session)
        
        print(f"✅ 세션{session_num} 저장 완료: {qa_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 세션 저장 실패: {e}")
        return False

def main():
    """메인 함수"""
    if len(sys.argv) < 3:
        print("사용법: python save_qa_session.py \"질문\" \"답변\" [파일경로]")
        print("예시: python save_qa_session.py \"OOP의 문제점은?\" \"OOP는 복잡성을 증가시킵니다...\"")
        sys.exit(1)
    
    question = sys.argv[1]
    answer = sys.argv[2]
    
    # 선택적 파일 경로
    qa_file_path = sys.argv[3] if len(sys.argv) > 3 else 'qa_sessions.md'
    
    # 세션 저장
    success = save_qa_session(question, answer, qa_file_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()