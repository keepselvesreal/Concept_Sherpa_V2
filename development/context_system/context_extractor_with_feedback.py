# 생성 시간: 2025-09-03 12:13:49 KST
# 핵심 내용: 사용자 의견을 반영한 실제 맥락 추출 스크립트
# 상세 내용:
#   - setup_logging (라인 41-66): 로깅 시스템 설정 함수
#   - ContextExtractorWithFeedback (라인 69-345): 사용자 피드백 기반 맥락 추출 메인 클래스
#   - extract_session_and_feedback (라인 91-128): analysis 파일에서 세션 ID와 사용자 의견 추출
#   - collect_user_files_only (라인 130-170): 특정 세션의 user 파일들만 수집 및 정렬
#   - identify_relevant_sequences (라인 172-201): 사용자 의견 기반 관련 시퀀스 번호 AI 식별
#   - analyze_response_relevance (라인 203-240): 점진적 내용 확장으로 관련성 판단
#   - extract_contexts_by_topic (라인 242-268): 관련 응답들을 맥락별로 그룹화하고 추출
#   - save_unified_contexts (라인 270-299): 통합 마크다운 파일 저장
#   - main (라인 302-345): 메인 실행 함수 및 argparse 처리
# 상태: active
# 주소: context_extractor_with_feedback
# 참조: context_extractor, ai_providers

#!/usr/bin/env python3
"""
사용자 의견 기반 맥락 추출기

AI가 제안한 맥락 후보에 대한 사용자 의견을 반영하여
실제로 필요한 맥락을 세션 기록에서 추출합니다.

사용법:
    python context_extractor_with_feedback.py <analysis_file_path> <session_log_folder> <output_path>
    
예시:
    python context_extractor_with_feedback.py ./output/context_analysis_de374da6_20250903_112612.md ./logs/chat-logs/25-09-02 ./output/extracted_contexts.md
"""

import os
import json
import logging
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

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


class ContextExtractorWithFeedback:
    """사용자 의견 기반 맥락 추출기"""
    
    def __init__(self, analysis_file_path: str, session_log_folder: str, output_path: str, 
                 ai_provider: str = 'claude-sdk', log_file: str = None):
        self.analysis_file_path = Path(analysis_file_path)
        self.session_log_folder = Path(session_log_folder)
        self.output_path = Path(output_path)
        self.ai_provider_type = ai_provider
        
        # 로깅 설정
        if not log_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = self.output_path.parent / f"context_extraction_feedback_{timestamp}.log"
        self.logger = setup_logging(str(log_file))
        
        # 상세 분석 로그 파일 경로 설정
        self.detailed_log_path = self.output_path.parent / f"detailed_analysis_{timestamp}.md"
        self.detailed_logs = []  # 상세 로그 저장용 리스트
        
        # AI Provider 초기화
        self.ai_provider = AIProviderFactory.create_provider(self.ai_provider_type)
        
        self.logger.info(f"ContextExtractorWithFeedback 초기화: analysis_file={analysis_file_path}, provider={ai_provider}")
        self.logger.info(f"상세 분석 로그 파일: {self.detailed_log_path}")
    
    def extract_session_and_feedback(self) -> Tuple[str, str]:
        """analysis 파일에서 세션 ID와 사용자 의견 추출"""
        try:
            if not self.analysis_file_path.exists():
                raise FileNotFoundError(f"analysis 파일이 존재하지 않습니다: {self.analysis_file_path}")
            
            with open(self.analysis_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 세션 ID 추출
            session_id_match = re.search(r'\*\*세션 ID\*\*: ([a-f0-9\-]+)', content)
            if not session_id_match:
                raise ValueError("analysis 파일에서 세션 ID를 찾을 수 없습니다")
            session_id = session_id_match.group(1)
            
            # 사용자 의견 추출
            user_opinion_match = re.search(r'## 사용자 의견\n(.+?)(?:\n---|\n\*본 문서는|$)', content, re.DOTALL)
            if not user_opinion_match:
                raise ValueError("analysis 파일에서 사용자 의견을 찾을 수 없습니다")
            user_opinion = user_opinion_match.group(1).strip()
            
            if not user_opinion or user_opinion == '---':
                raise ValueError("사용자 의견이 비어있습니다")
            
            self.logger.info(f"세션 ID 추출: {session_id}")
            self.logger.info(f"사용자 의견 추출: {user_opinion[:100]}...")
            
            return session_id, user_opinion
            
        except Exception as e:
            self.logger.error(f"세션 ID와 사용자 의견 추출 중 오류: {e}")
            raise
    
    def collect_user_files_only(self, session_id: str) -> List[Tuple[str, Dict[str, Any]]]:
        """특정 세션의 user 파일들만 수집하여 시퀀스별로 정렬"""
        user_files = []
        session_short_id = session_id.split('-')[0]  # de374da6 같은 짧은 형태
        
        try:
            if not self.session_log_folder.exists():
                raise FileNotFoundError(f"세션 로그 폴더가 존재하지 않습니다: {self.session_log_folder}")
            
            # 파일명 패턴: {시간}_{session_short_id}_{sequence}_user.json
            pattern = re.compile(rf'\d{{4}}_{session_short_id}_.*_user\.json$')
            
            for file_path in self.session_log_folder.glob('*.json'):
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
                raise ValueError(f"세션 ID {session_id}에 해당하는 사용자 파일을 찾을 수 없습니다")
            
            # 시퀀스 번호로 정렬
            user_files.sort(key=lambda x: x[0])
            self.logger.info(f"총 {len(user_files)}개 사용자 파일 수집 완료")
            
            return user_files
            
        except Exception as e:
            self.logger.error(f"사용자 파일 수집 중 오류: {e}")
            raise
    
    def collect_assistant_responses(self, session_id: str, relevant_sequences: List[str]) -> Dict[str, str]:
        """관련 시퀀스들의 assistant 응답들을 수집"""
        assistant_responses = {}
        session_short_id = session_id.split('-')[0]
        
        try:
            # 파일명 패턴: {시간}_{session_short_id}_{sequence}_response.json
            pattern = re.compile(rf'\d{{4}}_{session_short_id}_.*_response\.json$')
            
            for file_path in self.session_log_folder.glob('*.json'):
                if pattern.match(file_path.name):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        # 세션 ID 검증 및 관련 시퀀스 확인
                        if data.get('session_id', '').startswith(session_short_id):
                            sequence_number = data.get('sequence_number', '000')
                            if sequence_number in relevant_sequences:
                                content = data.get('content', '').strip()
                                if content:
                                    assistant_responses[sequence_number] = content
                                    self.logger.info(f"Assistant 응답 로드: {file_path.name}, sequence: {sequence_number}")
                    
                    except (json.JSONDecodeError, FileNotFoundError) as e:
                        self.logger.warning(f"Assistant 응답 파일 로드 실패 {file_path}: {e}")
                        continue
            
            self.logger.info(f"총 {len(assistant_responses)}개 assistant 응답 수집 완료")
            return assistant_responses
            
        except Exception as e:
            self.logger.error(f"Assistant 응답 수집 중 오류: {e}")
            raise
    
    def identify_relevant_sequences(self, user_opinion: str, user_files: List[Tuple[str, Dict[str, Any]]]) -> List[str]:
        """사용자 의견 기반으로 관련 시퀀스 번호들 AI 식별"""
        try:
            self.logger.info("사용자 의견 기반 관련 시퀀스 식별 시작")
            
            # 상세 로그 시작
            self.detailed_logs.append("## 1. 사용자 의견 기반 관련 시퀀스 식별 과정\n")
            self.detailed_logs.append(f"**사용자 의견**: {user_opinion}\n")
            self.detailed_logs.append(f"**분석 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 사용자 질의들을 하나의 텍스트로 결합
            user_queries = []
            self.detailed_logs.append("### 분석 대상 사용자 질의들\n")
            for sequence, file_data in user_files:
                content = file_data.get('content', '').strip()
                if content:
                    user_queries.append(f"[{sequence}] {content}")
                    self.detailed_logs.append(f"- **[{sequence}]**: {content[:200]}{'...' if len(content) > 200 else ''}\n")
            
            combined_queries = '\n\n'.join(user_queries)
            
            # AI로 관련 시퀀스 식별
            prompt = f"""사용자 의견: "{user_opinion}"

다음 사용자 질의들 중에서 위 사용자 의견과 관련된 시퀀스 번호들을 식별해주세요:

{combined_queries}

관련된 시퀀스 번호들을 쉼표로 구분하여 나열해주세요. 예: 001, 003, 007"""
            
            self.detailed_logs.append(f"\n### AI 식별 프롬프트\n```\n{prompt}\n```\n\n")
            
            response = self.ai_provider.generate_text(prompt)
            
            self.detailed_logs.append(f"### AI 응답\n```\n{response}\n```\n\n")
            
            # 시퀀스 번호 파싱
            sequence_numbers = []
            for match in re.findall(r'\b\d{3}\b', response):
                sequence_numbers.append(match)
            
            self.detailed_logs.append(f"### 파싱된 관련 시퀀스 번호들\n{', '.join(sequence_numbers) if sequence_numbers else '없음'}\n\n")
            self.detailed_logs.append("---\n\n")
            
            self.logger.info(f"식별된 관련 시퀀스: {sequence_numbers}")
            return sequence_numbers
            
        except Exception as e:
            self.logger.error(f"관련 시퀀스 식별 중 오류: {e}")
            self.detailed_logs.append(f"### ❌ 오류 발생\n{str(e)}\n\n---\n\n")
            raise
    
    def analyze_response_relevance(self, sequence: str, content: str, user_opinion: str, max_chars: int = 1000) -> bool:
        """점진적으로 내용을 확장하며 관련성 판단"""
        start_chars = 250
        step_chars = 200
        
        try:
            # 상세 로그 시작
            self.detailed_logs.append(f"### 시퀀스 [{sequence}] 점진적 분석\n")
            self.detailed_logs.append(f"**전체 길이**: {len(content)}글자\n")
            self.detailed_logs.append(f"**분석 시간**: {datetime.now().strftime('%H:%M:%S')}\n\n")
            
            for chars in range(start_chars, max_chars + 1, step_chars):
                if len(content) <= chars * 2:
                    snippet = content
                    self.detailed_logs.append(f"**{chars}글자 단계**: 전체 내용 사용 (길이가 짧음)\n")
                else:
                    start_part = content[:chars]
                    end_part = content[-chars:]
                    snippet = f"{start_part}\n\n[... 중간 생략 ...]\n\n{end_part}"
                    self.detailed_logs.append(f"**{chars}글자 단계**: 처음 {chars}글자 + 마지막 {chars}글자\n")
                
                # 단순 관련성 판단
                prompt = f"""사용자 관심사: "{user_opinion}"

다음 내용이 위 사용자 관심사와 관련이 있는지 판단해주세요:

{snippet}

관련이 있으면 "예", 없으면 "아니오"로만 답해주세요."""
                
                response = self.ai_provider.generate_text(prompt).strip()
                
                self.detailed_logs.append(f"  - AI 응답: {response}\n")
                
                if "예" in response:
                    self.detailed_logs.append(f"  - ✅ **최종 판단**: 관련성 있음 ({chars}글자에서 확정)\n\n")
                    return True
                elif "아니오" in response:
                    self.detailed_logs.append(f"  - ❌ **최종 판단**: 관련성 없음 ({chars}글자에서 확정)\n\n")
                    return False
                else:
                    self.detailed_logs.append(f"  - ⚠️ 명확하지 않은 응답, 다음 단계로 진행\n")
            
            # 최대치 도달시 전체 내용으로 판단
            self.detailed_logs.append(f"**최종 단계**: 전체 내용으로 판단\n")
            prompt = f"""사용자 관심사: "{user_opinion}"

다음 내용이 위 사용자 관심사와 관련이 있는지 판단해주세요:

{content}

관련이 있으면 "예", 없으면 "아니오"로만 답해주세요."""
            
            response = self.ai_provider.generate_text(prompt).strip()
            is_relevant = "예" in response
            
            self.detailed_logs.append(f"  - AI 응답: {response}\n")
            self.detailed_logs.append(f"  - {'✅' if is_relevant else '❌'} **최종 판단**: {'관련성 있음' if is_relevant else '관련성 없음'} (전체 내용 분석)\n\n")
            
            return is_relevant
            
        except Exception as e:
            self.logger.error(f"관련성 판단 중 오류: {e}")
            self.detailed_logs.append(f"  - ❌ **오류 발생**: {str(e)}\n\n")
            return False
    
    def extract_contexts_by_topic(self, user_opinion: str, relevant_sequences: List[str], 
                                  assistant_responses: Dict[str, str]) -> List[Dict[str, str]]:
        """관련 응답들을 맥락별로 그룹화하고 추출"""
        try:
            self.logger.info("맥락별 내용 추출 시작")
            
            # 상세 로그 시작
            self.detailed_logs.append("## 2. 최종 결합된 응답 내용\n")
            self.detailed_logs.append(f"**분석 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.detailed_logs.append(f"**관련 시퀀스 개수**: {len(relevant_sequences)}개\n\n")
            
            # 관련 시퀀스의 assistant 응답들 수집
            relevant_responses = []
            for sequence in relevant_sequences:
                if sequence in assistant_responses:
                    response_content = assistant_responses[sequence]
                    relevant_responses.append(f"[{sequence}] {response_content}")
                    
                    # 상세 로그에 기록
                    self.detailed_logs.append(f"### 시퀀스 [{sequence}] Assistant 응답\n")
                    self.detailed_logs.append(f"**길이**: {len(response_content)}글자\n")
                    self.detailed_logs.append(f"**내용 미리보기**: {response_content[:300]}{'...' if len(response_content) > 300 else ''}\n\n")
            
            combined_responses = '\n\n'.join(relevant_responses)
            
            # 최종 결합된 내용을 상세 로그에 기록
            self.detailed_logs.append("### 🔗 최종 결합된 응답 내용 (AI 분석용)\n")
            self.detailed_logs.append(f"**전체 길이**: {len(combined_responses)}글자\n")
            self.detailed_logs.append(f"**결합 내용**:\n```\n{combined_responses[:1000]}{'...' if len(combined_responses) > 1000 else ''}\n```\n\n")
            self.detailed_logs.append("---\n\n")
            
            # AI로 맥락 주제들 식별 및 내용 추출
            prompt = f"""사용자 관심사: "{user_opinion}"

다음은 사용자가 관심을 가진 주제와 관련된 AI 모델 응답들입니다:

{combined_responses}

이 응답들을 바탕으로 사용자 관심사를 세분화하여 정리해주세요. 
각 맥락별로 다음 형식으로 작성해주세요:

[맥락 제목]
사용자 관심: 이 맥락에서 사용자가 관심을 가진 구체적인 내용
모델 응답: 해당 관심사에 대한 답변 내용 정리

여러 맥락이 있다면 각각 구분해서 작성해주세요."""
            
            response = self.ai_provider.generate_text(prompt)
            
            # 응답을 파싱하여 구조화
            contexts = self._parse_context_response(response)
            
            self.logger.info(f"추출된 맥락 개수: {len(contexts)}")
            return contexts
            
        except Exception as e:
            self.logger.error(f"맥락 추출 중 오류: {e}")
            self.detailed_logs.append(f"### ❌ 맥락 추출 오류\n{str(e)}\n\n---\n\n")
            return []
    
    def _parse_context_response(self, response: str) -> List[Dict[str, str]]:
        """AI 응답을 파싱하여 맥락 구조로 변환"""
        contexts = []
        
        # 맥락 제목으로 구분하여 파싱
        sections = re.split(r'\[([^\]]+)\]', response)[1:]  # 첫 번째 빈 요소 제거
        
        for i in range(0, len(sections), 2):
            if i + 1 < len(sections):
                title = sections[i].strip()
                content = sections[i + 1].strip()
                
                # 사용자 관심과 모델 응답 추출
                user_interest = ""
                model_response = ""
                
                lines = content.split('\n')
                current_section = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('사용자 관심:'):
                        current_section = "user"
                        user_interest += line.replace('사용자 관심:', '').strip() + '\n'
                    elif line.startswith('모델 응답:'):
                        current_section = "model"
                        model_response += line.replace('모델 응답:', '').strip() + '\n'
                    elif line and current_section == "user":
                        user_interest += line + '\n'
                    elif line and current_section == "model":
                        model_response += line + '\n'
                
                if title and (user_interest.strip() or model_response.strip()):
                    contexts.append({
                        'title': title,
                        'user_interest': user_interest.strip(),
                        'model_response': model_response.strip()
                    })
        
        return contexts
    
    def save_unified_contexts(self, contexts: List[Dict[str, str]]) -> str:
        """통합 마크다운 파일에 모든 맥락 저장"""
        try:
            self.logger.info("통합 맥락 파일 저장 시작")
            
            # 출력 디렉토리 생성
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 마크다운 내용 생성
            content = ""
            for context in contexts:
                content += f"# {context['title']}\n"
                if context.get('user_interest'):
                    content += f"- 사용자 관심: {context['user_interest']}\n"
                if context.get('model_response'):
                    content += f"- 모델 응답: {context['model_response']}\n"
                content += "\n"
            
            # 파일 저장
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"통합 맥락 파일 저장 완료: {self.output_path}")
            return str(self.output_path)
            
        except Exception as e:
            self.logger.error(f"통합 맥락 파일 저장 중 오류: {e}")
            raise
    
    def save_detailed_analysis_log(self) -> str:
        """상세 분석 로그를 마크다운 파일로 저장"""
        try:
            self.logger.info("상세 분석 로그 저장 시작")
            
            # 로그 헤더 생성
            header = f"""# 상세 분석 로그

**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**분석 파일**: {self.analysis_file_path.name}
**AI Provider**: {self.ai_provider_type}

이 파일은 맥락 추출 과정의 상세한 분석 로그를 포함합니다.

---

"""
            
            # 전체 내용 결합
            full_content = header + ''.join(self.detailed_logs)
            
            # 파일 저장
            with open(self.detailed_log_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            self.logger.info(f"상세 분석 로그 저장 완료: {self.detailed_log_path}")
            return str(self.detailed_log_path)
            
        except Exception as e:
            self.logger.error(f"상세 분석 로그 저장 중 오류: {e}")
            raise


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='사용자 의견을 반영하여 실제 맥락을 추출합니다',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s ./output/context_analysis_de374da6_20250903_112612.md ./logs/chat-logs/25-09-02 ./output/extracted_contexts.md
  %(prog)s ./output/context_analysis.md ./logs ./output/contexts.md --provider openai
        """
    )
    
    parser.add_argument('analysis_file_path', help='분석 결과 파일 경로')
    parser.add_argument('session_log_folder', help='세션 로그 파일들이 있는 폴더 경로')
    parser.add_argument('output_path', help='추출된 맥락을 저장할 파일 경로')
    parser.add_argument('--provider', '-p', 
                       choices=['gemini', 'openai', 'anthropic', 'claude-sdk'],
                       default='claude-sdk',
                       help='사용할 AI provider (기본값: claude-sdk)')
    parser.add_argument('--log-file', '-l',
                       help='로그 파일 경로 (지정하지 않으면 자동 생성)')
    
    args = parser.parse_args()
    
    try:
        # 추출기 초기화
        extractor = ContextExtractorWithFeedback(
            analysis_file_path=args.analysis_file_path,
            session_log_folder=args.session_log_folder,
            output_path=args.output_path,
            ai_provider=args.provider,
            log_file=args.log_file
        )
        
        # 실행
        extractor.logger.info("사용자 의견 기반 맥락 추출 시작")
        
        # 1. 세션 ID와 사용자 의견 추출
        session_id, user_opinion = extractor.extract_session_and_feedback()
        
        # 2. 사용자 파일들 수집
        user_files = extractor.collect_user_files_only(session_id)
        
        # 3. 관련 시퀀스 식별
        relevant_sequences = extractor.identify_relevant_sequences(user_opinion, user_files)
        
        # 4. Assistant 응답들 수집
        assistant_responses = extractor.collect_assistant_responses(session_id, relevant_sequences)
        
        # 5. 점진적 분석으로 최종 관련 시퀀스 확정
        extractor.detailed_logs.append("## 3. 점진적 응답 분석 과정\n\n")
        final_relevant_responses = {}
        
        for sequence in relevant_sequences:
            if sequence in assistant_responses:
                is_relevant = extractor.analyze_response_relevance(
                    sequence, assistant_responses[sequence], user_opinion
                )
                if is_relevant:
                    final_relevant_responses[sequence] = assistant_responses[sequence]
        
        extractor.logger.info(f"최종 관련 응답: {len(final_relevant_responses)}개")
        
        # 6. 맥락별 내용 추출
        contexts = extractor.extract_contexts_by_topic(user_opinion, list(final_relevant_responses.keys()), final_relevant_responses)
        
        # 7. 통합 파일 저장
        output_path = extractor.save_unified_contexts(contexts)
        
        # 8. 상세 분석 로그 저장
        detailed_log_path = extractor.save_detailed_analysis_log()
        
        extractor.logger.info(f"맥락 추출 완료: {output_path}")
        extractor.logger.info(f"상세 분석 로그: {detailed_log_path}")
        print(f"✅ 맥락 추출 완료! 결과: {output_path}")
        print(f"🔍 상세 분석 로그: {detailed_log_path}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())