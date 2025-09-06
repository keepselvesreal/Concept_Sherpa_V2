"""
생성 시간: 2025-09-01 15:25:00 KST
핵심 내용: section_extractor_v2.py 로직 기반 콘텐츠 노드 분석 및 추출
상세 내용:
    - import 구문 (25-40): 필요한 라이브러리 import
    - ContentNodeAnalyzer 클래스 (42-350): 콘텐츠 노드 분석 및 파일 추출 로직
        - __init__ (43-70): 초기화 및 config_manager 연동
        - analyze_chapter_toc (72-150): has_content 필드 분석 (content_node_extractor_v3.py 로직)
        - extract_content_nodes_to_files (152-200): section_extractor_v2.py 기반 파일 추출
        - create_full_markdown_from_pdf (202-230): PDF → 전체 마크다운 변환
        - extract_single_section_with_claude (232-280): Claude SDK 섹션 추출
        - extract_sections_with_claude_parallel (282-320): 배치 병렬 처리
        - save_sections_to_files (322-350): 개별 파일 저장
상태: active
참조: section_extractor_v2.py, content_node_extractor_v3.py
"""

import json
import os
import re
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# 프로젝트 내부 모듈
from .config_manager import ConfigManager

class ContentNodeAnalyzer:
    """section_extractor_v2.py 로직 기반 콘텐츠 노드 분석 및 추출"""
    
    def __init__(self, config_path: str = None, logger=None):
        """초기화 및 설정"""
        self.config_manager = ConfigManager(config_path)
        
        # 로깅 설정
        if logger:
            self.logger = logger
        else:
            self.setup_logging()
        
        # Gemini 기반 has_content 분석기 초기화
        self.content_analyzer = self.config_manager.create_content_node_analyzer(self.logger)
        
        # Claude SDK 기반 콘텐츠 추출기 초기화 
        self.content_extractor = self.config_manager.create_content_extractor(self.logger)
        
        log_msg = f"ContentNodeAnalyzer 초기화: {self.content_analyzer.get_name()}"
        print(log_msg)
        self.logger.info(log_msg)
    
    def setup_logging(self, log_file=None):
        """로깅 시스템 설정"""
        if log_file is None:
            log_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "content_analysis.log")
        
        self.logger = logging.getLogger('ContentNodeAnalyzer')
        self.logger.setLevel(logging.DEBUG)
        
        # 기존 핸들러 제거
        self.logger.handlers.clear()
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
        print(f"📝 로그 파일: {log_file}")

    async def analyze_chapter_toc(self, toc_path: str, content_md_path: str) -> Dict[str, Any]:
        """section_extractor_v2.py 로직 기반: 이미 생성된 마크다운에서 has_content 필드 분석"""
        try:
            print("🔍 장별 TOC has_content 분석 시작...")
            self.logger.info(f"=== 장별 TOC has_content 분석 시작 ===")
            self.logger.info(f"TOC 파일: {toc_path}")
            self.logger.info(f"마크다운 파일: {content_md_path}")
            
            # TOC JSON 로드
            print("📖 TOC JSON 파일 읽는 중...")
            with open(toc_path, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            print(f"✅ TOC JSON 로드 완료: {len(toc_data)}개 항목")
            self.logger.info(f"TOC JSON 로드 완료: {len(toc_data)}개 항목")
            
            # 이미 생성된 마크다운 파일 로드
            print("📄 마크다운 파일 읽는 중...")
            with open(content_md_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            print(f"✅ 마크다운 문서 로드 완료: {len(markdown_content)} 문자")
            self.logger.info(f"마크다운 문서 로드 완료: {len(markdown_content)} 문자")
            
            # 최대 레벨 찾기
            max_level = max(item.get('level', 0) for item in toc_data)
            self.logger.info(f"최대 레벨: {max_level}")
            
            # 최대 레벨 항목들 has_content = true 설정
            max_level_count = 0
            for item in toc_data:
                if item.get('level', 0) == max_level:
                    item['has_content'] = True
                    max_level_count += 1
                    self.logger.info(f"✅ [{item['title']}] - 최대 레벨({max_level}) → has_content: true")
            
            self.logger.info(f"최대 레벨 항목 {max_level_count}개 처리 완료")
            
            # 최대 레벨 제외한 항목들 AI 분석
            items_to_analyze = [item for item in toc_data if item.get('level', 0) < max_level]
            self.logger.info(f"AI 분석 대상: {len(items_to_analyze)}개 항목")
            
            for i, item in enumerate(items_to_analyze, 1):
                self.logger.info(f"분석 중 ({i}/{len(items_to_analyze)}): {item['title']} (레벨 {item.get('level', 0)})")
                
                # AI 분석
                has_content = await self.analyze_content_with_ai(item, markdown_content)
                item['has_content'] = has_content
                
                status = "✅" if has_content else "❌"
                self.logger.info(f"{status} [{item['title']}] → has_content: {has_content}")
            
            # content_nodes.json 저장
            output_dir = os.path.dirname(toc_path)
            content_nodes_path = os.path.join(output_dir, "content_nodes.json")
            
            with open(content_nodes_path, 'w', encoding='utf-8') as f:
                json.dump(toc_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✅ 콘텐츠 노드 저장 완료: {content_nodes_path}")
            
            content_count = sum(1 for item in toc_data if item.get('has_content', False))
            self.logger.info(f"🎉 ✅ 장별 TOC 분석 완료: {content_count}개 콘텐츠 노드 발견")
            
            return {
                'success': True,
                'content_nodes_path': content_nodes_path,
                'total_nodes': len(toc_data),
                'content_nodes': content_count
            }
            
        except Exception as e:
            self.logger.error(f"TOC 분석 실패: {str(e)}", exc_info=True)
            return {'success': False, 'error': str(e)}

    async def analyze_content_with_ai(self, item: dict, markdown_content: str) -> bool:
        """AI로 has_content 분석"""
        try:
            prompt = f"""다음은 책의 목차 항목입니다:

제목: {item['title']}
레벨: {item.get('level', 0)}
페이지: {item.get('page', 'N/A')}

이 목차 항목이 실제 내용을 담고 있는 섹션인지 판단해주세요.
단순한 목차나 제목만 있는 경우는 False, 실제 내용이 있는 경우는 True로 판단합니다.

다음 중 하나로만 답변하세요: true 또는 false"""
            
            response = await self.content_analyzer.query(prompt)
            
            # 응답에서 boolean 추출
            response_lower = response.lower().strip()
            if 'true' in response_lower:
                return True
            elif 'false' in response_lower:
                return False
            else:
                # 기본값: true (안전한 선택)
                self.logger.warning(f"AI 응답 해석 실패: {response}, 기본값 true 사용")
                return True
                
        except Exception as e:
            self.logger.error(f"AI 분석 실패: {str(e)}")
            return True  # 실패시 안전한 기본값

    async def extract_content_nodes_to_files(self, content_nodes_path: str, content_md_path: str) -> Dict[str, Any]:
        """section_extractor_v2.py 로직: 이미 생성된 마크다운에서 Claude SDK 기반 콘텐츠 파일 추출"""
        try:
            self.logger.info(f"=== section_extractor_v2.py 로직 기반 콘텐츠 파일 추출 시작 ===")
            self.logger.info(f"Content nodes: {content_nodes_path}")
            self.logger.info(f"마크다운 파일: {content_md_path}")
            
            # content_nodes.json 로드
            with open(content_nodes_path, 'r', encoding='utf-8') as f:
                content_nodes = json.load(f)
            
            # has_content = true인 항목들만 추출
            content_sections = [node for node in content_nodes if node.get('has_content', False)]
            self.logger.info(f"콘텐츠 섹션 추출: {len(content_sections)}개 (전체 {len(content_nodes)}개 중)")
            
            if not content_sections:
                return {'success': False, 'error': 'has_content=true인 섹션이 없음'}
            
            # 이미 생성된 마크다운 파일 로드
            with open(content_md_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            self.logger.info(f"마크다운 문서 로드 완료: {len(markdown_content)} 문자")
            
            # section_extractor_v2.py 스타일 병렬 섹션 추출
            self.logger.info("🔍 Claude SDK 병렬 섹션 추출 시작")
            section_results = await self.extract_sections_with_claude_parallel(content_sections, markdown_content)
            
            if not section_results:
                self.logger.error("섹션 추출 결과가 비어있음")
                return {'success': False, 'error': '섹션 추출 결과가 비어있음'}
            
            self.logger.info(f"섹션 추출 완료: {len(section_results)}개 결과")
            
            # 개별 파일로 저장
            output_dir = os.path.dirname(content_nodes_path)
            self.logger.info(f"파일 저장 시작: {output_dir}")
            saved_files = self.save_sections_to_files(section_results, output_dir)
            
            successful_extractions = len([f for f in saved_files if f.get('success', False)])
            
            self.logger.info(f"🎉 section_extractor_v2.py 로직 콘텐츠 추출 완료: {successful_extractions}/{len(content_sections)}개 성공")
            print(f"🎉 section_extractor_v2.py 로직 콘텐츠 추출 완료: {successful_extractions}/{len(content_sections)}개 성공")
            
            return {
                'success': True,
                'total_nodes': len(content_sections),
                'successful_extractions': successful_extractions,
                'extracted_files': saved_files,
                'output_directory': output_dir
            }
            
        except Exception as e:
            self.logger.error(f"콘텐츠 노드 파일 추출 실패: {str(e)}", exc_info=True)
            return {'success': False, 'error': str(e)}

    async def extract_single_section_with_claude(self, section_title: str, next_section_title: str, markdown_content: str) -> str:
        """section_extractor_v2.py 로직: Claude SDK로 특정 섹션 하나만 추출"""
        next_title_info = f"다음 섹션 제목: {next_section_title}" if next_section_title else "문서 끝까지"
        
        prompt = f"""다음 마크다운 문서에서 특정 섹션의 내용을 추출해주세요.

추출할 섹션: {section_title}
{next_title_info}

마크다운 문서:
```markdown
{markdown_content}
```

작업 지시:
1. '{section_title}' 제목을 문서에서 찾으세요
2. 해당 제목부터 {'다음 섹션(' + next_section_title + ')' if next_section_title else '문서 끝'} 전까지의 모든 내용을 추출하세요
3. 페이지 구분자(--- 페이지 X ---)도 포함해서 추출하세요
4. 섹션 내의 내용을 그대로 유지하세요
5. 제목과 문맥으로 섹션 범위를 판단하세요

중요한 제약사항:
- 어떤 설명이나 부가 정보도 추가하지 마세요
- "문서에서 ... 섹션의 내용을 추출하겠습니다" 같은 설명 금지
- "해당 섹션은..." 같은 부연설명 금지
- 오직 원본 문서의 해당 섹션 내용만 그대로 출력하세요

응답 형식:
섹션 내용을 그대로 복사하여 제공하세요. 어떤 추가 설명이나 마커 없이 원본 텍스트를 정확히 출력하세요.
"""

        try:
            self.logger.info(f"Claude SDK 요청 시작: '{section_title}'")
            response_text = await self.content_extractor.query(prompt)
            self.logger.info(f"Claude SDK 응답 받음: '{section_title}' (길이: {len(response_text)} 문자)")
            
            # 후처리: 섹션 제목 제거 (section_extractor_v2.py 스타일)
            cleaned_content = self.remove_section_title_from_content(response_text.strip(), section_title)
            
            return cleaned_content
            
        except Exception as e:
            error_msg = f"Claude SDK 섹션 '{section_title}' 추출 실패: {e}"
            self.logger.error(error_msg)
            return None

    def remove_section_title_from_content(self, content: str, section_title: str) -> str:
        """추출된 내용에서 불필요한 제목들을 제거 (section_extractor_v2.py 로직)"""
        self.logger.debug(f"후처리 시작: '{section_title}' (내용 길이: {len(content)} 문자)")
        
        lines = content.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 장 제목 제거 (# 1 Complexity of object- oriented programming 등)
            if line_stripped.startswith('# ') and ('Complexity of object' in line_stripped or 'oriented programming' in line_stripped):
                self.logger.info(f"장 제목 제거: '{line_stripped}'")
                continue
            
            # 섹션 제목 중복 제거 (현재 섹션 제목과 일치하는 경우)
            title_without_hash = section_title.lstrip('#').strip()
            line_without_hash = line_stripped.lstrip('#').strip()
            
            if line_without_hash == title_without_hash and line_stripped.startswith('#'):
                self.logger.info(f"섹션 제목 중복 제거: '{line_stripped}'")
                continue
            
            result_lines.append(line)
        
        result = '\n'.join(result_lines).strip()
        self.logger.debug(f"후처리 완료: '{section_title}' (결과 길이: {len(result)} 문자)")
        
        return result

    async def extract_sections_with_claude_parallel(self, content_sections: list, markdown_content: str):
        """section_extractor_v2.py 로직: Claude SDK로 섹션별 개별 요청, 병렬 처리"""
        self.logger.info(f"🔍 Claude SDK로 {len(content_sections)}개 섹션 개별 추출 시작")
        print(f"\n🔍 Claude SDK로 {len(content_sections)}개 섹션 개별 추출 시작")
        
        # 다음 섹션 제목 정보 준비
        section_pairs = []
        for i, section in enumerate(content_sections):
            next_section = content_sections[i + 1] if i + 1 < len(content_sections) else None
            next_title = next_section['title'] if next_section else None
            section_pairs.append((section, next_title))
            self.logger.debug(f"섹션 페어 준비: {section['title']} → {next_title}")
        
        # 배치 크기 설정 (section_extractor_v2.py와 동일)
        batch_size = 4
        batches = [section_pairs[i:i + batch_size] for i in range(0, len(section_pairs), batch_size)]
        self.logger.info(f"총 {len(batches)}개 배치로 분할 (배치 크기: {batch_size})")
        
        all_results = []
        for batch_idx, batch in enumerate(batches):
            self.logger.info(f"📦 배치 {batch_idx + 1}/{len(batches)} 처리 중 ({len(batch)}개 섹션)...")
            print(f"\n📦 배치 {batch_idx + 1}/{len(batches)} 처리 중 ({len(batch)}개 섹션)...")
            
            # 배치 내 병렬 처리
            tasks = []
            sections_in_batch = []
            for section, next_title in batch:
                self.logger.debug(f"배치 {batch_idx + 1} 태스크 생성: {section['title']}")
                task = self.extract_single_section_with_claude(section['title'], next_title, markdown_content)
                tasks.append(task)
                sections_in_batch.append(section)
            
            # 병렬 실행
            try:
                self.logger.info(f"배치 {batch_idx + 1} 병렬 실행 시작 ({len(tasks)}개 태스크)")
                results = await asyncio.gather(*tasks, return_exceptions=True)
                self.logger.info(f"배치 {batch_idx + 1} 병렬 실행 완료")
                
                batch_results = []
                for section, result in zip(sections_in_batch, results):
                    if isinstance(result, Exception):
                        error_msg = f"❌ '{section['title']}' 추출 실패: {result}"
                        print(error_msg)
                        self.logger.error(error_msg)
                        batch_results.append((section, None))
                    else:
                        success_msg = f"✅ '{section['title']}' 추출 완료 (길이: {len(result) if result else 0})"
                        print(success_msg)
                        self.logger.info(success_msg)
                        batch_results.append((section, result))
                        
            except Exception as e:
                error_msg = f"❌ 배치 {batch_idx + 1} 처리 실패: {e}"
                print(error_msg)
                self.logger.error(error_msg, exc_info=True)
                batch_results = [(section, None) for section in sections_in_batch]
            
            all_results.extend(batch_results)
            self.logger.info(f"배치 {batch_idx + 1} 처리 완료. 누적 결과: {len(all_results)}개")
        
        self.logger.info(f"🎉 전체 추출 완료: {len(all_results)}개 섹션")
        print(f"🎉 전체 추출 완료: {len(all_results)}개 섹션")
        return all_results

    def save_sections_to_files(self, section_results: list, output_dir: str) -> list:
        """섹션별 추출 결과를 개별 .md 파일로 저장 (section_extractor_v2.py 로직)"""
        self.logger.info(f"📁 파일 저장 시작: {len(section_results)}개 섹션 → {output_dir}")
        print(f"\n📁 파일 저장 시작: {len(section_results)}개 섹션 → {output_dir}")
        
        if not section_results:
            self.logger.warning("저장할 섹션 결과가 없음")
            return []
        
        # 출력 디렉토리 생성
        try:
            os.makedirs(output_dir, exist_ok=True)
            self.logger.info(f"출력 디렉토리 생성/확인 완료: {output_dir}")
        except Exception as e:
            self.logger.error(f"출력 디렉토리 생성 실패: {e}")
            raise
        
        saved_files = []
        
        for idx, (section, content) in enumerate(section_results, 1):
            self.logger.info(f"파일 저장 처리 중 ({idx}/{len(section_results)}): {section['title']}")
            
            if content is None:
                error_msg = f"⚠️ 섹션 '{section['title']}' 내용이 없어 건너뜀"
                print(error_msg)
                self.logger.warning(error_msg)
                saved_files.append({
                    'node_id': section.get('id'),
                    'title': section['title'],
                    'success': False,
                    'error': '내용이 없음'
                })
                continue
            
            # 파일명 생성 (section_extractor_v2.py와 동일한 정규화 로직)
            section_title = section['title']
            title_clean = re.sub(r'[^\w\s.-]', '', section_title)  # 점(.)도 유지
            title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
            filename = f"{title_clean}.md"
            filepath = os.path.join(output_dir, filename)
            
            self.logger.debug(f"파일명 생성: '{section_title}' → '{filename}'")
            self.logger.debug(f"저장 경로: {filepath}")
            self.logger.debug(f"내용 길이: {len(content)} 문자")
            
            # 파일 저장
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success_msg = f"✅ 섹션 저장: {filename} ({len(content)} 문자)"
                print(success_msg)
                self.logger.info(success_msg)
                
                saved_files.append({
                    'node_id': section.get('id'),
                    'title': section['title'],
                    'level': section.get('level', 0),
                    'content_file': filepath,
                    'success': True,
                    'content_length': len(content)
                })
                
            except Exception as e:
                error_msg = f"❌ 섹션 '{section_title}' 저장 실패: {e}"
                print(error_msg)
                self.logger.error(error_msg, exc_info=True)
                saved_files.append({
                    'node_id': section.get('id'),
                    'title': section_title,
                    'success': False,
                    'error': f'저장 실패: {e}'
                })
        
        success_count = len([f for f in saved_files if f.get('success', False)])
        self.logger.info(f"📁 파일 저장 완료: {success_count}/{len(section_results)}개 성공")
        print(f"📁 파일 저장 완료: {success_count}/{len(section_results)}개 성공")
        
        return saved_files