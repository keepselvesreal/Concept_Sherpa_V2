# 목차
# - 생성 시간: 2025-08-07 20:20:30 KST
# - 핵심 내용: Part 2 리프노드 개선된 추출 스크립트 (2차 시도)
# - 상세 내용: 
#   - TOC JSON 파일을 참조하여 정확한 페이지 범위 매핑
#   - 누락된 Introduction 섹션들과 Summary 섹션 정확 추출
#   - part2_leafnodes_v2/ 디렉토리에 저장
# - 상태: 활성
# - 주소: part2_leaf_extractor_v2
# - 참조: part2_leaf_extractor.py, toc_with_page_ranges_v2.json

#!/usr/bin/env python3
import os
import sys
import json
import re

def load_toc_json(toc_file_path):
    """TOC JSON 파일 로드"""
    try:
        with open(toc_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading TOC JSON: {e}")
        return None

def find_section_by_title(toc_data, title_pattern):
    """TOC에서 제목으로 섹션 찾기"""
    for item in toc_data:
        if re.search(title_pattern, item.get('title', ''), re.IGNORECASE):
            return item
    return None

def extract_part2_leaf_nodes_v2(part2_file_path, toc_file_path):
    """Part 2의 모든 리프노드를 개선된 방식으로 추출 (2차 시도)"""
    
    # 출력 디렉토리 생성
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/part2_leafnodes_v2"
    os.makedirs(output_dir, exist_ok=True)
    
    # Part 2 파일 및 TOC 읽기
    try:
        with open(part2_file_path, 'r', encoding='utf-8') as f:
            part2_content = f.read()
        
        toc_data = load_toc_json(toc_file_path)
        if not toc_data:
            return
            
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        return
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return
    
    def extract_content_by_page_markers(content, start_pattern, end_pattern=None):
        """페이지 마커를 기준으로 내용 추출"""
        start_match = re.search(rf"## 페이지 {start_pattern}", content)
        if not start_match:
            return ""
            
        start_idx = start_match.start()
        
        if end_pattern:
            end_match = re.search(rf"## 페이지 {end_pattern}", content[start_idx + 50:])
            if end_match:
                end_idx = start_idx + 50 + end_match.start()
            else:
                end_idx = len(content)
        else:
            end_idx = len(content)
            
        extracted = content[start_idx:end_idx].strip()
        
        # 페이지 마커 다음부터 내용 시작
        first_newline = extracted.find('\n\n')
        if first_newline != -1:
            extracted = extracted[first_newline + 2:].strip()
        
        return extracted
    
    def extract_content_by_section_headers(content, start_header, end_header=None):
        """섹션 헤더를 기준으로 내용 추출"""
        # 헤더 패턴 매칭 (숫자.숫자 형식 포함)
        start_pattern = re.escape(start_header).replace(r'\.', r'\.')
        start_match = re.search(rf"^{start_pattern}(?:\s|$)", content, re.MULTILINE)
        
        if not start_match:
            return ""
            
        start_idx = start_match.start()
        
        if end_header:
            end_pattern = re.escape(end_header).replace(r'\.', r'\.')
            end_match = re.search(rf"^{end_pattern}(?:\s|$)", content[start_idx + 50:], re.MULTILINE)
            if end_match:
                end_idx = start_idx + 50 + end_match.start()
            else:
                end_idx = len(content)
        else:
            # 다음 주요 섹션까지
            next_chapter = re.search(r"^\d+\s+\w+", content[start_idx + 50:], re.MULTILINE)
            if next_chapter:
                end_idx = start_idx + 50 + next_chapter.start()
            else:
                end_idx = len(content)
                
        return content[start_idx:end_idx].strip()
    
    def extract_summary_content(content, chapter_num):
        """특정 챕터의 Summary 추출"""
        # Summary 패턴을 더 정확하게 찾기
        summary_patterns = [
            rf"Summary\s*\n.*?(?=\n\n\d+\s+\w+|\nPart\s+\d+|\Z)",
            rf"^Summary.*?(?=^\d+\s+\w+|^Part\s+\d+|\Z)",
        ]
        
        # 해당 챕터 이후 영역에서 Summary 찾기
        chapter_pattern = rf"^{chapter_num}\s+\w+"
        chapter_match = re.search(chapter_pattern, content, re.MULTILINE)
        
        if chapter_match:
            search_start = chapter_match.end()
            search_content = content[search_start:]
            
            for pattern in summary_patterns:
                summary_match = re.search(pattern, search_content, re.DOTALL | re.MULTILINE)
                if summary_match:
                    return summary_match.group(0).strip()
        
        return ""
    
    # 개선된 리프노드 정의 (TOC 기반)
    leaf_sections = [
        # Part 2 Introduction
        {
            "file": "part2_0_introduction.md",
            "title": "# Part 2 Introduction (사용자 추가)",
            "extract_method": "page_range",
            "start_page": "165",
            "end_page": "169"
        },
        
        # Chapter 7 - Basic data validation
        {
            "file": "7_0_introduction.md",
            "title": "# 7.0 Introduction (사용자 추가)",
            "extract_method": "page_range", 
            "start_page": "169",
            "end_page": "170",
            "description": "Chapter 7 도입부 (7 Basic data validation과 7.1 사이)"
        },
        {
            "file": "7_1_data_validation_dop.md",
            "title": "# 7.1 Data validation in DOP",
            "extract_method": "section_header",
            "start_header": "7.1 Data validation in DOP",
            "end_header": "7.2 JSON Schema in a nutshell"
        },
        {
            "file": "7_2_json_schema.md",
            "title": "# 7.2 JSON Schema in a nutshell",
            "extract_method": "section_header",
            "start_header": "7.2 JSON Schema in a nutshell",
            "end_header": "7.3 Schema flexibility and strictness"
        },
        {
            "file": "7_3_schema_flexibility.md",
            "title": "# 7.3 Schema flexibility and strictness",
            "extract_method": "section_header",
            "start_header": "7.3 Schema flexibility and strictness",
            "end_header": "7.4 Schema composition"
        },
        {
            "file": "7_4_schema_composition.md",
            "title": "# 7.4 Schema composition",
            "extract_method": "section_header",
            "start_header": "7.4 Schema composition", 
            "end_header": "7.5 Details about data validation failures"
        },
        {
            "file": "7_5_validation_failures.md",
            "title": "# 7.5 Details about data validation failures",
            "extract_method": "section_header",
            "start_header": "7.5 Details about data validation failures",
            "end_header": "Summary"
        },
        {
            "file": "7_summary.md",
            "title": "# Chapter 7 Summary",
            "extract_method": "summary",
            "chapter_num": 7
        },
        
        # Chapter 8 - Advanced concurrency control
        {
            "file": "8_0_introduction.md", 
            "title": "# 8.0 Introduction (사용자 추가)",
            "extract_method": "page_range",
            "start_page": "191",
            "end_page": "192",
            "description": "Chapter 8 도입부"
        },
        {
            "file": "8_1_complexity_locks.md",
            "title": "# 8.1 The complexity of locks",
            "extract_method": "section_header",
            "start_header": "8.1 The complexity of locks",
            "end_header": "8.2 Thread-safe counter with atoms"
        },
        {
            "file": "8_2_thread_safe_counter.md",
            "title": "# 8.2 Thread-safe counter with atoms",
            "extract_method": "section_header",
            "start_header": "8.2 Thread-safe counter with atoms",
            "end_header": "8.3 Thread-safe cache with atoms"
        },
        {
            "file": "8_3_thread_safe_cache.md",
            "title": "# 8.3 Thread-safe cache with atoms", 
            "extract_method": "section_header",
            "start_header": "8.3 Thread-safe cache with atoms",
            "end_header": "8.4 State management with atoms"
        },
        {
            "file": "8_4_state_management_atoms.md",
            "title": "# 8.4 State management with atoms",
            "extract_method": "section_header",
            "start_header": "8.4 State management with atoms",
            "end_header": "Summary"
        },
        {
            "file": "8_summary.md",
            "title": "# Chapter 8 Summary",
            "extract_method": "summary",
            "chapter_num": 8
        },
        
        # Chapter 9 - Persistent data structures
        {
            "file": "9_0_introduction.md",
            "title": "# 9.0 Introduction (사용자 추가)",
            "extract_method": "section_header",
            "start_header": "9 Persistent data structures",
            "end_header": "9.1 The need for persistent data structures"
        },
        {
            "file": "9_1_need_persistent.md",
            "title": "# 9.1 The need for persistent data structures",
            "extract_method": "section_header",
            "start_header": "9.1 The need for persistent data structures",
            "end_header": "9.2 The efficiency of persistent data structures"
        },
        {
            "file": "9_2_efficiency_persistent.md",
            "title": "# 9.2 The efficiency of persistent data structures",
            "extract_method": "section_header",
            "start_header": "9.2 The efficiency of persistent data structures",
            "end_header": "9.3 Persistent data structures libraries"
        },
        {
            "file": "9_3_0_introduction.md",
            "title": "# 9.3.0 Introduction (사용자 추가)",
            "extract_method": "section_header",
            "start_header": "9.3 Persistent data structures libraries",
            "end_header": "9.3.1 Persistent data structures in Java"
        },
        {
            "file": "9_3_1_java.md",
            "title": "# 9.3.1 Persistent data structures in Java",
            "extract_method": "section_header",
            "start_header": "9.3.1 Persistent data structures in Java",
            "end_header": "9.3.2 Persistent data structures in JavaScript"
        },
        {
            "file": "9_3_2_javascript.md",
            "title": "# 9.3.2 Persistent data structures in JavaScript",
            "extract_method": "section_header",
            "start_header": "9.3.2 Persistent data structures in JavaScript",
            "end_header": "9.4 Persistent data structures in action"
        },
        {
            "file": "9_4_0_introduction.md", 
            "title": "# 9.4.0 Introduction (사용자 추가)",
            "extract_method": "section_header",
            "start_header": "9.4 Persistent data structures in action",
            "end_header": "9.4.1 Writing queries with persistent data structures"
        },
        {
            "file": "9_4_1_queries.md",
            "title": "# 9.4.1 Writing queries with persistent data structures",
            "extract_method": "section_header",
            "start_header": "9.4.1 Writing queries with persistent data structures",
            "end_header": "9.4.2 Writing mutations with persistent data structures"
        },
        {
            "file": "9_4_2_mutations.md",
            "title": "# 9.4.2 Writing mutations with persistent data structures",
            "extract_method": "section_header",
            "start_header": "9.4.2 Writing mutations with persistent data structures",
            "end_header": "9.4.3 Serialization and deserialization"
        },
        {
            "file": "9_4_3_serialization.md",
            "title": "# 9.4.3 Serialization and deserialization",
            "extract_method": "section_header",
            "start_header": "9.4.3 Serialization and deserialization",
            "end_header": "9.4.4 Structural diff"
        },
        {
            "file": "9_4_4_structural_diff.md",
            "title": "# 9.4.4 Structural diff",
            "extract_method": "section_header",
            "start_header": "9.4.4 Structural diff",
            "end_header": "Summary"
        },
        {
            "file": "9_summary.md",
            "title": "# Chapter 9 Summary",
            "extract_method": "summary", 
            "chapter_num": 9
        },
        
        # Chapter 10 - Database operations
        {
            "file": "10_0_introduction.md",
            "title": "# 10.0 Introduction (사용자 추가)",
            "extract_method": "section_header",
            "start_header": "10 Database operations",
            "end_header": "10.1 Fetching data from the database"
        },
        {
            "file": "10_1_fetching_data.md",
            "title": "# 10.1 Fetching data from the database",
            "extract_method": "section_header",
            "start_header": "10.1 Fetching data from the database",
            "end_header": "10.2 Storing data in the database"
        },
        {
            "file": "10_2_storing_data.md",
            "title": "# 10.2 Storing data in the database",
            "extract_method": "section_header",
            "start_header": "10.2 Storing data in the database",
            "end_header": "10.3 Simple data manipulation"
        },
        {
            "file": "10_3_simple_manipulation.md",
            "title": "# 10.3 Simple data manipulation",
            "extract_method": "section_header",
            "start_header": "10.3 Simple data manipulation",
            "end_header": "10.4 Advanced data manipulation"
        },
        {
            "file": "10_4_advanced_manipulation.md",
            "title": "# 10.4 Advanced data manipulation",
            "extract_method": "section_header",
            "start_header": "10.4 Advanced data manipulation",
            "end_header": "Summary"
        },
        {
            "file": "10_summary.md",
            "title": "# Chapter 10 Summary",
            "extract_method": "summary",
            "chapter_num": 10
        },
        
        # Chapter 11 - Web services
        {
            "file": "11_0_introduction.md",
            "title": "# 11.0 Introduction (사용자 추가)",
            "extract_method": "section_header",
            "start_header": "11 Web services",
            "end_header": "11.1 Another feature request"
        },
        {
            "file": "11_1_feature_request.md",
            "title": "# 11.1 Another feature request",
            "extract_method": "section_header",
            "start_header": "11.1 Another feature request",
            "end_header": "11.2 Building the insides like the outsides"
        },
        {
            "file": "11_2_building_insides.md",
            "title": "# 11.2 Building the insides like the outsides",
            "extract_method": "section_header", 
            "start_header": "11.2 Building the insides like the outsides",
            "end_header": "11.3 Representing a client request as a map"
        },
        {
            "file": "11_3_client_request.md",
            "title": "# 11.3 Representing a client request as a map",
            "extract_method": "section_header",
            "start_header": "11.3 Representing a client request as a map",
            "end_header": "11.4 Representing a server response as a map"
        },
        {
            "file": "11_4_server_response.md",
            "title": "# 11.4 Representing a server response as a map",
            "extract_method": "section_header",
            "start_header": "11.4 Representing a server response as a map",
            "end_header": "11.5 Passing information forward"
        },
        {
            "file": "11_5_passing_information.md",
            "title": "# 11.5 Passing information forward",
            "extract_method": "section_header",
            "start_header": "11.5 Passing information forward",
            "end_header": "11.6 Search result enrichment in action"
        },
        {
            "file": "11_6_search_enrichment.md",
            "title": "# 11.6 Search result enrichment in action",
            "extract_method": "section_header",
            "start_header": "11.6 Search result enrichment in action",
            "end_header": "Delivering on time"
        },
        {
            "file": "11_delivering_on_time.md",
            "title": "# Delivering on time",
            "extract_method": "section_header",
            "start_header": "Delivering on time",
            "end_header": "Summary"
        },
        {
            "file": "11_summary.md",
            "title": "# Chapter 11 Summary", 
            "extract_method": "summary",
            "chapter_num": 11
        }
    ]
    
    # 각 리프노드별로 파일 생성
    created_files = 0
    failed_files = 0
    
    for section in leaf_sections:
        try:
            content = ""
            
            # 추출 방법에 따른 내용 추출
            if section["extract_method"] == "page_range":
                start_page = section["start_page"]
                end_page = section.get("end_page")
                content = extract_content_by_page_markers(part2_content, start_page, end_page)
                
            elif section["extract_method"] == "section_header":
                start_header = section["start_header"]
                end_header = section.get("end_header")
                content = extract_content_by_section_headers(part2_content, start_header, end_header)
                
            elif section["extract_method"] == "summary":
                chapter_num = section["chapter_num"]
                content = extract_summary_content(part2_content, chapter_num)
            
            if content:
                full_content = f"{section['title']}\n\n{content}"
                
                file_path = os.path.join(output_dir, section["file"])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                print(f"✅ Created: {section['file']} ({len(content)} chars)")
                created_files += 1
            else:
                description = section.get("description", "")
                print(f"⚠️  No content found for: {section['file']} {description}")
                failed_files += 1
                
        except Exception as e:
            print(f"❌ Error creating {section['file']}: {e}")
            failed_files += 1
    
    print(f"\n🎯 Part 2 Extraction Complete (v2)!")
    print(f"📁 Output directory: {output_dir}")
    print(f"✅ Successfully created: {created_files} files")
    print(f"❌ Failed: {failed_files} files")
    print(f"\n📋 Compare with v1 results in: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/part2_leafnodes/")

def main():
    if len(sys.argv) != 3:
        print("Usage: python part2_leaf_extractor_v2.py <part2_file_path> <toc_json_path>")
        print("Example: python part2_leaf_extractor_v2.py /path/to/Part_02_Part_2_Scalability.md /path/to/toc_with_page_ranges_v2.json")
        sys.exit(1)
    
    part2_file_path = sys.argv[1]
    toc_file_path = sys.argv[2]
    
    if not os.path.exists(part2_file_path):
        print(f"❌ Error: Part 2 file does not exist - {part2_file_path}")
        sys.exit(1)
        
    if not os.path.exists(toc_file_path):
        print(f"❌ Error: TOC JSON file does not exist - {toc_file_path}")
        sys.exit(1)
    
    print(f"🚀 Starting Part 2 leaf node extraction (v2)...")
    print(f"📄 Source file: {part2_file_path}")
    print(f"📋 TOC reference: {toc_file_path}")
    
    extract_part2_leaf_nodes_v2(part2_file_path, toc_file_path)

if __name__ == "__main__":
    main()