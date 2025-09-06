# 속성
---
content_processing: unified
created_at: 2025-08-28 11:43:31.980838
folder_name: null
process_status: true
source: 2022_Data-Oriented Programming_Manning.pdf
source_language: english
source_type: book
structure_type: component
title: Data-Oriented Programming

# 추출
---

## 핵심 내용

이 문서는 객체 지향 프로그래밍(OOP)의 복잡성이 OOP의 근본적인 특징, 즉 상태와 상태를 조작하는 메서드를 함께 묶는 객체 구성 방식에서 비롯된다고 주장합니다. 코드와 데이터를 혼합하고, 객체를 변경 가능하게 만들고, 데이터를 객체 내부에 잠그는 등의 OOP 특징들이 시스템을 이해하기 어렵게 만들고 복잡성을 증가시킨다고 설명합니다.

## 상세 핵심 내용

이 문서는 객체 지향 프로그래밍(OOP)의 복잡성을 분석하고, 데이터 중심 프로그래밍(DOP)이라는 대안적 패러다임을 제시합니다. OOP는 코드와 데이터를 객체 안에 묶어 관리하지만, 이로 인해 클래스 간의 관계가 복잡해지고, 객체의 가변성으로 인해 예측 불가능한 코드 동작이 발생하며, 데이터 직렬화가 어려워지는 경향이 있습니다. 특히, 새로운 요구사항 추가 시 클래스 상속 구조가 복잡해지는 문제가 발생합니다. DOP는 코드와 데이터를 분리하고 불변성을 강조함으로써 시스템의 복잡성을 줄이는 것을 목표로 합니다. 궁극적으로 이 문서는 OOP의 내재된 복잡성을 인지하고, DOP와 같은 대안적 접근 방식을 통해 더 단순하고 이해하기 쉬운 시스템을 구축하도록 동기를 부여합니다. DOP는 OOP 및 함수형 프로그래밍(FP)과 모두 호환되어 유연한 적용이 가능합니다.

## 상세 내용

## 주요 화제

다음 문서의 주요 화제는 다음과 같습니다.

*   **객체 지향 프로그래밍(OOP)의 복잡성**: OOP 시스템이 복잡해지는 경향을 탐구하고, 그 이유를 분석합니다. 특히, OOP의 기본 원리인 객체 기반 구성과 그로 인한 복잡성을 다룹니다.
*   **데이터 중심 프로그래밍(DOP)**: OOP의 대안으로 DOP를 소개하며, 시스템 복잡성을 줄이는 데 어떻게 기여하는지 설명합니다. DOP가 OOP와 FP와 호환될 수 있음을 언급합니다.
*   **OOP 설계**: Klafim Global Library Management System의 프로토타입을 예시로 사용하여, OOP 설계의 복잡성을 보여줍니다. 클래스 다이어그램과 UML을 활용하여 시스템 구조를 설명합니다.
*   **복잡성의 원인**: OOP 시스템의 복잡성을 증가시키는 요인들을 분석합니다. 코드와 데이터의 혼합, 객체의 가변성, 데이터 및 코드의 클래스 내 고정 등을 주요 원인으로 지적합니다.
*   **UML**: UML 다이어그램의 다양한 관계(composition, association, inheritance, usage)에 대한 설명이 제공됩니다.
*   **코드의 예측 불가능성**: 객체의 가변성으로 인해 발생하는 코드 동작의 예측 불가능성을 설명하고, 데이터 불변성이 DOP 개발자에게 안정감을 제공함을 강조합니다.
*   **데이터 직렬화의 어려움**: OOP에서 JSON 직렬화 및 역직렬화의 복잡성을 지적하고, DOP가 제공하는 일반적인 데이터 접근 방식을 간략하게 소개합니다.
*   **클래스 계층의 복잡성**: 상속을 사용할 때 발생하는 문제점과 다이아몬드 상속 문제(Deadly Diamonds of Death)를 언급하고, composition over inheritance 디자인 패턴을 옹호합니다.
*   **핵심 개념 요약**: 문서 전반에 걸쳐 사용된 중요한 용어와 개념(예: 복잡성, 코드, DOP, OOP, FP, composition, association, immutability)을 요약합니다.

## 부차 화제

다음은 문서에서 파악된 부차적인 주제들입니다.

*   **OOP 언어의 특징 및 프레임워크**:
    *   익명 클래스 및 익명 함수와 같은 새로운 언어 기능
    *   Spring, Jackson(Java)과 같은 프레임워크
    *   Reflection, Custom Annotations과 같은 고급 언어 기능

*   **소프트웨어 개발 회사의 구조 및 역할**:
    *   Albatross라는 소프트웨어 컨설팅 회사
    *   스타트업 부서 및 엔터프라이즈 부서
    *   Tech Lead의 역할 (딜 클로징, 프로젝트 납기)

*   **소프트웨어 개발 프로세스**:
    *   UML 클래스 다이어그램을 사용한 시스템 설계
    *   코드 구현 전 설계 단계의 중요성

*   **소프트웨어 개발자의 토론**:
    *   객체 상태 변화에 대한 디버깅 문제
    *   설계 기술 향상

*   **UML 다이어그램**:
    *   다양한 유형의 화살표 (합성, 연관, 상속, 사용)
    *   합성(composition) 및 연관(association) 관계의 차이점
    *   다대다(many-to-many) 연관 관계
    *   사용(usage) 관계 및 상속(inheritance) 관계

*   **도서관 관리 시스템 클래스**:
    *   Library, Book, BookItem, BookLending, Member, Librarian, User, Catalog, Author 클래스

*   **JSON 데이터 처리**:
    *   REST API를 통한 데이터 접근
    *   JSON 직렬화 및 역직렬화의 어려움

*   **클래스 상속 및 다이아몬드 문제**:
    *   새로운 요구사항 추가 시 클래스 계층 구조 변경의 어려움
    *   다중 상속으로 인한 다이아몬드 문제 발생

*   **디자인 패턴**:
    *   구성(composition) vs 클래스 상속(class inheritance)

# 내용
---
# 1_Complexity_of_object_oriented_programming

--- 페이지 31 ---
3
Complexity of object-
oriented programming
A capricious entrepreneur
In this chapter, we'll explore why object-oriented programming (OOP) systems tend to
be complex. This complexity is not related to the syntax or the semantics of a specific
OOP language. It is something that is inherent to OOP's fundamental insight—
programs should be composed from objects, which consist of some state, together
with methods for accessing and manipulating that state.
 Over the years, OOP ecosystems have alleviated this complexity by adding new
features to the language (e.g., anonymous classes and anonymous functions) and
by developing frameworks that hide some of this complexity, providing a simpler
interface for developers (e.g., Spring and Jackson in Java). Internally, the frame-
works rely on the advanced features of the language such as reflection and custom
annotations.
 
This chapter covers
The tendency of OOP to increase system 
complexity
What makes OOP systems hard to understand
The cost of mixing code and data together into 
objects


--- 페이지 32 ---
4
CHAPTER 1
Complexity of object-oriented programming
 This chapter is not meant to be read as a critical analysis of OOP. Its purpose is to
raise your awareness of the tendency towards OOP's increased complexity as a pro-
gramming paradigm. Hopefully, it will motivate you to discover a different program-
ming paradigm, where system complexity tends to be reduced. This paradigm is
known as data-oriented programming (DOP).

# 구성
---
16_lev2_1.1_OOP_design_Classic_or_classical_info.md
17_lev3_1.1.1_The_design_phase_info.md
18_lev3_1.1.2_UML_101_info.md
19_lev3_1.1.3_Explaining_each_piece_of_the_class_diagram_info.md
20_lev3_1.1.4_The_implementation_phase_info.md
21_lev2_1.2_Sources_of_complexity_info.md
22_lev3_1.2.1_Many_relations_between_classes_info.md
23_lev3_1.2.2_Unpredictable_code_behavior_info.md
24_lev3_1.2.3_Not_trivial_data_serialization_info.md
25_lev3_1.2.4_Complex_class_hierarchies_info.md
26_lev2_Summary_info.md
