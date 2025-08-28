# 객체 지향 프로그래밍(Object-Oriented Programming)

## 🎯 객체 지향 프로그래밍 (OOP) 핵심

### 기본 개념
**현실 세계의 사물을 객체로 모델링**하여 프로그램을 설계하는 방식

### 4가지 핵심 원리

**1. 캡슐화 (Encapsulation)**
- 데이터와 메서드를 하나로 묶음
- 외부에서 직접 접근 제한

**2. 상속 (Inheritance)**
- 기존 클래스의 특성을 물려받아 새 클래스 생성
- 코드 재사용성 향상

**3. 다형성 (Polymorphism)**
- 같은 인터페이스로 다른 동작 수행
- 하나의 메서드가 여러 형태로 동작

**4. 추상화 (Abstraction)**
- 복잡한 구현을 숨기고 필요한 기능만 노출
- 인터페이스로 본질만 표현

## 💡 간단한 예시
```python
class Animal:  # 부모 클래스
    def speak(self):
        pass

class Dog(Animal):  # 상속
    def speak(self):
        return "멍멍"  # 다형성

class Cat(Animal):
    def speak(self):
        return "야옹"  # 다형성
```

## 🏆 장점
- **재사용성**: 코드 중복 최소화
- **유지보수**: 모듈화된 구조
- **확장성**: 새 기능 추가 용이
- **직관성**: 현실 세계와 유사한 구조