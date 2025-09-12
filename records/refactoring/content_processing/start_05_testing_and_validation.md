# 테스트 및 검증 가이드

## 1. 테스트 환경 구성

### 1.1 테스트 데이터 준비

#### 1.1.1 원본 테스트 경로
```
/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming
```

#### 1.1.2 테스트용 파일 목록

**리프 노드들** (구성 섹션 비어있음):
- `17_lev3_1.1.1_The_design_phase_info.md`
- `18_lev3_1.1.2_UML_101_info.md`  
- `19_lev3_1.1.3_Explaining_each_piece_of_the_class_diagram_info.md`
- `20_lev3_1.1.4_The_implementation_phase_info.md`

**부모 노드** (구성 섹션에 위 4개 파일명 포함):
- `16_lev2_1.1_OOP_design_Classic_or_classical_info.md`

#### 1.1.3 TOC 파일
- `1_Complexity_of_object_oriented_programming_toc.json`
- JSON 구조: `[{"id": 16, "title": "1.1 OOP design: Classic or classical?", "level": 2, ...}, ...]`

### 1.2 ContentProcessingStageTester 클래스

#### 1.2.1 임시 디렉터리 기반 테스트 환경
```python
class ContentProcessingStageTester:
    """ContentProcessingStage 안전 테스트 클래스"""
    
    def __init__(self, original_chapter_path: str, config: Dict, ai_service):
        self.original_chapter_path = Path(original_chapter_path)
        self.config = config
        self.ai_service = ai_service
        self.test_temp_dir = None
        self.test_chapter_dir = None
        
    def setup_test_environment(self, selected_files: List[str] = None):
        """테스트 환경 구성 - 원본 파일들을 임시 디렉터리로 복사"""
        self.test_temp_dir = tempfile.mkdtemp(prefix="content_processing_test_")
        print(f"📁 테스트 임시 디렉터리 생성: {self.test_temp_dir}")
        
        # 디렉터리 구조 생성 및 파일 복사
        chapter_name = self.original_chapter_path.name
        self.test_chapter_dir = Path(self.test_temp_dir) / chapter_name
        test_unified_dir = self.test_chapter_dir / "unified_info_docs"
        test_unified_dir.mkdir(parents=True)
        
        # 선택된 파일들 복사
        if selected_files:
            for file_name in selected_files:
                src = self.original_chapter_path / "unified_info_docs" / file_name
                dst = test_unified_dir / file_name
                if src.exists():
                    shutil.copy2(src, dst)
                    print(f"  ✅ 복사: {file_name}")
        
        # TOC 파일 복사
        toc_file = self.original_chapter_path / f"{chapter_name}_toc.json"
        if toc_file.exists():
            shutil.copy2(toc_file, self.test_chapter_dir / f"{chapter_name}_toc.json")
        
        return str(self.test_chapter_dir)
```

#### 1.2.2 원본 보호 메커니즘
- 모든 작업을 임시 디렉터리에서 수행
- 원본 파일에 대한 읽기 전용 접근
- 테스트 완료 후 사용자가 직접 정리

#### 1.2.3 수동 정리 방식
```python
def cleanup_test_environment(self):
    """테스트 환경 정리 - 사용자가 직접 호출"""
    if self.test_temp_dir and Path(self.test_temp_dir).exists():
        shutil.rmtree(self.test_temp_dir)
        print(f"🗑️ 임시 디렉터리 삭제 완료: {self.test_temp_dir}")
        self.test_temp_dir = None
        self.test_chapter_dir = None

# 사용법:
# tester.cleanup_test_environment()  # 사용자가 확인 후 직접 호출
```

## 2. 단계별 테스트 시나리오

### 2.1 1단계: 기본 추출 테스트 (test_01_basic_extraction)

#### 2.1.1 대상
- 단일 리프 노드: `17_lev3_1.1.1_The_design_phase_info.md`

#### 2.1.2 테스트 시나리오
```python
async def test_01_basic_extraction(self):
    """1단계: 기본 추출 테스트"""
    try:
        # 테스트 환경 구성
        test_files = ["17_lev3_1.1.1_The_design_phase_info.md"]
        test_chapter = self.setup_test_environment(test_files)
        
        # ContentProcessingStage 생성 및 테스트
        stage = ContentProcessingStage(self.config, self.ai_service)
        test_doc_path = Path(test_chapter) / "unified_info_docs" / test_files[0]
        
        # 1. 문서 파싱
        doc_data = await stage.parse_unified_document(str(test_doc_path))
        
        # 2. 추출 작업
        extraction_result = await stage.generate_extract_section(doc_data)
        
        # 3. 파일 업데이트
        formatted_content = stage.format_extraction_content(extraction_result)
        await stage.update_extraction_section(str(test_doc_path), formatted_content)
        
        print("✅ 1단계 테스트 완료")
        print(f"📁 테스트 결과 확인: {test_chapter}")
        print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

#### 2.1.3 검증 포인트
- **추출 섹션에 5개 정보 타입 생성**: 핵심 내용, 상세 핵심 내용, 상세 정보, 주요 화제, 부차 화제
- **상태 마킹 없음**: 추출 작업 시에는 마킹 없이 내용만 삽입
- **내용이 추출 섹션 바로 밑에 시작**: `# 추출\n---\n` 다음에 바로 추출된 내용

#### 2.1.4 수동 확인 방법
```python
# 테스트 파일 확인
with open(test_doc_path, 'r') as f:
    content = f.read()
    print("=== 업데이트된 추출 섹션 ===")
    extraction_section = re.search(r'# 추출\n---\n(.*?)(?=\n# 내용)', content, re.DOTALL)
    if extraction_section:
        print(extraction_section.group(1)[:500] + "...")
```

### 2.2 2단계: 부모-자식 관계 처리 (test_02_parent_child_processing)

#### 2.2.1 대상
- 구성 노드 4개 + 부모 노드 1개 (총 5개 파일)

#### 2.2.2 처리 순서
1. **구성 노드들 추출 작업** (리프 노드 4개)
2. **부모 노드 추출 작업**  
3. **부모 노드에 구성 노드 반영** → `<구성 노드 반영 완료>` 마킹
4. **구성 노드들에 부모 노드 반영** → `<부모 노드 반영 완료>` 마킹

#### 2.2.3 테스트 시나리오
```python
async def test_02_parent_child_processing(self):
    """2단계: 부모-자식 관계 처리 테스트"""
    try:
        test_files = [
            "17_lev3_1.1.1_The_design_phase_info.md",
            "18_lev3_1.1.2_UML_101_info.md", 
            "19_lev3_1.1.3_Explaining_each_piece_of_the_class_diagram_info.md",
            "20_lev3_1.1.4_The_implementation_phase_info.md",
            "16_lev2_1.1_OOP_design_Classic_or_classical_info.md"  # 부모 노드
        ]
        test_chapter = self.setup_test_environment(test_files)
        
        stage = ContentProcessingStage(self.config, self.ai_service)
        test_unified_dir = Path(test_chapter) / "unified_info_docs"
        
        # 1. 구성 노드들 추출 작업
        composition_files = test_files[:-1]
        for comp_file in composition_files:
            comp_path = test_unified_dir / comp_file
            comp_doc = await stage.parse_unified_document(str(comp_path))
            extraction = await stage.generate_extract_section(comp_doc)
            formatted_content = stage.format_extraction_content(extraction)
            await stage.update_extraction_section(str(comp_path), formatted_content)
        
        # 2. 부모 노드 처리
        parent_file = test_files[-1]
        parent_path = test_unified_dir / parent_file
        parent_doc = await stage.parse_unified_document(str(parent_path))
        parent_extraction = await stage.generate_extract_section(parent_doc)
        formatted_parent_content = stage.format_extraction_content(parent_extraction)
        await stage.update_extraction_section(str(parent_path), formatted_parent_content)
        
        # 3. 부모 노드에 구성 노드 내용 반영
        await stage.update_current_extraction_section(parent_doc, parent_extraction)
        await stage.add_update_status_mark(str(parent_path), "<구성 노드 반영 완료>")
        
        # 4. 구성 노드들에 부모 노드 내용 반영
        await stage.update_composition_extraction_sections(parent_doc, parent_extraction)
        for comp_file in composition_files:
            comp_path = test_unified_dir / comp_file
            await stage.add_update_status_mark(str(comp_path), "<부모 노드 반영 완료>")
        
        print("✅ 2단계 테스트 완료")
        print(f"📁 테스트 결과 확인: {test_chapter}")
        print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

#### 2.2.4 검증 포인트
- **모든 파일의 추출 섹션에 5개 정보 타입 생성됨**
- **구성 노드들**: `<부모 노드 반영 완료>` 마킹 확인
- **부모 노드**: `<구성 노드 반영 완료>` 마킹 확인  
- **구성 노드들의 주요/부차 화제가 보존됨** (핵심 3개 섹션만 업데이트)
- **부모 노드가 구성 내용을 종합하여 개선됨**

### 2.3 3단계: 문서 정렬 테스트 (test_03_document_sorting)

#### 2.3.1 대상
- 전체 통합 문서 (모든 `*_info.md` 파일)

#### 2.3.2 자동 검증
```python
async def test_03_document_sorting(self):
    """3단계: 문서 정렬 테스트"""
    try:
        test_chapter = self.setup_test_environment()  # 모든 파일 복사
        stage = ContentProcessingStage(self.config, self.ai_service)
        
        # 문서 정렬 실행
        sorted_groups = await stage.load_and_sort_documents(test_chapter)
        
        # 검증: 첫 번째 그룹이 리프 노드들인지
        leaf_group = sorted_groups[0]
        for doc in leaf_group:
            assert not doc.get('composition_files', []), f"리프 노드가 아님: {doc['title']}"
        
        # 검증: 나머지 그룹들이 level 내림차순인지
        if len(sorted_groups) > 1:
            for i in range(1, len(sorted_groups)-1):
                if sorted_groups[i] and sorted_groups[i+1]:
                    current_level = sorted_groups[i][0].get('level', 0)
                    next_level = sorted_groups[i+1][0].get('level', 0)
                    assert current_level >= next_level, f"정렬 오류: level {current_level} → {next_level}"
        
        print("✅ 3단계 테스트 완료 - 자동 검증 통과")
        print(f"📁 테스트 결과 확인: {test_chapter}")
        print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

#### 2.3.3 출력 형식 및 확인 방법
```python
# 정렬 결과 출력
print(f"📋 총 {len(sorted_groups)}개 그룹으로 정렬됨:")
for i, group in enumerate(sorted_groups):
    if i == 0:
        print(f"  그룹 {i+1} (리프 노드): {len(group)}개")
        for doc in group:
            print(f"    - {doc.get('title', 'N/A')} (level: {doc.get('level', 'N/A')})")
    else:
        if group:
            level = group[0].get('level', 0)
            print(f"  그룹 {i+1} (Level {level}): {len(group)}개")
            for doc in group:
                comp_count = len(doc.get('composition_files', []))
                print(f"    - {doc.get('title', 'N/A')} (구성: {comp_count}개)")
```

### 2.4 4단계: 제한적 목차 생성 (test_04_limited_toc_generation)

#### 2.4.1 대상
- 선별된 문서들 (2단계에서 사용한 것과 동일)

#### 2.4.2 목차 생성 프로세스
1. 제한된 파일들로 테스트 환경 구성
2. 간단한 추출 작업 수행 (목차 생성을 위해)
3. 개선된 목차 MD 파일 생성
4. 생성된 파일 확인

#### 2.4.3 테스트 시나리오
```python
async def test_04_limited_toc_generation(self):
    """4단계: 제한적 목차 생성 테스트"""
    try:
        test_files = [
            "17_lev3_1.1.1_The_design_phase_info.md",
            "18_lev3_1.1.2_UML_101_info.md", 
            "16_lev2_1.1_OOP_design_Classic_or_classical_info.md"
        ]
        test_chapter = self.setup_test_environment(test_files)
        stage = ContentProcessingStage(self.config, self.ai_service)
        
        # 추출 작업 (목차 생성을 위해)
        test_unified_dir = Path(test_chapter) / "unified_info_docs"
        for test_file in test_files:
            file_path = test_unified_dir / test_file
            doc_data = await stage.parse_unified_document(str(file_path))
            extraction_result = await stage.generate_extract_section(doc_data)
            formatted_content = stage.format_extraction_content(extraction_result)
            await stage.update_extraction_section(str(file_path), formatted_content)
        
        # 목차 생성
        await stage.generate_enhanced_toc_file(test_chapter)
        
        # 생성된 파일 확인
        chapter_name = Path(test_chapter).name
        toc_file = Path(test_chapter) / f"{chapter_name}_enhanced_toc.md"
        
        if toc_file.exists():
            print(f"✅ 목차 파일 생성됨: {toc_file}")
            with open(toc_file, 'r') as f:
                content = f.read()
                print("📖 목차 파일 미리보기:")
                print(content[:500] + "...")
        
        print("✅ 4단계 테스트 완료")
        print(f"📁 테스트 결과 확인: {test_chapter}")
        print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

#### 2.4.4 검증 포인트
- **level에 따른 헤더 개수 정확성**: level 2 → `##`, level 3 → `###`
- **헤더 바로 밑에 추출 섹션 내용 삽입됨**: 줄바꿈 없이 바로 연결
- **각 문서별 적절한 구분과 포맷팅**: 섹션 간 빈 줄 2개로 구분
- **파일 생성 위치**: `{chapter_name}_enhanced_toc.md`

## 3. 디버깅 및 문제 해결

### 3.1 주요 체크포인트
```python
# 문서 파싱 검증
print(f"📊 파싱된 문서: {doc_data.get('title', 'N/A')}")
print(f"📝 level: {doc_data.get('level', 'N/A')}")
print(f"🔗 구성 파일 수: {len(doc_data.get('composition_files', []))}")

# 추출 결과 검증  
print(f"📋 추출된 섹션 수: {len([k for k, v in extraction_result.items() if v.strip()])}/5")

# 상태 마킹 검증
with open(file_path, 'r') as f:
    content = f.read()
    if '<구성 노드 반영 완료>' in content:
        print("✅ 부모 노드 상태 마킹 확인")
    if '<부모 노드 반영 완료>' in content:
        print("✅ 구성 노드 상태 마킹 확인")
```

### 3.2 일반적인 문제 패턴

#### 3.2.1 파일 파싱 실패
```python
# 증상: doc_data가 None이거나 불완전한 정보
# 원인: 정규표현식 패턴 불일치, 파일 형식 변경
# 해결: 실제 파일 내용과 정규표현식 패턴 확인
```

#### 3.2.2 AI 응답 파싱 오류
```python
# 증상: 추출된 섹션이 비어있거나 형식 오류
# 원인: AI 응답 형식 변경, 섹션 헤더 불일치
# 해결: 응답 내용 직접 확인, 파싱 로직 검증
```

#### 3.2.3 상태 마킹 위치 오류
```python
# 증상: 마킹이 잘못된 위치에 삽입됨
# 원인: 정규표현식 패턴 오류, 파일 구조 변경
# 해결: 마킹 전후 파일 내용 비교, 정규표현식 테스트
```

#### 3.2.4 목차 생성 실패
```python
# 증상: 목차 파일 생성되지 않거나 내용 누락
# 원인: TOC 파일 매칭 실패, 문서 제목 불일치
# 해결: TOC 구조와 문서 제목 매칭 확인
```

### 3.3 문제 해결 가이드

#### 3.3.1 단계별 진단 방법
```python
# 1. 파일 존재 여부 확인
assert os.path.exists(test_doc_path), f"파일 없음: {test_doc_path}"

# 2. 문서 파싱 확인
doc_data = await stage.parse_unified_document(str(test_doc_path))
assert doc_data is not None, "문서 파싱 실패"
assert doc_data.get('title'), "제목 추출 실패"

# 3. AI 호출 확인
try:
    extraction_result = await stage.generate_extract_section(doc_data)
    assert extraction_result, "AI 추출 실패"
except Exception as e:
    print(f"AI 호출 오류: {e}")

# 4. 파일 업데이트 확인
await stage.update_extraction_section(str(test_doc_path), formatted_content)
with open(test_doc_path, 'r') as f:
    updated_content = f.read()
    assert '## 핵심 내용' in updated_content, "추출 내용 삽입 실패"
```

#### 3.3.2 로그 분석 기법
```python
# 로그 필터링
grep "ERROR" content_processing.log
grep "⚠️" content_processing.log  
grep "API 호출" content_processing.log

# 성능 분석
grep "처리 시간" content_processing.log
grep "API 호출 횟수" content_processing.log
```

#### 3.3.3 수동 검증 방법
```python
# 추출 섹션 수동 확인
def manual_verify_extraction(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# 내용)', content, re.DOTALL)
    if extraction_match:
        extraction_content = extraction_match.group(1)
        sections = ['## 핵심 내용', '## 상세 핵심 내용', '## 상세 정보', '## 주요 화제', '## 부차 화제']
        found_sections = [s for s in sections if s in extraction_content]
        print(f"발견된 섹션: {len(found_sections)}/5개")
        return len(found_sections) >= 3
    return False
```

#### 3.3.4 복구 절차
```python
# 테스트 실패 시 복구 절차
try:
    # 테스트 실행
    await test_function()
except Exception as e:
    print(f"테스트 실패: {e}")
    
    # 1. 임시 디렉터리 보존 (분석용)
    print(f"분석용 임시 디렉터리 보존: {tester.test_temp_dir}")
    
    # 2. 로그 확인
    print("로그 파일 확인:")
    os.system("tail -20 content_processing.log")
    
    # 3. 수동 정리는 사용자 선택
    choice = input("임시 디렉터리를 삭제하시겠습니까? (y/n): ")
    if choice.lower() == 'y':
        tester.cleanup_test_environment()
```

## 4. 테스트 실행 방법

### 4.1 전체 테스트 실행
```bash
# 메인 테스트 실행
python test_content_processing_stage.py

# 또는 asyncio로 직접 실행
python -c "
import asyncio
from test_content_processing_stage import run_all_tests
asyncio.run(run_all_tests())
"
```

### 4.2 단계별 테스트 실행
```python
# 개별 테스트 실행 예시
async def run_single_test():
    config = load_test_config()
    ai_service = create_test_ai_service(config)
    original_path = "/path/to/test/chapter"
    
    tester = ContentProcessingStageTester(original_path, config, ai_service)
    
    # 1단계만 실행
    await tester.test_01_basic_extraction()
    # 확인 후 정리
    tester.cleanup_test_environment()

asyncio.run(run_single_test())
```

### 4.3 테스트 결과 활용
```python
# 테스트 성공 시
print("🎉 모든 테스트 완료!")
print("✅ 원본 파일들은 전혀 변경되지 않았습니다.")
print("📁 임시 테스트 결과는 자동 정리되었습니다.")

# 테스트 실패 시  
print("❌ 테스트 중 오류 발생")
print("🔍 임시 디렉터리에서 결과 확인 후 수동 정리하세요")
print(f"📁 임시 디렉터리: {tester.test_temp_dir}")
```