Line 1: # 객체 지향 프로그래밍(Object-Oriented Programming)
Line 2: 
Line 3: ## 🎯 객체 지향 프로그래밍 (OOP) 핵심
Line 4: 
Line 5: ### 기본 개념
Line 6: **현실 세계의 사물을 객체로 모델링**하여 프로그램을 설계하는 방식
Line 7: 
Line 8: ### 4가지 핵심 원리
Line 9: 
Line 10: **1. 캡슐화 (Encapsulation)**
Line 11: - 데이터와 메서드를 하나로 묶음
Line 12: - 외부에서 직접 접근 제한
Line 13: 
Line 14: **2. 상속 (Inheritance)**
Line 15: - 기존 클래스의 특성을 물려받아 새 클래스 생성
Line 16: - 코드 재사용성 향상
Line 17: 
Line 18: **3. 다형성 (Polymorphism)**
Line 19: - 같은 인터페이스로 다른 동작 수행
Line 20: - 하나의 메서드가 여러 형태로 동작
Line 21: 
Line 22: **4. 추상화 (Abstraction)**
Line 23: - 복잡한 구현을 숨기고 필요한 기능만 노출
Line 24: - 인터페이스로 본질만 표현
Line 25: 
Line 26: ## 💡 간단한 예시
Line 27: ```python
Line 28: class Animal:  # 부모 클래스
Line 29:     def speak(self):
Line 30:         pass
Line 31: 
Line 32: class Dog(Animal):  # 상속
Line 33:     def speak(self):
Line 34:         return "멍멍"  # 다형성
Line 35: 
Line 36: class Cat(Animal):
Line 37:     def speak(self):
Line 38:         return "야옹"  # 다형성
Line 39: ```
Line 40: 
Line 41: ## 🏆 장점
Line 42: - **재사용성**: 코드 중복 최소화
Line 43: - **유지보수**: 모듈화된 구조
Line 44: - **확장성**: 새 기능 추가 용이
Line 45: - **직관성**: 현실 세계와 유사한 구조
