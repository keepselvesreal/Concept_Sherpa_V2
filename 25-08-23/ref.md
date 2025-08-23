## 📊 데이터 지향 프로그래밍(Data-Oriented Programming) 개요

데이터 지향 프로그래밍은 **데이터와 그 변환에 초점을 맞춘** 프로그래밍 패러다임입니다.

## 🎯 핵심 원리

### 1. 데이터 우선 설계※
- 객체나 함수가 아닌 **데이터 구조를 먼저 설계**
- 데이터의 흐름과 변환을 중심으로 사고
- "어떤 데이터가 필요한가?"부터 시작

### 2. 불변성(Immutability)※
```python
# 데이터 변경 대신 새로운 데이터 생성
original_data = {"name": "John", "age": 30}
updated_data = {**original_data, "age": 31}  # 원본 유지
```

### 3. 데이터와 로직 분리※
```python
# ❌ 객체지향 방식
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def is_adult(self):
        return self.age >= 18

# ✅ 데이터 지향 방식
def is_adult(user_data):
    return user_data["age"] >= 18

user = {"name": "John", "age": 30}
print(is_adult(user))
```

## 🏗️ 주요 특징

### 데이터 변환 파이프라인※
```python
# 함수형 스타일로 데이터 변환
users = [
    {"name": "Alice", "age": 25, "city": "Seoul"},
    {"name": "Bob", "age": 17, "city": "Busan"}
]

adults = (
    users
    |> filter(lambda u: u["age"] >= 18)
    |> map(lambda u: u["name"])
    |> list
)
```

### 단순한 데이터 구조※
- 복잡한 클래스 대신 **기본 데이터 타입** 사용
- 딕셔너리, 리스트, 튜플 등 활용
- JSON과 호환 가능한 구조 선호

## 💡 장점

### 🚀 성능상 이점※
- **메모리 지역성** 향상
- CPU 캐시 효율성 증대
- 벡터화 연산 가능

### 🔧 유지보수성※
- 데이터 구조가 명확해 **디버깅 용이**
- 테스트하기 쉬운 순수 함수
- 부작용(side effect) 최소화

### 🔄 확장성※
- 데이터 추가/변경이 용이
- 병렬 처리에 적합
- 마이크로서비스 아키텍처와 호환

## ⚖️ 단점

### 복잡성 증가※
- 초기 설계 시 더 많은 고민 필요
- 객체지향에 익숙한 개발자에게 낯설음

### 메모리 사용량※
- 불변성으로 인한 메모리 오버헤드
- 대용량 데이터 처리 시 주의 필요

## 🛠️ 실제 적용 예시

### 게임 개발※
```python
# Entity Component System (ECS)
entities = [
    {"id": 1, "position": (0, 0), "velocity": (1, 0), "health": 100},
    {"id": 2, "position": (5, 3), "velocity": (-1, 1), "health": 80}
]

def update_positions(entities):
    return [
        {**entity, "position": (
            entity["position"][0] + entity["velocity"][0],
            entity["position"][1] + entity["velocity"][1]
        )}
        for entity in entities
    ]
```

### 데이터 분석※
```python
# 판다스 스타일 데이터 처리
sales_data = [
    {"product": "A", "price": 100, "quantity": 5},
    {"product": "B", "price": 200, "quantity": 3}
]

total_revenue = sum(item["price"] * item["quantity"] for item in sales_data)
```

## 🌍 관련 기술/언어

### 함수형 언어※
- **Clojure**: DOP의 대표적 구현체
- **F#**: .NET 생태계의 함수형 언어
- **Elixir**: 액터 모델과 결합

### 라이브러리/프레임워크※
- **Redux** (JavaScript): 상태 관리
- **Pandas** (Python): 데이터 분석
- **Apache Kafka**: 스트리밍 데이터 처리

## 📚 DOP vs 다른 패러다임

| 특징 | 객체지향(OOP) | 함수형(FP) | 데이터지향(DOP) |
|------|---------------|-------------|-----------------|
| 중심 | 객체와 메서드 | 함수와 합성 | 데이터와 변환 |
| 상태 | 가변 상태 | 불변 상태 | 불변 데이터 |
| 구조 | 클래스/인터페이스 | 함수 | 기본 데이터 타입 |

**결론**: 데이터 지향 프로그래밍은 특히 **데이터 처리가 많은 시스템**에서 성능과 유지보수성을 크게 향상시킬 수 있는 강력한 패러다임입니다※.