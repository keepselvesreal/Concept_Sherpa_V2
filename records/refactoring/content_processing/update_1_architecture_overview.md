# ContentProcessingStage 아키텍처 개요 (업데이트 1)

## 수정 내용 요약

### 1. 입력 데이터 방식 변경
- **기존**: `book_folder_path` → 파일시스템 스캔 기반
- **수정**: `prev_result` → 메모리 데이터 기반 (`process_result.json` 구조 활용)

### 2. 처리 흐름 최적화
- **기존**: 파일 기반 순차 처리
- **수정**: 메모리 기반 + 공통 저장 로직 통합

### 3. process_single_document 효율성 개선
- 모든 노드에서 추출 결과 먼저 저장
- 파일 읽기 → 업데이트 → 마킹 추가 → 저장의 공통 패턴 적용
- update_current_extraction_section에서 명시적 두 값 반환

## 수정된 전체 아키텍처

### 1. 시스템 구성도
```
ContentProcessingStage (메모리 기반)
├── 메모리 데이터 로딩 및 정렬 (load_and_sort_documents)
├── 그룹별 병렬 처리
├── 단일 문서 처리 (process_single_document)
│   ├── 추출 작업 (generate_extract_section)
│   ├── 추출 결과 저장 (save_extraction_result) - 모든 노드 공통
│   ├── [비리프 노드만] 현재 노드 업데이트 (update_current_extraction_section)
│   └── [비리프 노드만] 구성 노드 업데이트 (update_composition_extraction_sections)
└── 공통 업데이트 저장 로직 (save_updated_content_with_marking)
```

### 2. 처리 흐름 다이어그램
```
prev_result (메모리 데이터)
   ↓
메모리에서 unified_documents 추출
   ↓
문서 정렬 (리프 노드 → 비리프 노드(level 내림차순))
   ↓
그룹별 처리
   ├── 모든 노드: 추출 작업 → 사용자 지정 경로에 저장
   └── 비리프 노드: 파일에서 읽기 → 업데이트 → 마킹 추가 → 저장
   ↓
load_and_sort_result.json 생성 및 성공 결과 반환
```

### 3. 핵심 변경점

#### 3.1 메모리 기반 입력 처리
```python
async def process(self, prev_result: Dict) -> Dict[str, Any]:
    """
    Args:
        prev_result: {
            "documents": {
                "data": {
                    "unified_documents": List[Dict]  # process_result.json 구조
                }
            }
        }
    """
    unified_documents = prev_result["documents"]["data"]["unified_documents"]
    sorted_groups = await self.load_and_sort_documents(unified_documents)
    # ...
```

#### 3.2 통합된 처리 로직
```python
async def process_single_document(self, doc: Dict, user_output_path: str) -> Dict:
    # 1. 모든 노드에서 추출 결과 먼저 저장
    extraction_result = await self.generate_extract_section(doc)
    await self.save_extraction_result(doc, extraction_result, user_output_path)
    
    # 2. 비리프 노드만 업데이트 과정 진행
    if doc.get('composition_files'):
        updated_current_extraction, used_composition_extractions = await self.update_current_extraction_section(doc, user_output_path)
        await self.update_composition_extraction_sections(doc, updated_current_extraction, used_composition_extractions, user_output_path)
```

#### 3.3 공통 저장 로직 통합
```python
async def save_updated_content_with_marking(self, file_path: str, updated_extraction: Dict, status_mark: str):
    """파일 읽기 → 마킹 추가 → 업데이트된 내용 저장 (공통 패턴)"""
    # 1. 파일에서 기존 내용 읽기
    # 2. 추출 섹션 업데이트
    # 3. 상태 마킹 추가
    # 4. 파일 저장
```

## 성능 및 확장성 고려사항

### 4.1 메모리 기반 처리 장점
- 파일 I/O 최소화로 성능 향상
- 중간 결과 JSON 저장으로 디버깅 용이
- 파이프라인 간 데이터 전달 효율화

### 4.2 공통 로직 통합 장점
- 코드 중복 제거 및 유지보수성 향상
- 일관성 있는 오류 처리 및 로깅
- 확장 시 공통 로직만 수정으로 변경 영향 최소화

### 4.3 명시적 반환값 장점
- 데이터 흐름 명확화
- 중복 작업 제거
- 디버깅 및 테스트 용이성

## 입출력 정의

### 5.1 수정된 입력 규격
- **prev_result** (Dict): 이전 단계 결과 (process_result.json 구조)
- **user_output_path** (str): 사용자 지정 저장 경로

### 5.2 수정된 출력 규격
```python
{
    "success": bool,
    "processed_documents": List[Dict],        # 처리된 문서 정보
    "load_and_sort_result_path": str,        # 정렬 결과 JSON 경로
    "error": Optional[str]
}
```

### 5.3 중간 데이터 구조 (변경사항 없음)
- 문서 데이터 구조 및 추출 결과 구조는 기존과 동일
- 추가: 사용자 지정 경로를 통한 파일 저장 위치 관리