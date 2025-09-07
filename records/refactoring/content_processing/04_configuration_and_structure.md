# 설정 및 파일 구조 가이드

## 1. 파일 구조 및 경로 설정

### 1.1 디렉터리 구조
```
refactoring/src/stages/
├── content_processing_stage.py          # 메인 구현 파일
└── content_processing_utils.py          # 전용 유틸리티 함수들
```

**구조 선택 이유**:
- `stages/` 폴더: 파이프라인 단계들의 논리적 그룹핑
- 응집력: content_processing 관련 모든 코드가 한 곳에 위치
- 확장성: 다른 단계들과 일관성 있는 구조

### 1.2 import 경로 및 의존성

#### 1.2.1 상대/절대 경로 규칙
```python
# content_processing_stage.py
from .content_processing_utils import (
    extract_level_from_filename,
    parse_extraction_response,
    format_composition_info,
    clean_section_content,
    find_matching_document
)

# 외부 모듈 import
from ..services.ai_service_v4 import AIService
import asyncio
import json
import logging
import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Optional, Any
```

#### 1.2.2 외부 모듈 import
```python
# 표준 라이브러리
import asyncio
import json
import logging
import os
import re
import glob
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any

# 프로젝트 내 모듈
from ..services.ai_service_v4 import AIService
```

#### 1.2.3 순환 의존성 방지
- 유틸리티 함수들을 별도 파일로 분리
- 의존성 방향: stage → utils, stage → services
- services와 utils 간 직접 의존성 없음

## 2. 설정 파일 구성

### 2.1 ai_config.yaml 수정사항

**기존 구조 유지하며 content_processing 섹션 추가**:
```yaml
# 기본 AI 설정 (모든 단계에서 fallback)
default_ai:
  provider: "gemini" 
  model: "gemini-2.0-flash-lite"
  temperature: 0.1
  max_tokens: 8192
  api_key: null  # 환경변수 GEMINI_API_KEY 사용

# 단계별 AI 설정
stage_specific_ai:
  workspace_preparation:
    chapter_toc_extraction:
      provider: "gemini"
      model: "gemini-2.0-flash-lite"
      temperature: 0.1
      max_tokens: 8192
    
    chapter_content_extraction:
      provider: "gemini"
      model: "gemini-2.0-flash-lite"
      temperature: 0.1
      max_tokens: 8192
    
  information_integration:
    detect_section_content:
      provider: "gemini"
      model: "gemini-2.0-flash-lite"
      temperature: 0.1
      max_tokens: 8192
      
    extract_section_content:
      provider: "gemini"
      model: "gemini-2.0-flash-lite"
      temperature: 0.1
      max_tokens: 8192
    
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
    
  toc_generation:
    provider: "gemini"
    model: "gemini-1.5-flash"
    temperature: 0.1
    max_tokens: 4096
```

### 2.2 pipeline_config.yaml 수정사항

**기존 구조 유지하며 content_processing 섹션 수정**:
```yaml
# 테스트 모드 설정
test_mode:
  enabled: false
  selected_chapters: []
  debug_verbose: true
  skip_on_error: false

# 1단계: 기본 작업 준비
workspace_preparation:
  toc_extraction:
    method: "PyMuPDF"
    hierarchy_enabled: true
  
  folder_structure:
    base_path: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output"
    chapter_naming: "normalized_title"
    create_subdirs: true
  
  ai_analysis:
    enabled: true
    provider: "gemini"
    fallback_on_failure: true

# 2단계: 통합 노드 정보 문서 생성
information_integration:
  sequential_processing: true
  continue_on_chapter_failure: true
  node_document_generation:
    enabled: true
  content_analysis:
    enabled: true

# 3단계: 가공 작업 (핵심 단계) - 수정됨
content_processing:
  processing_mode: "unified_type_processing"  # unified_type_processing | individual_type_processing
  max_parallel: 4
  parallel_processing: true

# 4단계: 목차 생성
toc_generation:
  enhanced_toc:
    enabled: true
    combine_extracts: true
  output_format: "markdown"

# 전역 설정
global:
  output_base_dir: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output"
  logs_base_dir: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/logs"
  temp_cleanup: true
```

## 3. 통합 문서 파일 포맷

### 3.1 파일 구조 파싱 규칙

#### 3.1.1 섹션 구분자
```
# 속성
---
process_status: false

# 추출
---
[추출된 내용 또는 비어있음]

# 내용
---
[원본 문서 내용]

# 구성
---
[구성 노드 파일명들 또는 비어있음]
```

#### 3.1.2 정규표현식 패턴
```python
# 섹션 분리 정규표현식
extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# 내용\n---|$)', content, re.DOTALL)
content_match = re.search(r'# 내용\n---\n(.*?)(?=\n# 구성\n---|$)', content, re.DOTALL)  
composition_match = re.search(r'# 구성\n---\n(.*?)$', content, re.DOTALL)

# level 추출 정규표현식 
level_match = re.search(r'lev(\d+)', filename)
if level_match:
    level = int(level_match.group(1))
```

#### 3.1.3 level 추출 규칙
- 파일명 패턴: `{id}_lev{level}_{title}_info.md`
- 예시: `16_lev2_1.1_OOP_design_Classic_or_classical_info.md` → level = 2

### 3.2 상태 마킹 규칙

#### 3.2.1 삽입 위치
```
# 추출
---
<상태마킹>
[추출된 내용]

# 내용
---
```

**정확한 위치**: `# 추출\n---\n` 바로 다음에 줄바꿈 없이 삽입

#### 3.2.2 마킹 형식
- 추출 완료: 마킹 없음 (추출된 내용만 삽입)
- 구성 노드 반영 완료: `<구성 노드 반영 완료>`
- 부모 노드 반영 완료: `<부모 노드 반영 완료>`

#### 3.2.3 내용 삽입 규칙
```python
# 상태 마킹 삽입 (줄바꿈 없이)
content = re.sub(
    r'(# 추출\n---\n)',
    f'\\1{status_mark}\n',
    content
)

# 추출 내용 삽입 (마킹 다음 줄)
pattern = r'(# 추출\n---\n)(<[^>]+>\n)?(.*?)(?=\n# 내용\n---|$)'
def replacement(match):
    header = match.group(1)
    status_mark = match.group(2) if match.group(2) else ""
    return f"{header}{status_mark}{new_content}"
```

## 4. 출력 파일 포맷

### 4.1 enhanced_toc.md 생성 규칙

#### 4.1.1 level별 헤더 개수
```python
# level에 따른 헤더 생성
header_prefix = "#" * toc_item['level']
header = f"{header_prefix} {toc_item['title']}"

# 예시:
# level 1: # 1 Complexity of object-oriented programming
# level 2: ## 1.1 OOP design: Classic or classical?
# level 3: ### 1.1.1 The design phase
```

#### 4.1.2 헤더-내용 삽입 방식 (줄바꿈 없이)
```python
# 헤더 바로 밑에 내용 삽입
if extraction_content.strip():
    enhanced_lines.append(f"{header}\n{extraction_content}")
else:
    enhanced_lines.append(f"{header}\n[추출 내용 없음]")
```

#### 4.1.3 섹션 간 구분 (빈 줄 2개)
```python
# 각 섹션 사이에 빈 줄 2개 추가 (가독성)
enhanced_lines.append("")
enhanced_lines.append("")
```

### 4.2 파일명 생성 규칙

#### 4.2.1 출력 디렉터리 설정
```python
# 입력 챕터와 동일한 디렉터리에 생성
output_file = f"{book_folder_path}/{chapter_name}_enhanced_toc.md"
```

#### 4.2.2 네이밍 컨벤션
- 패턴: `{chapter_name}_enhanced_toc.md`
- 예시: `1_Complexity_of_object_oriented_programming_enhanced_toc.md`

#### 4.2.3 충돌 방지 전략
```python
# 파일이 이미 존재하는 경우 덮어쓰기
# 백업이 필요한 경우 타임스탬프 추가
if os.path.exists(output_file):
    backup_file = f"{output_file}.backup.{int(time.time())}"
    shutil.copy2(output_file, backup_file)
    logging.info(f"기존 파일 백업: {backup_file}")
```

## 5. 로깅 전략

### 5.1 로그 레벨 및 포맷
```python
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_processing.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('ContentProcessingStage')
```

### 5.2 주요 체크포인트
```python
# 진행 단계 로깅
logger.info(f"🚀 ContentProcessingStage 시작: {book_folder_path}")
logger.info(f"📊 총 {len(sorted_groups)}개 그룹으로 정렬됨")
logger.info(f"🔄 그룹 {i+1}/{len(sorted_groups)} 처리 시작: {len(group)}개 문서")

# 문서별 처리 로깅
logger.info(f"📄 문서 처리 시작: {doc.get('title', 'N/A')}")
logger.info(f"🤖 AI 추출 작업 시작...")
logger.info(f"✅ 추출 작업 완료")
logger.info(f"💾 파일 업데이트 완료")

# API 호출 추적
logger.info(f"📊 API 호출 횟수: {self.api_calls_counter}")

# 오류 및 경고
logger.warning(f"⚠️ AI 요청 실패 (시도 {attempt + 1}/{max_retries}): {e}")
logger.error(f"❌ 문서 처리 실패: {doc_path} - {e}")

# 성공 완료
logger.info(f"🎉 ContentProcessingStage 완료 - 처리된 문서: {processed_count}개")
```

### 5.3 디버그 정보 수집
```python
# 디버그 레벨에서만 상세 정보
logger.debug(f"📋 문서 파싱 결과: {doc_data}")
logger.debug(f"🔍 추출 섹션 길이: {len(extraction_content)} 문자")
logger.debug(f"📝 구성 노드 파일들: {composition_files}")

# 성능 측정
import time
start_time = time.time()
# ... 처리 로직 ...
processing_time = time.time() - start_time
logger.info(f"⏱️ 처리 시간: {processing_time:.2f}초")
```

### 5.4 오류 복구 로깅
```python
# 재시도 로직 로깅
for attempt in range(max_retries):
    try:
        response = await self.ai_service.query_single_request(...)
        logger.info(f"✅ AI 요청 성공 (시도 {attempt + 1})")
        break
    except Exception as e:
        if attempt == max_retries - 1:
            logger.error(f"❌ AI 요청 최종 실패: {e}")
            raise e
        else:
            logger.warning(f"⚠️ AI 요청 실패, 재시도 {attempt + 1}/{max_retries}: {e}")
            await asyncio.sleep(1)
```