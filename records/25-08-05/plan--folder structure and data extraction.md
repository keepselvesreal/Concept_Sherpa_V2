Data-Oriented Programming 폴더 구조화 및 데이터 추출 계획                                              │ │
│ │                                                                                                        │ │
│ │ 목표                                                                                                   │ │
│ │                                                                                                        │ │
│ │ normalized_toc_with_node_types.md를 바탕으로 계층적 폴더 구조를 생성하고 leaf node들의 실제 내용을     │ │
│ │ 추출하여 저장                                                                                          │ │
│ │                                                                                                        │ │
│ │ 폴더 구조 계획                                                                                         │ │
│ │                                                                                                        │ │
│ │ Root Directory                                                                                         │ │
│ │                                                                                                        │ │
│ │ /home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented-Programming/                                    │ │
│ │                                                                                                        │ │
│ │ Internal Node → 폴더 생성                                                                              │ │
│ │                                                                                                        │ │
│ │ Data-Oriented-Programming/                                                                             │ │
│ │ ├── Front-Matter/                                                                                      │ │
│ │ ├── Part1-Flexibility/                                                                                 │ │
│ │ ├── Part2-Scalability/                                                                                 │ │
│ │ ├── Part3-Maintainability/                                                                             │ │
│ │ ├── Appendices/                                                                                        │ │
│ │ └── Index/                                                                                             │ │
│ │                                                                                                        │ │
│ │ Leaf Node → MD 파일 생성 (총 19개)                                                                     │ │
│ │                                                                                                        │ │
│ │ 1. Part1-Flexibility/ (6개 파일)                                                                       │ │
│ │   - ch1-0-introduction.md                                                                              │ │
│ │   - ch1-complexity-of-oop.md                                                                           │ │
│ │   - ch2-separation-between-code-and-data.md                                                            │ │
│ │   - ch3-basic-data-manipulation.md                                                                     │ │
│ │   - ch4-state-management.md                                                                            │ │
│ │   - ch5-basic-concurrency-control.md                                                                   │ │
│ │   - ch6-unit-tests.md                                                                                  │ │
│ │ 2. Part2-Scalability/ (6개 파일)                                                                       │ │
│ │   - ch2-0-introduction.md                                                                              │ │
│ │   - ch7-basic-data-validation.md                                                                       │ │
│ │   - ch8-advanced-concurrency-control.md                                                                │ │
│ │   - ch9-persistent-data-structures.md                                                                  │ │
│ │   - ch10-database-operations.md                                                                        │ │
│ │   - ch11-web-services.md                                                                               │ │
│ │ 3. Part3-Maintainability/ (5개 파일)                                                                   │ │
│ │   - ch3-0-introduction.md                                                                              │ │
│ │   - ch12-advanced-data-validation.md                                                                   │ │
│ │   - ch13-polymorphism.md                                                                               │ │
│ │   - ch14-advanced-data-manipulation.md                                                                 │ │
│ │   - ch15-debugging.md                                                                                  │ │
│ │ 4. Appendices/ (4개 파일)                                                                              │ │
│ │   - appendix-a-principles-of-dop.md                                                                    │ │
│ │   - appendix-b-generic-data-access.md                                                                  │ │
│ │   - appendix-c-programming-paradigms.md                                                                │ │
│ │   - appendix-d-lodash-reference.md                                                                     │ │
│ │                                                                                                        │ │
│ │ 데이터 추출 전략                                                                                       │ │
│ │                                                                                                        │ │
│ │ 기존 데이터 소스 활용                                                                                  │ │
│ │                                                                                                        │ │
│ │ - /Data-Oriented_Programming_Manning/ 폴더의 기존 original_text.md 파일들 사용                         │ │
│ │ - 15개 챕터의 원본 텍스트가 이미 추출되어 있음                                                         │ │
│ │                                                                                                        │ │
│ │ 누락된 내용 처리                                                                                       │ │
│ │                                                                                                        │ │
│ │ - Front Matter: PDF에서 직접 추출 필요                                                                 │ │
│ │ - Introduction 섹션들: 사용자가 추가한 항목들로 플레이스홀더 생성                                      │ │
│ │ - Appendices: PDF에서 직접 추출 필요                                                                   │ │
│ │ - Index: PDF에서 직접 추출 필요                                                                        │ │
│ │                                                                                                        │ │
│ │ 파일 구조                                                                                              │ │
│ │                                                                                                        │ │
│ │ 각 MD 파일은 다음 구조를 가질 예정:                                                                    │ │
│ │ # [Chapter Title]                                                                                      │ │
│ │                                                                                                        │ │
│ │ ## 목차                                                                                                │ │
│ │ - [TOC의 해당 섹션 내용]                                                                               │ │
│ │                                                                                                        │ │
│ │ ## 내용                                                                                                │ │
│ │ [실제 추출된 텍스트 내용]                                                                              │ │
│ │                                                                                                        │ │
│ │ ## 메타데이터                                                                                          │ │
│ │ - 파트: [Part 1/2/3]                                                                                   │ │
│ │ - 챕터 번호: [N]                                                                                       │ │
│ │ - 페이지 범위: [추출 시 확인]                                                                          │ │
│ │                                                                                                        │ │
│ │ 실행 단계                                                                                              │ │
│ │                                                                                                        │ │
│ │ 1. 루트 폴더 및 내부 구조 생성                                                                         │ │
│ │ 2. 기존 original_text.md 파일들을 새 구조로 복사 및 이름 변경                                          │ │
│ │ 3. 누락된 섹션들에 대한 플레이스홀더 파일 생성                                                         │ │
│ │ 4. 각 파일에 적절한 목차 정보 및 메타데이터 추가  