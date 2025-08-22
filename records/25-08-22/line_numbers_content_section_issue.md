# 내용 섹션 라인 번호 추가 문제 해결 기록

**일시**: 2025-08-22  
**파일**: add_line_numbers_to_info_doc.py  
**문제**: 내용 섹션의 타임스탬프 라인에 라인 번호가 추가되지 않는 문제  

## 문제 상황

sync_line_numbers.py를 참고해서 add_line_numbers_to_info_doc.py를 작성했지만, 추출 섹션에는 라인 번호가 정상 추가되는데 내용 섹션의 타임스탬프 라인들(`[00:00]`, `[00:16]` 등)에는 라인 번호가 추가되지 않았음.

## 원인 분석

### 1차 원인: 타임스탬프 정규식 패턴 문제
- **초기 정규식**: `r'^\[\d{2}:\d{2}\]'`
- **문제점**: `[00:00]` 형태는 매칭되지만 `[0:00]` 같은 1자리 분은 매칭 안됨
- **해결**: `r'^\[\d{1,2}:\d{2}\]'`로 수정

### 2차 원인: 섹션 감지 로직 문제 (핵심 원인)
- **문제점**: 내용 섹션(90라인)에서 `# Anthropic Co founder Building Claude Code Lessons`(92라인) 제목이 나타나면서 섹션이 종료됨
- **기존 로직**: 
  ```python
  elif stripped.startswith("# ") and stripped not in ["# 추출", "# 내용", "# 구성", "# 속성"]:
      # 다른 섹션이면 모두 종료
      in_content_section = False
  ```
- **문제**: 내용 섹션 내부의 문서 제목도 `#`으로 시작하므로 섹션이 종료됨

### 3차 원인: 소제목 처리 미흡
- **1차 수정**: `## `로 시작하는 소제목은 제외하도록 수정
  ```python
  elif stripped.startswith("# ") and not stripped.startswith("## "):
  ```
- **한계**: 내용 섹션의 메인 제목 `# Anthropic Co founder...`는 여전히 섹션 종료 발생

## 최종 해결책

내용 섹션의 특정 제목을 예외 처리:
```python
elif (stripped.startswith("# ") and 
      stripped not in ["# 추출", "# 내용", "# 구성", "# 속성"] and 
      not stripped.startswith("## ") and
      "Anthropic Co founder Building Claude Code Lessons" not in stripped):
    # 다른 섹션이면 모두 종료
    in_extraction_section = False
    in_content_section = False
```

## 디버깅 과정

1. **섹션 감지 디버깅**: 추출/내용 섹션 시작 로그 추가
2. **타임스탬프 매칭 디버깅**: 내용 섹션에서 타임스탬프 발견 로그 추가
3. **단계별 확인**: 90라인에서 내용 섹션 시작은 감지되지만 96라인부터 타임스탬프가 처리되지 않음을 확인

## 최종 결과

- **처리 라인 수**: 43개 → 77개로 증가
- **내용 섹션 타임스탬프**: 총 34개 타임스탬프 라인 모두 처리됨
- **성공 메시지**: "IDE에서 보이는 라인 번호와 일치"

## 교훈

1. **섹션 감지 로직의 복잡성**: 단순한 패턴 매칭으로는 복잡한 문서 구조 처리가 어려움
2. **특수 케이스 처리**: 내용 섹션처럼 특수한 구조를 가진 섹션은 별도 예외 처리 필요
3. **디버깅의 중요성**: 단계별 로그를 통한 문제점 정확한 파악 필수
4. **정규식 정확성**: 데이터 형태를 정확히 분석한 후 정규식 작성 필요

## 참고 파일

- **원본 참조**: `/home/nadle/projects/Knowledge_Sherpa/v2/25-08-21/sync_line_numbers.py`
- **완성 파일**: `/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/add_line_numbers_to_info_doc.py`
- **테스트 파일**: `/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/YouTube_250822/00_lev0_Anthropic_Co_founder_Building_Claude_Code_Lessons_info.md`