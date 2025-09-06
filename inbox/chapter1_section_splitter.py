#!/usr/bin/env python3
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class Chapter1SectionSplitter:
    """
    Chapter 1 전용 정확한 섹션 분할기
    원본 텍스트의 구조를 정확히 파악하여 도입부와 각 섹션을 올바르게 분할
    """
    
    def __init__(self, chapter_path: str, output_dir: str = None):
        self.chapter_path = Path(chapter_path)
        self.output_dir = Path(output_dir) if output_dir else self.chapter_path.parent / "content"
        self.original_text = ""
        self.lines = []
        
    def load_text(self) -> str:
        """원본 텍스트 로드"""
        with open(self.chapter_path, 'r', encoding='utf-8') as f:
            self.original_text = f.read()
        self.lines = self.original_text.split('\n')
        return self.original_text
    
    def find_section_boundaries(self) -> Dict[str, Dict]:
        """Chapter 1의 정확한 섹션 경계 찾기"""
        boundaries = {}
        
        # 핵심 마커들을 정확히 찾기
        for i, line in enumerate(self.lines):
            line_stripped = line.strip()
            
            # Chapter 시작 (메타데이터 이후 실제 내용)
            if "=== PAGE 31 ===" in line:
                boundaries['chapter_start'] = i
            
            # 1.1 섹션 시작
            elif line_stripped == "1.1 OOP design: Classic or classical?":
                boundaries['section_1_1_start'] = i
            
            # 1.1.1 시작
            elif line_stripped == "1.1.1 The design phase":
                boundaries['section_1_1_1_start'] = i
            
            # 1.1.2 시작
            elif line_stripped == "1.1.2 UML 101":
                boundaries['section_1_1_2_start'] = i
            
            # 1.1.3 시작
            elif line_stripped == "1.1.3 Explaining each piece of the class diagram":
                boundaries['section_1_1_3_start'] = i
            
            # 1.1.4 시작
            elif line_stripped == "1.1.4 The implementation phase":
                boundaries['section_1_1_4_start'] = i
            
            # 1.2 섹션 시작
            elif line_stripped == "1.2 Sources of complexity":
                boundaries['section_1_2_start'] = i
            
            # 1.2.1 시작
            elif line_stripped == "1.2.1 Many relations between classes":
                boundaries['section_1_2_1_start'] = i
            
            # 1.2.2 시작
            elif line_stripped == "1.2.2 Unpredictable code behavior":
                boundaries['section_1_2_2_start'] = i
            
            # 1.2.3 시작
            elif line_stripped == "1.2.3 Not trivial data serialization":
                boundaries['section_1_2_3_start'] = i
            
            # 1.2.4 시작
            elif line_stripped == "1.2.4 Complex class hierarchies":
                boundaries['section_1_2_4_start'] = i
            
            # Summary 시작
            elif line_stripped == "Summary":
                boundaries['summary_start'] = i
        
        return boundaries
    
    def extract_page_range(self, content: str) -> str:
        """내용에서 페이지 범위 추출"""
        page_numbers = []
        for match in re.finditer(r'=== PAGE (\d+) ===', content):
            page_numbers.append(int(match.group(1)))
        
        if page_numbers:
            return f"{min(page_numbers)}-{max(page_numbers)}"
        return ""
    
    def split_sections(self) -> Dict[str, Dict]:
        """정확한 섹션 분할 수행"""
        boundaries = self.find_section_boundaries()
        sections = {}
        
        print(f"🔍 발견된 경계점: {len(boundaries)}개")
        for key, line_num in boundaries.items():
            print(f"  - {key}: line {line_num}")
        
        # 1. Chapter 도입부 (시작 ~ 1.1 이전)
        if 'chapter_start' in boundaries and 'section_1_1_start' in boundaries:
            start = boundaries['chapter_start']
            end = boundaries['section_1_1_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['chapter_intro'] = {
                'title': 'Chapter Introduction',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'intro',
                'description': '챕터 도입부 (31-32페이지 초반)'
            }
        
        # 2. Section 1.1 도입부 (1.1 시작 ~ 1.1.1 이전)
        if 'section_1_1_start' in boundaries and 'section_1_1_1_start' in boundaries:
            start = boundaries['section_1_1_start']
            end = boundaries['section_1_1_1_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_1_intro'] = {
                'title': 'Section 1.1 Introduction - OOP design: Classic or classical?',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'section_intro',
                'description': '1.1 도입부'
            }
        
        # 3. Section 1.1.1
        if 'section_1_1_1_start' in boundaries and 'section_1_1_2_start' in boundaries:
            start = boundaries['section_1_1_1_start']
            end = boundaries['section_1_1_2_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_1_1'] = {
                'title': '1.1.1 The design phase',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.1.1 The design phase'
            }
        
        # 4. Section 1.1.2
        if 'section_1_1_2_start' in boundaries and 'section_1_1_3_start' in boundaries:
            start = boundaries['section_1_1_2_start']
            end = boundaries['section_1_1_3_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_1_2'] = {
                'title': '1.1.2 UML 101',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.1.2 UML 101'
            }
        
        # 5. Section 1.1.3
        if 'section_1_1_3_start' in boundaries and 'section_1_1_4_start' in boundaries:
            start = boundaries['section_1_1_3_start']
            end = boundaries['section_1_1_4_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_1_3'] = {
                'title': '1.1.3 Explaining each piece of the class diagram',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.1.3 Explaining each piece'
            }
        
        # 6. Section 1.1.4
        if 'section_1_1_4_start' in boundaries and 'section_1_2_start' in boundaries:
            start = boundaries['section_1_1_4_start']
            end = boundaries['section_1_2_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_1_4'] = {
                'title': '1.1.4 The implementation phase',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.1.4 Implementation phase'
            }
        
        # 7. Section 1.2 도입부 (1.2 시작 ~ 1.2.1 이전)
        if 'section_1_2_start' in boundaries and 'section_1_2_1_start' in boundaries:
            start = boundaries['section_1_2_start']
            end = boundaries['section_1_2_1_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_2_intro'] = {
                'title': 'Section 1.2 Introduction - Sources of complexity',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'section_intro',
                'description': '1.2 도입부'
            }
        
        # 8. Section 1.2.1
        if 'section_1_2_1_start' in boundaries and 'section_1_2_2_start' in boundaries:
            start = boundaries['section_1_2_1_start']
            end = boundaries['section_1_2_2_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_2_1'] = {
                'title': '1.2.1 Many relations between classes',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.2.1 Many relations'
            }
        
        # 9. Section 1.2.2
        if 'section_1_2_2_start' in boundaries and 'section_1_2_3_start' in boundaries:
            start = boundaries['section_1_2_2_start']
            end = boundaries['section_1_2_3_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_2_2'] = {
                'title': '1.2.2 Unpredictable code behavior',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.2.2 Unpredictable behavior'
            }
        
        # 10. Section 1.2.3
        if 'section_1_2_3_start' in boundaries and 'section_1_2_4_start' in boundaries:
            start = boundaries['section_1_2_3_start']
            end = boundaries['section_1_2_4_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_2_3'] = {
                'title': '1.2.3 Not trivial data serialization',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.2.3 Data serialization'
            }
        
        # 11. Section 1.2.4
        if 'section_1_2_4_start' in boundaries and 'summary_start' in boundaries:
            start = boundaries['section_1_2_4_start']
            end = boundaries['summary_start']
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['section_1_2_4'] = {
                'title': '1.2.4 Complex class hierarchies',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'subsection',
                'description': '1.2.4 Complex hierarchies'
            }
        
        # 12. Summary
        if 'summary_start' in boundaries:
            start = boundaries['summary_start']
            end = len(self.lines)
            content = '\n'.join(self.lines[start:end]).strip()
            
            sections['summary'] = {
                'title': 'Summary',
                'content': content,
                'page_range': self.extract_page_range(content),
                'type': 'summary',
                'description': 'Summary 섹션'
            }
        
        return sections
    
    def create_section_files(self, sections: Dict[str, Dict]) -> None:
        """섹션 파일들 생성"""
        sections_dir = self.output_dir / "sections"
        sections_dir.mkdir(parents=True, exist_ok=True)
        
        # 정해진 순서대로 섹션 생성
        ordered_sections = [
            'chapter_intro',
            'section_1_1_intro', 
            'section_1_1_1',
            'section_1_1_2',
            'section_1_1_3',
            'section_1_1_4',
            'section_1_2_intro',
            'section_1_2_1',
            'section_1_2_2',
            'section_1_2_3',
            'section_1_2_4',
            'summary'
        ]
        
        created_files = []
        for section_id in ordered_sections:
            if section_id in sections:
                section = sections[section_id]
                filename = f"{section_id}.md"
                file_path = sections_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {section['title']}\n\n")
                    f.write(f"**설명:** {section['description']}\n")
                    if section['page_range']:
                        f.write(f"**페이지 범위:** {section['page_range']}\n")
                    f.write(f"**섹션 유형:** {section['type']}\n\n")
                    f.write(section['content'])
                
                created_files.append(filename)
                print(f"✓ 생성: {filename} ({len(section['content'])} chars)")
        
        return created_files
    
    def generate_metadata(self, sections: Dict[str, Dict]) -> Dict:
        """메타데이터 생성"""
        metadata = {
            'extraction_timestamp': datetime.now().isoformat(),
            'source_file': str(self.chapter_path),
            'total_sections': len(sections),
            'extractor': 'Chapter1SectionSplitter',
            'sections': {}
        }
        
        for section_id, section in sections.items():
            metadata['sections'][section_id] = {
                'title': section['title'],
                'type': section['type'],
                'description': section['description'],
                'page_range': section['page_range'],
                'content_length': len(section['content'])
            }
        
        return metadata
    
    def validate_sections(self, sections: Dict[str, Dict]) -> Dict:
        """섹션 분할 검증"""
        validation = {
            'is_complete': True,
            'issues': [],
            'statistics': {
                'expected_sections': 12,
                'found_sections': len(sections),
                'total_content_length': sum(len(s['content']) for s in sections.values()),
                'original_length': len(self.original_text)
            }
        }
        
        expected_sections = [
            'chapter_intro', 'section_1_1_intro', 'section_1_1_1', 'section_1_1_2',
            'section_1_1_3', 'section_1_1_4', 'section_1_2_intro', 'section_1_2_1',
            'section_1_2_2', 'section_1_2_3', 'section_1_2_4', 'summary'
        ]
        
        # 누락된 섹션 확인
        missing_sections = [s for s in expected_sections if s not in sections]
        if missing_sections:
            validation['issues'].append(f"누락된 섹션: {', '.join(missing_sections)}")
            validation['is_complete'] = False
        
        # 빈 섹션 확인
        empty_sections = [s for s, data in sections.items() if len(data['content'].strip()) < 10]
        if empty_sections:
            validation['issues'].append(f"내용이 부족한 섹션: {', '.join(empty_sections)}")
        
        # 커버리지 계산
        if validation['statistics']['original_length'] > 0:
            coverage = (validation['statistics']['total_content_length'] / 
                       validation['statistics']['original_length']) * 100
            validation['statistics']['coverage_percentage'] = round(coverage, 1)
        
        return validation
    
    def generate_report(self, sections: Dict, metadata: Dict, validation: Dict) -> None:
        """분할 보고서 생성"""
        report_path = self.output_dir / "chapter1_split_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Chapter 1 전용 섹션 분할 보고서\n\n")
            f.write(f"**분할 일시:** {metadata['extraction_timestamp']}\n")
            f.write(f"**원본 파일:** {metadata['source_file']}\n")
            f.write(f"**총 섹션 수:** {metadata['total_sections']}\n")
            f.write(f"**추출기:** {metadata['extractor']}\n\n")
            
            # 검증 결과
            f.write("## 🔍 검증 결과\n\n")
            status = "✅ 완료" if validation['is_complete'] else "⚠️ 경고"
            f.write(f"**완전성:** {status}\n")
            f.write(f"**발견된 섹션:** {validation['statistics']['found_sections']}/{validation['statistics']['expected_sections']}\n")
            
            if 'coverage_percentage' in validation['statistics']:
                f.write(f"**커버리지:** {validation['statistics']['coverage_percentage']}%\n")
            
            if validation['issues']:
                f.write(f"\n**발견된 문제:**\n")
                for issue in validation['issues']:
                    f.write(f"- {issue}\n")
            f.write("\n")
            
            # 섹션 목록
            f.write("## 📋 생성된 섹션 목록\n\n")
            section_order = [
                'chapter_intro', 'section_1_1_intro', 'section_1_1_1', 'section_1_1_2',
                'section_1_1_3', 'section_1_1_4', 'section_1_2_intro', 'section_1_2_1',
                'section_1_2_2', 'section_1_2_3', 'section_1_2_4', 'summary'
            ]
            
            for i, section_id in enumerate(section_order, 1):
                if section_id in sections:
                    section = sections[section_id]
                    f.write(f"{i}. **{section_id}**: {section['title']}")
                    if section['page_range']:
                        f.write(f" (페이지: {section['page_range']})")
                    f.write(f" [{section['type']}]\n")
                    f.write(f"   - {section['description']}\n")
                else:
                    f.write(f"{i}. **{section_id}**: ❌ 누락\n")
        
        print(f"📋 보고서 생성: {report_path}")
    
    def split_chapter1(self) -> Dict:
        """Chapter 1 전체 분할 실행"""
        print(f"📚 Chapter 1 전용 분할 시작: {self.chapter_path}")
        
        # 1. 텍스트 로드
        self.load_text()
        
        # 2. 섹션 분할
        sections = self.split_sections()
        
        # 3. 파일 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        created_files = self.create_section_files(sections)
        
        # 4. 메타데이터 생성
        metadata = self.generate_metadata(sections)
        
        # 5. 검증
        validation = self.validate_sections(sections)
        
        # 6. 메타데이터 저장
        with open(self.output_dir / "chapter1_sections_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # 7. 보고서 생성
        self.generate_report(sections, metadata, validation)
        
        result = {
            'sections': sections,
            'metadata': metadata,
            'validation': validation,
            'created_files': created_files,
            'output_dir': str(self.output_dir)
        }
        
        status = "완료" if validation['is_complete'] else "경고"
        print(f"✅ Chapter 1 분할 {status}: {len(sections)}개 섹션 생성")
        
        return result

def main():
    """메인 실행"""
    chapter_path = "/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_Manning/Part1_Flexibility/Chapter1/original_text.md"
    
    splitter = Chapter1SectionSplitter(chapter_path)
    
    try:
        result = splitter.split_chapter1()
        
        print(f"\n🎉 Chapter 1 분할 완료!")
        print(f"📁 출력 디렉토리: {result['output_dir']}")
        print(f"📊 생성된 파일: {len(result['created_files'])}개")
        
        validation = result['validation']
        if not validation['is_complete']:
            print(f"⚠️ 검증 경고:")
            for issue in validation['issues']:
                print(f"   - {issue}")
        
        if 'coverage_percentage' in validation['statistics']:
            print(f"📈 커버리지: {validation['statistics']['coverage_percentage']}%")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()