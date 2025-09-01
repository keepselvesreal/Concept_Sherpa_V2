# 생성 시간: 2025-08-28 11:10:38 KST
# 핵심 내용: 참조 문서의 영어 내용을 한글로 번역하여 _kr.md 파일로 저장하는 스크립트
# 상세 내용:
#   - main(): 메인 실행 함수, 명령행 인자 처리 및 전체 플로우 관리 (line 30-55)
#   - translate_document(): 문서 번역 처리 함수, 파일 읽기부터 저장까지 전체 로직 (line 57-120)
#   - setup_logging(): 로깅 시스템 초기화 (line 122-145)
#   - translate_with_claude(): Claude SDK를 사용한 번역 API 호출 (line 147-220)
# 상태: active
# 주소: document_translator
# 참조: supplementary_context_analyzer.py (Claude SDK 사용법 참조)

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional

try:
    from claude_code_sdk import query as claude_query
except ImportError as e:
    print(f"❌ claude_code_sdk 모듈을 찾을 수 없습니다: {e}")
    print("다음 명령어로 설치하세요: npm install -g @anthropic-ai/claude-code")
    sys.exit(1)


async def main():
    """메인 실행 함수"""
    try:
        # 명령행 인자 파싱
        parser = argparse.ArgumentParser(description='참조 문서 영어 내용을 한글로 번역')
        parser.add_argument('file_path', type=str, help='번역할 문서 파일 경로')
        parser.add_argument('--verbose', action='store_true', help='상세 로그 출력')
        
        args = parser.parse_args()
        
        # 로깅 초기화
        logger = setup_logging(args.verbose)
        
        # 문서 번역 처리
        result = await translate_document(args.file_path, logger)
        
        if result['success']:
            print(f"✅ 번역 완료: {result['output_file']}")
            return 0
        else:
            print(f"❌ 번역 실패: {result['error']}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
        return 1
    except Exception as e:
        print(f"❌ 예상치 못한 오류가 발생했습니다: {e}")
        return 1


async def translate_document(file_path: str, logger: logging.Logger) -> dict:
    """문서 번역 처리 함수"""
    start_time = time.time()
    
    try:
        # 파일 경로 검증
        input_file = Path(file_path)
        if not input_file.exists():
            error_msg = f"파일을 찾을 수 없습니다: {file_path}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        if not input_file.suffix.lower() in ['.md', '.txt']:
            error_msg = f"지원하지 않는 파일 형식입니다: {input_file.suffix}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 출력 파일 경로 생성
        output_file = input_file.parent / f"{input_file.stem}_kr{input_file.suffix}"
        
        # 파일 읽기
        logger.info(f"파일 읽는 중: {input_file}")
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                full_content = f.read()
        except Exception as e:
            error_msg = f"파일 읽기 실패: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        if not full_content.strip():
            error_msg = "파일이 비어있습니다"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # "# 내용" 섹션 이후 내용만 추출
        content_section_marker = "# 내용"
        marker_index = full_content.find(content_section_marker)
        
        if marker_index == -1:
            error_msg = f"'{content_section_marker}' 섹션을 찾을 수 없습니다"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # "# 내용" 라인 이후부터 추출 (구분선 "---" 다음부터)
        content_start = full_content.find("---", marker_index)
        if content_start == -1:
            # "---" 구분선이 없으면 "# 내용" 다음 줄부터
            content_start = marker_index + len(content_section_marker)
        else:
            content_start += 3  # "---" 다음부터
        
        content = full_content[content_start:].strip()
        
        if not content:
            error_msg = "내용 섹션이 비어있습니다"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        logger.info(f"전체 파일 크기: {len(full_content)} 문자")
        logger.info(f"번역 대상 내용 크기: {len(content)} 문자")
        
        # Claude를 통한 번역
        logger.info("번역 요청 중...")
        logger.debug(f"번역 대상 내용 첫 200자: {content[:200]}...")
        
        translation_start_time = time.time()
        translated_content = await translate_with_claude(content, logger)
        translation_elapsed = time.time() - translation_start_time
        logger.info(f"번역 API 호출 완료 ({translation_elapsed:.2f}초)")
        
        if not translated_content:
            error_msg = "번역 결과를 받지 못했습니다"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 결과 저장
        logger.info(f"번역 결과 저장 중: {output_file}")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
        except Exception as e:
            error_msg = f"파일 저장 실패: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        elapsed_time = time.time() - start_time
        logger.info(f"번역 완료 ({elapsed_time:.2f}초)")
        
        return {
            'success': True, 
            'output_file': str(output_file),
            'elapsed_time': elapsed_time
        }
        
    except Exception as e:
        error_msg = f"문서 번역 중 오류: {e}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}


def setup_logging(verbose: bool = False) -> logging.Logger:
    """로깅 시스템 초기화"""
    logger = logging.getLogger('document_translator')
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 로그 레벨 설정
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # 포맷터
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


async def translate_with_claude(content: str, logger: logging.Logger, max_retries: int = 3) -> Optional[str]:
    """Claude SDK를 사용한 번역 API 호출"""
    
    logger.debug(f"프롬프트 생성 중... (콘텐츠 크기: {len(content)} 문자)")
    
    # 번역 프롬프트
    prompt = f"""참조 문서의 내용 부분에 해당하는 영어만 해당 문장/문단 밑에 한글 번역을 추가해서 새로운 파일명으로 저장해줘. 기존 라인 정보(Line {{라인 숫자}})는 그대로 유지되어야 함. 추가된 한글 번역에는 라인 정보 추가할 필요 없음.

번역 시 주의사항:
1. Line 번호는 절대 변경하지 말 것
2. 영어 문장/문단 바로 아래에 한글 번역 추가
3. 번역은 자연스럽고 이해하기 쉽게 작성
4. 기술 용어는 적절히 한글화하되 원문도 병기
5. 문서의 전체적인 구조와 포맷은 유지

문서 내용:
{content}

위 문서를 번역 규칙에 따라 처리해서 완전한 번역본을 제공해주세요."""

    retry_delay = 2.0
    
    for attempt in range(max_retries):
        api_start_time = time.time()
        try:
            logger.info(f"Claude API 호출 중... (시도: {attempt + 1}/{max_retries})")
            logger.debug(f"프롬프트 길이: {len(prompt)} 문자")
            
            responses = []
            response_count = 0
            
            async for message in claude_query(prompt=prompt):
                response_count += 1
                logger.debug(f"응답 청크 {response_count} 받음")
                
                if hasattr(message, 'content'):
                    content_obj = message.content
                    if isinstance(content_obj, list):
                        for block in content_obj:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                                logger.debug(f"텍스트 블록 추가됨 (길이: {len(block.text)})")
                    elif hasattr(content_obj, 'text'):
                        responses.append(content_obj.text)
                        logger.debug(f"텍스트 응답 추가됨 (길이: {len(content_obj.text)})")
                    else:
                        text_content = str(content_obj)
                        responses.append(text_content)
                        logger.debug(f"문자열 변환 응답 추가됨 (길이: {len(text_content)})")
            
            api_elapsed = time.time() - api_start_time
            translated_content = '\n'.join(responses) if responses else ''
            
            logger.info(f"API 응답 수신 완료 ({api_elapsed:.2f}초, {response_count}개 청크, 총 {len(translated_content)} 문자)")
            
            if translated_content.strip():
                logger.info("번역 완료")
                logger.debug(f"번역 결과 첫 200자: {translated_content[:200]}...")
                return translated_content
            else:
                logger.warning(f"빈 응답 받음, 재시도 중... ({attempt + 1}/{max_retries})")
                
        except Exception as e:
            api_elapsed = time.time() - api_start_time
            logger.warning(f"API 호출 실패 ({api_elapsed:.2f}초), 재시도 중... ({attempt + 1}/{max_retries}): {e}")
            logger.debug(f"오류 상세: {type(e).__name__}: {str(e)}")
            
        if attempt < max_retries - 1:
            logger.info(f"{retry_delay}초 대기 후 재시도...")
            time.sleep(retry_delay)
            retry_delay *= 1.5  # 더 느린 증가율
    
    logger.error(f"모든 재시도 실패 ({max_retries}번 시도)")
    return None


if __name__ == "__main__":
    import asyncio
    sys.exit(asyncio.run(main()))