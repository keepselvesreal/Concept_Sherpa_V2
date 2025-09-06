# 생성 시간: 2025년 8월 26일 9:27 KST
# 핵심 내용: 백그라운드 실행 테스트를 위한 간단한 Python 스크립트
# 상세 내용:
#   - main() 함수(라인 18-27): 5초마다 현재 시간과 카운터를 출력하는 메인 로직
#   - 실행 루프(라인 20-26): 총 6회 반복하여 30초간 실행
# 상태: active
# 주소: background_test
# 참조: 없음

import time
import datetime

def main():
    """5초마다 현재 시간과 카운터를 출력하는 테스트 스크립트"""
    print("🚀 백그라운드 테스트 스크립트 시작!")
    print("=" * 50)
    
    for i in range(6):  # 6번 반복 (30초간)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{i+1}/6] 현재 시간: {current_time}")
        
        if i < 5:  # 마지막 반복이 아니면 대기
            print("   → 5초 대기 중...")
            time.sleep(5)
    
    print("=" * 50)
    print("✅ 백그라운드 테스트 스크립트 완료!")

if __name__ == "__main__":
    main()