# 생성 시간: 2025-09-03 10:51:18 KST
# 핵심 내용: 세션 로그에서 콘텍스트 주제를 추출하는 메인 스크립트
# 상세 내용:
#   - setup_logging (라인 33-48): 로깅 시스템 설정 함수
#   - SessionLogExtractor (라인 51-172): 세션 로그 처리 메인 클래스
#   - load_user_files (라인 63-90): 특정 세션의 사용자 파일들 로드
#   - extract_and_combine_content (라인 92-115): 콘텐츠 추출 및 결합
#   - analyze_with_ai (라인 117-134): AI를 통한 콘텍스트 분석
#   - save_markdown_output (라인 136-172): 마크다운 형식으로 결과 저장
#   - main (라인 175-223): 메인 실행 함수 및 argparse 처리
# 상태: active
# 주소: context_extractor
# 참조: ai_providers

#!/usr/bin/env python3
"""
세션 로그 콘텍스트 추출기

Claude Code 세션 로그에서 사용자 질의를 분석하여
향후 작업에 활용할 콘텍스트 주제들을 추출합니다.

사용법:
    python context_extractor.py <session_id> <log_folder_path> <output_folder_path>
    
예시:
    python context_extractor.py de374da6-c4de-487a-8ed7-fec9991f5d90 ./logs/chat-logs/25-09-02 ./output
"""

import os
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re

from ai_providers import AIProviderFactory


def setup_logging(log_file: str) -> logging.Logger:
    """로깅 시스템 설정"""
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # 기존 핸들러 제거
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 파일 핸들러
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포맷터
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 메인 로거 반환
    logger = logging.getLogger(__name__)
    
    return logger


class SessionLogExtractor:
    """세션 로그 콘텍스트 추출기"""
    
    def __init__(self, session_id: str, log_folder: str, output_folder: str, 
                 ai_provider: str = 'gemini', log_file: str = None):
        self.session_id = session_id
        self.log_folder = Path(log_folder)
        self.output_folder = Path(output_folder)
        self.ai_provider_type = ai_provider
        
        # 로깅 설정
        if not log_file:
            log_file = self.output_folder / f"context_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.logger = setup_logging(str(log_file))
        
        self.logger.info(f"SessionLogExtractor 초기화: session_id={session_id}, provider={ai_provider}")
    
    def load_user_files(self) -> List[Tuple[str, Dict[str, Any]]]:
        """특정 세션의 사용자 파일들을 로드"""
        user_files = []
        session_short_id = self.session_id.split('-')[0]  # de374da6 같은 짧은 형태
        
        try:
            if not self.log_folder.exists():
                raise FileNotFoundError(f"로그 폴더가 존재하지 않습니다: {self.log_folder}")
            
            # 파일명 패턴: {시간}_{session_short_id}_{sequence}_user.json
            pattern = re.compile(rf'\d{{4}}_{session_short_id}_.*_user\.json$')
            
            for file_path in self.log_folder.glob('*.json'):
                if pattern.match(file_path.name):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        # 세션 ID 검증
                        if data.get('session_id', '').startswith(session_short_id):
                            sequence_number = data.get('sequence_number', '000')
                            user_files.append((sequence_number, data))
                            self.logger.info(f"사용자 파일 로드: {file_path.name}, sequence: {sequence_number}")
                    
                    except (json.JSONDecodeError, FileNotFoundError) as e:
                        self.logger.warning(f"파일 로드 실패 {file_path}: {e}")
                        continue
            
            if not user_files:
                raise ValueError(f"세션 ID {self.session_id}에 해당하는 사용자 파일을 찾을 수 없습니다")
            
            # 시퀀스 번호로 정렬
            user_files.sort(key=lambda x: x[0])
            self.logger.info(f"총 {len(user_files)}개 사용자 파일 로드 완료")
            
        except Exception as e:
            self.logger.error(f"사용자 파일 로드 중 오류: {e}")
            raise
        
        return user_files
    
    def extract_and_combine_content(self, user_files: List[Tuple[str, Dict[str, Any]]]) -> str:
        """콘텐츠 추출 및 결합"""
        combined_content = []
        
        try:
            for sequence, file_data in user_files:
                content = file_data.get('content', '').strip()
                if content:
                    timestamp = file_data.get('timestamp', '')
                    combined_content.append(f"[{sequence}] {timestamp}\n{content}")
                    self.logger.debug(f"콘텐츠 추출: sequence {sequence}, 길이 {len(content)}")
            
            if not combined_content:
                raise ValueError("추출할 콘텐츠가 없습니다")
            
            result = '\n\n---\n\n'.join(combined_content)
            self.logger.info(f"콘텐츠 결합 완료: 총 {len(combined_content)}개 항목, {len(result)} 글자")
            
            return result
            
        except Exception as e:
            self.logger.error(f"콘텐츠 추출 중 오류: {e}")
            raise
    
    def analyze_with_ai(self, content: str) -> Dict[str, Any]:
        """AI를 통한 콘텍스트 분석"""
        try:
            self.logger.info(f"{self.ai_provider_type} provider로 콘텍스트 분석 시작")
            
            provider = AIProviderFactory.create_provider(self.ai_provider_type)
            result = provider.analyze_context(content)
            
            self.logger.info("AI 분석 완료")
            return result
            
        except Exception as e:
            self.logger.error(f"AI 분석 중 오류: {e}")
            # 기본 응답 반환
            return {
                "error": str(e),
                "raw_content": content[:500] + "..." if len(content) > 500 else content
            }
    
    def save_markdown_output(self, analysis_result: Dict[str, Any], user_files_count: int) -> str:
        """마크다운 형식으로 결과 저장"""
        try:
            # 출력 폴더 생성
            self.output_folder.mkdir(parents=True, exist_ok=True)
            
            # 파일명 생성
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"context_analysis_{self.session_id.split('-')[0]}_{timestamp}.md"
            output_path = self.output_folder / filename
            
            # 마크다운 내용 생성
            content = self._format_markdown(analysis_result, user_files_count)
            
            # 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"마크다운 파일 저장: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"마크다운 저장 중 오류: {e}")
            raise
    
    def _format_markdown(self, analysis_result: Dict[str, Any], user_files_count: int) -> str:
        """마크다운 형식으로 포맷팅"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        content = f"""# 콘텍스트 분석 결과

**세션 ID**: {self.session_id}
**분석 시간**: {timestamp}
**AI Provider**: {self.ai_provider_type}
**분석 파일 수**: {user_files_count}개

---

"""
        
        # AI 분석 결과 처리
        if "error" in analysis_result:
            content += f"""## ⚠️ 분석 오류

**오류 내용**: {analysis_result['error']}

### 원본 내용 (일부)
```
{analysis_result.get('raw_content', '내용 없음')}
```

---

"""
        elif "parse_error" in analysis_result:
            content += f"""## ⚠️ 파싱 오류

**파싱 오류**: {analysis_result['parse_error']}

### AI 원본 응답
```
{analysis_result.get('raw_response', '응답 없음')[:1000]}
{"..." if len(analysis_result.get('raw_response', '')) > 1000 else ""}
```

### 분석
이 오류는 AI가 요청한 JSON 형식으로 응답하지 않았을 때 발생합니다.
- AI 응답을 확인하여 JSON 구조가 올바른지 점검하세요
- 입력 데이터가 너무 짧거나 분석하기 어려운 내용일 수 있습니다

---

"""
        elif "raw_response" in analysis_result:
            content += f"""## AI 분석 결과 (구조화되지 않음)

### 원본 AI 응답
```
{analysis_result.get('raw_response', '응답 없음')[:2000]}
{"..." if len(analysis_result.get('raw_response', '')) > 2000 else ""}
```

### 분석
AI가 구조화된 JSON 응답 대신 일반 텍스트로 응답했습니다.
위 내용을 검토하여 수동으로 콘텍스트를 정리해주세요.

---

"""
        else:
            # 구조화된 결과 처리 - 소문자 키만 사용
            epic = analysis_result.get('epic', '❌ ERROR: epic 키 누락 - AI 응답 형식 불일치')
            contexts = analysis_result.get('contexts', [])
            
            content += f"""## Epic

{epic}

## 추출 맥락 후보
"""
            for i, context in enumerate(contexts, 1):
                name = context.get('name', f'❌ ERROR: name 키 누락 (context {i})')
                description = context.get('description', '❌ ERROR: description 키 누락')
                reason = context.get('reason', '❌ ERROR: reason 키 누락 - AI가 추출 필요 이유를 제공하지 않음')
                
                content += f"""### {i}. {name}

- **설명**: {description}
- **추출 필요 이유**: {reason}

"""
        
        content += """## 사용자 의견

---

*본 문서는 context_extractor.py에 의해 자동 생성되었습니다.*
"""
        
        return content


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='세션 로그에서 콘텍스트 주제를 추출합니다',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s de374da6-c4de-487a-8ed7-fec9991f5d90 ./logs/chat-logs/25-09-02 ./output
  %(prog)s de374da6 ./logs/chat-logs/25-09-02 ./output --provider openai
        """
    )
    
    parser.add_argument('session_id', help='추출할 세션 ID (전체 또는 앞 8자리)')
    parser.add_argument('log_folder', help='로그 파일들이 있는 폴더 경로')
    parser.add_argument('output_folder', help='결과를 저장할 폴더 경로')
    parser.add_argument('--provider', '-p', 
                       choices=['gemini', 'openai', 'anthropic', 'claude-sdk'],
                       default='claude-sdk',
                       help='사용할 AI provider (기본값: claude-sdk)')
    parser.add_argument('--log-file', '-l',
                       help='로그 파일 경로 (지정하지 않으면 자동 생성)')
    
    args = parser.parse_args()
    
    try:
        # 추출기 초기화
        extractor = SessionLogExtractor(
            session_id=args.session_id,
            log_folder=args.log_folder,
            output_folder=args.output_folder,
            ai_provider=args.provider,
            log_file=args.log_file
        )
        
        # 실행
        extractor.logger.info("콘텍스트 추출 시작")
        
        # 1. 사용자 파일 로드
        user_files = extractor.load_user_files()
        
        # 2. 콘텐츠 추출 및 결합
        combined_content = extractor.extract_and_combine_content(user_files)
        
        # 3. AI 분석
        analysis_result = extractor.analyze_with_ai(combined_content)
        
        # 4. 디버깅을 위한 JSON 저장
        import json
        debug_path = Path(args.output_folder) / f"debug_analysis_{args.session_id.split('-')[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        with open(debug_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        extractor.logger.info(f"디버그 JSON 저장: {debug_path}")
        
        # 5. 결과 저장
        output_path = extractor.save_markdown_output(analysis_result, len(user_files))
        
        extractor.logger.info(f"콘텍스트 추출 완료: {output_path}")
        print(f"✅ 분석 완료! 결과: {output_path}")
        print(f"🔍 디버그 JSON: {debug_path}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())