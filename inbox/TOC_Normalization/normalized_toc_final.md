# Data-Oriented Programming - Table of Contents

## Front Matter
- Data-Oriented Programming
- brief contents
- contents
- forewords
- preface
- acknowledgments
- about this book
  - Who should read this book?
  - How this book is organized: A road map
  - About the code
  - liveBook discussion forum
- about the author
- about the cover illustration
- dramatis personae

## Part 1—Flexibility

1.0 Introduction (사용자 추가)
### 1 Complexity of object-oriented programming
- 1.0 Introduction (사용자 추가)
- 1.1 OOP design: Classic or classical?
  - 1.1.0 Introduction (사용자 추가)
  - 1.1.1 The design phase
  - 1.1.2 UML 101
  - 1.1.3 Explaining each piece of the class diagram
  - 1.1.4 The implementation phase
- 1.2 Sources of complexity
  - 1.2.0 Introduction (사용자 추가)
  - 1.2.1 Many relations between classes
  - 1.2.2 Unpredictable code behavior
  - 1.2.3 Not trivial data serialization
  - 1.2.4 Complex class hierarchies
- Summary

### 2 Separation between code and data
- 2.1 The two parts of a DOP system
- 2.2 Data entities
- 2.3 Code modules
- 2.4 DOP systems are easy to understand
- 2.0 Introduction (사용자 추가)
- 2.5 DOP systems are flexible
- Summary

### 3 Basic data manipulation
- 3.0 Introduction (사용자 추가)
- 3.1 Designing a data model
- 3.2 Representing records as maps
- 3.3 Manipulating data with generic functions
- 3.4 Calculating search results
- 3.5 Handling records of different types
- Summary

### 4 State management
- 4.0 Introduction (사용자 추가)
- 4.1 Multiple versions of the system data
- 4.2 Structural sharing
- 4.3 Implementing structural sharing
- 4.4 Data safety
- 4.5 The commit phase of a mutation
- 4.6 Ensuring system state integrity
- 4.7 Restoring previous states
- Summary

### 5 Basic concurrency control
- 5.0 Introduction (사용자 추가)
- 5.1 Optimistic concurrency control
- 5.2 Reconciliation between concurrent mutations
- 5.3 Reducing collections
- 5.4 Structural difference
- 5.5 Implementing the reconciliation algorithm
- Summary

### 6 Unit tests
- 6.1 The simplicity of data-oriented test cases
- 6.0 Introduction (사용자 추가)
- 6.2 Unit tests for data manipulation code
  - 6.2.0 Introduction (사용자 추가)
  - 6.2.1 The tree of function calls
  - 6.2.2 Unit tests for functions down the tree
  - 6.2.3 Unit tests for nodes in the tree
- 6.3 Unit tests for queries
- 6.4 Unit tests for mutations
- Moving forward
- Summary

## Part 2—Scalability

2.0 Introduction (사용자 추가)
### 7 Basic data validation
- 7.1 Data validation in DOP
- 7.0 Introduction (사용자 추가)
- 7.2 JSON Schema in a nutshell
- 7.3 Schema flexibility and strictness
- 7.4 Schema composition
- 7.5 Details about data validation failures
- Summary

### 8 Advanced concurrency control
- 8.1 The complexity of locks
- 8.0 Introduction (사용자 추가)
- 8.2 Thread-safe counter with atoms
- 8.3 Thread-safe cache with atoms
- 8.4 State management with atoms
- Summary

### 9 Persistent data structures
- 9.1 The need for persistent data structures
- 9.0 Introduction (사용자 추가)
- 9.2 The efficiency of persistent data structures
- 9.3 Persistent data structures libraries
  - 9.3.0 Introduction (사용자 추가)
  - 9.3.1 Persistent data structures in Java
  - 9.3.2 Persistent data structures in JavaScript
- 9.4 Persistent data structures in action
  - 9.4.0 Introduction (사용자 추가)
  - 9.4.1 Writing queries with persistent data structures
  - 9.4.2 Writing mutations with persistent data structures
  - 9.4.3 Serialization and deserialization
  - 9.4.4 Structural diff
- Summary

### 10 Database operations
- 10.1 Fetching data from the database
- 10.0 Introduction (사용자 추가)
- 10.2 Storing data in the database
- 10.3 Simple data manipulation
- 10.4 Advanced data manipulation
- Summary

### 11 Web services
- 11.1 Another feature request
- 11.2 Building the insides like the outsides
- 11.0 Introduction (사용자 추가)
- 11.3 Representing a client request as a map
- 11.4 Representing a server response as a map
- 11.5 Passing information forward
- 11.6 Search result enrichment in action
- Delivering on time
- Summary

## Part 3—Maintainability

3.0 Introduction (사용자 추가)
### 12 Advanced data validation
- 12.1 Function arguments validation
- 12.0 Introduction (사용자 추가)
- 12.2 Return value validation
- 12.3 Advanced data validation
- 12.4 Automatic generation of data model diagrams
- 12.5 Automatic generation of schema-based unit tests
- 12.6 A new gift
- Summary

### 13 Polymorphism
- 13.1 The essence of polymorphism
- 13.0 Introduction (사용자 추가)
- 13.2 Multimethods with single dispatch
- 13.3 Multimethods with multiple dispatch
- 13.4 Multimethods with dynamic dispatch
- 13.5 Integrating multimethods in a production system
- Summary

### 14 Advanced data manipulation
- 14.1 Updating a value in a map with eloquence
- 14.0 Introduction (사용자 추가)
- 14.2 Manipulating nested data
- 14.3 Using the best tool for the job
- 14.4 Unwinding at ease
- Summary

### 15 Debugging
- 15.1 Determinism in programming
- 15.0 Introduction (사용자 추가)
- 15.2 Reproducibility with numbers and strings
- 15.3 Reproducibility with any data
- 15.4 Unit tests
- 15.5 Dealing with external data sources
- Farewell
- Summary

## Appendices

### Appendix A—Principles of data-oriented programming
- A.1 Principle #1: Separate code from data
  - A.1.0 Introduction (사용자 추가)
  - A.1.1 Illustration of Principle #1
  - A.1.2 Benefits of Principle #1
  - A.1.3 Cost for Principle #1
  - A.1.4 Summary of Principle #1
- A.2 Principle #2: Represent data with generic data structures
  - A.2.0 Introduction (사용자 추가)
  - A.2.1 Illustration of Principle #2
  - A.2.2 Benefits of Principle #2
  - A.2.3 Cost for Principle #2
  - A.2.4 Summary of Principle #2
- A.3 Principle #3: Data is immutable
  - A.3.0 Introduction (사용자 추가)
  - A.3.1 Illustration of Principle #3
  - A.3.2 Benefits of Principle #3
  - A.3.3 Cost for Principle #3
  - A.3.4 Summary of Principle #3
- A.4 Principle #4: Separate data schema from data representation
  - A.4.0 Introduction (사용자 추가)
  - A.4.1 Illustration of Principle #4
  - A.4.2 Benefits of Principle #4
  - A.4.3 Cost for Principle #4
  - A.4.4 Summary of Principle #4
- Conclusion

### Appendix B—Generic data access in statically-typed languages
- B.1 Dynamic getters for string maps
  - B.1.0 Introduction (사용자 추가)
  - B.1.1 Accessing non-nested map fields with dynamic getters
  - B.1.2 Accessing nested map fields with dynamic getters
- B.2 Value getters for maps
  - B.2.0 Introduction (사용자 추가)
  - B.2.1 Accessing non-nested map fields with value getters
  - B.2.2 Accessing nested map fields with value getters
- B.3 Typed getters for maps
  - B.3.0 Introduction (사용자 추가)
  - B.3.1 Accessing non-nested map fields with typed getters
  - B.3.2 Accessing nested map fields with typed getters
- B.4 Generic access to class members
  - B.4.0 Introduction (사용자 추가)
  - B.4.1 Generic access to non-nested class members
  - B.4.2 Generic access to nested class members
  - B.4.3 Automatic JSON serialization of objects
- Summary

### Appendix C—Data-oriented programming: A link in the chain of programming paradigms
- C.1 Time line
  - C.1.1 1958: Lisp
  - C.1.0 Introduction (사용자 추가)
  - C.1.2 1981: Values and objects
  - C.1.3 2000: Ideal hash trees
  - C.1.4 2006: Out of the Tar Pit
  - C.1.5 2007: Clojure
  - C.1.6 2009: Immutability for all
- C.2 DOP principles as best practices
  - C.2.0 Introduction (사용자 추가)
  - C.2.1 Principle #1: Separate code from data
  - C.2.2 Principle #2: Represent data with generic data structures
  - C.2.3 Principle #3: Data is immutable
  - C.2.4 Principle #4: Separate data schema from data representation
- C.3 DOP and other data-related paradigms
  - C.3.0 Introduction (사용자 추가)
  - C.3.1 Data-oriented design
  - C.3.2 Data-driven programming
  - C.3.3 Data-oriented programming (DOP)
- Summary

### Appendix D—Lodash reference

## Index
- A
- B
- C
- D
- E
- F
- G
- H
- I
- J
- K
- L
- M
- N
- O
- P
- Q
- R
- S
- T
- U
- V
- W