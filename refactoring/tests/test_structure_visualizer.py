# 생성 시간: Wed Sep 11 17:02:15 KST 2025
# 핵심 내용: Refactoring 프로젝트 테스트 구조 시각화
# 상세 내용:
#   - 테스트 파일과 직접 관련된 부분만 시각화 (fixtures, unit, integration, e2e)
#   - ContentProcessingStage 관련 테스트 파일 연관성 표시
# 상태: active

"""
📁 refactoring/tests/
├── 📄 conftest.py
│
├── 📁 unit/
│   ├── 📄 test_content_processing_stage_load_and_sort.py
│   │   └── TestContentProcessingStageLoadAndSort
│   │       ├── test_load_and_sort_documents_returns_chapter_groups() [unit, sociable]
│   │       ├── test_load_and_sort_documents_separates_leaf_and_nonleaf_nodes() [unit, sociable]
│   │       └── test_load_and_sort_documents_sorts_nonleaf_by_level_desc() [unit, sociable]
│   │
│   └── 📄 test_workspace_preparation.py
│       └── TestWorkspacePreparation
│
├── 📁 integration/
│   ├── 📄 test_integrated_node_generation_stage.py    # IntegratedNodeGenerationStage 통합 테스트
│   ├── 📄 test_claude_sdk_session_validation.py      # Claude SDK 세션 검증
│   └── 📄 test_gemini_api_multiturn_validation.py    # Gemini API 멀티턴 검증
│
├── 📁 e2e/
│   └── (비어있음)
│
└── 📁 fixtures/
    ├── 📄 content_processing_fixtures.py              # ContentProcessingStage 관련 픽스처
    │   └── integrated_node_generation_stage_data()    # 실제 데이터 픽스처 (44K tokens)
    ├── 📄 integrated_node_generation_fixtures.py     # IntegratedNodeGeneration 픽스처
    └── 📄 workspace_preparation_fixtures.py          # WorkspacePreparation 픽스처

🔗 ContentProcessingStage 관련 테스트 파일 연관성:
┌─────────────────────────────────────────────────────┐
│ 📄 ContentProcessingStage 관련 테스트 파일들          │
├─────────────────────────────────────────────────────┤
│ 🎯 Main (예정): test_content_processing_stage.py     │
│    └── TestContentProcessingStage                   │
│        └── test_generate_extract_section_success()  │
│            [sociable, expensive]                    │
│                                                     │
│ 🔍 Detailed (기존): test_content_processing_stage_load_and_sort.py │
│    └── TestContentProcessingStageLoadAndSort        │
│        └── load_and_sort_documents 메서드 상세 테스트 │
│                                                     │
│ 📦 Fixture: content_processing_fixtures.py          │
│    └── integrated_node_generation_stage_data()      │
└─────────────────────────────────────────────────────┘
"""