# 목차
# - 생성 시간: 2025-08-07 20:15:30 KST
# - 핵심 내용: Part 2 리프노드 자동 추출 스크립트
# - 상세 내용: 
#   - Part_02_Part_2_Scalability.md 파일을 인자로 받아서 파싱
#   - Part 2의 모든 리프노드를 개별 파일로 추출
#   - part2_leafnodes/ 디렉토리에 저장
# - 상태: 활성
# - 주소: part2_leaf_extractor
# - 참조: chapter1_leaf_extractor.py

#!/usr/bin/env python3
import os
import sys
import re

def extract_part2_leaf_nodes(part2_file_path):
    """Part 2의 모든 리프노드를 개별 파일로 추출"""
    
    # 출력 디렉토리 생성
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/part2_leafnodes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Part 2 파일 읽기
    try:
        with open(part2_file_path, 'r', encoding='utf-8') as f:
            part2_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found - {part2_file_path}")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # Part 2 리프노드 정의 (목차 구조 기반)
    leaf_sections = [
        {
            "file": "part2_0_introduction.md",
            "title": "# Part2 Introduction (사용자 추가)",
            "chapter_marker": "## 페이지 165",
            "content_start": "Part 2\nScalability",
            "next_chapter_marker": "7 Basic data validation"
        },
        # Chapter 7 - Basic data validation
        {
            "file": "7_0_introduction.md",
            "title": "# 7.0 Introduction (사용자 추가)",
            "chapter_marker": "7 Basic data validation",
            "content_start": "7 Basic data validation",
            "section_end": "7.1 Data validation in DOP"
        },
        {
            "file": "7_1_data_validation_dop.md", 
            "title": "# 7.1 Data validation in DOP",
            "section_start": "7.1 Data validation in DOP",
            "section_end": "7.2 JSON Schema in a nutshell"
        },
        {
            "file": "7_2_json_schema.md",
            "title": "# 7.2 JSON Schema in a nutshell", 
            "section_start": "7.2 JSON Schema in a nutshell",
            "section_end": "7.3 Schema flexibility and strictness"
        },
        {
            "file": "7_3_schema_flexibility.md",
            "title": "# 7.3 Schema flexibility and strictness",
            "section_start": "7.3 Schema flexibility and strictness", 
            "section_end": "7.4 Schema composition"
        },
        {
            "file": "7_4_schema_composition.md",
            "title": "# 7.4 Schema composition",
            "section_start": "7.4 Schema composition",
            "section_end": "7.5 Details about data validation failures"
        },
        {
            "file": "7_5_validation_failures.md",
            "title": "# 7.5 Details about data validation failures",
            "section_start": "7.5 Details about data validation failures",
            "next_chapter_marker": "8 Advanced concurrency control"
        },
        {
            "file": "7_summary.md",
            "title": "# Chapter 7 Summary",
            "summary_chapter": 7,
            "next_chapter_marker": "8 Advanced concurrency control"
        },
        
        # Chapter 8 - Advanced concurrency control
        {
            "file": "8_0_introduction.md",
            "title": "# 8.0 Introduction (사용자 추가)", 
            "chapter_marker": "8 Advanced concurrency control",
            "content_start": "8 Advanced concurrency control",
            "section_end": "8.1 The complexity of locks"
        },
        {
            "file": "8_1_complexity_locks.md",
            "title": "# 8.1 The complexity of locks",
            "section_start": "8.1 The complexity of locks",
            "section_end": "8.2 Thread-safe counter with atoms"
        },
        {
            "file": "8_2_thread_safe_counter.md",
            "title": "# 8.2 Thread-safe counter with atoms",
            "section_start": "8.2 Thread-safe counter with atoms",
            "section_end": "8.3 Thread-safe cache with atoms"
        },
        {
            "file": "8_3_thread_safe_cache.md", 
            "title": "# 8.3 Thread-safe cache with atoms",
            "section_start": "8.3 Thread-safe cache with atoms",
            "section_end": "8.4 State management with atoms"
        },
        {
            "file": "8_4_state_management_atoms.md",
            "title": "# 8.4 State management with atoms",
            "section_start": "8.4 State management with atoms",
            "next_chapter_marker": "9 Persistent data structures"
        },
        {
            "file": "8_summary.md", 
            "title": "# Chapter 8 Summary",
            "summary_chapter": 8,
            "next_chapter_marker": "9 Persistent data structures"
        },
        
        # Chapter 9 - Persistent data structures  
        {
            "file": "9_0_introduction.md",
            "title": "# 9.0 Introduction (사용자 추가)",
            "chapter_marker": "9 Persistent data structures",
            "content_start": "9 Persistent data structures", 
            "section_end": "9.1 The need for persistent data structures"
        },
        {
            "file": "9_1_need_persistent.md",
            "title": "# 9.1 The need for persistent data structures",
            "section_start": "9.1 The need for persistent data structures",
            "section_end": "9.2 The efficiency of persistent data structures"
        },
        {
            "file": "9_2_efficiency_persistent.md",
            "title": "# 9.2 The efficiency of persistent data structures", 
            "section_start": "9.2 The efficiency of persistent data structures",
            "section_end": "9.3 Persistent data structures libraries"
        },
        {
            "file": "9_3_0_introduction.md",
            "title": "# 9.3.0 Introduction (사용자 추가)",
            "section_start": "9.3 Persistent data structures libraries",
            "section_end": "9.3.1 Persistent data structures in Java"
        },
        {
            "file": "9_3_1_java.md",
            "title": "# 9.3.1 Persistent data structures in Java",
            "section_start": "9.3.1 Persistent data structures in Java",
            "section_end": "9.3.2 Persistent data structures in JavaScript"
        },
        {
            "file": "9_3_2_javascript.md",
            "title": "# 9.3.2 Persistent data structures in JavaScript",
            "section_start": "9.3.2 Persistent data structures in JavaScript",
            "section_end": "9.4 Persistent data structures in action"
        },
        {
            "file": "9_4_0_introduction.md",
            "title": "# 9.4.0 Introduction (사용자 추가)",
            "section_start": "9.4 Persistent data structures in action",
            "section_end": "9.4.1 Writing queries with persistent data structures"
        },
        {
            "file": "9_4_1_queries.md",
            "title": "# 9.4.1 Writing queries with persistent data structures",
            "section_start": "9.4.1 Writing queries with persistent data structures",
            "section_end": "9.4.2 Writing mutations with persistent data structures"
        },
        {
            "file": "9_4_2_mutations.md",
            "title": "# 9.4.2 Writing mutations with persistent data structures",
            "section_start": "9.4.2 Writing mutations with persistent data structures", 
            "section_end": "9.4.3 Serialization and deserialization"
        },
        {
            "file": "9_4_3_serialization.md",
            "title": "# 9.4.3 Serialization and deserialization",
            "section_start": "9.4.3 Serialization and deserialization",
            "section_end": "9.4.4 Structural diff"
        },
        {
            "file": "9_4_4_structural_diff.md", 
            "title": "# 9.4.4 Structural diff",
            "section_start": "9.4.4 Structural diff",
            "next_chapter_marker": "10 Database operations"
        },
        {
            "file": "9_summary.md",
            "title": "# Chapter 9 Summary",
            "summary_chapter": 9,
            "next_chapter_marker": "10 Database operations"
        },
        
        # Chapter 10 - Database operations
        {
            "file": "10_0_introduction.md",
            "title": "# 10.0 Introduction (사용자 추가)",
            "chapter_marker": "10 Database operations",
            "content_start": "10 Database operations",
            "section_end": "10.1 Fetching data from the database"
        },
        {
            "file": "10_1_fetching_data.md",
            "title": "# 10.1 Fetching data from the database",
            "section_start": "10.1 Fetching data from the database",
            "section_end": "10.2 Storing data in the database"
        },
        {
            "file": "10_2_storing_data.md",
            "title": "# 10.2 Storing data in the database",
            "section_start": "10.2 Storing data in the database",
            "section_end": "10.3 Simple data manipulation"
        },
        {
            "file": "10_3_simple_manipulation.md",
            "title": "# 10.3 Simple data manipulation",
            "section_start": "10.3 Simple data manipulation",
            "section_end": "10.4 Advanced data manipulation"
        },
        {
            "file": "10_4_advanced_manipulation.md",
            "title": "# 10.4 Advanced data manipulation",
            "section_start": "10.4 Advanced data manipulation", 
            "next_chapter_marker": "11 Web services"
        },
        {
            "file": "10_summary.md",
            "title": "# Chapter 10 Summary", 
            "summary_chapter": 10,
            "next_chapter_marker": "11 Web services"
        },
        
        # Chapter 11 - Web services
        {
            "file": "11_0_introduction.md",
            "title": "# 11.0 Introduction (사용자 추가)",
            "chapter_marker": "11 Web services",
            "content_start": "11 Web services",
            "section_end": "11.1 Another feature request"
        },
        {
            "file": "11_1_feature_request.md",
            "title": "# 11.1 Another feature request", 
            "section_start": "11.1 Another feature request",
            "section_end": "11.2 Building the insides like the outsides"
        },
        {
            "file": "11_2_building_insides.md",
            "title": "# 11.2 Building the insides like the outsides",
            "section_start": "11.2 Building the insides like the outsides",
            "section_end": "11.3 Representing a client request as a map"
        },
        {
            "file": "11_3_client_request.md",
            "title": "# 11.3 Representing a client request as a map",
            "section_start": "11.3 Representing a client request as a map",
            "section_end": "11.4 Representing a server response as a map"
        },
        {
            "file": "11_4_server_response.md",
            "title": "# 11.4 Representing a server response as a map",
            "section_start": "11.4 Representing a server response as a map",
            "section_end": "11.5 Passing information forward"
        },
        {
            "file": "11_5_passing_information.md",
            "title": "# 11.5 Passing information forward",
            "section_start": "11.5 Passing information forward",
            "section_end": "11.6 Search result enrichment in action"
        },
        {
            "file": "11_6_search_enrichment.md", 
            "title": "# 11.6 Search result enrichment in action",
            "section_start": "11.6 Search result enrichment in action",
            "section_end": "Delivering on time"
        },
        {
            "file": "11_delivering_on_time.md",
            "title": "# Delivering on time",
            "section_start": "Delivering on time",
            "end_of_part": True
        },
        {
            "file": "11_summary.md",
            "title": "# Chapter 11 Summary",
            "summary_chapter": 11,
            "end_of_part": True
        }
    ]
    
    def find_content_between_markers(text, start_marker, end_marker=None, next_chapter=None, is_summary=False):
        """마커 사이의 내용을 찾아서 반환"""
        if is_summary:
            # Summary 섹션 찾기
            summary_pattern = rf"Summary.*?(?=(?:\d+ \w+|\Z))"
            matches = re.search(summary_pattern, text, re.DOTALL | re.MULTILINE)
            if matches:
                return matches.group(0).strip()
            return ""
        
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return ""
        
        if end_marker:
            end_idx = text.find(end_marker, start_idx + len(start_marker))
        elif next_chapter:
            end_idx = text.find(next_chapter, start_idx + len(start_marker))
        else:
            end_idx = len(text)
        
        if end_idx == -1:
            end_idx = len(text)
            
        content = text[start_idx:end_idx].strip()
        # 시작 마커 제거
        if content.startswith(start_marker):
            content = content[len(start_marker):].strip()
            
        return content
    
    # 각 리프노드별로 파일 생성
    created_files = 0
    failed_files = 0
    
    for section in leaf_sections:
        try:
            content = ""
            
            # Summary 처리
            if "summary_chapter" in section:
                # Chapter summary 찾기 
                chapter_num = section["summary_chapter"]
                summary_pattern = rf"(Summary.*?)(?=\d+ \w+|Part \d+|\Z)"
                
                # 해당 챕터 이후의 Summary 찾기
                chapter_pattern = rf"{chapter_num} \w+"
                chapter_match = re.search(chapter_pattern, part2_content)
                if chapter_match:
                    search_start = chapter_match.end()
                    remaining_text = part2_content[search_start:]
                    summary_match = re.search(summary_pattern, remaining_text, re.DOTALL | re.MULTILINE)
                    if summary_match:
                        content = summary_match.group(1).strip()
                        
            # Part Introduction 처리
            elif "part2_0_introduction" in section["file"]:
                start_idx = part2_content.find("Part 2\nScalability")
                if start_idx != -1:
                    # 7장 시작까지 찾기
                    end_pattern = r"7\s+Basic data validation"
                    end_match = re.search(end_pattern, part2_content[start_idx:])
                    if end_match:
                        content = part2_content[start_idx:start_idx + end_match.start()].strip()
                        
            # 일반 섹션 처리
            else:
                if "content_start" in section:
                    start_marker = section["content_start"]
                elif "section_start" in section:
                    start_marker = section["section_start"]
                else:
                    continue
                    
                end_marker = section.get("section_end")
                next_chapter = section.get("next_chapter_marker")
                
                content = find_content_between_markers(
                    part2_content, 
                    start_marker, 
                    end_marker, 
                    next_chapter
                )
            
            if content:
                full_content = f"{section['title']}\n\n{content}"
                
                file_path = os.path.join(output_dir, section["file"])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                print(f"✅ Created: {section['file']}")
                created_files += 1
            else:
                print(f"⚠️  No content found for: {section['file']}")
                failed_files += 1
                
        except Exception as e:
            print(f"❌ Error creating {section['file']}: {e}")
            failed_files += 1
    
    print(f"\n🎯 Part 2 Extraction Complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"✅ Successfully created: {created_files} files")
    print(f"❌ Failed: {failed_files} files")

def main():
    if len(sys.argv) != 2:
        print("Usage: python part2_leaf_extractor.py <part2_file_path>")
        print("Example: python part2_leaf_extractor.py /path/to/Part_02_Part_2_Scalability.md")
        sys.exit(1)
    
    part2_file_path = sys.argv[1]
    
    if not os.path.exists(part2_file_path):
        print(f"❌ Error: File does not exist - {part2_file_path}")
        sys.exit(1)
    
    print(f"🚀 Starting Part 2 leaf node extraction...")
    print(f"📄 Source file: {part2_file_path}")
    
    extract_part2_leaf_nodes(part2_file_path)

if __name__ == "__main__":
    main()