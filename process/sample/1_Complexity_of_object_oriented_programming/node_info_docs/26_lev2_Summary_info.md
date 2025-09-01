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

## 핵심 내용
이 문서는 전통적인 객체 지향 프로그래밍(OOP) 시스템의 복잡성을 지적하고, 데이터 중심 프로그래밍(DOP)이 OOP 및 함수형 프로그래밍(FP)과 호환되면서 데이터 재고를 통해 복잡성을 줄일 수 있음을 설명한다. OOP에서 코드와 데이터의 결합, 가변적인 데이터, 클래스 간의 복잡한 관계 등이 복잡성을 증가시키는 원인으로 분석되며, DOP는 이러한 문제에 대한 효과적인 해결책을 제시한다.

## 상세 핵심 내용

## 상세 핵심 내용
전통적인 OOP 시스템은 이해하기 어려운 복잡성을 가지며, 코드와 데이터가 클래스 내에 혼합되어 있고 데이터가 가변적이라는 특징을 가진다. 이러한 특징은 클래스 간의 복잡한 관계를 유발하고, 멀티 스레드 환경에서의 동기화 문제, 데이터 직렬화의 어려움, 복잡한 클래스 계층 구조 등의 문제를 야기한다. 데이터 중심 프로그래밍(DOP)은 데이터 재고를 통해 이러한 복잡성을 줄이며, 데이터 불변성을 통해 개발자에게 안정감을 제공한다. DOP는 OOP 및 FP와 호환 가능하며, OOP의 복잡성을 완화하는 대안으로 제시된다. DOP를 통해 데이터와 로직을 분리하고 데이터 구조를 명확히 함으로써 시스템의 유지보수성과 확장성을 높일 수 있다.

## 상세 정보

## 상세 정보
*   **정의 및 약어:**
    *   복잡성: 이해하기 어려움
    *   코드와 행동은 같은 의미로 사용
    *   DOP: 데이터 중심 프로그래밍
    *   OOP: 객체 지향 프로그래밍
    *   FP: 함수형 프로그래밍
*   **관계:**
    *   합성 관계: 한 객체가 소멸하면 다른 객체도 소멸 (다이아몬드와 별표로 표시)
    *   연관 관계: 각 객체는 독립적인 생명 주기 (다이아몬드와 별표로 표시)
    *   사용 관계: 클래스가 다른 클래스의 메서드를 사용 (점선 화살표로 표시)
    *   상속 관계: 빈 삼각형 화살표가 슈퍼클래스를 가리킴
*   **전통적인 OOP의 문제점:**
    *   시스템 복잡성 증가 (이해하기 어려움)
    *   코드와 데이터가 클래스 내에 혼합
    *   데이터가 가변적임
    *   클래스 간의 복잡한 관계
    *   멀티 스레드 환경에서의 동기화 문제
    *   데이터 직렬화의 어려움
    *   복잡한 클래스 계층 구조
*   **DOP (데이터 중심 프로그래밍):**
    *   데이터 재고를 통해 복잡성을 줄임
    *   데이터 불변성을 강조
    *   OOP 및 FP와 호환 가능
*   **기타:**
    *   디자인 패턴을 사용하여 OOP의 복잡성을 완화할 수 있음
    *   JSON 변환의 어려움 (reflection 사용 또는 코드 복잡성 증가). DOP는 명확하게 정의된 데이터 구조를 사용하여 JSON 직렬화 및 역직렬화를 단순화할 수 있다.

## 주요 화제
*   객체 지향 프로그래밍 (OOP)의 복잡성
*   데이터 중심 프로그래밍 (DOP)
*   코드와 데이터의 결합
*   데이터 가변성
*   시스템 설계의 복잡성 관리

## 부차 화제
*   함수형 프로그래밍 (FP)
*   디자인 패턴의 활용
*   JSON 직렬화의 어려움
*   클래스 관계 (합성, 연관, 사용, 상속)
*   멀티 스레드 환경에서의 동기화 문제


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

