# 속성
---
process_status: true


# 추출
---
## 핵심 내용
이 문서는 객체 지향 프로그래밍의 복잡성에 대한 내용을 담고 있습니다. 객체 지향 프로그래밍은 코드의 재사용성과 유지보수성을 높이는 장점이 있지만, 설계 및 구현 단계에서 여러 복잡성을 야기할 수 있습니다. 이러한 복잡성은 개발 프로세스의 효율성을 저해하고, 오류 발생 가능성을 높일 수 있습니다.

## 상세 핵심 내용
객체 지향 프로그래밍은 캡슐화, 상속, 다형성 등의 개념을 통해 코드의 구조화와 재사용성을 높이는 데 기여합니다. 하지만 이러한 특징들은 복잡한 시스템 설계와 구현을 필요로 합니다. 예를 들어, 상속 관계의 깊이와 다형성을 활용하는 과정에서 코드의 가독성이 저하될 수 있으며, 예상치 못한 부작용이 발생할 수 있습니다. 또한, 객체 간의 의존성이 복잡해지면서 변경의 파급 효과를 예측하기 어려워져 유지보수가 어려워질 수 있습니다. 이러한 복잡성을 해결하기 위해서는 설계 단계에서 신중한 고려가 필요하며, 적절한 디자인 패턴과 개발 방법론의 적용이 중요합니다.

## 상세 정보
### 객체 지향 프로그래밍의 장점
*   코드 재사용성 향상
*   유지보수 용이성 증가
*   코드 구조화
### 객체 지향 프로그래밍의 복잡성
*   상속 관계의 깊이로 인한 코드 가독성 저하
*   다형성 사용 시 부작용 발생 가능성
*   객체 간 의존성 증가로 인한 유지보수 어려움
### 복잡성 해결 방안
*   설계 단계에서 신중한 고려
*   적절한 디자인 패턴 활용
*   적절한 개발 방법론 적용

## 주요 화제
*   객체 지향 프로그래밍의 복잡성
*   객체 지향 프로그래밍의 장점
*   복잡성 해결 방안

## 부차 화제
*   캡슐화, 상속, 다형성 (객체 지향 프로그래밍의 핵심 개념)
*   코드의 재사용성
*   유지보수성
*   디자인 패턴
*   개발 방법론


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
