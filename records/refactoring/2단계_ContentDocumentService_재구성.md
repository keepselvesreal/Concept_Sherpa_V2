# 2단계: ContentDocumentService 재구성 안내 문서

## 🎯 목표
ContentDocumentService를 완전히 재구성하여 두 가지 핵심 메서드만으로 콘텐츠 문서 생성 기능 구현

## 수정 대상 파일
- `/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/src/services/content_document_service_v3.py`

---

## 1. 전면 재구성 개요

### 🔴 기존 메서드 완전 제거
```python
# 제거할 메서드들 (모든 기존 메서드)
async def detect_section_content(self, chapter_sections, chapter_content, stage_name)  # 기존 것
async def _analyze_sections_with_session(self, ...)
async def _extract_content_with_session(self, ...)  
async def _analyze_with_individual_requests(self, ...)
async def _extract_content_individually(self, ...)
def _parse_has_content_response(self, ...)
```

### 새로운 클래스 구조
```python
from typing import Dict, List, Any, Optional
import json
import os
from .ai_service_v3 import AIService

class ContentDocumentService:
    """콘텐츠 문서 생성 서비스 - 두 가지 핵심 기능만 제공"""
    
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
    
    # 새로운 두 가지 핵심 메서드
    async def detect_section_content(self, chapter_sections: List[Dict], 
                                   chapter_content: str, stage_name: str) -> List[Dict]:
    async def extract_section_content(self, content_sections: List[Dict], 
                                    chapter_content: str, stage_name: str) -> List[Dict]:
    
    # 지원 메서드들
    def _parse_json_response(self, response_text: str, section_title: str) -> List[Dict]:
    def _save_content_json(self, sections_with_content: List[Dict], chapter_folder: str):
    def _save_section_files(self, extracted_sections: List[Dict], chapter_folder: str):
```

---

## 2. detect_section_content 구현

### 메서드 시그니처
```python
async def detect_section_content(self, chapter_sections: List[Dict], 
                               chapter_content: str, stage_name: str) -> List[Dict]:
    """
    일회성 쿼리로 장의 각 섹션 내용 포함 여부 분석
    
    Args:
        chapter_sections: 장을 구성하는 섹션 목차 정보 리스트
                         [{"id": 1, "title": "섹션명", "level": 2}, ...]
        chapter_content: 장 전체의 마크다운 내용
        stage_name: AI 설정에서 사용할 단계명
    
    Returns:
        has_content 필드가 추가된 섹션 리스트
        [{"id": 1, "title": "섹션명", "level": 2, "has_content": true}, ...]
    """
```

### 구현 로직
```python
async def detect_section_content(self, chapter_sections: List[Dict], 
                               chapter_content: str, stage_name: str) -> List[Dict]:
    try:
        # AI 서비스 초기화
        ai_service = AIService(self.config_manager, self.logger, f"workspace_preparation.{stage_name}")
        self.logger.info(f"섹션 내용 분석 시작 - 제공자: {ai_service.get_name()}, 섹션 수: {len(chapter_sections)}")
        
        # 프롬프트 구성
        detect_prompt = f"""다음 장(chapter)의 전체 내용에서 각 섹션별로 실질적인 내용 포함 여부를 분석해주세요.

장 전체 내용:
```markdown
{chapter_content}
```

분석 대상 섹션 목록:
{json.dumps(chapter_sections, ensure_ascii=False, indent=2)}

분석 기준:
- 실질 내용 있음 (has_content: true): 30자 이상의 의미있는 텍스트, 설명문, 예제, 코드 등
- 실질 내용 없음 (has_content: false): 단순 제목이나 페이지 번호, 목차만 있는 경우

요청: 위 섹션 목록에 각각 has_content 필드를 추가하여 JSON 배열로 응답해주세요.

응답 형식:
```json
[
  {{
    "id": 1,
    "title": "섹션 제목",
    "level": 2,
    "has_content": true
  }},
  ...
]
```"""
        
        # 일회성 쿼리 실행
        self.logger.info("일회성 쿼리로 섹션 내용 분석 실행...")
        response_text = await ai_service.query_single_request(detect_prompt)
        
        # JSON 응답 파싱
        sections_with_content = self._parse_json_response(response_text, "섹션 목록")
        
        self.logger.info(f"섹션 분석 완료 - 총 {len(sections_with_content)}개 섹션, " +
                        f"내용 포함: {len([s for s in sections_with_content if s.get('has_content', False)])}개")
        
        return sections_with_content
        
    except Exception as e:
        error_msg = f"섹션 내용 분석 실패: {str(e)}"
        self.logger.error(error_msg)
        
        # 재시도 로직: 최대 3회까지 재시도
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.warning(f"AI 요청 재시도 {attempt}/{max_retries}...")
                response_text = await ai_service.query_single_request(detect_prompt)
                sections_with_content = self._parse_json_response(response_text, "섹션 목록")
                self.logger.info(f"재시도 {attempt}회차에서 성공")
                return sections_with_content
            except Exception as retry_e:
                self.logger.error(f"재시도 {attempt}회차 실패: {str(retry_e)}")
                if attempt == max_retries:
                    self.logger.error(f"최대 재시도 {max_retries}회 모두 실패")
                    raise Exception(f"섹션 내용 분석 최대 재시도 실패: {str(e)}")
        
        # 여기에 도달하면 모든 재시도 실패
        raise Exception(f"섹션 내용 분석 실패: {str(e)}")
```

---

## 3. extract_section_content 구현

### 메서드 시그니처
```python
async def extract_section_content(self, content_sections: List[Dict], 
                                chapter_content: str, stage_name: str) -> List[Dict]:
    """
    멀티턴으로 각 섹션의 실제 내용 추출
    
    Args:
        content_sections: has_content=True인 섹션들만 포함된 리스트
                         [{"id": 1, "title": "섹션명", "level": 2, "has_content": true}, ...]
        chapter_content: 장 전체의 마크다운 내용
        stage_name: AI 설정에서 사용할 단계명
    
    Returns:
        추출된 섹션 내용 리스트
        [{"section_title": "제목", "extracted_content": "마크다운 내용", ...}, ...]
    """
```

### 구현 로직
```python
async def extract_section_content(self, content_sections: List[Dict], 
                                chapter_content: str, stage_name: str) -> List[Dict]:
    try:
        if not content_sections:
            self.logger.info("추출할 섹션이 없습니다")
            return []
        
        # AI 서비스 초기화
        ai_service = AIService(self.config_manager, self.logger, f"workspace_preparation.{stage_name}")
        self.logger.info(f"섹션 내용 추출 시작 - 제공자: {ai_service.get_name()}, 대상: {len(content_sections)}개")
        
        # 새 세션 생성 (SessionInfo 객체 반환)
        session_info = await ai_service.create_session()
        self.logger.info(f"추출용 세션 생성: {session_info.provider_type}")
        
        # 첫 번째 턴: 컨텍스트 설정
        context_prompt = f"""다음 장의 전체 내용과 목차 구조를 제공합니다. 이후 개별 섹션별로 내용 추출을 요청하겠습니다.

장 전체 내용:
```markdown
{chapter_content}
```

장 목차 구조:
{json.dumps(content_sections, ensure_ascii=False, indent=2)}

준비가 되면 "준비완료"라고 응답해주세요."""
        
        self.logger.info("컨텍스트 설정 중...")
        context_response = await ai_service.query_with_persistent_session(context_prompt, session_info)
        self.logger.info(f"컨텍스트 설정 완료: {context_response[:50]}...")
        
        # 각 섹션별 내용 추출
        extracted_sections = []
        
        for section in content_sections:
            section_title = section.get('title', '제목 없음')
            
            try:
                # 개별 섹션 추출 프롬프트
                section_prompt = f"""섹션 제목: "{section_title}"

위 장 내용에서 이 섹션에 해당하는 모든 내용을 정확히 추출해주세요.

추출 요청:
1. 섹션 제목에 해당하는 모든 관련 내용
2. 제목, 설명, 예제, 코드 등 포함  
3. 마크다운 형식 유지

응답: 추출된 섹션의 마크다운 내용만 반환"""
                
                self.logger.info(f"섹션 내용 추출 중: '{section_title}'")
                extracted_content = await ai_service.query_with_persistent_session(section_prompt, session_info)
                
                # 추출 결과 저장
                section_document = {
                    "section_id": section.get('id'),
                    "section_title": section_title,
                    "level": section.get('level'),
                    "has_content": True,
                    "extracted_content": extracted_content,
                    "content_length": len(extracted_content)
                }
                
                extracted_sections.append(section_document)
                self.logger.info(f"섹션 추출 완료: '{section_title}' ({len(extracted_content)} 문자)")
                
            except Exception as e:
                error_msg = f"섹션 '{section_title}' 추출 실패: {str(e)}"
                self.logger.error(error_msg)
                # 한 섹션 실패 시 전체 실패
                raise Exception(error_msg)
        
        self.logger.info(f"전체 섹션 추출 완료: {len(extracted_sections)}개")
        return extracted_sections
        
    except Exception as e:
        error_msg = f"섹션 내용 추출 실패: {str(e)}"
        self.logger.error(error_msg)
        
        # 재시도 로직: 실패한 지점부터 다시 시도
        max_retries = 2
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.warning(f"섹션 추출 재시도 {attempt}/{max_retries}...")
                
                # 새로운 세션으로 전체 작업 재시작
                retry_session_info = await ai_service.create_session()
                self.logger.info(f"재시도용 새 세션 생성: {retry_session_info.provider_type}")
                
                # 컨텍스트 재설정
                context_response = await ai_service.query_with_persistent_session(context_prompt, retry_session_info)
                
                # 전체 섹션 재추출
                retry_extracted_sections = []
                for section in content_sections:
                    section_title = section.get('title', '제목 없음')
                    section_prompt = f"""섹션 제목: "{section_title}"

위 장 내용에서 이 섹션에 해당하는 모든 내용을 정확히 추출해주세요.

추출 요청:
1. 섹션 제목에 해당하는 모든 관련 내용
2. 제목, 설명, 예제, 코드 등 포함  
3. 마크다운 형식 유지

응답: 추출된 섹션의 마크다운 내용만 반환"""
                    
                    extracted_content = await ai_service.query_with_persistent_session(section_prompt, retry_session_info)
                    
                    section_document = {
                        "section_id": section.get('id'),
                        "section_title": section_title,
                        "level": section.get('level'),
                        "has_content": True,
                        "extracted_content": extracted_content,
                        "content_length": len(extracted_content)
                    }
                    
                    retry_extracted_sections.append(section_document)
                
                self.logger.info(f"재시도 {attempt}회차에서 성공: {len(retry_extracted_sections)}개 섹션")
                return retry_extracted_sections
                
            except Exception as retry_e:
                self.logger.error(f"재시도 {attempt}회차 실패: {str(retry_e)}")
                if attempt == max_retries:
                    self.logger.error(f"최대 재시도 {max_retries}회 모두 실패")
                    raise Exception(f"섹션 내용 추출 최대 재시도 실패: {str(e)}")
        
        # 여기에 도달하면 모든 재시도 실패
        raise Exception(f"섹션 내용 추출 실패: {str(e)}")
```

---

## 4. 지원 메서드 구현

### JSON 파싱 메서드
```python
def _parse_json_response(self, response_text: str, section_title: str) -> List[Dict]:
    """AI 응답에서 JSON 배열 파싱 - 엄격한 파싱, 실패 시 예외 발생"""
    try:
        import re
        
        # JSON 블록 찾기
        json_match = re.search(r'```json\s*(\[.*?\])\s*```', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
        else:
            # JSON 블록이 없으면 대괄호로 감싼 부분 찾기
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
            else:
                json_text = response_text.strip()
        
        # JSON 파싱
        parsed_data = json.loads(json_text)
        
        if not isinstance(parsed_data, list):
            raise ValueError("응답이 배열 형식이 아닙니다")
        
        self.logger.info(f"JSON 파싱 성공: {len(parsed_data)}개 항목")
        return parsed_data
        
    except (json.JSONDecodeError, ValueError) as e:
        error_msg = f"JSON 파싱 실패 ({section_title}): {e}"
        self.logger.error(error_msg)
        raise Exception(error_msg)
```

### content.json 저장 메서드
```python
def _save_content_json(self, sections_with_content: List[Dict], chapter_folder: str):
    """content.json 파일 저장 - 지정된 필드만 포함"""
    try:
        # 필드 제한: id, title, level, has_content만 포함
        content_json = []
        for section in sections_with_content:
            filtered_section = {
                "id": section.get("id"),
                "title": section.get("title"),
                "level": section.get("level"),
                "has_content": section.get("has_content", False)
            }
            content_json.append(filtered_section)
        
        # content.json 파일 저장
        content_file_path = os.path.join(chapter_folder, "content.json")
        with open(content_file_path, 'w', encoding='utf-8') as f:
            json.dump(content_json, f, ensure_ascii=False, indent=2)
        
        content_count = len([s for s in content_json if s.get('has_content', False)])
        self.logger.info(f"content.json 저장 완료: {content_file_path}")
        self.logger.info(f"총 {len(content_json)}개 섹션, 내용 포함: {content_count}개")
        
    except Exception as e:
        error_msg = f"content.json 저장 실패: {str(e)}"
        self.logger.error(error_msg)
        raise Exception(error_msg)
```

### 섹션 파일 저장 메서드
```python
def _save_section_files(self, extracted_sections: List[Dict], chapter_folder: str):
    """sections/ 폴더에 개별 섹션 파일 저장"""
    try:
        from utils.text_utils import normalize_title
        
        # sections 폴더 생성
        sections_dir = os.path.join(chapter_folder, "sections")
        os.makedirs(sections_dir, exist_ok=True)
        self.logger.info(f"sections 폴더 확인: {sections_dir}")
        
        # 각 섹션별 파일 저장
        saved_count = 0
        for section in extracted_sections:
            section_title = section.get('section_title', '제목없음')
            extracted_content = section.get('extracted_content', '')
            
            if not extracted_content.strip():
                self.logger.warning(f"섹션 '{section_title}' 내용이 비어있음 - 저장 건너뜀")
                continue
            
            # 안전한 파일명 생성
            safe_filename = f"{normalize_title(section_title)}.md"
            file_path = os.path.join(sections_dir, safe_filename)
            
            # 마크다운 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(extracted_content)
            
            saved_count += 1
            self.logger.info(f"섹션 파일 저장: {safe_filename} ({len(extracted_content)} 문자)")
        
        self.logger.info(f"sections 폴더 저장 완료: {saved_count}개 파일")
        
    except Exception as e:
        error_msg = f"섹션 파일 저장 실패: {str(e)}"
        self.logger.error(error_msg)
        raise Exception(error_msg)
```

---

## 5. 검증 포인트

### 구현 완료 후 확인사항
1. **메서드 구조**: 기존 메서드 완전 제거, 새 메서드 2개만 존재
2. **JSON 파싱**: 엄격한 파싱, 실패 시 예외 발생
3. **파일 저장**: content.json(지정 필드만), sections/*.md 파일 생성
4. **에러 처리**: 모든 단계에서 실패 시 전체 실패
5. **로깅**: 각 단계별 상세한 로그 출력

### 테스트 방법
```python
# 테스트 데이터 준비
chapter_sections = [
    {"id": 1, "title": "소개", "level": 2},
    {"id": 2, "title": "주요 개념", "level": 2},
]
chapter_content = "# 장 제목\n\n## 소개\n실제 내용...\n\n## 주요 개념\n개념 설명..."

# ContentDocumentService 테스트
service = ContentDocumentService(config_manager, logger)

# 1단계: 내용 분석
sections_with_content = await service.detect_section_content(
    chapter_sections, chapter_content, "test_stage"
)
print(f"분석 결과: {len(sections_with_content)}개 섹션")

# 2단계: 내용 추출
content_sections = [s for s in sections_with_content if s.get('has_content', False)]
extracted_sections = await service.extract_section_content(
    content_sections, chapter_content, "test_stage"
)
print(f"추출 결과: {len(extracted_sections)}개 섹션")
```

---

## 6. 주의사항

### ⚠️ 반드시 지킬 것
- **완전 재구성**: 기존 메서드들을 모두 제거하고 새로 시작
- **엄격한 에러 처리**: JSON 파싱 실패, 섹션 추출 실패 시 즉시 예외 발생
- **단일 책임**: 각 메서드는 하나의 명확한 역할만 담당
- **지정된 파일 구조**: content.json 필드, sections 폴더 구조 정확히 준수

### 🔴 추가 제안 (태수 승인 필요)
없음 - 모든 변경사항은 명시된 요구사항에 기반함

---

## 7. 완료 조건
- [ ] 기존 메서드들 완전 제거
- [ ] detect_section_content 메서드 구현
- [ ] extract_section_content 메서드 구현
- [ ] 지원 메서드 3개 구현 (_parse_json_response, _save_content_json, _save_section_files)
- [ ] JSON 파싱 테스트 (정상 케이스, 실패 케이스)
- [ ] 파일 저장 테스트 (content.json, sections 폴더)
- [ ] 전체 플로우 테스트