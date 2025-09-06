# 폴더 구조 요약 (수정판)

**Root 폴더:** Data-Oriented Programming
**전체 노드 수:** 216
**Internal 노드 (폴더):** 145
**Leaf 노드 (파일 대상):** 71

## 수정사항
- 폴더명: 1.1 -> 1-1, A.1 -> A-1
- Appendices의 단일 문자 폴더(A, B, C 등) 제거
- metadata.json 파일 생성 안함

## 폴더 구조

```
Data-Oriented_Programming/
├── Part_1_Flexibility/
│   ├── 1-0_Introduction_사용자_추가/
│   ├── 1_Complexity_of_object-oriented_programming/
│   │   ├── 1-0_Introduction_사용자_추가/
│   │   ├── 1-1_OOP_design_Classic_or_classical/
│   │   │   ├── 📄 1.1.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 1.1.1 The design phase (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 1.1.2 UML 101 (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 1.1.3 Explaining each piece of the class diagram (node4) [LEAF - 파일 생성 대상]
│   │   │   └── 📄 1.1.4 The implementation phase (node4) [LEAF - 파일 생성 대상]
│   │   ├── 1-2_Sources_of_complexity/
│   │   │   ├── 📄 1.2.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 1.2.1 Many relations between classes (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 1.2.2 Unpredictable code behavior (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 1.2.3 Not trivial data serialization (node4) [LEAF - 파일 생성 대상]
│   │   │   └── 📄 1.2.4 Complex class hierarchies (node4) [LEAF - 파일 생성 대상]
│   │   └── Summary/
│   ├── 2_Separation_between_code_and_data/
│   │   ├── 2-1_The_two_parts_of_a_DOP_system/
│   │   ├── 2-2_Data_entities/
│   │   ├── 2-3_Code_modules/
│   │   ├── 2-4_DOP_systems_are_easy_to_understand/
│   │   ├── 2-0_Introduction_사용자_추가/
│   │   ├── 2-5_DOP_systems_are_flexible/
│   │   └── Summary/
│   ├── 3_Basic_data_manipulation/
│   │   ├── 3-0_Introduction_사용자_추가/
│   │   ├── 3-1_Designing_a_data_model/
│   │   ├── 3-2_Representing_records_as_maps/
│   │   ├── 3-3_Manipulating_data_with_generic_functions/
│   │   ├── 3-4_Calculating_search_results/
│   │   ├── 3-5_Handling_records_of_different_types/
│   │   └── Summary/
│   ├── 4_State_management/
│   │   ├── 4-0_Introduction_사용자_추가/
│   │   ├── 4-1_Multiple_versions_of_the_system_data/
│   │   ├── 4-2_Structural_sharing/
│   │   ├── 4-3_Implementing_structural_sharing/
│   │   ├── 4-4_Data_safety/
│   │   ├── 4-5_The_commit_phase_of_a_mutation/
│   │   ├── 4-6_Ensuring_system_state_integrity/
│   │   ├── 4-7_Restoring_previous_states/
│   │   └── Summary/
│   ├── 5_Basic_concurrency_control/
│   │   ├── 5-0_Introduction_사용자_추가/
│   │   ├── 5-1_Optimistic_concurrency_control/
│   │   ├── 5-2_Reconciliation_between_concurrent_mutations/
│   │   ├── 5-3_Reducing_collections/
│   │   ├── 5-4_Structural_difference/
│   │   ├── 5-5_Implementing_the_reconciliation_algorithm/
│   │   └── Summary/
│   └── 6_Unit_tests/
│       ├── 6-1_The_simplicity_of_data-oriented_test_cases/
│       ├── 6-0_Introduction_사용자_추가/
│       ├── 6-2_Unit_tests_for_data_manipulation_code/
│       │   ├── 📄 6.2.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
│       │   ├── 📄 6.2.1 The tree of function calls (node4) [LEAF - 파일 생성 대상]
│       │   ├── 📄 6.2.2 Unit tests for functions down the tree (node4) [LEAF - 파일 생성 대상]
│       │   └── 📄 6.2.3 Unit tests for nodes in the tree (node4) [LEAF - 파일 생성 대상]
│       ├── 6-3_Unit_tests_for_queries/
│       ├── 6-4_Unit_tests_for_mutations/
│       ├── Moving_forward/
│       └── Summary/
├── Part_2_Scalability/
│   ├── 2-0_Introduction_사용자_추가/
│   ├── 7_Basic_data_validation/
│   │   ├── 7-1_Data_validation_in_DOP/
│   │   ├── 7-0_Introduction_사용자_추가/
│   │   ├── 7-2_JSON_Schema_in_a_nutshell/
│   │   ├── 7-3_Schema_flexibility_and_strictness/
│   │   ├── 7-4_Schema_composition/
│   │   ├── 7-5_Details_about_data_validation_failures/
│   │   └── Summary/
│   ├── 8_Advanced_concurrency_control/
│   │   ├── 8-1_The_complexity_of_locks/
│   │   ├── 8-0_Introduction_사용자_추가/
│   │   ├── 8-2_Thread-safe_counter_with_atoms/
│   │   ├── 8-3_Thread-safe_cache_with_atoms/
│   │   ├── 8-4_State_management_with_atoms/
│   │   └── Summary/
│   ├── 9_Persistent_data_structures/
│   │   ├── 9-1_The_need_for_persistent_data_structures/
│   │   ├── 9-0_Introduction_사용자_추가/
│   │   ├── 9-2_The_efficiency_of_persistent_data_structures/
│   │   ├── 9-3_Persistent_data_structures_libraries/
│   │   │   ├── 📄 9.3.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 9.3.1 Persistent data structures in Java (node4) [LEAF - 파일 생성 대상]
│   │   │   └── 📄 9.3.2 Persistent data structures in JavaScript (node4) [LEAF - 파일 생성 대상]
│   │   ├── 9-4_Persistent_data_structures_in_action/
│   │   │   ├── 📄 9.4.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 9.4.1 Writing queries with persistent data structures (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 9.4.2 Writing mutations with persistent data structures (node4) [LEAF - 파일 생성 대상]
│   │   │   ├── 📄 9.4.3 Serialization and deserialization (node4) [LEAF - 파일 생성 대상]
│   │   │   └── 📄 9.4.4 Structural diff (node4) [LEAF - 파일 생성 대상]
│   │   └── Summary/
│   ├── 10_Database_operations/
│   │   ├── 10-1_Fetching_data_from_the_database/
│   │   ├── 10-0_Introduction_사용자_추가/
│   │   ├── 10-2_Storing_data_in_the_database/
│   │   ├── 10-3_Simple_data_manipulation/
│   │   ├── 10-4_Advanced_data_manipulation/
│   │   └── Summary/
│   └── 11_Web_services/
│       ├── 11-1_Another_feature_request/
│       ├── 11-2_Building_the_insides_like_the_outsides/
│       ├── 11-0_Introduction_사용자_추가/
│       ├── 11-3_Representing_a_client_request_as_a_map/
│       ├── 11-4_Representing_a_server_response_as_a_map/
│       ├── 11-5_Passing_information_forward/
│       ├── 11-6_Search_result_enrichment_in_action/
│       ├── Delivering_on_time/
│       └── Summary/
├── Part_3_Maintainability/
│   ├── 3-0_Introduction_사용자_추가/
│   ├── 12_Advanced_data_validation/
│   │   ├── 12-1_Function_arguments_validation/
│   │   ├── 12-0_Introduction_사용자_추가/
│   │   ├── 12-2_Return_value_validation/
│   │   ├── 12-3_Advanced_data_validation/
│   │   ├── 12-4_Automatic_generation_of_data_model_diagrams/
│   │   ├── 12-5_Automatic_generation_of_schema-based_unit_tests/
│   │   ├── 12-6_A_new_gift/
│   │   └── Summary/
│   ├── 13_Polymorphism/
│   │   ├── 13-1_The_essence_of_polymorphism/
│   │   ├── 13-0_Introduction_사용자_추가/
│   │   ├── 13-2_Multimethods_with_single_dispatch/
│   │   ├── 13-3_Multimethods_with_multiple_dispatch/
│   │   ├── 13-4_Multimethods_with_dynamic_dispatch/
│   │   ├── 13-5_Integrating_multimethods_in_a_production_system/
│   │   └── Summary/
│   ├── 14_Advanced_data_manipulation/
│   │   ├── 14-1_Updating_a_value_in_a_map_with_eloquence/
│   │   ├── 14-0_Introduction_사용자_추가/
│   │   ├── 14-2_Manipulating_nested_data/
│   │   ├── 14-3_Using_the_best_tool_for_the_job/
│   │   ├── 14-4_Unwinding_at_ease/
│   │   └── Summary/
│   └── 15_Debugging/
│       ├── 15-1_Determinism_in_programming/
│       ├── 15-0_Introduction_사용자_추가/
│       ├── 15-2_Reproducibility_with_numbers_and_strings/
│       ├── 15-3_Reproducibility_with_any_data/
│       ├── 15-4_Unit_tests/
│       ├── 15-5_Dealing_with_external_data_sources/
│       ├── Farewell/
│       └── Summary/
└── Appendices/
    ├── Appendix_A_Principles_of_data-oriented_programming/
    │   ├── A-1_Principle_1_Separate_code_from_data/
    │   │   ├── 📄 A.1.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.1.1 Illustration of Principle #1 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.1.2 Benefits of Principle #1 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.1.3 Cost for Principle #1 (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 A.1.4 Summary of Principle #1 (node4) [LEAF - 파일 생성 대상]
    │   ├── A-2_Principle_2_Represent_data_with_generic_data_structures/
    │   │   ├── 📄 A.2.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.2.1 Illustration of Principle #2 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.2.2 Benefits of Principle #2 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.2.3 Cost for Principle #2 (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 A.2.4 Summary of Principle #2 (node4) [LEAF - 파일 생성 대상]
    │   ├── A-3_Principle_3_Data_is_immutable/
    │   │   ├── 📄 A.3.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.3.1 Illustration of Principle #3 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.3.2 Benefits of Principle #3 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.3.3 Cost for Principle #3 (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 A.3.4 Summary of Principle #3 (node4) [LEAF - 파일 생성 대상]
    │   ├── A-4_Principle_4_Separate_data_schema_from_data_representation/
    │   │   ├── 📄 A.4.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.4.1 Illustration of Principle #4 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.4.2 Benefits of Principle #4 (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 A.4.3 Cost for Principle #4 (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 A.4.4 Summary of Principle #4 (node4) [LEAF - 파일 생성 대상]
    │   └── Conclusion/
    ├── Appendix_B_Generic_data_access_in_statically-typed_languages/
    │   ├── B-1_Dynamic_getters_for_string_maps/
    │   │   ├── 📄 B.1.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 B.1.1 Accessing non-nested map fields with dynamic getters (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 B.1.2 Accessing nested map fields with dynamic getters (node4) [LEAF - 파일 생성 대상]
    │   ├── B-2_Value_getters_for_maps/
    │   │   ├── 📄 B.2.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 B.2.1 Accessing non-nested map fields with value getters (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 B.2.2 Accessing nested map fields with value getters (node4) [LEAF - 파일 생성 대상]
    │   ├── B-3_Typed_getters_for_maps/
    │   │   ├── 📄 B.3.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 B.3.1 Accessing non-nested map fields with typed getters (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 B.3.2 Accessing nested map fields with typed getters (node4) [LEAF - 파일 생성 대상]
    │   ├── B-4_Generic_access_to_class_members/
    │   │   ├── 📄 B.4.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 B.4.1 Generic access to non-nested class members (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 B.4.2 Generic access to nested class members (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 B.4.3 Automatic JSON serialization of objects (node4) [LEAF - 파일 생성 대상]
    │   └── Summary/
    ├── Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/
    │   ├── C-1_Time_line/
    │   │   ├── 📄 C.1.1 1958: Lisp (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.1.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.1.2 1981: Values and objects (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.1.3 2000: Ideal hash trees (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.1.4 2006: Out of the Tar Pit (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.1.5 2007: Clojure (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 C.1.6 2009: Immutability for all (node4) [LEAF - 파일 생성 대상]
    │   ├── C-2_DOP_principles_as_best_practices/
    │   │   ├── 📄 C.2.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.2.1 Principle #1: Separate code from data (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.2.2 Principle #2: Represent data with generic data structures (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.2.3 Principle #3: Data is immutable (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 C.2.4 Principle #4: Separate data schema from data representation (node4) [LEAF - 파일 생성 대상]
    │   ├── C-3_DOP_and_other_data-related_paradigms/
    │   │   ├── 📄 C.3.0 Introduction (사용자 추가) (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.3.1 Data-oriented design (node4) [LEAF - 파일 생성 대상]
    │   │   ├── 📄 C.3.2 Data-driven programming (node4) [LEAF - 파일 생성 대상]
    │   │   └── 📄 C.3.3 Data-oriented programming (DOP) (node4) [LEAF - 파일 생성 대상]
    │   └── Summary/
    └── Appendix_D_Lodash_reference/
```

## Leaf 노드 목록 (콘텐츠 추출 대상)

- **1.1.0 Introduction (사용자 추가)** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-1_OOP_design_Classic_or_classical`

- **1.1.1 The design phase** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-1_OOP_design_Classic_or_classical`

- **1.1.2 UML 101** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-1_OOP_design_Classic_or_classical`

- **1.1.3 Explaining each piece of the class diagram** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-1_OOP_design_Classic_or_classical`

- **1.1.4 The implementation phase** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-1_OOP_design_Classic_or_classical`

- **1.2.0 Introduction (사용자 추가)** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-2_Sources_of_complexity`

- **1.2.1 Many relations between classes** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-2_Sources_of_complexity`

- **1.2.2 Unpredictable code behavior** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-2_Sources_of_complexity`

- **1.2.3 Not trivial data serialization** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-2_Sources_of_complexity`

- **1.2.4 Complex class hierarchies** (node4)
  - 경로: `Part_1_Flexibility/1_Complexity_of_object-oriented_programming/1-2_Sources_of_complexity`

- **6.2.0 Introduction (사용자 추가)** (node4)
  - 경로: `Part_1_Flexibility/6_Unit_tests/6-2_Unit_tests_for_data_manipulation_code`

- **6.2.1 The tree of function calls** (node4)
  - 경로: `Part_1_Flexibility/6_Unit_tests/6-2_Unit_tests_for_data_manipulation_code`

- **6.2.2 Unit tests for functions down the tree** (node4)
  - 경로: `Part_1_Flexibility/6_Unit_tests/6-2_Unit_tests_for_data_manipulation_code`

- **6.2.3 Unit tests for nodes in the tree** (node4)
  - 경로: `Part_1_Flexibility/6_Unit_tests/6-2_Unit_tests_for_data_manipulation_code`

- **9.3.0 Introduction (사용자 추가)** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-3_Persistent_data_structures_libraries`

- **9.3.1 Persistent data structures in Java** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-3_Persistent_data_structures_libraries`

- **9.3.2 Persistent data structures in JavaScript** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-3_Persistent_data_structures_libraries`

- **9.4.0 Introduction (사용자 추가)** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-4_Persistent_data_structures_in_action`

- **9.4.1 Writing queries with persistent data structures** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-4_Persistent_data_structures_in_action`

- **9.4.2 Writing mutations with persistent data structures** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-4_Persistent_data_structures_in_action`

- **9.4.3 Serialization and deserialization** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-4_Persistent_data_structures_in_action`

- **9.4.4 Structural diff** (node4)
  - 경로: `Part_2_Scalability/9_Persistent_data_structures/9-4_Persistent_data_structures_in_action`

- **A.1.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-1_Principle_1_Separate_code_from_data`

- **A.1.1 Illustration of Principle #1** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-1_Principle_1_Separate_code_from_data`

- **A.1.2 Benefits of Principle #1** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-1_Principle_1_Separate_code_from_data`

- **A.1.3 Cost for Principle #1** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-1_Principle_1_Separate_code_from_data`

- **A.1.4 Summary of Principle #1** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-1_Principle_1_Separate_code_from_data`

- **A.2.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-2_Principle_2_Represent_data_with_generic_data_structures`

- **A.2.1 Illustration of Principle #2** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-2_Principle_2_Represent_data_with_generic_data_structures`

- **A.2.2 Benefits of Principle #2** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-2_Principle_2_Represent_data_with_generic_data_structures`

- **A.2.3 Cost for Principle #2** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-2_Principle_2_Represent_data_with_generic_data_structures`

- **A.2.4 Summary of Principle #2** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-2_Principle_2_Represent_data_with_generic_data_structures`

- **A.3.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-3_Principle_3_Data_is_immutable`

- **A.3.1 Illustration of Principle #3** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-3_Principle_3_Data_is_immutable`

- **A.3.2 Benefits of Principle #3** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-3_Principle_3_Data_is_immutable`

- **A.3.3 Cost for Principle #3** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-3_Principle_3_Data_is_immutable`

- **A.3.4 Summary of Principle #3** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-3_Principle_3_Data_is_immutable`

- **A.4.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-4_Principle_4_Separate_data_schema_from_data_representation`

- **A.4.1 Illustration of Principle #4** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-4_Principle_4_Separate_data_schema_from_data_representation`

- **A.4.2 Benefits of Principle #4** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-4_Principle_4_Separate_data_schema_from_data_representation`

- **A.4.3 Cost for Principle #4** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-4_Principle_4_Separate_data_schema_from_data_representation`

- **A.4.4 Summary of Principle #4** (node4)
  - 경로: `Appendices/Appendix_A_Principles_of_data-oriented_programming/A-4_Principle_4_Separate_data_schema_from_data_representation`

- **B.1.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-1_Dynamic_getters_for_string_maps`

- **B.1.1 Accessing non-nested map fields with dynamic getters** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-1_Dynamic_getters_for_string_maps`

- **B.1.2 Accessing nested map fields with dynamic getters** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-1_Dynamic_getters_for_string_maps`

- **B.2.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-2_Value_getters_for_maps`

- **B.2.1 Accessing non-nested map fields with value getters** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-2_Value_getters_for_maps`

- **B.2.2 Accessing nested map fields with value getters** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-2_Value_getters_for_maps`

- **B.3.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-3_Typed_getters_for_maps`

- **B.3.1 Accessing non-nested map fields with typed getters** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-3_Typed_getters_for_maps`

- **B.3.2 Accessing nested map fields with typed getters** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-3_Typed_getters_for_maps`

- **B.4.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-4_Generic_access_to_class_members`

- **B.4.1 Generic access to non-nested class members** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-4_Generic_access_to_class_members`

- **B.4.2 Generic access to nested class members** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-4_Generic_access_to_class_members`

- **B.4.3 Automatic JSON serialization of objects** (node4)
  - 경로: `Appendices/Appendix_B_Generic_data_access_in_statically-typed_languages/B-4_Generic_access_to_class_members`

- **C.1.1 1958: Lisp** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.1.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.1.2 1981: Values and objects** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.1.3 2000: Ideal hash trees** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.1.4 2006: Out of the Tar Pit** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.1.5 2007: Clojure** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.1.6 2009: Immutability for all** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-1_Time_line`

- **C.2.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-2_DOP_principles_as_best_practices`

- **C.2.1 Principle #1: Separate code from data** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-2_DOP_principles_as_best_practices`

- **C.2.2 Principle #2: Represent data with generic data structures** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-2_DOP_principles_as_best_practices`

- **C.2.3 Principle #3: Data is immutable** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-2_DOP_principles_as_best_practices`

- **C.2.4 Principle #4: Separate data schema from data representation** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-2_DOP_principles_as_best_practices`

- **C.3.0 Introduction (사용자 추가)** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-3_DOP_and_other_data-related_paradigms`

- **C.3.1 Data-oriented design** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-3_DOP_and_other_data-related_paradigms`

- **C.3.2 Data-driven programming** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-3_DOP_and_other_data-related_paradigms`

- **C.3.3 Data-oriented programming (DOP)** (node4)
  - 경로: `Appendices/Appendix_C_Data-oriented_programming_A_link_in_the_chain_of_programming_paradigm/C-3_DOP_and_other_data-related_paradigms`

