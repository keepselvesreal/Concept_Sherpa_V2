#!/usr/bin/env python3
import pdfplumber
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class PartBasedExtractor:
    def __init__(self, pdf_path: str, output_dir: str = "Data-Oriented_Programming_Manning"):
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.parts_info = self._get_parts_info()
        
    def _get_parts_info(self) -> Dict:
        """Part별 Chapter 정보를 반환"""
        return {
            "Part1_Flexibility": {
                "title": "Flexibility",
                "chapters": [
                    {"num": 1, "title": "Complexity of object-oriented programming", "subtitle": "A capricious entrepreneur", "start": 31, "end": 53},
                    {"num": 2, "title": "Separation between code and data", "subtitle": "A whole new world", "start": 54, "end": 70},
                    {"num": 3, "title": "Basic data manipulation", "subtitle": "Meditation and programming", "start": 71, "end": 98},
                    {"num": 4, "title": "State management", "subtitle": "Time travel", "start": 99, "end": 118},
                    {"num": 5, "title": "Basic concurrency control", "subtitle": "Conflicts at home", "start": 119, "end": 137},
                    {"num": 6, "title": "Unit tests", "subtitle": "Programming at a coffee shop", "start": 138, "end": 168}
                ]
            },
            "Part2_Scalability": {
                "title": "Scalability", 
                "chapters": [
                    {"num": 7, "title": "Basic data validation", "subtitle": "A solemn gift", "start": 169, "end": 190},
                    {"num": 8, "title": "Advanced concurrency control", "subtitle": "No more deadlocks!", "start": 191, "end": 202},
                    {"num": 9, "title": "Persistent data structures", "subtitle": "Standing on the shoulders of giants", "start": 203, "end": 224},
                    {"num": 10, "title": "Database operations", "subtitle": "A cloud is a cloud", "start": 225, "end": 247},
                    {"num": 11, "title": "Web services", "subtitle": "A faithful messenger", "start": 248, "end": 274}
                ]
            },
            "Part3_Maintainability": {
                "title": "Maintainability",
                "chapters": [
                    {"num": 12, "title": "Advanced data validation", "subtitle": "A self-made gift", "start": 275, "end": 299},
                    {"num": 13, "title": "Polymorphism", "subtitle": "Playing with the animals in the countryside", "start": 300, "end": 322},
                    {"num": 14, "title": "Advanced data manipulation", "subtitle": "Whatever is well-conceived is clearly said", "start": 323, "end": 338},
                    {"num": 15, "title": "Debugging", "subtitle": "Innovation at the museum", "start": 339, "end": 380}  # 추정값
                ]
            }
        }
    
    def extract_all_parts(self) -> None:
        """모든 Part의 모든 Chapter를 추출"""
        print("PDF에서 모든 Part와 Chapter 추출 시작...")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"총 PDF 페이지 수: {total_pages}")
            
            for part_id, part_info in self.parts_info.items():
                print(f"\n=== {part_id}: {part_info['title']} 처리 중 ===")
                
                # Part 디렉토리 생성
                part_dir = self.output_dir / part_id
                part_dir.mkdir(parents=True, exist_ok=True)
                
                # Part 메타데이터 생성
                part_metadata = {
                    "part_name": part_id,
                    "part_title": part_info['title'],
                    "chapters_count": len(part_info['chapters']),
                    "chapters": []
                }
                
                # 각 Chapter 추출
                for chapter_info in part_info['chapters']:
                    print(f"  Chapter {chapter_info['num']}: {chapter_info['title']} 추출 중...")
                    
                    chapter_data = self._extract_chapter(pdf, chapter_info, total_pages)
                    if chapter_data and chapter_data['full_text'].strip():
                        # Chapter 저장
                        self._save_chapter(part_dir, chapter_data)
                        part_metadata['chapters'].append({
                            "chapter_num": chapter_info['num'],
                            "title": chapter_info['title'],
                            "subtitle": chapter_info['subtitle'],
                            "page_range": f"{chapter_info['start']}-{chapter_info['end']}"
                        })
                        print(f"    ✓ 저장 완료: {chapter_info['start']}-{chapter_info['end']}페이지")
                    else:
                        print(f"    ✗ 추출 실패: Chapter {chapter_info['num']}")
                
                # Part 메타데이터 저장
                with open(part_dir / "part_metadata.json", "w", encoding="utf-8") as f:
                    json.dump(part_metadata, f, indent=2, ensure_ascii=False)
                
                print(f"✓ {part_id} 완료: {len(part_metadata['chapters'])}개 챕터 추출")
        
        print("\n🎉 모든 Part와 Chapter 추출 완료!")
        self._create_summary_report()
    
    def _extract_chapter(self, pdf, chapter_info: Dict, total_pages: int) -> Optional[Dict]:
        """단일 Chapter를 추출"""
        start_page = chapter_info['start'] - 1  # 0-based index
        end_page = min(chapter_info['end'], total_pages) - 1
        
        chapter_text = ""
        actual_start = None
        actual_end = None
        
        # 챕터 텍스트 추출
        for page_num in range(start_page, end_page + 1):
            if page_num >= total_pages:
                break
                
            page = pdf.pages[page_num]
            page_text = page.extract_text() or ""
            
            if page_text.strip():
                if actual_start is None:
                    actual_start = page_num + 1
                actual_end = page_num + 1
                chapter_text += f"=== PAGE {page_num + 1} ===\n{page_text}\n\n"
        
        if not chapter_text.strip():
            return None
        
        return {
            "chapter_number": chapter_info['num'],
            "title": chapter_info['title'],
            "subtitle": chapter_info['subtitle'],
            "planned_start_page": chapter_info['start'],
            "planned_end_page": chapter_info['end'],
            "actual_start_page": actual_start,
            "actual_end_page": actual_end,
            "full_text": chapter_text.strip()
        }
    
    def _save_chapter(self, part_dir: Path, chapter_data: Dict) -> None:
        """Chapter 데이터를 파일로 저장"""
        chapter_num = chapter_data['chapter_number']
        chapter_dir = part_dir / f"Chapter{chapter_num}"
        chapter_dir.mkdir(exist_ok=True)
        
        # 원본 텍스트 저장
        original_file = chapter_dir / "original_text.md"
        with open(original_file, "w", encoding="utf-8") as f:
            f.write(f"# Chapter {chapter_num}: {chapter_data['title']}\n\n")
            f.write(f"**부제목:** {chapter_data['subtitle']}\n")
            f.write(f"**계획된 페이지:** {chapter_data['planned_start_page']}-{chapter_data['planned_end_page']}\n")
            f.write(f"**실제 페이지:** {chapter_data['actual_start_page']}-{chapter_data['actual_end_page']}\n\n")
            f.write(chapter_data['full_text'])
        
        # Chapter 메타데이터 저장
        metadata = {
            "chapter_number": chapter_data['chapter_number'],
            "title": chapter_data['title'],
            "subtitle": chapter_data['subtitle'],
            "planned_page_range": f"{chapter_data['planned_start_page']}-{chapter_data['planned_end_page']}",
            "actual_page_range": f"{chapter_data['actual_start_page']}-{chapter_data['actual_end_page']}",
            "text_length": len(chapter_data['full_text']),
            "extraction_timestamp": "2025-01-24"
        }
        
        with open(chapter_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _create_summary_report(self) -> None:
        """전체 추출 결과 요약 보고서 생성"""
        summary = {
            "extraction_date": "2025-01-24",
            "total_parts": len(self.parts_info),
            "parts_summary": {}
        }
        
        total_chapters = 0
        for part_id, part_info in self.parts_info.items():
            part_dir = self.output_dir / part_id
            if part_dir.exists():
                chapters_extracted = len([d for d in part_dir.iterdir() if d.is_dir() and d.name.startswith("Chapter")])
                total_chapters += chapters_extracted
                
                summary["parts_summary"][part_id] = {
                    "title": part_info['title'],
                    "planned_chapters": len(part_info['chapters']),
                    "extracted_chapters": chapters_extracted,
                    "success_rate": f"{chapters_extracted}/{len(part_info['chapters'])}"
                }
        
        summary["total_chapters_extracted"] = total_chapters
        summary["total_chapters_planned"] = sum(len(part['chapters']) for part in self.parts_info.values())
        
        # 요약 보고서 저장
        with open(self.output_dir / "extraction_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # 사람이 읽기 쉬운 요약 보고서
        with open(self.output_dir / "extraction_report.md", "w", encoding="utf-8") as f:
            f.write("# Data-Oriented Programming - 추출 완료 보고서\n\n")
            f.write(f"**추출 일시:** {summary['extraction_date']}\n")
            f.write(f"**총 Part 수:** {summary['total_parts']}\n")
            f.write(f"**총 추출된 Chapter 수:** {summary['total_chapters_extracted']}/{summary['total_chapters_planned']}\n\n")
            
            f.write("## Part별 추출 결과\n\n")
            for part_id, part_summary in summary["parts_summary"].items():
                f.write(f"### {part_id}: {part_summary['title']}\n")
                f.write(f"- 계획된 Chapter 수: {part_summary['planned_chapters']}\n")
                f.write(f"- 추출된 Chapter 수: {part_summary['extracted_chapters']}\n")
                f.write(f"- 성공률: {part_summary['success_rate']}\n\n")
            
            f.write("## 디렉토리 구조\n\n")
            f.write("```\n")
            f.write("Data-Oriented_Programming_Manning/\n")
            for part_id, part_info in self.parts_info.items():
                f.write(f"├── {part_id}/\n")
                f.write(f"│   ├── part_metadata.json\n")
                for chapter in part_info['chapters']:
                    f.write(f"│   └── Chapter{chapter['num']}/\n")
                    f.write(f"│       ├── original_text.md\n")
                    f.write(f"│       └── metadata.json\n")
            f.write("├── extraction_summary.json\n")
            f.write("└── extraction_report.md\n")
            f.write("```\n")
        
        print(f"\n📊 요약 보고서 생성 완료:")
        print(f"   - 총 {summary['total_chapters_extracted']}/{summary['total_chapters_planned']} 챕터 추출")
        print(f"   - 보고서 위치: {self.output_dir / 'extraction_report.md'}")

def main():
    """메인 실행 함수"""
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print("🚀 Data-Oriented Programming 책 전체 추출 시작")
    print(f"📖 PDF 경로: {pdf_path}")
    
    extractor = PartBasedExtractor(pdf_path)
    
    try:
        extractor.extract_all_parts()
        print("\n✅ 모든 작업이 성공적으로 완료되었습니다!")
        
    except Exception as e:
        print(f"\n❌ 추출 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()