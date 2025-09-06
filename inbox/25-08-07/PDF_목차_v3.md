# 목차
# - 생성 시간: 2025-08-07 20:02:46 KST
# - 핵심 내용: Data-Oriented Programming 책의 완전한 목차 정리 (Introduction 항목 추가)
# - 상세 내용: 
#   - PDF에서 추출한 목차를 독자가 읽기 쉽게 구조화한 문서
#   - 상위 구성 단위와 하위 구성 단위 사이 도입 내용을 "Introduction (사용자 추가)" 항목으로 추가
#   - 각 Introduction 항목의 시작-종료 페이지 표시
# - 상태: 활성
# - 주소: PDF_목차_v3
# - 참조: PDF_목차.md (원본), 2022_Data-Oriented Programming_Manning.pdf

# Data-Oriented Programming 목차 (Introduction 항목 포함)

## 📖 책 정보
- **제목**: Data-Oriented Programming  
- **출판사**: Manning Publications
- **총 페이지**: 426페이지

---

## 📋 전체 구조

### 🔖 Part 1: Flexibility (유연성)
**페이지 29-164 (136페이지)**

**1-0. Introduction (사용자 추가)** (페이지 29-30)

1. **Complexity of object-oriented programming** (페이지 31)
   - **1.0 Introduction (사용자 추가)** (페이지 31-32)
   - 1.1 OOP design: Classic or classical? (페이지 33-41)
     - 1.1.1 The design phase  
     - 1.1.2 UML 101
     - 1.1.3 Explaining each piece of the class diagram
     - 1.1.4 The implementation phase
   - 1.2 Sources of complexity (페이지 42-53)
     - 1.2.1 Many relations between classes
     - 1.2.2 Unpredictable code behavior  
     - 1.2.3 Not trivial data serialization
     - 1.2.4 Complex class hierarchies

2. **Separation between code and data** (페이지 54)
   - **2.0 Introduction (사용자 추가)** (페이지 54-55)
   - 2.1 The two parts of a DOP system
   - 2.2 Data entities
   - 2.3 Code modules
   - 2.4 DOP systems are easy to understand
   - 2.5 DOP systems are flexible

3. **Basic data manipulation** (페이지 71)
   - **3.0 Introduction (사용자 추가)** (페이지 71-72)
   - 3.1 Designing a data model
   - 3.2 Representing records as maps
   - 3.3 Manipulating data with generic functions
   - 3.4 Calculating search results
   - 3.5 Handling records of different types

4. **State management** (페이지 99)
   - **4.0 Introduction (사용자 추가)** (페이지 99-100)
   - 4.1 Multiple versions of the system data
   - 4.2 Structural sharing
   - 4.3 Implementing structural sharing
   - 4.4 Data safety
   - 4.5 The commit phase of a mutation
   - 4.6 Ensuring system state integrity
   - 4.7 Restoring previous states

5. **Basic concurrency control** (페이지 119)
   - **5.0 Introduction (사용자 추가)** (페이지 119-120)
   - 5.1 Optimistic concurrency control
   - 5.2 Reconciliation between concurrent mutations
   - 5.3 Reducing collections
   - 5.4 Structural difference
   - 5.5 Implementing the reconciliation algorithm

6. **Unit tests** (페이지 138)
   - **6.0 Introduction (사용자 추가)** (페이지 138-139)
   - 6.1 The simplicity of data-oriented test cases
   - 6.2 Unit tests for data manipulation code
     - 6.2.1 The tree of function calls
     - 6.2.2 Unit tests for functions down the tree
     - 6.2.3 Unit tests for nodes in the tree
   - 6.3 Unit tests for queries
   - 6.4 Unit tests for mutations

---

### 🔖 Part 2: Scalability (확장성)  
**페이지 165-272 (108페이지)**

**2-0. Introduction (사용자 추가)** (페이지 165-168)

7. **Basic data validation** (페이지 169)
   - **7.0 Introduction (사용자 추가)** (페이지 169-170)
   - 7.1 Data validation in DOP
   - 7.2 JSON Schema in a nutshell
   - 7.3 Schema flexibility and strictness
   - 7.4 Schema composition
   - 7.5 Details about data validation failures

8. **Advanced concurrency control** (페이지 191)
   - **8.0 Introduction (사용자 추가)** (페이지 191-192)
   - 8.1 The complexity of locks
   - 8.2 Thread-safe counter with atoms
   - 8.3 Thread-safe cache with atoms
   - 8.4 State management with atoms

9. **Persistent data structures** (페이지 203)
   - **9.0 Introduction (사용자 추가)** (페이지 203-204)
   - 9.1 The need for persistent data structures
   - 9.2 The efficiency of persistent data structures
   - 9.3 Persistent data structures libraries
     - 9.3.1 Persistent data structures in Java
     - 9.3.2 Persistent data structures in JavaScript
   - 9.4 Persistent data structures in action
     - 9.4.1 Writing queries with persistent data structures
     - 9.4.2 Writing mutations with persistent data structures
     - 9.4.3 Serialization and deserialization
     - 9.4.4 Structural diff

10. **Database operations** (페이지 225)
    - **10.0 Introduction (사용자 추가)** (페이지 225-226)
    - 10.1 Fetching data from the database
    - 10.2 Storing data in the database
    - 10.3 Simple data manipulation
    - 10.4 Advanced data manipulation

11. **Web services** (페이지 248)
    - **11.0 Introduction (사용자 추가)** (페이지 248-249)
    - 11.1 Another feature request
    - 11.2 Building the insides like the outsides
    - 11.3 Representing a client request as a map
    - 11.4 Representing a server response as a map
    - 11.5 Passing information forward
    - 11.6 Search result enrichment in action

---

### 🔖 Part 3: Maintainability (유지보수성)
**페이지 273-360 (88페이지)**

**3-0. Introduction (사용자 추가)** (페이지 273-274)

12. **Advanced data validation** (페이지 275)
    - **12.0 Introduction (사용자 추가)** (페이지 275-276)
    - 12.1 Function arguments validation
    - 12.2 Return value validation
    - 12.3 Advanced data validation
    - 12.4 Automatic generation of data model diagrams
    - 12.5 Automatic generation of schema-based unit tests
    - 12.6 A new gift

13. **Polymorphism** (페이지 300)
    - **13.0 Introduction (사용자 추가)** (페이지 300-301)
    - 13.1 The essence of polymorphism
    - 13.2 Multimethods with single dispatch
    - 13.3 Multimethods with multiple dispatch
    - 13.4 Multimethods with dynamic dispatch
    - 13.5 Integrating multimethods in a production system

14. **Advanced data manipulation** (페이지 323)
    - **14.0 Introduction (사용자 추가)** (페이지 323-324)
    - 14.1 Updating a value in a map with eloquence
    - 14.2 Manipulating nested data
    - 14.3 Using the best tool for the job
    - 14.4 Unwinding at ease

15. **Debugging** (페이지 339)
    - **15.0 Introduction (사용자 추가)** (페이지 339-340)
    - 15.1 Determinism in programming
    - 15.2 Reproducibility with numbers and strings
    - 15.3 Reproducibility with any data
    - 15.4 Unit tests
    - 15.5 Dealing with external data sources

---

## 📎 부록 (Appendices)

**Appendix A**: Principles of data-oriented programming (페이지 361)
- **A.0 Introduction (사용자 추가)** (페이지 361-362)
- A.1 Principle #1: Separate code from data
- A.2 Principle #2: Represent data with generic data structures  
- A.3 Principle #3: Data is immutable
- A.4 Principle #4: Separate data schema from data representation

**Appendix B**: Generic data access in statically-typed languages (페이지 392)
- **B.0 Introduction (사용자 추가)** (페이지 392-393)
- B.1 Dynamic getters for string maps
- B.2 Value getters for maps
- B.3 Typed getters for maps
- B.4 Generic access to class members

**Appendix C**: Data-oriented programming: A link in the chain of programming paradigms (페이지 409)
- **C.0 Introduction (사용자 추가)** (페이지 409-410)
- C.1 Time line
- C.2 DOP principles as best practices
- C.3 DOP and other data-related paradigms

**Appendix D**: Lodash reference (페이지 415)
- **D.0 Introduction (사용자 추가)** (페이지 415-416)

---

## 📊 목차 통계 (수정된 버전)
- **총 15개 챕터** (3개 Part에 걸쳐)
- **4개 부록**  
- **218개 기존 세부 섹션** (북마크 기준)
- **추가된 Introduction 항목**: 22개
  - Part Introduction: 3개 (1-0, 2-0, 3-0)
  - Chapter Introduction: 15개 (1.0~15.0)
  - Appendix Introduction: 4개 (A.0~D.0)
- **전체 332페이지** (본문)
- **총 426페이지** (부록 포함)

## 🎯 핵심 주제
1. **유연성**: OOP 복잡성 해결, 코드-데이터 분리, 기본 데이터 조작
2. **확장성**: 데이터 검증, 동시성 제어, 영속 데이터 구조, 데이터베이스 및 웹 서비스
3. **유지보수성**: 고급 검증, 다형성, 고급 데이터 조작, 디버깅

## 📝 수정 사항
- **추가된 Introduction 항목**: 상위 구성 단위와 첫 번째 하위 구성 단위 사이의 도입 내용을 명시적으로 표시
- **페이지 범위 추정**: 각 Introduction 항목은 일반적으로 1-2페이지 범위로 추정
- **체계적 번호 매기기**: Part는 "X-0", Chapter는 "X.0", Appendix는 "X.0" 형식으로 통일
- **사용자 추가 표시**: 모든 추가된 항목에 "(사용자 추가)" 라벨 표시