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

이 문서는 전통적인 객체 지향 프로그래밍(OOP)의 복잡성을 지적하고, 데이터 중심 프로그래밍(DOP)이 데이터와 코드를 분리하여 복잡성을 줄이는 대안임을 설명합니다. OOP 시스템은 코드와 데이터의 혼합, 객체의 가변성 등으로 인해 이해하기 어렵고, 다중 스레드 환경에서의 동기화 및 데이터 직렬화에 어려움을 겪는 반면, DOP는 데이터 불변성을 통해 이러한 문제를 완화하고 OOP 및 함수형 프로그래밍(FP)과 호환됩니다.

## 상세 핵심 내용

이 문서는 복잡성 감소를 목표로 데이터 중심 프로그래밍(DOP)의 개념을 소개하며, 전통적인 객체 지향 프로그래밍(OOP)의 복잡성 원인을 분석합니다. OOP에서는 코드(메서드)와 데이터(멤버)가 클래스 내에 혼합되어 있어 시스템 이해를 어렵게 만들고, 클래스 간의 복잡한 관계를 유발하며, 데이터 변경 가능성은 코드의 예측 불가능성을 높이고 동기화 문제를 야기합니다. 또한, OOP는 데이터 직렬화 및 클래스 계층 구조의 복잡성을 증가시킵니다. 반면 DOP는 코드와 데이터를 분리하여 시스템을 단순화하고, 데이터 불변성을 통해 예측 가능성을 높이며, OOP 및 FP와의 호환성을 제공합니다. 디자인 패턴을 사용하여 OOP의 복잡성을 완화할 수 있지만, DOP는 데이터에 대한 새로운 접근 방식을 통해 근본적인 복잡성을 줄이는 데 중점을 둡니다.

## 상세 내용

## 주요 화제

다음은 문서의 주요 화제들을 불렛 포인트로 정리한 것입니다:

*   **복잡성(Complexity):** 문서 전반에 걸쳐 복잡성을 줄이는 것에 대한 논의가 주를 이루며, 특히 전통적인 OOP 시스템의 복잡성을 강조합니다.
*   **코드와 데이터의 분리:** OOP에서 코드와 데이터가 결합되는 것이 복잡성을 야기하는 주요 원인으로 지적되며, 코드와 데이터를 분리하는 것의 장점을 설명합니다.
*   **가변성(Mutability)과 불변성(Immutability):** 데이터의 가변성이 코드의 예측 불가능성을 초래하고 동기화 문제를 야기한다는 점을 강조하며, 데이터 불변성이 DOP 개발자에게 안정감을 준다고 언급합니다.
*   **데이터 중심 프로그래밍(DOP):** DOP가 데이터에 대한 새로운 접근 방식을 통해 복잡성을 줄이는 방법과 OOP 및 FP와의 호환성을 설명합니다.
*   **객체 지향 프로그래밍(OOP)의 문제점:** 전통적인 OOP 시스템의 복잡성, 코드와 데이터의 혼합, 데이터 가변성, 복잡한 클래스 계층 구조, 데이터 직렬화의 어려움 등을 지적합니다.
*   **관계(Relations):** 컴포지션 관계(Composition relation), 연관 관계(Association relation), 사용 관계(Usage relation), 상속 관계(Inheritance relation)의 정의와 UML 다이어그램 표현 방식을 설명합니다.
*   **디자인 패턴(Design Patterns):** 디자인 패턴이 전통적인 OOP에서 복잡성을 완화하는 데 도움을 줄 수 있음을 언급합니다.
*   **JSON 변환:** OOP 프로그래밍 언어에서 JSON 변환의 어려움을 지적합니다.
*   **약어:** DOP, OOP, FP 등의 약어를 정의합니다.

## 부차 화제

이 문서의 주요 주제는 객체 지향 프로그래밍(OOP)의 복잡성, 데이터 중심 프로그래밍(DOP)의 간결성, 그리고 두 프로그래밍 패러다임의 비교입니다. 주요 주제 외에 부차적으로 언급되는 주제들은 다음과 같습니다.

*   **코드와 행동(Code and Behavior):** 코드와 행동이라는 용어가 상호 교환적으로 사용된다는 점.
*   **관계(Relations):** 합성(Composition), 연관(Association), 사용(Usage), 상속(Inheritance) 관계에 대한 설명과 UML 다이어그램에서의 표현 방식.
*   **가변성(Mutability):** OOP에서의 데이터 가변성이 시스템 복잡성을 증가시키는 요인이며, 멀티 스레드 환경에서의 동기화 문제와 데이터 직렬화의 어려움을 야기한다는 점.
*   **디자인 패턴(Design Patterns):** 숙련된 OOP 개발자들이 디자인 패턴을 사용하여 더 나은 설계를 할 수 있다는 언급, 그리고 디자인 패턴이 OOP의 복잡성을 완화하는 데 도움이 될 수 있다는 점.
*   **JSON 직렬화(JSON Serialization):** OOP 언어에서의 JSON 직렬화의 어려움과 복잡성 (reflection 사용 또는 코드의 장황함).
*   **시스템 구조(System Architecture):** 코드를 데이터로부터 분리하는 것이 복잡성을 줄이는 데 도움이 되며, 여러 개의 단순한 독립적인 부분으로 구성된 시스템이 단일 복잡한 부분으로 구성된 시스템보다 덜 복잡하다는 점.
*   **데이터 직렬화(Data Serialization):** OOP에서 데이터가 클래스에 묶여 있어 데이터 직렬화가 어렵다는 점.

# 내용
---
## Summary

Summary
Complexity in the context of this book means hard to understand.
We use the terms code and behavior interchangeably.
DOP stands for data-oriented programming.
OOP stands for object-oriented programming.
FP stands for functional programming.
In a composition relation, when one object dies, the other one also dies.
A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
In an association relation, each object has an independent life cycle.
A many-to-many association relation is represented by an empty diamond and a
star at both edges.
Dashed arrows indicate a usage relation; for instance, when a class uses a method
of another class.
Plain arrows with empty triangles represent class inheritance, where the arrow
points towards the superclass.
The design presented in this chapter doesn't pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.

--- 페이지 53 ---
25
Summary
Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
In traditional OOP, data is mutable.
The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
When code and data are mixed, classes tend to be involved in many relations.
When objects are mutable, extra thinking is required in order to understand
how the code behaves.
When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
When data is locked in objects, data serialization is not trivial.
When code is locked in classes, class hierarchies tend to be complex.
A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
When data is mutable, code is unpredictable.
A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
Data immutability brings serenity to DOP developers' minds.
Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
In traditional OOP, data serialization is difficult.
In traditional OOP, data is locked in classes as members.
In traditional OOP, code is locked into classes.
DOP reduces complexity by rethinking data.
DOP is compatible both with OOP and FP.

# 구성
---

