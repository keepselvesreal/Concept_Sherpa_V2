# Query Answering Service V2 - Project Overview

**생성 시간:** Tue Sep 16 11:42:00 KST 2025

**핵심 내용:** AI 기반 목차 질의 매칭 시스템 구현 계획 - 사용자 질의와 목차 항목 간의 연관성을 AI로 판단하여 관련 헤더를 반환하는 서비스

**상세 내용:**
- 프로젝트 개요 (라인 1-50): 핵심 기능, 입출력 구조, 주요 요구사항
- 아키텍처 설계 (라인 51-100): 클래스 구조, AI 서비스 통합 방안
- 구현 계획 (라인 101-150): 단계별 개발 계획, 우선순위
- 기술 스펙 (라인 151-200): AI 프롬프트 전략, 데이터 형식

**상태:** active

**참조:** 기존 ai_service_v4.py의 query_single_request 메서드 활용

---

## 프로젝트 개요

### 🎯 핵심 기능

**AI 기반 목차 질의 매칭 시스템** (AI-based TOC Query Matching System)

사용자의 질의와 목차 내용을 AI로 분석하여, 질의와 관련성이 높은 목차 항목의 헤더 제목을 반환하는 서비스입니다.

### 📋 입출력 구조

**입력 (Input):**
- **사용자 질의** (User Query): 자연어로 작성된 질문 또는 요청
- **목차 데이터** (TOC Data): 책 목차 또는 장 목차 내용

**출력 (Output):**
- **매칭된 목차 헤더**: 관련성 높은 항목의 헤더 제목 (최대 3개)
- **빈 결과**: 관련성이 낮은 경우 아무것도 반환하지 않음

### 🔍 데이터 형식 예시

**책 목차 형식:**
```
1_Complexity_of_object_oriented_programming
2_Separation_between_code_and_data
```

**장 목차 형식:**
```
28_lev2_2.1_The_two_parts_of_a_DOP_system_info.md
29_lev2_2.2_Data_entities_info.md
30_lev2_2.3_Code_modules_info.md
```

### ⚡ 핵심 요구사항

1. **엄격한 관련성 기준**: 애매한 경우 선택하지 않음
2. **최대 3개 제한**: 결과의 품질을 위한 수량 제한
3. **헤더 원본 반환**: 목차 헤더 제목을 그대로 반환
4. **기존 AI 서비스 활용**: ai_service_v4.py의 query_single_request 재사용

---

## 아키텍처 설계

### 🏗️ 클래스 구조

```python
class TocQueryMatcher:
    """간단한 AI 기반 목차 매칭 서비스"""
    
    def __init__(self, ai_service: AIService):
        """AI 서비스 의존성 주입"""
        self.ai_service = ai_service
        
    async def match_query_to_toc(
        self, 
        user_query: str, 
        toc_content: str
    ) -> List[str]:
        """
        질의와 목차 매칭 메인 메서드
        
        Args:
            user_query: 사용자 질의
            toc_content: 목차 내용
            
        Returns:
            List[str]: 매칭된 헤더 제목들 (최대 3개, 관련성 없으면 빈 리스트)
        """
        
    def _generate_prompt(self, query: str, toc_content: str) -> str:
        """AI 매칭용 프롬프트 생성"""
        
    def _parse_ai_response(self, response: str) -> List[str]:
        """AI 응답 파싱 및 헤더 추출 (최대 3개)"""
```

### 🔗 기존 시스템 통합

**파일 위치:**
```
refactoring/src/services/toc_query_matching_service.py
```

**의존성:**
- ✅ `ai_service_v4.py` → query_single_request 메서드 활용
- ✅ `typing` → List, Optional 타입 힌트
- 🔄 `text_utils.py` → 텍스트 처리 유틸리티 (필요시)

### 📊 데이터 플로우

```
사용자 질의 + 목차 데이터
    ↓
프롬프트 생성
    ↓
AI 서비스 호출 (query_single_request)
    ↓
AI 응답 파싱
    ↓
헤더 제목 추출 (최대 3개)
    ↓
결과 반환
```

---

## 구현 계획

### 📅 단계별 개발 계획

**1단계: 핵심 기능 구현** (Priority: High)
- [ ] TocQueryMatcher 클래스 기본 구조 생성
- [ ] AI 프롬프트 템플릿 작성 (엄격한 관련성 체크)
- [ ] ai_service_v4와 연동 구현
- [ ] 최대 3개 제한 로직 구현

**2단계: 응답 처리 로직** (Priority: High)
- [ ] AI 응답 파싱 로직 구현
- [ ] "관련 항목 없음" 케이스 처리
- [ ] 헤더 제목 정확한 추출 로직

**3단계: 테스트 및 검증** (Priority: Medium)
- [ ] 관련성 높은 질의 테스트
- [ ] 관련성 낮은 질의 테스트 (빈 결과 확인)
- [ ] 경계 케이스 테스트 (빈 목차, 긴 질의 등)
- [ ] 성능 테스트

**4단계: 최적화 및 통합** (Priority: Low)
- [ ] 에러 처리 강화
- [ ] 로깅 추가
- [ ] 문서화 완성

### 🎯 개발 우선순위

**파레토 80/20 원칙 적용:**
- **80% 가치**: AI 프롬프트 엔지니어링 + 응답 파싱
- **20% 가치**: 에러 처리 + 최적화

---

## 기술 스펙

### 🧠 AI 프롬프트 전략

**핵심 프롬프트 템플릿:**
```
사용자 질의: "{user_query}"

다음 목차 항목들을 검토하고, 질의와 **밀접하게 관련된** 항목만 선택하세요.
관련성이 낮거나 애매하면 선택하지 마세요.
최대 3개까지만 선택하고, 헤더 제목을 그대로 반환하세요.

목차:
{toc_content}

응답 형식 (관련 항목이 있을 경우만):
1. [헤더제목1]
2. [헤더제목2] 
3. [헤더제목3]

관련 항목이 없으면: "관련 항목 없음"
```

**프롬프트 설계 원칙:**
- **명확한 지시**: "밀접하게 관련된" 강조
- **엄격한 기준**: "애매하면 선택하지 마세요"
- **수량 제한**: "최대 3개까지만"
- **일관된 형식**: 구조화된 응답 요구

### 📄 응답 파싱 로직

**예상 AI 응답 형식:**
```
1. 1_Complexity_of_object_oriented_programming
2. 2_Separation_between_code_and_data
```

**파싱 알고리즘:**
1. 라인별 분할
2. 번호 제거 (1., 2., 3.)
3. 헤더 제목 추출
4. 최대 3개 제한 적용
5. "관련 항목 없음" 케이스 처리

### 🔧 기술적 고려사항

**성능:**
- 비동기 처리 (async/await)
- AI API 호출 최적화

**안정성:**
- 예외 처리 (AI 서비스 오류)
- 입력 검증 (빈 문자열, None 처리)

**확장성:**
- 인터페이스 기반 설계
- 설정 가능한 최대 결과 수

---

## 예상 사용 사례

### 📝 테스트 케이스 예시

**Case 1: 높은 관련성**
```
질의: "객체 지향 프로그래밍의 문제점이 뭐야?"
목차: book_toc.md
예상 결과: ["1_Complexity_of_object_oriented_programming"]
```

**Case 2: 중간 관련성**
```
질의: "DOP에서 데이터는 어떻게 처리해?"
목차: chapter_2_toc.md
예상 결과: ["29_lev2_2.2_Data_entities_info.md"]
```

**Case 3: 낮은 관련성**
```
질의: "파이썬 설치 방법이 뭐야?"
목차: book_toc.md
예상 결과: [] (빈 리스트)
```

---

## 프로젝트 메타데이터

**개발 환경:** Python 3.8+, async/await 지원
**의존성:** ai_service_v4.py, typing
**테스트 데이터:** Data_Oriented_Programming 도서 목차
**개발 기간:** 2-3일 (핵심 기능), 1주 (전체 완성)
**유지보수 복잡도:** 낮음 (단순한 구조)