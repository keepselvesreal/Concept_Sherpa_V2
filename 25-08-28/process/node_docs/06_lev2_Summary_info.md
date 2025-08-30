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
(Summary) 본 요약은 DOP 원칙에 따른 데이터 스키마와 표현의 분리 및 시스템 경계에서의 데이터 검증의 중요성을 강조합니다. JSON Schema를 활용한 데이터 유효성 검증 방법과 장점, 그리고 Ajv 라이브러리의 특징을 간략하게 설명합니다. 이는 DOP에서의 데이터 유효성 검증 전반을 아우르며, 부모 노드의 핵심 내용을 종합적으로 요약하고, 각 구성 노드의 내용을 연결합니다.

## 상세 정보
Summary: **7장 요약: 데이터 유효성 검증 - 핵심 내용 정리**

이 챕터는 7장의 핵심 내용을 요약하고, 데이터 유효성 검증의 중요성을 다시 한번 강조합니다. 부모 노드의 7 Basic data validation 내용과 연계하여, 핵심 개념들을 간결하게 정리합니다.

**핵심 내용 (부모 노드 내용 반영):** 7장의 주요 내용을 간략하게 요약합니다. 데이터 유효성 검증의 중요성, JSON Schema의 활용, 오류 처리 방법 등을 포함합니다.

**추가 상세 정보 및 새로운 내용 (부모 노드 내용 및 추가 보충):**

*   **DOP 원칙 4 (데이터 스키마와 표현의 분리) 관련:** 데이터 스키마와 표현을 분리함으로써, 데이터 유효성 검증 로직을 변경하지 않고도 데이터 표현 방식을 유연하게 변경할 수 있습니다. (부모 노드 'DOP 원칙 및 데이터 검증의 중요성 재강조' 참고)
*   **시스템 경계 정의 (데이터 교환 영역) 관련:** 시스템 경계는 데이터가 입력되거나 출력되는 모든 지점을 포함하며, 이는 API 엔드포인트, 파일 입출력, 데이터베이스 연결, 외부 서비스와의 통신 등 다양한 형태로 나타날 수 있습니다. (부모 노드 '시스템 경계의 정의' 참고)
*   **경계에서의 검증 예시 (클라이언트 요청/응답, 외부 소스 데이터) 관련:**
    *   **클라이언트 요청/응답:** API 엔드포인트에 전송되는 JSON 데이터의 유효성을 검증하여, 예상치 못한 데이터로 인한 시스템 오류를 방지하고, API 응답 데이터가 클라이언트에 올바르게 전달되는지 검증합니다.
    *   **외부 소스 데이터:** 외부 API, 데이터베이스, 파일 등에서 수신하는 데이터가 시스템에서 요구하는 스키마를 준수하는지 검증합니다. 데이터 품질을 보장하고, 잠재적인 데이터 손상 문제를 예방합니다. (부모 노드 '경계에서의 검증 예시' 참고)
*   **DOP 데이터 검증 의미 (스키마 준수 여부 확인) 관련:** 스키마를 준수하는 데이터는 시스템이 예상하는 형식과 구조를 갖춘 데이터이며, 시스템의 안정성과 신뢰성을 확보하는 데 중요합니다. (부모 노드 'DOP 데이터 검증 의미' 참고)
*   **검증 실패 정보 (상세한 검증 실패 정보와 사용자 친화적 형식) 관련:** 실패 정보를 사용자 친화적인 형식으로 제공함으로써, 문제의 원인을 쉽게 파악하고 수정할 수 있도록 돕습니다. (부모 노드 '데이터 검증 실패 정보' 참고)
*   **경계 검증의 중요성 (내부 재검증 불필요) 관련:** 경계에서 한 번 검증된 데이터는 시스템 내부에서 추가적인 유효성 검사를 거치지 않아도 됩니다. 이는 성능 향상과 코드 복잡성 감소에 기여합니다. 다만, 보안적인 측면에서 신뢰할 수 없는 데이터에 대한 검증은 필요할 수 있습니다.
*   **JSON Schema 특징 (언어, 구문, 표현력, 조작성) 관련:** (부모 노드 'JSON Schema 특징' 참고)
    *   **언어:** JSON 형식으로 작성되어 사람이 읽고 이해하기 쉽습니다.
    *   **구문:** 상세하지만 명확합니다.
    *   **표현력:** 복잡한 데이터 구조와 유효성 검사 규칙을 표현할 수 있습니다.
    *   **조작성:** JSON 객체이므로, 코드를 사용하여 동적으로 생성하거나 수정할 수 있습니다.
*   **필드 기본값과 모범 사례 (옵션 필드와 외부 소스 검증) 관련:**
    *   **옵션 필드:** JSON Schema에서 필드는 기본적으로 선택 사항입니다.
    *   **모범 사례:** 외부 소스에서 데이터를 가져올 때, 데이터의 유효성을 반드시 검증해야 합니다. (부모 노드 '필드 기본값과 모범 사례' 참고)
*   **데이터 전송 원칙 (엄격한 송신, 유연한 수신) 관련:**
    *   **엄격한 송신:** 데이터를 전송할 때는, 수신 측에서 예상하는 스키마를 정확하게 준수해야 합니다.
    *   **유연한 수신:** 데이터를 수신할 때는, 가능한 유연하게 처리해야 합니다. (부모 노드 '데이터 전송 원칙' 참고)
*   **Ajv 라이브러리 특징 (JavaScript JSON Schema 라이브러리와 기본 동작) 관련:**
    *   **기본 동작:** Ajv는 기본적으로 첫 번째 유효성 검사 실패만 보고합니다.
    *   **고급 유효성 검사:** 12장에서 Ajv의 고급 기능에 대한 자세한 내용이 다루어집니다. (부모 노드 'Ajv 라이브러리 특징' 참고)

**결론:** 7장은 DOP에서의 데이터 유효성 검증의 중요성을 강조하고, JSON Schema를 활용한 구체적인 구현 방법을 제시합니다. 특히, 시스템 경계에서의 데이터 검증, 스키마 유연성, 오류 처리의 중요성을 강조합니다. (부모 노드의 '요약' 참고)

## 주요 화제
- **DOP 원칙과 데이터 검증**: DOP 원칙 4 (데이터 스키마와 표현의 분리)와 데이터 검증의 의미, 경계에서의 검증 예시, 경계 검증의 중요성에 대한 내용.
- **시스템 경계 정의와 검증**: 시스템 경계의 정의, 경계에서의 데이터 검증 (클라이언트 요청/응답, 외부 소스 데이터), 경계 검증의 중요성에 대한 내용.
- **JSON Schema**: JSON Schema의 특징 (언어, 구문, 표현력, 조작성)과 JSON Schema를 활용한 데이터 검증 방법.
- **검증 실패 정보**: 데이터 검증 실패 시 얻는 정보와 사용자 친화적인 형식으로의 제공.
- **필드 기본값과 데이터 전송 원칙**: JSON Schema에서의 필드 기본값, 외부 소스 데이터 검증, 데이터 전송 시의 엄격한 송신과 유연한 수신 원칙.
- **Ajv 라이브러리**: JavaScript JSON Schema 라이브러리인 Ajv의 특징과 기본 동작.

## 부차 화제
- 시스템 경계 정의: 데이터 교환이 발생하는 영역에 대한 정의
- 경계에서의 검증 예시: 클라이언트 요청/응답 및 외부 소스 데이터 검증
- 검증 실패 정보: 상세한 검증 실패 정보와 사용자 친화적 형식
- 경계 검증의 중요성: 경계에서 검증하면 내부 재검증 불필요
- JSON Schema 특징: 언어, 구문, 표현력, 조작성, 필드 기본값 등
- 필드 기본값과 모범 사례: 옵션 필드와 외부 소스 검증
- 데이터 전송 원칙: 엄격한 송신, 유연한 수신
- Ajv 라이브러리 특징: JavaScript JSON Schema 라이브러리와 기본 동작, 첫 번째 validation failure만 catch
- 12장 언급: Advanced validation covered

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
