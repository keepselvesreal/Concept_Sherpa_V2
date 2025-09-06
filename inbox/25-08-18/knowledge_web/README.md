# Knowledge Sherpa Web UI

**생성 시간**: 2025-08-18 (한국 시간)  
**핵심 내용**: FastAPI + HTML/CSS 기반 웹 UI  
**상세 내용**:
  - app.py: FastAPI 메인 애플리케이션
  - templates/: HTML 템플릿 파일들
  - static/: CSS, JS 정적 파일들
  - api/: API 엔드포인트 모듈들
  - uploads/: 업로드된 파일 임시 저장

**상태**: 개발 중  
**주소**: knowledge_web  
**참조**: ../knowledge_ui/ 핸들러들

## 프로젝트 구조

```
knowledge_web/
├── app.py                 # FastAPI 메인 앱
├── api/                   # API 엔드포인트들
│   ├── __init__.py
│   ├── youtube.py         # YouTube 처리 API
│   └── file_handler.py    # 파일 처리 API
├── templates/             # HTML 템플릿
│   └── index.html         # 메인 페이지
├── static/                # 정적 파일
│   ├── css/
│   │   └── style.css      # 스타일시트
│   └── js/
│       └── main.js        # JavaScript
├── uploads/               # 업로드 파일 임시 저장
└── outputs/               # 처리 결과 저장
    ├── transcripts/       # YouTube 대본
    └── processed_files/   # 처리된 파일들
```

## 실행 방법

```bash
# 의존성 설치
pip install fastapi uvicorn python-multipart

# 서버 실행
cd knowledge_web
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 브라우저에서 접속
http://localhost:8000
```

## 기능

- 🎥 YouTube URL 입력 → 대본 추출
- 📁 파일 업로드 → 경로 전달 및 처리
- 🌐 웹 브라우저에서 직접 사용 가능