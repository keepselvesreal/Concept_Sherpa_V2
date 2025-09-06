# Knowledge Sherpa UI 사용법

**생성 시간**: 2025-08-18 (한국 시간)  
**핵심 내용**: Knowledge Sherpa UI 사용 가이드  
**상태**: 활성  
**주소**: knowledge_ui/docs/usage_guide  

## 설치 및 실행

### 1. 필요한 라이브러리 설치

```bash
pip install youtube-transcript-api
```

### 2. UI 실행

```bash
cd knowledge_ui
python run_ui.py
```

또는

```bash
python main_ui.py
```

## 주요 기능

### 🎥 YouTube 대본 추출

1. **URL 입력**: YouTube URL을 입력란에 붙여넣기
2. **대본 추출 버튼 클릭**: "대본 추출" 버튼 클릭
3. **결과 확인**: 
   - 처리 결과가 하단 결과 영역에 표시
   - 성공 시 `outputs/transcripts/` 폴더에 마크다운 파일 저장

**지원 URL 형식**:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

### 📁 파일 처리

1. **파일 선택**: "파일 선택..." 버튼 클릭
2. **파일 선택 대화상자**: Windows 파일 탐색기에서 파일 선택
3. **파일 처리**: "파일 처리" 버튼 클릭
4. **결과 확인**:
   - 선택된 파일 경로가 콘솔에 출력
   - 처리 결과가 UI 하단에 표시
   - 처리 로그가 `outputs/processed_files/` 폴더에 저장

**지원 파일 형식**:
- 모든 파일 형식 지원
- 텍스트, 마크다운, PDF, 워드 문서 등

## 출력 파일 위치

```
knowledge_ui/
├── outputs/
│   ├── transcripts/           # YouTube 대본 파일들
│   │   └── youtube_transcript_VIDEO_ID.md
│   └── processed_files/       # 파일 처리 결과
│       └── file_processing_log.txt
```

## 문제 해결

### 일반적인 문제

1. **"youtube-transcript-api 모듈을 찾을 수 없음"**
   ```bash
   pip install youtube-transcript-api
   ```

2. **"tkinter 모듈을 찾을 수 없음"**
   - Linux: `sudo apt-get install python3-tk`
   - macOS: tkinter는 기본 설치됨
   - Windows: Python 재설치 (tkinter 옵션 체크)

3. **"대본을 추출할 수 없습니다"**
   - 영상에 대본이 없거나 비활성화됨
   - 비공개 영상이거나 접근 제한됨
   - 네트워크 연결 문제

### 로그 확인

- **콘솔 출력**: 실시간 처리 상황 확인
- **UI 결과 영역**: 상세한 처리 결과 표시
- **로그 파일**: `outputs/processed_files/file_processing_log.txt`

## 개발자 정보

- **개발 목적**: YouTube 대본 추출 및 파일 경로 전달 테스트
- **기술 스택**: Python, Tkinter, youtube-transcript-api
- **확장 가능성**: 웹 UI 전환, 더 많은 파일 처리 기능 추가