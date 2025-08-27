# 생성 시간: 2025년 8월 26일 9:30 KST  
# 핵심 내용: 백그라운드 실행 결과를 파일로 저장하는 테스트 스크립트
# 상세 내용:
#   - main() 함수(라인 20-40): 로그 파일에 결과를 저장하며 실행하는 메인 로직
#   - 로그 파일 생성(라인 24): 타임스탬프 포함한 로그 파일명 생성
#   - 실행 루프(라인 27-37): 콘솔과 파일에 동시 출력
# 상태: active
# 주소: background_test_with_log
# 참조: background_test

import time
import datetime
import os

def main():
    """5초마다 현재 시간과 카운터를 출력하며 로그 파일에 저장하는 테스트 스크립트"""
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    log_file = f"background_test_log_{timestamp}.txt"
    
    # 로그 파일 초기화
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"🚀 백그라운드 테스트 시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
    
    print(f"🚀 백그라운드 테스트 시작! (로그: {log_file})")
    
    for i in range(6):  # 6번 반복 (30초간)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{i+1}/6] 현재 시간: {current_time}"
        
        print(message)
        
        # 파일에도 저장
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(message + "\n")
            if i < 5:
                f.write("   → 5초 대기 중...\n")
        
        if i < 5:  # 마지막 반복이 아니면 대기
            print("   → 5초 대기 중...")
            time.sleep(5)
    
    # 완료 메시지
    end_time = datetime.datetime.now()
    completion_msg = f"✅ 백그라운드 테스트 완료: {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    print("=" * 50)
    print(completion_msg)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write(completion_msg + "\n")
        f.write(f"총 실행 시간: {(end_time - start_time).total_seconds():.1f}초\n")
    
    print(f"📋 결과가 {log_file}에 저장되었습니다.")

if __name__ == "__main__":
    main()