#!/usr/bin/env python3
"""
Script to populate start_text and end_text fields in JSON file based on markdown content.
This script analyzes the markdown file to find section boundaries for each title.
"""

import json
import re
from pathlib import Path

def find_section_boundaries(markdown_content, title):
    """
    Find the start and end text for a section based on its title.
    Returns tuple of (start_text, end_text)
    """
    lines = markdown_content.split('\n')
    
    # Clean the title for matching (remove level numbers like "7.1", "7.2", etc.)
    clean_title = title
    if re.match(r'^\d+(\.\d+)?\s+', title):
        clean_title = re.sub(r'^\d+(\.\d+)?\s+', '', title)
    
    start_text = ""
    end_text = ""
    
    # Special handling for "7 Introduction" - look for chapter start
    if title.startswith('7 ') and 'Introduction' in title:
        # Find the chapter start
        for i, line in enumerate(lines):
            if 'Basic data validation' in line and not line.startswith('=== '):
                title_line_idx = i
                break
    else:
        # Find the line that contains this title
        title_line_idx = None
        for i, line in enumerate(lines):
            # Look for exact title match or title as a heading
            if (clean_title.lower() in line.lower() and 
                (line.strip().startswith('#') or 
                 line.strip() == clean_title or
                 clean_title in line)):
                title_line_idx = i
                break
        
        if title_line_idx is None:
            # Try alternative matching strategies
            for i, line in enumerate(lines):
                # Match key phrases from the title
                title_words = clean_title.lower().split()
                if len(title_words) >= 2:
                    if all(word in line.lower() for word in title_words[:2]):
                        title_line_idx = i
                        break
    
    if title_line_idx is not None:
        # Get start text (first meaningful line after title)
        for i in range(title_line_idx, min(title_line_idx + 10, len(lines))):
            line = lines[i].strip()
            if (line and 
                not line.startswith('=== ') and 
                not line.startswith('#') and
                len(line) > 10 and
                clean_title.lower() not in line.lower()):
                start_text = line[:100] + "..." if len(line) > 100 else line
                break
        
        # Find end text (look for next section or end of content)
        next_section_idx = None
        for i in range(title_line_idx + 1, len(lines)):
            line = lines[i].strip()
            # Look for next major section (starts with number)
            if (re.match(r'^\d+(\.\d+)?\s+', line) and 
                not line.lower().startswith(clean_title.lower())):
                next_section_idx = i
                break
            # Look for "Summary" section
            elif line.lower().startswith('summary'):
                next_section_idx = i
                break
        
        # Get end text (last meaningful line before next section)
        if next_section_idx:
            for i in range(next_section_idx - 1, max(title_line_idx, next_section_idx - 20), -1):
                line = lines[i].strip()
                if (line and 
                    not line.startswith('=== ') and 
                    not line.startswith('#') and
                    len(line) > 10):
                    end_text = line[:100] + "..." if len(line) > 100 else line
                    break
        else:
            # If no next section found, use last meaningful line
            for i in range(len(lines) - 1, max(0, len(lines) - 50), -1):
                line = lines[i].strip()
                if (line and 
                    not line.startswith('=== ') and 
                    len(line) > 10):
                    end_text = line[:100] + "..." if len(line) > 100 else line
                    break
    
    return start_text, end_text

def main():
    # File paths
    json_file = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes/Part2_Scalability_Chapter_07.json")
    markdown_file = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md")
    
    # Read files
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Process each element
    updated_count = 0
    for item in data:
        title = item.get('title', '')
        print(f"Processing: {title}")
        
        start_text, end_text = find_section_boundaries(markdown_content, title)
        
        if start_text or end_text:
            item['start_text'] = start_text
            item['end_text'] = end_text
            updated_count += 1
            print(f"  ✓ Found boundaries")
            print(f"    Start: {start_text[:50]}...")
            print(f"    End: {end_text[:50]}...")
        else:
            print(f"  ✗ No boundaries found")
        print()
    
    # Save updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {updated_count} out of {len(data)} items")
    print(f"Updated file saved to: {json_file}")

if __name__ == "__main__":
    main()