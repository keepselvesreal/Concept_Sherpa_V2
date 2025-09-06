# Neon PostgreSQL Vector Database Documentation

## 📊 데이터베이스 개요

**Knowledge Sherpa v2**는 Neon PostgreSQL + pgvector를 사용하여 Data-Oriented Programming 관련 지식을 벡터 형태로 저장하고 검색하는 시스템입니다.

### 📈 현재 데이터 통계
- **core_content**: 13개 항목 (핵심 내용)
- **detailed_content**: 11개 항목 (상세 분석) 
- **총 항목**: 24개
- **임베딩 차원**: 384차원 (sentence-transformers)

---

## 🗄️ 데이터베이스 스키마

### 1. core_content 테이블

핵심 내용을 저장하는 메인 테이블로, 상위 섹션(메타데이터 구조체)과 하위 섹션(원문)을 모두 포함합니다.

| 필드명 | 데이터 타입 | Nullable | 기본값 | 설명 |
|--------|-------------|----------|--------|------|
| `id` | VARCHAR(100) | NO | - | 고유 식별자 (PK) |
| `embedding` | VECTOR(384) | YES | - | 384차원 벡터 임베딩 |
| `document` | TEXT | YES | - | 문서 내용 (JSON 또는 마크다운) |
| `metadata` | JSONB | YES | - | 메타데이터 (doc_type, collection 등) |
| `doc_type` | VARCHAR(50) | YES | - | 문서 타입 (composite_section/leaf_section) |
| `created_at` | TIMESTAMP | YES | CURRENT_TIMESTAMP | 생성 시간 |

**인덱스**: HNSW 벡터 인덱스 (`core_content_embedding_idx`)

### 2. detailed_content 테이블

상세 분석 내용을 저장하는 테이블로, document 필드 없이 core_ref로 원문을 참조합니다.

| 필드명 | 데이터 타입 | Nullable | 기본값 | 설명 |
|--------|-------------|----------|--------|------|
| `id` | VARCHAR(100) | NO | - | 고유 식별자 (PK) |
| `embedding` | VECTOR(384) | YES | - | 384차원 벡터 임베딩 |
| `core_ref` | VARCHAR(100) | YES | - | 원문 참조 ID (FK to core_content.id) |
| `metadata` | JSONB | YES | - | 메타데이터 (type, collection 등) |
| `created_at` | TIMESTAMP | YES | CURRENT_TIMESTAMP | 생성 시간 |

**인덱스**: HNSW 벡터 인덱스 (`detailed_content_embedding_idx`)

---

## 🔍 데이터 구조 예시

### core_content 데이터 구조

#### 상위 섹션 (composite_section)
```json
{
  "id": "chapter1",
  "embedding": [0.123, -0.456, ...],
  "document": "{\"type\": \"composite_section\", \"title\": \"Chapter 1\", \"composed_of\": [...]}",
  "metadata": {"doc_type": "composite_section", "collection": "core_content"},
  "doc_type": "composite_section"
}
```

#### 하위 섹션 (leaf_section)
```json
{
  "id": "section_1_1_1", 
  "embedding": [0.321, -0.654, ...],
  "document": "# 1.1.1 The design phase\n\n실제 마크다운 원문...",
  "metadata": {"doc_type": "leaf_section", "collection": "core_content"},
  "doc_type": "leaf_section"
}
```

### detailed_content 데이터 구조

```json
{
  "id": "section_1_1_1_detail",
  "embedding": [0.789, -0.123, ...], 
  "core_ref": "section_1_1_1",
  "metadata": {"type": "detailed_analysis", "collection": "detailed_content"}
}
```

---

## 🔧 Query Neon 스크립트

Neon DB에서 벡터 검색을 수행하는 명령어 도구입니다.

### 사용법

```bash
python query_neon.py "검색할 질의" [최대결과수]
```

**예시:**
```bash
python query_neon.py "OOP의 문제점은 무엇인가?" 5
```

### 스크립트 코드

```python
#!/usr/bin/env python3
"""
Neon DB 질의 스크립트
첫 번째 인자로 질의를 받아서 Neon PostgreSQL에서 검색하고 출처와 함께 결과 반환
"""

import sys
import json
from embedding_service_v2 import get_embedding_service
from neon_vector_db import NeonVectorDB
import logging

# 로깅 레벨을 WARNING으로 설정하여 불필요한 로그 숨김
logging.getLogger().setLevel(logging.WARNING)

def query_neon_db(query: str, max_results: int = 3) -> str:
    """
    Neon DB에서 질의 검색 및 결과 반환
    
    Args:
        query: 검색 질의
        max_results: 최대 결과 수
        
    Returns:
        포매팅된 검색 결과
    """
    try:
        # 시스템 초기화
        embedding_service = get_embedding_service()
        neon_db = NeonVectorDB()
        
        # 질의를 임베딩으로 변환
        query_embedding = embedding_service.create_embedding(query)
        
        # 핵심 내용 검색
        core_results = neon_db.search_core_content(query_embedding, max_results)
        
        # 상세 내용 검색
        detailed_results = neon_db.search_detailed_content(query_embedding, max_results)
        
        # 상세 내용에 원문 추가
        for result in detailed_results:
            if result['core_ref']:
                original = neon_db.get_core_content_by_id(result['core_ref'])
                if original:
                    result['original_content'] = original['document']
        
        # 결과 포매팅
        output = format_search_results(query, core_results, detailed_results)
        
        # 리소스 정리
        neon_db.close()
        
        return output
        
    except Exception as e:
        return f"❌ 검색 중 오류 발생: {str(e)}"

def format_search_results(query: str, core_results: list, detailed_results: list) -> str:
    """검색 결과 포매팅"""
    
    if not core_results and not detailed_results:
        return f"🤔 '{query}'에 대한 관련 정보를 찾을 수 없습니다."
    
    output = f"## 🔍 질의: '{query}'\n\n"
    
    # 핵심 내용 결과
    if core_results:
        output += "### 📚 핵심 내용\n\n"
        
        for i, result in enumerate(core_results, 1):
            confidence = max(0, (1 - result['distance']) * 100)
            
            output += f"**{i}. {result['id']}** (신뢰도: {confidence:.1f}%)\n"
            
            # 문서 내용 파싱
            doc = result['document']
            if doc.startswith('{'):  # JSON 형태 (상위 섹션)
                try:
                    doc_obj = json.loads(doc)
                    output += f"- **제목**: {doc_obj.get('title', 'N/A')}\n"
                    output += f"- **요약**: {doc_obj.get('content_summary', 'N/A')}\n"
                    if doc_obj.get('composed_of'):
                        output += f"- **하위 구성**: {', '.join(doc_obj['composed_of'])}\n"
                except:
                    output += f"- **내용**: {doc[:200]}...\n"
            else:  # 일반 텍스트 (하위 섹션)
                # 제목 추출
                title_lines = [line for line in doc.split('\n') if line.startswith('# ')]
                if title_lines:
                    title = title_lines[0].replace('# ', '').strip()
                    output += f"- **제목**: {title}\n"
                
                # 페이지 정보 추출
                page_lines = [line for line in doc.split('\n') if '페이지 범위' in line]
                if page_lines:
                    page_info = page_lines[0].split('**페이지 범위:**')[1].strip() if '**페이지 범위:**' in page_lines[0] else 'N/A'
                    output += f"- **페이지**: {page_info}\n"
                
                # 첫 번째 내용 단락 추출
                content_lines = [line.strip() for line in doc.split('\n') 
                               if line.strip() and not line.startswith('#') 
                               and not line.startswith('**') and len(line.strip()) > 20]
                if content_lines:
                    first_content = content_lines[0][:150]
                    output += f"- **내용**: {first_content}...\n"
            
            output += f"- **출처**: Neon DB - core_content 테이블\n\n"
    
    # 상세 내용 결과
    if detailed_results:
        output += "### 🔬 상세 분석\n\n"
        
        for i, result in enumerate(detailed_results, 1):
            confidence = max(0, (1 - result['distance']) * 100)
            
            output += f"**{i}. {result['id']}** (신뢰도: {confidence:.1f}%)\n"
            output += f"- **원문 참조**: {result['core_ref']}\n"
            
            # 참조된 원문 정보 표시
            if result.get('original_content'):
                original = result['original_content']
                if original.startswith('{'):
                    try:
                        doc_obj = json.loads(original)
                        output += f"- **참조 섹션**: {doc_obj.get('title', 'N/A')}\n"
                    except:
                        pass
                else:
                    title_lines = [line for line in original.split('\n') if line.startswith('# ')]
                    if title_lines:
                        title = title_lines[0].replace('# ', '').strip()
                        output += f"- **참조 섹션**: {title}\n"
            
            output += f"- **출처**: Neon DB - detailed_content 테이블\n\n"
    
    # 검색 통계
    total_results = len(core_results) + len(detailed_results)
    output += f"---\n"
    output += f"📊 **검색 통계**: {total_results}개 결과 (핵심: {len(core_results)}, 상세: {len(detailed_results)})\n"
    output += f"🗄️ **데이터베이스**: Neon PostgreSQL + pgvector\n"
    
    return output

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python query_neon.py \"검색할 질의\"")
        print("예시: python query_neon.py \"OOP의 문제점은 무엇인가?\"")
        sys.exit(1)
    
    # 첫 번째 인자를 질의로 사용
    query = sys.argv[1]
    
    # 선택적으로 최대 결과 수 지정 (기본값: 3)
    max_results = 3
    if len(sys.argv) > 2:
        try:
            max_results = int(sys.argv[2])
        except ValueError:
            print("❌ 최대 결과 수는 숫자여야 합니다.")
            sys.exit(1)
    
    # 질의 실행 및 결과 출력
    result = query_neon_db(query, max_results)
    print(result)

if __name__ == "__main__":
    main()
```

---

## 🎯 검색 결과 형태

### 출력 예시

```markdown
## 🔍 질의: 'OOP의 문제점은 무엇인가?'

### 📚 핵심 내용

**1. section_1_2** (신뢰도: 86.2%)
- **제목**: OOP 복잡성의 4가지 근본 원인
- **요약**: 코드-데이터 혼합, 가변성, 데이터 캡슐화, 코드 캡슐화 문제
- **하위 구성**: section_1_2_1, section_1_2_2, section_1_2_3, section_1_2_4
- **출처**: Neon DB - core_content 테이블

### 🔬 상세 분석

**1. section_1_2_1_detail** (신뢰도: 75.3%)
- **원문 참조**: section_1_2_1
- **참조 섹션**: 1.2.1 Many relations between classes
- **출처**: Neon DB - detailed_content 테이블

---
📊 **검색 통계**: 6개 결과 (핵심: 3, 상세: 3)
🗄️ **데이터베이스**: Neon PostgreSQL + pgvector
```

---

## 🚀 시스템 특징

### 장점
1. **정확한 검색**: pgvector HNSW 인덱스로 빠른 벡터 검색
2. **확장성**: Neon Serverless PostgreSQL의 자동 스케일링
3. **데이터 무결성**: ACID 트랜잭션 보장
4. **효율적 저장**: 원문 중복 제거 및 참조 구조
5. **성능**: 30x 빠른 인덱스 빌드 (pgvector 0.6.0)

### 기술 스택
- **데이터베이스**: Neon PostgreSQL
- **벡터 검색**: pgvector (HNSW 인덱스)
- **임베딩**: sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)
- **차원**: 384차원
- **언어**: Python 3.11+

---

## 📝 참고 문서

- [Neon PostgreSQL 공식 문서](https://neon.com/docs)
- [pgvector 확장 가이드](https://neon.com/docs/extensions/pgvector)
- [sentence-transformers 문서](https://www.sbert.net/)

---

*생성일: 2025-07-24*  
*Knowledge Sherpa v2 - Neon PostgreSQL Vector Database*