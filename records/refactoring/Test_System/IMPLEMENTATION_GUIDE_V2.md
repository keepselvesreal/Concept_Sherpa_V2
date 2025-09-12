테스트 데이터 생성 및 관리 체계 구현 계획 - 정리본

  1. 프로젝트 목표

  1.1 핵심 목표

  - WorkspacePreparationStage에서 생성되는 실제 데이터를 테스트용으로 저장
  - I/O와 로직 분리를 통한 파이프라인 개선
  - 다음 단계로 실제 데이터 전달 (경로 대신)

  1.2 개선 방향

  - 기존: 경로 전달 방식 → 개선: 실제 데이터 전달 방식
  - 파이프라인 단계간 I/O 최소화
  - 테스트 격리 및 재사용성 향상

  2. 현재 상황 분석

  2.1 기존 데이터 전달 구조의 문제점

  WorkspacePreparationStage → IntegratedNodeGenerationStage
  🔴 경로만 전달: 'output_directory', 'folder_path', 'toc_file'  
  🔴 다음 단계에서 파일 I/O 필요
  🔴 테스트 시 실제 파일 시스템 의존

  2.2 파악된 제약사항

  - PDF 처리: fitz.open(pdf_path) - 불가피한 I/O
  - 서비스 의존성: TocService, ChapterExtractionService 등이 파일 시스템 기반
  - 기존 파이프라인 호환성 고려 필요

  3. 해결 방안: 하이브리드 방식

  3.1 WorkspacePreparationStage 수정 방향

  # 기존 로직 유지: 폴더/파일 생성 (ChapterExtractionService 등 호환성)
  # 🟢 추가: 생성된 파일을 읽어서 data 필드에 실제 데이터 포함

  return {
      'success': True,
      'data': {
          'book_metadata': {...},
          'chapters_data': [           # 🟢 실제 데이터
              {
                  'toc_structure': [...],     # 실제 목차 데이터
                  'content_text': "...",      # 실제 콘텐츠 데이터
                  'metadata': {...}
              }
          ]
      },
      'error': None
  }

  3.2 파이프라인 개선 효과

  # 기존: 파일 경로 전달 + I/O 필요
  stage2_input = {'book_directory': stage1_result['output_directory']}

  # 개선: 실제 데이터 직접 전달
  stage2_input = stage1_result['data']  # 🟢 메모리에서 바로 사용

  3.3 IntegratedNodeGenerationStage 개선

  - 기존: os.listdir() + 파일 읽기 필요
  - 개선: chapters_data에서 바로 데이터 접근

  4. 테스트 데이터 생성 체계

  4.1 테스트 파일 구조

  tests/
  ├── conftest.py                    # 기본 fixture (수정)
  ├── schemas/
  │   └── stage_schemas.py           # 데이터 스키마 정의
  ├── fixtures/
  │   └── pdfs/                      # 테스트용 PDF (사용자 제공)
  ├── data/
  │   └── workspace_preparation/     # 생성된 테스트 데이터
  └── test_workspace_preparation_data_generation.py

  4.2 데이터 생성 테스트 역할

  async def test_workspace_preparation_data_generation():
      # 1. 실제 WorkspacePreparationStage 실행
      stage = WorkspacePreparationStage(config_manager, logger)
      result = await stage.process({"pdf_path": pdf_path})

      # 2. 스키마 검증
      assert WorkspacePreparationOutput.validate(result)

      # 3. 테스트 데이터 저장 (tests/data/에)
      save_test_data("workspace_preparation_output", result['data'])

  5. 구현 단계별 계획

  5.1 Phase 1: 기본틀 구축

  1. conftest.py 수정: Logger 직접 사용하도록 fixture 추가
  2. 스키마 정의: WorkspacePreparationOutput 스키마 작성
  3. 데이터 생성 테스트: 메인 테스트 파일 작성
  4. PDF 파일 배치: fixtures/pdfs/ 폴더 준비

  5.2 Phase 2: WorkspacePreparationStage 수정

  1. 하이브리드 구조 구현: 기존 로직 + 데이터 반환
  2. 반환값 구조 변경: {success, data, error} 형태
  3. 데이터 로딩 로직: 생성된 파일을 읽어서 data에 포함

  5.3 Phase 3: 파이프라인 연결

  1. pipeline_orchestrator_v2.py 수정: 데이터 직접 전달
  2. IntegratedNodeGenerationStage 수정: 입력 데이터 구조 변경
  3. 통합 테스트: 전체 파이프라인 데이터 흐름 검증

  6. 예상 효과

  6.1 I/O 성능 개선

  - 파이프라인 단계간 파일 I/O 최소화
  - 메모리 기반 데이터 처리로 속도 향상

  6.2 테스트 용이성

  - 실제 데이터 기반 테스트 가능
  - Mock 없이도 격리된 테스트 환경
  - 회귀 테스트용 참조 데이터 확보

  6.3 유지보수성

  - 단계간 데이터 의존성 명확화
  - 스키마 기반 데이터 검증
  - 점진적 개선 가능한 구조

  7. 다음 작업 단계

  1. conftest.py fixture 추가 (Logger 기반)
  2. 스키마 정의 파일 작성
  3. 데이터 생성 테스트 파일 작성
  4. PDF 파일 제공받아 fixtures에 배치
  5. WorkspacePreparationStage 하이브리드 구조 구현