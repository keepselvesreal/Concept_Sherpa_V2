진행할 작업 정리

  🎯 구현 목표

  WorkspacePreparationStage 테스트 시스템 구축:
  - 데이터 생성 테스트: 실제 PDF → 실제 데이터 생성 → 픽스처 저장
  - 메인 로직 테스트: 픽스처 데이터 활용한 개별 메서드 검증
  - 자동 갱신 시스템: --regen-fixtures 옵션 지원

  📋 작업 단계

  Phase 1: 기본 테스트 인프라 구축

  1.1 conftest.py 수정

  # 추가할 내용들
  def pytest_addoption(parser):
      """--regen-fixtures 옵션 정의"""

  @pytest.fixture(scope="session")
  def config_manager():
      """ConfigManager fixture (Logger v2 호환)"""

  @pytest.fixture(scope="session") 
  def test_logger():
      """Logger 직접 사용 fixture"""

  @pytest.fixture(scope="session")
  def real_pdf_path():
      """실제 PDF 파일 경로"""

  @pytest.fixture(scope="session")
  def expected_toc_data():
      """픽스처: TOC 추출 결과 비교용 데이터"""

  @pytest.fixture(scope="session") 
  def real_toc_data():
      """픽스처: AI 분석 입력용 실제 목차 데이터"""

  1.2 스키마 정의 파일 작성

  # tests/schemas/stage_schemas.py
  @dataclass
  class WorkspacePreparationOutput:
      success: bool
      data: Dict[str, Any]
      error: Optional[str]

      @classmethod
      def validate(cls, result: Dict[str, Any]) -> bool:
          """결과 데이터 스키마 검증"""

  Phase 2: 데이터 생성 테스트 구현

  2.1 데이터 생성 테스트 파일

  # test_workspace_preparation_data_generation.py
  async def test_generate_workspace_data():
      """실제 PDF로 데이터 생성 → 픽스처 저장"""
      # 1. 실제 WorkspacePreparationStage 실행
      # 2. 전체 결과 저장
      # 3. 메인 테스트용 개별 데이터 저장:
      #    - toc_data.json (TOC 추출 결과)  
      #    - toc_structure.json (AI 분석 입력용)
      #    - chapters_analysis.json (AI 분석 결과)

  Phase 3: 메인 로직 테스트 구현

  3.1 메인 테스트 파일

  # test_workspace_preparation.py

  async def test_extract_toc_from_pdf_logic(real_pdf_path, expected_toc_data):
      """PDF → TOC 추출 결과가 픽스처와 동일한지 검증"""
      stage = WorkspacePreparationStage(config_manager, test_logger)
      result = await stage.extract_toc_from_pdf(real_pdf_path)

      # 픽스처 데이터와 비교
      assert result['data']['toc_structure'] == expected_toc_data['toc_structure']

  async def test_analyze_chapters_with_ai_logic(real_toc_data):
      """실제 목차 → AI 분석 결과 구조 검증"""
      stage = WorkspacePreparationStage(config_manager, test_logger)
      result = await stage.analyze_chapters_with_ai(real_toc_data)

      # 결과 구조 검증
      assert result['success'] is True
      assert 'chapters_info' in result
      assert len(result['chapters_info']) > 0

  def test_create_output_directories_logic():
      """디렉토리 생성 로직 검증"""

  def test_save_toc_file_logic():
      """TOC 파일 저장 로직 검증"""

  def test_create_chapter_folders_logic():
      """장별 폴더 생성 로직 검증"""

  Phase 4: 자동 갱신 시스템

  4.1 --regen-fixtures 구현

  # conftest.py에 추가
  def regenerate_test_data():
      """테스트 데이터 자동 재생성"""
      # WorkspacePreparationStage 실행
      # 픽스처 데이터 갱신

  Phase 5: WorkspacePreparationStage 수정

  5.1 하이브리드 반환 구조 구현

  # workspace_preparation_v2.py 수정
  async def process(self, input_data):
      # 기존 로직 유지 (폴더/파일 생성)
      # ...

      # 🟢 추가: 생성된 데이터를 메모리로 반환
      chapters_data = []
      for folder_info in created_folders:
          toc_data = json.load(open(folder_info['toc_file']))
          content_data = open(folder_info['content_file']).read()
          chapters_data.append({
              'toc_structure': toc_data,
              'content_text': content_data,
              'metadata': folder_info
          })

      return {
          'success': True,
          'data': {
              'book_metadata': {...},
              'chapters_data': chapters_data
          },
          'error': None
      }

  📁 생성될 파일 구조

  tests/
  ├── conftest.py                                    # ✏️ 수정
  ├── schemas/
  │   └── stage_schemas.py                           # 🆕 생성
  ├── fixtures/
  │   └── pdfs/
  │       └── sample_book.pdf                        # 📄 사용자 제공
  ├── data/
  │   └── workspace_preparation/
  │       ├── workspace_preparation_output.json      # 📊 생성
  │       ├── toc_data.json                         # 📊 생성
  │       ├── toc_structure.json                    # 📊 생성
  │       └── chapters_analysis.json                # 📊 생성
  ├── test_workspace_preparation_data_generation.py  # 🆕 생성
  └── test_workspace_preparation.py                  # 🆕 생성

  🚀 실행 방법

  # 1단계: 데이터 생성 (PDF 제공 후)
  pytest test_workspace_preparation_data_generation.py

  # 2단계: 로직 테스트 
  pytest test_workspace_preparation.py

  # 자동 갱신
  pytest --regen-fixtures

  📝 다음 즉시 작업

  1. fixtures/pdfs 폴더 생성
  2. conftest.py fixture 추가
  3. 스키마 정의 파일 작성
  4. 데이터 생성 테스트 파일 기본 구조 작성