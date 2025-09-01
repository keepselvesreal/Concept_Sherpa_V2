Line 1: # 함수형 프로그래밍 (Functional Programming)
Line 2: 
Line 3: ## 🎯 함수형 프로그래밍 (FP) 핵심
Line 4: 
Line 5: ### 기본 개념
Line 6: **함수를 일급 시민으로 취급**하고 **순수 함수**를 기반으로 프로그램을 구성하는 방식
Line 7: 
Line 8: ### 핵심 원리
Line 9: 
Line 10: **1. 순수 함수 (Pure Functions)**
Line 11: - 같은 입력 → 항상 같은 출력
Line 12: - 부작용(side effect) 없음
Line 13: 
Line 14: **2. 불변성 (Immutability)**
Line 15: - 데이터를 변경하지 않음
Line 16: - 새로운 데이터를 생성하여 반환
Line 17: 
Line 18: **3. 고차 함수 (Higher-Order Functions)**
Line 19: - 함수를 인자로 받거나 함수를 반환
Line 20: - `map`, `filter`, `reduce` 등
Line 21: 
Line 22: **4. 함수 합성 (Function Composition)**
Line 23: - 작은 함수들을 조합하여 복잡한 기능 구현
Line 24: 
Line 25: ## 💡 간단한 예시
Line 26: ```python
Line 27: # 순수 함수
Line 28: def add(x, y):
Line 29:     return x + y  # 부작용 없음
Line 30: 
Line 31: # 고차 함수
Line 32: numbers = [1, 2, 3, 4, 5]
Line 33: doubled = list(map(lambda x: x * 2, numbers))  # [2, 4, 6, 8, 10]
Line 34: evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
Line 35: ```
Line 36: 
Line 37: ## 🏆 장점
Line 38: - **예측 가능성**: 순수 함수로 버그 줄임
Line 39: - **테스트 용이**: 입출력이 명확
Line 40: - **병렬 처리**: 불변성으로 안전한 동시성
Line 41: - **재사용성**: 작은 함수들의 조합
Line 42: 
Line 43: ## ⚖️ OOP vs FP
Line 44: - **OOP**: 데이터 중심, 객체 상태 변경
Line 45: - **FP**: 함수 중심, 데이터 변환 체인
