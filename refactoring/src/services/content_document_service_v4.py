# 생성 시간: Sat Sep  6 11:08:48 KST 2025
# 핵심 내용: 콘텐츠 문서 생성 서비스 - 두 가지 핵심 기능만 제공 (완전 재구성)
# 상세 내용:
#   - ContentDocumentService (라인 25-80): 메인 서비스 클래스
#   - detect_section_content (라인 30-110): 일회성 쿼리로 섹션별 has_content 분석
#   - extract_section_content (라인 112-220): 멀티턴으로 각 섹션 내용 추출
#   - _parse_json_response (라인 222-260): JSON 응답 파싱 지원 메서드
#   - _save_content_json (라인 262-290): content.json 파일 저장 메서드
#   - _save_section_files (라인 292-330): sections 폴더에 섹션 파일 저장 메서드
# 상태: active
# 참조: content_document_service_v3.py (완전 재구성)

from typing import Dict, List, Any, Optional
import json
import os
import re
from pathlib import Path
import sys
from .ai_service_v4 import AIService

# text_utils import
sys.path.append(str(Path(__file__).parent.parent / "utils"))
from text_utils import normalize_title

class ContentDocumentService:
    """콘텐츠 문서 생성 서비스 - 두 가지 핵심 기능만 제공"""
    
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
    
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
        try:
            # 🔍 **입력 확인**
            self.logger.info(f"📥 **입력 확인** - 섹션 수: {len(chapter_sections)}, 장 내용 길이: {len(chapter_content)}자")
            
            # AI 서비스 초기화
            ai_service = AIService(self.config_manager, self.logger, f"information_integration.{stage_name}")
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
            
            # 🔍 **AI 응답 확인**
            self.logger.info(f"📤 **AI 응답** - 길이: {len(response_text)}자, 첫 100자: {response_text[:100]}...")
            
            # JSON 응답 파싱
            sections_with_content = self._parse_json_response(response_text, "섹션 목록")
            
            # 🔍 **파싱 결과 확인**
            content_count = len([s for s in sections_with_content if s.get('has_content', False)])
            self.logger.info(f"📊 **파싱 결과** - 총 {len(sections_with_content)}개 섹션, 내용 포함: {content_count}개")
            
            return sections_with_content
            
        except Exception as e:
            error_msg = f"섹션 내용 분석 실패: {str(e)}"
            self.logger.error(f"❌ **오류 발생**: {error_msg}")
            
            # 재시도 로직: 최대 3회까지 재시도
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    self.logger.warning(f"🔄 **재시도** {attempt}/{max_retries}...")
                    response_text = await ai_service.query_single_request(detect_prompt)
                    sections_with_content = self._parse_json_response(response_text, "섹션 목록")
                    self.logger.info(f"✅ **재시도 성공** - {attempt}회차에서 성공")
                    return sections_with_content
                except Exception as retry_e:
                    self.logger.error(f"❌ **재시도 실패** {attempt}회차: {str(retry_e)}")
                    if attempt == max_retries:
                        self.logger.error(f"❌ **최대 재시도 실패** - {max_retries}회 모두 실패")
                        raise Exception(f"섹션 내용 분석 최대 재시도 실패: {str(e)}")
            
            # 여기에 도달하면 모든 재시도 실패
            raise Exception(f"섹션 내용 분석 실패: {str(e)}")

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
        try:
            if not content_sections:
                self.logger.info("추출할 섹션이 없습니다")
                return []
            
            # 🔍 **입력 확인**
            self.logger.info(f"📥 **추출 입력** - 대상 섹션: {len(content_sections)}개")
            
            # AI 서비스 초기화
            ai_service = AIService(self.config_manager, self.logger, f"information_integration.{stage_name}")
            self.logger.info(f"섹션 내용 추출 시작 - 제공자: {ai_service.get_name()}, 대상: {len(content_sections)}개")
            
            # 새 세션 생성 (SessionInfo 객체 반환)
            session_info = await ai_service.create_session()
            self.logger.info(f"추출용 세션 생성: {session_info.provider_type}")
            
            # 첫 번째 턴: 컨텍스트 설정
            context_prompt = f"""다음 장의 전체 내용과 목차 구조를 제공합니다. 이후 개별 섹션별로 해당 섹션만의 정확한 내용을 추출하겠습니다.

장 전체 내용:
```markdown
{chapter_content}
```

장 목차 구조:
{json.dumps(content_sections, ensure_ascii=False, indent=2)}

중요한 추출 규칙:
1. 각 섹션은 해당 섹션 제목부터 다음 동일/상위 레벨 섹션 직전까지만 추출
2. 하위 섹션들은 포함하지 않음 (별도 요청시에만 추출)
3. 순수한 텍스트 내용만 추출 (메타데이터, 포맷팅 태그 제외)

준비가 되면 "준비완료"라고 응답해주세요."""
            
            self.logger.info("컨텍스트 설정 중...")
            context_response = await ai_service.query_with_persistent_session(context_prompt, session_info)
            self.logger.info(f"✅ **컨텍스트 설정 완료**: {context_response[:50]}...")
            
            # 각 섹션별 내용 추출
            extracted_sections = []
            
            for section in content_sections:
                section_title = section.get('title', '제목 없음')
                
                try:
                    # 다음 섹션 제목 찾기 (간단히 다음 항목에서 가져오기)
                    current_index = content_sections.index(section)
                    next_section_title = None
                    
                    if current_index + 1 < len(content_sections):
                        next_section_title = content_sections[current_index + 1].get('title')
                    
                    # 개별 섹션 추출 프롬프트
                    if next_section_title:
                        section_prompt = f"""섹션 제목: "{section_title}"

위 장 내용에서 "{section_title}" 섹션의 내용만 정확히 추출해주세요.

추출 범위:
- 시작: "{section_title}" 제목 부분부터
- 종료: "{next_section_title}" 제목 직전까지

추출 요구사항:
1. 해당 섹션의 본문 내용만 추출 (하위 섹션 제외)
2. 페이지 정보(--- 페이지 N ---)는 반드시 포함
3. 메타데이터 제외: **생성 시간**, ---, # 제목, ```markdown 등
4. 섹션 제목은 포함하지 않음

응답: 순수 본문 내용만 반환 (페이지 정보는 포함)"""
                    else:
                        section_prompt = f"""섹션 제목: "{section_title}"

위 장 내용에서 "{section_title}" 섹션의 내용만 정확히 추출해주세요.

추출 범위:
- 시작: "{section_title}" 제목 부분부터  
- 종료: 장의 끝까지

추출 요구사항:
1. 해당 섹션의 본문 내용만 추출 (하위 섹션 제외)
2. 순수한 텍스트만 (```markdown, **생성시간** 등 메타데이터 제외)
3. 섹션 제목은 포함하지 않음

응답: 추출된 본문 내용만 반환"""
                    
                    self.logger.info(f"📝 **섹션 추출 중**: '{section_title}'")
                    extracted_content = await ai_service.query_with_persistent_session(section_prompt, session_info)
                    
                    # 🔍 **추출 결과 확인**
                    self.logger.info(f"📤 **추출 완료**: '{section_title}' ({len(extracted_content)} 문자)")
                    
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
                    
                except Exception as e:
                    error_msg = f"섹션 '{section_title}' 추출 실패: {str(e)}"
                    self.logger.error(f"❌ **섹션 추출 오류**: {error_msg}")
                    # 한 섹션 실패 시 전체 실패
                    raise Exception(error_msg)
            
            self.logger.info(f"✅ **전체 섹션 추출 완료**: {len(extracted_sections)}개")
            return extracted_sections
            
        except Exception as e:
            error_msg = f"섹션 내용 추출 실패: {str(e)}"
            self.logger.error(f"❌ **추출 전체 실패**: {error_msg}")
            
            # 재시도 로직: 실패한 지점부터 다시 시도
            max_retries = 2
            for attempt in range(1, max_retries + 1):
                try:
                    self.logger.warning(f"🔄 **추출 재시도** {attempt}/{max_retries}...")
                    
                    # 새로운 세션으로 전체 작업 재시작
                    retry_session_info = await ai_service.create_session()
                    self.logger.info(f"재시도용 새 세션 생성: {retry_session_info.provider_type}")
                    
                    # 컨텍스트 재설정
                    context_response = await ai_service.query_with_persistent_session(context_prompt, retry_session_info)
                    
                    # 전체 섹션 재추출
                    retry_extracted_sections = []
                    for section in content_sections:
                        section_title = section.get('title', '제목 없음')
                        
                        # 다음 섹션 제목 찾기
                        current_index = content_sections.index(section)
                        next_section_title = None
                        
                        if current_index + 1 < len(content_sections):
                            next_section_title = content_sections[current_index + 1].get('title')
                        
                        if next_section_title:
                            section_prompt = f"""섹션 제목: "{section_title}"

위 장 내용에서 "{section_title}" 섹션의 내용만 정확히 추출해주세요.

추출 범위:
- 시작: "{section_title}" 제목 부분부터
- 종료: "{next_section_title}" 제목 직전까지

추출 요구사항:
1. 해당 섹션의 본문 내용만 추출 (하위 섹션 제외)
2. 페이지 정보(--- 페이지 N ---)는 반드시 포함
3. 메타데이터 제외: **생성 시간**, ---, # 제목, ```markdown 등
4. 섹션 제목은 포함하지 않음

응답: 순수 본문 내용만 반환 (페이지 정보는 포함)"""
                        else:
                            section_prompt = f"""섹션 제목: "{section_title}"

위 장 내용에서 "{section_title}" 섹션의 내용만 정확히 추출해주세요.

추출 범위:
- 시작: "{section_title}" 제목 부분부터  
- 종료: 장의 끝까지

추출 요구사항:
1. 해당 섹션의 본문 내용만 추출 (하위 섹션 제외)
2. 페이지 정보(--- 페이지 N ---)는 반드시 포함
3. 메타데이터 제외: **생성 시간**, ---, # 제목, ```markdown 등
4. 섹션 제목은 포함하지 않음

응답: 순수 본문 내용만 반환 (페이지 정보는 포함)"""
                        
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
                    
                    self.logger.info(f"✅ **재시도 성공**: {attempt}회차에서 {len(retry_extracted_sections)}개 섹션")
                    return retry_extracted_sections
                    
                except Exception as retry_e:
                    self.logger.error(f"❌ **재시도 실패** {attempt}회차: {str(retry_e)}")
                    if attempt == max_retries:
                        self.logger.error(f"❌ **최대 재시도 실패** - {max_retries}회 모두 실패")
                        raise Exception(f"섹션 내용 추출 최대 재시도 실패: {str(e)}")
            
            # 여기에 도달하면 모든 재시도 실패
            raise Exception(f"섹션 내용 추출 실패: {str(e)}")

    def _parse_json_response(self, response_text: str, section_title: str) -> List[Dict]:
        """AI 응답에서 JSON 배열 파싱 - 엄격한 파싱, 실패 시 예외 발생"""
        try:
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
            
            self.logger.info(f"✅ **JSON 파싱 성공**: {len(parsed_data)}개 항목")
            return parsed_data
            
        except (json.JSONDecodeError, ValueError) as e:
            error_msg = f"JSON 파싱 실패 ({section_title}): {e}"
            self.logger.error(f"❌ **JSON 파싱 오류**: {error_msg}")
            raise Exception(error_msg)

    def _save_content_json(self, sections_with_content: List[Dict], chapter_folder: str):
        """content.json 파일 저장 - 지정된 필드만 포함"""
        try:
            # 🔍 **저장 입력 확인**
            self.logger.info(f"📥 **content.json 저장** - 섹션: {len(sections_with_content)}개, 대상 폴더: {chapter_folder}")
            
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
            self.logger.info(f"✅ **content.json 저장 완료**: {content_file_path}")
            self.logger.info(f"📊 **저장 결과** - 총 {len(content_json)}개 섹션, 내용 포함: {content_count}개")
            
        except Exception as e:
            error_msg = f"content.json 저장 실패: {str(e)}"
            self.logger.error(f"❌ **content.json 저장 오류**: {error_msg}")
            raise Exception(error_msg)

    def _save_section_files(self, extracted_sections: List[Dict], chapter_folder: str):
        """sections/ 폴더에 개별 섹션 파일 저장"""
        try:
            # 🔍 **저장 입력 확인**
            self.logger.info(f"📥 **섹션 파일 저장** - 섹션: {len(extracted_sections)}개, 대상 폴더: {chapter_folder}")
            
            # sections 폴더 생성
            sections_dir = os.path.join(chapter_folder, "sections")
            os.makedirs(sections_dir, exist_ok=True)
            self.logger.info(f"✅ **sections 폴더 확인**: {sections_dir}")
            
            # 각 섹션별 파일 저장
            saved_count = 0
            for section in extracted_sections:
                section_title = section.get('section_title', '제목없음')
                extracted_content = section.get('extracted_content', '')
                
                if not extracted_content.strip():
                    self.logger.warning(f"⚠️ **빈 내용 건너뜀**: 섹션 '{section_title}' 내용이 비어있음")
                    continue
                
                # 안전한 파일명 생성
                safe_filename = f"{normalize_title(section_title)}.md"
                file_path = os.path.join(sections_dir, safe_filename)
                
                # 마크다운 파일 저장
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_content)
                
                saved_count += 1
                self.logger.info(f"📄 **섹션 파일 저장**: {safe_filename} ({len(extracted_content)} 문자)")
            
            self.logger.info(f"✅ **sections 폴더 저장 완료**: {saved_count}개 파일")
            
        except Exception as e:
            error_msg = f"섹션 파일 저장 실패: {str(e)}"
            self.logger.error(f"❌ **섹션 파일 저장 오류**: {error_msg}")
            raise Exception(error_msg)