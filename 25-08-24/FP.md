# 함수형 프로그래밍 (Functional Programming)

## 🎯 함수형 프로그래밍 (FP) 핵심

### 기본 개념
**함수를 일급 시민으로 취급**하고 **순수 함수**를 기반으로 프로그램을 구성하는 방식

### 핵심 원리

**1. 순수 함수 (Pure Functions)**
- 같은 입력 → 항상 같은 출력
- 부작용(side effect) 없음

**2. 불변성 (Immutability)**
- 데이터를 변경하지 않음
- 새로운 데이터를 생성하여 반환

**3. 고차 함수 (Higher-Order Functions)**
- 함수를 인자로 받거나 함수를 반환
- `map`, `filter`, `reduce` 등

**4. 함수 합성 (Function Composition)**
- 작은 함수들을 조합하여 복잡한 기능 구현

## 💡 간단한 예시
```python
# 순수 함수
def add(x, y):
    return x + y  # 부작용 없음

# 고차 함수
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))  # [2, 4, 6, 8, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
```

## 🏆 장점
- **예측 가능성**: 순수 함수로 버그 줄임
- **테스트 용이**: 입출력이 명확
- **병렬 처리**: 불변성으로 안전한 동시성
- **재사용성**: 작은 함수들의 조합

## ⚖️ OOP vs FP
- **OOP**: 데이터 중심, 객체 상태 변경
- **FP**: 함수 중심, 데이터 변환 체인