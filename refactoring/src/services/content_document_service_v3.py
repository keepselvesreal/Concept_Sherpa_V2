# 생성 시간: Thu Sep  4 17:25:45 KST 2025
# 핵심 내용: 콘텐츠 문서 생성 서비스 (네이티브 세션 방식)
# 상세 내용:
#   - ContentDocumentService (라인 25-150): 메인 서비스 클래스 
#   - extract_sections (라인 45-90): 네이티브 세션 기반 섹션 추출
#   - _analyze_sections_with_session (라인 92-130): 통합 세션 기반 분석
#   - _extract_content_with_session (라인 132-170): 통합 세션 기반 내용 추출
#   - ContentDocumentResult (라인 18-23): 처리 결과 데이터 클래스
# 상태: active
# 참조: content_document_service_v2.py (네이티브 세션 방식으로 통합)

from typing import Dict, List, Any
from dataclasses import dataclass, field

# AI 서비스 임포트
from .ai_service_v3 import AIService

@dataclass
class ContentDocumentResult:
    """콘텐츠 문서 생성 결과 데이터 클래스"""
    success: bool = False
    processed_sections: int = 0
    content_sections: int = 0
    extracted_documents: int = 0
    errors: List[str] = field(default_factory=list)
    updated_chapter_sections: List[Dict[str, Any]] = field(default_factory=list)
    section_documents: List[Dict[str, Any]] = field(default_factory=list)
    session_info: Dict[str, Any] = field(default_factory=dict)  # 세션 정보 추가

class ContentDocumentService:
    """콘텐츠 문서 생성 서비스 - 네이티브 세션 방식"""
    
    def __init__(self, config_manager, logger):
        """
        Args:
            config_manager: 설정 관리자
            logger: 로거 인스턴스
        """
        self.config_manager = config_manager
        self.logger = logger
        
    async def extract_sections(self, chapter_sections: List[Dict[str, Any]], 
                             chapter_content: str,
                             stage_name: str = "chapter_content_extraction") -> ContentDocumentResult:
        """
        장의 각 섹션에서 실질적인 내용 포함 여부 분석 및 추출 (네이티브 세션 방식)
        
        Args:
            chapter_sections: 장을 구성하는 섹션 목차 정보 리스트
            chapter_content: 장 전체의 마크다운 내용  
            stage_name: 설정에서 사용할 단계명 (기본값: "chapter_content_extraction")
            
        Returns:
            ContentDocumentResult: 처리 결과
        """
        result = ContentDocumentResult()
        
        try:
            # AI 서비스 초기화 (설정 기반 제공자 선택)
            ai_service = AIService(self.config_manager, self.logger, f"workspace_preparation.{stage_name}")
            
            self.logger.info(f"섹션 추출 시작 - 제공자: {ai_service.get_name()}, 섹션 수: {len(chapter_sections)}")
            
            # 네이티브 세션 생성
            session_id = await ai_service.create_session()
            session_info = ai_service.get_session_info(session_id)
            
            # 세션 연속성 추적을 위한 핵심 정보 로깅
            native_data = session_info.native_session_data if session_info else {}
            self.logger.info(f"🔗 [SESSION] 생성: {session_id[:12]}... | {ai_service.get_name()} | 네이티브키: {list(native_data.keys())[:3]} | 대상: {len(chapter_sections)}섹션")
            
            result.session_info = {
                "session_id": session_id,
                "provider_type": session_info.provider_type if session_info else "unknown", 
                "provider_name": ai_service.get_name(),
                "native_keys": list(native_data.keys()) if native_data else []
            }
            
            # 1단계: 세션 기반 섹션 내용 존재 여부 분석
            sections_with_content = await self._analyze_sections_with_session(
                chapter_sections, chapter_content, ai_service, session_id
            )
            
            result.processed_sections = len(chapter_sections)
            result.content_sections = len([s for s in sections_with_content if s.get('has_content', False)])
            result.updated_chapter_sections = sections_with_content
            
            # 2단계: has_content=True인 섹션들의 실제 내용 추출
            if result.content_sections > 0:
                section_documents = await self._extract_content_with_session(
                    sections_with_content, chapter_content, ai_service, session_id
                )
                result.section_documents = section_documents
                result.extracted_documents = len(section_documents)
            
            result.success = True
            
            # 세션 완료 요약 - 단순한 성공 지표만
            total_queries = len(chapter_sections) + len([s for s in sections_with_content if s.get('has_content', False)]) + 2
            final_usage = ai_service.get_session_info(session_id).message_count if ai_service.get_session_info(session_id) else 0
            
            self.logger.info(f"🎯 [SESSION] 완료: {session_id[:12]}... | 총쿼리: {total_queries} | 최종사용: {final_usage} | 성공")
            
            self.logger.info(f"섹션 추출 완료 - 처리: {result.processed_sections}, 내용 포함: {result.content_sections}, 추출: {result.extracted_documents}")
            
        except Exception as e:
            error_msg = f"섹션 추출 실패: {str(e)}"
            self.logger.error(error_msg)
            result.errors.append(error_msg)
            result.success = False
        
        return result
    
    async def _analyze_sections_with_session(self, chapter_sections: List[Dict[str, Any]], 
                                           chapter_content: str, 
                                           ai_service: AIService,
                                           session_id: str) -> List[Dict[str, Any]]:
        """
        네이티브 세션을 사용한 섹션 내용 존재 여부 분석 (모든 AI 제공자 통합)
        
        Args:
            chapter_sections: 섹션 목차 정보
            chapter_content: 장 전체 내용
            ai_service: AI 서비스 인스턴스
            session_id: 네이티브 세션 ID
        
        Returns:
            has_content 필드가 추가된 섹션 리스트
        """
        updated_sections = []
        
        try:
            # 1단계: 컨텍스트 설정 (장 전체 내용 제공)
            context_prompt = f"""다음은 한 장(chapter)의 전체 내용입니다. 이제 이 장의 각 섹션별로 실질적인 내용 포함 여부를 분석하겠습니다.

장 전체 내용:
```markdown
{chapter_content}
```

분석 기준:
- 실질 내용 있음 (has_content: true): 30자 이상의 의미있는 텍스트, 설명문, 예제, 코드 등
- 실질 내용 없음 (has_content: false): 단순 제목이나 페이지 번호, 목차만 있는 경우

이제 각 섹션별로 질문하겠습니다. 위 내용을 기억해주세요."""

            # 컨텍스트 설정 - 세션 생존 여부만 추적
            usage_before = ai_service.get_session_info(session_id).message_count if ai_service.get_session_info(session_id) else 0
            self.logger.info(f"📝 [SESSION] 컨텍스트설정: {session_id[:12]}... | 사용#{usage_before} | 내용: {len(chapter_content)}자")
            
            await ai_service.query_with_session(context_prompt, session_id)
            
            # 세션 사용 횟수 증가 확인 (세션 연속성 간접 확인)
            usage_after = ai_service.get_session_info(session_id).message_count if ai_service.get_session_info(session_id) else 0
            self.logger.info(f"✅ [SESSION] 컨텍스트완료: {session_id[:12]}... | 사용#{usage_after} | 증가: {'Yes' if usage_after > usage_before else 'No'}")
            
            # 2단계: 각 섹션별 분석 (네이티브 세션 유지)
            for section in chapter_sections:
                try:
                    section_title = section.get('title', '제목 없음')
                    section_query = f"""섹션 제목: "{section_title}"

위에서 제공한 장 전체 내용에서 이 섹션이 실질적인 내용을 담고 있나요?

JSON 형식으로만 응답해주세요:
{{"has_content": true/false, "reason": "판단 근거"}}"""
                    
                    # 주요 섹션에서만 세션 활성 상태 체크 (매번 하지 않고)
                    if len(chapter_sections) <= 5 or section == chapter_sections[0] or section == chapter_sections[-1]:
                        current_usage = ai_service.get_session_info(session_id).message_count if ai_service.get_session_info(session_id) else 0
                        self.logger.info(f"❓ [SESSION] 섹션분석: '{section_title}' | 사용#{current_usage}")
                    
                    response_text = await ai_service.query_with_session(section_query, session_id)
                    
                    # JSON 파싱 및 결과 저장
                    has_content = self._parse_has_content_response(response_text, section_title)
                    updated_section = section.copy()
                    updated_section['has_content'] = has_content
                    updated_sections.append(updated_section)
                    
                    self.logger.info(f"섹션 분석 완료: '{section_title}' → {has_content}")
                    
                except Exception as e:
                    self.logger.warning(f"섹션 분석 실패: '{section_title}' - {str(e)}")
                    updated_section = section.copy()
                    updated_section['has_content'] = False  # 실패 시 기본값
                    updated_sections.append(updated_section)
            
        except Exception as e:
            self.logger.error(f"세션 기반 분석 실패: {str(e)}")
            # 세션 실패 시 개별 요청 방식으로 fallback
            return await self._analyze_with_individual_requests(
                chapter_sections, chapter_content, ai_service
            )
        
        return updated_sections
    
    async def _extract_content_with_session(self, sections_with_content: List[Dict[str, Any]], 
                                          chapter_content: str, 
                                          ai_service: AIService,
                                          session_id: str) -> List[Dict[str, Any]]:
        """네이티브 세션을 사용한 내용 추출"""
        section_documents = []
        content_sections = [s for s in sections_with_content if s.get('has_content', False)]
        
        if not content_sections:
            return section_documents
        
        try:
            # 컨텍스트 설정 (동일 세션 사용)
            context_prompt = f"""이제 앞서 분석한 장에서 실질 내용이 있는 섹션들의 내용을 정확히 추출하겠습니다.

각 섹션별로 해당하는 내용을 정확히 추출하여 마크다운 형식으로 제공해주세요."""

            # 내용 추출 단계 - 세션 살아있는지만 확인
            self.logger.info(f"📄 [SESSION] 추출컨텍스트: {session_id[:12]}... | 대상섹션: {len(content_sections)}")
            
            await ai_service.query_with_session(context_prompt, session_id)
            
            self.logger.info(f"✅ [SESSION] 추출준비완료: {session_id[:12]}... | 내용추출 시작")
            
            # 각 섹션별 내용 추출 (네이티브 세션 유지)
            for section in content_sections:
                try:
                    section_title = section.get('title', '제목 없음')
                    
                    extraction_query = f"""섹션 제목: "{section_title}"

위 장 내용에서 이 섹션에 해당하는 내용을 정확히 추출해주세요.

추출 요청:
1. 섹션 제목에 해당하는 모든 관련 내용
2. 제목, 설명, 예제, 코드 등 포함  
3. 마크다운 형식 유지

응답: 추출된 섹션의 마크다운 내용만 반환"""
                    
                    # [디버깅] 섹션별 내용 추출 전 세션 확인
                    self.logger.info(f"📝 [MULTITURN_DEBUG] 내용 추출 시작: '{section_title}' | 세션: {session_id[:12]}... | 컨텍스트 기억 활용")
                    
                    extracted_content = await ai_service.query_with_session(extraction_query, session_id)
                    
                    section_document = {
                        "section_id": section.get('id'),
                        "section_title": section_title,
                        "has_content": True,
                        "extracted_content": extracted_content,
                        "content_length": len(extracted_content),
                        "ai_provider": ai_service.get_name(),
                        "extraction_method": "native_session",
                        "session_id": session_id
                    }
                    
                    section_documents.append(section_document)
                    self.logger.info(f"섹션 내용 추출 완료: '{section_title}' ({len(extracted_content)} 문자)")
                    
                except Exception as e:
                    self.logger.error(f"섹션 내용 추출 실패: '{section_title}' - {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"세션 기반 내용 추출 실패: {str(e)}")
            # 개별 요청 방식으로 fallback
            return await self._extract_content_individually(content_sections, chapter_content, ai_service)
        
        return section_documents
    
    async def _analyze_with_individual_requests(self, chapter_sections: List[Dict[str, Any]], 
                                              chapter_content: str, 
                                              ai_service: AIService) -> List[Dict[str, Any]]:
        """개별 요청 방식으로 섹션 분석 (fallback용)"""
        updated_sections = []
        
        for section in chapter_sections:
            try:
                section_title = section.get('title', '제목 없음')
                
                prompt = f"""다음 장 내용에서 특정 섹션의 실질적인 내용 포함 여부를 분석해주세요.

장 전체 내용:
```markdown
{chapter_content[:3000]}...
```

분석 대상 섹션: "{section_title}"

분석 기준:
- 실질 내용 있음: 30자 이상의 의미있는 텍스트, 설명문, 예제, 코드 등
- 실질 내용 없음: 단순 제목이나 페이지 번호, 목차만 있는 경우

JSON 형식으로만 응답:
{{"has_content": true/false, "reason": "판단 근거"}}"""
                
                additional_data = {
                    "section_title": section_title,
                    "analysis_type": "content_detection"
                }
                
                response_text = await ai_service.query(prompt, additional_data)
                has_content = self._parse_has_content_response(response_text, section_title)
                
                updated_section = section.copy()
                updated_section['has_content'] = has_content
                updated_sections.append(updated_section)
                
                self.logger.info(f"섹션 분석 완료: '{section_title}' → {has_content}")
                
            except Exception as e:
                self.logger.warning(f"섹션 분석 실패: '{section_title}' - {str(e)}")
                updated_section = section.copy()
                updated_section['has_content'] = False
                updated_sections.append(updated_section)
        
        return updated_sections
    
    async def _extract_content_individually(self, content_sections: List[Dict[str, Any]], 
                                          chapter_content: str, 
                                          ai_service: AIService) -> List[Dict[str, Any]]:
        """개별 요청 방식으로 내용 추출 (fallback)"""
        section_documents = []
        
        for section in content_sections:
            try:
                section_title = section.get('title', '제목 없음')
                
                extraction_prompt = f"""다음 장 내용에서 특정 섹션의 내용을 정확히 추출해주세요:

추출 대상 섹션: "{section_title}"

장 전체 내용:
```markdown
{chapter_content}
```

추출 요청:
1. 위 섹션 제목에 해당하는 내용을 정확히 추출
2. 제목, 설명, 예제, 코드 등 모든 관련 내용 포함  
3. 마크다운 형식 유지

응답: 추출된 섹션의 마크다운 내용만 반환"""
                
                additional_data = {
                    "section_title": section_title,
                    "extraction_type": "section_content"
                }
                
                extracted_content = await ai_service.query(extraction_prompt, additional_data)
                
                section_document = {
                    "section_id": section.get('id'),
                    "section_title": section_title,
                    "has_content": True,
                    "extracted_content": extracted_content,
                    "content_length": len(extracted_content),
                    "ai_provider": ai_service.get_name(),
                    "extraction_method": "individual_request"
                }
                
                section_documents.append(section_document)
                self.logger.info(f"섹션 내용 추출 완료: '{section_title}' ({len(extracted_content)} 문자)")
                
            except Exception as e:
                self.logger.error(f"섹션 내용 추출 실패: '{section_title}' - {str(e)}")
        
        return section_documents
    
    def _parse_has_content_response(self, response_text: str, section_title: str) -> bool:
        """AI 응답에서 has_content 값 파싱"""
        try:
            import json
            import re
            
            # JSON 블록 찾기
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                # JSON 블록이 없으면 중괄호로 감싼 부분 찾기
                json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(0)
                else:
                    json_text = response_text
            
            result = json.loads(json_text)
            return result.get('has_content', False)
            
        except (json.JSONDecodeError, AttributeError) as e:
            self.logger.warning(f"JSON 파싱 실패 ({section_title}): {e}")
            # 텍스트에서 true/false 직접 찾기
            if 'true' in response_text.lower():
                return True
            elif 'false' in response_text.lower():
                return False
            else:
                return False  # 파싱 실패 시 기본값