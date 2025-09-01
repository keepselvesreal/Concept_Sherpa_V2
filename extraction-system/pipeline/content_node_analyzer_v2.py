# 생성 시간: Mon Sep  1 17:49:15 KST 2025
# 핵심 내용: 실시간 모니터링 강화된 콘텐츠 노드 분석 및 추출
# 상세 내용:
#   - ContentNodeAnalyzer (line 30-450): 실시간 모니터링 강화 클래스
#     - log_and_print (line 45-55): 로그+stdout 동시 실시간 출력
#     - extract_sections_with_enhanced_monitoring (line 320-400): 실시간 진행률 추적
#     - extract_single_section_with_monitoring (line 250-290): Claude API 상세 모니터링
# 상태: active
# 참조: content_node_analyzer.py에서 실시간 모니터링 기능 강화

import json
import os
import re
import asyncio
import logging
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import fitz  # PyMuPDF

# 프로젝트 내부 모듈
from config_manager import ConfigManager

class ContentNodeAnalyzer:
    """실시간 모니터링 강화된 콘텐츠 노드 분석 및 추출"""
    
    def __init__(self, config_path: str = None, logger=None):
        """초기화 및 설정"""
        self.config_manager = ConfigManager(config_path)
        
        # 로깅 설정
        if logger:
            self.logger = logger
        else:
            self.setup_logging()
        
        # Gemini 기반 has_content 분석기 초기화 (기존 방식)
        self.content_analyzer = self.config_manager.create_content_node_analyzer(self.logger)
        
        # Claude SDK 기반 콘텐츠 추출기 초기화 
        self.content_extractor = self.config_manager.create_content_extractor(self.logger)
        
        log_msg = f"ContentNodeAnalyzer 초기화: {self.content_analyzer.get_name()}"
        self.log_and_print('info', log_msg)
    
    def log_and_print(self, level: str, message: str):
        """로그 파일 + stdout 동시 실시간 출력"""
        # 로거에 기록
        getattr(self.logger, level.lower())(message)
        
        # 실시간 출력 (즉시 플러시)
        timestamp = datetime.now().strftime('%H:%M:%S')
        level_symbol = {'info': '📋', 'debug': '🔍', 'warning': '⚠️', 'error': '❌'}.get(level, '📋')
        print(f"[{timestamp}] {level_symbol} {message}")
        sys.stdout.flush()

    def setup_logging(self):
        """로깅 설정"""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    async def analyze_chapter_toc(self, toc_path: str, content_md_path: str) -> Dict[str, Any]:
        """장 TOC 분석 및 has_content 필드 업데이트"""
        self.log_and_print('info', f"📖 장 TOC 분석 시작: {os.path.basename(toc_path)}")
        
        try:
            # 이미 생성된 마크다운 파일 로드 (section_extractor_v2.py 패턴)
            if not os.path.exists(content_md_path):
                raise FileNotFoundError(f"장 내용 파일 없음: {content_md_path}")
                
            with open(content_md_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            self.log_and_print('info', f"📄 마크다운 내용 로드: {len(markdown_content)} 문자")
            
            # TOC 파일 로드
            with open(toc_path, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            
            # TOC 데이터 형식 확인 및 처리
            if isinstance(toc_data, dict) and 'toc_structure' in toc_data:
                toc_structure = toc_data['toc_structure']
            elif isinstance(toc_data, list):
                toc_structure = toc_data
                self.log_and_print('info', f"🔧 TOC 파일이 리스트 형태로 감지됨")
            else:
                raise ValueError(f"예상하지 못한 TOC 파일 형식: {toc_path}")
            self.log_and_print('info', f"🔍 TOC 구조 로드: {len(toc_structure)}개 노드")
            
            # has_content 분석 시작 (AI 기반 판단)
            self.log_and_print('info', f"🤖 AI 기반 has_content 분석 시작...")
            
            # 모든 노드에 대해 AI 기반 has_content 판단 수행
            updated_toc = await self.analyze_all_nodes_with_ai(toc_structure, markdown_content)
            
            content_count = len([item for item in updated_toc if item.get('has_content') == True])
            self.log_and_print('info', f"✅ AI 기반 has_content 분석 완료: {content_count}개 콘텐츠 노드")
            
            # has_content=true인 노드만 필터링
            content_sections = [node for node in updated_toc if node.get('has_content', False)]
            self.log_and_print('info', f"📊 콘텐츠 섹션 필터링: {len(content_sections)}/{len(updated_toc)}개")
            
            # TOC 파일 업데이트 저장
            if isinstance(toc_data, dict):
                toc_data['toc_structure'] = updated_toc
                save_data = toc_data
            else:
                # 리스트 형태면 그대로 저장
                save_data = updated_toc
            
            with open(toc_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            self.log_and_print('info', f"💾 TOC 파일 업데이트 완료: {len(content_sections)}개 콘텐츠 섹션")
            
            # 콘텐츠 노드 파일을 각 장 폴더에 직접 저장
            toc_dir = os.path.dirname(toc_path)
            content_output_dir = toc_dir  # 각 장 폴더에 직접 저장
            
            # 콘텐츠 노드 파일들을 바로 생성 (section_extractor_v2.py 로직 적용)
            if content_sections:
                self.log_and_print('info', f"🚀 콘텐츠 노드 파일 생성 시작: {len(content_sections)}개 섹션")
                # 콘텐츠 노드 추출 및 파일 저장 수행
                section_results = await self.extract_sections_with_enhanced_monitoring(content_sections, markdown_content)
                saved_files = self.save_sections_to_files(section_results, content_output_dir)
                
                extraction_result = {
                    'success': len(saved_files) > 0,
                    'extracted_files': saved_files,
                    'total_sections': len(content_sections),
                    'success_count': len([f for f in saved_files if f.get('success', False)])
                }
                
                if extraction_result.get('success', False):
                    self.log_and_print('info', f"✅ 콘텐츠 노드 파일 생성 완료")
                    return {
                        'success': True,
                        'content_sections': content_sections,
                        'markdown_content': markdown_content,
                        'total_sections': len(updated_toc),
                        'content_sections_count': len(content_sections),
                        'content_nodes_path': content_output_dir,
                        'extracted_files': extraction_result.get('extracted_files', [])
                    }
                else:
                    error_msg = f"콘텐츠 노드 파일 생성 실패: {extraction_result.get('error', '알 수 없는 오류')}"
                    self.log_and_print('error', error_msg)
                    return {
                        'success': False,
                        'error': error_msg
                    }
            else:
                self.log_and_print('warning', f"⚠️ 생성할 콘텐츠 섹션이 없음")
                return {
                    'success': True,
                    'content_sections': content_sections,
                    'markdown_content': markdown_content,
                    'total_sections': len(updated_toc),
                    'content_sections_count': len(content_sections),
                    'content_nodes_path': content_output_dir,
                    'extracted_files': []
                }
            
        except Exception as e:
            error_msg = f"TOC 분석 실패: {str(e)}"
            self.log_and_print('error', error_msg)
            return {
                'success': False,
                'error': error_msg,
                'content_sections': [],
                'markdown_content': '',
                'total_sections': 0,
                'content_sections_count': 0
            }

    async def analyze_all_nodes_with_ai(self, toc_structure: List[Dict], markdown_content: str) -> List[Dict]:
        """모든 노드에 대해 AI 기반 has_content 판단"""
        self.log_and_print('info', f"🔍 {len(toc_structure)}개 노드 AI 분석 시작...")
        
        for i, current_item in enumerate(toc_structure):
            # 다음 항목 찾기
            next_item = toc_structure[i + 1] if i + 1 < len(toc_structure) else None
            
            try:
                # AI 기반 has_content 판단
                has_content = await self.analyze_content_with_ai(current_item, next_item, markdown_content)
                current_item['has_content'] = has_content
                
                status = "✅" if has_content else "❌"
                self.log_and_print('debug', f"{status} [{current_item['title']}] → has_content: {has_content}")
                
            except Exception as e:
                self.log_and_print('warning', f"⚠️ AI 분석 실패 [{current_item['title']}]: {str(e)}")
                # 실패시 기본값 설정
                if not current_item.get('children_ids') or len(current_item.get('children_ids', [])) == 0:
                    current_item['has_content'] = True  # 리프 노드 기본값
                else:
                    current_item['has_content'] = False  # 부모 노드 기본값
        
        return toc_structure

    async def analyze_content_with_ai(self, current_item: Dict, next_item: Optional[Dict], markdown_content: str) -> bool:
        """AI를 통한 콘텐츠 존재 여부 분석 (content_node_extractor_v2.py 로직)"""
        current_title = current_item.get('title', '')
        next_title = next_item.get('title', '') if next_item else '문서 끝'
        
        prompt = f"""다음 마크다운 문서에서 '{current_title}' 제목과 '{next_title}' 제목 사이에 실제 텍스트 내용이 있는지 분석해주세요.

현재 항목: {current_title}
다음 항목: {next_title}

마크다운 문서:
```markdown
{markdown_content}
```

작업:
1. '{current_title}' 제목을 찾으세요
2. '{next_title}' 제목을 찾으세요  
3. 두 제목 사이에 의미있는 텍스트 내용이 있는지 확인하세요
4. 단순한 페이지 구분자(--- 페이지 X ---)나 챕터 헤더는 제외하고 판단하세요

판단 기준:
- 30자 이상의 의미있는 텍스트가 있으면 true
- 단순 제목이나 페이지 번호만 있으면 false
- NOTE, 설명문, 대화문 등이 있으면 true

응답 형식 (JSON만):
{{
    "has_content": true/false
}}"""

        try:
            response_text = await self.content_analyzer.query(prompt)
            
            # JSON 파싱 시도
            if '```json' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text
            else:
                json_text = response_text
            
            result = json.loads(json_text)
            return result.get('has_content', False)
            
        except json.JSONDecodeError as e:
            self.log_and_print('warning', f"AI 응답 JSON 파싱 실패: {e}")
            # 파싱 실패시 응답 텍스트에서 true/false 찾기
            if 'true' in response_text.lower():
                return True
            elif 'false' in response_text.lower():
                return False
            else:
                # 최종 안전장치: 리프노드면 True, 부모노드면 False
                return not bool(current_item.get('children_ids'))
                
        except Exception as e:
            self.log_and_print('error', f"AI 분석 오류: {str(e)}")
            # 오류시 안전장치
            return not bool(current_item.get('children_ids'))

    async def extract_content_nodes_to_files(self, chapter_folder: str, toc_file: str, content_md_file: str) -> Dict[str, Any]:
        """콘텐츠 노드를 개별 파일로 추출 (section_extractor_v2.py 로직)"""
        self.log_and_print('info', f"🚀 콘텐츠 노드 파일 추출 시작: {os.path.basename(chapter_folder)}")
        
        try:
            # 1. has_content 분석
            analysis_result = await self.analyze_chapter_toc(toc_file, content_md_file)
            if not analysis_result['success']:
                return analysis_result
            
            content_sections = analysis_result['content_sections']
            markdown_content = analysis_result['markdown_content']
            
            if not content_sections:
                self.log_and_print('warning', f"⚠️ 콘텐츠 섹션 없음: {chapter_folder}")
                return {'success': True, 'extracted_files': [], 'message': '콘텐츠 섹션 없음'}
            
            # 2. Claude SDK로 섹션별 콘텐츠 추출 (실시간 모니터링)
            section_results = await self.extract_sections_with_enhanced_monitoring(content_sections, markdown_content)
            
            # 3. 개별 파일로 저장
            saved_files = self.save_sections_to_files(section_results, chapter_folder)
            
            success_count = len([f for f in saved_files if f.get('success', False)])
            self.log_and_print('info', f"🎉 section_extractor_v2.py 로직 콘텐츠 추출 완료: {success_count}/{len(content_sections)}개 성공")
            
            return {
                'success': True,
                'extracted_files': saved_files,
                'total_sections': len(content_sections),
                'success_count': success_count
            }
            
        except Exception as e:
            error_msg = f"콘텐츠 노드 추출 실패: {str(e)}"
            self.log_and_print('error', error_msg)
            return {
                'success': False,
                'error': error_msg,
                'extracted_files': [],
                'total_sections': 0,
                'success_count': 0
            }

    async def extract_single_section_with_monitoring(self, section_title: str, next_title: Optional[str], markdown_content: str) -> Optional[str]:
        """Claude API 호출 상태 상세 모니터링"""
        api_start = time.time()
        
        try:
            self.log_and_print('debug', f"    🌐 Claude API 호출: '{section_title}'")
            
            # API 요청
            result = await self.content_extractor.extract_content_with_ai(
                section_title, next_title, markdown_content
            )
            
            api_elapsed = time.time() - api_start
            if result:
                # 후처리 (불필요한 제목 제거)
                cleaned_result = self.remove_section_title_from_content(result, section_title)
                self.log_and_print('debug', f"    📡 API 응답 성공: {len(cleaned_result)} 문자 ({api_elapsed:.2f}초)")
                return cleaned_result
            else:
                self.log_and_print('warning', f"    📡 API 응답 빈 결과 ({api_elapsed:.2f}초)")
                return None
                
        except Exception as e:
            api_elapsed = time.time() - api_start
            self.log_and_print('error', f"    📡 API 호출 실패: {str(e)} ({api_elapsed:.2f}초)")
            return None

    def remove_section_title_from_content(self, content: str, section_title: str) -> str:
        """추출된 내용에서 불필요한 제목들을 제거 (section_extractor_v2.py 로직)"""
        self.log_and_print('debug', f"후처리 시작: '{section_title}' (내용 길이: {len(content)} 문자)")
        
        lines = content.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 장 제목 제거 (# 1 Complexity of object- oriented programming 등)
            if line_stripped.startswith('# ') and ('Complexity of object' in line_stripped or 'oriented programming' in line_stripped):
                self.log_and_print('debug', f"장 제목 제거: '{line_stripped}'")
                continue
            
            # 섹션 제목 중복 제거 (현재 섹션 제목과 일치하는 경우)
            title_without_hash = section_title.lstrip('#').strip()
            line_without_hash = line_stripped.lstrip('#').strip()
            
            if line_without_hash == title_without_hash and line_stripped.startswith('#'):
                self.log_and_print('debug', f"섹션 제목 중복 제거: '{line_stripped}'")
                continue
            
            result_lines.append(line)
        
        result = '\n'.join(result_lines).strip()
        self.log_and_print('debug', f"후처리 완료: '{section_title}' (결과 길이: {len(result)} 문자)")
        
        return result

    async def extract_sections_with_enhanced_monitoring(self, content_sections: list, markdown_content: str):
        """실시간 모니터링 강화된 섹션 추출"""
        total_sections = len(content_sections)
        self.log_and_print('info', f"🔍 Claude SDK로 {total_sections}개 섹션 개별 추출 시작")
        
        # 진행률 추적
        progress_tracker = {
            'total': total_sections,
            'completed': 0,
            'failed': 0,
            'current_batch': 0,
            'start_time': time.time()
        }
        
        # 다음 섹션 제목 정보 준비
        section_pairs = []
        for i, section in enumerate(content_sections):
            next_section = content_sections[i + 1] if i + 1 < len(content_sections) else None
            next_title = next_section['title'] if next_section else None
            section_pairs.append((section, next_title))
            self.log_and_print('debug', f"섹션 페어 준비: {section['title']} → {next_title}")
        
        # 배치 크기 설정 (section_extractor_v2.py와 동일)
        batch_size = 4
        batches = [section_pairs[i:i + batch_size] for i in range(0, len(section_pairs), batch_size)]
        self.log_and_print('info', f"총 {len(batches)}개 배치로 분할 (배치 크기: {batch_size})")
        
        all_results = []
        for batch_idx, batch in enumerate(batches):
            progress_tracker['current_batch'] = batch_idx + 1
            self.log_and_print('info', f"📦 배치 {batch_idx + 1}/{len(batches)} 처리 중 ({len(batch)}개 섹션)...")
            
            # 배치 내 병렬 처리
            tasks = []
            sections_in_batch = []
            for section, next_title in batch:
                self.log_and_print('debug', f"배치 {batch_idx + 1} 태스크 생성: {section['title']}")
                task = self.extract_single_section_with_monitoring(section['title'], next_title, markdown_content)
                tasks.append(task)
                sections_in_batch.append(section)
            
            # 병렬 실행
            try:
                self.log_and_print('info', f"  🔄 배치 {batch_idx + 1} 병렬 실행 시작 ({len(tasks)}개 태스크)")
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                batch_results = []
                for section, result in zip(sections_in_batch, results):
                    if isinstance(result, Exception):
                        progress_tracker['failed'] += 1
                        error_msg = f"  ❌ [{progress_tracker['completed']+progress_tracker['failed']}/{total_sections}] '{section['title']}' 추출 실패: {result}"
                        self.log_and_print('error', error_msg)
                        batch_results.append((section, None))
                    else:
                        progress_tracker['completed'] += 1
                        success_msg = f"  ✅ [{progress_tracker['completed']}/{total_sections}] '{section['title']}' 추출 완료 (길이: {len(result) if result else 0})"
                        self.log_and_print('info', success_msg)
                        batch_results.append((section, result))
                        
            except Exception as e:
                error_msg = f"❌ 배치 {batch_idx + 1} 처리 실패: {e}"
                self.log_and_print('error', error_msg)
                batch_results = [(section, None) for section in sections_in_batch]
                progress_tracker['failed'] += len(sections_in_batch)
            
            all_results.extend(batch_results)
            
            # 배치 완료 상태
            total_elapsed = time.time() - progress_tracker['start_time']
            self.log_and_print('info', f"📊 진행률: {progress_tracker['completed']}/{total_sections} 성공, {progress_tracker['failed']}/{total_sections} 실패 ({progress_tracker['completed']/total_sections*100:.1f}%)")
        
        self.log_and_print('info', f"🎉 전체 추출 완료: {len(all_results)}개 섹션")
        return all_results

    def save_sections_to_files(self, section_results: list, output_dir: str) -> list:
        """섹션별 추출 결과를 개별 .md 파일로 저장 (section_extractor_v2.py 로직)"""
        self.log_and_print('info', f"📁 파일 저장 시작: {len(section_results)}개 섹션 → {output_dir}")
        
        saved_files = []
        success_count = 0
        
        for section, content in section_results:
            if not content:
                self.log_and_print('warning', f"⚠️ 빈 콘텐츠로 저장 건너뜀: {section['title']}")
                saved_files.append({
                    'section_title': section['title'],
                    'filename': '',
                    'success': False,
                    'error': '콘텐츠 없음'
                })
                continue
            
            try:
                # 파일명 생성 (특수문자 제거)
                safe_title = re.sub(r'[^\w\s.-]', '', section['title'])
                safe_title = re.sub(r'[-\s]+', '_', safe_title).strip('_')
                filename = f"{safe_title}.md"
                filepath = os.path.join(output_dir, filename)
                
                # 파일 저장
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success_count += 1
                self.log_and_print('info', f"✅ 섹션 저장: {filename} ({len(content)} 문자)")
                saved_files.append({
                    'section_title': section['title'],
                    'filename': filename,
                    'filepath': filepath,
                    'content_length': len(content),
                    'success': True
                })
                
            except Exception as e:
                error_msg = f"❌ 파일 저장 실패 ({section['title']}): {e}"
                self.log_and_print('error', error_msg)
                saved_files.append({
                    'section_title': section['title'],
                    'filename': '',
                    'success': False,
                    'error': str(e)
                })
        
        self.log_and_print('info', f"📁 파일 저장 완료: {success_count}/{len(section_results)}개 성공")
        return saved_files