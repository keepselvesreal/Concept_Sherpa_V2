# 추가 정보

## 핵심 내용
JSON Schema 검증에서 데이터가 유효하지 않을 때, 오류의 상세 정보를 얻을 수 있습니다. JavaScript의 Ajv 라이브러리에서는 `ajv.errors` 배열에 실패 정보가 저장되며, `errorsText()` 함수로 사람이 읽기 쉬운 형태로 변환할 수 있고, `allErrors: true` 옵션을 사용하면 여러 개의 검증 오류를 한 번에 포착할 수 있습니다.

## 상세 핵심 내용
이 텍스트는 JSON Schema 데이터 검증 실패에 대한 세부 정보를 다루는 내용입니다. 핵심 내용을 체계적으로 정리하면 다음과 같습니다.

## 데이터 검증 실패의 세부 정보

### 기본 개념
- JSON Schema 검증은 단순히 유효/무효의 이진 결과가 아니라, 무효한 경우 **실패 이유에 대한 세부 정보**를 제공합니다
- 누락된 필드명, 잘못된 데이터 타입 등의 구체적인 오류 정보를 얻을 수 있습니다

### 라이브러리별 차이점
- 각 데이터 검증 라이브러리마다 **검증 실패 세부 정보를 노출하는 방식이 다릅니다**
- JavaScript의 Ajv 라이브러리에서는 마지막 검증의 오류들이 **validator 인스턴스 내부의 배열**로 저장됩니다

### Ajv에서의 오류 처리

**단일 오류 처리:**
```javascript
var ajv = new Ajv();
ajv.validate(searchBooksRequestSchema, invalidSearchBooksRequest);
ajv.errors // 검증 오류들을 표시
```

**오류 정보 구조:**
```javascript
[{
    "instancePath": "",
    "schemaPath": "#/required", 
    "keyword": "required",
    "params": {"missingProperty":"title"},
    "message": "must have required property 'title'"
}]
```

**사람이 읽기 쉬운 형태 변환:**
```javascript
ajv.errorsText(ajv.errors);
// → "data must have required property 'title'"
```

### 다중 오류 처리

**기본 동작:**
- Ajv는 기본적으로 **첫 번째 검증 실패만** 포착합니다
- 성능상의 이유로 오류 발견 시 데이터 파싱을 중단합니다

**다중 오류 활성화:**
```javascript
var ajv = new Ajv({allErrors: true}); // 모든 오류를 포착하도록 설정
```

**다중 오류 결과 예시:**
```
"data must have required property 'title',
data/fields/0 must be string, 
data/fields/1 must be string"
```

### JSON Schema 참조 가이드

**기본 스키마 구조:**
```javascript
{
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "myNumber": {"type": "number"},
            "myString": {"type": "string"}, 
            "myEnum": {"enum": ["myVal", "yourVal"]},
            "myBool": {"type": "boolean"}
        },
        "required": ["myNumber", "myString"],
        "additionalProperties": false
    }
}
```

**유효한 데이터 예시:**
```javascript
[
    {
        "myNumber": 42,
        "myString": "Hello", 
        "myEnum": "myVal",
        "myBool": true
    },
    {
        "myNumber": 54,
        "myString": "Happy"
    }
]
```

### 실용적 의미
이러한 세부 오류 정보는 시스템의 경계에서 데이터 검증을 구현할 때 매우 유용하며, 특히 웹 서버로 전환할 때 필수적인 기능입니다.

## 주요 화제
- 데이터 검증 실패 상세 정보 추출: JSON Schema 검증이 실패했을 때 단순한 성공/실패가 아닌 구체적인 실패 원인과 위치를 파악하는 방법

- Ajv 라이브러리의 오류 처리 메커니즘: JavaScript Ajv에서 검증 오류가 배열 형태로 저장되는 구조와 validator 인스턴스 내부의 errors 속성 활용법

- 단일 검증 실패 사례 분석: 필수 필드 누락(title → myTitle) 시 instancePath, schemaPath, keyword, params 등의 상세 오류 정보 구조

- 검증 오류의 인간 친화적 표시: errorsText() 유틸리티 함수를 사용하여 복잡한 오류 객체를 읽기 쉬운 텍스트로 변환하는 방법

- 다중 검증 실패 처리: allErrors 옵션을 통해 첫 번째 오류뿐만 아니라 모든 검증 실패를 한 번에 수집하는 기법

- JSON Schema 치트시트: 기본 데이터 타입(array, object, number, string, boolean), 열거형(enum), 필수 필드(required), 추가 속성 제한(additionalProperties) 등의 스키마 정의 패턴

## 부차 화제
- Ajv 라이브러리의 특정 구현 방식: 검증 실패 정보를 validator 인스턴스 내의 배열로 저장하는 방식과 errorsText 유틸리티 함수를 통한 가독성 개선

- 검증 오류 개수 제어 메커니즘: 기본적으로 첫 번째 오류만 감지하는 성능 최적화와 allErrors 옵션을 통한 다중 오류 감지 설정

- JSON Schema 치트시트 제공: 배열, 객체, 다양한 데이터 타입(number, string, enum, boolean), 필수 필드, additionalProperties 설정을 포함한 스키마 작성 가이드

- 유효한 데이터 예시 제시: 치트시트에 대응하는 실제 유효 데이터 구조 샘플과 필수 필드 조건을 만족하는 다양한 케이스

- 도서 검색 요청 스키마 예제: title과 fields 속성을 가진 구체적인 검증 시나리오와 다양한 검증 실패 사례(필드명 오류, 타입 불일치)
