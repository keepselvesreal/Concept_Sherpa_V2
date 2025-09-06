# AI 설정 참조 문서

## 🎯 목표
새로운 하위 단계들의 AI 설정 구성 및 설정 해결 방식 이해

## 수정된 설정 파일
- `/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/config/ai_config.yaml`

---

## 1. 추가된 설정 구조

### information_integration 하위 단계 설정
```yaml
information_integration:
  # information_integration 하위 단계들
  detect_section_content:  # 섹션 내용 포함 여부 분석
    provider: "gemini"
    model: "gemini-2.0-flash-lite"
    temperature: 0.1
    max_tokens: 8192
    
  extract_section_content:  # 개별 섹션 내용 추출
    provider: "gemini"
    model: "gemini-2.0-flash-lite"
    temperature: 0.1
    max_tokens: 8192
```

---

## 2. 설정 경로 매핑

### ContentDocumentService 메서드별 설정 경로
```python
# detect_section_content 메서드
stage_name = "information_integration.detect_section_content"
ai_service = AIService(config_manager, logger, stage_name)
# → config 경로: stage_specific_ai.information_integration.detect_section_content

# extract_section_content 메서드  
stage_name = "information_integration.extract_section_content"
ai_service = AIService(config_manager, logger, stage_name)
# → config 경로: stage_specific_ai.information_integration.extract_section_content
```

### AIService 설정 해결 우선순위
```
1. stage_specific_ai.information_integration.detect_section_content  (구체적 단계)
2. stage_specific_ai.information_integration                         (상위 단계)
3. default_ai                                                       (기본 설정)
```

---

## 3. 구현에서의 실제 사용

### 2단계 ContentDocumentService에서의 적용
```python
# detect_section_content 메서드에서
async def detect_section_content(self, chapter_sections, chapter_content, stage_name):
    # stage_name = "information_integration" → 실제로는 하위 단계 사용
    ai_service = AIService(
        self.config_manager, 
        self.logger, 
        "information_integration.detect_section_content"  # 구체적 경로
    )
    # → gemini-2.0-flash-lite 사용
    
# extract_section_content 메서드에서  
async def extract_section_content(self, content_sections, chapter_content, stage_name):
    ai_service = AIService(
        self.config_manager, 
        self.logger, 
        "information_integration.extract_section_content"  # 구체적 경로
    )
    # → gemini-2.0-flash-lite 사용
```

### 3단계 IntegratedNodeGenerationStage에서의 호출
```python
async def generate_content_documents(self, chapter_folder: str):
    # ContentDocumentService 초기화 - 실제 호출에서는 구체적 stage_name 사용됨
    content_service = ContentDocumentService(self.config_manager, self.logger)
    
    # 1단계: 내용 분석 - information_integration.detect_section_content 설정 사용
    sections_with_content = await content_service.detect_section_content(
        chapter_sections, 
        chapter_content,
        "information_integration"  # ContentDocumentService 내부에서 세분화됨
    )
    
    # 2단계: 내용 추출 - information_integration.extract_section_content 설정 사용
    extracted_sections = await content_service.extract_section_content(
        content_sections,
        chapter_content, 
        "information_integration"  # ContentDocumentService 내부에서 세분화됨
    )
```

---

## 4. 설정 변경의 영향

### 이전 설정 (제거됨)
```yaml
information_integration:
  provider: "gemini"
  model: "gemini-1.5-pro"  # 더 복잡한 작업에는 pro 모델
  temperature: 0.05
  max_tokens: 8192
```

### 새로운 설정 (현재)
```yaml
information_integration:
  detect_section_content:
    provider: "gemini"
    model: "gemini-2.0-flash-lite"  # 더 빠른 최신 모델
    temperature: 0.1               # 약간 높은 창의성
    max_tokens: 8192
    
  extract_section_content:
    provider: "gemini"
    model: "gemini-2.0-flash-lite"  # 일관된 모델 사용
    temperature: 0.1
    max_tokens: 8192
```

### 변경 이유
- **성능 향상**: gemini-2.0-flash-lite가 더 빠르고 효율적
- **작업 특성**: 두 작업 모두 복잡한 추론보다는 빠른 처리가 중요
- **일관성**: 동일한 정보 처리 단계에서 같은 모델 사용

---

## 5. 실제 구현에서 주의사항

### ContentDocumentService에서의 올바른 사용법
```python
# ❌ 잘못된 방법
ai_service = AIService(self.config_manager, self.logger, stage_name)  # 상위에서 받은 그대로 사용

# ✅ 올바른 방법
ai_service = AIService(
    self.config_manager, 
    self.logger, 
    f"information_integration.detect_section_content"  # 구체적 하위 단계 지정
)
```

### 로깅에서 확인 가능한 정보
```
[information_integration.detect_section_content] AI 단발성 쿼리 시작 - Gemini Chat (gemini-2.0-flash-lite)
[information_integration.extract_section_content] 세션 쿼리 시작 - Gemini Chat (gemini-2.0-flash-lite)
```

---

## 6. 다른 구현 단계와의 연관성

### 1단계 AIProvider 인터페이스 개선
- AIService의 `_resolve_ai_config()` 메서드가 새로운 경로 구조를 지원
- 단계별 설정 해결 로직이 하위 단계까지 처리

### 2단계 ContentDocumentService 재구성
- 각 메서드에서 구체적인 하위 단계명을 사용하여 AI 서비스 초기화
- 설정에 맞는 모델과 파라미터로 작업 수행

### 3단계 Stage 클래스 연동
- IntegratedNodeGenerationStage는 상위 단계명만 전달
- ContentDocumentService가 내부적으로 하위 단계명으로 세분화

---

## 7. 설정 확장성

### 추후 추가 가능한 설정들
```yaml
information_integration:
  detect_section_content:
    provider: "gemini"
    model: "gemini-2.0-flash-lite" 
    temperature: 0.1
    max_tokens: 8192
    # 추가 가능한 설정들
    retry_count: 3
    timeout_seconds: 30
    
  extract_section_content:
    provider: "gemini"  
    model: "gemini-2.0-flash-lite"
    temperature: 0.1
    max_tokens: 8192
    # 멀티턴 특화 설정들
    session_timeout: 600
    max_context_length: 32768
```

### 다른 제공자 사용 예시
```yaml
information_integration:
  detect_section_content:
    provider: "claude"  # Claude 사용
    model: "claude-3-haiku"
    temperature: 0.1
    
  extract_section_content:
    provider: "gemini"  # 혼합 사용도 가능
    model: "gemini-2.0-flash-lite"
    temperature: 0.1
```

---

## 8. 검증 방법

### 설정 로드 테스트
```python
from services.ai_service_v3 import AIService

# detect_section_content 설정 확인
ai_service = AIService(config_manager, logger, "information_integration.detect_section_content")
config_summary = ai_service.get_config_summary()
print(f"Provider: {config_summary['provider_name']}")
print(f"Config: {config_summary['config']}")

# extract_section_content 설정 확인  
ai_service = AIService(config_manager, logger, "information_integration.extract_section_content")
config_summary = ai_service.get_config_summary()
print(f"Provider: {config_summary['provider_name']}")
print(f"Config: {config_summary['config']}")
```

### 예상 출력
```
Provider: Gemini Chat (gemini-2.0-flash-lite)
Config: {'provider': 'gemini', 'model': 'gemini-2.0-flash-lite', 'temperature': 0.1, 'max_tokens': 8192}
```

---

## 9. 다른 안내 문서와의 연관성

### 1단계 문서와의 연관
- AIService의 `_resolve_ai_config()` 메서드가 이 설정 구조를 지원해야 함
- 하위 단계별 설정 해결이 정상 동작해야 함

### 2단계 문서와의 연관  
- ContentDocumentService의 각 메서드에서 올바른 stage_name 사용 필수
- AI 서비스 초기화 시 구체적인 하위 단계명 지정

### 3단계 문서와의 연관
- IntegratedNodeGenerationStage에서는 상위 단계명만 전달
- 실제 세분화는 ContentDocumentService 내부에서 처리

---

## 10. 완료 확인사항
- [ ] ai_config.yaml에 하위 단계 설정 추가 완료
- [ ] 설정 경로 구조 이해 완료  
- [ ] 각 구현 단계에서의 올바른 stage_name 사용법 숙지
- [ ] 설정 로드 테스트로 정상 동작 확인
- [ ] 로그에서 올바른 모델명 출력 확인