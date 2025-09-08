# 속성
---
process_status: true


# 추출
---
## 핵심 내용
이 문서는 객체 지향 프로그래밍(OOP)의 복잡성을 지적하고, 데이터 지향 프로그래밍(DOP)을 대안으로 제시하며 DOP가 OOP 및 함수형 프로그래밍(FP)과 호환된다고 설명한다. OOP의 문제점은 코드와 데이터의 혼합, 데이터의 가변성, 클래스 계층의 복잡성 등으로 요약된다. DOP는 데이터에 대한 재고를 통해 이러한 복잡성을 줄이는 데 초점을 맞춘다.

## 상세 핵심 내용
이 책에서는 '복잡성'을 이해하기 어렵다는 의미로 사용하며, 코드와 동작을 동의어로 본다. OOP는 코드와 데이터를 클래스 내에서 혼합하여 복잡성을 증가시키는데, 데이터는 가변적이며, 데이터 직렬화가 어렵다. DOP는 이러한 OOP의 문제점을 해결하기 위해 데이터에 집중하며, DOP는 OOP와 FP 모두와 호환된다. 또한, 데이터의 불변성은 개발자에게 안정감을 주고, OOP의 설계 패턴은 복잡성을 완화하는 데 도움이 될 수 있다. 마지막으로, 데이터 직렬화와 JSON 변환이 OOP에서는 복잡하거나 장황하다.

## 상세 정보
*   **핵심 개념**:
    *   Complexity: Hard to understand.
    *   Code & Behavior: Used interchangeably.
    *   DOP: Data-oriented programming.
    *   OOP: Object-oriented programming.
    *   FP: Functional programming.
*   **관계**:
    *   Composition: One object dies, the other dies too. Represented by a plain diamond and an optional star.
    *   Association: Independent life cycles. Represented by an empty diamond and a star at both edges for many-to-many relations.
    *   Usage: Dashed arrows.
    *   Inheritance: Plain arrows with empty triangles (superclass direction).
*   **OOP의 문제점**:
    *   Increases system complexity (hard to understand).
    *   Code and data are mixed (data as members, code as methods).
    *   Data is mutable.
    *   Root cause of complexity: mixing code and data.
    *   Classes involved in many relations when code and data are mixed.
    *   Extra thinking required when objects are mutable.
    *   Explicit synchronization required on multi-threaded environments when objects are mutable.
    *   Data serialization is not trivial when data is locked in objects.
    *   Class hierarchies tend to be complex when code is locked in classes.
    *   Data serialization is difficult.
    *   Data is locked in classes as members.
    *   Code is locked into classes.
*   **DOP의 장점**:
    *   Reduces complexity by rethinking data.
    *   Compatible with OOP and FP.
    *   Immutability brings serenity.
*   **설계 팁**:
    *   Design patterns can mitigate complexity.
*   **OOP vs DOP**:
    *   A system where every class is split into two independent parts (code and data) is simpler.
    *   A system made of multiple simple independent parts is less complex.
    *   Data immutability makes code predictable.
    *   Most OOP programming languages alleviate slightly the difficulty involved the conversion from and to JSON. It either involves reflection, which is definitely a complex thing, or code verbosity.

## 주요 화제
*   OOP의 복잡성
*   DOP의 소개와 OOP와의 비교
*   데이터 가변성의 문제점

## 부차 화제
*   설계 패턴의 활용
*   JSON 변환의 어려움
*   코드와 데이터의 분리
*   관계(Composition, Association, Usage, Inheritance)의 표현


# 내용
---
## Summary
Complexity in the context of this book means hard to understand.
We use the terms code and behavior interchangeably.
DOP stands for data-oriented programming.
OOP stands for object-oriented programming.
FP stands for functional programming.
In a composition relation, when one object dies, the other one also dies.
A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
In an association relation, each object has an independent life cycle.
A many-to-many association relation is represented by an empty diamond and a
star at both edges.
Dashed arrows indicate a usage relation; for instance, when a class uses a method
of another class.
Plain arrows with empty triangles represent class inheritance, where the arrow
points towards the superclass.
The design presented in this chapter doesn’t pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.
Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
In traditional OOP, data is mutable.
The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
When code and data are mixed, classes tend to be involved in many relations.
When objects are mutable, extra thinking is required in order to understand
how the code behaves.
When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
When data is locked in objects, data serialization is not trivial.
When code is locked in classes, class hierarchies tend to be complex.
A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
When data is mutable, code is unpredictable.
A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
Data immutability brings serenity to DOP developers’ minds.
Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
In traditional OOP, data serialization is difficult.
In traditional OOP, data is locked in classes as members.
In traditional OOP, code is locked into classes.
DOP reduces complexity by rethinking data.
DOP is compatible both with OOP and FP.

# 구성
---

