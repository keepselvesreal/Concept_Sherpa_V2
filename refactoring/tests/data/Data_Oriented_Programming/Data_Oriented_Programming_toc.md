# Data-Oriented Programming

## 27_lev1_2_Separation_between_code_and_data_info.md
<구성 노드 반영 완료>

## Core 내용
코드와 데이터 분리를 핵심으로 하는 DOP(Data-Oriented Programming) 시스템은 시스템 복잡성을 줄이고 유연성을 높이는 프로그래밍 패러다임입니다. 데이터는 데이터 엔티티로 표현되고, 코드는 상태를 갖지 않는(stateless) 함수들의 집합인 코드 모듈로 구성됩니다.

## 상세 핵심 내용
본 문서는 "27 lev1 2 Separation between code and data"라는 제목으로, DOP 시스템의 핵심 원리를 설명합니다. DOP는 OOP의 데이터 캡슐화를 지양하고, 코드와 데이터의 분리를 통해 시스템의 이해도와 유연성을 향상시킵니다. 데이터 엔티티는 시스템의 정보를 담고, 코드 모듈은 데이터 엔티티를 조작하는 역할을 수행합니다. DOP는 특정 언어나 패러다임에 종속되지 않으며, OOP와 FP 모두에서 적용 가능합니다. 본 문서에서는 DOP의 개념, 장점, 데이터 엔티티 및 코드 모듈의 설계, 시스템의 이해 용이성 및 유연성에 대해 다룹니다. 특히 도서관 관리 시스템을 예시로, 데이터 엔티티 식별, 그룹화, 시각화 방법과 코드 모듈의 설계 원리를 구체적으로 제시합니다.

## 상세 정보 내용
본 문서는 DOP 시스템의 설계와 구현에 대한 내용을 담고 있으며, 각 구성 요소의 특징과 장점을 상세하게 설명합니다. 
-   **28 lev2 2.1 The two parts of a DOP system**: DOP의 핵심 원리, DOP와 OOP의 차이점, DOP의 장점 (복잡성 감소, 유연성 증가), DOP의 언어 독립성.
-   **29 lev2 2.2 Data entities**: DOP에서의 데이터 엔티티 개념, 데이터 엔티티 식별 및 그룹화 방법, 도서관 관리 시스템 예시, 데이터 엔티티의 시각화 방법.
-   **30 lev2 2.3 Code modules**: DOP에서의 코드 모듈 정의, 코드 모듈 설계 원칙 (stateless, explicit data argument), OOP와의 비교, 고수준 모듈 구성.
-   **31 lev2 2.4 DOP systems are easy to understand**: DOP 시스템의 이해 용이성, DOP 시스템의 구성 요소 (코드 모듈, 데이터 엔티티), DOP 모듈 다이어그램의 특징, DOP에서의 다형성 구현 방식.
-   **32 lev2 2.5 DOP systems are flexible**: DOP 시스템의 유연성, 요구 사항 변경에 대한 적응성, Super 멤버 및 VIP 멤버 기능 구현 예시.
-   **33 lev2 Summary**: DOP의 원리, 코드와 데이터 분리, DOP 시스템의 장점, 데이터 엔티티와 코드 모듈의 역할 및 관계.

## 주요 화제
*   코드와 데이터의 분리 (DOP의 핵심 원리)
*   DOP (Data-Oriented Programming) 시스템의 개념, 장점, 설계 원리
*   데이터 엔티티 (식별, 그룹화, 시각화)
*   코드 모듈 (stateless, 데이터 엔티티 기반)
*   DOP 시스템의 이해 용이성 및 유연성
*   도서관 관리 시스템을 예시로 한 DOP 적용

## 부차 화제
*   OOP(객체 지향 프로그래밍)과의 비교
*   FP(함수형 프로그래밍)과의 관계
*   데이터 엔티티 관계 (연관 또는 구성)
*   데이터 엔티티 디자인의 반복적 성격
*   DOP 시스템의 API 설계
*   모듈과 클래스의 관계
*   Python에서의 self와 DOP의 데이터 전달 방식 비교
*   DOP 시스템의 Polymorphism 구현 방식
*   에러 관리 (챕터 3)
*   데이터 쿼리 (챕터 3)
*   시스템 상태 관리 (챕터 4)


