# Data-Oriented Programming (node0)

## Part1—Flexibility (node1)

### Part1 Introduction (사용자 추가) (node2)
- Part1 Introduction content (node3) **[LEAF]**

### 1 Complexity of object-oriented programming (node2)
- 1.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 31-32]**
- 1.1 OOP design: Classic or classical? (node3)
  - 1.1.0 Introduction (사용자 추가) (node4) **[LEAF]** **[Pages: 32-33]**
  - 1.1.1 The design phase (node4) **[LEAF]** **[Pages: 34-35]**
  - 1.1.2 UML 101 (node4) **[LEAF]** **[Pages: 36-37]**
  - 1.1.3 Explaining each piece of the class diagram (node4) **[LEAF]** **[Pages: 38-39]**
  - 1.1.4 The implementation phase (node4) **[LEAF]** **[Pages: 40-41]**
- 1.2 Sources of complexity (node3)
  - 1.2.0 Introduction (사용자 추가) (node4) **[LEAF]** **[Pages: 42-43]**
  - 1.2.1 Many relations between classes (node4) **[LEAF]** **[Pages: 44-45]**
  - 1.2.2 Unpredictable code behavior (node4) **[LEAF]** **[Pages: 46-47]**
  - 1.2.3 Not trivial data serialization (node4) **[LEAF]** **[Pages: 48-49]**
  - 1.2.4 Complex class hierarchies (node4) **[LEAF]** **[Pages: 50-51]**
- Summary (node3) **[LEAF]** **[Pages: 52-53]**

### 2 Separation between code and data (node2)
- 2.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 54-55]**
- 2.1 The two parts of a DOP system (node3) **[LEAF]** **[Pages: 56-57]**
- 2.2 Data entities (node3) **[LEAF]** **[Pages: 58-59]**
- 2.3 Code modules (node3) **[LEAF]** **[Pages: 60-61]**
- 2.4 DOP systems are easy to understand (node3) **[LEAF]** **[Pages: 62-63]**
- 2.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 54-55]**
- 2.5 DOP systems are flexible (node3) **[LEAF]** **[Pages: 66-67]**
- Summary (node3) **[LEAF]** **[Pages: 68-70]**

### 3 Basic data manipulation (node2)
- 3.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 71-74]**
- 3.1 Designing a data model (node3) **[LEAF]** **[Pages: 75-78]**
- 3.2 Representing records as maps (node3) **[LEAF]** **[Pages: 79-82]**
- 3.3 Manipulating data with generic functions (node3) **[LEAF]** **[Pages: 83-86]**
- 3.4 Calculating search results (node3) **[LEAF]** **[Pages: 87-90]**
- 3.5 Handling records of different types (node3) **[LEAF]** **[Pages: 91-94]**
- Summary (node3) **[LEAF]** **[Pages: 95-98]**

### 4 State management (node2)
- 4.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 99-100]**
- 4.1 Multiple versions of the system data (node3) **[LEAF]** **[Pages: 101-102]**
- 4.2 Structural sharing (node3) **[LEAF]** **[Pages: 103-104]**
- 4.3 Implementing structural sharing (node3) **[LEAF]** **[Pages: 105-106]**
- 4.4 Data safety (node3) **[LEAF]** **[Pages: 107-109]**
- 4.5 The commit phase of a mutation (node3) **[LEAF]** **[Pages: 110-111]**
- 4.6 Ensuring system state integrity (node3) **[LEAF]** **[Pages: 112-113]**
- 4.7 Restoring previous states (node3) **[LEAF]** **[Pages: 114-115]**
- Summary (node3) **[LEAF]** **[Pages: 116-118]**

### 5 Basic concurrency control (node2)
- 5.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 119-120]**
- 5.1 Optimistic concurrency control (node3) **[LEAF]** **[Pages: 121-123]**
- 5.2 Reconciliation between concurrent mutations (node3) **[LEAF]** **[Pages: 124-126]**
- 5.3 Reducing collections (node3) **[LEAF]** **[Pages: 127-128]**
- 5.4 Structural difference (node3) **[LEAF]** **[Pages: 129-131]**
- 5.5 Implementing the reconciliation algorithm (node3) **[LEAF]** **[Pages: 132-134]**
- Summary (node3) **[LEAF]** **[Pages: 135-137]**

### 6 Unit tests (node2)
- 6.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 138-139]**
- 6.1 The simplicity of data-oriented test cases (node3) **[LEAF]** **[Pages: 140-142]**
- 6.2 Unit tests for data manipulation code (node3)
  - 6.2.0 Introduction (사용자 추가) (node4) **[LEAF]** **[Pages: 143-144]**
  - 6.2.1 The tree of function calls (node4) **[LEAF]** **[Pages: 145-147]**
  - 6.2.2 Unit tests for functions down the tree (node4) **[LEAF]** **[Pages: 148-149]**
  - 6.2.3 Unit tests for nodes in the tree (node4) **[LEAF]** **[Pages: 150-152]**
- 6.3 Unit tests for queries (node3) **[LEAF]** **[Pages: 153-155]**
- 6.4 Unit tests for mutations (node3) **[LEAF]** **[Pages: 156-157]**
- Moving forward (node3) **[LEAF]** **[Pages: 158-160]**
- Summary (node3) **[LEAF]** **[Pages: 161-162]**

## Part2—Scalability (node1)
- Part2 Introduction content (node3) **[LEAF]** **[Pages: 163-165]**

### Part2 Introduction (사용자 추가) (node2)
- Part2 Introduction content (node3) **[LEAF]** **[Pages: 163-165]**

### 7 Basic data validation (node2)
- 7.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 169-171]**
- 7.1 Data validation in DOP (node3) **[LEAF]** **[Pages: 172-174]**
- 7.2 JSON Schema in a nutshell (node3) **[LEAF]** **[Pages: 175-177]**
- 7.3 Schema flexibility and strictness (node3) **[LEAF]** **[Pages: 178-180]**
- 7.4 Schema composition (node3) **[LEAF]** **[Pages: 181-183]**
- 7.5 Details about data validation failures (node3) **[LEAF]** **[Pages: 184-186]**
- Summary (node3) **[LEAF]** **[Pages: 187-190]**

### 8 Advanced concurrency control (node2)
- 8.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 191-192]**
- 8.1 The complexity of locks (node3) **[LEAF]** **[Pages: 193-194]**
- 8.2 Thread-safe counter with atoms (node3) **[LEAF]** **[Pages: 195-196]**
- 8.3 Thread-safe cache with atoms (node3) **[LEAF]** **[Pages: 197-198]**
- 8.4 State management with atoms (node3) **[LEAF]** **[Pages: 199-200]**
- Summary (node3) **[LEAF]** **[Pages: 201-202]**

### 9 Persistent data structures (node2)
- 9.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 203-204]**
- 9.1 The need for persistent data structures (node3) **[LEAF]** **[Pages: 204-205]**
- 9.2 The efficiency of persistent data structures (node3) **[LEAF]** **[Pages: 206-207]**
- 9.3 Persistent data structures libraries (node3)
  - 9.3.0 Introduction (사용자 추가) (node4) **[LEAF]** **[Pages: 208-209]**
  - 9.3.1 Persistent data structures in Java (node4) **[LEAF]** **[Pages: 210-211]**
  - 9.3.2 Persistent data structures in JavaScript (node4) **[LEAF]** **[Pages: 212-213]**
- 9.4 Persistent data structures in action (node3)
  - 9.4.0 Introduction (사용자 추가) (node4) **[LEAF]** **[Pages: 214-215]**
  - 9.4.1 Writing queries with persistent data structures (node4) **[LEAF]** **[Pages: 215-216]**
  - 9.4.2 Writing mutations with persistent data structures (node4) **[LEAF]** **[Pages: 217-218]**
  - 9.4.3 Serialization and deserialization (node4) **[LEAF]** **[Pages: 219-220]**
  - 9.4.4 Structural diff (node4) **[LEAF]** **[Pages: 221-222]**
- Summary (node3) **[LEAF]** **[Pages: 223-224]**

### 10 Database operations (node2)
- 10.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 225-227]**
- 10.1 Fetching data from the database (node3) **[LEAF]** **[Pages: 228-231]**
- 10.2 Storing data in the database (node3) **[LEAF]** **[Pages: 232-235]**
- 10.3 Simple data manipulation (node3) **[LEAF]** **[Pages: 236-239]**
- 10.4 Advanced data manipulation (node3) **[LEAF]** **[Pages: 240-243]**
- Summary (node3) **[LEAF]** **[Pages: 244-247]**

### 11 Web services (node2)
- 11.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 248-249]**
- 11.1 Another feature request (node3) **[LEAF]** **[Pages: 250-252]**
- 11.2 Building the insides like the outsides (node3) **[LEAF]** **[Pages: 253-255]**
- 11.3 Representing a client request as a map (node3) **[LEAF]** **[Pages: 256-257]**
- 11.4 Representing a server response as a map (node3) **[LEAF]** **[Pages: 258-260]**
- 11.5 Passing information forward (node3) **[LEAF]** **[Pages: 261-263]**
- 11.6 Search result enrichment in action (node3) **[LEAF]** **[Pages: 264-265]**
- Delivering on time (node3) **[LEAF]** **[Pages: 266-268]**
- Summary (node3) **[LEAF]** **[Pages: 269-271]**

## Part3—Maintainability (node1)

### Part3 Introduction (사용자 추가) (node2)
- Part3 Introduction content (node3) **[LEAF]** **[Pages: 272-274]**

### 12 Advanced data validation (node2)
- 12.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 275-277]**
- 12.1 Function arguments validation (node3) **[LEAF]** **[Pages: 278-280]**
- 12.2 Return value validation (node3) **[LEAF]** **[Pages: 281-283]**
- 12.3 Advanced data validation (node3) **[LEAF]** **[Pages: 284-286]**
- 12.4 Automatic generation of data model diagrams (node3) **[LEAF]** **[Pages: 287-289]**
- 12.5 Automatic generation of schema-based unit tests (node3) **[LEAF]** **[Pages: 290-292]**
- 12.6 A new gift (node3) **[LEAF]** **[Pages: 293-295]**
- Summary (node3) **[LEAF]** **[Pages: 296-299]**

### 13 Polymorphism (node2)
- 13.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 300-302]**
- 13.1 The essence of polymorphism (node3) **[LEAF]** **[Pages: 303-305]**
- 13.2 Multimethods with single dispatch (node3) **[LEAF]** **[Pages: 306-308]**
- 13.3 Multimethods with multiple dispatch (node3) **[LEAF]** **[Pages: 309-312]**
- 13.4 Multimethods with dynamic dispatch (node3) **[LEAF]** **[Pages: 313-315]**
- 13.5 Integrating multimethods in a production system (node3) **[LEAF]** **[Pages: 316-318]**
- Summary (node3) **[LEAF]** **[Pages: 319-322]**

### 14 Advanced data manipulation (node2)
- 14.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 323-324]**
- 14.1 Updating a value in a map with eloquence (node3) **[LEAF]** **[Pages: 325-327]**
- 14.2 Manipulating nested data (node3) **[LEAF]** **[Pages: 328-330]**
- 14.3 Using the best tool for the job (node3) **[LEAF]** **[Pages: 331-332]**
- 14.4 Unwinding at ease (node3) **[LEAF]** **[Pages: 333-335]**
- Summary (node3) **[LEAF]** **[Pages: 336-338]**

### 15 Debugging (node2)
- 15.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 339-340]**
- 15.1 Determinism in programming (node3) **[LEAF]** **[Pages: 339-340]**
- 15.2 Reproducibility with numbers and strings (node3) **[LEAF]** **[Pages: 340-341]**
- 15.3 Reproducibility with any data (node3) **[LEAF]** **[Pages: 341-342]**
- 15.4 Unit tests (node3) **[LEAF]** **[Pages: 342-343]**
- 15.5 Dealing with external data sources (node3) **[LEAF]** **[Pages: 343-344]**
- Farewell (node3) **[LEAF]** **[Pages: 343-344]**
- Summary (node3) **[LEAF]** **[Pages: 344-345]**

## Appendix A—Principles of data-oriented programming (node1)
- A.0 Introduction (사용자 추가) (node2) **[LEAF]** **[Pages: 345-346]**
- A.1 Principle #1: Separate code from data (node2)
  - A.1.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 346-347]**
  - A.1.1 Illustration of Principle #1 (node3) **[LEAF]** **[Pages: 347-348]**
  - A.1.2 Benefits of Principle #1 (node3) **[LEAF]** **[Pages: 347-348]**
  - A.1.3 Cost for Principle #1 (node3) **[LEAF]** **[Pages: 348-349]**
  - A.1.4 Summary of Principle #1 (node3) **[LEAF]** **[Pages: 349-350]**
- A.2 Principle #2: Represent data with generic data structures (node2)
  - A.2.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 350-351]**
  - A.2.1 Illustration of Principle #2 (node3) **[LEAF]** **[Pages: 351-352]**
  - A.2.2 Benefits of Principle #2 (node3) **[LEAF]** **[Pages: 351-352]**
  - A.2.3 Cost for Principle #2 (node3) **[LEAF]** **[Pages: 352-353]**
  - A.2.4 Summary of Principle #2 (node3) **[LEAF]** **[Pages: 353-354]**
- A.3 Principle #3: Data is immutable (node2)
  - A.3.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 354-355]**
  - A.3.1 Illustration of Principle #3 (node3) **[LEAF]** **[Pages: 355-356]**
  - A.3.2 Benefits of Principle #3 (node3) **[LEAF]** **[Pages: 356-357]**
  - A.3.3 Cost for Principle #3 (node3) **[LEAF]** **[Pages: 356-357]**
  - A.3.4 Summary of Principle #3 (node3) **[LEAF]** **[Pages: 357-358]**
- A.4 Principle #4: Separate data schema from data representation (node2)
  - A.4.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 358-359]**
  - A.4.1 Illustration of Principle #4 (node3) **[LEAF]** **[Pages: 359-360]**
  - A.4.2 Benefits of Principle #4 (node3) **[LEAF]** **[Pages: 360-361]**
  - A.4.3 Cost for Principle #4 (node3) **[LEAF]** **[Pages: 360-361]**
  - A.4.4 Summary of Principle #4 (node3) **[LEAF]** **[Pages: 361-362]**
- Conclusion (node2) **[LEAF]** **[Pages: 362-363]**

## Appendix B—Generic data access in statically-typed languages (node1)
- B.0 Introduction (사용자 추가) (node2) **[LEAF]** **[Pages: 363-364]**
- B.1 Dynamic getters for string maps (node2)
  - B.1.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 364-365]**
  - B.1.1 Accessing non-nested map fields with dynamic getters (node3) **[LEAF]** **[Pages: 364-365]**
  - B.1.2 Accessing nested map fields with dynamic getters (node3) **[LEAF]** **[Pages: 365-366]**
- B.2 Value getters for maps (node2)
  - B.2.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 366-367]**
  - B.2.1 Accessing non-nested map fields with value getters (node3) **[LEAF]** **[Pages: 367-368]**
  - B.2.2 Accessing nested map fields with value getters (node3) **[LEAF]** **[Pages: 368-369]**
- B.3 Typed getters for maps (node2)
  - B.3.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 368-369]**
  - B.3.1 Accessing non-nested map fields with typed getters (node3) **[LEAF]** **[Pages: 369-370]**
  - B.3.2 Accessing nested map fields with typed getters (node3) **[LEAF]** **[Pages: 370-371]**
- B.4 Generic access to class members (node2)
  - B.4.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 371-372]**
  - B.4.1 Generic access to non-nested class members (node3) **[LEAF]** **[Pages: 372-373]**
  - B.4.2 Generic access to nested class members (node3) **[LEAF]** **[Pages: 373-374]**
  - B.4.3 Automatic JSON serialization of objects (node3) **[LEAF]** **[Pages: 373-374]**
- Summary (node2) **[LEAF]** **[Pages: 344-345]**

## Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
- C.0 Introduction (사용자 추가) (node2) **[LEAF]** **[Pages: 375-376]**
- C.1 Time line (node2)
  - C.1.1 1958: Lisp (node3) **[LEAF]** **[Pages: 376-377]**
  - C.1.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 377-378]**
  - C.1.2 1981: Values and objects (node3) **[LEAF]** **[Pages: 377-378]**
  - C.1.3 2000: Ideal hash trees (node3) **[LEAF]** **[Pages: 378-379]**
  - C.1.4 2006: Out of the Tar Pit (node3) **[LEAF]** **[Pages: 379-380]**
  - C.1.5 2007: Clojure (node3) **[LEAF]** **[Pages: 380-381]**
  - C.1.6 2009: Immutability for all (node3) **[LEAF]** **[Pages: 381-382]**
- C.2 DOP principles as best practices (node2)
  - C.2.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 381-382]**
  - C.2.1 Principle #1: Separate code from data (node3) **[LEAF]** **[Pages: 382-383]**
  - C.2.2 Principle #2: Represent data with generic data structures (node3) **[LEAF]** **[Pages: 383-384]**
  - C.2.3 Principle #3: Data is immutable (node3) **[LEAF]** **[Pages: 384-385]**
  - C.2.4 Principle #4: Separate data schema from data representation (node3) **[LEAF]** **[Pages: 385-386]**
- C.3 DOP and other data-related paradigms (node2)
  - C.3.0 Introduction (사용자 추가) (node3) **[LEAF]** **[Pages: 385-386]**
  - C.3.1 Data-oriented design (node3) **[LEAF]** **[Pages: 386-387]**
  - C.3.2 Data-driven programming (node3) **[LEAF]** **[Pages: 387-388]**
  - C.3.3 Data-oriented programming (DOP) (node3) **[LEAF]** **[Pages: 388-389]**
- Summary (node2) **[LEAF]** **[Pages: 344-345]**

## Appendix D—Lodash reference (node1)