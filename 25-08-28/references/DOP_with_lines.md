Line 1: # 데이터 지향 프로그래밍(Data-Oriented Programming)
Line 2: 
Line 3: ## 📊 데이터 지향 프로그래밍(Data-Oriented Programming) 개요
Line 4: 
Line 5: 데이터 지향 프로그래밍은 **데이터와 그 변환에 초점을 맞춘** 프로그래밍 패러다임입니다.
Line 6: 
Line 7: ## 🎯 핵심 원리
Line 8: 
Line 9: ### 1. 데이터 우선 설계※
Line 10: - 객체나 함수가 아닌 **데이터 구조를 먼저 설계**
Line 11: - 데이터의 흐름과 변환을 중심으로 사고
Line 12: - "어떤 데이터가 필요한가?"부터 시작
Line 13: 
Line 14: ### 2. 불변성(Immutability)※
Line 15: ```python
Line 16: # 데이터 변경 대신 새로운 데이터 생성
Line 17: original_data = {"name": "John", "age": 30}
Line 18: updated_data = {**original_data, "age": 31}  # 원본 유지
Line 19: ```
Line 20: 
Line 21: ### 3. 데이터와 로직 분리※
Line 22: ```python
Line 23: # ❌ 객체지향 방식
Line 24: class User:
Line 25:     def __init__(self, name, age):
Line 26:         self.name = name
Line 27:         self.age = age
Line 28:     
Line 29:     def is_adult(self):
Line 30:         return self.age >= 18
Line 31: 
Line 32: # ✅ 데이터 지향 방식
Line 33: def is_adult(user_data):
Line 34:     return user_data["age"] >= 18
Line 35: 
Line 36: user = {"name": "John", "age": 30}
Line 37: print(is_adult(user))
Line 38: ```
Line 39: 
Line 40: ## 🏗️ 주요 특징
Line 41: 
Line 42: ### 데이터 변환 파이프라인※
Line 43: ```python
Line 44: # 함수형 스타일로 데이터 변환
Line 45: users = [
Line 46:     {"name": "Alice", "age": 25, "city": "Seoul"},
Line 47:     {"name": "Bob", "age": 17, "city": "Busan"}
Line 48: ]
Line 49: 
Line 50: adults = (
Line 51:     users
Line 52:     |> filter(lambda u: u["age"] >= 18)
Line 53:     |> map(lambda u: u["name"])
Line 54:     |> list
Line 55: )
Line 56: ```
Line 57: 
Line 58: ### 단순한 데이터 구조※
Line 59: - 복잡한 클래스 대신 **기본 데이터 타입** 사용
Line 60: - 딕셔너리, 리스트, 튜플 등 활용
Line 61: - JSON과 호환 가능한 구조 선호
Line 62: 
Line 63: ## 💡 장점
Line 64: 
Line 65: ### 🚀 성능상 이점※
Line 66: - **메모리 지역성** 향상
Line 67: - CPU 캐시 효율성 증대
Line 68: - 벡터화 연산 가능
Line 69: 
Line 70: ### 🔧 유지보수성※
Line 71: - 데이터 구조가 명확해 **디버깅 용이**
Line 72: - 테스트하기 쉬운 순수 함수
Line 73: - 부작용(side effect) 최소화
Line 74: 
Line 75: ### 🔄 확장성※
Line 76: - 데이터 추가/변경이 용이
Line 77: - 병렬 처리에 적합
Line 78: - 마이크로서비스 아키텍처와 호환
Line 79: 
Line 80: ## ⚖️ 단점
Line 81: 
Line 82: ### 복잡성 증가※
Line 83: - 초기 설계 시 더 많은 고민 필요
Line 84: - 객체지향에 익숙한 개발자에게 낯설음
Line 85: 
Line 86: ### 메모리 사용량※
Line 87: - 불변성으로 인한 메모리 오버헤드
Line 88: - 대용량 데이터 처리 시 주의 필요
Line 89: 
Line 90: ## 🛠️ 실제 적용 예시
Line 91: 
Line 92: ### 게임 개발※
Line 93: ```python
Line 94: # Entity Component System (ECS)
Line 95: entities = [
Line 96:     {"id": 1, "position": (0, 0), "velocity": (1, 0), "health": 100},
Line 97:     {"id": 2, "position": (5, 3), "velocity": (-1, 1), "health": 80}
Line 98: ]
Line 99: 
Line 100: def update_positions(entities):
Line 101:     return [
Line 102:         {**entity, "position": (
Line 103:             entity["position"][0] + entity["velocity"][0],
Line 104:             entity["position"][1] + entity["velocity"][1]
Line 105:         )}
Line 106:         for entity in entities
Line 107:     ]
Line 108: ```
Line 109: 
Line 110: ### 데이터 분석※
Line 111: ```python
Line 112: # 판다스 스타일 데이터 처리
Line 113: sales_data = [
Line 114:     {"product": "A", "price": 100, "quantity": 5},
Line 115:     {"product": "B", "price": 200, "quantity": 3}
Line 116: ]
Line 117: 
Line 118: total_revenue = sum(item["price"] * item["quantity"] for item in sales_data)
Line 119: ```
Line 120: 
Line 121: ## 🌍 관련 기술/언어
Line 122: 
Line 123: ### 함수형 언어※
Line 124: - **Clojure**: DOP의 대표적 구현체
Line 125: - **F#**: .NET 생태계의 함수형 언어
Line 126: - **Elixir**: 액터 모델과 결합
Line 127: 
Line 128: ### 라이브러리/프레임워크※
Line 129: - **Redux** (JavaScript): 상태 관리
Line 130: - **Pandas** (Python): 데이터 분석
Line 131: - **Apache Kafka**: 스트리밍 데이터 처리
Line 132: 
Line 133: ## 📚 DOP vs 다른 패러다임
Line 134: 
Line 135: | 특징 | 객체지향(OOP) | 함수형(FP) | 데이터지향(DOP) |
Line 136: |------|---------------|-------------|-----------------|
Line 137: | 중심 | 객체와 메서드 | 함수와 합성 | 데이터와 변환 |
Line 138: | 상태 | 가변 상태 | 불변 상태 | 불변 데이터 |
Line 139: | 구조 | 클래스/인터페이스 | 함수 | 기본 데이터 타입 |
Line 140: 
Line 141: **결론**: 데이터 지향 프로그래밍은 특히 **데이터 처리가 많은 시스템**에서 성능과 유지보수성을 크게 향상시킬 수 있는 강력한 패러다임입니다※.
