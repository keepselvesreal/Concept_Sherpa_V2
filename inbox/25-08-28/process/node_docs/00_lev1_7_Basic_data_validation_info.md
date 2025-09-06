# 속성
---
process_status: true
source: 2022_Data-Oriented Programming_Manning.pdf
source_type: book
source_language: english
structure_type: component
content_processing: unified
title: Data-Oriented Programming
folder_name: 
created_at: 2025-08-28T11:43:31.980838

# 추출
---
## 핵심 내용
DOP에서 데이터 유효성 검사는 데이터 스키마와 표현을 분리하여 시스템 경계에서 데이터를 검증하는 것을 의미합니다. JSON Schema를 사용하여 유효성 검사를 수행하며, 검증 실패 시 상세 정보를 얻을 수 있고, 외부 데이터 소스에 대해 엄격한 검증을 적용하는 것이 좋습니다.


## 상세 핵심 내용
## 7 Basic Data Validation 상세 정리

### 7.1 Data validation in DOP

*   **DOP 원칙 4:** 데이터 스키마와 데이터 표현의 분리 (Separate data schema from data representation).
*   **데이터 검증의 중요성:** DOP에서 데이터 검증은 가능하며 권장됨.
*   **시스템 경계 (Boundaries) 정의:** 시스템이 데이터를 교환하는 영역 (클라이언트, 데이터베이스, 웹 서비스).
*   **두 가지 종류의 데이터 검증:**
    *   **경계에서의 검증:** 시스템의 입출력 데이터 검증 (가장 중요).
    *   **내부에서의 검증:** 코드베이스가 커짐에 따라 개발 편의성을 위해 사용.
*   **경계 검증의 목적:** 유효하지 않은 데이터의 입출력 방지, 오류 발생 시 상세 정보 제공.
*   **팁:** 경계에서 데이터 검증이 완료되면 내부에서의 재검증은 필수는 아님.

### 7.2 JSON Schema in a nutshell

*   **JSON Schema 개요:** 데이터 스키마를 JSON 형식으로 정의하는 언어.
*   **데이터 스키마와 표현의 분리:** 데이터 표현과 독립적으로 스키마 정의 가능.
*   **JSON Schema 기본 구조:**
    *   `type`: 데이터 유형 (예: "object", "string", "array").
    *   `properties`: 각 필드의 스키마 정의 (객체인 경우).
    *   `items`: 배열 요소의 스키마 (배열인 경우).
    *   `enum`: 허용되는 값 목록 (열거형).
    *   `required`: 필수 필드 목록.
*   **JSON Schema의 특징:**
    *   언어 독립성 (다양한 프로그래밍 언어에서 사용 가능).
    *   표현력: 클래스 기반 데이터 표현보다 더 복잡한 검증 조건 표현 가능.

### 7.3 Schema flexibility and strictness

*   **검증 대상:** 클라이언트 요청, 서버 응답, 외부 데이터 소스 등
*   **JSON Schema의 유연성:**
    *   필드는 기본적으로 선택 사항.
    *   `required` 필드를 통해 필수 필드 지정.
    *   스키마는 맵이므로 쉽게 구성하고 조작 가능.
*   **`additionalProperties` 필드:**
    *   기본적으로 스키마에 정의되지 않은 필드 허용.
    *   `additionalProperties: false`를 설정하여 추가 필드 금지 (엄격한 검증).
*   **모범 사례:**
    *   요청에서는 유연하게 (추가 필드 허용).
    *   응답에서는 엄격하게 (추가 필드 금지).
*   **데이터 전송 원칙:** "보내는 것은 보수적으로, 받는 것은 관대하게 (Be conservative in what you send, be liberal in what you accept)."

### 7.4 Schema composition

*   **스키마 조합:**  `allOf`, `anyOf`, `oneOf` 등을 사용하여 스키마를 조합.
    *   `allOf`: 모든 스키마를 만족해야 함 (AND).
    *   `anyOf`: 하나 이상의 스키마를 만족해야 함 (OR).
    *   `oneOf`: 정확히 하나의 스키마를 만족해야 함.
*   **스키마 조합의 장점:** 클래스 정의보다 더 유연하고 강력한 데이터 검증 조건 표현 가능.

### 7.5 Details about data validation failures

*   **검증 실패 시 상세 정보:** 유효성 검사 실패의 원인에 대한 구체적인 정보 제공 (예: 누락된 필수 필드, 잘못된 데이터 유형).
*   **구체적인 에러 정보:**  JSON Schema 검증 라이브러리 (예: Ajv)는 검증 실패에 대한 자세한 정보를 제공.
    *   `instancePath`: 에러가 발생한 데이터 경로.
    *   `schemaPath`: 에러가 발생한 스키마 경로.
    *   `keyword`: 발생한 에러 유형 (예: "required", "type").
    *   `params`: 에러에 대한 추가 정보.
    *   `message`: 사람이 읽을 수 있는 에러 메시지.
*   **Ajv 라이브러리의 특징:**
    *   기본적으로 첫 번째 검증 실패만 감지 (성능 향상).
    *   `allErrors: true` 옵션을 사용하여 여러 개의 오류를 한 번에 감지 가능.
    *   `errorsText()` 유틸리티 함수를 사용하여 에러 정보를 사람이 읽기 쉬운 형식으로 변환.


## 상세 정보
## 7 Basic Data Validation - 추가 상세 정보 및 새로운 내용 정리

다음은 "7 Basic data validation" 내용에서 추출한 추가적인 상세 정보와 새로운 내용입니다. 기존 핵심 내용 요약에 포함되지 않은 내용들을 중심으로 정리했습니다.

**1. DOP 원칙 및 데이터 검증의 중요성 재강조**

*   **DOP 원칙 #4 재확인 (915행):** 데이터 스키마와 데이터 표현의 분리. 이 원칙은 DOP에서 데이터 검증을 가능하게 하며, 데이터 구조와 검증 로직을 분리하여 유연성을 제공합니다.

**2. 시스템 경계 및 데이터 교환 (916-918행):**

*   **시스템 경계의 정의:** 시스템이 데이터를 교환하는 모든 지점. 예를 들어, 웹 서버의 경우 클라이언트, 데이터베이스, 외부 웹 서비스와의 통신 지점이 경계가 됩니다. 그림 7.1 (170페이지)에서 웹 서버 아키텍처를 예시로 보여줌.

**3. 경계에서의 검증 예시 및 목적 (919-921, 925-927행):**

*   **경계 검증 예시:** 클라이언트 요청, 데이터베이스 응답, 외부 웹 서비스 응답 등 시스템 외부와의 데이터 교환 지점에서 데이터의 유효성을 검사합니다.
*   **경계 검증의 목적:** 시스템으로 유효하지 않은 데이터가 들어오거나 나가는 것을 막고, 오류 발생 시 사용자에게 이해하기 쉬운 방식으로 오류를 표시합니다.
*   **내부 검증의 필요성 (926행):** 경계에서 검증이 이루어진 경우 내부에서의 검증은 선택사항이 될 수 있지만, 코드의 유지 보수성을 높이기 위해 내부 검증을 수행할 수 있습니다.

**4. JSON Schema 상세 정보 (927-937행):**

*   **JSON Schema의 특징:**
    *   **언어 독립성:** 다양한 프로그래밍 언어에서 사용할 수 있는 JSON 기반 스키마 정의 언어입니다. (177페이지 표 7.2 참고)
    *   **표현력:** 클래스 기반 데이터 구조보다 훨씬 강력한 유효성 검사 조건을 표현할 수 있습니다. (예: 범위, 정규식 등)
    *   **구조:** JSON 객체를 사용하여 스키마를 정의하며, `type`, `properties`, `required`, `items`, `enum`, `additionalProperties` 등의 키워드를 사용합니다. (172-175페이지에서 예시 확인)
    *   **조작성:** JSON 객체이므로 스키마를 변수에 저장하고, 다른 스키마를 구성하는 데 사용할 수 있습니다. (179페이지)

**5. JSON Schema 예시 (171-181페이지):**

*   **검색 요청 스키마:** (171-176페이지, Listing 7.1-7.6)
    *   `type: "object"` (map)
    *   `properties`:  `title: {type: "string"}`, `fields: {type: "array", items: {enum: [...]}}`
    *   `required: ["title", "fields"]`
*   **검색 응답 스키마:** (177-179페이지, Listing 7.10-7.12)
    *   `type: "array"` (배열)
    *   `items`: `{type: "object", required: ["title", "available"], properties: {...}}`
    *   `bookInfoSchema` (스키마 재사용)
*   **데이터베이스 응답 스키마:** (180-181페이지, Listing 7.13-7.15)
    *   `type: "array"`
    *   `items`: `{type: "object", required: ["title", "isbn", "available"], additionalProperties: false, properties: {...}}`
    *   `additionalProperties: false` (추가 속성 허용 여부)

**6. JSON Schema의 유연성 및 엄격성 (935-941행):**

*   **필드 기본값:** JSON Schema에서는 맵의 필드가 기본적으로 선택 사항입니다. 필수 필드는 `required` 배열에 명시해야 합니다.
*   **추가 속성 (additionalProperties):**  JSON Schema에서 `additionalProperties`를 `false`로 설정하면 스키마에 정의되지 않은 추가 필드를 허용하지 않습니다. 요청에서는 유연하게, 응답에서는 엄격하게 설정하는 것이 좋습니다.
*   **데이터 전송 원칙:** "보내는 데이터는 엄격하게, 받는 데이터는 유연하게"

**7. Schema composition (182-185페이지):**

*   **스키마 조합 (allOf, anyOf):** 여러 스키마를 조합하여 더 복잡한 유효성 검사 조건을 만들 수 있습니다. (183-185페이지, Listing 7.18-7.19)
    *   `allOf`: 모든 스키마를 만족해야 함 (AND)
    *   `anyOf`: 최소한 하나의 스키마를 만족해야 함 (OR)
    *   `oneOf`: 정확히 하나의 스키마를 만족해야 함 (NOT 언급)

**8. 데이터 검증 실패 정보 (923-925, 186-188페이지):**

*   **상세 오류 정보:** JSON Schema 유효성 검사 실패 시, 실패 이유에 대한 상세 정보를 얻을 수 있습니다.
*   **Ajv (JavaScript JSON Schema Validator) 예시:**
    *   유효성 검사 실패 시 `ajv.errors` 배열에 오류 정보가 저장됩니다.
    *   `instancePath`, `schemaPath`, `keyword`, `params`, `message` 등의 정보를 포함합니다. (Listing 7.21)
    *   `ajv.errorsText(ajv.errors)` 함수를 사용하여 오류 정보를 사람이 읽기 쉬운 형식으로 변환할 수 있습니다. (Listing 7.22)
    *   `allErrors: true` 옵션을 사용하여 여러 오류를 한 번에 감지할 수 있습니다. (Listing 7.23)

**9. JSON Schema Cheat Sheet (188-189페이지):**

*   간결한 JSON Schema 정의 예시와 유효한 데이터 예시를 제공하여 JSON Schema 학습에 도움을 줍니다. (Listing 7.24-7.25)

**10. 외부 API 통합 (182-185페이지):**

*   **Open Library Books API 예시:** 외부 API 응답의 스키마를 정의하고, `allOf`와 `anyOf`를 사용하여 ISBN 필드의 조건부 필수 여부를 표현합니다.

이러한 추가 정보를 통해 7 Basic data validation 장의 내용을 더욱 깊이 있게 이해하고, 실제 프로젝트에 적용하는 데 필요한 구체적인 지식을 얻을 수 있습니다.


## 주요 화제
- DOP 원칙 4 (데이터 스키마와 표현의 분리): 데이터 지향 프로그래밍(DOP)의 핵심 원칙으로, 데이터 스키마와 데이터 표현을 분리하여 유연성을 확보하는 내용.
- 시스템 경계에서의 데이터 검증: 시스템 경계, 즉 데이터 교환이 일어나는 지점에서 데이터 유효성을 검증하는 중요성을 강조하며, 클라이언트 요청/응답, 외부 소스 데이터 등의 예시를 제시.
- JSON Schema를 이용한 데이터 검증: JSON Schema 언어를 사용하여 데이터 검증을 수행하는 방법, JSON Schema의 특징(언어 독립성, 표현력, 조작성 등) 설명.
- 데이터 검증 실패 정보 확인: 데이터 유효성 검증 실패 시, 구체적인 실패 원인과 사용자 친화적인 형식으로 오류 정보를 제공하는 방법.
- 시스템 경계에서의 데이터 검증 중요성: 시스템 경계에서 데이터를 검증하면, 시스템 내부에서의 재검증 필요성을 줄여 개발 효율성을 높이는 내용.
- JSON Schema의 특징과 활용: JSON Schema의 문법, 표현력, 스키마 조작 방법, 재사용성 및 유연성에 대한 내용.
- 필드 기본값 및 모범 사례: JSON Schema에서 필드의 기본 동작 (선택적 필드), 외부 데이터 소스 검증, 데이터 전송 원칙(엄격한 송신, 유연한 수신) 등을 다룸.
- Ajv 라이브러리 소개: JavaScript용 JSON Schema 검증 라이브러리인 Ajv의 사용법, 오류 처리 방식, 오류 메시지 형식 등에 대한 설명.


## 부차 화제
- 시스템 경계의 종류: 웹 서버, 클라이언트, 데이터베이스, 웹 서비스 등 데이터가 교환되는 구체적인 지점
- 데이터 유효성 검사 종류: 시스템 경계에서의 데이터 유효성 검사와 시스템 내부에서의 데이터 유효성 검사 (목적, 환경의 차이)
- JSON Schema 언어의 특징: 언어 독립성, 다양한 프로그래밍 언어 지원, 클래스 기반 데이터 표현보다 높은 표현력, JSON Schema의 구체적인 사용 방법
- JSON Schema의 활용: 데이터 유효성 검사 라이브러리 (예: Ajv) 사용법, 유효성 검사 실패 시의 상세 정보 획득 및 활용
- JSON Schema의 고급 기능: 스키마 합성 (AND, OR, NOT), additionalProperties 설정, enum keyword, required fields 지정 등
- JSON Schema의 유연성: 맵 필드의 기본 옵션, 스키마의 재사용 및 조작 가능성
- 데이터 전송 및 수신에 대한 모범 사례: 엄격한 데이터 전송과 유연한 데이터 수신
- Ajv 라이브러리의 특징: JavaScript 환경에서의 JSON Schema 검증 라이브러리, 오류 처리 방법 (단일 오류 vs. 다중 오류)

# 내용
---
# 7 Basic data validation

=== 페이지 169 ===
Basic data validation
A solemn gift
This chapter covers
 The importance of validating data at system
boundaries
 Validating data using the JSON Schema language
 Integrating data validation into an existing code
base
 Getting detailed information about data validation
failures
At first glance, it may seem that embracing DOP means accessing data without validat-
ing it and engaging in wishful thinking, where data is always valid. In fact, data valida-
tion is not only possible but recommended when we follow data-oriented principles.
This chapter illustrates how to validate data when data is represented with
generic data structures. It focuses on data validation occurring at the boundaries of
the system, while in part 3, we will deal with validating data as it flows through the
system. This chapter is a deep dive into the fourth principle of DOP.
PRINCIPLE #4 Separate data schema from data representation.
141

# 구성
---
01_lev2_7.1_Data_validation_in_DOP_info.md
02_lev2_7.2_JSON_Schema_in_a_nutshell_info.md
03_lev2_7.3_Schema_flexibility_and_strictness_info.md
04_lev2_7.4_Schema_composition_info.md
05_lev2_7.5_Details_about_data_validation_failures_info.md
06_lev2_Summary_info.md
