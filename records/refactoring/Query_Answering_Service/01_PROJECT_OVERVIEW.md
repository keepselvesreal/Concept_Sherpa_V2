# 질의 응답 시스템 구현 프로젝트

## 프로젝트 목표
사용자 질의에 대해 책 목차 기반으로 관련 장/섹션을 찾아 답변을 생성하는 독립적인 서비스 구현

## 핵심 기능
- **chapter_based_response**: 장 단위 질의 응답 (장 전체 내용 기반)
- **section_based_response**: 섹션 + unified_info_docs 기반 응답
- **AI 기반 관련도 판단**: 목차와 질의 간의 유사도 판단
- **정규화된 파일 매핑**: normalize_title()을 통한 파일 시스템 매칭

## 기술적 제약사항
- 기존 Knowledge Sherpa v2 파이프라인과 **독립적으로 동작**
- `ai_service_v4.py`의 `query_single_request` 메서드 **필수 사용**
- `text_utils.py`의 `normalize_title()` 함수 **필수 활용**
- 완료된 workspace 데이터만 사용 (실시간 처리 없음)

## 입출력 명세
- **입력**: 사용자 질의(str), 책 폴더 경로(str), 응답 모드(str)
- **출력**: 질의, 선택된 장/섹션, 개별 답변들, 종합 답변을 포함한 Dict

## 성능 요구사항
- **병렬 처리**: 최대 4개 장/섹션 동시 처리
- **안정성**: AI 서비스 장애 시 최대 3회 재시도
- **내결함성**: 일부 장/섹션 실패 시에도 성공한 답변들로 종합 응답 생성

## 프로젝트 구조
```
refactoring/src/
├── services/
│   └── query_answering_service.py      # 메인 서비스
├── components/
│   ├── chapter_selector.py             # AI 기반 장 선택
│   ├── section_selector.py             # AI 기반 섹션 선택
│   ├── parallel_answer_generator.py    # 병렬 답변 생성
│   ├── workspace_data_loader.py        # 데이터 로더
│   └── content_mapper.py               # 파일 매핑
└── config/
    └── query_answering.yaml            # 설정 파일
```