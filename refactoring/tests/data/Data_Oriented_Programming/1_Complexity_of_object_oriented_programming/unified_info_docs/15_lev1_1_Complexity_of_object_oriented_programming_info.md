# 속성
---
process_status: false

# 추출
---
## 핵심 내용
이 문서는 객체 지향 프로그래밍(OOP)의 복잡성에 대한 내용을 다루고 있습니다. OOP 설계, UML, 구현 단계 등 OOP 관련 다양한 주제를 다루며, 복잡성의 원인과 관련된 세부 정보도 제공합니다.

## 상세 핵심 내용
이 문서는 객체 지향 프로그래밍의 설계, UML 사용법, 구현 단계 등 OOP의 전반적인 과정을 구성 파일 형태로 제시합니다. 객체 지향 프로그래밍의 설계와 구현 단계, UML 다이어그램의 활용, 그리고 복잡성의 원인 분석에 중점을 둡니다. 복잡성의 원인으로는 클래스 간의 다양한 관계, 예측 불가능한 코드 동작, 데이터 직렬화의 어려움, 복잡한 클래스 계층 구조 등이 있습니다. 마지막으로, OOP의 복잡성을 요약하는 구성 파일을 포함합니다.

## 상세 정보
### 구성 파일 목록:
*   16\_lev2\_1.1\_OOP\_design\_Classic\_or\_classical\_info.md
*   17\_lev3\_1.1.1\_The\_design\_phase\_info.md
*   18\_lev3\_1.1.2\_UML\_101\_info.md
*   19\_lev3\_1.1.3\_Explaining\_each\_piece\_of\_the\_class\_diagram\_info.md
*   20\_lev3\_1.1.4\_The\_implementation\_phase\_info.md
*   21\_lev2\_1.2\_Sources\_of\_complexity\_info.md
*   22\_lev3\_1.2.1\_Many\_relations\_between\_classes\_info.md
*   23\_lev3\_1.2.2\_Unpredictable\_code\_behavior\_info.md
*   24\_lev3\_1.2.3\_Not\_trivial\_data\_serialization\_info.md
*   25\_lev3\_1.2.4\_Complex\_class\_hierarchies\_info.md
*   26\_lev2\_Summary\_info.md

### OOP 설계
*   클래식 OOP 설계
*   설계 단계
*   UML 101
*   클래스 다이어그램 설명
*   구현 단계

### OOP 복잡성 원인
*   클래스 간의 다양한 관계
*   예측 불가능한 코드 동작
*   데이터 직렬화의 어려움
*   복잡한 클래스 계층 구조

## 주요 화제
*   객체 지향 프로그래밍 (OOP)
*   OOP 설계
*   UML
*   구현 단계
*   OOP 복잡성

## 부차 화제
*   클래스 다이어그램
*   데이터 직렬화
*   클래스 계층 구조


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
