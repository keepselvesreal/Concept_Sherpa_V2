#!/usr/bin/env python3

# 생성 시간: 2025-08-25 11:45 KST
# 핵심 내용: 현재 실행 중인 Claude Code 세션 ID 가져오기
# 상세 내용:
#   - get_session_from_logs() (라인 15-30): 훅 로그에서 최신 세션 ID 추출
#   - get_session_from_temp_files() (라인 32-50): 임시 파일에서 세션 ID 추출
#   - get_session_from_process() (라인 52-70): 프로세스 정보에서 세션 ID 추출
#   - main() (라인 72-90): 여러 방법으로 세션 ID 찾기 시도
# 상태: active
# 주소: get_session_id
# 참조: 없음

import re
import subprocess
import glob
import json
import os
from datetime import datetime

def get_session_from_logs():
    """훅 로그에서 최신 세션 ID 추출"""
    try:
        result = subprocess.run(['tail', '-20', '/tmp/claude_hook_debug.log'], 
                              capture_output=True, text=True, timeout=5)
        
        # session_id 패턴 찾기 (최신 것부터)
        matches = re.findall(r'"session_id":"([^"]+)"', result.stdout)
        return matches[-1] if matches else None
    except Exception as e:
        print(f"로그에서 세션 ID 추출 실패: {e}")
        return None

def get_session_from_temp_files():
    """임시 파일에서 세션 ID 추출"""
    try:
        # Claude 관련 임시 파일 찾기
        patterns = [
            "/tmp/claude_session_*.json",
            "/tmp/claude_session_*.tmp"
        ]
        
        all_files = []
        for pattern in patterns:
            all_files.extend(glob.glob(pattern))
        
        if not all_files:
            return None
            
        # 가장 최근 파일
        latest = max(all_files, key=os.path.getmtime)
        
        # 파일명에서 세션 ID 추출 시도
        match = re.search(r'claude_session_[^_]*_([a-f0-9-]+)', latest)
        if match:
            return match.group(1)
            
        # 파일 내용에서 세션 ID 추출 시도
        with open(latest, 'r') as f:
            content = f.read()
            match = re.search(r'"?session_id"?\s*:\s*"([^"]+)"', content)
            return match.group(1) if match else None
            
    except Exception as e:
        print(f"임시 파일에서 세션 ID 추출 실패: {e}")
        return None

def get_session_from_process():
    """프로세스 정보에서 세션 ID 추출"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
        
        # Claude 프로세스 찾기
        for line in result.stdout.split('\n'):
            if 'claude' in line.lower() and 'session' in line.lower():
                # 세션 ID 패턴 찾기
                match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', line)
                if match:
                    return match.group(1)
        return None
    except Exception as e:
        print(f"프로세스에서 세션 ID 추출 실패: {e}")
        return None

def main():
    print("🔍 Claude Code 세션 ID 찾는 중...")
    print("=" * 50)
    
    methods = [
        ("훅 로그", get_session_from_logs),
        ("임시 파일", get_session_from_temp_files),
        ("프로세스 정보", get_session_from_process)
    ]
    
    found_session = None
    
    for method_name, method_func in methods:
        print(f"📝 {method_name}에서 검색 중...")
        session_id = method_func()
        
        if session_id:
            print(f"✅ {method_name}에서 발견: {session_id}")
            if not found_session:
                found_session = session_id
        else:
            print(f"❌ {method_name}에서 찾지 못함")
        print()
    
    if found_session:
        print("🎯 최종 결과:")
        print(f"세션 ID: {found_session}")
        print(f"세션 ID (앞 8자리): {found_session[:8]}")
        print(f"확인 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 세션 파일 존재 확인
        session_prefix = found_session[:8]
        session_file_pattern = f"/home/nadle/projects/Knowledge_Sherpa/v2/25-08-25/chat-logs/session_{session_prefix}*.json"
        session_files = glob.glob(session_file_pattern)
        
        if session_files:
            print(f"📁 해당 세션 파일: {session_files[0]}")
        else:
            print("📁 해당 세션 파일 없음 (아직 생성되지 않음)")
            
    else:
        print("❌ 어떤 방법으로도 세션 ID를 찾을 수 없습니다.")
        print("💡 새로운 Claude Code 세션을 시작해보세요.")

if __name__ == "__main__":
    main()