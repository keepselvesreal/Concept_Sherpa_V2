# ⚙️ 설정 템플릿 및 구성 가이드

## 🤖 AI 설정 템플릿 (ai_config.yaml)

# AI 설정 (단순화된 모듈별 설정)
ai_settings:
  chapter_workspace:
    provider: "claude_sdk"
    system_prompt_key: "chapter_analysis_system"
    allowed_tools: ["Read"]
    temperature: 0.2
    max_turns: 3
    
  node_document_processor:
    provider: "claude_sdk" 
    system_prompt_key: "node_processing_system"
    allowed_tools: ["Read", "Write"]
    temperature: 0.0
    max_turns: 5
    
  enhanced_toc_generator:
    provider: "claude_sdk"
    system_prompt_key: "toc_generation_system"
    allowed_tools: ["Read", "Write"]
    temperature: 0.1
    max_turns: 2

# 전역 설정
global_settings:
  default_language: "ko"
  log_level: "INFO"
  enable_caching: true
  cache_ttl_seconds: 3600
  max_concurrent_requests: 3
  request_timeout_seconds: 120
```

## 📋 프롬프트 템플릿 파일들

### system_prompts.yaml
```yaml
# 시스템 프롬프트 정의 (통합 관리)
prompts:
  chapter_analysis_system: |
    당신은 도서 구조 분석 전문가입니다. 
    PDF 목차를 분석하여 실제 장과 부록을 정확히 구분하세요.
    
    작업 수행:
    1. PDF에서 추출한 원시 목차 데이터를 분석
    2. 계층 구조 파악 및 정리
    3. 페이지 범위 계산 및 검증
    4. 구조화된 JSON 형태로 결과 반환
    
    준수 사항:
    - 정확성을 최우선으로 함
    - 모호한 경우 명시적으로 표시
    - 일관된 형식으로 출력
    
  node_processing_system: |
    당신은 기술 문서 구조 분석 전문가입니다.
    텍스트를 의미있는 노드로 분할하고 핵심 정보를 추출하세요.
    
    작업 수행:
    1. 노드별 콘텐츠 분석
    2. 핵심 정보 추출
    3. 관련성 평가
    4. 처리 결과 구조화
    
    준수 사항:
    - 콘텐츠의 본질 보존
    - 효율적인 처리 방식 적용
    - 품질 검증 수행
    
  toc_generation_system: |
    당신은 문서 요약 전문가입니다.
    명확하고 구조화된 목차를 마크다운 형식으로 생성하세요.
    
    작업 수행:
    1. 기존 목차 구조 개선
    2. 추가 메타데이터 통합
    3. 사용자 친화적 형태로 변환
    4. 완성된 목차 문서 생성
    
    준수 사항:
    - 가독성 최우선
    - 네비게이션 편의성 고려
    - 일관성 있는 스타일 적용
```

### chapter_analysis.yaml
```yaml
# 장 분석 관련 프롬프트
chapter_prompts:
  workspace_preparation:
    instruction: |
      다음 PDF 파일의 장별 워크스페이스를 준비하세요.
      
      입력: {pdf_path}
      작업:
      1. 책 제목 추출 및 정규화
      2. 장별 디렉터리 구조 계획
      3. 필요한 폴더 생성 계획 수립
      
      출력 형식:
      ```json
      {{
        "book_title": "정규화된 책 제목",
        "normalized_title": "파일명용_제목",
        "chapters": [
          {{
            "chapter_number": 1,
            "title": "장 제목",
            "folder_path": "경로",
            "page_range": "페이지 범위"
          }}
        ]
      }}
      ```
      
  integration_analysis:
    instruction: |
      장별 정보를 통합 분석하세요.
      
      입력: 
      - 장 정보: {chapter_info}
      - 추출된 콘텐츠: {content}
      
      작업:
      1. 콘텐츠 구조 분석
      2. 핵심 개념 추출  
      3. 장간 연관성 분석
      4. 메타데이터 생성
      
      출력: 구조화된 장 정보 JSON
```

### content_processing.yaml
```yaml
# 콘텐츠 처리 관련 프롬프트
content_prompts:
  node_analysis:
    instruction: |
      다음 노드 문서를 분석하여 핵심 정보를 추출하세요.
      
      노드 정보:
      - ID: {node_id}
      - 타입: {node_type}
      - 콘텐츠: {content}
      
      분석 항목:
      1. 주요 개념 및 키워드
      2. 구조적 중요도
      3. 다른 노드와의 연관성
      4. 요약 정보
      
      출력 형식: JSON 구조
      
  batch_processing:
    instruction: |
      다음 노드들을 배치로 처리하세요.
      
      노드 리스트: {nodes}
      
      각 노드에 대해:
      1. 개별 분석 수행
      2. 배치 내 관련성 확인
      3. 우선순위 설정
      4. 처리 결과 취합
      
  quality_validation:
    instruction: |
      처리 결과의 품질을 검증하세요.
      
      검증 대상: {processing_results}
      
      검증 항목:
      1. 완성도 확인
      2. 일관성 검사
      3. 정확도 평가
      4. 개선 사항 제안
```

### toc_generation.yaml
```yaml
# 목차 생성 관련 프롬프트
toc_prompts:
  enhanced_generation:
    instruction: |
      다음 정보를 바탕으로 향상된 목차를 생성하세요.
      
      입력 데이터:
      - 원본 목차: {original_toc}
      - 장별 분석: {chapter_analysis}
      - 노드 정보: {node_data}
      
      생성 요구사항:
      1. 원본 구조 보존
      2. 추가 메타데이터 포함
      3. 네비게이션 링크 생성
      4. 사용자 친화적 형태
      
      출력: 마크다운 형식의 향상된 목차
      
  formatting_rules:
    template: |
      # {book_title}
      
      ## 📋 목차
      
      {generated_toc}
      
      ---
      
      ## 📊 통계 정보
      - 총 장 수: {total_chapters}
      - 총 페이지 수: {total_pages}  
      - 생성 일시: {timestamp}
      
      ## 🔍 추가 정보
      {additional_metadata}
```

## 🔧 설정 클래스 정의

### AIConfig 데이터클래스 (수정됨)
```python
# 생성 시간: 2025-09-03 14:45:00
# 핵심 내용: 단순화된 AI 설정 데이터클래스
# 상세 내용:
#   - AIConfig 데이터클래스 (15-25): 단순화된 AI 설정 저장
#   - provider 필드: claude_sdk 고정
#   - system_prompt_key 필드: 프롬프트 키 참조
#   - allowed_tools 필드: Claude Code 도구 목록
#   - cost_limit 제거됨
# 상태: active
# 참조: 기존 AIConfig에서 단순화

from dataclasses import dataclass
from typing import List, Optional
import yaml
from pathlib import Path

@dataclass  
class AIConfig:
    """단순화된 AI 설정"""
    provider: str = "claude_sdk"
    system_prompt_key: Optional[str] = None  # 프롬프트 키
    allowed_tools: Optional[List[str]] = None
    temperature: float = 0.1
    max_tokens: int = 8192
    max_turns: int = 5
    
    def __post_init__(self):
        if self.allowed_tools is None:
            self.allowed_tools = ["Read", "Write", "Bash"]

class AIConfigManager:
    """AI 설정 관리 클래스"""
    
    def __init__(self, config_path: str = "config/ai_config.yaml"):
        self.config_path = Path(config_path)
        self.ai_settings: Dict[str, AIConfig] = {}
        self.global_settings: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self):
        """설정 파일을 로드합니다"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"AI config file not found: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        # AI 설정 로드 (모듈별)
        for module_name, settings in config_data.get('ai_settings', {}).items():
            self.ai_settings[module_name] = AIConfig(**settings)
        
        # 전역 설정 로드
        self.global_settings = config_data.get('global_settings', {})
    
    def get_config(self, module_name: str) -> Optional[AIConfig]:
        """특정 모듈의 AI 설정을 반환합니다"""
        return self.ai_settings.get(module_name)
    
    def get_all_configs(self) -> Dict[str, AIConfig]:
        """모든 모듈의 AI 설정을 반환합니다"""
        return self.ai_settings
```

## 📝 로깅 설정 (logging_config.yaml)

```yaml
# 로깅 시스템 설정
logging:
  version: 1
  disable_existing_loggers: false
  
  formatters:
    standard:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      datefmt: "%Y-%m-%d %H:%M:%S"
    
    detailed:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(funcName)s - %(message)s"
      datefmt: "%Y-%m-%d %H:%M:%S"
    
    json:
      "()": "pythonjsonlogger.jsonlogger.JsonFormatter"
      format: "%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s"
  
  handlers:
    console:
      class: logging.StreamHandler
      level: INFO
      formatter: standard
      stream: ext://sys.stdout
    
    file:
      class: logging.handlers.RotatingFileHandler
      level: DEBUG
      formatter: detailed
      filename: logs/book_pipeline.log
      maxBytes: 10485760  # 10MB
      backupCount: 5
      encoding: utf-8
    
    refactoring:
      class: logging.handlers.RotatingFileHandler
      level: DEBUG
      formatter: json
      filename: logs/refactoring.log
      maxBytes: 5242880   # 5MB
      backupCount: 3
      encoding: utf-8
  
  loggers:
    book_pipeline:
      level: DEBUG
      handlers: [console, file]
      propagate: false
    
    refactoring:
      level: DEBUG  
      handlers: [refactoring]
      propagate: false
    
    ai_provider:
      level: INFO
      handlers: [console, file]
      propagate: false
  
  root:
    level: INFO
    handlers: [console]

# RefactoringLogger 전용 설정
refactoring_logger:
  log_directory: "logs/refactoring"
  log_file_prefix: "operation"
  max_file_size_mb: 10
  backup_count: 5
  log_level: "DEBUG"
  enable_console_output: true
  operation_timeout_seconds: 300
```

## 🧪 테스트 설정 (pytest.ini)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --verbose
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=85

markers =
    unit: Unit tests
    integration: Integration tests  
    characterization: Characterization tests for refactoring
    slow: Slow tests (require AI API calls)
    requires_pdf: Tests that require PDF files
    requires_ai: Tests that require AI provider access

# 테스트 환경 변수
env =
    ENVIRONMENT = test
    LOG_LEVEL = WARNING
    ENABLE_AI_CALLS = false
```

## 🐍 Python 의존성 (requirements.txt)

```txt
# 생성 시간: 2025-09-03 14:50:00
# 핵심 내용: 리팩토링된 책 파이프라인의 Python 의존성 정의
# 상태: active

# AI 프로바이더
claude-code-sdk>=0.1.0
anthropic>=0.25.0

# PDF 처리
PyMuPDF>=1.23.0
pymupdf4llm>=0.0.5

# 비동기 처리
asyncio>=3.4.3
aiofiles>=23.2.0

# 데이터 처리
pydantic>=2.0.0
pydantic-settings>=2.0.0

# 설정 관리  
PyYAML>=6.0.1
python-dotenv>=1.0.0

# 로깅
python-json-logger>=2.0.7

# 테스트
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0
pytest-env>=0.8.2
pytest-mock>=3.11.0

# 개발 도구
black>=23.7.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.5.0

# 타입 힌트
types-PyYAML>=6.0.12
types-aiofiles>=23.2.0
```

## 🚀 초기 설정 스크립트

### setup_project.py
```python
#!/usr/bin/env python3
"""
프로젝트 초기 설정 스크립트
"""

import os
import sys
from pathlib import Path
import shutil
import subprocess

def create_directory_structure():
    """디렉터리 구조 생성"""
    directories = [
        "src/application",
        "src/domain/pipeline", 
        "src/domain/chapter",
        "src/domain/toc",
        "src/domain/document",
        "src/infrastructure/ai",
        "src/infrastructure/logging", 
        "src/infrastructure/filesystem",
        "src/config",
        "tests/unit",
        "tests/integration", 
        "tests/characterization",
        "tests/test_data",
        "tests/test_data/expected_results",
        "prompts",
        "config", 
        "docs",
        "logs",
        "logs/refactoring", 
        "scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
    print("✅ 디렉터리 구조 생성 완료")

def copy_existing_logger():
    """기존 RefactoringLogger 복사"""
    source = Path("../refactoring_logger.py")
    target = Path("src/refactoring_logger.py") 
    
    if source.exists():
        shutil.copy2(source, target)
        print("✅ RefactoringLogger 복사 완료")
    else:
        print("⚠️ RefactoringLogger 원본 파일을 찾을 수 없습니다")

def create_init_files():
    """__init__.py 파일 생성"""
    init_paths = [
        "src/__init__.py",
        "src/application/__init__.py",
        "src/domain/__init__.py", 
        "src/domain/pipeline/__init__.py",
        "src/domain/chapter/__init__.py",
        "src/domain/toc/__init__.py", 
        "src/domain/document/__init__.py",
        "src/infrastructure/__init__.py",
        "src/infrastructure/ai/__init__.py",
        "src/infrastructure/logging/__init__.py",
        "src/infrastructure/filesystem/__init__.py",
        "src/config/__init__.py",
        "tests/__init__.py"
    ]
    
    for path in init_paths:
        Path(path).touch()
        
    print("✅ __init__.py 파일 생성 완료")

def setup_git():
    """Git 저장소 초기화"""
    try:
        subprocess.run(["git", "init"], check=True)
        
        # .gitignore 생성
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/

# Logs
logs/
*.log

# Configuration
config/ai_config.yaml
.env

# Test data
tests/test_data/*.pdf
tests/test_data/expected_results/
""".strip()
        
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
            
        print("✅ Git 저장소 초기화 완료")
        
    except subprocess.CalledProcessError:
        print("⚠️ Git 초기화 실패 - git이 설치되어 있는지 확인하세요")

def main():
    """메인 함수"""
    print("🚀 책 파이프라인 리팩토링 프로젝트 초기 설정을 시작합니다...")
    
    create_directory_structure()
    copy_existing_logger()
    create_init_files()
    setup_git()
    
    print("\n✅ 프로젝트 초기 설정이 완료되었습니다!")
    print("\n다음 단계:")
    print("1. config/ai_config.yaml 파일을 생성하고 AI 설정을 입력하세요")
    print("2. .env 파일을 생성하고 API 키를 설정하세요")  
    print("3. uv를 사용하여 의존성을 설치하세요: uv pip install -r requirements.txt")
    print("4. 첫 번째 특성화 테스트를 작성하세요")

if __name__ == "__main__":
    main()
```

## 🔧 Claude SDK Provider 구현 예제

### ClaudeSDKProvider 클래스 (로그 기반 수정 버전)
```python
# 생성 시간: 2025-09-03 15:45:00
# 핵심 내용: Claude Code SDK를 사용하는 AI Provider 구현
# 상세 내용:
#   - ClaudeSDKProvider 클래스: claude_code_sdk 기반 구현
#   - PromptManager 통합: 시스템 프롬프트 외부화
#   - ClaudeCodeOptions 사용: SDK 전용 옵션 설정
# 상태: active
# 참조: 이전 대화의 실제 사용 예제 기반

from claude_code_sdk import ClaudeCodeClient, ClaudeCodeOptions
from typing import Dict, Any, List, Optional
import asyncio

class ClaudeSDKProvider(AIProviderInterface):
    """Claude Code SDK 기반 AI Provider"""
    
    def __init__(self, config: AIConfig, prompt_manager: PromptManager = None):
        super().__init__(config)
        self.prompt_manager = prompt_manager or PromptManager()
        self.client_options = self._create_client_options()
        
    def _create_client_options(self) -> ClaudeCodeOptions:
        """Claude Code SDK 옵션 생성"""
        # 시스템 프롬프트를 외부에서 가져옴
        system_prompt = self.prompt_manager.get_prompt(self.config.system_prompt_key)
        
        return ClaudeCodeOptions(
            system_prompt=system_prompt,
            allowed_tools=self.config.allowed_tools or ["Read", "Write", "Bash"],
            max_turns=getattr(self.config, 'max_turns', 5),
            temperature=self.config.temperature
        )
    
    async def analyze_content(
        self,
        content: str,
        system_prompt_key: str,
        **kwargs
    ) -> Dict[str, Any]:
        """콘텐츠 분석 수행"""
        
        async with ClaudeCodeClient(self.client_options) as client:
            try:
                response = await client.send_message(content)
                
                return {
                    "success": True,
                    "response": response,
                    "metadata": {
                        "model": "claude-3-5-sonnet",
                        "system_prompt_key": system_prompt_key
                    }
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
    
    def is_available(self) -> bool:
        """Claude Code SDK 사용 가능 여부 확인"""
        try:
            return True  # Max Plan 기반이므로 별도 체크 불필요
        except Exception:
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """프로바이더 정보 반환"""
        return {
            "name": "claude_sdk",
            "type": "Claude Code SDK",
            "system_prompt_key": self.config.system_prompt_key,
            "allowed_tools": self.config.allowed_tools,
            "max_turns": self.config.max_turns
        }
```

## 💡 핵심 변화점

### 이전 대화에서 확인된 수정 사항:
1. **프롬프트 통합 관리**: 모든 시스템 프롬프트를 `prompts/system_prompts.yaml`에서 통합 관리
2. **설정 파일 단순화**: 모듈별 독립 설정으로 단순화
3. **cost_limit 제거**: 비용 제한 설정 완전 제거
4. **Claude SDK Provider**: `claude_code_sdk` 기반 실제 구현체 사용

### 다음 구현 세션 시작점:
1. `PromptManager` + 프롬프트 파일들 생성
2. `ClaudeSDKProvider` 구현  
3. `TOCExtractor` 도메인 서비스 구현
4. 기존 코드 동작과 비교 테스트

이제 실제 구현에 필요한 모든 설정 템플릿과 가이드가 준비되었습니다. 구현 세션에서는 이 문서들을 참조하여 체계적으로 리팩토링을 진행할 수 있을 것입니다.