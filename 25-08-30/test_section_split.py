#!/usr/bin/env python3

# 섹션 분할 테스트 스크립트
content = """# 속성
---
process_status: false
source: 2022_Data-Oriented Programming_Manning.pdf
source_type: book
source_language: english
structure_type: component
content_processing: unified
title: Data-Oriented Programming
folder_name: 
created_at: 2025-08-28T11:43:31.980838

# 추출
---

## 핵심 내용

## 상세 핵심 내용

## 상세 내용

## 주요 화제

## 부차 화제

# 내용
---
### 1.1.1 The design phase
"""

# 현재 로직 시뮬레이션
section_name = "핵심 내용"
section_header = f"## {section_name}"
section_start = content.find(section_header)

print(f"section_header: {repr(section_header)}")
print(f"section_start: {section_start}")

header_end = content.find('\n', section_start)
if header_end == -1:
    header_end = len(content)
content_start = header_end + 1

print(f"header_end: {header_end}")
print(f"content_start: {content_start}")

print(f"\ncontent[:content_start] 내용:")
print(repr(content[:content_start]))

print(f"\ncontent[content_start:] 시작 부분:")
print(repr(content[content_start:content_start+50]))