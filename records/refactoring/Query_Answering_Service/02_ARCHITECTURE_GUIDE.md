# 기술 아키텍처 가이드

## 핵심 설계 패턴
- **Service Pattern**: QueryAnsweringService (Stage가 아닌 독립 서비스)
- **Strategy Pattern**: response_mode별 처리 전략
- **Dependency Injection**: ai_service, config_manager, logger 주입
- **Command Pattern**: 각 컴포넌트가 독립적인 책임 수행

## 아키텍처 구성요소
```python
QueryAnsweringService
├── ParallelAnswerGenerator (병렬 답변 생성, 최대 4개)
├── ChapterSelector (AI 기반 장 선택)
├── SectionSelector (AI 기반 섹션 선택)  
├── WorkspaceDataLoader (완료된 데이터 로드)
└── ContentMapper (정규화 기반 파일 매핑)
```

## 데이터 플로우
### chapter_based_response 모드
1. 사용자 질의 입력
2. workspace 데이터 로드 (책 목차, 장별 폴더 스캔)
3. AI 기반 관련 장 선택 (최대 3개)
4. 정규화 기반 장 폴더 매핑
5. **병렬로** 각 장의 전체 내용 기반 답변 생성
6. 모든 답변 완료 후 최종 종합 답변 생성

### section_based_response 모드  
1. 사용자 질의 입력
2. workspace 데이터 로드
3. AI 기반 관련 장 선택
4. 각 장의 목차에서 AI 기반 섹션 선택
5. 정규화 기반 unified_info_docs 파일 매핑
6. **병렬로** 각 섹션의 unified_info_docs 기반 답변 생성
7. 모든 답변 완료 후 최종 종합 답변 생성

## 병렬 처리 설계
- **asyncio.Semaphore**: 최대 4개 동시 실행 제어
- **Graceful Failure**: 개별 실패가 전체 프로세스에 영향 주지 않음
- **Status Tracking**: 성공/실패 상태를 개별 추적
- **Resource Bounded**: 예측 가능한 리소스 사용량

## 안정성 설계 원칙
- **Fail-Safe**: 일부 실패가 전체 실패로 이어지지 않음
- **Retry-First**: AI 서비스 일시적 장애에 대한 3회 자동 재시도
- **JSON Parsing Resilience**: 파싱 실패 시 더 명확한 프롬프트로 재요청
- **Resource Protection**: 동시 처리 수 제한으로 시스템 보호

## 확장 가능성
- **설정 기반**: 재시도 횟수, 동시 처리 수 등 설정으로 조정 가능
- **Plugin Architecture**: 새로운 응답 모드 추가 용이
- **Cache Ready**: 목차 데이터 및 AI 응답 캐싱 준비
- **Monitoring Hooks**: 상세한 로깅 및 메트릭 수집 지점 제공