### 1 Complexity of object-oriented programming
### 1 Complexity of object-oriented programming Intro
- 1.1 OOP design: Classic or classical?
- 1.1 OOP design: Classic or classical? Intro
  - 1.1.1 The design phase
  - 1.1.2 UML 101
  - 1.1.3 Explaining each piece of the class diagram
  - 1.1.4 The implementation phase
- 1.2 Sources of complexity
- 1.2 Sources of complexity Intro
  - 1.2.1 Many relations between classes
  - 1.2.2 Unpredictable code behavior
  - 1.2.3 Not trivial data serialization
  - 1.2.4 Complex class hierarchies
### 2 Separation between code and data
- 2.1 The two parts of a DOP system
- 2.2 Data entities
- 2.3 Code modules
- 2.4 DOP systems are easy to understand
- 2.5 DOP systems are flexible
### 3 Basic data manipulation
- 3.1 Designing a data model
- 3.2 Representing records as maps
- 3.3 Manipulating data with generic functions
- 3.4 Calculating search results
- 3.5 Handling records of different types
### 4 State management
- 4.1 Multiple versions of the system data
- 4.2 Structural sharing
- 4.3 Implementing structural sharing
- 4.4 Data safety
- 4.5 The commit phase of a mutation
- 4.6 Ensuring system state integrity
- 4.7 Restoring previous states
### 5 Basic concurrency control
- 5.1 Optimistic concurrency control
- 5.2 Reconciliation between concurrent mutations
- 5.3 Reducing collections
- 5.4 Structural difference
- 5.5 Implementing the reconciliation algorithm
### 6 Unit tests
- 6.1 The simplicity of data-oriented test cases
- 6.2 Unit tests for data manipulation code
  - 6.2.1 The tree of function calls
  - 6.2.2 Unit tests for functions down the tree
  - 6.2.3 Unit tests for nodes in the tree
- 6.3 Unit tests for queries
- 6.4 Unit tests for mutations
### 7 Basic data validation
- 7.1 Data validation in DOP
- 7.2 JSON Schema in a nutshell
- 7.3 Schema flexibility and strictness
- 7.4 Schema composition
- 7.5 Details about data validation failures
### 8 Advanced concurrency control
- 8.1 The complexity of locks
- 8.2 Thread-safe counter with atoms
- 8.3 Thread-safe cache with atoms
- 8.4 State management with atoms
### 9 Persistent data structures
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
### 10 Database operations
- 10.1 Fetching data from the database
- 10.2 Storing data in the database
- 10.3 Simple data manipulation
- 10.4 Advanced data manipulation
### 11 Web services
- 11.1 Another feature request
- 11.2 Building the insides like the outsides
- 11.3 Representing a client request as a map
- 11.4 Representing a server response as a map
- 11.5 Passing information forward
- 11.6 Search result enrichment in action
### 12 Advanced data validation
- 12.1 Function arguments validation
- 12.2 Return value validation
- 12.3 Advanced data validation
- 12.4 Automatic generation of data model diagrams
- 12.5 Automatic generation of schema-based unit tests
- 12.6 A new gift
### 13 Polymorphism
- 13.1 The essence of polymorphism
- 13.2 Multimethods with single dispatch
- 13.3 Multimethods with multiple dispatch
- 13.4 Multimethods with dynamic dispatch
- 13.5 Integrating multimethods in a production system
### 14 Advanced data manipulation
- 14.1 Updating a value in a map with eloquence
- 14.2 Manipulating nested data
- 14.3 Using the best tool for the job
- 14.4 Unwinding at ease
### 15 Debugging
- 15.1 Determinism in programming
- 15.2 Reproducibility with numbers and strings
- 15.3 Reproducibility with any data
- 15.4 Unit tests
- 15.5 Dealing with external data sources