#!/usr/bin/env python3
"""
2단계: 추출된 JSON 내용을 해당 TOC_Structure 파일들에 저장
"""

import json
import re
from pathlib import Path
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentSaver:
    def __init__(self, json_file: str, toc_structure_path: str):
        self.json_file = Path(json_file)
        self.toc_structure_path = Path(toc_structure_path)
        self.content_data = {}
        
    def load_extracted_content(self) -> dict:
        """JSON 파일에서 추출된 내용을 로드한다"""
        
        if not self.json_file.exists():
            raise FileNotFoundError(f"JSON 파일이 존재하지 않습니다: {self.json_file}")
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.content_data = data["sections"]
        logger.info(f"JSON 로드 완료: {len(self.content_data)}개 섹션")
        
        return data
    
    def find_content_files(self, section_title: str) -> List[Path]:
        """섹션 제목에 해당하는 [CONTENT].md 파일들을 찾는다"""
        
        # 제목 정리
        clean_title = section_title.replace(" (사용자 추가)", "")
        
        # 검색 패턴들
        search_patterns = []
        
        # 1. 정확한 제목으로 검색
        clean_for_search = re.sub(r'[^\w\s\-\.]', ' ', clean_title)
        clean_for_search = re.sub(r'\s+', ' ', clean_for_search).strip()
        search_patterns.append(f"*{clean_for_search}*[CONTENT].md")
        
        # 2. 숫자 패턴이 있으면 숫자로도 검색
        if re.match(r'^\d+', clean_title):
            number_match = re.match(r'^(\d+(?:\.\d+(?:\.\d+)?)?)', clean_title)
            if number_match:
                number_part = number_match.group(1)
                search_patterns.append(f"*{number_part}*[CONTENT].md")
        
        # 3. 주요 키워드로 검색
        key_words = []
        if "Summary" in section_title:
            key_words.append("Summary")
        elif "Introduction" in section_title:
            key_words.append("Introduction")
        elif "design phase" in section_title:
            key_words.extend(["design", "phase"])
        elif "UML" in section_title:
            key_words.append("UML")
        elif "class diagram" in section_title:
            key_words.extend(["class", "diagram"])
        elif "implementation" in section_title:
            key_words.append("implementation")
        elif "relations" in section_title:
            key_words.append("relations")
        elif "Unpredictable" in section_title:
            key_words.append("Unpredictable")
        elif "serialization" in section_title:
            key_words.append("serialization")
        elif "hierarchies" in section_title:
            key_words.append("hierarchies")
        elif "tree of function" in section_title:
            key_words.extend(["tree", "function"])
        elif "functions down" in section_title:
            key_words.extend(["functions", "down"])
        elif "nodes in the tree" in section_title:
            key_words.extend(["nodes", "tree"])
        
        for word in key_words:
            search_patterns.append(f"*{word}*[CONTENT].md")
        
        # 실제 파일 검색
        found_files = []
        for pattern in search_patterns:
            files = list(self.toc_structure_path.rglob(pattern))
            found_files.extend(files)
        
        # 중복 제거
        unique_files = list(set(found_files))
        
        if unique_files:
            logger.info(f"'{section_title}' -> {len(unique_files)}개 파일 발견")
            for file in unique_files[:3]:  # 처음 3개만 로그
                logger.info(f"  - {file.name}")
        else:
            logger.warning(f"'{section_title}'에 해당하는 파일을 찾을 수 없음")
        
        return unique_files
    
    def save_content_to_file(self, file_path: Path, section_data: dict) -> bool:
        """내용을 특정 파일에 저장한다"""
        
        try:
            # 디렉토리 확인
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            title = section_data["title"]
            content = section_data["content"]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                
                if content:
                    f.write("## 추출된 내용\n\n")
                    f.write(content)
                    f.write(f"\n\n---\n\n")
                    f.write(f"**추출 완료**: {section_data['length']} 문자\n")
                    f.write(f"**추출 시간**: {section_data['extracted_at']}\n")
                    f.write(f"**파일 경로**: {file_path.name}\n")
                else:
                    f.write("## 내용 추출 실패\n\n")
                    f.write("PDF에서 해당 섹션을 찾을 수 없습니다.\n")
            
            logger.info(f"저장 완료: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"파일 저장 실패 {file_path}: {e}")
            return False
    
    def process_all_sections(self, save_mode: str = "first") -> dict:
        """모든 섹션을 처리한다
        
        Args:
            save_mode: "first" (첫 번째 파일만), "all" (모든 매칭 파일), "ask" (사용자 선택)
        """
        
        if not self.content_data:
            self.load_extracted_content()
        
        results = {
            "processed": 0,
            "saved": 0,
            "no_files_found": 0,
            "errors": 0,
            "details": []
        }
        
        for section_title, section_data in self.content_data.items():
            logger.info(f"\n처리 중: {section_title}")
            
            # 해당 파일들 찾기
            matching_files = self.find_content_files(section_title)
            
            if not matching_files:
                results["no_files_found"] += 1
                results["details"].append({
                    "section": section_title,
                    "status": "no_files_found",
                    "files": []
                })
                continue
            
            # 저장 모드에 따라 처리
            files_to_save = []
            if save_mode == "first":
                files_to_save = [matching_files[0]]
            elif save_mode == "all":
                files_to_save = matching_files
            elif save_mode == "ask":
                print(f"\n[{section_title}] 매칭된 파일들:")
                for i, file in enumerate(matching_files, 1):
                    print(f"  {i}. {file.name}")
                
                choice = input("저장할 파일 선택 (1-숫자, a-모두, s-스킵): ").strip().lower()
                
                if choice == 's':
                    continue
                elif choice == 'a':
                    files_to_save = matching_files
                elif choice.isdigit() and 1 <= int(choice) <= len(matching_files):
                    files_to_save = [matching_files[int(choice) - 1]]
            
            # 실제 저장
            saved_files = []
            for file_path in files_to_save:
                if self.save_content_to_file(file_path, section_data):
                    saved_files.append(str(file_path))
                    results["saved"] += 1
                else:
                    results["errors"] += 1
            
            results["details"].append({
                "section": section_title,
                "status": "saved" if saved_files else "error",
                "files": saved_files
            })
            
            results["processed"] += 1
        
        return results
    
    def print_summary(self, results: dict):
        """결과 요약을 출력한다"""
        
        print(f"\n=== 저장 결과 요약 ===")
        print(f"처리된 섹션: {results['processed']}")
        print(f"저장 성공: {results['saved']} 파일")
        print(f"파일 없음: {results['no_files_found']} 섹션")
        print(f"오류 발생: {results['errors']} 파일")
        
        print(f"\n=== 상세 결과 ===")
        for detail in results["details"]:
            status_emoji = {"saved": "✅", "no_files_found": "❌", "error": "⚠️"}.get(detail["status"], "❓")
            print(f"{status_emoji} {detail['section']}")
            if detail["files"]:
                for file in detail["files"]:
                    print(f"    → {Path(file).name}")

def main():
    json_file = "/home/nadle/projects/Knowledge_Sherpa/v2/extracted_content.json"
    toc_structure_path = "/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization/TOC_Structure"
    
    if not Path(json_file).exists():
        print(f"오류: {json_file}이 존재하지 않습니다.")
        print("먼저 step1_extract_content.py를 실행하세요.")
        return
    
    saver = ContentSaver(json_file, toc_structure_path)
    
    print("=== 2단계: 파일 저장 ===")
    print("저장 모드 선택:")
    print("1. first - 각 섹션마다 첫 번째 매칭 파일에만 저장")
    print("2. all - 각 섹션마다 모든 매칭 파일에 저장")  
    print("3. ask - 각 섹션마다 사용자가 선택")
    
    mode_choice = input("선택하세요 (1-3): ").strip()
    
    save_mode = {"1": "first", "2": "all", "3": "ask"}.get(mode_choice, "first")
    
    print(f"\n'{save_mode}' 모드로 처리를 시작합니다...")
    
    # 처리 실행
    results = saver.process_all_sections(save_mode)
    
    # 결과 출력
    saver.print_summary(results)
    
    print(f"\n2단계 완료!")

if __name__ == "__main__":
    main()