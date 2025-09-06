# 추가 정보

## 핵심 내용
JSON Schema는 `allOf`(AND), `anyOf`(OR), `oneOf`(정확히 하나) 키워드를 사용해 여러 스키마를 조합할 수 있는 기능을 제공합니다. 예를 들어 도서 정보에서 `isbn_10` 또는 `isbn_13` 중 적어도 하나는 필수로 있어야 하는 조건을 `allOf`와 `anyOf`를 결합해 표현할 수 있습니다. 이러한 스키마 조합 기능을 통해 클래스 기반 데이터 표현보다 더 강력하고 유연한 검증 조건을 구현할 수 있습니다.

## 상세 핵심 내용
## Schema Composition 개념과 활용

### Schema Composition이란?
JSON Schema에서 여러 스키마를 논리적으로 결합하여 복잡한 유효성 검사 규칙을 만드는 방법입니다. 프로그래밍의 논리 연산자(AND, OR, NOT)와 유사한 방식으로 작동합니다.

### 핵심 연산자

#### allOf (AND 연산)
- 데이터가 **모든** 하위 스키마를 만족해야 함
- 여러 조건을 동시에 충족해야 하는 경우 사용

#### anyOf (OR 연산)  
- 데이터가 **최소 하나** 이상의 하위 스키마를 만족하면 됨
- 여러 선택지 중 하나만 충족하면 되는 경우 사용

#### oneOf (XOR 연산)
- 데이터가 **정확히 하나**의 하위 스키마만 만족해야 함
- 상호 배타적인 조건을 표현할 때 사용

### 실제 활용 사례: Open Library Books API

#### 문제 상황
Open Library Books API에서 책 정보를 검증할 때 다음 요구사항이 있었습니다:
- `title`은 항상 필수
- `isbn_10` 또는 `isbn_13` 중 **최소 하나**는 반드시 존재해야 함
- 1986년 출간작인 Watchmen은 재출간되어 두 ISBN을 모두 가질 수 있음

#### 해결 방법
```javascript
var bookInfoSchema = {
  "allOf": [
    basicBookInfoSchema,           // 기본 책 정보 (title 필수)
    {
      "anyOf": [                   // ISBN 중 하나는 필수
        mandatoryIsbn13,           // isbn_13 필수
        mandatoryIsbn10            // isbn_10 필수
      ]
    }
  ]
};
```

### Schema 구조 분석

#### basicBookInfoSchema
- `title`만 필수 필드로 지정
- 나머지 필드들(`publishers`, `number_of_pages`, `weight` 등)은 선택사항
- 기본적인 책 정보 구조 정의

#### 개별 ISBN 요구사항 스키마
```javascript
var mandatoryIsbn13 = {
  "type": "object",
  "required": ["isbn_13"]
};

var mandatoryIsbn10 = {
  "type": "object", 
  "required": ["isbn_10"]
};
```

### 논리적 표현
Schema Composition을 논리식으로 표현하면:
```
basicBookInfoSchema AND (mandatoryIsbn13 OR mandatoryIsbn10)
```

이는 다음을 의미합니다:
1. 기본 책 정보 스키마를 만족해야 함 **그리고**
2. ISBN-13이 있거나 **또는** ISBN-10이 있어야 함

### 장점과 특징

#### 표현력 향상
- 클래스 기반 데이터 표현보다 더 복잡하고 유연한 검증 규칙 작성 가능
- 조건부 유효성 검사를 명확하게 표현

#### 재사용성
- 기본 스키마를 작성하고 추가 조건을 조합하여 확장 가능
- 모듈화된 스키마 설계로 유지보수성 향상

#### 복잡한 비즈니스 로직 표현
- 단순한 필드 존재 여부를 넘어서 복잡한 조건부 로직 구현
- 실제 비즈니스 요구사항을 스키마 레벨에서 직접 표현

### 한계점

#### 오류 메시지의 모호성
Theo가 지적한 바와 같이, Schema Composition을 사용할 때 데이터가 유효하지 않은 경우 구체적으로 어느 부분에서 실패했는지 파악하기 어려울 수 있습니다. 이는 복잡한 조합 스키마에서 디버깅을 어렵게 만드는 요소입니다.

## 주요 화제
- JSON Schema validation for external API responses: Open Library Books API 응답 데이터를 검증하기 위한 스키마 작성과 실제 API 응답 예제 분석

- Schema composition 개념과 활용: allOf, anyOf 키워드를 사용하여 여러 스키마를 AND, OR 논리로 결합하는 방법

- 조건부 필수 필드 검증: ISBN-10과 ISBN-13 중 최소 하나는 반드시 존재해야 하는 비즈니스 로직을 스키마로 표현하는 방법

- 복합 스키마 구조 설계: basicBookInfoSchema, mandatoryIsbn13, mandatoryIsbn10을 조합하여 완전한 검증 스키마를 구성하는 실습

- JSON Schema의 표현력 확장: 클래스 기반 데이터 표현보다 더 복잡한 검증 조건을 표현할 수 있는 JSON Schema의 장점

## 부차 화제
- Open Library Books API: 외부 웹 서비스에서 제공하는 책 정보 API의 구조와 응답 형태
- ISBN 시스템: ISBN-10과 ISBN-13의 차이점과 출판 연도에 따른 사용 구분 (2007년 기준)
- Watchmen 책 정보: DC Comics에서 출간한 그래픽 노블의 구체적인 출판 정보와 사양
- JSON Schema 논리 연산자: allOf(AND), anyOf(OR), oneOf의 역할과 스키마 조합 방법
- 클래스 기반 데이터 표현의 한계: JSON Schema의 표현력이 전통적인 클래스보다 우수한 점
- 데이터 검증 오류 처리: 유효성 검사 실패 시 구체적인 오류 원인 파악의 어려움
