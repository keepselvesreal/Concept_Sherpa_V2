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