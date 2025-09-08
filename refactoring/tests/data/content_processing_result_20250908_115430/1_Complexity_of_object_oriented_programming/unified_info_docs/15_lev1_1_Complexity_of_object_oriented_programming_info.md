# 속성
---
process_status: false

# 추출
---
## 핵심 내용
이 문서는 객체 지향 프로그래밍의 복잡성에 대해 다루고 있습니다. 객체 지향 프로그래밍의 복잡성을 분석하고, 이해하기 어려운 부분을 파악하여 프로그래밍 생산성 향상에 기여하는 것을 목표로 합니다.

## 상세 핵심 내용
객체 지향 프로그래밍은 코드 재사용성과 유지보수성을 높이는 장점이 있지만, 클래스, 객체, 상속, 다형성 등 다양한 개념으로 인해 복잡성이 증가합니다. 특히, 디자인 패턴과 프레임워크를 사용할 경우, 복잡성은 더욱 심화될 수 있습니다. 이 문서는 이러한 복잡성을 분석하고, 개발자들이 객체 지향 프로그래밍의 어려운 부분을 효과적으로 이해하고 활용할 수 있도록 돕는 것을 목표로 합니다. 복잡성을 줄이기 위한 방법, 예를 들어 코드 구조 개선, 적절한 디자인 패턴 선택, 그리고 린(Lean) 개발 방법론의 적용 등을 제시할 수 있을 것입니다. 이러한 노력은 결과적으로 개발 생산성을 향상시키고, 유지보수 비용을 절감하는 데 기여할 수 있습니다.

## 상세 정보
*   객체 지향 프로그래밍의 복잡성 분석
    *   클래스, 객체, 상속, 다형성 등 주요 개념의 이해
    *   디자인 패턴과 프레임워크 사용으로 인한 복잡성 증가
*   복잡성 감소 방안
    *   코드 구조 개선
    *   적절한 디자인 패턴 선택
    *   린(Lean) 개발 방법론 적용
*   목표: 개발 생산성 향상 및 유지보수 비용 절감

## 주요 화제
*   객체 지향 프로그래밍의 복잡성
*   객체 지향 프로그래밍의 주요 개념 (클래스, 객체, 상속, 다형성)
*   디자인 패턴과 프레임워크의 복잡성 증가
*   복잡성 감소 방안
*   개발 생산성 향상 및 유지보수 비용 절감

## 부차 화제
*   린(Lean) 개발 방법론


# 내용
---
# 1 Complexity of object- oriented programming
--- 페이지 31 ---
3
Complexity of object-
oriented programming
A capricious entrepreneur
In this chapter, we’ll explore why object-oriented programming (OOP) systems tend to
be complex. This complexity is not related to the syntax or the semantics of a specific
OOP language. It is something that is inherent to OOP’s fundamental insight—
programs should be composed from objects, which consist of some state, together
with methods for accessing and manipulating that state.
 Over the years, OOP ecosystems have alleviated this complexity by adding new
features to the language (e.g., anonymous classes and anonymous functions) and
by developing frameworks that hide some of this complexity, providing a simpler
interface for developers (e.g., Spring and Jackson in Java). Internally, the frame-
works rely on the advanced features of the language such as reflection and custom
annotations.
 
This chapter covers
The tendency of OOP to increase system 
complexity
What makes OOP systems hard to understand
The cost of mixing code and data together into 
objects

--- 페이지 32 ---
4
CHAPTER 1
Complexity of object-oriented programming
 This chapter is not meant to be read as a critical analysis of OOP. Its purpose is to
raise your awareness of the tendency towards OOP’s increased complexity as a pro-
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
