# 속성
---
process_status: false

# 추출
---
<부모 노드 반영 완료>

## Core 내용
DOP는 코드와 데이터 분리를 핵심으로 하는 프로그래밍 패러다임으로, 시스템의 유연성과 단순성을 향상시킵니다. 데이터는 데이터 엔티티로, 코드는 stateless functions로 구성됩니다.

## 상세 핵심 내용
본 챕터는 DOP의 핵심 원리를 요약하고, 코드와 데이터 분리의 중요성을 강조합니다. DOP 시스템의 장점, 데이터 엔티티와 코드 모듈의 역할 및 관계를 명확히 설명합니다. 또한, OOP와의 비교 및 다형성 구현 방식을 간략하게 언급합니다.

## 상세 정보 내용
본 챕터는 DOP의 원리, 코드와 데이터 분리, DOP 시스템의 장점, 데이터 엔티티와 코드 모듈의 역할 및 관계를 요약합니다. DOP와 OOP 비교, stateless functions, 데이터 캡슐화에 대한 간략한 설명을 제공합니다.

## 주요 화제
*   DOP (Data-Oriented Programming)의 원리
*   코드와 데이터의 분리
*   DOP 시스템의 장점 (유연성, 단순성, 변경 용이성)
*   데이터 엔티티와 코드 모듈의 역할 및 관계

## 부차 화제
*   DOP와 OOP 비교
*   Stateless functions
*   데이터 캡슐화
*   Polymorphism (챕터 13 참조)


# 내용
---
## Summary
DOP principles are language-agnostic.
DOP principle #1 is to separate code from data.
The separation between code and data in DOP systems makes them simpler
(easier to understand) than traditional OOP systems.
Data entities are the parts of your system that hold information.
DOP is against data encapsulation.
The more flexible a system is, the easier it is to adapt to changing requirements.
The separation between code and data in DOP systems makes them more flexi-
ble than traditional OOP systems.
When code is separated from data, we have the freedom to design code and
data in isolation.
We represent data as data entities.
We discover the data entities of our system and sort them into high-level groups,
either as a nested list or as a mind map.
A DOP system is easier to understand than a traditional OOP system because
the system is split into two parts: data entities and code modules.
In DOP, a code module is an aggregation of stateless functions.
DOP systems are flexible. Quite often they adapt to changing requirements
without changing the system design.
In traditional OOP, the state of the object is an implicit argument to the meth-
ods of the object.
Stateless functions receive data they manipulate as an explicit argument.
The high-level modules of a DOP system correspond to high-level data entities.
The only kind of relation between code modules is the usage relation.
The only kinds of relation between data entities are the association and the compo-
sition relation.
For a discussion of polymorphism in DOP, see chapter 13.


# 구성
---

