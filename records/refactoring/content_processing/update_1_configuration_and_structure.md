# 설정 및 파일 구조 가이드 (업데이트 1)

## 수정된 파일 구조 및 경로 설정

### 1.1 디렉터리 구조 (변경사항 없음)
```
refactoring/src/stages/
├── content_processing_stage.py          # 메인 구현 파일 (메모리 기반으로 수정)
└── content_processing_utils.py          # 전용 유틸리티 함수들 (파일 처리 함수 추가)
```

### 1.2 import 경로 및 의존성 (추가 사항)

#### 1.2.1 추가된 import 구문
```python
# content_processing_stage.py
from .content_processing_utils import (
    extract_level_from_filename,
    parse_extraction_response,
    format_composition_info,
    clean_section_content,
    find_matching_document,
    # 새로 추가된 유틸리티 함수들
    extract_title_from_content,
    extract_content_section_from_full_content,
    parse_composition_files_from_content
)

# 추가된 표준 라이브러리
import json
import datetime
from typing import Tuple  # 명시적 반환값 타입을 위해
```

## 수정된 설정 파일 구성

### 2.1 ai_config.yaml 수정사항 (변경사항 없음)
기존 content_processing 섹션 그대로 유지:
```yaml
content_processing:
  extract_section_information:
    provider: "gemini"
    model: "gemini-2.0-flash-lite"
    temperature: 0.0
    max_tokens: 8192
    
  update_section_information:
    provider: "gemini"
    model: "gemini-2.0-flash-lite"
    temperature: 0.0
    max_tokens: 8192
```

### 2.2 pipeline_config.yaml 수정사항

#### 2.2.1 수정된 content_processing 섹션
```yaml
# 3단계: 가공 작업 (핵심 단계) - 메모리 기반으로 수정
content_processing:
  processing_mode: "memory_based_processing"  # 고정값
  max_parallel: 4
  parallel_processing: true
  
  # 새로 추가된 설정
  memory_processing:
    enabled: true
    cache_intermediate_results: true
    save_load_and_sort_result: true
    
  # 파일 저장 설정
  output_settings:
    create_subdirectories: true
    preserve_file_structure: true
    backup_existing_files: false
```

#### 2.2.2 추가된 경로 설정
```yaml
# 전역 설정에 메모리 기반 처리 경로 추가
global:
  output_base_dir: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output"
  logs_base_dir: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/logs"
  temp_cleanup: true
  
  # 새로 추가된 설정
  intermediate_results_dir: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/content_processing"
  memory_cache_enabled: true
```

## 수정된 데이터 입력/출력 구조

### 3.1 입력 데이터 구조 (대폭 변경)

#### 3.1.1 기존 파일 기반 → 메모리 기반으로 변경
```python
# 기존: book_folder_path (str)
# 수정: prev_result (Dict)

input_structure = {
    "documents": {
        "success": True,
        "data": {
            "processed_chapters": [
                {
                    "chapter_title": "1 Complexity of object- oriented programming",
                    "normalized_title": "1_Complexity_of_object_oriented_programming"
                }
            ],
            "unified_documents": [
                {
                    "file_name": "1_Complexity_of_object_oriented_programming/unified_info_docs/17_lev3_1.1.1_The_design_phase_info.md",
                    "content": "# 속성\n---\nprocess_status: false\n\n# 추출\n---\n\n# 내용\n---\n### 1.1.1 The design phase\n..."
                }
            ]
        }
    }
}
```

#### 3.1.2 메모리 데이터 파싱 규칙
```python
# unified_documents 배열의 각 항목에서 추출
document_info = {
    "file_name": str,     # 파일 경로 정보
    "content": str        # 전체 통합 문서 내용 (# 속성, # 추출, # 내용, # 구성 포함)
}

# content 내에서 섹션별 파싱
sections = {
    "속성": "process_status: false",
    "추출": "",  # 초기에는 비어있음
    "내용": "실제 문서 내용...",
    "구성": "구성 노드 파일명들 또는 비어있음"
}
```

### 3.2 출력 데이터 구조 (수정됨)

#### 3.2.1 수정된 메인 반환값
```python
output_structure = {
    "success": bool,
    "processed_documents": List[Dict],        # 처리된 문서 정보 리스트
    "load_and_sort_result_path": str,        # 정렬 결과 JSON 파일 경로
    "user_output_path": str,                 # 사용자 지정 저장 경로
    "api_calls_count": int,                  # API 호출 횟수
    "processing_time": float,                # 처리 시간 (초)
    "error": Optional[str]
}
```

#### 3.2.2 load_and_sort_result.json 구조
```json
{
  "method": "load_and_sort_documents",
  "input_source": "memory_data",
  "generation_time": "Fri Sep 12 17:12:51 KST 2025",
  "result": {
    "output": {
      "chapters": [
        {
          "leaf_nodes": [
            {
              "title": "17 lev3 1.1.1 The design phase",
              "level": 3,
              "composition_files": [],
              "file_name": "1_Complexity_of_object_oriented_programming/unified_info_docs/17_lev3_1.1.1_The_design_phase_info.md"
            }
          ],
          "non_leaf_groups": [
            [
              {
                "title": "16 lev2 1.1 OOP design Classic or classical",
                "level": 2,
                "composition_files": ["17_lev3_1.1.1_The_design_phase_info.md", "18_lev3_1.1.2_UML_101_info.md"]
              }
            ]
          ]
        }
      ]
    }
  }
}
```

### 3.3 사용자 지정 경로 파일 구조

#### 3.3.1 저장된 통합 문서 포맷 (수정됨)
```
user_output_path/
└── 1_Complexity_of_object_oriented_programming/
    └── unified_info_docs/
        ├── 17_lev3_1.1.1_The_design_phase_info.md
        ├── 18_lev3_1.1.2_UML_101_info.md
        └── 16_lev2_1.1_OOP_design_Classic_or_classical_info.md
```

#### 3.3.2 각 파일 내부 구조 (상태 마킹 포함)
```markdown
# 속성
---
process_status: true

# 추출
---
<구성 노드 반영 완료>
## 핵심 내용
[추출된 핵심 내용]

## 상세 핵심 내용
[추출된 상세 핵심 내용]

## 상세 정보
[추출된 상세 정보]

## 주요 화제
[추출된 주요 화제]

## 부차 화제
[추출된 부차 화제]

# 내용
---
[원본 문서 내용]

# 구성
---
[구성 노드 파일명들]
```

## 수정된 유틸리티 함수들

### 4.1 새로 추가된 유틸리티 함수들

#### 4.1.1 메모리 데이터 처리 함수들
```python
def extract_title_from_content(content: str) -> str:
    """콘텐츠에서 제목 추출 (# 내용 섹션의 첫 번째 헤더에서)"""
    content_match = re.search(r'# 내용\n---\n(.*?)(?=\n---|\n#|$)', content, re.DOTALL)
    if content_match:
        lines = content_match.group(1).split('\n')
        for line in lines:
            if line.strip() and line.startswith('#'):
                return line.replace('#', '').strip()
    return "Unknown Title"

def extract_content_section_from_full_content(full_content: str) -> str:
    """전체 내용에서 # 내용 섹션만 추출"""
    content_match = re.search(r'# 내용\n---\n(.*?)(?=\n# 구성\n---|$)', full_content, re.DOTALL)
    return content_match.group(1).strip() if content_match else ""

def parse_composition_files_from_content(content: str) -> List[str]:
    """전체 내용에서 구성 파일들 추출"""
    composition_match = re.search(r'# 구성\n---\n(.*?)$', content, re.DOTALL)
    if composition_match:
        composition_section = composition_match.group(1).strip()
        if composition_section and composition_section != '---':
            return [line.strip() for line in composition_section.split('\n') 
                   if line.strip() and not line.startswith('---')]
    return []
```

#### 4.1.2 파일 처리 함수들
```python
def update_extraction_section_in_content(original_content: str, new_extraction_content: str) -> str:
    """메모리 내용에서 추출 섹션 업데이트"""
    pattern = r'(# 추출\n---\n)(<[^>]+>\n)?(.*?)(?=\n# 내용\n---|$)'
    
    def replacement(match):
        header = match.group(1)  # # 추출\n---\n
        status_mark = match.group(2) if match.group(2) else ""  # 기존 상태 마킹
        return f"{header}{status_mark}{new_extraction_content}"
    
    return re.sub(pattern, replacement, original_content, flags=re.DOTALL)

def add_update_status_mark_to_content(content: str, status_mark: str) -> str:
    """메모리 내용에 상태 마킹 추가"""
    pattern = r'(# 추출\n---\n)(?!<)'  # 이미 마킹이 없는 경우만
    replacement = f'\\1{status_mark}\n'
    return re.sub(pattern, replacement, content)
```

### 4.2 수정된 기존 함수들

#### 4.2.1 extract_level_from_filename() 확장
```python
def extract_level_from_filename(filename: str) -> int:
    """파일명에서 level 추출 (경로 포함 파일명 지원)"""
    # 경로에서 파일명만 추출
    base_filename = os.path.basename(filename)
    level_match = re.search(r'lev(\d+)', base_filename)
    return int(level_match.group(1)) if level_match else 0
```

#### 4.2.2 확장된 parse_extraction_response()
```python
def parse_extraction_response(response: str) -> Dict[str, str]:
    """AI 응답을 5개 섹션으로 파싱 (engines_v5.py와 동일)"""
    # 기존 로직 그대로 유지
    sections = {
        'core_content': '',
        'detailed_core_content': '',
        'detailed_content': '',
        'main_topics': '',
        'sub_topics': ''
    }
    # ... 파싱 로직
    return sections
```

## 로깅 전략 (업데이트)

### 5.1 메모리 기반 처리 로깅
```python
# 메모리 데이터 로딩
logger.info(f"📊 메모리에서 {len(unified_documents)}개 문서 로드")
logger.info(f"🔄 문서 정렬 완료: 리프 노드 {len(leaf_nodes)}개, 비리프 그룹 {len(non_leaf_groups)}개")

# 사용자 지정 경로 저장
logger.info(f"📁 사용자 지정 경로: {user_output_path}")
logger.info(f"💾 추출 결과 저장: {output_file_path}")

# 공통 로직 처리
logger.info(f"🔄 파일 기반 업데이트: {file_path}")
logger.info(f"✅ 상태 마킹 추가: {status_mark}")
```

### 5.2 성능 추적 로깅
```python
# 처리 시간 및 효율성
logger.info(f"⏱️ 메모리 처리 시간: {memory_processing_time:.2f}초")
logger.info(f"💾 파일 저장 시간: {file_save_time:.2f}초")
logger.info(f"🔄 업데이트 처리 시간: {update_processing_time:.2f}초")

# API 호출 통계
logger.info(f"📊 총 API 호출 횟수: {self.api_calls_counter}")
logger.info(f"⚡ 평균 응답 시간: {average_response_time:.2f}초")
```

### 5.3 오류 및 복구 로깅
```python
# 메모리 데이터 처리 오류
logger.error(f"❌ 메모리 데이터 파싱 실패: {e}")
logger.warning(f"⚠️ 파일 누락, 스킵 처리: {missing_file}")

# 파일 저장 오류
logger.error(f"❌ 파일 저장 실패: {output_path} - {e}")
logger.info(f"🔄 재시도 중: {retry_count}/{max_retries}")

# 복구 처리
logger.info(f"✅ 복구 완료: {recovered_file}")
logger.info(f"📋 총 처리 결과: 성공 {success_count}개, 실패 {failure_count}개")
```

## 환경 변수 및 설정

### 6.1 추가된 환경 변수
```bash
# 메모리 기반 처리 설정
CONTENT_PROCESSING_MEMORY_MODE=true
CONTENT_PROCESSING_CACHE_ENABLED=true

# 파일 저장 설정
CONTENT_PROCESSING_OUTPUT_BASE_DIR="/path/to/output"
CONTENT_PROCESSING_BACKUP_ENABLED=false

# 성능 튜닝
CONTENT_PROCESSING_MAX_PARALLEL=4
CONTENT_PROCESSING_MEMORY_CACHE_SIZE=100MB
```

### 6.2 런타임 설정 검증
```python
def validate_runtime_config(config: Dict) -> bool:
    """런타임 설정 유효성 검증"""
    required_paths = [
        config.get('global', {}).get('intermediate_results_dir'),
        config.get('global', {}).get('output_base_dir')
    ]
    
    for path in required_paths:
        if path and not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logger.info(f"📁 디렉터리 생성: {path}")
    
    return True
```