"""
생성 시간: 2025-08-10 22:28:30 KST
핵심 내용: Data-Oriented Programming의 기본 데이터 검증 (7장) 소개 섹션
상세 내용:
    - 7장 제목과 개요 (1-29행): DOP에서 데이터 검증의 중요성과 이 장에서 다룰 내용 소개
    - 페이지 169 내용 (10-29행): 장 제목, 다룰 내용 목록, DOP에서 데이터 검증이 필요한 이유
상태: 활성
주소: chapter7_00_introduction  
참조: 원본 파일 /home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md
"""

# 7 Basic data validation

**Level:** 1
**페이지 범위:** 169 - 190
**총 페이지 수:** 22
**ID:** 65

---

=== 페이지 169 ===
Basic data validation
A solemn gift
This chapter covers
 The importance of validating data at system
boundaries
 Validating data using the JSON Schema language
 Integrating data validation into an existing code
base
 Getting detailed information about data validation
failures
At first glance, it may seem that embracing DOP means accessing data without validat-
ing it and engaging in wishful thinking, where data is always valid. In fact, data valida-
tion is not only possible but recommended when we follow data-oriented principles.
This chapter illustrates how to validate data when data is represented with
generic data structures. It focuses on data validation occurring at the boundaries of
the system, while in part 3, we will deal with validating data as it flows through the
system. This chapter is a deep dive into the fourth principle of DOP.
PRINCIPLE #4 Separate data schema from data representation.
141