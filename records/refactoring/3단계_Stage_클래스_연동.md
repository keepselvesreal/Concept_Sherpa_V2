# 3단계: Stage 클래스 연동 안내 문서

## 🎯 목표
IntegratedNodeGenerationStage에서 새로운 ContentDocumentService 메서드들을 활용한 통합 콘텐츠 문서 생성 구현

## 수정 대상 파일
- `/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/src/stages/integrated_node_generation_stage_v2.py`

---

## 1. 메서드명 변경

### 기존 메서드명 수정
```python
# 라인 207: 메서드명 변경
async def extract_content_nodes(self, chapter_folder: str) -> Dict[str, Any]:
    ↓ 변경
async def generate_content_documents(self, chapter_folder: str) -> Dict[str, Any]:
```

### 호출부 수정
```python
# 라인 92: 메서드 호출명 변경
sections_result = await self.extract_content_nodes(chapter_folder)
    ↓ 변경
sections_result = await self.generate_content_documents(chapter_folder)
```

---

## 2. generate_content_documents 구현

### 전체 메서드 재작성
```python
async def generate_content_documents(self, chapter_folder: str) -> Dict[str, Any]:
    """2단계: AI 기반 콘텐츠 문서 생성 (detect + extract 통합)"""
    
    folder_name = os.path.basename(chapter_folder)
    toc_file = os.path.join(chapter_folder, f"{folder_name}_toc.json")
    content_file = os.path.join(chapter_folder, f"{folder_name}_content.md")
    
    try:
        self.logger.info(f"콘텐츠 문서 생성 시작: {folder_name}")
        
        # 필수 파일 존재 검증
        if not os.path.exists(toc_file):
            error_msg = f"TOC 파일이 존재하지 않습니다: {toc_file}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
            
        if not os.path.exists(content_file):
            error_msg = f"Content 파일이 존재하지 않습니다: {content_file}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 파일 로드
        with open(toc_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        
        with open(content_file, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        # TOC를 섹션 리스트로 변환 (필요한 필드만 추출)
        chapter_sections = []
        for node in toc_data:
            chapter_sections.append({
                'id': node.get('id'),
                'title': node.get('title', ''),
                'level': node.get('level', 1)
            })
        
        self.logger.info(f"분석 대상 섹션: {len(chapter_sections)}개")
        
        # ContentDocumentService 초기화
        from services.content_document_service_v3 import ContentDocumentService
        content_service = ContentDocumentService(self.config_manager, self.logger)
        
        # 1단계: 섹션 내용 포함 여부 분석
        self.logger.info("1단계: 섹션 내용 분석 시작...")
        sections_with_content = await content_service.detect_section_content(
            chapter_sections, 
            chapter_content,
            "information_integration"
        )
        
        # content.json 저장
        content_service._save_content_json(sections_with_content, chapter_folder)
        
        # 내용이 있는 섹션들만 필터링
        content_sections = [s for s in sections_with_content if s.get('has_content', False)]
        content_count = len(content_sections)
        
        self.logger.info(f"1단계 완료 - 총 {len(sections_with_content)}개 중 {content_count}개 섹션에 내용 포함")
        
        # 2단계: 내용이 있는 섹션들의 실제 내용 추출
        if content_count > 0:
            self.logger.info("2단계: 섹션 내용 추출 시작...")
            extracted_sections = await content_service.extract_section_content(
                content_sections,
                chapter_content, 
                "information_integration"
            )
            
            # sections 폴더에 개별 파일 저장
            content_service._save_section_files(extracted_sections, chapter_folder)
            
            self.logger.info(f"2단계 완료 - {len(extracted_sections)}개 섹션 파일 저장")
        else:
            self.logger.info("2단계 건너뜀 - 내용이 포함된 섹션이 없음")
            extracted_sections = []
        
        self.logger.info(f"{folder_name} 콘텐츠 문서 생성 완료")
        
        return {
            'success': True,
            'total_sections': len(sections_with_content),
            'content_sections': content_count,
            'extracted_files': len(extracted_sections) if content_count > 0 else 0,
            'error': None
        }
        
    except Exception as e:
        error_msg = f"콘텐츠 문서 생성 중 예외: {str(e)}"
        self.logger.error(f"{folder_name} {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }
```

---

## 3. integrate_documents 메서드 수정

### unified_info_docs 폴더 생성 및 통합
```python
def _integrate_single_document(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                              content_dir: str, node_docs_dir: str) -> bool:
    """단일 노드 문서 통합 - unified_info_docs 폴더에 통합 문서 생성"""
    try:
        # unified_info_docs 폴더 생성
        unified_dir = os.path.join(content_dir, "unified_info_docs")
        os.makedirs(unified_dir, exist_ok=True)
        
        # 파일 경로 구성
        title_clean = normalize_title(node['title'])
        node_doc_filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
        node_doc_path = os.path.join(node_docs_dir, node_doc_filename)
        unified_doc_path = os.path.join(unified_dir, node_doc_filename)
        
        # 기존 노드 문서 존재 확인
        if not os.path.exists(node_doc_path):
            self.logger.warning(f"노드 문서 없음: {node_doc_filename}")
            return False
        
        # sections 폴더에서 매칭되는 파일 찾기
        sections_dir = os.path.join(content_dir, "sections")
        section_content = ""
        
        if os.path.exists(sections_dir):
            section_file_path = os.path.join(sections_dir, f"{title_clean}.md")
            if os.path.exists(section_file_path):
                try:
                    with open(section_file_path, 'r', encoding='utf-8') as f:
                        section_content = f.read().strip()
                    self.logger.info(f"매칭된 섹션 파일: {title_clean}.md")
                except Exception as e:
                    self.logger.warning(f"섹션 파일 로드 실패: {e}")
                    section_content = ""
            else:
                self.logger.info(f"매칭되는 섹션 파일 없음: {title_clean}.md")
        
        # 모든 하위 노드 정보 수집 (기존 로직)
        descendants_files = self._get_all_descendants_info(node, all_nodes)
        descendants_text = "\n".join(descendants_files) if descendants_files else ""
        
        # 레벨에 따른 헤더 생성
        header_prefix = "#" * node['level']  
        content_header = f"{header_prefix} {node['title']}"
        
        # 통합 문서 내용 생성 (기존 통합 로직과 동일)
        unified_content = f"""# 속성
---
process_status: false

# 추출
---

# 내용
---
{content_header}

{section_content}

# 구성
---
{descendants_text}
"""
        
        # unified_info_docs에 통합 파일 저장
        with open(unified_doc_path, 'w', encoding='utf-8') as f:
            f.write(unified_content)
        
        self.logger.info(f"통합 문서 생성 완료: unified_info_docs/{node_doc_filename}")
        return True
        
    except Exception as e:
        self.logger.error(f"통합 실패 (ID: {node.get('id', '?')}): {e}")
        return False
```

---

## 4. 파일 저장 결과 확인

### 예상되는 폴더 구조
```
{장_폴더}/
├── {장명}_toc.json           # 입력: 기존 TOC 파일
├── {장명}_content.md         # 입력: 기존 내용 파일
├── content.json              # 출력: has_content 필드가 추가된 섹션 목록
├── sections/                 # 출력: 추출된 섹션 내용들
│   ├── 소개.md
│   ├── 주요_개념.md
│   └── ...
├── node_info_docs/          # 기존: 원본 노드 정보 문서들 (유지)
│   ├── 01_lev1_장제목_info.md
│   ├── 02_lev2_소개_info.md
│   └── ...
└── unified_info_docs/       # 신규: 통합된 최종 문서들
    ├── 01_lev1_장제목_info.md (노드 문서 + 섹션 내용 통합)
    ├── 02_lev2_소개_info.md (노드 문서 + sections/소개.md 통합)
    └── ...
```

### content.json 예시
```json
[
  {
    "id": 1,
    "title": "소개",
    "level": 2,
    "has_content": true
  },
  {
    "id": 2,
    "title": "목차만있음",
    "level": 2,
    "has_content": false
  }
]
```

---

## 5. 기존 메서드 제거

### 🔴 제거할 메서드 코드 블록
```python
# 라인 490-550 제거: _save_content_extraction_results 메서드 전체
def _save_content_extraction_results(self, chapter_number: int, content_result) -> None:
    # ... 전체 메서드 코드 제거
```

---

## 6. 검증 포인트

### 구현 완료 후 확인사항
1. **메서드명 변경**: `extract_content_nodes` → `generate_content_documents`
2. **호출부 수정**: process 메서드에서 올바른 메서드명 호출
3. **파일 생성**: content.json, sections/*.md 파일들 정상 생성
4. **노드 통합**: node_info_docs의 문서들에 sections 내용 포함
5. **로깅**: 각 단계별 상세한 진행 상황 로그
6. **에러 처리**: 실패 시 적절한 에러 메시지와 함께 중단

### 테스트 방법
```python
# 테스트 실행 예시
import asyncio
from stages.integrated_node_generation_stage_v2 import IntegratedNodeGenerationStage

async def test_integration():
    # Stage 초기화
    stage = IntegratedNodeGenerationStage(config_manager, logger_factory)
    
    # 테스트 데이터 준비 (실제 장 폴더 경로)
    test_chapter_folder = "/path/to/test/chapter"
    
    # 콘텐츠 문서 생성 테스트
    result = await stage.generate_content_documents(test_chapter_folder)
    
    print(f"처리 결과: {result}")
    
    # 파일 존재 확인
    import os
    content_json = os.path.join(test_chapter_folder, "content.json")
    sections_dir = os.path.join(test_chapter_folder, "sections")
    
    print(f"content.json 존재: {os.path.exists(content_json)}")
    print(f"sections 폴더 존재: {os.path.exists(sections_dir)}")
    
    if os.path.exists(sections_dir):
        files = os.listdir(sections_dir)
        print(f"sections 파일들: {files}")

# 실행
asyncio.run(test_integration())
```

---

## 7. 전체 파이프라인 흐름

### 3단계 처리 흐름
```
1. generate_node_documents()     # 1단계: 노드 정보 문서 생성
   └── NodeDocumentService 사용
   
2. generate_content_documents()  # 2단계: 콘텐츠 문서 생성 (NEW)
   ├── detect_section_content()  → content.json 저장
   └── extract_section_content() → sections/*.md 저장
   
3. integrate_documents()         # 3단계: 문서 통합
   └── node_info_docs + sections 내용 통합
```

### 주요 변경점 요약
- **메서드명**: `extract_content_nodes` → `generate_content_documents`
- **처리 방식**: 기존 단순 분석 → detect + extract 2단계 처리
- **결과물**: content.json + sections 폴더 생성
- **통합**: sections 내용이 node_info_docs에 포함됨

---

## 8. 주의사항

### ⚠️ 반드시 지킬 것
- **메서드 시그니처**: 기존과 동일한 입출력 형태 유지
- **에러 처리**: 기존 패턴 유지, 실패 시 적절한 딕셔너리 반환
- **로깅 스타일**: 기존 로깅 패턴과 메시지 형식 유지
- **파일 경로**: 절대 경로 사용, 폴더 구조 정확히 준수

### 🔴 추가 제안 (태수 승인 필요)
- **integrate_documents 수정**: sections 폴더 내용을 node_info_docs 문서에 통합하는 로직 추가
- **불필요 메서드 제거**: `_save_content_extraction_results` 메서드 제거

---

## 9. 완료 조건
- [ ] 메서드명 변경 (`extract_content_nodes` → `generate_content_documents`)
- [ ] 호출부 수정 (라인 92)
- [ ] generate_content_documents 메서드 재구현
- [ ] integrate_documents의 sections 통합 로직 추가 (승인 필요)
- [ ] 불필요 메서드 제거 (승인 필요)
- [ ] content.json 파일 생성 테스트
- [ ] sections 폴더 생성 테스트
- [ ] 전체 파이프라인 동작 테스트
- [ ] node_info_docs 통합 결과 확인