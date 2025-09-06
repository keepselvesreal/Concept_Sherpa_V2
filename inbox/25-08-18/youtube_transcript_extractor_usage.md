# YouTube 대본 추출기 사용법

**생성 시간:** 2025-08-18 19:50:42 KST  
**주소:** youtube_transcript_extractor_usage

## 개요

`youtube_transcript_extractor.py`는 YouTube 영상의 대본을 추출하여 마크다운 파일로 저장하는 스크립트입니다.

## 설치 요구사항

```bash
uv add youtube-transcript-api
```

## 사용법

### 1. 명령줄에서 URL 인수로 실행
```bash
python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. 대화형 모드로 실행
```bash
python youtube_transcript_extractor.py
# URL 입력 프롬프트가 나타남
```

## 지원 기능

- **다양한 YouTube URL 형식 지원**
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `https://www.youtube.com/embed/VIDEO_ID`
  - `https://www.youtube.com/v/VIDEO_ID`

- **언어 우선순위**
  - 1순위: 한국어 (ko)
  - 2순위: 영어 (en)
  - 3순위: 기본 사용 가능한 언어

- **출력 형식**
  - 마크다운 파일 (.md)
  - 타임스탬프 포함 ([분:초] 형식)
  - 영상 URL 및 추출 정보 헤더

## 출력 예시

```markdown
# YouTube 대본

**영상 URL:** https://www.youtube.com/watch?v=EgXOaH-ZqfU
**추출 언어:** en
**추출 시간:** 2025-08-18 19:50:15

---

[00:00] AI coding is constantly evolving.
[00:02] Whether you use clawed code or cursor,
[00:04] it doesn't matter. People are realizing
...
```

## 에러 처리

- 대본이 비활성화된 영상 감지
- 유효하지 않은 YouTube URL 검증
- 네트워크 오류 및 API 제한 처리
- 지원되지 않는 언어 자동 대체

## 파일명 규칙

생성되는 파일명: `youtube_transcript_{VIDEO_ID}.md`

예: `youtube_transcript_EgXOaH-ZqfU.md`