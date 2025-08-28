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
이 요약은 7장 "Basic data validation"의 핵심 내용을 담고 있으며, 데이터 스키마와 표현의 분리, 시스템 경계에서의 검증, JSON Schema를 활용한 데이터 유효성 검증 방법을 다룹니다. 특히, 데이터 전송 시에는 엄격한 송신과 유연한 수신, Ajv 라이브러리를 사용한 JavaScript 환경에서의 검증을 권장합니다.


## 상세 핵심 내용
## Summary 분석

### 기본 정보

*   **생성 시간:** 2025-08-10 22:28:30 KST
*   **핵심 내용:** 7장 요약 (Basic data validation 핵심 개념 정리)
*   **상태:** 활성
*   **주소:** chapter7\_06\_summary
*   **참조:** /home/nadle/projects/Knowledge\_Sherpa/v2/25-08-09/extracted\_texts/Level01\_7 Basic data validation.md
*   **페이지:** 190

### 핵심 개념

*   **DOP 원칙 #4:** 데이터 스키마와 표현의 분리.
*   **시스템 경계:** 시스템이 데이터를 교환하는 영역 (ex: 클라이언트 요청/응답, 외부 데이터).
*   **경계에서의 검증:**
    *   클라이언트 요청 및 응답 유효성 검사.
    *   외부 소스 데이터 유효성 검사.
*   **DOP 데이터 검증의 의미:** 데이터가 스키마를 준수하는지 확인.
*   **검증 실패 시:**
    *   상세한 검증 실패 정보 제공.
    *   사용자 친화적인 형식으로 오류 메시지 제공.
*   **경계 검증의 중요성:** 경계에서 데이터가 유효하면 내부에서 재검증 불필요.

### JSON Schema

*   **특징:**
    *   데이터 유효성 검증과 표현을 분리하는 언어.
    *   문법은 다소 상세함.
    *   표현력이 높음.
    *   맵과 유사하여 프로그램 내에서 자유롭게 조작 가능.
    *   스키마 정의를 변수에 저장하고 다른 스키마에서 활용 가능.
    *   맵 필드는 기본적으로 선택적 (optional).

### 모범 사례 및 데이터 전송 원칙

*   **모범 사례:** 외부 데이터 소스로부터 데이터를 검증하는 것이 좋음.
*   **데이터 전송 원칙:**
    *   송신 시 엄격하게 데이터 형식 준수.
    *   수신 시 유연하게 데이터 처리.

### Ajv 라이브러리

*   **Ajv:** JavaScript용 JSON Schema 라이브러리.
*   **기본 동작:** 기본적으로 첫 번째 유효성 검사 실패만 포착.
*   **고급 검증:** 12장에서 다룸.


## 상세 정보
## Summary 분석 및 추가 상세 정보

제공된 "Summary" 내용과 원본 텍스트를 분석하여, 이전에 언급되지 않은 상세 정보와 새로운 내용을 다음과 같이 정리합니다.

**1. DOP 원칙 4 (데이터 스키마와 표현의 분리) 관련:**

*   **추가 정보 없음:** 요약 내용과 원본 내용 모두 DOP 원칙 4에 대한 기본적인 정의만 제공하며, 구체적인 예시나 추가적인 설명은 부족합니다.

**2. 시스템 경계 정의 (데이터 교환 영역) 관련:**

*   **추가 정보 없음:** 시스템 경계에 대한 정의와 관련 예시(클라이언트 요청/응답, 외부 데이터)는 요약과 원본 모두 동일하게 제공됩니다.

**3. 경계에서의 검증 예시 (클라이언트 요청/응답, 외부 소스 데이터) 관련:**

*   **추가 정보 없음:** 경계 검증의 예시는 요약과 원본 내용이 동일합니다.

**4. DOP 데이터 검증 의미 (스키마 준수 여부 확인) 관련:**

*   **추가 정보 없음:** DOP 데이터 검증의 의미는 요약과 원본 내용에서 동일하게 설명됩니다.

**5. 검증 실패 정보 (상세한 검증 실패 정보와 사용자 친화적 형식) 관련:**

*   **추가 정보 없음:** 검증 실패 정보에 대한 설명은 요약과 원본 내용에서 동일합니다.

**6. 경계 검증의 중요성 (경계에서 검증하면 내부 재검증 불필요) 관련:**

*   **추가 정보 없음:** 경계 검증의 중요성에 대한 설명은 요약과 원본 내용에서 동일합니다.

**7. JSON Schema 특징 (언어, 구문, 표현력, 조작성) 관련:**

*   **JSON Schema 구문 (Syntax):** 요약에서는 'JSON Schema syntax is a bit verbose'라는 구문이 추가되었습니다. 이는 JSON Schema의 구문이 다소 장황하다는 점을 지적합니다.
*   **JSON Schema 조작 (Manipulation):** JSON Schema는 맵(maps)과 같으므로, 프로그램 내에서 자유롭게 조작할 수 있습니다. 스키마 정의를 변수에 저장하고 다른 스키마에서 사용할 수도 있습니다.

**8. 필드 기본값과 모범 사례 (옵션 필드와 외부 소스 검증) 관련:**

*   **JSON Schema의 필드 기본값:** JSON Schema에서 맵 필드는 기본적으로 옵션 필드입니다.
*   **모범 사례:** 외부 데이터 소스에서 가져온 데이터를 검증하는 것이 좋은 관행입니다.

**9. 데이터 전송 원칙 (엄격한 송신, 유연한 수신) 관련:**

*   **추가 정보 없음:** 데이터 전송 원칙에 대한 설명은 요약과 원본 내용에서 동일합니다.

**10. Ajv 라이브러리 특징 (JavaScript JSON Schema 라이브러리와 기본 동작) 관련:**

*   **Ajv의 기본 동작:** Ajv는 기본적으로 첫 번째 유효성 검사 실패만 포착합니다.
*   **고급 유효성 검사:** 고급 유효성 검사는 12장에서 다룹니다.

**결론:**

요약과 원본 텍스트를 비교 분석한 결과, 다음과 같은 새로운 상세 정보가 추가되었습니다.

*   JSON Schema 구문이 다소 장황하다는 점
*   JSON Schema는 맵과 같아서 조작이 자유롭다는 점
*   JSON Schema에서 맵 필드는 기본적으로 옵션 필드라는 점
*   Ajv는 기본적으로 첫 번째 유효성 검사 실패만 포착한다는 점
*   고급 유효성 검사는 12장에서 다룬다는 점

이러한 정보들은 "Summary"에서 제시된 핵심 개념들을 보완하며, 데이터 유효성 검증과 관련된 구체적인 내용들을 이해하는 데 도움을 줄 수 있습니다.


## 주요 화제
- DOP (Data-Oriented Programming) 원칙 #4와 데이터 검증: 데이터 스키마와 표현의 분리, DOP에서의 데이터 검증 의미 (스키마 준수 여부 확인).
- 시스템 경계에서의 데이터 검증: 시스템 경계 정의 (데이터 교환 영역), 경계 검증 예시 (클라이언트 요청/응답, 외부 소스 데이터), 경계 검증의 중요성 (내부 재검증 불필요).
- 검증 실패 정보: 상세한 검증 실패 정보, 사용자 친화적 형식으로의 제공.
- JSON Schema: JSON Schema의 특징 (언어, 구문, 표현력, 조작성), JSON Schema를 이용한 데이터 검증, 필드 기본값 및 모범 사례 (옵션 필드, 외부 소스 검증).
- 데이터 전송 원칙: 엄격한 송신, 유연한 수신.
- Ajv 라이브러리: JavaScript JSON Schema 라이브러리인 Ajv의 특징 및 기본 동작 (첫 번째 유효성 검사 실패만 포착).


## 부차 화제
- DOP 원칙 4 (데이터 스키마와 표현의 분리): 데이터 스키마와 표현을 분리하는 DOP 원칙에 대한 간략한 설명.
- 시스템 경계 정의: 데이터 교환이 발생하는 시스템 경계에 대한 정의.
- 경계에서의 검증 예시: 클라이언트 요청/응답, 외부 소스 데이터 등 시스템 경계에서의 데이터 검증 예시.
- 검증 실패 정보: 검증 실패 시 상세 정보 제공 및 사용자 친화적 형식의 중요성.
- 경계 검증의 중요성: 경계에서 검증하면 내부 재검증이 불필요하다는 내용.
- JSON Schema 특징: 언어, 구문, 표현력, 조작성, 필드 기본값, 외부 소스 검증 등 JSON Schema의 특징.
- 필드 기본값과 모범 사례: 옵션 필드, 외부 소스 데이터 검증과 관련된 모범 사례.
- 데이터 전송 원칙: 엄격한 송신, 유연한 수신 원칙.
- Ajv 라이브러리 특징: JavaScript JSON Schema 라이브러리인 Ajv의 특징과 기본 동작.
- 7장 내용 요약: Basic data validation 핵심 개념 정리.
- Advanced validation: Chapter 12에서 다룰 내용 언급.

# 내용
---
## Summary

"""
생성 시간: 2025-08-10 22:28:30 KST
핵심 내용: 7장 요약 (Summary) - Basic data validation 핵심 개념 정리
상세 내용:
    - DOP 원칙 4 (915행): 데이터 스키마와 표현의 분리
    - 시스템 경계 정의 (916-918행): 데이터 교환이 발생하는 영역
    - 경계에서의 검증 예시 (919-921행): 클라이언트 요청/응답, 외부 소스 데이터
    - DOP 데이터 검증 의미 (921-923행): 스키마 준수 여부 확인
    - 검증 실패 정보 (923-925행): 상세한 검증 실패 정보와 사용자 친화적 형식
    - 경계 검증의 중요성 (925-927행): 경계에서 검증하면 내부 재검증 불필요
    - JSON Schema 특징 (927-937행): 언어, 구문, 표현력, 조작성
    - 필드 기본값과 모범 사례 (935-941행): 옵션 필드와 외부 소스 검증
    - 데이터 전송 원칙 (940-942행): 엄격한 송신, 유연한 수신
    - Ajv 라이브러리 특징 (942-945행): JavaScript JSON Schema 라이브러리와 기본 동작
상태: 활성
주소: chapter7_06_summary
참조: 원본 파일 /home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md
"""

# Summary

Summary
 DOP Principle #4 is to separate data schema and data representation.
 The boundaries of a system are defined to be the areas where the system
exchanges data.
 Some examples of data validation at the boundaries of the system are validation
of client requests and responses, and validation of data that comes from exter-
nal sources.
 Data validation in DOP means checking whether a piece of data conforms to a
schema.
 When a piece of data is not valid, we get information about the validation fail-
ures and send this information back to the client in a human readable format.
 When data at system boundaries is valid, it's not critical to validate data again
inside the system.
 JSON Schema is a language that allows us to separate data validation from data
representation.
 JSON Schema syntax is a bit verbose.
 The expressive power of JSON Schema is high.
 JSON Schemas are just maps and, as so, we are free to manipulate them like any
other maps in our programs.
 We can store a schema definition in a variable and use this variable in another
schema.
 In JSON Schema, map fields are optional by default.
 It's good practice to validate data that comes from an external data source.

=== 페이지 190 ===
162 CHAPTER 7 Basic data validation
 It's good practice to be strict regarding data that you send and to be flexible
regarding data that you receive.
 Ajv is a JSON Schema library in JavaScript.
 By default, Ajv catches only the first validation failure.
 Advanced validation is covered in chapter 12.

# 구성
---
없음 (리프 노드)
