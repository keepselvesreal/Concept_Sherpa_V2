# 추가 정보

## 핵심 내용
JSON Schema는 데이터 표현과 별도로 데이터 스키마를 정의할 수 있는 언어 독립적인 도구입니다. 기본 구조는 `type`과 `properties` 필드로 구성되며, 객체, 배열, 문자열 등의 데이터 타입을 정의하고 `required` 필드로 필수 항목을 지정할 수 있습니다. 다양한 프로그래밍 언어에서 사용할 수 있는 검증 라이브러리를 통해 데이터가 스키마에 부합하는지 검증할 수 있으며, 클래스 기반 데이터 표현보다 더 강력한 검증 조건을 표현할 수 있습니다.

## 상세 핵심 내용
이 섹션의 내용 분석에 실패했습니다. 원본 텍스트를 직접 확인해주세요.

## 주요 화제
- JSON Schema 기본 개념: 데이터와 스키마를 분리하여 표현하는 방법, JSON Schema를 사용한 데이터 검증의 개념과 장점

- JSON Schema 문법 구조: type, properties, items, enum, required 등의 키워드를 사용한 스키마 정의 방법과 객체, 배열, 문자열 타입 지정

- 도서 검색 요청 스키마 설계: title(문자열)과 fields(문자열 배열) 필드를 가진 검색 요청의 JSON Schema 작성 과정

- 열거형 값 제한: enum 키워드를 사용하여 허용되는 필드 값들을 제한하는 방법 (publishers, number_of_pages, weight 등)

- 필수 필드 지정: required 배열을 사용하여 필수 입력 필드를 명시하는 방법

- 데이터 검증 실행: validate 함수를 사용하여 실제 데이터가 스키마에 부합하는지 확인하는 과정과 유효/무효 데이터 예시

- JSON Schema 검증 라이브러리: JavaScript(Ajv), Java(Snow), C#(JSON.net Schema), Python(jschon), Ruby(JSONSchemer) 등 다양한 언어별 라이브러리

- JSON Schema의 장점: 언어 독립성, 클래스 기반 방식보다 높은 표현력, 고급 검증 기능 지원

## 부차 화제
- Library Management System의 발전 계획: 메모리 내 애플리케이션에서 실제 웹 서버로 발전시키는 계획 (데이터베이스, HTTP 클라이언트, 외부 서비스 연결)

- JSON Schema 언어 소개: JSON Schema version 2020-12를 사용한 데이터 스키마 정의 방법과 공식 웹사이트 정보

- 프로그래밍 언어별 JSON Schema 검증 라이브러리: JavaScript(Ajv), Java(Snow), C#(JSON.net Schema), Python(jschon), Ruby(JSONSchemer) 등 다양한 언어의 검증 라이브러리 목록

- JSON Schema의 고급 검증 기능: 숫자 범위 검증, 정규표현식 매칭 등의 고급 검증 기능에 대한 예고

- 검증 실패 시 상세 정보 제공: 데이터가 스키마에 맞지 않을 때 구체적인 오류 원인을 알려주는 기능

- 검색 응답 스키마의 복잡성: 다중 도서 결과와 선택적 필드들로 인한 응답 스키마의 복잡성
