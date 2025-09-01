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
이 문서는 객체 지향 프로그래밍(OOP) 시스템의 복잡성을 분석하고, OOP의 본질적인 특성으로 인해 시스템이 복잡해지는 경향을 설명한다. 또한 데이터 지향 프로그래밍(DOP)이라는 대안적인 프로그래밍 패러다임을 소개하며, OOP 시스템의 복잡성을 완화할 수 있는 DOP의 원칙을 제시한다.

## 상세 핵심 내용
OOP는 프로그램이 객체로 구성되어 있고, 객체는 상태와 상태를 조작하는 메서드로 이루어져 있기 때문에 복잡성이 증가하는 경향이 있다. OOP 시스템의 복잡성은 코드와 데이터의 혼합, 객체의 가변성, 데이터 및 코드의 객체 내 고정, 클래스 간의 많은 관계로 인해 발생한다. 이러한 복잡성은 시스템을 이해하기 어렵게 만들고, 예측 불가능한 코드 동작, 복잡한 데이터 직렬화, 복잡한 클래스 계층 구조와 같은 문제점을 야기한다. DOP는 데이터 중심적인 접근 방식을 통해 이러한 복잡성을 줄이며, OOP 및 함수형 프로그래밍(FP)과 호환될 수 있다.

## 상세 정보
*   **OOP의 복잡성:** OOP 시스템은 본질적으로 복잡하며, 이는 특정 언어의 구문이나 의미와는 관련이 없다.
*   **복잡성의 원인:** 코드와 데이터의 혼합, 객체의 가변성, 데이터가 객체 내에 잠겨 있고, 코드가 클래스 내에 잠겨 있는 것이 주요 원인이다.
*   **복잡성의 결과:** 이해하기 어려운 시스템, 예측 불가능한 코드 동작(특히 다중 스레드 환경), 복잡한 데이터 직렬화, 복잡한 클래스 계층 구조가 발생한다.
*   **DOP 소개:** 데이터 지향 프로그래밍은 OOP의 복잡성을 줄이는 대안적인 프로그래밍 패러다임이다.
*   **DOP의 특징:** 데이터와 코드를 분리하고, 불변성을 강조하며, 데이터에 대한 일반적인 접근 방식을 제공한다.
*   **DOP와 OOP의 호환성:** DOP 원칙을 준수하는 OOP 시스템은 복잡성이 줄어들 수 있다.
*   **클래스 다이어그램 분석:** UML 다이어그램을 통해 클래스 간의 관계를 시각적으로 분석하고, 복잡성의 원인을 파악한다.
*   **사례 연구:** 도서관 관리 시스템의 설계 예시를 통해 OOP의 복잡성을 구체적으로 설명하고, DOP를 적용했을 때의 효과를 제시한다.
*   **JSON 직렬화의 어려움:** OOP에서 JSON 직렬화 및 역직렬화의 복잡성을 지적하고, DOP가 이를 어떻게 해결할 수 있는지 암시한다.
*   **상속의 문제점:** 클래스 상속의 복잡성과 다중 상속으로 인한 문제점을 지적하고, 구성(composition)을 사용하는 것이 더 나은 선택일 수 있음을 시사한다.
*   **핵심 용어 정의:** 복잡성, 코드, 동작, DOP, OOP, FP 등의 용어를 정의한다.

## 주요 화제
*   객체 지향 프로그래밍 (OOP)의 복잡성
*   데이터 지향 프로그래밍 (DOP)
*   코드와 데이터의 혼합
*   객체의 가변성 (Mutability)
*   데이터 직렬화 (Serialization)
*   클래스 계층 구조 (Class Hierarchies)
*   UML 다이어그램

## 부차 화제
*   소프트웨어 설계 패턴
*   다중 스레드 환경에서의 동기화 문제
*   함수형 프로그래밍 (FP)
*   JSON (JavaScript Object Notation)
*   클래스 상속 vs. 구성 (Inheritance vs. Composition)
*   소프트웨어 개발 프로젝트의 데드라인 및 요구사항 변경
*   소프트웨어 컨설팅 회사 (Albatross)의 경영 및 고객 관리


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
