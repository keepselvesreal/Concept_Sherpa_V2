# Playwright MCP 기반 웹 콘텐츠 추출기 구현 계획

## 생성 시간: 2025-08-18 15:42 KST

## 핵심 내용: Playwright MCP를 활용한 웹 페이지 메인 콘텐츠 자동 추출 시스템 설계

## 상세 내용:
- 기술 조사 결과 요약 (라인 21-65): Playwright MCP 주요 기능 및 활용 가능성
- 콘텐츠 추출 전략 (라인 67-89): 다양한 추출 방법론 및 도구
- 유료 서비스 대응 방안 (라인 91-112): 인증 및 세션 관리 방법
- 구현 아키텍처 (라인 114-165): 시스템 구조 및 컴포넌트 설계
- 기능 명세 (라인 167-201): 주요 기능 및 옵션
- 실행 계획 (라인 203-229): 단계별 개발 로드맵

## 상태: 계획 수립 완료
## 주소: playwright_content_extractor_plan

---

## 1. 기술 조사 결과 요약

### Playwright MCP 주요 기능
- **브라우저 자동화**: Chrome, Firefox, WebKit 지원
- **DOM 조작**: `browser_snapshot`, `browser_evaluate`, `browser_navigate`
- **텍스트 추출**: `browser_type`, `browser_click`, `browser_press_key`
- **대기 기능**: `browser_wait_for` - 특정 조건 대기
- **네트워크 추적**: 요청/응답 모니터링
- **스크린샷**: 시각적 검증 가능

### 접근성 중심 설계
- 픽셀 기반이 아닌 **구조화된 접근성 스냅샷** 사용
- LLM 친화적 출력 형식
- 결정론적 도구 적용 가능

### 기존 MCP 서버 활용 옵션
1. **mcp-playwright-scraper** (Dennis Lin): 웹 콘텐츠 → 마크다운 변환
2. **fetcher-mcp**: Readability 알고리즘 내장, 메인 콘텐츠 자동 추출
3. **executeautomation/mcp-playwright**: 포괄적 브라우저 자동화

## 2. 콘텐츠 추출 전략

### 자동 메인 콘텐츠 추출
- **Readability 알고리즘**: 광고, 네비게이션, 비필수 요소 제거
- **CSS 셀렉터**: `article`, `main`, `.post-content` 등 의미적 요소 활용
- **휴리스틱 분석**: 텍스트 밀도, 단락 길이, 링크 비율 등

### 다양한 사이트 대응
- **Medium**: `article` 태그, `.post-content` 클래스
- **기술 블로그**: `main`, `.content`, `.article-body`
- **뉴스 사이트**: `article`, `.story-body`, `.article-content`
- **GitHub**: `.markdown-body`, `.Box-body`

### 출력 형식 옵션
- **마크다운**: 구조화된 텍스트, 제목 계층 유지
- **HTML**: 원본 구조 보존
- **플레인 텍스트**: 순수 텍스트만 추출

## 3. 유료 서비스 대응 방안

### 인증 방법 1: 수동 로그인 + 세션 유지
```
1. Playwright MCP로 로그인 페이지 열기
2. 사용자가 직접 브라우저에서 로그인
3. 세션 쿠키 자동 저장
4. 후속 요청에서 인증 상태 유지
```

### 인증 방법 2: 쿠키 전달
```
1. 기존 브라우저에서 쿠키 추출
2. Playwright context에 쿠키 주입
3. 인증된 상태로 페이지 접근
```

### 세션 관리
- **Storage State**: 로그인 상태 영구 저장
- **Context Cookies**: `context.cookies()`, `context.add_cookies()`
- **Profile 유지**: `--user-data-dir` 지정으로 프로필 재사용

## 4. 구현 아키텍처

### 시스템 구조
```
WebContentExtractor
├── PlaywrightManager: 브라우저 세션 관리
├── AuthenticationHandler: 인증 및 쿠키 관리  
├── ContentExtractor: 메인 콘텐츠 추출 로직
├── ContentProcessor: 텍스트 정제 및 변환
└── FileManager: 추출 결과 저장
```

### 핵심 컴포넌트

#### PlaywrightManager
- MCP 서버 연결 관리
- 브라우저 컨텍스트 생성/종료
- 네비게이션 및 페이지 상태 관리

#### AuthenticationHandler  
- 로그인 세션 감지
- 쿠키 저장/복원
- 인증 상태 검증

#### ContentExtractor
- 다중 추출 전략 적용
- 사이트별 커스텀 셀렉터
- 콘텐츠 품질 검증

#### ContentProcessor
- HTML → 마크다운 변환
- 텍스트 정제 (불필요한 공백, 특수문자 제거)
- 메타데이터 추가 (URL, 제목, 추출 시간)

## 5. 기능 명세

### 주요 기능
1. **URL 입력** → 자동 콘텐츠 추출
2. **다중 URL 배치 처리**
3. **추출 전략 선택** (자동/수동 셀렉터)
4. **출력 형식 지정** (마크다운/HTML/텍스트)
5. **메타데이터 포함** 옵션

### 추가 옵션
- **스크린샷 저장**: 시각적 확인용
- **전체 페이지 vs 메인 콘텐츠**: 추출 범위 선택
- **대기 조건**: 동적 콘텐츠 로딩 대기
- **에러 처리**: 실패 시 대체 전략

### CLI 인터페이스 예시
```bash
python extract_content.py --url "https://medium.com/@user/article" 
                         --format markdown 
                         --output ./extracted/
                         --auth-required
                         --include-metadata
```

## 6. 실행 계획

### Phase 1: 기본 구조 구현 (1-2일)
- PlaywrightManager 클래스 구현
- 기본 네비게이션 및 콘텐츠 추출
- 마크다운 변환 기능

### Phase 2: 인증 기능 추가 (1일)  
- 쿠키 관리 시스템
- 세션 유지 메커니즘
- Medium 등 유료 서비스 테스트

### Phase 3: 고도화 및 최적화 (1-2일)
- 다중 사이트 대응 셀렉터
- 배치 처리 기능
- 에러 처리 및 복구

### Phase 4: 검증 및 문서화 (1일)
- 다양한 사이트 테스트
- 사용법 문서 작성
- 예시 실행 결과 생성

## 참조: 기존 Knowledge_Sherpa/v2 프로젝트 구조와 통합