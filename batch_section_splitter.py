#!/usr/bin/env python3
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from universal_section_splitter import UniversalSectionSplitter
import concurrent.futures
from datetime import datetime

class BatchSectionSplitter:
    """
    전체 챕터에 대한 일괄 섹션 분할 시스템
    """
    
    def __init__(self, base_dir: str = "Data-Oriented_Programming_Manning"):
        self.base_dir = Path(base_dir)
        self.results = {}
        
    def find_all_chapters(self) -> List[Dict[str, str]]:
        """모든 챕터 파일 찾기"""
        chapters = []
        
        for part_dir in self.base_dir.iterdir():
            if part_dir.is_dir() and part_dir.name.startswith("Part"):
                for chapter_dir in part_dir.iterdir():
                    if chapter_dir.is_dir() and chapter_dir.name.startswith("Chapter"):
                        original_text_path = chapter_dir / "original_text.md"
                        if original_text_path.exists():
                            chapters.append({
                                'part': part_dir.name,
                                'chapter': chapter_dir.name,
                                'path': str(original_text_path),
                                'output_dir': str(chapter_dir / "content")
                            })
        
        return sorted(chapters, key=lambda x: (x['part'], x['chapter']))
    
    def split_single_chapter(self, chapter_info: Dict[str, str]) -> Dict[str, Any]:
        """단일 챕터 분할"""
        try:
            print(f"🔄 분할 중: {chapter_info['part']}/{chapter_info['chapter']}")
            
            splitter = UniversalSectionSplitter(
                chapter_path=chapter_info['path'],
                output_base_dir=chapter_info['output_dir']
            )
            
            result = splitter.split_chapter()
            result['chapter_info'] = chapter_info
            result['status'] = 'success'
            
            return result
            
        except Exception as e:
            print(f"❌ 실패: {chapter_info['part']}/{chapter_info['chapter']} - {e}")
            return {
                'chapter_info': chapter_info,
                'status': 'failed',
                'error': str(e)
            }
    
    def split_all_chapters(self, max_workers: int = 4) -> Dict[str, Any]:
        """모든 챕터 일괄 분할"""
        chapters = self.find_all_chapters()
        print(f"📚 총 {len(chapters)}개 챕터 발견")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_chapters': len(chapters),
            'successful': 0,
            'failed': 0,
            'chapters': {}
        }
        
        # 병렬 처리로 성능 향상
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_chapter = {
                executor.submit(self.split_single_chapter, chapter): chapter 
                for chapter in chapters
            }
            
            for future in concurrent.futures.as_completed(future_to_chapter):
                chapter = future_to_chapter[future]
                try:
                    result = future.result()
                    chapter_key = f"{chapter['part']}/{chapter['chapter']}"
                    results['chapters'][chapter_key] = result
                    
                    if result['status'] == 'success':
                        results['successful'] += 1
                        validation = result.get('validation', {})
                        if validation.get('is_complete', True):
                            print(f"✅ 완료: {chapter_key} ({len(result['sections'])}개 섹션)")
                        else:
                            print(f"⚠️  완료: {chapter_key} ({len(result['sections'])}개 섹션, 경고 있음)")
                    else:
                        results['failed'] += 1
                        
                except Exception as e:
                    chapter_key = f"{chapter['part']}/{chapter['chapter']}"
                    results['chapters'][chapter_key] = {
                        'chapter_info': chapter,
                        'status': 'failed',
                        'error': str(e)
                    }
                    results['failed'] += 1
                    print(f"❌ 실패: {chapter_key} - {e}")
        
        # 전체 요약 보고서 생성
        self._generate_batch_report(results)
        
        return results
    
    def split_specific_chapters(self, part_names: List[str] = None, chapter_numbers: List[int] = None) -> Dict[str, Any]:
        """특정 Part나 Chapter만 분할"""
        all_chapters = self.find_all_chapters()
        
        # 필터링
        filtered_chapters = []
        for chapter in all_chapters:
            include = True
            
            if part_names:
                if not any(pname in chapter['part'] for pname in part_names):
                    include = False
            
            if chapter_numbers:
                chapter_num = int(chapter['chapter'].replace('Chapter', ''))
                if chapter_num not in chapter_numbers:
                    include = False
            
            if include:
                filtered_chapters.append(chapter)
        
        print(f"📚 필터링된 {len(filtered_chapters)}개 챕터 분할 시작")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_chapters': len(filtered_chapters),
            'successful': 0,
            'failed': 0,
            'chapters': {},
            'filter_criteria': {
                'part_names': part_names,
                'chapter_numbers': chapter_numbers
            }
        }
        
        for chapter in filtered_chapters:
            result = self.split_single_chapter(chapter)
            chapter_key = f"{chapter['part']}/{chapter['chapter']}"
            results['chapters'][chapter_key] = result
            
            if result['status'] == 'success':
                results['successful'] += 1
            else:
                results['failed'] += 1
        
        self._generate_batch_report(results)
        return results
    
    def _generate_batch_report(self, results: Dict[str, Any]) -> None:
        """일괄 분할 보고서 생성"""
        report_path = self.base_dir / "batch_split_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 일괄 섹션 분할 보고서\n\n")
            f.write(f"**분할 일시:** {results['timestamp']}\n")
            f.write(f"**총 챕터 수:** {results['total_chapters']}\n")
            f.write(f"**성공:** {results['successful']}개\n")
            f.write(f"**실패:** {results['failed']}개\n")
            f.write(f"**성공률:** {(results['successful']/results['total_chapters']*100):.1f}%\n\n")
            
            if 'filter_criteria' in results:
                f.write("## 필터 조건\n\n")
                if results['filter_criteria']['part_names']:
                    f.write(f"- **Part:** {', '.join(results['filter_criteria']['part_names'])}\n")
                if results['filter_criteria']['chapter_numbers']:
                    f.write(f"- **Chapter:** {', '.join(map(str, results['filter_criteria']['chapter_numbers']))}\n")
                f.write("\n")
            
            # 성공한 챕터들
            successful_chapters = [
                (key, data) for key, data in results['chapters'].items() 
                if data['status'] == 'success'
            ]
            
            if successful_chapters:
                f.write("## ✅ 성공한 챕터\n\n")
                for chapter_key, data in successful_chapters:
                    sections_count = len(data['sections'])
                    validation = data.get('validation', {})
                    coverage = validation.get('statistics', {}).get('coverage_percentage', 0)
                    status_icon = "✅" if validation.get('is_complete', True) else "⚠️"
                    
                    f.write(f"- {status_icon} **{chapter_key}**: {sections_count}개 섹션 (커버리지: {coverage:.1f}%)\n")
                f.write("\n")
            
            # 실패한 챕터들
            failed_chapters = [
                (key, data) for key, data in results['chapters'].items() 
                if data['status'] == 'failed'
            ]
            
            if failed_chapters:
                f.write("## ❌ 실패한 챕터\n\n")
                for chapter_key, data in failed_chapters:
                    f.write(f"- **{chapter_key}**: {data.get('error', '알 수 없는 오류')}\n")
                f.write("\n")
            
            # 전체 통계
            f.write("## 📊 전체 통계\n\n")
            if successful_chapters:
                total_sections = sum(len(data['sections']) for _, data in successful_chapters)
                avg_sections = total_sections / len(successful_chapters)
                f.write(f"- **총 생성된 섹션:** {total_sections}개\n")
                f.write(f"- **챕터당 평균 섹션:** {avg_sections:.1f}개\n")
                
                # 섹션 유형별 통계
                type_counts = {}
                for _, data in successful_chapters:
                    for section in data['sections'].values():
                        section_type = section['type']
                        type_counts[section_type] = type_counts.get(section_type, 0) + 1
                
                f.write(f"- **섹션 유형별:**\n")
                for section_type, count in sorted(type_counts.items()):
                    f.write(f"  - {section_type}: {count}개\n")
        
        # JSON 결과도 저장
        with open(self.base_dir / "batch_split_results.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📋 일괄 분할 보고서 생성: {report_path}")

def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Data-Oriented Programming 책 섹션 일괄 분할")
    parser.add_argument("--base-dir", default="Data-Oriented_Programming_Manning", 
                       help="기본 디렉토리 경로")
    parser.add_argument("--parts", nargs="+", help="특정 Part만 분할 (예: Part1 Part2)")
    parser.add_argument("--chapters", nargs="+", type=int, help="특정 Chapter만 분할 (예: 1 2 3)")
    parser.add_argument("--workers", type=int, default=4, help="병렬 처리 worker 수")
    parser.add_argument("--list-only", action="store_true", help="챕터 목록만 표시")
    
    args = parser.parse_args()
    
    splitter = BatchSectionSplitter(args.base_dir)
    
    if args.list_only:
        chapters = splitter.find_all_chapters()
        print(f"📚 발견된 {len(chapters)}개 챕터:")
        for chapter in chapters:
            print(f"  - {chapter['part']}/{chapter['chapter']}")
        return
    
    try:
        if args.parts or args.chapters:
            print("🎯 특정 챕터 분할 모드")
            results = splitter.split_specific_chapters(
                part_names=args.parts,
                chapter_numbers=args.chapters
            )
        else:
            print("🌍 전체 챕터 분할 모드")
            results = splitter.split_all_chapters(max_workers=args.workers)
        
        print(f"\n🎉 일괄 분할 완료!")
        print(f"✅ 성공: {results['successful']}/{results['total_chapters']}개")
        if results['failed'] > 0:
            print(f"❌ 실패: {results['failed']}개")
        
        print(f"📋 상세 보고서: {splitter.base_dir / 'batch_split_report.md'}")
        
    except Exception as e:
        print(f"❌ 일괄 분할 중 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()