#!/usr/bin/env python3
import re
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

class UniversalSectionSplitter:
    """
    모든 챕터에서 재사용 가능한 범용 섹션 분할 시스템
    각 챕터를 체계적으로 섹션별로 분할하여 재귀적 분석에 최적화된 구조 생성
    """
    
    def __init__(self, chapter_path: str, output_base_dir: str = None):
        self.chapter_path = Path(chapter_path)
        self.output_base_dir = Path(output_base_dir) if output_base_dir else self.chapter_path.parent / "content"
        self.sections = {}
        self.metadata = {}
        self.original_text = ""
        
        # 섹션 패턴 정의 (다양한 챕터 구조에 대응)
        self.patterns = {
            # 주섹션 패턴: "1.1 Title", "2.1 Title" 등
            'main_section': r'^(\d+\.\d+)\s+(.+?)$',
            # 하위섹션 패턴: "1.1.1 Title", "2.1.1 Title" 등  
            'sub_section': r'^(\d+\.\d+\.\d+)\s+(.+?)$',
            # 페이지 마커: "=== PAGE 31 ==="
            'page_marker': r'^=== PAGE (\d+) ===$',
            # 챕터 제목 패턴
            'chapter_title': r'^# Chapter (\d+): (.+)$',
            # "This chapter covers" 패턴
            'chapter_covers': r'This chapter covers',
            # Summary 패턴
            'summary': r'^Summary\s*$'
        }
    
    def load_chapter_text(self) -> str:
        """챕터 텍스트 로드"""
        if not self.chapter_path.exists():
            raise FileNotFoundError(f"Chapter file not found: {self.chapter_path}")
        
        with open(self.chapter_path, 'r', encoding='utf-8') as f:
            self.original_text = f.read()
        
        return self.original_text
    
    def detect_section_patterns(self, text: str) -> Dict[str, List[Tuple]]:
        """텍스트에서 모든 섹션 패턴 감지"""
        patterns_found = {
            'main_sections': [],
            'sub_sections': [],
            'page_markers': [],
            'chapter_info': {},
            'special_sections': []
        }
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 챕터 정보 추출
            chapter_match = re.match(self.patterns['chapter_title'], line)
            if chapter_match:
                patterns_found['chapter_info'] = {
                    'number': chapter_match.group(1),
                    'title': chapter_match.group(2),
                    'line_num': i
                }
            
            # 주섹션 감지
            main_match = re.match(self.patterns['main_section'], line)
            if main_match:
                patterns_found['main_sections'].append({
                    'number': main_match.group(1),
                    'title': main_match.group(2),
                    'line_num': i,
                    'full_line': line
                })
            
            # 하위섹션 감지
            sub_match = re.match(self.patterns['sub_section'], line)
            if sub_match:
                patterns_found['sub_sections'].append({
                    'number': sub_match.group(1),
                    'title': sub_match.group(2),
                    'line_num': i,
                    'full_line': line
                })
            
            # 페이지 마커 감지
            page_match = re.match(self.patterns['page_marker'], line)
            if page_match:
                patterns_found['page_markers'].append({
                    'page_num': int(page_match.group(1)),
                    'line_num': i
                })
            
            # Summary 감지
            if re.match(self.patterns['summary'], line):
                patterns_found['special_sections'].append({
                    'type': 'summary',
                    'title': 'Summary',
                    'line_num': i,
                    'full_line': line
                })
        
        return patterns_found
    
    def extract_sections_with_hierarchy(self, text: str) -> Dict[str, Any]:
        """계층적 구조로 섹션 추출"""
        patterns = self.detect_section_patterns(text)
        lines = text.split('\n')
        sections = {}
        
        # 모든 섹션을 하나의 리스트로 통합 (순서 유지)
        all_sections = []
        
        # 챕터 도입부 처리
        chapter_intro_end = 0
        if patterns['main_sections']:
            chapter_intro_end = patterns['main_sections'][0]['line_num']
        elif patterns['sub_sections']:
            chapter_intro_end = patterns['sub_sections'][0]['line_num']
        
        if chapter_intro_end > 0:
            all_sections.append({
                'id': 'chapter_intro',
                'type': 'intro',
                'title': 'Chapter Introduction',
                'start_line': 0,
                'end_line': chapter_intro_end,
                'level': 0
            })
        
        # 주섹션들 추가
        for main_sec in patterns['main_sections']:
            all_sections.append({
                'id': f"section_{main_sec['number'].replace('.', '_')}",
                'type': 'main_section',
                'number': main_sec['number'],
                'title': main_sec['title'],
                'start_line': main_sec['line_num'],
                'level': 1
            })
        
        # 하위섹션들 추가
        for sub_sec in patterns['sub_sections']:
            all_sections.append({
                'id': f"section_{sub_sec['number'].replace('.', '_')}",
                'type': 'sub_section', 
                'number': sub_sec['number'],
                'title': sub_sec['title'],
                'start_line': sub_sec['line_num'],
                'level': 2
            })
        
        # 특수 섹션들 추가 (Summary 등)
        for special in patterns['special_sections']:
            all_sections.append({
                'id': special['type'],
                'type': 'special',
                'title': special['title'],
                'start_line': special['line_num'],
                'level': 1
            })
        
        # 섹션들을 시작 라인 기준으로 정렬
        all_sections.sort(key=lambda x: x['start_line'])
        
        # 각 섹션의 끝 라인 계산
        for i, section in enumerate(all_sections):
            if i + 1 < len(all_sections):
                section['end_line'] = all_sections[i + 1]['start_line']
            else:
                section['end_line'] = len(lines)
        
        # 섹션 내용 추출
        for section in all_sections:
            start = section['start_line']
            end = section['end_line']
            section['content'] = '\n'.join(lines[start:end]).strip()
            section['page_range'] = self._extract_page_range(section['content'])
            
            sections[section['id']] = section
        
        # 도입부 섹션들 식별 및 생성
        sections.update(self._extract_section_intros(sections, lines))
        
        return sections
    
    def _extract_section_intros(self, sections: Dict, lines: List[str]) -> Dict[str, Any]:
        """주섹션들의 도입부 추출"""
        intro_sections = {}
        
        # 주섹션들 찾기
        main_sections = [s for s in sections.values() if s['type'] == 'main_section']
        
        for main_section in main_sections:
            section_number = main_section['number']
            
            # 이 주섹션에 속하는 첫 번째 하위섹션 찾기
            first_subsection = None
            for section in sections.values():
                if (section['type'] == 'sub_section' and 
                    section['number'].startswith(section_number + '.')):
                    if first_subsection is None or section['start_line'] < first_subsection['start_line']:
                        first_subsection = section
            
            # 도입부가 존재하는지 확인
            if first_subsection and first_subsection['start_line'] > main_section['start_line']:
                intro_id = f"section_{section_number.replace('.', '_')}_intro"
                intro_sections[intro_id] = {
                    'id': intro_id,
                    'type': 'section_intro',
                    'parent_section': section_number,
                    'title': f"Section {section_number} Introduction",
                    'start_line': main_section['start_line'],
                    'end_line': first_subsection['start_line'],
                    'content': '\n'.join(lines[main_section['start_line']:first_subsection['start_line']]).strip(),
                    'level': 1.5,
                    'page_range': self._extract_page_range('\n'.join(lines[main_section['start_line']:first_subsection['start_line']]))
                }
        
        return intro_sections
    
    def _extract_page_range(self, content: str) -> str:
        """내용에서 페이지 범위 추출"""
        page_numbers = []
        for match in re.finditer(self.patterns['page_marker'], content, re.MULTILINE):
            page_numbers.append(int(match.group(1)))
        
        if page_numbers:
            return f"{min(page_numbers)}-{max(page_numbers)}"
        return ""
    
    def create_section_files(self, sections: Dict[str, Any], output_dir: Path) -> None:
        """섹션별 파일 생성"""
        sections_dir = output_dir / "sections"
        sections_dir.mkdir(parents=True, exist_ok=True)
        
        for section_id, section in sections.items():
            filename = f"{section_id}.md"
            file_path = sections_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # 헤더 정보
                f.write(f"# {section['title']}\n\n")
                
                if section.get('number'):
                    f.write(f"**섹션 번호:** {section['number']}\n")
                if section.get('page_range'):
                    f.write(f"**페이지 범위:** {section['page_range']}\n")
                
                f.write(f"**섹션 유형:** {section['type']}\n\n")
                
                # 내용
                f.write(section['content'])
        
        print(f"✓ {len(sections)}개 섹션 파일 생성 완료: {sections_dir}")
    
    def generate_metadata(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """섹션 메타데이터 생성"""
        metadata = {
            'extraction_timestamp': datetime.now().isoformat(),
            'source_file': str(self.chapter_path),
            'total_sections': len(sections),
            'section_types': {},
            'hierarchy': {},
            'sections': {}
        }
        
        # 섹션 유형별 통계
        for section in sections.values():
            section_type = section['type']
            if section_type not in metadata['section_types']:
                metadata['section_types'][section_type] = 0
            metadata['section_types'][section_type] += 1
        
        # 계층 구조 분석
        main_sections = [s for s in sections.values() if s['type'] == 'main_section']
        for main_sec in main_sections:
            section_number = main_sec['number']
            sub_sections = [s for s in sections.values() 
                          if s['type'] == 'sub_section' and s['number'].startswith(section_number + '.')]
            
            metadata['hierarchy'][section_number] = {
                'title': main_sec['title'],
                'subsections': [s['number'] for s in sub_sections],
                'has_intro': any(s['type'] == 'section_intro' and s.get('parent_section') == section_number 
                               for s in sections.values())
            }
        
        # 각 섹션 상세 정보
        for section_id, section in sections.items():
            metadata['sections'][section_id] = {
                'title': section['title'],
                'type': section['type'],
                'page_range': section.get('page_range', ''),
                'content_length': len(section['content']),
                'level': section.get('level', 0)
            }
            if section.get('number'):
                metadata['sections'][section_id]['number'] = section['number']
        
        return metadata
    
    def validate_split_completeness(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """분할 결과의 완전성 검증"""
        validation_result = {
            'is_complete': True,
            'issues': [],
            'statistics': {
                'original_length': len(self.original_text),
                'sections_total_length': sum(len(s['content']) for s in sections.values()),
                'coverage_percentage': 0
            }
        }
        
        # 길이 비교 (정확히 일치하지 않을 수 있음 - 중복/공백 처리로 인해)
        total_section_length = validation_result['statistics']['sections_total_length']
        original_length = validation_result['statistics']['original_length']
        
        if total_section_length > 0:
            coverage = (total_section_length / original_length) * 100
            validation_result['statistics']['coverage_percentage'] = round(coverage, 2)
        
        # 기본 검증 규칙
        if not any(s['type'] == 'intro' for s in sections.values()):
            validation_result['issues'].append("챕터 도입부가 감지되지 않았습니다.")
        
        if not any(s['type'] == 'main_section' for s in sections.values()):
            validation_result['issues'].append("주섹션이 감지되지 않았습니다.")
        
        if validation_result['statistics']['coverage_percentage'] < 80:
            validation_result['issues'].append(f"내용 커버리지가 낮습니다: {validation_result['statistics']['coverage_percentage']:.1f}%")
        
        validation_result['is_complete'] = len(validation_result['issues']) == 0
        
        return validation_result
    
    def split_chapter(self) -> Dict[str, Any]:
        """단일 챕터 분할 수행"""
        print(f"📚 챕터 분할 시작: {self.chapter_path}")
        
        # 1. 텍스트 로드
        text = self.load_chapter_text()
        
        # 2. 섹션 추출
        sections = self.extract_sections_with_hierarchy(text)
        
        # 3. 메타데이터 생성
        metadata = self.generate_metadata(sections)
        
        # 4. 검증
        validation = self.validate_split_completeness(sections)
        
        # 5. 파일 생성
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.create_section_files(sections, self.output_base_dir)
        
        # 6. 메타데이터 저장
        with open(self.output_base_dir / "sections_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # 7. 분할 보고서 생성
        self._generate_split_report(sections, metadata, validation)
        
        result = {
            'sections': sections,
            'metadata': metadata,
            'validation': validation,
            'output_dir': str(self.output_base_dir)
        }
        
        print(f"✅ 분할 완료: {len(sections)}개 섹션, 유효성: {'통과' if validation['is_complete'] else '경고'}")
        
        return result
    
    def _generate_split_report(self, sections: Dict, metadata: Dict, validation: Dict) -> None:
        """분할 보고서 생성"""
        report_path = self.output_base_dir / "split_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 섹션 분할 보고서\n\n")
            f.write(f"**분할 일시:** {metadata['extraction_timestamp']}\n")
            f.write(f"**원본 파일:** {metadata['source_file']}\n")
            f.write(f"**총 섹션 수:** {metadata['total_sections']}\n\n")
            
            # 검증 결과
            f.write("## 검증 결과\n\n")
            f.write(f"**완전성:** {'✅ 통과' if validation['is_complete'] else '⚠️ 경고'}\n")
            f.write(f"**커버리지:** {validation['statistics']['coverage_percentage']:.1f}%\n\n")
            
            if validation['issues']:
                f.write("**발견된 문제:**\n")
                for issue in validation['issues']:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            # 섹션 유형별 통계
            f.write("## 섹션 유형별 통계\n\n")
            for section_type, count in metadata['section_types'].items():
                f.write(f"- **{section_type}:** {count}개\n")
            f.write("\n")
            
            # 계층 구조
            f.write("## 계층 구조\n\n")
            for section_num, info in metadata['hierarchy'].items():
                f.write(f"### {section_num}: {info['title']}\n")
                if info['has_intro']:
                    f.write(f"- 도입부: ✅\n")
                if info['subsections']:
                    f.write(f"- 하위섹션: {', '.join(info['subsections'])}\n")
                f.write("\n")
            
            # 전체 섹션 목록
            f.write("## 생성된 섹션 목록\n\n")
            sorted_sections = sorted(sections.items(), key=lambda x: x[1].get('start_line', 0))
            for section_id, section in sorted_sections:
                f.write(f"- **{section_id}**: {section['title']}")
                if section.get('page_range'):
                    f.write(f" (페이지: {section['page_range']})")
                f.write(f" [{section['type']}]\n")
        
        print(f"📋 분할 보고서 생성: {report_path}")

def main():
    """테스트 및 실행"""
    import sys
    
    if len(sys.argv) < 2:
        print("사용법: python universal_section_splitter.py <chapter_path> [output_dir]")
        print("예시: python universal_section_splitter.py Data-Oriented_Programming_Manning/Part1_Flexibility/Chapter1/original_text.md")
        return
    
    chapter_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        splitter = UniversalSectionSplitter(chapter_path, output_dir)
        result = splitter.split_chapter()
        
        print(f"\n🎉 분할 작업 완료!")
        print(f"📁 출력 디렉토리: {result['output_dir']}")
        print(f"📊 생성된 섹션: {len(result['sections'])}개")
        
        if not result['validation']['is_complete']:
            print(f"⚠️  검증 경고: {len(result['validation']['issues'])}개 문제 발견")
            for issue in result['validation']['issues']:
                print(f"   - {issue}")
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()