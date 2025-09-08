# 속성
---
process_status: false

# 추출
---
## 핵심 내용
이 문서는 OOP(객체 지향 프로그래밍)의 복잡성을 지적하고, DOP(데이터 지향 프로그래밍)을 대안으로 제시합니다. OOP에서 코드와 데이터의 혼합, 데이터의 가변성 등이 복잡성을 증가시키는 원인으로 분석하며, DOP를 통해 이러한 문제를 해결하고 시스템의 단순성을 확보할 수 있다고 주장합니다.

## 상세 핵심 내용
문서는 OOP 시스템의 복잡성이 코드와 데이터의 혼합, 데이터의 가변성, 클래스 계층 구조의 복잡성, 데이터 직렬화의 어려움 등과 관련이 있음을 설명합니다. OOP에서 코드와 데이터가 섞여 있으면 클래스 간의 관계가 복잡해지고, 데이터가 변경 가능하면 코드의 동작 예측이 어려워집니다. DOP는 데이터를 재고함으로써 이러한 문제를 해결하고, OOP와 FP(함수형 프로그래밍) 모두와 호환됩니다. DOP는 데이터 불변성을 통해 개발자의 심리적 안정감을 높이며, 시스템을 여러 개의 단순한 독립적인 부분으로 구성하여 복잡성을 줄입니다. 마지막으로, 디자인 패턴의 전략적인 사용은 OOP에서 복잡성을 완화하는 데 도움이 될 수 있다고 언급합니다.

## 상세 정보
*   **OOP의 문제점:**
    *   복잡성: 이해하기 어려움.
    *   코드와 데이터 혼합: 클래스 내부에 데이터(멤버)와 코드(메서드)가 함께 존재.
    *   데이터 가변성: 변경 가능.
    *   데이터는 객체에 묶여 있음.
    *   코드 또한 클래스에 묶여 있음.
    *   데이터 직렬화의 어려움.
    *   복잡한 클래스 계층 구조.
*   **DOP의 특징:**
    *   OOP와 FP 모두와 호환.
    *   데이터 재고를 통해 복잡성 감소.
    *   데이터 불변성.
*   **관계:**
    *   Composition: 한 객체가 죽으면 다른 객체도 죽음 (plain diamond + optional star).
    *   Association: 독립적인 생명 주기 (empty diamond + star at both edges).
    *   Usage: dashed arrows.
    *   Inheritance: plain arrows with empty triangles (superclass 방향).
*   **기타:**
    *   디자인 패턴의 활용은 OOP 복잡성 완화에 도움.
    *   OOP에서는 JSON 변환이 복잡하거나 코드의 장황함이 발생.

## 주요 화제
*   OOP의 복잡성
*   DOP의 개념과 장점
*   OOP와 DOP의 비교

## 부차 화제
*   디자인 패턴의 역할
*   JSON 변환의 어려움
*   다중 스레딩 환경에서의 동기화


# 내용
---
## Summary
Summary
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

