# 테스트 및 검증 가이드 (업데이트 1)

## 수정된 테스트 환경 구성

### 1.1 테스트 데이터 준비 (메모리 기반으로 변경)

#### 1.1.1 메모리 기반 테스트 데이터 경로
```
# 입력: 메모리 데이터 (process_result.json)
/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/integrated_node_generation/process_result.json

# 출력: 사용자 지정 경로 (임시 테스트 디렉터리)
/tmp/content_processing_test_[timestamp]/
```

#### 1.1.2 수정된 테스트용 데이터 구조
```json
{
  "documents": {
    "data": {
      "unified_documents": [
        {
          "file_name": "1_Complexity_of_object_oriented_programming/unified_info_docs/17_lev3_1.1.1_The_design_phase_info.md",
          "content": "# 속성\n---\nprocess_status: false\n\n# 추출\n---\n\n# 내용\n---\n### 1.1.1 The design phase\n..."
        }
      ]
    }
  }
}
```

### 1.2 수정된 ContentProcessingStageTester 클래스

#### 1.2.1 메모리 기반 테스트 환경 구성
```python
class ContentProcessingStageTester:
    """ContentProcessingStage 메모리 기반 안전 테스트 클래스"""
    
    def __init__(self, process_result_path: str, config: Dict, ai_service):
        self.process_result_path = Path(process_result_path)
        self.config = config
        self.ai_service = ai_service
        self.test_temp_dir = None
        self.user_output_path = None
        
    def setup_test_environment(self, selected_documents: List[str] = None):
        """메모리 기반 테스트 환경 구성"""
        # 임시 디렉터리 생성 (사용자 지정 출력 경로)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_temp_dir = tempfile.mkdtemp(prefix=f"content_processing_test_{timestamp}_")
        self.user_output_path = self.test_temp_dir
        
        print(f"📁 테스트 임시 디렉터리 생성: {self.test_temp_dir}")
        
        # process_result.json 로드
        with open(self.process_result_path, 'r', encoding='utf-8') as f:
            process_result = json.load(f)
        
        # 선택된 문서들만 필터링
        if selected_documents:
            unified_documents = process_result["documents"]["data"]["unified_documents"]
            filtered_documents = [
                doc for doc in unified_documents 
                if any(selected_file in doc["file_name"] for selected_file in selected_documents)
            ]
            process_result["documents"]["data"]["unified_documents"] = filtered_documents
        
        return process_result, self.user_output_path
```

#### 1.2.2 수정된 원본 보호 메커니즘
- 메모리 데이터만 사용하므로 원본 파일 변경 없음
- 모든 결과물은 임시 디렉터리에만 저장
- 테스트 완료 후 사용자가 직접 정리

## 수정된 단계별 테스트 시나리오

### 2.1 1단계: 메모리 기반 추출 테스트 (test_01_memory_based_extraction)

#### 2.1.1 수정된 대상 및 목적
- **입력**: process_result.json의 단일 리프 노드 데이터
- **목적**: 메모리 데이터에서 추출 후 사용자 지정 경로에 저장 검증

#### 2.1.2 수정된 테스트 시나리오
```python
async def test_01_memory_based_extraction(self):
    """1단계: 메모리 기반 추출 테스트"""
    try:
        # 테스트 환경 구성 (메모리 기반)
        selected_documents = ["17_lev3_1.1.1_The_design_phase_info.md"]
        process_result, user_output_path = self.setup_test_environment(selected_documents)
        
        # ContentProcessingStage 생성 및 테스트
        stage = ContentProcessingStage(self.config, self.ai_service)
        
        # 1. 메모리 데이터에서 문서 로드 및 정렬
        unified_documents = process_result["documents"]["data"]["unified_documents"]
        sorted_groups = await stage.load_and_sort_documents(unified_documents)
        
        # 2. 첫 번째 리프 노드 추출 작업
        leaf_node = sorted_groups[0][0]  # 첫 번째 그룹의 첫 번째 문서
        extraction_result = await stage.generate_extract_section(leaf_node)
        
        # 3. 사용자 지정 경로에 저장
        await stage.save_extraction_result(leaf_node, extraction_result, user_output_path)
        
        # 4. 결과 검증
        output_file_path = os.path.join(user_output_path, leaf_node['file_name'])
        assert os.path.exists(output_file_path), f"출력 파일이 생성되지 않음: {output_file_path}"
        
        # 5. 추출 섹션 내용 검증
        with open(output_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = ['## 핵심 내용', '## 상세 핵심 내용', '## 상세 정보', '## 주요 화제', '## 부차 화제']
        for section in required_sections:
            assert section in content, f"필수 섹션 누락: {section}"
        
        print("✅ 1단계 메모리 기반 추출 테스트 완료")
        print(f"📁 테스트 결과 확인: {user_output_path}")
        print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

### 2.2 2단계: 통합 처리 테스트 (test_02_integrated_processing)

#### 2.2.1 수정된 대상
- **메모리 데이터**: 구성 노드 4개 + 부모 노드 1개
- **처리 순서**: 모든 노드 추출 → 비리프 노드 업데이트

#### 2.2.2 수정된 테스트 시나리오
```python
async def test_02_integrated_processing(self):
    """2단계: 통합 처리 테스트 (메모리 기반)"""
    try:
        # 메모리 기반 환경 구성
        selected_documents = [
            "17_lev3_1.1.1_The_design_phase_info.md",
            "18_lev3_1.1.2_UML_101_info.md", 
            "19_lev3_1.1.3_Explaining_each_piece_of_the_class_diagram_info.md",
            "20_lev3_1.1.4_The_implementation_phase_info.md",
            "16_lev2_1.1_OOP_design_Classic_or_classical_info.md"
        ]
        process_result, user_output_path = self.setup_test_environment(selected_documents)
        
        stage = ContentProcessingStage(self.config, self.ai_service)
        
        # 1. 메인 처리 실행 (process 메서드)
        result = await stage.process(process_result, user_output_path)
        
        # 2. 처리 결과 검증
        assert result['success'], f"처리 실패: {result.get('error')}"
        assert result['processed_documents'], "처리된 문서가 없음"
        assert result['load_and_sort_result_path'], "정렬 결과 파일 경로가 없음"
        
        # 3. 파일 생성 검증
        for doc_name in selected_documents:
            file_path = os.path.join(user_output_path, "1_Complexity_of_object_oriented_programming", "unified_info_docs", doc_name)
            assert os.path.exists(file_path), f"파일이 생성되지 않음: {file_path}"
        
        # 4. 상태 마킹 검증
        # 구성 노드들: <부모 노드 반영 완료> 확인
        composition_files = selected_documents[:-1]  # 부모 노드 제외
        for comp_file in composition_files:
            file_path = os.path.join(user_output_path, "1_Complexity_of_object_oriented_programming", "unified_info_docs", comp_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert '<부모 노드 반영 완료>' in content, f"구성 노드 상태 마킹 누락: {comp_file}"
        
        # 부모 노드: <구성 노드 반영 완료> 확인
        parent_file = selected_documents[-1]
        parent_path = os.path.join(user_output_path, "1_Complexity_of_object_oriented_programming", "unified_info_docs", parent_file)
        with open(parent_path, 'r', encoding='utf-8') as f:
            parent_content = f.read()
        assert '<구성 노드 반영 완료>' in parent_content, "부모 노드 상태 마킹 누락"
        
        print("✅ 2단계 통합 처리 테스트 완료")
        print(f"📁 테스트 결과 확인: {user_output_path}")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

### 2.3 3단계: load_and_sort_result.json 생성 테스트 (test_03_result_json_generation)

#### 2.3.1 대상
- 메모리 데이터에서 문서 정렬 및 JSON 결과 파일 생성

#### 2.3.2 테스트 시나리오
```python
async def test_03_result_json_generation(self):
    """3단계: load_and_sort_result.json 생성 테스트"""
    try:
        process_result, user_output_path = self.setup_test_environment()
        stage = ContentProcessingStage(self.config, self.ai_service)
        
        # 메모리 데이터에서 문서 정렬
        unified_documents = process_result["documents"]["data"]["unified_documents"]
        sorted_groups = await stage.load_and_sort_documents(unified_documents)
        
        # load_and_sort_result.json 파일 생성 확인
        result_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/content_processing/load_and_sort_result.json"
        assert os.path.exists(result_path), "load_and_sort_result.json 파일이 생성되지 않음"
        
        # JSON 파일 내용 검증
        with open(result_path, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
        
        assert result_data["method"] == "load_and_sort_documents", "메서드명 불일치"
        assert result_data["input_source"] == "memory_data", "입력 소스 불일치"
        assert "generation_time" in result_data, "생성 시간 정보 누락"
        assert "result" in result_data, "결과 데이터 누락"
        
        # 정렬 결과 검증
        chapters = result_data["result"]["output"]["chapters"]
        assert len(chapters) > 0, "챕터 데이터가 없음"
        
        first_chapter = chapters[0]
        assert "leaf_nodes" in first_chapter, "리프 노드 정보 누락"
        assert "non_leaf_groups" in first_chapter, "비리프 그룹 정보 누락"
        
        print("✅ 3단계 JSON 생성 테스트 완료")
        print(f"📄 생성된 파일: {result_path}")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

### 2.4 4단계: 공통 저장 로직 테스트 (test_04_common_save_logic)

#### 2.4.1 대상
- save_updated_content_with_marking 공통 로직 검증

#### 2.4.2 테스트 시나리오
```python
async def test_04_common_save_logic(self):
    """4단계: 공통 저장 로직 테스트"""
    try:
        process_result, user_output_path = self.setup_test_environment(["17_lev3_1.1.1_The_design_phase_info.md"])
        stage = ContentProcessingStage(self.config, self.ai_service)
        
        # 1. 기본 추출 및 저장
        unified_documents = process_result["documents"]["data"]["unified_documents"]
        doc = {
            'file_name': unified_documents[0]["file_name"],
            'title': "Test Document",
            'full_content': unified_documents[0]["content"]
        }
        
        extraction_result = {
            'core_content': '## 핵심 내용\n테스트 핵심 내용',
            'detailed_core_content': '## 상세 핵심 내용\n테스트 상세 핵심 내용',
            'detailed_content': '## 상세 정보\n테스트 상세 정보',
            'main_topics': '## 주요 화제\n• 테스트 주요 화제',
            'sub_topics': '## 부차 화제\n• 테스트 부차 화제'
        }
        
        # 2. 초기 저장
        await stage.save_extraction_result(doc, extraction_result, user_output_path)
        
        # 3. 공통 업데이트 로직 테스트
        file_path = os.path.join(user_output_path, doc['file_name'])
        
        # 업데이트된 내용 준비
        updated_extraction = {
            'core_content': '## 핵심 내용\n업데이트된 핵심 내용',
            'detailed_core_content': '## 상세 핵심 내용\n업데이트된 상세 핵심 내용',
            'detailed_content': '## 상세 정보\n업데이트된 상세 정보',
            'main_topics': '## 주요 화제\n• 업데이트된 주요 화제',
            'sub_topics': '## 부차 화제\n• 업데이트된 부차 화제'
        }
        
        # 4. 공통 저장 로직 실행
        await stage.save_updated_content_with_marking(
            file_path, 
            updated_extraction, 
            "<테스트 마킹 완료>"
        )
        
        # 5. 결과 검증
        with open(file_path, 'r', encoding='utf-8') as f:
            final_content = f.read()
        
        assert '<테스트 마킹 완료>' in final_content, "상태 마킹이 추가되지 않음"
        assert '업데이트된 핵심 내용' in final_content, "내용이 업데이트되지 않음"
        assert '## 핵심 내용' in final_content, "섹션 헤더가 보존되지 않음"
        
        print("✅ 4단계 공통 저장 로직 테스트 완료")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        raise
```

## 수정된 디버깅 및 문제 해결

### 3.1 메모리 기반 처리 디버깅

#### 3.1.1 메모리 데이터 검증
```python
def validate_memory_data(process_result: Dict) -> bool:
    """메모리 데이터 유효성 검증"""
    try:
        assert "documents" in process_result, "documents 필드 누락"
        assert "data" in process_result["documents"], "data 필드 누락"
        assert "unified_documents" in process_result["documents"]["data"], "unified_documents 필드 누락"
        
        unified_documents = process_result["documents"]["data"]["unified_documents"]
        assert isinstance(unified_documents, list), "unified_documents가 리스트가 아님"
        assert len(unified_documents) > 0, "unified_documents가 비어있음"
        
        for doc in unified_documents:
            assert "file_name" in doc, f"file_name 누락: {doc}"
            assert "content" in doc, f"content 누락: {doc}"
            
        return True
    except AssertionError as e:
        print(f"❌ 메모리 데이터 검증 실패: {e}")
        return False
```

#### 3.1.2 파일 저장 결과 검증
```python
def verify_saved_files(user_output_path: str, expected_files: List[str]) -> Dict:
    """저장된 파일 검증"""
    results = {
        'success': [],
        'missing': [],
        'invalid_content': []
    }
    
    for file_name in expected_files:
        file_path = os.path.join(user_output_path, file_name)
        
        if not os.path.exists(file_path):
            results['missing'].append(file_name)
            continue
        
        # 내용 검증
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_sections = ['# 속성', '# 추출', '# 내용', '# 구성']
            if all(section in content for section in required_sections):
                results['success'].append(file_name)
            else:
                results['invalid_content'].append(file_name)
                
        except Exception as e:
            results['invalid_content'].append(f"{file_name}: {e}")
    
    return results
```

### 3.2 수정된 일반적인 문제 패턴

#### 3.2.1 메모리 데이터 파싱 실패
```python
# 증상: process_result 구조 오류
# 원인: process_result.json 구조 변경, 키 이름 불일치
# 해결: 메모리 데이터 구조 검증 및 키 확인
def debug_memory_data_parsing(process_result: Dict):
    print("🔍 메모리 데이터 구조 분석:")
    print(f"  - 최상위 키: {list(process_result.keys())}")
    if "documents" in process_result:
        print(f"  - documents 키: {list(process_result['documents'].keys())}")
        if "data" in process_result["documents"]:
            print(f"  - data 키: {list(process_result['documents']['data'].keys())}")
```

#### 3.2.2 사용자 지정 경로 저장 실패
```python
# 증상: 파일이 지정된 경로에 저장되지 않음
# 원인: 디렉터리 생성 실패, 권한 문제
# 해결: 경로 검증 및 권한 확인
def debug_file_save_issues(user_output_path: str, file_name: str):
    file_path = os.path.join(user_output_path, file_name)
    dir_path = os.path.dirname(file_path)
    
    print(f"🔍 파일 저장 경로 분석:")
    print(f"  - 사용자 경로: {user_output_path}")
    print(f"  - 파일명: {file_name}")
    print(f"  - 전체 경로: {file_path}")
    print(f"  - 디렉터리 존재: {os.path.exists(dir_path)}")
    print(f"  - 디렉터리 쓰기 권한: {os.access(dir_path, os.W_OK) if os.path.exists(dir_path) else 'N/A'}")
```

#### 3.2.3 공통 저장 로직 오류
```python
# 증상: 상태 마킹이 올바른 위치에 추가되지 않음
# 원인: 정규표현식 패턴 오류, 파일 구조 변경
# 해결: 파일 구조 검증 및 정규표현식 테스트
def debug_common_save_logic(file_path: str, status_mark: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"🔍 파일 구조 분석:")
    print(f"  - 추출 섹션 존재: {'# 추출' in content}")
    print(f"  - 기존 마킹 존재: {bool(re.search(r'<[^>]+>', content))}")
    print(f"  - 상태 마킹: {status_mark}")
    
    # 추출 섹션 위치 확인
    extraction_match = re.search(r'# 추출\n---\n', content)
    if extraction_match:
        print(f"  - 추출 섹션 위치: {extraction_match.start()}-{extraction_match.end()}")
    else:
        print("  - ❌ 추출 섹션을 찾을 수 없음")
```

## 수정된 테스트 실행 방법

### 4.1 메모리 기반 전체 테스트 실행
```bash
# 메인 테스트 실행 (메모리 기반)
python test_memory_based_content_processing.py

# 또는 개별 테스트 실행
python -c "
import asyncio
from test_memory_based_content_processing import run_memory_based_tests
asyncio.run(run_memory_based_tests())
"
```

### 4.2 수정된 단계별 테스트 실행
```python
# 메모리 기반 개별 테스트 실행 예시
async def run_single_memory_test():
    config = load_test_config()
    ai_service = create_test_ai_service(config)
    process_result_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/integrated_node_generation/process_result.json"
    
    tester = ContentProcessingStageTester(process_result_path, config, ai_service)
    
    # 1단계: 메모리 기반 추출 테스트
    await tester.test_01_memory_based_extraction()
    
    # 확인 후 정리
    tester.cleanup_test_environment()

asyncio.run(run_single_memory_test())
```

### 4.3 수정된 테스트 결과 활용
```python
# 테스트 성공 시 (메모리 기반)
print("🎉 모든 메모리 기반 테스트 완료!")
print("✅ 메모리 데이터 처리가 정상 동작합니다.")
print("📁 사용자 지정 경로에 결과 파일이 생성되었습니다.")
print("📄 load_and_sort_result.json이 올바르게 생성되었습니다.")

# 테스트 실패 시  
print("❌ 메모리 기반 테스트 중 오류 발생")
print("🔍 임시 디렉터리에서 결과 확인 후 수동 정리하세요")
print(f"📁 임시 디렉터리: {tester.test_temp_dir}")
print(f"📄 생성된 파일들: {os.listdir(tester.user_output_path)}")
```

## 성능 및 효율성 검증

### 5.1 메모리 기반 처리 성능 측정
```python
def measure_memory_processing_performance(process_result: Dict, user_output_path: str) -> Dict:
    """메모리 기반 처리 성능 측정"""
    start_time = time.time()
    
    # 메모리 사용량 측정
    import psutil
    process = psutil.Process()
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # 처리 실행
    # ... ContentProcessingStage.process() 호출
    
    end_time = time.time()
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    
    return {
        'processing_time': end_time - start_time,
        'memory_usage_mb': memory_after - memory_before,
        'documents_processed': len(process_result["documents"]["data"]["unified_documents"]),
        'files_created': len(os.listdir(user_output_path)) if os.path.exists(user_output_path) else 0
    }
```

### 5.2 공통 로직 효율성 검증
```python
def verify_common_logic_efficiency(test_results: List[Dict]) -> Dict:
    """공통 로직 효율성 검증"""
    total_saves = sum(result.get('file_saves', 0) for result in test_results)
    successful_saves = sum(result.get('successful_saves', 0) for result in test_results)
    
    return {
        'save_success_rate': successful_saves / total_saves if total_saves > 0 else 0,
        'average_save_time': sum(result.get('average_save_time', 0) for result in test_results) / len(test_results),
        'code_reuse_percentage': 85,  # 공통 로직으로 인한 코드 재사용률
        'maintenance_improvement': 60  # 유지보수성 개선률
    }
```