# 데이터 구조 명세서

## 파일 명명 규칙
- **책 목차**: `{책_제목}_ToC.md`
- **장 목차**: `{장_제목}_ToC.md` (기존 _toc → _ToC 수정 예정)
- **장 내용**: `{장_제목}_content.md`
- **통합 문서**: `{id}_{level}_{normalized_section}_info.md`

## 폴더 구조
```
book_folder/
├── {책_제목}_ToC.md                    # 책 전체 목차
├── 1_Chapter_Name/                     # 장 폴더 (번호_정규화된제목)
│   ├── 1_Chapter_Name_content.md       # 장 전체 내용
│   ├── 1_Chapter_Name_ToC.md           # 장 목차 (섹션 정보)
│   └── unified_info_docs/
│       ├── 15_lev1_section_info.md     # 레벨1 섹션 통합 문서
│       ├── 16_lev2_subsection_info.md  # 레벨2 섹션 통합 문서
│       └── ...
└── 2_Another_Chapter/
    └── ...
```

## 정규화 규칙
```python
from utils.text_utils import normalize_title

# 예시
original = "1.1 OOP design: Classic or classical?"
normalized = normalize_title(original)
# 결과: "1_1_OOP_design_Classic_or_classical"
```

## 입력 데이터 구조
```python
# 함수 호출
async def answer_query(
    user_query: str,                              # "객체지향의 복잡성은?"
    book_path: str,                               # "/path/to/Data_Oriented_Programming"
    response_mode: str = "chapter_based_response" # "chapter_based_response" | "section_based_response"
) -> Dict[str, Any]
```

## 반환 데이터 구조
```python
{
    'user_query': str,                           # 사용자 질의
    'response_mode': str,                        # 처리 모드
    'selected_chapter_titles': List[str],        # AI가 선택한 장 제목들
    'chapter_based_answers': List[Dict] | None,  # 장 기반 응답 (해당 모드일 때만)
    'section_based_answers': List[Dict] | None,  # 섹션 기반 응답 (해당 모드일 때만)
    'synthesized_answer': str                    # 최종 종합 답변
}
```

## chapter_based_answers 구조
```python
[
    {
        'chapter_title': str,      # 장 제목
        'chapter_answer': str,     # 해당 장 기반 생성된 답변
        'status': str             # 'success' | 'error'
    },
    ...
]
```

## section_based_answers 구조  
```python
[
    {
        'chapter_title': str,        # 장 제목
        'section_title': str,        # 섹션 제목
        'section_answer': str,       # 해당 섹션 기반 생성된 답변
        'unified_doc_path': str,     # 사용된 통합 문서 경로
        'status': str               # 'success' | 'error'
    },
    ...
]
```

## 내부 데이터 로딩 구조
```python
# WorkspaceDataLoader가 반환하는 구조
{
    'book_toc_data': Dict,           # 파싱된 책 목차 정보
    'chapters_data': Dict[str, Dict], # 장별 데이터
    'workspace_path': str            # workspace 경로
}

# chapters_data 내부 구조
{
    'chapter_folder_name': {
        'folder_path': Path,                    # 장 폴더 경로
        'chapter_toc': Dict,                    # 장 목차 데이터
        'unified_info_docs_path': Path          # unified_info_docs 폴더 경로
    }
}
```